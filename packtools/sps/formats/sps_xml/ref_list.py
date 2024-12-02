from lxml import etree as ET

from packtools.sps.formats.sps_xml.ref import build_ref


def build_ref_list(data):
    """
    Constructs an XML "ref-list" element using provided reference data.

    Parameters:
        data (dict): A dictionary containing:
            - "title" (str): The title of the reference list (required).
            - "ref-list-node" (list, optional): A list of prebuilt XML elements to include as references.
            - "ref-list-dict" (list, optional): A list of dictionaries used to construct references
                                                using the 'build_ref' function.

    Returns:
        xml.etree.ElementTree.Element: An XML "ref-list" element containing the title and references.

    Raises:
        ValueError: If "title" is missing or neither "ref-list-node" nor "ref-list-dict" is provided.

    Example:
        data = {
            "title": "References",
            "ref-list-node": [<Element>, <Element>],  # List of prebuilt XML elements (optional)
            "ref-list-dict": [ref_dict, ref_dict]    # List of dictionaries to build references (optional)
        }
    """
    if not (title := data.get("title")):
        raise ValueError("Title is required")

    ref_list_elem = ET.Element("ref-list")
    ET.SubElement(ref_list_elem, "title").text = title

    if list_node := data.get("ref-list-node"):
        ref_list_elem.extend(list_node)
    elif list_dict := data.get("ref-list-dict"):
        ref_list_elem.extend(list(build_ref(ref) for ref in list_dict))
    else:
        raise ValueError("A list of references is required")

    return ref_list_elem