from unittest import TestCase

from lxml import etree

from packtools.sps.validation.aff import AffiliationValidation


class ArticleAuthorsValidationTest(TestCase):
    def test_affiliations(self):
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

        data = etree.fromstring(xml)
        message = AffiliationValidation(data).validate_affiliation(default_values=['BR'])

        expected_output = {
            'validation': [
                {
                    'title': 'aff/institution element original attribute validation',
                    'xpath': './/aff/institution[@content-type="original"]',
                    'validation_type': 'exist',
                    'response': 'OK',
                    'expected_value': 'original affiliation',
                    'got_value': 'Secretaria Municipal de Saúde de Belo Horizonte. Belo Horizonte, MG, Brasil',
                    'message': 'Got True, expected True',
                    'advice': None

                },
                {
                    'title': 'aff/institution element orgname attribute validation',
                    'xpath': './/aff/institution[@content-type="orgname"]',
                    'validation_type': 'exist',
                    'response': 'OK',
                    'expected_value': 'orgname affiliation',
                    'got_value': 'Secretaria Municipal de Saúde de Belo Horizonte',
                    'message': 'Got True, expected True',
                    'advice': None

                },
                {
                    'title': 'aff element country attribute validation',
                    'xpath': './/aff/country',
                    'validation_type': 'exist',
                    'response': 'OK',
                    'expected_value': 'country affiliation',
                    'got_value': 'Brasil',
                    'message': 'Got True, expected True',
                    'advice': None
                },
                {
                    'title': 'aff element @country attribute validation',
                    'xpath': './/aff/@country',
                    'validation_type': 'value in list',
                    'response': 'OK',
                    'expected_value': ['BR'],
                    'got_value': 'BR',
                    'message': "Got BR, expected ['BR']",
                    'advice': None
                },
                {
                    'title': 'aff/addr-line element state attribute validation',
                    'xpath': './/aff/addr-line/named-content[@content-type="state"]',
                    'validation_type': 'exist',
                    'response': 'OK',
                    'expected_value': 'state affiliation',
                    'got_value': 'MG',
                    'message': 'Got True, expected True',
                    'advice': None
                },
                {
                    'title': 'aff/addr-line element city attribute validation',
                    'xpath': './/aff/addr-line/named-content[@content-type="city"]',
                    'validation_type': 'exist',
                    'response': 'OK',
                    'expected_value': 'city affiliation',
                    'got_value': 'Belo Horizonte',
                    'message': 'Got True, expected True',
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
                    'message': 'Got True, expected True',
                    'advice': None

                },
                {
                    'title': 'aff/institution element orgname attribute validation',
                    'xpath': './/aff/institution[@content-type="orgname"]',
                    'validation_type': 'exist',
                    'response': 'OK',
                    'expected_value': 'orgname affiliation',
                    'got_value': 'Universidade Federal de Minas Gerais',
                    'message': 'Got True, expected True',
                    'advice': None

                },
                {
                    'title': 'aff element country attribute validation',
                    'xpath': './/aff/country',
                    'validation_type': 'exist',
                    'response': 'OK',
                    'expected_value': 'country affiliation',
                    'got_value': 'Brasil',
                    'message': 'Got True, expected True',
                    'advice': None
                },
                {
                    'title': 'aff element @country attribute validation',
                    'xpath': './/aff/@country',
                    'validation_type': 'value in list',
                    'response': 'OK',
                    'expected_value': ['BR'],
                    'got_value': 'BR',
                    'message': "Got BR, expected ['BR']",
                    'advice': None
                },
                {
                    'title': 'aff/addr-line element state attribute validation',
                    'xpath': './/aff/addr-line/named-content[@content-type="state"]',
                    'validation_type': 'exist',
                    'response': 'OK',
                    'expected_value': 'state affiliation',
                    'got_value': 'MG',
                    'message': 'Got True, expected True',
                    'advice': None
                },
                {
                    'title': 'aff/addr-line element city attribute validation',
                    'xpath': './/aff/addr-line/named-content[@content-type="city"]',
                    'validation_type': 'exist',
                    'response': 'OK',
                    'expected_value': 'city affiliation',
                    'got_value': 'Belo Horizonte',
                    'message': 'Got True, expected True',
                    'advice': None
                }
            ]
        }

        self.assertEqual(message, expected_output)

    def test_affiliations_without_original(self):
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

        data = etree.fromstring(xml)
        message = AffiliationValidation(data).validate_affiliation(default_values=['BR'])

        expected_output = {
            'validation': [
                {
                    'title': 'aff/institution element original attribute validation',
                    'xpath': './/aff/institution[@content-type="original"]',
                    'validation_type': 'exist',
                    'response': 'ERROR',
                    'expected_value': 'original affiliation',
                    'got_value': None,
                    'message': 'Got False, expected True',
                    'advice': 'provide the original affiliation'

                },
                {
                    'title': 'aff/institution element orgname attribute validation',
                    'xpath': './/aff/institution[@content-type="orgname"]',
                    'validation_type': 'exist',
                    'response': 'OK',
                    'expected_value': 'orgname affiliation',
                    'got_value': 'Secretaria Municipal de Saúde de Belo Horizonte',
                    'message': 'Got True, expected True',
                    'advice': None

                },
                {
                    'title': 'aff element country attribute validation',
                    'xpath': './/aff/country',
                    'validation_type': 'exist',
                    'response': 'OK',
                    'expected_value': 'country affiliation',
                    'got_value': 'Brasil',
                    'message': 'Got True, expected True',
                    'advice': None
                },
                {
                    'title': 'aff element @country attribute validation',
                    'xpath': './/aff/@country',
                    'validation_type': 'value in list',
                    'response': 'OK',
                    'expected_value': ['BR'],
                    'got_value': 'BR',
                    'message': "Got BR, expected ['BR']",
                    'advice': None
                },
                {
                    'title': 'aff/addr-line element state attribute validation',
                    'xpath': './/aff/addr-line/named-content[@content-type="state"]',
                    'validation_type': 'exist',
                    'response': 'OK',
                    'expected_value': 'state affiliation',
                    'got_value': 'MG',
                    'message': 'Got True, expected True',
                    'advice': None
                },
                {
                    'title': 'aff/addr-line element city attribute validation',
                    'xpath': './/aff/addr-line/named-content[@content-type="city"]',
                    'validation_type': 'exist',
                    'response': 'OK',
                    'expected_value': 'city affiliation',
                    'got_value': 'Belo Horizonte',
                    'message': 'Got True, expected True',
                    'advice': None
                }
            ]
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

        data = etree.fromstring(xml)
        message = AffiliationValidation(data).validate_affiliation(default_values=['BR'])

        expected_output = {
            'validation': [
                {
                    'title': 'aff/institution element original attribute validation',
                    'xpath': './/aff/institution[@content-type="original"]',
                    'validation_type': 'exist',
                    'response': 'OK',
                    'expected_value': 'original affiliation',
                    'got_value': 'Secretaria Municipal de Saúde de Belo Horizonte. Belo Horizonte, MG, Brasil',
                    'message': 'Got True, expected True',
                    'advice': None

                },
                {
                    'title': 'aff/institution element orgname attribute validation',
                    'xpath': './/aff/institution[@content-type="orgname"]',
                    'validation_type': 'exist',
                    'response': 'ERROR',
                    'expected_value': 'orgname affiliation',
                    'got_value': None,
                    'message': 'Got False, expected True',
                    'advice': 'provide the orgname affiliation'

                },
                {
                    'title': 'aff element country attribute validation',
                    'xpath': './/aff/country',
                    'validation_type': 'exist',
                    'response': 'OK',
                    'expected_value': 'country affiliation',
                    'got_value': 'Brasil',
                    'message': 'Got True, expected True',
                    'advice': None
                },
                {
                    'title': 'aff element @country attribute validation',
                    'xpath': './/aff/@country',
                    'validation_type': 'value in list',
                    'response': 'OK',
                    'expected_value': ['BR'],
                    'got_value': 'BR',
                    'message': "Got BR, expected ['BR']",
                    'advice': None
                },
                {
                    'title': 'aff/addr-line element state attribute validation',
                    'xpath': './/aff/addr-line/named-content[@content-type="state"]',
                    'validation_type': 'exist',
                    'response': 'OK',
                    'expected_value': 'state affiliation',
                    'got_value': 'MG',
                    'message': 'Got True, expected True',
                    'advice': None
                },
                {
                    'title': 'aff/addr-line element city attribute validation',
                    'xpath': './/aff/addr-line/named-content[@content-type="city"]',
                    'validation_type': 'exist',
                    'response': 'OK',
                    'expected_value': 'city affiliation',
                    'got_value': 'Belo Horizonte',
                    'message': 'Got True, expected True',
                    'advice': None
                }
            ]
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

        data = etree.fromstring(xml)
        message = AffiliationValidation(data).validate_affiliation(default_values=['BR'])

        expected_output = {
            'validation': [
                {
                    'title': 'aff/institution element original attribute validation',
                    'xpath': './/aff/institution[@content-type="original"]',
                    'validation_type': 'exist',
                    'response': 'OK',
                    'expected_value': 'original affiliation',
                    'got_value': 'Secretaria Municipal de Saúde de Belo Horizonte. Belo Horizonte, MG, Brasil',
                    'message': 'Got True, expected True',
                    'advice': None

                },
                {
                    'title': 'aff/institution element orgname attribute validation',
                    'xpath': './/aff/institution[@content-type="orgname"]',
                    'validation_type': 'exist',
                    'response': 'OK',
                    'expected_value': 'orgname affiliation',
                    'got_value': 'Secretaria Municipal de Saúde de Belo Horizonte',
                    'message': 'Got True, expected True',
                    'advice': None

                },
                {
                    'title': 'aff element country attribute validation',
                    'xpath': './/aff/country',
                    'validation_type': 'exist',
                    'response': 'ERROR',
                    'expected_value': 'country affiliation',
                    'got_value': None,
                    'message': 'Got False, expected True',
                    'advice': 'provide the country affiliation'
                },
                {
                    'title': 'aff element @country attribute validation',
                    'xpath': './/aff/@country',
                    'validation_type': 'value in list',
                    'response': 'ERROR',
                    'expected_value': ['BR'],
                    'got_value': None,
                    'message': "Got None, expected ['BR']",
                    'advice': 'provide a valid @country affiliation'
                },
                {
                    'title': 'aff/addr-line element state attribute validation',
                    'xpath': './/aff/addr-line/named-content[@content-type="state"]',
                    'validation_type': 'exist',
                    'response': 'OK',
                    'expected_value': 'state affiliation',
                    'got_value': 'MG',
                    'message': 'Got True, expected True',
                    'advice': None
                },
                {
                    'title': 'aff/addr-line element city attribute validation',
                    'xpath': './/aff/addr-line/named-content[@content-type="city"]',
                    'validation_type': 'exist',
                    'response': 'OK',
                    'expected_value': 'city affiliation',
                    'got_value': 'Belo Horizonte',
                    'message': 'Got True, expected True',
                    'advice': None
                }
            ]
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

        data = etree.fromstring(xml)
        message = AffiliationValidation(data).validate_affiliation(default_values=['BR'])

        expected_output = {
            'validation': [
                {
                    'title': 'aff/institution element original attribute validation',
                    'xpath': './/aff/institution[@content-type="original"]',
                    'validation_type': 'exist',
                    'response': 'OK',
                    'expected_value': 'original affiliation',
                    'got_value': 'Secretaria Municipal de Saúde de Belo Horizonte. Belo Horizonte, MG, Brasil',
                    'message': 'Got True, expected True',
                    'advice': None

                },
                {
                    'title': 'aff/institution element orgname attribute validation',
                    'xpath': './/aff/institution[@content-type="orgname"]',
                    'validation_type': 'exist',
                    'response': 'OK',
                    'expected_value': 'orgname affiliation',
                    'got_value': 'Secretaria Municipal de Saúde de Belo Horizonte',
                    'message': 'Got True, expected True',
                    'advice': None

                },
                {
                    'title': 'aff element country attribute validation',
                    'xpath': './/aff/country',
                    'validation_type': 'exist',
                    'response': 'OK',
                    'expected_value': 'country affiliation',
                    'got_value': 'Brasil',
                    'message': 'Got True, expected True',
                    'advice': None
                },
                {
                    'title': 'aff element @country attribute validation',
                    'xpath': './/aff/@country',
                    'validation_type': 'value in list',
                    'response': 'ERROR',
                    'expected_value': ['BR'],
                    'got_value': None,
                    'message': "Got None, expected ['BR']",
                    'advice': 'provide a valid @country affiliation'
                },
                {
                    'title': 'aff/addr-line element state attribute validation',
                    'xpath': './/aff/addr-line/named-content[@content-type="state"]',
                    'validation_type': 'exist',
                    'response': 'OK',
                    'expected_value': 'state affiliation',
                    'got_value': 'MG',
                    'message': 'Got True, expected True',
                    'advice': None
                },
                {
                    'title': 'aff/addr-line element city attribute validation',
                    'xpath': './/aff/addr-line/named-content[@content-type="city"]',
                    'validation_type': 'exist',
                    'response': 'OK',
                    'expected_value': 'city affiliation',
                    'got_value': 'Belo Horizonte',
                    'message': 'Got True, expected True',
                    'advice': None
                }
            ]
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

        data = etree.fromstring(xml)
        message = AffiliationValidation(data).validate_affiliation(default_values=['BR'])

        expected_output = {
            'validation': [
                {
                    'title': 'aff/institution element original attribute validation',
                    'xpath': './/aff/institution[@content-type="original"]',
                    'validation_type': 'exist',
                    'response': 'OK',
                    'expected_value': 'original affiliation',
                    'got_value': 'Secretaria Municipal de Saúde de Belo Horizonte. Belo Horizonte, MG, Brasil',
                    'message': 'Got True, expected True',
                    'advice': None

                },
                {
                    'title': 'aff/institution element orgname attribute validation',
                    'xpath': './/aff/institution[@content-type="orgname"]',
                    'validation_type': 'exist',
                    'response': 'OK',
                    'expected_value': 'orgname affiliation',
                    'got_value': 'Secretaria Municipal de Saúde de Belo Horizonte',
                    'message': 'Got True, expected True',
                    'advice': None

                },
                {
                    'title': 'aff element country attribute validation',
                    'xpath': './/aff/country',
                    'validation_type': 'exist',
                    'response': 'OK',
                    'expected_value': 'country affiliation',
                    'got_value': 'Brasil',
                    'message': 'Got True, expected True',
                    'advice': None
                },
                {
                    'title': 'aff element @country attribute validation',
                    'xpath': './/aff/@country',
                    'validation_type': 'value in list',
                    'response': 'OK',
                    'expected_value': ['BR'],
                    'got_value': 'BR',
                    'message': "Got BR, expected ['BR']",
                    'advice': None
                },
                {
                    'title': 'aff/addr-line element state attribute validation',
                    'xpath': './/aff/addr-line/named-content[@content-type="state"]',
                    'validation_type': 'exist',
                    'response': 'ERROR',
                    'expected_value': 'state affiliation',
                    'got_value': None,
                    'message': 'Got False, expected True',
                    'advice': 'provide the state affiliation'
                },
                {
                    'title': 'aff/addr-line element city attribute validation',
                    'xpath': './/aff/addr-line/named-content[@content-type="city"]',
                    'validation_type': 'exist',
                    'response': 'OK',
                    'expected_value': 'city affiliation',
                    'got_value': 'Belo Horizonte',
                    'message': 'Got True, expected True',
                    'advice': None
                }
            ]
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

        data = etree.fromstring(xml)
        message = AffiliationValidation(data).validate_affiliation(default_values=['BR'])

        expected_output = {
            'validation': [
                {
                    'title': 'aff/institution element original attribute validation',
                    'xpath': './/aff/institution[@content-type="original"]',
                    'validation_type': 'exist',
                    'response': 'OK',
                    'expected_value': 'original affiliation',
                    'got_value': 'Secretaria Municipal de Saúde de Belo Horizonte. Belo Horizonte, MG, Brasil',
                    'message': 'Got True, expected True',
                    'advice': None

                },
                {
                    'title': 'aff/institution element orgname attribute validation',
                    'xpath': './/aff/institution[@content-type="orgname"]',
                    'validation_type': 'exist',
                    'response': 'OK',
                    'expected_value': 'orgname affiliation',
                    'got_value': 'Secretaria Municipal de Saúde de Belo Horizonte',
                    'message': 'Got True, expected True',
                    'advice': None

                },
                {
                    'title': 'aff element country attribute validation',
                    'xpath': './/aff/country',
                    'validation_type': 'exist',
                    'response': 'OK',
                    'expected_value': 'country affiliation',
                    'got_value': 'Brasil',
                    'message': 'Got True, expected True',
                    'advice': None
                },
                {
                    'title': 'aff element @country attribute validation',
                    'xpath': './/aff/@country',
                    'validation_type': 'value in list',
                    'response': 'OK',
                    'expected_value': ['BR'],
                    'got_value': 'BR',
                    'message': "Got BR, expected ['BR']",
                    'advice': None
                },
                {
                    'title': 'aff/addr-line element state attribute validation',
                    'xpath': './/aff/addr-line/named-content[@content-type="state"]',
                    'validation_type': 'exist',
                    'response': 'OK',
                    'expected_value': 'state affiliation',
                    'got_value': 'MG',
                    'message': 'Got True, expected True',
                    'advice': None
                },
                {
                    'title': 'aff/addr-line element city attribute validation',
                    'xpath': './/aff/addr-line/named-content[@content-type="city"]',
                    'validation_type': 'exist',
                    'response': 'ERROR',
                    'expected_value': 'city affiliation',
                    'got_value': None,
                    'message': 'Got False, expected True',
                    'advice': 'provide the city affiliation'
                }
            ]
        }

        self.assertEqual(message, expected_output)


    # def test_affiliations(self):
    #     xml = ("""
    #     <article>
    #         <front>
    #             <article-meta>
    #                 <aff id="aff1">
    #                     <label>I</label>
    #                     <institution content-type="orgname">Secretaria Municipal de Saúde de Belo Horizonte</institution>
    #                     <addr-line>
    #                         <named-content content-type="city">Belo Horizonte</named-content>
    #                         <named-content content-type="state">MG</named-content>
    #                     </addr-line>
    #                     <country>Brasil</country>
    #                     <institution content-type="original">Secretaria Municipal de Saúde de Belo Horizonte. Belo Horizonte, MG, Brasil</institution>
    #                 </aff>
    #                 <aff id="aff2">
    #                     <label>II</label>
    #                     <institution content-type="orgdiv1">Faculdade de Medicina</institution>
    #                     <institution content-type="orgname">Universidade Federal de Minas Gerais</institution>
    #                     <addr-line>
    #                         <named-content content-type="city">Belo Horizonte</named-content>
    #                         <named-content content-type="state">MG</named-content>
    #                     </addr-line>
    #                     <country>Brasil</country>
    #                     <institution content-type="original">Grupo de Pesquisas em Epidemiologia e Avaliação em Saúde. Faculdade de Medicina. Universidade Federal de Minas Gerais. Belo Horizonte, MG, Brasil</institution>
    #                 </aff>
    #             </article-meta>
    #             <front-stub>
    #             <aff id="aff3">
    #                 <label>III</label>
    #                 <institution content-type="orgdiv2">Departamento de Ciências Sociais</institution>
    #                 <institution content-type="orgdiv1">Escola Nacional de Saúde Pública Sergio Arouca</institution>
    #                 <institution content-type="orgname">Fundação Oswaldo Cruz</institution>
    #                 <addr-line>
    #                     <named-content content-type="city">Rio de Janeiro</named-content>
    #                     <named-content content-type="state">RJ</named-content>
    #                 </addr-line>
    #                 <country>Brasil</country>
    #                 <institution content-type="original">Departamento de Ciências Sociais. Escola Nacional de Saúde Pública Sergio Arouca. Fundação Oswaldo Cruz. Rio de Janeiro, RJ, Brasil</institution>
    #             </aff>
    #         </front-stub>
    #         </front>
    #     </article>
    #     """)
    #     data = etree.fromstring(xml)
    #     message = AffiliationValidation(data).validate_affiliation
    #
    #     expected_output = [
    #         {
    #             'result': 'success',
    #             'message': 'The affiliation of id: aff1 is ok!'
    #         },
    #         {
    #             'result': 'success',
    #             'message': 'The affiliation of id: aff2 is ok!'
    #         },
    #         {
    #             'result': 'success',
    #             'message': 'The affiliation of id: aff3 is ok!'
    #         }
    #     ]
    #
    #     self.assertEqual(message, expected_output)