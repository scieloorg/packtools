"""
Corpo e back do artigo (seções, parágrafos, fórmulas, listas, tabelas,
figuras, agradecimentos e referências).

Migra de tests/sps/formats/old_pdf/pipeline/test_xml.py as classes
TestExtractAcknowledgmentData, TestExtractBodyData, TestExtractReferencesData,
TestExtractTableData, TestExtractTableDataMultipleTables,
TestExtractTableDataBareRows, TestExtractBodyDataTableDedup e
TestExtractFigureData. As funções internas do old_pdf (extract_body_data,
extract_table_data...) são verificadas pelo comportamento equivalente: blocos
de extract_article/flow, layout de layout.placement e, quando o teste antigo
era sobre a página, o DOCX gerado.
"""

import unittest

from lxml import etree

from packtools.sps.formats.pdf.config import page as page_config
from packtools.sps.formats.pdf.assets import Assets
from packtools.sps.formats.pdf.extract.runs import runs_text
from packtools.sps.formats.pdf.layout.placement import place

from tests.sps.formats.pdf.helpers import NS, article, article_xml, docx, extract, summary, texts, xml

SINGLE, DOUBLE = page_config.SINGLE_COLUMN, page_config.DOUBLE_COLUMN


def main(body='', back='', **kwargs):
    """Blocos de ``main`` de um artigo mínimo."""
    return article(article_xml(body=body, back=back, **kwargs))['main']


def headings(blocks):
    """(nível, texto) de cada título."""
    return [(b['level'], runs_text(b['runs'])) for b in blocks if b['type'] == 'heading']


def tables(blocks):
    """Blocos de tabela."""
    return [b for b in blocks if b['type'] == 'table']


def table(wrap):
    """Blocos de tabela de um ``<table-wrap>`` (dentro de uma seção)."""
    return tables(extract(xml(f'<sec>{wrap}</sec>')))


def cells(block):
    """Texto das células, linha a linha."""
    rows = [[] for _ in range(block['nrows'])]
    for cell in block['cells']:
        rows[cell['row']].append(runs_text(cell['runs']))
    return rows


def foot(block):
    """Texto de cada nota da tabela."""
    return [runs_text(runs) for runs in block['foot']]


def placed(blocks, **kwargs):
    """Blocos com o layout decidido por layout.placement.place."""
    return place(blocks, page_config.load_page(), Assets(), **kwargs)


def omml(run):
    """True se o run é uma fórmula OMML."""
    return 'omml' in run and etree.QName(run['omml']).localname == 'oMath'


class AcknowledgmentTest(unittest.TestCase):
    def test_no_ack_gives_no_blocks(self):
        """old: TestExtractAcknowledgmentData.test_extract_acknowledgment_data_empty_xml

        diferença intencional: sem <ack> não sai nada (antes, título vazio e lista vazia).
        """
        self.assertEqual(main(body='<p>x</p>'), main(body='<p>x</p>', back='<ack/>'))

    def test_ack_title_and_paragraphs(self):
        """old: TestExtractAcknowledgmentData.test_extract_acknowledgment_data_with_title_no_paragraphs,
        test_extract_acknowledgment_data_with_paragraphs_no_title,
        test_extract_acknowledgment_data_complete,
        test_extract_acknowledgment_data_nested_paragraphs
        """
        cases = [
            ('<title>Acknowledgments</title>', [('heading', 'Acknowledgments')]),
            ('<p>First</p><p>Second</p>', [('body', 'First'), ('body', 'Second')]),
            ('<title>Ack Section</title><p>A</p><p>B</p><p>C</p>',
             [('heading', 'Ack Section'), ('body', 'A'), ('body', 'B'), ('body', 'C')]),
            # <sec> sem título dentro do <ack>: os parágrafos seguem sob o título do <ack>
            ('<title>Acknowledgments</title><sec><p>Nested 1</p><p>Nested 2</p></sec>',
             [('heading', 'Acknowledgments'), ('body', 'Nested 1'), ('body', 'Nested 2')]),
        ]
        for ack, expected in cases:
            with self.subTest(ack=ack):
                self.assertEqual(summary(main(back=f'<ack>{ack}</ack>')), expected)

    def test_ack_keeps_text_after_and_around_inline_markup(self):
        """old: TestExtractAcknowledgmentData.test_extract_acknowledgment_data_keeps_text_after_inline_markup,
        test_extract_acknowledgment_data_paragraph_starting_with_markup,
        test_extract_acknowledgment_data_title_with_markup
        """
        (p,) = main(back='<ack><p>aos pareceristas da <italic>S &amp; A</italic>, pela avaliação; '
                         'ao comitê da <italic>S &amp; A</italic>, pela acolhida.</p></ack>')
        self.assertEqual(runs_text(p['runs']),
                         'aos pareceristas da S & A, pela avaliação; ao comitê da S & A, pela acolhida.')
        self.assertEqual([r['text'] for r in p['runs'] if r.get('italic')], ['S & A', 'S & A'])

        (p,) = main(back='<ack><p><bold>CNPq</bold> e CAPES.</p></ack>')
        self.assertEqual(p['runs'], [{'text': 'CNPq', 'bold': True}, {'text': ' e CAPES.'}])

        (heading,) = main(back='<ack><title>Agradecimentos à <italic>FAPESP</italic> e ao CNPq</title></ack>')
        self.assertEqual(runs_text(heading['runs']), 'Agradecimentos à FAPESP e ao CNPq')
        self.assertTrue(heading['runs'][1]['italic'])


class SectionTest(unittest.TestCase):
    def test_section_title_and_paragraphs(self):
        """old: TestExtractBodyData.test_extract_body_data_basic

        diferença intencional: a <sec> de primeiro nível é título nível 2
        sempre (antes, 1 sem <body> e 2 com <body>).
        """
        blocks = main(body='<sec><title>Section 1</title><p>Paragraph 1</p><p>Paragraph 2</p></sec>')
        self.assertEqual(summary(blocks), [('heading', 'Section 1'), ('body', 'Paragraph 1'), ('body', 'Paragraph 2')])
        self.assertEqual(headings(blocks), [(2, 'Section 1')])

    def test_nested_sections_go_one_level_down(self):
        """old: TestExtractBodyData.test_extract_body_data_with_nested_sections"""
        blocks = main(body='<sec><title>Section 1</title><p>Paragraph 1</p>'
                           '<sec><title>Subsection 1.1</title><p>Paragraph 1.1</p></sec></sec>')
        self.assertEqual(headings(blocks), [(2, 'Section 1'), (3, 'Subsection 1.1')])
        self.assertEqual(texts(blocks), ['Section 1', 'Paragraph 1', 'Subsection 1.1', 'Paragraph 1.1'])

    def test_section_with_table_and_table_reference(self):
        """old: TestExtractBodyData.test_extract_body_data_with_tables,
        test_extract_body_data_with_table_references
        """
        wrap = ('<table-wrap><label>Table 1</label><title>Sample Table</title><table>'
                '<thead><tr><th>Header</th></tr></thead><tbody><tr><td>Data</td></tr></tbody></table></table-wrap>')
        for p, expected in (('Paragraph 1', 'Paragraph 1'),
                            ('Paragraph with <xref ref-type="table">Table 1</xref>', 'Paragraph with Table 1')):
            with self.subTest(p=p):
                blocks = placed(main(body=f'<sec><title>Section 1</title><p>{p}</p>{wrap}</sec>'))
                self.assertEqual(summary(blocks), [('heading', 'Section 1'), ('body', expected)])
                (block,) = tables(blocks)
                self.assertIs(block, blocks[-1])
                self.assertEqual(runs_text(block['caption']), 'Table 1 Sample Table')
                self.assertEqual(cells(block), [['Header'], ['Data']])
                self.assertEqual([c['header'] for c in block['cells']], [True, False])
                self.assertEqual((block['layout'], block['foot']), (DOUBLE, []))
                self.assertEqual(block['column_widths'], [block['width']])

    def test_structured_abstract_sections_are_not_repeated_in_body(self):
        """old: TestExtractBodyData.test_extract_body_data_excludes_abstract_and_trans_abstract_sections"""
        result = article(article_xml(
            front='<abstract><sec><title>Background:</title><p>Abstract text.</p></sec></abstract>'
                  '<trans-abstract xml:lang="en"><sec><title>Contexto:</title><p>Texto.</p></sec></trans-abstract>',
            body='<sec><title>Introduction</title><p>Body text.</p></sec>'))
        self.assertEqual(texts(result['main']), ['Introduction', 'Body text.'])
        self.assertIn('Background: Abstract text.', texts(result['front']))

    def test_supplementary_material_section_goes_to_annex(self):
        """old: TestExtractBodyData.test_extract_body_data_excludes_supplementary_material_section,
        test_extract_body_data_excludes_supplementary_material_section_without_sec_type
        """
        for attr in (' sec-type="supplementary-material"', ' sec-type="supplementary"', ''):
            with self.subTest(attr=attr):
                result = article(article_xml(
                    body='<sec><title>Introduction</title><p>Body text.</p></sec>',
                    back=f'<sec{attr}><title>Supplementary Material</title>'
                         '<supplementary-material id="s1"><label>Suppl. 1</label></supplementary-material></sec>'))
                self.assertEqual(texts(result['main']), ['Introduction', 'Body text.'])
                self.assertEqual(texts(result['annex']), ['Supplementary Material', 'Suppl. 1'])

    def test_section_with_subsections_mentioning_supplementary_material_stays_in_body(self):
        """old: TestExtractBodyData.test_extract_body_data_keeps_real_section_that_merely_references_supplementary_material
        (parte: a seção pai e as irmãs ficam no corpo)
        """
        blocks = main(body=SUPPLEMENTARY_SUBSECTION)
        self.assertIn((2, 'Discussion'), headings(blocks))
        self.assertIn((3, 'Floristic composition'), headings(blocks))
        self.assertIn('Real content.', texts(blocks))

    def test_nested_supplementary_material_leaf_section_goes_to_annex(self):
        """old: TestExtractBodyData.test_extract_body_data_keeps_real_section_that_merely_references_supplementary_material
        (parte: a subseção folha "Supplementary Data" sai do corpo e vai para os anexos)
        """
        result = article(article_xml(body=SUPPLEMENTARY_SUBSECTION))
        self.assertNotIn('Supplementary Data', texts(result['main']))
        self.assertEqual(texts(result['annex']), ['Supplementary Data', 'Table S1'])

    def test_appendix_goes_to_annex_with_its_tables(self):
        """
        old: TestExtractBodyData.test_extract_body_data_excludes_app_group_sections

        O grupo e o <app> não têm título (só a <sec> de dentro): o grupo
        recebe o título padrão no idioma do documento (pt).
        """
        result = article(article_xml(
            body='<sec><title>Results</title><p>Body text.</p></sec>',
            back='<app-group><app><sec><title>Zone 1</title><table-wrap id="t1"><label>Table A1</label>'
                 '<table><tbody><tr><td>Data</td></tr></tbody></table></table-wrap></sec></app></app-group>'))
        self.assertEqual(texts(result['main']), ['Results', 'Body text.'])
        self.assertEqual(tables(result['main']), [])
        self.assertEqual(texts(result['annex']), ['Apêndice', 'Zone 1'])
        self.assertEqual(len(tables(result['annex'])), 1)

    def test_body_without_sec_keeps_its_paragraphs(self):
        """old: TestExtractBodyData.test_extract_body_data_falls_back_to_body_when_no_sec_exists"""
        self.assertEqual(summary(main(body='<p>Paragraph 1</p><p>Paragraph 2</p>')),
                         [('body', 'Paragraph 1'), ('body', 'Paragraph 2')])

    def test_body_without_sec_keeps_table_and_figure_in_place(self):
        """old: TestExtractBodyData.test_extract_body_data_falls_back_to_body_with_table_and_figure

        diferença intencional: figura e tabela ficam na ordem do documento; a
        figura sem <graphic> sai só como legenda.
        """
        blocks = main(body='<p>Intro paragraph.</p>'
                           '<p>Figure 1<fig id="f1"><label>Figure 1</label></fig></p>'
                           '<p>Table 1<table-wrap id="t1"><label>Table 1</label><caption><title>Sample Table</title>'
                           '</caption><table><thead><tr><th>Header</th></tr></thead>'
                           '<tbody><tr><td>Data</td></tr></tbody></table></table-wrap></p>')
        self.assertEqual([b.get('role', b['type']) for b in blocks],
                         ['body', 'body', 'figure_caption', 'body', 'table'])
        self.assertEqual(headings(blocks), [])
        self.assertEqual(runs_text(blocks[2]['runs']), 'Figure 1')
        self.assertEqual(runs_text(blocks[4]['caption']), 'Table 1. Sample Table')

    def test_single_section_is_not_duplicated(self):
        """old: TestExtractBodyData.test_extract_body_data_does_not_fall_back_when_sec_exists"""
        self.assertEqual(summary(main(body='<sec><title>Introduction</title><p>Body text.</p></sec>')),
                         [('heading', 'Introduction'), ('body', 'Body text.')])

    def test_body_without_sec_and_back_sec_both_kept(self):
        """old: TestExtractBodyData.test_extract_body_data_falls_back_even_when_an_unrelated_sec_exists_outside_body

        diferença intencional: o <label> da seção vira o título (antes, título None).
        """
        blocks = main(body='<p>Body paragraph.</p>',
                      back='<sec sec-type="data-availability"><label>Data availability</label>'
                           '<p>Data statement.</p></sec>')
        self.assertEqual(summary(blocks), [('body', 'Body paragraph.'), ('heading', 'Data availability'),
                                           ('body', 'Data statement.')])

    def test_translation_sub_article_is_its_own_document(self):
        """old: TestExtractBodyData.test_extract_body_data_excludes_sub_article_sections

        diferença intencional: a tradução não some, é o documento do seu idioma.
        """
        root = article_xml(body='<sec><title>Introdução</title><p>Texto em português.</p></sec>',
                           extra='<sub-article article-type="translation" xml:lang="en"><body>'
                                 '<sec><title>Introduction</title><p>English text.</p></sec></body></sub-article>')
        self.assertEqual(texts(article(root)['main']), ['Introdução', 'Texto em português.'])
        self.assertEqual(texts(article(root, 'en')['main']), ['Introduction', 'English text.'])

    def test_reviewer_report_and_reply_are_kept(self):
        """old: TestExtractBodyData.test_extract_body_data_includes_reviewer_report_and_reply_sections"""
        blocks = main(body='<sec><title>Results</title><p>Body text.</p></sec>',
                      extra='<sub-article article-type="reviewer-report" xml:lang="en"><body>'
                            '<sec><title>Reviewer #1</title><p>Comments.</p></sec></body></sub-article>'
                            '<sub-article article-type="reply" xml:lang="en"><body>'
                            "<sec><title>Authors' response</title><p>Reply text.</p></sec></body></sub-article>")
        self.assertEqual([t for _, t in headings(blocks)], ['Results', 'Reviewer #1', "Authors' response"])
        self.assertIn('Comments.', texts(blocks))
        self.assertIn('Reply text.', texts(blocks))


SUPPLEMENTARY_SUBSECTION = (
    '<sec sec-type="discussion"><title>Discussion</title>'
    '<sec><title>Floristic composition</title><p>Real content.</p></sec>'
    '<sec><title>Supplementary Data</title>'
    '<supplementary-material id="suppl1"><label>Table S1</label></supplementary-material></sec></sec>'
)


class CategoryTest(unittest.TestCase):
    """Os testes de extract_category estavam (por engano) em TestExtractBodyData."""

    def meta(self, categories):
        return article(article_xml(front=f'<article-categories>{categories}</article-categories>'))['meta']

    def test_category_is_heading_subject_text(self):
        """old: TestExtractBodyData.test_extract_category_returns_text,
        test_extract_category_returns_element,
        test_extract_category_with_empty_subject

        diferença intencional: meta é um dict plano de textos; não há versão que devolve o elemento.
        """
        cases = [('Original Article', 'Original Article'), ('', '')]
        for subject, expected in cases:
            with self.subTest(subject=subject):
                meta = self.meta(f'<subj-group subj-group-type="heading"><subject>{subject}</subject></subj-group>')
                self.assertEqual(meta['category'], expected)

    def test_missing_category_is_empty_text(self):
        """old: TestExtractBodyData.test_extract_category_missing_category_raises_attribute_error,
        test_extract_category_empty_xml_raises_attribute_error

        diferença intencional: sem categoria, texto vazio (antes, AttributeError).
        """
        self.assertEqual(self.meta('<subj-group><subject>Other Content</subject></subj-group>')['category'], '')
        self.assertEqual(article(xml('<article/>'))['meta']['category'], '')


class FormulaTest(unittest.TestCase):
    def test_display_formula_sibling_of_p_becomes_formula_block(self):
        """old: TestExtractBodyData.test_extract_body_data_includes_disp_formula_as_sibling_of_p"""
        blocks = main(body='<sec><title>Section 1</title><p>See the formula below.</p>'
                           '<disp-formula id="e01"><mml:math><mml:mi>Y</mml:mi><mml:mo>=</mml:mo>'
                           '<mml:mn>1</mml:mn></mml:math></disp-formula><p>Where Y is the result.</p></sec>')
        self.assertEqual([b['type'] for b in blocks], ['heading', 'paragraph', 'formula', 'paragraph'])
        self.assertEqual(texts([blocks[1], blocks[3]]), ['See the formula below.', 'Where Y is the result.'])
        bookmark, formula = blocks[2]['runs']
        self.assertEqual(bookmark, {'bookmark': 'e01'})
        self.assertTrue(omml(formula))
        omml_text = ''.join(formula['omml'].itertext())
        self.assertIn('Y', omml_text)
        self.assertIn('1', omml_text)

    def test_inline_formulas_become_omml_runs_amid_text(self):
        """old: TestExtractBodyData.test_extract_body_data_converts_inline_formula_mixed_with_running_text,
        test_extract_body_data_converts_multiple_inline_formulas_in_same_paragraph,
        test_extract_body_data_converts_inline_formula_inside_list_item
        """
        def math(x):
            return f'<inline-formula><mml:math><mml:mi>{x}</mml:mi></mml:math></inline-formula>'

        cases = [
            (f'<p>where {math("sigma")} is the dispersion coefficient.</p>',
             ['where ', 'F', ' is the dispersion coefficient.']),
            (f'<p>If {math("x")} and {math("y")} hold.</p>', ['If ', 'F', ' and ', 'F', ' hold.']),
            (f'<list list-type="bullet"><list-item><p>where {math("x")} is the mean.</p></list-item></list>',
             ['• where ', 'F', ' is the mean.']),
        ]
        for content, expected in cases:
            with self.subTest(content=content):
                (p,) = main(body=content)
                self.assertEqual(['F' if omml(r) else r['text'] for r in p['runs']], expected)

    def test_inline_formula_without_mathml_keeps_its_text(self):
        """old: TestExtractBodyData.test_extract_body_data_falls_back_to_flattened_text_when_inline_formula_has_no_mathml"""
        (p,) = main(body='<p>where <inline-formula id="e1">x</inline-formula> is undefined.</p>')
        self.assertEqual(texts([p]), ['where x is undefined.'])

    def test_graphic_display_formula_becomes_figure_in_place(self):
        """old: TestExtractBodyData.test_extract_body_data_includes_graphic_disp_formula_as_figure,
        test_extract_body_data_includes_labeled_graphic_disp_formula_as_figure

        diferença intencional: a figura fica entre os parágrafos (ordem do
        documento) e o texto alternativo, sem <alt-text>, é o endereço.
        """
        for label, caption in (('', ''), ('<label>(1)</label>', '(1)')):
            with self.subTest(label=label):
                blocks = main(body=f'<sec><title>Section 1</title><p>See the formula below.</p>'
                                   f'<disp-formula id="e01">{label}<graphic xlink:href="e01.tif"/></disp-formula>'
                                   '<p>Where Y is the result.</p></sec>')
                self.assertEqual([b['type'] for b in blocks], ['heading', 'paragraph', 'figure', 'paragraph'])
                figure = blocks[2]
                self.assertEqual((figure['href'], figure['alt'], figure['anchor']), ('e01.tif', 'e01.tif', 'e01'))
                self.assertEqual(runs_text(figure['caption']), caption)


class ListTest(unittest.TestCase):
    def test_list_markers_by_type(self):
        """old: TestExtractBodyData.test_extract_body_data_includes_bullet_list_items,
        test_extract_body_data_includes_ordered_list_items_with_numbering
        """
        cases = [
            ('bullet', ['T1 - Control', 'T2 - Treated'], ['• T1 - Control', '• T2 - Treated']),
            ('order', ['First', 'Second', 'Third'], ['1. First', '2. Second', '3. Third']),
        ]
        for list_type, items, expected in cases:
            with self.subTest(list_type=list_type):
                list_items = ''.join(f'<list-item><p>{i}</p></list-item>' for i in items)
                blocks = main(body=f'<sec><title>Section 1</title><p>The treatments included:</p>'
                                   f'<list list-type="{list_type}">{list_items}</list></sec>')
                self.assertEqual(texts(blocks), ['Section 1', 'The treatments included:'] + expected)

    def test_simple_list_has_no_marker_and_keeps_display_formula_with_label(self):
        """old: TestExtractBodyData.test_extract_body_data_simple_list_has_no_marker

        diferença intencional: a fórmula em destaque dentro do <p> divide o
        parágrafo e vira bloco próprio, com o rótulo depois.
        """
        p, formula = main(body='<list list-type="simple"><list-item><p>Total biomass:'
                               '<disp-formula id="e03"><mml:math><mml:mi>Y</mml:mi><mml:mo>=</mml:mo>'
                               '<mml:mn>1</mml:mn></mml:math><label>(3)</label></disp-formula></p></list-item></list>')
        self.assertEqual(p['runs'], [{'text': 'Total biomass:'}])
        self.assertEqual(formula['type'], 'formula')
        self.assertTrue(omml(formula['runs'][1]))
        self.assertEqual(formula['runs'][-1], {'text': ' (3)'})

    def test_list_nested_inside_p_is_kept(self):
        """old: TestExtractBodyData.test_extract_body_data_includes_list_nested_inside_p"""
        blocks = main(body='<sec><title>Section 1</title><p>The following propositions were formulated:</p>'
                           '<p><list list-type="simple"><list-item><p>Proposition P1: text one.</p></list-item>'
                           '<list-item><p>Proposition P2: text two.</p></list-item></list></p></sec>')
        self.assertEqual(summary(blocks), [
            ('heading', 'Section 1'),
            ('body', 'The following propositions were formulated:'),
            ('body', 'Proposition P1: text one.'),
            ('body', 'Proposition P2: text two.'),
        ])


class InlineTextTest(unittest.TestCase):
    def test_citations_have_no_stray_space_around_parentheses(self):
        """old: TestExtractBodyData.test_paragraph_citations_have_no_stray_space_around_parentheses"""
        (p,) = main(body='<p>Pressure is increasing (<xref ref-type="bibr" rid="B1">Lang and Barling, 2012</xref>'
                         '; <xref ref-type="bibr" rid="B2">Ripple et al., 2019</xref>) worldwide.</p>')
        self.assertEqual(texts([p]), ['Pressure is increasing (Lang and Barling, 2012; Ripple et al., 2019) worldwide.'])

    def test_embedded_fig_splits_paragraph_without_raw_whitespace(self):
        """old: TestExtractBodyData.test_embedded_fig_tail_whitespace_is_collapsed_not_left_raw

        diferença intencional: a figura fica no lugar e divide o parágrafo
        (antes, ia para o fim da seção e o texto era emendado).
        """
        blocks = main(body='<p>See the figure below\n<fig id="f1"><label>Figure 1</label></fig>\n            '
                           'for details.</p>')
        self.assertEqual(summary(blocks), [('body', 'See the figure below'), ('figure_caption', 'Figure 1'),
                                           ('body', 'for details.')])

    def test_inline_formatting_is_preserved(self):
        """old: TestExtractBodyData.test_extract_body_data_preserves_inline_formatting"""
        (p,) = main(body='<p>The species <italic>Genus species</italic> was observed'
                         '<sup>1</sup> in <bold>high</bold> numbers.</p>')
        self.assertEqual(p['runs'], [
            {'text': 'The species '},
            {'text': 'Genus species', 'italic': True},
            {'text': ' was observed'},
            {'text': '1', 'superscript': True},
            {'text': ' in '},
            {'text': 'high', 'bold': True},
            {'text': ' numbers.'},
        ])


class ReferencesTest(unittest.TestCase):
    def test_no_ref_list_gives_no_references_section(self):
        """old: TestExtractReferencesData.test_extract_references_data_empty_xml

        diferença intencional: sem <ref-list> não sai título "References" (o
        old_pdf sempre imprimia o título, mesmo vazio).
        """
        self.assertEqual(summary(main(body='<p>x</p>')), [('body', 'x')])
        self.assertNotIn('References', texts(main(body='<p>x</p>', back='<ack><p>a</p></ack>')))

    def test_empty_ref_list_gives_only_the_default_title(self):
        """old: TestExtractReferencesData.test_extract_references_data_with_empty_ref_list"""
        self.assertEqual(summary(extract(xml('<back><ref-list/></back>'))), [('heading', 'References')])

    def test_one_paragraph_per_mixed_citation(self):
        """old: TestExtractReferencesData.test_extract_references_data_with_multiple_references

        diferença intencional: toda referência termina com ponto.
        """
        blocks = extract(xml('<back><ref-list><ref><mixed-citation>Reference 1</mixed-citation></ref>'
                             '<ref><mixed-citation>Reference 2</mixed-citation></ref></ref-list></back>'))
        self.assertEqual(summary(blocks), [('heading', 'References'), ('reference', 'Reference 1.'),
                                           ('reference', 'Reference 2.')])

    def test_ref_list_in_article_back(self):
        """old: TestExtractReferencesData.test_extract_references_data_with_nested_ref_list"""
        blocks = main(body='<p>x</p>', back='<ref-list><ref><mixed-citation>Nested Reference</mixed-citation>'
                                            '</ref></ref-list>', lang='en')
        self.assertEqual(summary(blocks)[1:], [('heading', 'References'), ('reference', 'Nested Reference.')])

    def test_ref_without_mixed_citation_keeps_its_text(self):
        """old: TestExtractReferencesData.test_extract_references_data_without_mixed_citation

        diferença intencional: a <ref> sem <mixed-citation> não é descartada;
        sai o texto dos demais filhos (sem perda de conteúdo).
        """
        blocks = extract(xml('<back><ref-list><ref><element-citation>Citation without mixed'
                             '</element-citation></ref></ref-list></back>'))
        self.assertEqual(summary(blocks)[1:], [('reference', 'Citation without mixed.')])


class TableTest(unittest.TestCase):
    def test_complete_table(self):
        """old: TestExtractTableData.test_extract_table_data_complete,
        test_extract_table_data_no_label_no_title,
        test_extract_table_data_multiple_header_rows

        diferença intencional: <title> solto no <table-wrap> (fora de
        <caption>) entra na legenda depois do rótulo, sem ponto.
        """
        thead = '<thead><tr><th>Name</th><th>Age</th></tr></thead>'
        tbody = '<tbody><tr><td>John</td><td>25</td></tr><tr><td>Jane</td><td>30</td></tr></tbody>'
        cases = [
            ('<label>Table 1</label><title>Sample Data</title>', thead, 'Table 1 Sample Data'),
            ('<label>Table 1</label><caption><title>Sample Data</title></caption>', thead, 'Table 1. Sample Data'),
            ('', thead, ''),
            ('', '<thead><tr><th>Name</th><th>Age</th></tr><tr><th>N</th><th>A</th></tr></thead>', ''),
        ]
        for caption, head, expected_caption in cases:
            with self.subTest(caption=caption, head=head):
                (block,) = placed(table(f'<table-wrap>{caption}<table>{head}{tbody}</table></table-wrap>'))
                self.assertEqual(runs_text(block['caption']), expected_caption)
                if caption:
                    self.assertEqual(block['caption'][0], {'text': 'Table 1', 'bold': True})
                nhead = head.count('<tr>')
                self.assertEqual(cells(block)[nhead:], [['John', '25'], ['Jane', '30']])
                self.assertEqual([c['header'] for c in block['cells']], [True] * 2 * nhead + [False] * 4)
                self.assertTrue(all(c['rowspan'] == c['colspan'] == 1 for c in block['cells']))
                self.assertEqual((block['ncols'], block['foot'], block['layout']), (2, [], DOUBLE))
                # pesos iguais (mínimo de 50pt): colunas de mesma largura
                self.assertEqual(len(set(block['column_widths'])), 1)

    def test_empty_table(self):
        """old: TestExtractTableData.test_extract_table_data_empty_table"""
        (block,) = placed(table('<table-wrap><label>Table 2</label><caption><title>Empty Table</title></caption>'
                                '<table><thead/><tbody/></table></table-wrap>'))
        self.assertEqual((block['nrows'], block['ncols'], block['cells'], block['foot']), (0, 0, [], []))
        self.assertEqual(runs_text(block['caption']), 'Table 2. Empty Table')
        self.assertEqual((block['layout'], block['column_widths']), (DOUBLE, []))

    def test_table_wrap_without_table_keeps_caption(self):
        """old: TestExtractTableData.test_extract_table_data_no_table

        diferença intencional: sem <table> nem imagem, sai só a legenda (não uma tabela vazia).
        """
        blocks = extract(xml('<sec><table-wrap><label>Table 3</label><caption><title>Missing Table</title>'
                             '</caption></table-wrap></sec>'))
        self.assertEqual(summary(blocks), [('table_caption', 'Table 3. Missing Table')])

    def test_table_foot_keeps_every_item_in_document_order(self):
        """old: TestExtractTableData.test_extract_table_data_foot_with_fn_and_attrib,
        test_extract_table_data_foot_with_direct_p_elements,
        test_extract_table_data_foot_preserves_mixed_document_order,
        test_extract_table_data_no_foot_defaults_to_empty_list
        """
        cases = [
            ('<table-wrap-foot><fn id="TFN1"><p>Source: Authors.</p></fn><fn id="TFN2"><p>* p &lt; 0.05.</p></fn>'
             '<attrib>Adapted from Smith (2020).</attrib></table-wrap-foot>',
             ['Source: Authors.', '* p < 0.05.', 'Adapted from Smith (2020).']),
            ('<table-wrap-foot><p>Legenda: Outros (BR): 87 titulos.</p>'
             '<p>Fonte: Dados da pesquisa (Florianopolis, 2022).</p></table-wrap-foot>',
             ['Legenda: Outros (BR): 87 titulos.', 'Fonte: Dados da pesquisa (Florianopolis, 2022).']),
            ('<table-wrap-foot><p>Legenda solta.</p><fn id="TFN1"><p>Nota de rodape.</p></fn>'
             '<attrib>Fonte: Autores.</attrib></table-wrap-foot>',
             ['Legenda solta.', 'Nota de rodape.', 'Fonte: Autores.']),
            ('', []),
        ]
        for wrap_foot, expected in cases:
            with self.subTest(expected=expected):
                (block,) = table(f'<table-wrap><table><tbody><tr><td>Data</td></tr></tbody></table>{wrap_foot}'
                                 '</table-wrap>')
                self.assertEqual(foot(block), expected)

    def test_layout_by_longest_cell(self):
        """old: TestExtractTableData.test_determine_table_layout_single_long_cell_forces_single_column,
        test_determine_table_layout_moderately_long_cell_stays_double_column
        """
        for length, expected in ((500, SINGLE), (150, DOUBLE)):
            with self.subTest(length=length):
                (block,) = placed(table(f'<table-wrap><table><tbody><tr><td>{"x" * length}</td></tr></tbody>'
                                        '</table></table-wrap>'))
                self.assertEqual(block['layout'], expected)

    def test_layout_override_by_id(self):
        """old: TestExtractTableData.test_extract_table_data_override_layout_wins_over_heuristic,
        test_extract_table_data_invalid_override_falls_back_to_heuristic

        diferença intencional: o override é por @id do <table-wrap> (layout.placement.place).
        """
        for override, expected in ((SINGLE, SINGLE), ('not-a-real-layout', DOUBLE)):
            with self.subTest(override=override):
                (block,) = placed(table('<table-wrap id="t1"><table><tbody><tr><td>Data</td></tr></tbody></table>'
                                        '</table-wrap>'), overrides={'t1': override})
                self.assertEqual(block['layout'], expected)


TWO_TABLES = (
    '<table-wrap id="t1"><label>Table 1</label><caption><title>Two programs</title></caption>'
    '<table><thead><tr><th>Program A</th></tr></thead><tbody><tr><td>A1</td></tr></tbody></table>'
    '<table><thead><tr><th>Program B</th></tr></thead><tbody><tr><td>B1</td></tr></tbody></table>'
    '<table-wrap-foot><p>Shared note.</p></table-wrap-foot></table-wrap>'
)


class MultipleTablesTest(unittest.TestCase):
    def test_one_block_per_table(self):
        """old: TestExtractTableDataMultipleTables.test_returns_one_dict_per_table"""
        first, second = table(TWO_TABLES)
        self.assertEqual((first['panel'], second['panel']), (0, 1))
        self.assertEqual(cells(first), [['Program A'], ['A1']])
        self.assertEqual(cells(second), [['Program B'], ['B1']])

    def test_caption_only_on_first_and_foot_only_on_last(self):
        """old: TestExtractTableDataMultipleTables.test_caption_only_on_first_table,
        test_foot_only_on_last_table
        """
        first, second = table(TWO_TABLES)
        self.assertEqual((runs_text(first['caption']), second['caption']), ('Table 1. Two programs', []))
        self.assertEqual((first['foot'], foot(second)), ([], ['Shared note.']))

    def test_layout_considers_every_table(self):
        """old: TestExtractTableDataMultipleTables.test_layout_considers_every_table_not_just_the_first"""
        blocks = placed(table('<table-wrap><table><tbody><tr><td>A</td></tr></tbody></table>'
                              '<table><tbody><tr><td>1</td><td>2</td><td>3</td><td>4</td><td>5</td></tr></tbody>'
                              '</table></table-wrap>'))
        self.assertEqual([b['layout'] for b in blocks], [SINGLE, SINGLE])


class BareRowsTest(unittest.TestCase):
    def test_bare_tr_rows_are_read(self):
        """old: TestExtractTableDataBareRows.test_bare_tr_rows_are_read_as_body"""
        (block,) = table('<table-wrap><table><tr><td>PULMOES:</td><td>Sem alteracoes.</td></tr>'
                         '<tr><td>BACO:</td><td>Sem alteracoes.</td></tr></table></table-wrap>')
        self.assertEqual(cells(block), [['PULMOES:', 'Sem alteracoes.'], ['BACO:', 'Sem alteracoes.']])
        self.assertFalse(any(c['header'] for c in block['cells']))

    def test_bare_tr_with_th_cells(self):
        """old: TestExtractTableDataBareRows.test_bare_tr_accepts_th_cells_without_a_thead_wrapper

        diferença intencional: <th> fora de <thead> é marcada como cabeçalho
        (antes, lida como linha comum); o conteúdo é o mesmo.
        """
        (block,) = table('<table-wrap><table><tr><th>Predictor</th><th>Value</th></tr>'
                         '<tr><td>Age</td><td>37</td></tr></table></table-wrap>')
        self.assertEqual(cells(block), [['Predictor', 'Value'], ['Age', '37']])
        self.assertEqual([c['header'] for c in block['cells']], [True, True, False, False])


def nested_table(parent_table=''):
    """Seção Parent (com tabela opcional) contendo Child com uma tabela."""
    return (f'<sec><title>Parent</title>{parent_table}<sec><title>Child</title><p>Child text.</p>'
            '<table-wrap{id}><label>Table 2</label><table><tbody><tr><td>Data</td></tr></tbody></table>'
            '</table-wrap></sec></sec>')


class TableDedupTest(unittest.TestCase):
    def test_table_in_nested_section_appears_once_at_its_position(self):
        """old: TestExtractBodyDataTableDedup.test_table_in_nested_subsection_is_not_duplicated,
        test_table_in_nested_subsection_stays_at_its_natural_position,
        test_tables_without_id_still_avoid_duplication_and_hoisting
        """
        for table_id in (' id="t2"', ''):
            with self.subTest(table_id=table_id):
                blocks = main(body=nested_table().format(id=table_id))
                self.assertEqual([b.get('role', b['type']) for b in blocks],
                                 ['heading', 'heading', 'body', 'table'])
                self.assertEqual(texts(blocks), ['Parent', 'Child', 'Child text.'])

    def test_table_directly_in_parent_stays_in_parent(self):
        """old: TestExtractBodyDataTableDedup.test_table_directly_in_parent_is_not_skipped"""
        blocks = main(body=nested_table('<table-wrap id="t1"><label>Table 1</label><table><tbody><tr><td>Data</td>'
                                        '</tr></tbody></table></table-wrap>').format(id=' id="t2"'))
        order = [runs_text(b['caption']) if b['type'] == 'table' else runs_text(b['runs']) for b in blocks]
        self.assertEqual(order, ['Parent', 'Table 1', 'Child', 'Child text.', 'Table 2'])

    def test_table_layout_overrides_reach_the_document(self):
        """old: TestExtractBodyDataTableDedup.test_table_layout_overrides_reach_extract_table_data"""
        root = article_xml(body='<sec><title>Parent</title><p>x</p><table-wrap id="t1"><label>Table 1</label>'
                                '<table><tbody><tr><td>Data</td></tr></tbody></table></table-wrap><p>y</p></sec>')
        (block,) = tables(placed(article(root)['main'], overrides={'t1': SINGLE}))
        self.assertEqual(block['layout'], SINGLE)

        def columns(**data):
            return [s._sectPr.xpath('./w:cols/@w:num') for s in docx(root, **data).sections]

        # sem override: tudo na seção de 2 colunas; com: a tabela abre uma seção de 1 coluna
        self.assertEqual(columns(), [[], ['2']])
        self.assertEqual(columns(table_layout_overrides={'t1': SINGLE}), [[], ['2'], ['1'], ['2']])


class FigureTest(unittest.TestCase):
    def test_graphic_choice(self):
        """old: TestExtractFigureData.test_direct_graphic_child_is_used_as_is,
        test_alternatives_prefers_scielo_web_over_raw_tif,
        test_alternatives_prefers_scielo_web_over_raw_graphic,
        test_alternatives_falls_back_to_tif_when_no_better_option
        """
        thumb = '<graphic xlink:href="thumb.jpg" specific-use="scielo-web" content-type="scielo-267x140"/>'
        cases = [
            ('<graphic xlink:href="figure1.jpg"/>', 'figure1.jpg'),
            (f'<alternatives><graphic xlink:href="raw.tif"/>'
             f'<graphic xlink:href="web.png" specific-use="scielo-web"/>{thumb}</alternatives>', 'web.png'),
            (f'<alternatives><graphic xlink:href="raw.png"/>'
             f'<graphic xlink:href="web.jpg" specific-use="scielo-web"/>{thumb}</alternatives>', 'web.jpg'),
            ('<alternatives><graphic xlink:href="raw.tif"/></alternatives>', 'raw.tif'),
        ]
        for content, expected in cases:
            with self.subTest(expected=expected):
                (figure,) = extract(xml(f'<sec {NS}><fig id="F1"><label>Figure 1</label>{content}</fig></sec>'))
                self.assertEqual((figure['type'], figure['href']), ('figure', expected))
                self.assertEqual(runs_text(figure['caption']), 'Figure 1')


if __name__ == '__main__':
    unittest.main()
