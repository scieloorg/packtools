"""
data = {
    "table-wrap-id": "t01",
    "label": "Table 1",
    "caption-title": "Título da tabela",
    "caption-p": ["Deaths Among Patients..."],
    "fns": [
        {
            "fn-id": "fn01",
            "fn-label": "*",
            "fn-p": "text"
        }
    ]
}

obs.:
    - nota de tabela não tem o atributo 'fn-type'
    - o atributo 'id' é obrigatório
"""

import xml.etree.ElementTree as ET


def build_table_wrap(data):
    table_id = data.get("table-wrap-id")
    if not table_id:
        raise ValueError("Attrib table-wrap-id is required")

    # build table_wrap
    table_elem = ET.Element("table-wrap", attrib={"id": table_id})

    # add label
    if label := data.get("label"):
        label_elem = ET.SubElement(table_elem, "label")
        label_elem.text = label

    # add caption
    caption = data.get("caption-title")
    paragraphs = data.get("caption-p")
    if caption or paragraphs:
        caption_elem = ET.SubElement(table_elem, "caption")
        if caption:
            title_elem = ET.SubElement(caption_elem, "title")
            title_elem.text = caption

        for paragraph in (paragraphs or []):
            paragraph_elem = ET.SubElement(caption_elem, "p")
            paragraph_elem.text = paragraph

    # add footnotes
    if fns := data.get("fns"):
        table_wrap_foot_elem = ET.SubElement(table_elem, "table-wrap-foot")
        for fn in fns:
            if not (fn_id := fn.get("fn-id")):
                raise ValueError("fn-id is required")
            fn_elem = ET.SubElement(table_wrap_foot_elem, "fn", attrib={"id": fn_id})

            if label := fn.get("fn-label"):
                label_elem = ET.SubElement(fn_elem, "label")
                label_elem.text = label

            if p := fn.get("fn-p"):
                p_elem = ET.SubElement(fn_elem, "p")
                p_elem.text = p

    return table_elem
