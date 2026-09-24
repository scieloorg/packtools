import re
import string
from pathlib import Path

from citeproc import Citation, CitationItem, CitationStylesBibliography, CitationStylesStyle, formatter
from citeproc.source.json import CiteProcJSON

from packtools.sps.formats.pdf import enum as pdf_enum
from packtools.sps.formats.pdf.pipeline import formula
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

    Only `<contrib>` elements with `@contrib-type="author"` (or no
    `contrib-type` attribute at all, treated as author for backward
    compatibility) are included - a translator, editor, or other non-author
    contributor in the same `<contrib-group>` must not end up in the
    citation's author list (#1350 review: reproduced with
    tests/fixtures/htmlgenerator/translator/dqR6y8bPFVVQnxnFHY66ZZK.xml).

    Returns:
        list: Author strings in document order; empty if there's no
        <contrib-group> or no author <contrib> has both <surname> and text.
    """
    article_meta = xml_tree.find('./front/article-meta')
    metadata_scope = article_meta if article_meta is not None else xml_tree
    contrib_group = metadata_scope.find('.//contrib-group')
    if contrib_group is None:
        return []

    authors = []
    for contrib in contrib_group.findall('.//contrib'):
        if contrib.get('contrib-type', 'author') != 'author':
            continue
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


def _build_csl_reference(xml_tree, footer_data, csl_type='article-journal'):
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

    `csl_type` (#1350 review: non-blocking, flagged for future
    parametrization) is the CSL item type - 'article-journal' covers a
    regular research article; a caller can pass e.g. 'editorial' or
    'personal_communication' for other article types once packtools
    distinguishes them, without changing this function's other behavior.

    Returns:
        dict, or None when there are no authors to build a reference from.
    """
    authors = _extract_citation_authors(xml_tree)
    if not authors:
        return None

    reference = {
        'id': 'cite-as',
        'type': csl_type,
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


def _format_via_citeproc(xml_tree, footer_data, csl_filename, csl_type='article-journal'):
    """
    Renders a full citation for `xml_tree`/`footer_data` through citeproc-py
    using the named CSL style file (packaged under
    packtools/sps/formats/pdf/citation_styles/). Returns '' when there are
    no authors to build a reference from.
    """
    reference = _build_csl_reference(xml_tree, footer_data, csl_type)
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


def build_full_citation(xml_tree, footer_data, style=CITATION_STYLE_VANCOUVER, csl_type='article-journal'):
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

    `csl_type` selects the CSL item type (#1350 review: non-blocking).
    Defaults to 'article-journal'; a caller can pass a different CSL type
    for editorial/communication/letter articles once packtools
    distinguishes them from regular research articles.

    Args:
        xml_tree (ElementTree): The XML tree to build the citation from.
        footer_data (dict): Output of `extract_footer_data` (year/volume/issue/location_label).
        style (str, optional): Citation format identifier. Defaults to CITATION_STYLE_VANCOUVER.
        csl_type (str, optional): CSL item type. Defaults to 'article-journal'.

    Returns:
        str: The complete citation, or '' when the style is unknown or the
        article has no authors to build one from.
    """
    csl_filename = _CITATION_STYLE_CSL_FILES.get(style)
    if csl_filename is None:
        return ''
    return _format_via_citeproc(xml_tree, footer_data, csl_filename, csl_type)


def _int_to_roman(number):
    """Converts a positive int to a lowercase roman numeral string."""
    values = (1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1)
    symbols = ('m', 'cm', 'd', 'cd', 'c', 'xc', 'l', 'xl', 'x', 'ix', 'v', 'iv', 'i')
    result = []
    for value, symbol in zip(values, symbols):
        count, number = divmod(number, value)
        result.append(symbol * count)
    return ''.join(result)


def _list_item_marker(list_type, index):
    """
    Returns the text marker (e.g. "1. ", "a. ") for a <list-item> at
    position `index` (1-based) of a <list list-type="...">, or '' for a
    list-type with no visual marker ("simple", the type used when a list's
    own items already carry their numbering some other way, e.g. a
    <disp-formula>'s own <label> - see issue #1365/a5.xml) or an
    unrecognized/absent list-type.
    """
    if list_type == 'bullet':
        return '• '
    if list_type in ('order', 'arabic'):
        return f'{index}. '
    if list_type == 'roman-lower':
        return f'{_int_to_roman(index)}. '
    if list_type == 'roman-upper':
        return f'{_int_to_roman(index).upper()}. '
    if list_type == 'alpha-lower':
        return f'{string.ascii_lowercase[(index - 1) % 26]}. '
    if list_type == 'alpha-upper':
        return f'{string.ascii_uppercase[(index - 1) % 26]}. '
    return ''


def _plain_text_segment(text):
    """An unstyled text segment, in the shape get_segments_from_node returns."""
    return {'type': 'text', 'text': text, 'italic': False, 'bold': False, 'superscript': False, 'subscript': False}


_INLINE_FORMULA_TAGS = {'inline-formula'}


def _inline_formula_segment(inline_formula):
    """Converte o MathML de um <inline-formula> (fórmula no meio de texto corrido) em um segmento 'formula'.

    Ao contrário de <disp-formula>, não carrega <label> próprio (fase 2 de
    #1347, issue #1353).

    Args:
        inline_formula (ElementTree): The <inline-formula> element.

    Returns:
        dict, or None when there's no MathML descendant or
        formula.mathml_to_omml couldn't convert it (unsupported construct) -
        the caller (xml_utils.get_segments_from_node) falls back to
        flattening it as plain text, same as any unrecognized tag.
    """
    math_node = inline_formula.find('.//{http://www.w3.org/1998/Math/MathML}math')
    if math_node is None:
        return None
    omml_element = formula.mathml_to_omml(math_node)
    if omml_element is None:
        return None
    return {'type': 'formula', 'omml': omml_element}


def _disp_formula_segments(disp_formula):
    """Converte o MathML de um <disp-formula> em um segmento 'formula', mais um segmento de texto para o <label>, se houver.

    O segmento de fórmula leva 'display': True (fórmula em bloco); o renderer
    usa essa marca para separá-la do texto e distingui-la de fórmula inline.

    Args:
        disp_formula (ElementTree): The <disp-formula> element.

    Returns:
        list[dict], or None when there's no MathML descendant or
        formula.mathml_to_omml couldn't convert it (unsupported construct) -
        callers should fall back to the existing flattened-text paragraph
        in that case, never drop the formula silently.
    """
    math_node = disp_formula.find('.//{http://www.w3.org/1998/Math/MathML}math')
    if math_node is None:
        return None
    omml_element = formula.mathml_to_omml(math_node)
    if omml_element is None:
        return None

    segments = [{'type': 'formula', 'omml': omml_element, 'display': True}]
    label = disp_formula.find('label')
    if label is not None:
        label_text = ''.join(label.itertext()).strip()
        if label_text:
            segments.append(_plain_text_segment(f' {label_text}'))
    return segments


def _paragraph_with_trailing_formula(p_node):
    """Trata <p>texto:<disp-formula>...</disp-formula></p>: fórmula em bloco com texto simples antes, no mesmo parágrafo.

    Escopo restrito: um <p> com mais de um <disp-formula>, ou com
    conteúdo depois da fórmula, retorna None (o chamador cai no fallback).

    Args:
        p_node (ElementTree): The <p> element.

    Returns:
        list[dict], or None when `p_node` doesn't match this specific shape.
    """
    formulas = p_node.findall('disp-formula')
    if len(formulas) != 1:
        return None
    formula = formulas[0]
    siblings = list(p_node)
    if siblings[-1] is not formula:
        return None
    if (formula.tail or '').strip():
        return None

    formula_segments = _disp_formula_segments(formula)
    if formula_segments is None:
        return None

    leading_segments = xml_utils.get_segments_from_node(
        p_node, skip_tags={'disp-formula'},
        formula_tags=_INLINE_FORMULA_TAGS, formula_converter=_inline_formula_segment,
    )
    return leading_segments + formula_segments


def _extract_list_paragraphs(list_node):
    """
    Extracts a <list>'s <list-item>s as paragraph entries (issue #1365):
    one per item, each the same list-of-segments shape as any other
    paragraph, with a bullet/number/letter marker (see _list_item_marker)
    prepended as its own leading segment - or no marker for list-type
    "simple" (used when the items already carry their own numbering some
    other way, e.g. each <disp-formula>'s own <label>) or an unrecognized
    list-type.

    Um <disp-formula> ao final do <p> de um <list-item> recebe conversão
    OMML real via _paragraph_with_trailing_formula, em vez do texto
    achatado ambíguo que a recursão comum de get_segments_from_node
    produziria. Uma fórmula só-imagem (sem MathML) aninhada nesse nível
    ainda é descartada silenciosamente (não vista no corpus de testes).

    Args:
        list_node (ElementTree): The <list> element.

    Returns:
        list[list[dict]]: One entry per non-empty <list-item> paragraph.
    """
    list_type = list_node.get('list-type', '')
    paragraphs = []
    for index, item in enumerate(list_node.findall('list-item'), start=1):
        marker = _list_item_marker(list_type, index)
        for item_p in item.findall('p'):
            item_segments = _paragraph_with_trailing_formula(item_p)
            if item_segments is None:
                item_segments = xml_utils.get_segments_from_node(
                    item_p, skip_tags={'fig', 'table-wrap'},
                    formula_tags=_INLINE_FORMULA_TAGS, formula_converter=_inline_formula_segment,
                )
            if not item_segments:
                continue
            if marker:
                item_segments = [_plain_text_segment(marker)] + item_segments
                marker = ''
            paragraphs.append(item_segments)
    return paragraphs


def extract_body_data(xml_tree, table_layout_overrides=None):
    """
    Extracts the body data from an XML tree, including section titles, paragraphs, and tables.

    Excludes any <sec> nested inside <abstract> or <trans-abstract> - those
    are structured-abstract subsections handled by extract_abstract_data /
    extract_trans_abstract_data, and would otherwise be picked up twice by
    a plain './/sec' search.

    Also excludes a <sec> that IS the supplementary-material section -
    identified structurally as a <sec> with a <supplementary-material>
    descendant and no <sec> of its own (not by @sec-type, which varies
    across the corpus: "supplementary-material", "materials|supplementary-
    material", "supplementary" or absent entirely) - handled separately by
    supplementary_material.extract_data, which already renders it under its
    own heading; leaving it in here too would duplicate the content. The
    "no <sec> of its own" guard matters: a real body section (e.g.
    "Discussion") that merely references supplementary material somewhere
    inside one of its own subsections is not a supplementary-material
    section and must stay in the body (issue #1375 review).

    Falls back to treating <body> itself as an extra, untitled section when
    <body> has no <sec> of its own (valid JATS pattern for unsectioned
    short communications/brief reports) - otherwise its content would be
    silently dropped even though an unrelated <sec> elsewhere in the
    document (e.g. a data-availability statement under <back>) keeps the
    section search from returning empty.

    Args:
        xml_tree (ElementTree): The XML tree to extract the body data from.
        table_layout_overrides (dict, optional): Maps a table-wrap @id to a forced
            layout ('single-column-layout' or 'double-column-layout'), bypassing
            `determine_table_layout`'s heuristic for that specific table.

    Returns:
        list: A list of dictionaries, where each dictionary represents a section in the body of the document. Each dictionary has the following keys:
            - 'level': The nesting level of the section.
            - 'title': The title of the section, if present.
            - 'paragraphs': A list of paragraphs, each a list of style-tagged
              text segments (see xml_utils.get_segments_from_node) preserving
              inline <italic>/<bold>/<sup>/<sub> markup, and converting any
              <inline-formula> found in running text to a real OMML formula
              segment (issue #1353, fase 2 de #1347) instead of flattening
              its MathML to ambiguous text. Also includes any
              <disp-formula> found as a direct sibling of a <p>, since a
              structured formula isn't always wrapped in one - as a single
              plain-text segment (no MathML->OMML conversion yet, see issue
              #1347's phased plan). Also includes each <list-item> of a
              direct-child <list>, one per item, with a bullet/number/letter
              marker prepended as its own leading segment (see
              _list_item_marker; nothing prepended for list-type "simple" or
              unrecognized). Excludes paragraphs that contain table/figure
              references or wrappers.
            - 'tables': A list of dictionaries representing the tables in the section, as returned by the `extract_table_data` function.
            - 'figures': A list of dictionaries representing figures in the section, as returned by the `extract_figure_data` function
              (also includes any <disp-formula> that is a graphic rather than
              MathML/text - whether a direct sibling of a <p> or, since a
              <label> would otherwise make it look like flattenable text,
              carrying its own <label> - since there's nothing to flatten
              into a paragraph).
    """
    data = []
    seen_fig_keys = set()

    body_sections = xml_tree.xpath(
        './/sec[not(ancestor::abstract) and not(ancestor::trans-abstract)'
        ' and not(.//supplementary-material and not(sec))]'
    )
    body = xml_tree.find('.//body')
    if body is not None and body.find('.//sec') is None:
        body_sections = [body] + body_sections

    for document_section in body_sections:
        data.append(extract_section_data(document_section, xml_tree, seen_fig_keys, table_layout_overrides))

    return data


def extract_section_data(document_section, xml_tree, seen_fig_keys, table_layout_overrides=None, level=None):
    """
    Extrai título, parágrafos, tabelas e figuras de um único nó de seção
    (<sec>, <body> sem <sec> ou <app>), no formato descrito em
    extract_body_data. seen_fig_keys é compartilhado entre as seções de
    um mesmo bloco para não repetir figuras; level, quando informado,
    substitui a profundidade do nó na árvore.
    """
    sec = {'paragraphs': [], 'tables': [], 'figures': []}
    sec['level'] = level if level is not None else xml_utils.get_node_level(document_section, xml_tree)
    sec['title'] = document_section.find('title')

    if sec['title'] is not None:
        sec['title'] = ''.join(sec['title'].itertext()).strip()

    # Collect textual paragraphs but exclude figure/table elements. Uses
    # get_text_from_node (tail-preserving) rather than a bare
    # `.xpath('.//text()...')` + `' '.join(...)`, which inserted an
    # artificial space between every text-node fragment regardless of
    # whether the source had one there (e.g. "(<xref>...</xref>)" came
    # out as "( ... )", and "<xref/>; <xref/>" as "... ; ...").
    #
    # <disp-formula> isn't always nested inside a <p> - it's often a
    # direct sibling of one - so a plain `findall('p')` silently drops
    # it. Walking direct children instead of just `<p>` catches that
    # case too. This still only flattens the formula's text (no
    # MathML->OMML conversion yet, see issue #1347's phased plan), but
    # flattened-and-present beats silently missing.
    for child in document_section:
        if child.tag == 'p':
            # <p>texto:<disp-formula>...</disp-formula></p>: tratado antes do
            # achatamento genérico, para gerar um segmento OMML real
            formula_paragraph_segments = _paragraph_with_trailing_formula(child)
            if formula_paragraph_segments is not None:
                sec['paragraphs'].append(formula_paragraph_segments)
                continue
            # <list> can also occur as a child of <p> rather than as its
            # own sibling (issue #1365, seen in a28.xml: the JATS source
            # wraps a <list> of research propositions in a <p> with no
            # other content). skip_tags drops it from the flattened text
            # the same way it already does for <fig>/<table-wrap> -
            # get_segments_from_node has no special handling for <list>,
            # so leaving it in would silently flatten it to nothing -
            # and its items are extracted separately right after.
            nested_lists = child.findall('list')
            skip_tags = {'fig', 'table-wrap', 'list'} if nested_lists else {'fig', 'table-wrap'}
            para_segments = xml_utils.get_segments_from_node(
                child, skip_tags=skip_tags,
                formula_tags=_INLINE_FORMULA_TAGS, formula_converter=_inline_formula_segment,
            )
            if para_segments:
                sec['paragraphs'].append(para_segments)
            for nested_list in nested_lists:
                sec['paragraphs'].extend(_extract_list_paragraphs(nested_list))
            continue
        elif child.tag == 'disp-formula':
            # A formula rendered as an image (<graphic>, no MathML) has to
            # be identified by shape, not by "no flattenable text": a
            # <label> sibling of <graphic> (e.g. "(1)") makes
            # get_text_from_node return non-empty even though the
            # <graphic> itself has nothing to flatten, so checking
            # `not para_text` alone let a labeled graphic formula fall
            # through and drop its <graphic> as a bare label paragraph
            # (issue #1365).
            has_graphic = child.find('.//graphic') is not None
            has_math = bool(child.xpath('.//*[local-name()="math"]'))
            if has_graphic and not has_math:
                # extract_figure_data reads the same label/caption/graphic
                # shape <fig> has, so a <disp-formula> with a <graphic>
                # can reuse it as-is and render like any other figure
                # instead of vanishing.
                formula_fig = extract_figure_data(child)
                formula_key = child.get('id') or formula_fig.get('href') or ''
                if not formula_key or formula_key not in seen_fig_keys:
                    sec['figures'].append(formula_fig)
                    if formula_key:
                        seen_fig_keys.add(formula_key)
                continue
            if has_math:
                formula_segments = _disp_formula_segments(child)
                if formula_segments is not None:
                    sec['paragraphs'].append(formula_segments)
                    continue
            # fallback: sem MathML ou conversao falhou - texto achatado,
            # ambiguo mas presente e melhor que descartado silenciosamente
            para_text = xml_utils.get_text_from_node(child).strip()
            para_segments = xml_utils.get_segments_from_node(child) if para_text else []
        elif child.tag == 'list':
            # A <list> as a direct sibling of <p> - not visited at all
            # otherwise, falling to the `else: continue` below and
            # dropping the whole list (issue #1365; a5.xml loses both
            # its plain bullet lists and the Equations 3-10, which live
            # one level deeper inside <list-item><p><disp-formula>).
            sec['paragraphs'].extend(_extract_list_paragraphs(child))
            continue
        else:
            continue
        if para_segments:
            sec['paragraphs'].append(para_segments)

    for table_wrap in document_section.findall('.//table-wrap'):
        closest_sec = table_wrap.xpath('ancestor::sec[1]')
        if closest_sec and closest_sec[0] is not document_section:
            continue
        table_id = table_wrap.get('id') or table_wrap.get('xml:id')
        override_layout = (table_layout_overrides or {}).get(table_id)
        sec['tables'].extend(extract_table_data(table_wrap, override_layout=override_layout))

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

    return sec

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

def extract_table_data(table_wrap, override_layout=None):
    """
    Extracts table data from an XML table-wrap element, handling merged cells.

    A <table-wrap> can contain more than one <table> (e.g. side-by-side
    "Program A"/"Program B"/"Program C" panels sharing one caption - real
    corpus pattern, issue #1368). Only the first used to be read; now every
    <table> is extracted as its own dict, so callers get one renderable
    table per <table> element instead of silently losing every table past
    the first. The shared <label>/<title> caption is attached only to the
    first dict (repeating it before every panel would look wrong), and any
    <table-wrap-foot> notes only to the last (read as applying to the whole
    group, once, after the last panel) - the ones in between get empty
    label/title/foot.

    Args:
        table_wrap (ElementTree): The XML table-wrap element to extract data from.
        override_layout (str, optional): Forces 'layout' to this value instead of
            running `determine_table_layout`'s heuristic. Must be one of
            pdf_enum.SINGLE_COLUMN_PAGE_LABEL/DOUBLE_COLUMN_PAGE_LABEL, otherwise ignored.

    Returns:
        list[dict]: One dict per <table> in the table-wrap (or a single
        empty-shell dict if the table-wrap has no <table> at all), each
        with the following keys:
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
    layout = determine_table_layout(table_wrap, override=override_layout)

    tables = table_wrap.findall('.//table')
    if not tables:
        return [{
            'label': label_text,
            'title': title_text,
            'headers': [],
            'rows': [],
            'layout': layout,
            'column_widths': [],
            'header_spans': [],
            'row_spans': [],
            'foot': foot_notes,
        }]

    results = []
    for i, table in enumerate(tables):
        headers, header_spans, rows, row_spans = _extract_single_table_rows(table)
        column_widths = _calculate_column_widths(headers, rows)
        results.append({
            'label': label_text if i == 0 else '',
            'title': title_text if i == 0 else '',
            'headers': headers,
            'rows': rows,
            'layout': layout,
            'column_widths': column_widths,
            'header_spans': header_spans,
            'row_spans': row_spans,
            'foot': foot_notes if i == len(tables) - 1 else [],
        })
    return results

def _extract_single_table_rows(table):
    """Extracts headers/rows/spans for a single <table> element."""
    headers = []
    rows = []
    header_spans = []
    row_spans = []

    thead = table.find('.//thead')
    if thead is not None:
        header_rows = thead.findall('.//tr')
        headers = _extract_table_rows_with_merged_cells(header_rows, 'th')
        header_spans = _extract_table_spans(header_rows, 'th')

    tbody = table.find('.//tbody')
    if tbody is not None:
        body_rows = tbody.findall('.//tr')
        rows = _extract_table_rows_with_merged_cells(body_rows, 'td')
        row_spans = _extract_table_spans(body_rows, 'td')
    elif thead is None:
        # <tr> as direct children of <table>, no <thead>/<tbody> wrapper at
        # all - valid JATS/NLM table shape (issue #1368; real example: a
        # structured radiology-report-style table). Without this fallback
        # the whole table body was silently dropped. Accept both <td> and
        # <th> cells since a bare table sometimes still marks a cell with
        # <th> without a <thead> wrapper.
        body_rows = table.findall('.//tr')
        if body_rows:
            rows = _extract_table_rows_with_merged_cells(body_rows, ('td', 'th'))
            row_spans = _extract_table_spans(body_rows, ('td', 'th'))

    return headers, header_spans, rows, row_spans

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

    # A table-wrap can hold more than one <table> (issue #1368); the layout
    # decision is for the wrap as a whole, so it has to look at every
    # <table> in it, not just the first - otherwise a wrap whose first
    # panel happens to be narrow could still get double-column-layout even
    # though a later panel needs the full width.
    max_columns = 0
    max_cell_length = 0
    for table in table_wrap.findall('.//table'):
        thead = table.find('.//thead')
        if thead is not None:
            max_columns = max(max_columns, _calculate_max_columns(thead.findall('.//tr'), 'th'))

        tbody = table.find('.//tbody')
        if tbody is not None:
            max_columns = max(max_columns, _calculate_max_columns(tbody.findall('.//tr'), 'td'))
        elif thead is None:
            max_columns = max(max_columns, _calculate_max_columns(table.findall('.//tr'), ('td', 'th')))

        max_cell_length = max(max_cell_length, _max_cell_text_length(table))

    if max_columns > 4:
        return pdf_enum.SINGLE_COLUMN_PAGE_LABEL

    if max_cell_length > _PATHOLOGICAL_CELL_LENGTH:
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


def _find_cells(el, cell_tag):
    """Finds cell elements under el, in document order.

    cell_tag is normally a single tag ('td' or 'th'), preserving the exact
    prior behavior via findall(). It can also be a tuple of tags (used by
    the bare-<tr>-no-thead/tbody fallback, issue #1368, where a row's own
    cells might be marked <td> or <th> with no wrapper to tell them apart)
    - lxml's xpath union operator returns matches in document order, same
    guarantee findall gives for a single tag.
    """
    if isinstance(cell_tag, str):
        return el.findall(f'.//{cell_tag}')
    return el.xpath(' | '.join(f'.//{tag}' for tag in cell_tag))

def _extract_table_rows_with_merged_cells(row_elements, cell_tag):
    """
    Extracts table rows handling merged cells (colspan/rowspan).

    Args:
        row_elements (list): The <tr> elements to extract, in document order.
        cell_tag (str or tuple[str]): The cell tag(s) to look for ('td', 'th', or both).

    Returns:
        list: A list of lists representing the table rows with merged cells properly handled.
    """
    rows = []

    if not row_elements:
        return rows

    # Create a matrix to track occupied positions
    max_cols = _calculate_max_columns(row_elements, cell_tag)
    occupied = [[False] * max_cols for _ in range(len(row_elements))]

    for row_idx, tr in enumerate(row_elements):
        row_data = [''] * max_cols
        col_idx = 0

        for cell in _find_cells(tr, cell_tag):
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

def _extract_table_spans(row_elements, cell_tag):
    """
    Builds a grid describing cell spans (colspan/rowspan) for a set of rows.

    Each entry is either None (no cell starts here) or a dict with keys:
      - 'colspan': int
      - 'rowspan': int
      - 'text': str (cell text)

    The grid has dimensions [number_of_rows][max_columns] where max_columns
    takes into account merged cells.

    Args:
        row_elements (list): The <tr> elements to extract, in document order.
        cell_tag (str or tuple[str]): The cell tag(s) to look for ('td', 'th', or both).
    """
    spans = []
    if not row_elements:
        return spans

    max_cols = _calculate_max_columns(row_elements, cell_tag)
    # Track occupied positions due to spans
    occupied = [[False] * max_cols for _ in range(len(row_elements))]

    for row_idx, tr in enumerate(row_elements):
        row_spans = [None] * max_cols
        col_idx = 0

        for cell in _find_cells(tr, cell_tag):
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

def _calculate_max_columns(row_elements, cell_tag):
    """
    Calculates the maximum number of columns across a set of rows, considering merged cells.

    Args:
        row_elements (list): The <tr> elements to consider.
        cell_tag (str or tuple[str]): The cell tag(s) to look for ('td', 'th', or both).

    Returns:
        int: The maximum number of columns.
    """
    max_cols = 0

    for tr in row_elements:
        current_cols = 0
        for cell in _find_cells(tr, cell_tag):
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
