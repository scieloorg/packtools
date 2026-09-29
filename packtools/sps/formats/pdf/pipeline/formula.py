"""Módulo de compatibilidade: a conversão MathML -> OMML foi para ooxml/formula.py."""

import importlib
import warnings

_MOVED = {
    'normalize_empty_base_superscripts': 'packtools.sps.formats.pdf.ooxml.formula',
    'match_paragraph_font': 'packtools.sps.formats.pdf.ooxml.formula',
    'mathml_to_omml': 'packtools.sps.formats.pdf.ooxml.formula',
}


def __getattr__(name):
    if name in _MOVED:
        warnings.warn(
            f"{name} has moved to {_MOVED[name]}. "
            f"Importing from packtools.sps.formats.pdf.pipeline.formula is deprecated.",
            DeprecationWarning,
            stacklevel=2,
        )
        return getattr(importlib.import_module(_MOVED[name]), name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
