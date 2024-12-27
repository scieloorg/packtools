"""
data = [
    {
        "person-group-type": "author",
        "persons": [
            {
                "surname": "Einstein",
                "given-names": "Albert",
                "prefix": "Prof.",
                "suffix": "Neto"
            }
        ],
        "collab": ["Instituto Brasil Leitor"],
        "role": ["Pesquisador"]
    }
]
"""

from lxml import etree as ET


def build_person_group(data):
    for person_group in data or []:
        person_group_type = person_group.get("person-group-type")
        if not person_group_type:
            raise ValueError("person-group-type is required")

        person_group_elem = ET.Element("person-group", attrib={"person-group-type": person_group_type})

        persons = person_group.get("persons")
        if persons:
            name_elem = ET.Element("name")
            for person in persons:
                for key, value in person.items():
                    if value:
                        elem = ET.Element(key)
                        elem.text = value
                        name_elem.append(elem)
            person_group_elem.append(name_elem)

        for collab_text in person_group.get("collab") or []:
            collab_elem = ET.Element("collab")
            collab_elem.text = collab_text
            person_group_elem.append(collab_elem)

        for role_text in person_group.get("role") or []:
            role_elem = ET.Element("role")
            role_elem.text = role_text
            person_group_elem.append(role_elem)

        yield person_group_elem
