import xml.etree.ElementTree as ET


def build_abstract(data):
    """
    Builds a structured abstract XML element.

    Args:
        data (dict): A dictionary containing the abstract details with the following keys:
            - "title" (str): The title of the abstract (required).
            - "lang" (str or None): The language of the abstract, used for translation (optional).
            - "secs" (list): A list of sections, each represented as a dictionary with:
                - "title" (str): Title of the section (optional).
                - "p" (str): Paragraph content of the section (optional).

    Returns:
        xml.etree.ElementTree.Element: An XML element representing the abstract.

    Raises:
        ValueError: If "title" is missing.

    Example:
        Input:
            data = {
                "title": "Resumo",
                "lang": None,
                "secs": [
                    {"title": "Objetivo", "p": "Verificar a sensibilidade ..."},
                    {"title": "Métodos", "p": "Durante quatro meses ..."}
                ]
            }
        Output:
            <abstract>
                <title>Resumo</title>
                <sec>
                    <title>Objetivo</title>
                    <p>Verificar a sensibilidade ...</p>
                </sec>
                <sec>
                    <title>Métodos</title>
                    <p>Durante quatro meses ...</p>
                </sec>
            </abstract>
    """
    abstract_elem = ET.Element("abstract")
    return build_abstract_content(data, abstract_elem)


def build_trans_abstract(data):
    """
    Builds a translated abstract XML element.

    Args:
        data (dict): A dictionary containing the abstract details with the following keys:
            - "title" (str): The title of the abstract (required).
            - "lang" (str): The language of the translated abstract (required).
            - "secs" (list): A list of sections (optional). See `build_abstract` for structure.

    Returns:
        xml.etree.ElementTree.Element: An XML element representing the translated abstract.

    Raises:
        ValueError: If "lang" or "title" is missing.

    Example:
        See `build_abstract` for input/output examples.
    """
    if not (lang := data.get("lang")):
        raise ValueError("Lang is required")

    abstract_elem = ET.Element("trans-abstract", attrib={"xml:lang": lang})
    return build_abstract_content(data, abstract_elem)


def build_abstract_content(data, abstract_elem):
    """
    Helper function to build the content of an abstract or translated abstract.

    Args:
        data (dict): Abstract content details. See `build_abstract` for structure.
        abstract_elem (xml.etree.ElementTree.Element): The root element for the abstract.

    Returns:
        xml.etree.ElementTree.Element: The updated abstract element with content.

    Raises:
        ValueError: If "title" is missing.
    """
    title_text = data.get("title")
    if not title_text:
        raise ValueError("title is required")

    title_elem = ET.Element("title")
    title_elem.text = title_text
    abstract_elem.append(title_elem)

    p_text = data.get("p")
    if p_text:
        p_elem = ET.Element("p")
        p_elem.text = p_text
        abstract_elem.append(p_elem)

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


def build_visual_abstract(data):
    """
    Builds a visual abstract XML element.

    Args:
        data (dict): A dictionary containing the visual abstract details with the following keys:
            - "title" (str): The title of the abstract (required).
            - "fig_id" (str): Unique identifier for the figure (required).
            - "caption" (str): Caption for the figure (optional).
            - "href" (str): Path or URL to the graphical representation (optional).

    Returns:
        xml.etree.ElementTree.Element: An XML element representing the visual abstract.

    Raises:
        ValueError: If "title" or "fig_id" is missing.

    Example:
        Input:
            data = {
                "title": "Visual Abstract",
                "fig_id": "vf01",
                "caption": "Título",
                "href": "1234-5678-zwy-12-04-0123-vs01.tif"
            }
        Output:
            <abstract abstract-type="graphical">
                <title>Visual Abstract</title>
                <p>
                    <fig id="vf01">
                        <caption>
                            <title>Título</title>
                        </caption>
                        <graphic xlink:href="1234-5678-zwy-12-04-0123-vs01.tif" />
                    </fig>
                </p>
            </abstract>
    """
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
