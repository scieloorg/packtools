"""
Seções e parágrafos: ``<sec>`` e os elementos com o mesmo tratamento,
``<p>``, ``<app-group>``, ``<disp-quote>``, ``<preformat>`` e ``<fn>``.
"""

from packtools.sps.formats.pdf.extract.context import child
from packtools.sps.formats.pdf.extract.flow import flow, paragraph
from packtools.sps.formats.pdf.extract.inline import inlines
from packtools.sps.formats.pdf.extract.registry import block_handler
from packtools.sps.formats.pdf.extract.runs import has_content, runs_text, tag, text_run
from packtools.sps.formats.pdf.extract.supplementary_material import (
    SUPPLEMENTARY_MATERIAL_TAGS,
    has_text_outside_supplementary_material,
    is_supplementary_section,
)
from packtools.sps.formats.pdf.extract.title import label_of, note_label_runs, title_runs
from packtools.sps.formats.pdf.config.labels import label


# -----------------
# ``<sec>`` e os elementos com o mesmo tratamento: título seguido do conteúdo.
# -----------------
# Registra também ``<app>``, ``<ack>``, ``<boxed-text>``, ``<glossary>``,
# ``<fn-group>``, ``<notes>``, ``<bio>``, ``<statement>``, ``<verse-group>``,
# ``<sig-block>``, ``<question-wrap>``, ``<question>``, ``<answer>``,
# ``<explanation>`` e ``<disp-formula-group>``. `handle_section` é
# reaproveitado por lista, apêndices, referências e citação em bloco.


@block_handler(
    "app", "ack", "boxed-text", "glossary", "fn-group", "notes", "bio",
    "statement", "verse-group", "sig-block", "question-wrap", "question",
    "answer", "explanation", "disp-formula-group",
)
def handle_section(node, ctx, default_title=None, handlers=None, title=None):
    """
    Converte uma seção em título seguido do conteúdo.

    Parâmetros
    ----------
    node : lxml.etree._Element
        Elemento da seção.
    ctx : dict
        Contexto.
    default_title : str, opcional
        Título quando o elemento não tem ``<label>``/``<title>``.
    handlers : dict, opcional
        Handlers locais repassados a flow (ex. ``<list-item>``).
    title : str, opcional
        Texto que substitui o do ``<title>`` (ver title.title_runs).

    Retorna
    -------
    list of dict
        Heading um nível abaixo do contexto (se houver título) e os blocos
        do conteúdo. Em resumo estruturado (``ctx["inline_titles"]``) o
        título vai em negrito no início do primeiro parágrafo, como
        "Métodos: ...".
    """
    runs, consumed = title_runs(node, replacement=title)
    if not has_content(runs) and default_title:
        runs = [text_run(default_title)]
    if not has_content(runs):
        return flow(node, ctx, skip=consumed, handlers=handlers)
    if ctx["inline_titles"]:
        # Herdado do old_pdf: no resumo estruturado, o título da subseção
        # ("Métodos") abre o parágrafo; ":" só é posto se o XML não trouxer
        # pontuação no fim do título ("Métodos:" já vem assim em alguns XMLs).
        text = runs_text(runs).rstrip()
        prefix = [dict(r, bold=True) for r in runs]
        prefix.append(text_run(" " if text[-1:] in ":.!?;" else ": "))
        return flow(node, ctx, prefix=prefix, skip=consumed, handlers=handlers)
    level = ctx["level"] + 1
    heading = {"type": "heading", "level": level, "runs": runs}
    return [heading] + flow(node, child(ctx, level=level), skip=consumed, handlers=handlers)


def to_annex(node, ctx, extract):
    """
    Desvia um elemento para os anexos, quando o documento os coleta.

    Parâmetros
    ----------
    node : lxml.etree._Element
        ``<app-group>`` ou a seção de material suplementar.
    ctx : dict
        Contexto; ``ctx["annex"]`` é a lista dos anexos (ou None).
    extract : callable
        ``função(node, ctx) -> blocos``.

    Retorna
    -------
    list of dict
        Vazia quando os blocos foram para ``ctx["annex"]`` (extraídos como
        seção de primeiro nível, sem recuo); sem coletor, os próprios blocos.

    Notas
    -----
    Herdado do old_pdf (regra editorial): apêndices e a seção de material
    suplementar saem do fluxo e vão para páginas próprias (página nova,
    coluna única, rodapé sem número de página; ver render/document.py), em
    qualquer nível do ``<body>``/``<back>`` (o old_pdf usava ``.//app-group``
    e ``.//sec[.//supplementary-material and not(sec)]``).
    """
    if ctx["annex"] is None:
        return extract(node, ctx)
    ctx["annex"].extend(extract(node, child(ctx, level=1, indent=0, annex=None)))
    return []


@block_handler("sec")
def handle_sec(node, ctx):
    """
    Converte uma ``<sec>``; a de material suplementar vai para os anexos.

    Parâmetros
    ----------
    node : lxml.etree._Element
        ``<sec>``.
    ctx : dict
        Contexto.

    Retorna
    -------
    list of dict
        Blocos da seção (ver `handle_section`), ou vazia quando a seção é a
        de material suplementar (ver supplementary_material.
        is_supplementary_section) e foi para os anexos, com o título padrão
        "Supplementary Material" se não tiver ``<title>``/``<label>``.
    """
    if not is_supplementary_section(node):
        return handle_section(node, ctx)
    return to_annex(
        node,
        ctx,
        lambda n, c: handle_section(n, c, default_title=label("supplementary_material", c["lang"])),
    )


# -----------------
# ``<p>`` e os elementos com o mesmo tratamento: ``<verse-line>`` e ``<attrib>``.
# -----------------


@block_handler("p", "verse-line", "attrib")
def handle_p(node, ctx, prefix=None):
    """
    Converte um parágrafo.

    Parâmetros
    ----------
    node : lxml.etree._Element
        ``<p>``, ``<verse-line>`` ou ``<attrib>``.
    ctx : dict
        Contexto.
    prefix : list of dict, opcional
        Runs no início do parágrafo (marcador de lista, rótulo de nota; ver
        flow.process_child).

    Retorna
    -------
    list of dict
        Um parágrafo, ou mais se houver blocos dentro (lista, fórmula em
        destaque, figura...), que dividem o texto em volta. Material
        suplementar com texto em volta fica no meio do parágrafo; sozinho,
        continua um parágrafo próprio.
    """
    if has_text_outside_supplementary_material(node):
        # handler local None: o item vira texto do parágrafo em aberto (ver flow.handler)
        return flow(
            node, ctx, prefix=prefix, handlers=dict.fromkeys(SUPPLEMENTARY_MATERIAL_TAGS)
        )
    return flow(node, ctx, prefix=prefix)


# -----------------
# ``<app-group>``: grupo de apêndices.
# -----------------
# Os ``<app>`` dentro dele são seções comuns (`handle_section`). No artigo, o
# ``<app-group>`` vai para os anexos (ver article.py).


@block_handler("app-group")
def handle_app_group(node, ctx):
    """
    Converte um grupo de apêndices (para os anexos, ver `to_annex`).

    Parâmetros
    ----------
    node : lxml.etree._Element
        ``<app-group>``.
    ctx : dict
        Contexto.

    Retorna
    -------
    list of dict
        Blocos do grupo; vazia quando foram para os anexos.

    Notas
    -----
    Títulos herdados do old_pdf:

    - grupo sem título e nenhum ``<app>`` com título: o grupo recebe o
      título padrão "Appendix" no idioma do documento;
    - grupo sem título, mais de um ``<app>`` e algum com título: cada
      ``<app>`` sem título recebe "Appendix N" (N = posição), para não
      ficar sob o título do apêndice anterior.
    """
    return to_annex(node, ctx, _app_group_blocks)


def _app_group_blocks(node, ctx):
    """Blocos do ``<app-group>`` com os títulos padrão (ver `handle_app_group`)."""
    apps = [app for app in node if tag(app) == "app"]
    titled = [bool(title_runs(app)[0]) for app in apps]
    group_titled = bool(title_runs(node)[0])
    default = None if group_titled or any(titled) else label("appendix", ctx["lang"])
    handlers = None
    if not group_titled and any(titled) and len(apps) > 1:
        numbers = {app: i for i, app in enumerate(apps, 1)}

        def handle_app(app, app_ctx):
            """``<app>`` sem título recebe "Appendix N"."""
            return handle_section(app, app_ctx, default_title=f"{label('appendix', app_ctx['lang'])} {numbers[app]}")

        handlers = {"app": handle_app}
    return handle_section(node, ctx, default_title=default, handlers=handlers)


# -----------------
# ``<disp-quote>``: citação em bloco.
# -----------------


@block_handler("disp-quote")
def handle_disp_quote(node, ctx):
    """
    Converte uma citação em bloco.

    Parâmetros
    ----------
    node : lxml.etree._Element
        ``<disp-quote>``.
    ctx : dict
        Contexto.

    Retorna
    -------
    list of dict
        Blocos da citação (título, parágrafos, ``<attrib>``) com um nível a
        mais de recuo.
    """
    return handle_section(node, child(ctx, indent=ctx["indent"] + 1))


# -----------------
# ``<preformat>`` e ``<code>``: texto pré-formatado.
# -----------------


@block_handler("preformat", "code")
def handle_preformat(node, ctx):
    """
    Converte texto pré-formatado.

    Parâmetros
    ----------
    node : lxml.etree._Element
        ``<preformat>`` ou ``<code>``.
    ctx : dict
        Contexto.

    Retorna
    -------
    list of dict
        Parágrafo monoespaçado, com espaços e quebras de linha preservados.
    """
    return paragraph(inlines(node, ctx["fmt"] | {"monospace"}), ctx, preserve=True)


# -----------------
# ``<fn>``: nota (de rodapé do artigo, de tabela ou de autor).
# -----------------


@block_handler("fn")
def handle_fn(node, ctx):
    """
    Converte uma nota.

    Parâmetros
    ----------
    node : lxml.etree._Element
        ``<fn>``.
    ctx : dict
        Contexto.

    Retorna
    -------
    list of dict
        Blocos da nota, com o rótulo no início do primeiro parágrafo (ver
        label.note_label_runs).
    """
    label = label_of(node)
    if label is None:
        return flow(node, ctx)
    return flow(node, ctx, prefix=note_label_runs(label), skip=[label])
