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
            AffiliationsListValidation(xml_tree, ["BR"]).validade_affiliations_list()
        )

        expected = [
            {
                "title": "Affiliation validation",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "research-article",
                "parent_lang": "pt",
                "item": "institution",
                "sub_item": '@content-type="original"',
                "validation_type": "exist",
                "response": "OK",
                "expected_value": "original affiliation",
                "got_value": "Secretaria Municipal de Saúde de Belo Horizonte. Belo Horizonte, MG, Brasil",
                "message": "Got Secretaria Municipal de Saúde de Belo Horizonte. Belo Horizonte, MG, Brasil, expected original affiliation",
                "advice": None,
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
                    "original": "Secretaria Municipal de Saúde de Belo Horizonte. Belo Horizonte, MG, Brasil",
                    "parent": "article",
                    "parent_article_type": "research-article",
                    "parent_id": None,
                    "parent_lang": "pt",
                    "state": "MG",
                },
            },
            {
                "title": "Affiliation validation",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "research-article",
                "parent_lang": "pt",
                "item": "institution",
                "sub_item": '@content-type="orgname"',
                "validation_type": "exist",
                "response": "OK",
                "expected_value": "orgname affiliation",
                "got_value": "Secretaria Municipal de Saúde de Belo Horizonte",
                "message": "Got Secretaria Municipal de Saúde de Belo Horizonte, expected orgname affiliation",
                "advice": None,
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
                    "original": "Secretaria Municipal de Saúde de Belo Horizonte. Belo Horizonte, MG, Brasil",
                    "parent": "article",
                    "parent_article_type": "research-article",
                    "parent_id": None,
                    "parent_lang": "pt",
                    "state": "MG",
                },
            },
            {
                "title": "Affiliation validation",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "research-article",
                "parent_lang": "pt",
                "item": "aff",
                "sub_item": "country",
                "validation_type": "exist",
                "response": "OK",
                "expected_value": "country affiliation",
                "got_value": "Brasil",
                "message": "Got Brasil, expected country affiliation",
                "advice": None,
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
                    "original": "Secretaria Municipal de Saúde de Belo Horizonte. Belo Horizonte, MG, Brasil",
                    "parent": "article",
                    "parent_article_type": "research-article",
                    "parent_id": None,
                    "parent_lang": "pt",
                    "state": "MG",
                },
            },
            {
                "title": "Affiliation validation",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "research-article",
                "parent_lang": "pt",
                "item": "country",
                "sub_item": "@country",
                "validation_type": "value in list",
                "response": "OK",
                "expected_value": ["BR"],
                "got_value": "BR",
                "message": "Got BR, expected ['BR']",
                "advice": None,
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
                    "original": "Secretaria Municipal de Saúde de Belo Horizonte. Belo Horizonte, MG, Brasil",
                    "parent": "article",
                    "parent_article_type": "research-article",
                    "parent_id": None,
                    "parent_lang": "pt",
                    "state": "MG",
                },
            },
            {
                "title": "Affiliation validation",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "research-article",
                "parent_lang": "pt",
                "item": "addr-line",
                "sub_item": "state",
                "validation_type": "exist",
                "response": "OK",
                "expected_value": "state affiliation",
                "got_value": "MG",
                "message": "Got MG, expected state affiliation",
                "advice": None,
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
                    "original": "Secretaria Municipal de Saúde de Belo Horizonte. Belo Horizonte, MG, Brasil",
                    "parent": "article",
                    "parent_article_type": "research-article",
                    "parent_id": None,
                    "parent_lang": "pt",
                    "state": "MG",
                },
            },
            {
                "title": "Affiliation validation",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "research-article",
                "parent_lang": "pt",
                "item": "addr-line",
                "sub_item": "city",
                "validation_type": "exist",
                "response": "OK",
                "expected_value": "city affiliation",
                "got_value": "Belo Horizonte",
                "message": "Got Belo Horizonte, expected city affiliation",
                "advice": None,
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
                    "original": "Secretaria Municipal de Saúde de Belo Horizonte. Belo Horizonte, MG, Brasil",
                    "parent": "article",
                    "parent_article_type": "research-article",
                    "parent_id": None,
                    "parent_lang": "pt",
                    "state": "MG",
                },
            },
            {
                "title": "Affiliation validation",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "research-article",
                "parent_lang": "pt",
                "item": "institution",
                "sub_item": '@content-type="original"',
                "validation_type": "exist",
                "response": "OK",
                "expected_value": "original affiliation",
                "got_value": "Grupo de Pesquisas em Epidemiologia e Avaliação em Saúde. Faculdade de Medicina. "
                "Universidade Federal de Minas Gerais. Belo Horizonte, MG, Brasil",
                "message": "Got Grupo de Pesquisas em Epidemiologia e Avaliação em Saúde. Faculdade de Medicina. "
                "Universidade Federal de Minas Gerais. Belo Horizonte, MG, Brasil, expected original "
                "affiliation",
                "advice": None,
                "data": {
                    "city": "Belo Horizonte",
                    "country_code": "BR",
                    "country_name": "Brasil",
                    "email": None,
                    "id": "aff2",
                    "label": "II",
                    "orgdiv1": "Faculdade de Medicina",
                    "orgdiv2": None,
                    "orgname": "Universidade Federal de Minas Gerais",
                    "original": "Grupo de Pesquisas em Epidemiologia e Avaliação em "
                    "Saúde. Faculdade de Medicina. Universidade Federal de "
                    "Minas Gerais. Belo Horizonte, MG, Brasil",
                    "parent": "article",
                    "parent_article_type": "research-article",
                    "parent_id": None,
                    "parent_lang": "pt",
                    "state": "MG",
                },
            },
            {
                "title": "Affiliation validation",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "research-article",
                "parent_lang": "pt",
                "item": "institution",
                "sub_item": '@content-type="orgname"',
                "validation_type": "exist",
                "response": "OK",
                "expected_value": "orgname affiliation",
                "got_value": "Universidade Federal de Minas Gerais",
                "message": "Got Universidade Federal de Minas Gerais, expected orgname affiliation",
                "advice": None,
                "data": {
                    "city": "Belo Horizonte",
                    "country_code": "BR",
                    "country_name": "Brasil",
                    "email": None,
                    "id": "aff2",
                    "label": "II",
                    "orgdiv1": "Faculdade de Medicina",
                    "orgdiv2": None,
                    "orgname": "Universidade Federal de Minas Gerais",
                    "original": "Grupo de Pesquisas em Epidemiologia e Avaliação em "
                    "Saúde. Faculdade de Medicina. Universidade Federal de "
                    "Minas Gerais. Belo Horizonte, MG, Brasil",
                    "parent": "article",
                    "parent_article_type": "research-article",
                    "parent_id": None,
                    "parent_lang": "pt",
                    "state": "MG",
                },
            },
            {
                "title": "Affiliation validation",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "research-article",
                "parent_lang": "pt",
                "item": "aff",
                "sub_item": "country",
                "validation_type": "exist",
                "response": "OK",
                "expected_value": "country affiliation",
                "got_value": "Brasil",
                "message": "Got Brasil, expected country affiliation",
                "advice": None,
                "data": {
                    "city": "Belo Horizonte",
                    "country_code": "BR",
                    "country_name": "Brasil",
                    "email": None,
                    "id": "aff2",
                    "label": "II",
                    "orgdiv1": "Faculdade de Medicina",
                    "orgdiv2": None,
                    "orgname": "Universidade Federal de Minas Gerais",
                    "original": "Grupo de Pesquisas em Epidemiologia e Avaliação em "
                    "Saúde. Faculdade de Medicina. Universidade Federal de "
                    "Minas Gerais. Belo Horizonte, MG, Brasil",
                    "parent": "article",
                    "parent_article_type": "research-article",
                    "parent_id": None,
                    "parent_lang": "pt",
                    "state": "MG",
                },
            },
            {
                "title": "Affiliation validation",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "research-article",
                "parent_lang": "pt",
                "item": "country",
                "sub_item": "@country",
                "validation_type": "value in list",
                "response": "OK",
                "expected_value": ["BR"],
                "got_value": "BR",
                "message": "Got BR, expected ['BR']",
                "advice": None,
                "data": {
                    "city": "Belo Horizonte",
                    "country_code": "BR",
                    "country_name": "Brasil",
                    "email": None,
                    "id": "aff2",
                    "label": "II",
                    "orgdiv1": "Faculdade de Medicina",
                    "orgdiv2": None,
                    "orgname": "Universidade Federal de Minas Gerais",
                    "original": "Grupo de Pesquisas em Epidemiologia e Avaliação em "
                    "Saúde. Faculdade de Medicina. Universidade Federal de "
                    "Minas Gerais. Belo Horizonte, MG, Brasil",
                    "parent": "article",
                    "parent_article_type": "research-article",
                    "parent_id": None,
                    "parent_lang": "pt",
                    "state": "MG",
                },
            },
            {
                "title": "Affiliation validation",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "research-article",
                "parent_lang": "pt",
                "item": "addr-line",
                "sub_item": "state",
                "validation_type": "exist",
                "response": "OK",
                "expected_value": "state affiliation",
                "got_value": "MG",
                "message": "Got MG, expected state affiliation",
                "advice": None,
                "data": {
                    "city": "Belo Horizonte",
                    "country_code": "BR",
                    "country_name": "Brasil",
                    "email": None,
                    "id": "aff2",
                    "label": "II",
                    "orgdiv1": "Faculdade de Medicina",
                    "orgdiv2": None,
                    "orgname": "Universidade Federal de Minas Gerais",
                    "original": "Grupo de Pesquisas em Epidemiologia e Avaliação em "
                    "Saúde. Faculdade de Medicina. Universidade Federal de "
                    "Minas Gerais. Belo Horizonte, MG, Brasil",
                    "parent": "article",
                    "parent_article_type": "research-article",
                    "parent_id": None,
                    "parent_lang": "pt",
                    "state": "MG",
                },
            },
            {
                "title": "Affiliation validation",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "research-article",
                "parent_lang": "pt",
                "item": "addr-line",
                "sub_item": "city",
                "validation_type": "exist",
                "response": "OK",
                "expected_value": "city affiliation",
                "got_value": "Belo Horizonte",
                "message": "Got Belo Horizonte, expected city affiliation",
                "advice": None,
                "data": {
                    "city": "Belo Horizonte",
                    "country_code": "BR",
                    "country_name": "Brasil",
                    "email": None,
                    "id": "aff2",
                    "label": "II",
                    "orgdiv1": "Faculdade de Medicina",
                    "orgdiv2": None,
                    "orgname": "Universidade Federal de Minas Gerais",
                    "original": "Grupo de Pesquisas em Epidemiologia e Avaliação em "
                    "Saúde. Faculdade de Medicina. Universidade Federal de "
                    "Minas Gerais. Belo Horizonte, MG, Brasil",
                    "parent": "article",
                    "parent_article_type": "research-article",
                    "parent_id": None,
                    "parent_lang": "pt",
                    "state": "MG",
                },
            },
        ]

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(item, obtained[i])

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
        obtained = list(AffiliationValidation(affiliations_list[0]).validate_original())

        expected = [
            {
                "title": "Affiliation validation",
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
        ]

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(item, obtained[i])

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
        obtained = list(AffiliationValidation(affiliations_list[0]).validate_orgname())

        expected = [
            {
                "title": "Affiliation validation",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "research-article",
                "parent_lang": "pt",
                "item": "institution",
                "sub_item": '@content-type="orgname"',
                "validation_type": "exist",
                "response": "CRITICAL",
                "expected_value": "orgname affiliation",
                "got_value": None,
                "message": "Got None, expected orgname affiliation",
                "advice": "provide the orgname affiliation",
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
        ]

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(item, obtained[i])

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
        obtained = list(AffiliationValidation(affiliations_list[0]).validate_country())

        expected = [
            {
                "title": "Affiliation validation",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "research-article",
                "parent_lang": "pt",
                "item": "aff",
                "sub_item": "country",
                "validation_type": "exist",
                "response": "CRITICAL",
                "expected_value": "country affiliation",
                "got_value": None,
                "message": "Got None, expected country affiliation",
                "advice": "provide the country affiliation",
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
        ]

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(item, obtained[i])

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
        obtained = list(
            AffiliationValidation(affiliations_list[0], ["BR"]).validate_country_code()
        )

        expected = [
            {
                "title": "Affiliation validation",
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
                "advice": "provide a valid @country affiliation",
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
        ]

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(item, obtained[i])

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
        obtained = list(AffiliationValidation(affiliations_list[0]).validate_state())

        expected = [
            {
                "title": "Affiliation validation",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "research-article",
                "parent_lang": "pt",
                "item": "addr-line",
                "sub_item": "state",
                "validation_type": "exist",
                "response": "ERROR",
                "expected_value": "state affiliation",
                "got_value": None,
                "message": "Got None, expected state affiliation",
                "advice": "provide the state affiliation",
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
        ]

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(item, obtained[i])

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
        obtained = list(AffiliationValidation(affiliations_list[0]).validate_city())

        expected = [
            {
                "title": "Affiliation validation",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "research-article",
                "parent_lang": "pt",
                "item": "addr-line",
                "sub_item": "city",
                "validation_type": "exist",
                "response": "ERROR",
                "expected_value": "city affiliation",
                "got_value": None,
                "message": "Got None, expected city affiliation",
                "advice": "provide the city affiliation",
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
        ]

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(item, obtained[i])

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
        obtained = list(AffiliationValidation(affiliations_list[0]).validate_id())

        expected = [
            {
                "title": "Affiliation validation",
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
        ]

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(item, obtained[i])

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
            {
                "title": "Affiliation validation",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "research-article",
                "parent_lang": "pt",
                "item": "institution",
                "sub_item": '@content-type="original"',
                "validation_type": "exist",
                "response": "OK",
                "expected_value": "original affiliation",
                "got_value": "Secretaria Municipal de Saúde de Belo Horizonte. Belo Horizonte, MG, Brasil",
                "message": "Got Secretaria Municipal de Saúde de Belo Horizonte. Belo Horizonte, MG, Brasil, expected original affiliation",
                "advice": None,
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
                    "original": "Secretaria Municipal de Saúde de Belo Horizonte. Belo Horizonte, MG, Brasil",
                    "parent": "article",
                    "parent_id": None,
                    "parent_article_type": "research-article",
                    "parent_lang": "pt",
                    "state": "MG",
                },
            },
            {
                "title": "Affiliation validation",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "research-article",
                "parent_lang": "pt",
                "item": "institution",
                "sub_item": '@content-type="orgname"',
                "validation_type": "exist",
                "response": "OK",
                "expected_value": "orgname affiliation",
                "got_value": "Secretaria Municipal de Saúde de Belo Horizonte",
                "message": "Got Secretaria Municipal de Saúde de Belo Horizonte, expected orgname affiliation",
                "advice": None,
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
                    "original": "Secretaria Municipal de Saúde de Belo Horizonte. Belo Horizonte, MG, Brasil",
                    "parent": "article",
                    "parent_id": None,
                    "parent_article_type": "research-article",
                    "parent_lang": "pt",
                    "state": "MG",
                },
            },
            {
                "title": "Affiliation validation",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "research-article",
                "parent_lang": "pt",
                "item": "aff",
                "sub_item": "country",
                "validation_type": "exist",
                "response": "OK",
                "expected_value": "country affiliation",
                "got_value": "Brasil",
                "message": "Got Brasil, expected country affiliation",
                "advice": None,
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
                    "original": "Secretaria Municipal de Saúde de Belo Horizonte. Belo Horizonte, MG, Brasil",
                    "parent": "article",
                    "parent_id": None,
                    "parent_article_type": "research-article",
                    "parent_lang": "pt",
                    "state": "MG",
                },
            },
            {
                "title": "Affiliation validation",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "research-article",
                "parent_lang": "pt",
                "item": "country",
                "sub_item": "@country",
                "validation_type": "value in list",
                "response": "OK",
                "expected_value": ["BR"],
                "got_value": "BR",
                "message": "Got BR, expected ['BR']",
                "advice": None,
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
                    "original": "Secretaria Municipal de Saúde de Belo Horizonte. Belo Horizonte, MG, Brasil",
                    "parent": "article",
                    "parent_id": None,
                    "parent_article_type": "research-article",
                    "parent_lang": "pt",
                    "state": "MG",
                },
            },
            {
                "title": "Affiliation validation",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "research-article",
                "parent_lang": "pt",
                "item": "addr-line",
                "sub_item": "state",
                "validation_type": "exist",
                "response": "OK",
                "expected_value": "state affiliation",
                "got_value": "MG",
                "message": "Got MG, expected state affiliation",
                "advice": None,
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
                    "original": "Secretaria Municipal de Saúde de Belo Horizonte. Belo Horizonte, MG, Brasil",
                    "parent": "article",
                    "parent_id": None,
                    "parent_article_type": "research-article",
                    "parent_lang": "pt",
                    "state": "MG",
                },
            },
            {
                "title": "Affiliation validation",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "research-article",
                "parent_lang": "pt",
                "item": "addr-line",
                "sub_item": "city",
                "validation_type": "exist",
                "response": "OK",
                "expected_value": "city affiliation",
                "got_value": "Belo Horizonte",
                "message": "Got Belo Horizonte, expected city affiliation",
                "advice": None,
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
                    "original": "Secretaria Municipal de Saúde de Belo Horizonte. Belo Horizonte, MG, Brasil",
                    "parent": "article",
                    "parent_id": None,
                    "parent_article_type": "research-article",
                    "parent_lang": "pt",
                    "state": "MG",
                },
            },
            {
                "title": "Affiliation validation",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "research-article",
                "parent_lang": "pt",
                "item": "institution",
                "sub_item": '@content-type="original"',
                "validation_type": "exist",
                "response": "OK",
                "expected_value": "original affiliation",
                "got_value": "Grupo de Pesquisas em Epidemiologia e Avaliação em Saúde. Faculdade de Medicina. "
                "Universidade Federal de Minas Gerais. Belo Horizonte, MG, Brasil",
                "message": "Got Grupo de Pesquisas em Epidemiologia e Avaliação em Saúde. Faculdade de Medicina. "
                "Universidade Federal de Minas Gerais. Belo Horizonte, MG, Brasil, expected original "
                "affiliation",
                "advice": None,
                "data": {
                    "city": "Belo Horizonte",
                    "country_code": "BR",
                    "country_name": "Brasil",
                    "email": None,
                    "id": "aff2",
                    "label": "II",
                    "orgdiv1": "Faculdade de Medicina",
                    "orgdiv2": None,
                    "orgname": "Universidade Federal de Minas Gerais",
                    "original": "Grupo de Pesquisas em Epidemiologia e Avaliação em "
                    "Saúde. Faculdade de Medicina. Universidade Federal de "
                    "Minas Gerais. Belo Horizonte, MG, Brasil",
                    "parent": "article",
                    "parent_id": None,
                    "parent_article_type": "research-article",
                    "parent_lang": "pt",
                    "state": "MG",
                },
            },
            {
                "title": "Affiliation validation",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "research-article",
                "parent_lang": "pt",
                "item": "institution",
                "sub_item": '@content-type="orgname"',
                "validation_type": "exist",
                "response": "OK",
                "expected_value": "orgname affiliation",
                "got_value": "Universidade Federal de Minas Gerais",
                "message": "Got Universidade Federal de Minas Gerais, expected orgname affiliation",
                "advice": None,
                "data": {
                    "city": "Belo Horizonte",
                    "country_code": "BR",
                    "country_name": "Brasil",
                    "email": None,
                    "id": "aff2",
                    "label": "II",
                    "orgdiv1": "Faculdade de Medicina",
                    "orgdiv2": None,
                    "orgname": "Universidade Federal de Minas Gerais",
                    "original": "Grupo de Pesquisas em Epidemiologia e Avaliação em "
                    "Saúde. Faculdade de Medicina. Universidade Federal de "
                    "Minas Gerais. Belo Horizonte, MG, Brasil",
                    "parent": "article",
                    "parent_id": None,
                    "parent_article_type": "research-article",
                    "parent_lang": "pt",
                    "state": "MG",
                },
            },
            {
                "title": "Affiliation validation",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "research-article",
                "parent_lang": "pt",
                "item": "aff",
                "sub_item": "country",
                "validation_type": "exist",
                "response": "OK",
                "expected_value": "country affiliation",
                "got_value": "Brasil",
                "message": "Got Brasil, expected country affiliation",
                "advice": None,
                "data": {
                    "city": "Belo Horizonte",
                    "country_code": "BR",
                    "country_name": "Brasil",
                    "email": None,
                    "id": "aff2",
                    "label": "II",
                    "orgdiv1": "Faculdade de Medicina",
                    "orgdiv2": None,
                    "orgname": "Universidade Federal de Minas Gerais",
                    "original": "Grupo de Pesquisas em Epidemiologia e Avaliação em "
                    "Saúde. Faculdade de Medicina. Universidade Federal de "
                    "Minas Gerais. Belo Horizonte, MG, Brasil",
                    "parent": "article",
                    "parent_id": None,
                    "parent_article_type": "research-article",
                    "parent_lang": "pt",
                    "state": "MG",
                },
            },
            {
                "title": "Affiliation validation",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "research-article",
                "parent_lang": "pt",
                "item": "country",
                "sub_item": "@country",
                "validation_type": "value in list",
                "response": "OK",
                "expected_value": ["BR"],
                "got_value": "BR",
                "message": "Got BR, expected ['BR']",
                "advice": None,
                "data": {
                    "city": "Belo Horizonte",
                    "country_code": "BR",
                    "country_name": "Brasil",
                    "email": None,
                    "id": "aff2",
                    "label": "II",
                    "orgdiv1": "Faculdade de Medicina",
                    "orgdiv2": None,
                    "orgname": "Universidade Federal de Minas Gerais",
                    "original": "Grupo de Pesquisas em Epidemiologia e Avaliação em "
                    "Saúde. Faculdade de Medicina. Universidade Federal de "
                    "Minas Gerais. Belo Horizonte, MG, Brasil",
                    "parent": "article",
                    "parent_id": None,
                    "parent_article_type": "research-article",
                    "parent_lang": "pt",
                    "state": "MG",
                },
            },
            {
                "title": "Affiliation validation",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "research-article",
                "parent_lang": "pt",
                "item": "addr-line",
                "sub_item": "state",
                "validation_type": "exist",
                "response": "OK",
                "expected_value": "state affiliation",
                "got_value": "MG",
                "message": "Got MG, expected state affiliation",
                "advice": None,
                "data": {
                    "city": "Belo Horizonte",
                    "country_code": "BR",
                    "country_name": "Brasil",
                    "email": None,
                    "id": "aff2",
                    "label": "II",
                    "orgdiv1": "Faculdade de Medicina",
                    "orgdiv2": None,
                    "orgname": "Universidade Federal de Minas Gerais",
                    "original": "Grupo de Pesquisas em Epidemiologia e Avaliação em "
                    "Saúde. Faculdade de Medicina. Universidade Federal de "
                    "Minas Gerais. Belo Horizonte, MG, Brasil",
                    "parent": "article",
                    "parent_id": None,
                    "parent_article_type": "research-article",
                    "parent_lang": "pt",
                    "state": "MG",
                },
            },
            {
                "title": "Affiliation validation",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "research-article",
                "parent_lang": "pt",
                "item": "addr-line",
                "sub_item": "city",
                "validation_type": "exist",
                "response": "OK",
                "expected_value": "city affiliation",
                "got_value": "Belo Horizonte",
                "message": "Got Belo Horizonte, expected city affiliation",
                "advice": None,
                "data": {
                    "city": "Belo Horizonte",
                    "country_code": "BR",
                    "country_name": "Brasil",
                    "email": None,
                    "id": "aff2",
                    "label": "II",
                    "orgdiv1": "Faculdade de Medicina",
                    "orgdiv2": None,
                    "orgname": "Universidade Federal de Minas Gerais",
                    "original": "Grupo de Pesquisas em Epidemiologia e Avaliação em "
                    "Saúde. Faculdade de Medicina. Universidade Federal de "
                    "Minas Gerais. Belo Horizonte, MG, Brasil",
                    "parent": "article",
                    "parent_id": None,
                    "parent_article_type": "research-article",
                    "parent_lang": "pt",
                    "state": "MG",
                },
            },
        ]

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(item, obtained[i])

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
                </article>
                """

        xml_tree = etree.fromstring(xml)
        data = {"country_codes_list": ["BR"]}
        obtained = list(AffiliationsListValidation(xml_tree).validate(data))
        expected = [
            {
                "title": "Affiliation validation",
                "parent": "sub-article",
                "parent_id": "TRpt",
                "parent_article_type": "translation",
                "parent_lang": "pt",
                "item": "institution",
                "sub_item": '@content-type="original"',
                "validation_type": "exist",
                "response": "OK",
                "expected_value": "original affiliation",
                "got_value": "Universidade Federal de Pelotas. Faculdade de Medicina. Programa de Pós-Graduação em Epidemiologia. Pelotas, RS, Brasil",
                "message": "Got Universidade Federal de Pelotas. Faculdade de Medicina. Programa de Pós-Graduação em Epidemiologia. Pelotas, RS, Brasil, expected original affiliation",
                "advice": None,
                "data": {
                    "city": None,
                    "country_code": "BR",
                    "country_name": "Brasil",
                    "email": None,
                    "id": "aff1002",
                    "label": "I",
                    "orgdiv1": None,
                    "orgdiv2": None,
                    "orgname": None,
                    "original": "Universidade Federal de Pelotas. Faculdade de Medicina. Programa de Pós-Graduação em Epidemiologia. Pelotas, RS, Brasil",
                    "parent": "sub-article",
                    "parent_article_type": "translation",
                    "parent_id": "TRpt",
                    "parent_lang": "pt",
                    "state": None,
                }
            }

        ]

        self.assertEqual(len(obtained), 1)
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(item, obtained[i])

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
                        'article': '<aff id=aff1>',
                        'sub_article': '<aff id=aff1002>'
                    },
                    {
                        'article': '<aff id=aff2>',
                        'sub_article': '<aff id=aff2002>'
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
        obtained = list(AffiliationsListValidation(xml_tree).validate(data))
        expected = [
            {
                "advice": None,
                "data": {
                    "city": "João Pessoa",
                    "country_code": "BR",
                    "country_name": "Brasil",
                    "email": "kidinho_dc@hotmail.com",
                    "id": "aff1",
                    "label": "*",
                    "orgdiv1": "Programa de Pós-Graduação em Filosofia",
                    "orgdiv2": None,
                    "orgname": "Universidade Federal da Paraíba -UFPB",
                    "original": "Mestre em Filosofia pelo Programa de Pós-Graduação em "
                                "Filosofia da Universidade Federal da Paraíba -UFPB, "
                                "João Pessoa, Paraíba, Brasil; kidinho_dc@hotmail.com",
                    "parent": "article",
                    "parent_article_type": "research-article",
                    "parent_id": None,
                    "parent_lang": "pt",
                    "state": "Paraíba",
                },
                "expected_value": "original affiliation",
                "got_value": "Mestre em Filosofia pelo Programa de Pós-Graduação em Filosofia "
                             "da Universidade Federal da Paraíba -UFPB, João Pessoa, Paraíba, "
                             "Brasil; kidinho_dc@hotmail.com",
                "item": "institution",
                "message": "Got Mestre em Filosofia pelo Programa de Pós-Graduação em "
                           "Filosofia da Universidade Federal da Paraíba -UFPB, João Pessoa, "
                           "Paraíba, Brasil; kidinho_dc@hotmail.com, expected original "
                           "affiliation",
                "parent": "article",
                "parent_article_type": "research-article",
                "parent_id": None,
                "parent_lang": "pt",
                "response": "OK",
                "sub_item": '@content-type="original"',
                "title": "Affiliation validation",
                "validation_type": "exist",
            },
            {
                "advice": None,
                "data": {
                    "city": "João Pessoa",
                    "country_code": "BR",
                    "country_name": "Brasil",
                    "email": "kidinho_dc@hotmail.com",
                    "id": "aff1",
                    "label": "*",
                    "orgdiv1": "Programa de Pós-Graduação em Filosofia",
                    "orgdiv2": None,
                    "orgname": "Universidade Federal da Paraíba -UFPB",
                    "original": "Mestre em Filosofia pelo Programa de Pós-Graduação em "
                                "Filosofia da Universidade Federal da Paraíba -UFPB, "
                                "João Pessoa, Paraíba, Brasil; kidinho_dc@hotmail.com",
                    "parent": "article",
                    "parent_article_type": "research-article",
                    "parent_id": None,
                    "parent_lang": "pt",
                    "state": "Paraíba",
                },
                "expected_value": "orgname affiliation",
                "got_value": "Universidade Federal da Paraíba -UFPB",
                "item": "institution",
                "message": "Got Universidade Federal da Paraíba -UFPB, expected orgname "
                           "affiliation",
                "parent": "article",
                "parent_article_type": "research-article",
                "parent_id": None,
                "parent_lang": "pt",
                "response": "OK",
                "sub_item": '@content-type="orgname"',
                "title": "Affiliation validation",
                "validation_type": "exist",
            },
            {
                "advice": None,
                "data": {
                    "city": "João Pessoa",
                    "country_code": "BR",
                    "country_name": "Brasil",
                    "email": "kidinho_dc@hotmail.com",
                    "id": "aff1",
                    "label": "*",
                    "orgdiv1": "Programa de Pós-Graduação em Filosofia",
                    "orgdiv2": None,
                    "orgname": "Universidade Federal da Paraíba -UFPB",
                    "original": "Mestre em Filosofia pelo Programa de Pós-Graduação em "
                                "Filosofia da Universidade Federal da Paraíba -UFPB, "
                                "João Pessoa, Paraíba, Brasil; kidinho_dc@hotmail.com",
                    "parent": "article",
                    "parent_article_type": "research-article",
                    "parent_id": None,
                    "parent_lang": "pt",
                    "state": "Paraíba",
                },
                "expected_value": "country affiliation",
                "got_value": "Brasil",
                "item": "aff",
                "message": "Got Brasil, expected country affiliation",
                "parent": "article",
                "parent_article_type": "research-article",
                "parent_id": None,
                "parent_lang": "pt",
                "response": "OK",
                "sub_item": "country",
                "title": "Affiliation validation",
                "validation_type": "exist",
            },
            {
                "advice": None,
                "data": {
                    "city": "João Pessoa",
                    "country_code": "BR",
                    "country_name": "Brasil",
                    "email": "kidinho_dc@hotmail.com",
                    "id": "aff1",
                    "label": "*",
                    "orgdiv1": "Programa de Pós-Graduação em Filosofia",
                    "orgdiv2": None,
                    "orgname": "Universidade Federal da Paraíba -UFPB",
                    "original": "Mestre em Filosofia pelo Programa de Pós-Graduação em "
                                "Filosofia da Universidade Federal da Paraíba -UFPB, "
                                "João Pessoa, Paraíba, Brasil; kidinho_dc@hotmail.com",
                    "parent": "article",
                    "parent_article_type": "research-article",
                    "parent_id": None,
                    "parent_lang": "pt",
                    "state": "Paraíba",
                },
                "expected_value": ["BR"],
                "got_value": "BR",
                "item": "country",
                "message": "Got BR, expected ['BR']",
                "parent": "article",
                "parent_article_type": "research-article",
                "parent_id": None,
                "parent_lang": "pt",
                "response": "OK",
                "sub_item": "@country",
                "title": "Affiliation validation",
                "validation_type": "value in list",
            },
            {
                "advice": None,
                "data": {
                    "city": "João Pessoa",
                    "country_code": "BR",
                    "country_name": "Brasil",
                    "email": "kidinho_dc@hotmail.com",
                    "id": "aff1",
                    "label": "*",
                    "orgdiv1": "Programa de Pós-Graduação em Filosofia",
                    "orgdiv2": None,
                    "orgname": "Universidade Federal da Paraíba -UFPB",
                    "original": "Mestre em Filosofia pelo Programa de Pós-Graduação em "
                                "Filosofia da Universidade Federal da Paraíba -UFPB, "
                                "João Pessoa, Paraíba, Brasil; kidinho_dc@hotmail.com",
                    "parent": "article",
                    "parent_article_type": "research-article",
                    "parent_id": None,
                    "parent_lang": "pt",
                    "state": "Paraíba",
                },
                "expected_value": "state affiliation",
                "got_value": "Paraíba",
                "item": "addr-line",
                "message": "Got Paraíba, expected state affiliation",
                "parent": "article",
                "parent_article_type": "research-article",
                "parent_id": None,
                "parent_lang": "pt",
                "response": "OK",
                "sub_item": "state",
                "title": "Affiliation validation",
                "validation_type": "exist",
            },
            {
                "advice": None,
                "data": {
                    "city": "João Pessoa",
                    "country_code": "BR",
                    "country_name": "Brasil",
                    "email": "kidinho_dc@hotmail.com",
                    "id": "aff1",
                    "label": "*",
                    "orgdiv1": "Programa de Pós-Graduação em Filosofia",
                    "orgdiv2": None,
                    "orgname": "Universidade Federal da Paraíba -UFPB",
                    "original": "Mestre em Filosofia pelo Programa de Pós-Graduação em "
                                "Filosofia da Universidade Federal da Paraíba -UFPB, "
                                "João Pessoa, Paraíba, Brasil; kidinho_dc@hotmail.com",
                    "parent": "article",
                    "parent_article_type": "research-article",
                    "parent_id": None,
                    "parent_lang": "pt",
                    "state": "Paraíba",
                },
                "expected_value": "city affiliation",
                "got_value": "João Pessoa",
                "item": "addr-line",
                "message": "Got João Pessoa, expected city affiliation",
                "parent": "article",
                "parent_article_type": "research-article",
                "parent_id": None,
                "parent_lang": "pt",
                "response": "OK",
                "sub_item": "city",
                "title": "Affiliation validation",
                "validation_type": "exist",
            },
            {
                "advice": None,
                "data": {
                    "city": None,
                    "country_code": None,
                    "country_name": None,
                    "email": None,
                    "id": "aff2",
                    "label": "*",
                    "orgdiv1": None,
                    "orgdiv2": None,
                    "orgname": None,
                    "original": "MA in Philosophy from Programa de Pós-Graduação em "
                                "Filosofia at Universidade Federal da Paraíba – UFPB, "
                                "João Pessoa, Paraíba, Brazil; kidinho_dc@hotmail.com",
                    "parent": "sub-article",
                    "parent_article_type": "translation",
                    "parent_id": "s1",
                    "parent_lang": "en",
                    "state": None,
                },
                "expected_value": "original affiliation",
                "got_value": "MA in Philosophy from Programa de Pós-Graduação em Filosofia at "
                             "Universidade Federal da Paraíba – UFPB, João Pessoa, Paraíba, "
                             "Brazil; kidinho_dc@hotmail.com",
                "item": "institution",
                "message": "Got MA in Philosophy from Programa de Pós-Graduação em Filosofia "
                           "at Universidade Federal da Paraíba – UFPB, João Pessoa, Paraíba, "
                           "Brazil; kidinho_dc@hotmail.com, expected original affiliation",
                "parent": "sub-article",
                "parent_article_type": "translation",
                "parent_id": "s1",
                "parent_lang": "en",
                "response": "OK",
                "sub_item": '@content-type="original"',
                "title": "Affiliation validation",
                "validation_type": "exist",
            }
        ]
        self.assertEqual(len(obtained), 7)
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(item, obtained[i])

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
                        "article": "<aff id=aff1>",
                        "sub_article": "<aff id=aff2>"
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
            {
                "advice": None,
                "data": {
                    "city": "Tubarão",
                    "country_code": "BR",
                    "country_name": "Brasil",
                    "email": None,
                    "id": "aff1",
                    "label": " 1 ",
                    "orgdiv1": None,
                    "orgdiv2": None,
                    "orgname": "Universidade do Sul de Santa Catarina",
                    "original": "Universidade do Sul de Santa Catarina, Tubarão, SC – " "Brasil",
                    "parent": "article",
                    "parent_article_type": "letter",
                    "parent_id": None,
                    "parent_lang": "pt",
                    "state": "SC",
                },
                "expected_value": "original affiliation",
                "got_value": "Universidade do Sul de Santa Catarina, Tubarão, SC – Brasil",
                "item": "institution",
                "message": "Got Universidade do Sul de Santa Catarina, Tubarão, SC – Brasil, "
                           "expected original affiliation",
                "parent": "article",
                "parent_article_type": "letter",
                "parent_id": None,
                "parent_lang": "pt",
                "response": "OK",
                "sub_item": '@content-type="original"',
                "title": "Affiliation validation",
                "validation_type": "exist",
            },
            {
                "advice": None,
                "data": {
                    "city": "Tubarão",
                    "country_code": "BR",
                    "country_name": "Brasil",
                    "email": None,
                    "id": "aff1",
                    "label": " 1 ",
                    "orgdiv1": None,
                    "orgdiv2": None,
                    "orgname": "Universidade do Sul de Santa Catarina",
                    "original": "Universidade do Sul de Santa Catarina, Tubarão, SC – " "Brasil",
                    "parent": "article",
                    "parent_article_type": "letter",
                    "parent_id": None,
                    "parent_lang": "pt",
                    "state": "SC",
                },
                "expected_value": "orgname affiliation",
                "got_value": "Universidade do Sul de Santa Catarina",
                "item": "institution",
                "message": "Got Universidade do Sul de Santa Catarina, expected orgname "
                           "affiliation",
                "parent": "article",
                "parent_article_type": "letter",
                "parent_id": None,
                "parent_lang": "pt",
                "response": "OK",
                "sub_item": '@content-type="orgname"',
                "title": "Affiliation validation",
                "validation_type": "exist",
            },
            {
                "advice": None,
                "data": {
                    "city": "Tubarão",
                    "country_code": "BR",
                    "country_name": "Brasil",
                    "email": None,
                    "id": "aff1",
                    "label": " 1 ",
                    "orgdiv1": None,
                    "orgdiv2": None,
                    "orgname": "Universidade do Sul de Santa Catarina",
                    "original": "Universidade do Sul de Santa Catarina, Tubarão, SC – " "Brasil",
                    "parent": "article",
                    "parent_article_type": "letter",
                    "parent_id": None,
                    "parent_lang": "pt",
                    "state": "SC",
                },
                "expected_value": "country affiliation",
                "got_value": "Brasil",
                "item": "aff",
                "message": "Got Brasil, expected country affiliation",
                "parent": "article",
                "parent_article_type": "letter",
                "parent_id": None,
                "parent_lang": "pt",
                "response": "OK",
                "sub_item": "country",
                "title": "Affiliation validation",
                "validation_type": "exist",
            },
            {
                "advice": None,
                "data": {
                    "city": "Tubarão",
                    "country_code": "BR",
                    "country_name": "Brasil",
                    "email": None,
                    "id": "aff1",
                    "label": " 1 ",
                    "orgdiv1": None,
                    "orgdiv2": None,
                    "orgname": "Universidade do Sul de Santa Catarina",
                    "original": "Universidade do Sul de Santa Catarina, Tubarão, SC – " "Brasil",
                    "parent": "article",
                    "parent_article_type": "letter",
                    "parent_id": None,
                    "parent_lang": "pt",
                    "state": "SC",
                },
                "expected_value": ["BR"],
                "got_value": "BR",
                "item": "country",
                "message": "Got BR, expected ['BR']",
                "parent": "article",
                "parent_article_type": "letter",
                "parent_id": None,
                "parent_lang": "pt",
                "response": "OK",
                "sub_item": "@country",
                "title": "Affiliation validation",
                "validation_type": "value in list",
            },
            {
                "advice": None,
                "data": {
                    "city": "Tubarão",
                    "country_code": "BR",
                    "country_name": "Brasil",
                    "email": None,
                    "id": "aff1",
                    "label": " 1 ",
                    "orgdiv1": None,
                    "orgdiv2": None,
                    "orgname": "Universidade do Sul de Santa Catarina",
                    "original": "Universidade do Sul de Santa Catarina, Tubarão, SC – " "Brasil",
                    "parent": "article",
                    "parent_article_type": "letter",
                    "parent_id": None,
                    "parent_lang": "pt",
                    "state": "SC",
                },
                "expected_value": "state affiliation",
                "got_value": "SC",
                "item": "addr-line",
                "message": "Got SC, expected state affiliation",
                "parent": "article",
                "parent_article_type": "letter",
                "parent_id": None,
                "parent_lang": "pt",
                "response": "OK",
                "sub_item": "state",
                "title": "Affiliation validation",
                "validation_type": "exist",
            },
            {
                "advice": None,
                "data": {
                    "city": "Tubarão",
                    "country_code": "BR",
                    "country_name": "Brasil",
                    "email": None,
                    "id": "aff1",
                    "label": " 1 ",
                    "orgdiv1": None,
                    "orgdiv2": None,
                    "orgname": "Universidade do Sul de Santa Catarina",
                    "original": "Universidade do Sul de Santa Catarina, Tubarão, SC – " "Brasil",
                    "parent": "article",
                    "parent_article_type": "letter",
                    "parent_id": None,
                    "parent_lang": "pt",
                    "state": "SC",
                },
                "expected_value": "city affiliation",
                "got_value": "Tubarão",
                "item": "addr-line",
                "message": "Got Tubarão, expected city affiliation",
                "parent": "article",
                "parent_article_type": "letter",
                "parent_id": None,
                "parent_lang": "pt",
                "response": "OK",
                "sub_item": "city",
                "title": "Affiliation validation",
                "validation_type": "exist",
            },
            {
                "advice": None,
                "data": {
                    "city": None,
                    "country_code": "BR",
                    "country_name": "Brazil",
                    "email": None,
                    "id": "aff1001",
                    "label": " 1 ",
                    "orgdiv1": None,
                    "orgdiv2": None,
                    "orgname": None,
                    "original": "Universidade do Sul de Santa Catarina, Tubarão, SC – " "Brazil",
                    "parent": "sub-article",
                    "parent_article_type": "translation",
                    "parent_id": "TRen",
                    "parent_lang": "en",
                    "state": None,
                },
                "expected_value": "original affiliation",
                "got_value": "Universidade do Sul de Santa Catarina, Tubarão, SC – Brazil",
                "item": "institution",
                "message": "Got Universidade do Sul de Santa Catarina, Tubarão, SC – Brazil, "
                           "expected original affiliation",
                "parent": "sub-article",
                "parent_article_type": "translation",
                "parent_id": "TRen",
                "parent_lang": "en",
                "response": "OK",
                "sub_item": '@content-type="original"',
                "title": "Affiliation validation",
                "validation_type": "exist",
            }
        ]
        self.assertEqual(len(obtained), 7)
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(item, obtained[i])

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
                        "article": "<aff id=aff1>",
                        "sub_article": "<aff id=aff1001>"
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
