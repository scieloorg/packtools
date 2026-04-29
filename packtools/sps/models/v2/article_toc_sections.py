from packtools.sps.models.article_and_subarticles import Fulltext
from packtools.sps.utils.xml_utils import node_text_without_fn_xref


import warnings as _warnings


def __getattr__(name):
    _moved = {
        "ArticleTocSections": "packtools.sps.validation.models.article_toc_sections",
    }
    if name in _moved:
        import importlib
        _warnings.warn(
            f"{name} has moved to {_moved[name]}. "
            f"Importing from packtools.sps.models.v2.article_toc_sections is deprecated.",
            DeprecationWarning,
            stacklevel=2,
        )
        mod = importlib.import_module(_moved[name])
        return getattr(mod, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
