from lxml import etree as ET


def build_ack(data):
    """
    Builds an XML element representing the acknowledgments section.

    Args:
        data (dict): A dictionary containing acknowledgment details with the following keys:
            - "title" (str, optional): Title of the acknowledgment section.
            - "p" (list of str, optional): A list of paragraphs for the acknowledgment.

    Returns:
        xml.etree.ElementTree.Element: An XML element representing the acknowledgment section.

    Example input:
        data = {
            "title": "Acknowledgments",
            "p": [
                "We thank the participants for their time.",
                "Funding was provided by XYZ organization."
            ]
        }

    Example output:
        <ack>
            <title>Acknowledgments</title>
            <p>We thank the participants for their time.</p>
            <p>Funding was provided by XYZ organization.</p>
        </ack>
    """
    title = data.get("title")
    paragraphs = data.get("p")

    if title or paragraphs:
        ack_elem = ET.Element("ack")
        if title:
            ET.SubElement(ack_elem, "title").text = title
        for paragraph in paragraphs or []:
            ET.SubElement(ack_elem, "p").text = paragraph

        return ack_elem
