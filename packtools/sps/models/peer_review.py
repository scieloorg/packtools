from packtools.sps.models.article_and_subarticles import Fulltext
from packtools.sps.models.article_contribs import Contrib
from packtools.sps.models.article_license import License
from packtools.sps.models.dates import FulltextDates
from packtools.sps.models.related_articles import FulltextRelatedArticles


import warnings as _warnings


def __getattr__(name):
    _moved = {
        "PeerReview": "packtools.sps.validation.models.peer_review",
        "CustomMeta": "packtools.sps.validation.models.peer_review",
    }
    if name in _moved:
        import importlib
        _warnings.warn(
            f"{name} has moved to {_moved[name]}. "
            f"Importing from packtools.sps.models.peer_review is deprecated.",
            DeprecationWarning,
            stacklevel=2,
        )
        mod = importlib.import_module(_moved[name])
        return getattr(mod, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
