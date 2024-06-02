from urllib.parse import urlparse
from bs4 import BeautifulSoup
import warnings

def parse_url(url):
    parsed_url = urlparse(url)
    components = {
        "scheme": parsed_url.scheme,
        "domain": parsed_url.netloc,
        "path": parsed_url.path,
        "query": parsed_url.query,
        "params": parsed_url.params,
        "fragment": parsed_url.fragment
    }
    return components

def parse_html(html_content):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=UserWarning)  # Suppress the warning
        return BeautifulSoup(html_content, 'html.parser')

def parse_http_headers(http_headers):
    headers_dict = {}
    for header in http_headers.split('\n'):
        if ':' in header:
            key, value = header.split(':', 1)
            headers_dict[key.strip()] = value.strip()
    return headers_dict
