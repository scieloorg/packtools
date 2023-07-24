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

from unittest import TestCase, skip

from lxml import etree

from packtools.sps.models.article_authors import Authors


class AuthorsWithoutXrefTest(TestCase):
    def setUp(self):
        xml = """
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
                </contrib>
                </contrib-group>
            </article-meta>
          </front>
        </article>
        """
        xmltree = etree.fromstring(xml)
        self.authors = Authors(xmltree)

    def test_contribs(self):
        result = self.authors.contribs
        self.assertIsNone(result[0].get("rid"))


class AuthorsTest(TestCase):
    def setUp(self):
        xml = """
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
                  <xref ref-type="aff" rid="aff2"/>
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
        """
        xmltree = etree.fromstring(xml)
        self.authors = Authors(xmltree)

    def test_contribs(self):
        expected = [
            {
                "surname": "VENEGAS-MARTÍNEZ",
                "given_names": "FRANCISCO",
                "prefix": "Prof",
                "suffix": "Nieto",
                "rid": ["aff1", "aff2"],
                "contrib-type": "author",
            },
            {
                "surname": "Higa",
                "given_names": "Vanessa M.",
                "orcid": "0000-0001-5518-4853",
                "rid": ["aff1"],
                "contrib-type": "author",
            },
        ]
        result = self.authors.contribs
        self.assertDictEqual(expected[0], result[0])
        self.assertDictEqual(expected[1], result[1])

    def test_collab(self):
        self.assertIsNone(self.authors.collab)

    def test_role_with_role_content_type(self):
        xml = """
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
                    <xref ref-type="aff" rid="aff1">a</xref>
                    <role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Role 1</role>
                    <role content-type="https://credit.niso.org/contributor-roles/data-curation/">Role 2</role>
                    <role content-type="https://credit.niso.org/contributor-roles/formal-analysis/">Role 3</role>
                    <role content-type="https://credit.niso.org/contributor-roles/writing-original-draft/">Role 4</role>
                </contrib>
                <contrib contrib-type="author">
                  <contrib-id contrib-id-type="orcid">0000-0001-5518-4853</contrib-id>
                  <name>
                    <surname>Higa</surname>
                    <given-names>Vanessa M.</given-names>
                  </name>
                  <xref ref-type="aff" rid="aff1">a</xref>
                    <role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>
                    <role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>
                    <role content-type="https://credit.niso.org/contributor-roles/formal-analysis/">Formal Analysis</role>
                    <role content-type="https://credit.niso.org/contributor-roles/writing-original-draft/">Writing &#x2013; original draft</role>
                </contrib>
              </contrib-group>
            </article-meta>
          </front>
        </article>
        """

        data = etree.fromstring(xml)
        xmldata = Authors(data).contribs

        expect_output = [
            {
                "surname": "VENEGAS-MARTÍNEZ",
                "given_names": "FRANCISCO",
                "prefix": "Prof",
                "suffix": "Nieto",
                "role": [
                    {
                        "text": "Role 1",
                        "content-type": "https://credit.niso.org/contributor-roles/conceptualization/",
                    },
                    {
                        "text": "Role 2",
                        "content-type": "https://credit.niso.org/contributor-roles/data-curation/",
                    },
                    {
                        "text": "Role 3",
                        "content-type": "https://credit.niso.org/contributor-roles/formal-analysis/",
                    },
                    {
                        "text": "Role 4",
                        "content-type": "https://credit.niso.org/contributor-roles/writing-original-draft/",
                    },
                ],
                "rid": ["aff1"],
                "contrib-type": "author",
            },
            {
                "surname": "Higa",
                "given_names": "Vanessa M.",
                "orcid": "0000-0001-5518-4853",
                "role": [
                    {
                        "text": "Conceptualization",
                        "content-type": "https://credit.niso.org/contributor-roles/conceptualization/",
                    },
                    {
                        "text": "Data curation",
                        "content-type": "https://credit.niso.org/contributor-roles/data-curation/",
                    },
                    {
                        "text": "Formal Analysis",
                        "content-type": "https://credit.niso.org/contributor-roles/formal-analysis/",
                    },
                    {
                        "text": "Writing – original draft",
                        "content-type": "https://credit.niso.org/contributor-roles/writing-original-draft/",
                    },
                ],
                "rid": ["aff1"],
                "contrib-type": "author",
            },
        ]

        self.assertEqual(xmldata, expect_output)

    def test_role_wihtout_content_type(self):
        xml = """
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
                  <role>Role 1</role>
                  <role>Role 2</role>
                  <role>Role 3</role>
                  <role>Role 4</role>
                </contrib>
                <contrib contrib-type="author">
                  <contrib-id contrib-id-type="orcid">0000-0001-5518-4853</contrib-id>
                  <name>
                    <surname>Higa</surname>
                    <given-names>Vanessa M.</given-names>
                  </name>
                  <xref ref-type="aff" rid="aff1">a</xref>
                  <role>Conceptualization</role>
                  <role>Data curation</role>
                  <role>Formal Analysis</role>
                  <role>Writing &#x2013; original draft</role>
                </contrib>
              </contrib-group>
            </article-meta>
          </front>
        </article>
        """
        data = etree.fromstring(xml)
        xmldata = Authors(data).contribs

        expected_output = [
            {
                "surname": "VENEGAS-MARTÍNEZ",
                "prefix": "Prof",
                "suffix": "Nieto",
                "given_names": "FRANCISCO",
                "role": [
                    {"text": "Role 1", "content-type": None},
                    {"text": "Role 2", "content-type": None},
                    {"text": "Role 3", "content-type": None},
                    {"text": "Role 4", "content-type": None},
                ],
                "rid": ["aff1"],
                "contrib-type": "author",
            },
            {
                "surname": "Higa",
                "given_names": "Vanessa M.",
                "orcid": "0000-0001-5518-4853",
                "role": [
                    {"text": "Conceptualization", "content-type": None},
                    {"text": "Data curation", "content-type": None},
                    {"text": "Formal Analysis", "content-type": None},
                    {"text": "Writing – original draft", "content-type": None},
                ],
                "rid": ["aff1"],
                "contrib-type": "author",
            },
        ]

        self.assertEqual(xmldata, expected_output)


class AuthorsCollabTest(TestCase):
    def setUp(self):
        xml = """
        <article>
        <front>
            <article-meta>
              <contrib-group>
                <collab>XXXX</collab>
                </contrib-group>
            </article-meta>
          </front>
        </article>
        """
        xmltree = etree.fromstring(xml)
        self.authors = Authors(xmltree)

    def test_contribs(self):
        self.assertEqual([], self.authors.contribs)

    def test_collab(self):
        self.assertEqual("XXXX", self.authors.collab)


class AuthorsWithAffTest(TestCase):
    def setUp(self):
        xml = """
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
                          <xref ref-type="aff" rid="aff2"/>
                        </contrib>
                    </contrib-group>
                    <aff id="aff1">
                        <label>I</label>
                        <institution content-type="orgname">Secretaria Municipal de Saúde de Belo Horizonte</institution>
                        <addr-line>
                            <named-content content-type="city">Belo Horizonte</named-content>
                            <named-content content-type="state">MG</named-content>
                        </addr-line>
                        <country>Brasil</country>
                        <institution content-type="original">Secretaria Municipal de Saúde de Belo Horizonte. Belo Horizonte, MG, Brasil</institution>
                    </aff>
                    <aff id="aff2">
                        <label>II</label>
                        <institution content-type="orgdiv1">Faculdade de Medicina</institution>
                        <institution content-type="orgname">Universidade Federal de Minas Gerais</institution>
                        <addr-line>
                            <named-content content-type="city">Belo Horizonte</named-content>
                            <named-content content-type="state">MG</named-content>
                        </addr-line>
                        <country>Brasil</country>
                        <institution content-type="original">Grupo de Pesquisas em Epidemiologia e Avaliação em Saúde. Faculdade de Medicina. Universidade Federal de Minas Gerais. Belo Horizonte, MG, Brasil</institution>
                    </aff>
                </article-meta>
            </front>
        </article>
        """
        xmltree = etree.fromstring(xml)
        self.authors = Authors(xmltree)

    def test_contribs(self):
        expected = [
            {
                "surname": "VENEGAS-MARTÍNEZ",
                "prefix": "Prof",
                "suffix": "Nieto",
                "given_names": "FRANCISCO",
                "rid": "aff2",
                "rid-aff": ["aff1", "aff2"],
                "aff_rids": ["aff1", "aff2"],
                "contrib-type": "author",
                "affs": [
                    {
                        "id": "aff1",
                        "label": "I",
                        "orgname": "Secretaria Municipal de Saúde de Belo Horizonte",
                        "orgdiv1": None,
                        "orgdiv2": None,
                        "original": "Secretaria Municipal de Saúde de Belo Horizonte. Belo Horizonte, MG, Brasil",
                        "city": "Belo Horizonte",
                        "state": "MG",
                        "country_code": None,
                        "country_name": "Brasil",
                        "email": None,
                    },
                    {
                        "id": "aff2",
                        "label": "II",
                        "city": "Belo Horizonte",
                        "state": "MG",
                        "country_code": None,
                        "country_name": "Brasil",
                        "orgname": "Universidade Federal de Minas Gerais",
                        "orgdiv1": "Faculdade de Medicina",
                        "orgdiv2": None,
                        "original": "Grupo de Pesquisas em Epidemiologia e Avaliação em Saúde. Faculdade de Medicina. Universidade Federal de Minas Gerais. Belo Horizonte, MG, Brasil",
                        "email": None,
                    },
                ],
            }
        ]
        for item in self.authors.contribs_with_affs:
            with self.subTest(item):
                self.assertDictEqual(expected[0], item)


class AuthorsWithAffInContribGroupTest(TestCase):
    def setUp(self):
        xml = """
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
                          <xref ref-type="aff" rid="aff2"/>
                        </contrib>
                        <aff id="aff1">
                            <label>I</label>
                            <institution content-type="orgname">Secretaria Municipal de Saúde de Belo Horizonte</institution>
                            <addr-line>
                                <named-content content-type="city">Belo Horizonte</named-content>
                                <named-content content-type="state">MG</named-content>
                            </addr-line>
                            <country>Brasil</country>
                            <institution content-type="original">Secretaria Municipal de Saúde de Belo Horizonte. Belo Horizonte, MG, Brasil</institution>
                        </aff>
                        <aff id="aff2">
                            <label>II</label>
                            <institution content-type="orgdiv1">Faculdade de Medicina</institution>
                            <institution content-type="orgname">Universidade Federal de Minas Gerais</institution>
                            <addr-line>
                                <named-content content-type="city">Belo Horizonte</named-content>
                                <named-content content-type="state">MG</named-content>
                            </addr-line>
                            <country>Brasil</country>
                            <institution content-type="original">Grupo de Pesquisas em Epidemiologia e Avaliação em Saúde. Faculdade de Medicina. Universidade Federal de Minas Gerais. Belo Horizonte, MG, Brasil</institution>
                        </aff>
                    </contrib-group>
                </article-meta>
            </front>
        </article>
        """
        xmltree = etree.fromstring(xml)
        self.authors = Authors(xmltree)

    def test_contribs(self):
        expected = [
            {
                "surname": "VENEGAS-MARTÍNEZ",
                "prefix": "Prof",
                "suffix": "Nieto",
                "given_names": "FRANCISCO",
                "rid": "aff2",
                "rid-aff": ["aff1", "aff2"],
                "aff_rids": ["aff1", "aff2"],
                "contrib-type": "author",
                "affs": [
                    {
                        "id": "aff1",
                        "label": "I",
                        "orgname": "Secretaria Municipal de Saúde de Belo Horizonte",
                        "orgdiv1": None,
                        "orgdiv2": None,
                        "original": "Secretaria Municipal de Saúde de Belo Horizonte. Belo Horizonte, MG, Brasil",
                        "city": "Belo Horizonte",
                        "state": "MG",
                        "country_code": None,
                        "country_name": "Brasil",
                        "email": None,
                    },
                    {
                        "id": "aff2",
                        "label": "II",
                        "city": "Belo Horizonte",
                        "state": "MG",
                        "country_code": None,
                        "country_name": "Brasil",
                        "orgname": "Universidade Federal de Minas Gerais",
                        "orgdiv1": "Faculdade de Medicina",
                        "orgdiv2": None,
                        "original": "Grupo de Pesquisas em Epidemiologia e Avaliação em Saúde. Faculdade de Medicina. Universidade Federal de Minas Gerais. Belo Horizonte, MG, Brasil",
                        "email": None,
                    },
                ],
            }
        ]
        for item in self.authors.contribs_with_affs:
            with self.subTest(item):
                self.assertDictEqual(expected[0], item)
