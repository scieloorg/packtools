"""
Estilos de texto (``<italic>``, ``<bold>``, ``<sup>``...) e ``<break>``.
"""

from packtools.sps.formats.pdf.extract import inline
from packtools.sps.formats.pdf.extract.registry import inline_handler
from packtools.sps.formats.pdf.extract.runs import tag


# -----------------
# Elementos de estilo: ``<italic>``, ``<bold>``, ``<sup>``, ``<sub>``,
# ``<sc>``, ``<underline>``, ``<strike>``, ``<monospace>``.
# -----------------
# Todos têm o mesmo tratamento: acrescentam um formato aos ativos e seguem o
# conteúdo. Os formatos se acumulam (``<bold><italic>x</italic></bold>`` dá
# um run negrito e itálico). Um elemento de estilo que contém blocos (ex.
# ``<bold>`` em volta de uma lista) é tratado em flow.handle_container, que
# usa a mesma tabela FORMATS.


# tag -> formato do run (ver runs.FLAGS)
FORMATS = {
    "italic": "italic",
    "bold": "bold",
    "sup": "superscript",
    "sub": "subscript",
    "sc": "small_caps",
    "underline": "underline",
    "strike": "strike",
    "monospace": "monospace",
}


@inline_handler(*FORMATS)
def handle_style(node, fmt):
    """
    Trata um elemento de estilo.

    Parâmetros
    ----------
    node : lxml.etree._Element
        ``<italic>``, ``<bold>``, ``<sup>``...
    fmt : frozenset of str
        Formatos ativos herdados.

    Retorna
    -------
    list of dict
        Runs do conteúdo com o formato do elemento somado aos herdados.
    """
    return inline.inlines(node, fmt | {FORMATS[tag(node)]})


# -----------------
# ``<break>``: quebra de linha dentro do texto (o ``_`` evita o nome reservado ``break``).
# -----------------


@inline_handler("break")
def handle_break(node, fmt):
    """Run de quebra de linha."""
    return [{"break": True}]
