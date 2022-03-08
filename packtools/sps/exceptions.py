class NotAllowedtoChangeAttributeValueError(Exception):
    """ To handle improperly attribute change attempts.
    """


class InvalidAttributeValueError(Exception):
    """ To handle invalid attribute values.
    """


class InvalidValueForOrderError(Exception):
    """ To handle invalid order values.
    """


class SPSLoadToXMLError(Exception):
    """ Generic error during SPS Package loading.
    """


class SHA1Error(Exception):
    """ To handle invalid SHA1 value.
    """


class SPSConnectionError(Exception):
    """ To handle connection errors.
    """


class SPSHTTPError(Exception):
    """ To handle HTTP errors.
    """


class SPSHTTPForbiddenError(Exception):
    """ To handle forbidden request errors.
    """


class SPSHTTPResourceNotFoundError(Exception):
    """ To handle resource not found errors.
    """


class SPSHTTPInternalServerError(Exception):
    """ To handle internal server errors.
    """


class SPSHTTPBadGatewayError(Exception):
    """ To handle bad gateway errors.
    """


class SPSHTTPServiceUnavailableError(Exception):
    """ To handle service unavailable errors.
    """


class SPSDownloadXMLError(Exception):
    """ To handle XML file download failures.
    """


class SPSXMLLinkError(Exception):
    """ To handle invalid XML links.
    """


class SPSXMLContentError(Exception):
    """ To handle invalid XML content.
    """


class SPSXMLFileError(Exception):
    """ To handle invalid XML files.
    """


class SPSAssetOrRenditionFileError(Exception):
    """ To handle invalid Asset or Rendition files.
    """


class SPSMakePackageFromPathsMissingKeyError(Exception):
    """ To handle missing paths.
    """
