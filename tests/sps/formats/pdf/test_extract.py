import unittest

from lxml import etree

from packtools.sps.formats.pdf.extract.article import extract_article
from packtools.sps.formats.pdf.extract.context import context
from packtools.sps.formats.pdf.extract.flow import flow
from packtools.sps.formats.pdf.extract.inline import inlines
from packtools.sps.formats.pdf.extract.languages import document_for, languages
from packtools.sps.formats.pdf.extract.runs import normalize, runs_text
from packtools.sps.formats.pdf.extract import table as table_extract

NS = 'xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML"'


def xml(text):
    return etree.fromstring(text)


def texts(blocks):
    return [runs_text(b['runs']) for b in blocks if 'runs' in b]


def summary(blocks):
    """(papel ou tipo, texto) de cada bloco com runs: comparação plana nos testes."""
    return [(b.get('role', b['type']), runs_text(b['runs'])) for b in blocks if 'runs' in b]


def extract(node):
    """Blocos de um fragmento XML, no contexto inicial."""
    return flow(node, context())


class InlineTest(unittest.TestCase):
    def test_keeps_text_and_tail_of_every_node_including_unknown_and_comments(self):
        node = xml('<p>a <unknown>b <x>c</x> d</unknown> e<!-- note --> f<?pi x?> g</p>')
        self.assertEqual(runs_text(normalize(inlines(node))), 'a b c d e f g')

    def test_formatting_is_cumulative(self):
        runs = normalize(inlines(xml('<p>x <bold>y <italic>z</italic></bold></p>')))
        z = next(r for r in runs if r['text'] == 'z')
        self.assertTrue(z['bold'] and z['italic'])

    def test_whitespace_and_punctuation_normalized_across_runs(self):
        runs = normalize(inlines(xml('<p>  ( <xref>Fig. 1</xref> ) ,   end  </p>')))
        self.assertEqual(runs_text(runs), '(Fig. 1), end')

    def test_ext_link_becomes_hyperlink_run(self):
        runs = normalize(inlines(xml(f'<p {NS}>see <ext-link xlink:href="http://x.org">site</ext-link></p>')))
        self.assertEqual(runs[-1], {'text': 'site', 'href': 'http://x.org'})

    def test_inline_formula_becomes_omml(self):
        node = xml(f'<p {NS}>v <inline-formula><mml:math><mml:mi>x</mml:mi></mml:math></inline-formula></p>')
        self.assertIn('omml', inlines(node)[-1])


class FlowTest(unittest.TestCase):
    def test_block_inside_paragraph_splits_it_without_losing_tail(self):
        node = xml('<p>before <list list-type="order"><list-item><p>one</p></list-item></list> after</p>')
        self.assertEqual(texts(extract(node)), ['before', '1. one', 'after'])

    def test_unknown_wrapper_with_blocks_is_a_container(self):
        node = xml('<sec><wrapper><p>a</p><p>b</p></wrapper></sec>')
        self.assertEqual(texts(extract(node)), ['a', 'b'])

    def test_section_label_and_title_make_the_heading_and_nesting_sets_level(self):
        node = xml('<body><sec><label>1</label><title>Intro</title><p>x</p>'
                   '<sec><title>Sub</title><p>y</p></sec></sec></body>')
        blocks = extract(node)
        headings = [(b['level'], runs_text(b['runs'])) for b in blocks if b['type'] == 'heading']
        self.assertEqual(headings, [(2, '1 Intro'), (3, 'Sub')])

    def test_footnote_label_joins_first_paragraph(self):
        node = xml('<fn-group><fn><label>1</label><p>Note.</p></fn></fn-group>')
        (block,) = extract(node)
        self.assertEqual(block['runs'][0], {'text': '1', 'superscript': True})
        self.assertEqual(runs_text(block['runs']), '1 Note.')

    def test_reference_uses_mixed_citation_and_ignores_element_citation(self):
        node = xml('<back><ref-list><ref><label>2</label>'
                   '<element-citation><person-group><name><surname>Silva</surname>'
                   '<given-names>A</given-names></name></person-group><source>Atlas</source>'
                   '</element-citation>'
                   '<mixed-citation>SILVA, A. <italic>Atlas</italic>. 2017</mixed-citation></ref></ref-list></back>')
        blocks = extract(node)
        self.assertEqual(runs_text(blocks[0]['runs']), 'References')
        self.assertEqual(texts(blocks[1:]), ['2. SILVA, A. Atlas. 2017.'])
        self.assertTrue(blocks[1]['runs'][1]['italic'])

    def test_reference_without_mixed_citation_keeps_its_text(self):
        node = xml('<back><ref-list><ref><element-citation><source>Atlas</source> <year>2017</year>'
                   '</element-citation></ref></ref-list></back>')
        self.assertEqual(texts(extract(node)[1:]), ['Atlas 2017.'])

    def test_display_formula_in_paragraph_and_its_label(self):
        node = xml(f'<p {NS}>where:<disp-formula><label>(1)</label><mml:math><mml:mi>y</mml:mi>'
                   '</mml:math></disp-formula></p>')
        paragraph, formula = extract(node)
        self.assertEqual(runs_text(paragraph['runs']), 'where:')
        self.assertEqual(formula['type'], 'formula')
        self.assertEqual(formula['runs'][-1]['text'], ' (1)')

    def test_display_formula_with_empty_tex_math_uses_the_image(self):
        # #1441: <tex-math> vazio interrompia a geração com IndexError
        node = xml(f'<sec {NS}><disp-formula id="e1"><label>(1)</label><alternatives><tex-math/>'
                   '<graphic xlink:href="e1.jpg"/></alternatives></disp-formula></sec>')
        (figure,) = extract(node)
        self.assertEqual((figure['type'], figure['href']), ('figure', 'e1.jpg'))
        self.assertEqual(runs_text(figure['caption']), '(1)')

    def test_display_formula_with_empty_tex_math_and_no_image_keeps_the_label(self):
        node = xml(f'<sec {NS}><disp-formula id="e1"><label>(1)</label><tex-math/></disp-formula></sec>')
        self.assertEqual(texts(extract(node)), ['(1)'])

    def test_inline_formula_with_empty_tex_math_uses_one_image(self):
        # só a melhor das representações (graphic.best), não a miniatura junto
        from packtools.sps.formats.pdf.extract.formula import formula_runs
        for name, image in (('disp-formula', 'graphic'), ('inline-formula', 'inline-graphic')):
            with self.subTest(name=name):
                node = xml(f'<{name} {NS}><alternatives><tex-math/>'
                           f'<{image} xlink:href="e1-thumb.jpg" content-type="scielo-267x140"/>'
                           f'<{image} xlink:href="e1.jpg"/></alternatives></{name}>')
                self.assertEqual([r.get('image') for r in formula_runs(node)], ['e1.jpg'])

    def test_table_grid_resolves_spans_and_keeps_th_in_body(self):
        node = xml('<sec><table-wrap id="t1"><label>Table 1</label><caption><title>T</title></caption><table>'
                   '<thead><tr><th colspan="2">H</th></tr></thead>'
                   '<tbody><tr><td rowspan="2">a</td><td><italic>b</italic></td></tr>'
                   '<tr><th>c</th></tr></tbody></table>'
                   '<table-wrap-foot><fn><p>foot</p></fn></table-wrap-foot></table-wrap></sec>')
        (table,) = extract(node)
        self.assertEqual((table['nrows'], table['ncols'], table['panel']), (3, 2, 0))
        cells = {(c['row'], c['col']): c for c in table['cells']}
        self.assertEqual(cells[(2, 1)]['runs'], [{'text': 'c'}])
        self.assertTrue(cells[(2, 1)]['header'])
        self.assertTrue(cells[(1, 1)]['runs'][0]['italic'])
        self.assertEqual(runs_text(table['caption']), 'Table 1. T')
        self.assertEqual([runs_text(r) for r in table['foot']], ['foot'])

    def test_table_wrap_with_two_tables_gives_one_block_per_panel(self):
        node = xml('<sec><table-wrap id="t1"><label>Table 1</label><table><tr><td>a</td></tr></table>'
                   '<table><tr><td>b</td><td>c</td></tr></table>'
                   '<table-wrap-foot><p>foot</p></table-wrap-foot></table-wrap></sec>')
        first, second = extract(node)
        self.assertEqual([(b['panel'], b['ncols']) for b in (first, second)], [(0, 1), (1, 2)])
        # legenda só no 1º painel, notas só no último, marca do xref só no 1º
        self.assertEqual((runs_text(first['caption']), second['caption']), ('Table 1', []))
        self.assertEqual((first['foot'], [runs_text(r) for r in second['foot']]), ([], ['foot']))
        self.assertEqual((first.get('anchor'), second.get('anchor')), ('t1', None))

    def test_table_wrap_with_only_an_image_becomes_a_figure_with_caption_first(self):
        node = xml(f'<sec {NS}><table-wrap><label>Table 2</label><graphic xlink:href="t2.jpg"/></table-wrap></sec>')
        (block,) = extract(node)
        self.assertEqual((block['type'], block['href'], block['caption_first']), ('figure', 't2.jpg', True))

    def test_table_with_positions_without_cell_warns_with_its_rows(self):
        # #1380: cabeçalho de 3 colunas (colspan) e corpo de 4, como na Tabela 6 de delta-42-02-e202642271967
        node = xml('<sec><table-wrap id="t6"><table>'
                   '<thead><tr><th>V</th><th colspan="2">H</th></tr></thead>'
                   '<tbody><tr><td>a</td><td>1</td><td>2</td><td>3</td></tr>'
                   '<tr><td>b</td><td>4</td></tr></tbody></table></table-wrap></sec>')
        with self.assertLogs(table_extract.logger, level='WARNING') as logs:
            (table,) = extract(node)
        self.assertEqual(table_extract.holes(table), [(0, 3), (2, 2), (2, 3)])
        self.assertEqual(len(logs.output), 1)
        self.assertIn('tabela t6: 3 posições sem célula no XML (linhas 1, 3)', logs.output[0])

    def test_consistent_table_does_not_warn(self):
        node = xml('<sec><table-wrap id="t1"><table><thead><tr><th colspan="2">H</th></tr></thead>'
                   '<tbody><tr><td rowspan="2">a</td><td>b</td></tr><tr><td>c</td></tr></tbody>'
                   '</table></table-wrap></sec>')
        with self.assertNoLogs(table_extract.logger, level='WARNING'):
            (table,) = extract(node)
        self.assertEqual(table_extract.holes(table), [])


class ArticleTest(unittest.TestCase):
    def test_body_text_before_first_section_is_kept(self):
        root = xml('<article><front><article-meta/></front><body><p>lead</p>'
                   '<sec><title>S</title><p>x</p></sec></body></article>')
        self.assertIn('lead', texts(extract_article(root)['main']))

    def test_appendix_and_supplementary_section_go_to_annex_translation_is_another_document(self):
        root = xml('<article><front><article-meta/></front><body><p>b</p></body><back>'
                   '<ack><title>Ack</title><p>thanks</p></ack>'
                   '<app-group><app><title>App A</title><p>appendix</p></app></app-group>'
                   '<sec><title>Supp</title><supplementary-material><label>S1</label></supplementary-material></sec>'
                   '</back><sub-article article-type="translation"><body><p>tradução</p></body></sub-article>'
                   '<sub-article article-type="reviewer-report"><front-stub><title-group>'
                   '<article-title>Review</article-title></title-group></front-stub><body><p>ok</p></body>'
                   '</sub-article></article>')
        article = extract_article(root)
        self.assertEqual(texts(article['main']), ['b', 'Ack', 'thanks', 'Review', 'ok'])
        self.assertEqual(texts(article['annex']), ['App A', 'appendix', 'Supp', 'S1'])

    def test_cite_as_note_goes_to_footer_only(self):
        root = xml('<article><front><article-meta><author-notes><fn fn-type="other"><label>How to cite</label>'
                   '<p>Doe J. Title.</p></fn></author-notes></article-meta></front>'
                   '<back><fn-group><fn fn-type="other"><p>Como citar: Doe J. Title.</p></fn></fn-group></back></article>')
        article = extract_article(root)
        self.assertEqual(article['meta']['cite_as'], 'Doe J. Title.')
        # sem título nem autores, e a nota "como citar" não vira nota de autor
        self.assertEqual(article['front'], [])
        self.assertIn('Como citar: Doe J. Title.', texts(article['main']))

    def test_front_authors_affiliations_and_abstract_keywords(self):
        root = xml('<article xml:lang="en"><front><article-meta>'
                   '<contrib-group><contrib><name><surname>Costa</surname><given-names>Ana</given-names>'
                   '<suffix>Neto</suffix></name><xref ref-type="aff" rid="a1">1</xref>'
                   '<xref ref-type="aff" rid="a2">2</xref><xref ref-type="corresp" rid="c1"/></contrib>'
                   '<contrib><collab>Group X</collab></contrib></contrib-group>'
                   '<aff id="a1"><label>1</label><institution content-type="orgname">USP</institution>'
                   '<addr-line><city>SP</city></addr-line><country>Brazil</country></aff>'
                   '<abstract><title>Abstract</title><sec><title>Methods</title><p>m</p></sec></abstract>'
                   '<kwd-group xml:lang="en"><title>Keywords</title><kwd>a</kwd><kwd><italic>b</italic></kwd></kwd-group>'
                   '</article-meta></front></article>')
        front = extract_article(root)['front']
        self.assertEqual(summary(front), [
            ('author', 'Ana Costa Neto1,2* and Group X'),
            ('affiliation', '1 USP, SP, Brazil'),
            ('abstract_title', 'Abstract'),
            ('abstract', 'Methods: m'),
            ('keywords', 'Keywords a, b'),
        ])
        authors, aff = front[0], front[1]
        # cada marca é link interno para a afiliação/nota (o "," entre elas não)
        self.assertEqual([r.get('anchor') for r in authors['runs'] if r.get('superscript')],
                         ['a1', None, 'a2', 'c1'])
        # a afiliação é o alvo: marca no início e rótulo sobrescrito
        self.assertEqual(aff['runs'][:2], [{'bookmark': 'a1'}, {'text': '1', 'superscript': True}])
        self.assertEqual((authors['char_role'], aff['char_role']), ('author_char', 'affiliation_char'))
        keywords = front[-1]['runs']
        self.assertEqual(keywords[0].get('char_role'), 'keywords_title_char')
        self.assertTrue(keywords[-1]['italic'])


TRANSLATED = (
    '<article xml:lang="pt"><front><article-meta>'
    '<article-id pub-id-type="doi">10/pt</article-id>'
    '<title-group><article-title>Título</article-title></title-group>'
    '<contrib-group><contrib><name><surname>Silva</surname><given-names>Ana</given-names></name></contrib></contrib-group>'
    '<volume>5</volume>'
    '<abstract><title>Resumo</title><p>resumo pt</p></abstract>'
    '<trans-abstract xml:lang="es"><title>Resumen</title><p>resumen es</p></trans-abstract>'
    '<kwd-group xml:lang="pt"><kwd>chave</kwd></kwd-group>'
    '<kwd-group xml:lang="es"><kwd>clave</kwd></kwd-group>'
    '</article-meta></front>'
    '<body><p>corpo pt</p></body>'
    '<back><ack><p>agradecimento</p></ack><ref-list><ref><mixed-citation>Ref A.</mixed-citation></ref></ref-list></back>'
    '<sub-article article-type="reviewer-report" xml:lang="pt"><body><p>parecer pt</p></body></sub-article>'
    '<sub-article article-type="translation" xml:lang="en"><front-stub>'
    '<article-id pub-id-type="doi">10/en</article-id>'
    '<title-group><article-title>Title</article-title></title-group>'
    '<abstract><title>Abstract</title><p>abstract en</p></abstract>'
    '<kwd-group xml:lang="en"><kwd>key</kwd></kwd-group>'
    '</front-stub><body><p>body en</p></body><back><ack><p>thanks</p></ack></back>'
    '<sub-article article-type="reviewer-report" xml:lang="en"><body><p>review en</p></body></sub-article>'
    '</sub-article></article>'
)


class LanguagesTest(unittest.TestCase):
    def setUp(self):
        self.root = xml(TRANSLATED)

    def test_languages_like_htmlgenerator(self):
        self.assertEqual(languages(self.root), ['pt', 'en'])

    def test_main_document_has_no_translation(self):
        article = extract_article(document_for(self.root))
        self.assertEqual(texts(article['main']), ['corpo pt', 'agradecimento', 'Referências', 'Ref A.', 'parecer pt'])
        self.assertEqual(article['meta']['title_text'], 'Título')

    def test_translation_front_stub_overrides_article_front(self):
        article = extract_article(document_for(self.root, 'en'))
        meta = article['meta']
        self.assertEqual((meta['title_text'], meta['doi'], meta['lang']), ('Title', '10/en', 'en'))
        # o que o front-stub não traz vem do artigo
        self.assertEqual(meta['volume'], '5')
        self.assertEqual(summary(article['front']), [
            ('article_title', 'Title'),
            ('author', 'Ana Silva'),
            ('abstract_title', 'Abstract'), ('abstract', 'abstract en'), ('keywords', 'key'),
            ('abstract_title', 'Resumo'), ('abstract', 'resumo pt'), ('keywords', 'chave'),
            ('abstract_title', 'Resumen'), ('abstract', 'resumen es'), ('keywords', 'clave'),
        ])

    def test_translation_body_with_article_back_and_translated_back_and_sub_articles(self):
        article = extract_article(document_for(self.root, 'en'))
        self.assertEqual(texts(article['main']), ['body en', 'thanks', 'References', 'Ref A.', 'review en'])

    def test_original_tree_is_not_changed_and_unknown_language_fails(self):
        before = etree.tostring(self.root)
        document_for(self.root, 'en')
        self.assertEqual(etree.tostring(self.root), before)
        with self.assertRaises(ValueError):
            document_for(self.root, 'fr')


class ColumnWeightsTest(unittest.TestCase):
    def grid(self, rows):
        node = xml('<sec><table-wrap><table>' + ''.join(
            '<tr>' + ''.join(rows_) + '</tr>' for rows_ in rows) + '</table></table-wrap></sec>')
        return extract(node)[0]

    def test_weights_follow_longest_text_with_limits_and_empty_columns(self):
        from packtools.sps.formats.pdf.layout.placement import column_weights
        grid = self.grid([['<th colspan="2">Brasil</th>', '<th></th>'],
                          ['<td>Shannon index</td>', '<td>1</td>', '<td></td>'],
                          ['<td>x</td>', '<td>' + 'long text ' * 10 + '</td>', '<td></td>']])
        weights, words = column_weights(grid)
        # "Shannon index" = 12.7 caracteres médios x 6pt; o texto longo bate no
        # teto de 200pt; a 3ª coluna não tem conteúdo
        self.assertAlmostEqual(weights[0], 76.2)
        self.assertEqual(weights[1:], [200, None])
        # maior palavra x 6pt; "Brasil" (5.2 x 6 / 2 = 15.6) não supera "Shannon" nem "long"
        self.assertAlmostEqual(words[0], 7.2 * 6)
        self.assertAlmostEqual(words[1], 4 * 6)
        self.assertIsNone(words[2])

    def test_merged_cell_spreads_its_width(self):
        from packtools.sps.formats.pdf.layout.placement import column_weights
        grid = self.grid([['<th colspan="2">Brasil</th>'], ['<td>1</td>', '<td>2</td>']])
        _, words = column_weights(grid)
        # "Brasil" = 5.2 caracteres médios (B 1.2, i e l 0.5) x 6pt, dividido por 2
        self.assertEqual([round(w, 1) for w in words], [15.6, 15.6])

    def test_formula_only_column_is_not_empty(self):
        # #1442: coluna só com fórmula ficava com a largura mínima (aabc-98-s1-e20250485, Tabela II)
        from packtools.sps.formats.pdf.layout.placement import column_weights
        node = xml(f'<sec {NS}><table-wrap><table><tr><td>Model</td>'
                   '<td><inline-formula><mml:math><mml:mn>0.843</mml:mn></mml:math></inline-formula></td>'
                   '</tr></table></table-wrap></sec>')
        weights, words = column_weights(extract(node)[0])
        # "0.843" = 5 caracteres médios: peso mínimo de 50pt e palavra de 30pt
        self.assertEqual(weights[1], 50)
        self.assertAlmostEqual(words[1], 5 * 6)

    def test_formula_counts_with_the_text_of_its_line(self):
        from packtools.sps.formats.pdf.layout.placement import column_weights
        node = xml(f'<sec {NS}><table-wrap><table><tr><td>'
                   '<inline-formula><mml:math><mml:msup><mml:mi>R</mml:mi><mml:mn>2</mml:mn></mml:msup>'
                   '</mml:math></inline-formula> adjusted value</td></tr></table></table-wrap></sec>')
        weights, words = column_weights(extract(node)[0])
        # "R2" (2.2) + "adjusted value" (13.0) na mesma linha; maior palavra "adjusted" (7.5)
        self.assertAlmostEqual(weights[0], 15.2 * 6)
        self.assertAlmostEqual(words[0], 7.5 * 6)

    def test_image_counts_by_its_natural_width(self):
        from packtools.sps.formats.pdf.layout.placement import column_weights
        node = xml(f'<sec {NS}><table-wrap><table><tr><td>a</td>'
                   '<td><inline-graphic xlink:href="x.png"/></td></tr></table></table-wrap></sec>')
        weights, words = column_weights(extract(node)[0], lambda href: 120 * 12700)
        # 120pt de largura natural: peso e palavra de 120pt
        self.assertAlmostEqual(weights[1], 120)
        self.assertAlmostEqual(words[1], 120)

    def test_unreadable_image_counts_by_its_alt_text(self):
        from packtools.sps.formats.pdf.layout.placement import column_weights
        node = xml(f'<sec {NS}><table-wrap><table><tr><td>a</td>'
                   '<td><inline-graphic xlink:href="x.png"><alt-text>logo</alt-text></inline-graphic></td>'
                   '</tr></table></table-wrap></sec>')
        _, words = column_weights(extract(node)[0], lambda href: None)
        # sem largura natural, conta o texto que o render escreve no lugar ("logo" = 3.5)
        self.assertAlmostEqual(words[1], 3.5 * 6)

    def test_widths_are_proportional_and_fill_the_table(self):
        from packtools.sps.formats.pdf.layout.placement import EMPTY_COLUMN_WIDTH, column_widths
        widths = column_widths([50, 150, None], [40, 10, None], 10 ** 7)
        self.assertEqual(widths[2], EMPTY_COLUMN_WIDTH)
        self.assertEqual(widths[1], 3 * widths[0])
        self.assertAlmostEqual(sum(widths), 10 ** 7, delta=2)

    def test_widths_without_columns_or_content(self):
        from packtools.sps.formats.pdf.layout.placement import column_widths
        self.assertEqual(column_widths([], [], 10 ** 7), [])
        # todas vazias: larguras iguais
        self.assertEqual(column_widths([None, None], [None, None], 10 ** 7), [5 * 10 ** 6] * 2)

    def test_split_width_sums_to_total(self):
        from packtools.sps.formats.pdf.layout.page import split_width
        self.assertEqual(split_width(1001, 0.5), [500, 501])

    def test_uses_longest_word_when_weights_do_not_fit(self):
        from packtools.sps.formats.pdf.layout.placement import column_widths
        # 3 x 50pt = 150pt de pesos numa tabela de 60pt: vale a maior palavra
        widths = column_widths([50, 50, 50], [42, 18, 12], 60 * 12700)
        self.assertEqual([round(w / 12700) for w in widths], [35, 15, 10])

    def test_panels_of_the_same_table_wrap_share_the_layout(self):
        from packtools.sps.formats.pdf.config.page import DOUBLE_COLUMN, SINGLE_COLUMN, load_page
        from packtools.sps.formats.pdf.layout.page import content_width
        from packtools.sps.formats.pdf.layout.placement import place
        # 1º painel estreito, 2º com colunas demais: os dois vão para a largura toda
        node = xml('<sec><table-wrap id="t1"><table><tr><td>a</td></tr></table><table><tr>'
                   + '<td>x</td>' * 5 + '</tr></table></table-wrap>'
                   '<table-wrap id="t2"><table><tr><td>b</td></tr></table></table-wrap></sec>')
        page = load_page()
        blocks = place(extract(node), page=page, assets=None)
        self.assertEqual([b['layout'] for b in blocks], [SINGLE_COLUMN, SINGLE_COLUMN, DOUBLE_COLUMN])
        # mesmo layout, mesma largura; as colunas são de cada painel
        self.assertEqual([b['width'] for b in blocks[:2]], [content_width(page)] * 2)
        self.assertEqual([len(b['column_widths']) for b in blocks], [1, 5, 1])
        blocks = place(extract(node), page=page, assets=None, overrides={'t1': DOUBLE_COLUMN})
        self.assertEqual([b['layout'] for b in blocks], [DOUBLE_COLUMN] * 3)


class OpenIssuesTest(unittest.TestCase):
    def test_square_root_gets_hidden_degree_so_libreoffice_draws_the_radicand(self):
        from packtools.sps.formats.pdf.extract import formula
        m = '{http://schemas.openxmlformats.org/officeDocument/2006/math}'
        sqrt = xml('<math xmlns="http://www.w3.org/1998/Math/MathML"><msqrt><mi>x</mi></msqrt></math>')
        rad = formula.mathml_to_omml(sqrt).find(f'.//{m}rad')
        self.assertEqual([etree.QName(c).localname for c in rad], ['radPr', 'deg', 'e'])
        self.assertEqual(rad.find(f'{m}radPr/{m}degHide').get(f'{m}val'), '1')

    def test_footer_omits_missing_parts_without_dangling_colon(self):
        from packtools.sps.formats.pdf.render.front import vol_issue_year
        empty = {'volume': '', 'issue': '', 'year': '', 'location_label': ''}
        self.assertEqual(vol_issue_year({**empty, 'year': '2023'}), '2023')
        self.assertEqual(vol_issue_year({**empty, 'volume': '53', 'issue': '4', 'year': '2023',
                                         'location_label': '271-280'}), 'VOL. 53 (4) 2023: 271-280')
        self.assertEqual(vol_issue_year(empty), '')

    def test_abstract_and_keywords_titles_keep_formatting(self):
        # o old_pdf lia esses títulos como texto puro e perdia o itálico
        root = xml('<article xml:lang="en"><front><article-meta>'
                   '<abstract><title>Abstract of <italic>Zea</italic></title><p>a</p></abstract>'
                   '<kwd-group xml:lang="en"><title>Key <italic>words</italic>:</title><kwd>k</kwd></kwd-group>'
                   '</article-meta></front></article>')
        title, _, keywords = extract_article(root)['front']
        self.assertEqual(title['runs'][-1], {'text': 'Zea', 'italic': True})
        self.assertEqual(runs_text(keywords['runs']), 'Key words: k')
        self.assertTrue(keywords['runs'][1]['italic'])
        self.assertEqual({r.get('char_role') for r in keywords['runs'][:3]}, {'keywords_title_char'})

    def test_default_titles_follow_document_language(self):
        root = xml('<article xml:lang="pt"><front><article-meta/></front><back><ref-list>'
                   '<ref><mixed-citation>A.</mixed-citation></ref></ref-list></back></article>')
        self.assertEqual(texts(extract_article(root)['main'])[0], 'Referências')

    def test_translation_gets_reference_title_in_its_language(self):
        root = xml(TRANSLATED.replace('<ref-list>', '<ref-list><title>REFERÊNCIAS</title>'))
        self.assertIn('REFERÊNCIAS', texts(extract_article(document_for(root))['main']))
        self.assertIn('References', texts(extract_article(document_for(root, 'en'))['main']))


class InternalLinksTest(unittest.TestCase):
    def test_xref_becomes_internal_link_to_rid(self):
        node = xml('<p>see <xref ref-type="bibr" rid="B1 B2">Silva, 2020</xref>.</p>')
        runs = normalize(inlines(node))
        self.assertEqual(runs[1], {'text': 'Silva, 2020', 'anchor': 'B1'})

    def test_element_with_id_marks_its_first_block(self):
        node = xml('<back><ref-list><ref id="B1"><mixed-citation>Ref.</mixed-citation></ref></ref-list>'
                   '<fn-group><fn id="fn1"><label>1</label><p>Note.</p></fn></fn-group></back>')
        blocks = extract(node)
        marks = [b['runs'][0] for b in blocks if b['runs'][0].get('bookmark')]
        self.assertEqual(marks, [{'bookmark': 'B1'}, {'bookmark': 'fn1'}])

    def test_figure_and_table_get_anchor(self):
        node = xml(f'<sec {NS}><fig id="f1"><graphic xlink:href="a.jpg"/></fig>'
                   '<table-wrap id="t1"><table><tr><td>x</td></tr></table></table-wrap></sec>')
        self.assertEqual([b.get('anchor') for b in extract(node)], ['f1', 't1'])
