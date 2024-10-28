"""
data = {
    "author": [
        {
            "surname": "Einstein",
            "given_names": "Albert",
            "prefix": "Prof.",
            "suffix": "Neto"
        }
    ],
    "collab": ["Instituto Brasil Leitor"],
    "role": ["Pesquisador"]

}
"""

import xml.etree.ElementTree as ET


def build_person_group(data):
    for person_group_type in ("author", "compiler"):
        persons = data.get(person_group_type)
        if persons:
            break
    else:
        raise ValueError("person group type is required")

    person_group_elem = ET.Element("person-group", attrib={"person-group-type": person_group_type})

    if isinstance(persons, list):
        name_elem = ET.Element("name")
        for person in persons:
            if isinstance(person, dict):
                for key, value in person.items():
                    if value:
                        elem = ET.Element(key)
                        elem.text = value
                        name_elem.append(elem)
        person_group_elem.append(name_elem)

    collab_list = data.get("collab")
    if isinstance(collab_list, list):
        for collab_text in collab_list:
            collab_elem = ET.Element("collab")
            collab_elem.text = collab_text
            person_group_elem.append(collab_elem)

    role_list = data.get("role")
    if isinstance(role_list, list):
        for role_text in role_list:
            role_elem = ET.Element("role")
            role_elem.text = role_text
            person_group_elem.append(role_elem)

    return person_group_elem
