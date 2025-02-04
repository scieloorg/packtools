from unittest import TestCase

from lxml import etree

from packtools.sps.models.v2.aff import (
    Affiliation,
    FulltextAffiliations,
    XMLAffiliations,
)


class AffiliationTest(TestCase):
    def setUp(self):
        xml = """
        <aff id="aff1">
            <label>I</label>
            <institution content-type="orgname">Universidade Federal de Pelotas</institution>
            <institution content-type="orgdiv1">Faculdade de Medicina</institution>
            <institution content-type="orgdiv2">Programa de Pós-Graduação em Epidemiologia</institution>
            <addr-line>
                <named-content content-type="city">Pelotas</named-content>
                <named-content content-type="state">RS</named-content>
            </addr-line>
            <country country="BR">Brasil</country>
            <institution content-type="original">Universidade Federal de Pelotas. Faculdade de Medicina. Programa de Pós-Graduação em Epidemiologia. Pelotas, RS, Brasil</institution>
            <email>exemplo@ufpel.edu.br</email>
        </aff>
        """
        self.aff_node = etree.fromstring(xml)
        self.aff = Affiliation(self.aff_node, {})

    def test_aff_id(self):
        obtained = self.aff.aff_id
        self.assertEqual(obtained, "aff1")

    def test_label(self):
        obtained = self.aff.label
        self.assertEqual(obtained, "I")

    def test_orgdiv1(self):
        obtained = self.aff.orgdiv1
        self.assertEqual(obtained, "Faculdade de Medicina")

    def test_orgdiv2(self):
        obtained = self.aff.orgdiv2
        self.assertEqual(obtained, "Programa de Pós-Graduação em Epidemiologia")

    def test_original(self):
        obtained = self.aff.original
        self.assertEqual(
            obtained,
            "Universidade Federal de Pelotas. Faculdade de Medicina. Programa de Pós-Graduação em Epidemiologia. Pelotas, RS, Brasil",
        )

    def test_orgname(self):
        obtained = self.aff.orgname
        self.assertEqual(obtained, "Universidade Federal de Pelotas")

    def test_country(self):
        obtained = self.aff.country
        self.assertEqual(obtained, "Brasil")

    def test_country_code(self):
        obtained = self.aff.country_code
        self.assertEqual(obtained, "BR")

    def test_state(self):
        obtained = self.aff.state
        self.assertEqual(obtained, "RS")

    def test_city(self):
        obtained = self.aff.city
        self.assertEqual(obtained, "Pelotas")

    def test_email(self):
        obtained = self.aff.email
        self.assertEqual(obtained, "exemplo@ufpel.edu.br")

    def test_data(self):
        obtained = self.aff.data
        expected = {
            "city": "Pelotas",
            "country_code": "BR",
            "country_name": "Brasil",
            "email": "exemplo@ufpel.edu.br",
            "id": "aff1",
            "label": "I",
            "orgdiv1": "Faculdade de Medicina",
            "orgdiv2": "Programa de Pós-Graduação em Epidemiologia",
            "orgname": "Universidade Federal de Pelotas",
            "original": "Universidade Federal de Pelotas. Faculdade de Medicina. Programa de Pós-Graduação em "
            "Epidemiologia. Pelotas, RS, Brasil",
            "state": "RS",
        }

        self.assertDictEqual(obtained, expected)

    def test_str_main_tag(self):
        self.assertEqual(self.aff.str_main_tag, '<aff id="aff1">')

    def test_str(self):
        self.maxDiff = None
        self.assertEqual(
            str(self.aff),
            """<aff id="aff1">
            <label>I</label>
            <institution content-type="orgname">Universidade Federal de Pelotas</institution>
            <institution content-type="orgdiv1">Faculdade de Medicina</institution>
            <institution content-type="orgdiv2">Programa de Pós-Graduação em Epidemiologia</institution>
            <addr-line>
                <named-content content-type="city">Pelotas</named-content>
                <named-content content-type="state">RS</named-content>
            </addr-line>
            <country country="BR">Brasil</country>
            <institution content-type="original">Universidade Federal de Pelotas. Faculdade de Medicina. Programa de Pós-Graduação em Epidemiologia. Pelotas, RS, Brasil</institution>
            <email>exemplo@ufpel.edu.br</email>
        </aff>""",
        )

    def test_xml(self):
        self.maxDiff = None
        self.assertEqual(
            self.aff.xml(),
            """<aff id="aff1">
            <label>I</label>
            <institution content-type="orgname">Universidade Federal de Pelotas</institution>
            <institution content-type="orgdiv1">Faculdade de Medicina</institution>
            <institution content-type="orgdiv2">Programa de Pós-Graduação em Epidemiologia</institution>
            <addr-line>
                <named-content content-type="city">Pelotas</named-content>
                <named-content content-type="state">RS</named-content>
            </addr-line>
            <country country="BR">Brasil</country>
            <institution content-type="original">Universidade Federal de Pelotas. Faculdade de Medicina. Programa de Pós-Graduação em Epidemiologia. Pelotas, RS, Brasil</institution>
            <email>exemplo@ufpel.edu.br</email>
        </aff>
""",
        )


class TestXMLAffiliations(TestCase):
    def setUp(self):
        self.xml_sample = """
        <article xml:lang="pt" article-type="research-article">
            <front>
                <aff id="aff1">
                    <label>I</label>
                    <institution content-type="orgname">Universidade Federal de Pelotas</institution>
                    <institution content-type="orgdiv1">Faculdade de Medicina</institution>
                    <institution content-type="orgdiv2">Programa de Pós-Graduação em Epidemiologia</institution>
                    <addr-line>
                        <named-content content-type="city">Pelotas</named-content>
                        <named-content content-type="state">RS</named-content>
                    </addr-line>
                    <country country="BR">Brasil</country>
                    <institution content-type="original">Universidade Federal de Pelotas. Faculdade de Medicina. Programa de Pós-Graduação em Epidemiologia. Pelotas, RS, Brasil</institution>
                    <email>exemplo@ufpel.edu.br</email>
                </aff>
            </front>
            <sub-article article-type="translation" xml:lang="en" id="s1">
                <front-stub>
                    <aff id="aff2">
                        <institution content-type="orgname">Institution 2</institution>
                        <country country="BR">Brazil</country>
                    </aff>
                </front-stub>
            </sub-article>
            <sub-article article-type="reviewer-report" xml:lang="pt" id="s2">
                <front-stub>
                    <aff id="aff3">
                        <institution content-type="orgname">Institution 3</institution>
                        <country country="BR">Brasil</country>
                    </aff>
                </front-stub>
                <sub-article article-type="translation" xml:lang="en" id="s3">
                    <front-stub>
                        <aff id="aff4">
                            <institution content-type="orgname">Institution 3</institution>
                            <country country="BR">Brazil</country>
                        </aff>
                    </front-stub>
                </sub-article>
            </sub-article>
        </article>
        """
        self.xml_tree = etree.fromstring(self.xml_sample)
        self.xml_affs = XMLAffiliations(self.xml_tree)
        self.fulltext_affs = FulltextAffiliations(self.xml_tree.find("."))

    def test_article_affs(self):
        """Test main article affiliations"""
        affs = self.xml_affs.article_affs
        self.assertEqual(len(affs), 1)
        self.assertEqual(affs[0]["id"], "aff1")

    def test_items_property(self):
        """Test retrieval of all affiliations through items property"""
        all_affs = list(self.xml_affs.items)
        self.assertEqual(len(all_affs), 4)  # Should get all 4 affiliations

    def test_by_ids_property(self):
        """Test the by_ids property returns all affiliation IDs correctly"""
        by_ids = self.xml_affs.by_ids
        expected_ids = ["aff1", "aff2", "aff3", "aff4"]
        self.assertSetEqual(set(by_ids.keys()), set(expected_ids))

    def test_data_structure(self):
        """Test the structure of the data property"""
        data = self.xml_affs.data
        self.assertEqual(
            ["main", "translations", "not_translations"], list(data.keys())
        )

        # Check main affiliations
        self.assertEqual(len(data["main"]), 1)

        # Check translations
        self.assertEqual(len(data["translations"]), 1)
        self.assertIn("en", data["translations"])
        self.assertEqual(len(data["translations"]["en"]), 1)

        # Check non-translations
        self.assertEqual(len(data["not_translations"]), 1)
        self.assertIn("s2", data["not_translations"])
        self.assertIn("main", data["not_translations"]["s2"])
        self.assertIn("translations", data["not_translations"]["s2"])
        self.assertNotIn("not_translations", data["not_translations"]["s2"])

    def test_by_ids_property_empty_xml(self):
        """Test by_ids property with XML containing no affiliations"""
        xml_tree = etree.fromstring("<article/>")
        xml_affs = XMLAffiliations(xml_tree)
        self.assertEqual(list(xml_affs.by_ids.keys()), [])

    def test_by_ids_property_single_aff(self):
        """Test by_ids property with XML containing single affiliation"""
        single_aff_xml = """
        <article xml:lang="pt">
            <front>
                <aff id="aff1">
                    <institution content-type="orgname">Institution 1</institution>
                </aff>
            </front>
        </article>
        """
        xml_tree = xml_tree = etree.fromstring(single_aff_xml)
        xml_affs = XMLAffiliations(xml_tree)
        self.assertEqual(list(xml_affs.by_ids.keys()), ["aff1"])
