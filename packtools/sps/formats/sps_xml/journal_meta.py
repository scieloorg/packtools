"""
data = {
    "journal_ids_nlm_ta": "Braz J Med Biol Res",
    "journal_ids_publisher_id": "bjmbr",
    "journal_title": "Brazilian Journal of Medical and Biological Research",
    "abbrev_journal_title": "Braz. J. Med. Biol. Res.",
    "issn_epub": "1414-431X",
    "issn_ppub": "0100-879X",
    "publisher_names": ["Associação Brasileira de Divulgação Científica"]
}
"""

import xml.etree.ElementTree as ET


def build_journal_meta(data):
    # Criação do elemento principal <journal-meta>
    journal_meta = ET.Element("journal-meta")

    for journal_id_type in ("journal_ids_nlm-ta", "journal_ids_publisher-id"):
        journal_id_value = data.get(journal_id_type)
        if journal_id_value:
            # Adiciona <journal-id> elementos, verificando se o valor não é None
            journal_id_type = journal_id_type.replace("journal_ids_", "")
            journal_id_elem = ET.Element("journal-id", attrib={"journal-id-type": journal_id_type})
            journal_id_elem.text = journal_id_value
            journal_meta.append(journal_id_elem)

    if any(data.get(key) for key in ("journal_title", "abbrev_journal_title")):
        # Cria <journal-title-group>
        journal_title_group = ET.Element("journal-title-group")

        if data.get('journal_title'):
            # Adiciona <journal-title> se o valor não é None
            journal_title_elem = ET.Element("journal-title")
            journal_title_elem.text = data.get('journal_title')

            journal_title_group.append(journal_title_elem)

        if data.get("abbrev_journal_title"):
            # Adiciona <abbrev-journal-title> se o valor não é None
            abbrev_journal_title_elem = ET.Element("abbrev-journal-title", attrib={"abbrev-type": "publisher"})
            abbrev_journal_title_elem.text = data.get('abbrev_journal_title')

            journal_title_group.append(abbrev_journal_title_elem)

        # Adiciona <journal-title-group> ao <journal-meta>
        journal_meta.append(journal_title_group)

    for issn_type in ("issn_epub", "issn_ppub"):
        issn_value = data.get(issn_type)
        if issn_value:
            issn_type = issn_type.replace("issn_", "")
            issn_elem = ET.Element("issn", attrib={"pub-type": issn_type})
            issn_elem.text = issn_value
            journal_meta.append(issn_elem)

    # Cria <publisher> e <publisher-name> se existirem no dicionáŕrio
    if data.get('publisher_names'):
        publisher_elem = ET.Element("publisher")
        for publisher_name in data["publisher_names"] or []:
            publisher_name_elem = ET.Element("publisher-name")
            publisher_name_elem.text = publisher_name
            publisher_elem.append(publisher_name_elem)

        journal_meta.append(publisher_elem)

    return journal_meta
