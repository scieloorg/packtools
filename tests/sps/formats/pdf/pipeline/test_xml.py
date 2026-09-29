import unittest

from lxml import etree

from packtools.sps.formats.pdf.pipeline import xml as xml_pipe
from packtools.sps.formats.pdf import enum as pdf_enum


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
        result = xml_pipe.extract_acknowledgment_data(xml_tree)
        self.assertEqual(result["title"], '')
        self.assertEqual(
            _paragraph_texts(result),
            ["First acknowledgment paragraph", "Second acknowledgment paragraph"],
        )

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
        result = xml_pipe.extract_acknowledgment_data(xml_tree)
        self.assertEqual(result["title"], "Acknowledgements Section")
        self.assertEqual(
            _paragraph_texts(result),
            [
                "Thank you to all contributors",
                "Special thanks to funding agencies",
                "Additional acknowledgments",
            ],
        )

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
        result = xml_pipe.extract_acknowledgment_data(xml_tree)
        self.assertEqual(result["title"], "Acknowledgments")
        self.assertEqual(_paragraph_texts(result), ["Nested paragraph 1", "Nested paragraph 2"])

    def test_extract_acknowledgment_data_keeps_text_after_inline_markup(self):
        # sant/v16n2/2238-3875-sant-16-02-e250090 (#1374): o texto era cortado no 1o <italic>
        xml_tree = etree.fromstring(
            """
            <article>
                <ack>
                    <p>aos pareceristas ad hoc da <italic>Sociologia &amp; Antropologia</italic>, pela avaliação cuidadosa; ao comitê editorial da <italic>Sociologia &amp; Antropologia</italic>, pela acolhida do manuscrito.</p>
                </ack>
            </article>
            """
        )
        result = xml_pipe.extract_acknowledgment_data(xml_tree)
        self.assertEqual(
            _paragraph_texts(result),
            [
                "aos pareceristas ad hoc da Sociologia & Antropologia, pela avaliação cuidadosa; "
                "ao comitê editorial da Sociologia & Antropologia, pela acolhida do manuscrito."
            ],
        )
        italic = [seg["text"] for seg in result["paragraphs"][0] if seg["italic"]]
        self.assertEqual(italic, ["Sociologia & Antropologia", "Sociologia & Antropologia"])

    def test_extract_acknowledgment_data_paragraph_starting_with_markup(self):
        # antes, paragraph.text era None quando o <p> começava por um elemento
        xml_tree = etree.fromstring(
            "<article><ack><p><bold>CNPq</bold> e CAPES.</p></ack></article>"
        )
        result = xml_pipe.extract_acknowledgment_data(xml_tree)
        self.assertEqual(_paragraph_texts(result), ["CNPq e CAPES."])

    def test_extract_acknowledgment_data_title_with_markup(self):
        xml_tree = etree.fromstring(
            "<article><ack><title>Agradecimentos à <italic>FAPESP</italic> e ao CNPq</title></ack></article>"
        )
        result = xml_pipe.extract_acknowledgment_data(xml_tree)
        self.assertEqual(result["title"], "Agradecimentos à FAPESP e ao CNPq")


def _paragraph_texts(ack_data):
    return ["".join(seg["text"] for seg in segments) for segments in ack_data["paragraphs"]]


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

    def test_extract_body_data_excludes_supplementary_material_section_without_sec_type(self):
        # Regression, PR #1384 review: matching by @sec-type="supplementary-
        # material" missed real corpus articles whose <sec> has no @sec-type
        # at all (e.g. jped/v102n1), or a different value (e.g. "supplementary",
        # jbchs/v37nspe1). The exclusion is now structural: a <sec> with a
        # <supplementary-material> descendant and no <sec> of its own, not by
        # its @sec-type string.
        xml = etree.fromstring(
            '<article>'
            '<body>'
            '<sec><title>Introduction</title><p>Body text.</p></sec>'
            '</body>'
            '<back>'
            '<sec><title>Supplementary materials</title>'
            '<supplementary-material id="suppl1"><label>Suppl. 1</label></supplementary-material>'
            '</sec>'
            '</back>'
            '</article>'
        )
        result = xml_pipe.extract_body_data(xml)
        self.assertEqual(1, len(result))
        self.assertEqual('Introduction', result[0]['title'])

    def test_extract_body_data_keeps_real_section_that_merely_references_supplementary_material(self):
        # Regression, PR #1384 review: the structural exclusion above must
        # not swallow a real body section (e.g. "Discussion") that has its
        # own subsections, one of them a dedicated leaf "Supplementary
        # Data" sub-section - reproduced against the real corpus sample
        # abb/v40/1677-941X-abb-40-e20250182.xml, where <supplementary-
        # material> sits inside its own <sec>, a sibling of "Floristic
        # composition" and the other real subsections, all nested inside
        # <sec sec-type="discussion">. The "no <sec> of its own" guard
        # excludes only the dedicated leaf subsection, not its ancestor
        # or its siblings.
        xml = etree.fromstring(
            '<article>'
            '<body>'
            '<sec sec-type="discussion"><title>Discussion</title>'
            '<sec><title>Floristic composition</title><p>Real content.</p></sec>'
            '<sec><title>Supplementary Data</title>'
            '<supplementary-material id="suppl1"><label>Table S1</label></supplementary-material>'
            '</sec>'
            '</sec>'
            '</body>'
            '</article>'
        )
        result = xml_pipe.extract_body_data(xml)
        titles = [s['title'] for s in result]
        self.assertIn('Discussion', titles)
        self.assertIn('Floristic composition', titles)
        self.assertNotIn('Supplementary Data', titles)

    def test_extract_body_data_excludes_app_group_sections(self):
        # Regression for issue #1372, real corpus sample
        # bjrs/v14n1/2319-0612-bjrs-v14n1-09-e3014.xml (a37.xml): the
        # appendix subsections "Zone 1/2/3" leaked into the body, and are
        # now rendered by supplementary_material.extract_data instead.
        xml = etree.fromstring(
            '<article>'
            '<body>'
            '<sec><title>Results</title><p>Body text.</p></sec>'
            '</body>'
            '<back>'
            '<app-group>'
            '<app>'
            '<sec><title>Zone 1</title>'
            '<table-wrap id="t1"><label>Table A1</label>'
            '<table><tbody><tr><td>Data</td></tr></tbody></table>'
            '</table-wrap>'
            '</sec>'
            '</app>'
            '</app-group>'
            '</back>'
            '</article>'
        )
        result = xml_pipe.extract_body_data(xml)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['title'], 'Results')
        self.assertEqual(sum(len(s['tables']) for s in result), 0)

    def test_extract_body_data_includes_disp_formula_as_sibling_of_p(self):
        # Regression for issue #1347/#1352: <disp-formula> is often a direct
        # sibling of <p>, not nested inside one - a plain findall('p') never
        # visits it, so the formula silently vanished from the output.
        # Since Phase 1 (#1352), a formula with MathML gets a real OMML
        # conversion (a single 'formula' segment) instead of flattened text.
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
        result = xml_pipe.extract_body_data(xml)
        paragraphs = result[0]['paragraphs']
        self.assertEqual(paragraphs[0], _plain_para('See the formula below.'))
        self.assertEqual(paragraphs[2], _plain_para('Where Y is the result.'))
        self.assertEqual(len(paragraphs[1]), 1)
        formula_segment = paragraphs[1][0]
        self.assertEqual(formula_segment['type'], 'formula')
        self.assertTrue(formula_segment['display'])
        self.assertEqual(etree.QName(formula_segment['omml']).localname, 'oMath')
        omml_text = ''.join(formula_segment['omml'].itertext())
        self.assertIn('Y', omml_text)
        self.assertIn('1', omml_text)
        self.assertEqual(result[0]['level'], 1)
        self.assertEqual(result[0]['title'], 'Section 1')
        self.assertEqual(result[0]['tables'], [])
        self.assertEqual(result[0]['figures'], [])

    def test_extract_body_data_converts_inline_formula_mixed_with_running_text(self):
        # Fase 2 de #1347 (issue #1353): <inline-formula> no meio de uma
        # frase vira um segmento 'formula' real (OMML), em vez de ser
        # achatada em texto ambíguo pela recursão padrão de
        # get_segments_from_node.
        xml = etree.fromstring(
            '<article xmlns:mml="http://www.w3.org/1998/Math/MathML">'
            '<sec><title>Section 1</title>'
            '<p>where <inline-formula id="e1"><mml:math><mml:mi>sigma</mml:mi></mml:math>'
            '</inline-formula> is the dispersion coefficient.</p>'
            '</sec></article>'
        )
        result = xml_pipe.extract_body_data(xml)
        segments = result[0]['paragraphs'][0]
        self.assertEqual(len(segments), 3)
        self.assertEqual(segments[0], {
            'type': 'text', 'text': 'where ', 'italic': False, 'bold': False,
            'superscript': False, 'subscript': False,
        })
        self.assertEqual(segments[1]['type'], 'formula')
        self.assertEqual(etree.QName(segments[1]['omml']).localname, 'oMath')
        self.assertEqual(segments[2], {
            'type': 'text', 'text': ' is the dispersion coefficient.', 'italic': False, 'bold': False,
            'superscript': False, 'subscript': False,
        })

    def test_extract_body_data_converts_multiple_inline_formulas_in_same_paragraph(self):
        xml = etree.fromstring(
            '<article xmlns:mml="http://www.w3.org/1998/Math/MathML">'
            '<sec><title>Section 1</title>'
            '<p>If <inline-formula id="e1"><mml:math><mml:mi>x</mml:mi></mml:math></inline-formula>'
            ' and <inline-formula id="e2"><mml:math><mml:mi>y</mml:mi></mml:math></inline-formula>'
            ' hold.</p>'
            '</sec></article>'
        )
        result = xml_pipe.extract_body_data(xml)
        segments = result[0]['paragraphs'][0]
        formula_segments = [seg for seg in segments if seg['type'] == 'formula']
        self.assertEqual(len(formula_segments), 2)
        self.assertEqual([seg['type'] for seg in segments], ['text', 'formula', 'text', 'formula', 'text'])

    def test_extract_body_data_falls_back_to_flattened_text_when_inline_formula_has_no_mathml(self):
        # Sem <mml:math> descendente, _inline_formula_segment retorna None e
        # o texto cai no achatamento de sempre - nunca descartado.
        xml = etree.fromstring(
            '<article xmlns:mml="http://www.w3.org/1998/Math/MathML">'
            '<sec><title>Section 1</title>'
            '<p>where <inline-formula id="e1">x</inline-formula> is undefined.</p>'
            '</sec></article>'
        )
        result = xml_pipe.extract_body_data(xml)
        segments = result[0]['paragraphs'][0]
        self.assertEqual(segments, _plain_para('where x is undefined.'))

    def test_extract_body_data_converts_inline_formula_inside_list_item(self):
        xml = etree.fromstring(
            '<article xmlns:mml="http://www.w3.org/1998/Math/MathML">'
            '<sec><title>Section 1</title>'
            '<list list-type="bullet">'
            '<list-item><p>where <inline-formula id="e1"><mml:math><mml:mi>x</mml:mi></mml:math>'
            '</inline-formula> is the mean.</p></list-item>'
            '</list>'
            '</sec></article>'
        )
        result = xml_pipe.extract_body_data(xml)
        segments = result[0]['paragraphs'][0]
        self.assertEqual([seg['type'] for seg in segments], ['text', 'text', 'formula', 'text'])

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
        # by its own <disp-formula><label>, not by the list. Since Phase 1
        # (#1352), the trailing <disp-formula> in the <p> gets a real OMML
        # conversion plus its own <label> as a trailing text segment,
        # instead of everything flattened into one text blob.
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
        result = xml_pipe.extract_body_data(xml)
        paragraphs = result[0]['paragraphs']
        self.assertEqual(len(paragraphs), 1)
        segments = paragraphs[0]
        self.assertEqual(segments[0], _plain_para('Total biomass:')[0])
        self.assertEqual(segments[1]['type'], 'formula')
        self.assertTrue(segments[1]['display'])
        self.assertEqual(etree.QName(segments[1]['omml']).localname, 'oMath')
        self.assertEqual(segments[2], _plain_para(' (3)')[0])

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

    def test_extract_body_data_excludes_sub_article_sections(self):
        # Regression for issue #1372, reproduced against the real corpus
        # sample regepe/2965-1506-regepe-15-e2659.xml: a <sub-article> (a
        # full translation of the article) has its own <sec> tree, which an
        # unscoped './/sec' search picked up and duplicated the entire
        # article's body in a second language.
        xml = etree.fromstring(
            '<article>'
            '<body>'
            '<sec><title>Introdução</title><p>Texto em português.</p></sec>'
            '</body>'
            '<sub-article article-type="translation" xml:lang="en">'
            '<body>'
            '<sec><title>Introduction</title><p>English text.</p></sec>'
            '</body>'
            '</sub-article>'
            '</article>'
        )
        result = xml_pipe.extract_body_data(xml)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['title'], 'Introdução')

    def test_extract_body_data_includes_reviewer_report_and_reply_sections(self):
        # Regression for issue #1372's review: not(ancestor::sub-article)
        # was too broad and also dropped <sub-article article-type=
        # "reviewer-report"/"reply">, which are real, published body
        # content, not a duplicate like a translation. Reproduced against
        # the real corpus sample mioc/v121/1678-8060-mioc-121-e250154.xml.
        xml = etree.fromstring(
            '<article>'
            '<body>'
            '<sec><title>Results</title><p>Body text.</p></sec>'
            '</body>'
            '<sub-article article-type="reviewer-report" xml:lang="en">'
            '<body>'
            '<sec><title>Reviewer #1</title><p>Comments.</p></sec>'
            '</body>'
            '</sub-article>'
            '<sub-article article-type="reply" xml:lang="en">'
            '<body>'
            '<sec><title>Authors\' response</title><p>Reply text.</p></sec>'
            '</body>'
            '</sub-article>'
            '</article>'
        )
        result = xml_pipe.extract_body_data(xml)
        self.assertEqual(len(result), 3)
        self.assertEqual([s['title'] for s in result], ['Results', 'Reviewer #1', "Authors' response"])


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
