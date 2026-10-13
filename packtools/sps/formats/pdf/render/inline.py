"""Runs (dicts da extração) -> runs do python-docx num parágrafo existente."""

import re

from docx.opc.constants import RELATIONSHIP_TYPE as RT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt
from packtools.sps.formats.pdf.extract import formula
from packtools.sps.formats.pdf.render import styles

_MONOSPACE_FONT = "Courier New"


def add_runs(paragraph, runs, state, char_role=None, size=None, bold=None):
    """
    Escreve runs no parágrafo. char_role: estilo de caractere de todos os
    runs (um run com a chave 'char_role' usa o seu, ex. o título das
    palavras-chave); size/bold: formatação direta forçada (células de tabela). Runs com
    'href' viram hyperlink externo e runs com 'anchor' (de <xref>), link
    interno para a marca do alvo; run 'bookmark' é a marca (alvo de links);
    fórmula entra como OMML; imagem inline entra no tamanho natural limitado
    à largura de coluna.
    """
    char_style = styles.get(state.doc, char_role) if char_role else None
    link = None  # (destino, <w:hyperlink>) em aberto
    for run in runs:
        if "bookmark" in run:
            add_bookmark(paragraph, run["bookmark"], state)
            continue
        if "omml" in run:
            _add_formula(paragraph, run["omml"])
            link = None
            continue
        docx_run = paragraph.add_run()
        run_style = styles.get(state.doc, run["char_role"]) if run.get("char_role") else char_style
        if run_style is not None:
            docx_run.style = run_style
        if size:
            docx_run.font.size = Pt(size)
        if bold is not None:
            docx_run.bold = bold
        if run.get("break"):
            docx_run.add_break()
        elif "image" in run:
            if not state.add_inline_image(docx_run, run["image"]):
                docx_run.text = run.get("alt") or run["image"]
        else:
            docx_run.text = run["text"]
            _format(docx_run, run)
        target = ("href", run["href"]) if run.get("href") else (
            ("anchor", run["anchor"]) if run.get("anchor") else None
        )
        if target:
            if link is None or link[0] != target:
                link = (target, _hyperlink(paragraph, docx_run, *target))
            link[1].append(docx_run._r)
        else:
            link = None
    return paragraph


def bookmark_name(anchor):
    """
    Nome de marca válido no Word para um id do XML.

    Parâmetros
    ----------
    anchor : str
        ``@id`` do alvo (ou ``@rid`` do ``<xref>``).

    Retorna
    -------
    str
        Só letras, dígitos e "_", começando por letra, até 40 caracteres
        (regras do Word). O mesmo id gera sempre o mesmo nome, então o link
        (``w:anchor``) e a marca (``w:bookmarkStart``) se encontram.
    """
    name = re.sub(r"\W", "_", anchor)
    if not name[:1].isalpha():
        name = f"id_{name}"
    return name[:40]


def add_bookmark(paragraph, anchor, state):
    """
    Insere uma marca (alvo de link interno) na posição atual do parágrafo.

    Parâmetros
    ----------
    paragraph : docx.text.paragraph.Paragraph
        Parágrafo onde a marca entra (depois do que já foi escrito nele).
    anchor : str
        ``@id`` do elemento alvo.
    state : render.document.State
        Documento em construção; numera as marcas e ignora id repetido.
    """
    name = bookmark_name(anchor)
    if name in state.bookmarks:
        return
    state.bookmarks.add(name)
    number = str(len(state.bookmarks))
    for kind in ("w:bookmarkStart", "w:bookmarkEnd"):
        element = OxmlElement(kind)
        element.set(qn("w:id"), number)
        if kind == "w:bookmarkStart":
            element.set(qn("w:name"), name)
        paragraph._p.append(element)


def _format(docx_run, run):
    """Aplica ao run do python-docx os formatos marcados no run extraído."""
    # ausente: herda do estilo; False explícito desliga (texto da legenda, cujo estilo é negrito)
    if run.get("bold") is not None:
        docx_run.bold = run["bold"]
    if run.get("italic"):
        docx_run.italic = True
    if run.get("underline"):
        docx_run.underline = True
    if run.get("strike"):
        docx_run.font.strike = True
    if run.get("small_caps"):
        docx_run.font.small_caps = True
    if run.get("monospace"):
        docx_run.font.name = _MONOSPACE_FONT
    # mesmo atributo OOXML (w:vertAlign): mutuamente exclusivos
    if run.get("superscript"):
        docx_run.font.superscript = True
    elif run.get("subscript"):
        docx_run.font.subscript = True


def _hyperlink(paragraph, docx_run, kind, value):
    """<w:hyperlink> inserido antes do run: externo (kind "href", URL) ou interno (kind "anchor", id do alvo)."""
    hyperlink = OxmlElement("w:hyperlink")
    if kind == "anchor":
        hyperlink.set(qn("w:anchor"), bookmark_name(value))
    else:
        hyperlink.set(
            qn("r:id"), paragraph.part.relate_to(value, RT.HYPERLINK, is_external=True)
        )
    docx_run._r.addprevious(hyperlink)
    return hyperlink


def _add_formula(paragraph, omml):
    """OMML como XML bruto (python-docx não modela fórmula), com fonte/tamanho do estilo do parágrafo."""
    style = paragraph.style
    if (
        style is not None
        and style.font.size is not None
        and style.font.name is not None
    ):
        formula.match_paragraph_font(omml, style.font.size.pt, style.font.name)
    paragraph._p.append(omml)
