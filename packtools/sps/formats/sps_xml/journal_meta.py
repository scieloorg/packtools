"""
data = {
    "journal_ids": {
        "nlm-ta": "Braz J Med Biol Res",
        "publisher-id": "bjmbr"
    },
    "journal_title": "Brazilian Journal of Medical and Biological Research",
    "abbrev_journal_title": "Braz. J. Med. Biol. Res.",
    "issn": {
        "epub": "1414-431X",
        "ppub": "0100-879X"
    },
    "publisher_name": "Associação Brasileira de Divulgação Científica"
}
"""

import xml.etree.ElementTree as ET


def build_journal_meta(data):
    # Criação do elemento principal <journal-meta>
    journal_meta = ET.Element("journal-meta")

    # Adiciona <journal-id> elementos
    for journal_id_type, journal_id_value in data.get('journal_ids', {}).items():
        journal_id_elem = ET.Element("journal-id", attrib={"journal-id-type": journal_id_type})
        journal_id_elem.text = journal_id_value
        journal_meta.append(journal_id_elem)  # Adiciona ao <journal-meta>

    # Cria <journal-title-group> e seus elementos filhos
    journal_title_group = ET.Element("journal-title-group")

    journal_title_elem = ET.Element("journal-title")
    journal_title_elem.text = data.get('journal_title', '')
    journal_title_group.append(journal_title_elem)  # Adiciona <journal-title> ao <journal-title-group>

    abbrev_journal_title_elem = ET.Element("abbrev-journal-title", attrib={"abbrev-type": "publisher"})
    abbrev_journal_title_elem.text = data.get('abbrev_journal_title', '')
    journal_title_group.append(abbrev_journal_title_elem)  # Adiciona <abbrev-journal-title> ao <journal-title-group>

    journal_meta.append(journal_title_group)  # Adiciona <journal-title-group> ao <journal-meta>

    # Adiciona <issn> elementos
    for issn_type, issn_value in data.get('issn', {}).items():
        issn_elem = ET.Element("issn", attrib={"pub-type": issn_type})
        issn_elem.text = issn_value
        journal_meta.append(issn_elem)  # Adiciona <issn> ao <journal-meta>

    # Cria <publisher> e <publisher-name>
    publisher_elem = ET.Element("publisher")
    publisher_name_elem = ET.Element("publisher-name")
    publisher_name_elem.text = data.get('publisher_name', '')
    publisher_elem.append(publisher_name_elem)  # Adiciona <publisher-name> ao <publisher>

    journal_meta.append(publisher_elem)  # Adiciona <publisher> ao <journal-meta>

    return journal_meta
