import requests


def requests_get_content(uri, timeout=10):
    response = requests.get(uri, timeout=timeout)
    return response.content.decode("utf-8")


def requests_get(uri, timeout=10):
    response = requests.get(uri, timeout=timeout)
    return response.content
