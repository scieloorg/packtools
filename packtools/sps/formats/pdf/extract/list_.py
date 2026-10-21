"""
Listas: ``<list>`` e ``<def-list>`` (o ``_`` evita sombrear o ``list`` do Python).
"""

import string

from packtools.sps.formats.pdf.extract.context import child
from packtools.sps.formats.pdf.extract.flow import flow
from packtools.sps.formats.pdf.extract.inline import inlines, plain_text
from packtools.sps.formats.pdf.extract.registry import block_handler
from packtools.sps.formats.pdf.extract.runs import text_run
from packtools.sps.formats.pdf.extract.sec import handle_section
from packtools.sps.formats.pdf.extract.title import label_of


# -----------------
# ``<list>`` e ``<list-item>`` (o ``_`` evita sombrear o ``list`` do Python).
# -----------------


def roman(number):
    """
    Converte um número em algarismos romanos minúsculos.

    Exemplos
    --------
    >>> roman(14)
    'xiv'
    """
    values = (1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1)
    symbols = ("m", "cm", "d", "cd", "c", "xc", "l", "xl", "x", "ix", "v", "iv", "i")
    result = ""
    for value, symbol in zip(values, symbols):
        count, number = divmod(number, value)
        result += symbol * count
    return result


# Herdado do old_pdf (#1365): marcador de cada list-type. list-type="simple" (ou
# desconhecido) fica sem marcador: os itens já trazem a própria numeração (ex.
# o <label> de cada <disp-formula>).
MARKERS = {
    "bullet": lambda i: "•",
    "order": str,
    "arabic": str,
    "roman-lower": roman,
    "roman-upper": lambda i: roman(i).upper(),
    "alpha-lower": lambda i: string.ascii_lowercase[(i - 1) % 26],
    "alpha-upper": lambda i: string.ascii_uppercase[(i - 1) % 26],
}


def marker_text(list_node, item, position):
    """
    Texto do marcador de um item.

    Parâmetros
    ----------
    list_node : lxml.etree._Element
        ``<list>`` (fornece ``@list-type``).
    item : lxml.etree._Element
        ``<list-item>``; o ``<label>`` dele tem precedência.
    position : int
        Posição do item, a partir de 1.

    Retorna
    -------
    str
        Ex. "•", "1.", "iv.", "a." ou o rótulo do item; vazio sem marcador.
    """
    label = label_of(item)
    if label is not None:
        return plain_text(label)
    list_type = list_node.get("list-type", "")
    marker = MARKERS.get(list_type)
    if marker is None:
        return ""
    text = marker(position)
    return text if list_type == "bullet" else f"{text}."


@block_handler("list")
def handle_list(node, ctx):
    """
    Converte uma lista em um parágrafo por item.

    Parâmetros
    ----------
    node : lxml.etree._Element
        ``<list>``.
    ctx : dict
        Contexto.

    Retorna
    -------
    list of dict
        Título da lista (se houver) e os blocos dos itens, com o marcador no
        início do primeiro parágrafo de cada item. Listas aninhadas ganham
        um nível de recuo.
    """
    depth = ctx["list_depth"]
    item_ctx = child(ctx, list_depth=depth + 1, indent=ctx["indent"] + (1 if depth else 0))
    position = 0

    def handle_list_item(item, _ctx):
        """``<list-item>``: o contador de posição é desta lista (handler local, ver flow.process_child)."""
        nonlocal position
        position += 1
        text = marker_text(node, item, position)
        prefix = [text_run(f"{text} ")] if text else []
        label = label_of(item)
        return flow(item, item_ctx, prefix=prefix, skip=[label] if label is not None else ())

    return handle_section(node, ctx, handlers={"list-item": handle_list_item})


# -----------------
# ``<def-list>``, ``<def-item>``, ``<term>`` e ``<def>``: lista de definições.
# -----------------


def handle_def_item(item, ctx):
    """
    Converte um ``<def-item>``.

    Parâmetros
    ----------
    item : lxml.etree._Element
        ``<def-item>``.
    ctx : dict
        Contexto.

    Retorna
    -------
    list of dict
        Blocos de ``<def>`` com "termo: " em negrito no início.
    """
    terms = item.findall("term")
    prefix = []
    for term in terms:
        prefix += inlines(term, ctx["fmt"] | {"bold"}) + [text_run(": ")]
    return flow(item, ctx, prefix=prefix, skip=terms)


@block_handler("def-list")
def handle_def_list(node, ctx):
    """
    Converte uma lista de definições.

    Parâmetros
    ----------
    node : lxml.etree._Element
        ``<def-list>``.
    ctx : dict
        Contexto.

    Retorna
    -------
    list of dict
        Título (se houver) e um parágrafo "termo: definição" por item.
    """
    return handle_section(node, ctx, handlers={"def-item": handle_def_item})
