import copy

import mathml2omml
from lxml import etree

_OMML_NS = 'http://schemas.openxmlformats.org/officeDocument/2006/math'
_W_NS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'


def normalize_empty_base_superscripts(math_element):
    """Funde um `<msup>` de base vazia (`<mrow/>`) com o irmão anterior, evitando um glyph de caixa vazia na conversão.

    Args:
        math_element (lxml.etree._Element): The `<mml:math>` node.

    Returns:
        lxml.etree._Element: A deep copy of `math_element` with the fix
        applied wherever the pattern is found.
    """
    root = copy.deepcopy(math_element)
    # lista materializada antes de mutar: iterar e mover na mesma passada pula item alternado
    candidate_msups = [
        el for el in root.iter()
        if isinstance(el.tag, str) and etree.QName(el).localname == 'msup'
    ]
    for msup in candidate_msups:
        children = list(msup)
        if len(children) != 2:
            continue
        base = children[0]
        if etree.QName(base).localname != 'mrow' or len(base) or (base.text or '').strip():
            continue
        previous = msup.getprevious()
        if previous is None:
            continue
        parent = msup.getparent()
        parent.remove(previous)
        msup.replace(base, previous)
    return root


def _strip_namespace(element):
    """Remove o prefixo de namespace de cada tag: o parser SAX do mathml2omml espera nomes locais puros (`math`, não `{...}math`)."""
    stripped = copy.deepcopy(element)
    for el in stripped.iter():
        if isinstance(el.tag, str) and '}' in el.tag:
            el.tag = el.tag.split('}', 1)[1]
    etree.cleanup_namespaces(stripped)
    return stripped


def _normalize_plain_style_runs(omml_element):
    """LibreOffice não quebra linha entre linhas de m:m/m:eqArr quando o
    último run de uma linha tem `<m:sty m:val="p"/>`; troca por `<m:nor/>`
    (mesmo significado - texto normal, sem itálico) em todo o documento.
    """
    rpr_tag = f'{{{_OMML_NS}}}rPr'
    sty_tag = f'{{{_OMML_NS}}}sty'
    val_attr = f'{{{_OMML_NS}}}val'
    for rpr in omml_element.iter(rpr_tag):
        sty = rpr.find(sty_tag)
        if sty is not None and sty.get(val_attr) == 'p':
            rpr.remove(sty)
            etree.SubElement(rpr, f'{{{_OMML_NS}}}nor')
    return omml_element


def match_paragraph_font(omml_element, size_pt, font_name):
    """Define w:sz/w:szCs/w:rFonts em cada run do OMML.

    Zona de matemática não herda tamanho nem fonte do parágrafo: sem isso,
    renderiza maior (tamanho padrão da zona de fórmula) e com um fallback
    de fonte de matemática mais largo que o corpo do texto (ex.: Cambria
    Math, ausente no sistema, cai para Latin Modern Math) - a combinação
    estoura a largura da coluna mesmo depois de corrigir só o tamanho.

    Args:
        omml_element (lxml.etree._Element): The `<m:oMath>` node, mutated in place.
        size_pt (float): Target font size in points (e.g. `paragraph.style.font.size.pt`).
        font_name (str): Target font family (e.g. `paragraph.style.font.name`).

    Returns:
        lxml.etree._Element: The same `omml_element`, for chaining.
    """
    half_points = str(int(round(size_pt * 2)))
    r_tag = f'{{{_OMML_NS}}}r'
    rpr_tag = f'{{{_OMML_NS}}}rPr'
    w_val_attr = f'{{{_W_NS}}}val'
    for run in omml_element.iter(r_tag):
        # CT_R (OOXML §22.1.2.85): m:rPr? seguido de w:rPr? - w:rPr é irmão
        # de m:rPr dentro de m:r, não filho dele; aninhado dentro de m:rPr
        # o LibreOffice ignora silenciosamente (tamanho/fonte não aplicam).
        w_rpr = etree.Element(f'{{{_W_NS}}}rPr', nsmap={'w': _W_NS})
        etree.SubElement(w_rpr, f'{{{_W_NS}}}sz').set(w_val_attr, half_points)
        etree.SubElement(w_rpr, f'{{{_W_NS}}}szCs').set(w_val_attr, half_points)
        rfonts = etree.SubElement(w_rpr, f'{{{_W_NS}}}rFonts')
        for attr in ('ascii', 'hAnsi', 'cs', 'eastAsia'):
            rfonts.set(f'{{{_W_NS}}}{attr}', font_name)

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
        mathml_str = etree.tostring(stripped, encoding='unicode', with_tail=False)
        omml_str = mathml2omml.convert(mathml_str)
    except Exception:
        return None

    omml_str = omml_str.replace('<m:oMath>', f'<m:oMath xmlns:m="{_OMML_NS}">', 1)
    try:
        omml = etree.fromstring(omml_str.encode('utf-8'))
    except etree.XMLSyntaxError:
        return None
    return _normalize_plain_style_runs(omml)
