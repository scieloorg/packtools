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
