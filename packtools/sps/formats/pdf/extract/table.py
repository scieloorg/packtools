"""
Tabelas: ``<table-wrap>``, ``<table>`` e ``<alternatives>`` solto.
"""

from packtools.sps.formats.pdf.extract.context import child
from packtools.sps.formats.pdf.extract.flow import block_runs, flow, paragraph
from packtools.sps.formats.pdf.extract.graphic import best, figure_block, graphics, handle_block
from packtools.sps.formats.pdf.extract.registry import block_handler
from packtools.sps.formats.pdf.extract.runs import normalize, runs_text, tag
from packtools.sps.formats.pdf.extract.title import caption_runs


# -----------------
# ``<table>``, ``<tr>``, ``<th>`` e ``<td>``: grade de células com a posição
# já resolvida (colspan/rowspan). A legenda e as notas ficam no ``<table-wrap>``.
# -----------------


def tables(node):
    """
    Lista as ``<table>`` de um elemento.

    Parâmetros
    ----------
    node : lxml.etree._Element
        ``<table-wrap>`` ou ``<alternatives>``.

    Retorna
    -------
    list of lxml.etree._Element
        As ``<table>`` que não estão dentro de outra ``<table>`` (tabela
        aninhada fica dentro da célula).
    """
    return [t for t in node.iter() if tag(t) == "table" and not _inside_table(t, node)]


def _inside_table(element, stop):
    """True se element está dentro de outra ``<table>`` abaixo de stop."""
    parent = element.getparent()
    while parent is not None and parent is not stop:
        if tag(parent) == "table":
            return True
        parent = parent.getparent()
    return False


def _span(cell, attr):
    """colspan/rowspan da célula como inteiro >= 1 (valor inválido vira 1)."""
    try:
        return max(1, int(cell.get(attr, 1)))
    except ValueError:
        return 1


def grid(table, cell_runs):
    """
    Lê a grade de uma ``<table>``.

    Parâmetros
    ----------
    table : lxml.etree._Element
        ``<table>``.
    cell_runs : callable
        ``função(célula) -> runs`` com o conteúdo completo da célula.

    Retorna
    -------
    dict
        ``{"nrows", "ncols", "cells"}``; cada célula é
        ``{"row", "col", "rowspan", "colspan", "header", "runs"}``. Entram
        todas as linhas (``<thead>``, ``<tbody>``, ``<tfoot>`` ou ``<tr>``
        soltos), na ordem do documento, e todas as células; ``header`` é
        célula ``<th>`` ou dentro de ``<thead>``.
    """
    rows = [tr for tr in table.iter() if tag(tr) == "tr" and not _inside_table(tr, table)]
    occupied, cells = set(), []
    for r, tr in enumerate(rows):
        in_head = tag(tr.getparent()) == "thead"
        c = 0
        for cell in tr:
            if tag(cell) not in ("td", "th"):
                continue
            while (r, c) in occupied:
                c += 1
            rowspan = min(_span(cell, "rowspan"), len(rows) - r)
            colspan = _span(cell, "colspan")
            occupied.update((r + i, c + j) for i in range(rowspan) for j in range(colspan))
            # <th> fora de <thead> também entra (o old_pdf lia só <td> no <tbody>)
            cells.append(
                {
                    "row": r,
                    "col": c,
                    "rowspan": rowspan,
                    "colspan": colspan,
                    "header": in_head or tag(cell) == "th",
                    "runs": cell_runs(cell),
                }
            )
            c += colspan
    ncols = max((col + 1 for _, col in occupied), default=0)
    return {"nrows": len(rows), "ncols": ncols, "cells": cells}


def max_cell_length(block):
    """Tamanho, em caracteres, do texto da célula mais longa de um bloco de tabela."""
    return max((len(runs_text(cell["runs"])) for cell in block["cells"]), default=0)


# -----------------
# ``<table-wrap>`` e ``<table-wrap-foot>``: tabela com legenda e notas.
# -----------------


@block_handler("table-wrap")
def handle_table_wrap(node, ctx):
    """
    Converte uma tabela.

    Parâmetros
    ----------
    node : lxml.etree._Element
        ``<table-wrap>`` (ou ``<alternatives>`` com ``<table>``).
    ctx : dict
        Contexto.

    Retorna
    -------
    list of dict
        Um bloco ``table`` por ``<table>``::

            {"type": "table", "id", "panel", "caption", "nrows", "ncols", "cells", "foot"}

        Herdado do old_pdf (#1368): um ``<table-wrap>`` pode ter várias
        ``<table>`` (painéis lado a lado com uma legenda só). A legenda vai
        no primeiro bloco e as notas no último; ``panel`` (0, 1, 2...) diz
        que os blocos são partes da mesma tabela, para o layout decidir a
        largura delas juntas. Tabela publicada como imagem vira bloco
        ``figure`` com a legenda antes (o old_pdf imprimia só a legenda e
        perdia a imagem); sem tabela nem imagem, um parágrafo com a legenda.
    """
    caption = caption_runs(node)
    panels = tables(node)
    if not panels:
        images = graphics(node)
        if images:
            return [
                figure_block(node, image, caption if i == 0 else [], "table_caption", True)
                for i, image in enumerate(images)
            ]
        return paragraph(caption, ctx, role="table_caption")

    cell_ctx = child(ctx, indent=0)

    def cell_runs(cell):
        """Conteúdo completo da célula (parágrafos, fórmulas, listas) achatado em runs."""
        return normalize(block_runs(flow(cell, cell_ctx)))

    foot = []
    for item in node:
        if tag(item) == "table-wrap-foot":
            foot += [block["runs"] for block in flow(item, cell_ctx)]

    blocks = []
    last = len(panels) - 1
    for i, panel in enumerate(panels):
        blocks.append(
            {
                "type": "table",
                "id": node.get("id"),
                "panel": i,
                "caption": caption if i == 0 else [],
                **grid(panel, cell_runs),
                "foot": foot if i == last else [],
            }
        )
    return blocks


# -----------------
# ``<alternatives>`` solto: várias representações do mesmo conteúdo; usa-se uma.
# -----------------


@block_handler("alternatives")
def handle_alternatives(node, ctx):
    """
    Converte um ``<alternatives>`` fora de figura, tabela ou fórmula.

    Parâmetros
    ----------
    node : lxml.etree._Element
        ``<alternatives>``.
    ctx : dict
        Contexto.

    Retorna
    -------
    list of dict
        Blocos da representação escolhida, nesta ordem de preferência:
        tabela, melhor imagem (ver graphic.best), primeira representação.
    """
    if any(tag(e) == "table" for e in node):
        return handle_table_wrap(node, ctx)
    image = best(g for g in node if tag(g) == "graphic")
    if image is not None:
        return handle_block(image, ctx)
    first = next((e for e in node if tag(e)), None)
    return flow(first, ctx) if first is not None else []
