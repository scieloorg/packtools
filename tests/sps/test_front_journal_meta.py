"""<article>
<front>
    <journal-meta>
      <journal-id journal-id-type="publisher-id">ram</journal-id>
      <journal-title-group>
        <journal-title>RAM. Revista de Administração Mackenzie</journal-title>
        <abbrev-journal-title abbrev-type="publisher">RAM, Rev. Adm. Mackenzie</abbrev-journal-title>
      </journal-title-group>
      <issn pub-type="epub">1678-6971</issn>
      <issn pub-type="ppub">0213-6971</issn>
      <publisher>
        <publisher-name>Editora Mackenzie; Universidade Presbiteriana Mackenzie</publisher-name>
      </publisher>
    </journal-meta>
</article>
"""


from unittest import TestCase

from lxml import etree

from packtools.sps.models import front_journal_meta


def _get_xmltree(issns=None):
    issns = issns or (
        """
        <issn pub-type="epub">1678-6971</issn>
        <issn pub-type="ppub">0213-6971</issn>
        """
    )
    xml = (
        f"""
        <article>
        <front>
            <journal-meta>
              <journal-id journal-id-type="publisher-id">ram</journal-id>
              <journal-title-group>
                <journal-title>RAM. Revista de Administração Mackenzie</journal-title>
                <abbrev-journal-title abbrev-type="publisher">RAM, Rev. Adm. Mackenzie</abbrev-journal-title>
              </journal-title-group>
              {issns}
              <publisher>
                <publisher-name>Editora Mackenzie; Universidade Presbiteriana Mackenzie</publisher-name>
              </publisher>
            </journal-meta>
        </front></article>
        """
    )
    xmltree = etree.fromstring(xml)
    return xmltree


class IssnTest(TestCase):

    def test_data(self):
        expected = [
            {"type": "epub", "value": "1678-6971"},
            {"type": "ppub", "value": "0213-6971"},
        ]
        issns = front_journal_meta.ISSN(_get_xmltree())
        self.assertEqual(expected, issns.data)

    def test_epub(self):
        issns = front_journal_meta.ISSN(_get_xmltree())
        self.assertEqual("1678-6971", issns.epub)

    def test_ppub(self):
        issns = front_journal_meta.ISSN(_get_xmltree())
        self.assertEqual("0213-6971", issns.ppub)
