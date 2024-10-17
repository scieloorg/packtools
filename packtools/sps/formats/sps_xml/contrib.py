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
    contrib_type = data.get("contrib_type") or ""

    # Criação do elemento principal <contrib> com o tipo de contribuição
    contrib_elem = ET.Element("contrib", attrib={"contrib-type": contrib_type})

    # Adiciona os elementos <contrib-id> para ORCID e Scopus, se existirem no dicionário
    for contrib_id_type, contrib_id_value in data.get('contrib_ids', {}).items():
        contrib_id_elem = ET.Element("contrib-id", attrib={"contrib-id-type": contrib_id_type})
        contrib_id_elem.text = contrib_id_value
        contrib_elem.append(contrib_id_elem)

    # Cria e adiciona o <name> com <surname> e <given-names> somente se existirem no dicionário
    if "surname" in data or "given_names" in data:
        name_elem = ET.Element("name")

        if "surname" in data:  # Adiciona <surname> somente se estiver presente no dicionário
            surname_elem = ET.Element("surname")
            surname_elem.text = data.get("surname", "")  # Mesmo se for vazio, cria o elemento
            name_elem.append(surname_elem)

        if "given_names" in data:  # Adiciona <given-names> somente se estiver presente no dicionário
            given_names_elem = ET.Element("given-names")
            given_names_elem.text = data.get("given_names", "")  # Mesmo se for vazio, cria o elemento
            name_elem.append(given_names_elem)

        contrib_elem.append(name_elem)

    # Adiciona o <xref> para afiliação apenas se rid ou text forem fornecidos no dicionário
    for xref_data in data.get("affiliations", []):
        rid = xref_data.get("rid")
        text = xref_data.get("text")
        if rid is not None or text is not None:  # Certifica-se de que pelo menos um não seja None
            xref_elem = ET.Element("xref", attrib={"ref-type": "aff"})
            if rid is not None:
                xref_elem.set("rid", rid)
            if text is not None:
                xref_elem.text = text
            contrib_elem.append(xref_elem)

    return contrib_elem

