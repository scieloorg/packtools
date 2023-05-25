import unittest
from unittest.mock import patch

from lxml import etree as ET
from packtools.sps.utils import xml_utils
from packtools.sps.models.dates import ArticleDates
from packtools.sps.formats.oai_dc_agris import (
    xml_oai_dc_agris_record_pipe,
    xml_oai_dc_agris_header_pipe,
    get_identifier,
    add_identifier,
    add_set_spec,
    get_issn,
    xml_oai_dc_agris_metadata_pipe,
    xml_oai_dc_agris_resouce_pipe,
    xml_oai_dc_agris_title_pipe,
    xml_oai_dc_agris_creator_pipe,
    xml_oai_dc_agris_publisher_pipe,
    xml_oai_dc_agris_date_pipe,
    xml_oai_dc_agris_subject_pipe,
    xml_oai_dc_agris_description_pipe,
    xml_oai_dc_agris_identifier_pipe,
    xml_oai_dc_agris_type_pipe,
    xml_oai_dc_agris_format_pipe,
    xml_oai_dc_agris_language_pipe,
    xml_oai_dc_agris_availability_pipe,
    xml_oai_dc_agris_citation_pipe,
)


class TestPipelineOaiDcAgris(unittest.TestCase):
    def test_xml_oai_dc_agris_record_pipe(self):
        expected = (
            '<record/>'
        )

        xml_oai_dc_agris = xml_oai_dc_agris_record_pipe()

        self.obtained = ET.tostring(xml_oai_dc_agris, encoding="utf-8").decode("utf-8")

        self.assertIn(expected, self.obtained)

    def test_get_identifier(self):
        xml_tree = ET.fromstring(
            '<article xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'xmlns:xlink="http://www.w3.org/1999/xlink" '
            'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
            '<front>'
            '<article-meta>'
            '<article-id specific-use="scielo-v2" pub-id-type="publisher-id">S0718-71812021000100011</article-id>'
            '<article-id pub-id-type="doi">10.7764/69.1</article-id>'
            '</article-meta>'
            '</front>'
            '</article>'
        )

        self.assertEqual('2021000111', get_identifier(xml_tree))

    def test_add_identifier(self):
        xml_tree = ET.fromstring(
            '<article xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'xmlns:xlink="http://www.w3.org/1999/xlink" '
            'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
            '<front>'
            '<article-meta>'
            '<article-id specific-use="scielo-v2" pub-id-type="publisher-id">S0718-71812021000100011</article-id>'
            '<article-id pub-id-type="doi">10.7764/69.1</article-id>'
            '</article-meta>'
            '</front>'
            '</article>'
        )
        expected = (
            '<identifier>oai:agris.scielo:XS2021000111</identifier>'
        )

        xml_oai_dc_agris = ET.fromstring(
            '<record/>'
        )

        add_identifier(xml_oai_dc_agris, xml_tree)

        self.obtained = ET.tostring(xml_oai_dc_agris, encoding="utf-8").decode("utf-8")

        self.assertIn(expected, self.obtained)

    def test_add_identifier_not_found(self):
        xml_tree = ET.fromstring(
            '<article xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'xmlns:xlink="http://www.w3.org/1999/xlink" '
            'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
            '<front>'
            '<article-meta>'
            '<article-id pub-id-type="doi">10.7764/69.1</article-id>'
            '</article-meta>'
            '</front>'
            '</article>'
        )

        xml_oai_dc_agris = ET.fromstring(
            '<record/>'
        )

        add_identifier(xml_oai_dc_agris, xml_tree)

        self.assertIsNone(xml_oai_dc_agris.find('identifier'))

    def test_add_set_spec(self):
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

        xml_oai_dc_agris = ET.fromstring(
            '<record/>'
        )

        add_set_spec(xml_oai_dc_agris, xml_tree)

        self.obtained = ET.tostring(xml_oai_dc_agris, encoding="utf-8").decode("utf-8")

        self.assertIn(expected, self.obtained)

    def test_add_set_spec_not_found(self):
        xml_tree = ET.fromstring(
            '<article xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'xmlns:xlink="http://www.w3.org/1999/xlink" '
            'article-type="research-article" dtd-version="1.1" '
            'specific-use="sps-1.9" xml:lang="en">'
            '<front>'
            '</front>'
            '</article>'
        )

        xml_oai_dc_agris = ET.fromstring(
            '<record/>'
        )

        add_set_spec(xml_oai_dc_agris, xml_tree)

        self.assertIsNone(xml_oai_dc_agris.find('setSpec'))

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

    def test_xml_oai_dc_agris_header_pipe(self):
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
            '<article-meta>'
            '<article-id specific-use="scielo-v2" pub-id-type="publisher-id">S0718-71812021000100011</article-id>'
            '<article-id pub-id-type="doi">10.7764/69.1</article-id>'
            '</article-meta>'
            '</front>'
            '</article>'
        )

        expected = (
            '<identifier>oai:agris.scielo:XS2021000111</identifier>'
            '<setSpec>1980-220X</setSpec>'
        )

        xml_oai_dc_agris = ET.fromstring(
            '<record>'
            '</record>'
        )

        xml_oai_dc_agris_header_pipe(xml_oai_dc_agris, xml_tree)

        self.obtained = ET.tostring(xml_oai_dc_agris, encoding="utf-8").decode("utf-8")

        self.assertIn(expected, self.obtained)

    def test_xml_oai_dc_agris_metadata_pipe(self):
        expected = (
            '<ags:resources '
            'xmlns:xsl="http://www.w3.org/1999/XSL/Transform" '
            'xmlns:ags="http://purl.org/agmes/1.1/" '
            'xmlns:dc="http://purl.org/dc/elements/1.1/" '
            'xmlns:agls="http://www.naa.gov.au/recordkeeping/gov_online/agls/1.2" '
            'xmlns:dcterms="http://purl.org/dc/terms/"/>'
        )

        xml_oai_dc_agris = ET.fromstring(
            '<record>'
            '</record>'
        )

        xml_oai_dc_agris_metadata_pipe(xml_oai_dc_agris)

        self.obtained = ET.tostring(xml_oai_dc_agris, encoding="utf-8").decode("utf-8")

        self.assertIn(expected, self.obtained)

