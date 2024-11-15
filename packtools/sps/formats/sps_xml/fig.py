import xml.etree.ElementTree as ET


def build_fig(data):
    """
    Constructs an XML `fig` element based on the provided data.

    Args:
        data (dict): A dictionary containing the attributes and sub-elements
            for the `fig` element. Expected keys include:
            - "fig-id" (str): Required. The ID for the figure.
            - "fig-type" (str): Optional. The type of the figure.
            - "label" (str): Optional. The label for the figure.
            - "caption-title" (str): Optional. The title of the caption.
            - "caption-p" (list of str): Optional. Paragraphs for the caption.
            - "graphic-xlink" (str): Optional. The xlink for a graphic element.
            - "attrib" (str): Optional. An additional attribute for the figure.

    Returns:
        xml.etree.ElementTree.Element: The constructed `fig` XML element.

    Raises:
        ValueError: If the "fig-id" key is missing in the input data.

    Example input:
        data = {
            "fig-id": "f01",
            "fig-type": "map",
            "label": "Figure 1",
            "caption-title": "Título de figura",
            "caption-p": ["Deaths Among Patients..."],
            "graphic-xlink": "1234-5678-zwy-12-04-0123-gf02.tif",
            "attrib": "Fonte: IBGE (2018)"
        }

    Example output:
        <fig id="f01" fig-type="map">
            <label>Figure 1</label>
            <caption>
                <title>Título de figura</title>
                <p>Deaths Among Patients...</p>
            </caption>
            <graphic xlink:href="1234-5678-zwy-12-04-0123-gf02.tif" />
            <attrib>Fonte: IBGE (2018)</attrib>
        </fig>
    """
    fig_id = data.get("fig-id")
    if not fig_id:
        raise ValueError("Attrib id is required")

    attrib = {"id": fig_id}

    fig_type = data.get("fig-type")
    if fig_type:
        attrib["fig-type"] = fig_type

    # build fig
    fig_elem = ET.Element("fig", attrib=attrib)

    # add label
    if label := data.get("label"):
        label_elem = ET.Element("label")
        label_elem.text = label
        fig_elem.append(label_elem)

    # add caption
    caption = data.get("caption-title")
    paragraphs = data.get("caption-p")
    if caption or paragraphs:
        caption_elem = ET.Element("caption")
        if caption:
            # testando SubElement
            title_elem = ET.SubElement(caption_elem, "title")
            title_elem.text = caption

        for paragraph in (paragraphs or []):
            # testando SubElement
            paragraph_elem = ET.SubElement(caption_elem, "p")
            paragraph_elem.text = paragraph

        fig_elem.append(caption_elem)

    # add xlink
    if xlink := data.get("graphic-xlink"):
        xlink_elem = ET.Element("graphic", attrib={"xlink:href": xlink})
        fig_elem.append(xlink_elem)

    # add attrib
    if attrib := data.get("attrib"):
        attrib_elem = ET.Element("attrib")
        attrib_elem.text = attrib
        fig_elem.append(attrib_elem)

    return fig_elem
