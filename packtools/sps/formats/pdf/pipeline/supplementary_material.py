"""Módulo de compatibilidade: a extração de apêndices e material suplementar foi para extract/supplementary_material.py."""

import importlib
import warnings

_MOVED = {
    'extract_data': 'packtools.sps.formats.pdf.extract.supplementary_material',
    'extract_supplementary_items': 'packtools.sps.formats.pdf.extract.supplementary_material',
    'format_item': 'packtools.sps.formats.pdf.extract.supplementary_material',
}


def __getattr__(name):
    if name in _MOVED:
        warnings.warn(
            f"{name} has moved to {_MOVED[name]}. "
            f"Importing from packtools.sps.formats.pdf.pipeline.supplementary_material is deprecated.",
            DeprecationWarning,
            stacklevel=2,
        )
        return getattr(importlib.import_module(_MOVED[name]), name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
