from packtools.sps.formats.pdf.utils import xml_utils


def extract_article_main_language(xml_tree, namespaces={'xml': 'http://www.w3.org/XML/1998/namespace'}):
    """
    Extracts the main language of the article from the given XML tree.
    
    Args:
        xml_tree (ElementTree): The XML tree to extract the main language from.
        namespaces (dict, optional): A dictionary of namespace prefixes and their corresponding URIs. Defaults to {'xml': 'http://www.w3.org/XML/1998/namespace'}.
    
    Returns:
        str: The main language of the article.
    """
    lang_attrib_name = "{" + f'{namespaces["xml"]}' + "}lang"
    return xml_tree.attrib.get(lang_attrib_name)

def extract_article_title(xml_tree, return_text=True):
    """
    Extracts the article title from the given XML tree.
    
    Args:
        xml_tree (ElementTree): The XML tree to extract the article title from.
        return_text (bool, optional): If True, returns the text content of the article-title element. If False, returns the element itself. Defaults to True.
    
    Returns:
        str or ElementTree: The article title text or the article-title element, depending on the value of the `return_text` parameter.
    """
    node = xml_tree.find('.//article-title')
    if return_text:
        return ''.join(node.itertext()).strip()
    return node
