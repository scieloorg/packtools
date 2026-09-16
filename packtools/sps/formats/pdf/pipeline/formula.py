import copy

import mathml2omml
from lxml import etree

_OMML_NS = 'http://schemas.openxmlformats.org/officeDocument/2006/math'


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
