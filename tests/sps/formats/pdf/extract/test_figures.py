import unittest

from lxml import etree

from packtools.sps.formats.pdf.extract import figures


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
        result = figures.extract_figure_data(xml)
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
        result = figures.extract_figure_data(xml)
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
        result = figures.extract_figure_data(xml)
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
        result = figures.extract_figure_data(xml)
        self.assertEqual(result['href'], 'raw.tif')


class TestExtractFigureDataCaption(unittest.TestCase):

    def test_caption_joins_title_and_paragraphs(self):
        xml = etree.fromstring(
            '<fig><label> Figure 2 </label><caption><title>Título</title>'
            '<p>Primeiro <italic>p</italic>.</p><p> </p><p>Segundo.</p></caption></fig>'
        )
        result = figures.extract_figure_data(xml)
        self.assertEqual(result['label'], 'Figure 2')
        self.assertEqual(result['caption'], 'Título Primeiro p. Segundo.')

    def test_missing_label_caption_and_graphic(self):
        result = figures.extract_figure_data(etree.fromstring('<fig/>'))
        self.assertEqual(result, {'label': '', 'caption': '', 'href': None, 'alt': ''})

    def test_alt_text_from_direct_graphic(self):
        xml = etree.fromstring(
            '<fig xmlns:xlink="http://www.w3.org/1999/xlink"><graphic xlink:href="a.png" alt="descrição"/></fig>'
        )
        self.assertEqual(figures.extract_figure_data(xml)['alt'], 'descrição')


class TestExtractFigureDataAlternativesRanking(unittest.TestCase):

    def _href(self, graphics):
        xml = etree.fromstring(
            f'<fig xmlns:xlink="http://www.w3.org/1999/xlink"><alternatives>{graphics}</alternatives></fig>'
        )
        return figures.extract_figure_data(xml)

    def test_graphic_without_href_is_ignored(self):
        self.assertEqual(self._href('<graphic/><graphic xlink:href="b.jpg"/>')['href'], 'b.jpg')

    def test_larger_area_wins(self):
        result = self._href(
            '<graphic xlink:href="small.png" content-type="scielo-100x100"/>'
            '<graphic xlink:href="big.png" content-type="scielo-800x600"/>'
        )
        self.assertEqual(result['href'], 'big.png')

    def test_better_extension_wins_on_tie(self):
        self.assertEqual(self._href('<graphic xlink:href="a.tif"/><graphic xlink:href="a.png"/>')['href'], 'a.png')

    def test_alt_comes_from_chosen_candidate(self):
        result = self._href('<graphic xlink:href="a.png" alt-text="alt a"/>')
        self.assertEqual(result['alt'], 'alt a')

    def test_no_usable_candidate_leaves_href_none(self):
        self.assertIsNone(self._href('<graphic/>')['href'])
