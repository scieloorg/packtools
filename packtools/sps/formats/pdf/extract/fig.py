"""
Figuras: ``<fig>``, ``<fig-group>`` e ``<table-wrap-group>``.
"""

from packtools.sps.formats.pdf.extract import registry
from packtools.sps.formats.pdf.extract.flow import mark_target, paragraph
from packtools.sps.formats.pdf.extract.graphic import figure_block, graphics
from packtools.sps.formats.pdf.extract.registry import block_handler
from packtools.sps.formats.pdf.extract.runs import has_content, tag
from packtools.sps.formats.pdf.extract.title import GROUP_MEMBERS, caption_runs


# -----------------
# ``<fig>``: figura.
# -----------------


@block_handler("fig")
def handle_fig(node, ctx):
    """
    Converte uma figura.

    Parâmetros
    ----------
    node : lxml.etree._Element
        ``<fig>``.
    ctx : dict
        Contexto.

    Retorna
    -------
    list of dict
        Um bloco ``figure`` por imagem, com a legenda na última; sem
        imagem, um parágrafo só com a legenda. A figura fica onde está no
        XML (o old_pdf juntava todas no fim da seção).
    """
    images = graphics(node)
    caption = caption_runs(node)
    if not images:
        return paragraph(caption, ctx, role="figure_caption")
    blocks = [figure_block(node, image, []) for image in images]
    blocks[-1]["caption"] = caption
    return blocks


# -----------------
# ``<fig-group>`` e ``<table-wrap-group>``: grupo de figuras ou de tabelas.
# -----------------


@block_handler("fig-group", "table-wrap-group")
def handle_group(node, ctx):
    """
    Converte um grupo de figuras ou tabelas.

    Parâmetros
    ----------
    node : lxml.etree._Element
        ``<fig-group>`` ou ``<table-wrap-group>``.
    ctx : dict
        Contexto.

    Retorna
    -------
    list of dict
        Parágrafo com a legenda do grupo (se houver) e os blocos de cada
        membro (``<fig>``, ``<table-wrap>`` ou grupo aninhado), cada um
        marcado como alvo do próprio ``@id``.
    """
    caption = caption_runs(node)
    blocks = paragraph(caption, ctx, role="figure_caption") if has_content(caption) else []
    for member in node:
        if tag(member) in GROUP_MEMBERS:
            blocks += mark_target(member, registry.BLOCK[tag(member)](member, ctx))
    return blocks
