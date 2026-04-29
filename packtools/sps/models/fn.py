from packtools.sps.models.basenotes import BaseNoteGroup, BaseNoteGroups, Fn
from packtools.sps.models.article_and_subarticles import Fulltext


class FnGroup(BaseNoteGroup):

    @property
    def label(self):
        return self.fn_parent_node.findtext("label")

    @property
    def title(self):
        return self.fn_parent_node.findtext("title")

    @property
    def data(self):
        return {
            "label": self.label,
            "title": self.title,
            "fns": list(self.items),
        }


class FulltextFnGroups(BaseNoteGroups):
    def __init__(self, node):
        super().__init__(node, "fn-group", FnGroup)


import warnings as _warnings


def __getattr__(name):
    _moved = {
        "XMLFns": "packtools.sps.validation.models.fn",
    }
    if name in _moved:
        import importlib
        _warnings.warn(
            f"{name} has moved to {_moved[name]}. "
            f"Importing from packtools.sps.models.fn is deprecated.",
            DeprecationWarning,
            stacklevel=2,
        )
        mod = importlib.import_module(_moved[name])
        return getattr(mod, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
