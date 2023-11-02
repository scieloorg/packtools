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
        xml = ("""
        <article>
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
        """)

        xml_tree = etree.fromstring(xml)
        message = AffiliationsListValidation(xml_tree, ['BR']).validade_affiliations_list()

        expected_output = [
                {
                    'title': 'aff/institution element original attribute validation',
                    'xpath': './/aff/institution[@content-type="original"]',
                    'validation_type': 'exist',
                    'response': 'OK',
                    'expected_value': 'original affiliation',
                    'got_value': 'Secretaria Municipal de Saúde de Belo Horizonte. Belo Horizonte, MG, Brasil',
                    'message': 'Got Secretaria Municipal de Saúde de Belo Horizonte. Belo Horizonte, MG, Brasil, expected original affiliation',
                    'advice': None

                },
                {
                    'title': 'aff/institution element orgname attribute validation',
                    'xpath': './/aff/institution[@content-type="orgname"]',
                    'validation_type': 'exist',
                    'response': 'OK',
                    'expected_value': 'orgname affiliation',
                    'got_value': 'Secretaria Municipal de Saúde de Belo Horizonte',
                    'message': 'Got Secretaria Municipal de Saúde de Belo Horizonte, expected orgname affiliation',
                    'advice': None

                },
                {
                    'title': 'aff element country attribute validation',
                    'xpath': './/aff/country',
                    'validation_type': 'exist',
                    'response': 'OK',
                    'expected_value': 'country affiliation',
                    'got_value': 'Brasil',
                    'message': 'Got Brasil, expected country affiliation',
                    'advice': None
                },
                {
                    'title': 'aff element @country attribute validation',
                    'xpath': './/aff/@country',
                    'validation_type': 'value in list',
                    'response': 'OK',
                    'expected_value': ['BR'],
                    'got_value': 'BR',
                    'message': "Got BR, expected one item of this list: ['BR']",
                    'advice': None
                },
                {
                    'title': 'aff/addr-line element state attribute validation',
                    'xpath': './/aff/addr-line/named-content[@content-type="state"]',
                    'validation_type': 'exist',
                    'response': 'OK',
                    'expected_value': 'state affiliation',
                    'got_value': 'MG',
                    'message': 'Got MG, expected state affiliation',
                    'advice': None
                },
                {
                    'title': 'aff/addr-line element city attribute validation',
                    'xpath': './/aff/addr-line/named-content[@content-type="city"]',
                    'validation_type': 'exist',
                    'response': 'OK',
                    'expected_value': 'city affiliation',
                    'got_value': 'Belo Horizonte',
                    'message': 'Got Belo Horizonte, expected city affiliation',
                    'advice': None
                },
                {
                    'title': 'aff/institution element original attribute validation',
                    'xpath': './/aff/institution[@content-type="original"]',
                    'validation_type': 'exist',
                    'response': 'OK',
                    'expected_value': 'original affiliation',
                    'got_value': 'Grupo de Pesquisas em Epidemiologia e Avaliação em Saúde. Faculdade de Medicina. '
                                 'Universidade Federal de Minas Gerais. Belo Horizonte, MG, Brasil',
                    'message': 'Got Grupo de Pesquisas em Epidemiologia e Avaliação em Saúde. Faculdade de Medicina. '
                                 'Universidade Federal de Minas Gerais. Belo Horizonte, MG, Brasil, expected original affiliation',
                    'advice': None

                },
                {
                    'title': 'aff/institution element orgname attribute validation',
                    'xpath': './/aff/institution[@content-type="orgname"]',
                    'validation_type': 'exist',
                    'response': 'OK',
                    'expected_value': 'orgname affiliation',
                    'got_value': 'Universidade Federal de Minas Gerais',
                    'message': 'Got Universidade Federal de Minas Gerais, expected orgname affiliation',
                    'advice': None

                },
                {
                    'title': 'aff element country attribute validation',
                    'xpath': './/aff/country',
                    'validation_type': 'exist',
                    'response': 'OK',
                    'expected_value': 'country affiliation',
                    'got_value': 'Brasil',
                    'message': 'Got Brasil, expected country affiliation',
                    'advice': None
                },
                {
                    'title': 'aff element @country attribute validation',
                    'xpath': './/aff/@country',
                    'validation_type': 'value in list',
                    'response': 'OK',
                    'expected_value': ['BR'],
                    'got_value': 'BR',
                    'message': "Got BR, expected one item of this list: ['BR']",
                    'advice': None
                },
                {
                    'title': 'aff/addr-line element state attribute validation',
                    'xpath': './/aff/addr-line/named-content[@content-type="state"]',
                    'validation_type': 'exist',
                    'response': 'OK',
                    'expected_value': 'state affiliation',
                    'got_value': 'MG',
                    'message': 'Got MG, expected state affiliation',
                    'advice': None
                },
                {
                    'title': 'aff/addr-line element city attribute validation',
                    'xpath': './/aff/addr-line/named-content[@content-type="city"]',
                    'validation_type': 'exist',
                    'response': 'OK',
                    'expected_value': 'city affiliation',
                    'got_value': 'Belo Horizonte',
                    'message': 'Got Belo Horizonte, expected city affiliation',
                    'advice': None
                }
            ]

        self.assertEqual(message, expected_output)

    def test_affiliation_without_original(self):
        self.maxDiff = None
        xml = ("""
        <article>
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
        """)

        xml_tree = etree.fromstring(xml)
        affiliations_list = Affiliation(xml_tree).affiliation_list
        message = AffiliationValidation(affiliations_list[0]).validate_original()

        expected_output = {
                    'title': 'aff/institution element original attribute validation',
                    'xpath': './/aff/institution[@content-type="original"]',
                    'validation_type': 'exist',
                    'response': 'ERROR',
                    'expected_value': 'original affiliation',
                    'got_value': None,
                    'message': 'Got None, expected original affiliation',
                    'advice': 'provide the original affiliation'
        }

        self.assertEqual(message, expected_output)

    def test_affiliations_without_orgname(self):
        self.maxDiff = None
        xml = ("""
        <article>
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
        """)

        xml_tree = etree.fromstring(xml)
        affiliations_list = Affiliation(xml_tree).affiliation_list
        message = AffiliationValidation(affiliations_list[0]).validate_orgname()

        expected_output = {
                    'title': 'aff/institution element orgname attribute validation',
                    'xpath': './/aff/institution[@content-type="orgname"]',
                    'validation_type': 'exist',
                    'response': 'ERROR',
                    'expected_value': 'orgname affiliation',
                    'got_value': None,
                    'message': 'Got None, expected orgname affiliation',
                    'advice': 'provide the orgname affiliation'
                }

        self.assertEqual(message, expected_output)

    def test_affiliations_without_country(self):
        self.maxDiff = None
        xml = ("""
        <article>
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
        """)

        xml_tree = etree.fromstring(xml)
        affiliations_list = Affiliation(xml_tree).affiliation_list
        message = AffiliationValidation(affiliations_list[0]).validate_country()

        expected_output = {
                    'title': 'aff element country attribute validation',
                    'xpath': './/aff/country',
                    'validation_type': 'exist',
                    'response': 'ERROR',
                    'expected_value': 'country affiliation',
                    'got_value': None,
                    'message': 'Got None, expected country affiliation',
                    'advice': 'provide the country affiliation'
                }

        self.assertEqual(message, expected_output)

    def test_affiliations_without_country_code(self):
        self.maxDiff = None
        xml = ("""
        <article>
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
        """)

        xml_tree = etree.fromstring(xml)
        affiliations_list = Affiliation(xml_tree).affiliation_list
        message = AffiliationValidation(affiliations_list[0], ['BR']).validate_country_code()

        expected_output = {
                    'title': 'aff element @country attribute validation',
                    'xpath': './/aff/@country',
                    'validation_type': 'value in list',
                    'response': 'ERROR',
                    'expected_value': ['BR'],
                    'got_value': None,
                    'message': "Got None, expected one item of this list: ['BR']",
                    'advice': 'provide a valid @country affiliation'
                }

        self.assertEqual(message, expected_output)

    def test_affiliations_without_state(self):
        self.maxDiff = None
        xml = ("""
        <article>
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
        """)

        xml_tree = etree.fromstring(xml)
        affiliations_list = Affiliation(xml_tree).affiliation_list
        message = AffiliationValidation(affiliations_list[0]).validate_state()

        expected_output = {
                    'title': 'aff/addr-line element state attribute validation',
                    'xpath': './/aff/addr-line/named-content[@content-type="state"]',
                    'validation_type': 'exist',
                    'response': 'ERROR',
                    'expected_value': 'state affiliation',
                    'got_value': None,
                    'message': 'Got None, expected state affiliation',
                    'advice': 'provide the state affiliation'
                }

        self.assertEqual(message, expected_output)

    def test_affiliations_without_city(self):
        self.maxDiff = None
        xml = ("""
        <article>
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
        """)

        xml_tree = etree.fromstring(xml)
        affiliations_list = Affiliation(xml_tree).affiliation_list
        message = AffiliationValidation(affiliations_list[0]).validate_city()

        expected_output = {
                    'title': 'aff/addr-line element city attribute validation',
                    'xpath': './/aff/addr-line/named-content[@content-type="city"]',
                    'validation_type': 'exist',
                    'response': 'ERROR',
                    'expected_value': 'city affiliation',
                    'got_value': None,
                    'message': 'Got None, expected city affiliation',
                    'advice': 'provide the city affiliation'
                }

        self.assertEqual(message, expected_output)

    def test_validate(self):
        self.maxDiff = None
        xml = ("""
        <article>
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
        """)

        xml_tree = etree.fromstring(xml)
        data = {
            'country_codes_list':  ['BR']
        }
        message = AffiliationsListValidation(xml_tree).validate(data)

        expected_output = {
            'affiliations_validation': [
                {
                    'title': 'aff/institution element original attribute validation',
                    'xpath': './/aff/institution[@content-type="original"]',
                    'validation_type': 'exist',
                    'response': 'OK',
                    'expected_value': 'original affiliation',
                    'got_value': 'Secretaria Municipal de Saúde de Belo Horizonte. Belo Horizonte, MG, Brasil',
                    'message': 'Got Secretaria Municipal de Saúde de Belo Horizonte. Belo Horizonte, MG, Brasil, expected original affiliation',
                    'advice': None

                },
                {
                    'title': 'aff/institution element orgname attribute validation',
                    'xpath': './/aff/institution[@content-type="orgname"]',
                    'validation_type': 'exist',
                    'response': 'OK',
                    'expected_value': 'orgname affiliation',
                    'got_value': 'Secretaria Municipal de Saúde de Belo Horizonte',
                    'message': 'Got Secretaria Municipal de Saúde de Belo Horizonte, expected orgname affiliation',
                    'advice': None

                },
                {
                    'title': 'aff element country attribute validation',
                    'xpath': './/aff/country',
                    'validation_type': 'exist',
                    'response': 'OK',
                    'expected_value': 'country affiliation',
                    'got_value': 'Brasil',
                    'message': 'Got Brasil, expected country affiliation',
                    'advice': None
                },
                {
                    'title': 'aff element @country attribute validation',
                    'xpath': './/aff/@country',
                    'validation_type': 'value in list',
                    'response': 'OK',
                    'expected_value': ['BR'],
                    'got_value': 'BR',
                    'message': "Got BR, expected one item of this list: ['BR']",
                    'advice': None
                },
                {
                    'title': 'aff/addr-line element state attribute validation',
                    'xpath': './/aff/addr-line/named-content[@content-type="state"]',
                    'validation_type': 'exist',
                    'response': 'OK',
                    'expected_value': 'state affiliation',
                    'got_value': 'MG',
                    'message': 'Got MG, expected state affiliation',
                    'advice': None
                },
                {
                    'title': 'aff/addr-line element city attribute validation',
                    'xpath': './/aff/addr-line/named-content[@content-type="city"]',
                    'validation_type': 'exist',
                    'response': 'OK',
                    'expected_value': 'city affiliation',
                    'got_value': 'Belo Horizonte',
                    'message': 'Got Belo Horizonte, expected city affiliation',
                    'advice': None
                },
                {
                    'title': 'aff/institution element original attribute validation',
                    'xpath': './/aff/institution[@content-type="original"]',
                    'validation_type': 'exist',
                    'response': 'OK',
                    'expected_value': 'original affiliation',
                    'got_value': 'Grupo de Pesquisas em Epidemiologia e Avaliação em Saúde. Faculdade de Medicina. '
                                 'Universidade Federal de Minas Gerais. Belo Horizonte, MG, Brasil',
                    'message': 'Got Grupo de Pesquisas em Epidemiologia e Avaliação em Saúde. Faculdade de Medicina. '
                                 'Universidade Federal de Minas Gerais. Belo Horizonte, MG, Brasil, expected original affiliation',
                    'advice': None

                },
                {
                    'title': 'aff/institution element orgname attribute validation',
                    'xpath': './/aff/institution[@content-type="orgname"]',
                    'validation_type': 'exist',
                    'response': 'OK',
                    'expected_value': 'orgname affiliation',
                    'got_value': 'Universidade Federal de Minas Gerais',
                    'message': 'Got Universidade Federal de Minas Gerais, expected orgname affiliation',
                    'advice': None

                },
                {
                    'title': 'aff element country attribute validation',
                    'xpath': './/aff/country',
                    'validation_type': 'exist',
                    'response': 'OK',
                    'expected_value': 'country affiliation',
                    'got_value': 'Brasil',
                    'message': 'Got Brasil, expected country affiliation',
                    'advice': None
                },
                {
                    'title': 'aff element @country attribute validation',
                    'xpath': './/aff/@country',
                    'validation_type': 'value in list',
                    'response': 'OK',
                    'expected_value': ['BR'],
                    'got_value': 'BR',
                    'message': "Got BR, expected one item of this list: ['BR']",
                    'advice': None
                },
                {
                    'title': 'aff/addr-line element state attribute validation',
                    'xpath': './/aff/addr-line/named-content[@content-type="state"]',
                    'validation_type': 'exist',
                    'response': 'OK',
                    'expected_value': 'state affiliation',
                    'got_value': 'MG',
                    'message': 'Got MG, expected state affiliation',
                    'advice': None
                },
                {
                    'title': 'aff/addr-line element city attribute validation',
                    'xpath': './/aff/addr-line/named-content[@content-type="city"]',
                    'validation_type': 'exist',
                    'response': 'OK',
                    'expected_value': 'city affiliation',
                    'got_value': 'Belo Horizonte',
                    'message': 'Got Belo Horizonte, expected city affiliation',
                    'advice': None
                }
            ]
        }

        self.assertEqual(message, expected_output)
