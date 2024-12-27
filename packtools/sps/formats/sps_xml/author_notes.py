"""
data = {
    "corresp_id": "c01",
    "corresp_label": "*",
    "corresp_text": "Correspondence Dr. Edmundo Figueira Departamento de Fisioterapia, Universidade FISP - Hogwarts,  Brasil.",
    "corresp_email": "contato@foo.com"
    "fns": [
        {
            "fn_type": "supported-by",
            "fn_id": "fn01",
            "fn_label": "*",
            "fn_p": "Vivamus sodales fermentum lorem,..."
        }
    ]
}

"""

from lxml import etree as ET

from packtools.sps.formats.sps_xml.fn_group import build_fn


def build_author_notes(data):
    author_notes_elem = ET.Element("author-notes")

    if any(data.get(key) for key in ("corresp_id", "corresp_label", "corresp_text", "corresp_email")):
        id_text = data.get("corresp_id")
        if id_text:
            corresp_elem = ET.Element("corresp", attrib={"id": id_text})
        else:
            corresp_elem = ET.Element("corresp")

        corresp_text = data.get("corresp_text")
        if corresp_text:
            corresp_elem.text = corresp_text

        email_text = data.get("corresp_email")
        if email_text:
            email_elem = ET.Element("email")
            email_elem.text = email_text
            corresp_elem.append(email_elem)

        label_text = data.get("label")
        if label_text:
            label_elem = ET.Element("label")
            label_elem.text = label_text
            corresp_elem.append(label_elem)

        author_notes_elem.append(corresp_elem)

    fn_list = data.get("fns")
    for fn_dict in fn_list or []:
        fn_elem = build_fn(fn_dict)
        author_notes_elem.append(fn_elem)

    return author_notes_elem
