from unittest import TestCase

from lxml import etree

from packtools.sps.models.aff import Affiliation
from packtools.sps.validation.aff import (
    AffiliationValidation,
    AffiliationsListValidation,
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
                "expected_value": "city affiliation",
                "got_value": None,
                "message": "Got None, expected city affiliation",
                "advice": "provide the city affiliation",
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
