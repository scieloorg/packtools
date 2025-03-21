from unittest import TestCase
from lxml import etree
from packtools.sps.models.article_contribs import (
    Contrib,
    ContribGroup,
    TextContribs,
    XMLContribs,
)

class ContribTest(TestCase):
    def setUp(self):
        self.contrib = Contrib(self._make_node())

    def _make_node(self):
        xml = """
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
        """
        return etree.fromstring(xml)

    def test_basic_fields(self):
        self.assertEqual(self.contrib.contrib_type, "author")
        self.assertEqual(self.contrib.collab, "The MARS Group")
        self.assertEqual(self.contrib.contrib_full_name, "Prof Albert Einstein Nieto")

    def test_contrib_ids(self):
        expected = {"orcid": "0000-0001-8528-2091", "scopus": "24771926600"}
        self.assertDictEqual(self.contrib.contrib_ids, expected)

    def test_contrib_name(self):
        expected = {
            "given-names": "Albert",
            "surname": "Einstein",
            "prefix": "Prof",
            "suffix": "Nieto",
        }
        self.assertDictEqual(self.contrib.contrib_name, expected)

    def test_contrib_xref(self):
        expected = [{"rid": "aff1", "ref_type": "aff", "text": "1"}]
        self.assertEqual(list(self.contrib.contrib_xref), expected)

    def test_contrib_role(self):
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
        self.assertEqual(list(self.contrib.contrib_role), expected)

    def test_data_output(self):
        data = self.contrib.data
        self.assertIn("contrib_type", data)
        self.assertIn("contrib_ids", data)
        self.assertIn("collab", data)
        self.assertIn("contrib_full_name", data)
        self.assertIn("contrib_xref", data)
        self.assertIn("contrib_role", data)
        self.assertEqual(data["contrib_full_name"], "Prof Albert Einstein Nieto")

class TextContribsTest(TestCase):
    def setUp(self):
        self.xml = etree.fromstring(self._xml_string())
        self.text_contribs = TextContribs(self.xml.find("."))

    def _xml_string(self):
        return """
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

    def test_contrib_groups(self):
        groups = list(self.text_contribs.contrib_groups)
        self.assertEqual(len(groups), 1)
        self.assertIsInstance(groups[0], ContribGroup)

    def test_main_contribs(self):
        contribs = list(self.text_contribs.main_contribs)
        self.assertEqual(len(contribs), 1)
        self.assertEqual(contribs[0]["contrib_full_name"], "John Smith")

    def test_items_include_sub_article(self):
        items = list(self.text_contribs.items)
        names = [item.get("contrib_full_name") for item in items]
        self.assertIn("John Smith", names)
        self.assertIn("Ana García", names)
        self.assertEqual(len(items), 2)

class XMLContribsTest(TestCase):
    def setUp(self):
        self.xml = etree.fromstring(self._xml_string())
        self.xml_contribs = XMLContribs(self.xml)

    def _xml_string(self):
        return """
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

    def test_contribs_with_affs(self):
        contribs = list(self.xml_contribs.contribs)
        self.assertEqual(len(contribs), 1)
        self.assertIn("affs", contribs[0])
        self.assertEqual(contribs[0]["contrib_full_name"], "John Smith")

    def test_all_contribs(self):
        all_contribs = list(self.xml_contribs.all_contribs)
        self.assertEqual(len(all_contribs), 2)
        names = [c.get("contrib_full_name") for c in all_contribs]
        self.assertIn("John Smith", names)
        self.assertIn("Ana García", names)

    def test_contrib_full_name_by_orcid(self):
        mapping = self.xml_contribs.contrib_full_name_by_orcid
        self.assertIn("0000-0001-2345-6789", mapping)
        self.assertIn("9999-0001-2345-6789", mapping)
        self.assertIn("John Smith", mapping["0000-0001-2345-6789"])
        self.assertIn("Ana García", mapping["9999-0001-2345-6789"])
