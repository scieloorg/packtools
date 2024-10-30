"""
data = {
    "title": "Notas",
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

import xml.etree.ElementTree as ET


def build_fn_group(data):
    fn_group_elem = ET.Element("fn-group")

    title_text = data.get("title")
    if title_text:
        title_element = ET.Element("title")
        title_element.text = title_text
        fn_group_elem.append(title_element)

    fn_list = data.get("fns")
    if isinstance(fn_list, list):
        for fn_dict in fn_list:
            if isinstance(fn_dict, dict):
                fn_elem = build_fn(fn_dict)
                fn_group_elem.append(fn_elem)

    return fn_group_elem


def build_fn(data):
    fn_type_text = data.get("fn_type")
    if not fn_type_text:
        raise ValueError("fn type is required")

    fn_id_text = data.get("fn_id")
    if fn_id_text:
        fn_elem = ET.Element("fn", attrib={"fn-type": fn_type_text, "id": fn_id_text})
    else:
        fn_elem = ET.Element("fn", attrib={"fn-type": fn_type_text})

    label_text = data.get("fn_label")
    if label_text:
        label_elem = ET.Element("label")
        label_elem.text = label_text
        fn_elem.append(label_elem)

    p_text = data.get("fn_p")
    if p_text:
        p_elem = ET.Element("p")
        p_elem.text = p_text
        fn_elem.append(p_elem)

    return fn_elem
