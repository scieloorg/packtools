import re
from pathlib import Path

from citeproc import Citation, CitationItem, CitationStylesBibliography, CitationStylesStyle, formatter
from citeproc.source.json import CiteProcJSON

from packtools.sps.formats.pdf import enum as pdf_enum
from packtools.sps.formats.pdf.utils import xml_utils

_CITATION_STYLES_DIR = Path(__file__).parent.parent / "citation_styles"

# Anchor phrases (pt/en) that mark a footnote as the "how to cite this
# article" note, replacing a bare `'cit' in signal.lower()` check (#1349
# review: too easy to false-positive/negative on an unrelated 3-letter
# substring). Matched case-insensitively against the <label> text, or the
# leading text of <p> when there's no <label>.
_CITE_AS_LABEL_PHRASES = (
    r'como\s+citar',
    r'cita(?:ç|c)[aã]o\s+sugerida',
    r'cite\s+this\s+article\s+as',
    r'how\s+to\s+cite\s+this\s+article',
    r'how\s+to\s+cite',
    r'cite\s+as',
)
_CITE_AS_LABEL_RE = re.compile('|'.join(_CITE_AS_LABEL_PHRASES), re.IGNORECASE)
_CITE_AS_LEADING_PHRASE_RE = re.compile(
    r'^\s*(?:' + '|'.join(_CITE_AS_LABEL_PHRASES) + r')\s*:?\s*',
    re.IGNORECASE,
)


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
            item['title'] = ''.join(node_title.itertext()).strip()

        item['lang'] = node.attrib.get(lang_attrib_name)

        abstract = []
        for p in node.findall('p'):
            if p is not None:
                abstract.append(''.join(p.itertext()).strip())
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

def extract_cite_as_part_one(xml_tree, return_node=False):
    """
    Extracts the first part of the "cite as" data from the given XML tree.

    fn-type="other" is a generic JATS bucket that publishers use for all
    sorts of unrelated footnotes (institutional acknowledgment, AI-use
    declaration, JEL codes, plagiarism policy, ZooBank registration...),
    so picking the first <fn fn-type="other"> in the document - regardless
    of what it actually says - often surfaces the wrong note in the PDF's
    citable CITE AS field (see issue #1349). Only a <fn> whose <label>
    (or, when there's no <label>, the leading text of its <p>) actually
    names it as a citation note - matched against _CITE_AS_LABEL_RE, e.g.
    "Como citar:", "CITE AS:", "How to cite this article" - is used;
    nothing is returned when no such note exists.

    When the note has no <label> of its own, the citation phrase lives
    inline at the start of <p> (e.g. "Como citar: Author AB..."), which
    would otherwise get printed a second time next to the caller's own
    "CITE AS: " prefix. That leading phrase is stripped in this case (but
    left alone when it's a separate <label>, since then it isn't part of
    the returned <p> text to begin with).

    Args:
        xml_tree (ElementTree): The XML tree to extract the "cite as" data from.
        return_node (bool, optional): If True, returns the XML node containing the "cite as" data. If False, returns the text content of the node. Defaults to False.

    Returns:
        str or ElementTree: The first part of the "cite as" data, either as a string or as an XML node, depending on the value of the `return_node` parameter.
    """
    for fn in xml_tree.findall('.//fn[@fn-type="other"]'):
        part_one = fn.find('p')
        if part_one is None:
            continue

        label = fn.find('label')
        signal = ''.join(label.itertext()) if label is not None else ''.join(part_one.itertext())[:40]
        if not _CITE_AS_LABEL_RE.search(signal):
            continue

        if return_node:
            return part_one

        text = xml_utils.get_text_from_node(part_one).strip()
        if label is None:
            text = _CITE_AS_LEADING_PHRASE_RE.sub('', text, count=1)
        return text


def _extract_citation_authors(xml_tree):
    """
    Returns the article's own contributors as Vancouver-style "Surname IN"
    strings (surname, then the initials of given names - lowercase
    particles like "da"/"de"/"dos" excluded from initials, e.g. "Bárbara
    Passos da Silva" -> "BPS").

    Args:
        xml_tree (ElementTree): The XML tree to extract authors from.

    Returns:
        list: Author strings in document order; empty if there's no
        <contrib-group> or no <contrib> has both <surname> and text.
    """
    article_meta = xml_tree.find('./front/article-meta')
    metadata_scope = article_meta if article_meta is not None else xml_tree
    contrib_group = metadata_scope.find('.//contrib-group')
    if contrib_group is None:
        return []

    authors = []
    for contrib in contrib_group.findall('.//contrib'):
        name = contrib.find('name')
        if name is None:
            continue
        surname = name.find('surname')
        if surname is None or not (surname.text or '').strip():
            continue

        given_names = name.find('given-names')
        initials = ''
        if given_names is not None and given_names.text:
            initials = ''.join(
                word[0].upper() for word in given_names.text.split() if word[:1].isupper()
            )

        author = surname.text.strip()
        if initials:
            author = f'{author} {initials}'
        authors.append(author)

    return authors


def _build_csl_reference(xml_tree, footer_data):
    """
    Builds a CSL-JSON reference dict (see
    https://docs.citationstyles.org/en/stable/specification.html#appendix-iv-variables)
    from the article's own metadata, for handing to citeproc-py.

    Authors are passed as CSL "literal" names (`_extract_citation_authors`'s
    "Surname IN" strings, already correct - lowercase particles like
    "da"/"de"/"dos" excluded from initials) rather than letting citeproc-py
    parse family/given names itself, since CSL's own name-parsing doesn't
    know Portuguese naming particles. citeproc-py still applies the style's
    own et-al truncation/ordering/punctuation rules on top of these,
    literal-or-not.

    Returns:
        dict, or None when there are no authors to build a reference from.
    """
    authors = _extract_citation_authors(xml_tree)
    if not authors:
        return None

    reference = {
        'id': 'cite-as',
        'type': 'article-journal',
        'author': [{'literal': author} for author in authors],
    }

    title = extract_article_title(xml_tree)
    if title:
        reference['title'] = title

    abbrev_journal = xml_tree.find('.//abbrev-journal-title')
    journal = (
        ''.join(abbrev_journal.itertext()).strip()
        if abbrev_journal is not None
        else extract_journal_title(xml_tree)
    )
    if journal:
        reference['container-title'] = journal

    year = footer_data.get('year') or ''
    if year:
        reference['issued'] = {'date-parts': [[year]]}

    volume = footer_data.get('volume') or ''
    if volume:
        reference['volume'] = volume

    issue = footer_data.get('issue') or ''
    if issue:
        reference['issue'] = issue

    location = footer_data.get('location_label') or ''
    if location:
        reference['page'] = location

    # Not extract_doi(): that function raises AttributeError on a missing
    # DOI by design (see test_extract_doi_missing_doi) - a DOI is just
    # another optional piece of a citation, not something to blow up over.
    doi_node = xml_tree.find('.//article-id[@pub-id-type="doi"]')
    doi = doi_node.text if doi_node is not None else None
    if doi:
        reference['DOI'] = doi

    return reference


def _format_via_citeproc(xml_tree, footer_data, csl_filename):
    """
    Renders a full citation for `xml_tree`/`footer_data` through citeproc-py
    using the named CSL style file (packaged under
    packtools/sps/formats/pdf/citation_styles/). Returns '' when there are
    no authors to build a reference from.
    """
    reference = _build_csl_reference(xml_tree, footer_data)
    if reference is None:
        return ''

    source = CiteProcJSON([reference])
    style = CitationStylesStyle(str(_CITATION_STYLES_DIR / csl_filename), validate=False)
    bibliography = CitationStylesBibliography(style, source, formatter.plain)
    citation = Citation([CitationItem(reference['id'])])
    bibliography.register(citation)
    bibliography.cite(citation, lambda missing_id: None)

    entries = list(bibliography.bibliography())
    return str(entries[0]) if entries else ''


# Only 'vancouver' exists today, backed by a packtools-adapted variant of
# the CSL "nlm-name-year" style (citation_styles/scielo_nlm_name_year.csl -
# see that file for what was changed and why). Kept as a plain function
# parameter/dict dispatch (instead of hardcoding the style name inline) so
# a future per-journal JSON config can plug in a different CSL file by name
# without changing build_full_citation's contract - the same
# not-wired-yet-to-config pattern as layout_config.load_page_attributes.
CITATION_STYLE_VANCOUVER = 'vancouver'

_CITATION_STYLE_CSL_FILES = {
    CITATION_STYLE_VANCOUVER: 'scielo_nlm_name_year.csl',
}


def build_full_citation(xml_tree, footer_data, style=CITATION_STYLE_VANCOUVER):
    """
    Builds a complete "how to cite this article" citation from the
    article's own metadata (authors, title, journal, volume/issue/location,
    DOI) via citeproc-py, for use as a fallback when
    `extract_cite_as_part_one` finds no explicit editorial note (see issue
    #1349's review: some articles simply don't carry one).

    `style` selects the citation format. Only CITATION_STYLE_VANCOUVER
    exists today; it's a plain parameter (not read from a config file) so a
    future per-journal JSON config can choose a different CSL style by name
    later without changing this function's contract - not wired to the
    CLI/API yet.

    Args:
        xml_tree (ElementTree): The XML tree to build the citation from.
        footer_data (dict): Output of `extract_footer_data` (year/volume/issue/location_label).
        style (str, optional): Citation format identifier. Defaults to CITATION_STYLE_VANCOUVER.

    Returns:
        str: The complete citation, or '' when the style is unknown or the
        article has no authors to build one from.
    """
    csl_filename = _CITATION_STYLE_CSL_FILES.get(style)
    if csl_filename is None:
        return ''
    return _format_via_citeproc(xml_tree, footer_data, csl_filename)

def extract_body_data(xml_tree, table_layout_overrides=None):
    """
    Extracts the body data from an XML tree, including section titles, paragraphs, and tables.

    Args:
        xml_tree (ElementTree): The XML tree to extract the body data from.
        table_layout_overrides (dict, optional): Maps a table-wrap @id to a forced
            layout ('single-column-layout' or 'double-column-layout'), bypassing
            `determine_table_layout`'s heuristic for that specific table.

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

        # Collect textual paragraphs but exclude figure/table elements. Uses
        # get_text_from_node (tail-preserving) rather than a bare
        # `.xpath('.//text()...')` + `' '.join(...)`, which inserted an
        # artificial space between every text-node fragment regardless of
        # whether the source had one there (e.g. "(<xref>...</xref>)" came
        # out as "( ... )", and "<xref/>; <xref/>" as "... ; ...").
        for para in document_section.findall('p'):
            para_text = xml_utils.get_text_from_node(para, skip_tags={'fig', 'table-wrap'}).strip()
            if para_text:
                sec['paragraphs'].append(para_text)

        for table_wrap in document_section.findall('.//table-wrap'):
            closest_sec = table_wrap.xpath('ancestor::sec[1]')
            if closest_sec and closest_sec[0] is not document_section:
                continue
            table_id = table_wrap.get('id') or table_wrap.get('xml:id')
            override_layout = (table_layout_overrides or {}).get(table_id)
            sec['tables'].append(extract_table_data(table_wrap, override_layout=override_layout))

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

    # graphic may be a direct child, or offered as several representations
    # inside <alternatives> - only match the direct child here so the latter
    # case falls through to the ranking logic below instead of grabbing the
    # first <graphic> in document order.
    href = None
    alt_text = None

    graphic = fig_node.find('graphic')
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
                is_scielo_web = (g.get('specific-use') or '').lower() == 'scielo-web'
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
                    'is_scielo_web': is_scielo_web,
                    'alt': g.get('alt') or g.get('alt-text')
                })
            if candidates:
                # Choose best: avoid thumbnails, prefer the SciELO Web
                # representation, larger area first, then better extension
                candidates.sort(key=lambda c: (
                    c['is_thumbnail'],           # False (0) before True (1)
                    not c['is_scielo_web'],       # scielo-web first
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

def extract_table_data(table_wrap, override_layout=None):
    """
    Extracts table data from an XML table-wrap element, handling merged cells.

    Args:
        table_wrap (ElementTree): The XML table-wrap element to extract data from.
        override_layout (str, optional): Forces 'layout' to this value instead of
            running `determine_table_layout`'s heuristic. Must be one of
            pdf_enum.SINGLE_COLUMN_PAGE_LABEL/DOUBLE_COLUMN_PAGE_LABEL, otherwise ignored.

    Returns:
        dict: A dictionary containing the following keys:
            - 'label': The text content of the table label element, or an empty string if not found.
            - 'title': The text content of the table title element, or an empty string if not found.
            - 'headers': A list of lists, where each inner list represents the text content of the table header cells.
            - 'rows': A list of lists, where each inner list represents the text content of the table data cells.
            - 'layout': A string indicating the table layout ('single-column-layout' or 'double-column-layout').
            - 'column_widths': A list of calculated column widths based on content.
            - 'foot': A list of footnote/attribution strings from <table-wrap-foot>, if present.
    """
    table_label = table_wrap.find('.//label')
    label_text = table_label.text if table_label is not None else ""

    table_title = table_wrap.find('.//title')
    title_text = table_title.text if table_title is not None else ""

    foot_notes = _extract_table_foot(table_wrap)

    headers = []
    rows = []
    header_spans = []
    row_spans = []
    table = table_wrap.find('.//table')
    layout = determine_table_layout(table_wrap, override=override_layout)

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
        'foot': foot_notes,
    }

_PATHOLOGICAL_CELL_LENGTH = 400

def determine_table_layout(table_wrap, override=None):
    """
    Determines the layout of a table based on the number of columns it contains,
    considering merged cells, with an escape hatch for an explicit override and a
    guard against a single excessively long cell (which the column-count heuristic
    alone can't catch: a table can have few columns and still need full width).

    Args:
        table_wrap (ElementTree): The XML table-wrap element to analyze.
        override (str, optional): Forces this layout instead of running the heuristic.
            Must be one of pdf_enum.SINGLE_COLUMN_PAGE_LABEL/DOUBLE_COLUMN_PAGE_LABEL,
            otherwise ignored.

    Returns:
        str: A string indicating the table layout. Possible values are 'single-column-layout' and 'double-column-layout'.
    """
    if override in (pdf_enum.SINGLE_COLUMN_PAGE_LABEL, pdf_enum.DOUBLE_COLUMN_PAGE_LABEL):
        return override

    table = table_wrap.find('.//table')
    if table is not None:
        # Check both thead and tbody for maximum columns
        max_columns = 0

        thead = table.find('.//thead')
        if thead is not None:
            max_columns = max(max_columns, _calculate_max_columns(thead, 'th'))

        tbody = table.find('.//tbody')
        if tbody is not None:
            max_columns = max(max_columns, _calculate_max_columns(tbody, 'td'))

        if max_columns > 4:
            return pdf_enum.SINGLE_COLUMN_PAGE_LABEL

        if _max_cell_text_length(table) > _PATHOLOGICAL_CELL_LENGTH:
            return pdf_enum.SINGLE_COLUMN_PAGE_LABEL

    return pdf_enum.DOUBLE_COLUMN_PAGE_LABEL

def get_table_column_info(headers, rows):
    """
    Provides detailed information about table columns including content analysis.
    
    Args:
        headers (list): List of header rows.
        rows (list): List of data rows.
    
    Returns:
        list: A list of dictionaries with column information including:
            - 'index': Column index
            - 'max_length': Maximum character length in the column
            - 'avg_length': Average character length in the column
            - 'content_type': Estimated content type ('numeric', 'text', 'mixed')
            - 'suggested_width': Suggested width in points
    """
    if not headers and not rows:
        return []
    
    # Determine number of columns
    num_cols = 0
    if headers:
        num_cols = max(num_cols, max(len(row) for row in headers) if headers else 0)
    if rows:
        num_cols = max(num_cols, max(len(row) for row in rows) if rows else 0)
    
    column_info = []
    
    for col_idx in range(num_cols):
        col_data = {
            'index': col_idx,
            'max_length': 0,
            'total_length': 0,
            'cell_count': 0,
            'numeric_count': 0,
            'text_count': 0
        }
        
        # Analyze headers
        for header_row in headers:
            if col_idx < len(header_row) and header_row[col_idx]:
                content = header_row[col_idx].strip()
                if content:
                    length = len(content)
                    col_data['max_length'] = max(col_data['max_length'], length)
                    col_data['total_length'] += length
                    col_data['cell_count'] += 1
                    col_data['text_count'] += 1
        
        # Analyze data rows
        for data_row in rows:
            if col_idx < len(data_row) and data_row[col_idx]:
                content = data_row[col_idx].strip()
                if content:
                    length = len(content)
                    col_data['max_length'] = max(col_data['max_length'], length)
                    col_data['total_length'] += length
                    col_data['cell_count'] += 1
                    
                    # Check if content is numeric
                    try:
                        float(content.replace(',', '.').replace('%', '').replace('$', '').strip())
                        col_data['numeric_count'] += 1
                    except ValueError:
                        col_data['text_count'] += 1
        
        # Calculate averages and content type
        avg_length = col_data['total_length'] / col_data['cell_count'] if col_data['cell_count'] > 0 else 0
        
        if col_data['numeric_count'] > col_data['text_count']:
            content_type = 'numeric'
        elif col_data['text_count'] > col_data['numeric_count']:
            content_type = 'text'
        else:
            content_type = 'mixed'
        
        # Calculate suggested width
        base_width = col_data['max_length'] * 6  # 6 points per character
        if content_type == 'numeric':
            suggested_width = max(50, min(base_width, 120))  # Narrower for numbers
        else:
            suggested_width = max(80, min(base_width, 200))  # Wider for text
        
        column_info.append({
            'index': col_idx,
            'max_length': col_data['max_length'],
            'avg_length': round(avg_length, 1),
            'content_type': content_type,
            'suggested_width': suggested_width
        })
    
    return column_info


# -----------------
# Private helpers
# -----------------

def _extract_table_rows_with_merged_cells(table_section, cell_tag):
    """
    Extracts table rows handling merged cells (colspan/rowspan).
    
    Args:
        table_section (ElementTree): The thead or tbody element.
        cell_tag (str): The cell tag to look for ('td' or 'th').
    
    Returns:
        list: A list of lists representing the table rows with merged cells properly handled.
    """
    rows = []
    row_elements = table_section.findall('.//tr')
    
    if not row_elements:
        return rows
    
    # Create a matrix to track occupied positions
    max_cols = _calculate_max_columns(table_section, cell_tag)
    occupied = [[False] * max_cols for _ in range(len(row_elements))]
    
    for row_idx, tr in enumerate(row_elements):
        row_data = [''] * max_cols
        col_idx = 0
        
        for cell in tr.findall(f'.//{cell_tag}'):
            # Find next available column
            while col_idx < max_cols and occupied[row_idx][col_idx]:
                col_idx += 1
            
            if col_idx >= max_cols:
                break
                
            # Get cell content
            cell_text = ''.join(cell.itertext()).strip() if cell.text or len(list(cell)) > 0 else ''
            
            # Get colspan and rowspan
            colspan = int(cell.get('colspan', 1))
            rowspan = int(cell.get('rowspan', 1))
            
            # Fill the cell and mark occupied positions
            row_data[col_idx] = cell_text
            for r in range(row_idx, min(row_idx + rowspan, len(row_elements))):
                for c in range(col_idx, min(col_idx + colspan, max_cols)):
                    occupied[r][c] = True
            
            col_idx += colspan
        
        rows.append(row_data)
    
    return rows

def _extract_table_spans(table_section, cell_tag):
    """
    Builds a grid describing cell spans (colspan/rowspan) for a table section.

    Each entry is either None (no cell starts here) or a dict with keys:
      - 'colspan': int
      - 'rowspan': int
      - 'text': str (cell text)

    The grid has dimensions [number_of_rows][max_columns] where max_columns
    takes into account merged cells.
    """
    spans = []
    row_elements = table_section.findall('.//tr')
    if not row_elements:
        return spans

    max_cols = _calculate_max_columns(table_section, cell_tag)
    # Track occupied positions due to spans
    occupied = [[False] * max_cols for _ in range(len(row_elements))]

    for row_idx, tr in enumerate(row_elements):
        row_spans = [None] * max_cols
        col_idx = 0

        for cell in tr.findall(f'.//{cell_tag}'):
            # Advance to next free column
            while col_idx < max_cols and occupied[row_idx][col_idx]:
                col_idx += 1
            if col_idx >= max_cols:
                break

            cell_text = ''.join(cell.itertext()).strip() if cell.text or len(list(cell)) > 0 else ''
            colspan = int(cell.get('colspan', 1))
            rowspan = int(cell.get('rowspan', 1))

            row_spans[col_idx] = {
                'colspan': colspan,
                'rowspan': rowspan,
                'text': cell_text,
            }

            for r in range(row_idx, min(row_idx + rowspan, len(row_elements))):
                for c in range(col_idx, min(col_idx + colspan, max_cols)):
                    occupied[r][c] = True

            col_idx += colspan

        spans.append(row_spans)

    return spans

def _calculate_max_columns(table_section, cell_tag):
    """
    Calculates the maximum number of columns in a table section, considering merged cells.
    
    Args:
        table_section (ElementTree): The thead or tbody element.
        cell_tag (str): The cell tag to look for ('td' or 'th').
    
    Returns:
        int: The maximum number of columns.
    """
    max_cols = 0
    
    for tr in table_section.findall('.//tr'):
        current_cols = 0
        for cell in tr.findall(f'.//{cell_tag}'):
            colspan = int(cell.get('colspan', 1))
            current_cols += colspan
        max_cols = max(max_cols, current_cols)
    
    return max_cols

def _max_cell_text_length(table):
    """Returns the character length of the longest single cell's text in the table."""
    max_len = 0
    for cell in table.xpath('.//td | .//th'):
        cell_len = len(''.join(cell.itertext()).strip())
        max_len = max(max_len, cell_len)
    return max_len

def _extract_table_foot(table_wrap):
    """
    Extracts footnote/attribution text from a table's <table-wrap-foot>, if present.

    Args:
        table_wrap (ElementTree): The XML table-wrap element to extract from.

    Returns:
        list: One string per <p>, <fn> or <attrib> child found, in document order.
    """
    notes = []
    foot = table_wrap.find('.//table-wrap-foot')
    if foot is None:
        return notes

    for node in foot.xpath('./p | ./fn | ./attrib | ./fn-group/fn'):
        text = ' '.join(' '.join(node.itertext()).split()).strip()
        if text:
            notes.append(text)

    return notes

def _calculate_column_widths(headers, rows, min_width=50, max_width=200):
    """
    Calculates optimal column widths based on content length.
    
    Args:
        headers (list): List of header rows.
        rows (list): List of data rows.
        min_width (int): Minimum column width in points. Defaults to 50.
        max_width (int): Maximum column width in points. Defaults to 200.
    
    Returns:
        list: A list of calculated column widths.
    """
    if not headers and not rows:
        return []
    
    # Determine number of columns
    num_cols = 0
    if headers:
        num_cols = max(num_cols, max(len(row) for row in headers) if headers else 0)
    if rows:
        num_cols = max(num_cols, max(len(row) for row in rows) if rows else 0)
    
    if num_cols == 0:
        return []
    
    # Calculate max content length for each column
    column_max_lengths = [0] * num_cols
    
    # Check headers
    for header_row in headers:
        for col_idx, cell_content in enumerate(header_row):
            if col_idx < num_cols and cell_content:
                column_max_lengths[col_idx] = max(
                    column_max_lengths[col_idx], 
                    _estimate_text_width(cell_content)
                )
    
    # Check data rows
    for data_row in rows:
        for col_idx, cell_content in enumerate(data_row):
            if col_idx < num_cols and cell_content:
                column_max_lengths[col_idx] = max(
                    column_max_lengths[col_idx], 
                    _estimate_text_width(cell_content)
                )
    
    # Apply min/max constraints and convert to points
    column_widths = []
    for max_length in column_max_lengths:
        # Base calculation: approximately 6 points per character
        base_width = max_length * 6
        
        # Apply constraints
        width = max(min_width, min(base_width, max_width))
        column_widths.append(width)
    
    # Normalize to ensure reasonable distribution
    total_width = sum(column_widths)
    if total_width > 500:  # If total is too wide, proportionally reduce
        scaling_factor = 500 / total_width
        column_widths = [int(width * scaling_factor) for width in column_widths]
    
    return column_widths

def _estimate_text_width(text):
    """
    Estimates the display width of text content.
    
    Args:
        text (str): The text to measure.
    
    Returns:
        int: Estimated width in characters.
    """
    if not text:
        return 0
    
    # Remove extra whitespace and count actual display characters
    clean_text = ' '.join(text.split())
    
    # Account for different character widths (rough approximation)
    width = 0
    for char in clean_text:
        if char.isupper():
            width += 1.2  # Uppercase letters are typically wider
        elif char.isdigit():
            width += 1.0  # Numbers are consistent width
        elif char in 'ijl':
            width += 0.5  # These letters are narrower
        elif char in 'mwMW':
            width += 1.5  # These letters are wider
        else:
            width += 1.0  # Standard character width
    
    return int(width)
