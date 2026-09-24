import unittest

from lxml import etree

from packtools.sps.formats.pdf.pipeline import supplementary_material


def _texts(section):
    return [''.join(segment.get('text', '') for segment in paragraph) for paragraph in section['paragraphs']]


def _outline(result):
    return [(section['title'], section['level']) for section in result]


class TestExtractDataAppendix(unittest.TestCase):

    def test_empty_xml_tree(self):
        xml = etree.fromstring("<root></root>")
        self.assertEqual([], supplementary_material.extract_data(xml))

    def test_single_app_reads_its_paragraphs(self):
        # Regression, PR #1384 review: <app><p> was never read (85 apps in
        # 40 real articles)
        xml = etree.fromstring(
            "<root><app-group><app><p>Sample text content</p></app></app-group></root>"
        )
        result = supplementary_material.extract_data(xml)
        self.assertEqual([('Appendix', 2)], _outline(result))
        self.assertEqual(['Sample text content'], _texts(result[0]))

    def test_multiple_app_groups(self):
        xml = etree.fromstring(
            "<root>"
            "<app-group><app><p>Text 1</p></app></app-group>"
            "<app-group><app><p>Text 2</p></app></app-group>"
            "</root>"
        )
        result = supplementary_material.extract_data(xml)
        self.assertEqual([['Text 1'], ['Text 2']], [_texts(section) for section in result])

    def test_app_with_table(self):
        xml = etree.fromstring(
            "<root><app-group><app>"
            "<table-wrap><label>Table 1</label><caption><title>Sample Table</title></caption>"
            "<table><tbody><tr><td>a</td></tr></tbody></table></table-wrap>"
            "</app></app-group></root>"
        )
        result = supplementary_material.extract_data(xml)
        self.assertEqual(1, len(result))
        self.assertEqual(1, len(result[0]['tables']))

    def test_app_with_figure_inside_paragraph(self):
        # Regression, PR #1384 review: opus/v32/1517-7017-opus-32-e263206.xml,
        # every appendix is a <p><fig> and the whole appendix disappeared
        xml = etree.fromstring(
            '<root xmlns:xlink="http://www.w3.org/1999/xlink"><app-group>'
            '<app><title>1. Abordagem vertical</title>'
            '<p><fig id="f65"><graphic xlink:href="gf65.tif"/></fig></p></app>'
            '</app-group></root>'
        )
        result = supplementary_material.extract_data(xml)
        self.assertEqual(['gf65.tif'], [figure['href'] for figure in result[0]['figures']])

    def test_app_with_direct_graphic(self):
        # ts/v38n1/1809-4554-ts-38-1-e2026.241656.xml: <app> whose only
        # content is a <graphic>, with no <fig> around it
        xml = etree.fromstring(
            '<root xmlns:xlink="http://www.w3.org/1999/xlink"><app-group>'
            '<app><label>Anexo 2</label><title>GRÁFICA 1</title><graphic xlink:href="gf01.tif"/></app>'
            '</app-group></root>'
        )
        result = supplementary_material.extract_data(xml)
        self.assertEqual('GRÁFICA 1', result[0]['title'])
        self.assertEqual(['gf01.tif'], [figure['href'] for figure in result[0]['figures']])

    def test_app_nested_sec_becomes_subsection(self):
        # Regression, PR #1388 review: bjrs/v14n1/2319-0612-bjrs-v14n1-09-e3014.xml,
        # "Zone 1/2/3" <sec> inside <app> lost title and paragraphs
        xml = etree.fromstring(
            "<root><back><app-group><app><label>Annex 1</label>"
            "<p>In this annex, the properties are presented.</p>"
            "<sec><title>Zone 1</title><p>Zone 1 text</p>"
            "<sec><title>Zone 1.1</title><p>Zone 1.1 text</p></sec></sec>"
            "<sec><title>Zone 2</title><p>Zone 2 text</p></sec>"
            "</app></app-group></back></root>"
        )
        result = supplementary_material.extract_data(xml)
        self.assertEqual(
            [('Annex 1', 2), ('Zone 1', 3), ('Zone 1.1', 4), ('Zone 2', 3)],
            _outline(result),
        )
        self.assertEqual(['In this annex, the properties are presented.'], _texts(result[0]))
        self.assertEqual(['Zone 1.1 text'], _texts(result[2]))

    def test_nested_sec_table_is_not_duplicated_in_the_app(self):
        xml = etree.fromstring(
            "<root><back><app-group><app><label>Annex 1</label>"
            "<sec><title>Zone 1</title>"
            "<table-wrap><table><tbody><tr><td>a</td></tr></tbody></table></table-wrap>"
            "</sec></app></app-group></back></root>"
        )
        result = supplementary_material.extract_data(xml)
        self.assertEqual([0, 1], [len(section['tables']) for section in result])

    def test_nested_sec_figure_stays_in_its_subsection(self):
        # rbtur/v20/1982-6125-rbtur-20-e3423.xml: figures of "7.3. Outliers"
        # would otherwise be rendered under the "7. APPENDIX" heading
        xml = etree.fromstring(
            '<root xmlns:xlink="http://www.w3.org/1999/xlink"><back><app-group>'
            '<app><label>7. APPENDIX</label>'
            '<sec><title>7.1</title><p>A</p></sec>'
            '<sec><title>7.3. Outliers</title><fig id="f1"><graphic xlink:href="gf1.tif"/></fig></sec>'
            '</app></app-group></back></root>'
        )
        result = supplementary_material.extract_data(xml)
        self.assertEqual([0, 0, 1], [len(section['figures']) for section in result])

    def test_group_title_is_not_rendered_as_a_paragraph(self):
        # Regression, PR #1384 review: bpsr/v20n1/1981-3821-bpsr-20-1-e0001.xml
        # showed "APPENDIX" (heading) and then "Appendix" (paragraph)
        xml = etree.fromstring(
            "<root><app-group><title>Appendix</title>"
            "<app><label>Appendix</label><p>Texto</p></app></app-group></root>"
        )
        result = supplementary_material.extract_data(xml)
        self.assertEqual([('Appendix', 2)], _outline(result))
        self.assertEqual(['Texto'], _texts(result[0]))

    def test_group_title_with_titled_apps_as_subsections(self):
        # opus/v32: <app-group><title>Apêndices</title> with 8 titled <app>;
        # the group title was dropped when the apps were split
        xml = etree.fromstring(
            "<root><app-group><title>Apêndices</title>"
            "<app><title>1. Abordagem vertical</title><p>A</p></app>"
            "<app><title>2. Abordagem horizontal</title><p>B</p></app>"
            "</app-group></root>"
        )
        result = supplementary_material.extract_data(xml)
        self.assertEqual(
            [('Apêndices', 2), ('1. Abordagem vertical', 3), ('2. Abordagem horizontal', 3)],
            _outline(result),
        )

    def test_group_title_keeps_single_app_title(self):
        # rbpi: <title>Appendix</title> + <app><title>Documentary Sources...</title>,
        # the app title was dropped in favor of the group title
        xml = etree.fromstring(
            "<root><app-group><title>Appendix</title>"
            "<app><title>Documentary Sources</title><p>Texto</p></app></app-group></root>"
        )
        result = supplementary_material.extract_data(xml)
        self.assertEqual([('Appendix', 2), ('Documentary Sources', 3)], _outline(result))

    def test_app_group_direct_content(self):
        # aem/v70n3: <table-wrap> directly under <app-group>, outside any <app>
        xml = etree.fromstring(
            "<root><app-group><title>Anexo</title>"
            "<table-wrap><table><tbody><tr><td>a</td></tr></tbody></table></table-wrap>"
            "<app><p>Texto</p></app></app-group></root>"
        )
        result = supplementary_material.extract_data(xml)
        self.assertEqual([('Anexo', 2)], _outline(result))
        self.assertEqual(1, len(result[0]['tables']))
        self.assertEqual(['Texto'], _texts(result[0]))

    def test_app_group_falls_back_to_default_title_without_title_element(self):
        xml = etree.fromstring(
            "<root><app-group><app><p>Texto</p></app></app-group></root>"
        )
        self.assertEqual('Appendix', supplementary_material.extract_data(xml)[0]['title'])

    def test_single_app_falls_back_to_its_own_label_without_group_title(self):
        # tests/fixtures/pdf/a1.xml: <app><label>SUPPLEMENTARY MATERIAL</label></app>
        # with no <app-group><title>
        xml = etree.fromstring(
            '<root><app-group>'
            '<app><label>SUPPLEMENTARY MATERIAL</label><p>Texto</p></app>'
            '</app-group></root>'
        )
        self.assertEqual('SUPPLEMENTARY MATERIAL', supplementary_material.extract_data(xml)[0]['title'])

    def test_multiple_apps_with_titles_get_one_section_each(self):
        # ecos/v35n3/1657-4206-ecos-35-03-e294345.xml (3 <app>, "Anexo A/B/C")
        xml = etree.fromstring(
            '<root><app-group>'
            '<app><title>Anexo A</title><p>A</p></app>'
            '<app><title>Anexo B</title><p>B</p></app>'
            '</app-group></root>'
        )
        result = supplementary_material.extract_data(xml)
        self.assertEqual([('Anexo A', 2), ('Anexo B', 2)], _outline(result))

    def test_multiple_apps_without_any_title_stay_merged(self):
        # dilemas/v19n2/2178-2792-dilemas-19-02-e65794.xml: 2 untitled <app>
        xml = etree.fromstring(
            '<root><app-group><app><p>A</p></app><app><p>B</p></app></app-group></root>'
        )
        result = supplementary_material.extract_data(xml)
        self.assertEqual(['Appendix'], [section['title'] for section in result if section['title']])
        self.assertEqual(['A', 'B'], [text for section in result for text in _texts(section)])

    def test_multiple_apps_use_label_when_title_is_missing(self):
        xml = etree.fromstring(
            '<root><app-group>'
            '<app><label>Anexo 1</label><p>A</p></app>'
            '<app><title>Anexo 2</title><p>B</p></app>'
            '</app-group></root>'
        )
        result = supplementary_material.extract_data(xml)
        self.assertEqual(['Anexo 1', 'Anexo 2'], [section['title'] for section in result])

    def test_multiple_apps_falls_back_to_numbered_default_for_the_untitled_one(self):
        xml = etree.fromstring(
            '<root><app-group>'
            '<app><title>Anexo 1</title><p>A</p></app>'
            '<app><p>B</p></app>'
            '</app-group></root>'
        )
        result = supplementary_material.extract_data(xml)
        self.assertEqual(['Anexo 1', 'Appendix 2'], [section['title'] for section in result])

    def test_app_group_in_translation_sub_article_is_skipped(self):
        # Regression: 11 real articles (e.g. codas, rbso) repeated the whole
        # appendix in the translation's language
        xml = etree.fromstring(
            '<root><back><app-group><app><p>Principal</p></app></app-group></back>'
            '<sub-article article-type="translation"><back>'
            '<app-group><app><p>Translation</p></app></app-group>'
            '</back></sub-article></root>'
        )
        result = supplementary_material.extract_data(xml)
        self.assertEqual(['Principal'], [text for section in result for text in _texts(section)])


class TestExtractDataSupplementaryMaterial(unittest.TestCase):

    def test_supplementary_material_with_label_and_media_in_sec(self):
        xml = etree.fromstring(
            '<root xmlns:xlink="http://www.w3.org/1999/xlink">'
            '<body><sec><supplementary-material id="suppl1">'
            '<label>Supplementary Material</label>'
            '<media mime-subtype="mp4" mimetype="video" xlink:href="a-suppl1.mp4"/>'
            '</supplementary-material></sec></body>'
            '</root>'
        )
        result = supplementary_material.extract_data(xml)
        self.assertEqual([('Supplementary Material', 2)], _outline(result))
        self.assertEqual(['Supplementary Material: a-suppl1.mp4 (video/mp4)'], _texts(result[0]))

    def test_heading_uses_sec_title(self):
        # Regression, PR #1384 review: csp/v42/1678-4464-csp-42-EN217725.xml,
        # <title>Material Suplementar</title> came out as "SUPPLEMENTARY MATERIAL"
        xml = etree.fromstring(
            '<root xmlns:xlink="http://www.w3.org/1999/xlink"><back>'
            '<sec sec-type="supplementary-material"><title>Material Suplementar</title>'
            '<supplementary-material id="suppl1"><label>Material Suplementar</label>'
            '<media mime-subtype="pdf" mimetype="application" xlink:href="a-s.pdf"/>'
            '</supplementary-material></sec></back></root>'
        )
        self.assertEqual('Material Suplementar', supplementary_material.extract_data(xml)[0]['title'])

    def test_heading_falls_back_to_sec_label(self):
        # jped/v102n1/0021-7557-jped-102-01-101471.xml: <label>, no <title>
        xml = etree.fromstring(
            '<root><back><sec><label>Supplementary materials</label>'
            '<supplementary-material id="suppl1"><label>Suppl. 1</label></supplementary-material>'
            '</sec></back></root>'
        )
        self.assertEqual('Supplementary materials', supplementary_material.extract_data(xml)[0]['title'])

    def test_heading_ignores_translation_sec_title(self):
        xml = etree.fromstring(
            '<root><back><sec><title>Material suplementar</title>'
            '<supplementary-material id="s1"><label>S1</label></supplementary-material></sec></back>'
            '<sub-article article-type="translation"><back><sec><title>Supplementary Materials</title>'
            '<supplementary-material id="s1-en"><label>S1 EN</label></supplementary-material>'
            '</sec></back></sub-article></root>'
        )
        result = supplementary_material.extract_data(xml)
        self.assertEqual('Material suplementar', result[0]['title'])
        self.assertEqual(['S1'], _texts(result[0]))

    def test_supplementary_material_in_back(self):
        xml = etree.fromstring(
            '<root xmlns:xlink="http://www.w3.org/1999/xlink">'
            '<back><supplementary-material id="suppl1">'
            '<label>Suppl. 1</label>'
            '<media mime-subtype="pdf" mimetype="application" xlink:href="suppl1.pdf"/>'
            '</supplementary-material></back>'
            '</root>'
        )
        result = supplementary_material.extract_data(xml)
        self.assertEqual([('Supplementary Material', 2)], _outline(result))
        self.assertEqual(['Suppl. 1: suppl1.pdf (application/pdf)'], _texts(result[0]))

    def test_multiple_supplementary_material_items(self):
        xml = etree.fromstring(
            '<root xmlns:xlink="http://www.w3.org/1999/xlink">'
            '<back>'
            '<supplementary-material id="suppl1">'
            '<label>Suppl. 1</label>'
            '<media mime-subtype="pdf" mimetype="application" xlink:href="a.pdf"/>'
            '</supplementary-material>'
            '<supplementary-material id="suppl2">'
            '<label>Suppl. 2</label>'
            '<media mime-subtype="xlsx" mimetype="application" xlink:href="b.xlsx"/>'
            '</supplementary-material>'
            '</back>'
            '</root>'
        )
        result = supplementary_material.extract_data(xml)
        self.assertEqual(
            ['Suppl. 1: a.pdf (application/pdf)', 'Suppl. 2: b.xlsx (application/xlsx)'],
            _texts(result[0]),
        )

    def test_sec_paragraphs_and_items_keep_document_order(self):
        # jped/v102n4/0021-7557-jped-102-04-101548.xml: availability/DOI
        # sentence in a <p> of the supplementary-material <sec>
        xml = etree.fromstring(
            '<root xmlns:xlink="http://www.w3.org/1999/xlink">'
            '<body><sec sec-type="supplementary-material">'
            '<title>Supplementary materials</title>'
            '<p>Before.</p>'
            '<supplementary-material id="suppl1"><label>Suppl. 1</label>'
            '<media mime-subtype="pdf" mimetype="application" xlink:href="a.pdf"/>'
            '</supplementary-material>'
            '<p>After.</p>'
            '</sec></body>'
            '</root>'
        )
        result = supplementary_material.extract_data(xml)
        self.assertEqual(['Before.', 'Suppl. 1: a.pdf (application/pdf)', 'After.'], _texts(result[0]))

    def test_sec_paragraph_that_only_wraps_the_item_is_not_duplicated(self):
        # bn/v26n1/1676-0611-bn-26-1-e20251852.xml: <p><supplementary-material/></p>
        xml = etree.fromstring(
            '<root xmlns:xlink="http://www.w3.org/1999/xlink">'
            '<body><sec sec-type="supplementary-material">'
            '<title>Supplementary Material</title>'
            '<p><supplementary-material id="suppl1"><label>Suppl. 1</label>'
            '<media mime-subtype="pdf" mimetype="application" xlink:href="a.pdf"/>'
            '</supplementary-material></p>'
            '</sec></body>'
            '</root>'
        )
        result = supplementary_material.extract_data(xml)
        self.assertEqual(['Suppl. 1: a.pdf (application/pdf)'], _texts(result[0]))

    def test_app_group_and_supplementary_material_are_separate_sections(self):
        # SPS 1.10: "<app-group> e <app> nao comportam <supplementary-material>"
        xml = etree.fromstring(
            '<root xmlns:xlink="http://www.w3.org/1999/xlink">'
            '<back>'
            '<app-group><title>Annex 1</title><app><p>Texto do anexo</p></app></app-group>'
            '<supplementary-material id="suppl1"><label>Suppl. 1</label>'
            '<media mime-subtype="pdf" mimetype="application" xlink:href="a.pdf"/>'
            '</supplementary-material>'
            '</back>'
            '</root>'
        )
        result = supplementary_material.extract_data(xml)
        self.assertEqual(['Annex 1', 'Supplementary Material'], [section['title'] for section in result])


class TestExtractSupplementaryItems(unittest.TestCase):

    def _item(self, inner):
        xml = etree.fromstring(
            '<root xmlns:xlink="http://www.w3.org/1999/xlink"><back>'
            f'<supplementary-material id="suppl1">{inner}</supplementary-material>'
            '</back></root>'
        )
        return supplementary_material.extract_supplementary_items(xml)[0]

    def test_without_label_or_media(self):
        self.assertEqual({
            'type': 'supplementary_item',
            'label': '',
            'caption': '',
            'filename': '',
            'mimetype': '',
            'mime_subtype': '',
            'description': '',
            'notes': '',
        }, self._item(''))

    def test_graphic_instead_of_media(self):
        # SPS 1.10: figura em material suplementar usa <graphic>, nao <media>
        item = self._item(
            '<label>Supplementary material 2</label>'
            '<caption><title>Figure 1</title></caption>'
            '<graphic xlink:href="a-suppl2-gf3.jpg"/>'
        )
        self.assertEqual(('Supplementary material 2', 'Figure 1', 'a-suppl2-gf3.jpg', ''),
                         (item['label'], item['caption'], item['filename'], item['mimetype']))

    def test_extracts_long_desc_from_media(self):
        item = self._item(
            '<media mime-subtype="mp4" mimetype="video" xlink:href="a.mp4">'
            '<long-desc>Descricao detalhada do video.</long-desc></media>'
        )
        self.assertEqual('Descricao detalhada do video.', item['description'])

    def test_falls_back_to_alt_text_without_long_desc(self):
        item = self._item('<graphic xlink:href="gf3.jpg"><alt-text>Breve descricao da figura.</alt-text></graphic>')
        self.assertEqual('Breve descricao da figura.', item['description'])

    def test_prefers_long_desc_over_alt_text(self):
        item = self._item(
            '<media mime-subtype="mp4" mimetype="video" xlink:href="a.mp4">'
            '<alt-text>Breve.</alt-text><long-desc>Detalhada.</long-desc></media>'
        )
        self.assertEqual('Detalhada.', item['description'])

    def test_prefers_media_over_graphic_when_both_present(self):
        item = self._item(
            '<media mime-subtype="mp4" mimetype="video" xlink:href="video.mp4"/>'
            '<graphic xlink:href="thumbnail.jpg"/>'
        )
        self.assertEqual(('video.mp4', 'video'), (item['filename'], item['mimetype']))

    def test_paragraph_with_link_keeps_the_address(self):
        # PR #1384 review: <p>/<ext-link> inside <supplementary-material>
        # were ignored (ijcs/v39/2359-4802-ijcs-39-e20250202.xml, "click here")
        item = self._item(
            '<label>*Supplemental Materials</label>'
            '<media mime-subtype="pdf" mimetype="application" xlink:href="Supp01.pdf"/>'
            '<p>For additional information, please <ext-link ext-link-type="uri" '
            'xlink:href="http://example.org/appendix.pdf">click here</ext-link>.</p>'
        )
        self.assertEqual(
            'For additional information, please click here (http://example.org/appendix.pdf).',
            item['notes'],
        )

    def test_paragraph_with_link_showing_the_address_is_not_repeated(self):
        # abc/v123n8/0066-782x-abc-123-8-e20250718.xml: link text is the URL itself
        item = self._item(
            '<p>Para Tabela Suplementar 1, clique aqui. <ext-link ext-link-type="uri" '
            'xlink:href="https://example.org/t1.pdf">https://example.org/t1.pdf</ext-link></p>'
        )
        self.assertEqual('Para Tabela Suplementar 1, clique aqui. https://example.org/t1.pdf', item['notes'])

    def test_translation_items_are_skipped(self):
        xml = etree.fromstring(
            '<root><back><supplementary-material id="s1"/></back>'
            '<sub-article article-type="translation"><back>'
            '<supplementary-material id="s1-en"/></back></sub-article></root>'
        )
        self.assertEqual(1, len(supplementary_material.extract_supplementary_items(xml)))


class TestFormatItem(unittest.TestCase):

    def test_label_filename_and_media_type(self):
        element = {'label': 'Suppl. 1', 'filename': 'a.pdf', 'mimetype': 'application', 'mime_subtype': 'pdf'}
        self.assertEqual(supplementary_material.format_item(element), 'Suppl. 1: a.pdf (application/pdf)')

    def test_missing_label_falls_back_to_default(self):
        element = {'label': '', 'filename': 'a.pdf', 'mimetype': '', 'mime_subtype': ''}
        self.assertEqual(supplementary_material.format_item(element), 'Supplementary Material: a.pdf')

    def test_missing_filename_shows_only_label(self):
        element = {'label': 'Suppl. 1', 'filename': '', 'mimetype': '', 'mime_subtype': ''}
        self.assertEqual(supplementary_material.format_item(element), 'Suppl. 1')

    def test_missing_everything_uses_default_label_only(self):
        element = {'label': '', 'filename': '', 'mimetype': '', 'mime_subtype': ''}
        self.assertEqual(supplementary_material.format_item(element), 'Supplementary Material')

    def test_includes_caption_when_present(self):
        element = {'label': 'Suppl. 2', 'caption': 'Figure 1', 'filename': 'gf3.jpg', 'mimetype': '', 'mime_subtype': ''}
        self.assertEqual(supplementary_material.format_item(element), 'Suppl. 2 (Figure 1): gf3.jpg')

    def test_includes_description_when_present(self):
        element = {
            'label': 'Suppl. 1', 'filename': 'a.mp4', 'mimetype': 'video', 'mime_subtype': 'mp4',
            'description': 'Descricao detalhada do video.',
        }
        self.assertEqual(
            supplementary_material.format_item(element),
            'Suppl. 1: a.mp4 (video/mp4). Descricao detalhada do video.',
        )

    def test_includes_notes_when_present(self):
        element = {
            'label': 'Suppl. 1', 'filename': 'a.pdf', 'mimetype': '', 'mime_subtype': '',
            'notes': 'Clique aqui (https://example.org/a.pdf).',
        }
        self.assertEqual(
            supplementary_material.format_item(element),
            'Suppl. 1: a.pdf. Clique aqui (https://example.org/a.pdf).',
        )
