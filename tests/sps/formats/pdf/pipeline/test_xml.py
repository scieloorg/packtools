import unittest

from lxml import etree

from packtools.sps.formats.pdf.pipeline import xml as xml_pipe
from packtools.sps.formats.pdf import enum as pdf_enum


class TestExtractAbstractData(unittest.TestCase):

    def test_extract_abstract_data_with_title_and_content(self):
        xml = etree.fromstring(
            '<article><abstract>'
            '<title>Abstract Title</title>'
            '<p>First paragraph.</p>'
            '<p>Second paragraph.</p>'
            '</abstract></article>'
        )
        expected = {
            'title': 'Abstract Title',
            'content': 'First paragraph. Second paragraph.'
        }
        result = xml_pipe.extract_abstract_data(xml)
        self.assertEqual(result, expected)

    def test_extract_abstract_data_with_title_only(self):
        xml = etree.fromstring(
            '<article><abstract>'
            '<title>Abstract Title</title>'
            '</abstract></article>'
        )
        expected = {
            'title': 'Abstract Title',
            'content': ''
        }
        result = xml_pipe.extract_abstract_data(xml)
        self.assertEqual(result, expected)

    def test_extract_abstract_data_with_content_only(self):
        xml = etree.fromstring(
            '<article><abstract>'
            '<p>First paragraph.</p>'
            '<p>Second paragraph.</p>'
            '</abstract></article>'
        )
        expected = {
            'title': '',
            'content': 'First paragraph. Second paragraph.'
        }
        result = xml_pipe.extract_abstract_data(xml)
        self.assertEqual(result, expected)

    def test_extract_abstract_data_empty_abstract(self):
        xml = etree.fromstring('<article><abstract></abstract></article>')
        expected = {
            'title': '',
            'content': ''
        }
        result = xml_pipe.extract_abstract_data(xml)
        self.assertEqual(result, expected)

    def test_extract_abstract_data_no_abstract(self):
        xml = etree.fromstring('<article></article>')
        expected = {
            'title': '',
            'content': ''
        }
        result = xml_pipe.extract_abstract_data(xml)
        self.assertEqual(result, expected)

    def test_extract_abstract_data_with_nested_elements(self):
        xml = etree.fromstring(
            '<article><abstract>'
            '<title>Abstract <italic>Title</italic></title>'
            '<p>First <bold>paragraph</bold>.</p>'
            '<p>Second <italic>paragraph</italic>.</p>'
            '</abstract></article>'
        )
        expected = {
            'title': 'Abstract Title',
            'content': 'First paragraph. Second paragraph.'
        }
        result = xml_pipe.extract_abstract_data(xml)
        self.assertEqual(result, expected)

    def test_extract_abstract_data_structured_with_sections(self):
        # Regression for issue #1332: a structured abstract wraps
        # each subsection in its own <sec>, so a plain findall('p') (direct
        # children only) found nothing and returned an empty content.
        xml = etree.fromstring(
            '<article><abstract>'
            '<title>Abstract</title>'
            '<sec><title>Introduction:</title><p>Some introduction text.</p></sec>'
            '<sec><title>Methods:</title><p>Some methods text.</p></sec>'
            '</abstract></article>'
        )
        expected = {
            'title': 'Abstract',
            'content': 'Introduction: Some introduction text. Methods: Some methods text.',
        }
        result = xml_pipe.extract_abstract_data(xml)
        self.assertEqual(result, expected)

    def test_extract_abstract_data_structured_section_title_without_punctuation(self):
        # Some XMLs don't carry a trailing colon in the <sec><title>, unlike
        # the "Methods:" style above - a colon must be added so the title
        # doesn't run into the paragraph text (e.g. "Objetivodescrever...").
        xml = etree.fromstring(
            '<article><abstract>'
            '<sec><title>Objetivo</title><p>Descrever o metodo.</p></sec>'
            '</abstract></article>'
        )
        expected = {'title': '', 'content': 'Objetivo: Descrever o metodo.'}
        result = xml_pipe.extract_abstract_data(xml)
        self.assertEqual(result, expected)

    def test_extract_abstract_data_structured_section_without_title(self):
        xml = etree.fromstring(
            '<article><abstract>'
            '<sec><p>Untitled section text.</p></sec>'
            '</abstract></article>'
        )
        expected = {'title': '', 'content': 'Untitled section text.'}
        result = xml_pipe.extract_abstract_data(xml)
        self.assertEqual(result, expected)

    def test_extract_abstract_data_mixed_direct_and_sectioned_paragraphs(self):
        xml = etree.fromstring(
            '<article><abstract>'
            '<p>Lead paragraph.</p>'
            '<sec><title>Conclusion:</title><p>Final remarks.</p></sec>'
            '</abstract></article>'
        )
        expected = {'title': '', 'content': 'Lead paragraph. Conclusion: Final remarks.'}
        result = xml_pipe.extract_abstract_data(xml)
        self.assertEqual(result, expected)


class TestExtractAcknowledgmentData(unittest.TestCase):

    def test_extract_acknowledgment_data_empty_xml(self):
        xml_tree = etree.fromstring("<article></article>")
        expected = {"paragraphs": [], 'title': ''}
        result = xml_pipe.extract_acknowledgment_data(xml_tree)
        self.assertEqual(expected, result)

    def test_extract_acknowledgment_data_with_title_no_paragraphs(self):
        xml_tree = etree.fromstring(
            """
            <article>
                <ack>
                    <title>Acknowledgments</title>
                </ack>
            </article>
            """
        )
        expected = {
            "title": "Acknowledgments",
            "paragraphs": []
        }
        result = xml_pipe.extract_acknowledgment_data(xml_tree)
        self.assertEqual(expected, result)

    def test_extract_acknowledgment_data_with_paragraphs_no_title(self):
        xml_tree = etree.fromstring(
            """
            <article>
                <ack>
                    <p>First acknowledgment paragraph</p>
                    <p>Second acknowledgment paragraph</p>
                </ack>
            </article>
            """
        )
        expected = {
            "paragraphs": ["First acknowledgment paragraph", "Second acknowledgment paragraph"], "title": '',
        }
        result = xml_pipe.extract_acknowledgment_data(xml_tree)
        self.assertEqual(expected, result)

    def test_extract_acknowledgment_data_complete(self):
        xml_tree = etree.fromstring(
            """
            <article>
                <ack>
                    <title>Acknowledgements Section</title>
                    <p>Thank you to all contributors</p>
                    <p>Special thanks to funding agencies</p>
                    <p>Additional acknowledgments</p>
                </ack>
            </article>
            """
        )
        expected = {
            "title": "Acknowledgements Section",
            "paragraphs": [
                "Thank you to all contributors",
                "Special thanks to funding agencies",
                "Additional acknowledgments"
            ]
        }
        result = xml_pipe.extract_acknowledgment_data(xml_tree)
        self.assertEqual(expected, result)

    def test_extract_acknowledgment_data_nested_paragraphs(self):
        xml_tree = etree.fromstring(
            """
            <article>
                <ack>
                    <title>Acknowledgments</title>
                    <sec>
                        <p>Nested paragraph 1</p>
                        <p>Nested paragraph 2</p>
                    </sec>
                </ack>
            </article>
            """
        )
        expected = {
            "title": "Acknowledgments",
            "paragraphs": ["Nested paragraph 1", "Nested paragraph 2"]
        }
        result = xml_pipe.extract_acknowledgment_data(xml_tree)
        self.assertEqual(expected, result)


class TestExtractArticleMainLanguage(unittest.TestCase):

    def test_extract_article_main_language_with_valid_lang(self):
        xmltree = etree.fromstring(
            '<article xmlns:xml="http://www.w3.org/XML/1998/namespace" xml:lang="en">'
            '<front><article-meta></article-meta></front>'
            '</article>'
        )
        expected = "en"
        result = xml_pipe.extract_article_main_language(xmltree)
        self.assertEqual(expected, result)

    def test_extract_article_main_language_without_lang(self):
        xmltree = etree.fromstring(
            '<article xmlns:xml="http://www.w3.org/XML/1998/namespace">'
            '<front><article-meta></article-meta></front>'
            '</article>'
        )
        result = xml_pipe.extract_article_main_language(xmltree)
        self.assertIsNone(result)

    def test_extract_article_main_language_with_custom_namespace(self):
        xmltree = etree.fromstring(
            '<article xmlns:custom="http://custom.namespace" custom:lang="pt">'
            '<front><article-meta></article-meta></front>'
            '</article>'
        )
        expected = "pt"
        result = xml_pipe.extract_article_main_language(
            xmltree, 
            namespaces={'xml': 'http://custom.namespace'}
        )
        self.assertEqual(expected, result)

    def test_extract_article_main_language_with_multiple_langs(self):
        xmltree = etree.fromstring(
            '<article xmlns:xml="http://www.w3.org/XML/1998/namespace" xml:lang="es">'
            '<front xml:lang="en"><article-meta></article-meta></front>'
            '</article>'
        )
        expected = "es"
        result = xml_pipe.extract_article_main_language(xmltree)
        self.assertEqual(expected, result)


class TestExtractArticleTitle(unittest.TestCase):

    def test_extract_article_title_basic(self):
        xml = etree.fromstring(
            '<article><article-meta>'
            '<article-title>Sample Title</article-title>'
            '</article-meta></article>'
        )
        result = xml_pipe.extract_article_title(xml)
        self.assertEqual(result, 'Sample Title')

    def test_extract_article_title_return_element(self):
        xml = etree.fromstring(
            '<article><article-meta>'
            '<article-title>Sample Title</article-title>'
            '</article-meta></article>'
        )
        result = xml_pipe.extract_article_title(xml, return_text=False)
        self.assertIsInstance(result, etree._Element)
        
    def test_extract_article_title_empty(self):
        xml = etree.fromstring(
            '<article><article-meta>'
            '<article-title></article-title>'
            '</article-meta></article>'
        )
        result = xml_pipe.extract_article_title(xml)
        self.assertEqual(result, '')

    def test_extract_article_title_with_formatting(self):
        xml = etree.fromstring(
            '<article><article-meta>'
            '<article-title>Title with <italic>formatting</italic></article-title>'
            '</article-meta></article>'
        )
        result = xml_pipe.extract_article_title(xml)
        self.assertEqual(result, 'Title with formatting')

    def test_extract_article_title_missing(self):
        xml = etree.fromstring('<article><article-meta></article-meta></article>')
        with self.assertRaises(AttributeError):
            xml_pipe.extract_article_title(xml)


class TestExtractArticleType(unittest.TestCase):

    def test_extract_article_type_valid(self):
        xml = etree.fromstring('<article article-type="research-article"></article>')
        result = xml_pipe.extract_article_type(xml)
        self.assertEqual(result, 'research-article')

    def test_extract_article_type_missing(self):
        xml = etree.fromstring('<article></article>')
        result = xml_pipe.extract_article_type(xml)
        self.assertIsNone(result)

    def test_extract_article_type_empty(self):
        xml = etree.fromstring('<article article-type=""></article>')
        result = xml_pipe.extract_article_type(xml)
        self.assertEqual(result, '')


def _plain_para(text):
    """A single-segment, unstyled paragraph, as extract_body_data now returns it."""
    return [{'type': 'text', 'text': text, 'italic': False, 'bold': False, 'superscript': False, 'subscript': False}]


class TestExtractBodyData(unittest.TestCase):

    def test_extract_body_data_basic(self):
        xml = etree.fromstring(
            '<article>'
            '<sec>'
            '<title>Section 1</title>'
            '<p>Paragraph 1</p>'
            '<p>Paragraph 2</p>'
            '</sec>'
            '</article>'
        )
        expected = [
            {
                'level': 1,
                'title': 'Section 1',
                'paragraphs': [_plain_para('Paragraph 1'), _plain_para('Paragraph 2')],
                'tables': [],
                'figures': [],
            }
        ]
        result = xml_pipe.extract_body_data(xml)
        self.assertEqual(result, expected)

    def test_extract_body_data_excludes_abstract_and_trans_abstract_sections(self):
        # Regression: a structured abstract/trans-abstract wraps each
        # subsection in its own <sec> (see extract_abstract_data), which a
        # plain './/sec' search would also pick up as a body section,
        # duplicating the same content in both the abstract and the body.
        xml = etree.fromstring(
            '<article>'
            '<abstract>'
            '<sec><title>Background:</title><p>Abstract text.</p></sec>'
            '</abstract>'
            '<trans-abstract>'
            '<sec><title>Contexto:</title><p>Texto do resumo.</p></sec>'
            '</trans-abstract>'
            '<body>'
            '<sec><title>Introduction</title><p>Body text.</p></sec>'
            '</body>'
            '</article>'
        )
        expected = [
            {
                'level': 2,
                'title': 'Introduction',
                'paragraphs': [_plain_para('Body text.')],
                'tables': [],
                'figures': [],
            }
        ]
        result = xml_pipe.extract_body_data(xml)
        self.assertEqual(result, expected)

    def test_extract_body_data_excludes_supplementary_material_section(self):
        # Regression: <sec sec-type="supplementary-material"> (SPS 1.10) e
        # tratada por supplementary_material.extract_data/docx_supplementary_material_pipe -
        # sem essa exclusao, o titulo aparecia duplicado (uma vez aqui, vazio,
        # e outra na secao dedicada com o conteudo real).
        xml = etree.fromstring(
            '<article>'
            '<body>'
            '<sec><title>Introduction</title><p>Body text.</p></sec>'
            '</body>'
            '<back>'
            '<sec sec-type="supplementary-material"><title>Supplementary Material</title>'
            '<supplementary-material id="suppl1"><label>Suppl. 1</label></supplementary-material>'
            '</sec>'
            '</back>'
            '</article>'
        )
        result = xml_pipe.extract_body_data(xml)
        self.assertEqual(1, len(result))
        self.assertEqual('Introduction', result[0]['title'])

    def test_extract_body_data_includes_disp_formula_as_sibling_of_p(self):
        # Regression for issue #1347: <disp-formula> is often a direct
        # sibling of <p>, not nested inside one - a plain findall('p') never
        # visits it, so the formula silently vanished from the output. No
        # MathML->OMML conversion yet (see #1347's phased plan), just
        # flattened text, but present beats missing.
        xml = etree.fromstring(
            '<article xmlns:mml="http://www.w3.org/1998/Math/MathML">'
            '<sec>'
            '<title>Section 1</title>'
            '<p>See the formula below.</p>'
            '<disp-formula id="e01">'
            '<mml:math><mml:mi>Y</mml:mi><mml:mo>=</mml:mo><mml:mn>1</mml:mn></mml:math>'
            '</disp-formula>'
            '<p>Where Y is the result.</p>'
            '</sec>'
            '</article>'
        )
        expected = [
            {
                'level': 1,
                'title': 'Section 1',
                'paragraphs': [
                    _plain_para('See the formula below.'),
                    _plain_para('Y=1'),
                    _plain_para('Where Y is the result.'),
                ],
                'tables': [],
                'figures': [],
            }
        ]
        result = xml_pipe.extract_body_data(xml)
        self.assertEqual(result, expected)

    def test_extract_body_data_includes_graphic_disp_formula_as_figure(self):
        # Regression for issue #1347: a <disp-formula> rendered as an image
        # (<graphic>, no MathML) has no text for get_text_from_node to
        # flatten, so it was silently dropped even after the fix for the
        # MathML/text case above. extract_figure_data reads the same
        # label/caption/graphic shape <fig> has, so the formula is rendered
        # as a figure instead of vanishing.
        xml = etree.fromstring(
            '<article>'
            '<sec>'
            '<title>Section 1</title>'
            '<p>See the formula below.</p>'
            '<disp-formula id="e01">'
            '<graphic xlink:href="e01.tif" xmlns:xlink="http://www.w3.org/1999/xlink"/>'
            '</disp-formula>'
            '<p>Where Y is the result.</p>'
            '</sec>'
            '</article>'
        )
        expected = [
            {
                'level': 1,
                'title': 'Section 1',
                'paragraphs': [
                    _plain_para('See the formula below.'),
                    _plain_para('Where Y is the result.'),
                ],
                'tables': [],
                'figures': [
                    {'label': '', 'caption': '', 'href': 'e01.tif', 'alt': ''},
                ],
            }
        ]
        result = xml_pipe.extract_body_data(xml)
        self.assertEqual(result, expected)

    def test_extract_body_data_includes_labeled_graphic_disp_formula_as_figure(self):
        # Regression for issue #1365 (review on PR #1348): a <graphic>
        # formula with a <label> (e.g. "(1)") still has to be treated as a
        # figure - get_text_from_node returns the label text, which isn't
        # empty, so a check that only looked at "no flattenable text" missed
        # this case and dropped the <graphic>, keeping just the bare label
        # as a paragraph.
        xml = etree.fromstring(
            '<article>'
            '<sec>'
            '<title>Section 1</title>'
            '<p>See the formula below.</p>'
            '<disp-formula id="e01">'
            '<label>(1)</label>'
            '<graphic xlink:href="e01.tif" xmlns:xlink="http://www.w3.org/1999/xlink"/>'
            '</disp-formula>'
            '<p>Where Y is the result.</p>'
            '</sec>'
            '</article>'
        )
        expected = [
            {
                'level': 1,
                'title': 'Section 1',
                'paragraphs': [
                    _plain_para('See the formula below.'),
                    _plain_para('Where Y is the result.'),
                ],
                'tables': [],
                'figures': [
                    {'label': '(1)', 'caption': '', 'href': 'e01.tif', 'alt': ''},
                ],
            }
        ]
        result = xml_pipe.extract_body_data(xml)
        self.assertEqual(result, expected)

    def test_extract_body_data_includes_bullet_list_items(self):
        # Regression for issue #1365: <list> isn't 'p' or 'disp-formula', so
        # a plain child-tag check silently dropped it and every <list-item>
        # inside - reproduced against a5.xml's Treatment Series lists.
        xml = etree.fromstring(
            '<article>'
            '<sec>'
            '<title>Section 1</title>'
            '<p>The treatments included:</p>'
            '<list list-type="bullet">'
            '<list-item><p>T1 - Control</p></list-item>'
            '<list-item><p>T2 - Treated</p></list-item>'
            '</list>'
            '</sec>'
            '</article>'
        )
        expected = [
            {
                'level': 1,
                'title': 'Section 1',
                'paragraphs': [
                    _plain_para('The treatments included:'),
                    [
                        {'type': 'text', 'text': '• ', 'italic': False, 'bold': False,
                         'superscript': False, 'subscript': False},
                        {'type': 'text', 'text': 'T1 - Control', 'italic': False, 'bold': False,
                         'superscript': False, 'subscript': False},
                    ],
                    [
                        {'type': 'text', 'text': '• ', 'italic': False, 'bold': False,
                         'superscript': False, 'subscript': False},
                        {'type': 'text', 'text': 'T2 - Treated', 'italic': False, 'bold': False,
                         'superscript': False, 'subscript': False},
                    ],
                ],
                'tables': [],
                'figures': [],
            }
        ]
        result = xml_pipe.extract_body_data(xml)
        self.assertEqual(result, expected)

    def test_extract_body_data_includes_ordered_list_items_with_numbering(self):
        xml = etree.fromstring(
            '<article>'
            '<sec>'
            '<title>Section 1</title>'
            '<list list-type="order">'
            '<list-item><p>First step</p></list-item>'
            '<list-item><p>Second step</p></list-item>'
            '<list-item><p>Third step</p></list-item>'
            '</list>'
            '</sec>'
            '</article>'
        )
        result = xml_pipe.extract_body_data(xml)
        markers = [para[0]['text'] for para in result[0]['paragraphs']]
        self.assertEqual(markers, ['1. ', '2. ', '3. '])

    def test_extract_body_data_simple_list_has_no_marker(self):
        # list-type="simple" is used when the items already carry their own
        # numbering some other way - a5.xml's Equations 3-10, each numbered
        # by its own <disp-formula><label>, not by the list.
        xml = etree.fromstring(
            '<article xmlns:mml="http://www.w3.org/1998/Math/MathML">'
            '<sec>'
            '<title>Section 1</title>'
            '<list list-type="simple">'
            '<list-item><p>Total biomass:'
            '<disp-formula id="e03">'
            '<mml:math><mml:mi>Y</mml:mi><mml:mo>=</mml:mo><mml:mn>1</mml:mn></mml:math>'
            '<label>(3)</label>'
            '</disp-formula>'
            '</p></list-item>'
            '</list>'
            '</sec>'
            '</article>'
        )
        expected = [
            {
                'level': 1,
                'title': 'Section 1',
                'paragraphs': [
                    _plain_para('Total biomass:Y=1(3)'),
                ],
                'tables': [],
                'figures': [],
            }
        ]
        result = xml_pipe.extract_body_data(xml)
        self.assertEqual(result, expected)

    def test_extract_body_data_includes_list_nested_inside_p(self):
        # Regression for issue #1365, reproduced against the real corpus
        # sample a28.xml: <list> can also occur as a child of <p> rather
        # than as its own sibling. get_segments_from_node has no special
        # handling for <list>, so leaving it unhandled would silently
        # flatten it to nothing - same content loss as a <list> direct
        # sibling of <p>, just one level deeper.
        xml = etree.fromstring(
            '<article>'
            '<sec>'
            '<title>Section 1</title>'
            '<p>The following propositions were formulated:</p>'
            '<p>'
            '<list list-type="simple">'
            '<list-item><p>Proposition P1: text one.</p></list-item>'
            '<list-item><p>Proposition P2: text two.</p></list-item>'
            '</list>'
            '</p>'
            '</sec>'
            '</article>'
        )
        expected = [
            {
                'level': 1,
                'title': 'Section 1',
                'paragraphs': [
                    _plain_para('The following propositions were formulated:'),
                    _plain_para('Proposition P1: text one.'),
                    _plain_para('Proposition P2: text two.'),
                ],
                'tables': [],
                'figures': [],
            }
        ]
        result = xml_pipe.extract_body_data(xml)
        self.assertEqual(result, expected)

    def test_extract_body_data_with_tables(self):
        xml = etree.fromstring(
            '<article>'
            '<sec>'
            '<title>Section 1</title>'
            '<p>Paragraph 1</p>'
            '<table-wrap>'
            '<label>Table 1</label>'
            '<title>Sample Table</title>'
            '<table>'
            '<thead><tr><th>Header</th></tr></thead>'
            '<tbody><tr><td>Data</td></tr></tbody>'
            '</table>'
            '</table-wrap>'
            '</sec>'
            '</article>'
        )
        expected = [
            {
                'level': 1,
                'title': 'Section 1',
                'paragraphs': [_plain_para('Paragraph 1')],
                'tables': [
                    {
                        'label': 'Table 1',
                        'title': 'Sample Table',
                        'headers': [['Header']],
                        'rows': [['Data']],
                        'layout': 'double-column-layout',
                        'column_widths': [50],
                        'header_spans': [[{'colspan': 1, 'rowspan': 1, 'text': 'Header'}]],
                        'row_spans': [[{'colspan': 1, 'rowspan': 1, 'text': 'Data'}]],
                        'foot': [],
                    }
                ],
                'figures': [],
            }
        ]
        result = xml_pipe.extract_body_data(xml)
        self.assertEqual(result, expected)

    def test_extract_body_data_with_nested_sections(self):
        xml = etree.fromstring(
            '<article>'
            '<sec>'
            '<title>Section 1</title>'
            '<p>Paragraph 1</p>'
            '<sec>'
            '<title>Subsection 1.1</title>'
            '<p>Paragraph 1.1</p>'
            '</sec>'
            '</sec>'
            '</article>'
        )
        expected = [
            {
                'level': 1,
                'title': 'Section 1',
                'paragraphs': [_plain_para('Paragraph 1')],
                'tables': [],
                'figures': [],
            },
            {
                'level': 2,
                'title': 'Subsection 1.1',
                'paragraphs': [_plain_para('Paragraph 1.1')],
                'tables': [],
                'figures': [],
            }
        ]
        result = xml_pipe.extract_body_data(xml)
        self.assertEqual(result, expected)

    def test_extract_body_data_with_table_references(self):
        xml = etree.fromstring(
            '<article>'
            '<sec>'
            '<title>Section 1</title>'
            '<p>Paragraph with <xref ref-type="table">Table 1</xref></p>'
            '<table-wrap>'
            '<label>Table 1</label>'
            '<title>Sample Table</title>'
            '<table>'
            '<thead><tr><th>Header</th></tr></thead>'
            '<tbody><tr><td>Data</td></tr></tbody>'
            '</table>'
            '</table-wrap>'
            '</sec>'
            '</article>'
        )
        expected = [
            {
                'level': 1,
                'title': 'Section 1',
                'paragraphs': [_plain_para('Paragraph with Table 1')],
                'tables': [
                    {
                        'label': 'Table 1',
                        'title': 'Sample Table',
                        'headers': [['Header']],
                        'rows': [['Data']],
                        'layout': 'double-column-layout',
                        'column_widths': [50],
                        'header_spans': [[{'colspan': 1, 'rowspan': 1, 'text': 'Header'}]],
                        'row_spans': [[{'colspan': 1, 'rowspan': 1, 'text': 'Data'}]],
                        'foot': [],
                    }
                ],
                'figures': [],
            }
        ]
        result = xml_pipe.extract_body_data(xml)
        self.assertEqual(result, expected)

    def test_paragraph_citations_have_no_stray_space_around_parentheses(self):
        # Regression: a naive `.xpath('.//text()...')` + `' '.join(...)`
        # inserted a space between every text-node fragment regardless of
        # adjacency in the source, turning "(<xref>...</xref>; <xref>...
        # </xref>)" into "( ... ; ... )".
        xml = etree.fromstring(
            '<article><sec><title>Introduction</title>'
            '<p>Pressure is increasing '
            '(<xref ref-type="bibr" rid="B1">Lang and Barling, 2012</xref>'
            '; <xref ref-type="bibr" rid="B2">Ripple et al., 2019</xref>) '
            'worldwide.</p>'
            '</sec></article>'
        )
        result = xml_pipe.extract_body_data(xml)
        self.assertEqual(
            result[0]['paragraphs'],
            [_plain_para('Pressure is increasing (Lang and Barling, 2012; Ripple et al., 2019) worldwide.')],
        )

    def test_embedded_fig_tail_whitespace_is_collapsed_not_left_raw(self):
        # A skipped <fig>'s tail can carry the source's pretty-printing
        # indentation (a newline + spaces); it must collapse to one space
        # rather than leak into the rendered paragraph.
        xml = etree.fromstring(
            '<article><sec><title>Results</title>'
            '<p>See the figure below\n'
            '<fig id="f1"><label>Figure 1</label></fig>\n            '
            'for details.</p>'
            '</sec></article>'
        )
        result = xml_pipe.extract_body_data(xml)
        self.assertEqual(
            result[0]['paragraphs'],
            [_plain_para('See the figure below for details.')],
        )

    def test_extract_body_data_preserves_inline_formatting(self):
        # Item 04 of the pdf_generator backlog: <italic>/<bold>/<sup>/<sub>
        # inside a body paragraph used to be flattened to plain text by
        # get_text_from_node. extract_body_data now keeps them as
        # style-tagged segments instead of a single string.
        xml = etree.fromstring(
            '<article><sec><title>Results</title>'
            '<p>The species <italic>Genus species</italic> was observed'
            '<sup>1</sup> in <bold>high</bold> numbers.</p>'
            '</sec></article>'
        )
        result = xml_pipe.extract_body_data(xml)
        self.assertEqual(
            result[0]['paragraphs'],
            [[
                {'type': 'text', 'text': 'The species ', 'italic': False, 'bold': False, 'superscript': False, 'subscript': False},
                {'type': 'text', 'text': 'Genus species', 'italic': True, 'bold': False, 'superscript': False, 'subscript': False},
                {'type': 'text', 'text': ' was observed', 'italic': False, 'bold': False, 'superscript': False, 'subscript': False},
                {'type': 'text', 'text': '1', 'italic': False, 'bold': False, 'superscript': True, 'subscript': False},
                {'type': 'text', 'text': ' in ', 'italic': False, 'bold': False, 'superscript': False, 'subscript': False},
                {'type': 'text', 'text': 'high', 'italic': False, 'bold': True, 'superscript': False, 'subscript': False},
                {'type': 'text', 'text': ' numbers.', 'italic': False, 'bold': False, 'superscript': False, 'subscript': False},
            ]],
        )

    def test_extract_body_data_falls_back_to_body_when_no_sec_exists(self):
        # Regression for issue #1351: a <body> with <p> as direct children
        # and no <sec> at all (valid JATS pattern for unsectioned short
        # communications/brief reports) used to disappear entirely, since
        # the section search only ever looked for <sec>.
        xml = etree.fromstring(
            '<article><body>'
            '<p>Paragraph 1</p>'
            '<p>Paragraph 2</p>'
            '</body></article>'
        )
        expected = [
            {
                'level': 1,
                'title': None,
                'paragraphs': [_plain_para('Paragraph 1'), _plain_para('Paragraph 2')],
                'tables': [],
                'figures': [],
            }
        ]
        result = xml_pipe.extract_body_data(xml)
        self.assertEqual(result, expected)

    def test_extract_body_data_falls_back_to_body_with_table_and_figure(self):
        xml = etree.fromstring(
            '<article><body>'
            '<p>Intro paragraph.</p>'
            '<p>Figure 1<fig id="f1"><label>Figure 1</label></fig></p>'
            '<p>Table 1'
            '<table-wrap id="t1">'
            '<label>Table 1</label>'
            '<title>Sample Table</title>'
            '<table>'
            '<thead><tr><th>Header</th></tr></thead>'
            '<tbody><tr><td>Data</td></tr></tbody>'
            '</table>'
            '</table-wrap>'
            '</p>'
            '</body></article>'
        )
        result = xml_pipe.extract_body_data(xml)
        self.assertEqual(len(result), 1)
        self.assertIsNone(result[0]['title'])
        self.assertEqual(len(result[0]['tables']), 1)
        self.assertEqual(len(result[0]['figures']), 1)

    def test_extract_body_data_does_not_fall_back_when_sec_exists(self):
        # Regression: the fallback must not kick in for a normally
        # sectioned article, even one with just a single <sec>.
        xml = etree.fromstring(
            '<article><body>'
            '<sec><title>Introduction</title><p>Body text.</p></sec>'
            '</body></article>'
        )
        expected = [
            {
                'level': 2,
                'title': 'Introduction',
                'paragraphs': [_plain_para('Body text.')],
                'tables': [],
                'figures': [],
            }
        ]
        result = xml_pipe.extract_body_data(xml)
        self.assertEqual(result, expected)

    def test_extract_body_data_falls_back_even_when_an_unrelated_sec_exists_outside_body(self):
        # Regression for issue #1351, reproduced against the real corpus
        # sample a8.xml: <body> has no <sec> of its own, but a <sec
        # sec-type="data-availability"> lives under <back>. A naive
        # "any <sec> found anywhere -> skip the fallback" check would
        # wrongly treat body as already covered by that unrelated sec and
        # keep discarding body's own content.
        xml = etree.fromstring(
            '<article>'
            '<body>'
            '<p>Body paragraph.</p>'
            '</body>'
            '<back>'
            '<sec sec-type="data-availability">'
            '<label>Data availability</label>'
            '<p>Data statement.</p>'
            '</sec>'
            '</back>'
            '</article>'
        )
        result = xml_pipe.extract_body_data(xml)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['title'], None)
        self.assertEqual(result[0]['paragraphs'], [_plain_para('Body paragraph.')])
        self.assertEqual(result[1]['paragraphs'], [_plain_para('Data statement.')])


class TestExtractCategory(unittest.TestCase):

    def setUp(self):
        self.xml_with_category = etree.fromstring("""
            <article>
                <article-meta>
                    <article-categories>
                        <subj-group subj-group-type="heading">
                            <subject>Original Article</subject>
                        </subj-group>
                    </article-categories>
                </article-meta>
            </article>
        """)
        
        self.xml_without_category = etree.fromstring("""
            <article>
                <article-meta>
                    <article-categories>
                        <subj-group>
                            <subject>Other Content</subject>
                        </subj-group>
                    </article-categories>
                </article-meta>
            </article>
        """)

    def test_extract_category_returns_text(self):
        result = xml_pipe.extract_category(self.xml_with_category)
        self.assertEqual(result, "Original Article")

    def test_extract_category_returns_element(self):
        result = xml_pipe.extract_category(self.xml_with_category, return_text=False)
        self.assertIsInstance(result, etree._Element)
        self.assertEqual(result.text, "Original Article")

    def test_extract_category_missing_category_raises_attribute_error(self):
        with self.assertRaises(AttributeError):
            xml_pipe.extract_category(self.xml_without_category)

    def test_extract_category_empty_xml_raises_attribute_error(self):
        empty_xml = etree.fromstring("<article></article>")
        with self.assertRaises(AttributeError):
            xml_pipe.extract_category(empty_xml)

    def test_extract_category_with_empty_subject(self):
        xml = etree.fromstring("""
            <article>
                <article-meta>
                    <article-categories>
                        <subj-group subj-group-type="heading">
                            <subject></subject>
                        </subj-group>
                    </article-categories>
                </article-meta>
            </article>
        """)
        result = xml_pipe.extract_category(xml)
        self.assertEqual(result, "")


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
        result = xml_pipe.extract_cite_as_part_one(xml)
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
        result = xml_pipe.extract_cite_as_part_one(xml)
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
        result = xml_pipe.extract_cite_as_part_one(xml, return_node=True)
        self.assertIsInstance(result, etree._Element)
        self.assertEqual(result.tag, 'p')
        self.assertEqual(result.text, 'Cite as: Example Citation')

    def test_extract_cite_as_part_one_no_fn_group(self):
        xml = etree.fromstring('<article></article>')
        result = xml_pipe.extract_cite_as_part_one(xml)
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
        result = xml_pipe.extract_cite_as_part_one(xml)
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
        result = xml_pipe.extract_cite_as_part_one(xml)
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
        result = xml_pipe.extract_cite_as_part_one(xml)
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
        result = xml_pipe.extract_cite_as_part_one(xml)
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
        self.assertEqual(xml_pipe.build_full_citation(xml, footer_data), expected)

    def test_omits_issue_parens_when_issue_is_absent(self):
        xml = self._article(given_names=('Bárbara Passos da Silva',))
        footer_data = {'year': '2024', 'volume': '10', 'issue': '',
                        'location_label': 'e12345'}
        result = xml_pipe.build_full_citation(xml, footer_data)
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
        result = xml_pipe.build_full_citation(xml, footer_data)
        self.assertIn('2023;e236720.', result)

    def test_initials_exclude_lowercase_particles(self):
        xml = self._article(given_names=('Bárbara Passos da Silva',))
        footer_data = {'year': '2024', 'volume': '', 'issue': '', 'location_label': ''}
        result = xml_pipe.build_full_citation(xml, footer_data)
        self.assertTrue(result.startswith('Surname0 BPS.'))

    def test_truncates_to_et_al_beyond_six_authors(self):
        xml = self._article(given_names=[f'Author{i}' for i in range(8)])
        footer_data = {'year': '2024', 'volume': '', 'issue': '', 'location_label': ''}
        result = xml_pipe.build_full_citation(xml, footer_data)
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
        self.assertEqual(xml_pipe.build_full_citation(xml, footer_data), '')

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
        result = xml_pipe.build_full_citation(xml, footer_data)
        self.assertIn('Full Journal Name.', result)

    def test_unknown_style_returns_empty_string(self):
        xml = self._article(given_names=('Bárbara Passos da Silva',))
        footer_data = {'year': '2024', 'volume': '', 'issue': '', 'location_label': ''}
        result = xml_pipe.build_full_citation(xml, footer_data, style='abnt')
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
        result = xml_pipe.build_full_citation(xml, footer_data)
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
        result = xml_pipe.build_full_citation(xml, footer_data)
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
        reference = xml_pipe._build_csl_reference(self._article(), {})
        self.assertEqual(reference['type'], 'article-journal')

    def test_accepts_custom_csl_type(self):
        reference = xml_pipe._build_csl_reference(self._article(), {}, csl_type='editorial')
        self.assertEqual(reference['type'], 'editorial')


class TestExtractContribData(unittest.TestCase):

    def test_extract_contrib_data_complete(self):
        xml = etree.fromstring("""
            <article>
                <contrib-group>
                    <contrib>
                        <name>
                            <surname>Smith</surname>
                            <given-names>John</given-names>
                        </name>
                        <xref ref-type="aff" rid="aff1"/>
                        <xref ref-type="corresp" rid="c1"/>
                        <contrib-id contrib-id-type="orcid">0000-0002-1234-5678</contrib-id>
                    </contrib>
                </contrib-group>
                <aff id="aff1">
                    <label>1</label>
                    <institution content-type="original">University of Testing</institution>
                </aff>
                <author-notes>
                    <corresp id="c1">
                        <email>john.smith@test.edu</email>
                    </corresp>
                </author-notes>
            </article>
        """)
        result = xml_pipe.extract_contrib_data(xml)
        self.assertEqual(result['authors_names'], ['John Smith[^]1*'])
        self.assertEqual(result['affiliations'], ['1[^] University of Testing'])
        self.assertEqual(result['corresponding_author'], '*[^] Corresponding author: john.smith@test.edu; https://orcid.org/0000-0002-1234-5678')

    def test_extract_contrib_data_multiple_authors(self):
        xml = etree.fromstring("""
            <article>
                <contrib-group>
                    <contrib>
                        <name>
                            <surname>Smith</surname>
                            <given-names>John</given-names>
                        </name>
                        <xref ref-type="aff" rid="aff1"/>
                    </contrib>
                    <contrib>
                        <name>
                            <surname>Doe</surname>
                            <given-names>Jane</given-names>
                        </name>
                        <xref ref-type="aff" rid="aff2"/>
                    </contrib>
                </contrib-group>
                <aff id="aff1">
                    <label>1</label>
                    <institution content-type="original">University A</institution>
                </aff>
                <aff id="aff2">
                    <label>2</label>
                    <institution content-type="original">University B</institution>
                </aff>
            </article>
        """)
        result = xml_pipe.extract_contrib_data(xml)
        self.assertEqual(result['authors_names'], ['John Smith[^]1', 'Jane Doe[^]2'])
        self.assertEqual(result['affiliations'], ['1[^] University A', '2[^] University B'])
        self.assertEqual(result['corresponding_author'], '')

    def test_extract_contrib_data_empty_tree(self):
        xml = etree.fromstring("<article></article>")
        result = xml_pipe.extract_contrib_data(xml)
        self.assertEqual(result['authors_names'], [])
        self.assertEqual(result['affiliations'], [])
        self.assertEqual(result['corresponding_author'], '')

    def test_extract_contrib_data_missing_institution(self):
        xml = etree.fromstring("""
            <article>
                <contrib-group>
                    <contrib>
                        <name>
                            <surname>Smith</surname>
                            <given-names>John</given-names>
                        </name>
                        <xref ref-type="aff" rid="aff1"/>
                    </contrib>
                </contrib-group>
                <aff id="aff1">
                    <label>1</label>
                </aff>
            </article>
        """)
        result = xml_pipe.extract_contrib_data(xml)
        self.assertEqual(result['authors_names'], ['John Smith[^]1'])
        self.assertEqual(result['affiliations'], [])

    def test_extract_contrib_data_missing_label(self):
        xml = etree.fromstring("""
            <article>
                <contrib-group>
                    <contrib>
                        <name>
                            <surname>Smith</surname>
                            <given-names>John</given-names>
                        </name>
                        <xref ref-type="aff" rid="aff1"/>
                    </contrib>
                </contrib-group>
                <aff id="aff1">
                    <institution content-type="original">University X</institution>
                </aff>
            </article>
        """)
        result = xml_pipe.extract_contrib_data(xml)
        self.assertEqual(result['authors_names'], ['John Smith[^]'])
        self.assertEqual(result['affiliations'], ['[^] University X'])

    def test_subarticle_affiliation_is_not_printed(self):
        # Regression: translated affiliations in a sub-article must not be
        # included in the affiliation list of the main article.
        xml = etree.fromstring("""
            <article>
                <front>
                    <article-meta>
                        <contrib-group>
                            <contrib>
                                <name>
                                    <surname>Smith</surname>
                                    <given-names>John</given-names>
                                </name>
                                <xref ref-type="aff" rid="aff1"/>
                            </contrib>
                        </contrib-group>
                        <aff id="aff1">
                            <label>I</label>
                            <institution content-type="original">University A</institution>
                        </aff>
                    </article-meta>
                </front>
                <sub-article article-type="translation">
                    <front-stub>
                        <contrib-group>
                            <contrib>
                                <name>
                                    <surname>Smith</surname>
                                    <given-names>John</given-names>
                                </name>
                                <xref ref-type="aff" rid="aff1e"/>
                            </contrib>
                        </contrib-group>
                        <aff id="aff1e">
                            <label>I</label>
                            <institution content-type="original">Universidade A</institution>
                        </aff>
                    </front-stub>
                </sub-article>
            </article>
        """)
        result = xml_pipe.extract_contrib_data(xml)
        self.assertEqual(result['affiliations'], ['I[^] University A'])

    def test_main_article_affiliations_are_kept_regardless_of_id_pattern(self):
        xml = etree.fromstring("""
            <article>
                <front>
                    <article-meta>
                        <contrib-group>
                            <contrib>
                                <name>
                                    <surname>Smith</surname>
                                    <given-names>John</given-names>
                                </name>
                                <xref ref-type="aff" rid="aff01"/>
                            </contrib>
                            <contrib>
                                <name>
                                    <surname>Doe</surname>
                                    <given-names>Jane</given-names>
                                </name>
                                <xref ref-type="aff" rid="aff0100"/>
                            </contrib>
                        </contrib-group>
                        <aff id="aff01">
                            <label>1</label>
                            <institution content-type="original">University A</institution>
                        </aff>
                        <aff id="aff0100">
                            <label>2</label>
                            <institution content-type="original">University B</institution>
                        </aff>
                    </article-meta>
                </front>
            </article>
        """)
        result = xml_pipe.extract_contrib_data(xml)
        self.assertEqual(
            result['affiliations'],
            ['1[^] University A', '2[^] University B'],
        )

    def test_main_article_affiliation_without_xref_is_printed(self):
        xml = etree.fromstring("""
            <article>
                <front>
                    <article-meta>
                        <contrib-group>
                            <contrib>
                                <name>
                                    <surname>Smith</surname>
                                    <given-names>John</given-names>
                                </name>
                            </contrib>
                        </contrib-group>
                        <aff id="aff1">
                            <label>1</label>
                            <institution content-type="original">University A</institution>
                        </aff>
                    </article-meta>
                </front>
                <sub-article article-type="translation">
                    <front-stub>
                        <aff id="aff1e">
                            <label>1</label>
                            <institution content-type="original">Universidade A</institution>
                        </aff>
                    </front-stub>
                </sub-article>
            </article>
        """)
        result = xml_pipe.extract_contrib_data(xml)
        self.assertEqual(result['affiliations'], ['1[^] University A'])


class TestExtractDOI(unittest.TestCase):

    def setUp(self):
        self.xml_with_doi = etree.fromstring(
            '<article>'
            '<article-meta>'
            '<article-id pub-id-type="doi">10.1234/example.doi.2023</article-id>'
            '</article-meta>'
            '</article>'
        )
        
    def test_extract_doi_text(self):
        result = xml_pipe.extract_doi(self.xml_with_doi, return_text=True)
        self.assertEqual(result, "10.1234/example.doi.2023")

    def test_extract_doi_element(self):
        result = xml_pipe.extract_doi(self.xml_with_doi, return_text=False)
        self.assertIsInstance(result, etree._Element)
        self.assertEqual(result.tag, "article-id")
        self.assertEqual(result.get("pub-id-type"), "doi")

    def test_extract_doi_missing_doi(self):
        xml_without_doi = etree.fromstring(
            '<article>'
            '<article-meta>'
            '<article-id pub-id-type="other">12345</article-id>'
            '</article-meta>'
            '</article>'
        )
        with self.assertRaises(AttributeError):
            xml_pipe.extract_doi(xml_without_doi)

    def test_extract_doi_empty_doi(self):
        xml_empty_doi = etree.fromstring(
            '<article>'
            '<article-meta>'
            '<article-id pub-id-type="doi"></article-id>'
            '</article-meta>'
            '</article>'
        )
        result = xml_pipe.extract_doi(xml_empty_doi)
        self.assertIsNone(result)

    def test_extract_doi_malformed_xml(self):
        xml_malformed = etree.fromstring(
            '<article>'
            '<article-meta>'
            '<article-id>10.1234/malformed</article-id>'
            '</article-meta>'
            '</article>'
        )
        with self.assertRaises(AttributeError):
            xml_pipe.extract_doi(xml_malformed)


class TestExtractFooterData(unittest.TestCase):

    def test_extract_footer_data_complete(self):
        xml = etree.fromstring(
            '<article>'
            '<pub-date date-type="collection" publication-format="electronic">'
            '<year>2023</year>'
            '</pub-date>'
            '<front>'
            '<volume>10</volume>'
            '<issue>2</issue>'
            '<fpage>123</fpage>'
            '<lpage>130</lpage>'
            '</front>'
            '</article>'
        )
        expected = {
            'year': '2023',
            'volume': '10',
            'issue': '2',
            'fpage': 123,
            'lpage': 130,
            'elocation_id': '',
            'location_label': '123-130',
        }
        result = xml_pipe.extract_footer_data(xml)
        self.assertEqual(result, expected)

    def test_extract_footer_data_missing_elements(self):
        xml = etree.fromstring(
            '<article>'
            '<pub-date date-type="collection" publication-format="electronic">'
            '<year>2023</year>'
            '</pub-date>'
            '<front>'
            '</front>'
            '</article>'
        )
        expected = {
            'year': '2023',
            'volume': '',
            'issue': '',
            'fpage': '',
            'lpage': '',
            'elocation_id': '',
            'location_label': '',
        }
        result = xml_pipe.extract_footer_data(xml)
        self.assertEqual(result, expected)

    def test_extract_footer_data_no_pub_date(self):
        xml = etree.fromstring('<article></article>')
        expected = {
            'year': '', 'volume': '', 'issue': '', 'fpage': '', 'lpage': '',
            'elocation_id': '', 'location_label': '',
        }
        result = xml_pipe.extract_footer_data(xml)
        self.assertEqual(result, expected)

    def test_extract_footer_data_uses_elocation_id_when_fpage_is_absent(self):
        xml = etree.fromstring(
            '<article>'
            '<pub-date date-type="collection" publication-format="electronic">'
            '<year>2024</year>'
            '</pub-date>'
            '<front>'
            '<volume>33</volume>'
            '<issue>3</issue>'
            '<elocation-id>e282794</elocation-id>'
            '</front>'
            '</article>'
        )
        expected = {
            'year': '2024',
            'volume': '33',
            'issue': '3',
            'fpage': '',
            'lpage': '',
            'elocation_id': 'e282794',
            'location_label': 'e282794',
        }
        result = xml_pipe.extract_footer_data(xml)
        self.assertEqual(result, expected)


class TestExtractJournalTitle(unittest.TestCase):

    def test_extract_journal_title_basic(self):
        xml = etree.fromstring(
            '<article><journal-meta><journal-title>Science Journal</journal-title></journal-meta></article>'
        )
        result = xml_pipe.extract_journal_title(xml)
        self.assertEqual(result, 'Science Journal')

    def test_extract_journal_title_return_node(self):
        xml = etree.fromstring(
            '<article><journal-meta><journal-title>Science Journal</journal-title></journal-meta></article>'
        )
        result = xml_pipe.extract_journal_title(xml, return_text=False)
        self.assertIsInstance(result, etree._Element)
        self.assertEqual(result.tag, 'journal-title')
        self.assertEqual(result.text, 'Science Journal')

    def test_extract_journal_title_empty(self):
        xml = etree.fromstring(
            '<article><journal-meta><journal-title></journal-title></journal-meta></article>'
        )
        result = xml_pipe.extract_journal_title(xml)
        self.assertEqual(result, '')

    def test_extract_journal_title_missing(self):
        xml = etree.fromstring('<article><journal-meta></journal-meta></article>')
        with self.assertRaises(AttributeError):
            xml_pipe.extract_journal_title(xml)

    def test_extract_journal_title_with_nested_elements(self):
        xml = etree.fromstring(
            '<article><journal-meta><journal-title>Science <italic>Journal</italic></journal-title></journal-meta></article>'
        )
        result = xml_pipe.extract_journal_title(xml)
        self.assertEqual(result, 'Science Journal')


class TestExtractKeywordsData(unittest.TestCase):

    def test_extract_keywords_data_basic(self):
        xml = etree.fromstring(
            '<article>'
            '<kwd-group xml:lang="en">'
            '<title>Keywords</title>'
            '<kwd>Keyword1</kwd>'
            '<kwd>Keyword2</kwd>'
            '</kwd-group>'
            '</article>'
        )
        expected = {
            'title': 'Keywords',
            'keywords': 'Keyword1, Keyword2'
        }
        result = xml_pipe.extract_keywords_data(xml)
        self.assertEqual(result, expected)

    def test_extract_keywords_data_no_keywords(self):
        xml = etree.fromstring(
            '<article>'
            '<kwd-group xml:lang="en">'
            '<title>Keywords</title>'
            '</kwd-group>'
            '</article>'
        )
        expected = {
            'title': 'Keywords',
            'keywords': ''
        }
        result = xml_pipe.extract_keywords_data(xml)
        self.assertEqual(result, expected)

    def test_extract_keywords_data_no_title(self):
        xml = etree.fromstring(
            '<article>'
            '<kwd-group xml:lang="en">'
            '<kwd>Keyword1</kwd>'
            '<kwd>Keyword2</kwd>'
            '</kwd-group>'
            '</article>'
        )
        expected = {
            'title': '',
            'keywords': 'Keyword1, Keyword2'
        }
        result = xml_pipe.extract_keywords_data(xml)
        self.assertEqual(result, expected)

    def test_extract_keywords_data_different_language(self):
        xml = etree.fromstring(
            '<article>'
            '<kwd-group xml:lang="es">'
            '<title>Palabras clave</title>'
            '<kwd>Palabra1</kwd>'
            '<kwd>Palabra2</kwd>'
            '</kwd-group>'
            '</article>'
        )
        expected = {
            'title': 'Palabras clave',
            'keywords': 'Palabra1, Palabra2'
        }
        result = xml_pipe.extract_keywords_data(xml, lang='es')
        self.assertEqual(result, expected)

    def test_extract_keywords_data_no_kwd_group(self):
        xml = etree.fromstring('<article></article>')
        expected = {
            'title': '',
            'keywords': ''
        }
        result = xml_pipe.extract_keywords_data(xml)
        self.assertEqual(result, expected)

    def test_extract_keywords_data_keyword_with_inline_markup(self):
        """
        Regression test for issue #1321: a <kwd> containing inline markup
        (e.g. <italic>) used to be truncated at kwd.text, dropping the
        italic text and everything after it within that keyword.
        """
        xml = etree.fromstring(
            '<article>'
            '<kwd-group xml:lang="en">'
            '<title>Keywords</title>'
            '<kwd>maize (<italic>Zea mays</italic> L.)</kwd>'
            '<kwd>growth stimulation</kwd>'
            '</kwd-group>'
            '</article>'
        )
        expected = {
            'title': 'Keywords',
            'keywords': 'maize (Zea mays L.), growth stimulation'
        }
        result = xml_pipe.extract_keywords_data(xml)
        self.assertEqual(result, expected)

    def test_extract_keywords_data_title_with_inline_markup(self):
        xml = etree.fromstring(
            '<article>'
            '<kwd-group xml:lang="en">'
            '<title>Keywords<italic>*</italic></title>'
            '<kwd>Keyword1</kwd>'
            '</kwd-group>'
            '</article>'
        )
        result = xml_pipe.extract_keywords_data(xml)
        self.assertEqual(result['title'], 'Keywords*')


class TestExtractReferencesData(unittest.TestCase):

    def test_extract_references_data_empty_xml(self):
        xmltree = etree.fromstring("<root></root>")
        expected = {'title': 'References', 'references': []}
        result = xml_pipe.extract_references_data(xmltree)
        self.assertEqual(expected, result)

    def test_extract_references_data_with_empty_ref_list(self):
        xmltree = etree.fromstring("<root><ref-list></ref-list></root>")
        expected = {'title': 'References', 'references': []}
        result = xml_pipe.extract_references_data(xmltree)
        self.assertEqual(expected, result)

    def test_extract_references_data_with_multiple_references(self):
        xml_content = """
            <root>
                <ref-list>
                    <ref>
                        <mixed-citation>Reference 1</mixed-citation>
                    </ref>
                    <ref>
                        <mixed-citation>Reference 2</mixed-citation>
                    </ref>
                </ref-list>
            </root>
        """
        xmltree = etree.fromstring(xml_content)
        result = xml_pipe.extract_references_data(xmltree)
        self.assertEqual('References', result['title'])
        self.assertEqual(2, len(result['references']))
        self.assertEqual('Reference 1', result['references'][0].text)
        self.assertEqual('Reference 2', result['references'][1].text)

    def test_extract_references_data_with_nested_ref_list(self):
        xml_content = """
            <root>
                <article>
                    <back>
                        <ref-list>
                            <ref>
                                <mixed-citation>Nested Reference</mixed-citation>
                            </ref>
                        </ref-list>
                    </back>
                </article>
            </root>
        """
        xmltree = etree.fromstring(xml_content)
        result = xml_pipe.extract_references_data(xmltree)
        self.assertEqual(1, len(result['references']))
        self.assertEqual('Nested Reference', result['references'][0].text)

    def test_extract_references_data_without_mixed_citation(self):
        xml_content = """
            <root>
                <ref-list>
                    <ref>
                        <element-citation>Citation without mixed</element-citation>
                    </ref>
                </ref-list>
            </root>
        """
        xmltree = etree.fromstring(xml_content)
        result = xml_pipe.extract_references_data(xmltree)
        self.assertEqual(0, len(result['references']))


class TestExtractTableData(unittest.TestCase):

    def test_extract_table_data_complete(self):
        xml_str = """
            <table-wrap>
                <label>Table 1</label>
                <title>Sample Data</title>
                <table>
                    <thead>
                        <tr><th>Name</th><th>Age</th></tr>
                    </thead>
                    <tbody>
                        <tr><td>John</td><td>25</td></tr>
                        <tr><td>Jane</td><td>30</td></tr>
                    </tbody>
                </table>
            </table-wrap>
        """
        table_wrap = etree.fromstring(xml_str)
        expected = {
            'label': 'Table 1',
            'title': 'Sample Data',
            'headers': [['Name', 'Age']],
            'rows': [['John', '25'], ['Jane', '30']],
            'layout': 'double-column-layout',
            'column_widths': [50, 50],
            'header_spans': [[{'colspan': 1, 'rowspan': 1, 'text': 'Name'},
                               {'colspan': 1, 'rowspan': 1, 'text': 'Age'}]],
            'row_spans': [[{'colspan': 1, 'rowspan': 1, 'text': 'John'},
                           {'colspan': 1, 'rowspan': 1, 'text': '25'}],
                          [{'colspan': 1, 'rowspan': 1, 'text': 'Jane'},
                           {'colspan': 1, 'rowspan': 1, 'text': '30'}]],
            'foot': [],
        }
        result = xml_pipe.extract_table_data(table_wrap)
        self.assertEqual([expected], result)

    def test_extract_table_data_no_label_no_title(self):
        xml_str = """
            <table-wrap>
                <table>
                    <thead>
                        <tr><th>Col1</th></tr>
                    </thead>
                    <tbody>
                        <tr><td>Data1</td></tr>
                    </tbody>
                </table>
            </table-wrap>
        """
        table_wrap = etree.fromstring(xml_str)
        expected = {
            'label': '',
            'title': '',
            'headers': [['Col1']],
            'rows': [['Data1']],
            'layout': 'double-column-layout',
            'column_widths': [50],
            'header_spans': [[{'colspan': 1, 'rowspan': 1, 'text': 'Col1'}]],
            'row_spans': [[{'colspan': 1, 'rowspan': 1, 'text': 'Data1'}]],
            'foot': [],
        }
        result = xml_pipe.extract_table_data(table_wrap)
        self.assertEqual([expected], result)

    def test_extract_table_data_empty_table(self):
        xml_str = """
            <table-wrap>
                <label>Table 2</label>
                <title>Empty Table</title>
                <table>
                    <thead></thead>
                    <tbody></tbody>
                </table>
            </table-wrap>
        """
        table_wrap = etree.fromstring(xml_str)
        expected = {
            'label': 'Table 2',
            'title': 'Empty Table',
            'headers': [],
            'rows': [],
            'layout': 'double-column-layout',
            'column_widths': [],
            'header_spans': [],
            'row_spans': [],
            'foot': [],
        }
        result = xml_pipe.extract_table_data(table_wrap)
        self.assertEqual([expected], result)

    def test_extract_table_data_no_table(self):
        xml_str = """
            <table-wrap>
                <label>Table 3</label>
                <title>Missing Table</title>
            </table-wrap>
        """
        table_wrap = etree.fromstring(xml_str)
        expected = {
            'label': 'Table 3',
            'title': 'Missing Table',
            'headers': [],
            'rows': [],
            'layout': 'double-column-layout',
            'column_widths': [],
            'header_spans': [],
            'row_spans': [],
            'foot': [],
        }
        result = xml_pipe.extract_table_data(table_wrap)
        self.assertEqual([expected], result)

    def test_extract_table_data_multiple_header_rows(self):
        xml_str = """
            <table-wrap>
                <table>
                    <thead>
                        <tr><th>Col1</th><th>Col2</th></tr>
                        <tr><th>SubCol1</th><th>SubCol2</th></tr>
                    </thead>
                    <tbody>
                        <tr><td>Val1</td><td>Val2</td></tr>
                    </tbody>
                </table>
            </table-wrap>
        """
        table_wrap = etree.fromstring(xml_str)
        expected = {
            'label': '',
            'title': '',
            'headers': [['Col1', 'Col2'], ['SubCol1', 'SubCol2']],
            'rows': [['Val1', 'Val2']],
            'layout': 'double-column-layout',
            'column_widths': [50, 50],
            'header_spans': [[{'colspan': 1, 'rowspan': 1, 'text': 'Col1'},
                               {'colspan': 1, 'rowspan': 1, 'text': 'Col2'}],
                              [{'colspan': 1, 'rowspan': 1, 'text': 'SubCol1'},
                               {'colspan': 1, 'rowspan': 1, 'text': 'SubCol2'}]],
            'row_spans': [[{'colspan': 1, 'rowspan': 1, 'text': 'Val1'},
                           {'colspan': 1, 'rowspan': 1, 'text': 'Val2'}]],
            'foot': [],
        }
        result = xml_pipe.extract_table_data(table_wrap)
        self.assertEqual([expected], result)

    def test_extract_table_data_foot_with_fn_and_attrib(self):
        xml_str = """
            <table-wrap>
                <table>
                    <tbody><tr><td>Data</td></tr></tbody>
                </table>
                <table-wrap-foot>
                    <fn id="TFN1"><p>Source: Authors.</p></fn>
                    <fn id="TFN2"><p>* p &lt; 0.05.</p></fn>
                    <attrib>Adapted from Smith (2020).</attrib>
                </table-wrap-foot>
            </table-wrap>
        """
        table_wrap = etree.fromstring(xml_str)
        result = xml_pipe.extract_table_data(table_wrap)
        self.assertEqual(
            result[0]['foot'],
            ['Source: Authors.', '* p < 0.05.', 'Adapted from Smith (2020).'],
        )

    def test_extract_table_data_foot_with_direct_p_elements(self):
        # Regression: table-wrap-foot can hold <p> children directly, not
        # only wrapped in <fn> or <attrib> (e.g. Table 2 of a2.xml fixture).
        xml_str = """
            <table-wrap>
                <table>
                    <tbody><tr><td>Data</td></tr></tbody>
                </table>
                <table-wrap-foot>
                    <p>Legenda: Outros (BR): 87 titulos.</p>
                    <p>Fonte: Dados da pesquisa (Florianopolis, 2022).</p>
                </table-wrap-foot>
            </table-wrap>
        """
        table_wrap = etree.fromstring(xml_str)
        result = xml_pipe.extract_table_data(table_wrap)
        self.assertEqual(
            result[0]['foot'],
            ['Legenda: Outros (BR): 87 titulos.', 'Fonte: Dados da pesquisa (Florianopolis, 2022).'],
        )

    def test_extract_table_data_foot_preserves_mixed_document_order(self):
        xml_str = """
            <table-wrap>
                <table>
                    <tbody><tr><td>Data</td></tr></tbody>
                </table>
                <table-wrap-foot>
                    <p>Legenda solta.</p>
                    <fn id="TFN1"><p>Nota de rodape.</p></fn>
                    <attrib>Fonte: Autores.</attrib>
                </table-wrap-foot>
            </table-wrap>
        """
        table_wrap = etree.fromstring(xml_str)
        result = xml_pipe.extract_table_data(table_wrap)
        self.assertEqual(
            result[0]['foot'],
            ['Legenda solta.', 'Nota de rodape.', 'Fonte: Autores.'],
        )

    def test_extract_table_data_no_foot_defaults_to_empty_list(self):
        xml_str = "<table-wrap><table><tbody><tr><td>Data</td></tr></tbody></table></table-wrap>"
        table_wrap = etree.fromstring(xml_str)
        result = xml_pipe.extract_table_data(table_wrap)
        self.assertEqual(result[0]['foot'], [])

    def test_determine_table_layout_single_long_cell_forces_single_column(self):
        long_text = "x" * 500
        xml_str = f"<table-wrap><table><tbody><tr><td>{long_text}</td></tr></tbody></table></table-wrap>"
        table_wrap = etree.fromstring(xml_str)
        self.assertEqual(
            xml_pipe.determine_table_layout(table_wrap),
            pdf_enum.SINGLE_COLUMN_PAGE_LABEL,
        )

    def test_determine_table_layout_moderately_long_cell_stays_double_column(self):
        moderate_text = "x" * 150
        xml_str = f"<table-wrap><table><tbody><tr><td>{moderate_text}</td></tr></tbody></table></table-wrap>"
        table_wrap = etree.fromstring(xml_str)
        self.assertEqual(
            xml_pipe.determine_table_layout(table_wrap),
            pdf_enum.DOUBLE_COLUMN_PAGE_LABEL,
        )

    def test_extract_table_data_override_layout_wins_over_heuristic(self):
        xml_str = "<table-wrap><table><tbody><tr><td>Data</td></tr></tbody></table></table-wrap>"
        table_wrap = etree.fromstring(xml_str)
        result = xml_pipe.extract_table_data(
            table_wrap, override_layout=pdf_enum.SINGLE_COLUMN_PAGE_LABEL
        )
        self.assertEqual(result[0]['layout'], pdf_enum.SINGLE_COLUMN_PAGE_LABEL)

    def test_extract_table_data_invalid_override_falls_back_to_heuristic(self):
        xml_str = "<table-wrap><table><tbody><tr><td>Data</td></tr></tbody></table></table-wrap>"
        table_wrap = etree.fromstring(xml_str)
        result = xml_pipe.extract_table_data(table_wrap, override_layout='not-a-real-layout')
        self.assertEqual(result[0]['layout'], pdf_enum.DOUBLE_COLUMN_PAGE_LABEL)


class TestExtractTableDataMultipleTables(unittest.TestCase):
    """
    Regression tests for issue #1368: a <table-wrap> can hold more than one
    <table> (real corpus pattern - side-by-side "Program A"/"Program B"
    panels sharing one caption). table_wrap.find('.//table') used to grab
    only the first, silently dropping every table past it. extract_table_data
    now returns one dict per <table>, the shared label/title only on the
    first and any <table-wrap-foot> notes only on the last.
    """

    def _two_table_xml(self):
        return """
            <table-wrap>
                <label>Table 1</label>
                <title>Two programs</title>
                <table>
                    <thead><tr><th>Program A</th></tr></thead>
                    <tbody><tr><td>A1</td></tr></tbody>
                </table>
                <table>
                    <thead><tr><th>Program B</th></tr></thead>
                    <tbody><tr><td>B1</td></tr></tbody>
                </table>
                <table-wrap-foot>
                    <p>Shared note.</p>
                </table-wrap-foot>
            </table-wrap>
        """

    def test_returns_one_dict_per_table(self):
        table_wrap = etree.fromstring(self._two_table_xml())
        result = xml_pipe.extract_table_data(table_wrap)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['rows'], [['A1']])
        self.assertEqual(result[1]['rows'], [['B1']])

    def test_caption_only_on_first_table(self):
        table_wrap = etree.fromstring(self._two_table_xml())
        result = xml_pipe.extract_table_data(table_wrap)
        self.assertEqual(result[0]['label'], 'Table 1')
        self.assertEqual(result[0]['title'], 'Two programs')
        self.assertEqual(result[1]['label'], '')
        self.assertEqual(result[1]['title'], '')

    def test_foot_only_on_last_table(self):
        table_wrap = etree.fromstring(self._two_table_xml())
        result = xml_pipe.extract_table_data(table_wrap)
        self.assertEqual(result[0]['foot'], [])
        self.assertEqual(result[1]['foot'], ['Shared note.'])

    def test_layout_considers_every_table_not_just_the_first(self):
        # First table has 1 narrow column; second has 5, past the
        # single-column-layout threshold. The wrap-level layout decision
        # must reflect the widest table, not just the first.
        xml_str = """
            <table-wrap>
                <table><tbody><tr><td>A</td></tr></tbody></table>
                <table><tbody><tr>
                    <td>1</td><td>2</td><td>3</td><td>4</td><td>5</td>
                </tr></tbody></table>
            </table-wrap>
        """
        table_wrap = etree.fromstring(xml_str)
        result = xml_pipe.extract_table_data(table_wrap)
        self.assertEqual(result[0]['layout'], pdf_enum.SINGLE_COLUMN_PAGE_LABEL)
        self.assertEqual(result[1]['layout'], pdf_enum.SINGLE_COLUMN_PAGE_LABEL)


class TestExtractTableDataBareRows(unittest.TestCase):
    """
    Regression tests for issue #1368: a <table> can have <tr> as direct
    children with no <thead>/<tbody> wrapper at all (valid JATS/NLM shape -
    real corpus example: a structured radiology-report table). Both were
    previously required for any content to be read, so the whole table body
    was silently dropped.
    """

    def test_bare_tr_rows_are_read_as_body(self):
        xml_str = """
            <table-wrap>
                <table>
                    <tr><td>PULMOES:</td><td>Sem alteracoes.</td></tr>
                    <tr><td>BACO:</td><td>Sem alteracoes.</td></tr>
                </table>
            </table-wrap>
        """
        table_wrap = etree.fromstring(xml_str)
        result = xml_pipe.extract_table_data(table_wrap)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['headers'], [])
        self.assertEqual(
            result[0]['rows'],
            [['PULMOES:', 'Sem alteracoes.'], ['BACO:', 'Sem alteracoes.']],
        )

    def test_bare_tr_accepts_th_cells_without_a_thead_wrapper(self):
        xml_str = """
            <table-wrap>
                <table>
                    <tr><th>Predictor</th><th>Value</th></tr>
                    <tr><td>Age</td><td>37</td></tr>
                </table>
            </table-wrap>
        """
        table_wrap = etree.fromstring(xml_str)
        result = xml_pipe.extract_table_data(table_wrap)
        self.assertEqual(
            result[0]['rows'],
            [['Predictor', 'Value'], ['Age', '37']],
        )


class TestExtractBodyDataTableDedup(unittest.TestCase):
    """
    Regression tests for a table-wrap inside a nested <sec> being collected
    once, by its closest section ancestor, at its natural position. It was
    previously collected by every ancestor section too (findall('.//sec')
    yields each nested <sec> as its own entry, and each searches all
    table-wrap descendants), duplicating the table and hoisting one copy of
    it into a block ahead of the subsection's own text.
    """

    def test_table_in_nested_subsection_is_not_duplicated(self):
        xml = etree.fromstring(
            '<article>'
            '<sec>'
            '<title>Parent</title>'
            '<sec>'
            '<title>Child</title>'
            '<table-wrap id="t1">'
            '<label>Table 1</label>'
            '<table><tbody><tr><td>Data</td></tr></tbody></table>'
            '</table-wrap>'
            '</sec>'
            '</sec>'
            '</article>'
        )
        result = xml_pipe.extract_body_data(xml)
        all_tables = [t for sec in result for t in sec['tables']]
        self.assertEqual(len(all_tables), 1)

    def test_table_in_nested_subsection_stays_at_its_natural_position(self):
        # Not just deduplicated: the surviving copy must belong to the Child
        # section (its actual position in the text), not get hoisted up to
        # Parent (a table-id-keyed dedup that kept "whichever copy is seen
        # first" would have kept the wrong one, since findall('.//sec') visits
        # Parent before Child).
        xml = etree.fromstring(
            '<article>'
            '<sec>'
            '<title>Parent</title>'
            '<sec>'
            '<title>Child</title>'
            '<table-wrap id="t1">'
            '<label>Table 1</label>'
            '<table><tbody><tr><td>Data</td></tr></tbody></table>'
            '</table-wrap>'
            '</sec>'
            '</sec>'
            '</article>'
        )
        result = xml_pipe.extract_body_data(xml)
        parent_sec = next(s for s in result if s['title'] == 'Parent')
        child_sec = next(s for s in result if s['title'] == 'Child')
        self.assertEqual(len(parent_sec['tables']), 0)
        self.assertEqual(len(child_sec['tables']), 1)

    def test_tables_without_id_still_avoid_duplication_and_hoisting(self):
        # The fix doesn't rely on @id at all (unlike the figure dedup it was
        # modeled after): it's based on each table-wrap's closest <sec>
        # ancestor, so this must work the same with or without an id.
        xml = etree.fromstring(
            '<article>'
            '<sec>'
            '<title>Parent</title>'
            '<sec>'
            '<title>Child</title>'
            '<table-wrap>'
            '<label>Table 1</label>'
            '<table><tbody><tr><td>Data</td></tr></tbody></table>'
            '</table-wrap>'
            '</sec>'
            '</sec>'
            '</article>'
        )
        result = xml_pipe.extract_body_data(xml)
        all_tables = [t for sec in result for t in sec['tables']]
        self.assertEqual(len(all_tables), 1)
        parent_sec = next(s for s in result if s['title'] == 'Parent')
        self.assertEqual(len(parent_sec['tables']), 0)

    def test_table_directly_in_parent_is_not_skipped(self):
        # A table that's a direct child of Parent (not inside Child) must
        # still be collected by Parent, the fix must not over-correct into
        # skipping every table above the deepest section.
        xml = etree.fromstring(
            '<article>'
            '<sec>'
            '<title>Parent</title>'
            '<table-wrap id="t1"><label>Table 1</label>'
            '<table><tbody><tr><td>Data</td></tr></tbody></table></table-wrap>'
            '<sec>'
            '<title>Child</title>'
            '<table-wrap id="t2"><label>Table 2</label>'
            '<table><tbody><tr><td>Data</td></tr></tbody></table></table-wrap>'
            '</sec>'
            '</sec>'
            '</article>'
        )
        result = xml_pipe.extract_body_data(xml)
        parent_sec = next(s for s in result if s['title'] == 'Parent')
        child_sec = next(s for s in result if s['title'] == 'Child')
        self.assertEqual([t['label'] for t in parent_sec['tables']], ['Table 1'])
        self.assertEqual([t['label'] for t in child_sec['tables']], ['Table 2'])

    def test_table_layout_overrides_reach_extract_table_data(self):
        xml = etree.fromstring(
            '<article>'
            '<sec>'
            '<title>Parent</title>'
            '<table-wrap id="t1">'
            '<label>Table 1</label>'
            '<table><tbody><tr><td>Data</td></tr></tbody></table>'
            '</table-wrap>'
            '</sec>'
            '</article>'
        )
        result = xml_pipe.extract_body_data(
            xml, table_layout_overrides={'t1': pdf_enum.SINGLE_COLUMN_PAGE_LABEL}
        )
        self.assertEqual(result[0]['tables'][0]['layout'], pdf_enum.SINGLE_COLUMN_PAGE_LABEL)


class TestExtractTransAbstractData(unittest.TestCase):

    def test_extract_trans_abstract_data_basic(self):
        xml = etree.fromstring(
            '<article>'
            '<trans-abstract xml:lang="en">'
            '<title>English Abstract</title>'
            '<p>First paragraph.</p>'
            '<p>Second paragraph.</p>'
            '</trans-abstract>'
            '</article>'
        )
        expected = [
            {
                'lang': 'en',
                'title': 'English Abstract',
                'content': 'First paragraph. Second paragraph.'
            }
        ]
        result = xml_pipe.extract_trans_abstract_data(xml)
        self.assertEqual(result, expected)

    def test_extract_trans_abstract_data_multiple_abstracts(self):
        xml = etree.fromstring(
            '<article>'
            '<trans-abstract xml:lang="en">'
            '<title>English Abstract</title>'
            '<p>First paragraph.</p>'
            '</trans-abstract>'
            '<trans-abstract xml:lang="es">'
            '<title>Resumen en Español</title>'
            '<p>Primer párrafo.</p>'
            '</trans-abstract>'
            '</article>'
        )
        expected = [
            {
                'lang': 'en',
                'title': 'English Abstract',
                'content': 'First paragraph.'
            },
            {
                'lang': 'es',
                'title': 'Resumen en Español',
                'content': 'Primer párrafo.'
            }
        ]
        result = xml_pipe.extract_trans_abstract_data(xml)
        self.assertEqual(result, expected)

    def test_extract_trans_abstract_data_no_abstracts(self):
        xml = etree.fromstring('<article></article>')
        expected = []
        result = xml_pipe.extract_trans_abstract_data(xml)
        self.assertEqual(result, expected)

    def test_extract_trans_abstract_data_empty_abstract(self):
        xml = etree.fromstring(
            '<article>'
            '<trans-abstract xml:lang="en">'
            '<title></title>'
            '<p></p>'
            '</trans-abstract>'
            '</article>'
        )
        expected = [
            {
                'lang': 'en',
                'title': '',
                'content': ''
            }
        ]
        result = xml_pipe.extract_trans_abstract_data(xml)
        self.assertEqual(result, expected)

    def test_extract_trans_abstract_data_custom_namespace(self):
        xml = etree.fromstring(
            '<article xmlns:custom="http://custom.namespace">'
            '<trans-abstract custom:lang="fr">'
            '<title>Résumé en Français</title>'
            '<p>Premier paragraphe.</p>'
            '</trans-abstract>'
            '</article>'
        )
        expected = [
            {
                'lang': 'fr',
                'title': 'Résumé en Français',
                'content': 'Premier paragraphe.'
            }
        ]
        result = xml_pipe.extract_trans_abstract_data(
            xml,
            namespaces={'xml': 'http://custom.namespace'}
        )
        self.assertEqual(result, expected)

    def test_extract_trans_abstract_data_paragraph_with_inline_markup(self):
        """
        Regression test for issue #1321: a <p> containing inline markup
        (e.g. <italic>) used to be truncated at p.text, dropping the italic
        text and everything after it in that paragraph.
        """
        xml = etree.fromstring(
            '<article>'
            '<trans-abstract xml:lang="pt">'
            '<title>Resumo</title>'
            '<p>Efeito do milho (<italic>Zea mays</italic> L.) na produtividade.</p>'
            '</trans-abstract>'
            '</article>'
        )
        expected = [
            {
                'lang': 'pt',
                'title': 'Resumo',
                'content': 'Efeito do milho (Zea mays L.) na produtividade.'
            }
        ]
        result = xml_pipe.extract_trans_abstract_data(xml)
        self.assertEqual(result, expected)

    def test_extract_trans_abstract_data_title_with_inline_markup(self):
        xml = etree.fromstring(
            '<article>'
            '<trans-abstract xml:lang="pt">'
            '<title>Resumo<italic>*</italic></title>'
            '<p>Texto.</p>'
            '</trans-abstract>'
            '</article>'
        )
        result = xml_pipe.extract_trans_abstract_data(xml)
        self.assertEqual(result[0]['title'], 'Resumo*')

    def test_extract_trans_abstract_data_structured_with_sections(self):
        # Regression for issue #1332: same bug as extract_abstract_data,
        # a structured trans-abstract's <p> nested in <sec> was invisible
        # to a plain findall('p'), so the translated abstract's content
        # came out empty (e.g. a10.xml's RESUMO in the real test corpus).
        xml = etree.fromstring(
            '<article>'
            '<trans-abstract xml:lang="pt">'
            '<title>Resumo</title>'
            '<sec><title>Contexto:</title><p>Texto de contexto.</p></sec>'
            '<sec><title>Métodos:</title><p>Texto de métodos.</p></sec>'
            '</trans-abstract>'
            '</article>'
        )
        expected = [
            {
                'lang': 'pt',
                'title': 'Resumo',
                'content': 'Contexto: Texto de contexto. Métodos: Texto de métodos.',
            }
        ]
        result = xml_pipe.extract_trans_abstract_data(xml)
        self.assertEqual(result, expected)


class TestExtractFigureData(unittest.TestCase):
    """Tests for extract_figure_data's graphic href resolution, including
    the ranking logic used when a figure only offers <alternatives>."""

    def test_direct_graphic_child_is_used_as_is(self):
        xml = etree.fromstring(
            '<fig xmlns:xlink="http://www.w3.org/1999/xlink" id="F1">'
            '<label>Figure 1</label>'
            '<graphic xlink:href="figure1.jpg"/>'
            '</fig>'
        )
        result = xml_pipe.extract_figure_data(xml)
        self.assertEqual(result['href'], 'figure1.jpg')

    def test_alternatives_prefers_scielo_web_over_raw_tif(self):
        xml = etree.fromstring(
            '<fig xmlns:xlink="http://www.w3.org/1999/xlink" id="F1">'
            '<label>Graph 1</label>'
            '<alternatives>'
            '<graphic xlink:href="raw.tif"/>'
            '<graphic xlink:href="web.png" specific-use="scielo-web"/>'
            '<graphic xlink:href="thumb.jpg" specific-use="scielo-web" content-type="scielo-267x140"/>'
            '</alternatives>'
            '</fig>'
        )
        result = xml_pipe.extract_figure_data(xml)
        self.assertEqual(result['href'], 'web.png')

    def test_alternatives_prefers_scielo_web_over_raw_graphic(self):
        # Isolates specific-use as the deciding factor: raw.png would win on
        # extension ranking alone (png before jpg), so picking web.jpg here
        # can only be explained by specific-use="scielo-web" taking priority.
        xml = etree.fromstring(
            '<fig xmlns:xlink="http://www.w3.org/1999/xlink" id="F1">'
            '<label>Graph 1</label>'
            '<alternatives>'
            '<graphic xlink:href="raw.png"/>'
            '<graphic xlink:href="web.jpg" specific-use="scielo-web"/>'
            '<graphic xlink:href="thumb.jpg" specific-use="scielo-web" content-type="scielo-267x140"/>'
            '</alternatives>'
            '</fig>'
        )
        result = xml_pipe.extract_figure_data(xml)
        self.assertEqual(result['href'], 'web.jpg')

    def test_alternatives_falls_back_to_tif_when_no_better_option(self):
        xml = etree.fromstring(
            '<fig xmlns:xlink="http://www.w3.org/1999/xlink" id="F1">'
            '<label>Graph 1</label>'
            '<alternatives>'
            '<graphic xlink:href="raw.tif"/>'
            '</alternatives>'
            '</fig>'
        )
        result = xml_pipe.extract_figure_data(xml)
        self.assertEqual(result['href'], 'raw.tif')
