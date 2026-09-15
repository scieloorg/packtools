import copy

import mathml2omml
from lxml import etree

_OMML_NS = 'http://schemas.openxmlformats.org/officeDocument/2006/math'


def normalize_empty_base_superscripts(math_element):
    """
    Fixes a real-world MathML authoring pattern seen in the corpus (e.g.
    a5.xml): instead of a single nested `<msup>` for "x1^0.5", the source
    represents it as `<msub>x,1</msub>` followed by a *separate* `<msup>`
    whose base is an empty `<mrow/>` - relying purely on visual adjacency
    to look like "x1 raised to 0.5" when rendered as MathML. A literal
    MathML->OMML conversion reproduces this structure faithfully, which
    Word/LibreOffice then render as a visible empty box glyph where the
    superscript's base should be (confirmed by rendering a real PDF from
    this pattern before this fix existed).

    Merges each such `<msup>` with its immediately preceding sibling
    (wrapping that sibling as the superscript's real base) so the
    resulting MathML has no empty base left to convert. Operates on a
    deep copy - never mutates the caller's tree. A `<msup>` with no
    preceding sibling, or whose base isn't empty, is left untouched (the
    empty-box outcome only affects that rare shape, not scope for this
    phase to eliminate entirely).

    Args:
        math_element (lxml.etree._Element): The `<mml:math>` node.

    Returns:
        lxml.etree._Element: A deep copy of `math_element` with the fix
        applied wherever the pattern is found.
    """
    root = copy.deepcopy(math_element)
    # Materialize the target list before mutating - moving elements around
    # while root.iter() is still walking the live tree makes it skip every
    # other match (confirmed empirically: only alternating occurrences got
    # fixed when this iterated and mutated in the same pass).
    candidate_msups = [el for el in root.iter() if etree.QName(el).localname == 'msup']
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
    """Returns a deep copy of `element` with every tag's namespace prefix removed - mathml2omml's SAX-based parser expects bare local names (e.g. 'math', not '{http://www.w3.org/1998/Math/MathML}math')."""
    stripped = copy.deepcopy(element)
    for el in stripped.iter():
        if isinstance(el.tag, str) and '}' in el.tag:
            el.tag = el.tag.split('}', 1)[1]
    etree.cleanup_namespaces(stripped)
    return stripped


def mathml_to_omml(math_element):
    """
    Converts a `<mml:math>` node to an OMML `<m:oMath>` element ready to be
    appended into a python-docx paragraph's raw XML (`paragraph._p.append(...)`),
    via the `mathml2omml` library (MIT-licensed, pure Python - no XSLT
    vendoring, avoids the licensing ambiguity of the Microsoft-authored
    mml2omml.xsl commonly used for this).

    Applies `normalize_empty_base_superscripts` first (see its docstring).

    Args:
        math_element (lxml.etree._Element): The `<mml:math>` node to convert.

    Returns:
        lxml.etree._Element, or None if the MathML uses a construct
        mathml2omml doesn't support (it raises on unrecognized tags) -
        callers should fall back to flattened text rather than propagate
        the exception, so one malformed formula doesn't abort the whole
        article's generation (same principle as issue #1371's fix).
    """
    normalized = normalize_empty_base_superscripts(math_element)
    stripped = _strip_namespace(normalized)
    mathml_str = etree.tostring(stripped, encoding='unicode')

    try:
        omml_str = mathml2omml.convert(mathml_str)
    except Exception:
        return None

    omml_str = omml_str.replace('<m:oMath>', f'<m:oMath xmlns:m="{_OMML_NS}">', 1)
    try:
        return etree.fromstring(omml_str.encode('utf-8'))
    except etree.XMLSyntaxError:
        return None
