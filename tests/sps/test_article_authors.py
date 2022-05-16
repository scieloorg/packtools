"""<article>
<front>
    <article-meta>
      <contrib-group>
        <contrib contrib-type="author">
          <name>
            <surname>VENEGAS-MARTÍNEZ</surname>
            <given-names>FRANCISCO</given-names>
          </name>
          <xref ref-type="aff" rid="aff1"/>
        </contrib>
      </contrib-group>
    </article-meta>
  </front>
</article>
"""

from packtools.sps.models.article_authors import (
    Authors,
)
from unittest import TestCase, skip

from lxml import etree


class AuthorsTest(TestCase):

    def setUp(self):
        xml = ("""
        <article>
        <front>
            <article-meta>
              <contrib-group>
                <contrib contrib-type="author">
                  <name>
                    <surname>VENEGAS-MARTÍNEZ</surname>
                    <given-names>FRANCISCO</given-names>
                    <prefix>Prof</prefix>
                    <suffix>Nieto</suffix>
                  </name>
                  <xref ref-type="aff" rid="aff1"/>
                </contrib>
                <contrib contrib-type="author">
                  <contrib-id contrib-id-type="orcid">0000-0001-5518-4853</contrib-id>
                  <name>
                    <surname>Higa</surname>
                    <given-names>Vanessa M.</given-names>
                  </name>
                  <xref ref-type="aff" rid="aff1">a</xref>
                </contrib>
              </contrib-group>
            </article-meta>
          </front>
        </article>
        """)
        xmltree = etree.fromstring(xml)
        self.authors = Authors(xmltree)

    def test_contribs(self):
        expected = [
            {"surname": "VENEGAS-MARTÍNEZ", "given_names": "FRANCISCO",
             "prefix": "Prof", "suffix": "Nieto"},
            {"surname": "Higa", "given_names": "Vanessa M.",
             "orcid": "0000-0001-5518-4853"
            },
        ]
        result = self.authors.contribs
        self.assertDictEqual(expected[0], result[0])
        self.assertDictEqual(expected[1], result[1])

    def test_collab(self):
        self.assertIsNone(self.authors.collab)


class AuthorsCollabTest(TestCase):

    def setUp(self):
        xml = ("""
        <article>
        <front>
            <article-meta>
              <contrib-group>
                <collab>XXXX</collab>
                </contrib-group>
            </article-meta>
          </front>
        </article>
        """)
        xmltree = etree.fromstring(xml)
        self.authors = Authors(xmltree)

    def test_contribs(self):
        self.assertEqual([], self.authors.contribs)

    def test_collab(self):
        self.assertEqual("XXXX", self.authors.collab)
