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

    def test_xml_oai_dc_title(self):
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
            '<title-group>'
            '<article-title>'
            'Effects of an educational intervention with nursing professionals on approaches to hospitalized smokers: a quasi-experimental study'
            '<xref ref-type="fn" rid="FN1">*</xref>'
            '</article-title>'
            '<trans-title-group xml:lang="es">'
            '<trans-title>Efectos de una intervención educativa con profesionales de enfermería en el abordaje de pacientes fumadores: un estudio cuasi-experimental</trans-title>'
            '</trans-title-group>'
            '</title-group>'
            '</article-meta>'
            '</front>'
            '</article>'
        )

        expected = (
            '<metadata>'
            '<dc:title xmlns:dc="http://purl.org/dc/elements/1.1/">'
            '<![CDATA[ Effects of an educational intervention with nursing professionals on approaches to hospitalized smokers: a quasi-experimental study ]]>'
            '</dc:title>'
            '</metadata>'
        )

        xml_oai_dc = ET.fromstring(
            '<metadata>'
            '</metadata>'
        )

        xml_oai_dc_title(xml_oai_dc, xml_tree)

        self.obtained = ET.tostring(xml_oai_dc, encoding="utf-8").decode("utf-8")

        self.assertIn(expected, self.obtained)

    def test_xml_oai_dc_creator(self):
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
            '<contrib-group>'
            '<contrib contrib-type="author">'
            '<contrib-id contrib-id-type="orcid">0000-0003-0843-6485</contrib-id>'
            '<name>'
            '<surname>Boni</surname>'
            '<given-names>Fernanda Guarilha</given-names>'
            '</name>'
            '<xref ref-type="aff" rid="aff1">'
            '<sup>1</sup>'
            '</xref>'
            '</contrib>'
            '<contrib contrib-type="author">'
            '<contrib-id contrib-id-type="orcid">0000-0001-7364-4753</contrib-id>'
            '<name>'
            '<surname>da Rosa</surname>'
            '<given-names>Yasmin Lorenz</given-names>'
            '</name>'
            '<xref ref-type="aff" rid="aff2">'
            '<sup>2</sup>'
            '</xref>'
            '</contrib>'
            '<contrib contrib-type="author">'
            '<contrib-id contrib-id-type="orcid">0000-0002-0777-8806</contrib-id>'
            '<name>'
            '<surname>Leite</surname>'
            '<given-names>Renata Meirelles</given-names>'
            '</name>'
            '<xref ref-type="aff" rid="aff2">'
            '<sup>2</sup>'
            '</xref>'
            '</contrib>'
            '<contrib contrib-type="author">'
            '<contrib-id contrib-id-type="orcid">0000-0002-4853-7670</contrib-id>'
            '<name>'
            '<surname>Lopes</surname>'
            '<given-names>Fernanda Machado</given-names>'
            '</name>'
            '<xref ref-type="aff" rid="aff3">'
            '<sup>3</sup>'
            '</xref>'
            '</contrib>'
            '<contrib contrib-type="author">'
            '<contrib-id contrib-id-type="orcid">0000-0001-5425-205X</contrib-id>'
            '<name>'
            '<surname>Echer</surname>'
            '<given-names>Isabel Cristina</given-names>'
            '</name>'
            '<xref ref-type="aff" rid="aff1">'
            '<sup>1</sup>'
            '</xref>'
            '</contrib>'
            '</contrib-group>'
            '</article-meta>'
            '</front>'
            '</article>'
        )

        expected = (
            '<metadata>'
            '<dc:creator xmlns:dc="http://purl.org/dc/elements/1.1/">'
            '<![CDATA[ Boni,Fernanda Guarilha ]]>'
            '</dc:creator>'
            '</metadata>'
        )

        xml_oai_dc = ET.fromstring(
            '<metadata>'
            '</metadata>'
        )

        xml_oai_dc_creator(xml_oai_dc, xml_tree)

        self.obtained = ET.tostring(xml_oai_dc, encoding="utf-8").decode("utf-8")

        self.assertIn(expected, self.obtained)

    def test_xml_oai_dc_subject(self):
        xml_tree = ET.fromstring(
            '<article xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'xmlns:xlink="http://www.w3.org/1999/xlink" '
            'article-type="research-article" dtd-version="1.1" '
            'specific-use="sps-1.9" xml:lang="en">'
            '<front>'
            '<article-meta>'
            '<article-id specific-use="scielo-v3" pub-id-type="publisher-id">ZwzqmpTpbhTmtwR9GfDzP7c</article-id>'
            '<article-id specific-use="scielo-v2" pub-id-type="publisher-id">S0080-62342022000100445</article-id>'
            '<article-id pub-id-type="doi">10.1590/1980-220X-REEUSP-2021-0569en</article-id>'
            '<article-id pub-id-type="other">00445</article-id>'
            '<kwd-group xml:lang="en">'
            '<title>DESCRIPTORS</title>'
            '<kwd>Tobacco Use Cessation</kwd>'
            '<kwd>Health Education</kwd>'
            '<kwd>Nursing Team</kwd>'
            '<kwd>Education</kwd>'
            '<kwd>Nursing</kwd>'
            '<kwd>Continuing</kwd>'
            '<kwd>Teaching</kwd>'
            '</kwd-group>'
            '<kwd-group xml:lang="es">'
            '<title>DESCRIPTORES</title>'
            '<kwd>Cese del Uso de Tabaco</kwd>'
            '<kwd>Educación en Salud</kwd>'
            '<kwd>Grupo de Enfermería</kwd>'
            '<kwd>Educación Continua en Enfermería</kwd>'
            '<kwd>Enseñanza</kwd>'
            '</kwd-group>'
            '</article-meta>'
            '</front>'
            '</article>'
        )

        expected = (
            '<metadata>'
            '<dc:subject xmlns:dc="http://purl.org/dc/elements/1.1/">'
            '<![CDATA[ Tobacco Use Cessation ]]>'
            '</dc:subject>'
            '<dc:subject xmlns:dc="http://purl.org/dc/elements/1.1/">'
            '<![CDATA[ Health Education ]]>'
            '</dc:subject>'
            '<dc:subject xmlns:dc="http://purl.org/dc/elements/1.1/">'
            '<![CDATA[ Nursing Team ]]>'
            '</dc:subject>'
            '<dc:subject xmlns:dc="http://purl.org/dc/elements/1.1/">'
            '<![CDATA[ Education ]]>'
            '</dc:subject>'
            '<dc:subject xmlns:dc="http://purl.org/dc/elements/1.1/">'
            '<![CDATA[ Nursing ]]>'
            '</dc:subject>'
            '<dc:subject xmlns:dc="http://purl.org/dc/elements/1.1/">'
            '<![CDATA[ Continuing ]]>'
            '</dc:subject>'
            '<dc:subject xmlns:dc="http://purl.org/dc/elements/1.1/">'
            '<![CDATA[ Teaching ]]>'
            '</dc:subject>'
            '</metadata>'

        )

        xml_oai_dc = ET.fromstring(
            '<metadata>'
            '</metadata>'
        )

        xml_oai_dc_subject(xml_oai_dc, xml_tree)

        self.obtained = ET.tostring(xml_oai_dc, encoding="utf-8").decode("utf-8")

        self.assertIn(expected, self.obtained)

    def test_xml_oai_dc_description(self):
        xml_tree = ET.fromstring(
            '<article xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'xmlns:xlink="http://www.w3.org/1999/xlink" '
            'article-type="research-article" dtd-version="1.1" '
            'specific-use="sps-1.9" xml:lang="en">'
            '<front>'
            '<article-meta>'
            '<article-id specific-use="scielo-v3" pub-id-type="publisher-id">ZwzqmpTpbhTmtwR9GfDzP7c</article-id>'
            '<article-id specific-use="scielo-v2" pub-id-type="publisher-id">S0080-62342022000100445</article-id>'
            '<article-id pub-id-type="doi">10.1590/1980-220X-REEUSP-2021-0569en</article-id>'
            '<article-id pub-id-type="other">00445</article-id>'
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
            '</article-meta>'
            '</front>'
            '</article>'
        )

        expected = (
            '<metadata>'
            '<dc:description xmlns:dc="http://purl.org/dc/elements/1.1/">'
            '<![CDATA[ Abstract Objective: to assess the effects of an educational intervention '
            'on smoking cessation aimed at the nursing team. Method: this is a quasi-experimental '
            'study with 37 nursing professionals from a Brazilian hospital from May/2019 to '
            'December/2020. The intervention consisted of training nursing professionals on '
            'approaches to hospitalized smokers divided into two steps, the first, online, a '
            'prerequisite for the face-to-face/videoconference. The effect of the intervention was '
            'assessed through pre- and post-tests completed by participants. Smokers’ medical '
            'records were also analyzed. For analysis, McNemar’s chi-square test was used. '
            'Results: there was an increase in the frequency of actions aimed at smoking cessation '
            'after the intervention. Significant differences were found in guidelines related to '
            'disclosure to family members of their decision to quit smoking and the need for '
            'support, encouragement of abstinence after hospital discharge, and information on '
            'tobacco cessation and relapse strategies. Conclusion: the educational intervention '
            'proved to be innovative and with a great capacity for disseminating knowledge. '
            'The post-test showed a positive effect on the frequency of actions aimed at smoking '
            'cessation implemented by the nursing team. ]]>'
            '</dc:description>'
            '</metadata>'

        )

        xml_oai_dc = ET.fromstring(
            '<metadata>'
            '</metadata>'
        )

        xml_oai_dc_description(xml_oai_dc, xml_tree)

        self.obtained = ET.tostring(xml_oai_dc, encoding="utf-8").decode("utf-8")

        self.assertIn(expected, self.obtained)

    def test_xml_oai_dc_publisher(self):
        xml_tree = ET.fromstring(
            '<article xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'xmlns:xlink="http://www.w3.org/1999/xlink" '
            'article-type="research-article" dtd-version="1.0" '
            'specific-use="sps-1.6" xml:lang="pt">'
            '<front>'
            '<journal-meta>'
            '<publisher>'
            '<publisher-name>Escola Paulista de Enfermagem, Universidade Federal de São Paulo</publisher-name>'
            '</publisher>'
            '</journal-meta>'
            '</front>'
            '</article>'
        )

        expected = (
            '<metadata>'
            '<dc:publisher xmlns:dc="http://purl.org/dc/elements/1.1/">'
            '<![CDATA[ Escola Paulista de Enfermagem, Universidade Federal de São Paulo ]]>'
            '</dc:publisher>'
            '</metadata>'

        )

        xml_oai_dc = ET.fromstring(
            '<metadata>'
            '</metadata>'
        )

        xml_oai_dc_publisher(xml_oai_dc, xml_tree)

        self.obtained = ET.tostring(xml_oai_dc, encoding="utf-8").decode("utf-8")

        self.assertIn(expected, self.obtained)

    def test_xml_oai_dc_source(self):
        xml_tree = ET.fromstring(
            '<article xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'xmlns:xlink="http://www.w3.org/1999/xlink" '
            'article-type="research-article" dtd-version="1.0" '
            'specific-use="sps-1.6" xml:lang="pt">'
            '<front>'
            '<journal-meta>'
            '<journal-title-group>'
            '<journal-title>Acta Paulista de Enfermagem</journal-title>'
            '<abbrev-journal-title abbrev-type="publisher">Acta Paul Enferm</abbrev-journal-title>'
            '</journal-title-group>'
            '</journal-meta>'
            '</front>'
            '</article>'
        )

        expected = (
            '<metadata>'
            '<dc:source xmlns:dc="http://purl.org/dc/elements/1.1/">'
            '<![CDATA[ Acta Paulista de Enfermagem ]]>'
            '</dc:source>'
            '</metadata>'
        )

        xml_oai_dc = ET.fromstring(
            '<metadata>'
            '</metadata>'
        )

        xml_oai_dc_source(xml_oai_dc, xml_tree)

        self.obtained = ET.tostring(xml_oai_dc, encoding="utf-8").decode("utf-8")

        self.assertIn(expected, self.obtained)

if __name__ == '__main__':
    unittest.main()
