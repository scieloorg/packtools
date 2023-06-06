import unittest
from lxml import etree as ET

from packtools.sps.formats.pubmed import (
    xml_pubmed_article_pipe,
    xml_pubmed_journal_pipe,
    xml_pubmed_publisher_name_pipe,
    xml_pubmed_journal_title_pipe,
    xml_pubmed_issn_pipe,
    xml_pubmed_volume_pipe,
    xml_pubmed_issue_pipe,
    xml_pubmed_pub_date_pipe,
    xml_pubmed_article_title_pipe,
    xml_pubmed_first_page_pipe,
    xml_pubmed_elocation_pipe,
    xml_pubmed_language_pipe,
)


class PipelinePubmed(unittest.TestCase):
    def test_xml_pubmed_article_pipe(self):
        expected = (
            '<Article/>'
        )

        obtained = ET.tostring(xml_pubmed_article_pipe(), encoding="utf-8").decode("utf-8")

        self.assertEqual(obtained, expected)

