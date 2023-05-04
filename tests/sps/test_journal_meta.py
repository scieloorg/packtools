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

from packtools.sps.models import journal_meta


def _get_xmltree(issns=None, publisher=None):
    issns = issns or (
        """
        <issn>1678-6971</issn>
        <issn pub-type="epub">1678-6971</issn>
        <issn pub-type="ppub">0213-6971</issn>
        """
    )
    publisher = publisher or ''
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
              {publisher}
            </journal-meta>
        </front></article>
        """
    )
    xmltree = etree.fromstring(xml)
    return xmltree


class IssnTest(TestCase):

    def test_data(self):
        expected = [
            {"type": None, "value": "1678-6971"},
            {"type": "epub", "value": "1678-6971"},
            {"type": "ppub", "value": "0213-6971"},
        ]
        issns = journal_meta.ISSN(_get_xmltree())
        self.assertEqual(expected, issns.data)

    def test_epub(self):
        issns = journal_meta.ISSN(_get_xmltree())
        self.assertEqual("1678-6971", issns.epub)

    def test_ppub(self):
        issns = journal_meta.ISSN(_get_xmltree())
        self.assertEqual("0213-6971", issns.ppub)

    def test_without_pub_type(self):
        issns = journal_meta.ISSN(_get_xmltree())
        self.assertEqual("1678-6971", issns.without_pub_type)


class PublisherTest(TestCase):

  def test_data(self):
    publisher = """
    <publisher>
      <publisher-name>Editora Mackenzie; Universidade Presbiteriana Mackenzie</publisher-name>
    </publisher>
    """
    xmltree = _get_xmltree(publisher)
    
    expected = ['Editora Mackenzie; Universidade Presbiteriana Mackenzie']
    publishers_names = journal_meta.Publisher(xmltree).publishers_names
    self.assertEqual(expected, publishers_names)

  def test_multivalued_publisher(self):
    publisher = """
    <publisher>
      <publisher-name>SciELO Editor Group</publisher-name>
      <publisher-name>Editora Mackenzie; Universidade Presbiteriana Mackenzie</publisher-name>
    </publisher>
    """
    xmltree = _get_xmltree(publisher)

    expected = [
      'SciELO Editor Group', 
      'Editora Mackenzie; Universidade Presbiteriana Mackenzie'
    ]
    publishers_names = journal_meta.Publisher(xmltree).publishers_names
    self.assertListEqual(expected, publishers_names)
  