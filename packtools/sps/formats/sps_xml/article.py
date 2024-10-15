import xml.etree.ElementTree as ET


def build_article_node(article_data: dict):
    namespaces = {
        "xlink": "http://www.w3.org/1999/xlink",
        "mml": "http://www.w3.org/1998/Math/MathML"
    }

    # Adiciona os namespaces
    for prefix, uri in namespaces.items():
        ET.register_namespace(prefix, uri)

    # Cria o elemento <article>
    article_elem = ET.Element("article", {
        "xmlns:xlink": namespaces["xlink"],
        "xmlns:mml": namespaces["mml"],
        "dtd-version": article_data.get("dtd-version"),
        "specific-use": article_data.get("specific-use"),
        "article-type": article_data.get("article-type"),
        "xml:lang": article_data.get("xml:lang")
    })

    return article_elem
