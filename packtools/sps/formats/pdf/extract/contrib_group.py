"""
Autores da capa: ``<contrib-group>``, ``<aff>`` e ``<author-notes>``.
"""

import re

from packtools.sps.formats.pdf.extract import nodes
from packtools.sps.formats.pdf.extract.flow import styled_paragraph
from packtools.sps.formats.pdf.extract.inline import inlines, plain_text
from packtools.sps.formats.pdf.extract.link import rid
from packtools.sps.formats.pdf.extract.runs import (
    bookmark_runs,
    normalize,
    runs_text,
    tag,
    text_run,
)
from packtools.sps.formats.pdf.extract.title import label_of, note_label_runs

_LEADING_MARK = re.compile(r"^([*†‡§¶#]+|\d+)\s")


# -----------------
# ``<contrib-group>`` e ``<contrib>``: autores da capa.
# -----------------


def contrib_name(contrib):
    """
    Nome de um ``<contrib>``.

    Parâmetros
    ----------
    contrib : lxml.etree._Element
        ``<contrib>``.

    Retorna
    -------
    str
        "Prefixo Nomes Sobrenome Sufixo" de ``<name>``; ou o texto de
        ``<string-name>``/``<collab>``; vazio sem nome.
    """
    name = contrib.find("name")
    if name is not None:
        parts = [plain_text(name.find(t)) for t in ("prefix", "given-names", "surname", "suffix")]
        return " ".join(p for p in parts if p)
    for alternative in ("string-name", "collab", "name-alternatives/name"):
        if contrib.find(alternative) is not None:
            return plain_text(contrib.find(alternative))
    return ""


def marks(contrib, aff_labels):
    """
    Marcas sobrescritas de um autor.

    Parâmetros
    ----------
    contrib : lxml.etree._Element
        ``<contrib>``.
    aff_labels : dict
        ``@id`` da afiliação -> rótulo, para ``<xref>`` sem texto.

    Retorna
    -------
    list of dict
        Texto de cada ``<xref>`` (ou o rótulo da afiliação; "*" para
        correspondência), separados por vírgula, com ``anchor`` = ``@rid``:
        viram links para a afiliação e para a nota de correspondência.
        Todas as afiliações entram (o old_pdf usava só a primeira); a marca
        de correspondência vai no fim.
    """
    found, corresp = [], []
    for xref in contrib.iter("xref"):
        text = plain_text(xref)
        target = rid(xref)
        anchor = {"anchor": target} if target else {}
        if xref.get("ref-type") == "corresp":
            corresp = [text_run(text or "*", **anchor)]
        elif text or aff_labels.get(xref.get("rid")):
            if found:
                found.append(text_run(","))
            found.append(text_run(text or aff_labels[xref.get("rid")], **anchor))
    return found + corresp


def authors_block(meta):
    """
    Parágrafo dos autores.

    Parâmetros
    ----------
    meta : list of lxml.etree._Element
        Filhos do article-meta (ver languages.py).

    Retorna
    -------
    list of dict
        Um parágrafo "Nome¹, Nome² and Nome³", marcas sobrescritas, ou lista
        vazia sem autores. Inclui ``<suffix>`` e ``<collab>``.
    """
    aff_labels = {aff.get("id"): plain_text(aff.find("label")) for aff in nodes.iter_all(meta, "aff")}
    authors = [c for c in nodes.iter_all(meta, "contrib") if contrib_name(c)]
    runs = []
    for index, contrib in enumerate(authors):
        runs.append(text_run(contrib_name(contrib)))
        runs += [dict(mark, superscript=True) for mark in marks(contrib, aff_labels)]
        if index <= len(authors) - 3:
            runs.append(text_run(", "))
        elif index == len(authors) - 2:
            runs.append(text_run(" and "))
    return styled_paragraph(runs, "author", "author_char")


# -----------------
# ``<aff>``: afiliações da capa.
# -----------------


def aff_text(aff):
    """
    Texto de uma afiliação.

    Parâmetros
    ----------
    aff : lxml.etree._Element
        ``<aff>``.

    Retorna
    -------
    str
        ``<institution content-type="original">``; sem ela, as partes da
        ``<aff>`` (exceto o rótulo) separadas por vírgula. O old_pdf
        descartava a afiliação sem a versão "original".
    """
    original = aff.find('institution[@content-type="original"]')
    if original is not None:
        return plain_text(original)
    parts = [aff.text or ""] + [_part(item) for item in aff if tag(item) not in ("label", None)]
    return ", ".join(" ".join(p.split()) for p in parts if p and p.strip(" ,"))


def _part(node):
    """Texto de uma parte da ``<aff>``; ``<addr-line>`` com filhos vira "cidade, estado"."""
    if tag(node) == "addr-line" and len(node):
        return ", ".join(plain_text(c) for c in node if tag(c) and plain_text(c))
    return plain_text(node).strip(" ,")


def aff_blocks(meta):
    """
    Parágrafos das afiliações.

    Parâmetros
    ----------
    meta : list of lxml.etree._Element
        Filhos do article-meta (ver languages.py).

    Retorna
    -------
    list of dict
        Um parágrafo por ``<aff>`` com texto: marca do ``@id`` (alvo das
        marcas dos autores), rótulo sobrescrito e o texto.
    """
    blocks = []
    for aff in nodes.iter_all(meta, "aff"):
        text = aff_text(aff)
        if not text:
            continue
        label = plain_text(aff.find("label"))
        runs = bookmark_runs(aff) + ([text_run(label, superscript=True)] if label else [])
        # o espaço separa o rótulo sobrescrito do texto; sem rótulo, não há o que separar
        blocks += styled_paragraph(runs + [text_run(f" {text}" if label else text)], "affiliation", "affiliation_char")
    return blocks


# -----------------
# ``<author-notes>``, ``<corresp>`` e suas ``<fn>``: notas de autor da capa.
# -----------------


def leading_mark_superscript(runs):
    """'* Autor...' -> '*' sobrescrito + ' Autor...' (como no old_pdf)."""
    if not runs or "text" not in runs[0]:
        return runs
    match = _LEADING_MARK.match(runs[0]["text"])
    if not match:
        return runs
    first = runs[0]
    return [
        dict(first, text=match.group(1), superscript=True),
        dict(first, text=first["text"][match.end(1):]),
    ] + runs[1:]


def corresp_runs(runs, node, meta):
    """
    Completa a nota de correspondência.

    Parâmetros
    ----------
    runs : list of dict
        Runs do ``<corresp>``.
    node : lxml.etree._Element
        ``<corresp>``.
    meta : list of lxml.etree._Element
        Filhos do article-meta (para achar o ORCID do autor correspondente).

    Retorna
    -------
    list of dict
        Com só o e-mail no ``<corresp>``, "* Corresponding author: e-mail";
        e o ORCID do autor correspondente no fim, se ainda não estiver no texto.
    """
    email = plain_text(node.find(".//email"))
    text = runs_text(runs)
    if email and text.strip(" *") == email:
        runs = (
            [text_run("* ", superscript=True), text_run("Corresponding author: ")]
            + [r for r in runs if r.get("text", "").strip(" *")]
        )
    for contrib in nodes.iter_all(meta, "contrib"):
        if contrib.find('xref[@ref-type="corresp"]') is not None:
            orcid = plain_text(contrib.find('contrib-id[@contrib-id-type="orcid"]'))
            if orcid and orcid not in text:
                runs.append(text_run(f"; https://orcid.org/{orcid}"))
    return runs


def author_notes_blocks(meta, cite_note):
    """
    Parágrafos das notas de autor.

    Parâmetros
    ----------
    meta : list of lxml.etree._Element
        Filhos do article-meta (ver languages.py).
    cite_note : lxml.etree._Element or None
        Nota "como citar", que vai para o rodapé e não se repete aqui.

    Retorna
    -------
    list of dict
        Um parágrafo por filho de ``<author-notes>`` (``<corresp>``,
        ``<fn>``, ``<p>``...), com a marca do ``@id`` (alvo das marcas dos
        autores) e o rótulo como em label.note_label_runs.
    """
    blocks = []
    for group in nodes.findall(meta, "author-notes"):
        for node in group:
            if tag(node) in (None, "title", "label") or node is cite_note:
                continue
            label = label_of(node)
            if label is None:
                runs = leading_mark_superscript(normalize(inlines(node)))
            else:
                runs = normalize(note_label_runs(label) + inlines(node, skip=[label]))
            if tag(node) == "corresp":
                runs = corresp_runs(runs, node, meta)
            blocks += styled_paragraph(
                bookmark_runs(node) + runs if runs else runs, "affiliation", "affiliation_char"
            )
    return blocks
