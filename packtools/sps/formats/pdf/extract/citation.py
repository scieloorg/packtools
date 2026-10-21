"""
Citação do rodapé ("CITE AS"): a nota "como citar" do XML ou, sem ela, a
citação montada pelos metadados (citeproc-py + CSL).
"""

from citeproc import (
    Citation,
    CitationItem,
    CitationStylesBibliography,
    CitationStylesStyle,
    formatter,
)
from citeproc.source.json import CiteProcJSON

from packtools.sps.formats.pdf.extract import languages, nodes
from packtools.sps.formats.pdf.extract.inline import plain_text
from packtools.sps.formats.pdf.config.citation import (
    CITATION_STYLES,
    CITATION_STYLES_DIR,
    CITE_AS_LEADING_RE,
    CITE_AS_RE,
)


def cite_as_note(view):
    """
    Acha a nota "como citar este artigo".

    Parâmetros
    ----------
    view : dict
        Visão do documento (ver languages.py).

    Retorna
    -------
    lxml.etree._Element or None
        A primeira ``<fn fn-type="other">`` cujo rótulo (ou o início do
        ``<p>``) a identifica como "como citar" (ver config/citation.py).
    """
    for fn in languages.iter_tag(view, "fn"):
        if fn.get("fn-type") != "other" or fn.find("p") is None:
            continue
        label = fn.find("label")
        signal = plain_text(label) if label is not None else plain_text(fn.find("p"))[:40]
        if CITE_AS_RE.search(signal):
            return fn
    return None


def cite_as_text(fn):
    """Texto da nota "como citar"; sem ``<label>``, tira a frase inicial ("Como citar:") do ``<p>``."""
    if fn is None:
        return ""
    text = plain_text(fn.find("p"))
    return text if fn.find("label") is not None else CITE_AS_LEADING_RE.sub("", text, count=1)


def citation_authors(meta):
    """
    Autores no formato da citação.

    Parâmetros
    ----------
    meta : list of lxml.etree._Element
        Filhos do article-meta (ver languages.py).

    Retorna
    -------
    list of str
        "Sobrenome INICIAIS" de cada autor do primeiro ``<contrib-group>``.

    Notas
    -----
    Herdado do old_pdf (#1350): só autores entram (contrib-type "author" ou
    sem tipo); tradutor, editor e outros contribuidores não. Partículas
    ("da", "de", "dos") não viram inicial: "Bárbara Passos da Silva" -> "BPS".
    """
    group = next(nodes.iter_all(meta, "contrib-group"), None)
    authors = []
    for contrib in group.iter("contrib") if group is not None else ():
        if contrib.get("contrib-type", "author") != "author":
            continue
        surname = plain_text(contrib.find("name/surname"))
        if not surname:
            continue
        given = plain_text(contrib.find("name/given-names"))
        initials = "".join(w[0].upper() for w in given.split() if w[:1].isupper())
        authors.append(f"{surname} {initials}".strip())
    return authors


def build_citation(meta_data, meta, style="vancouver", csl_type="article-journal"):
    """
    Monta a citação pelos metadados, usada quando não há nota "como citar".

    Parâmetros
    ----------
    meta_data : dict
        Metadados já extraídos (ver article_meta.extract_meta): título,
        periódico, volume, número, local, ano e DOI.
    meta : list of lxml.etree._Element
        Filhos do article-meta (para os autores).
    style : str, opcional
        Estilo (chave de config/citation.CITATION_STYLES).
    csl_type : str, opcional
        Tipo do item CSL.

    Retorna
    -------
    str
        Citação formatada; vazia sem estilo conhecido ou sem autores.
    """
    csl_file = CITATION_STYLES.get(style)
    authors = citation_authors(meta)
    if not csl_file or not authors:
        return ""
    reference = {
        "id": "cite-as",
        "type": csl_type,
        # Herdado do old_pdf: nomes "literal", já no formato final, porque o
        # parser de nomes do CSL não conhece as partículas do português.
        "author": [{"literal": a} for a in authors],
    }
    optional = {
        "title": meta_data["title_text"],
        "container-title": meta_data["abbrev_journal_title"] or meta_data["journal_title"],
        "volume": meta_data["volume"],
        "issue": meta_data["issue"],
        "page": meta_data["location_label"],
        "DOI": meta_data["doi"],
    }
    reference.update({k: v for k, v in optional.items() if v})
    if meta_data["year"]:
        reference["issued"] = {"date-parts": [[meta_data["year"]]]}

    style_obj = CitationStylesStyle(str(CITATION_STYLES_DIR / csl_file), validate=False)
    bibliography = CitationStylesBibliography(style_obj, CiteProcJSON([reference]), formatter.plain)
    citation = Citation([CitationItem("cite-as")])
    bibliography.register(citation)
    bibliography.cite(citation, lambda missing: None)
    entries = list(bibliography.bibliography())
    return str(entries[0]) if entries else ""
