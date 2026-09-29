"""Campo "como citar" do rodapé da primeira página: nota editorial do artigo ou citação gerada via CSL."""

import re
from pathlib import Path

from citeproc import Citation, CitationItem, CitationStylesBibliography, CitationStylesStyle, formatter
from citeproc.source.json import CiteProcJSON

from packtools.sps.formats.pdf.extract import metadata
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

    title = metadata.extract_article_title(xml_tree)
    if title:
        reference['title'] = title

    abbrev_journal = xml_tree.find('.//abbrev-journal-title')
    journal = (
        ''.join(abbrev_journal.itertext()).strip()
        if abbrev_journal is not None
        else metadata.extract_journal_title(xml_tree)
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


def extract_cite_as(xml_tree, footer_data):
    """
    Returns the text for the first page's "CITE AS" field.

    Prefers the article's own editorial "how to cite" note; when it has
    none, builds a complete citation from metadata instead of leaving the
    field partial (journal/volume/location only - see issue #1349).

    Args:
        xml_tree (ElementTree): The XML tree to extract the citation from.
        footer_data (dict): Output of `metadata.extract_footer_data`.

    Returns:
        str: The editorial note text, the generated citation, or '' when
        neither is available.
    """
    return extract_cite_as_part_one(xml_tree) or build_full_citation(xml_tree, footer_data)
