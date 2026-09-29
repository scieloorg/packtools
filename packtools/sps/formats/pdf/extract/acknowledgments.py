"""Agradecimentos (<ack>)."""

from packtools.sps.formats.pdf.utils import xml_utils


def extract_acknowledgment_data(xml_tree):
    """
    Extracts acknowledgment data from an XML tree.
    
    Args:
        xml_tree (ElementTree): The XML tree to extract the acknowledgment data from.
    
    Returns:
        dict: A dictionary containing the acknowledgment data, with the following keys:
            - 'title': The title of the acknowledgment section, if present.
            - 'paragraphs': One list of style-tagged segments (see
              xml_utils.get_segments_from_node) per paragraph, so text after
              inline markup is kept and the markup itself is preserved.
    """
    data = {'paragraphs': [], 'title': ''}

    ack = xml_tree.find('.//ack')
    if ack is not None:
        title = ack.find('title')
        if title is not None:
            data['title'] = xml_utils.get_text_from_node(title)
    
        for paragraph in ack.findall('.//p'):
            data['paragraphs'].append(xml_utils.get_segments_from_node(paragraph))

    return data
