import requests

# from tenacity import retry, wait_exponential


# @retry(wait=wait_exponential(multiplier=1, min=4, max=20))
def requests_get_content(uri, timeout=10):
    response = requests.get(uri, timeout=timeout)
    return response.content.decode("utf-8")


# @retry(wait=wait_exponential(multiplier=1, min=4, max=20))
def requests_get(uri, timeout=10):
    response = requests.get(uri, timeout=timeout)
    return response.content
