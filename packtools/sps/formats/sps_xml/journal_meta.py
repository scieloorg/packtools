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

    if "journal_ids" in data:
        journal_ids = data.get("journal_ids")
        if journal_ids is None:
            # Se journal_ids é um dicionário vazio, cria um <journal-id> vazio
            journal_id_elem = ET.Element("journal-id")
            journal_meta.append(journal_id_elem)  # Adiciona ao <journal-meta>
        elif journal_ids:
            # Adiciona <journal-id> elementos, verificando se o valor não é None
            for journal_id_type, journal_id_value in journal_ids.items():
                journal_id_elem = ET.Element("journal-id", attrib={"journal-id-type": journal_id_type})
                journal_id_elem.text = journal_id_value or ""  # Se journal_id_value for None ou vazio, usa ""
                journal_meta.append(journal_id_elem)  # Adiciona ao <journal-meta>

    if 'journal_title' in data or "abbrev_journal_title" in data:
        # Cria <journal-title-group>
        journal_title_group = ET.Element("journal-title-group")

        if 'journal_title' in data:
            # Adiciona <journal-title> se o valor for None, insere string vazia
            journal_title_elem = ET.Element("journal-title")
            journal_title_elem.text = data.get('journal_title') or ''

            journal_title_group.append(journal_title_elem)

        if "abbrev_journal_title" in data:
            # Adiciona <abbrev-journal-title>, verificando se o valor não é None
            abbrev_journal_title_elem = ET.Element("abbrev-journal-title", attrib={"abbrev-type": "publisher"})
            abbrev_journal_title_elem.text = data.get('abbrev_journal_title') or ''

            journal_title_group.append(abbrev_journal_title_elem)

        # Adiciona <journal-title-group> ao <journal-meta>
        journal_meta.append(journal_title_group)

    if "issn" in data:
        if data.get("issn") is None:
            issn_elem = ET.Element("issn")
            journal_meta.append(issn_elem)
        else:
            # Adiciona <issn> elementos, verificando se o valor não é None
            for issn_type, issn_value in (data.get('issn') or {}).items():
                issn_elem = ET.Element("issn", attrib={"pub-type": issn_type})
                issn_elem.text = issn_value or ""
                journal_meta.append(issn_elem)

    # Cria <publisher> e <publisher-name>, insere string vazia se o valor for None
    if 'publisher_name' in data:
        publisher_elem = ET.Element("publisher")
        publisher_name_elem = ET.Element("publisher-name")
        publisher_name_elem.text = data.get('publisher_name') or ''
        publisher_elem.append(publisher_name_elem)

        journal_meta.append(publisher_elem)

    return journal_meta
