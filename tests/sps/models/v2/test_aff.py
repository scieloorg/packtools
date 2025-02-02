from unittest import TestCase, skip

from packtools.sps.models.v2.aff import Affiliation, Affiliations, ArticleAffiliations
from packtools.sps.utils import xml_utils

from lxml import etree


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
        self.aff = Affiliation(self.aff_node)

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


class AffiliationsTest(TestCase):
    @skip("Teste pendente de correção e/ou ajuste")
    def test_affiliations(self):

        self.xml_tree = xml_utils.get_xml_tree("tests/samples/1518-8787-rsp-56-79.xml")
        obtained = list(Affiliations(self.xml_tree).affiliations())
        expected = [
            {
                "city": "Pelotas",
                "country_code": "BR",
                "country_name": "Brasil",
                "email": None,
                "id": "aff1",
                "label": "I",
                "orgdiv1": "Faculdade de Medicina",
                "orgdiv2": "Programa de Pós-Graduação em\n\t\t\t\t\tEpidemiologia",
                "orgname": "Universidade Federal de Pelotas",
                "original": " Universidade Federal de Pelotas. Faculdade de\n\t\t\t\t\tMedicina. Programa de "
                "Pós-Graduação em Epidemiologia. Pelotas, RS,\n\t\t\t\t\tBrasil",
                "parent": "article",
                "parent_article_type": "research-article",
                "parent_id": None,
                "parent_lang": "en",
                "state": "RS",
            },
            {
                "city": "Pelotas",
                "country_code": "BR",
                "country_name": "Brasil",
                "email": None,
                "id": "aff2",
                "label": "II",
                "orgdiv1": "Escola Superior de Educação Física",
                "orgdiv2": "Programa de Pós-Graduação em Educação\n\t\t\t\t\tFísica",
                "orgname": "Universidade Federal de Pelotas",
                "original": " Universidade Federal de Pelotas. Escola\n"
                "\t\t\t\t\tSuperior de Educação Física. Programa de Pós-Graduação "
                "em Educação Física.\n"
                "\t\t\t\t\tPelotas, RS, Brasil",
                "parent": "article",
                "parent_article_type": "research-article",
                "parent_id": None,
                "parent_lang": "en",
                "state": "RS",
            },
        ]

        self.assertEqual(len(obtained), 2)
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(item, obtained[i])


class ArticleAffiliationsTest(TestCase):
    @skip("Teste pendente de correção e/ou ajuste")
    def test_article_affs(self):
        self.maxDiff = None
        self.xmltree = xml_utils.get_xml_tree("tests/samples/1518-8787-rsp-56-79.xml")
        obtained = list(ArticleAffiliations(self.xmltree).article_affs())
        expected = [
            {
                "city": "Pelotas",
                "country_code": "BR",
                "country_name": "Brasil",
                "email": None,
                "id": "aff1",
                "label": "I",
                "orgdiv1": "Faculdade de Medicina",
                "orgdiv2": "Programa de Pós-Graduação em\n\t\t\t\t\tEpidemiologia",
                "orgname": "Universidade Federal de Pelotas",
                "original": " Universidade Federal de Pelotas. Faculdade de\n\t\t\t\t\tMedicina. Programa de "
                "Pós-Graduação em Epidemiologia. Pelotas, RS,\n\t\t\t\t\tBrasil",
                "parent": "article",
                "parent_article_type": "research-article",
                "parent_id": None,
                "parent_lang": "en",
                "state": "RS",
            },
            {
                "city": "Pelotas",
                "country_code": "BR",
                "country_name": "Brasil",
                "email": None,
                "id": "aff2",
                "label": "II",
                "orgdiv1": "Escola Superior de Educação Física",
                "orgdiv2": "Programa de Pós-Graduação em Educação\n\t\t\t\t\tFísica",
                "orgname": "Universidade Federal de Pelotas",
                "original": " Universidade Federal de Pelotas. Escola\n"
                "\t\t\t\t\tSuperior de Educação Física. Programa de Pós-Graduação "
                "em Educação Física.\n"
                "\t\t\t\t\tPelotas, RS, Brasil",
                "parent": "article",
                "parent_article_type": "research-article",
                "parent_id": None,
                "parent_lang": "en",
                "state": "RS",
            },
        ]

        self.assertEqual(len(obtained), 2)
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(item, obtained[i])

    @skip("Teste pendente de correção e/ou ajuste")
    def test_sub_article_translation_affs(self):
        self.maxDiff = None
        self.xmltree = xml_utils.get_xml_tree("tests/samples/1518-8787-rsp-56-79.xml")
        obtained = list(
            ArticleAffiliations(self.xmltree).sub_article_translation_affs()
        )
        expected = [
            {
                "city": None,
                "country_code": "BR",
                "country_name": "Brasil",
                "email": None,
                "id": "aff1002",
                "label": "I",
                "orgdiv1": None,
                "orgdiv2": None,
                "orgname": None,
                "original": "Universidade Federal de Pelotas. Faculdade de\n"
                "\t\t\t\t\tMedicina. Programa de Pós-Graduação em Epidemiologia. "
                "Pelotas, RS,\n"
                "\t\t\t\t\tBrasil",
                "parent": "sub-article",
                "parent_article_type": "translation",
                "parent_id": "TRpt",
                "parent_lang": "pt",
                "state": None,
            },
            {
                "city": None,
                "country_code": "BR",
                "country_name": "Brasil",
                "email": None,
                "id": "aff2002",
                "label": "II",
                "orgdiv1": None,
                "orgdiv2": None,
                "orgname": None,
                "original": "Universidade Federal de Pelotas. Escola\n"
                "\t\t\t\t\tSuperior de Educação Física. Programa de Pós-Graduação "
                "em Educação Física.\n"
                "\t\t\t\t\tPelotas, RS, Brasil",
                "parent": "sub-article",
                "parent_article_type": "translation",
                "parent_id": "TRpt",
                "parent_lang": "pt",
                "state": None,
            },
        ]

        self.assertEqual(len(obtained), 2)
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(item, obtained[i])

    @skip("Teste pendente de correção e/ou ajuste")
    def test_sub_article_non_translation_affs(self):
        self.maxDiff = None
        self.xmltree = xml_utils.get_xml_tree("tests/samples/1518-8787-rsp-56-79.xml")
        obtained = list(
            ArticleAffiliations(self.xmltree).sub_article_non_translation_affs()
        )

        self.assertEqual(len(obtained), 0)

    @skip("Teste pendente de correção e/ou ajuste")
    def test_all_affs(self):
        self.maxDiff = None
        self.xmltree = xml_utils.get_xml_tree("tests/samples/1518-8787-rsp-56-79.xml")
        obtained = list(ArticleAffiliations(self.xmltree).all_affs())
        expected = [
            {
                "city": "Pelotas",
                "country_code": "BR",
                "country_name": "Brasil",
                "email": None,
                "id": "aff1",
                "label": "I",
                "orgdiv1": "Faculdade de Medicina",
                "orgdiv2": "Programa de Pós-Graduação em\n\t\t\t\t\tEpidemiologia",
                "orgname": "Universidade Federal de Pelotas",
                "original": " Universidade Federal de Pelotas. Faculdade de\n"
                "\t\t\t\t\tMedicina. Programa de Pós-Graduação em Epidemiologia. "
                "Pelotas, RS,\n"
                "\t\t\t\t\tBrasil",
                "parent": "article",
                "parent_article_type": "research-article",
                "parent_id": None,
                "parent_lang": "en",
                "state": "RS",
            },
            {
                "city": "Pelotas",
                "country_code": "BR",
                "country_name": "Brasil",
                "email": None,
                "id": "aff2",
                "label": "II",
                "orgdiv1": "Escola Superior de Educação Física",
                "orgdiv2": "Programa de Pós-Graduação em Educação\n\t\t\t\t\tFísica",
                "orgname": "Universidade Federal de Pelotas",
                "original": " Universidade Federal de Pelotas. Escola\n"
                "\t\t\t\t\tSuperior de Educação Física. Programa de Pós-Graduação "
                "em Educação Física.\n"
                "\t\t\t\t\tPelotas, RS, Brasil",
                "parent": "article",
                "parent_article_type": "research-article",
                "parent_id": None,
                "parent_lang": "en",
                "state": "RS",
            },
            {
                "city": None,
                "country_code": "BR",
                "country_name": "Brasil",
                "email": None,
                "id": "aff1002",
                "label": "I",
                "orgdiv1": None,
                "orgdiv2": None,
                "orgname": None,
                "original": "Universidade Federal de Pelotas. Faculdade de\n"
                "\t\t\t\t\tMedicina. Programa de Pós-Graduação em Epidemiologia. "
                "Pelotas, RS,\n"
                "\t\t\t\t\tBrasil",
                "parent": "sub-article",
                "parent_article_type": "translation",
                "parent_id": "TRpt",
                "parent_lang": "pt",
                "state": None,
            },
            {
                "city": None,
                "country_code": "BR",
                "country_name": "Brasil",
                "email": None,
                "id": "aff2002",
                "label": "II",
                "orgdiv1": None,
                "orgdiv2": None,
                "orgname": None,
                "original": "Universidade Federal de Pelotas. Escola\n"
                "\t\t\t\t\tSuperior de Educação Física. Programa de Pós-Graduação "
                "em Educação Física.\n"
                "\t\t\t\t\tPelotas, RS, Brasil",
                "parent": "sub-article",
                "parent_article_type": "translation",
                "parent_id": "TRpt",
                "parent_lang": "pt",
                "state": None,
            },
        ]

        self.assertEqual(len(obtained), 4)
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(item, obtained[i])
