"""
``<article-meta>`` (e ``<journal-meta>``): metadados, título e blocos da capa.
"""

from packtools.sps.formats.pdf.extract import citation, nodes
from packtools.sps.formats.pdf.extract.abstract import abstracts_blocks
from packtools.sps.formats.pdf.extract.contrib_group import (
    aff_blocks,
    author_notes_blocks,
    authors_block,
)
from packtools.sps.formats.pdf.extract.flow import styled_paragraph
from packtools.sps.formats.pdf.extract.inline import inlines, plain_text
from packtools.sps.formats.pdf.extract.runs import normalize, runs_text, text_run


# -----------------
# ``<article-meta>`` (e ``<journal-meta>``): metadados e blocos da capa.
# -----------------
# `extract_meta` devolve um dict plano, sem sub-dicts, com o que o render usa
# no cabeçalho, no rodapé e na citação. `front_blocks` devolve a capa como uma
# lista de blocos do mesmo formato do corpo (parágrafos com papel de estilo),
# na ordem de exibição.


# Herdado do old_pdf: o ano do rodapé é o da data de coleção eletrônica
# (o fascículo); as demais são alternativas para XML sem ela.
_PUB_DATES = (
    "pub-date[@date-type='collection'][@publication-format='electronic']",
    "pub-date[@date-type='collection']",
    "pub-date[@date-type='pub']",
    "pub-date",
)


def extract_meta(view, citation_style="vancouver"):
    """
    Metadados do cabeçalho, do rodapé e da citação.

    Parâmetros
    ----------
    view : dict
        Visão do documento (ver languages.py).
    citation_style : str, opcional
        Estilo da citação montada (ver citation.build_citation).

    Retorna
    -------
    dict
        Chaves: ``lang``, ``journal_title``, ``abbrev_journal_title``,
        ``doi``, ``article_type``, ``category``, ``title_text``,
        ``volume``, ``issue``, ``fpage``, ``lpage``, ``elocation_id``,
        ``year``, ``location_label`` e ``cite_as``. Todos os valores são
        texto (vazio quando ausente).
    """
    root, meta = view["root"], view["meta"]
    journal = root.find("front/journal-meta")
    pub_date = next((d for d in (nodes.find(meta, p) for p in _PUB_DATES) if d is not None), None)
    data = {
        "lang": view["lang"] or "",
        "journal_title": plain_text(journal.find(".//journal-title")) if journal is not None else "",
        "abbrev_journal_title": plain_text(journal.find(".//abbrev-journal-title")) if journal is not None else "",
        "doi": plain_text(nodes.find(meta, 'article-id[@pub-id-type="doi"]')),
        "article_type": root.get("article-type", ""),
        "category": plain_text(
            nodes.find(meta, 'article-categories//subj-group[@subj-group-type="heading"]/subject')
        ),
        "title_text": runs_text(article_title_runs(nodes.find(meta, "title-group"))),
        "volume": plain_text(nodes.find(meta, "volume")),
        "issue": plain_text(nodes.find(meta, "issue")),
        "fpage": plain_text(nodes.find(meta, "fpage")),
        "lpage": plain_text(nodes.find(meta, "lpage")),
        "elocation_id": plain_text(nodes.find(meta, "elocation-id")),
        "year": plain_text(pub_date.find("year")) if pub_date is not None else "",
    }
    # Herdado do old_pdf: artigo de publicação contínua não tem fpage/lpage, e
    # sim elocation-id, que ocupa o mesmo lugar no rodapé e na citação.
    if data["fpage"]:
        data["location_label"] = "-".join(v for v in (data["fpage"], data["lpage"]) if v)
    else:
        data["location_label"] = data["elocation_id"]
    data["cite_as"] = citation.cite_as_text(citation.cite_as_note(view)) or citation.build_citation(
        data, meta, citation_style
    )
    return data


def front_blocks(view, meta_data, cite_note):
    """
    Blocos da capa, na ordem de exibição.

    Parâmetros
    ----------
    view : dict
        Visão do documento (ver languages.py).
    meta_data : dict
        Metadados (ver `extract_meta`).
    cite_note : lxml.etree._Element or None
        Nota "como citar", que não se repete nas notas de autor.

    Retorna
    -------
    list of dict
        Categoria | tipo, título, autores, afiliações, notas de autor e,
        para cada resumo, título, conteúdo e palavras-chave.
    """
    meta = view["meta"]
    category = " | ".join(v for v in (meta_data["category"], meta_data["article_type"]) if v)
    return (
        styled_paragraph([text_run(category)], "article_category")
        + styled_paragraph(article_title_runs(nodes.find(meta, "title-group")), "article_title")
        + authors_block(meta)
        + aff_blocks(meta)
        + author_notes_blocks(meta, cite_note)
        + abstracts_blocks(view["abstracts"], view["kwd_groups"])
    )


# -----------------
# ``<title-group>``: título do artigo (``<article-title>`` e ``<subtitle>``).
# -----------------


def article_title_runs(title_group):
    """
    Monta o título do artigo.

    Parâmetros
    ----------
    title_group : lxml.etree._Element or None
        ``<title-group>`` do article-meta ou do front-stub.

    Retorna
    -------
    list of dict
        Runs do ``<article-title>`` (itálico, sobrescrito etc. preservados),
        com o ``<subtitle>`` depois de ": "; vazio sem título.
    """
    if title_group is None:
        return []
    title = title_group.find("article-title")
    runs = inlines(title) if title is not None else []
    subtitle = title_group.find("subtitle")
    if subtitle is not None:
        runs += [text_run(": ")] + inlines(subtitle)
    return normalize(runs)
