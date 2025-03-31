from unittest import TestCase, skip
from lxml import etree

from packtools.sps.models.article_contribs import (
    Contrib,
    ContribGroup,
    TextContribs,
    XMLContribs,
)


class ContribTest(TestCase):
    def setUp(self):
        xml = """
            <article>
                <front>
                    <article-meta>
                        <contrib-group>
                            <contrib contrib-type="author">
                                <contrib-id contrib-id-type="orcid">0000-0001-8528-2091</contrib-id>
                                <contrib-id contrib-id-type="scopus">24771926600</contrib-id>
                                <collab>The MARS Group</collab>
                                <name>
                                    <surname>Einstein</surname>
                                    <given-names>Albert</given-names>
                                    <prefix>Prof</prefix>
                                    <suffix>Nieto</suffix>
                                </name>
                                <xref ref-type="aff" rid="aff1">1</xref>
                                <role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>
                                <role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>
                                <role specific-use="reviewer">Reviewer</role>
                            </contrib>
                        </contrib-group>
                    </article-meta>
                </front>
            </article>
            """
        self.xmltree = etree.fromstring(xml)

    def test_contrib_type(self):
        contrib = self.xmltree.xpath(".//contrib")[0]
        obtained = Contrib(contrib).contrib_type
        self.assertEqual(obtained, "author")

    def test_contrib_ids(self):
        contrib = self.xmltree.xpath(".//contrib")[0]
        obtained = Contrib(contrib).contrib_ids
        expected = {"orcid": "0000-0001-8528-2091", "scopus": "24771926600"}
        self.assertDictEqual(obtained, expected)

    def test_contrib_name(self):
        contrib = self.xmltree.xpath(".//contrib")[0]
        obtained = Contrib(contrib).contrib_name
        expected = {
            "given-names": "Albert",
            "surname": "Einstein",
            "prefix": "Prof",
            "suffix": "Nieto",
        }
        self.assertDictEqual(obtained, expected)

    def test_collab(self):
        contrib = self.xmltree.xpath(".//contrib")[0]
        obtained = Contrib(contrib).collab
        self.assertEqual(obtained, "The MARS Group")

    def test_contrib_xref(self):
        contrib = self.xmltree.xpath(".//contrib")[0]
        obtained = list(Contrib(contrib).contrib_xref)
        expected = [{"rid": "aff1", "ref_type": "aff", "text": "1"}]
        for i, item in enumerate(expected):
            with self.subTest(i=i):
                self.assertDictEqual(item, obtained[i])

    def test_contrib_role(self):
        contrib = self.xmltree.xpath(".//contrib")[0]
        obtained = list(Contrib(contrib).contrib_role)
        expected = [
            {
                "text": "Data curation",
                "content-type": "https://credit.niso.org/contributor-roles/data-curation/",
                "specific-use": None,
            },
            {
                "text": "Conceptualization",
                "content-type": "https://credit.niso.org/contributor-roles/conceptualization/",
                "specific-use": None,
            },
            {
                "text": "Reviewer",
                "content-type": None,
                "specific-use": "reviewer",
            },
        ]
        for i, item in enumerate(expected):
            with self.subTest(i=i):
                self.assertDictEqual(item, obtained[i])

    def test_data(self):
        self.maxDiff = None
        contrib = self.xmltree.xpath(".//contrib")[0]
        obtained = Contrib(contrib).data
        expected = {
            "contrib_type": "author",
            "contrib_ids": {"orcid": "0000-0001-8528-2091", "scopus": "24771926600"},
            "collab": "The MARS Group",
            "contrib_full_name": "Prof Albert Einstein Nieto",
            "contrib_name": {
                "given-names": "Albert",
                "surname": "Einstein",
                "prefix": "Prof",
                "suffix": "Nieto",
            },
            "contrib_xref": [{"ref_type": "aff", "rid": "aff1", "text": "1"}],
            "contrib_role": [
                {
                    "content-type": "https://credit.niso.org/contributor-roles/data-curation/",
                    "specific-use": None,
                    "text": "Data curation",
                },
                {
                    "content-type": "https://credit.niso.org/contributor-roles/conceptualization/",
                    "specific-use": None,
                    "text": "Conceptualization",
                },
                {
                    "content-type": None,
                    "specific-use": "reviewer",
                    "text": "Reviewer",
                },
            ],
        }
        self.assertDictEqual(obtained, expected)


class ContribWithoutContribTypeTest(TestCase):
    def setUp(self):
        xml = """
            <article>
                <front>
                    <article-meta>
                        <contrib-group>
                            <contrib>
                                <contrib-id contrib-id-type="orcid">0000-0001-8528-2091</contrib-id>
                                <contrib-id contrib-id-type="scopus">24771926600</contrib-id>
                                <collab>The MARS Group</collab>
                                <name>
                                    <surname>Einstein</surname>
                                    <given-names>Albert</given-names>
                                    <prefix>Prof</prefix>
                                    <suffix>Nieto</suffix>
                                </name>
                                <xref ref-type="aff" rid="aff1">1</xref>
                                <role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>
                                <role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>
                                <role specific-use="reviewer">Reviewer</role>
                            </contrib>
                        </contrib-group>
                    </article-meta>
                </front>
            </article>
            """
        self.xmltree = etree.fromstring(xml)

    def test_data(self):
        self.maxDiff = None
        contrib = self.xmltree.xpath(".//contrib")[0]
        obtained = Contrib(contrib).data
        expected = {
            "contrib_ids": {"orcid": "0000-0001-8528-2091", "scopus": "24771926600"},
            "collab": "The MARS Group",
            "contrib_full_name": "Prof Albert Einstein Nieto",
            "contrib_name": {
                "given-names": "Albert",
                "surname": "Einstein",
                "prefix": "Prof",
                "suffix": "Nieto",
            },
            "contrib_xref": [{"ref_type": "aff", "rid": "aff1", "text": "1"}],
            "contrib_role": [
                {
                    "content-type": "https://credit.niso.org/contributor-roles/data-curation/",
                    "specific-use": None,
                    "text": "Data curation",
                },
                {
                    "content-type": "https://credit.niso.org/contributor-roles/conceptualization/",
                    "specific-use": None,
                    "text": "Conceptualization",
                },
                {
                    "content-type": None,
                    "specific-use": "reviewer",
                    "text": "Reviewer",
                },
            ],
        }
        self.assertDictEqual(obtained, expected)


class ContribWithoutContribIdTest(TestCase):
    def setUp(self):
        xml = """
            <article>
                <front>
                    <article-meta>
                        <contrib-group>
                            <contrib contrib-type="author">
                                <collab>The MARS Group</collab>
                                <name>
                                    <surname>Einstein</surname>
                                    <given-names>Albert</given-names>
                                    <prefix>Prof</prefix>
                                    <suffix>Nieto</suffix>
                                </name>
                                <xref ref-type="aff" rid="aff1">1</xref>
                                <role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>
                                <role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>
                                <role specific-use="reviewer">Reviewer</role>
                            </contrib>
                        </contrib-group>
                    </article-meta>
                </front>
            </article>
            """
        self.xmltree = etree.fromstring(xml)

    def test_data(self):
        self.maxDiff = None
        contrib = self.xmltree.xpath(".//contrib")[0]
        obtained = Contrib(contrib).data
        expected = {
            "contrib_type": "author",
            "collab": "The MARS Group",
            "contrib_full_name": "Prof Albert Einstein Nieto",
            "contrib_name": {
                "given-names": "Albert",
                "surname": "Einstein",
                "prefix": "Prof",
                "suffix": "Nieto",
            },
            "contrib_xref": [{"ref_type": "aff", "rid": "aff1", "text": "1"}],
            "contrib_role": [
                {
                    "content-type": "https://credit.niso.org/contributor-roles/data-curation/",
                    "specific-use": None,
                    "text": "Data curation",
                },
                {
                    "content-type": "https://credit.niso.org/contributor-roles/conceptualization/",
                    "specific-use": None,
                    "text": "Conceptualization",
                },
                {
                    "content-type": None,
                    "specific-use": "reviewer",
                    "text": "Reviewer",
                },
            ],
        }
        self.assertDictEqual(obtained, expected)


class ContribWithoutCollabTest(TestCase):
    def setUp(self):
        xml = """
            <article>
                <front>
                    <article-meta>
                        <contrib-group>
                            <contrib contrib-type="author">
                                <contrib-id contrib-id-type="orcid">0000-0001-8528-2091</contrib-id>
                                <contrib-id contrib-id-type="scopus">24771926600</contrib-id>
                                <name>
                                    <surname>Einstein</surname>
                                    <given-names>Albert</given-names>
                                    <prefix>Prof</prefix>
                                    <suffix>Nieto</suffix>
                                </name>
                                <xref ref-type="aff" rid="aff1">1</xref>
                                <role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>
                                <role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>
                                <role specific-use="reviewer">Reviewer</role>
                            </contrib>
                        </contrib-group>
                    </article-meta>
                </front>
            </article>
            """
        self.xmltree = etree.fromstring(xml)

    def test_data(self):
        self.maxDiff = None
        contrib = self.xmltree.xpath(".//contrib")[0]
        obtained = Contrib(contrib).data
        expected = {
            "contrib_type": "author",
            "contrib_ids": {"orcid": "0000-0001-8528-2091", "scopus": "24771926600"},
            "contrib_full_name": "Prof Albert Einstein Nieto",
            "contrib_name": {
                "given-names": "Albert",
                "surname": "Einstein",
                "prefix": "Prof",
                "suffix": "Nieto",
            },
            "contrib_xref": [{"ref_type": "aff", "rid": "aff1", "text": "1"}],
            "contrib_role": [
                {
                    "content-type": "https://credit.niso.org/contributor-roles/data-curation/",
                    "specific-use": None,
                    "text": "Data curation",
                },
                {
                    "content-type": "https://credit.niso.org/contributor-roles/conceptualization/",
                    "specific-use": None,
                    "text": "Conceptualization",
                },
                {
                    "content-type": None,
                    "specific-use": "reviewer",
                    "text": "Reviewer",
                },
            ],
        }
        self.assertDictEqual(obtained, expected)


class ContribWithoutNameTest(TestCase):
    def setUp(self):
        xml = """
            <article>
                <front>
                    <article-meta>
                        <contrib-group>
                            <contrib contrib-type="author">
                                <contrib-id contrib-id-type="orcid">0000-0001-8528-2091</contrib-id>
                                <contrib-id contrib-id-type="scopus">24771926600</contrib-id>
                                <collab>The MARS Group</collab>
                                <xref ref-type="aff" rid="aff1">1</xref>
                                <role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>
                                <role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>
                                <role specific-use="reviewer">Reviewer</role>
                            </contrib>
                        </contrib-group>
                    </article-meta>
                </front>
            </article>
            """
        self.xmltree = etree.fromstring(xml)

    def test_data(self):
        self.maxDiff = None
        contrib = self.xmltree.xpath(".//contrib")[0]
        obtained = Contrib(contrib).data
        expected = {
            "contrib_type": "author",
            "contrib_ids": {"orcid": "0000-0001-8528-2091", "scopus": "24771926600"},
            "collab": "The MARS Group",
            "contrib_xref": [{"ref_type": "aff", "rid": "aff1", "text": "1"}],
            "contrib_role": [
                {
                    "content-type": "https://credit.niso.org/contributor-roles/data-curation/",
                    "specific-use": None,
                    "text": "Data curation",
                },
                {
                    "content-type": "https://credit.niso.org/contributor-roles/conceptualization/",
                    "specific-use": None,
                    "text": "Conceptualization",
                },
                {
                    "content-type": None,
                    "specific-use": "reviewer",
                    "text": "Reviewer",
                },
            ],
        }
        self.assertDictEqual(obtained, expected)


class ContribWithoutXrefTest(TestCase):
    def setUp(self):
        xml = """
            <article>
                <front>
                    <article-meta>
                        <contrib-group>
                            <contrib contrib-type="author">
                                <contrib-id contrib-id-type="orcid">0000-0001-8528-2091</contrib-id>
                                <contrib-id contrib-id-type="scopus">24771926600</contrib-id>
                                <collab>The MARS Group</collab>
                                <name>
                                    <surname>Einstein</surname>
                                    <given-names>Albert</given-names>
                                    <prefix>Prof</prefix>
                                    <suffix>Nieto</suffix>
                                </name>
                                <role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>
                                <role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>
                                <role specific-use="reviewer">Reviewer</role>
                            </contrib>
                        </contrib-group>
                    </article-meta>
                </front>
            </article>
            """
        self.xmltree = etree.fromstring(xml)

    def test_data(self):
        self.maxDiff = None
        contrib = self.xmltree.xpath(".//contrib")[0]
        obtained = Contrib(contrib).data
        expected = {
            "contrib_type": "author",
            "contrib_ids": {"orcid": "0000-0001-8528-2091", "scopus": "24771926600"},
            "collab": "The MARS Group",
            "contrib_full_name": "Prof Albert Einstein Nieto",
            "contrib_name": {
                "given-names": "Albert",
                "surname": "Einstein",
                "prefix": "Prof",
                "suffix": "Nieto",
            },
            "contrib_role": [
                {
                    "content-type": "https://credit.niso.org/contributor-roles/data-curation/",
                    "specific-use": None,
                    "text": "Data curation",
                },
                {
                    "content-type": "https://credit.niso.org/contributor-roles/conceptualization/",
                    "specific-use": None,
                    "text": "Conceptualization",
                },
                {
                    "content-type": None,
                    "specific-use": "reviewer",
                    "text": "Reviewer",
                },
            ],
        }
        self.assertDictEqual(obtained, expected)


class ContribWithoutRoleTest(TestCase):
    def setUp(self):
        xml = """
            <article>
                <front>
                    <article-meta>
                        <contrib-group>
                            <contrib contrib-type="author">
                                <contrib-id contrib-id-type="orcid">0000-0001-8528-2091</contrib-id>
                                <contrib-id contrib-id-type="scopus">24771926600</contrib-id>
                                <collab>The MARS Group</collab>
                                <name>
                                    <surname>Einstein</surname>
                                    <given-names>Albert</given-names>
                                    <prefix>Prof</prefix>
                                    <suffix>Nieto</suffix>
                                </name>
                                <xref ref-type="aff" rid="aff1">1</xref>
                            </contrib>
                        </contrib-group>
                    </article-meta>
                </front>
            </article>
            """
        self.xmltree = etree.fromstring(xml)

    def test_data(self):
        self.maxDiff = None
        contrib = self.xmltree.xpath(".//contrib")[0]
        obtained = Contrib(contrib).data
        expected = {
            "contrib_type": "author",
            "contrib_ids": {"orcid": "0000-0001-8528-2091", "scopus": "24771926600"},
            "collab": "The MARS Group",
            "contrib_full_name": "Prof Albert Einstein Nieto",
            "contrib_name": {
                "given-names": "Albert",
                "surname": "Einstein",
                "prefix": "Prof",
                "suffix": "Nieto",
            },
            "contrib_xref": [{"ref_type": "aff", "rid": "aff1", "text": "1"}],
        }
        self.assertDictEqual(obtained, expected)


class ContribGroupTest(TestCase):
    def setUp(self):
        xml = """
            <article>
                <front>
                    <article-meta>
                        <contrib-group>
                            <contrib contrib-type="author">
                                <collab collab-type="committee">Technical Committee ISO/TC 108, Subcommittee SC 2</collab>
                                <xref ref-type="aff" rid="aff1"/>
                            </contrib>
                            <contrib contrib-type="author">
                                <collab>
                                    <named-content content-type="program">Joint United
                                    Nations Program on HIV/AIDS (UNAIDS)</named-content>,
                                    <institution>World Health Organization</institution>,
                                    Geneva, <country>Switzerland</country>
                                </collab>
                            </contrib>
                            <contrib contrib-type="author">
                                <collab>
                                    <named-content content-type="program">Nonoccupational HIV
                                    PEP Task Force, Brown University AIDS Program</named-content>
                                    and the <institution>Rhode Island Department of
                                    Health</institution>, Providence, Rhode Island
                                </collab>
                            </contrib>
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
                    </article-meta>
                </front>
            </article>
            """
        self.xmltree = etree.fromstring(xml)

    def test_data(self):
        self.maxDiff = None
        contrib_group = self.xmltree.xpath(".//contrib-group")[0]
        obtained = [item.data for item in ContribGroup(contrib_group).contribs]
        expected = [
            {
                "collab": "Technical Committee ISO/TC 108, Subcommittee SC 2",
                "contrib_type": "author",
                "contrib_xref": [{"ref_type": "aff", "rid": "aff1", "text": None}],
            },
            {
                "collab": "Joint United Nations Program on HIV/AIDS (UNAIDS), World Health Organization, Geneva, Switzerland",
                "contrib_type": "author",
            },
            {
                "collab": "Nonoccupational HIV PEP Task Force, Brown University AIDS Program and the Rhode Island Department of Health, Providence, Rhode Island",
                "contrib_type": "author",
            },
            {
                "contrib_full_name": "Prof FRANCISCO VENEGAS-MARTÍNEZ Nieto",
                "contrib_name": {
                    "given-names": "FRANCISCO",
                    "prefix": "Prof",
                    "suffix": "Nieto",
                    "surname": "VENEGAS-MARTÍNEZ",
                },
                "contrib_type": "author",
                "contrib_xref": [
                    {"ref_type": "aff", "rid": "aff1", "text": None},
                    {"ref_type": "aff", "rid": "aff2", "text": None},
                ],
            },
        ]
        for i, item in enumerate(expected):
            with self.subTest(i=i):
                self.assertDictEqual(item, obtained[i])


class ArticleContribTest(TestCase):
    def setUp(self):
        xml = """
            <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
               <front>
                  <article-meta>
                     <contrib-group>
                        <contrib contrib-type="author">
                           <contrib-id contrib-id-type="orcid">0000-0003-2243-0821</contrib-id>
                           <name>
                              <surname>Castro</surname>
                              <given-names>Silvana de</given-names>
                           </name>
                           <xref ref-type="aff" rid="aff1">a</xref>
                           <xref ref-type="corresp" rid="c1">*</xref>
                        </contrib>
                        <aff id="aff1">
                           <label>a</label>
                           <institution content-type="orgname">Universidade Federal do Rio de Janeiro (UFRJ)</institution>
                           <addr-line>
                              <named-content content-type="city">Rio de Janeiro</named-content>
                              <named-content content-type="state">RJ</named-content>
                           </addr-line>
                           <country country="BR">Brazil</country>
                           <institution content-type="original">Universidade Federal do Rio de Janeiro (UFRJ)</institution>
                        </aff>
                     </contrib-group>
                  </article-meta>
               </front>
               <sub-article article-type="translation" id="SA1" xml:lang="pt">
                  <front-stub>
                     <article-id pub-id-type="doi">10.1016/j.bjan.2019.01.002</article-id>
                     <contrib-group>
                        <contrib contrib-type="author">
                           <contrib-id contrib-id-type="orcid">0000-0003-2243-0821</contrib-id>
                           <name>
                              <surname>Castro</surname>
                              <given-names>Silvana de</given-names>
                           </name>
                           <xref ref-type="aff" rid="aff4">a</xref>
                           <xref ref-type="corresp" rid="c2">*</xref>
                        </contrib>
                     </contrib-group>
                     <aff id="aff4">
                        <label>a</label>
                        <institution content-type="original">Universidade Federal do Rio de Janeiro (UFRJ)</institution>
                     </aff>
                  </front-stub>
               </sub-article>
            </article>
            """
        self.xmltree = etree.fromstring(xml)

    def test_data(self):
        self.maxDiff = None
        obtained = list(XMLContribs(self.xmltree).all_contribs)
        expected = [
            {
                "original_article_type": "research-article",
                "parent": "article",
                "parent_article_type": "research-article",
                "parent_id": None,
                "parent_lang": "en",
                "contrib_ids": {"orcid": "0000-0003-2243-0821"},
                "contrib-group-type": None,
                "contrib_full_name": "Silvana de Castro",
                "contrib_name": {"given-names": "Silvana de", "surname": "Castro"},
                "contrib_type": "author",
                "contrib_xref": [
                    {"ref_type": "aff", "rid": "aff1", "text": "a"},
                    {"ref_type": "corresp", "rid": "c1", "text": "*"},
                ],
                "affs": [
                    {
                        "city": "Rio de Janeiro",
                        "country_code": "BR",
                        "country_name": "Brazil",
                        "email": None,
                        "id": "aff1",
                        "label": "a",
                        "orgdiv1": None,
                        "orgdiv2": None,
                        "orgname": "Universidade Federal do Rio de Janeiro (UFRJ)",
                        "original": "Universidade Federal do Rio de Janeiro (UFRJ)",
                        "state": "RJ",
                        "parent": "article",
                        "parent_article_type": "research-article",
                        "original_article_type": "research-article",
                        "parent_id": None,
                        "parent_lang": "en",
                    }
                ],
            },
            {
                "original_article_type": "research-article",
                "parent": "sub-article",
                "parent_article_type": "translation",
                "parent_id": "SA1",
                "parent_lang": "pt",
                "contrib_ids": {"orcid": "0000-0003-2243-0821"},
                "contrib-group-type": None,
                "contrib_full_name": "Silvana de Castro",
                "contrib_name": {"given-names": "Silvana de", "surname": "Castro"},
                "contrib_type": "author",
                "contrib_xref": [
                    {"ref_type": "aff", "rid": "aff4", "text": "a"},
                    {"ref_type": "corresp", "rid": "c2", "text": "*"},
                ],
                "affs": [
                    {
                        "city": None,
                        "country_name": None,
                        "country_code": None,
                        "email": None,
                        "id": "aff4",
                        "label": "a",
                        "orgdiv1": None,
                        "orgdiv2": None,
                        "orgname": None,
                        "original": "Universidade Federal do Rio de Janeiro (UFRJ)",
                        "state": None,
                        "parent": "sub-article",
                        "parent_article_type": "translation",
                        "original_article_type": "research-article",
                        "parent_id": "SA1",
                        "parent_lang": "pt",
                    }
                ],
            },
        ]
        for i, item in enumerate(expected):
            with self.subTest(i=i):
                self.assertDictEqual(item, obtained[i])

    def test_fix_bug_without_prefix(self):
        self.maxDiff = None
        xml_tree = etree.fromstring(
            """
        <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink" 
        article-type="editorial" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en"> 
            <front>
                <contrib-group> 
                    <contrib contrib-type="author"> 
                        <name> 
                            <surname>SIM&#213;ES</surname> 
                            <given-names>JEFFERSON C.</given-names>
                            <suffix>Nieto</suffix>
                        </name> 
                    </contrib>
                </contrib-group>
            </front>
        </article>
        """
        )
        obtained = list(XMLContribs(xml_tree).contribs)
        expected = ["JEFFERSON C. SIMÕES Nieto"]
        self.assertEqual(len(obtained), 1)
        for i, item in enumerate(expected):
            with self.subTest(i=i):
                self.assertEqual(item, obtained[i].get("contrib_full_name"))

    def test_fix_bug_without_suffix(self):
        self.maxDiff = None
        xml_tree = etree.fromstring(
            """
        <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink" 
        article-type="editorial" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en"> 
            <front>
                <contrib-group> 
                    <contrib contrib-type="author"> 
                        <name> 
                            <surname>SIM&#213;ES</surname> 
                            <given-names>JEFFERSON C.</given-names>
                            <prefix>Prof</prefix>
                        </name> 
                    </contrib>
                </contrib-group>
            </front>
        </article>
        """
        )
        obtained = list(XMLContribs(xml_tree).contribs)
        expected = ["Prof JEFFERSON C. SIMÕES"]
        self.assertEqual(len(obtained), 1)
        for i, item in enumerate(expected):
            with self.subTest(i=i):
                self.assertEqual(item, obtained[i].get("contrib_full_name"))

    def test_fix_bug_without_given_name(self):
        self.maxDiff = None
        xml_tree = etree.fromstring(
            """
        <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink" 
        article-type="editorial" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en"> 
            <front>
                <contrib-group> 
                    <contrib contrib-type="author"> 
                        <name> 
                            <surname>SIM&#213;ES</surname> 
                            <prefix>Prof</prefix>
                            <suffix>Nieto</suffix>
                        </name> 
                    </contrib>
                </contrib-group>
            </front>
        </article>
        """
        )
        obtained = list(XMLContribs(xml_tree).contribs)
        expected = ["Prof SIMÕES Nieto"]
        self.assertEqual(len(obtained), 1)
        for i, item in enumerate(expected):
            with self.subTest(i=i):
                self.assertEqual(item, obtained[i].get("contrib_full_name"))

    def test_fix_bug_without_surname(self):
        self.maxDiff = None
        xml_tree = etree.fromstring(
            """
        <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink" 
        article-type="editorial" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en"> 
            <front>
                <contrib-group> 
                    <contrib contrib-type="author"> 
                        <name> 
                            <given-names>JEFFERSON C.</given-names>
                            <prefix>Prof</prefix>
                            <suffix>Nieto</suffix> 
                        </name> 
                    </contrib>
                </contrib-group>
            </front>
        </article>
        """
        )
        obtained = list(XMLContribs(xml_tree).contribs)
        expected = ["Prof JEFFERSON C. Nieto"]
        self.assertEqual(len(obtained), 1)
        for i, item in enumerate(expected):
            with self.subTest(i=i):
                self.assertEqual(item, obtained[i].get("contrib_full_name"))


class TestContribAnonymous(TestCase):

    def test_anonymous_when_present(self):
        xml = """
        <contrib>
            <anonymous/>
        </contrib>
        """
        node = etree.fromstring(xml)
        contrib = Contrib(node)
        self.assertEqual(contrib.anonymous, "anonymous")

    def test_anonymous_when_absent(self):
        xml = """
        <contrib>
            <name>
                <surname>Smith</surname>
            </name>
        </contrib>
        """
        node = etree.fromstring(xml)
        contrib = Contrib(node)
        self.assertIsNone(contrib.anonymous)

    def test_anonymous_with_empty_node(self):
        xml = """
        <contrib>
        </contrib>
        """
        node = etree.fromstring(xml)
        contrib = Contrib(node)
        self.assertIsNone(contrib.anonymous)

    def test_anonymous_present_in_data(self):
        xml = """
        <contrib>
            <anonymous/>
        </contrib>
        """
        node = etree.fromstring(xml)
        contrib = Contrib(node)
        data = contrib.data
        self.assertIn("anonymous", data)
        self.assertEqual(data["anonymous"], "anonymous")

    def test_anonymous_absent_in_data(self):
        xml = """
        <contrib>
            <name>
                <surname>Smith</surname>
            </name>
        </contrib>
        """
        node = etree.fromstring(xml)
        contrib = Contrib(node)
        data = contrib.data
        self.assertNotIn("anonymous", data)


def create_test_xml(contrib_type=None):
    xml = """
    <article article-type="research-article" xml:lang="en" id="article1">
        <front>
            <contrib-group>
                <contrib contrib-type="author">
                    <name>
                        <surname>Smith</surname>
                        <given-names>John</given-names>
                    </name>
                    <xref ref-type="aff" rid="aff1"/>
                    <contrib-id contrib-id-type="orcid">0000-0001-2345-6789</contrib-id>
                </contrib>
            </contrib-group>
            <aff id="aff1">
                <institution content-type="orgname">Test University</institution>
                <addr-line>
                    <city>Test City</city>
                    <state>Test State</state>
                </addr-line>
                <country country="US">United States</country>
            </aff>
        </front>
        <sub-article article-type="translation" xml:lang="es" id="S1">
            <front-stub>
                <contrib-group>
                    <contrib contrib-type="translator">
                        <name>
                            <surname>García</surname>
                            <given-names>Ana</given-names>
                        </name>
                        <contrib-id contrib-id-type="orcid">9999-0001-2345-6789</contrib-id>
                    </contrib>
                </contrib-group>
            </front-stub>
        </sub-article>
    </article>
    """
    if contrib_type:
        xml = xml.replace("translator", contrib_type)
    return etree.fromstring(xml)


class TestTextContribs(TestCase):
    def setUp(self):
        self.xml = create_test_xml()
        self.text_contribs = TextContribs(self.xml.find("."))

    def test_contrib_groups(self):
        groups = list(self.text_contribs.contrib_groups)
        self.assertEqual(len(groups), 1)
        self.assertIsInstance(groups[0], ContribGroup)

    def test_data(self):
        data = self.text_contribs.data
        self.assertIn("parent", data)
        self.assertIn("contrib-groups", data)
        self.assertIsInstance(data["contrib-groups"], list)
        self.assertEqual(len(data["contrib-groups"]), 1)

    def test_items(self):
        items = list(self.text_contribs.items)
        self.assertEqual(len(items), 2)
        self.assertIn("contrib-group-type", items[0])
        self.assertEqual(items[0]["parent"], "article")
        self.assertEqual(items[0]["parent_lang"], "en")

    def test_translations(self):
        # Converte os nós retornados em instâncias de TextContribs
        translations_nodes = list(self.text_contribs.translations)
        translations = [TextContribs(node) for node in translations_nodes]
        self.assertEqual(len(translations), 1)
        self.assertIsInstance(translations[0], TextContribs)

    def test_not_translations(self):
        not_translations = list(self.text_contribs.not_translations)
        self.assertEqual(len(not_translations), 0)


class TestXMLContribs(TestCase):
    def setUp(self):
        self.xml = create_test_xml()
        self.xml_contribs = XMLContribs(self.xml)

    def test_contribs(self):
        contribs = list(self.xml_contribs.contribs)
        self.assertEqual(len(contribs), 1)
        self.assertIn("contrib_full_name", contribs[0])
        self.assertEqual(contribs[0]["contrib_full_name"], "John Smith")

    def test_translation_contribs(self):
        # Filtra contribuições oriundas de sub-artigos (traduções)
        translation_contribs = [
            c for c in self.xml_contribs.all_contribs if c.get("parent") == "sub-article"
        ]
        self.assertEqual(len(translation_contribs), 1)
        self.assertEqual(translation_contribs[0]["contrib_full_name"], "Ana García")
        self.assertEqual(translation_contribs[0]["contrib_type"], "translator")

    def test_not_translation_contribs(self):
        xml = create_test_xml("author")
        xml_contribs = XMLContribs(xml)
        # Contribuições de sub-artigos devem ser inexistentes quando não são traduções
        not_translation_contribs = [
            c for c in xml_contribs.all_contribs if c.get("parent") == "sub-article" and c.get("contrib_type") == "translator"
        ]
        self.assertEqual(len(not_translation_contribs), 0)

    def test_all_contribs(self):
        all_contribs = list(self.xml_contribs.all_contribs)
        self.assertEqual(len(all_contribs), 2)  # Uma contribuição principal + uma tradução

    def test_contrib_full_name_by_orcid(self):
        orcid_dict = self.xml_contribs.contrib_full_name_by_orcid
        self.assertIn("0000-0001-2345-6789", orcid_dict)
        self.assertIn("John Smith", orcid_dict["0000-0001-2345-6789"])
        self.assertEqual(2, len(orcid_dict))

    def test_add_affs(self):
        results = list(self.xml_contribs.contribs)
        result = results[0]
        self.assertIn("affs", result)
        self.assertEqual(len(result["affs"]), 1)
        self.assertEqual(result["affs"][0]["orgname"], "Test University")
        self.assertEqual(result["affs"][0]["country_code"], "US")
