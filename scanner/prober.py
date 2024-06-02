import requests

def send_request(target_url, request_data=None, form_data=None, custom_headers=None, user_agent=None):
    try:
        headers = {"User-Agent": user_agent} if user_agent else {}
        if custom_headers:
            headers.update(custom_headers)
        
        if form_data is not None:
            response = requests.post(target_url, data=form_data, headers=headers)
        elif request_data is not None:
            response = requests.get(target_url, params=request_data, headers=headers)
        else:
            response = requests.get(target_url, headers=headers)
        return response.text
    except Exception as e:
        print(f"[!] Error occurred while sending request: {e}")
        return None
