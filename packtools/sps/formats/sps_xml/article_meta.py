"""
data = {
    "pub_id_doi": "10.1016/j.bjane.2019.01.003",
    "pub_id_other": "00603",
    "article_subject": "Original Article",
    "article_title": "Conocimientos de los pediatras sobre la laringomalacia",
    "trans_title": {
        "en": "Pediatrician knowledge about laryngomalacia",
    }
}
"""

import xml.etree.ElementTree as ET


def build_article_meta(data):
    article_meta = ET.Element("article-meta")

    for pub_id_type in ("pub_id_doi", "pub_id_other"):
        pub_id_value = data.get(pub_id_type)
        if pub_id_value:
            pub_id_type = pub_id_type.replace("pub_id_", "")
            pub_id_elem = ET.Element("article-id", attrib={"pub-id-type": pub_id_type})
            pub_id_elem.text = pub_id_value
            article_meta.append(pub_id_elem)

    subject_text = data.get("article_subject")
    if subject_text:
        article_categories_elem = ET.Element("article-categories")
        subj_group_elem = ET.Element("subj-group", attrib={"subj-group-type": "heading"})
        subject_elem = ET.Element("subject")
        subject_elem.text = subject_text
        subj_group_elem.append(subject_elem)
        article_categories_elem.append(subj_group_elem)
        article_meta.append(article_categories_elem)

    article_title_text = data.get("article_title")
    if article_title_text:
        title_group_elem = ET.Element("title-group")
        article_title_elem = ET.Element("article-title")
        article_title_elem.text = article_title_text
        title_group_elem.append(article_title_elem)

        trans_title_dict = data.get("trans_title")
        for lang, text in trans_title_dict.items() or {}:
            trans_title_group_elem = ET.Element("trans-title-group", attrib={"xml:lang": lang})
            trans_title_elem = ET.Element("trans-title")
            trans_title_elem.text = text
            trans_title_group_elem.append(trans_title_elem)
            title_group_elem.append(trans_title_group_elem)

        article_meta.append(title_group_elem)

    return article_meta
