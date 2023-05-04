import unittest
from unittest.mock import patch

from lxml import etree as ET
from packtools.sps.formats.oai_dc import (
    xml_oai_dc_record_pipe,
    xml_oai_dc_header_pipe,
    get_identifier,
    get_set_spec,
    get_issn,
    xml_oai_dc_metadata,
    setup_oai_dc_header_pipe,
)


class PipelineOaiDc(unittest.TestCase):
    def test_xml_oai_dc_record_pipe(self):
        expected = (
            '<record/>'
        )

        xml_oai_dc = xml_oai_dc_record_pipe()

        self.obtained = ET.tostring(xml_oai_dc, encoding="utf-8").decode("utf-8")

        self.assertIn(expected, self.obtained)

    @patch('packtools.sps.formats.oai_dc.get_datestamp')
    def test_xml_oai_dc_header_pipe(self, mock_datestamp):
        xml_tree = ET.fromstring(
            '<article xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'xmlns:xlink="http://www.w3.org/1999/xlink" '
            'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
            '<front>'
            '<journal-meta>'
            '<journal-id>0718-7181</journal-id>'
            '<issn>0718-7181</issn>'
            '</journal-meta>'
            '<article-meta>'
            '<article-id>S0718-71812022000200217</article-id>'
            '<article-id pub-id-type="doi">10.7764/aisth.72.12</article-id>'
            '</article-meta>'
            '</front>'
            '</article>'
        )
        expected = (
            '<header>'
            '<identifier>oai:scielo:S0718-71812022000200217</identifier>'
            '<datestamp>2023-04-04</datestamp>'
            '<setSpec>0718-7181</setSpec>'
            '</header>'
        )

        mock_datestamp.return_value = '2023-04-04'

        xml_oai_dc = ET.fromstring(
            '<record/>'
        )

        xml_oai_dc_header_pipe(xml_oai_dc, xml_tree)

        self.obtained = ET.tostring(xml_oai_dc, encoding="utf-8").decode("utf-8")

        self.assertIn(expected, self.obtained)

    def test_get_identifier(self):
        xml_tree = ET.fromstring(
            '<article xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'xmlns:xlink="http://www.w3.org/1999/xlink" '
            'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
            '<front>'
            '<journal-meta>'
            '<journal-id>0718-7181</journal-id>'
            '<issn>0718-7181</issn>'
            '</journal-meta>'
            '<article-meta>'
            '<article-id>S0718-71812022000200217</article-id>'
            '<article-id pub-id-type="doi">10.7764/aisth.72.12</article-id>'
            '</article-meta>'
            '</front>'
            '</article>'
        )
        expected = (
            '<identifier>oai:scielo:S0718-71812022000200217</identifier>'
        )

        xml_oai_dc = ET.fromstring(
            '<record/>'
        )

        get_identifier(xml_oai_dc, xml_tree)

        self.obtained = ET.tostring(xml_oai_dc, encoding="utf-8").decode("utf-8")

        self.assertIn(expected, self.obtained)

    def test_get_set_spec(self):
        xml_tree = ET.fromstring(
            '<article xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'xmlns:xlink="http://www.w3.org/1999/xlink" '
            'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
            '<front>'
            '<journal-meta>'
            '<journal-id>0718-7181</journal-id>'
            '<issn>0718-7181</issn>'
            '</journal-meta>'
            '<article-meta>'
            '<article-id>S0718-71812022000200217</article-id>'
            '<article-id pub-id-type="doi">10.7764/aisth.72.12</article-id>'
            '</article-meta>'
            '</front>'
            '</article>'
        )
        expected = (
            '<setSpec>0718-7181</setSpec>'
        )

        xml_oai_dc = ET.fromstring(
            '<record/>'
        )

        get_set_spec(xml_oai_dc, xml_tree)

        self.obtained = ET.tostring(xml_oai_dc, encoding="utf-8").decode("utf-8")

        self.assertIn(expected, self.obtained)

    def test_get_issn(self):
        xml_tree = ET.fromstring(
            '<article xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'xmlns:xlink="http://www.w3.org/1999/xlink" '
            'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
            '<front>'
            '<journal-meta>'
            '<journal-id>0718-7181</journal-id>'
            '<issn>0718-7181</issn>'
            '</journal-meta>'
            '<article-meta>'
            '<article-id>S0718-71812022000200217</article-id>'
            '<article-id pub-id-type="doi">10.7764/aisth.72.12</article-id>'
            '</article-meta>'
            '</front>'
            '</article>'
        )

        self.assertEqual('0718-7181', get_issn(xml_tree))

    def test_xml_oai_dc_metadata(self):
        expected = (
            '<metadata/>'
        )

        xml_oai_dc = ET.fromstring(
            '<record/>'
        )

        xml_oai_dc_metadata(xml_oai_dc)

        self.obtained = ET.tostring(xml_oai_dc, encoding="utf-8").decode("utf-8")

        self.assertIn(expected, self.obtained)

