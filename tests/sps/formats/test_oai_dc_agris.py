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

    def test_xml_oai_dc_agris_resouce_pipe(self):
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
            '<ags:resource ags:ARN="XS2021000111"/>'
        )

        xml_oai_dc_agris = ET.fromstring(
            '<record>'
            '<metadata>'
            '<ags:resources '
            'xmlns:xsl="http://www.w3.org/1999/XSL/Transform" '
            'xmlns:ags="http://purl.org/agmes/1.1/" '
            'xmlns:dc="http://purl.org/dc/elements/1.1/" '
            'xmlns:agls="http://www.naa.gov.au/recordkeeping/gov_online/agls/1.2" '
            'xmlns:dcterms="http://purl.org/dc/terms/">'
            '</ags:resources>'
            '</metadata>'
            '</record>'
        )

        xml_oai_dc_agris_resouce_pipe(xml_oai_dc_agris, xml_tree)

        self.obtained = ET.tostring(xml_oai_dc_agris, encoding="utf-8").decode("utf-8")

        self.assertIn(expected, self.obtained)

    def test_xml_oai_dc_agris_title_pipe(self):
        xml_tree = ET.fromstring(
            '<article '
            'xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'xmlns:xlink="http://www.w3.org/1999/xlink" '
            'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xml:lang="es">'
            '<front>'
            '<article-meta>'
            '<article-id>S0718-71812021000100011</article-id>'
            '<article-id pub-id-type="doi">10.7764/69.1</article-id>'
            '<title-group>'
            '<article-title xml:lang="es">'
            '<![CDATA[ La canción reflexiva: en torno al estatuto crítico de la música popular en Brasil ]]>'
            '</article-title>'
            '<article-title xml:lang="en">'
            '<![CDATA[ The Critical Song: On the Debate of the Reflective Status of Brazilian Popular Music ]]>'
            '</article-title>'
            '</title-group>'
            '</article-meta>'
            '</front>'
            '</article>'
        )

        expected = (
            '<dc:title xml:lang="es">'
            'La canción reflexiva: en torno al estatuto crítico de la música popular en Brasil'
            '</dc:title>'
        )

        xml_oai_dc_agris = ET.fromstring(

            '<metadata>'
            '<ags:resources '
            'xmlns:xsl="http://www.w3.org/1999/XSL/Transform" '
            'xmlns:ags="http://purl.org/agmes/1.1/" '
            'xmlns:dc="http://purl.org/dc/elements/1.1/" '
            'xmlns:agls="http://www.naa.gov.au/recordkeeping/gov_online/agls/1.2" '
            'xmlns:dcterms="http://purl.org/dc/terms/">'
            '<ags:resource ags:ARN="XS2021000111">'
            '</ags:resource>'
            '</ags:resources>'
            '</metadata>'

        )

        xml_oai_dc_agris_title_pipe(xml_oai_dc_agris, xml_tree)

        self.obtained = ET.tostring(xml_oai_dc_agris, encoding="utf-8").decode("utf-8")

        self.assertIn(expected, self.obtained)

    def test_xml_oai_dc_agris_title_pipe_without_title(self):
        xml_tree = ET.fromstring(
            '<article '
            'xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'xmlns:xlink="http://www.w3.org/1999/xlink" '
            'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xml:lang="es">'
            '<front>'
            '<article-meta>'
            '<article-id>S0718-71812021000100011</article-id>'
            '<article-id pub-id-type="doi">10.7764/69.1</article-id>'
            '</article-meta>'
            '</front>'
            '</article>'
        )

        expected = (
            '<metadata>'
            '<ags:resources '
            'xmlns:xsl="http://www.w3.org/1999/XSL/Transform" '
            'xmlns:ags="http://purl.org/agmes/1.1/" '
            'xmlns:dc="http://purl.org/dc/elements/1.1/" '
            'xmlns:agls="http://www.naa.gov.au/recordkeeping/gov_online/agls/1.2" '
            'xmlns:dcterms="http://purl.org/dc/terms/">'
            '<ags:resource ags:ARN="XS2021000111"/>'
            '</ags:resources>'
            '</metadata>'
        )

        xml_oai_dc_agris = ET.fromstring(
            '<metadata>'
            '<ags:resources '
            'xmlns:xsl="http://www.w3.org/1999/XSL/Transform" '
            'xmlns:ags="http://purl.org/agmes/1.1/" '
            'xmlns:dc="http://purl.org/dc/elements/1.1/" '
            'xmlns:agls="http://www.naa.gov.au/recordkeeping/gov_online/agls/1.2" '
            'xmlns:dcterms="http://purl.org/dc/terms/">'
            '<ags:resource ags:ARN="XS2021000111">'
            '</ags:resource>'
            '</ags:resources>'
            '</metadata>'
        )

        xml_oai_dc_agris_title_pipe(xml_oai_dc_agris, xml_tree)

        self.obtained = ET.tostring(xml_oai_dc_agris, encoding="utf-8").decode("utf-8")

        self.assertEqual(expected, self.obtained)

    def test_xml_oai_dc_agris_title_pipe_without_lang(self):
        xml_tree = ET.fromstring(
            '<article '
            'xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'xmlns:xlink="http://www.w3.org/1999/xlink" '
            'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
            '<front>'
            '<article-meta>'
            '<article-id>S0718-71812021000100011</article-id>'
            '<article-id pub-id-type="doi">10.7764/69.1</article-id>'
            '<title-group>'
            '<article-title xml:lang="es">'
            '<![CDATA[ La canción reflexiva: en torno al estatuto crítico de la música popular en Brasil ]]>'
            '</article-title>'
            '<article-title xml:lang="en">'
            '<![CDATA[ The Critical Song: On the Debate of the Reflective Status of Brazilian Popular Music ]]>'
            '</article-title>'
            '</title-group>'
            '</article-meta>'
            '</front>'
            '</article>'
        )

        expected = (
            '<metadata>'
            '<ags:resources '
            'xmlns:xsl="http://www.w3.org/1999/XSL/Transform" '
            'xmlns:ags="http://purl.org/agmes/1.1/" '
            'xmlns:dc="http://purl.org/dc/elements/1.1/" '
            'xmlns:agls="http://www.naa.gov.au/recordkeeping/gov_online/agls/1.2" '
            'xmlns:dcterms="http://purl.org/dc/terms/">'
            '<ags:resource ags:ARN="XS2021000111"/>'
            '</ags:resources>'
            '</metadata>'
        )

        xml_oai_dc_agris = ET.fromstring(

            '<metadata>'
            '<ags:resources '
            'xmlns:xsl="http://www.w3.org/1999/XSL/Transform" '
            'xmlns:ags="http://purl.org/agmes/1.1/" '
            'xmlns:dc="http://purl.org/dc/elements/1.1/" '
            'xmlns:agls="http://www.naa.gov.au/recordkeeping/gov_online/agls/1.2" '
            'xmlns:dcterms="http://purl.org/dc/terms/">'
            '<ags:resource ags:ARN="XS2021000111">'
            '</ags:resource>'
            '</ags:resources>'
            '</metadata>'

        )

        xml_oai_dc_agris_title_pipe(xml_oai_dc_agris, xml_tree)

        self.obtained = ET.tostring(xml_oai_dc_agris, encoding="utf-8").decode("utf-8")

        self.assertEqual(expected, self.obtained)

    def test_xml_oai_dc_agris_creator_pipe(self):
        xml_tree = ET.fromstring(
            '<article '
            'xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'xmlns:xlink="http://www.w3.org/1999/xlink" '
            'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xml:lang="es">'
            '<front>'
            '<article-meta>'
            '<article-id>S0718-71812021000100011</article-id>'
            '<article-id pub-id-type="doi">10.7764/69.1</article-id>'
            '<contrib-group>'
            '<contrib contrib-type="author">'
            '<name>'
            '<surname>'
            '<![CDATA[ de-Oliveira-Gerolamo ]]>'
            '</surname>'
            '<given-names>'
            '<![CDATA[ Ismael ]]>'
            '</given-names>'
            '</name>'
            '<xref ref-type="aff" rid="Aff"/>'
            '</contrib>'
            '</contrib-group>'
            '</article-meta>'
            '</front>'
            '</article>'
        )

        expected = (
            '<dc:creator>'
            '<ags:creatorPersonal>de-Oliveira-Gerolamo, Ismael</ags:creatorPersonal>'
            '</dc:creator>'
        )

        xml_oai_dc_agris = ET.fromstring(

            '<metadata>'
            '<ags:resources '
            'xmlns:xsl="http://www.w3.org/1999/XSL/Transform" '
            'xmlns:ags="http://purl.org/agmes/1.1/" '
            'xmlns:dc="http://purl.org/dc/elements/1.1/" '
            'xmlns:agls="http://www.naa.gov.au/recordkeeping/gov_online/agls/1.2" '
            'xmlns:dcterms="http://purl.org/dc/terms/">'
            '<ags:resource ags:ARN="XS2021000111">'
            '</ags:resource>'
            '</ags:resources>'
            '</metadata>'

        )

        xml_oai_dc_agris_creator_pipe(xml_oai_dc_agris, xml_tree)

        self.obtained = ET.tostring(xml_oai_dc_agris, encoding="utf-8").decode("utf-8")

        self.assertIn(expected, self.obtained)

    def test_xml_oai_dc_agris_creator_pipe_without_creator(self):
        xml_tree = ET.fromstring(
            '<article '
            'xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'xmlns:xlink="http://www.w3.org/1999/xlink" '
            'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xml:lang="es">'
            '<front>'
            '<article-meta>'
            '<article-id>S0718-71812021000100011</article-id>'
            '<article-id pub-id-type="doi">10.7764/69.1</article-id>'
            '</article-meta>'
            '</front>'
            '</article>'
        )

        expected = (
            '<metadata>'
            '<ags:resources '
            'xmlns:xsl="http://www.w3.org/1999/XSL/Transform" '
            'xmlns:ags="http://purl.org/agmes/1.1/" '
            'xmlns:dc="http://purl.org/dc/elements/1.1/" '
            'xmlns:agls="http://www.naa.gov.au/recordkeeping/gov_online/agls/1.2" '
            'xmlns:dcterms="http://purl.org/dc/terms/">'
            '<ags:resource ags:ARN="XS2021000111"/>'
            '</ags:resources>'
            '</metadata>'
        )

        xml_oai_dc_agris = ET.fromstring(

            '<metadata>'
            '<ags:resources '
            'xmlns:xsl="http://www.w3.org/1999/XSL/Transform" '
            'xmlns:ags="http://purl.org/agmes/1.1/" '
            'xmlns:dc="http://purl.org/dc/elements/1.1/" '
            'xmlns:agls="http://www.naa.gov.au/recordkeeping/gov_online/agls/1.2" '
            'xmlns:dcterms="http://purl.org/dc/terms/">'
            '<ags:resource ags:ARN="XS2021000111">'
            '</ags:resource>'
            '</ags:resources>'
            '</metadata>'

        )

        xml_oai_dc_agris_creator_pipe(xml_oai_dc_agris, xml_tree)

        self.obtained = ET.tostring(xml_oai_dc_agris, encoding="utf-8").decode("utf-8")

        self.assertEqual(expected, self.obtained)

    def test_xml_oai_dc_agris_publisher(self):
        xml_tree = ET.fromstring(
            '<article '
            'xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'xmlns:xlink="http://www.w3.org/1999/xlink" '
            'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xml:lang="es">'
            '<front>'
            '<journal-meta>'
            '<publisher>'
            '<publisher-name>'
            '<![CDATA[ Pontificia Universidad Católica de Chile, Facultad de Filosofía, Instituto de Estética ]]>'
            '</publisher-name>'
            '</publisher>'
            '</journal-meta>'
            '</front>'
            '</article>'
        )

        expected = (
            '<dc:publisher>'
            '<ags:publisherName>Pontificia Universidad Católica de Chile, Facultad de Filosofía, Instituto de Estética</ags:publisherName>'
            '</dc:publisher>'
        )

        xml_oai_dc_agris = ET.fromstring(

            '<metadata>'
            '<ags:resources '
            'xmlns:xsl="http://www.w3.org/1999/XSL/Transform" '
            'xmlns:ags="http://purl.org/agmes/1.1/" '
            'xmlns:dc="http://purl.org/dc/elements/1.1/" '
            'xmlns:agls="http://www.naa.gov.au/recordkeeping/gov_online/agls/1.2" '
            'xmlns:dcterms="http://purl.org/dc/terms/">'
            '<ags:resource ags:ARN="XS2021000111">'
            '</ags:resource>'
            '</ags:resources>'
            '</metadata>'

        )

        xml_oai_dc_agris_publisher_pipe(xml_oai_dc_agris, xml_tree)

        self.obtained = ET.tostring(xml_oai_dc_agris, encoding="utf-8").decode("utf-8")

        self.assertIn(expected, self.obtained)

    def test_xml_oai_dc_agris_publisher_without_publisher(self):
        xml_tree = ET.fromstring(
            '<article '
            'xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'xmlns:xlink="http://www.w3.org/1999/xlink" '
            'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xml:lang="es">'
            '<front>'
            '<journal-meta>'
            '</journal-meta>'
            '</front>'
            '</article>'
        )

        expected = (
            '<metadata>'
            '<ags:resources '
            'xmlns:xsl="http://www.w3.org/1999/XSL/Transform" '
            'xmlns:ags="http://purl.org/agmes/1.1/" '
            'xmlns:dc="http://purl.org/dc/elements/1.1/" '
            'xmlns:agls="http://www.naa.gov.au/recordkeeping/gov_online/agls/1.2" '
            'xmlns:dcterms="http://purl.org/dc/terms/">'
            '<ags:resource ags:ARN="XS2021000111"/>'
            '</ags:resources>'
            '</metadata>'
        )

        xml_oai_dc_agris = ET.fromstring(

            '<metadata>'
            '<ags:resources '
            'xmlns:xsl="http://www.w3.org/1999/XSL/Transform" '
            'xmlns:ags="http://purl.org/agmes/1.1/" '
            'xmlns:dc="http://purl.org/dc/elements/1.1/" '
            'xmlns:agls="http://www.naa.gov.au/recordkeeping/gov_online/agls/1.2" '
            'xmlns:dcterms="http://purl.org/dc/terms/">'
            '<ags:resource ags:ARN="XS2021000111">'
            '</ags:resource>'
            '</ags:resources>'
            '</metadata>'

        )

        xml_oai_dc_agris_publisher_pipe(xml_oai_dc_agris, xml_tree)

        self.obtained = ET.tostring(xml_oai_dc_agris, encoding="utf-8").decode("utf-8")

        self.assertEqual(expected, self.obtained)

    def test_xml_oai_dc_agris_date(self):
        xml_tree = ET.fromstring(
            '<article '
            'xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'xmlns:xlink="http://www.w3.org/1999/xlink" '
            'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xml:lang="es">'
            '<front>'
            '<article-meta>'
            '<pub-date pub-type="pub">'
            '<day>00</day>'
            '<month>07</month>'
            '<year>2021</year>'
            '</pub-date>'
            '<pub-date pub-type="epub">'
            '<day>00</day>'
            '<month>07</month>'
            '<year>2021</year>'
            '</pub-date>'
            '</article-meta>'
            '</front>'
            '</article>'
        )

        expected = (
            '<dc:date>'
            '<dcterms:dateIssued>2021</dcterms:dateIssued>'
            '</dc:date>'
        )

        xml_oai_dc_agris = ET.fromstring(

            '<metadata>'
            '<ags:resources '
            'xmlns:xsl="http://www.w3.org/1999/XSL/Transform" '
            'xmlns:ags="http://purl.org/agmes/1.1/" '
            'xmlns:dc="http://purl.org/dc/elements/1.1/" '
            'xmlns:agls="http://www.naa.gov.au/recordkeeping/gov_online/agls/1.2" '
            'xmlns:dcterms="http://purl.org/dc/terms/">'
            '<ags:resource ags:ARN="XS2021000111">'
            '</ags:resource>'
            '</ags:resources>'
            '</metadata>'

        )

        xml_oai_dc_agris_date_pipe(xml_oai_dc_agris, xml_tree)

        self.obtained = ET.tostring(xml_oai_dc_agris, encoding="utf-8").decode("utf-8")

        self.assertIn(expected, self.obtained)

    def test_xml_oai_dc_agris_datewithout_date(self):
        xml_tree = ET.fromstring(
            '<article '
            'xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'xmlns:xlink="http://www.w3.org/1999/xlink" '
            'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xml:lang="es">'
            '<front>'
            '<article-meta>'
            '</article-meta>'
            '</front>'
            '</article>'
        )

        expected = (
            '<metadata>'
            '<ags:resources '
            'xmlns:xsl="http://www.w3.org/1999/XSL/Transform" '
            'xmlns:ags="http://purl.org/agmes/1.1/" '
            'xmlns:dc="http://purl.org/dc/elements/1.1/" '
            'xmlns:agls="http://www.naa.gov.au/recordkeeping/gov_online/agls/1.2" '
            'xmlns:dcterms="http://purl.org/dc/terms/">'
            '<ags:resource ags:ARN="XS2021000111"/>'
            '</ags:resources>'
            '</metadata>'
        )

        xml_oai_dc_agris = ET.fromstring(
            '<metadata>'
            '<ags:resources '
            'xmlns:xsl="http://www.w3.org/1999/XSL/Transform" '
            'xmlns:ags="http://purl.org/agmes/1.1/" '
            'xmlns:dc="http://purl.org/dc/elements/1.1/" '
            'xmlns:agls="http://www.naa.gov.au/recordkeeping/gov_online/agls/1.2" '
            'xmlns:dcterms="http://purl.org/dc/terms/">'
            '<ags:resource ags:ARN="XS2021000111">'
            '</ags:resource>'
            '</ags:resources>'
            '</metadata>'
        )

        xml_oai_dc_agris_date_pipe(xml_oai_dc_agris, xml_tree)

        self.obtained = ET.tostring(xml_oai_dc_agris, encoding="utf-8").decode("utf-8")

        self.assertEqual(expected, self.obtained)

    def test_xml_oai_dc_agris_subject_pipe(self):
        xml_tree = ET.fromstring(
            '<article '
            'xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'xmlns:xlink="http://www.w3.org/1999/xlink" '
            'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xml:lang="es">'
            '<front>'
            '<article-meta>'
            '<kwd-group xml:lang="es">'
            '<title>DESCRIPTORES</title>'
            '<kwd>Canción popular</kwd>'
            '<kwd>música popular brasileña</kwd>'
            '<kwd>canción crítica</kwd>'
            '<kwd>arte político</kwd>'
            '</kwd-group>'
            '<kwd-group xml:lang="en">'
            '<title>DESCRIPTORS</title>'
            '<kwd>Popular song</kwd>'
            '<kwd>critical song</kwd>'
            '<kwd>Brazilian popular music</kwd>'
            '<kwd>art and politics</kwd>'
            '</kwd-group>'
            '</article-meta>'
            '</front>'
            '</article>'
        )

        expected = (
            '<dc:subject xml:lang="es">Canción popular</dc:subject>'
            '<dc:subject xml:lang="es">música popular brasileña</dc:subject>'
            '<dc:subject xml:lang="es">canción crítica</dc:subject>'
            '<dc:subject xml:lang="es">arte político</dc:subject>'
            '<dc:subject xml:lang="en">Popular song</dc:subject>'
            '<dc:subject xml:lang="en">critical song</dc:subject>'
            '<dc:subject xml:lang="en">Brazilian popular music</dc:subject>'
            '<dc:subject xml:lang="en">art and politics</dc:subject>'
        )

        xml_oai_dc_agris = ET.fromstring(

            '<metadata>'
            '<ags:resources '
            'xmlns:xsl="http://www.w3.org/1999/XSL/Transform" '
            'xmlns:ags="http://purl.org/agmes/1.1/" '
            'xmlns:dc="http://purl.org/dc/elements/1.1/" '
            'xmlns:agls="http://www.naa.gov.au/recordkeeping/gov_online/agls/1.2" '
            'xmlns:dcterms="http://purl.org/dc/terms/">'
            '<ags:resource ags:ARN="XS2021000111">'
            '</ags:resource>'
            '</ags:resources>'
            '</metadata>'

        )

        xml_oai_dc_agris_subject_pipe(xml_oai_dc_agris, xml_tree)

        self.obtained = ET.tostring(xml_oai_dc_agris, encoding="utf-8").decode("utf-8")

        self.assertIn(expected, self.obtained)

    def test_xml_oai_dc_agris_description_pipe(self):
        xml_tree = ET.fromstring(
            '<article '
            'xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'xmlns:xlink="http://www.w3.org/1999/xlink" '
            'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xml:lang="en">'
            '<front>'
            '<article-meta>'
            '<abstract>'
            '<title>Abstract</title>'
            '<sec>'
            '<title>Objective:</title>'
            '<p>to assess the effects of an educational intervention on smoking cessation aimed at the nursing team.</p>'
            '</sec>'
            '<sec>'
            '<title>Method:</title>'
            '<p>this is a quasi-experimental study with 37 nursing professionals from a Brazilian hospital from May/2019 to December/2020. The intervention consisted of training nursing professionals on approaches to hospitalized smokers divided into two steps, the first, online, a prerequisite for the face-to-face/videoconference. The effect of the intervention was assessed through pre- and post-tests completed by participants. Smokers’ medical records were also analyzed. For analysis, McNemar’s chi-square test was used.</p>'
            '</sec>'
            '<sec>'
            '<title>Results:</title>'
            '<p>there was an increase in the frequency of actions aimed at smoking cessation after the intervention. Significant differences were found in guidelines related to disclosure to family members of their decision to quit smoking and the need for support, encouragement of abstinence after hospital discharge, and information on tobacco cessation and relapse strategies.</p>'
            '</sec>'
            '<sec>'
            '<title>Conclusion:</title>'
            '<p>the educational intervention proved to be innovative and with a great capacity for disseminating knowledge. The post-test showed a positive effect on the frequency of actions aimed at smoking cessation implemented by the nursing team.</p>'
            '</sec>'
            '</abstract>'
            '<trans-abstract xml:lang="es">'
            '<title>RESUMEN</title>'
            '<sec>'
            '<title>Objetivo:</title>'
            '<p>evaluar los efectos de una intervención educativa para dejar de fumar dirigida al equipo de enfermería.</p>'
            '</sec>'
            '<sec>'
            '<title>Método:</title>'
            '<p>estudio cuasi-experimental con 37 profesionales de enfermería de un hospital brasileño de mayo/2019 a diciembre/2020. La intervención consistió en capacitar a los profesionales de enfermería en el abordaje del paciente fumador, dividida en dos etapas, la primera, en línea, requisito previo para la presencial/videoconferencia. El efecto de la intervención se evaluó a través del pre y post test realizado por los participantes. También se analizaron los registros en las historias clínicas de los fumadores. Para el análisis se utilizó la prueba Chi-Square de McNemar.</p>'
            '</sec>'
            '<sec>'
            '<title>Resultados:</title>'
            '<p>hubo un aumento en la frecuencia de acciones dirigidas a dejar de fumar después de la intervención. Se encontraron diferencias significativas en las guías relacionadas con la divulgación a los familiares de la decisión de dejar de fumar y la necesidad de apoyo, el estímulo de la abstinencia después del alta hospitalaria y la información sobre estrategias para dejar de fumar y recaer.</p>'
            '</sec>'
            '<sec>'
            '<title>Conclusión:</title>'
            '<p>la intervención educativa demostró ser innovadora y con gran capacidad de diseminación del conocimiento. El post-test mostró un efecto positivo en la frecuencia de las acciones dirigidas a la deshabituación tabáquica implementadas por el equipo de enfermería.</p>'
            '</sec>'
            '</trans-abstract>'
            '</article-meta>'
            '</front>'
            '</article>'
        )

        expected = (
            '<dc:description>'
            '<dcterms:abstract xml:lang="en">'
            'Abstract '
            'Objective: to assess the effects of an educational intervention on smoking cessation aimed at the nursing team. '
            'Method: this is a quasi-experimental study with 37 nursing professionals from a Brazilian hospital from May/2019 to December/2020. The intervention consisted of training nursing professionals on approaches to hospitalized smokers divided into two steps, the first, online, a prerequisite for the face-to-face/videoconference. The effect of the intervention was assessed through pre- and post-tests completed by participants. Smokers’ medical records were also analyzed. For analysis, McNemar’s chi-square test was used. '
            'Results: there was an increase in the frequency of actions aimed at smoking cessation after the intervention. Significant differences were found in guidelines related to disclosure to family members of their decision to quit smoking and the need for support, encouragement of abstinence after hospital discharge, and information on tobacco cessation and relapse strategies. '
            'Conclusion: the educational intervention proved to be innovative and with a great capacity for disseminating knowledge. The post-test showed a positive effect on the frequency of actions aimed at smoking cessation implemented by the nursing team.</dcterms:abstract>'
            '</dc:description>'
            '<dc:description>'
            '<dcterms:abstract xml:lang="es">RESUMEN '
            'Objetivo: evaluar los efectos de una intervención educativa para dejar de fumar dirigida al equipo de enfermería. '
            'Método: estudio cuasi-experimental con 37 profesionales de enfermería de un hospital brasileño de mayo/2019 a diciembre/2020. La intervención consistió en capacitar a los profesionales de enfermería en el abordaje del paciente fumador, dividida en dos etapas, la primera, en línea, requisito previo para la presencial/videoconferencia. El efecto de la intervención se evaluó a través del pre y post test realizado por los participantes. También se analizaron los registros en las historias clínicas de los fumadores. Para el análisis se utilizó la prueba Chi-Square de McNemar. '
            'Resultados: hubo un aumento en la frecuencia de acciones dirigidas a dejar de fumar después de la intervención. Se encontraron diferencias significativas en las guías relacionadas con la divulgación a los familiares de la decisión de dejar de fumar y la necesidad de apoyo, el estímulo de la abstinencia después del alta hospitalaria y la información sobre estrategias para dejar de fumar y recaer. '
            'Conclusión: la intervención educativa demostró ser innovadora y con gran capacidad de diseminación del conocimiento. El post-test mostró un efecto positivo en la frecuencia de las acciones dirigidas a la deshabituación tabáquica implementadas por el equipo de enfermería.</dcterms:abstract>'
            '</dc:description>'
        )

        xml_oai_dc_agris = ET.fromstring(

            '<metadata>'
            '<ags:resources '
            'xmlns:xsl="http://www.w3.org/1999/XSL/Transform" '
            'xmlns:ags="http://purl.org/agmes/1.1/" '
            'xmlns:dc="http://purl.org/dc/elements/1.1/" '
            'xmlns:agls="http://www.naa.gov.au/recordkeeping/gov_online/agls/1.2" '
            'xmlns:dcterms="http://purl.org/dc/terms/">'
            '<ags:resource ags:ARN="XS2021000111">'
            '</ags:resource>'
            '</ags:resources>'
            '</metadata>'

        )

        xml_oai_dc_agris_description_pipe(xml_oai_dc_agris, xml_tree)

        self.obtained = ET.tostring(xml_oai_dc_agris, encoding="utf-8").decode("utf-8")

        self.assertIn(expected, self.obtained)

    def test_xml_oai_dc_agris_description_pipe_without_description(self):
        xml_tree = ET.fromstring(
            '<article '
            'xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'xmlns:xlink="http://www.w3.org/1999/xlink" '
            'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xml:lang="en">'
            '<front>'
            '<article-meta>'
            '</article-meta>'
            '</front>'
            '</article>'
        )

        expected = (
            '<metadata>'
            '<ags:resources '
            'xmlns:xsl="http://www.w3.org/1999/XSL/Transform" '
            'xmlns:ags="http://purl.org/agmes/1.1/" '
            'xmlns:dc="http://purl.org/dc/elements/1.1/" '
            'xmlns:agls="http://www.naa.gov.au/recordkeeping/gov_online/agls/1.2" '
            'xmlns:dcterms="http://purl.org/dc/terms/">'
            '<ags:resource ags:ARN="XS2021000111"/>'
            '</ags:resources>'
            '</metadata>'
        )

        xml_oai_dc_agris = ET.fromstring(
            '<metadata>'
            '<ags:resources '
            'xmlns:xsl="http://www.w3.org/1999/XSL/Transform" '
            'xmlns:ags="http://purl.org/agmes/1.1/" '
            'xmlns:dc="http://purl.org/dc/elements/1.1/" '
            'xmlns:agls="http://www.naa.gov.au/recordkeeping/gov_online/agls/1.2" '
            'xmlns:dcterms="http://purl.org/dc/terms/">'
            '<ags:resource ags:ARN="XS2021000111"/>'
            '</ags:resources>'
            '</metadata>'
        )

        xml_oai_dc_agris_description_pipe(xml_oai_dc_agris, xml_tree)

        self.obtained = ET.tostring(xml_oai_dc_agris, encoding="utf-8").decode("utf-8")

        self.assertEqual(expected, self.obtained)

    def test_xml_oai_dc_agris_identifier_pipe(self):
        xml_tree = ET.fromstring(
            '<article xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'xmlns:xlink="http://www.w3.org/1999/xlink" '
            'article-type="research-article" dtd-version="1.0" '
            'specific-use="sps-1.6" xml:lang="pt">'
            '<front>'
            '<article-meta>'
            '<article-id pub-id-type="publisher-id" specific-use="scielo-v3">XZrRmc87LzCkDtLdcXwgztp</article-id>'
            '<article-id pub-id-type="publisher-id" specific-use="scielo-v2">S0103-21002017000400333</article-id>'
            '<article-id pub-id-type="publisher-id">1982-0194201700050</article-id>'
            '<article-id pub-id-type="doi">10.1590/1677-941X-ABB-2022-0208</article-id>'
            '<self-uri xlink:href="http://www.scielo.cl/scielo.php?script=sci_arttext&amp;pid=S0718-71812021000100011&amp;lng=en&amp;nrm=iso"/>'
            '<self-uri xlink:href="http://www.scielo.cl/scielo.php?script=sci_abstract&amp;pid=S0718-71812021000100011&amp;lng=en&amp;nrm=iso"/>'
            '<self-uri xlink:href="http://www.scielo.cl/scielo.php?script=sci_pdf&amp;pid=S0718-71812021000100011&amp;lng=en&amp;nrm=iso"/>'
            '</article-meta>'
            '</front>'
            '</article>'
        )

        expected = (
            '<dc:identifier scheme="dcterms:URI">'
            'http://www.scielo.cl/scielo.php?script=sci_arttext&amp;pid=S0718-71812021000100011&amp;lng=en&amp;nrm=iso'
            '</dc:identifier>'
            '<dc:identifier scheme="ags:DOI">10.1590/1677-941X-ABB-2022-0208</dc:identifier>'

        )

        xml_oai_dc_agris = ET.fromstring(

            '<metadata>'
            '<ags:resources '
            'xmlns:xsl="http://www.w3.org/1999/XSL/Transform" '
            'xmlns:ags="http://purl.org/agmes/1.1/" '
            'xmlns:dc="http://purl.org/dc/elements/1.1/" '
            'xmlns:agls="http://www.naa.gov.au/recordkeeping/gov_online/agls/1.2" '
            'xmlns:dcterms="http://purl.org/dc/terms/">'
            '<ags:resource ags:ARN="XS2021000111">'
            '</ags:resource>'
            '</ags:resources>'
            '</metadata>'

        )

        xml_oai_dc_agris_identifier_pipe(xml_oai_dc_agris, xml_tree)

        self.obtained = ET.tostring(xml_oai_dc_agris, encoding="utf-8").decode("utf-8")

        self.assertIn(expected, self.obtained)

    def test_xml_oai_dc_agris_type_pipe(self):
        data = {
            'type': 'journal article'
        }

        expected = (
             '<dc:type>journal article</dc:type>'

        )

        xml_oai_dc_agris = ET.fromstring(

            '<metadata>'
            '<ags:resources '
            'xmlns:xsl="http://www.w3.org/1999/XSL/Transform" '
            'xmlns:ags="http://purl.org/agmes/1.1/" '
            'xmlns:dc="http://purl.org/dc/elements/1.1/" '
            'xmlns:agls="http://www.naa.gov.au/recordkeeping/gov_online/agls/1.2" '
            'xmlns:dcterms="http://purl.org/dc/terms/">'
            '<ags:resource ags:ARN="XS2021000111">'
            '</ags:resource>'
            '</ags:resources>'
            '</metadata>'

        )

        xml_oai_dc_agris_type_pipe(xml_oai_dc_agris, data)

        self.obtained = ET.tostring(xml_oai_dc_agris, encoding="utf-8").decode("utf-8")

        self.assertIn(expected, self.obtained)

    def test_xml_oai_dc_agris_format_pipe(self):
        data = {
            'format': 'text/xml'
        }

        expected = (
            '<dc:format>'
            '<dcterms:medium>text/xml</dcterms:medium>'
            '</dc:format>'

        )

        xml_oai_dc_agris = ET.fromstring(
            '<metadata>'
            '<ags:resources '
            'xmlns:xsl="http://www.w3.org/1999/XSL/Transform" '
            'xmlns:ags="http://purl.org/agmes/1.1/" '
            'xmlns:dc="http://purl.org/dc/elements/1.1/" '
            'xmlns:agls="http://www.naa.gov.au/recordkeeping/gov_online/agls/1.2" '
            'xmlns:dcterms="http://purl.org/dc/terms/">'
            '<ags:resource ags:ARN="XS2021000111">'
            '</ags:resource>'
            '</ags:resources>'
            '</metadata>'
        )

        xml_oai_dc_agris_format_pipe(xml_oai_dc_agris, data)

        self.obtained = ET.tostring(xml_oai_dc_agris, encoding="utf-8").decode("utf-8")

        self.assertIn(expected, self.obtained)

    def test_xml_oai_dc_agris_language_pipe(self):
        xml_tree = ET.fromstring(
            '<article '
            'xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'xmlns:xlink="http://www.w3.org/1999/xlink" '
            'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xml:lang="es">'
            '<front>'
            '<article-meta>'
            '</article-meta>'
            '</front>'
            '</article>'
        )

        expected = (
            '<dc:language scheme="ags:ISO639-1">es</dc:language>'
        )

        xml_oai_dc_agris = ET.fromstring(
            '<metadata>'
            '<ags:resources '
            'xmlns:xsl="http://www.w3.org/1999/XSL/Transform" '
            'xmlns:ags="http://purl.org/agmes/1.1/" '
            'xmlns:dc="http://purl.org/dc/elements/1.1/" '
            'xmlns:agls="http://www.naa.gov.au/recordkeeping/gov_online/agls/1.2" '
            'xmlns:dcterms="http://purl.org/dc/terms/">'
            '<ags:resource ags:ARN="XS2021000111"/>'
            '</ags:resources>'
            '</metadata>'
        )

        xml_oai_dc_agris_language_pipe(xml_oai_dc_agris, xml_tree)

        self.obtained = ET.tostring(xml_oai_dc_agris, encoding="utf-8").decode("utf-8")

        self.assertIn(expected, self.obtained)

    def test_xml_oai_dc_agris_availability_pipe(self):
        data = {
            'location': 'SCIELO'
        }

        xml_tree = ET.fromstring(
            '<article xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'xmlns:xlink="http://www.w3.org/1999/xlink" '
            'article-type="research-article" dtd-version="1.0" '
            'specific-use="sps-1.6" xml:lang="pt">'
            '<front>'
            '<article-meta>'
            '<article-id pub-id-type="publisher-id" specific-use="scielo-v3">XZrRmc87LzCkDtLdcXwgztp</article-id>'
            '<article-id pub-id-type="publisher-id" specific-use="scielo-v2">S0103-21002017000400333</article-id>'
            '<article-id pub-id-type="publisher-id">1982-0194201700050</article-id>'
            '<article-id pub-id-type="doi">10.1590/1677-941X-ABB-2022-0208</article-id>'
            '<self-uri xlink:href="http://www.scielo.cl/scielo.php?script=sci_arttext&amp;pid=S0718-71812021000100011&amp;lng=en&amp;nrm=iso"/>'
            '<self-uri xlink:href="http://www.scielo.cl/scielo.php?script=sci_abstract&amp;pid=S0718-71812021000100011&amp;lng=en&amp;nrm=iso"/>'
            '<self-uri xlink:href="http://www.scielo.cl/scielo.php?script=sci_pdf&amp;pid=S0718-71812021000100011&amp;lng=en&amp;nrm=iso"/>'
            '</article-meta>'
            '</front>'
            '</article>'
        )

        expected = (
            '<agls:availability>'
            '<ags:availabilityLocation>SCIELO</ags:availabilityLocation>'
            '<ags:availabilityNumber>10.1590/1677-941X-ABB-2022-0208</ags:availabilityNumber>'
            '</agls:availability>'
        )

        xml_oai_dc_agris = ET.fromstring(
            '<metadata>'
            '<ags:resources '
            'xmlns:xsl="http://www.w3.org/1999/XSL/Transform" '
            'xmlns:ags="http://purl.org/agmes/1.1/" '
            'xmlns:dc="http://purl.org/dc/elements/1.1/" '
            'xmlns:agls="http://www.naa.gov.au/recordkeeping/gov_online/agls/1.2" '
            'xmlns:dcterms="http://purl.org/dc/terms/">'
            '<ags:resource ags:ARN="XS2021000111"/>'
            '</ags:resources>'
            '</metadata>'
        )

        xml_oai_dc_agris_availability_pipe(xml_oai_dc_agris, xml_tree, data)

        self.obtained = ET.tostring(xml_oai_dc_agris, encoding="utf-8").decode("utf-8")

        self.assertIn(expected, self.obtained)

    def test_xml_oai_dc_agris_availability_pipe_without_location(self):
        xml_tree = ET.fromstring(
            '<article xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'xmlns:xlink="http://www.w3.org/1999/xlink" '
            'article-type="research-article" dtd-version="1.0" '
            'specific-use="sps-1.6" xml:lang="pt">'
            '<front>'
            '<article-meta>'
            '<article-id pub-id-type="publisher-id" specific-use="scielo-v3">XZrRmc87LzCkDtLdcXwgztp</article-id>'
            '<article-id pub-id-type="publisher-id" specific-use="scielo-v2">S0103-21002017000400333</article-id>'
            '<article-id pub-id-type="publisher-id">1982-0194201700050</article-id>'
            '<article-id pub-id-type="doi">10.1590/1677-941X-ABB-2022-0208</article-id>'
            '<self-uri xlink:href="http://www.scielo.cl/scielo.php?script=sci_arttext&amp;pid=S0718-71812021000100011&amp;lng=en&amp;nrm=iso"/>'
            '<self-uri xlink:href="http://www.scielo.cl/scielo.php?script=sci_abstract&amp;pid=S0718-71812021000100011&amp;lng=en&amp;nrm=iso"/>'
            '<self-uri xlink:href="http://www.scielo.cl/scielo.php?script=sci_pdf&amp;pid=S0718-71812021000100011&amp;lng=en&amp;nrm=iso"/>'
            '</article-meta>'
            '</front>'
            '</article>'
        )

        expected = (
            '<agls:availability>'
            '<ags:availabilityNumber>10.1590/1677-941X-ABB-2022-0208</ags:availabilityNumber>'
            '</agls:availability>'
        )

        xml_oai_dc_agris = ET.fromstring(
            '<metadata>'
            '<ags:resources '
            'xmlns:xsl="http://www.w3.org/1999/XSL/Transform" '
            'xmlns:ags="http://purl.org/agmes/1.1/" '
            'xmlns:dc="http://purl.org/dc/elements/1.1/" '
            'xmlns:agls="http://www.naa.gov.au/recordkeeping/gov_online/agls/1.2" '
            'xmlns:dcterms="http://purl.org/dc/terms/">'
            '<ags:resource ags:ARN="XS2021000111"/>'
            '</ags:resources>'
            '</metadata>'
        )

        xml_oai_dc_agris_availability_pipe(xml_oai_dc_agris, xml_tree)

        self.obtained = ET.tostring(xml_oai_dc_agris, encoding="utf-8").decode("utf-8")

        self.assertIn(expected, self.obtained)

