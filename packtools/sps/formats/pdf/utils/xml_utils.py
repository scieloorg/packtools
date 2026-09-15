import re


def get_text_from_node(node, skip_tags=None):
    """
    Extracts text from an XML node, including its children, preserving the
    adjacency of the source (no space is inserted between fragments unless
    one was already there as literal text or a tail).

    Args:
        node (ElementTree): The XML node to extract text from.
        skip_tags (set, optional): Child tag names to drop entirely from the
            output; only their `.tail` (the text that follows them in the
            source) is kept. Used to flatten a paragraph to readable text
            while excluding embedded elements such as <fig>/<table-wrap>.

    Returns:
        str: The text extracted from the given node.
    """
    skip_tags = skip_tags or set()
    texts_els = []

    if node.text:
        texts_els.append(node.text)

    for child in node:
        if child.tag in skip_tags:
            pass
        else:
            texts_els.append(get_text_from_node(child, skip_tags=skip_tags))

        if child.tail:
            texts_els.append(child.tail)

    text = ''.join(texts_els)
    text = _remove_double_spaces(text)
    text = _normalize_punctuation_spacing(text)
    return text

_INLINE_STYLE_TAGS = {
    'italic': 'italic',
    'bold': 'bold',
    'sup': 'superscript',
    'sub': 'subscript',
}


def get_segments_from_node(node, skip_tags=None):
    """
    Extracts text from an XML node as a list of style-tagged segments
    instead of a single flattened string, so inline markup
    (<italic>/<bold>/<sup>/<sub>) can be rendered with the matching run
    formatting instead of being discarded.

    Preserves the same adjacency-preserving traversal as
    get_text_from_node (including skip_tags), then merges adjacent
    fragments that ended up with the same combination of active styles
    before normalizing whitespace/punctuation per merged segment - doing
    it per merged run rather than per raw fragment matters because a
    stray space next to a paren/bracket/comma (e.g. "( <xref>...</xref>
    )") always lands in the same text fragment as that punctuation, not
    split across a style boundary.

    Args:
        node (ElementTree): The XML node to extract segments from.
        skip_tags (set, optional): Child tag names to drop entirely from
            the output; only their `.tail` is kept. Same semantics as
            get_text_from_node.

    Returns:
        list[dict]: Segments in document order, each
            {'type': 'text', 'text': str, 'italic': bool, 'bold': bool,
            'superscript': bool, 'subscript': bool}. Empty after
            whitespace normalization/leading-trailing strip are dropped.
    """
    skip_tags = skip_tags or set()
    raw_segments = []
    _collect_style_segments(node, skip_tags, frozenset(), raw_segments)

    segments = []
    for text, styles in _merge_adjacent_segments(raw_segments):
        text = _remove_double_spaces(text)
        text = _normalize_punctuation_spacing(text)
        if text:
            segments.append(_build_text_segment(text, styles))

    if segments:
        segments[0]['text'] = segments[0]['text'].lstrip()
        segments[-1]['text'] = segments[-1]['text'].rstrip()
        segments = [seg for seg in segments if seg['text']]

    return segments


def _collect_style_segments(node, skip_tags, active_styles, raw_segments):
    """Recursively walk node, appending (text, active_styles) fragments to raw_segments."""
    if node.text:
        raw_segments.append((node.text, active_styles))

    for child in node:
        if child.tag in skip_tags:
            pass
        elif child.tag in _INLINE_STYLE_TAGS:
            child_styles = active_styles | {_INLINE_STYLE_TAGS[child.tag]}
            _collect_style_segments(child, skip_tags, child_styles, raw_segments)
        else:
            _collect_style_segments(child, skip_tags, active_styles, raw_segments)

        if child.tail:
            raw_segments.append((child.tail, active_styles))


def _merge_adjacent_segments(raw_segments):
    """Concatenate consecutive (text, styles) fragments that share the same styles."""
    merged = []
    for text, styles in raw_segments:
        if merged and merged[-1][1] == styles:
            merged[-1] = (merged[-1][0] + text, styles)
        else:
            merged.append((text, styles))
    return merged


def _build_text_segment(text, styles):
    return {
        'type': 'text',
        'text': text,
        'italic': 'italic' in styles,
        'bold': 'bold' in styles,
        'superscript': 'superscript' in styles,
        'subscript': 'subscript' in styles,
    }

def get_node_level(element, root):
    """
    Determines the level or depth of an XML element within the document tree.
    
    Args:
        element (ElementTree): The XML element to get the level for.
        root (ElementTree): The root XML element of the document.
    
    Returns:
        int: The level or depth of the given element within the document tree.
    """
    level = 0
    current = element

    while current is not root:
        parent_found = False

        for sibling in root.iter():
            if sibling is not current and current in sibling:
                current = sibling
                level += 1
                parent_found = True
                break

        if not parent_found:
            break

    return level

def get_text_from_mixed_citation_node(node):
    """
    Extracts text from a mixed_citation node, including its children.

    Args:
        node (ElementTree): The mixed_citation node to extract text from.
    
    Returns:
        str: The text extracted from the given mixed_citation node.
    """
    ref_text = ""
    
    if node.text:
        ref_text += node.text
    
    for elem in node:
        if elem.tag in set(['italic', 'bold',]):
            ref_text += f"{elem.text if elem.text else ''}"
        else:
            if elem.text:
                ref_text += f" {elem.text}"
        
        if elem.tail:
            ref_text += f"{elem.tail}"
    
    ref_text = _remove_double_spaces(ref_text)
    ref_text = ref_text.strip()
    ref_text = _add_period(ref_text)

    return ref_text

def _add_period(text):
    """
    Adds a period to the end of the given text if it does not already have one.

    Args:
        text (str): The text to add a period to.

    Returns:
        str: The text with a period added to the end.
    """
    if text and not text.endswith('.'):
        text += '.'
    return text

def _remove_double_spaces(text):
    """
    Collapses any run of whitespace (including tabs and newlines left over
    from pretty-printed XML, e.g. the indentation tail of a skipped
    <fig>/<table-wrap>) into a single space.

    Args:
        text (str): The text to normalize.

    Returns:
        str: The text with whitespace runs collapsed to single spaces.
    """
    return re.sub(r'\s+', ' ', text)

def _normalize_punctuation_spacing(text):
    """
    Removes whitespace that ends up glued to the inside of parentheses and
    brackets, or before a comma/semicolon, when the source XML has a space
    directly before/after an inline element such as <xref> (e.g. "( <xref>
    Fig. 1</xref> )") — a common defect that survives adjacency-preserving
    extraction because the space is literal text, not an artifact of it.

    Args:
        text (str): The text to normalize.

    Returns:
        str: The text with punctuation spacing normalized.
    """
    text = re.sub(r'\(\s+', '(', text)
    text = re.sub(r'\s+\)', ')', text)
    text = re.sub(r'\[\s+', '[', text)
    text = re.sub(r'\s+\]', ']', text)
    text = re.sub(r'\s+;', ';', text)
    text = re.sub(r'\s+,', ',', text)
    return text
