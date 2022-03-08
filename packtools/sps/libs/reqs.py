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


def _handle_http_error(status_code):
    if status_code == 403:
        raise exceptions.SPSHTTPForbiddenError()
    elif status_code == 404:
        raise exceptions.SPSHTTPResourceNotFoundError()
    elif status_code == 500:
        raise exceptions.SPSHTTPInternalServerError()
    elif status_code == 502:
        raise exceptions.SPSHTTPBadGatewayError()
    elif status_code == 503:
        raise exceptions.SPSHTTPServiceUnavailableError()
    else:
        raise exceptions.SPSHTTPError(f'{status_code}')
