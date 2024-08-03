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
        xml_tree = xml_utils.get_xml_tree("tests/samples/1518-8787-rsp-56-79.xml")
        data = {"country_codes_list": ["BR"]}
        obtained = list(AffiliationsListValidation(xml_tree).validate(data))
        expected = [
            {
                "title": "Affiliation validation",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "research-article",
                "parent_lang": "en",
                "item": "institution",
                "sub_item": '@content-type="original"',
                "validation_type": "exist",
                "response": "OK",
                "expected_value": "original affiliation",
                "got_value": " Universidade Federal de Pelotas. Faculdade de\n"
                "\t\t\t\t\tMedicina. Programa de Pós-Graduação em Epidemiologia. "
                "Pelotas, RS,\n"
                "\t\t\t\t\tBrasil",
                "message": "Got  Universidade Federal de Pelotas. Faculdade de\n"
                "\t\t\t\t\tMedicina. Programa de Pós-Graduação em Epidemiologia. "
                "Pelotas, RS,\n"
                "\t\t\t\t\tBrasil, expected original affiliation",
                "advice": None,
                "data": {
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
                    "\t\t\t\t\tMedicina. Programa de Pós-Graduação em "
                    "Epidemiologia. Pelotas, RS,\n"
                    "\t\t\t\t\tBrasil",
                    "parent": "article",
                    "parent_article_type": "research-article",
                    "parent_id": None,
                    "parent_lang": "en",
                    "state": "RS",
                },
            },
            {
                "title": "Affiliation validation",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "research-article",
                "parent_lang": "en",
                "item": "institution",
                "sub_item": '@content-type="orgname"',
                "validation_type": "exist",
                "response": "OK",
                "expected_value": "orgname affiliation",
                "got_value": "Universidade Federal de Pelotas",
                "message": "Got Universidade Federal de Pelotas, expected orgname affiliation",
                "advice": None,
                "data": {
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
                    "\t\t\t\t\tMedicina. Programa de Pós-Graduação em "
                    "Epidemiologia. Pelotas, RS,\n"
                    "\t\t\t\t\tBrasil",
                    "parent": "article",
                    "parent_article_type": "research-article",
                    "parent_id": None,
                    "parent_lang": "en",
                    "state": "RS",
                },
            },
            {
                "title": "Affiliation validation",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "research-article",
                "parent_lang": "en",
                "item": "aff",
                "sub_item": "country",
                "validation_type": "exist",
                "response": "OK",
                "expected_value": "country affiliation",
                "got_value": "Brasil",
                "message": "Got Brasil, expected country affiliation",
                "advice": None,
                "data": {
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
                    "\t\t\t\t\tMedicina. Programa de Pós-Graduação em "
                    "Epidemiologia. Pelotas, RS,\n"
                    "\t\t\t\t\tBrasil",
                    "parent": "article",
                    "parent_article_type": "research-article",
                    "parent_id": None,
                    "parent_lang": "en",
                    "state": "RS",
                },
            },
            {
                "title": "Affiliation validation",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "research-article",
                "parent_lang": "en",
                "item": "country",
                "sub_item": "@country",
                "validation_type": "value in list",
                "response": "OK",
                "expected_value": ["BR"],
                "got_value": "BR",
                "message": "Got BR, expected ['BR']",
                "advice": None,
                "data": {
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
                    "\t\t\t\t\tMedicina. Programa de Pós-Graduação em "
                    "Epidemiologia. Pelotas, RS,\n"
                    "\t\t\t\t\tBrasil",
                    "parent": "article",
                    "parent_article_type": "research-article",
                    "parent_id": None,
                    "parent_lang": "en",
                    "state": "RS",
                },
            },
            {
                "title": "Affiliation validation",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "research-article",
                "parent_lang": "en",
                "item": "addr-line",
                "sub_item": "state",
                "validation_type": "exist",
                "response": "OK",
                "expected_value": "state affiliation",
                "got_value": "RS",
                "message": "Got RS, expected state affiliation",
                "advice": None,
                "data": {
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
                    "\t\t\t\t\tMedicina. Programa de Pós-Graduação em "
                    "Epidemiologia. Pelotas, RS,\n"
                    "\t\t\t\t\tBrasil",
                    "parent": "article",
                    "parent_article_type": "research-article",
                    "parent_id": None,
                    "parent_lang": "en",
                    "state": "RS",
                },
            },
            {
                "title": "Affiliation validation",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "research-article",
                "parent_lang": "en",
                "item": "addr-line",
                "sub_item": "city",
                "validation_type": "exist",
                "response": "OK",
                "expected_value": "city affiliation",
                "got_value": "Pelotas",
                "message": "Got Pelotas, expected city affiliation",
                "advice": None,
                "data": {
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
                    "\t\t\t\t\tMedicina. Programa de Pós-Graduação em "
                    "Epidemiologia. Pelotas, RS,\n"
                    "\t\t\t\t\tBrasil",
                    "parent": "article",
                    "parent_article_type": "research-article",
                    "parent_id": None,
                    "parent_lang": "en",
                    "state": "RS",
                },
            },
            {
                "title": "Affiliation validation",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "research-article",
                "parent_lang": "en",
                "item": "institution",
                "sub_item": '@content-type="original"',
                "validation_type": "exist",
                "response": "OK",
                "expected_value": "original affiliation",
                "got_value": " Universidade Federal de Pelotas. Escola\n"
                "\t\t\t\t\tSuperior de Educação Física. Programa de "
                "Pós-Graduação em Educação Física.\n"
                "\t\t\t\t\tPelotas, RS, Brasil",
                "message": "Got  Universidade Federal de Pelotas. Escola\n"
                "\t\t\t\t\tSuperior de Educação Física. Programa de Pós-Graduação "
                "em Educação Física.\n"
                "\t\t\t\t\tPelotas, RS, Brasil, expected original affiliation",
                "advice": None,
                "data": {
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
                    "\t\t\t\t\tSuperior de Educação Física. Programa de "
                    "Pós-Graduação em Educação Física.\n"
                    "\t\t\t\t\tPelotas, RS, Brasil",
                    "parent": "article",
                    "parent_article_type": "research-article",
                    "parent_id": None,
                    "parent_lang": "en",
                    "state": "RS",
                },
            },
            {
                "title": "Affiliation validation",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "research-article",
                "parent_lang": "en",
                "item": "institution",
                "sub_item": '@content-type="orgname"',
                "validation_type": "exist",
                "response": "OK",
                "expected_value": "orgname affiliation",
                "got_value": "Universidade Federal de Pelotas",
                "message": "Got Universidade Federal de Pelotas, expected orgname affiliation",
                "advice": None,
                "data": {
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
                    "\t\t\t\t\tSuperior de Educação Física. Programa de "
                    "Pós-Graduação em Educação Física.\n"
                    "\t\t\t\t\tPelotas, RS, Brasil",
                    "parent": "article",
                    "parent_article_type": "research-article",
                    "parent_id": None,
                    "parent_lang": "en",
                    "state": "RS",
                },
            },
            {
                "title": "Affiliation validation",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "research-article",
                "parent_lang": "en",
                "item": "aff",
                "sub_item": "country",
                "validation_type": "exist",
                "response": "OK",
                "expected_value": "country affiliation",
                "got_value": "Brasil",
                "message": "Got Brasil, expected country affiliation",
                "advice": None,
                "data": {
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
                    "\t\t\t\t\tSuperior de Educação Física. Programa de "
                    "Pós-Graduação em Educação Física.\n"
                    "\t\t\t\t\tPelotas, RS, Brasil",
                    "parent": "article",
                    "parent_article_type": "research-article",
                    "parent_id": None,
                    "parent_lang": "en",
                    "state": "RS",
                },
            },
            {
                "title": "Affiliation validation",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "research-article",
                "parent_lang": "en",
                "item": "country",
                "sub_item": "@country",
                "validation_type": "value in list",
                "response": "OK",
                "expected_value": ["BR"],
                "got_value": "BR",
                "message": "Got BR, expected ['BR']",
                "advice": None,
                "data": {
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
                    "\t\t\t\t\tSuperior de Educação Física. Programa de "
                    "Pós-Graduação em Educação Física.\n"
                    "\t\t\t\t\tPelotas, RS, Brasil",
                    "parent": "article",
                    "parent_article_type": "research-article",
                    "parent_id": None,
                    "parent_lang": "en",
                    "state": "RS",
                },
            },
            {
                "title": "Affiliation validation",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "research-article",
                "parent_lang": "en",
                "item": "addr-line",
                "sub_item": "state",
                "validation_type": "exist",
                "response": "OK",
                "expected_value": "state affiliation",
                "got_value": "RS",
                "message": "Got RS, expected state affiliation",
                "advice": None,
                "data": {
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
                    "\t\t\t\t\tSuperior de Educação Física. Programa de "
                    "Pós-Graduação em Educação Física.\n"
                    "\t\t\t\t\tPelotas, RS, Brasil",
                    "parent": "article",
                    "parent_article_type": "research-article",
                    "parent_id": None,
                    "parent_lang": "en",
                    "state": "RS",
                },
            },
            {
                "title": "Affiliation validation",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "research-article",
                "parent_lang": "en",
                "item": "addr-line",
                "sub_item": "city",
                "validation_type": "exist",
                "response": "OK",
                "expected_value": "city affiliation",
                "got_value": "Pelotas",
                "message": "Got Pelotas, expected city affiliation",
                "advice": None,
                "data": {
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
                    "\t\t\t\t\tSuperior de Educação Física. Programa de "
                    "Pós-Graduação em Educação Física.\n"
                    "\t\t\t\t\tPelotas, RS, Brasil",
                    "parent": "article",
                    "parent_article_type": "research-article",
                    "parent_id": None,
                    "parent_lang": "en",
                    "state": "RS",
                },
            },
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
                "got_value": "Universidade Federal de Pelotas. Faculdade de\n"
                "\t\t\t\t\tMedicina. Programa de Pós-Graduação em Epidemiologia. "
                "Pelotas, RS,\n"
                "\t\t\t\t\tBrasil",
                "message": "Got Universidade Federal de Pelotas. Faculdade de\n"
                "\t\t\t\t\tMedicina. Programa de Pós-Graduação em Epidemiologia. "
                "Pelotas, RS,\n"
                "\t\t\t\t\tBrasil, expected original affiliation",
                "advice": None,
                "data": {
                    "id": "aff1002",
                    "label": "I",
                    "original": "Universidade Federal de Pelotas. Faculdade de\n"
                    "\t\t\t\t\tMedicina. Programa de Pós-Graduação em "
                    "Epidemiologia. Pelotas, RS,\n"
                    "\t\t\t\t\tBrasil",
                    "parent": "sub-article",
                    "parent_article_type": "translation",
                    "parent_id": "TRpt",
                    "parent_lang": "pt",
                },
            },
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
                "got_value": "Universidade Federal de Pelotas. Escola\n"
                "\t\t\t\t\tSuperior de Educação Física. Programa de "
                "Pós-Graduação em Educação Física.\n"
                "\t\t\t\t\tPelotas, RS, Brasil",
                "message": "Got Universidade Federal de Pelotas. Escola\n"
                "\t\t\t\t\tSuperior de Educação Física. Programa de Pós-Graduação "
                "em Educação Física.\n"
                "\t\t\t\t\tPelotas, RS, Brasil, expected original affiliation",
                "advice": None,
                "data": {
                    "id": "aff2002",
                    "label": "II",
                    "original": "Universidade Federal de Pelotas. Escola\n"
                    "\t\t\t\t\tSuperior de Educação Física. Programa de "
                    "Pós-Graduação em Educação Física.\n"
                    "\t\t\t\t\tPelotas, RS, Brasil",
                    "parent": "sub-article",
                    "parent_article_type": "translation",
                    "parent_id": "TRpt",
                    "parent_lang": "pt",
                },
            },
        ]

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
                "data": {"article_count": 2, "sub_article_count": 2},
            }
        ]
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(item, obtained[i])
