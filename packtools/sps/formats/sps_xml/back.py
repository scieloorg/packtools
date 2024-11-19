"""
    node = {
        element: [<Element>,...],
        ...
    }

"""

import xml.etree.ElementTree as ET


def build_back(node):
    if not node:
        raise ValueError("A list of child elements is required.")

    back_elem = ET.Element("back")
    for element_name, element_list in node.items():
        back_elem.extend(element_list)

    return back_elem
