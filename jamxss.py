import argparse
import sys
import os
import time
from lxml import html
import concurrent.futures
import queue
from urllib.parse import urlparse
import threading
import signal
import shutil
from collections import Counter

# Add the project's root directory to the Python path
current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)

from crawler.crawler import crawl_and_collect_links
from utils.parser import parse_url
from scanner.reflections import test_reflections
from banner import display_banner
from utils.context_analyzer_ml import predict_contexts_for_reflections, train_model
from utils.payload_generator import payload_generator
from scanner.prober import send_request

def print_separator():
    terminal_width = shutil.get_terminal_size((80, 20)).columns
    separator = '-' * (terminal_width // 3) + ' JAMXSS ' + '-' * (terminal_width // 3)
    if len(separator) > terminal_width:
        separator = separator[:terminal_width]
    print(separator)

def print_sub_separator():
    terminal_width = shutil.get_terminal_size((80, 20)).columns
    separator = '-' * (terminal_width // 3)
    if len(separator) > terminal_width:
        separator = separator[:terminal_width]
    print(separator)

def get_majority_context(contexts):
    context_counter = Counter(contexts)
    majority_context = context_counter.most_common(1)[0][0]
    return majority_context

def scanner_task(url_queue, stop_event, single_scan, stealth_mode, attack_mode, custom_cookie, user_agent):
    classifier, vectorizer = train_model()
    last_item_time = time.time()

    headers = {
        "User-Agent": user_agent
    }
    if custom_cookie:
        headers['Cookie'] = custom_cookie

    while not stop_event.is_set():
        try:
            url = url_queue.get(timeout=10)  # Wait for a URL to be available, with a timeout
            last_item_time = time.time()  # Update the last item time
            print_separator()
            print(f"[+] Testing URL: {url}")

            response_text_with_payload, reflections, request_data, form_data = test_reflections(url, headers=headers)
            
            if not response_text_with_payload or not reflections:
                if single_scan:
                    stop_event.set()
                continue
            
            html_response_lines = response_text_with_payload.split('\n')

            reflection_contexts = []
            for reflection in reflections:
                contexts = []
                for _ in range(5):
                    classifier, vectorizer = train_model()
                    context = predict_contexts_for_reflections(html_response_lines, [reflection], classifier, vectorizer)
                    contexts.append(context[0][1])
                majority_context = get_majority_context(contexts)
                reflection_contexts.append((reflection[0], majority_context))  # Extract only the parameter name

            print("[+] Reflections and Predicted Contexts:")
            for reflection, context in reflection_contexts:
                print(f"[+] Reflection Parameter: {reflection}, Predicted Context: {context}")

            whole_dict = {}

            for reflection, context in reflection_contexts:
                payload_and_find = payload_generator(context)
                whole_dict[reflection] = payload_and_find

            if stealth_mode:
                print_sub_separator()
                print("[+] Stealth-mode: Payloads suggested but not executed.")
                for key in whole_dict:
                    print(f"[+] Parameter: {key}, Suggested Payload: {whole_dict[key][0]['payload']}")
                if single_scan:
                    stop_event.set()
                continue

            if attack_mode:
                if request_data:
                    try:
                        for key in request_data:
                            if key in whole_dict:
                                request_data[key] = whole_dict[key][0]['payload']

                        response = send_request(url, request_data=request_data, form_data=form_data, custom_headers=headers)

                        if response:
                            page_html_tree = html.fromstring(response)

                            for key in whole_dict:
                                count = page_html_tree.xpath(whole_dict[key][0]['find'])

                                if len(count):
                                    print_sub_separator()
                                    print("[*] Request vulnerable for parameter:", key)
                                    print("[*] Payload executed:", whole_dict[key][0]['payload'])
                    except Exception as e:
                        print(f"[-] An error occurred: {e}")

                if form_data:
                    try:
                        for key in form_data:
                            if key in whole_dict:
                                form_data[key] = whole_dict[key][0]['payload']

                        response = send_request(url, request_data=request_data, form_data=form_data, custom_headers=headers)

                        if response:
                            page_html_tree = html.fromstring(response)

                            for key in whole_dict:
                                count = page_html_tree.xpath(whole_dict[key][0]['find'])

                                if len(count):
                                    print_sub_separator()
                                    print("[*] Request vulnerable for parameter:", key)
                                    print("[*] Payload executed:", whole_dict[key][0]['payload'])
                    except Exception as e:
                        print(f"[-] An error occurred: {e}")

            if single_scan:
                stop_event.set()

        except queue.Empty:
            if time.time() - last_item_time > 10:
                print_separator()
                print("[+] Queue is empty for more than 10 seconds.")
                stop_event.set()
            else:
                print("[+] Queue is empty, waiting for more URLs.")

def main():
    parser = argparse.ArgumentParser(description="JAMXSS (Just A Monster XSS Scanner) - A machine learning powered tool to test for reflected XSS vulnerabilities in web applications.")
    parser.add_argument("-u", "--url", help="Target URL of the web application")
    parser.add_argument("--single-scan", action="store_true", help="Perform a single scan on the provided URL only")
    parser.add_argument("--stealth-mode", action="store_true", help="Only suggest payloads without executing them")
    parser.add_argument("--attack-mode", action="store_true", help="Execute suggested payloads to test for vulnerabilities")
    parser.add_argument("--cookie", type=str, help="Custom cookie header to use for the requests")
    parser.add_argument("--user-agent", type=str, default="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36", help="Custom user agent string")
    args = parser.parse_args()

    if not args.url:
        parser.error('Please specify a target URL using the -u or --url argument.')

    if not args.stealth_mode and not args.attack_mode:
        parser.error('Please specify either --stealth-mode or --attack-mode to run the scanner.')

    if args.stealth_mode and args.attack_mode:
        parser.error('Please choose either --stealth-mode or --attack-mode, not both.')

    display_banner()

    url_queue = queue.Queue()
    stop_event = threading.Event()

    def signal_handler(sig, frame):
        print("[!] Program terminated.")
        stop_event.set()

    signal.signal(signal.SIGINT, signal_handler)

    # Start the scanner task in a separate thread
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        future = executor.submit(scanner_task, url_queue, stop_event, args.single_scan, args.stealth_mode, args.attack_mode, args.cookie, args.user_agent)

        # Start crawling and add links to the queue
        try:
            if args.single_scan:
                url_queue.put(args.url)
            else:
                for link in crawl_and_collect_links(args.url):
                    if stop_event.is_set():
                        break
                    url_queue.put(link)
                    time.sleep(0.1)  # Small sleep to simulate real-time crawling

            # Wait for the scanner task to complete or be interrupted
            future.result()
        except KeyboardInterrupt:
            stop_event.set()
            future.cancel()
            print('\n[!] Program terminated by user.')

    print('\n[*] The monster is exiting... Bye!')

if __name__ == "__main__":
    main()
