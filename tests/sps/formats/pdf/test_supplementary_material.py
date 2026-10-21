"""
Apêndices (``<app-group>``/``<app>``) e material suplementar no gerador novo.

Migra tests/sps/formats/old_pdf/pipeline/test_supplementary_material.py.
O old_pdf tinha ``extract_data`` (seções de anexo), ``extract_supplementary_items``
(dict por item) e ``format_item`` (linha descritiva); aqui o mesmo
comportamento é verificado pelos blocos de ``extract_article``: o
``<app-group>`` e a seção de material suplementar vão para ``annex``
(extract/article.py) e cada ``<supplementary-material>`` vira um parágrafo
descritivo (extract/supplementary_material.py).
"""

import unittest

from tests.sps.formats.pdf.helpers import article, article_xml, summary, texts


TABLE = '<table-wrap><table><tbody><tr><td>a</td></tr></tbody></table></table-wrap>'


def parts(back='', body='', extra='', lang='en'):
    """Artigo extraído a partir de trechos de ``<body>``/``<back>``."""
    return article(article_xml(body=body, back=back, extra=extra, lang=lang))


def annex(back='', body='', extra='', lang='en'):
    """Blocos dos anexos."""
    return parts(back, body, extra, lang)['annex']


def outline(blocks):
    """(texto, nível) de cada heading."""
    return [(texts([b])[0], b['level']) for b in blocks if b['type'] == 'heading']


def kinds(blocks):
    """Sequência de (tipo, texto ou href) para conferir onde cada figura/tabela caiu."""
    out = []
    for b in blocks:
        if b['type'] in ('figure', 'table'):
            out.append((b['type'], b.get('href')))
        else:
            out.append((b['type'], texts([b])[0]))
    return out


def item(inner, lang='en'):
    """
    Texto da(s) linha(s) de um ``<supplementary-material>`` filho do ``<back>``.

    O item solto vai para os anexos sob o título padrão (ver
    test_items_directly_in_back_go_to_annex_under_default_heading); aqui só
    interessa a linha do item, sem o título.
    """
    a = parts(back=f'<supplementary-material id="suppl1">{inner}</supplementary-material>', lang=lang)
    return texts(b for b in a['main'] + a['annex'] if b['type'] != 'heading')


class AppGroupTest(unittest.TestCase):

    def test_app_group_goes_to_annex_with_its_paragraphs(self):
        """
        old: TestExtractDataAppendix.test_single_app_reads_its_paragraphs (parte do texto)
        old: TestExtractDataAppendix.test_multiple_app_groups
        old: TestExtractDataAppendix.test_empty_xml_tree
        """
        cases = [
            ('<app-group><app><p>Sample text content</p></app></app-group>', ['Sample text content']),
            ('<app-group><app><p>Text 1</p></app></app-group>'
             '<app-group><app><p>Text 2</p></app></app-group>', ['Text 1', 'Text 2']),
            ('<ack><p>x</p></ack>', []),
        ]
        for back, expected in cases:
            with self.subTest(back=back):
                a = parts(back=back)
                self.assertEqual([t for t in texts(a['annex']) if t != 'Appendix'], expected)
                self.assertNotIn('Sample text content', texts(a['main']))

    def test_untitled_app_group_gets_default_localized_heading(self):
        """
        old: TestExtractDataAppendix.test_single_app_reads_its_paragraphs (outline)
        old: TestExtractDataAppendix.test_app_group_falls_back_to_default_title_without_title_element
        old: TestExtractDataAppendix.test_multiple_apps_without_any_title_stay_merged

        Diferença intencional: o título padrão sai no idioma do documento.
        """
        cases = [
            ('<app-group><app><p>Texto</p></app></app-group>', 'en',
             [('heading', 'Appendix'), ('body', 'Texto')]),
            ('<app-group><app><p>Texto</p></app></app-group>', 'pt',
             [('heading', 'Apêndice'), ('body', 'Texto')]),
            ('<app-group><app><p>A</p></app><app><p>B</p></app></app-group>', 'en',
             [('heading', 'Appendix'), ('body', 'A'), ('body', 'B')]),
        ]
        for back, lang, expected in cases:
            with self.subTest(back=back, lang=lang):
                self.assertEqual(summary(annex(back=back, lang=lang)), expected)
                self.assertEqual(outline(annex(back=back, lang=lang))[0][1], 2)

    def test_untitled_apps_keep_all_text_in_order(self):
        """old: TestExtractDataAppendix.test_multiple_apps_without_any_title_stay_merged (texto)"""
        blocks = annex(back='<app-group><app><p>A</p></app><app><p>B</p></app></app-group>')
        self.assertEqual([t for t in texts(blocks) if t != 'Appendix'], ['A', 'B'])

    def test_app_with_table_and_figures(self):
        """
        old: TestExtractDataAppendix.test_app_with_table
        old: TestExtractDataAppendix.test_app_with_figure_inside_paragraph
        old: TestExtractDataAppendix.test_app_with_direct_graphic

        Diferença intencional: o heading do <app> junta <label> e <title>
        ("Anexo 2 GRÁFICA 1"), como em toda seção; o old_pdf usava só o título.
        """
        cases = [
            ('<app-group><app><table-wrap><label>Table 1</label><caption><title>Sample Table</title>'
             '</caption><table><tbody><tr><td>a</td></tr></tbody></table></table-wrap></app></app-group>',
             [], 'table', None),
            ('<app-group><app><title>1. Abordagem vertical</title>'
             '<p><fig id="f65"><graphic xlink:href="gf65.tif"/></fig></p></app></app-group>',
             [('1. Abordagem vertical', 2)], 'figure', 'gf65.tif'),
            ('<app-group><app><label>Anexo 2</label><title>GRÁFICA 1</title>'
             '<graphic xlink:href="gf01.tif"/></app></app-group>',
             [('Anexo 2 GRÁFICA 1', 2)], 'figure', 'gf01.tif'),
        ]
        for back, headings, kind, href in cases:
            with self.subTest(back=back):
                blocks = annex(back=back)
                self.assertEqual([h for h in outline(blocks) if h[0] != 'Appendix'], headings)
                found = [b for b in blocks if b['type'] in ('figure', 'table')]
                self.assertEqual([(b['type'], b.get('href')) for b in found], [(kind, href)])

    def test_nested_sec_becomes_subsection_with_its_own_content(self):
        """
        old: TestExtractDataAppendix.test_app_nested_sec_becomes_subsection
        old: TestExtractDataAppendix.test_nested_sec_table_is_not_duplicated_in_the_app
        old: TestExtractDataAppendix.test_nested_sec_figure_stays_in_its_subsection

        Diferença intencional: o resultado é uma lista plana de blocos na
        ordem do documento; figura/tabela ficam depois do heading da subseção.
        """
        blocks = annex(back=(
            '<app-group><app><label>Annex 1</label>'
            '<p>In this annex, the properties are presented.</p>'
            '<sec><title>Zone 1</title><p>Zone 1 text</p>'
            '<sec><title>Zone 1.1</title><p>Zone 1.1 text</p></sec></sec>'
            '<sec><title>Zone 2</title><p>Zone 2 text</p></sec>'
            '</app></app-group>'))
        self.assertEqual(outline(blocks), [('Annex 1', 2), ('Zone 1', 3), ('Zone 1.1', 4), ('Zone 2', 3)])
        self.assertEqual(summary(blocks), [
            ('heading', 'Annex 1'), ('body', 'In this annex, the properties are presented.'),
            ('heading', 'Zone 1'), ('body', 'Zone 1 text'),
            ('heading', 'Zone 1.1'), ('body', 'Zone 1.1 text'),
            ('heading', 'Zone 2'), ('body', 'Zone 2 text'),
        ])
        cases = [
            ('<app-group><app><label>Annex 1</label><sec><title>Zone 1</title>'
             f'{TABLE}</sec></app></app-group>',
             [('heading', 'Annex 1'), ('heading', 'Zone 1'), ('table', None)]),
            ('<app-group><app><label>7. APPENDIX</label><sec><title>7.1</title><p>A</p></sec>'
             '<sec><title>7.3. Outliers</title><fig id="f1"><graphic xlink:href="gf1.tif"/></fig></sec>'
             '</app></app-group>',
             [('heading', '7. APPENDIX'), ('heading', '7.1'), ('paragraph', 'A'),
              ('heading', '7.3. Outliers'), ('figure', 'gf1.tif')]),
        ]
        for back, expected in cases:
            with self.subTest(back=back):
                self.assertEqual(kinds(annex(back=back)), expected)

    def test_group_title_and_app_titles(self):
        """
        old: TestExtractDataAppendix.test_group_title_is_not_rendered_as_a_paragraph
        old: TestExtractDataAppendix.test_group_title_with_titled_apps_as_subsections
        old: TestExtractDataAppendix.test_group_title_keeps_single_app_title
        old: TestExtractDataAppendix.test_app_group_direct_content

        Diferença intencional (primeiro caso): o old_pdf descartava o <label>
        do <app> igual ao título do grupo; o gerador novo não perde conteúdo
        e o mantém como subseção (nível 3). O título do grupo continua só
        como heading, nunca como parágrafo.
        """
        cases = [
            ('<app-group><title>Appendix</title><app><label>Appendix</label><p>Texto</p></app></app-group>',
             [('heading', 'Appendix'), ('heading', 'Appendix'), ('paragraph', 'Texto')],
             [('Appendix', 2), ('Appendix', 3)]),
            ('<app-group><title>Apêndices</title>'
             '<app><title>1. Abordagem vertical</title><p>A</p></app>'
             '<app><title>2. Abordagem horizontal</title><p>B</p></app></app-group>',
             [('heading', 'Apêndices'), ('heading', '1. Abordagem vertical'), ('paragraph', 'A'),
              ('heading', '2. Abordagem horizontal'), ('paragraph', 'B')],
             [('Apêndices', 2), ('1. Abordagem vertical', 3), ('2. Abordagem horizontal', 3)]),
            ('<app-group><title>Appendix</title><app><title>Documentary Sources</title><p>Texto</p></app></app-group>',
             [('heading', 'Appendix'), ('heading', 'Documentary Sources'), ('paragraph', 'Texto')],
             [('Appendix', 2), ('Documentary Sources', 3)]),
            (f'<app-group><title>Anexo</title>{TABLE}<app><p>Texto</p></app></app-group>',
             [('heading', 'Anexo'), ('table', None), ('paragraph', 'Texto')],
             [('Anexo', 2)]),
        ]
        for back, expected, headings in cases:
            with self.subTest(back=back):
                blocks = annex(back=back)
                self.assertEqual(kinds(blocks), expected)
                self.assertEqual(outline(blocks), headings)

    def test_app_title_or_label_becomes_heading_of_each_app(self):
        """
        old: TestExtractDataAppendix.test_single_app_falls_back_to_its_own_label_without_group_title
        old: TestExtractDataAppendix.test_multiple_apps_with_titles_get_one_section_each
        old: TestExtractDataAppendix.test_multiple_apps_use_label_when_title_is_missing
        """
        cases = [
            ('<app-group><app><label>SUPPLEMENTARY MATERIAL</label><p>Texto</p></app></app-group>',
             [('SUPPLEMENTARY MATERIAL', 2)]),
            ('<app-group><app><title>Anexo A</title><p>A</p></app>'
             '<app><title>Anexo B</title><p>B</p></app></app-group>',
             [('Anexo A', 2), ('Anexo B', 2)]),
            ('<app-group><app><label>Anexo 1</label><p>A</p></app>'
             '<app><title>Anexo 2</title><p>B</p></app></app-group>',
             [('Anexo 1', 2), ('Anexo 2', 2)]),
        ]
        for back, expected in cases:
            with self.subTest(back=back):
                self.assertEqual(outline(annex(back=back)), expected)

    def test_untitled_app_among_titled_ones_gets_numbered_default_heading(self):
        """old: TestExtractDataAppendix.test_multiple_apps_falls_back_to_numbered_default_for_the_untitled_one"""
        blocks = annex(back='<app-group><app><title>Anexo 1</title><p>A</p></app>'
                            '<app><p>B</p></app></app-group>')
        self.assertEqual(summary(blocks), [
            ('heading', 'Anexo 1'), ('body', 'A'), ('heading', 'Appendix 2'), ('body', 'B')])

    def test_translation_app_group_is_not_in_the_main_document(self):
        """old: TestExtractDataAppendix.test_app_group_in_translation_sub_article_is_skipped"""
        a = parts(back='<app-group><app><p>Principal</p></app></app-group>',
                  extra='<sub-article article-type="translation" xml:lang="pt" id="s1"><back>'
                        '<app-group><app><p>Translation</p></app></app-group></back></sub-article>')
        all_texts = texts(a['main'] + a['annex'])
        self.assertIn('Principal', all_texts)
        self.assertNotIn('Translation', all_texts)


class SupplementarySectionTest(unittest.TestCase):

    MEDIA = '<media mime-subtype="pdf" mimetype="application" xlink:href="a.pdf"/>'

    def test_supplementary_section_goes_to_annex_with_its_heading(self):
        """
        old: TestExtractDataSupplementaryMaterial.test_heading_uses_sec_title
        old: TestExtractDataSupplementaryMaterial.test_heading_falls_back_to_sec_label
        old: TestExtractDataSupplementaryMaterial.test_supplementary_material_with_label_and_media_in_sec (linha do item)
        """
        cases = [
            ('<sec sec-type="supplementary-material"><title>Material Suplementar</title>'
             '<supplementary-material id="suppl1"><label>Material Suplementar</label>'
             '<media mime-subtype="pdf" mimetype="application" xlink:href="a-s.pdf"/>'
             '</supplementary-material></sec>',
             [('heading', 'Material Suplementar'), ('body', 'Material Suplementar: a-s.pdf (application/pdf)')]),
            ('<sec><label>Supplementary materials</label>'
             '<supplementary-material id="suppl1"><label>Suppl. 1</label></supplementary-material></sec>',
             [('heading', 'Supplementary materials'), ('body', 'Suppl. 1')]),
        ]
        for back, expected in cases:
            with self.subTest(back=back):
                a = parts(back=back)
                self.assertEqual(summary(a['annex']), expected)
                self.assertEqual(outline(a['annex'])[0][1], 2)
                self.assertEqual(a['main'], [])
        a = parts(body='<sec><supplementary-material id="suppl1"><label>Supplementary Material</label>'
                       '<media mime-subtype="mp4" mimetype="video" xlink:href="a-suppl1.mp4"/>'
                       '</supplementary-material></sec>')
        self.assertIn('Supplementary Material: a-suppl1.mp4 (video/mp4)', texts(a['annex']))
        self.assertEqual(a['main'], [])

    def test_untitled_supplementary_section_gets_default_heading(self):
        """old: TestExtractDataSupplementaryMaterial.test_supplementary_material_with_label_and_media_in_sec"""
        blocks = annex(body='<sec><supplementary-material id="suppl1"><label>Supplementary Material</label>'
                            '<media mime-subtype="mp4" mimetype="video" xlink:href="a-suppl1.mp4"/>'
                            '</supplementary-material></sec>')
        self.assertEqual(outline(blocks), [('Supplementary Material', 2)])
        self.assertEqual(texts(blocks)[1:], ['Supplementary Material: a-suppl1.mp4 (video/mp4)'])

    def test_translation_supplementary_section_is_not_in_the_main_document(self):
        """old: TestExtractDataSupplementaryMaterial.test_heading_ignores_translation_sec_title"""
        a = parts(back='<sec><title>Material suplementar</title>'
                       '<supplementary-material id="s1"><label>S1</label></supplementary-material></sec>',
                  extra='<sub-article article-type="translation" xml:lang="pt" id="s2"><back>'
                        '<sec><title>Supplementary Materials</title><supplementary-material id="s1-en">'
                        '<label>S1 EN</label></supplementary-material></sec></back></sub-article>')
        self.assertEqual(summary(a['annex']), [('heading', 'Material suplementar'), ('body', 'S1')])
        self.assertEqual(a['main'], [])

    def test_section_paragraphs_and_items_keep_document_order_without_duplicates(self):
        """
        old: TestExtractDataSupplementaryMaterial.test_sec_paragraphs_and_items_keep_document_order
        old: TestExtractDataSupplementaryMaterial.test_sec_paragraph_that_only_wraps_the_item_is_not_duplicated
        """
        item_xml = f'<supplementary-material id="suppl1"><label>Suppl. 1</label>{self.MEDIA}</supplementary-material>'
        cases = [
            (f'<p>Before.</p>{item_xml}<p>After.</p>',
             ['Before.', 'Suppl. 1: a.pdf (application/pdf)', 'After.']),
            (f'<p>{item_xml}</p>', ['Suppl. 1: a.pdf (application/pdf)']),
        ]
        for content, expected in cases:
            with self.subTest(content=content):
                blocks = annex(body=f'<sec sec-type="supplementary-material"><title>Supp</title>{content}</sec>')
                self.assertEqual(texts(blocks), ['Supp'] + expected)

    def test_items_directly_in_back_are_extracted(self):
        """
        old: TestExtractDataSupplementaryMaterial.test_supplementary_material_in_back (linha do item)
        old: TestExtractDataSupplementaryMaterial.test_multiple_supplementary_material_items
        """
        cases = [
            ('<supplementary-material id="suppl1"><label>Suppl. 1</label>'
             '<media mime-subtype="pdf" mimetype="application" xlink:href="suppl1.pdf"/></supplementary-material>',
             ['Suppl. 1: suppl1.pdf (application/pdf)']),
            (f'<supplementary-material id="suppl1"><label>Suppl. 1</label>{self.MEDIA}</supplementary-material>'
             '<supplementary-material id="suppl2"><label>Suppl. 2</label>'
             '<media mime-subtype="xlsx" mimetype="application" xlink:href="b.xlsx"/></supplementary-material>',
             ['Suppl. 1: a.pdf (application/pdf)', 'Suppl. 2: b.xlsx (application/xlsx)']),
        ]
        for back, expected in cases:
            with self.subTest(back=back):
                a = parts(back=back)
                self.assertEqual([t for t in texts(a['main'] + a['annex']) if t != 'Supplementary Material'],
                                 expected)

    def test_items_directly_in_back_go_to_annex_under_default_heading(self):
        """
        old: TestExtractDataSupplementaryMaterial.test_supplementary_material_in_back
        old: TestExtractDataSupplementaryMaterial.test_app_group_and_supplementary_material_are_separate_sections
        """
        item_xml = f'<supplementary-material id="suppl1"><label>Suppl. 1</label>{self.MEDIA}</supplementary-material>'
        a = parts(back=item_xml)
        self.assertEqual(a['main'], [])
        self.assertEqual(summary(a['annex']), [
            ('heading', 'Supplementary Material'), ('body', 'Suppl. 1: a.pdf (application/pdf)')])
        a = parts(back=f'<app-group><title>Annex 1</title><app><p>Texto do anexo</p></app></app-group>{item_xml}')
        self.assertEqual([t for t, _ in outline(a['annex'])], ['Annex 1', 'Supplementary Material'])


class SupplementaryItemTest(unittest.TestCase):
    """Linha descritiva de cada <supplementary-material> (antigos extract_supplementary_items e format_item)."""

    def test_item_line(self):
        """
        old: TestExtractSupplementaryItems.test_without_label_or_media
        old: TestExtractSupplementaryItems.test_graphic_instead_of_media
        old: TestExtractSupplementaryItems.test_extracts_long_desc_from_media
        old: TestExtractSupplementaryItems.test_falls_back_to_alt_text_without_long_desc
        old: TestExtractSupplementaryItems.test_prefers_long_desc_over_alt_text
        old: TestFormatItem.test_label_filename_and_media_type
        old: TestFormatItem.test_missing_label_falls_back_to_default
        old: TestFormatItem.test_missing_filename_shows_only_label
        old: TestFormatItem.test_missing_everything_uses_default_label_only
        old: TestFormatItem.test_includes_caption_when_present
        old: TestFormatItem.test_includes_description_when_present
        """
        cases = [
            ('', 'Supplementary Material'),
            ('<label>Supplementary material 2</label><caption><title>Figure 1</title></caption>'
             '<graphic xlink:href="a-suppl2-gf3.jpg"/>',
             'Supplementary material 2 (Figure 1): a-suppl2-gf3.jpg'),
            ('<media mime-subtype="mp4" mimetype="video" xlink:href="a.mp4">'
             '<long-desc>Descricao detalhada do video.</long-desc></media>',
             'Supplementary Material: a.mp4 (video/mp4). Descricao detalhada do video.'),
            ('<graphic xlink:href="gf3.jpg"><alt-text>Breve descricao da figura.</alt-text></graphic>',
             'Supplementary Material: gf3.jpg. Breve descricao da figura.'),
            ('<media mime-subtype="mp4" mimetype="video" xlink:href="a.mp4">'
             '<alt-text>Breve.</alt-text><long-desc>Detalhada.</long-desc></media>',
             'Supplementary Material: a.mp4 (video/mp4). Detalhada.'),
            ('<label>Suppl. 1</label><media mime-subtype="pdf" mimetype="application" xlink:href="a.pdf"/>',
             'Suppl. 1: a.pdf (application/pdf)'),
            ('<media xlink:href="a.pdf"/>', 'Supplementary Material: a.pdf'),
            ('<label>Suppl. 1</label>', 'Suppl. 1'),
            ('<label>Suppl. 2</label><caption><title>Figure 1</title></caption><graphic xlink:href="gf3.jpg"/>',
             'Suppl. 2 (Figure 1): gf3.jpg'),
            ('<label>Suppl. 1</label><media mime-subtype="mp4" mimetype="video" xlink:href="a.mp4">'
             '<long-desc>Descricao detalhada do video.</long-desc></media>',
             'Suppl. 1: a.mp4 (video/mp4). Descricao detalhada do video.'),
        ]
        for inner, expected in cases:
            with self.subTest(inner=inner):
                self.assertEqual(item(inner), [expected])

    def test_default_label_follows_document_language(self):
        """
        old: TestFormatItem.test_missing_everything_uses_default_label_only

        Diferença intencional: o rótulo padrão sai no idioma do documento.
        """
        for lang, expected in (('en', 'Supplementary Material'), ('pt', 'Material suplementar'),
                               ('es', 'Material suplementario')):
            with self.subTest(lang=lang):
                self.assertEqual(item('', lang=lang), [expected])

    def test_prefers_media_over_graphic(self):
        """old: TestExtractSupplementaryItems.test_prefers_media_over_graphic_when_both_present"""
        (line,) = item('<media mime-subtype="mp4" mimetype="video" xlink:href="video.mp4"/>'
                       '<graphic xlink:href="thumbnail.jpg"/>')
        self.assertEqual(line, 'Supplementary Material: video.mp4 (video/mp4)')

    def test_paragraph_links_keep_the_address_visible_once(self):
        """
        old: TestExtractSupplementaryItems.test_paragraph_with_link_keeps_the_address
        old: TestExtractSupplementaryItems.test_paragraph_with_link_showing_the_address_is_not_repeated
        old: TestFormatItem.test_includes_notes_when_present

        Diferença intencional: o link continua clicável (run com href) e,
        sem <label>, a linha começa pelo rótulo padrão.
        """
        cases = [
            ('<label>*Supplemental Materials</label>'
             '<media mime-subtype="pdf" mimetype="application" xlink:href="Supp01.pdf"/>'
             '<p>For additional information, please <ext-link ext-link-type="uri" '
             'xlink:href="http://example.org/appendix.pdf">click here</ext-link>.</p>',
             '*Supplemental Materials: Supp01.pdf (application/pdf). For additional information, '
             'please click here (http://example.org/appendix.pdf).',
             'http://example.org/appendix.pdf'),
            ('<p>Para Tabela Suplementar 1, clique aqui. <ext-link ext-link-type="uri" '
             'xlink:href="https://example.org/t1.pdf">https://example.org/t1.pdf</ext-link></p>',
             'Supplementary Material. Para Tabela Suplementar 1, clique aqui. https://example.org/t1.pdf',
             'https://example.org/t1.pdf'),
            ('<label>Suppl. 1</label><media xlink:href="a.pdf"/>'
             '<p><ext-link xlink:href="https://example.org/a.pdf">Clique aqui</ext-link>.</p>',
             'Suppl. 1: a.pdf. Clique aqui (https://example.org/a.pdf).',
             'https://example.org/a.pdf'),
        ]
        for inner, expected, target in cases:
            with self.subTest(inner=inner):
                a = parts(back=f'<supplementary-material id="s1">{inner}</supplementary-material>')
                (block,) = [b for b in a['annex'] if b['type'] == 'paragraph']
                self.assertEqual(texts([block]), [expected])
                self.assertEqual(expected.count(target), 1)
                self.assertTrue(any(r.get('href') == target for r in block['runs']))

    def test_translation_items_are_not_in_the_main_document(self):
        """old: TestExtractSupplementaryItems.test_translation_items_are_skipped"""
        a = parts(back='<supplementary-material id="s1"><label>S1</label></supplementary-material>',
                  extra='<sub-article article-type="translation" xml:lang="pt" id="s2"><back>'
                        '<supplementary-material id="s1-en"><label>S1 EN</label></supplementary-material>'
                        '</back></sub-article>')
        self.assertEqual(a['main'], [])
        self.assertEqual(texts(a['annex']), ['Supplementary Material', 'S1'])


if __name__ == '__main__':
    unittest.main()
