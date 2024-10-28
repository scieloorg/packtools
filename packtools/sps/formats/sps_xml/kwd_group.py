"""
data = {
    "kwd_lang": "pt",
    "kwd_title": "Palavra-chave",
    "kwds": [
        "Broncoscopia",
    ]
}
"""

import xml.etree.ElementTree as ET


def build_kwd_group(data):
    kwd_lang_text = data.get("kwd_lang")
    if not kwd_lang_text:
        raise ValueError("kwd lang is required")

    kwd_title_text = data.get("kwd_title")
    if not kwd_title_text:
        raise ValueError("kwd title is required")

    kwd_group_elem = ET.Element("kwd-group", attrib={"xml:lang": kwd_lang_text})
    kwd_title_elem = ET.Element("title")
    kwd_title_elem.text = kwd_title_text
    kwd_group_elem.append(kwd_title_elem)

    kwds = data.get("kwds")
    if isinstance(kwds, list):
        for kwd in kwds:
            kwd_elem = ET.Element("kwd")
            kwd_elem.text = kwd
            kwd_group_elem.append(kwd_elem)

    return kwd_group_elem
