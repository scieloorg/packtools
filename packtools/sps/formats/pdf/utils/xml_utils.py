def get_text_from_node(node):
    """
    Extracts text from an XML node, including its children.

    Args:
        node (ElementTree): The XML node to extract text from.

    Returns:
        str: The text extracted from the given node.
    """
    texts_els = []

    if node.text:
        texts_els.append(node.text)

    for child in node:
        if child.tag == 'xref':
            xref_text = child.text if child.text else ''
            for subchild in child:
                if subchild.tag in ('italic', 'bold'):
                    xref_text += (subchild.text if subchild.text else '')
                    if subchild.tail:
                        xref_text += (subchild.tail if subchild.tail else '')
            texts_els.append(xref_text)
        elif child.tag in ('italic', 'bold'):
            if child.text:
                texts_els.append(child.text)
            for subchild in child:
                texts_els.append(get_text_from_node(subchild))
        else:
            texts_els.append(get_text_from_node(child))

        if child.tail:
            texts_els.append(child.tail)

    text = ''.join(texts_els)
    text = _remove_double_spaces(text)
    return text

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
