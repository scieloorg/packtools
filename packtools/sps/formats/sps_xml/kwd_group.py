"""
data = {
    "kwd-lang": "pt",
    "kwd-title": "Palavra-chave",
    "kwds": [
        "Broncoscopia",
    ]
}
"""

import xml.etree.ElementTree as ET


def build_kwd_group(data):
    kwd_lang_text = data.get("kwd-lang")
    if not kwd_lang_text:
        raise ValueError("kwd-lang is required")

    kwd_title_text = data.get("kwd-title")
    if not kwd_title_text:
        raise ValueError("kwd-title is required")

    kwd_group_elem = ET.Element("kwd-group", attrib={"xml:lang": kwd_lang_text})
    kwd_title_elem = ET.Element("title")
    kwd_title_elem.text = kwd_title_text
    kwd_group_elem.append(kwd_title_elem)

    try:
        kwds = data["kwds"]
        if not kwds:
            raise ValueError("kwds must not be an empty list")

        for kwd in kwds:
            kwd_elem = ET.Element("kwd")
            kwd_elem.text = kwd
            kwd_group_elem.append(kwd_elem)

    except KeyError:
        raise ValueError("kwds is required")
    except TypeError:
        # data["kwds"] is not a list or is None
        raise TypeError("kwds must be a list")

    return kwd_group_elem
