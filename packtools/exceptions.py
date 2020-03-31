class PacktoolsError(Exception):
    """ The root of all evil in this lib.
    """


class XMLDoctypeError(PacktoolsError, TypeError):
    """ To handle missing or unsupported DOCTYPE definitions.
    """


class XMLSPSVersionError(PacktoolsError, ValueError):
    """ To handle missing or unsupported SPS versions.
    """


class UndefinedDTDError(PacktoolsError, TypeError):
    """ To handle validation attempts without a previously defined validator.
    """


class HTMLGenerationError(PacktoolsError):
    """ Generic errors during HTML generation phase.
    """


class SPPackageError(PacktoolsError):
    """ Generic errors during SP Package optimisation.
    """


class XMLWebOptimiserError(SPPackageError):
    """ Generic errors during XML WEB optimisation.
    """


class WebImageGeneratorError(SPPackageError):
    """ Generic errors during WEB Image optimisation.
    """
