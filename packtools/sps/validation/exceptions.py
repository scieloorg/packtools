class ValidationArticleDataError(Exception):
    """ The root of Article data exceptions.
    """
    def __init__(self, *args: object, message, line):
        super().__init__(*args)
        self.message = message
        self.line = line


class ValidationArticleAndSubArticlesUnavailableLanguage(ValidationArticleDataError):
    ...


class ValidationArticleAndSubArticlesHasInvalidLanguage(ValidationArticleDataError):
    ...


class AffiliationValidationValidateCountryCodeException(Exception):
    ...
