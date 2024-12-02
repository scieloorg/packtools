from lxml import etree as ET


def build_article_meta(data, node=None):
    """
    Constrói o elemento XML 'article-meta' com base nos dados fornecidos.

    Args:
        data (dict): Dicionário contendo dados do artigo, como IDs de publicação,
                     título, contagens de elementos e informações sobre o artigo.
            Exemplo:
            {
                "pub-id-doi": "10.1016/j.bjane.2019.01.003",
                "pub-id-other": "00603",
                "article-subject": "Original Article",
                "article-title": "Conocimientos de los pediatras sobre la laringomalacia",
                "trans-title": {"en": "Pediatrician knowledge about laryngomalacia"},
                "volume": "69",
                "issue": "3",
                "fpage": "227",
                "lpage": "232",
                "fig-count": "5",
                "table-count": "3",
                "equation-count": "10",
                "ref-count": "26",
                "page-count": "6"
            }
        node (dict, opcional): Dicionário contendo elementos XML adicionais para
                               inclusão, como contribuições, resumos e permissões.
            Exemplo:
            {
                "contrib-group": [<Element>, <Element>],
                "affs": [<Element>, <Element>],
                "author-notes": <Element>,
                "pub-dates": [<Element>, <Element>],
                "abstract": <Element>,
                "trans-abstracts": [<Element>, <Element>],
                "kwd-group": [<Element>, <Element>],
                "history": <Element>,
                "permissions": <Element>,
                "funding-group": <Element>,
            }

    Returns:
        xml.etree.ElementTree.Element: Elemento 'article-meta' contendo a estrutura
                                       XML completa do artigo.
    """
    article_meta = ET.Element("article-meta")
    process_pub_ids(data, article_meta)
    process_article_subject(data, article_meta)
    process_article_title(data, article_meta)
    if node:
        process_contribs(node, article_meta)
        keys = ("affs", "author-notes", "pub-dates")
        process_node_elements(node, article_meta, keys)

    process_standard_items(data, article_meta)
    if node:
        keys = ("abstract", "trans-abstracts", "kwd-group", "history", "permissions", "funding-group")
        process_node_elements(node, article_meta, keys)
    process_counts(data, article_meta)

    return article_meta


def process_pub_ids(data, article_meta):
    """
    Adiciona IDs de publicação ao elemento 'article-meta'.

    Args:
        data (dict): Dicionário contendo valores para IDs de publicação.
            Exemplo:
            {
                "pub-id-doi": "10.1016/j.bjane.2019.01.003",
                "pub-id-other": "00603"
            }
        article_meta (xml.etree.ElementTree.Element): Elemento 'article-meta' onde
                                                      os IDs de publicação serão adicionados.
    """
    for pub_id_type in ("pub-id-doi", "pub-id-other"):
        if pub_id_value := data.get(pub_id_type):
            pub_id_type = pub_id_type.replace("pub-id-", "")
            ET.SubElement(
                article_meta, "article-id", attrib={"pub-id-type": pub_id_type}
            ).text = pub_id_value


def process_article_subject(data, article_meta):
    """
    Adiciona o elemento 'article-categories' ao 'article-meta' com a categoria do artigo.

    Args:
        data (dict): Dicionário contendo o assunto do artigo.
            Exemplo:
            {
                "article_subject": "Original Article"
            }
        article_meta (xml.etree.ElementTree.Element): Elemento 'article-meta' onde
                                                      o assunto será adicionado.
    """
    if subject_text := data.get("article-subject"):
        article_categories_elem = ET.SubElement(article_meta, "article-categories")
        subj_group_elem = ET.SubElement(
            article_categories_elem, "subj-group", attrib={"subj-group-type": "heading"}
        )
        ET.SubElement(subj_group_elem, "subject").text = subject_text


def process_article_title(data, article_meta):
    """
    Adiciona o título do artigo e suas traduções ao 'article-meta'.

    Args:
        data (dict): Dicionário contendo o título do artigo e suas traduções.
            Exemplo:
            {
                "article-title": "Conocimientos de los pediatras sobre la laringomalacia",
                "trans-title": {
                    "en": "Pediatrician knowledge about laryngomalacia"
                }
            }
        article_meta (xml.etree.ElementTree.Element): Elemento `article-meta` onde
                                                      o título e traduções serão adicionados.
    """
    if article_title_text := data.get("article-title"):
        title_group_elem = ET.SubElement(article_meta, "title-group")
        ET.SubElement(title_group_elem, "article-title").text = article_title_text

        trans_title_dict = data.get("trans-title", {})
        for lang, text in trans_title_dict.items():
            trans_title_group_elem = ET.SubElement(
                title_group_elem, "trans-title-group", attrib={"{http://www.w3.org/XML/1998/namespace}lang": lang}
            )
            ET.SubElement(trans_title_group_elem, "trans-title").text = text


def process_contribs(node, article_meta):
    """
    Adiciona o grupo de contribuições ao `article-meta`.

    Args:
        node (dict): Dicionário contendo o grupo de contribuições.
            Exemplo:
            {
                "contrib-group": [<Element>, <Element>]
            }
        article_meta (xml.etree.ElementTree.Element): Elemento 'article-meta' onde
                                                      o grupo de contribuições será adicionado.
    """
    if contribs := node.get("contrib-group"):
        contrib_group_elem = ET.SubElement(article_meta, "contrib-group")
        for contrib in contribs:
            contrib_group_elem.append(contrib)


def process_standard_items(data, article_meta):
    """
    Adiciona elementos padrão como volume, issue, fpage e lpage ao 'article-meta'.

    Args:
        data (dict): Dicionário contendo os valores dos itens padrão.
            Exemplo:
            {
                "volume": "69",
                "issue": "3",
                "fpage": "227",
                "lpage": "232"
            }
        article_meta (xml.etree.ElementTree.Element): Elemento 'article-meta' onde
                                                      os itens padrão serão adicionados.
    """
    for item in ("volume", "issue", "fpage", "lpage"):
        if elem_text := data.get(item):
            ET.SubElement(article_meta, item).text = elem_text


def process_node_elements(node, article_meta, keys):
    """
    Adiciona elementos específicos ao 'article-meta' com base em uma lista de chaves.

    Args:
        node (dict): Dicionário contendo os elementos a serem adicionados.
            Exemplo:
            {
                "affs": [<Element>, <Element>],
                "author-notes": <Element>,
                "pub-dates": [<Element>, <Element>]
            }
        article_meta (xml.etree.ElementTree.Element): Elemento 'article-meta' onde
                                                      os elementos serão adicionados.
        keys (tuple): Lista de chaves para elementos a serem adicionados ao 'article-meta'.
    """
    for elem_name in keys:
        if elements := node.get(elem_name):
            if isinstance(elements, list):
                for elem in elements:
                    article_meta.append(elem)
            else:
                article_meta.append(elements)


def process_counts(data, article_meta):
    """
    Adiciona contagem de elementos como figuras, tabelas, e referências ao 'article-meta'.

    Args:
        data (dict): Dicionário contendo os valores de contagem.
            Exemplo:
            {
                "fig-count": "5",
                "table-count": "3",
                "equation-count": "10",
                "ref-count": "26",
                "page-count": "6"
            }
        article_meta (xml.etree.ElementTree.Element): Elemento 'article-meta' onde
                                                      as contagens serão adicionadas.
    """
    counts = ("fig-count", "table-count", "equation-count", "ref-count", "page-count")
    if any(data.get(count) for count in counts):
        counts_elem = ET.SubElement(article_meta, "counts")
        for count in counts:
            if count_value := data.get(count):
                ET.SubElement(counts_elem, count, attrib={"count": count_value})
