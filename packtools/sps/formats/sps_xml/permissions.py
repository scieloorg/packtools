"""
data = {
    "copyright-statement": "Copyright © 2014 SciELO",
    "copyright-year": "2014",
    "copyright-holder": "SciELO",
    "licenses": [
        {
            "license-type": "open-access",
            "xlink:href": "http://creativecommons.org/licenses/by-nc-sa/4.0/",
            "xml:lang": "pt",
            "license-p": "This is an article published in open access under a Creative Commons license"
        }
    ]
}
"""

import xml.etree.ElementTree as ET


def build_permissions(data):
    permissions_elem = ET.Element("permissions")

    for item in ("copyright-statement", "copyright-year", "copyright-holder"):
        text = data.get(item)
        if text:
            elem = ET.Element(item)
            elem.text = text
            permissions_elem.append(elem)
            
    try:
        for license_dict in data["licenses"]:
            try:
                license_elem = ET.Element("license", attrib={
                    "license-type": license_dict["license-type"],
                    "xlink:href": license_dict["xlink:href"],
                    "xml:lang": license_dict["xml:lang"]
                })
                text = license_dict.get("license-p")
                if text:
                    license_elem.text = text
                permissions_elem.append(license_elem)
            except KeyError as e:
                raise ValueError(f"{e} is required")
    except KeyError:
        raise ValueError("licenses is required")
    except TypeError:
        raise TypeError("licenses must be a list")

    return permissions_elem
  