"""Metadados do artigo usados na primeira página e nos cabeçalhos/rodapés do PDF."""


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


def extract_article_type(xml_tree):
    """
    Extracts the article type from the given XML tree.
    
    Args:
        xml_tree (ElementTree): The XML tree to extract the article type from.
    
    Returns:
        str: The article type.
    """
    return xml_tree.attrib.get('article-type')


def extract_journal_title(xml_tree, return_text=True):
    """
    Extracts the journal title from the given XML tree.
    
    Args:
        xml_tree (ElementTree): The XML tree to extract the journal title from.
        return_text (bool, optional): If True, returns the text content of the journal-title element. If False, returns the element itself. Defaults to True.
    
    Returns:
        str or ElementTree: The journal title text or the journal-title element, depending on the value of the `return_text` parameter.
    """
    node = xml_tree.find('.//journal-title')
    if return_text:
        return ''.join(node.itertext()).strip()
    return node


def extract_doi(xml_tree, return_text=True):
    """
    Extracts the DOI (Digital Object Identifier) code from the given XML tree.
    
    Args:
        xml_tree (ElementTree): The XML tree to extract the DOI code from.
        return_text (bool, optional): If True, returns the text content of the DOI element. If False, returns the element itself. Defaults to True.
    
    Returns:
        str or ElementTree: The DOI code text or the DOI element, depending on the value of the `return_text` parameter.
    """
    node = xml_tree.find('.//article-id[@pub-id-type="doi"]')
    if return_text:
        return node.text
    return node


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


def extract_contrib_data(xml_tree):
    """
    Extracts contributor data from the given XML tree, including author names, affiliations, and corresponding author information.
    
    Args:
        xml_tree (ElementTree): The XML tree to extract contributor data from.
    
    Returns:
        dict: A dictionary containing the following keys:
            - 'authors_names': A list of author names, with affiliations and corresponding author mark if applicable.
            - 'affiliations': A list of affiliations, with label and institution name.
            - 'corresponding_author': The corresponding author information, including email and ORCID if available.
    """
    authors_names = []    
    affiliations = []
    corresponding_author = ''

    article_meta = xml_tree.find('./front/article-meta')
    metadata_scope = article_meta if article_meta is not None else xml_tree
    contrib_group = metadata_scope.find('.//contrib-group')
    if contrib_group is not None:
        aff_mapping = {}
        affs = metadata_scope.findall('.//aff')

        for aff in affs:
            aff_id = aff.get('id')
            label = aff.find('label').text if aff.find('label') is not None else ''
            institution = aff.find('institution[@content-type="original"]')
            institution_name = institution.text if institution is not None else ''
            aff_mapping[aff_id] = (label, institution_name)

        for contrib in contrib_group.findall('.//contrib'):
            name = contrib.find('name')
            if name is not None:
                surname = name.find('surname')
                given_names = name.find('given-names')
                xref_aff = contrib.find('.//xref[@ref-type="aff"]')
                xref_corresp = contrib.find('.//xref[@ref-type="corresp"]')
                corresp_mark = '*' if xref_corresp is not None else ''

                if surname is not None and given_names is not None:
                    full_name = f"{given_names.text} {surname.text}[^]"

                    if xref_aff is not None:
                        aff_ref_id = xref_aff.get('rid', '')
                        if aff_ref_id in aff_mapping:
                            label, institution_name = aff_mapping[aff_ref_id]
                            if label:
                                full_name += label
                    full_name += corresp_mark
                    authors_names.append(full_name)

        for aff in affs:
            label = aff.find('label').text if aff.find('label') is not None else ''
            institution = aff.find('institution[@content-type="original"]')
            institution_name = institution.text if institution is not None else ''

            if institution_name:
                aff_info = f"{label}[^] {institution_name}"
                affiliations.append(aff_info)

    corresp = xml_tree.find('.//author-notes//corresp')
    if corresp is not None:
        email = corresp.find('.//email')
        if email is not None:
            orcid = contrib_group.find('.//contrib-id[@contrib-id-type="orcid"]')
            orcid_text = f"; https://orcid.org/{orcid.text}" if orcid is not None else ''

            corresponding_author = f"*[^] Corresponding author: {email.text}{orcid_text}"

    return {'authors_names': authors_names, 'affiliations': affiliations, 'corresponding_author': corresponding_author}


def extract_abstract_data(xml_tree):
    """
    Extracts the title and content of the abstract from the given XML tree.

    Handles both a plain abstract (<p> direct children of <abstract>) and a
    structured one (subsections wrapped in <sec>, e.g. Introduction/Methods/
    Results, each with its own <title> and <p>) - see _extract_abstract_paragraphs.

    Args:
        xml_tree (ElementTree): The XML tree to extract the abstract from.

    Returns:
        dict: A dictionary containing the following keys:
            - 'title': The text content of the abstract title element, or an empty string if not found.
            - 'content': The text content of the abstract paragraphs (and, for a
              structured abstract, each subsection's title), concatenated into a
              single string.
    """
    data = {'title': '', 'content': ''}

    node_abstract = xml_tree.find(f'.//abstract')
    if node_abstract is not None:
        node_title = node_abstract.find('title')
    
        if node_title is not None:
            data['title'] = ''.join(node_title.itertext()).strip()

        data['content'] = ' '.join(_extract_abstract_paragraphs(node_abstract))

    return data


def extract_trans_abstract_data(xml_tree, namespaces={'xml': 'http://www.w3.org/XML/1998/namespace'}):
    """
    Extracts the title and content of translated abstracts from the given XML tree.

    Handles both a plain and a structured trans-abstract (subsections wrapped
    in <sec>) the same way extract_abstract_data does - see
    _extract_abstract_paragraphs.

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
            item['title'] = ''.join(node_title.itertext()).strip()

        item['lang'] = node.attrib.get(lang_attrib_name)

        item['content'] = ' '.join(_extract_abstract_paragraphs(node))

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
            data['title'] = ''.join(node_title.itertext()).strip()

        data['keywords'] = ', '.join(
            ''.join(kwd.itertext()).strip() for kwd in kwd_group.findall('kwd')
        )

    return data


def extract_footer_data(xmltree):
    """
    Extracts footer data from the given XML tree.

    Args:
        xmltree (ElementTree): The XML tree to extract the footer data from.

    Returns:
        dict: A dictionary containing the following keys:
            - 'year': The year value from the pub-date element.
            - 'front': The parent element of the pub-date element.
            - 'volume': The volume value from the front element.
            - 'issue': The issue value from the front element.
            - 'fpage': The first page value from the front element, converted to an integer.
            - 'lpage': The last page value from the front element, converted to an integer.
            - 'elocation_id': The elocation-id value from the front element.
            - 'location_label': '{fpage}-{lpage}' when fpage is present, otherwise
              elocation_id, otherwise an empty string. Continuous-publication
              articles carry elocation-id instead of fpage/lpage.
    """
    data = {'year': '', 'volume': '', 'issue': '', 'fpage': '', 'lpage': '', 'elocation_id': ''}

    pub_date_section = xmltree.find(".//pub-date[@date-type='collection'][@publication-format='electronic']")
    if pub_date_section is not None:
        node_year = pub_date_section.find('.//year')
        if node_year is not None:
            data['year'] = node_year.text

        node_front = pub_date_section.getparent()
        if node_front is not None:
            node_fpage = node_front.find('.//fpage')
            if node_fpage is not None:
                data['fpage'] = int(node_fpage.text)

            node_lpage = node_front.find('.//lpage')
            if node_lpage is not None:
                data['lpage'] = int(node_lpage.text)

            node_vol =   node_front.find('.//volume')
            if node_vol is not None:
                data['volume'] = node_vol.text

            node_issue = node_front.find('.//issue')
            if node_issue is not None:
                data['issue'] = node_issue.text

            node_elocation_id = node_front.find('.//elocation-id')
            if node_elocation_id is not None:
                data['elocation_id'] = node_elocation_id.text

    if data['fpage']:
        data['location_label'] = f"{data['fpage']}-{data['lpage']}"
    elif data['elocation_id']:
        data['location_label'] = data['elocation_id']
    else:
        data['location_label'] = ''

    return data


def _extract_abstract_paragraphs(node):
    """
    Collects an abstract's readable text as a list of strings, one per
    <p> found at any depth. A structured abstract wraps each subsection
    in its own <sec> (e.g. <sec><title>Methods:</title><p>...</p></sec>),
    so a plain `node.findall('p')` (direct children only) misses every
    paragraph and returns an empty abstract. Recursing into <sec> finds
    them, and including each <sec>'s own <title> in the flattened output
    preserves the abstract's structure instead of silently merging
    distinct subsections together. Some XMLs already carry a trailing
    colon in the title (e.g. "Methods:"), others don't (e.g. "Methods");
    a colon is appended only when the title lacks its own closing
    punctuation, so it never gets duplicated.

    Args:
        node (ElementTree): The <abstract> or <trans-abstract> element
            (or a <sec> within one, for the recursive call).

    Returns:
        list: Text fragments in document order - <sec> titles and <p> content.
    """
    parts = []
    for child in node:
        if child.tag == 'p':
            parts.append(''.join(child.itertext()).strip())
        elif child.tag == 'sec':
            sec_title = child.find('title')
            if sec_title is not None:
                title_text = ''.join(sec_title.itertext()).strip()
                if title_text:
                    if title_text[-1] not in ':.!?;':
                        title_text = f'{title_text}:'
                    parts.append(title_text)
            parts.extend(_extract_abstract_paragraphs(child))
    return parts
