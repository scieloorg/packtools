from lxml import etree as ET


def build_front(node):
    """
    Constructs an XML "front" element by combining "journal-meta" and "article-meta" sub-elements.

    Parameters:
        node (dict): A dictionary-like object containing the keys "journal-meta" and "article-meta",
                     which should map to XML elements.

    Returns:
        xml.etree.ElementTree.Element: An XML element named "front" that contains the "journal-meta"
                                       and "article-meta" elements as its children.

    Raises:
        ValueError: If either "journal-meta" or "article-meta" is missing in the input node.

    Example:
        node = {
            "journal-meta": <Element>,
            "article-meta": <Element>
        }
    """
    journal_meta = node.get("journal-meta")
    article_meta = node.get("article-meta")
    if journal_meta is None or article_meta is None:
        raise ValueError("journal-meta and article-meta nodes are required.")

    front = ET.Element("front")
    front.append(journal_meta)
    front.append(article_meta)

    return front
