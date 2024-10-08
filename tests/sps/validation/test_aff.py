import logging
from unittest import TestCase

from lxml import etree

from packtools.sps.models.aff import Affiliation
from packtools.sps.validation.aff import (
    AffiliationValidation,
    AffiliationsListValidation,
)
from packtools.sps.utils import xml_utils


class AffiliationValidationTest(TestCase):
    def test_validate_affiliations_list(self):
        self.maxDiff = None
        xml = """
        <article article-type="research-article" xml:lang="pt">
            <front>
                <article-meta>
                    <aff id="aff1">
                        <label>I</label>
                        <institution content-type="orgname">Secretaria Municipal de Saúde de Belo Horizonte</institution>
                        <addr-line>
                            <named-content content-type="city">Belo Horizonte</named-content>
                            <named-content content-type="state">MG</named-content>
                        </addr-line>
                        <country country="BR">Brasil</country>
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
                        <country country="BR">Brasil</country>
                        <institution content-type="original">Grupo de Pesquisas em Epidemiologia e Avaliação em Saúde. Faculdade de Medicina. Universidade Federal de Minas Gerais. Belo Horizonte, MG, Brasil</institution>
                    </aff>
                </article-meta>
            </front>
        </article>
        """

        xml_tree = etree.fromstring(xml)
        obtained = list(
            AffiliationsListValidation(xml_tree, ["BR"]).validate_affiliations_list()
        )
        expected = [
            "id", "original", "orgname", "country name", "country code", "state", "city",
            "id", "original", "orgname", "country name", "country code", "state", "city",
        ]
        self.assertEqual(14, len(obtained))
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertEqual(expected[i], item["title"])


    def test_affiliation_without_original(self):
        self.maxDiff = None
        xml = """
        <article article-type="research-article" xml:lang="pt">
            <front>
                <article-meta>
                    <aff id="aff1">
                        <label>I</label>
                        <institution content-type="orgname">Secretaria Municipal de Saúde de Belo Horizonte</institution>
                        <addr-line>
                            <named-content content-type="city">Belo Horizonte</named-content>
                            <named-content content-type="state">MG</named-content>
                        </addr-line>
                        <country country="BR">Brasil</country>
                    </aff>
                </article-meta>
            </front>
        </article>
        """

        xml_tree = etree.fromstring(xml)
        affiliations_list = list(Affiliation(xml_tree).affiliation_list)
        obtained = AffiliationValidation(affiliations_list[0]).validate_original()

        expected = {
                "title": "original",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "research-article",
                "parent_lang": "pt",
                "item": "institution",
                "sub_item": '@content-type="original"',
                "validation_type": "exist",
                "response": "ERROR",
                "expected_value": "original affiliation",
                "got_value": None,
                "message": "Got None, expected original affiliation",
                "advice": "provide the original affiliation",
                "data": {
                    "city": "Belo Horizonte",
                    "country_code": "BR",
                    "country_name": "Brasil",
                    "email": None,
                    "id": "aff1",
                    "label": "I",
                    "orgdiv1": None,
                    "orgdiv2": None,
                    "orgname": "Secretaria Municipal de Saúde de Belo Horizonte",
                    "original": None,
                    "parent": "article",
                    "parent_article_type": "research-article",
                    "parent_lang": "pt",
                    "parent_id": None,
                    "state": "MG",
                },
            }
        self.assertDictEqual(expected, obtained)

    def test_affiliations_without_orgname(self):
        self.maxDiff = None
        xml = """
        <article article-type="research-article" xml:lang="pt">
            <front>
                <article-meta>
                    <aff id="aff1">
                        <label>I</label>
                        <addr-line>
                            <named-content content-type="city">Belo Horizonte</named-content>
                            <named-content content-type="state">MG</named-content>
                        </addr-line>
                        <country country="BR">Brasil</country><institution content-type="original">Secretaria Municipal de Saúde de Belo Horizonte. Belo Horizonte, MG, Brasil</institution>
                    </aff>
                </article-meta>
            </front>
        </article>
        """

        xml_tree = etree.fromstring(xml)
        affiliations_list = list(Affiliation(xml_tree).affiliation_list)
        obtained = AffiliationValidation(affiliations_list[0]).validate_orgname()

        expected = {
                "title": "orgname",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "research-article",
                "parent_lang": "pt",
                "item": "institution",
                "sub_item": '@content-type="orgname"',
                "validation_type": "exist",
                "response": "CRITICAL",
                "expected_value": "orgname",
                "got_value": None,
                "message": "Got None, expected orgname",
                "advice": "provide the orgname",
                "data": {
                    "city": "Belo Horizonte",
                    "country_code": "BR",
                    "country_name": "Brasil",
                    "email": None,
                    "id": "aff1",
                    "label": "I",
                    "orgdiv1": None,
                    "orgdiv2": None,
                    "orgname": None,
                    "original": "Secretaria Municipal de Saúde de Belo Horizonte. Belo "
                    "Horizonte, MG, Brasil",
                    "parent": "article",
                    "parent_article_type": "research-article",
                    "parent_lang": "pt",
                    "parent_id": None,
                    "state": "MG",
                },
            }
        self.assertDictEqual(expected, obtained)


    def test_affiliations_without_country(self):
        self.maxDiff = None
        xml = """
        <article article-type="research-article" xml:lang="pt">
            <front>
                <article-meta>
                    <aff id="aff1">
                        <label>I</label>
                        <institution content-type="orgname">Secretaria Municipal de Saúde de Belo Horizonte</institution>
                        <addr-line>
                            <named-content content-type="city">Belo Horizonte</named-content>
                            <named-content content-type="state">MG</named-content>
                        </addr-line>
                        <institution content-type="original">Secretaria Municipal de Saúde de Belo Horizonte. Belo Horizonte, MG, Brasil</institution>
                    </aff>
                </article-meta>
            </front>
        </article>
        """

        xml_tree = etree.fromstring(xml)
        affiliations_list = list(Affiliation(xml_tree).affiliation_list)
        obtained = AffiliationValidation(affiliations_list[0]).validate_country()

        expected = {
                "title": "country name",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "research-article",
                "parent_lang": "pt",
                "item": "aff",
                "sub_item": "country",
                "validation_type": "exist",
                "response": "CRITICAL",
                "expected_value": "country name",
                "got_value": None,
                "message": "Got None, expected country name",
                "advice": "provide the country name",
                "data": {
                    "city": "Belo Horizonte",
                    "country_code": None,
                    "country_name": None,
                    "email": None,
                    "id": "aff1",
                    "label": "I",
                    "orgdiv1": None,
                    "orgdiv2": None,
                    "orgname": "Secretaria Municipal de Saúde de Belo Horizonte",
                    "original": "Secretaria Municipal de Saúde de Belo Horizonte. Belo "
                    "Horizonte, MG, Brasil",
                    "parent": "article",
                    "parent_id": None,
                    "parent_article_type": "research-article",
                    "parent_lang": "pt",
                    "state": "MG",
                },
            }
        self.assertDictEqual(expected, obtained)


    def test_affiliations_without_country_code(self):
        self.maxDiff = None
        xml = """
        <article article-type="research-article" xml:lang="pt">
            <front>
                <article-meta>
                    <aff id="aff1">
                        <label>I</label>
                        <institution content-type="orgname">Secretaria Municipal de Saúde de Belo Horizonte</institution>
                        <country>Brasil</country>
                        <addr-line>
                            <named-content content-type="city">Belo Horizonte</named-content>
                            <named-content content-type="state">MG</named-content>
                        </addr-line>
                        <institution content-type="original">Secretaria Municipal de Saúde de Belo Horizonte. Belo Horizonte, MG, Brasil</institution>
                    </aff>
                </article-meta>
            </front>
        </article>
        """

        xml_tree = etree.fromstring(xml)
        affiliations_list = list(Affiliation(xml_tree).affiliation_list)
        obtained = AffiliationValidation(affiliations_list[0], ["BR"]).validate_country_code()

        expected = {
                "title": "country code",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "research-article",
                "parent_lang": "pt",
                "item": "country",
                "sub_item": "@country",
                "validation_type": "value in list",
                "response": "CRITICAL",
                "expected_value": ["BR"],
                "got_value": None,
                "message": "Got None, expected ['BR']",
                "advice": "provide a valid @country",
                "data": {
                    "city": "Belo Horizonte",
                    "country_code": None,
                    "country_name": "Brasil",
                    "email": None,
                    "id": "aff1",
                    "label": "I",
                    "orgdiv1": None,
                    "orgdiv2": None,
                    "orgname": "Secretaria Municipal de Saúde de Belo Horizonte",
                    "original": "Secretaria Municipal de Saúde de Belo Horizonte. Belo "
                    "Horizonte, MG, Brasil",
                    "parent": "article",
                    "parent_id": None,
                    "parent_article_type": "research-article",
                    "parent_lang": "pt",
                    "state": "MG",
                },
            }
        self.assertDictEqual(expected, obtained)


    def test_affiliations_without_state(self):
        self.maxDiff = None
        xml = """
        <article article-type="research-article" xml:lang="pt">
            <front>
                <article-meta>
                    <aff id="aff1">
                        <label>I</label>
                        <institution content-type="orgname">Secretaria Municipal de Saúde de Belo Horizonte</institution>
                        <country country="BR">Brasil</country>
                        <addr-line>
                            <named-content content-type="city">Belo Horizonte</named-content>
                        </addr-line>
                        <institution content-type="original">Secretaria Municipal de Saúde de Belo Horizonte. Belo Horizonte, MG, Brasil</institution>
                    </aff>
                </article-meta>
            </front>
        </article>
        """

        xml_tree = etree.fromstring(xml)
        affiliations_list = list(Affiliation(xml_tree).affiliation_list)
        obtained = AffiliationValidation(affiliations_list[0]).validate_state()

        expected = {
                "title": "state",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "research-article",
                "parent_lang": "pt",
                "item": "addr-line",
                "sub_item": "state",
                "validation_type": "exist",
                "response": "ERROR",
                "expected_value": "state",
                "got_value": None,
                "message": "Got None, expected state",
                "advice": "provide the state",
                "data": {
                    "city": "Belo Horizonte",
                    "country_code": "BR",
                    "country_name": "Brasil",
                    "email": None,
                    "id": "aff1",
                    "label": "I",
                    "orgdiv1": None,
                    "orgdiv2": None,
                    "orgname": "Secretaria Municipal de Saúde de Belo Horizonte",
                    "original": "Secretaria Municipal de Saúde de Belo Horizonte. Belo "
                    "Horizonte, MG, Brasil",
                    "parent": "article",
                    "parent_id": None,
                    "parent_article_type": "research-article",
                    "parent_lang": "pt",
                    "state": None,
                },
            }
        self.assertDictEqual(expected, obtained)

    def test_affiliations_without_city(self):
        self.maxDiff = None
        xml = """
        <article article-type="research-article" xml:lang="pt">
            <front>
                <article-meta>
                    <aff id="aff1">
                        <label>I</label>
                        <institution content-type="orgname">Secretaria Municipal de Saúde de Belo Horizonte</institution>
                        <country country="BR">Brasil</country>
                        <addr-line>
                            <named-content content-type="state">MG</named-content>
                        </addr-line>
                        <institution content-type="original">Secretaria Municipal de Saúde de Belo Horizonte. Belo Horizonte, MG, Brasil</institution>
                    </aff>
                </article-meta>
            </front>
        </article>
        """

        xml_tree = etree.fromstring(xml)
        affiliations_list = list(Affiliation(xml_tree).affiliation_list)
        obtained = AffiliationValidation(affiliations_list[0]).validate_city()

        expected = {
                "title": "city",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "research-article",
                "parent_lang": "pt",
                "item": "addr-line",
                "sub_item": "city",
                "validation_type": "exist",
                "response": "ERROR",
                "expected_value": "city",
                "got_value": None,
                "message": "Got None, expected city",
                "advice": "provide the city",
                "data": {
                    "city": None,
                    "country_name": "Brasil",
                    "country_code": "BR",
                    "email": None,
                    "id": "aff1",
                    "label": "I",
                    "orgdiv1": None,
                    "orgdiv2": None,
                    "orgname": "Secretaria Municipal de Saúde de Belo Horizonte",
                    "original": "Secretaria Municipal de Saúde de Belo Horizonte. Belo "
                    "Horizonte, MG, Brasil",
                    "parent": "article",
                    "parent_id": None,
                    "parent_article_type": "research-article",
                    "parent_lang": "pt",
                    "state": "MG",
                },
            }
        self.assertDictEqual(expected, obtained)

    def test_affiliations_without_id(self):
        self.maxDiff = None
        xml = """
        <article article-type="research-article" xml:lang="pt">
            <front>
                <article-meta>
                    <aff>
                        <label>I</label>
                        <institution content-type="orgname">Secretaria Municipal de Saúde de Belo Horizonte</institution>
                        <country country="BR">Brasil</country>
                        <addr-line>
                            <named-content content-type="state">MG</named-content>
                        </addr-line>
                        <institution content-type="original">Secretaria Municipal de Saúde de Belo Horizonte. Belo Horizonte, MG, Brasil</institution>
                    </aff>
                </article-meta>
            </front>
        </article>
        """

        xml_tree = etree.fromstring(xml)
        affiliations_list = list(Affiliation(xml_tree).affiliation_list)
        obtained = AffiliationValidation(affiliations_list[0]).validate_id()

        expected = {
                "title": "id",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "research-article",
                "parent_lang": "pt",
                "item": "aff",
                "sub_item": "@id",
                "validation_type": "exist",
                "response": "CRITICAL",
                "expected_value": "affiliation ID",
                "got_value": None,
                "message": "Got None, expected affiliation ID",
                "advice": "provide the affiliation ID",
                "data": {
                    "city": None,
                    "country_name": "Brasil",
                    "country_code": "BR",
                    "email": None,
                    "id": None,
                    "label": "I",
                    "orgdiv1": None,
                    "orgdiv2": None,
                    "orgname": "Secretaria Municipal de Saúde de Belo Horizonte",
                    "original": "Secretaria Municipal de Saúde de Belo Horizonte. Belo "
                    "Horizonte, MG, Brasil",
                    "parent": "article",
                    "parent_id": None,
                    "parent_article_type": "research-article",
                    "parent_lang": "pt",
                    "state": "MG",
                },
            }
        self.assertDictEqual(expected, obtained)

    def test_validate(self):
        self.maxDiff = None
        xml = """
        <article article-type="research-article" xml:lang="pt">
            <front>
                <article-meta>
                    <aff id="aff1">
                        <label>I</label>
                        <institution content-type="orgname">Secretaria Municipal de Saúde de Belo Horizonte</institution>
                        <addr-line>
                            <named-content content-type="city">Belo Horizonte</named-content>
                            <named-content content-type="state">MG</named-content>
                        </addr-line>
                        <country country="BR">Brasil</country>
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
                        <country country="BR">Brasil</country>
                        <institution content-type="original">Grupo de Pesquisas em Epidemiologia e Avaliação em Saúde. Faculdade de Medicina. Universidade Federal de Minas Gerais. Belo Horizonte, MG, Brasil</institution>
                    </aff>
                </article-meta>
            </front>
        </article>
        """

        xml_tree = etree.fromstring(xml)
        data = {"country_codes_list": ["BR"]}
        obtained = list(AffiliationsListValidation(xml_tree).validate(data))

        expected = [
            "id", "original", "orgname", "country name", "country code", "state", "city",
            "id", "original", "orgname", "country name", "country code", "state", "city",
        ]
        self.assertEqual(14, len(obtained))
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertEqual(expected[i], item["title"])

    def test_validate_affiliation_sub_article_original_only(self):
        self.maxDiff = None
        xml = """
                <article article-type="research-article" xml:lang="pt">
                    <front>
                        <article-meta>

                        </article-meta>
                    </front>
                    <sub-article article-type="translation" id="TRpt" xml:lang="pt">
                        <front-stub>
                            <aff id="aff1002">
                                <label>I</label>
                                <country country="BR">Brasil</country>
                                <institution content-type="original">Universidade Federal de Pelotas. Faculdade de Medicina. Programa de Pós-Graduação em Epidemiologia. Pelotas, RS, Brasil</institution>
                            </aff>
                        </front-stub>
                    </sub-article>
                    <sub-article article-type="translation" id="TRes" xml:lang="es">
                        <front-stub>
                            <aff id="aff1002">
                                <label>I</label>
                                <country country="BR">Brasil</country>
                                <institution content-type="original">Universidade Federal de Pelotas. Faculdade de Medicina. Programa de Pós-Graduação em Epidemiologia. Pelotas, RS, Brasil</institution>
                            </aff>
                        </front-stub>
                    </sub-article>
                </article>
                """

        xml_tree = etree.fromstring(xml)
        data = {"country_codes_list": ["BR"]}
        obtained = list(AffiliationsListValidation(xml_tree).validate(data))

        expected = [
            "id", "original",
            "id", "original",
        ]
        self.assertEqual(4, len(obtained))
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertEqual(expected[i], item["title"])

    def test_validate_affiliation_count_article_vs_sub_article(self):
        self.maxDiff = None
        xml_tree = xml_utils.get_xml_tree("tests/samples/1518-8787-rsp-56-79.xml")
        obtained = list(
            AffiliationsListValidation(
                xml_tree
            ).validate_affiliation_count_article_vs_sub_article()
        )
        expected = [
            {
                "title": "Affiliation count validation",
                "parent": None,
                "parent_id": None,
                "parent_article_type": None,
                "parent_lang": None,
                "item": "aff",
                "sub_item": None,
                "validation_type": "match",
                "response": "OK",
                "expected_value": "equal counts in articles and sub-articles",
                "got_value": "articles: 2, sub-articles: 2",
                "message": "Got articles: 2, sub-articles: 2, expected equal counts in articles and sub-articles",
                "advice": None,
                "data": [
                    {
                        'article': '<aff id="aff1">',
                        'sub_article': '<aff id="aff1002">'
                    },
                    {
                        'article': '<aff id="aff2">',
                        'sub_article': '<aff id="aff2002">'
                    }
                ],
            }
        ]
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(item, obtained[i])

    def test_validate_affiliation_2176_4573_bak_p58270(self):
        self.maxDiff = None
        xml_tree = xml_utils.get_xml_tree("tests/fixtures/htmlgenerator/bak/2176-4573-bak-p58270.xml")
        data = {"country_codes_list": ["BR"]}
        validation = AffiliationsListValidation(xml_tree)
        obtained = list(validation.validate(data))
        expected = [
            "id", "original", "orgname", "country name", "country code", "state", "city",
            "id", "original",
        ]
        self.assertEqual(9, len(obtained))
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertEqual(expected[i], item["title"])


    def test_validate_affiliation_count_2176_4573_bak_p58270(self):
        self.maxDiff = None
        xml_tree = xml_utils.get_xml_tree("tests/fixtures/htmlgenerator/bak/2176-4573-bak-p58270.xml")
        obtained = list(
            AffiliationsListValidation(
                xml_tree
            ).validate_affiliation_count_article_vs_sub_article()
        )
        expected = [
            {
                "advice": None,
                "data": [
                    {
                        "article": '<aff id="aff1">',
                        "sub_article": '<aff id="aff2">'
                    }
                ],
                "expected_value": "equal counts in articles and sub-articles",
                "got_value": "articles: 1, sub-articles: 1",
                "item": "aff",
                "message": "Got articles: 1, sub-articles: 1, expected equal counts in "
                           "articles and sub-articles",
                "parent": None,
                "parent_article_type": None,
                "parent_id": None,
                "parent_lang": None,
                "response": "OK",
                "sub_item": None,
                "title": "Affiliation count validation",
                "validation_type": "match",
            }
        ]
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(item, obtained[i])

    def test_validate_affiliation_MNHpJQpnjvSX6pkKCg37yTJ(self):
        self.maxDiff = None
        xml_tree = xml_utils.get_xml_tree("tests/fixtures/htmlgenerator/sub-article_translation_with_sub-article_reply/MNHpJQpnjvSX6pkKCg37yTJ.xml")
        data = {"country_codes_list": ["BR"]}
        obtained = list(AffiliationsListValidation(xml_tree).validate(data))
        expected = [
            "id", "original", "orgname", "country name", "country code", "state", "city",
            "id", "original",
            "id", "original",
        ]
        self.assertEqual(9, len(obtained))
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertEqual(expected[i], item["title"])


    def test_validate_affiliation_count_MNHpJQpnjvSX6pkKCg37yTJ(self):
        self.maxDiff = None
        xml_tree = xml_utils.get_xml_tree("tests/fixtures/htmlgenerator/sub-article_translation_with_sub-article_reply/MNHpJQpnjvSX6pkKCg37yTJ.xml")
        obtained = list(
            AffiliationsListValidation(
                xml_tree
            ).validate_affiliation_count_article_vs_sub_article()
        )
        expected = [
            {
                "advice": None,
                "data": [
                    {
                        "article": '<aff id="aff1">',
                        "sub_article": '<aff id="aff1001">'
                    }
                ],
                "expected_value": "equal counts in articles and sub-articles",
                "got_value": "articles: 1, sub-articles: 1",
                "item": "aff",
                "message": "Got articles: 1, sub-articles: 1, expected equal counts in articles and sub-articles",
                "parent": None,
                "parent_article_type": None,
                "parent_id": None,
                "parent_lang": None,
                "response": "OK",
                "sub_item": None,
                "title": "Affiliation count validation",
                "validation_type": "match",
            }

        ]
        self.assertEqual(len(obtained), 1)
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(item, obtained[i])
