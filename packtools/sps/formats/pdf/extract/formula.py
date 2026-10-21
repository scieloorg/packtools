"""
Fórmulas: conversão MathML -> OMML, ``<inline-formula>``/``<mml:math>`` e
``<disp-formula>``.
"""

import copy
import re

import mathml2omml

from lxml import etree

from packtools.sps.formats.pdf.extract.flow import flow, paragraph
from packtools.sps.formats.pdf.extract.graphic import figure_block, graphics
from packtools.sps.formats.pdf.extract.inline import inlines
from packtools.sps.formats.pdf.extract.registry import block_handler, inline_handler
from packtools.sps.formats.pdf.extract.runs import MATHML, tag, text_runs
from packtools.sps.formats.pdf.extract.title import after_runs, caption_runs


# -----------------
# MathML -> OMML (o formato de fórmula do Word)
# -----------------


_OMML_NS = "http://schemas.openxmlformats.org/officeDocument/2006/math"
_W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"


def detached_copy(element):
    """
    Cópia independente de um elemento, sem o tail.

    Parâmetros
    ----------
    element : lxml.etree._Element
        Elemento do XML do artigo.

    Retorna
    -------
    lxml.etree._Element
        Nova árvore com o mesmo conteúdo. A conversão de fórmula precisa
        alterar o MathML (normalizações abaixo) e o XML do artigo não pode
        mudar; esta é a única cópia feita na extração.
    """
    return etree.fromstring(etree.tostring(element, with_tail=False))


def normalize_empty_base_superscripts(math_element):
    """Funde um `<msup>` de base vazia (`<mrow/>`) com o irmão anterior, evitando um glyph de caixa vazia na conversão.

    Args:
        math_element (lxml.etree._Element): The `<mml:math>` node.

    Returns:
        lxml.etree._Element: A copy of `math_element` (see detached_copy)
        with the fix applied wherever the pattern is found.
    """
    root = detached_copy(math_element)
    # lista materializada antes de mutar: iterar e mover na mesma passada pula item alternado
    candidate_msups = [
        el
        for el in root.iter()
        if isinstance(el.tag, str) and etree.QName(el).localname == "msup"
    ]
    for msup in candidate_msups:
        children = list(msup)
        if len(children) != 2:
            continue
        base = children[0]
        if (
            etree.QName(base).localname != "mrow"
            or len(base)
            or (base.text or "").strip()
        ):
            continue
        previous = msup.getprevious()
        if previous is None:
            continue
        parent = msup.getparent()
        parent.remove(previous)
        msup.replace(base, previous)
    return root


def _strip_namespace(element):
    """
    Remove o prefixo de namespace de cada tag, no lugar.

    O parser SAX do mathml2omml espera nomes locais puros (`math`, não
    `{...}math`). Recebe a cópia feita por normalize_empty_base_superscripts,
    então pode alterá-la sem copiar de novo.
    """
    for el in element.iter():
        if isinstance(el.tag, str) and "}" in el.tag:
            el.tag = el.tag.split("}", 1)[1]
    etree.cleanup_namespaces(element)
    return element


# com <m:nor/> o LibreOffice escreve parêntese e chave com barra: "\(", "\{"
_BRACKETS = re.compile(r"([(){}]+)")


def _normalize_plain_style_runs(omml_element):
    """LibreOffice não quebra linha entre linhas de m:m/m:eqArr quando o
    último run de uma linha tem `<m:sty m:val="p"/>`, e troca "-", "[",
    "|", "*" e outros por um glyph inválido; troca por `<m:nor/>` (mesmo
    significado - texto normal, sem itálico) em todo o documento.

    Parênteses e chaves são a exceção: com `<m:nor/>` o LibreOffice os
    escreve com barra, "ln \\( P R R \\)" (vem de `<mo stretchy="false">`)
    e "concentration \\(mg/L\\)" (vem de `<mtext>`, que o mathml2omml já
    gera com `<m:nor/>`); com `m:sty p` saem certos, também no fim da
    linha. O run de texto que os contém é dividido, e só eles ficam com
    `m:sty p`.
    """
    m = f"{{{_OMML_NS}}}"
    for run in list(omml_element.iter(f"{m}r")):
        rpr = run.find(f"{m}rPr")
        if rpr is None:
            continue
        sty = rpr.find(f"{m}sty")
        if sty is not None and sty.get(f"{m}val") == "p":
            rpr.remove(sty)
            etree.SubElement(rpr, f"{m}nor")
        if rpr.find(f"{m}nor") is not None:
            _split_brackets(run)
    return omml_element


def _split_brackets(run):
    """Divide um run `<m:nor/>` para que parênteses e chaves fiquem em runs `m:sty p` (ver _normalize_plain_style_runs)."""
    m = f"{{{_OMML_NS}}}"
    text = "".join(t.text or "" for t in run.iter(f"{m}t"))
    if not _BRACKETS.search(text):
        return
    parts = []
    for piece in _BRACKETS.split(text):
        if not piece:
            continue
        part = etree.Element(f"{m}r")
        rpr = copy.deepcopy(run.find(f"{m}rPr"))
        for style in rpr.findall(f"{m}sty") + rpr.findall(f"{m}nor"):
            rpr.remove(style)
        part.append(rpr)
        if _BRACKETS.fullmatch(piece):
            etree.SubElement(rpr, f"{m}sty").set(f"{m}val", "p")
        else:
            etree.SubElement(rpr, f"{m}nor")
        t = etree.SubElement(part, f"{m}t")
        t.text = piece
        t.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
        parts.append(part)
    parent = run.getparent()
    index = parent.index(run)
    parent.remove(run)
    for offset, part in enumerate(parts):
        parent.insert(index + offset, part)


# mathml2omml 0.0.2 fecha <m:groupChrPr> com </m:groupChr> (XML inválido)
_UNCLOSED_GROUP_CHR_PR = re.compile(
    r'(<m:groupChrPr><m:chr m:val="[^"]*"/><m:pos m:val="(?:top|bot)"/>)</m:groupChr>'
)

# caracteres que o LibreOffice desenha certo em <m:bar>/<m:acc>; "˜", "∼" e "·" sairiam como apóstrofo
_BAR_CHARS = {"¯", "ˉ", "―", "-", "−", "_", "̅"}
_ACCENT_CHARS = {
    "→": "→",
    "^": "^",
    "̂": "̂",
    "~": "~",
    "̃": "̃",
    "˜": "~",
    "∼": "~",
    "̇": "̇",
    "˙": "˙",
    "·": "˙",
    "̈": "̈",
    "¨": "¨",
    "`": "`",
    "´": "´",
}


def _close_group_chr_pr(omml_str):
    """Fecha o ``<m:groupChrPr>`` que o mathml2omml deixa aberto (ver _UNCLOSED_GROUP_CHR_PR)."""
    return _UNCLOSED_GROUP_CHR_PR.sub(r"\1</m:groupChrPr>", omml_str)


def _normalize_group_chars(omml_element):
    """
    Troca o ``<m:groupChr>`` de barra ou acento acima da base por ``<m:bar>`` ou ``<m:acc>``.

    Parâmetros
    ----------
    omml_element : lxml.etree._Element
        O ``<m:oMath>``, alterado no lugar.

    Retorna
    -------
    lxml.etree._Element
        O mesmo ``omml_element``.

    Notas
    -----
    O mathml2omml converte ``<mover>`` de acento esticável em
    ``<m:groupChr>``. No LibreOffice, "P̄R" (a24.xml, Eq. 5) sai com um
    traço curto acima do centro; com ``<m:bar>`` e ``<m:acc>`` o sinal sai
    sobre a base inteira.
    """
    m = f"{{{_OMML_NS}}}"
    val = f"{m}val"
    for element in list(omml_element.iter(f"{m}groupChr")):
        base = element.find(f"{m}e")
        char = element.find(f"{m}groupChrPr/{m}chr")
        pos = element.find(f"{m}groupChrPr/{m}pos")
        if base is None or char is None or pos is None or pos.get(val) != "top":
            continue
        char = char.get(val)
        if char in _BAR_CHARS:
            new = etree.Element(f"{m}bar")
            etree.SubElement(etree.SubElement(new, f"{m}barPr"), f"{m}pos").set(val, "top")
        elif char in _ACCENT_CHARS:
            new = etree.Element(f"{m}acc")
            etree.SubElement(etree.SubElement(new, f"{m}accPr"), f"{m}chr").set(
                val, _ACCENT_CHARS[char]
            )
        else:
            continue
        new.append(base)
        element.getparent().replace(element, new)
    return omml_element


def _normalize_radicals(omml_element):
    """
    Completa cada ``<m:rad>`` sem ``<m:deg>``, como o mathml2omml gera para ``<msqrt>``.

    Parâmetros
    ----------
    omml_element : lxml.etree._Element
        O ``<m:oMath>``, alterado no lugar.

    Retorna
    -------
    lxml.etree._Element
        O mesmo ``omml_element``.

    Notas
    -----
    O schema OMML exige ``<m:deg>`` (índice da raiz) antes de ``<m:e>``;
    raiz quadrada leva ``<m:deg/>`` vazio e ``<m:radPr><m:degHide m:val="1"/>``.
    Sem eles o LibreOffice desenha um índice vazio e não mostra o radicando:
    "U = ⁿ√□" no lugar de "U = √(Σ nᵢ²)" (a1.xml, Table S1).
    """
    deg_tag = f"{{{_OMML_NS}}}deg"
    rad_pr_tag = f"{{{_OMML_NS}}}radPr"
    for rad in omml_element.iter(f"{{{_OMML_NS}}}rad"):
        if rad.find(deg_tag) is not None:
            continue
        rad_pr = rad.find(rad_pr_tag)
        if rad_pr is None:
            rad_pr = etree.Element(rad_pr_tag)
            rad.insert(0, rad_pr)
        etree.SubElement(rad_pr, f"{{{_OMML_NS}}}degHide").set(
            f"{{{_OMML_NS}}}val", "1"
        )
        rad_pr.addnext(etree.Element(deg_tag))
    return omml_element


def match_paragraph_font(omml_element, size_pt, font_name):
    """Define w:sz/w:szCs/w:rFonts em cada run do OMML, a partir do estilo do parágrafo.

    Args:
        omml_element (lxml.etree._Element): The `<m:oMath>` node, mutated in place.
        size_pt (float): Target font size in points (e.g. `paragraph.style.font.size.pt`).
        font_name (str): Target font family (e.g. `paragraph.style.font.name`).

    Returns:
        lxml.etree._Element: The same `omml_element`, for chaining.
    """
    half_points = str(int(round(size_pt * 2)))
    r_tag = f"{{{_OMML_NS}}}r"
    rpr_tag = f"{{{_OMML_NS}}}rPr"
    w_val_attr = f"{{{_W_NS}}}val"
    for run in omml_element.iter(r_tag):
        # w:rPr é irmão de m:rPr dentro de m:r (schema CT_R), não filho dele
        w_rpr = etree.Element(f"{{{_W_NS}}}rPr", nsmap={"w": _W_NS})
        etree.SubElement(w_rpr, f"{{{_W_NS}}}sz").set(w_val_attr, half_points)
        etree.SubElement(w_rpr, f"{{{_W_NS}}}szCs").set(w_val_attr, half_points)
        rfonts = etree.SubElement(w_rpr, f"{{{_W_NS}}}rFonts")
        for attr in ("ascii", "hAnsi", "cs", "eastAsia"):
            rfonts.set(f"{{{_W_NS}}}{attr}", font_name)

        m_rpr = run.find(rpr_tag)
        insert_at = list(run).index(m_rpr) + 1 if m_rpr is not None else 0
        run.insert(insert_at, w_rpr)
    return omml_element


def mathml_to_omml(math_element):
    """Converte um nó `<mml:math>` em `<m:oMath>` (OOXML), pronto para `paragraph._p.append(...)`.

    Args:
        math_element (lxml.etree._Element): The `<mml:math>` node to convert.

    Returns:
        lxml.etree._Element, or None if the MathML uses a construct
        mathml2omml doesn't support - callers should fall back to
        flattened text instead of propagating the exception.
    """
    try:
        normalized = normalize_empty_base_superscripts(math_element)
        stripped = _strip_namespace(normalized)
        mathml_str = etree.tostring(stripped, encoding="unicode", with_tail=False)
        omml_str = mathml2omml.convert(mathml_str)
    except Exception:
        return None

    omml_str = _close_group_chr_pr(omml_str)
    omml_str = omml_str.replace("<m:oMath>", f'<m:oMath xmlns:m="{_OMML_NS}">', 1)
    try:
        omml = etree.fromstring(omml_str.encode("utf-8"))
    except etree.XMLSyntaxError:
        return None
    omml = _normalize_group_chars(omml)
    return _normalize_radicals(_normalize_plain_style_runs(omml))


# -----------------
# ``<inline-formula>`` e ``<mml:math>``: fórmula no meio do texto.
# -----------------
# `formula_runs` é reaproveitado por ``<disp-formula>`` (abaixo).


@inline_handler("inline-formula", "math")
def formula_runs(node, fmt=frozenset()):
    """
    Converte uma fórmula em runs.

    Parâmetros
    ----------
    node : lxml.etree._Element
        ``<inline-formula>``, ``<disp-formula>`` ou o próprio ``<mml:math>``.
    fmt : frozenset of str, opcional
        Formatos ativos (usados só no texto de reserva).

    Retorna
    -------
    list of dict
        ``[{"omml": ...}]`` quando o MathML converte; senão o texto do
        ``<tex-math>`` ou do próprio MathML (nunca vazio por falha de
        conversão); sem MathML nem TeX, o conteúdo como texto.
    """
    math = node if tag(node) == "math" else next(node.iter(MATHML + "math"), None)
    if math is not None:
        omml = mathml_to_omml(math)
        if omml is not None:
            return [{"omml": omml}]
    tex = next((e for e in node.iter() if tag(e) == "tex-math"), None)
    source = tex if tex is not None else math
    if source is not None:
        return text_runs(" ".join("".join(source.itertext()).split()), fmt)
    return inlines(node, fmt)


# -----------------
# ``<disp-formula>``: fórmula em destaque.
# -----------------


# dentro de texto (título, célula de tabela) a fórmula em destaque vira fórmula inline
inline_handler("disp-formula")(formula_runs)


@block_handler("disp-formula")
def handle_disp_formula(node, ctx):
    """
    Converte uma fórmula em destaque.

    Parâmetros
    ----------
    node : lxml.etree._Element
        ``<disp-formula>``.
    ctx : dict
        Contexto.

    Retorna
    -------
    list of dict
        Conforme o conteúdo:

        - MathML convertido: bloco ``formula`` (OMML) com o rótulo depois;
        - MathML/TeX sem conversão: parágrafo com o texto da fórmula e o rótulo;
        - só imagem: figura com o rótulo como legenda;
        - outro conteúdo: fluxo genérico.
    """
    if any(tag(e) in ("math", "tex-math") for e in node.iter()):
        runs = formula_runs(node, ctx["fmt"])
        if "omml" in runs[0]:
            return [{"type": "formula", "runs": runs + after_runs(node)}]
        return paragraph(runs + after_runs(node), ctx)
    images = graphics(node)
    if images:
        return [figure_block(node, images[0], caption=caption_runs(node))]
    return flow(node, ctx)
