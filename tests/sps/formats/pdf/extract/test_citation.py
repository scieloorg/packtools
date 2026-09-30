import unittest

from lxml import etree

from packtools.sps.formats.pdf.extract import citation


class TestExtractCiteAsPartOne(unittest.TestCase):

    def test_extract_cite_as_part_one_text(self):
        # No separate <label>, so the "Cite as:" phrase lives inline at the
        # start of <p> - stripped here since the caller already prints its
        # own "CITE AS: " prefix and would otherwise duplicate it.
        xml = etree.fromstring(
            '<article>'
            '<fn-group>'
            '<fn fn-type="other">'
            '<p>Cite as: Example Citation</p>'
            '</fn>'
            '</fn-group>'
            '</article>'
        )
        expected = 'Example Citation'
        result = citation.extract_cite_as_part_one(xml)
        self.assertEqual(result, expected)

    def test_extract_cite_as_part_one_strips_inline_phrase_only_without_label(self):
        # Regression for #1349's review round 2 (a3-shaped case): when
        # there's no <label>, "Como citar:" is embedded in <p> itself and
        # must be stripped - but when a <label> does provide the signal
        # (e.g. "CITE AS:"), <p> never had the phrase to begin with, so
        # there's nothing to strip (see the nested-markup test below).
        xml = etree.fromstring(
            '<article>'
            '<fn-group>'
            '<fn fn-type="other">'
            '<p>Como citar: Souza CM, Iser BM, Malta DC. Example title. '
            'Journal 31(3):e31030043.</p>'
            '</fn>'
            '</fn-group>'
            '</article>'
        )
        expected = 'Souza CM, Iser BM, Malta DC. Example title. Journal 31(3):e31030043.'
        result = citation.extract_cite_as_part_one(xml)
        self.assertEqual(result, expected)

    def test_extract_cite_as_part_one_node(self):
        xml = etree.fromstring(
            '<article>'
            '<fn-group>'
            '<fn fn-type="other">'
            '<p>Cite as: Example Citation</p>'
            '</fn>'
            '</fn-group>'
            '</article>'
        )
        result = citation.extract_cite_as_part_one(xml, return_node=True)
        self.assertIsInstance(result, etree._Element)
        self.assertEqual(result.tag, 'p')
        self.assertEqual(result.text, 'Cite as: Example Citation')

    def test_extract_cite_as_part_one_no_fn_group(self):
        xml = etree.fromstring('<article></article>')
        result = citation.extract_cite_as_part_one(xml)
        self.assertIsNone(result)

    def test_extract_cite_as_part_one_no_fn_type_other(self):
        xml = etree.fromstring(
            '<article>'
            '<fn-group>'
            '<fn fn-type="conflict">'
            '<p>Not a citation</p>'
            '</fn>'
            '</fn-group>'
            '</article>'
        )
        result = citation.extract_cite_as_part_one(xml)
        self.assertIsNone(result)

    def test_extract_cite_as_part_one_skips_unrelated_fn_type_other(self):
        # Regression for issue #1349: fn-type="other" is a generic bucket
        # publishers use for all sorts of unrelated notes (institutional
        # acknowledgment, AI-use declaration, JEL codes...), so the first
        # one in the document isn't necessarily the citation note. Only a
        # <fn> whose <label> actually names it as one should be picked,
        # even when it isn't the first fn-type="other" in the fn-group.
        xml = etree.fromstring(
            '<article>'
            '<fn-group>'
            '<fn fn-type="other"><label>ZooBank register</label>'
            '<p>https://zoobank.org/some-id</p></fn>'
            '<fn fn-type="other"><label>How to cite this article</label>'
            '<p>Author AB (2024) Example citation.</p></fn>'
            '</fn-group>'
            '</article>'
        )
        expected = 'Author AB (2024) Example citation.'
        result = citation.extract_cite_as_part_one(xml)
        self.assertEqual(result, expected)

    def test_extract_cite_as_part_one_none_when_no_note_is_a_citation(self):
        # a11.xml-shaped case: the only fn-type="other" notes are
        # institutional acknowledgments, with no <label> and no "cite"/
        # "citar" wording - none of them should be mistaken for the
        # citation note.
        xml = etree.fromstring(
            '<article>'
            '<fn-group>'
            '<fn fn-type="other"><p>Study carried out at University X.</p></fn>'
            '</fn-group>'
            '</article>'
        )
        result = citation.extract_cite_as_part_one(xml)
        self.assertIsNone(result)

    def test_extract_cite_as_part_one_full_text_with_nested_markup(self):
        # Regression for issue #1349: using node.text alone (instead of
        # full itertext) cut the citation off at the first child element,
        # e.g. a DOI wrapped in <ext-link> right after the reference text.
        xml = etree.fromstring(
            '<article>'
            '<fn-group>'
            '<fn fn-type="other"><label>CITE AS:</label>'
            '<p>Author AB. Example title. Journal 1: 2. '
            '<ext-link>https://doi.org/10.1590/example</ext-link>'
            '</p></fn>'
            '</fn-group>'
            '</article>'
        )
        expected = 'Author AB. Example title. Journal 1: 2. https://doi.org/10.1590/example'
        result = citation.extract_cite_as_part_one(xml)
        self.assertEqual(result, expected)


class TestBuildFullCitation(unittest.TestCase):
    """
    Regression for #1349's review round 2: many articles carry no explicit
    "how to cite this article" note at all (see
    test_extract_cite_as_part_one_none_when_no_note_is_a_citation) - this
    builds a complete citation from the article's own metadata for that
    fallback case, instead of the caller falling back to a bare
    "journal volume: location" with no authors/title/DOI.
    """

    def _article(self, given_names=('Bárbara Passos da Silva', 'Kelly Regina Batista')):
        contribs = ''.join(
            f'<contrib contrib-type="author"><name>'
            f'<surname>Surname{i}</surname><given-names>{gn}</given-names>'
            f'</name></contrib>'
            for i, gn in enumerate(given_names)
        )
        return etree.fromstring(
            '<article>'
            '<front><article-meta>'
            f'<contrib-group>{contribs}</contrib-group>'
            '<article-title>Example Article Title</article-title>'
            '<article-id pub-id-type="doi">10.1590/example</article-id>'
            '</article-meta></front>'
            '<journal-meta><abbrev-journal-title>Ex. J.</abbrev-journal-title></journal-meta>'
            '</article>'
        )

    def test_builds_complete_citation_with_volume_issue_and_doi(self):
        xml = self._article()
        footer_data = {'year': '2024', 'volume': '10', 'issue': '2',
                        'location_label': 'e12345'}
        expected = (
            'Surname0 BPS, Surname1 KRB. Example Article Title. Ex. J. '
            '2024;10(2):e12345. https://doi.org/10.1590/example'
        )
        self.assertEqual(citation.build_full_citation(xml, footer_data), expected)

    def test_omits_issue_parens_when_issue_is_absent(self):
        xml = self._article(given_names=('Bárbara Passos da Silva',))
        footer_data = {'year': '2024', 'volume': '10', 'issue': '',
                        'location_label': 'e12345'}
        result = citation.build_full_citation(xml, footer_data)
        self.assertIn('2024;10:e12345.', result)
        self.assertNotIn('()', result)

    def test_omits_volume_when_absent(self):
        # Continuous-publication articles carry no <volume>. citeproc-py's
        # own CSL rules join year and location with ";" rather than ":"
        # once there's no volume/issue to put a colon after - a style-engine
        # decision now, not a hand-picked separator.
        xml = self._article(given_names=('Bárbara Passos da Silva',))
        footer_data = {'year': '2023', 'volume': '', 'issue': '',
                        'location_label': 'e236720'}
        result = citation.build_full_citation(xml, footer_data)
        self.assertIn('2023;e236720.', result)

    def test_initials_exclude_lowercase_particles(self):
        xml = self._article(given_names=('Bárbara Passos da Silva',))
        footer_data = {'year': '2024', 'volume': '', 'issue': '', 'location_label': ''}
        result = citation.build_full_citation(xml, footer_data)
        self.assertTrue(result.startswith('Surname0 BPS.'))

    def test_truncates_to_et_al_beyond_six_authors(self):
        xml = self._article(given_names=[f'Author{i}' for i in range(8)])
        footer_data = {'year': '2024', 'volume': '', 'issue': '', 'location_label': ''}
        result = citation.build_full_citation(xml, footer_data)
        self.assertTrue(result.startswith(
            'Surname0 A, Surname1 A, Surname2 A, Surname3 A, Surname4 A, Surname5 A, et al.'
        ))

    def test_returns_empty_string_when_there_are_no_authors(self):
        xml = etree.fromstring(
            '<article><front><article-meta>'
            '<article-title>Example Article Title</article-title>'
            '</article-meta></front></article>'
        )
        footer_data = {'year': '2024', 'volume': '', 'issue': '', 'location_label': ''}
        self.assertEqual(citation.build_full_citation(xml, footer_data), '')

    def test_falls_back_to_full_journal_title_when_no_abbrev(self):
        xml = etree.fromstring(
            '<article><front><article-meta>'
            '<contrib-group><contrib contrib-type="author"><name>'
            '<surname>Surname</surname><given-names>Ana Maria</given-names>'
            '</name></contrib></contrib-group>'
            '<article-title>Example Article Title</article-title>'
            '</article-meta></front>'
            '<journal-meta><journal-title-group><journal-title>Full Journal Name</journal-title>'
            '</journal-title-group></journal-meta>'
            '</article>'
        )
        footer_data = {'year': '2024', 'volume': '', 'issue': '', 'location_label': ''}
        result = citation.build_full_citation(xml, footer_data)
        self.assertIn('Full Journal Name.', result)

    def test_unknown_style_returns_empty_string(self):
        xml = self._article(given_names=('Bárbara Passos da Silva',))
        footer_data = {'year': '2024', 'volume': '', 'issue': '', 'location_label': ''}
        result = citation.build_full_citation(xml, footer_data, style='abnt')
        self.assertEqual(result, '')

    def test_excludes_non_author_contrib_from_citation(self):
        # Regression for #1350 review: a translator (or other non-author
        # contrib-type) in the same <contrib-group> as the authors must not
        # be treated as an author in the built citation.
        xml = etree.fromstring(
            '<article><front><article-meta>'
            '<contrib-group>'
            '<contrib contrib-type="author"><name>'
            '<surname>Cholodenko</surname><given-names>Alan</given-names>'
            '</name></contrib>'
            '<contrib contrib-type="translator"><name>'
            '<surname>Sousa</surname><given-names>Adriano</given-names>'
            '</name></contrib>'
            '</contrib-group>'
            '<article-title>Example Article Title</article-title>'
            '</article-meta></front>'
            '<journal-meta><abbrev-journal-title>Ex. J.</abbrev-journal-title></journal-meta>'
            '</article>'
        )
        footer_data = {'year': '2024', 'volume': '', 'issue': '', 'location_label': ''}
        result = citation.build_full_citation(xml, footer_data)
        self.assertTrue(result.startswith('Cholodenko A.'))
        self.assertNotIn('Sousa', result)

    def test_includes_contrib_with_no_contrib_type_attribute(self):
        # Backward compatibility: a <contrib> with no contrib-type at all
        # (JATS allows omitting it) is still treated as an author.
        xml = etree.fromstring(
            '<article><front><article-meta>'
            '<contrib-group><contrib><name>'
            '<surname>Surname</surname><given-names>Ana</given-names>'
            '</name></contrib></contrib-group>'
            '<article-title>Example Article Title</article-title>'
            '</article-meta></front>'
            '<journal-meta><abbrev-journal-title>Ex. J.</abbrev-journal-title></journal-meta>'
            '</article>'
        )
        footer_data = {'year': '2024', 'volume': '', 'issue': '', 'location_label': ''}
        result = citation.build_full_citation(xml, footer_data)
        self.assertTrue(result.startswith('Surname A.'))


class TestBuildCslReferenceType(unittest.TestCase):
    """
    Regression for #1350 review: the CSL item type was hardcoded as
    'article-journal' inside _build_csl_reference - csl_type is now a
    parameter (default unchanged) so a future caller can build a citation
    for a non-research-article type.
    """

    def _article(self):
        return etree.fromstring(
            '<article><front><article-meta>'
            '<contrib-group><contrib contrib-type="author"><name>'
            '<surname>Surname</surname><given-names>Ana</given-names>'
            '</name></contrib></contrib-group>'
            '<article-title>Example Article Title</article-title>'
            '</article-meta></front>'
            '<journal-meta><abbrev-journal-title>Ex. J.</abbrev-journal-title></journal-meta>'
            '</article>'
        )

    def test_defaults_to_article_journal(self):
        reference = citation._build_csl_reference(self._article(), {})
        self.assertEqual(reference['type'], 'article-journal')

    def test_accepts_custom_csl_type(self):
        reference = citation._build_csl_reference(self._article(), {}, csl_type='editorial')
        self.assertEqual(reference['type'], 'editorial')


class TestExtractCiteAs(unittest.TestCase):

    _FOOTER = {'year': '2024', 'volume': '10', 'issue': '2', 'location_label': 'e123'}

    def _article(self, notes=''):
        return etree.fromstring(
            '<article>'
            '<front><article-meta>'
            '<contrib-group><contrib contrib-type="author"><name>'
            '<surname>Silva</surname><given-names>Ana</given-names>'
            '</name></contrib></contrib-group>'
            '<article-title>Title</article-title>'
            '</article-meta>'
            '<journal-meta><abbrev-journal-title>Ex. J.</abbrev-journal-title></journal-meta>'
            '</front>'
            f'<back><fn-group>{notes}</fn-group></back>'
            '</article>'
        )

    def test_prefers_editorial_note(self):
        xml = self._article(
            '<fn fn-type="other"><label>Como citar:</label><p>Nota editorial.</p></fn>'
        )
        self.assertEqual(citation.extract_cite_as(xml, self._FOOTER), 'Nota editorial.')

    def test_falls_back_to_generated_citation(self):
        xml = self._article()
        self.assertEqual(
            citation.extract_cite_as(xml, self._FOOTER),
            citation.build_full_citation(xml, self._FOOTER),
        )
        self.assertIn('Silva A', citation.extract_cite_as(xml, self._FOOTER))

    def test_empty_without_note_and_authors(self):
        xml = etree.fromstring('<article><front><article-meta/></front></article>')
        self.assertEqual(citation.extract_cite_as(xml, self._FOOTER), '')


class TestExtractCiteAsPartOneSkips(unittest.TestCase):

    def test_fn_without_p_is_skipped(self):
        xml = etree.fromstring(
            '<article><fn-group>'
            '<fn fn-type="other"><label>Como citar</label></fn>'
            '<fn fn-type="other"><label>Como citar</label><p>Autor A. Título.</p></fn>'
            '</fn-group></article>'
        )
        self.assertEqual(citation.extract_cite_as_part_one(xml), 'Autor A. Título.')


class TestExtractCitationAuthors(unittest.TestCase):

    def _authors(self, contribs):
        xml = etree.fromstring(
            f'<article><front><article-meta><contrib-group>{contribs}</contrib-group></article-meta></front></article>'
        )
        return citation._extract_citation_authors(xml)

    def test_no_contrib_group(self):
        self.assertEqual(citation._extract_citation_authors(etree.fromstring('<article/>')), [])

    def test_contrib_without_name_is_skipped(self):
        contribs = (
            '<contrib contrib-type="author"><collab>Grupo</collab></contrib>'
            '<contrib contrib-type="author"><name><surname>Silva</surname><given-names>Ana</given-names></name></contrib>'
        )
        self.assertEqual(self._authors(contribs), ['Silva A'])

    def test_contrib_with_missing_or_empty_surname_is_skipped(self):
        contribs = (
            '<contrib><name><given-names>Ana</given-names></name></contrib>'
            '<contrib><name><surname> </surname><given-names>Ana</given-names></name></contrib>'
        )
        self.assertEqual(self._authors(contribs), [])

    def test_surname_only(self):
        self.assertEqual(self._authors('<contrib><name><surname>Silva</surname></name></contrib>'), ['Silva'])
