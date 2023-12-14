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


class ValidationArticleAndSubArticlesLanguageCodeException(Exception):
    ...


class ValidationArticleAndSubArticlesSpecificUseException(Exception):
    ...


class ValidationArticleAndSubArticlesDtdVersionException(Exception):
    ...


class ValidationArticleAndSubArticlesArticleTypeException(Exception):
    ...


class ValidationArticleAndSubArticlesSubjectsException(Exception):
    ...


class ValidationRelatedArticleException(Exception):
    ...


class ValidationLicenseException(Exception):
    ...


class ValidationLicenseCodeException(Exception):
    ...