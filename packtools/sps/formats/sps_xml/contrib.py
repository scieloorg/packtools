"""
data = {
    "contrib_type": "author",
    "contrib_ids": {
        "orcid": "0000-0001-8528-2091",
        "scopus": "24771926600"
    },
    "surname": "Einstein",
    "given_names": "Albert",
    "affiliations": [
        {"rid": "aff1", "text": "1"}
    ]
}
"""

import xml.etree.ElementTree as ET


def build_contrib_author(data):
    # Garantir que o contrib_type seja uma string válida ou usar 'author' como padrão
    contrib_type = data.get("contrib_type") or "author"

    # Criação do elemento principal <contrib> com o tipo de contribuição
    contrib_elem = ET.Element("contrib", attrib={"contrib-type": contrib_type})

    # Adiciona os elementos <contrib-id> para ORCID e Scopus
    for contrib_id_type, contrib_id_value in data.get('contrib_ids', {}).items():
        if contrib_id_value:  # Verifica se o valor não é None
            contrib_id_elem = ET.Element("contrib-id", attrib={"contrib-id-type": contrib_id_type})
            contrib_id_elem.text = contrib_id_value
            contrib_elem.append(contrib_id_elem)  # Usando append para adicionar ao pai

    # Cria e adiciona o <name> com <surname> e <given-names>
    name_elem = ET.Element("name")

    surname_elem = ET.Element("surname")
    surname_elem.text = data.get("surname", "")
    name_elem.append(surname_elem)  # Adiciona <surname> ao <name>

    given_names_elem = ET.Element("given-names")
    given_names_elem.text = data.get("given_names", "")
    name_elem.append(given_names_elem)  # Adiciona <given-names> ao <name>

    contrib_elem.append(name_elem)  # Adiciona <name> ao <contrib>

    # Adiciona o <xref> para afiliação, apenas se rid e text não forem None
    for xref_data in data.get("affiliations", []):
        rid = xref_data.get("rid")
        text = xref_data.get("text")
        if rid and text:
            xref_elem = ET.Element("xref", attrib={"ref-type": "aff", "rid": rid})
            xref_elem.text = text
            contrib_elem.append(xref_elem)  # Adiciona <xref> ao <contrib>

    return contrib_elem
