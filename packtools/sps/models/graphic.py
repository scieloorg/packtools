from packtools.sps.models.visual_resource_base import (
    VisualResourceBase,
    XmlVisualResource,
)


class Graphic(VisualResourceBase):
    pass


class InlineGraphic(Graphic):
    pass


import warnings as _warnings


def __getattr__(name):
    _moved = {
        "XmlGraphic": "packtools.sps.validation.models.graphic",
    }
    if name in _moved:
        import importlib
        _warnings.warn(
            f"{name} has moved to {_moved[name]}. "
            f"Importing from packtools.sps.models.graphic is deprecated.",
            DeprecationWarning,
            stacklevel=2,
        )
        mod = importlib.import_module(_moved[name])
        return getattr(mod, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
