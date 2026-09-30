"""Ponte MathML -> segmento {'type': 'formula'} com OMML, para <disp-formula> e <inline-formula>."""

from packtools.sps.formats.pdf.ooxml import formula
from packtools.sps.formats.pdf.utils import xml_utils


INLINE_FORMULA_TAGS = {'inline-formula'}


def inline_formula_segment(inline_formula):
    """Converte o MathML de um <inline-formula> (fórmula no meio de texto corrido) em um segmento 'formula'.

    Ao contrário de <disp-formula>, não carrega <label> próprio (fase 2 de
    #1347, issue #1353).

    Args:
        inline_formula (ElementTree): The <inline-formula> element.

    Returns:
        dict, or None when there's no MathML descendant or
        formula.mathml_to_omml couldn't convert it (unsupported construct) -
        the caller (xml_utils.get_segments_from_node) falls back to
        flattening it as plain text, same as any unrecognized tag.
    """
    math_node = inline_formula.find('.//{http://www.w3.org/1998/Math/MathML}math')
    if math_node is None:
        return None
    omml_element = formula.mathml_to_omml(math_node)
    if omml_element is None:
        return None
    return {'type': 'formula', 'omml': omml_element}


def disp_formula_segments(disp_formula):
    """Converte o MathML de um <disp-formula> em um segmento 'formula', mais um segmento de texto para o <label>, se houver.

    O segmento de fórmula leva 'display': True (fórmula em bloco); o renderer
    usa essa marca para separá-la do texto e distingui-la de fórmula inline.

    Args:
        disp_formula (ElementTree): The <disp-formula> element.

    Returns:
        list[dict], or None when there's no MathML descendant or
        formula.mathml_to_omml couldn't convert it (unsupported construct) -
        callers should fall back to the existing flattened-text paragraph
        in that case, never drop the formula silently.
    """
    math_node = disp_formula.find('.//{http://www.w3.org/1998/Math/MathML}math')
    if math_node is None:
        return None
    omml_element = formula.mathml_to_omml(math_node)
    if omml_element is None:
        return None

    segments = [{'type': 'formula', 'omml': omml_element, 'display': True}]
    label = disp_formula.find('label')
    if label is not None:
        label_text = ''.join(label.itertext()).strip()
        if label_text:
            segments.append(xml_utils.plain_text_segment(f' {label_text}'))
    return segments


def paragraph_with_trailing_formula(p_node):
    """Trata <p>texto:<disp-formula>...</disp-formula></p>: fórmula em bloco com texto simples antes, no mesmo parágrafo.

    Escopo restrito: um <p> com mais de um <disp-formula>, ou com
    conteúdo depois da fórmula, retorna None (o chamador cai no fallback).

    Args:
        p_node (ElementTree): The <p> element.

    Returns:
        list[dict], or None when `p_node` doesn't match this specific shape.
    """
    formulas = p_node.findall('disp-formula')
    if len(formulas) != 1:
        return None
    formula = formulas[0]
    siblings = list(p_node)
    if siblings[-1] is not formula:
        return None
    if (formula.tail or '').strip():
        return None

    formula_segments = disp_formula_segments(formula)
    if formula_segments is None:
        return None

    leading_segments = xml_utils.get_segments_from_node(
        p_node, skip_tags={'disp-formula'},
        formula_tags=INLINE_FORMULA_TAGS, formula_converter=inline_formula_segment,
    )
    return leading_segments + formula_segments
