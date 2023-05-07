import unittest
from unittest.mock import patch

from lxml import etree as ET
from packtools.sps.models.dates import ArticleDates
from packtools.sps.formats.oai_dc import (
    xml_oai_dc_record_pipe,
    xml_oai_dc_header_pipe,
    add_identifier,
    add_set_spec,
    get_issn,
    xml_oai_dc_metadata,
    setup_oai_dc_header_pipe,
    xml_oai_dc_title,
    xml_oai_dc_creator,
    xml_oai_dc_subject,
    xml_oai_dc_description,
    xml_oai_dc_publisher,
    xml_oai_dc_source,
    xml_oai_dc_date,
    get_date,
    xml_oai_dc_format,
)


class TestPipelineOaiDc(unittest.TestCase):
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
            'article-type="research-article" dtd-version="1.1" '
            'specific-use="sps-1.9" xml:lang="en">'
            '<front>'
            '<journal-meta>'
            '<journal-id journal-id-type="nlm-ta">Rev Esc Enferm USP</journal-id>'
            '<journal-id journal-id-type="publisher-id">reeusp</journal-id>'
            '<journal-title-group>'
            '<journal-title>Revista da Escola de Enfermagem da USP</journal-title>'
            '<abbrev-journal-title abbrev-type="publisher">Rev. esc. enferm. USP</abbrev-journal-title>'
            '</journal-title-group>'
            '<issn pub-type="ppub">0080-6234</issn>'
            '<issn pub-type="epub">1980-220X</issn>'
            '<publisher>'
            '<publisher-name>Universidade de São Paulo, Escola de Enfermagem</publisher-name>'
            '</publisher>'
            '</journal-meta>'
            '<article-meta>'
            '<article-id specific-use="scielo-v3" pub-id-type="publisher-id">ZwzqmpTpbhTmtwR9GfDzP7c</article-id>'
            '<article-id specific-use="scielo-v2" pub-id-type="publisher-id">S0080-62342022000100445</article-id>'
            '<article-id pub-id-type="doi">10.1590/1980-220X-REEUSP-2021-0569en</article-id>'
            '<article-id pub-id-type="other">00445</article-id>'
            '</article-meta>'
            '</front>'
            '</article>'
        )
        expected = (
            '<header>'
            '<identifier>oai:scielo:S0080-62342022000100445</identifier>'
            '<datestamp>2023-04-04</datestamp>'
            '<setSpec>1980-220X</setSpec>'
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
            'article-type="research-article" dtd-version="1.1" '
            'specific-use="sps-1.9" xml:lang="en">'
            '<front>'
            '<article-meta>'
            '<article-id specific-use="scielo-v3" pub-id-type="publisher-id">ZwzqmpTpbhTmtwR9GfDzP7c</article-id>'
            '<article-id specific-use="scielo-v2" pub-id-type="publisher-id">S0080-62342022000100445</article-id>'
            '</article-meta>'
            '</front>'
            '</article>'
        )
        expected = (
            '<identifier>oai:scielo:S0080-62342022000100445</identifier>'
        )

        xml_oai_dc = ET.fromstring(
            '<record/>'
        )

        add_identifier(xml_oai_dc, xml_tree)

        self.obtained = ET.tostring(xml_oai_dc, encoding="utf-8").decode("utf-8")

        self.assertIn(expected, self.obtained)

    def test_get_identifier_not_found(self):
        xml_tree = ET.fromstring(
            '<article xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'xmlns:xlink="http://www.w3.org/1999/xlink" '
            'article-type="research-article" dtd-version="1.1" '
            'specific-use="sps-1.9" xml:lang="en">'
            '<front>'
            '<article-meta>'
            '</article-meta>'
            '</front>'
            '</article>'
        )

        xml_oai_dc = ET.fromstring(
            '<record/>'
        )

        add_identifier(xml_oai_dc, xml_tree)

        self.assertIsNone(xml_oai_dc.find('identifier'))

    def test_get_set_spec(self):
        xml_tree = ET.fromstring(
            '<article xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'xmlns:xlink="http://www.w3.org/1999/xlink" '
            'article-type="research-article" dtd-version="1.1" '
            'specific-use="sps-1.9" xml:lang="en">'
            '<front>'
            '<journal-meta>'
            '<issn pub-type="ppub">0080-6234</issn>'
            '<issn pub-type="epub">1980-220X</issn>'
            '</journal-meta>'
            '</front>'
            '</article>'
        )
        expected = (
            '<setSpec>1980-220X</setSpec>'
        )

        xml_oai_dc = ET.fromstring(
            '<record/>'
        )

        add_set_spec(xml_oai_dc, xml_tree)

        self.obtained = ET.tostring(xml_oai_dc, encoding="utf-8").decode("utf-8")

        self.assertIn(expected, self.obtained)

    def test_get_set_spec_not_found(self):
        xml_tree = ET.fromstring(
            '<article xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'xmlns:xlink="http://www.w3.org/1999/xlink" '
            'article-type="research-article" dtd-version="1.1" '
            'specific-use="sps-1.9" xml:lang="en">'
            '<front>'
            '</front>'
            '</article>'
        )

        xml_oai_dc = ET.fromstring(
            '<record/>'
        )

        add_set_spec(xml_oai_dc, xml_tree)

        self.assertIsNone(xml_oai_dc.find('setSpec'))

    def test_get_issn_epub(self):
        xml_tree = ET.fromstring(
            '<article xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'xmlns:xlink="http://www.w3.org/1999/xlink" '
            'article-type="research-article" dtd-version="1.1" '
            'specific-use="sps-1.9" xml:lang="en">'
            '<front>'
            '<journal-meta>'
            '<issn pub-type="ppub">0080-6234</issn>'
            '<issn pub-type="epub">1980-220X</issn>'
            '</journal-meta>'
            '</front>'
            '</article>'
        )

        self.assertEqual('1980-220X', get_issn(xml_tree))

    def test_get_issn_ppub(self):
        xml_tree = ET.fromstring(
            '<article xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'xmlns:xlink="http://www.w3.org/1999/xlink" '
            'article-type="research-article" dtd-version="1.1" '
            'specific-use="sps-1.9" xml:lang="en">'
            '<front>'
            '<journal-meta>'
            '<issn pub-type="ppub">0080-6234</issn>'
            '</journal-meta>'
            '</front>'
            '</article>'
        )

        self.assertEqual('0080-6234', get_issn(xml_tree))

    def test_get_issn_not_found(self):
        xml_tree = ET.fromstring(
            '<article xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'xmlns:xlink="http://www.w3.org/1999/xlink" '
            'article-type="research-article" dtd-version="1.1" '
            'specific-use="sps-1.9" xml:lang="en">'
            '<front>'
            '<journal-meta>'
            '<issn>0080-6234</issn>'
            '</journal-meta>'
            '</front>'
            '</article>'
        )

        self.assertEqual('', get_issn(xml_tree))

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

    def test_setup_oai_dc_header_pipe(self):
        expected = (
            '<metadata>'
            '<oai-dc:dc xmlns:oai-dc="http://www.openarchives.org/OAI/2.0/oai_dc/" '
            'xmlns:dc="http://purl.org/dc/elements/1.1/" '
            'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
            'xsi:schemaLocation="http://www.openarchives.org/OAI/2.0/oai_dc/ '
            'http://www.openarchives.org/OAI/2.0/oai_dc.xsd"/>'
            '</metadata>'
        )

        xml_oai_dc = ET.fromstring(
            '<metadata>'
            '</metadata>'
        )

        setup_oai_dc_header_pipe(xml_oai_dc)

        self.obtained = ET.tostring(xml_oai_dc, encoding="utf-8").decode("utf-8")

        self.assertIn(expected, self.obtained)


if __name__ == '__main__':
    unittest.main()
