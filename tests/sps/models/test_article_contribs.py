from unittest import TestCase
from unittest.mock import Mock

from lxml import etree

from packtools.sps.models.article_contribs import Contrib, ContribGroup, ArticleContribs
from packtools.sps.utils import xml_utils


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
            with self.subTest(i):
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
            with self.subTest(i):
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
                {"content-type": None, "specific-use": "reviewer", "text": "Reviewer"},
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
                {"content-type": None, "specific-use": "reviewer", "text": "Reviewer"},
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
                {"content-type": None, "specific-use": "reviewer", "text": "Reviewer"},
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
                {"content-type": None, "specific-use": "reviewer", "text": "Reviewer"},
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
                {"content-type": None, "specific-use": "reviewer", "text": "Reviewer"},
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
                {"content-type": None, "specific-use": "reviewer", "text": "Reviewer"},
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
        obtained = list(ContribGroup(contrib_group).contribs)
        expected = [
            {
                "collab": "Technical Committee ISO/TC 108, Subcommittee SC 2",
                "contrib_type": "author",
                "contrib_xref": [{"ref_type": "aff", "rid": "aff1", "text": None}],
            },
            {
                "collab": "Joint United Nations Program on HIV/AIDS (UNAIDS), World Health Organization, Geneva, "
                "Switzerland",
                "contrib_type": "author",
            },
            {
                "collab": "Nonoccupational HIV PEP Task Force, Brown University AIDS Program and the Rhode Island "
                "Department of Health, Providence, Rhode Island",
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
            with self.subTest(i):
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
        obtained = list(ArticleContribs(self.xmltree).contribs)
        expected = [
            {
                "parent": "article",
                "parent_article_type": "research-article",
                "parent_id": None,
                "parent_lang": "en",
                "contrib_ids": {"orcid": "0000-0003-2243-0821"},
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
                        "parent_id": None,
                        "parent_lang": "en",
                    }
                ],
            },
            {
                "parent": "sub-article",
                "parent_article_type": "translation",
                "parent_id": "SA1",
                "parent_lang": "pt",
                "contrib_ids": {"orcid": "0000-0003-2243-0821"},
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
                        "parent_id": "SA1",
                        "parent_lang": "pt",
                    }
                ],
            },
        ]

        for i, item in enumerate(expected):
            with self.subTest(i):
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
        obtained = list(ArticleContribs(xml_tree).contribs)
        expected = ["JEFFERSON C. SIMÕES Nieto"]
        self.assertEqual(len(obtained), 1)
        for i, item in enumerate(expected):
            with self.subTest(i):
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
        obtained = list(ArticleContribs(xml_tree).contribs)
        expected = ["Prof JEFFERSON C. SIMÕES"]
        self.assertEqual(len(obtained), 1)
        for i, item in enumerate(expected):
            with self.subTest(i):
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
        obtained = list(ArticleContribs(xml_tree).contribs)
        expected = ["Prof SIMÕES Nieto"]
        self.assertEqual(len(obtained), 1)
        for i, item in enumerate(expected):
            with self.subTest(i):
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
        obtained = list(ArticleContribs(xml_tree).contribs)
        expected = ["Prof JEFFERSON C. Nieto"]
        self.assertEqual(len(obtained), 1)
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertEqual(item, obtained[i].get("contrib_full_name"))


class TestContribAnonymous(TestCase):
    def setUp(self):
        self.contrib_class = Contrib

    def test_contrib_anonymous_when_present(self):
        # Create XML with anonymous node
        xml = """
        <contrib>
            <anonymous/>
        </contrib>
        """
        node = etree.fromstring(xml)
        contrib = self.contrib_class(node)

        # Test that contrib_anonymous returns "anonymous"
        self.assertEqual(contrib.contrib_anonymous, "anonymous")

    def test_contrib_anonymous_when_absent(self):
        # Create XML without anonymous node
        xml = """
        <contrib>
            <name>
                <surname>Smith</surname>
            </name>
        </contrib>
        """
        node = etree.fromstring(xml)
        contrib = self.contrib_class(node)

        # Test that contrib_anonymous returns None
        self.assertIsNone(contrib.contrib_anonymous)

    def test_contrib_anonymous_with_empty_node(self):
        # Create XML with empty contrib node
        xml = """
        <contrib>
        </contrib>
        """
        node = etree.fromstring(xml)
        contrib = self.contrib_class(node)

        # Test that contrib_anonymous returns None
        self.assertIsNone(contrib.contrib_anonymous)

    def test_contrib_anonymous_present_in_data(self):
        # Create XML with anonymous node
        xml = """
        <contrib>
            <anonymous/>
        </contrib>
        """
        node = etree.fromstring(xml)
        contrib = self.contrib_class(node)

        # Test that contrib_anonymous is present in data
        data = contrib.data
        self.assertIn("contrib_anonymous", data)
        self.assertEqual(data["contrib_anonymous"], "anonymous")

    def test_contrib_anonymous_absent_in_data(self):
        # Create XML without anonymous node
        xml = """
        <contrib>
            <name>
                <surname>Smith</surname>
            </name>
        </contrib>
        """
        node = etree.fromstring(xml)
        contrib = self.contrib_class(node)

        # Test that contrib_anonymous is not present in data
        data = contrib.data
        self.assertNotIn("contrib_anonymous", data)
