"""
Links: ``<xref>`` (interno, para o alvo no próprio documento) e
``<ext-link>``, ``<uri>``, ``<email>`` (externos).
"""

from packtools.sps.formats.pdf.extract.inline import inlines
from packtools.sps.formats.pdf.extract.registry import inline_handler
from packtools.sps.formats.pdf.extract.runs import href, runs_text, tag, text_run


# -----------------
# ``<xref>``: referência cruzada (citação, figura, tabela, nota, afiliação).
# -----------------
# O texto vira link interno para o alvo; o alvo recebe uma marca com o mesmo
# id em flow.mark_target (corpo) e na capa (afiliações, notas de autor).


def rid(node):
    """Primeiro id de ``@rid`` (``rid="B1 B2"`` aponta para várias referências; o link leva à primeira), ou None."""
    ids = (node.get("rid") or "").split()
    return ids[0] if ids else None


@inline_handler("xref")
def handle_xref(node, fmt):
    """
    Trata ``<xref>``.

    Parâmetros
    ----------
    node : lxml.etree._Element
        ``<xref>``.
    fmt : frozenset of str
        Formatos ativos herdados.

    Retorna
    -------
    list of dict
        Runs do conteúdo com ``anchor`` = `rid`; sem ``@rid``, o texto fica
        sem link.
    """
    anchor = rid(node)
    runs = inlines(node, fmt)
    if anchor:
        for run in runs:
            if "text" in run:
                run.setdefault("anchor", anchor)
    return runs


# -----------------
# ``<ext-link>``, ``<uri>`` e ``<email>``: links externos, clicáveis no PDF.
# -----------------


@inline_handler("ext-link", "uri", "email")
def handle_link(node, fmt):
    """
    Trata um link externo.

    Parâmetros
    ----------
    node : lxml.etree._Element
        ``<ext-link>``, ``<uri>`` ou ``<email>``.
    fmt : frozenset of str
        Formatos ativos herdados.

    Retorna
    -------
    list of dict
        Runs do conteúdo com ``href`` = destino (``xlink:href`` ou o próprio
        texto; ``mailto:`` para e-mail).
    """
    target = href(node) or "".join(node.itertext()).strip()
    if tag(node) == "email" and target and not target.startswith("mailto:"):
        target = f"mailto:{target}"
    runs = inlines(node, fmt)
    for run in runs:
        if "text" in run:
            run.setdefault("href", target)
    return runs


def visible_links(runs):
    """
    Torna visível o endereço de links cujo texto não o mostra.

    Parâmetros
    ----------
    runs : list of dict
        Runs que podem ter ``href``.

    Retorna
    -------
    list of dict
        Os mesmos runs, com " (endereço)" depois do último run de cada link
        cujo texto não contém o endereço (ex. "clique aqui"). Usado no
        material suplementar, onde o endereço do arquivo precisa aparecer
        impresso.
    """
    out = []
    for i, run in enumerate(runs):
        out.append(run)
        target = run.get("href")
        is_last = i + 1 == len(runs) or runs[i + 1].get("href") != target
        if target and is_last and target not in runs_text(r for r in runs if r.get("href") == target):
            out.append(text_run(f" ({target})"))
    return out
