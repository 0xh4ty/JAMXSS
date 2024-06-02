import requests
from lxml.html import fromstring
from urllib.parse import urljoin, urlparse
import queue

def crawl_and_collect_links(base_url):
    visited = set()
    failed = set()
    urls_to_visit = queue.Queue()
    urls_in_queue = set()  # Set to keep track of URLs already in the queue

    urls_to_visit.put(base_url)
    urls_in_queue.add(base_url)

    base_domain = urlparse(base_url).netloc

    while not urls_to_visit.empty():
        current_url = urls_to_visit.get()
        urls_in_queue.remove(current_url)  # Remove URL from the queue set

        if current_url in visited or current_url in failed:
            continue

        try:
            response = requests.get(current_url)
            response.raise_for_status()  # Raise an HTTPError on bad status
            visited.add(current_url)
            parser = fromstring(response.text)

            # Extract and queue up all links on the current page
            for element in parser.xpath('//a[@href]'):
                link = element.get('href')
                if not link:
                    continue

                # Resolve relative URLs
                full_url = urljoin(current_url, link)
                full_domain = urlparse(full_url).netloc

                # Ensure the link is within the same domain
                if full_domain == base_domain and full_url not in visited and full_url not in urls_in_queue:
                    urls_to_visit.put(full_url)
                    urls_in_queue.add(full_url)
                    
            yield current_url

        except requests.exceptions.RequestException as e:
            failed.add(current_url)  # Add to failed set to avoid retrying
