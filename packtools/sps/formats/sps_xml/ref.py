"""
data = {
    "ref_id": "B1",
    "label": "1",
    "mixed_citation": "Aires M, Paz AA, Perosa CT. Situação de saúde...",
    "publication_type": "journal",
    "article_title": "Situação de saúde e grau de...",
    "source": "Rev Gaucha Enferm",
    "year": "2009",
    "volume": "30",
    "issue": "3",
    "fpage": "192",
    "lpage": "199"
}
"""

import xml.etree.ElementTree as ET


def build_ref(data):
    id_text = data.get("ref_id")
    if not id_text:
        raise ValueError("attribute id is required")

    publication_type = data.get("publication_type")
    if not publication_type:
        raise ValueError("attribute publication type is required")

    ref_elem = ET.Element("ref", attrib={"id": id_text})

    element_citation_elem = ET.Element("element-citation", attrib={"publication-type": publication_type})
    ref_elem.append(element_citation_elem)

    for item in ("label", "mixed_citation", "article_title", "source", "year", "volume", "issue", "fpage", "lpage"):
        item_text = data.get(item)
        if item_text:
            item_elem = ET.Element(item)
            item_elem.text = item_text
            ref_elem.append(item_elem)

    return ref_elem
