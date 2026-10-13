"""``<supplementary-material>`` e ``<media>``: arquivo complementar ao artigo."""

from packtools.sps.formats.pdf.extract.link import visible_links
from packtools.sps.formats.pdf.extract.flow import paragraph
from packtools.sps.formats.pdf.extract.inline import inlines, plain_text
from packtools.sps.formats.pdf.extract.title import label_of
from packtools.sps.formats.pdf.extract.registry import block_handler
from packtools.sps.formats.pdf.extract.runs import href, tag, text_run
from packtools.sps.formats.pdf.config.labels import label


def is_supplementary_section(node):
    """True para a ``<sec>`` que é o bloco de material suplementar: tem ``<supplementary-material>`` e nenhuma ``<sec>`` própria."""
    return (
        tag(node) == "sec"
        and node.find("sec") is None
        and any(tag(e) == "supplementary-material" for e in node.iter())
    )


@block_handler("supplementary-material", "media")
def handle_supplementary_material(node, ctx):
    """
    Converte um material suplementar numa linha descritiva.

    Parâmetros
    ----------
    node : lxml.etree._Element
        ``<supplementary-material>`` ou ``<media>``.
    ctx : dict
        Contexto.

    Retorna
    -------
    list of dict
        Parágrafo "Rótulo (Título): arquivo (tipo/subtipo). Descrição.
        Notas", com o endereço visível dos links. Sem ``<label>``, o rótulo
        é "Supplementary Material" no idioma do documento.
    """
    own_label = label_of(node)
    runs = (
        inlines(own_label)
        if own_label is not None
        else [text_run(label("supplementary_material", ctx["lang"]))]
    )
    title = node.find("caption/title")
    if title is not None:
        runs += [text_run(" (")] + inlines(title) + [text_run(")")]
    media = next((e for e in node.iter() if tag(e) in ("media", "graphic")), None)
    if media is not None and href(media):
        kind = "/".join(v for v in (media.get("mimetype"), media.get("mime-subtype")) if v)
        runs.append(text_run(f": {href(media)}" + (f" ({kind})" if kind else "")))
        description = media.find("long-desc")
        if description is None:
            description = media.find("alt-text")
        if description is not None and plain_text(description):
            runs.append(text_run(f". {plain_text(description)}"))
    for p in (e for e in node.iter() if tag(e) == "p"):
        runs += [text_run(". ")] + visible_links(inlines(p))
    return paragraph(runs, ctx)
