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

node = {
    "person-group": [<Element>, <Element>]
}

"""

import xml.etree.ElementTree as ET


def build_ref(data, node=None):
    """
    Builds an XML element representing a bibliographic reference.

    Args:
        data (dict): A dictionary containing reference details with the following structure:
            - "ref-id" (str): Unique identifier for the reference (required).
            - "label" (str): Label for the reference, e.g., "1" (optional).
            - "mixed-citation" (str): Mixed content citation text (optional).
            - "publication-type" (str): Type of publication, e.g., "journal", "book" (required).
            - Additional bibliographic keys (optional):
                - "article-title", "chapter-title", "source", "edition", "publisher-loc",
                  "publisher-name", "series", "day", "month", "year", "volume", "issue",
                  "data-title", "version", "fpage", "lpage".
            - "ext-link" (list): A list of dictionaries, each containing:
                - "ext-link-type" (str): Type of external link (e.g., "uri") (required).
                - "xlink:href" (str): URL or URI of the external link (required).
                - "text" (str): Display text for the link (optional).
            - "pub-ids" (list): A list of dictionaries, each containing:
                - "pub-id-type" (str): Type of publication ID (e.g., "pmid") (required).
                - "text" (str): Value of the publication ID (required).
            - "dates-in-citation" (list): A list of dictionaries, each containing:
                - "content-type" (str): Type of date, e.g., "updated" (required).
                - "text" (str): Date value in text format (required).
        node (dict, optional): A dictionary containing additional XML elements to include in
            the reference. For example:
            - "person-group" (list): A list of XML elements representing authors or editors.

    Returns:
        xml.etree.ElementTree.Element: An XML element representing the reference.

    Raises:
        ValueError: If required fields are missing, including:
            - "ref-id".
            - "publication-type".
            - "ext-link-type" and "xlink:href" for external links.
            - "pub-id-type" for publication IDs.
            - "content-type" for dates in citation.

    Example input:
        data = {
            "ref-id": "B1",
            "label": "1",
            "mixed-citation": "Aires M, Paz AA, Perosa CT. Situação de saúde...",
            "publication-type": "journal",
            "article-title": "Situação de saúde e grau de...",
            "source": "Rev Gaucha Enferm",
            "volume": "30",
            "issue": "3",
            "fpage": "192",
            "lpage": "199",
            "ext-link": [
                {
                    "ext-link-type": "uri",
                    "xlink:href": "http://example.com",
                    "text": "http://example.com"
                }
            ],
            "pub-ids": [
                {
                    "pub-id-type": "pmid",
                    "text": "12345678"
                }
            ]
        }
        node = {
            "person-group": [ET.Element("person-group", attrib={"person-group-type": "author"})]
        }

    Example output:
        <ref id="B1">
            <label>1</label>
            <mixed-citation>Aires M, Paz AA, Perosa CT. Situação de saúde...</mixed-citation>
            <element-citation publication-type="journal">
                <article-title>Situação de saúde e grau de...</article-title>
                <source>Rev Gaucha Enferm</source>
                <volume>30</volume>
                <issue>3</issue>
                <fpage>192</fpage>
                <lpage>199</lpage>
                <ext-link ext-link-type="uri" xlink:href="http://example.com">http://example.com</ext-link>
                <pub-id pub-id-type="pmid">12345678</pub-id>
                <person-group person-group-type="author" />
            </element-citation>
        </ref>
        """
    if not (id_text := data.get("ref-id")):
        raise ValueError("attribute ref-id is required")

    ref_elem = ET.Element("ref", attrib={"id": id_text})

    for key in ("label", "mixed-citation"):
        if value := data.get(key):
            ET.SubElement(ref_elem, key).text = value

    if not (publication_type := data.get("publication-type")):
        raise ValueError("attribute publication-type is required")

    element_citation_elem = ET.SubElement(
        ref_elem, "element-citation", attrib={"publication-type": publication_type}
    )

    basic_keys = (
        "article-title",
        "chapter-title",
        "source",
        "edition",
        "publisher-loc",
        "publisher-name",
        "series",
        "day",
        "month",
        "year",
        "volume",
        "issue",
        "data-title",
        "version",
        "fpage",
        "lpage",
    )

    for key in basic_keys:
        if value := data.get(key):
            ET.SubElement(element_citation_elem, key).text = value

    for ext_link in data.get("ext-link") or []:
        ext_link_type = ext_link.get("ext-link-type")
        xlink_href = ext_link.get("xlink:href")
        if not ext_link_type or not xlink_href:
            raise ValueError("ext-link-type and xlink:href are required")

        if ext_link_text := ext_link.get("text"):
            ET.SubElement(
                element_citation_elem,
                "ext-link",
                attrib={"ext-link-type": ext_link_type, "xlink:href": xlink_href},
            ).text = ext_link_text

    for pub_id in data.get("pub-ids") or []:
        pub_id_type = pub_id.get("pub-id-type")
        if not pub_id_type:
            raise ValueError("pub-id-type is required")

        if pub_id_text := pub_id.get("text"):
            ET.SubElement(
                element_citation_elem, "pub-id", attrib={"pub-id-type": pub_id_type}
            ).text = pub_id_text

    for date_in_citation in data.get("dates-in-citation") or []:
        content_type = date_in_citation.get("content-type")
        if not content_type:
            raise ValueError("content-type is required")

        if date_in_citation_text := date_in_citation.get("text"):
            ET.SubElement(
                element_citation_elem,
                "date-in-citation",
                attrib={"content-type": content_type},
            ).text = date_in_citation_text

    return ref_elem
