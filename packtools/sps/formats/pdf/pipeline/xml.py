from packtools.sps.formats.pdf.utils import xml_utils


def extract_article_main_language(xml_tree, namespaces={'xml': 'http://www.w3.org/XML/1998/namespace'}):
    """
    Extracts the main language of the article from the given XML tree.
    
    Args:
        xml_tree (ElementTree): The XML tree to extract the main language from.
        namespaces (dict, optional): A dictionary of namespace prefixes and their corresponding URIs. Defaults to {'xml': 'http://www.w3.org/XML/1998/namespace'}.
    
    Returns:
        str: The main language of the article.
    """
    lang_attrib_name = "{" + f'{namespaces["xml"]}' + "}lang"
    return xml_tree.attrib.get(lang_attrib_name)


def extract_category(xml_tree, return_text=True):
    """
    Extracts the category from the given XML tree.
    
    Args:
        xml_tree (ElementTree): The XML tree to extract the category from.
        return_text (bool, optional): If True, returns the text content of the category element. If False, returns the element itself. Defaults to True.
    
    Returns:
        str or ElementTree: The category text or the category element, depending on the value of the `return_text` parameter.
    """
    node = xml_tree.find('.//subj-group[@subj-group-type="heading"]/subject')
    if return_text:
        return ''.join(node.itertext()).strip()
    return node

def extract_article_title(xml_tree, return_text=True):
    """
    Extracts the article title from the given XML tree.
    
    Args:
        xml_tree (ElementTree): The XML tree to extract the article title from.
        return_text (bool, optional): If True, returns the text content of the article-title element. If False, returns the element itself. Defaults to True.
    
    Returns:
        str or ElementTree: The article title text or the article-title element, depending on the value of the `return_text` parameter.
    """
    node = xml_tree.find('.//article-title')
    if return_text:
        return ''.join(node.itertext()).strip()
    return node
def extract_abstract_data(xml_tree):
    """
    Extracts the title and content of the abstract from the given XML tree.
    
    Args:
        xml_tree (ElementTree): The XML tree to extract the abstract from.
    
    Returns:
        dict: A dictionary containing the following keys:
            - 'title': The text content of the abstract title element, or an empty string if not found.
            - 'content': The text content of the abstract paragraphs, concatenated into a single string.
    """
    data = {'title': '', 'content': ''}

    node_abstract = xml_tree.find(f'.//abstract')
    if node_abstract is not None:
        node_title = node_abstract.find('title')
    
        if node_title is not None:
            data['title'] = ''.join(node_title.itertext()).strip()

        abstract = []
        for p in node_abstract.findall('p'):
            if p is not None:
                abstract.append(''.join(p.itertext()).strip())
        data['content'] = ' '.join(abstract)

    return data

def extract_trans_abstract_data(xml_tree, namespaces={'xml': 'http://www.w3.org/XML/1998/namespace'}):
    """
    Extracts the title and content of translated abstracts from the given XML tree.
    
    Args:
        xml_tree (ElementTree): The XML tree to extract the translated abstracts from.
        namespaces (dict, optional): A dictionary of XML namespaces to use in the XPath expressions.
    
    Returns:
        list: A list of dictionaries, where each dictionary contains the following keys:
            - 'lang': The language of the translated abstract.
            - 'title': The title of the translated abstract.
            - 'content': The content of the translated abstract.
    """ 
    data = []

    lang_attrib_name = "{" + f'{namespaces["xml"]}' + "}lang"

    for node in xml_tree.findall('.//trans-abstract'):
        item = {'lang': '', 'title': '', 'content': ''}

        node_title = node.find('title')
        if node_title is not None:
            item['title'] = node_title.text or ''

        item['lang'] = node.attrib.get(lang_attrib_name)

        abstract = []
        for p in node.findall('p'):
            if p is not None:
                abstract.append(p.text or '')
        item['content'] = ' '.join(abstract)

        data.append(item)
    
    return data

def extract_keywords_data(xml_tree, lang='en', namespaces={'xml': 'http://www.w3.org/XML/1998/namespace'}):
    """
    Extracts keyword data from the given XML tree.
    
    Args:
        xml_tree (ElementTree): The XML tree to extract the keyword data from.
        lang (str, optional): The language of the keywords to extract. Defaults to 'en'.
        namespaces (dict, optional): A dictionary of XML namespaces to use in the XPath expressions.
    
    Returns:
        dict: A dictionary containing the following keys:
            - 'title': The text content of the keyword group title element, or an empty string if not found.
            - 'keywords': A comma-separated string of the keyword text contents.
    """
    data = {'title': '', 'keywords': ''}

    kwd_group = xml_tree.find(f'.//kwd-group[@xml:lang="{lang}"]', namespaces)
     
    if kwd_group is not None:
        node_title = kwd_group.find('title')
        if node_title is not None:
            data['title'] = node_title.text

        data['keywords'] = ', '.join([kwd.text for kwd in kwd_group.findall('kwd')])

    return data

def extract_body_data(xml_tree):
    """
    Extracts the body data from an XML tree, including section titles, paragraphs, and tables.
    
    Args:
        xml_tree (ElementTree): The XML tree to extract the body data from.
    
    Returns:
        list: A list of dictionaries, where each dictionary represents a section in the body of the document. Each dictionary has the following keys:
            - 'level': The nesting level of the section.
            - 'title': The title of the section, if present.
            - 'paragraphs': A list of the text content of each paragraph in the section, excluding paragraphs that contain table references or table wrappers.
            - 'tables': A list of dictionaries representing the tables in the section, as returned by the `extract_table_data` function.
    """
    data = []

    for document_section in xml_tree.findall('.//sec'):
        sec = {'paragraphs': [], 'tables': []}
        sec['level'] = xml_utils.get_node_level(document_section, xml_tree)
        sec['title'] = document_section.find('title')

        if sec['title'] is not None:
            sec['title'] = sec['title'].text
            for para in document_section.findall('p'):
                has_table_ref = para.find('.//xref[@ref-type="table"]') is not None
                has_table_wrap = para.find('.//table-wrap') is not None

                if not has_table_ref and not has_table_wrap:
                    para_text = xml_utils.get_text_from_node(para)
                    if para_text:
                        sec['paragraphs'].append(para_text)

            for table_wrap in document_section.findall('.//table-wrap'):
                sec['tables'].append(extract_table_data(table_wrap))

        data.append(sec)
    
    return data

def extract_acknowledgment_data(xml_tree):
    """
    Extracts acknowledgment data from an XML tree.
    
    Args:
        xml_tree (ElementTree): The XML tree to extract the acknowledgment data from.
    
    Returns:
        dict: A dictionary containing the acknowledgment data, with the following keys:
            - 'title': The title of the acknowledgment section, if present.
            - 'paragraphs': A list of the text content of each paragraph in the acknowledgment section.
    """
    data = {'paragraphs': [], 'title': ''}

    ack = xml_tree.find('.//ack')
    if ack is not None:
        title = ack.find('title')
        if title is not None:
            data['title'] = title.text
    
        for paragraph in ack.findall('.//p'):
            data['paragraphs'].append(paragraph.text)

    return data

def extract_references_data(xml_tree):
    """
    Extracts reference data from an XML tree.
    
    Args:
        xml_tree (ElementTree): The XML tree to extract the reference data from.
    
    Returns:
        dict: A dictionary containing the reference data, with the following keys:
            - 'title': The title of the references section, which is set to 'References'.
            - 'references': A list of the mixed-citation elements from the ref-list in the XML tree.
    """
    data = {'title': 'References', 'references':[]}

    ref_list = xml_tree.find('.//ref-list')
    if ref_list is not None:
        for ref in ref_list.findall('.//mixed-citation'):
            data['references'].append(ref)

    return data

def extract_supplementary_data(xml_tree):
    """
    Extracts supplementary data from an XML tree.

    Args:
        xml_tree (ElementTree): The XML tree to extract the supplementary data from.

    Returns:
        dict: A dictionary containing the supplementary data, with the following keys:
            - 'title': The title of the supplementary section, if present.
            - 'paragraphs': A list of the text content of each paragraph in the supplementary section.
    """
    data = {'title': 'Supplementary Material', 'elements': []}

    app_groups = xml_tree.findall('.//app-group')
    if app_groups:
        for app_group in app_groups:
            for element in app_group:
                if element.text:
                    data['elements'].append({'content': element.text, 'type': 'text'})

                for table_wrap in element.findall('.//table-wrap'):
                    data['elements'].append({
                        'type': 'table',
                        'content': extract_table_data(table_wrap)
                    })
    return data

def extract_table_data(table_wrap):
    """
    Extracts table data from an XML table-wrap element.
    
    Args:
        table_wrap (ElementTree): The XML table-wrap element to extract data from.
    
    Returns:
        dict: A dictionary containing the following keys:
            - 'label': The text content of the table label element, or an empty string if not found.
            - 'title': The text content of the table title element, or an empty string if not found.
            - 'headers': A list of lists, where each inner list represents the text content of the table header cells.
            - 'rows': A list of lists, where each inner list represents the text content of the table data cells.
    """
    table_label = table_wrap.find('.//label')
    label_text = table_label.text if table_label is not None else ""

    table_title = table_wrap.find('.//title')
    title_text = table_title.text if table_title is not None else ""

    headers = []
    rows = []
    table = table_wrap.find('.//table')

    if table is not None:
        thead = table.find('.//thead')
        if thead is not None:
            headers = [[th.text for th in tr.findall('.//th')] for tr in thead.findall('.//tr')]

        tbody = table.find('.//tbody')
        if tbody is not None:
            rows = [[td.text for td in tr.findall('.//td')] for tr in tbody.findall('.//tr')]

    return {'label': label_text, 'title': title_text, 'headers': headers, 'rows': rows}
