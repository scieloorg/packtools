import unittest

from lxml import etree

from packtools.sps.formats.pdf.pipeline import supplementary_material


class TestExtractData(unittest.TestCase):

    def test_empty_xml_tree(self):
        xml = etree.fromstring("<root></root>")
        result = supplementary_material.extract_data(xml)
        self.assertEqual([], result)

    def test_single_app_group_with_text(self):
        xml = etree.fromstring(
            "<root><app-group><app>Sample text content</app></app-group></root>"
        )
        result = supplementary_material.extract_data(xml)
        self.assertEqual([{
            'title': 'Appendix',
            'elements': [{'content': 'Sample text content', 'type': 'text'}],
        }], result)

    def test_multiple_app_groups(self):
        xml = etree.fromstring(
            "<root>"
            "<app-group><app>Text 1</app></app-group>"
            "<app-group><app>Text 2</app></app-group>"
            "</root>"
        )
        result = supplementary_material.extract_data(xml)
        self.assertEqual(1, len(result))
        self.assertEqual([
            {'content': 'Text 1', 'type': 'text'},
            {'content': 'Text 2', 'type': 'text'}
        ], result[0]['elements'])

    def test_app_group_with_table(self):
        xml = etree.fromstring(
            "<root>"
            "<app-group>"
            "<app>"
            "<table-wrap>"
            "<label>Table 1</label>"
            "<caption><title>Sample Table</title></caption>"
            "</table-wrap>"
            "</app>"
            "</app-group>"
            "</root>"
        )
        result = supplementary_material.extract_data(xml)
        self.assertEqual(1, len(result))
        self.assertEqual(1, len(result[0]['elements']))
        self.assertEqual('table', result[0]['elements'][0]['type'])

    def test_mixed_content_app_group(self):
        xml = etree.fromstring(
            "<root>"
            "<app-group>"
            "<app>Text content</app>"
            "<app><table-wrap><label>Table 1</label></table-wrap></app>"
            "<app>More text</app>"
            "</app-group>"
            "</root>"
        )
        result = supplementary_material.extract_data(xml)
        elements = result[0]['elements']
        self.assertEqual(3, len(elements))
        self.assertEqual('text', elements[0]['type'])
        self.assertEqual('table', elements[1]['type'])
        self.assertEqual('text', elements[2]['type'])

    def test_app_group_uses_its_own_title_when_present(self):
        # SPS 1.10: <app-group><title> e opcional; a terminologia
        # (Apendice/Anexo/etc.) varia por periodico
        xml = etree.fromstring(
            "<root><app-group><title>Anexo</title>"
            "<app>Texto</app></app-group></root>"
        )
        result = supplementary_material.extract_data(xml)
        self.assertEqual('Anexo', result[0]['title'])

    def test_app_group_falls_back_to_default_title_without_title_element(self):
        xml = etree.fromstring(
            "<root><app-group><app>Texto</app></app-group></root>"
        )
        result = supplementary_material.extract_data(xml)
        self.assertEqual('Appendix', result[0]['title'])

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
        self.assertEqual([{
            'title': 'Supplementary Material',
            'elements': [{
                'type': 'supplementary_item',
                'label': 'Supplementary Material',
                'caption': '',
                'filename': 'a-suppl1.mp4',
                'mimetype': 'video',
                'mime_subtype': 'mp4',
                'description': '',
            }],
        }], result)

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
        self.assertEqual(1, len(result[0]['elements']))
        self.assertEqual('suppl1.pdf', result[0]['elements'][0]['filename'])

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
        elements = result[0]['elements']
        self.assertEqual(2, len(elements))
        self.assertEqual('a.pdf', elements[0]['filename'])
        self.assertEqual('b.xlsx', elements[1]['filename'])

    def test_supplementary_material_without_label_or_media(self):
        xml = etree.fromstring(
            '<root><back><supplementary-material id="suppl1"/></back></root>'
        )
        result = supplementary_material.extract_data(xml)
        self.assertEqual([{
            'title': 'Supplementary Material',
            'elements': [{
                'type': 'supplementary_item',
                'label': '',
                'caption': '',
                'filename': '',
                'mimetype': '',
                'mime_subtype': '',
                'description': '',
            }],
        }], result)

    def test_supplementary_material_with_graphic_instead_of_media(self):
        # SPS 1.10: figura em material suplementar usa <graphic>, nao <media>
        xml = etree.fromstring(
            '<root xmlns:xlink="http://www.w3.org/1999/xlink">'
            '<back><supplementary-material id="suppl2">'
            '<label>Supplementary material 2</label>'
            '<caption><title>Figure 1</title></caption>'
            '<graphic xlink:href="a-suppl2-gf3.jpg"/>'
            '</supplementary-material></back>'
            '</root>'
        )
        result = supplementary_material.extract_data(xml)
        self.assertEqual([{
            'type': 'supplementary_item',
            'label': 'Supplementary material 2',
            'caption': 'Figure 1',
            'filename': 'a-suppl2-gf3.jpg',
            'mimetype': '',
            'mime_subtype': '',
            'description': '',
        }], result[0]['elements'])

    def test_supplementary_material_extracts_long_desc_from_media(self):
        # SPS 1.10: <long-desc> e a descricao detalhada de acessibilidade,
        # filha do proprio <media>/<graphic>
        xml = etree.fromstring(
            '<root xmlns:xlink="http://www.w3.org/1999/xlink">'
            '<back><supplementary-material id="suppl1">'
            '<label>Suppl. 1</label>'
            '<media mime-subtype="mp4" mimetype="video" xlink:href="a.mp4">'
            '<long-desc>Descricao detalhada do video.</long-desc>'
            '</media>'
            '</supplementary-material></back>'
            '</root>'
        )
        result = supplementary_material.extract_data(xml)
        self.assertEqual('Descricao detalhada do video.', result[0]['elements'][0]['description'])

    def test_supplementary_material_falls_back_to_alt_text_without_long_desc(self):
        xml = etree.fromstring(
            '<root xmlns:xlink="http://www.w3.org/1999/xlink">'
            '<back><supplementary-material id="suppl2">'
            '<label>Suppl. 2</label>'
            '<graphic xlink:href="gf3.jpg">'
            '<alt-text>Breve descricao da figura.</alt-text>'
            '</graphic>'
            '</supplementary-material></back>'
            '</root>'
        )
        result = supplementary_material.extract_data(xml)
        self.assertEqual('Breve descricao da figura.', result[0]['elements'][0]['description'])

    def test_supplementary_material_prefers_long_desc_over_alt_text(self):
        xml = etree.fromstring(
            '<root xmlns:xlink="http://www.w3.org/1999/xlink">'
            '<back><supplementary-material id="suppl1">'
            '<label>Suppl. 1</label>'
            '<media mime-subtype="mp4" mimetype="video" xlink:href="a.mp4">'
            '<alt-text>Breve.</alt-text>'
            '<long-desc>Detalhada.</long-desc>'
            '</media>'
            '</supplementary-material></back>'
            '</root>'
        )
        result = supplementary_material.extract_data(xml)
        self.assertEqual('Detalhada.', result[0]['elements'][0]['description'])

    def test_supplementary_material_prefers_media_over_graphic_when_both_present(self):
        xml = etree.fromstring(
            '<root xmlns:xlink="http://www.w3.org/1999/xlink">'
            '<back><supplementary-material id="suppl1">'
            '<label>Suppl. 1</label>'
            '<media mime-subtype="mp4" mimetype="video" xlink:href="video.mp4"/>'
            '<graphic xlink:href="thumbnail.jpg"/>'
            '</supplementary-material></back>'
            '</root>'
        )
        result = supplementary_material.extract_data(xml)
        self.assertEqual('video.mp4', result[0]['elements'][0]['filename'])
        self.assertEqual('video', result[0]['elements'][0]['mimetype'])

    def test_supplementary_material_sec_direct_paragraphs_are_recovered(self):
        # Regression, PR #1384 review: extract_body_data excludes the whole
        # <sec sec-type="supplementary-material">, but its direct <p>
        # (e.g. the availability/DOI sentence) was never recaptured anywhere
        # else - reproduced against the real corpus sample
        # jped/v102n4/0021-7557-jped-102-04-101548.xml.
        xml = etree.fromstring(
            '<root xmlns:xlink="http://www.w3.org/1999/xlink">'
            '<body><sec sec-type="supplementary-material">'
            '<title>Supplementary materials</title>'
            '<p>Supplementary material associated with this article can be found online.</p>'
            '<supplementary-material id="suppl1"><label>Suppl. 1</label>'
            '<media mime-subtype="pdf" mimetype="application" xlink:href="a.pdf"/>'
            '</supplementary-material>'
            '</sec></body>'
            '</root>'
        )
        result = supplementary_material.extract_data(xml)
        elements = result[-1]['elements']
        self.assertEqual(elements[0], {
            'content': 'Supplementary material associated with this article can be found online.',
            'type': 'text',
        })
        self.assertEqual(elements[1]['type'], 'supplementary_item')

    def test_supplementary_material_sec_paragraph_that_only_wraps_the_item_is_not_duplicated(self):
        # A <p> whose only child is the <supplementary-material> itself (a
        # real corpus shape, e.g. bn/v26n1/1676-0611-bn-26-1-e20251852.xml)
        # has no text of its own to recover - the item is already captured
        # as a 'supplementary_item' element, recapturing the wrapping <p>
        # would duplicate it as an empty/near-empty 'text' element.
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
        elements = result[-1]['elements']
        self.assertEqual(len(elements), 1)
        self.assertEqual(elements[0]['type'], 'supplementary_item')

    def test_single_app_falls_back_to_its_own_label_without_group_title(self):
        # Regression, PR #1384 review: _app_group_title only looked at
        # <app-group><title>, but most real articles have the title on the
        # single <app> instead - reproduced against
        # tests/fixtures/pdf/a1.xml, <app><label>SUPPLEMENTARY MATERIAL
        # </label></app> with no <app-group><title>.
        xml = etree.fromstring(
            '<root><app-group>'
            '<app><label>SUPPLEMENTARY MATERIAL</label>'
            '<table-wrap><label>Table 1</label></table-wrap>'
            '</app>'
            '</app-group></root>'
        )
        result = supplementary_material.extract_data(xml)
        self.assertEqual('SUPPLEMENTARY MATERIAL', result[0]['title'])

    def test_single_app_falls_back_to_default_without_title_or_label(self):
        xml = etree.fromstring(
            '<root><app-group>'
            '<app><table-wrap><label>Table 1</label></table-wrap></app>'
            '</app-group></root>'
        )
        result = supplementary_material.extract_data(xml)
        self.assertEqual('Appendix', result[0]['title'])

    def test_multiple_apps_with_titles_get_one_section_each(self):
        # Regression, PR #1384 review: an <app-group> with more than one
        # <app>, each with its own <title>, was rendered as a single
        # "Appendix" section - reproduced against the real corpus sample
        # ecos/v35n3/1657-4206-ecos-35-03-e294345.xml (3 <app>, "Anexo A/B/C").
        xml = etree.fromstring(
            '<root><app-group>'
            '<app><title>Anexo A</title><table-wrap><label>Table A</label></table-wrap></app>'
            '<app><title>Anexo B</title><table-wrap><label>Table B</label></table-wrap></app>'
            '</app-group></root>'
        )
        result = supplementary_material.extract_data(xml)
        self.assertEqual(['Anexo A', 'Anexo B'], [s['title'] for s in result])
        self.assertEqual(1, len(result[0]['elements']))
        self.assertEqual(1, len(result[1]['elements']))

    def test_multiple_apps_without_any_title_stay_merged(self):
        # When no <app> in a multi-app group has a title/label to tell them
        # apart, splitting would invent a numbered title with no basis in
        # the source (e.g. dilemas/v19n2/2178-2792-dilemas-19-02-e65794.xml,
        # a real corpus sample with 2 untitled <app>) - stays merged under
        # one shared/default title, as before.
        xml = etree.fromstring(
            '<root><app-group>'
            '<app><table-wrap><label>Table A</label></table-wrap></app>'
            '<app><table-wrap><label>Table B</label></table-wrap></app>'
            '</app-group></root>'
        )
        result = supplementary_material.extract_data(xml)
        self.assertEqual(1, len(result))
        self.assertEqual('Appendix', result[0]['title'])
        self.assertEqual(2, len(result[0]['elements']))

    def test_multiple_apps_use_label_when_title_is_missing(self):
        xml = etree.fromstring(
            '<root><app-group>'
            '<app><label>Anexo 1</label><table-wrap><label>Table A</label></table-wrap></app>'
            '<app><title>Anexo 2</title><table-wrap><label>Table B</label></table-wrap></app>'
            '</app-group></root>'
        )
        result = supplementary_material.extract_data(xml)
        self.assertEqual(['Anexo 1', 'Anexo 2'], [s['title'] for s in result])

    def test_multiple_apps_falls_back_to_numbered_default_for_the_untitled_one(self):
        xml = etree.fromstring(
            '<root><app-group>'
            '<app><title>Anexo 1</title><table-wrap><label>Table A</label></table-wrap></app>'
            '<app><table-wrap><label>Table B</label></table-wrap></app>'
            '</app-group></root>'
        )
        result = supplementary_material.extract_data(xml)
        self.assertEqual(['Anexo 1', 'Appendix 2'], [s['title'] for s in result])

    def test_app_group_and_supplementary_material_are_separate_sections(self):
        # Regression: as duas tags nao aparecem sob o mesmo titulo -
        # SPS 1.10 e explicita que "<app-group> e <app> nao comportam
        # <supplementary-material>", sao conceitos diferentes
        xml = etree.fromstring(
            '<root xmlns:xlink="http://www.w3.org/1999/xlink">'
            '<back>'
            '<app-group><title>Annex 1</title><app>Texto do anexo</app></app-group>'
            '<supplementary-material id="suppl1"><label>Suppl. 1</label>'
            '<media mime-subtype="pdf" mimetype="application" xlink:href="a.pdf"/>'
            '</supplementary-material>'
            '</back>'
            '</root>'
        )
        result = supplementary_material.extract_data(xml)
        self.assertEqual(2, len(result))
        self.assertEqual('Annex 1', result[0]['title'])
        self.assertEqual('Supplementary Material', result[1]['title'])


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
