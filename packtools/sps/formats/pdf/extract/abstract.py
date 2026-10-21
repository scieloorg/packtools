"""
Resumos da capa: ``<abstract>``, ``<trans-abstract>`` e ``<kwd-group>``.
"""

from packtools.sps.formats.pdf.extract.context import context
from packtools.sps.formats.pdf.extract.flow import flow, styled_paragraph
from packtools.sps.formats.pdf.extract.inline import inlines
from packtools.sps.formats.pdf.extract.runs import normalize, tag, text_run


# -----------------
# ``<abstract>`` e ``<trans-abstract>``: resumos da capa.
# -----------------


def abstract_blocks(node, lang, kwd_group=None):
    """
    Blocos de um resumo.

    Parâmetros
    ----------
    node : lxml.etree._Element
        ``<abstract>`` ou ``<trans-abstract>``.
    lang : str
        Idioma do resumo (títulos padrão de figuras, listas... dentro dele).
    kwd_group : lxml.etree._Element, opcional
        ``<kwd-group>`` do mesmo idioma, posto logo depois do resumo.

    Retorna
    -------
    list of dict
        Título do resumo (papel ``abstract_title``), o conteúdo (papel
        ``abstract``; em resumo estruturado, cada subseção vira "Título:
        texto") e as palavras-chave.
    """
    title = node.find("title")
    # título com a formatação do XML (itálico de nome científico etc.)
    heading = styled_paragraph(normalize(inlines(title)), "abstract_title") if title is not None else []
    ctx = context(role="abstract", inline_titles=True, lang=lang)
    body = flow(node, ctx, skip=[title] if title is not None else ())
    return heading + body + keywords_block(kwd_group)


def abstracts_blocks(abstracts, kwd_groups):
    """
    Blocos de todos os resumos, cada um com as palavras-chave do seu idioma.

    Parâmetros
    ----------
    abstracts : list of (lxml.etree._Element, str)
        Resumos e seus idiomas, na ordem de exibição (ver languages.py).
    kwd_groups : list of (lxml.etree._Element, str)
        Grupos de palavras-chave e seus idiomas.

    Retorna
    -------
    list of dict
        Blocos dos resumos; um ``<kwd-group>`` sem resumo do mesmo idioma
        sai sozinho no fim, para não se perder.
    """
    remaining = list(kwd_groups)
    blocks = []
    for node, lang in abstracts:
        match = next((pair for pair in remaining if pair[1] == lang), None)
        if match is not None:
            remaining.remove(match)
        blocks += abstract_blocks(node, lang, match[0] if match else None)
    for group, _ in remaining:
        blocks += keywords_block(group)
    return blocks


# -----------------
# ``<kwd-group>`` e ``<kwd>``: palavras-chave da capa.
# -----------------


def keywords_block(group):
    """
    Parágrafo das palavras-chave de um grupo.

    Parâmetros
    ----------
    group : lxml.etree._Element or None
        ``<kwd-group>``.

    Retorna
    -------
    list of dict
        Um parágrafo "Título: palavra, palavra, ...", com o título no estilo
        de caractere ``keywords_title_char`` e as palavras (itálico etc.
        preservados) em ``keywords_char``; vazio sem grupo ou sem palavras.
    """
    if group is None:
        return []
    words = [normalize(inlines(kwd)) for kwd in group if tag(kwd) in ("kwd", "compound-kwd")]
    if not words:
        return []
    title = group.find("title")
    runs = normalize(inlines(title)) if title is not None else []
    if runs:
        # título com a formatação do XML, todo no estilo de caractere do
        # título; o espaço antes das palavras fica no mesmo run (normalize)
        runs = normalize(runs + [text_run(" ")], preserve_space=True)
        runs = [dict(r, char_role="keywords_title_char") for r in runs]
    for index, word in enumerate(words):
        runs += ([text_run(", ")] if index else []) + word
    return styled_paragraph(runs, "keywords", "keywords_char")
