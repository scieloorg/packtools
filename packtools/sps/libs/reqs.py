import requests


def requests_get_content(uri, timeout=10):
    response = requests.get(uri, timeout=timeout)
    if response.status_code == 200:
        return response.content.decode("utf-8")


def requests_get(uri, timeout=10):
    response = requests.get(uri, timeout=timeout)
    if response.status_code == 200:    
        return response.content
