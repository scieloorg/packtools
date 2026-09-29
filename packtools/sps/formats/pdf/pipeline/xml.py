"""Módulo de compatibilidade (depreciado).

A extração do XML para o PDF foi dividida em extract/ e layout/ (ver
docs/pdf_generator_architecture.md). Os nomes públicos que ficavam aqui
continuam acessíveis por este módulo, com DeprecationWarning; nenhum módulo
de produção deve importá-lo.
"""

import importlib
import warnings

from packtools.sps.formats.pdf.extract import tables
from packtools.sps.formats.pdf.layout import table_layout

_METADATA = 'packtools.sps.formats.pdf.extract.metadata'
_FIGURES = 'packtools.sps.formats.pdf.extract.figures'
_REFERENCES = 'packtools.sps.formats.pdf.extract.references'
_ACKNOWLEDGMENTS = 'packtools.sps.formats.pdf.extract.acknowledgments'
_CITATION = 'packtools.sps.formats.pdf.extract.citation'
_TABLES = 'packtools.sps.formats.pdf.extract.tables'
_BODY = 'packtools.sps.formats.pdf.extract.body'
_MOVED = {
    'extract_article_main_language': _METADATA,
    'extract_article_type': _METADATA,
    'extract_journal_title': _METADATA,
    'extract_doi': _METADATA,
    'extract_category': _METADATA,
    'extract_article_title': _METADATA,
    'extract_contrib_data': _METADATA,
    'extract_abstract_data': _METADATA,
    'extract_trans_abstract_data': _METADATA,
    'extract_keywords_data': _METADATA,
    'extract_footer_data': _METADATA,
    'extract_figure_data': _FIGURES,
    'extract_references_data': _REFERENCES,
    'extract_acknowledgment_data': _ACKNOWLEDGMENTS,
    'extract_cite_as_part_one': _CITATION,
    'CITATION_STYLE_VANCOUVER': _CITATION,
    'build_full_citation': _CITATION,
    'extract_table_data': _TABLES,
    'extract_body_data': _BODY,
    'extract_section_data': _BODY,
}


def __getattr__(name):
    if name in _MOVED:
        warnings.warn(
            f"{name} has moved to {_MOVED[name]}. "
            f"Importing from packtools.sps.formats.pdf.pipeline.xml is deprecated.",
            DeprecationWarning,
            stacklevel=2,
        )
        return getattr(importlib.import_module(_MOVED[name]), name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def determine_table_layout(table_wrap, override=None):
    """Depreciado: use layout.table_layout.determine_table_layout, que recebe
    os dados de extract.tables.read_table_wrap em vez do <table-wrap>."""
    warnings.warn(
        "determine_table_layout has moved to packtools.sps.formats.pdf.layout.table_layout "
        "and now takes extract.tables.read_table_wrap(table_wrap). "
        "Importing from packtools.sps.formats.pdf.pipeline.xml is deprecated.",
        DeprecationWarning,
        stacklevel=2,
    )
    return table_layout.determine_table_layout(tables.read_table_wrap(table_wrap), override=override)
