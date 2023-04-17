from packtools.sps.formats.crossref import (
    pipeline_crossref,
    setupdoibatch_pipe,
    xml_head_pipe,
    xml_doibatchid_pipe,
    xml_timestamp_pipe,
    xml_depositor_pipe,
    xml_registrant_pipe,
    xml_body_pipe,
    xml_journal_pipe,
    xml_journalmetadata_pipe,
    xml_journaltitle_pipe,
    xml_abbreviatedjournaltitle_pipe,
    xml_issn_pipe,
    xml_journalissue_pipe,
    xml_pubdate_pipe,
    xml_journalvolume_pipe,
    xml_volume_pipe,
    xml_issue_pipe,
    xml_journalarticle_pipe,
    xml_articlecontributors_pipe,

)
from unittest import TestCase
from unittest.mock import patch

from lxml import etree as ET


class PipelineCrossref(TestCase):

    def test_setupdoibatch_pipe(self):
        expected = (
            '<doi_batch xmlns:ai="http://www.crossref.org/AccessIndicators.xsd" '
            'xmlns:jats="http://www.ncbi.nlm.nih.gov/JATS1" '
            'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" version="4.4.0" '
            'xmlns="http://www.crossref.org/schema/4.4.0" '
            'xsi:schemaLocation="http://www.crossref.org/schema/4.4.0 '
            'http://www.crossref.org/schemas/crossref4.4.0.xsd"/>'
        )

        result = setupdoibatch_pipe()
        obtained = ET.tostring(result, encoding="utf-8").decode("utf-8")

        self.assertEqual(expected, obtained)

    def test_xmlhead_pipe(self):
        xml_crossref = setupdoibatch_pipe()
        xml_head_pipe(xml_crossref)

        self.assertIsNotNone(xml_crossref.find('head'))

    @patch('packtools.sps.formats.crossref.get_doi_batch_id')
    def test_xml_doibatchid_pipe(self, mock_get_doi_batch_id):
        expected = (
            "<head>"
            "<doi_batch_id>49d374553c5d48c0bdd54d25080e0045</doi_batch_id>"
            "</head>"
        )

        mock_get_doi_batch_id.return_value = '49d374553c5d48c0bdd54d25080e0045'

        xml_crossref = ET.fromstring(
            '<doi_batch>'
            '<head>'
            '</head>'
            '</doi_batch>'
        )

        xml_doibatchid_pipe(xml_crossref)

        self.obtained = ET.tostring(xml_crossref, encoding="utf-8").decode("utf-8")

        self.assertIn(expected, self.obtained)

    @patch('packtools.sps.formats.crossref.get_timestamp')
    def test_xml_timestamp_pipe(self, mock_get_timestamp):
        expected = (
            "<head>"
            "<timestamp>20230405112328</timestamp>"
            "</head>"
        )

        mock_get_timestamp.return_value = "20230405112328"
        xml_crossref = ET.fromstring(
            '<doi_batch>'
            '<head>'
            '</head>'
            '</doi_batch>'
        )
        xml_timestamp_pipe(xml_crossref)

        self.obtained = ET.tostring(xml_crossref, encoding="utf-8").decode("utf-8")

        self.assertIn(expected, self.obtained)

    def test_xml_depositor_pipe(self):
        expected = (
            "<head>"
            "<depositor>"
            "<depositor_name>depositor</depositor_name>"
            "<email_address>name@domain.com</email_address>"
            "</depositor>"
            "</head>"
        )

        data = {
            "depositor_name": "depositor",
            "depositor_email_address": "name@domain.com"
        }

        xml_crossref = setupdoibatch_pipe()
        xml_head_pipe(xml_crossref)
        xml_depositor_pipe(xml_crossref, data)

        self.obtained = ET.tostring(xml_crossref, encoding="utf-8").decode("utf-8")

        self.assertIn(expected, self.obtained)

    def test_xml_registrant_pipe(self):
        expected = (
            "<head>"
            "<registrant>registrant</registrant>"
            "</head>"
        )

        data = {
            "registrant": "registrant"
        }

        xml_crossref = setupdoibatch_pipe()
        xml_head_pipe(xml_crossref)
        xml_registrant_pipe(xml_crossref, data)

        self.obtained = ET.tostring(xml_crossref, encoding="utf-8").decode("utf-8")

        self.assertIn(expected, self.obtained)

    def test_xml_body_pipe(self):
        xml_crossref = setupdoibatch_pipe()
        xml_body_pipe(xml_crossref)

        self.assertIsNotNone(xml_crossref.find('body'))

    def test_xml_journal_pipe(self):
        xml_crossref = setupdoibatch_pipe()
        xml_body_pipe(xml_crossref)
        xml_journal_pipe(xml_crossref)

        self.assertIsNotNone(xml_crossref.find('./body/journal'))

    def test_xml_journalmetadata_pipe(self):
        xml_crossref = setupdoibatch_pipe()
        xml_body_pipe(xml_crossref)
        xml_journal_pipe(xml_crossref)
        xml_journalmetadata_pipe(xml_crossref)

        self.assertIsNotNone(xml_crossref.find('./body/journal/journal_metadata'))

    def test_xml_journaltitle_pipe(self):
        xml_tree = ET.fromstring(
            '<article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink" '
            'article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">'
            '<front>'
            '<journal-meta>'
            '<journal-id journal-id-type="nlm-ta">Rev Esc Enferm USP</journal-id>'
            '<journal-id journal-id-type="publisher-id">reeusp</journal-id>'
            '<journal-title-group>'
            '<journal-title>Revista da Escola de Enfermagem da USP</journal-title>'
            '</journal-title-group>'
            '</journal-meta>'
            '</front>'
            '</article>'
        )
        expected = (
            '<body>'
            '<journal>'
            '<journal_metadata>'
            '<full_title>Revista da Escola de Enfermagem da USP</full_title>'
            '</journal_metadata>'
            '</journal>'
            '</body>'
        )

        xml_crossref = setupdoibatch_pipe()
        xml_body_pipe(xml_crossref)
        xml_journal_pipe(xml_crossref)
        xml_journalmetadata_pipe(xml_crossref)

        xml_journaltitle_pipe(xml_tree, xml_crossref)

        obtained = ET.tostring(xml_crossref, encoding="utf-8").decode("utf-8")

        self.assertIn(expected, obtained)

    def test_xml_abbreviatedjournaltitle_pipe(self):
        xml_tree = ET.fromstring(
            '<article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink" '
            'article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">'
            '<front>'
            '<journal-meta>'
            '<journal-id journal-id-type="nlm-ta">Rev Esc Enferm USP</journal-id>'
            '<journal-id journal-id-type="publisher-id">reeusp</journal-id>'
            '<journal-title-group>'
            '<abbrev-journal-title abbrev-type="publisher">Rev. esc. enferm. USP</abbrev-journal-title>'
            '</journal-title-group>'
            '</journal-meta>'
            '</front>'
            '</article>'
        )
        expected = (
            '<body>'
            '<journal>'
            '<journal_metadata>'
            '<abbrev_title>Rev. esc. enferm. USP</abbrev_title>'
            '</journal_metadata>'
            '</journal>'
            '</body>'
        )

        xml_crossref = setupdoibatch_pipe()
        xml_body_pipe(xml_crossref)
        xml_journal_pipe(xml_crossref)
        xml_journalmetadata_pipe(xml_crossref)

        xml_abbreviatedjournaltitle_pipe(xml_tree, xml_crossref)

        obtained = ET.tostring(xml_crossref, encoding="utf-8").decode("utf-8")

        self.assertIn(expected, obtained)

    def test_xml_issn_pipe(self):
        xml_tree = ET.fromstring(
            '<article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink" '
            'article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">'
            '<front>'
            '<journal-meta>'
            '<journal-id journal-id-type="nlm-ta">Rev Esc Enferm USP</journal-id>'
            '<journal-id journal-id-type="publisher-id">reeusp</journal-id>'
            '<issn pub-type="ppub">0080-6234</issn>'
            '<issn pub-type="epub">1980-220X</issn>'
            '</journal-meta>'
            '</front>'
            '</article>'
        )
        expected = (
            '<body>'
            '<journal>'
            '<journal_metadata>'
            '<issn media_type="electronic">1980-220X</issn>'
            '<issn media_type="print">0080-6234</issn>'
            '</journal_metadata>'
            '</journal>'
            '</body>'
        )

        xml_crossref = setupdoibatch_pipe()
        xml_body_pipe(xml_crossref)
        xml_journal_pipe(xml_crossref)
        xml_journalmetadata_pipe(xml_crossref)

        xml_issn_pipe(xml_tree, xml_crossref)

        obtained = ET.tostring(xml_crossref, encoding="utf-8").decode("utf-8")

        self.assertIn(expected, obtained)

    def test_xml_journalissue_pipe(self):
        xml_crossref = setupdoibatch_pipe()
        xml_body_pipe(xml_crossref)
        xml_journal_pipe(xml_crossref)
        xml_journalmetadata_pipe(xml_crossref)

        self.assertIsNotNone(xml_crossref.find('./body/journal/journal_metadata'))

    def test_xml_pubdate_pipe(self):
        xml_tree = ET.fromstring(
            '<article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink" '
            'article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">'
            '<front>'
            '<article-meta>'
            '<pub-date date-type="pub" publication-format="electronic">'
            '<day>13</day>'
            '<month>05</month>'
            '<year>2022</year>'
            '</pub-date>'
            '<pub-date date-type="collection" publication-format="electronic">'
            '<year>2022</year>'
            '</pub-date>'
            '<volume>56</volume>'
            '<elocation-id>e20210569</elocation-id>'
            '</article-meta>'
            '</front>'
            '</article>'
        )
        expected = (
            '<body>'
            '<journal>'
            '<journal_issue>'
            '<publication_date media_type="online">'
            '<year>2022</year>'
            '</publication_date>'
            '</journal_issue>'
            '</journal>'
            '</body>'
        )

        xml_crossref = setupdoibatch_pipe()
        xml_body_pipe(xml_crossref)
        xml_journal_pipe(xml_crossref)
        xml_journalissue_pipe(xml_crossref)

        xml_pubdate_pipe(xml_tree, xml_crossref)

        obtained = ET.tostring(xml_crossref, encoding="utf-8").decode("utf-8")

        self.assertIn(expected, obtained)

    def test_xml_journalvolume_pipe(self):
        xml_crossref = setupdoibatch_pipe()
        xml_body_pipe(xml_crossref)
        xml_journal_pipe(xml_crossref)
        xml_journalissue_pipe(xml_crossref)
        xml_journalvolume_pipe(xml_crossref)

        self.assertIsNotNone(xml_crossref.find('./body/journal/journal_issue/journal_volume'))

    def test_xml_volume_pipe(self):
        xml_tree = ET.fromstring(
            '<article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink" '
            'article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">'
            '<front>'
            '<article-meta>'
            '<pub-date date-type="pub" publication-format="electronic">'
            '<day>13</day>'
            '<month>05</month>'
            '<year>2022</year>'
            '</pub-date>'
            '<pub-date date-type="collection" publication-format="electronic">'
            '<year>2022</year>'
            '</pub-date>'
            '<volume>56</volume>'
            '<elocation-id>e20210569</elocation-id>'
            '</article-meta>'
            '</front>'
            '</article>'
        )
        expected = (
            '<body>'
            '<journal>'
            '<journal_issue>'
            '<journal_volume>'
            '<volume>56</volume>'
            '</journal_volume>'
            '</journal_issue>'
            '</journal>'
            '</body>'
        )

        xml_crossref = setupdoibatch_pipe()
        xml_body_pipe(xml_crossref)
        xml_journal_pipe(xml_crossref)
        xml_journalissue_pipe(xml_crossref)
        xml_journalvolume_pipe(xml_crossref)

        xml_volume_pipe(xml_tree, xml_crossref)

        obtained = ET.tostring(xml_crossref, encoding="utf-8").decode("utf-8")

        self.assertIn(expected, obtained)

    def test_xml_issue_pipe(self):
        xml_tree = ET.fromstring(
            '<article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink" '
            'article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">'
            '<front>'
            '<article-meta>'
            '<pub-date date-type="pub" publication-format="electronic">'
            '<day>13</day>'
            '<month>05</month>'
            '<year>2022</year>'
            '</pub-date>'
            '<pub-date date-type="collection" publication-format="electronic">'
            '<year>2022</year>'
            '</pub-date>'
            '<volume>56</volume>'
            '<issue>4</issue>'
            '<elocation-id>e20210569</elocation-id>'
            '</article-meta>'
            '</front>'
            '</article>'
        )
        expected = (
            '<body>'
            '<journal>'
            '<journal_issue>'
            '<journal_volume>'
            '<issue>4</issue>'
            '</journal_volume>'
            '</journal_issue>'
            '</journal>'
            '</body>'
        )

        xml_crossref = setupdoibatch_pipe()
        xml_body_pipe(xml_crossref)
        xml_journal_pipe(xml_crossref)
        xml_journalissue_pipe(xml_crossref)
        xml_journalvolume_pipe(xml_crossref)

        xml_issue_pipe(xml_tree, xml_crossref)

        obtained = ET.tostring(xml_crossref, encoding="utf-8").decode("utf-8")

        self.assertIn(expected, obtained)

    def test_xml_journalarticle_pipe(self):
        xml_tree = ET.fromstring(
            '<article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink" '
            'article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">'
            '<front>'
            '<journal-meta>'
            '<journal-id journal-id-type="nlm-ta">Rev Esc Enferm USP</journal-id>'
            '<journal-id journal-id-type="publisher-id">reeusp</journal-id>'
            '<journal-title-group>'
            '<journal-title>Revista da Escola de Enfermagem da USP</journal-title>'
            '</journal-title-group>'
            '</journal-meta>'
            '</front>'
            '<sub-article article-type="translation" id="s1" xml:lang="pt">'
            '</sub-article>'
            '</article>'
        )
        expected = (
            '<body>'
            '<journal>'
            '<journal_article language="en" publication_type="research-article" reference_distribution_opts="any"/>'
            '<journal_article language="pt" publication_type="translation" reference_distribution_opts="any"/>'
            '</journal>'
            '</body>'
        )
        xml_crossref = setupdoibatch_pipe()
        xml_body_pipe(xml_crossref)
        xml_journal_pipe(xml_crossref)
        xml_journalarticle_pipe(xml_tree, xml_crossref)

        obtained = ET.tostring(xml_crossref, encoding="utf-8").decode("utf-8")

        self.assertIn(expected, obtained)

    def test_xml_articlecontributors_pipe(self):
        xml_tree = ET.fromstring(
            '<article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink" '
            'article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">'
            '<front>'
            '<article-meta>'
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
            '</contrib-group>'
            '<aff id="aff1">'
            '<label>1</label>'
            '<institution content-type="original">Universidade Federal do Rio Grande do Sul, Escola de Enfermagem, Programa de Pós-Graduação em Enfermagem, Porto Alegre, RS, Brazil.</institution>'
            '<institution content-type="orgname">Universidade Federal do Rio Grande do Sul</institution>'
            '<institution content-type="orgdiv1">Escola de Enfermagem</institution>'
            '<institution content-type="orgdiv2">Programa de Pós-Graduação em Enfermagem</institution>'
            '<addr-line>'
            '<named-content content-type="city">Porto Alegre</named-content>'
            '<named-content content-type="state">RS</named-content>'
            '</addr-line>'
            '<country country="BR">Brazil</country>'
            '</aff>'
            '<aff id="aff2">'
            '<label>2</label>'
            '<institution content-type="original">Universidade Federal do Rio Grande do Sul, Escola de Enfermagem, Porto Alegre, RS, Brazil.</institution>'
            '<institution content-type="orgname">Universidade Federal do Rio Grande do Sul</institution>'
            '<institution content-type="orgdiv1">Escola de Enfermagem</institution>'
            '<addr-line>'
            '<named-content content-type="city">Porto Alegre</named-content>'
            '<named-content content-type="state">RS</named-content>'
            '</addr-line>'
            '<country country="BR">Brazil</country>'
            '</aff>'
            '</article-meta>'
            '</front>'
            '<sub-article article-type="translation" id="s1" xml:lang="pt">'
            '</sub-article>'
            '</article>'
        )
        expected = (
            '<journal_article language="en" publication_type="research-article" reference_distribution_opts="any">'
            '<contributors>'
            '<person_name contributor_role="author" sequence="first">'
            '<given_name>Fernanda Guarilha</given_name>'
            '<surname>Boni</surname>'
            '<affiliation>Universidade Federal do Rio Grande do Sul, Brazil</affiliation>'
            '<ORCID>http://orcid.org/0000-0003-0843-6485</ORCID>'
            '</person_name>'
            '<person_name contributor_role="author" sequence="additional">'
            '<given_name>Yasmin Lorenz</given_name>'
            '<surname>da Rosa</surname>'
            '<affiliation>Universidade Federal do Rio Grande do Sul, Brazil</affiliation>'
            '<ORCID>http://orcid.org/0000-0001-7364-4753</ORCID>'
            '</person_name>'
            '</contributors>'
            '</journal_article>'
            '<journal_article language="pt" publication_type="translation" reference_distribution_opts="any">'
            '<contributors>'
            '<person_name contributor_role="author" sequence="first">'
            '<given_name>Fernanda Guarilha</given_name>'
            '<surname>Boni</surname>'
            '<affiliation>Universidade Federal do Rio Grande do Sul, Brazil</affiliation>'
            '<ORCID>http://orcid.org/0000-0003-0843-6485</ORCID>'
            '</person_name>'
            '<person_name contributor_role="author" sequence="additional">'
            '<given_name>Yasmin Lorenz</given_name>'
            '<surname>da Rosa</surname>'
            '<affiliation>Universidade Federal do Rio Grande do Sul, Brazil</affiliation>'
            '<ORCID>http://orcid.org/0000-0001-7364-4753</ORCID>'
            '</person_name>'
            '</contributors>'
            '</journal_article>'
        )
        xml_crossref = setupdoibatch_pipe()
        xml_body_pipe(xml_crossref)
        xml_journal_pipe(xml_crossref)
        xml_journalarticle_pipe(xml_tree, xml_crossref)
        xml_articlecontributors_pipe(xml_tree, xml_crossref)

        obtained = ET.tostring(xml_crossref, encoding="utf-8").decode("utf-8")

        self.assertIn(expected, obtained)
