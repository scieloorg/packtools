"""
data = {
    "contrib_type": "author",
    "orcid": "0000-0001-8528-2091",
    "scopus": "24771926600",
    "surname": "Einstein",
    "given_names": "Albert",
    "affiliations": [
        {"rid": "aff1", "text": "1"}
    ]
}
"""

import xml.etree.ElementTree as ET


def build_contrib_author(data):
    # Garantir que o contrib_type seja uma string válida
    contrib_type = data.get("contrib_type")
    if not contrib_type:
        raise NameError("contrib-type is required")

    # Criação do elemento principal <contrib> com o tipo de contribuição
    contrib_elem = ET.Element("contrib", attrib={"contrib-type": contrib_type})

    for contrib_id_type in ("lattes", "orcid", "researchid", "scopus"):
        contrib_id_value = data.get(contrib_id_type)
        if contrib_id_value:
            contrib_id_elem = ET.Element("contrib-id", attrib={"contrib-id-type": contrib_id_type})
            contrib_id_elem.text = contrib_id_value
            contrib_elem.append(contrib_id_elem)

    if data.get("collab"):
        collab_elem = ET.Element("collab")
        collab_elem.text = data["collab"]
        contrib_elem.append(collab_elem)

    # Cria e adiciona o <name> com <surname> e <given-names> somente se existirem no dicionário

    if any(data.get(key) for key in ("surname", "given_names", "prefix", "suffix")):
        name_elem = ET.Element("name")

        if data.get("surname"):  # Adiciona <surname> somente se estiver presente no dicionário
            surname_elem = ET.Element("surname")
            surname_elem.text = data["surname"]
            name_elem.append(surname_elem)

        if data.get("given_names"):  # Adiciona <given-names> somente se estiver presente no dicionário
            given_names_elem = ET.Element("given-names")
            given_names_elem.text = data["given_names"]
            name_elem.append(given_names_elem)

        if data.get("prefix"):  # Adiciona <prefix> somente se estiver presente no dicionário
            prefix_elem = ET.Element("prefix")
            prefix_elem.text = data["prefix"]
            name_elem.append(prefix_elem)

        if data.get("suffix"):  # Adiciona <suffix> somente se estiver presente no dicionário
            suffix_elem = ET.Element("suffix")
            suffix_elem.text = data["suffix"]
            name_elem.append(suffix_elem)

        contrib_elem.append(name_elem)

    # Adiciona o <xref> para afiliação apenas se rid ou text forem fornecidos no dicionário
    for xref_data in data.get("affiliations") or []:
        # rid é obrigatório, a ausência da chave deveria levantar exceção
        try:
            xref_elem = ET.Element("xref", attrib={"ref-type": "aff", "rid": xref_data["rid"]})
            xref_elem.text = xref_data["text"]
        except KeyError as e:
            raise KeyError(f"{e} is required")

        contrib_elem.append(xref_elem)

    return contrib_elem

