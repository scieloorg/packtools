"""
Artigo completo -> listas de blocos::

    {"meta": {...}, "front": [blocos], "main": [blocos], "annex": [blocos]}

``meta`` é um dict plano (cabeçalho, rodapé, citação); ``front``, ``main``
e ``annex`` são listas planas de blocos (ver flow.py).
"""

from packtools.sps.formats.pdf.extract import citation
from packtools.sps.formats.pdf.extract.article_meta import extract_meta, front_blocks
from packtools.sps.formats.pdf.extract.context import child, context
from packtools.sps.formats.pdf.extract.flow import flow, flow_nodes
from packtools.sps.formats.pdf.extract.inline import inlines
from packtools.sps.formats.pdf.extract.languages import XML_LANG, document_for
from packtools.sps.formats.pdf.extract.runs import normalize, text_run
from packtools.sps.formats.pdf.extract.supplementary_material import handle_supplementary_material
from packtools.sps.formats.pdf.config.labels import label


def extract_article(xml_tree, lang=None, citation_style="vancouver"):
    """
    Extrai o documento de um idioma.

    Parâmetros
    ----------
    xml_tree : lxml.etree._ElementTree, lxml.etree._Element or dict
        Artigo SPS, ou a visão já montada por languages.document_for.
    lang : str, opcional
        Idioma (ver languages.py); None é o idioma principal.
    citation_style : str, opcional
        Estilo da citação do rodapé (ver config/citation.py).

    Retorna
    -------
    dict
        ``meta``: metadados; ``front``: blocos da capa; ``main``: ``<body>``
        e ``<back>`` na ordem do documento, seguidos dos sub-articles que
        não são tradução (cada tradução é um documento próprio); ``annex``:
        ``<app-group>`` e a seção de material suplementar de primeiro nível.
        A nota "como citar", impressa no rodapé, não se repete.

    Notas
    -----
    Diferenças em relação ao old_pdf, que selecionava elementos esperados:
    agora saem também os ``<p>`` do ``<body>`` antes da primeira ``<sec>``,
    o ``<label>`` das seções e o ``<fn-group>``. Figuras e tabelas ficam na
    ordem do documento.
    """
    view = xml_tree if isinstance(xml_tree, dict) else document_for(xml_tree, lang)
    cite_note = citation.cite_as_note(view)
    exclude = [cite_note] if cite_note is not None else []
    meta = extract_meta(view, citation_style)
    main, annex = body_and_back(view, context(lang=view["lang"], exclude=exclude))
    for sub_article in view["sub_articles"]:
        main += sub_article_blocks(sub_article, exclude)
    return {
        "meta": meta,
        "front": front_blocks(view, meta, cite_note),
        "main": main,
        "annex": annex,
    }


def body_and_back(view, ctx):
    """
    Extrai ``<body>`` e ``<back>``, separando os anexos.

    Parâmetros
    ----------
    view : dict
        Visão do documento.
    ctx : dict
        Contexto inicial.

    Retorna
    -------
    main : list of dict
        Blocos do fluxo principal.
    annex : list of dict
        Blocos dos anexos, na ordem do documento.

    Notas
    -----
    Herdado do old_pdf (regra editorial): ``<app-group>`` e a seção de
    material suplementar, em qualquer nível, vão para os anexos; quem os
    desvia são os próprios handlers (sec.to_annex), pelo coletor
    ``ctx["annex"]``. Um ``<supplementary-material>`` solto, filho direto
    de ``<body>``/``<back>`` (sem ``<sec>``), também vai, sob o título
    padrão "Supplementary Material" (um só, para os itens seguidos).
    """
    annex = []
    ctx = child(ctx, annex=annex)
    loose = []  # último bloco posto nos anexos por um item solto

    def handle_loose_item(node, node_ctx):
        """Item solto vai para os anexos; o título padrão só abre uma nova sequência de itens."""
        if not (annex and loose and annex[-1] is loose[-1]):
            annex.append(
                {
                    "type": "heading",
                    "level": 2,
                    "runs": [text_run(label("supplementary_material", node_ctx["lang"]))],
                }
            )
        annex.extend(handle_supplementary_material(node, child(node_ctx, annex=None)))
        loose[:] = annex[-1:]
        return []

    routes = {"supplementary-material": handle_loose_item}
    main = flow(view["body"], ctx, handlers=routes) if view["body"] is not None else []
    back_ctx = child(ctx, ref_title=view["ref_title"])
    main += flow_nodes(view["back_text"], view["back"], back_ctx, handlers=routes)
    return main, annex


def sub_article_blocks(node, exclude):
    """
    Extrai um sub-article (parecer, resposta...): título como seção, ``<body>`` e ``<back>``.

    Parâmetros
    ----------
    node : lxml.etree._Element
        ``<sub-article>``.
    exclude : list of lxml.etree._Element
        Nós que não entram no fluxo.

    Retorna
    -------
    list of dict
        Heading com o título do sub-article (se houver) e os blocos, no
        idioma do próprio sub-article.
    """
    meta = node.find("front-stub")
    if meta is None:
        meta = node.find("front/article-meta")
    title = meta.find("title-group/article-title") if meta is not None else None
    runs = normalize(inlines(title)) if title is not None else []
    blocks = [{"type": "heading", "level": 2, "runs": runs}] if runs else []
    ctx = context(level=2 if runs else 1, lang=node.get(XML_LANG), exclude=exclude)
    for part in (node.find("body"), node.find("back")):
        if part is not None:
            blocks += flow(part, ctx)
    return blocks
