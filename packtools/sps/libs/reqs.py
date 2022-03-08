from packtools.sps import exceptions

import requests


def requests_get_content(uri, timeout=10):
    try:
        response = requests.get(uri, timeout=timeout)
        response.raise_for_status()
    except requests.exceptions.HTTPError:
        _handle_http_error(response.status_code)
    except requests.exceptions.ConnectionError:
        raise exceptions.SPSConnectionError()
    else:
        return response.content.decode("utf-8")


def requests_get(uri, timeout=10):
    try:
        response = requests.get(uri, timeout=timeout)
        response.raise_for_status()
    except requests.exceptions.HTTPError:
        _handle_http_error(response.status_code)
    except requests.exceptions.ConnectionError:
        raise exceptions.SPSConnectionError()
    else:
        return response.content
