from scanner.prober import send_request
from utils.parser import parse_html

def test_reflections(target_url, headers=None):
    # Send HTTP request
    response_text = send_request(target_url, custom_headers=headers)
    if not response_text:
        return None, [], None, None

    # Parse the HTML content of the response
    soup = parse_html(response_text)

    # Find the form element in the HTML response
    form = soup.find("form")
    if not form:
        print("[-] No injection points were found in the HTML response.")
        print("[-] URL not vulnerable to reflected XSS.")
        return response_text, [], None, None

    # Extract the form method
    form_method = form.get("method")

    # Initialize request data
    request_data = None
    form_data = None

    # If form method is GET, construct request data
    if form_method == "get" or form_method == "GET":
        # Extract input field names and values
        form_inputs = form.find_all("input")
        request_data = {}
        for input_field in form_inputs:
            input_name = input_field.get("name")
            input_value = input_field.get("value", "jam")
            if input_name:
                request_data[input_name] = input_value

    # If form method is POST, construct form data
    elif form_method == "post" or form_method == "POST":
        # Extract input field names
        form_inputs = form.find_all("input")
        form_data = {}
        for input_field in form_inputs:
            input_name = input_field.get("name")
            if input_name:
                form_data[input_name] = "jam"

    # Send HTTP request with the appropriate request type
    response_text_with_payload = send_request(target_url, request_data=request_data, form_data=form_data, custom_headers=headers)

    # Check for reflections in the response
    reflections = []

    # Check for reflections in request data
    if request_data:
        for param, value in request_data.items():
            if value in response_text_with_payload:
                reflections.append((param, value))

    # Check for reflections in form data
    if form_data:
        for param, value in form_data.items():
            if value in response_text_with_payload:
                reflections.append((param, value))

    # Print reflections found
    if reflections:
        print("[+] Reflections found:")
        for param, payload in reflections:
            print(f"[+] Parameter: {param}, Payload: {payload}")
    else:
        print("[-] No reflections were found in the HTML response.")
        print("[-] URL not vulnerable to reflected XSS.")

    return response_text_with_payload, reflections, request_data, form_data
