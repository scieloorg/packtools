import xml.etree.ElementTree as ET


def build_article_node(data):
    """
    Builds an XML article node with the specified attributes and child elements.

    Args:
        data (dict): A dictionary containing the data to build the <article> node. The keys should include:
            - "dtd-version" (str): The DTD version for the article (required).
            - "specific-use" (str): A specific-use attribute value, such as "sps-1.8" (required).
            - "article-type" (str): The type of the article, e.g., "research-article" (required).
            - "xml:lang" (str): The language of the article, e.g., "pt" (required).
            - "children_nodes" (list of xml.etree.ElementTree.Element): A list of child elements to append to the article node (required).

    Returns:
        xml.etree.ElementTree.Element: An XML element representing the <article> node with the specified attributes and children.

    Raises:
        KeyError: If any required keys ("dtd-version", "specific-use", "article-type", "xml:lang") are missing from the input dictionary.
        ValueError: If "children_nodes" is not provided or is empty.

    Example:
        Input:
            article_data = {
                "dtd-version": "1.1",
                "specific-use": "sps-1.8",
                "article-type": "research-article",
                "xml:lang": "pt",
                "children_nodes": [
                    ET.fromstring('<front />'),
                    ET.fromstring('<body />'),
                    ET.fromstring('<back />'),
                    ET.fromstring('<sub-article />')
                ]
            }

        Output:
            <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML"
            dtd-version="1.1" specific-use="sps-1.8" article-type="research-article" xml:lang="pt">
                <front />
                <body />
                <back />
                <sub-article />
            </article>
    """
    namespaces = {
        "xlink": "http://www.w3.org/1999/xlink",
        "mml": "http://www.w3.org/1998/Math/MathML"
    }

    # Adiciona os namespaces
    for prefix, uri in namespaces.items():
        ET.register_namespace(prefix, uri)

    try:
        # Cria o elemento <article>
        article_elem = ET.Element("article", {
            "xmlns:xlink": namespaces["xlink"],
            "xmlns:mml": namespaces["mml"],
            "dtd-version": data["dtd-version"],
            "specific-use": data["specific-use"],
            "article-type": data["article-type"],
            "xml:lang": data["xml:lang"]
        })
    except KeyError as e:
        raise KeyError(f"{e} is required")

    if list_node := data.get("children_nodes"):
        article_elem.extend(list_node)
    else:
        raise ValueError("A list of children nodes is required")

    return article_elem
