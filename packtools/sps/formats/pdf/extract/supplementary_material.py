"""``<supplementary-material>`` e ``<media>``: arquivo complementar ao artigo."""

from packtools.sps.formats.pdf.extract.link import visible_links
from packtools.sps.formats.pdf.extract.flow import paragraph
from packtools.sps.formats.pdf.extract.inline import inlines, plain_text
from packtools.sps.formats.pdf.extract.title import label_of
from packtools.sps.formats.pdf.extract.registry import block_handler, inline_handler
from packtools.sps.formats.pdf.extract.runs import bookmark_runs, href, tag, text_run
from packtools.sps.formats.pdf.config.labels import label

ITEM_TAGS = ("supplementary-material", "media")


def is_supplementary_section(node):
    """True para a ``<sec>`` que é o bloco de material suplementar: tem ``<supplementary-material>`` e nenhuma ``<sec>`` própria."""
    return (
        tag(node) == "sec"
        and node.find("sec") is None
        and any(tag(e) == "supplementary-material" for e in node.iter())
    )


def stands_alone(paragraph):
    """
    True se o parágrafo só tem material suplementar, sem texto em volta.

    Parâmetros
    ----------
    paragraph : lxml.etree._Element
        ``<p>`` (ou ``<verse-line>``, ``<attrib>``).

    Retorna
    -------
    bool
        True quando não há texto fora de ``<supplementary-material>`` e
        ``<media>``; aí cada item continua um parágrafo próprio, com o
        rótulo padrão quando não tem ``<label>``.
    """
    return not _text_outside_items(paragraph).strip()


def _text_outside_items(node):
    """Texto de node fora dos itens de material suplementar (comentários só contribuem com o tail)."""
    parts = [node.text or ""] if tag(node) is not None else []
    for child in node:
        if tag(child) is not None and tag(child) not in ITEM_TAGS:
            parts.append(_text_outside_items(child))
        parts.append(child.tail or "")
    return "".join(parts)


def item_runs(node, fmt=frozenset(), default_label=None):
    """
    Runs da linha descritiva de um material suplementar.

    Parâmetros
    ----------
    node : lxml.etree._Element
        ``<supplementary-material>`` ou ``<media>``.
    fmt : frozenset of str, opcional
        Formatos ativos herdados (itálico, negrito em volta do item).
    default_label : str, opcional
        Rótulo usado quando o item não tem ``<label>``; sem ele, a linha
        começa pelo título ou pelo arquivo.

    Retorna
    -------
    list of dict
        "Rótulo (Título): arquivo (tipo/subtipo). Descrição. Notas", com o
        endereço visível dos links.
    """
    own_label = label_of(node)
    if own_label is not None:
        runs = inlines(own_label, fmt)
    else:
        runs = [text_run(default_label, fmt)] if default_label else []
    title = node.find("caption/title")
    if title is not None:
        title_runs = inlines(title, fmt)
        runs += [text_run(" (", fmt)] + title_runs + [text_run(")", fmt)] if runs else title_runs
    media = next((e for e in node.iter() if tag(e) in ("media", "graphic")), None)
    if media is not None and href(media):
        kind = "/".join(v for v in (media.get("mimetype"), media.get("mime-subtype")) if v)
        line = href(media) + (f" ({kind})" if kind else "")
        runs.append(text_run(f": {line}" if runs else line, fmt))
        description = media.find("long-desc")
        if description is None:
            description = media.find("alt-text")
        if description is not None and plain_text(description):
            runs.append(text_run(f". {plain_text(description)}", fmt))
    for p in (e for e in node.iter() if tag(e) == "p"):
        runs += [text_run(". ", fmt)] + visible_links(inlines(p, fmt))
    return runs


@inline_handler(*ITEM_TAGS)
def handle_supplementary_material_inline(node, fmt):
    """
    Trata o material suplementar no meio do texto de um parágrafo.

    Parâmetros
    ----------
    node : lxml.etree._Element
        ``<supplementary-material>`` ou ``<media>``.
    fmt : frozenset of str
        Formatos ativos herdados.

    Retorna
    -------
    list of dict
        A linha descritiva (`item_runs`) no lugar do elemento, sem o rótulo
        padrão: o texto em volta já apresenta o item ("Download
        results.xlsx (application/xlsx) for full results."). Com ``@id``,
        começa com a marca do alvo de ``<xref>``.
    """
    return bookmark_runs(node) + item_runs(node, fmt)


@block_handler(*ITEM_TAGS)
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
        Parágrafo com a linha descritiva (`item_runs`). Sem ``<label>``, o
        rótulo é "Supplementary Material" no idioma do documento.
    """
    return paragraph(item_runs(node, default_label=label("supplementary_material", ctx["lang"])), ctx)
