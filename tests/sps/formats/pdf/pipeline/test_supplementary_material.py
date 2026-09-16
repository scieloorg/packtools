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
        }], result[0]['elements'])

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
