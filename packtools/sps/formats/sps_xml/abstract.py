"""
example of structured abstract:
data = {
            "title": "Resumo",
            "secs": [
                {
                    "title": "Objetivo",
                    "p": "Verificar a sensibilidade e especificidade ..."
                },
                {
                    "title": "Métodos",
                    "p": "Durante quatro meses foram selecionados ..."
                }
            ]
        }
"""

import xml.etree.ElementTree as ET


def build_structured_abstract(data):
    abstract_elem = ET.Element("abstract")

    title_text = data.get("title")
    if not title_text:
        raise ValueError(f"title is required")

    title_elem = ET.Element("title")
    title_elem.text = title_text
    abstract_elem.append(title_elem)

    secs = data.get("secs")
    if isinstance(secs, list):
        for sec in secs:
            if any(sec.get(key) for key in ("sec", "title")):
                sec_elem = ET.Element("sec")
                title_text = sec.get("title")
                if title_text:
                    title_elem = ET.Element("title")
                    title_elem.text = title_text
                    sec_elem.append(title_elem)
                p_text = sec.get("p")
                if p_text:
                    p_elem = ET.Element("p")
                    p_elem.text = p_text
                    sec_elem.append(p_elem)
                abstract_elem.append(sec_elem)

    return abstract_elem


"""
example of simple abstract:
data = {
            "title": "Resumo",
            "p": "Verificar a sensibilidade e especificidade ..."
        }
"""


def build_simple_abstract(data):
    abstract_elem = ET.Element("abstract")

    title_text = data.get("title")
    if not title_text:
        raise ValueError(f"title is required")

    title_elem = ET.Element("title")
    title_elem.text = title_text
    abstract_elem.append(title_elem)

    p_text = data.get("p")
    if p_text:
        p_elem = ET.Element("p")
        p_elem.text = p_text
        abstract_elem.append(p_elem)

    return abstract_elem


"""
example of visual abstract
data = {
            "title": "Visual Abstract",
            "fig_id": "vf01",
            "caption": "Título",
            "href": "1234-5678-zwy-12-04-0123-vs01.tif"
        }
"""


def build_visual_abstract(data):
    abstract_elem = ET.Element("abstract", attrib={"abstract-type": "graphical"})

    title_text = data.get("title")
    if not title_text:
        raise ValueError(f"title is required")

    title_elem = ET.Element("title")
    title_elem.text = title_text
    abstract_elem.append(title_elem)

    fig_id = data.get("fig_id")
    if not fig_id:
        raise ValueError("fig id is required")

    p_elem = ET.Element("p")
    fig_elem = ET.Element("fig", attrib={"id": fig_id})

    caption_text = data.get("caption")
    if caption_text:
        title_elem = ET.Element("title")
        title_elem.text = caption_text
        caption_elem = ET.Element("caption")
        caption_elem.append(title_elem)
        fig_elem.append(caption_elem)

    href_text = data.get("href")
    if href_text:
        graphic_elem = ET.Element("graphic", attrib={"xlink:href": href_text})
        fig_elem.append(graphic_elem)

    p_elem.append(fig_elem)
    abstract_elem.append(p_elem)

    return abstract_elem
