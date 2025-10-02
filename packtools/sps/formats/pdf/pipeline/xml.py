from packtools.sps.formats.pdf import enum as pdf_enum
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

    contrib_group = xml_tree.find('.//contrib-group')
    if contrib_group is not None:
        aff_mapping = {}

        for aff in xml_tree.findall('.//aff'):
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
        
        for aff in xml_tree.findall('.//aff'):
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
    """
    data = {'year': '', 'volume': '', 'issue': '', 'fpage': '', 'lpage': ''}

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

    return data

def extract_cite_as_part_one(xml_tree, return_node=False):
    """
    Extracts the first part of the "cite as" data from the given XML tree.
    
    Args:
        xml_tree (ElementTree): The XML tree to extract the "cite as" data from.
        return_node (bool, optional): If True, returns the XML node containing the "cite as" data. If False, returns the text content of the node. Defaults to False.
    
    Returns:
        str or ElementTree: The first part of the "cite as" data, either as a string or as an XML node, depending on the value of the `return_node` parameter.
    """
    fn_group = xml_tree.find('.//fn-group')
    
    if fn_group is not None:
        part_one = fn_group.find('.//fn[@fn-type="other"]/p')
        if part_one is not None:
            if return_node:
                return part_one
            else:
                return part_one.text

def extract_body_data(xml_tree):
    """
    Extracts the body data from an XML tree, including section titles, paragraphs, and tables.
    
    Args:
        xml_tree (ElementTree): The XML tree to extract the body data from.
    
    Returns:
        list: A list of dictionaries, where each dictionary represents a section in the body of the document. Each dictionary has the following keys:
            - 'level': The nesting level of the section.
            - 'title': The title of the section, if present.
            - 'paragraphs': A list of the text content of each paragraph in the section, excluding paragraphs that contain table/figure references or wrappers.
            - 'tables': A list of dictionaries representing the tables in the section, as returned by the `extract_table_data` function.
            - 'figures': A list of dictionaries representing figures in the section, as returned by the `extract_figure_data` function.
    """
    data = []
    seen_fig_keys = set()

    for document_section in xml_tree.findall('.//sec'):
        sec = {'paragraphs': [], 'tables': [], 'figures': []}
        sec['level'] = xml_utils.get_node_level(document_section, xml_tree)
        sec['title'] = document_section.find('title')

        if sec['title'] is not None:
            sec['title'] = ''.join(sec['title'].itertext()).strip()

        # Collect textual paragraphs but exclude figure/table elements
        for para in document_section.findall('p'):
            try:
                # Get text nodes that are not inside fig or table-wrap
                texts = para.xpath('.//text()[not(ancestor::fig) and not(ancestor::table-wrap)]')
                para_text = ' '.join(' '.join(texts).split()).strip()
            except Exception:
                # Fallback to generic text extraction
                para_text = xml_utils.get_text_from_node(para)
            if para_text:
                sec['paragraphs'].append(para_text)

        # Tables within the section
        for table_wrap in document_section.findall('.//table-wrap'):
            sec['tables'].append(extract_table_data(table_wrap))

        # Figures within the section (deduplicated across the body)
        for fig in document_section.findall('.//fig'):
            # Build a deduplication key: prefer @id; fallback to first href found
            fig_id = fig.get('id') or fig.get('xml:id')
            href = None
            g = fig.find('.//graphic')
            if g is not None:
                href = (
                    g.get('{http://www.w3.org/1999/xlink}href')
                    or g.get('xlink:href')
                    or g.get('href')
                )
            key = fig_id or (href or '')
            if key and key in seen_fig_keys:
                continue
            fig_data = extract_figure_data(fig)
            sec['figures'].append(fig_data)
            if key:
                seen_fig_keys.add(key)

        data.append(sec)
    
    return data

def extract_figure_data(fig_node):
    """
    Extracts figure metadata from a <fig> node.

    Args:
        fig_node (ElementTree): The XML <fig> element.

    Returns:
        dict: A dictionary with keys:
            - 'label': Figure label (e.g., "Figure 1")
            - 'caption': Caption text (title + paragraphs if present)
            - 'href': Path/URL from graphic/@xlink:href (or alternatives)
            - 'alt': Alternative text if present
    """
    def _get_href_from_node(node):
        # Try common attribute forms
        return (
            node.get('{http://www.w3.org/1999/xlink}href')
            or node.get('xlink:href')
            or node.get('href')
        )

    label_el = fig_node.find('label')
    label = (label_el.text or '').strip() if label_el is not None else ''

    caption_texts = []
    caption_el = fig_node.find('caption')
    if caption_el is not None:
        # Prefer title then paragraphs
        title_el = caption_el.find('title')
        if title_el is not None:
            caption_texts.append(''.join(title_el.itertext()).strip())
        for p in caption_el.findall('p'):
            txt = ''.join(p.itertext()).strip()
            if txt:
                caption_texts.append(txt)
    caption = ' '.join([c for c in caption_texts if c])

    # graphic may be direct child or inside <alternatives>
    href = None
    alt_text = None

    graphic = fig_node.find('.//graphic')
    if graphic is not None:
        href = _get_href_from_node(graphic)
        alt_text = graphic.get('alt') or graphic.get('alt-text')

    if href is None:
        alt = fig_node.find('.//alternatives')
        if alt is not None:
            preferred_ext_order = ('.png', '.jpg', '.jpeg', '.gif', '.tif', '.tiff')
            candidates = []
            for g in alt.findall('graphic'):
                _href = _get_href_from_node(g)
                if not _href:
                    continue
                # Extract potential size from content-type like 'scielo-267x140'
                ctype = (g.get('content-type') or '').lower()
                dims_area = 0
                import re
                m = re.search(r'(\d+)x(\d+)', ctype)
                if m:
                    try:
                        w = int(m.group(1))
                        h = int(m.group(2))
                        dims_area = w * h
                    except Exception:
                        dims_area = 0
                # Penalize obvious thumbnails
                is_thumbnail = '267x140' in ctype
                ext_rank = len(preferred_ext_order)
                lu = _href.lower()
                for i, ext in enumerate(preferred_ext_order):
                    if lu.endswith(ext):
                        ext_rank = i
                        break
                candidates.append({
                    'href': _href,
                    'dims_area': dims_area,
                    'ext_rank': ext_rank,
                    'is_thumbnail': is_thumbnail,
                    'alt': g.get('alt') or g.get('alt-text')
                })
            if candidates:
                # Choose best: avoid thumbnails, larger area first, then better extension
                candidates.sort(key=lambda c: (
                    c['is_thumbnail'],           # False (0) before True (1)
                    -c['dims_area'],              # larger first
                    c['ext_rank']                 # better extension first
                ))
                best = candidates[0]
                href = best['href']
                if alt_text is None:
                    alt_text = best.get('alt')

    return {
        'label': label,
        'caption': caption,
        'href': href,
        'alt': alt_text or '',
    }

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
    Extracts table data from an XML table-wrap element, handling merged cells.
    
    Args:
        table_wrap (ElementTree): The XML table-wrap element to extract data from.
    
    Returns:
        dict: A dictionary containing the following keys:
            - 'label': The text content of the table label element, or an empty string if not found.
            - 'title': The text content of the table title element, or an empty string if not found.
            - 'headers': A list of lists, where each inner list represents the text content of the table header cells.
            - 'rows': A list of lists, where each inner list represents the text content of the table data cells.
            - 'layout': A string indicating the table layout ('single-column-layout' or 'double-column-layout').
            - 'column_widths': A list of calculated column widths based on content.
    """
    table_label = table_wrap.find('.//label')
    label_text = table_label.text if table_label is not None else ""

    table_title = table_wrap.find('.//title')
    title_text = table_title.text if table_title is not None else ""

    headers = []
    rows = []
    table = table_wrap.find('.//table')
    layout = determine_table_layout(table_wrap)

    if table is not None:
        thead = table.find('.//thead')
        if thead is not None:
            headers = _extract_table_rows_with_merged_cells(thead, 'th')
            header_spans = _extract_table_spans(thead, 'th')
        else:
            header_spans = []

        tbody = table.find('.//tbody')
        if tbody is not None:
            rows = _extract_table_rows_with_merged_cells(tbody, 'td')
            row_spans = _extract_table_spans(tbody, 'td')
        else:
            row_spans = []

    # Calculate column widths based on content
    column_widths = _calculate_column_widths(headers, rows)
    
    return {
        'label': label_text,
        'title': title_text,
        'headers': headers,
        'rows': rows,
        'layout': layout,
        'column_widths': column_widths,
        'header_spans': header_spans,
        'row_spans': row_spans,
    }
