from unittest import TestCase
from unittest.mock import patch
import datetime
from lxml import etree

from packtools.sps.formats.am import h_record


class HRecord(TestCase):

    def test_code(self):
        self.xml_tree = etree.fromstring(
            """
            <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink" 
            article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="pt">
            <front>
            <article-meta>
            <article-id specific-use="scielo-v2" pub-id-type="publisher-id">S1414-98932020000100118</article-id>
            </article-meta>
            </front>
            </article>
            """
        )
        self.assertDictEqual(
            {"code": "S1414-98932020000100118"}, h_record.code(self.xml_tree, dict())
        )

    @patch("packtools.sps.formats.am.h_record.datetime")
    def test_processing_date(self, mock_datetime):
        fixed_time = datetime.datetime(2023, 5, 17, 12, 30, 45, 123456, tzinfo=datetime.timezone.utc)

        mock_datetime.datetime.now.return_value = fixed_time
        mock_datetime.timezone.utc = datetime.timezone.utc

        h_record_dict = {}

        result = h_record.processing_date(h_record_dict)
        expected_date = "2023-05-17T12:30:45.123Z"

        self.assertEqual(result["processing_date"], expected_date)

    def test_wos_status(self):
        self.assertDictEqual(
            {"sent_wos": False, "validated_wos": False}, h_record.wos_status(dict())
        )

    def test_code_issue(self):
        self.xml_tree = etree.fromstring(
            """
            <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink" 
            article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="pt">
            <front>
            <article-meta>
            <article-id specific-use="scielo-v2" pub-id-type="publisher-id">S1414-98932020000100118</article-id>
            </article-meta>
            </front>
            </article>
            """
        )
        self.assertDictEqual(
            {"code_issue": "1414-989320200001"}, h_record.code_issue(self.xml_tree, dict())
        )

    def test_code_title(self):
        self.xml_tree = etree.fromstring(
            """
            <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink" 
            article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="pt">
            <journal-meta>
            <issn pub-type="ppub">1679-4974</issn>
            <issn pub-type="epub">2237-9622</issn>
            </journal-meta>
            </article>
            """
        )
        self.assertDictEqual(
            {"code_title": ["1679-4974", "2237-9622"]}, h_record.code_title(self.xml_tree, dict())
        )

    def test_doi(self):
        self.xml_tree = etree.fromstring(
            """
            <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink" 
            article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="pt">
            <front>
            <article-meta>
            <article-id pub-id-type="doi">10.1590/S2237-96222023000200017</article-id>
            </article-meta>
            </front>
            </article>
            """
        )
        self.assertDictEqual(
            {"doi": "10.1590/S2237-96222023000200017"}, h_record.doi(self.xml_tree, dict())
        )

    def test_applicable(self):
        self.assertDictEqual(
            {"applicable": False}, h_record.applicable(xml_tree=None, h_record_dict={})
        )

    def test_publication_year(self):
        self.xml_tree = etree.fromstring(
            """
            <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink" 
            article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="pt">
            <front>
            <article-meta>
            <pub-date date-type="pub" publication-format="electronic">
            <day>18</day>
            <month>08</month>
            <year>2023</year>
            </pub-date>
            </article-meta>
            </front>
            </article>
            """
        )
        obtained = h_record.publication_dates(xml_tree=self.xml_tree, h_record_dict={})
        self.assertEqual("2023", obtained["publication_year"])

    def test_publication_date(self):
        self.xml_tree = etree.fromstring(
            """
            <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink" 
            article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="pt">
            <front>
            <article-meta>
            <pub-date date-type="pub" publication-format="electronic">
            <day>18</day>
            <month>08</month>
            <year>2023</year>
            </pub-date>
            </article-meta>
            </front>
            </article>
            """
        )
        obtained = h_record.publication_dates(xml_tree=self.xml_tree, h_record_dict={})
        self.assertEqual("2023-08-18", obtained["publication_date"])

