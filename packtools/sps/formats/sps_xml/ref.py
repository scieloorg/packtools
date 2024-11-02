"""
data = {
    "ref-id": "B1",
    "label": "1",
    "mixed-citation": "Aires M, Paz AA, Perosa CT. Situação de saúde...",
    "publication-type": "journal",
    "article-title": "Situação de saúde e grau de...",
    "chapter-title": "The epidemiology of idiopathic inflammatory bowel disease.",
    "source": "Rev Gaucha Enferm",
    "edition": "4th ed",
    "publisher-loc": "Rio de Janeiro",
    "publisher-name": "Universidade Federal do Paraná",
    "volume": "30",
    "issue": "3",
    "data-title": "Estudos de genes em ratos albinos na América Latina",
    "version": "23 jan.",
    "series": "Second International Workshop",
    "day": "22",
    "month": "10",
    "year": "2009",
    "fpage": "192",
    "lpage": "199",
    "ext-link": [
        {
            "ext-link-type": "uri",
            "xlink:href": "http://socialsciences.scielo.org",
            "text": "http://socialsciences.scielo.org"
        }
    ]
    "pub-ids": [
        {
            "pub-id-type": "pmid",
            "text": "15867408"
        }
    ]
    "dates-in-citation": [
        {
            "content-type": "updated",
            "text": "2006 Jul 20"
        }
    ]
}

"""

import xml.etree.ElementTree as ET


def build_ref(data):
    id_text = data.get("ref-id")
    if not id_text:
        raise ValueError("attribute ref-id is required")

    publication_type = data.get("publication-type")
    if not publication_type:
        raise ValueError("attribute publication-type is required")

    ref_elem = ET.Element("ref", attrib={"id": id_text})
    element_citation_elem = ET.Element("element-citation", attrib={"publication-type": publication_type})
    ref_elem.append(element_citation_elem)

    basic_keys = ("label", "mixed-citation", "article-title", "chapter-title", "source", "edition", "publisher-loc",
                  "publisher-name", "series", "day", "month", "year", "volume", "issue", "data-title", "version",
                  "fpage", "lpage")

    for key in basic_keys:
        key_text = data.get(key)
        if key_text:
            key_elem = ET.Element(key)
            key_elem.text = key_text
            ref_elem.append(key_elem)

    for ext_link in data.get("ext-link") or []:
        ext_link_type = ext_link.get("ext-link-type")
        xlink_href = ext_link.get("xlink:href")
        if not ext_link_type or not xlink_href:
            raise ValueError("ext-link-type and xlink:href are required")

        ext_link_text = ext_link.get("text")
        if ext_link_text:
            ext_link_elem = ET.Element("ext-link", attrib={"ext-link-type": ext_link_type, "xlink:href": xlink_href})
            ext_link_elem.text = ext_link_text
            ref_elem.append(ext_link_elem)

    for pub_id in data.get("pub-ids") or []:
        pub_id_type = pub_id.get("pub-id-type")
        if not pub_id_type:
            raise ValueError("pub-id-type is required")

        pub_id_text = pub_id.get("text")
        if pub_id_text:
            pub_id_elem = ET.Element("pub-id", attrib={"pub-id-type": pub_id_type})
            pub_id_elem.text = pub_id_text
            ref_elem.append(pub_id_elem)

    for date_in_citation in data.get("dates-in-citation") or []:
        content_type = date_in_citation.get("content-type")
        if not content_type:
            raise ValueError("content-type is required")

        date_in_citation_text = date_in_citation.get("text")
        if date_in_citation_text:
            date_in_citation_elem = ET.Element("date-in-citation", attrib={"content-type": content_type})
            date_in_citation_elem.text = date_in_citation_text
            ref_elem.append(date_in_citation_elem)

    return ref_elem
