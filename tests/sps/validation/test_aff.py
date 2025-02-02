from unittest import TestCase

from lxml import etree

from packtools.sps.models.v2.aff import ArticleAffiliations
from packtools.sps.validation.aff import (
    AffiliationValidation,
    AffiliationsValidation,
)
from packtools.sps.validation.exceptions import (
    AffiliationCountryCodeListNotProvidedException,
)


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
            AffiliationsValidation(xml_tree, ["BR"]).validate_main_affiliations()
        )
        self.assertEqual(0, len(obtained))
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertIsNone(item)

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
        affiliations_list = list(ArticleAffiliations(xml_tree).article_affs())
        obtained = list(
            AffiliationValidation(affiliations_list[0], ["BR"]).validate_original()
        )

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
        self.assertDictEqual(expected, obtained[0])

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
        affiliations_list = list(ArticleAffiliations(xml_tree).article_affs())
        obtained = list(
            AffiliationValidation(affiliations_list[0], ["BR"]).validate_orgname()
        )

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
        self.assertDictEqual(expected, obtained[0])

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
        affiliations_list = list(ArticleAffiliations(xml_tree).article_affs())
        obtained = list(
            AffiliationValidation(affiliations_list[0], ["BR"]).validate_country()
        )

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
        self.assertDictEqual(expected, obtained[0])

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
        affiliations_list = list(ArticleAffiliations(xml_tree).article_affs())
        obtained = list(
            AffiliationValidation(affiliations_list[0], ["BR"]).validate_country_code()
        )

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
            "expected_value": "one of ['BR']",
            "got_value": None,
            "message": "Got None, expected one of ['BR']",
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
        self.assertDictEqual(expected, obtained[0])

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
        affiliations_list = list(ArticleAffiliations(xml_tree).article_affs())
        obtained = list(
            AffiliationValidation(affiliations_list[0], ["BR"]).validate_state()
        )

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
        self.assertDictEqual(expected, obtained[0])

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
        affiliations_list = list(ArticleAffiliations(xml_tree).article_affs())
        obtained = list(
            AffiliationValidation(affiliations_list[0], ["BR"]).validate_city()
        )

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
        self.assertDictEqual(expected, obtained[0])

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
        affiliations_list = list(ArticleAffiliations(xml_tree).article_affs())
        obtained = list(
            AffiliationValidation(affiliations_list[0], ["BR"]).validate_id()
        )

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
        self.assertDictEqual(expected, obtained[0])

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
        obtained = list(
            AffiliationsValidation(xml_tree, ["BR"]).validate_main_affiliations(data)
        )
        self.assertEqual(0, len(obtained))

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
        obtained = list(
            AffiliationsValidation(xml_tree, ["BR"]).validate_translated_affiliations(
                data
            )
        )
        expected = [
            "orgname",
            "country name",
            "country code",
            "state",
            "city",
            "orgname",
            "country name",
            "country code",
            "state",
            "city",
        ]
        self.assertEqual(10, len(obtained))
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertEqual(expected[i], item["title"])

    def test_validate_affiliation_count(self):
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
                            <institution content-type="orgname">Universidade Federal de Minas Gerais</institution>
                            <addr-line>
                                <named-content content-type="city">Belo Horizonte</named-content>
                                <named-content content-type="state">MG</named-content>
                            </addr-line>
                            <country country="BR">Brasil</country>
                            <institution content-type="original">Faculdade de Medicina. Universidade Federal de Minas Gerais. Belo Horizonte, MG, Brasil</institution>
                        </aff>
                    </article-meta>
                </front>
                <sub-article article-type="translation" id="TRpt" xml:lang="en">
                    <front-stub>
                        <aff id="aff1001">
                            <label>I</label>
                            <institution content-type="orgname">Secretaria Municipal de Saúde de Belo Horizonte</institution>
                            <addr-line>
                                <named-content content-type="city">Belo Horizonte</named-content>
                                <named-content content-type="state">MG</named-content>
                            </addr-line>
                            <country country="BR">Brasil</country>
                            <institution content-type="original">Secretaria Municipal de Saúde de Belo Horizonte. Belo Horizonte, MG, Brasil</institution>
                        </aff>
                    </front-stub>
                </sub-article>
            </article>
            """

        xml_tree = etree.fromstring(xml)
        obtained = list(
            AffiliationsValidation(xml_tree, ["BR"]).validate_affiliation_count()
        )
        expected = [
            {
                "advice": "Check how the affiliations were identified in article-meta and in sub-article en",
                "data": {
                    "article": ["aff1", "aff2"],
                    "sub-article-en": ["aff1001"],
                },
                "expected_value": "equal counts in articles and sub-articles",
                "got_value": "article: 2, sub-article en: 1",
                "item": "aff",
                "message": "Got article: 2, sub-article en: 1, expected equal counts in articles and sub-articles",
                "parent": None,
                "parent_article_type": None,
                "parent_id": None,
                "parent_lang": None,
                "response": "CRITICAL",
                "sub_item": None,
                "title": "Total of affiliations",
                "validation_type": "match",
            }
        ]
        self.assertEqual(len(obtained), 1)
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(item, obtained[i])

    def test_validate_affiliation_multiple_languages(self):
        self.maxDiff = None
        xml = """
            <article article-type="research-article" xml:lang="pt">
                <front>
                    <article-meta>
                        <aff id="aff1">
                            <label>I</label>
                            <institution content-type="orgname">Universidade Federal de Minas Gerais</institution>
                            <addr-line>
                                <named-content content-type="city">Belo Horizonte</named-content>
                                <named-content content-type="state">MG</named-content>
                            </addr-line>
                            <country country="BR">Brasil</country>
                        </aff>
                    </article-meta>
                </front>
                <sub-article article-type="translation" id="TRen" xml:lang="en">
                    <front-stub>
                        <aff id="aff1001">
                            <label>I</label>
                            <institution content-type="orgname">Federal University of Minas Gerais</institution>
                            <addr-line>
                                <named-content content-type="city">Belo Horizonte</named-content>
                                <named-content content-type="state">MG</named-content>
                            </addr-line>
                            <country country="BR">Brazil</country>
                        </aff>
                    </front-stub>
                </sub-article>
                <sub-article article-type="translation" id="TRes" xml:lang="es">
                    <front-stub>
                        <aff id="aff1001">
                            <label>I</label>
                            <institution content-type="orgname">Universidad Federal de Minas Gerais</institution>
                            <addr-line>
                                <named-content content-type="city">Belo Horizonte</named-content>
                                <named-content content-type="state">MG</named-content>
                            </addr-line>
                            <country country="BR">Brasil</country>
                        </aff>
                    </front-stub>
                </sub-article>
            </article>
        """
        xml_tree = etree.fromstring(xml)
        obtained = list(
            AffiliationsValidation(xml_tree, ["BR"]).validate_affiliation_count()
        )
        self.assertEqual(len(obtained), 0)

    def test_validate_affiliation_empty_country_code_list(self):
        self.maxDiff = None
        xml = """
            <article article-type="research-article" xml:lang="pt">
                <front>
                    <article-meta>
                        <aff id="aff1">
                            <label>I</label>
                            <institution content-type="orgname">Universidade Federal de Minas Gerais</institution>
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
        with self.assertRaises(AffiliationCountryCodeListNotProvidedException):
            AffiliationsValidation(xml_tree, []).validate_main_affiliations()
