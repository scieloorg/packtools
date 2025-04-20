from unittest import TestCase
from unittest.mock import patch

from lxml import etree as ET

from packtools.sps.utils import xml_utils
from packtools.sps.formats.crossref import (
    pipeline_crossref,
    setup_doi_batch_pipe,
    xml_crossref_head_pipe,
    xml_crossref_doi_batch_id_pipe,
    xml_crossref_timestamp_pipe,
    xml_crossref_depositor_pipe,
    xml_crossref_registrant_pipe,
    xml_crossref_body_pipe,
    xml_crossref_journal_pipe,
    xml_crossref_journal_metadata_pipe,
    xml_crossref_journal_title_pipe,
    xml_crossref_abbreviated_journal_title_pipe,
    xml_crossref_issn_pipe,
    xml_crossref_journal_issue_pipe,
    xml_crossref_pubdate_pipe,
    xml_crossref_journal_volume_pipe,
    xml_crossref_volume_pipe,
    xml_crossref_issue_pipe,
    xml_crossref_journal_article_pipe,
    xml_crossref_article_contributors_pipe,
    xml_crossref_article_abstract_pipe,
    xml_crossref_article_pubdate_pipe,
    xml_crossref_pages_pipe,
    xml_crossref_pid_pipe,
    xml_crossref_elocation_pipe,
    xml_crossref_permissions_pipe,
    xml_crossref_article_titles_pipe,
    xml_crossref_program_related_item_pipe,
    xml_crossref_doi_data_pipe,
    xml_crossref_doi_pipe,
    xml_crossref_resource_pipe,
    xml_crossref_collection_pipe,
    xml_crossref_article_citations_pipe,
)


class PipelineCrossref(TestCase):

    def test_setup_doi_batch_pipe(self):
        expected = (
            '<doi_batch xmlns:ai="http://www.crossref.org/AccessIndicators.xsd" '
            'xmlns:jats="http://www.ncbi.nlm.nih.gov/JATS1" '
            'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" version="4.4.0" '
            'xmlns="http://www.crossref.org/schema/4.4.0" '
            'xsi:schemaLocation="http://www.crossref.org/schema/4.4.0 '
            'http://www.crossref.org/schemas/crossref4.4.0.xsd"/>'
        )

        result = setup_doi_batch_pipe()
        obtained = ET.tostring(result, encoding="utf-8").decode("utf-8")

        self.assertEqual(expected, obtained)

    def test_xml_head_pipe(self):
        xml_crossref = ET.fromstring(
            """
            <doi_batch xmlns:ai="http://www.crossref.org/AccessIndicators.xsd"
            xmlns:jats="http://www.ncbi.nlm.nih.gov/JATS1"
            xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" version="4.4.0"
            xmlns="http://www.crossref.org/schema/4.4.0"
            xsi:schemaLocation="http://www.crossref.org/schema/4.4.0
            http://www.crossref.org/schemas/crossref4.4.0.xsd">
            </doi_batch>
            """
        )

        xml_crossref_head_pipe(xml_crossref)

        self.assertIsNotNone(xml_crossref.find('head'))

    @patch('packtools.sps.formats.crossref.get_doi_batch_id')
    def test_xml_doi_batch_id_pipe(self, mock_get_doi_batch_id):
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

        xml_crossref_doi_batch_id_pipe(xml_crossref)

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
        xml_crossref_timestamp_pipe(xml_crossref)

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

        xml_crossref = ET.fromstring(
            '<doi_batch>'
            '<head>'
            '</head>'
            '</doi_batch>'
        )

        xml_crossref_depositor_pipe(xml_crossref, data)

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

        xml_crossref = ET.fromstring(
            '<doi_batch>'
            '<head>'
            '</head>'
            '</doi_batch>'
        )
        xml_crossref_registrant_pipe(xml_crossref, data)

        self.obtained = ET.tostring(xml_crossref, encoding="utf-8").decode("utf-8")

        self.assertIn(expected, self.obtained)

    def test_xml_body_pipe(self):
        xml_crossref = setup_doi_batch_pipe()
        xml_crossref_body_pipe(xml_crossref)

        self.assertIsNotNone(xml_crossref.find('body'))

    def test_xml_journal_pipe(self):
        xml_crossref = ET.fromstring(
            '<doi_batch>'
            '<head>'
            '</head>'
            '<body>'
            '</body>'
            '</doi_batch>'
        )
        xml_crossref_journal_pipe(xml_crossref)

        self.assertIsNotNone(xml_crossref.find('./body/journal'))

    def test_xml_journal_metadata_pipe(self):
        xml_crossref = ET.fromstring(
            '<doi_batch>'
            '<head>'
            '</head>'
            '<body>'
            '<journal>'
            '</journal>'
            '</body>'
            '</doi_batch>'
        )

        xml_crossref_journal_metadata_pipe(xml_crossref)

        self.assertIsNotNone(xml_crossref.find('./body/journal/journal_metadata'))

    def test_xml_journal_title_pipe(self):
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
        xml_crossref = ET.fromstring(
            '<doi_batch>'
            '<head>'
            '</head>'
            '<body>'
            '<journal>'
            '<journal_metadata>'
            '</journal_metadata>'
            '</journal>'
            '</body>'
            '</doi_batch>'
        )

        xml_crossref_journal_title_pipe(xml_crossref, xml_tree)

        obtained = ET.tostring(xml_crossref, encoding="utf-8").decode("utf-8")

        self.assertIn(expected, obtained)

    def test_xml_abbreviated_journal_title_pipe(self):
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
        xml_crossref = ET.fromstring(
            '<doi_batch>'
            '<body>'
            '<journal>'
            '<journal_metadata>'
            '</journal_metadata>'
            '</journal>'
            '</body>'
            '</doi_batch>'
        )

        xml_crossref_abbreviated_journal_title_pipe(xml_crossref, xml_tree)

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
        xml_crossref = ET.fromstring(
            '<doi_batch>'
            '<body>'
            '<journal>'
            '<journal_metadata>'
            '</journal_metadata>'
            '</journal>'
            '</body>'
            '</doi_batch>'
        )

        xml_crossref_issn_pipe(xml_crossref, xml_tree)

        obtained = ET.tostring(xml_crossref, encoding="utf-8").decode("utf-8")

        self.assertIn(expected, obtained)

    def test_xml_journal_issue_pipe(self):
        xml_crossref = ET.fromstring(
            '<doi_batch>'
            '<body>'
            '<journal>'
            '</journal>'
            '</body>'
            '</doi_batch>'
        )

        xml_crossref_journal_issue_pipe(xml_crossref)

        self.assertIsNotNone(xml_crossref.find('./body/journal/journal_issue'))

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
        xml_crossref = ET.fromstring(
            '<doi_batch>'
            '<body>'
            '<journal>'
            '<journal_issue>'
            '</journal_issue>'
            '</journal>'
            '</body>'
            '</doi_batch>'
        )

        xml_crossref_pubdate_pipe(xml_crossref, xml_tree)

        obtained = ET.tostring(xml_crossref, encoding="utf-8").decode("utf-8")

        self.assertIn(expected, obtained)

    def test_xml_journal_volume_pipe(self):
        xml_crossref = ET.fromstring(
            '<doi_batch>'
            '<body>'
            '<journal>'
            '<journal_issue>'
            '</journal_issue>'
            '</journal>'
            '</body>'
            '</doi_batch>'
        )

        xml_crossref_journal_volume_pipe(xml_crossref)

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
        xml_crossref = ET.fromstring(
            '<doi_batch>'
            '<body>'
            '<journal>'
            '<journal_issue>'
            '<journal_volume>'
            '</journal_volume>'
            '</journal_issue>'
            '</journal>'
            '</body>'
            '</doi_batch>'
        )

        xml_crossref_volume_pipe(xml_crossref, xml_tree)

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
        xml_crossref = ET.fromstring(
            '<doi_batch>'
            '<body>'
            '<journal>'
            '<journal_issue>'
            '<journal_volume>'
            '</journal_volume>'
            '</journal_issue>'
            '</journal>'
            '</body>'
            '</doi_batch>'
        )

        xml_crossref_issue_pipe(xml_crossref, xml_tree)

        obtained = ET.tostring(xml_crossref, encoding="utf-8").decode("utf-8")

        self.assertIn(expected, obtained)

    def test_xml_journal_article_pipe(self):
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
        xml_crossref = ET.fromstring(
            '<doi_batch>'
            '<body>'
            '<journal>'
            '</journal>'
            '</body>'
            '</doi_batch>'
        )

        xml_crossref_journal_article_pipe(xml_crossref, xml_tree)

        obtained = ET.tostring(xml_crossref, encoding="utf-8").decode("utf-8")

        self.assertIn(expected, obtained)

    def test_xml_article_contributors_pipe(self):
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
        xml_crossref = ET.fromstring(
            '<doi_batch>'
            '<body>'
            '<journal>'
            '<journal_article language="en" publication_type="research-article" reference_distribution_opts="any" />'
            '<journal_article language="pt" publication_type="translation" reference_distribution_opts="any" />'
            '</journal>'
            '</body>'
            '</doi_batch>'
        )

        xml_crossref_article_contributors_pipe(xml_crossref, xml_tree)

        obtained = ET.tostring(xml_crossref, encoding="utf-8").decode("utf-8")

        self.assertIn(expected, obtained)

    def test_xml_article_contributors_without_reviewers_example_1_pipe(self):
        xml_tree = ET.fromstring(
            '<article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink" '
            'article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="pt"> '
            '<front>'
            '<article-meta>'
            '<article-id specific-use="scielo-v3" pub-id-type="publisher-id">89LSWnjxHfJ9NB3z8h4bsKs</article-id>'
            '<article-id specific-use="scielo-v2" pub-id-type="publisher-id">S2176-45732023005002204</article-id>'
            '<article-id pub-id-type="doi">10.1590/2176-4573p58779</article-id>'
            '<article-id pub-id-type="other">02204</article-id>'
            '<contrib-group>'
            '<contrib contrib-type="author">'
            '<contrib-id contrib-id-type="orcid">0000-0002-8274-3101</contrib-id>'
            '<name>'
            '<surname>Ferreira</surname>'
            '<given-names>Maria</given-names>'
            '</name>'
            '<xref ref-type="aff" rid="aff1">*</xref>'
            '</contrib>'
            '</contrib-group>'
            '<aff id="aff1">'
            '<label>*</label>'
            '<institution content-type="orgname">Universidade de Lisboa – UL</institution>'
            '<institution content-type="orgdiv1">Instituto Superior de Ciências Sociais e Políticas</institution>'
            '<addr-line>'
            '<city>Lisbon</city>'
            '</addr-line>'
            '<country country="PT">Portugal</country>'
            '<email>mjmfsp@gmail.com</email>'
            '<institution content-type="original">Universidade de Lisboa – UL, Instituto Superior de Ciências Sociais e Políticas, Lisbon, Portugal; https://orcid.org/0000-0002-8274-3101; mjmfsp@gmail.com</institution>'
            '</aff>'
            '</article-meta>'
            '</front>'
            '<sub-article article-type="reviewer-report" id="s1" xml:lang="pt">'
            '<front-stub>'
            '<contrib-group>'
            '<contrib contrib-type="author">'
            '<contrib-id contrib-id-type="orcid">0000-0002-5592-8098</contrib-id>'
            '<name>'
            '<surname>Segundo</surname>'
            '<given-names>Paulo Roberto Gonçalves</given-names>'
            '</name>'
            '<xref ref-type="aff" rid="aff5"/>'
            '</contrib>'
            '</contrib-group>'
            '</front-stub>'
            '</sub-article>'
            '<sub-article article-type="reviewer-report" id="s2" xml:lang="pt">'
            '<front-stub>'
            '<contrib-group>'
            '<contrib contrib-type="author">'
            '<contrib-id contrib-id-type="orcid">0000-0003-1925-1435</contrib-id>'
            '<name>'
            '<surname>Gualda</surname>'
            '<given-names>Ricardo José Rosa</given-names>'
            '</name>'
            '<xref ref-type="aff" rid="aff6"/>'
            '</contrib>'
            '</contrib-group>'
            '</front-stub>'
            '</sub-article>'
            '<sub-article article-type="translation" id="s3" xml:lang="en">'
            '<sub-article article-type="reviewer-report" id="s4" xml:lang="en">'
            '<front-stub>'
            '<contrib-group>'
            '<contrib contrib-type="author">'
            '<contrib-id contrib-id-type="orcid">0000-0002-5592-8098</contrib-id>'
            '<name>'
            '<surname>Segundo</surname>'
            '<given-names>Paulo Roberto Gonçalves</given-names>'
            '</name>'
            '<xref ref-type="aff" rid="aff3"/>'
            '</contrib>'
            '</contrib-group>'
            '</front-stub>'
            '</sub-article>'
            '<sub-article article-type="reviewer-report" id="s5" xml:lang="en">'
            '<front-stub>'
            '<contrib-group>'
            '<contrib contrib-type="author">'
            '<contrib-id contrib-id-type="orcid">0000-0003-1925-1435</contrib-id>'
            '<name>'
            '<surname>Gualda</surname>'
            '<given-names>Ricardo José Rosa</given-names>'
            '</name>'
            '<role specific-use="reviewer">Reviewer</role>'
            '<xref ref-type="aff" rid="aff4"/>'
            '</contrib>'
            '</contrib-group>'
            '</front-stub>'
            '</sub-article>'
            '</sub-article>'
            '</article>'
        )
        expected = (
            '<journal_article language="pt" publication_type="research-article" reference_distribution_opts="any">'
            '<contributors>'
            '<person_name contributor_role="author" sequence="first">'
            '<given_name>Maria</given_name>'
            '<surname>Ferreira</surname>'
            '<affiliation>Universidade de Lisboa – UL, Portugal</affiliation>'
            '<ORCID>http://orcid.org/0000-0002-8274-3101</ORCID>'
            '</person_name>'
            '</contributors>'
            '</journal_article>'
            '<journal_article language="en" publication_type="translation" reference_distribution_opts="any">'
            '<contributors>'
            '<person_name contributor_role="author" sequence="first">'
            '<given_name>Maria</given_name>'
            '<surname>Ferreira</surname>'
            '<affiliation>Universidade de Lisboa – UL, Portugal</affiliation>'
            '<ORCID>http://orcid.org/0000-0002-8274-3101</ORCID>'
            '</person_name>'
            '</contributors>'
            '</journal_article>'
        )
        xml_crossref = ET.fromstring(
            '<doi_batch>'
            '<body>'
            '<journal>'
            '<journal_article language="pt" publication_type="research-article" reference_distribution_opts="any" />'
            '<journal_article language="en" publication_type="translation" reference_distribution_opts="any" />'
            '</journal>'
            '</body>'
            '</doi_batch>'
        )

        xml_crossref_article_contributors_pipe(xml_crossref, xml_tree)

        obtained = ET.tostring(xml_crossref, encoding="utf-8").decode("utf-8")

        self.assertIn(expected, obtained)

    def test_xml_article_contributors_without_reviewers_example_2_pipe(self):
        xml_tree = ET.fromstring(
            '<article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink" '
            'article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="pt"> '
            '<front>'
            '<article-meta>'
            '<article-id specific-use="scielo-v3" pub-id-type="publisher-id">3LMgVWMz8YNF8RqZRHDqhqg</article-id>'
            '<article-id specific-use="scielo-v2" pub-id-type="publisher-id">S2176-45732023005002202</article-id>'
            '<article-id pub-id-type="doi">10.1590/2176-4573p58095</article-id>'
            '<article-id pub-id-type="other">02202</article-id>'
            '<contrib-group>'
            '<contrib contrib-type="author">'
            '<contrib-id contrib-id-type="orcid">0000-0002-8916-0822</contrib-id>'
            '<name>'
            '<surname>Figueira</surname>'
            '<given-names>Filipo</given-names>'
            '</name>'
            '<xref ref-type="aff" rid="aff1">*</xref>'
            '</contrib>'
            '</contrib-group>'
            '<aff id="aff1">'
            '<label>*</label>'
            '<institution content-type="orgname">Universidade Estadual de Campinas – UNICAMP</institution>'
            '<institution content-type="orgdiv1">Linguística no Programa de Pós-Graduação em Linguística</institution>'
            '<addr-line>'
            '<city>Campinas</city>'
            '<state>São Paulo</state>'
            '</addr-line>'
            '<country country="RU">Brasil</country>'
            '<email>figueirafp1@gmail.com</email>'
            '<institution content-type="original">Doutorando em Linguística no Programa de Pós-Graduação em Linguística, Universidade Estadual de Campinas – UNICAMP, Campinas, São Paulo, Brasil; FAPESP, Proc. 2019/01680-1; https://orcid.org/0000-0002-8916-0822; figueirafp1@gmail.com</institution>'
            '</aff>'
            '</article-meta>'
            '</front>'
            '<sub-article article-type="reviewer-report" id="s2" xml:lang="pt">'
            '<front-stub>'
            '<contrib-group>'
            '<contrib contrib-type="author">'
            '<contrib-id contrib-id-type="orcid">0000-0002-2262-0206</contrib-id>'
            '<name>'
            '<surname>El-Jaick</surname>'
            '<given-names>Ana Paula Grillo</given-names>'
            '</name>'
            '<xref ref-type="aff" rid="aff3"/>'
            '</contrib>'
            '</contrib-group>'
            '<aff id="aff3">'
            '<institution content-type="orgname">Universidade Federal de Juiz de Fora</institution>'
            '<addr-line>'
            '<city>Juiz de Fora</city>'
            '<state>Minas Gerais</state>'
            '</addr-line>'
            '<country country="BR">Brasil</country>'
            '<email>anapaulaeljaick@gmail.com</email>'
            '<institution content-type="original">Universidade Federal de Juiz de Fora – UFJF, Juiz de Fora, Minas Gerais, Brasil</institution>'
            '</aff>'
            '</front-stub>'
            '</sub-article>'
            '<sub-article article-type="translation" id="s1" xml:lang="en">'
            '<front-stub>'
            '<article-id pub-id-type="doi">10.1590/2176-4573e58095</article-id>'
            '<contrib-group>'
            '<contrib contrib-type="author">'
            '<contrib-id contrib-id-type="orcid">0000-0002-8916-0822</contrib-id>'
            '<name>'
            '<surname>Figueira</surname>'
            '<given-names>Filipo</given-names>'
            '</name>'
            '<xref ref-type="aff" rid="aff2">*</xref>'
            '</contrib>'
            '</contrib-group>'
            '<aff id="aff2">'
            '<label>*</label>'
            '<institution content-type="original">PhD Student in Linguística at Universidade Estadual de Campinas – UNICAMP, Campinas, São Paulo, Brazil; FAPESP, Proc. 2019/01680-1; https://orcid.org/0000-0002-8916-0822; figueirafp1@gmail.com</institution>'
            '</aff>'
            '</front-stub>'
            '<sub-article article-type="reviewer-report" id="s3" xml:lang="en">'
            '<front-stub>'
            '<contrib-group>'
            '<contrib contrib-type="author">'
            '<contrib-id contrib-id-type="orcid">0000-0002-2262-0206</contrib-id>'
            '<name>'
            '<surname>El-Jaick</surname>'
            '<given-names>Ana Paula Grillo</given-names>'
            '</name>'
            '<xref ref-type="aff" rid="aff4"/>'
            '</contrib>'
            '</contrib-group>'
            '<aff id="aff4">'
            '<institution content-type="orgname">Universidade Federal de Juiz de Fora</institution>'
            '<addr-line>'
            '<city>Juiz de Fora</city>'
            '<state>Minas Gerais</state>'
            '</addr-line>'
            '<country country="BR">Brazil</country>'
            '<email>anapaulaeljaick@gmail.com</email>'
            '<institution content-type="original">Universidade Federal de Juiz de Fora – UFJF, Juiz de Fora, Minas Gerais, Brazil</institution>'
            '</aff>'
            '</front-stub>'
            '</sub-article>'
            '</sub-article>'
            '</article>'
        )
        expected = (
            '<journal_article language="pt" publication_type="research-article" reference_distribution_opts="any">'
            '<contributors>'
            '<person_name contributor_role="author" sequence="first">'
            '<given_name>Filipo</given_name>'
            '<surname>Figueira</surname>'
            '<affiliation>Universidade Estadual de Campinas – UNICAMP, Brasil</affiliation>'
            '<ORCID>http://orcid.org/0000-0002-8916-0822</ORCID>'
            '</person_name>'
            '</contributors>'
            '</journal_article>'
            '<journal_article language="en" publication_type="translation" reference_distribution_opts="any">'
            '<contributors>'
            '<person_name contributor_role="author" sequence="first">'
            '<given_name>Filipo</given_name>'
            '<surname>Figueira</surname>'
            '<affiliation>Universidade Estadual de Campinas – UNICAMP, Brasil</affiliation>'
            '<ORCID>http://orcid.org/0000-0002-8916-0822</ORCID>'
            '</person_name>'
            '</contributors>'
            '</journal_article>'
        )
        xml_crossref = ET.fromstring(
            '<doi_batch>'
            '<body>'
            '<journal>'
            '<journal_article language="pt" publication_type="research-article" reference_distribution_opts="any" />'
            '<journal_article language="en" publication_type="translation" reference_distribution_opts="any" />'
            '</journal>'
            '</body>'
            '</doi_batch>'
        )

        xml_crossref_article_contributors_pipe(xml_crossref, xml_tree)

        obtained = ET.tostring(xml_crossref, encoding="utf-8").decode("utf-8")

        self.assertIn(expected, obtained)

    def test_xml_article_contributors_without_reviewers_example_3_pipe(self):
        xml_tree = ET.fromstring(
            '<article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="pt">'
            '<front>'
            '<article-meta>'
            '<article-id specific-use="scielo-v3" pub-id-type="publisher-id">x8hVCbXFRc9ZYyJpy8jmyCR</article-id>'
            '<article-id specific-use="scielo-v2" pub-id-type="publisher-id">S2176-45732023005002203</article-id>'
            '<article-id pub-id-type="doi">10.1590/2176-4573p58710</article-id>'
            '<article-id pub-id-type="other">02203</article-id>'
            '<contrib-group>'
            '<contrib contrib-type="author">'
            '<contrib-id contrib-id-type="orcid">0000-0002-4862-2314</contrib-id>'
            '<name>'
            '<surname>Wieler</surname>'
            '<given-names>Bárbara Luisa Martins</given-names>'
            '</name>'
            '<xref ref-type="aff" rid="aff1">*</xref>'
            '</contrib>'
            '</contrib-group>'
            '<aff id="aff1">'
            '<label>*</label>'
            '<institution content-type="orgname">Universidade Federal do Paraná – UFPR</institution>'
            '<institution content-type="orgdiv1">Letras no Programa de Pós-Graduação em Letras</institution>'
            '<addr-line>'
            '<city>Curitiba</city>'
            '<state>Paraná</state>'
            '</addr-line>'
            '<country country="BR">Brasil</country>'
            '<email>bazinhawieler@gmail.com</email>'
            '<institution content-type="original">Doutoranda em Letras no Programa de Pós-Graduação em Letras, Universidade Federal do Paraná – UFPR, Curitiba, Paraná, Brasil; https://orcid.org/0000-0002-4862-2314; bazinhawieler@gmail.com</institution>'
            '</aff>'
            '</article-meta>'
            '</front>'
            '<sub-article article-type="reviewer-report" id="s2" xml:lang="pt">'
            '<front-stub>'
            '<contrib-group>'
            '<contrib contrib-type="author">'
            '<contrib-id contrib-id-type="orcid">0000-0002-4019-0502</contrib-id>'
            '<name>'
            '<surname>Pinheiro</surname>'
            '<given-names>Marina Assis</given-names>'
            '</name>'
            '<xref ref-type="aff" rid="aff3"/>'
            '</contrib>'
            '</contrib-group>'
            '<aff id="aff3">'
            '<institution content-type="orgname">Universidade Federal de Pernambuco</institution>'
            '<addr-line>'
            '<city>Recife</city>'
            '<state>Pernambuco</state>'
            '</addr-line>'
            '<country country="BR">Brasil</country>'
            '<email>marina.pinheiro@ufpe.br</email>'
            '<institution content-type="original">Universidade Federal de Pernambuco – UFPE, Recife, Pernambuco, Brasil</institution>'
            '</aff>'
            '</front-stub>'
            '</sub-article>'
            '<sub-article article-type="reviewer-report" id="s3" xml:lang="pt">'
            '<front-stub>'
            '<contrib-group>'
            '<contrib contrib-type="author">'
            '<contrib-id contrib-id-type="orcid">0000-0002-6740-9631</contrib-id>'
            '<name>'
            '<surname>Del Ré</surname>'
            '<given-names>Alessandra</given-names>'
            '</name>'
            '<xref ref-type="aff" rid="aff4"/>'
            '</contrib>'
            '</contrib-group>'
            '<aff id="aff4">'
            '<institution content-type="orgname">Universidade Estadual Paulista “Júlio de Mesquita Filho” – UNESP</institution>'
            '<addr-line>'
            '<city>Araraquara</city>'
            '<state>São Paulo</state>'
            '</addr-line>'
            '<country country="BR">Brasil</country>'
            '<email>del.re@unesp.br</email>'
            '<institution content-type="original">Universidade Estadual Paulista “Júlio de Mesquita Filho” – UNESP, Araraquara, São Paulo, Brasil</institution>'
            '</aff>'
            '</front-stub>'
            '</sub-article>'
            '<sub-article article-type="reviewer-report" id="s4" xml:lang="pt">'
            '<front-stub>'
            '<contrib-group>'
            '<contrib contrib-type="author">'
            '<contrib-id contrib-id-type="orcid">0000-0002-6740-9631</contrib-id>'
            '<name>'
            '<surname>Del Ré</surname>'
            '<given-names>Alessandra</given-names>'
            '</name>'
            '<xref ref-type="aff" rid="aff5"/>'
            '</contrib>'
            '</contrib-group>'
            '<aff id="aff5">'
            '<institution content-type="orgname">Universidade Estadual Paulista “Júlio de Mesquita Filho” – UNESP</institution>'
            '<addr-line>'
            '<city>Araraquara</city>'
            '<state>São Paulo</state>'
            '</addr-line>'
            '<country country="BR">Brasil</country>'
            '<email>del.re@unesp.br</email>'
            '<institution content-type="original">Alessandra Del Ré - Universidade Estadual Paulista “Júlio de Mesquita Filho” – UNESP, Araraquara, São Paulo, Brasil - https://orcid.org/0000-0002-6740-9631</institution>'
            '</aff>'
            '</front-stub>'
            '</sub-article>'
            '<sub-article article-type="translation" id="s1" xml:lang="en">'
            '<front-stub>'
            '<article-id pub-id-type="doi">10.1590/2176-4573e58710</article-id>'
            '<contrib-group>'
            '<contrib contrib-type="author">'
            '<contrib-id contrib-id-type="orcid">0000-0002-4862-2314</contrib-id>'
            '<name>'
            '<surname>Wieler</surname>'
            '<given-names>Bárbara Luisa Martins</given-names>'
            '</name>'
            '<xref ref-type="aff" rid="aff2">*</xref>'
            '</contrib>'
            '</contrib-group>'
            '<aff id="aff2">'
            '<label>*</label>'
            '<institution content-type="orgname">Universidade Federal do Paraná – UFPR</institution>'
            '<addr-line>'
            '<city>Curitiba</city>'
            '<state>Paraná</state>'
            '</addr-line>'
            '<country country="BR">Brazil</country>'
            '<email>bazinhawieler@gmail.com</email>'
            '<institution content-type="original">PhD Student in Letras at Universidade Federal do Paraná – UFPR, Curitiba, Paraná, Brazil; https://orcid.org/0000-0002-4862-2314; bazinhawieler@gmail.com</institution>'
            '</aff>'
            '</front-stub>'
            '<sub-article article-type="reviewer-report" id="s5" xml:lang="en">'
            '<front-stub>'
            '<contrib-group>'
            '<contrib contrib-type="author">'
            '<contrib-id contrib-id-type="orcid">0000-0002-4019-0502</contrib-id>'
            '<name>'
            '<surname>Pinheiro</surname>'
            '<given-names>Marina Assis</given-names>'
            '</name>'
            '<xref ref-type="aff" rid="aff6"/>'
            '</contrib>'
            '</contrib-group>'
            '<aff id="aff6">'
            '<institution content-type="orgname">Universidade Federal de Pernambuco</institution>'
            '<addr-line>'
            '<city>Recife</city>'
            '<state>Pernambuco</state>'
            '</addr-line>'
            '<country country="BR">Brasil</country>'
            '<email>marina.pinheiro@ufpe.br</email>'
            '<institution content-type="original">Universidade Federal de Pernambuco – UFPE, Recife, Pernambuco, Brasil</institution>'
            '</aff>'
            '</front-stub>'
            '</sub-article>'
            '<sub-article article-type="reviewer-report" id="s6" xml:lang="en">'
            '<front-stub>'
            '<contrib-group>'
            '<contrib contrib-type="author">'
            '<contrib-id contrib-id-type="orcid">0000-0002-6740-9631</contrib-id>'
            '<name>'
            '<surname>Ré</surname>'
            '<given-names>Alessandra Del</given-names>'
            '</name>'
            '<xref ref-type="aff" rid="aff7"/>'
            '</contrib>'
            '</contrib-group>'
            '<aff id="aff7">'
            '<institution content-type="orgname">Universidade Estadual Paulista “Júlio de Mesquita Filho” - UNESP</institution>'
            '<addr-line>'
            '<city>Araraquara</city>'
            '<state>São Paulo</state>'
            '</addr-line>'
            '<country country="BR">Brazil</country>'
            '<email>del.re@unesp.br</email>'
            '<institution content-type="original">Universidade Estadual Paulista “Júlio de Mesquita Filho” - UNESP, Araraquara, São Paulo, Brazil</institution>'
            '</aff>'
            '</front-stub>'
            '</sub-article>'
            '<sub-article article-type="reviewer-report" id="s7" xml:lang="en">'
            '<front-stub>'
            '<contrib-group>'
            '<contrib contrib-type="author">'
            '<contrib-id contrib-id-type="orcid">0000-0002-6740-9631</contrib-id>'
            '<name>'
            '<surname>Del Ré</surname>'
            '<given-names>Alessandra</given-names>'
            '</name>'
            '<xref ref-type="aff" rid="aff8"/>'
            '</contrib>'
            '</contrib-group>'
            '<aff id="aff8">'
            '<institution content-type="orgname">Universidade Estadual Paulista “Júlio de Mesquita Filho” – UNESP</institution>'
            '<addr-line>'
            '<city>Araraquara</city>'
            '<state>São Paulo</state>'
            '</addr-line>'
            '<country country="BR">Brazil</country>'
            '<email>del.re@unesp.br</email>'
            '<institution content-type="original">Universidade Estadual Paulista “Júlio de Mesquita Filho” – UNESP, Araraquara, São Paulo, Brazil</institution>'
            '</aff>'
            '</front-stub>'
            '</sub-article>'
            '</sub-article>'
            '</article>'
        )
        expected = (
            '<journal_article language="pt" publication_type="research-article" reference_distribution_opts="any">'
            '<contributors>'
            '<person_name contributor_role="author" sequence="first">'
            '<given_name>Bárbara Luisa Martins</given_name>'
            '<surname>Wieler</surname>'
            '<affiliation>Universidade Federal do Paraná – UFPR, Brasil</affiliation>'
            '<ORCID>http://orcid.org/0000-0002-4862-2314</ORCID>'
            '</person_name>'
            '</contributors>'
            '</journal_article>'
            '<journal_article language="en" publication_type="translation" reference_distribution_opts="any">'
            '<contributors>'
            '<person_name contributor_role="author" sequence="first">'
            '<given_name>Bárbara Luisa Martins</given_name>'
            '<surname>Wieler</surname>'
            '<affiliation>Universidade Federal do Paraná – UFPR, Brasil</affiliation>'
            '<ORCID>http://orcid.org/0000-0002-4862-2314</ORCID>'
            '</person_name>'
            '</contributors>'
            '</journal_article>'
        )
        xml_crossref = ET.fromstring(
            '<doi_batch>'
            '<body>'
            '<journal>'
            '<journal_article language="pt" publication_type="research-article" reference_distribution_opts="any" />'
            '<journal_article language="en" publication_type="translation" reference_distribution_opts="any" />'
            '</journal>'
            '</body>'
            '</doi_batch>'
        )

        xml_crossref_article_contributors_pipe(xml_crossref, xml_tree)

        obtained = ET.tostring(xml_crossref, encoding="utf-8").decode("utf-8")

        self.assertIn(expected, obtained)

    def test_xml_article_abstract_pipe(self):
        xml_tree = ET.fromstring(
            """
            <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink"
            article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
                <front>
                    <article-meta>
                    <abstract>
                        <title>Abstract</title>
                        <sec>
                        <title>Objective:</title>
                        <p>to assess the effects of an educational intervention on smoking cessation aimed at the nursing team.</p>
                        </sec>
                        <sec>
                        <title>Method:</title>
                        <p>this is a quasi-experimental study with 37 nursing professionals from a Brazilian hospital from May/2019 to December/2020. The intervention consisted of training nursing professionals on approaches to hospitalized smokers divided into two steps, the first, online, a prerequisite for the face-to-face/videoconference. The effect of the intervention was assessed through pre- and post-tests completed by participants. Smokers’ medical records were also analyzed. For analysis, McNemar’s chi-square test was used.</p>
                        </sec>
                        <sec>
                        <title>Results:</title>
                        <p>there was an increase in the frequency of actions aimed at smoking cessation after the intervention. Significant differences were found in guidelines related to disclosure to family members of their decision to quit smoking and the need for support, encouragement of abstinence after hospital discharge, and information on tobacco cessation and relapse strategies.</p>
                        </sec>
                        <sec>
                        <title>Conclusion:</title>
                        <p>the educational intervention proved to be innovative and with a great capacity for disseminating knowledge. The post-test showed a positive effect on the frequency of actions aimed at smoking cessation implemented by the nursing team.</p>
                        </sec>
                        </abstract>
                        <trans-abstract xml:lang="es">
                        <title>RESUMEN</title>
                        <sec>
                        <title>Objetivo:</title>
                        <p>Objetivo</p>
                        </sec>
                        <sec>
                        <title>Método:</title>
                        <p>Método</p>
                        </sec>
                        <sec>
                        <title>Resultados:</title>
                        <p>Resultados</p>
                        </sec>
                        <sec>
                        <title>Conclusión:</title>
                        <p>Conclusión</p>
                        </sec>
                        </trans-abstract>
                    </article-meta>
                </front>
                <sub-article article-type="translation" id="s1" xml:lang="pt">
                    <front-stub>
                        <abstract>
                        <title>RESUMO</title>
                        <sec>
                        <title>Objetivo:</title>
                        <p>Objetivo</p>
                        </sec>
                        <sec>
                        <title>Método:</title>
                        <p>Método</p>
                        </sec>
                        <sec>
                        <title>Resultados:</title>
                        <p>Resultados</p>
                        </sec>
                        <sec>
                        <title>Conclusão:</title>
                        <p>Conclusão</p>
                        </sec>
                        </abstract>
                    </front-stub>
                </sub-article>
            </article>
            """
        )
        expected = (
            '<jats:abstract xml:lang="en">'
            '<jats:p>Abstract '
            'Objective: to assess the effects of an educational intervention on smoking cessation aimed at the nursing team. '
            'Method: this is a quasi-experimental study with 37 nursing professionals from a Brazilian hospital from May/2019 to December/2020. The intervention consisted of training nursing professionals on approaches to hospitalized smokers divided into two steps, the first, online, a prerequisite for the face-to-face/videoconference. The effect of the intervention was assessed through pre- and post-tests completed by participants. Smokers’ medical records were also analyzed. For analysis, McNemar’s chi-square test was used. '
            'Results: there was an increase in the frequency of actions aimed at smoking cessation after the intervention. Significant differences were found in guidelines related to disclosure to family members of their decision to quit smoking and the need for support, encouragement of abstinence after hospital discharge, and information on tobacco cessation and relapse strategies. '
            'Conclusion: the educational intervention proved to be innovative and with a great capacity for disseminating knowledge. The post-test showed a positive effect on the frequency of actions aimed at smoking cessation implemented by the nursing team.</jats:p>'
            '</jats:abstract>'
            '<jats:abstract xml:lang="es">'
            '<jats:p>RESUMEN Objetivo: Objetivo Método: Método Resultados: Resultados Conclusión: Conclusión</jats:p>'
            '</jats:abstract>'
            '<jats:abstract xml:lang="pt">'
            '<jats:p>RESUMO Objetivo: Objetivo Método: Método Resultados: Resultados Conclusão: Conclusão</jats:p>'
            '</jats:abstract>'
        )
        # xml_crossref = ET.fromstring(
        #     '<doi_batch xmlns:ai="http://www.crossref.org/AccessIndicators.xsd" '
        #     'xmlns:jats="http://www.ncbi.nlm.nih.gov/JATS1" '
        #     'version="4.4.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
        #     'xmlns="http://www.crossref.org/schema/4.4.0" '
        #     'xsi:schemaLocation="http://www.crossref.org/schema/4.4.0 '
        #     'http://www.crossref.org/schemas/crossref4.4.0.xsd">'
        #     '<body>'
        #     '<journal>'
        #     '<journal_article language="en" publication_type="research-article" reference_distribution_opts="any" />'
        #     '<journal_article language="pt" publication_type="translation" reference_distribution_opts="any" />'
        #     '</journal>'
        #     '</body>'
        #     '</doi_batch>'
        # )
        xml_crossref = setup_doi_batch_pipe()
        xml_crossref_body_pipe(xml_crossref)
        xml_crossref_journal_pipe(xml_crossref)
        xml_crossref_journal_article_pipe(xml_crossref, xml_tree)

        xml_crossref_article_abstract_pipe(xml_crossref, xml_tree)

        obtained = ET.tostring(xml_crossref, encoding="utf-8").decode("utf-8")

        self.assertIn(expected, obtained)

    def test_xml_article_pubdate_pipe(self):
        xml_tree = ET.fromstring(
            '<article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink" '
            'article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">'
            '<front>'
            '<article-meta>'
            '<article-id specific-use="scielo-v3" pub-id-type="publisher-id">ZwzqmpTpbhTmtwR9GfDzP7c</article-id>'
            '<article-id specific-use="scielo-v2" pub-id-type="publisher-id">S0080-62342022000100445</article-id>'
            '<article-id pub-id-type="doi">10.1590/1980-220X-REEUSP-2021-0569en</article-id>'
            '<article-id pub-id-type="other">00445</article-id>'
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
            ' <sub-article article-type="translation" id="s1" xml:lang="pt">'
            '<front-stub>'
            '</front-stub>'
            '</sub-article>'
            '</article>'
        )
        expected = (
            '<journal_article language="en" publication_type="research-article" reference_distribution_opts="any">'
            '<publication_date media_type="online">'
            '<year>2022</year>'
            '</publication_date>'
            '</journal_article>'
            '<journal_article language="pt" publication_type="translation" reference_distribution_opts="any">'
            '<publication_date media_type="online">'
            '<year>2022</year>'
            '</publication_date>'
            '</journal_article>'
        )
        # xml_crossref = ET.fromstring(
        #     '<doi_batch xmlns:ai="http://www.crossref.org/AccessIndicators.xsd" '
        #     'xmlns:jats="http://www.ncbi.nlm.nih.gov/JATS1" '
        #     'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" version="4.4.0" '
        #     'xmlns="http://www.crossref.org/schema/4.4.0" '
        #     'xsi:schemaLocation="http://www.crossref.org/schema/4.4.0 '
        #     'http://www.crossref.org/schemas/crossref4.4.0.xsd">'
        #     '<body>'
        #     '<journal>'
        #     '<journal_article language="en" publication_type="research-article" reference_distribution_opts="any" />'
        #     '<journal_article language="pt" publication_type="translation" reference_distribution_opts="any" />'
        #     '</journal>'
        #     '</body>'
        #     '</doi_batch>'
        # )

        xml_crossref = setup_doi_batch_pipe()
        xml_crossref_body_pipe(xml_crossref)
        xml_crossref_journal_pipe(xml_crossref)
        xml_crossref_journal_article_pipe(xml_crossref, xml_tree)

        xml_crossref_article_pubdate_pipe(xml_crossref, xml_tree)

        obtained = ET.tostring(xml_crossref, encoding="utf-8").decode("utf-8")

        self.assertIn(expected, obtained)

    def test_xml_pages_pipe(self):
        xml_tree = ET.fromstring(
            """
            <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink"
            article-type="research-article" dtd-version="1.0" specific-use="sps-1.6" xml:lang="pt">
                <front>
                    <article-meta>
                        <article-id pub-id-type="publisher-id" specific-use="scielo-v3">XZrRmc87LzCkDtLdcXwgztp</article-id>
                        <article-id pub-id-type="publisher-id" specific-use="scielo-v2">S0103-21002017000400333</article-id>
                        <article-id pub-id-type="publisher-id">1982-0194201700050</article-id>
                        <article-id pub-id-type="doi">10.1590/1982-0194201700050</article-id>
                        <fpage>333</fpage>
                        <lpage>342</lpage>
                    </article-meta>
                </front>
            </article>
            """
        )
        expected = (
            '<doi_batch>'
            '<body>'
            '<journal>'
            '<journal_article>'
            '<pages>'
            '<first_page>333</first_page>'
            '<last_page>342</last_page>'
            '</pages>'
            '</journal_article>'
            '</journal>'
            '</body>'
            '</doi_batch>'
        )

        xml_crossref = ET.fromstring(
            '<doi_batch>'
            '<body>'
            '<journal>'
            '<journal_article>'
            '</journal_article>'
            '</journal>'
            '</body>'
            '</doi_batch>'
        )

        xml_crossref_pages_pipe(xml_crossref, xml_tree)

        obtained = ET.tostring(xml_crossref, encoding="utf-8").decode("utf-8")

        self.assertIn(expected, obtained)

    def test_xml_pid_pipe(self):
        xml_tree = ET.fromstring(
            """
            <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink"
            article-type="research-article" dtd-version="1.0" specific-use="sps-1.6" xml:lang="pt">
                <front>
                    <article-meta>
                        <article-id pub-id-type="publisher-id" specific-use="scielo-v3">XZrRmc87LzCkDtLdcXwgztp</article-id>
                        <article-id pub-id-type="publisher-id" specific-use="scielo-v2">S0103-21002017000400333</article-id>
                        <article-id pub-id-type="publisher-id">1982-0194201700050</article-id>
                        <article-id pub-id-type="doi">10.1590/1982-0194201700050</article-id>
                        <volume>30</volume>
                        <elocation-id>e20210569</elocation-id>
                        <issue>4</issue>
                        <fpage>333</fpage>
                        <lpage>342</lpage>
                    </article-meta>
                </front>
            </article>
            """
        )
        expected = (
            '<publisher_item>'
            '<identifier id_type="pii">S0103-21002017000400333</identifier>'
            '</publisher_item>'
        )

        xml_crossref = ET.fromstring(
            '<doi_batch>'
            '<head>'
            '<doi_batch_id>3f23a73dfbac48288d22545e53414203</doi_batch_id>'
            '<timestamp>20230418180226</timestamp>'
            '</head>'
            '<body>'
            '<journal>'
            '<journal_article>'
            '</journal_article>'
            '</journal>'
            '</body>'
            '</doi_batch>'
        )

        xml_crossref_pid_pipe(xml_crossref, xml_tree)

        obtained = ET.tostring(xml_crossref, encoding="utf-8").decode("utf-8")

        self.assertIn(expected, obtained)

    def test_xml_elocation_pipe(self):
        xml_tree = ET.fromstring(
            """
            <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink"
            article-type="research-article" dtd-version="1.0" specific-use="sps-1.6" xml:lang="pt">
                <front>
                    <article-meta>
                        <article-id pub-id-type="publisher-id" specific-use="scielo-v3">XZrRmc87LzCkDtLdcXwgztp</article-id>
                        <article-id pub-id-type="publisher-id" specific-use="scielo-v2">S0103-21002017000400333</article-id>
                        <article-id pub-id-type="publisher-id">1982-0194201700050</article-id>
                        <article-id pub-id-type="doi">10.1590/1982-0194201700050</article-id>
                        <elocation-id>e20210569</elocation-id>
                    </article-meta>
                </front>
            </article>
            """
        )
        expected = (
            '<doi_batch>'
            '<head>'
            '<doi_batch_id>3f23a73dfbac48288d22545e53414203</doi_batch_id>'
            '<timestamp>20230418180226</timestamp>'
            '</head>'
            '<body>'
            '<journal>'
            '<journal_article>'
            '<publisher_item>'
            '<item_number item_number_type="article_number">e20210569</item_number>'
            '</publisher_item>'
            '</journal_article>'
            '</journal>'
            '</body>'
            '</doi_batch>'
        )

        xml_crossref = ET.fromstring(
            '<doi_batch>'
            '<head>'
            '<doi_batch_id>3f23a73dfbac48288d22545e53414203</doi_batch_id>'
            '<timestamp>20230418180226</timestamp>'
            '</head>'
            '<body>'
            '<journal>'
            '<journal_article>'
            '<publisher_item>'
            '</publisher_item>'
            '</journal_article>'
            '</journal>'
            '</body>'
            '</doi_batch>'
        )

        xml_crossref_elocation_pipe(xml_crossref, xml_tree)

        obtained = ET.tostring(xml_crossref, encoding="utf-8").decode("utf-8")

        self.assertIn(expected, obtained)

    def test_xml_permissions_pipe(self):
        xml_tree = ET.fromstring(
            """
            <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink"
            article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
            <front>
            <article-meta>
            <article-id specific-use="scielo-v3" pub-id-type="publisher-id">ZwzqmpTpbhTmtwR9GfDzP7c</article-id>
            <article-id specific-use="scielo-v2" pub-id-type="publisher-id">S0080-62342022000100445</article-id>
            <article-id pub-id-type="doi">10.1590/1980-220X-REEUSP-2021-0569en</article-id>
            <article-id pub-id-type="other">00445</article-id>
            <permissions>
            <license license-type="open-access" xlink:href="https://creativecommons.org/licenses/by/4.0/" xml:lang="en">
            <license-p>This is an Open Access article distributed under the terms of the Creative Commons Attribution License, which permits unrestricted use, distribution, and reproduction in any medium, provided the original work is properly cited.</license-p>
            </license>
            </permissions>
            </article-meta>
            </front>
            <sub-article article-type="translation" id="s1" xml:lang="pt">
            </sub-article>
            </article>
            """
        )
        expected = (
            '<body>'
            '<journal>'
            '<journal_article language="en" publication_type="research-article" reference_distribution_opts="any">'
            '<ai:program name="AccessIndicators">'
            '<ai:free_to_read/>'
            '<ai:license_ref applies_to="vor">https://creativecommons.org/licenses/by/4.0/</ai:license_ref>'
            '<ai:license_ref applies_to="am">https://creativecommons.org/licenses/by/4.0/</ai:license_ref>'
            '<ai:license_ref applies_to="tdm">https://creativecommons.org/licenses/by/4.0/</ai:license_ref>'
            '</ai:program>'
            '</journal_article>'
            '<journal_article language="pt" publication_type="translation" reference_distribution_opts="any">'
            '<ai:program name="AccessIndicators">'
            '<ai:free_to_read/>'
            '<ai:license_ref applies_to="vor">https://creativecommons.org/licenses/by/4.0/</ai:license_ref>'
            '<ai:license_ref applies_to="am">https://creativecommons.org/licenses/by/4.0/</ai:license_ref>'
            '<ai:license_ref applies_to="tdm">https://creativecommons.org/licenses/by/4.0/</ai:license_ref>'
            '</ai:program>'
            '</journal_article>'
            '</journal>'
            '</body>'
        )

        # xml_crossref = ET.fromstring(
        #     '<doi_batch '
        #     'xmlns="http://www.crossref.org/schema/4.4.0" '
        #     'xmlns:ai="http://www.crossref.org/AccessIndicators.xsd" '
        #     'xmlns:jats="http://www.ncbi.nlm.nih.gov/JATS1" '
        #     'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" version="4.4.0" '
        #     'xsi:schemaLocation="http://www.crossref.org/schema/4.4.0 '
        #     'http://www.crossref.org/schemas/crossref4.4.0.xsd">'
        #     '<body>'
        #     '<journal>'
        #     '<journal_article xmlns:ai="http://www.crossref.org/AccessIndicators.xsd" '
        #     'xmlns:jats="http://www.ncbi.nlm.nih.gov/JATS1" '
        #     'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" language="en" '
        #     'publication_type="research-article" reference_distribution_opts="any"/>'
        #     '<journal_article xmlns:ai="http://www.crossref.org/AccessIndicators.xsd" '
        #     'xmlns:jats="http://www.ncbi.nlm.nih.gov/JATS1" '
        #     'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" language="pt" '
        #     'publication_type="translation" reference_distribution_opts="any"/>'
        #     '</journal>'
        #     '</body>'
        #     '</doi_batch>'
        # )

        xml_crossref = setup_doi_batch_pipe()
        xml_crossref_body_pipe(xml_crossref)
        xml_crossref_journal_pipe(xml_crossref)
        xml_crossref_journal_article_pipe(xml_crossref, xml_tree)

        xml_crossref_permissions_pipe(xml_crossref, xml_tree)

        obtained = ET.tostring(xml_crossref, encoding="utf-8").decode("utf-8")

        self.assertIn(expected, obtained)

    def test_xml_articletitles_pipe(self):
        xml_tree = ET.fromstring(
            """
            <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink"
            article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
            <front>
            <article-meta>
            <article-id specific-use="scielo-v3" pub-id-type="publisher-id">ZwzqmpTpbhTmtwR9GfDzP7c</article-id>
            <article-id specific-use="scielo-v2" pub-id-type="publisher-id">S0080-62342022000100445</article-id>
            <article-id pub-id-type="doi">10.1590/1980-220X-REEUSP-2021-0569en</article-id>
            <article-id pub-id-type="other">00445</article-id>
            <title-group>
            <article-title>Effects of an educational intervention with nursing professionals on approaches to hospitalized smokers: a quasi-experimental study<xref ref-type="fn" rid="FN1">*</xref></article-title>
            <trans-title-group xml:lang="es">
            <trans-title>Efectos de una intervención educativa con profesionales de enfermería en el abordaje de pacientes fumadores: un estudio cuasi-experimental</trans-title>
            </trans-title-group>
            </title-group>
            </article-meta>
            </front>
            <sub-article article-type="translation" id="s1" xml:lang="pt">
            <front-stub>
            <title-group>
            <article-title>Efeitos de uma intervenção educativa com profissionais de enfermagem sobre abordagens ao paciente tabagista: estudo quase-experimental<xref ref-type="fn" rid="FN2">*</xref></article-title>
            </title-group>
            </front-stub>
            </sub-article>
            </article>
            """
        )
        expected = (
            '<body>'
            '<journal>'
            '<journal_article language="en" publication_type="research-article" reference_distribution_opts="any">'
            '<titles>'
            '<title>Effects of an educational intervention with nursing professionals on approaches to hospitalized smokers: a quasi-experimental study</title>'
            '<original_language_title language="pt">Efeitos de uma intervenção educativa com profissionais de enfermagem sobre abordagens ao paciente tabagista: estudo quase-experimental</original_language_title>'
            '</titles>'
            '</journal_article>'
            '<journal_article language="pt" publication_type="translation" reference_distribution_opts="any">'
            '<titles>'
            '<title>Efeitos de uma intervenção educativa com profissionais de enfermagem sobre abordagens ao paciente tabagista: estudo quase-experimental</title>'
            '<original_language_title language="en">Effects of an educational intervention with nursing professionals on approaches to hospitalized smokers: a quasi-experimental study</original_language_title>'
            '</titles>'
            '</journal_article>'
            '</journal>'
            '</body>'
        )
        # xml_crossref = ET.fromstring(
        #     '<doi_batch xmlns:ai="http://www.crossref.org/AccessIndicators.xsd" '
        #     'xmlns:jats="http://www.ncbi.nlm.nih.gov/JATS1" '
        #     'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" version="4.4.0" '
        #     'xmlns="http://www.crossref.org/schema/4.4.0" '
        #     'xsi:schemaLocation="http://www.crossref.org/schema/4.4.0 '
        #     'http://www.crossref.org/schemas/crossref4.4.0.xsd">'
        #     '<body>'
        #     '<journal>'
        #     '<journal_article language="en" publication_type="research-article" reference_distribution_opts="any" />'
        #     '<journal_article language="pt" publication_type="translation" reference_distribution_opts="any" />'
        #     '</journal>'
        #     '</body>'
        #     '</doi_batch>'
        # )

        xml_crossref = setup_doi_batch_pipe()
        xml_crossref_body_pipe(xml_crossref)
        xml_crossref_journal_pipe(xml_crossref)
        xml_crossref_journal_article_pipe(xml_crossref, xml_tree)

        xml_crossref_article_titles_pipe(xml_crossref, xml_tree)

        obtained = ET.tostring(xml_crossref, encoding="utf-8").decode("utf-8")

        self.assertIn(expected, obtained)

    def test_xml_programrelateditem_pipe(self):
        xml_tree = ET.fromstring(
            """
            <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
            <front>
            <article-meta>
            <article-id specific-use="scielo-v3" pub-id-type="publisher-id">ZwzqmpTpbhTmtwR9GfDzP7c</article-id>
            <article-id specific-use="scielo-v2" pub-id-type="publisher-id">S0080-62342022000100445</article-id>
            <article-id pub-id-type="doi">10.1590/1980-220X-REEUSP-2021-0569en</article-id>
            <article-id pub-id-type="other">00445</article-id>
            <title-group>
            <article-title>Effects of an educational intervention with nursing professionals on approaches to hospitalized smokers: a quasi-experimental study<xref ref-type="fn" rid="FN1">*</xref></article-title>
            <trans-title-group xml:lang="es">
            <trans-title>Efectos de una intervención educativa con profesionales de enfermería en el abordaje de pacientes fumadores: un estudio cuasi-experimental</trans-title></trans-title-group>
            </title-group>
            </article-meta>
            </front>
            <sub-article article-type="translation" id="s1" xml:lang="pt">
            <front-stub>
            <article-id pub-id-type="doi">10.1590/1980-220X-REEUSP-2021-0569pt</article-id>
            <title-group>
            <article-title>Efeitos de uma intervenção educativa com profissionais de enfermagem sobre abordagens ao paciente tabagista: estudo quase-experimental<xref ref-type="fn" rid="FN2">*</xref></article-title>
            </title-group>
            </front-stub>
            </sub-article>
            </article>
            """
        )
        expected = (
            '<body>'
            '<journal>'
            '<journal_article language="en" publication_type="research-article" reference_distribution_opts="any">'
            '<program xmlns="http://www.crossref.org/relations.xsd">'
            '<related_item>'
            '<description>'
            'Efeitos de uma intervenção educativa com profissionais de enfermagem sobre abordagens ao paciente tabagista: estudo quase-experimental'
            '</description>'
            '<intra_work_relation relationship-type="isTranslationOf" identifier-type="doi">10.1590/1980-220X-REEUSP-2021-0569pt</intra_work_relation>'
            '</related_item>'
            '</program>'
            '</journal_article>'
            '<journal_article language="pt" publication_type="translation" reference_distribution_opts="any">'
            '<program xmlns="http://www.crossref.org/relations.xsd">'
            '<related_item>'
            '<description>Effects of an educational intervention with nursing professionals on approaches to hospitalized smokers: a quasi-experimental study</description>'
            '<intra_work_relation relationship-type="hasTranslation" identifier-type="doi">10.1590/1980-220X-REEUSP-2021-0569en</intra_work_relation>'
            '</related_item>'
            '</program>'
            '</journal_article>'
            '</journal>'
            '</body>'
        )

        xml_crossref = setup_doi_batch_pipe()
        xml_crossref_body_pipe(xml_crossref)
        xml_crossref_journal_pipe(xml_crossref)
        xml_crossref_journal_article_pipe(xml_crossref, xml_tree)

        xml_crossref_program_related_item_pipe(xml_crossref, xml_tree)

        obtained = ET.tostring(xml_crossref, encoding="utf-8").decode("utf-8")

        self.assertIn(expected, obtained)

    def test_xml_doi_data_pipe(self):
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
            '<journal_article language="en" publication_type="research-article" reference_distribution_opts="any">'
            '<doi_data />'
            '</journal_article>'
            '<journal_article language="pt" publication_type="translation" reference_distribution_opts="any">'
            '<doi_data />'
            '</journal_article>'
            '</journal>'
            '</body>'
        )

        xml_crossref = setup_doi_batch_pipe()
        xml_crossref_body_pipe(xml_crossref)
        xml_crossref_journal_pipe(xml_crossref)
        xml_crossref_journal_article_pipe(xml_crossref, xml_tree)

        xml_crossref_doi_data_pipe(xml_crossref)

        self.assertIsNotNone(xml_crossref.find('.//doi_data'))

    def test_xml_doi_pipe(self):
        xml_tree = ET.fromstring(
            """
            <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
            <front>
            <article-meta>
            <article-id specific-use="scielo-v3" pub-id-type="publisher-id">ZwzqmpTpbhTmtwR9GfDzP7c</article-id>
            <article-id specific-use="scielo-v2" pub-id-type="publisher-id">S0080-62342022000100445</article-id>
            <article-id pub-id-type="doi">10.1590/1980-220X-REEUSP-2021-0569en</article-id>
            <article-id pub-id-type="other">00445</article-id>
            <title-group>
            <article-title>Effects of an educational intervention with nursing professionals on approaches to hospitalized smokers: a quasi-experimental study<xref ref-type="fn" rid="FN1">*</xref></article-title>
            <trans-title-group xml:lang="es">
            <trans-title>Efectos de una intervención educativa con profesionales de enfermería en el abordaje de pacientes fumadores: un estudio cuasi-experimental</trans-title></trans-title-group>
            </title-group>
            </article-meta>
            </front>
            <sub-article article-type="translation" id="s1" xml:lang="pt">
            <front-stub>
            <article-id pub-id-type="doi">10.1590/1980-220X-REEUSP-2021-0569pt</article-id>
            <title-group>
            <article-title>Efeitos de uma intervenção educativa com profissionais de enfermagem sobre abordagens ao paciente tabagista: estudo quase-experimental<xref ref-type="fn" rid="FN2">*</xref></article-title>
            </title-group>
            </front-stub>
            </sub-article>
            </article>
            """
        )

        expected = (
            '<body>'
            '<journal>'
            '<journal_article language="en" publication_type="research-article" reference_distribution_opts="any">'
            '<doi_data>'
            '<doi>10.1590/1980-220X-REEUSP-2021-0569en</doi>'
            '</doi_data>'
            '</journal_article>'
            '<journal_article language="pt" publication_type="translation" reference_distribution_opts="any">'
            '<doi_data>'
            '<doi>10.1590/1980-220X-REEUSP-2021-0569pt</doi>'
            '</doi_data>'
            '</journal_article>'
            '</journal>'
            '</body>'
        )

        xml_crossref = setup_doi_batch_pipe()
        xml_crossref_body_pipe(xml_crossref)
        xml_crossref_journal_pipe(xml_crossref)
        xml_crossref_journal_article_pipe(xml_crossref, xml_tree)
        xml_crossref_doi_data_pipe(xml_crossref)

        xml_crossref_doi_pipe(xml_crossref, xml_tree)

        obtained = ET.tostring(xml_crossref, encoding="utf-8").decode("utf-8")

        self.assertIn(expected, obtained)

    def test_xml_resource_pipe(self):
        xml_tree = ET.fromstring(
            """
            <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
            <front>
            <article-meta>
            <article-id specific-use="scielo-v3" pub-id-type="publisher-id">ZwzqmpTpbhTmtwR9GfDzP7c</article-id>
            <article-id specific-use="scielo-v2" pub-id-type="publisher-id">S0080-62342022000100445</article-id>
            <article-id pub-id-type="doi">10.1590/1980-220X-REEUSP-2021-0569en</article-id>
            <article-id pub-id-type="other">00445</article-id>
            </article-meta>
            </front>
            <sub-article article-type="translation" id="s1" xml:lang="pt">
            <front-stub>
            <article-id pub-id-type="doi">10.1590/1980-220X-REEUSP-2021-0569pt</article-id>
            </front-stub>
            </sub-article>
            </article>
            """
        )

        expected = (
            '<body>'
            '<journal>'
            '<journal_article language="en" publication_type="research-article" reference_distribution_opts="any">'
            '<doi_data>'
            '<resource>http://www.scielo.br/scielo.php?script=sci_arttext&amp;pid=S0080-62342022000100445&amp;tlng=en</resource>'
            '</doi_data>'
            '</journal_article>'
            '<journal_article language="pt" publication_type="translation" reference_distribution_opts="any">'
            '<doi_data>'
            '<resource>http://www.scielo.br/scielo.php?script=sci_arttext&amp;pid=S0080-62342022000100445&amp;tlng=pt</resource>'
            '</doi_data>'
            '</journal_article>'
            '</journal>'
            '</body>'
        )

        xml_crossref = setup_doi_batch_pipe()
        xml_crossref_body_pipe(xml_crossref)
        xml_crossref_journal_pipe(xml_crossref)
        xml_crossref_journal_article_pipe(xml_crossref, xml_tree)
        xml_crossref_doi_data_pipe(xml_crossref)

        xml_crossref_resource_pipe(xml_crossref, xml_tree)

        obtained = ET.tostring(xml_crossref, encoding="utf-8").decode("utf-8")

        self.assertIn(expected, obtained)

    def test_xml_collection_pipe(self):
        xml_tree = ET.fromstring(
            """
            <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
            <front>
            <article-meta>
            <article-id specific-use="scielo-v3" pub-id-type="publisher-id">ZwzqmpTpbhTmtwR9GfDzP7c</article-id>
            <article-id specific-use="scielo-v2" pub-id-type="publisher-id">S0080-62342022000100445</article-id>
            <article-id pub-id-type="doi">10.1590/1980-220X-REEUSP-2021-0569en</article-id>
            <article-id pub-id-type="other">00445</article-id>
            </article-meta>
            </front>
            <sub-article article-type="translation" id="s1" xml:lang="pt">
            <front-stub>
            <article-id pub-id-type="doi">10.1590/1980-220X-REEUSP-2021-0569pt</article-id>
            </front-stub>
            </sub-article>
            </article>
            """
        )

        expected = (
            '<body>'
            '<journal>'
            '<journal_article language="en" publication_type="research-article" reference_distribution_opts="any">'
            '<doi_data>'
            '<collection property="crawler-based">'
            '<item crawler="iParadigms">'
            '<resource>http://www.scielo.br/scielo.php?script=sci_pdf&amp;pid=S0080-62342022000100445&amp;tlng=en</resource>'
            '</item>'
            '</collection>'
            '</doi_data>'
            '</journal_article>'
            '<journal_article language="pt" publication_type="translation" reference_distribution_opts="any">'
            '<doi_data>'
            '<collection property="crawler-based">'
            '<item crawler="iParadigms">'
            '<resource>http://www.scielo.br/scielo.php?script=sci_pdf&amp;pid=S0080-62342022000100445&amp;tlng=pt</resource>'
            '</item>'
            '</collection>'
            '</doi_data>'
            '</journal_article>'
            '</journal>'
            '</body>'
        )

        xml_crossref = setup_doi_batch_pipe()
        xml_crossref_body_pipe(xml_crossref)
        xml_crossref_journal_pipe(xml_crossref)
        xml_crossref_journal_article_pipe(xml_crossref, xml_tree)
        xml_crossref_doi_data_pipe(xml_crossref)

        xml_crossref_collection_pipe(xml_crossref, xml_tree)

        obtained = ET.tostring(xml_crossref, encoding="utf-8").decode("utf-8")

        self.assertIn(expected, obtained)

    def test_xml_article_citations_pipe(self):
        self.maxDiff = None
        xml_tree = ET.fromstring(
            """
            <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
            <back>
            <ref-list>
            <title>REFERENCES</title>
            <ref id="B1">
            <label>1</label>
            <mixed-citation>
            1. Tran B, Falster MO, Douglas K, Blyth F, Jorm LR. Smoking and potentially preventable hospitalisation: the benefit of smoking cessation in older ages. Drug Alcohol Depend. 2015;150:85-91. DOI:
            <ext-link ext-link-type="uri" xlink:href="https://doi.org/10.1016/j.drugalcdep.2015.02.028">https://doi.org/10.1016/j.drugalcdep.2015.02.028</ext-link>
            </mixed-citation>
            <element-citation publication-type="journal">
            <person-group person-group-type="author">
            <name>
            <surname>Tran</surname>
            <given-names>B</given-names>
            </name>
            <name>
            <surname>Falster</surname>
            <given-names>MO</given-names>
            </name>
            <name>
            <surname>Douglas</surname>
            <given-names>K</given-names>
            </name>
            <name>
            <surname>Blyth</surname>
            <given-names>F</given-names>
            </name>
            <name>
            <surname>Jorm</surname>
            <given-names>LR</given-names>
            </name>
            </person-group>
            <article-title>Smoking and potentially preventable hospitalisation: the benefit of smoking cessation in older ages</article-title>
            <source>Drug Alcohol Depend.</source>
            <year>2015</year>
            <volume>150</volume>
            <fpage>85</fpage>
            <lpage>91</lpage>
            <comment>
            DOI:
            <ext-link ext-link-type="uri" xlink:href="https://doi.org/10.1016/j.drugalcdep.2015.02.028">https://doi.org/10.1016/j.drugalcdep.2015.02.028</ext-link>
            </comment>
            </element-citation>
            </ref>
            <ref id="B2">
            <label>2</label>
            <mixed-citation>
            2. Kwon JA, Jeon W, Park EC, Kim JH, Kim SJ, Yoo KB, et al. Effects of disease detection on changes in smoking behavior. Yonsei Med J. 2015;56(4): 1143-9. DOI:
            <ext-link ext-link-type="uri" xlink:href="https://doi.org/10.3349/ymj.2015.56.4.1143">https://doi.org/10.3349/ymj.2015.56.4.1143</ext-link>
            </mixed-citation>
            <element-citation publication-type="journal">
            <person-group person-group-type="author">
            <name>
            <surname>Kwon</surname>
            <given-names>JA</given-names>
            </name>
            <name>
            <surname>Jeon</surname>
            <given-names>W</given-names>
            </name>
            <name>
            <surname>Park</surname>
            <given-names>EC</given-names>
            </name>
            <name>
            <surname>Kim</surname>
            <given-names>JH</given-names>
            </name>
            <name>
            <surname>Kim</surname>
            <given-names>SJ</given-names>
            </name>
            <name>
            <surname>Yoo</surname>
            <given-names>KB</given-names>
            </name>
            <etal/>
            </person-group>
            <article-title>Effects of disease detection on changes in smoking behavior</article-title>
            <source>Yonsei Med J.</source>
            <year>2015</year>
            <volume>56</volume>
            <issue>4</issue>
            <fpage>1143</fpage>
            <lpage>9</lpage>
            <comment>
            DOI:
            <ext-link ext-link-type="uri" xlink:href="https://doi.org/10.3349/ymj.2015.56.4.1143">https://doi.org/10.3349/ymj.2015.56.4.1143</ext-link>
            </comment>
            </element-citation>
            </ref>
            </ref-list>
            </back>
            <sub-article article-type="translation" id="s1" xml:lang="pt">
            </sub-article>
            </article>
            """
        )

        expected = (
            '<body>'
            '<journal>'
            '<journal_article language="en" publication_type="research-article" reference_distribution_opts="any">'
            '<citation_list>'
            '<citation key="ref1">'
            '<journal_title>Drug Alcohol Depend.</journal_title>'
            '<author>Tran B</author>'
            '<volume>150</volume>'
            '<first_page>85</first_page>'
            '<cYear>2015</cYear>'
            '<article_title>Smoking and potentially preventable hospitalisation: the benefit of smoking cessation in older ages</article_title>'
            '</citation>'
            '<citation key="ref2">'
            '<journal_title>Yonsei Med J.</journal_title>'
            '<author>Kwon JA</author>'
            '<volume>56</volume>'
            '<issue>4</issue>'
            '<first_page>1143</first_page>'
            '<cYear>2015</cYear>'
            '<article_title>Effects of disease detection on changes in smoking behavior</article_title>'
            '</citation>'
            '</citation_list>'
            '</journal_article>'
            '<journal_article language="pt" publication_type="translation" reference_distribution_opts="any">'
            '<citation_list>'
            '<citation key="ref1">'
            '<journal_title>Drug Alcohol Depend.</journal_title>'
            '<author>Tran B</author>'
            '<volume>150</volume>'
            '<first_page>85</first_page>'
            '<cYear>2015</cYear>'
            '<article_title>Smoking and potentially preventable hospitalisation: the benefit of smoking cessation in older ages</article_title>'
            '</citation>'
            '<citation key="ref2">'
            '<journal_title>Yonsei Med J.</journal_title>'
            '<author>Kwon JA</author>'
            '<volume>56</volume>'
            '<issue>4</issue>'
            '<first_page>1143</first_page>'
            '<cYear>2015</cYear>'
            '<article_title>Effects of disease detection on changes in smoking behavior</article_title>'
            '</citation>'
            '</citation_list>'
            '</journal_article>'
            '</journal>'
            '</body>'
        )

        xml_crossref = setup_doi_batch_pipe()
        xml_crossref_body_pipe(xml_crossref)
        xml_crossref_journal_pipe(xml_crossref)
        xml_crossref_journal_article_pipe(xml_crossref, xml_tree)

        xml_crossref_article_citations_pipe(xml_crossref, xml_tree)

        obtained = ET.tostring(xml_crossref, encoding="utf-8").decode("utf-8")

        self.assertIn(expected, obtained)

    # def test_xml_pipe_line_crossref(self):
    #     xmltree = xml_utils.get_xml_tree('tests/samples/scielo_format_example.xml')
    #     data = {
    #         "depositor_name": "depositor",
    #         "depositor_email_address": "name@domain.com",
    #         "registrant": "registrant"
    #     }
    #     xml_crossref = pipeline_crossref(xmltree, data)
    #     obtained = ET.tostring(xml_crossref, encoding="utf-8").decode("utf-8")
    #
    #     xml_crossref_expected = xml_utils.get_xml_tree('tests/samples/crossref_format_example.xml')
    #     expected = ET.tostring(xml_crossref_expected, encoding="utf-8").decode("utf-8")
    #
    #     self.assertEqual(expected, obtained)
