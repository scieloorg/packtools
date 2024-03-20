from unittest import TestCase

from lxml import etree

from packtools.sps.utils import xml_utils

from packtools.sps.validation.article_authors import ArticleAuthorsValidation

credit_taxonomy_terms_and_urls = [
    {
        "term": "Conceptualization",
        "uri": "https://credit.niso.org/contributor-roles/conceptualization/",
    },
    {
        "term": "Data curation",
        "uri": "https://credit.niso.org/contributor-roles/data-curation/",
    }
]


def callable_get_data(orcid):
    tests = {
        '0990-0001-0058-4853': 'FRANCISCO VENEGAS-MARTÍNEZ',
        '0000-3333-1238-6873': 'Vanessa M. Higa'
    }
    return tests.get(orcid)


def callable_get_data_empty(orcid):
    tests = {
        '0990-0001-0058-4853': None,
        '0000-3333-1238-6873': None
    }
    return tests.get(orcid)


class ArticleAuthorsValidationTest(TestCase):
    def test_without_role(self):
        self.maxDiff = None
        xml = """
        <article>
            <front>
                <article-meta>
                    <contrib-group>
                        <contrib contrib-type="author">
                            <name>
                                <surname>VENEGAS-MARTÍNEZ</surname>
                                <given-names>FRANCISCO</given-names>
                                <prefix>Prof</prefix>
                                <suffix>Nieto</suffix>
                            </name>
                            <xref ref-type="aff" rid="aff1"/>
                            </contrib>
                            <contrib contrib-type="author">
                            <contrib-id contrib-id-type="orcid">0000-0001-5518-4853</contrib-id>
                            <name>
                                <surname>Higa</surname>
                                <given-names>Vanessa M.</given-names>
                            </name>
                            <xref ref-type="aff" rid="aff1">a</xref>
                        </contrib>
                    </contrib-group>
                </article-meta>
            </front>
        </article>
        """

        data = etree.fromstring(xml)
        messages = ArticleAuthorsValidation(xmltree=data).validate_authors_role(
            credit_taxonomy_terms_and_urls=credit_taxonomy_terms_and_urls
        )

        expected_output = [
            {
                'title': 'CRediT taxonomy for contribs',
                'xpath': './contrib-group//contrib//role[@content-type="https://credit.niso.org/contributor-roles/*"]',
                'validation_type': 'value in list',
                'response': 'ERROR',
                'expected_value': [
                    '<role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>',
                    '<role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>'
                ],
                'got_value': None,
                'message': '''Got None expected ['<role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>', '<role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>']''',
                'advice': '''The author FRANCISCO VENEGAS-MARTÍNEZ does not have a valid role. Provide a role from the list: ['<role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>', '<role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>']'''
            },
            {
                'title': 'CRediT taxonomy for contribs',
                'xpath': './contrib-group//contrib//role[@content-type="https://credit.niso.org/contributor-roles/*"]',
                'validation_type': 'value in list',
                'response': 'ERROR',
                'expected_value': [
                    '<role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>',
                    '<role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>'
                ],
                'got_value': None,
                'message': '''Got None expected ['<role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>', '<role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>']''',
                'advice': '''The author Vanessa M. Higa does not have a valid role. Provide a role from the list: ['<role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>', '<role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>']'''
            }
        ]

        for i, item in enumerate(messages):
            with self.subTest(i):
                self.assertDictEqual(expected_output[i], item)

    def test_role_and_content_type_empty(self):
        self.maxDiff = None
        xml = """
        <article>
            <front>
                <article-meta>
                    <contrib-group>
                        <contrib contrib-type="author">
                            <name>
                                <surname>VENEGAS-MARTÍNEZ</surname>
                                <given-names>FRANCISCO</given-names>
                                <prefix>Prof</prefix>
                                <suffix>Nieto</suffix>
                            </name>
                            <xref ref-type="aff" rid="aff1"/>
                            <role></role>
                            </contrib>
                            <contrib contrib-type="author">
                            <contrib-id contrib-id-type="orcid">0000-0001-5518-4853</contrib-id>
                            <name>
                                <surname>Higa</surname>
                                <given-names>Vanessa M.</given-names>
                            </name>
                            <xref ref-type="aff" rid="aff1">a</xref>
                            <role></role>
                        </contrib>
                    </contrib-group>
                </article-meta>
            </front>
        </article>
        """

        data = etree.fromstring(xml)
        messages = ArticleAuthorsValidation(xmltree=data).validate_authors_role(
            credit_taxonomy_terms_and_urls=credit_taxonomy_terms_and_urls
        )

        expected_output = [
            {
                'title': 'CRediT taxonomy for contribs',
                'xpath': './contrib-group//contrib//role[@content-type="https://credit.niso.org/contributor-roles/*"]',
                'validation_type': 'value in list',
                'response': 'ERROR',
                'expected_value': [
                    '<role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>',
                    '<role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>'
                ],
                'got_value': '<role content-type="None">None</role>',
                'message': '''Got <role content-type="None">None</role> expected ['<role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>', '<role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>']''',
                'advice': '''The author FRANCISCO VENEGAS-MARTÍNEZ does not have a valid role. Provide a role from the list: ['<role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>', '<role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>']'''
            },
            {
                'title': 'CRediT taxonomy for contribs',
                'xpath': './contrib-group//contrib//role[@content-type="https://credit.niso.org/contributor-roles/*"]',
                'validation_type': 'value in list',
                'response': 'ERROR',
                'expected_value': [
                    '<role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>',
                    '<role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>'
                ],
                'got_value': '<role content-type="None">None</role>',
                'message': '''Got <role content-type="None">None</role> expected ['<role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>', '<role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>']''',
                'advice': '''The author Vanessa M. Higa does not have a valid role. Provide a role from the list: ['<role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>', '<role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>']'''
            }
        ]

        for i, item in enumerate(messages):
            with self.subTest(i):
                self.assertDictEqual(expected_output[i], item)

    def test_role_without_content_type(self):
        self.maxDiff = None
        xml = """
            <article>
                <front>
                    <article-meta>
                        <contrib-group>
                            <contrib contrib-type="author">
                                <name>
                                    <surname>VENEGAS-MARTÍNEZ</surname>
                                    <given-names>FRANCISCO</given-names>
                                    <prefix>Prof</prefix>
                                    <suffix>Nieto</suffix>
                                </name>
                                <xref ref-type="aff" rid="aff1"/>
                                <role>Data curation</role>
                                </contrib>
                                <contrib contrib-type="author">
                                <contrib-id contrib-id-type="orcid">0000-0001-5518-4853</contrib-id>
                                <name>
                                    <surname>Higa</surname>
                                    <given-names>Vanessa M.</given-names>
                                </name>
                                <xref ref-type="aff" rid="aff1">a</xref>
                                <role>Conceptualization</role>
                            </contrib>
                        </contrib-group>
                    </article-meta>
                </front>
            </article>
            """

        expected_output = [
            {
                'title': 'CRediT taxonomy for contribs',
                'xpath': './contrib-group//contrib//role[@content-type="https://credit.niso.org/contributor-roles/*"]',
                'validation_type': 'value in list',
                'response': 'ERROR',
                'expected_value': [
                    '<role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>',
                    '<role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>'
                ],
                'got_value': '<role content-type="None">Data curation</role>',
                'message': '''Got <role content-type="None">Data curation</role> expected ['<role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>', '<role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>']''',
                'advice': '''The author FRANCISCO VENEGAS-MARTÍNEZ does not have a valid role. Provide a role from the list: ['<role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>', '<role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>']'''
            },
            {
                'title': 'CRediT taxonomy for contribs',
                'xpath': './contrib-group//contrib//role[@content-type="https://credit.niso.org/contributor-roles/*"]',
                'validation_type': 'value in list',
                'response': 'ERROR',
                'expected_value': [
                    '<role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>',
                    '<role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>'
                ],
                'got_value': '<role content-type="None">Conceptualization</role>',
                'message': '''Got <role content-type="None">Conceptualization</role> expected ['<role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>', '<role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>']''',
                'advice': '''The author Vanessa M. Higa does not have a valid role. Provide a role from the list: ['<role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>', '<role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>']'''
            }
        ]

        data = etree.fromstring(xml)
        messages = ArticleAuthorsValidation(xmltree=data).validate_authors_role(
            credit_taxonomy_terms_and_urls=credit_taxonomy_terms_and_urls
        )

        for i, item in enumerate(messages):
            with self.subTest(i):
                self.assertDictEqual(expected_output[i], item)

    def test_role_no_text_with_content_type(self):
        self.maxDiff = None
        xml = """
            <article>
                <front>
                    <article-meta>
                        <contrib-group>
                            <contrib contrib-type="author">
                                <name>
                                    <surname>VENEGAS-MARTÍNEZ</surname>
                                    <given-names>FRANCISCO</given-names>
                                    <prefix>Prof</prefix>
                                    <suffix>Nieto</suffix>
                                </name>
                                <xref ref-type="aff" rid="aff1"/>
                                <role content-type="https://credit.niso.org/contributor-roles/data-curation/"></role>
                                <role content-type="https://credit.niso.org/contributor-roles/conceptualization/"></role>
                                </contrib>
                                <contrib contrib-type="author">
                                <contrib-id contrib-id-type="orcid">0000-0001-5518-4853</contrib-id>
                                <name>
                                    <surname>Higa</surname>
                                    <given-names>Vanessa M.</given-names>
                                </name>
                                <xref ref-type="aff" rid="aff1">a</xref>
                                <role content-type="https://credit.niso.org/contributor-roles/conceptualization/"></role>
                            </contrib>
                        </contrib-group>
                    </article-meta>
                </front>
            </article>
            """

        expected_output = [
            {
                'title': 'CRediT taxonomy for contribs',
                'xpath': './contrib-group//contrib//role[@content-type="https://credit.niso.org/contributor-roles/*"]',
                'validation_type': 'value in list',
                'response': 'ERROR',
                'expected_value': [
                    '<role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>',
                    '<role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>'
                ],
                'got_value': '<role content-type="https://credit.niso.org/contributor-roles/data-curation/">None</role>',
                'message': '''Got <role content-type="https://credit.niso.org/contributor-roles/data-curation/">None</role> expected ['<role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>', '<role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>']''',
                'advice': '''The author FRANCISCO VENEGAS-MARTÍNEZ does not have a valid role. Provide a role from the list: ['<role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>', '<role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>']'''
            },
            {
                'title': 'CRediT taxonomy for contribs',
                'xpath': './contrib-group//contrib//role[@content-type="https://credit.niso.org/contributor-roles/*"]',
                'validation_type': 'value in list',
                'response': 'ERROR',
                'expected_value': [
                    '<role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>',
                    '<role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>'
                ],
                'got_value': '<role content-type="https://credit.niso.org/contributor-roles/conceptualization/">None</role>',
                'message': '''Got <role content-type="https://credit.niso.org/contributor-roles/conceptualization/">None</role> expected ['<role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>', '<role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>']''',
                'advice': '''The author FRANCISCO VENEGAS-MARTÍNEZ does not have a valid role. Provide a role from the list: ['<role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>', '<role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>']'''
            },
            {
                'title': 'CRediT taxonomy for contribs',
                'xpath': './contrib-group//contrib//role[@content-type="https://credit.niso.org/contributor-roles/*"]',
                'validation_type': 'value in list',
                'response': 'ERROR',
                'expected_value': [
                    '<role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>',
                    '<role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>'
                ],
                'got_value': '<role content-type="https://credit.niso.org/contributor-roles/conceptualization/">None</role>',
                'message': '''Got <role content-type="https://credit.niso.org/contributor-roles/conceptualization/">None</role> expected ['<role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>', '<role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>']''',
                'advice': '''The author Vanessa M. Higa does not have a valid role. Provide a role from the list: ['<role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>', '<role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>']'''
            }
        ]

        data = etree.fromstring(xml)
        messages = ArticleAuthorsValidation(xmltree=data).validate_authors_role(
            credit_taxonomy_terms_and_urls=credit_taxonomy_terms_and_urls
        )

        for i, item in enumerate(messages):
            with self.subTest(i):
                self.assertDictEqual(expected_output[i], item)

    def test_wrong_role_and_content_type(self):
        self.maxDiff = None
        xml = """
        <article>
            <front>
                <article-meta>
                    <contrib-group>
                        <contrib contrib-type="author">
                            <name>
                                <surname>VENEGAS-MARTÍNEZ</surname>
                                <given-names>FRANCISCO</given-names>
                                <prefix>Prof</prefix>
                                <suffix>Nieto</suffix>
                            </name>
                            <xref ref-type="aff" rid="aff1"/>
                            <role content-type="https://credit.niso.org/contributor-roles/data-curan/">Data curation</role>
                            <role content-type="https://credit.niso.org/contributor-roles/conceualizan/">Conceplization</role>
                            </contrib>
                            <contrib contrib-type="author">
                            <contrib-id contrib-id-type="orcid">0000-0001-5518-4853</contrib-id>
                            <name>
                                <surname>Higa</surname>
                                <given-names>Vanessa M.</given-names>
                            </name>
                            <xref ref-type="aff" rid="aff1">a</xref>
                            <role content-type="https://credit.niso.org/contributor-roles/conceualizan/">Conceplization</role>
                        </contrib>
                    </contrib-group>
                </article-meta>
            </front>
        </article>
        """

        expected_output = [
            {
                'title': 'CRediT taxonomy for contribs',
                'xpath': './contrib-group//contrib//role[@content-type="https://credit.niso.org/contributor-roles/*"]',
                'validation_type': 'value in list',
                'response': 'ERROR',
                'expected_value': [
                    '<role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>',
                    '<role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>'
                ],
                'got_value': '<role content-type="https://credit.niso.org/contributor-roles/data-curan/">Data curation</role>',
                'message': '''Got <role content-type="https://credit.niso.org/contributor-roles/data-curan/">Data curation</role> expected ['<role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>', '<role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>']''',
                'advice': '''The author FRANCISCO VENEGAS-MARTÍNEZ does not have a valid role. Provide a role from the list: ['<role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>', '<role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>']'''
            },
            {
                'title': 'CRediT taxonomy for contribs',
                'xpath': './contrib-group//contrib//role[@content-type="https://credit.niso.org/contributor-roles/*"]',
                'validation_type': 'value in list',
                'response': 'ERROR',
                'expected_value': [
                    '<role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>',
                    '<role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>'
                ],
                'got_value': '<role content-type="https://credit.niso.org/contributor-roles/conceualizan/">Conceplization</role>',
                'message': '''Got <role content-type="https://credit.niso.org/contributor-roles/conceualizan/">Conceplization</role> expected ['<role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>', '<role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>']''',
                'advice': '''The author FRANCISCO VENEGAS-MARTÍNEZ does not have a valid role. Provide a role from the list: ['<role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>', '<role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>']'''
            },
            {
                'title': 'CRediT taxonomy for contribs',
                'xpath': './contrib-group//contrib//role[@content-type="https://credit.niso.org/contributor-roles/*"]',
                'validation_type': 'value in list',
                'response': 'ERROR',
                'expected_value': [
                    '<role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>',
                    '<role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>'
                ],
                'got_value': '<role content-type="https://credit.niso.org/contributor-roles/conceualizan/">Conceplization</role>',
                'message': '''Got <role content-type="https://credit.niso.org/contributor-roles/conceualizan/">Conceplization</role> expected ['<role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>', '<role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>']''',
                'advice': '''The author Vanessa M. Higa does not have a valid role. Provide a role from the list: ['<role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>', '<role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>']'''
            }
        ]

        data = etree.fromstring(xml)
        messages = ArticleAuthorsValidation(xmltree=data).validate_authors_role(
            credit_taxonomy_terms_and_urls=credit_taxonomy_terms_and_urls
        )

        for i, item in enumerate(messages):
            with self.subTest(i):
                self.assertDictEqual(expected_output[i], item)

    def test_success_role(self):
        self.maxDiff = None
        xml = """
        <article>
            <front>
                <article-meta>
                    <contrib-group>
                        <contrib contrib-type="author">
                            <name>
                                <surname>VENEGAS-MARTÍNEZ</surname>
                                <given-names>FRANCISCO</given-names>
                                <prefix>Prof</prefix>
                                <suffix>Nieto</suffix>
                            </name>
                            <xref ref-type="aff" rid="aff1"/>
                            <role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>
                            <role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>
                            </contrib>
                            <contrib contrib-type="author">
                            <contrib-id contrib-id-type="orcid">0000-0001-5518-4853</contrib-id>
                            <name>
                                <surname>Higa</surname>
                                <given-names>Vanessa M.</given-names>
                            </name>
                            <xref ref-type="aff" rid="aff1">a</xref>
                            <role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>
                        </contrib>
                    </contrib-group>
                </article-meta>
            </front>
        </article>
        """

        expected_output = [
            {
                'title': 'CRediT taxonomy for contribs',
                'xpath': './contrib-group//contrib//role[@content-type="https://credit.niso.org/contributor-roles/*"]',
                'validation_type': 'value in list',
                'response': 'OK',
                'expected_value': [
                    '<role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>',
                    '<role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>'
                ],
                'got_value': '<role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>',
                'message': '''Got <role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role> expected ['<role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>', '<role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>']''',
                'advice': None
            },
            {
                'title': 'CRediT taxonomy for contribs',
                'xpath': './contrib-group//contrib//role[@content-type="https://credit.niso.org/contributor-roles/*"]',
                'validation_type': 'value in list',
                'response': 'OK',
                'expected_value': [
                    '<role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>',
                    '<role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>'
                ],
                'got_value': '<role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>',
                'message': '''Got <role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role> expected ['<role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>', '<role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>']''',
                'advice': None
            },
            {
                'title': 'CRediT taxonomy for contribs',
                'xpath': './contrib-group//contrib//role[@content-type="https://credit.niso.org/contributor-roles/*"]',
                'validation_type': 'value in list',
                'response': 'OK',
                'expected_value': [
                    '<role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>',
                    '<role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>'
                ],
                'got_value': '<role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>',
                'message': '''Got <role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role> expected ['<role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>', '<role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>']''',
                'advice': None
            }
        ]

        data = etree.fromstring(xml)
        messages = ArticleAuthorsValidation(xmltree=data).validate_authors_role(
            credit_taxonomy_terms_and_urls=credit_taxonomy_terms_and_urls
        )

        for i, item in enumerate(messages):
            with self.subTest(i):
                self.assertDictEqual(expected_output[i], item)


class ArticleAuthorsValidationOrcidTest(TestCase):
    def test_validate_authors_orcid_format_fail(self):
        self.maxDiff = None
        xml = """
        <article>
        <front>
            <article-meta>
              <contrib-group>
                <contrib contrib-type="author">
                    <contrib-id contrib-id-type="orcid">0990-01-58-4853</contrib-id>
                  <name>
                    <surname>VENEGAS-MARTÍNEZ</surname>
                    <given-names>FRANCISCO</given-names>
                    <prefix>Prof</prefix>
                    <suffix>Nieto</suffix>
                  </name>
                  <xref ref-type="aff" rid="aff1"/>
                </contrib>
                <contrib contrib-type="author">
                  <contrib-id contrib-id-type="orcid">00-0001-5518-4853</contrib-id>
                  <name>
                    <surname>Higa</surname>
                    <given-names>Vanessa M.</given-names>
                  </name>
                  <xref ref-type="aff" rid="aff1">a</xref>
                </contrib>
              </contrib-group>
            </article-meta>
          </front>
        </article>
        """
        xmltree = etree.fromstring(xml)
        messages = ArticleAuthorsValidation(xmltree=xmltree).validate_authors_orcid_format()

        expected_output = [
            {
                'title': 'Author ORCID',
                'xpath': './/contrib-id[@contrib-id-type="orcid"]',
                'validation_type': 'format',
                'response': 'ERROR',
                'expected_value': 'A Open Researcher and Contributor ID valid',
                'got_value': '0990-01-58-4853',
                'message': f'Got 0990-01-58-4853 expected a Open Researcher and Contributor ID valid',
                'advice': 'The author FRANCISCO VENEGAS-MARTÍNEZ has 0990-01-58-4853 as ORCID and its format is not valid. Provide a valid ORCID.'
            },
            {
                'title': 'Author ORCID',
                'xpath': './/contrib-id[@contrib-id-type="orcid"]',
                'validation_type': 'format',
                'response': 'ERROR',
                'expected_value': 'A Open Researcher and Contributor ID valid',
                'got_value': '00-0001-5518-4853',
                'message': f'Got 00-0001-5518-4853 expected a Open Researcher and Contributor ID valid',
                'advice': 'The author Vanessa M. Higa has 00-0001-5518-4853 as ORCID and its format is not valid. Provide a valid ORCID.'
            },
        ]
        for i, item in enumerate(messages):
            with self.subTest(i):
                self.assertDictEqual(expected_output[i], item)

    def test_validate_authors_orcid_format_without_orcid(self):
        self.maxDiff = None
        xml = """
        <article>
        <front>
            <article-meta>
              <contrib-group>
                <contrib contrib-type="author">
                  <name>
                    <surname>VENEGAS-MARTÍNEZ</surname>
                    <given-names>FRANCISCO</given-names>
                    <prefix>Prof</prefix>
                    <suffix>Nieto</suffix>
                  </name>
                  <xref ref-type="aff" rid="aff1"/>
                </contrib>
                <contrib contrib-type="author">
                  <name>
                    <surname>Higa</surname>
                    <given-names>Vanessa M.</given-names>
                  </name>
                  <xref ref-type="aff" rid="aff1">a</xref>
                </contrib>
              </contrib-group>
            </article-meta>
          </front>
        </article>
        """
        xmltree = etree.fromstring(xml)
        messages = ArticleAuthorsValidation(xmltree=xmltree).validate_authors_orcid_format()

        expected_output = [
            {
                'title': 'Author ORCID',
                'xpath': './/contrib-id[@contrib-id-type="orcid"]',
                'validation_type': 'format',
                'response': 'ERROR',
                'expected_value': 'A Open Researcher and Contributor ID valid',
                'got_value': None,
                'message': f'Got None expected a Open Researcher and Contributor ID valid',
                'advice': 'The author FRANCISCO VENEGAS-MARTÍNEZ has None as ORCID and its format is not valid. Provide a valid ORCID.'
            },
            {
                'title': 'Author ORCID',
                'xpath': './/contrib-id[@contrib-id-type="orcid"]',
                'validation_type': 'format',
                'response': 'ERROR',
                'expected_value': 'A Open Researcher and Contributor ID valid',
                'got_value': None,
                'message': f'Got None expected a Open Researcher and Contributor ID valid',
                'advice': 'The author Vanessa M. Higa has None as ORCID and its format is not valid. Provide a valid ORCID.'
            },
        ]

        for i, item in enumerate(messages):
            with self.subTest(i):
                self.assertDictEqual(expected_output[i], item)

    def test_validate_authors_orcid_format_success(self):
        self.maxDiff = None
        xml = """
        <article>
        <front>
            <article-meta>
              <contrib-group>
                <contrib contrib-type="author">
                    <contrib-id contrib-id-type="orcid">0990-0001-0058-4853</contrib-id>
                  <name>
                    <surname>VENEGAS-MARTÍNEZ</surname>
                    <given-names>FRANCISCO</given-names>
                    <prefix>Prof</prefix>
                    <suffix>Nieto</suffix>
                  </name>
                  <xref ref-type="aff" rid="aff1"/>
                </contrib>
                <contrib contrib-type="author">
                    <contrib-id contrib-id-type="orcid">0000-3333-1238-6873</contrib-id>
                  <name>
                    <surname>Higa</surname>
                    <given-names>Vanessa M.</given-names>
                  </name>
                  <xref ref-type="aff" rid="aff1">a</xref>
                </contrib>
              </contrib-group>
            </article-meta>
          </front>
        </article>
        """

        xmltree = etree.fromstring(xml)
        messages = ArticleAuthorsValidation(xmltree=xmltree).validate_authors_orcid_format()

        expected_output = [
            {
                'title': 'Author ORCID',
                'xpath': './/contrib-id[@contrib-id-type="orcid"]',
                'validation_type': 'format',
                'response': 'OK',
                'expected_value': '0990-0001-0058-4853',
                'got_value': '0990-0001-0058-4853',
                'message': f'Got 0990-0001-0058-4853 expected 0990-0001-0058-4853',
                'advice': None
            },
            {
                'title': 'Author ORCID',
                'xpath': './/contrib-id[@contrib-id-type="orcid"]',
                'validation_type': 'format',
                'response': 'OK',
                'expected_value': '0000-3333-1238-6873',
                'got_value': '0000-3333-1238-6873',
                'message': f'Got 0000-3333-1238-6873 expected 0000-3333-1238-6873',
                'advice': None
            },
        ]

        for i, item in enumerate(messages):
            with self.subTest(i):
                self.assertDictEqual(expected_output[i], item)

    def test_validate_authors_orcid_is_unique_ok(self):
        self.maxDiff = None
        xml = """
        <article>
        <front>
            <article-meta>
              <contrib-group>
                <contrib contrib-type="author">
                    <contrib-id contrib-id-type="orcid">0990-0001-0058-4853</contrib-id>
                  <name>
                    <surname>VENEGAS-MARTÍNEZ</surname>
                    <given-names>FRANCISCO</given-names>
                    <prefix>Prof</prefix>
                    <suffix>Nieto</suffix>
                  </name>
                  <xref ref-type="aff" rid="aff1"/>
                </contrib>
                <contrib contrib-type="author">
                    <contrib-id contrib-id-type="orcid">0000-3333-1238-6873</contrib-id>
                  <name>
                    <surname>Higa</surname>
                    <given-names>Vanessa M.</given-names>
                  </name>
                  <xref ref-type="aff" rid="aff1">a</xref>
                </contrib>
              </contrib-group>
            </article-meta>
          </front>
        </article>
        """

        xmltree = etree.fromstring(xml)
        messages = ArticleAuthorsValidation(xmltree=xmltree).validate_authors_orcid_is_unique()

        expected_output = [
            {
                'title': 'Author ORCID element is unique',
                'xpath': './/contrib-id[@contrib-id-type="orcid"]',
                'validation_type': 'exist/verification',
                'response': 'OK',
                'expected_value': 'Unique ORCID values',
                'got_value': ['0990-0001-0058-4853', '0000-3333-1238-6873'],
                'message': 'Got ORCIDs and frequencies (\'0990-0001-0058-4853\', 1) | (\'0000-3333-1238-6873\', 1)',
                'advice': None
            }
        ]

        for i, item in enumerate(messages):
            with self.subTest(i):
                self.assertDictEqual(expected_output[i], item)

    def test_validate_authors_orcid_is_unique_not_ok(self):
        self.maxDiff = None
        xml = """
        <article>
        <front>
            <article-meta>
              <contrib-group>
                <contrib contrib-type="author">
                    <contrib-id contrib-id-type="orcid">0990-0001-0058-4853</contrib-id>
                  <name>
                    <surname>VENEGAS-MARTÍNEZ</surname>
                    <given-names>FRANCISCO</given-names>
                    <prefix>Prof</prefix>
                    <suffix>Nieto</suffix>
                  </name>
                  <xref ref-type="aff" rid="aff1"/>
                </contrib>
                <contrib contrib-type="author">
                    <contrib-id contrib-id-type="orcid">0990-0001-0058-4853</contrib-id>
                  <name>
                    <surname>Higa</surname>
                    <given-names>Vanessa M.</given-names>
                  </name>
                  <xref ref-type="aff" rid="aff1">a</xref>
                </contrib>
              </contrib-group>
            </article-meta>
          </front>
        </article>
        """

        xmltree = etree.fromstring(xml)
        messages = ArticleAuthorsValidation(xmltree=xmltree).validate_authors_orcid_is_unique()

        expected_output = [
            {
                'title': 'Author ORCID element is unique',
                'xpath': './/contrib-id[@contrib-id-type="orcid"]',
                'validation_type': 'exist/verification',
                'response': 'ERROR',
                'expected_value': 'Unique ORCID values',
                'got_value': ['0990-0001-0058-4853', '0990-0001-0058-4853'],
                'message': 'Got ORCIDs and frequencies (\'0990-0001-0058-4853\', 2)',
                'advice': 'Consider replacing the following ORCIDs that are not unique: 0990-0001-0058-4853',
            }
        ]

        for i, item in enumerate(messages):
            with self.subTest(i):
                self.assertDictEqual(expected_output[i], item)

    def test_validate_authors_orcid_is_registered_sucess(self):
        self.maxDiff = None
        xml = """
                <article>
                <front>
                    <article-meta>
                      <contrib-group>
                        <contrib contrib-type="author">
                            <contrib-id contrib-id-type="orcid">0990-0001-0058-4853</contrib-id>
                          <name>
                            <surname>VENEGAS-MARTÍNEZ</surname>
                            <given-names>FRANCISCO</given-names>
                            <prefix>Prof</prefix>
                            <suffix>Nieto</suffix>
                          </name>
                          <xref ref-type="aff" rid="aff1"/>
                        </contrib>
                        <contrib contrib-type="author">
                            <contrib-id contrib-id-type="orcid">0000-3333-1238-6873</contrib-id>
                          <name>
                            <surname>Higa</surname>
                            <given-names>Vanessa M.</given-names>
                          </name>
                          <xref ref-type="aff" rid="aff1">a</xref>
                        </contrib>
                      </contrib-group>
                    </article-meta>
                  </front>
                </article>
                """

        xmltree = etree.fromstring(xml)
        messages = ArticleAuthorsValidation(xmltree=xmltree).validate_authors_orcid_is_registered(
            callable_get_data
        )

        expected_output = [
            {
                'title': 'Author ORCID element is registered',
                'xpath': './/contrib-id[@contrib-id-type="orcid"]',
                'validation_type': 'exist',
                'response': 'OK',
                'expected_value': ['0990-0001-0058-4853', 'FRANCISCO VENEGAS-MARTÍNEZ'],
                'got_value': ['0990-0001-0058-4853', 'FRANCISCO VENEGAS-MARTÍNEZ'],
                'message': 'Got [\'0990-0001-0058-4853\', \'FRANCISCO VENEGAS-MARTÍNEZ\'] expected '
                           '[\'0990-0001-0058-4853\', \'FRANCISCO VENEGAS-MARTÍNEZ\']',
                'advice': None
            },
            {
                'title': 'Author ORCID element is registered',
                'xpath': './/contrib-id[@contrib-id-type="orcid"]',
                'validation_type': 'exist',
                'response': 'OK',
                'expected_value': ['0000-3333-1238-6873', 'Vanessa M. Higa'],
                'got_value': ['0000-3333-1238-6873', 'Vanessa M. Higa'],
                'message': 'Got [\'0000-3333-1238-6873\', \'Vanessa M. Higa\'] expected '
                           '[\'0000-3333-1238-6873\', \'Vanessa M. Higa\']',
                'advice': None
            }
        ]

        for i, item in enumerate(messages):
            with self.subTest(i):
                self.assertDictEqual(expected_output[i], item)

    def test_validate_authors_orcid_is_registered_fail(self):
        self.maxDiff = None
        xml = """
                <article>
                <front>
                    <article-meta>
                      <contrib-group>
                        <contrib contrib-type="author">
                            <contrib-id contrib-id-type="orcid">0990-0001-0058-4853</contrib-id>
                          <name>
                            <surname>VENEGAS MARTÍNEZ</surname>
                            <given-names>FRANCISCO</given-names>
                            <prefix>Prof</prefix>
                            <suffix>Nieto</suffix>
                          </name>
                          <xref ref-type="aff" rid="aff1"/>
                        </contrib>
                        <contrib contrib-type="author">
                            <contrib-id contrib-id-type="orcid">0000-3333-1238-6874</contrib-id>
                          <name>
                            <surname>Higa</surname>
                            <given-names>Vanessa M.</given-names>
                          </name>
                          <xref ref-type="aff" rid="aff1">a</xref>
                        </contrib>
                      </contrib-group>
                    </article-meta>
                  </front>
                </article>
                """

        xmltree = etree.fromstring(xml)
        messages = ArticleAuthorsValidation(xmltree=xmltree).validate_authors_orcid_is_registered(
            callable_get_data
        )

        expected_output = [
            {
                'title': 'Author ORCID element is registered',
                'xpath': './/contrib-id[@contrib-id-type="orcid"]',
                'validation_type': 'exist',
                'response': 'ERROR',
                'expected_value': ['0990-0001-0058-4853', 'FRANCISCO VENEGAS-MARTÍNEZ'],
                'got_value': ['0990-0001-0058-4853', 'FRANCISCO VENEGAS MARTÍNEZ'],
                'message': 'Got [\'0990-0001-0058-4853\', \'FRANCISCO VENEGAS MARTÍNEZ\'] expected '
                           '[\'0990-0001-0058-4853\', \'FRANCISCO VENEGAS-MARTÍNEZ\']',
                'advice': 'ORCID 0990-0001-0058-4853 is not registered to any authors'
            },
            {
                'title': 'Author ORCID element is registered',
                'xpath': './/contrib-id[@contrib-id-type="orcid"]',
                'validation_type': 'exist',
                'response': 'ERROR',
                'expected_value': ['0000-3333-1238-6874', None],
                'got_value': ['0000-3333-1238-6874', 'Vanessa M. Higa'],
                'message': 'Got [\'0000-3333-1238-6874\', \'Vanessa M. Higa\'] expected [\'0000-3333-1238-6874\', None]',
                'advice': 'ORCID 0000-3333-1238-6874 is not registered to any authors'
            }
        ]

        for i, item in enumerate(messages):
            with self.subTest(i):
                self.assertDictEqual(expected_output[i], item)

    def test_validate_authors_orcid_is_registered_fail_empty(self):
        self.maxDiff = None
        xml = """
                <article>
                <front>
                    <article-meta>
                      <contrib-group>
                        <contrib contrib-type="author">
                            <contrib-id contrib-id-type="orcid">0990-0001-0058-4853</contrib-id>
                          <name>
                            <surname>VENEGAS MARTÍNEZ</surname>
                            <given-names>FRANCISCO</given-names>
                            <prefix>Prof</prefix>
                            <suffix>Nieto</suffix>
                          </name>
                          <xref ref-type="aff" rid="aff1"/>
                        </contrib>
                        <contrib contrib-type="author">
                            <contrib-id contrib-id-type="orcid">0000-3333-1238-6874</contrib-id>
                          <name>
                            <surname>Higa</surname>
                            <given-names>Vanessa M.</given-names>
                          </name>
                          <xref ref-type="aff" rid="aff1">a</xref>
                        </contrib>
                      </contrib-group>
                    </article-meta>
                  </front>
                </article>
                """

        xmltree = etree.fromstring(xml)
        messages = ArticleAuthorsValidation(xmltree=xmltree).validate_authors_orcid_is_registered(
            callable_get_data_empty
        )

        expected_output = [
            {
                'title': 'Author ORCID element is registered',
                'xpath': './/contrib-id[@contrib-id-type="orcid"]',
                'validation_type': 'exist',
                'response': 'ERROR',
                'expected_value': ['0990-0001-0058-4853', None],
                'got_value': ['0990-0001-0058-4853', 'FRANCISCO VENEGAS MARTÍNEZ'],
                'message': 'Got [\'0990-0001-0058-4853\', \'FRANCISCO VENEGAS MARTÍNEZ\'] expected '
                           '[\'0990-0001-0058-4853\', None]',
                'advice': 'ORCID 0990-0001-0058-4853 is not registered to any authors'
            },
            {
                'title': 'Author ORCID element is registered',
                'xpath': './/contrib-id[@contrib-id-type="orcid"]',
                'validation_type': 'exist',
                'response': 'ERROR',
                'expected_value': ['0000-3333-1238-6874', None],
                'got_value': ['0000-3333-1238-6874', 'Vanessa M. Higa'],
                'message': 'Got [\'0000-3333-1238-6874\', \'Vanessa M. Higa\'] expected [\'0000-3333-1238-6874\', None]',
                'advice': 'ORCID 0000-3333-1238-6874 is not registered to any authors'
            }
        ]

        for i, item in enumerate(messages):
            with self.subTest(i):
                self.assertDictEqual(expected_output[i], item)

    def test_validate(self):
        self.maxDiff = None
        xml = """
        <article>
        <front>
            <article-meta>
              <contrib-group>
                <contrib contrib-type="author">
                    <contrib-id contrib-id-type="orcid">0990-0001-0058-4853</contrib-id>
                  <name>
                    <surname>VENEGAS-MARTÍNEZ</surname>
                    <given-names>FRANCISCO</given-names>
                    <prefix>Prof</prefix>
                    <suffix>Nieto</suffix>
                  </name>
                  <xref ref-type="aff" rid="aff1"/>
                </contrib>
                <contrib contrib-type="author">
                    <contrib-id contrib-id-type="orcid">0000-3333-1238-6873</contrib-id>
                  <name>
                    <surname>Higa</surname>
                    <given-names>Vanessa M.</given-names>
                  </name>
                  <xref ref-type="aff" rid="aff1">a</xref>
                </contrib>
              </contrib-group>
            </article-meta>
          </front>
        </article>
        """

        xmltree = etree.fromstring(xml)
        messages = list(ArticleAuthorsValidation(xmltree=xmltree).validate(
            {
                'credit_taxonomy_terms_and_urls': credit_taxonomy_terms_and_urls,
                'callable_get_data': callable_get_data
            }
        ))

        expected_output = [
            {
                'title': 'CRediT taxonomy for contribs',
                'xpath': './contrib-group//contrib//role[@content-type="https://credit.niso.org/contributor-roles/*"]',
                'validation_type': 'value in list',
                'response': 'ERROR',
                'expected_value': [
                    '<role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>',
                    '<role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>'
                ],
                'got_value': None,
                'message': '''Got None expected ['<role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>', '<role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>']''',
                'advice': '''The author FRANCISCO VENEGAS-MARTÍNEZ does not have a valid role. Provide a role from the list: ['<role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>', '<role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>']'''
            },
            {
                'title': 'CRediT taxonomy for contribs',
                'xpath': './contrib-group//contrib//role[@content-type="https://credit.niso.org/contributor-roles/*"]',
                'validation_type': 'value in list',
                'response': 'ERROR',
                'expected_value': [
                    '<role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>',
                    '<role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>'
                ],
                'got_value': None,
                'message': '''Got None expected ['<role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>', '<role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>']''',
                'advice': '''The author Vanessa M. Higa does not have a valid role. Provide a role from the list: ['<role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>', '<role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>']'''
            },
            {
                'title': 'Author ORCID',
                'xpath': './/contrib-id[@contrib-id-type="orcid"]',
                'validation_type': 'format',
                'response': 'OK',
                'expected_value': '0990-0001-0058-4853',
                'got_value': '0990-0001-0058-4853',
                'message': f'Got 0990-0001-0058-4853 expected 0990-0001-0058-4853',
                'advice': None
            },
            {
                'title': 'Author ORCID',
                'xpath': './/contrib-id[@contrib-id-type="orcid"]',
                'validation_type': 'format',
                'response': 'OK',
                'expected_value': '0000-3333-1238-6873',
                'got_value': '0000-3333-1238-6873',
                'message': f'Got 0000-3333-1238-6873 expected 0000-3333-1238-6873',
                'advice': None
            },
            {
                'title': 'Author ORCID element is unique',
                'xpath': './/contrib-id[@contrib-id-type="orcid"]',
                'validation_type': 'exist/verification',
                'response': 'OK',
                'expected_value': 'Unique ORCID values',
                'got_value': ['0990-0001-0058-4853', '0000-3333-1238-6873'],
                'message': 'Got ORCIDs and frequencies (\'0990-0001-0058-4853\', 1) | (\'0000-3333-1238-6873\', 1)',
                'advice': None
            },
            {
                'title': 'Author ORCID element is registered',
                'xpath': './/contrib-id[@contrib-id-type="orcid"]',
                'validation_type': 'exist',
                'response': 'OK',
                'expected_value': ['0990-0001-0058-4853', 'FRANCISCO VENEGAS-MARTÍNEZ'],
                'got_value': ['0990-0001-0058-4853', 'FRANCISCO VENEGAS-MARTÍNEZ'],
                'message': 'Got [\'0990-0001-0058-4853\', \'FRANCISCO VENEGAS-MARTÍNEZ\'] expected '
                           '[\'0990-0001-0058-4853\', \'FRANCISCO VENEGAS-MARTÍNEZ\']',
                'advice': None
            },
            {
                'title': 'Author ORCID element is registered',
                'xpath': './/contrib-id[@contrib-id-type="orcid"]',
                'validation_type': 'exist',
                'response': 'OK',
                'expected_value': ['0000-3333-1238-6873', 'Vanessa M. Higa'],
                'got_value': ['0000-3333-1238-6873', 'Vanessa M. Higa'],
                'message': 'Got [\'0000-3333-1238-6873\', \'Vanessa M. Higa\'] expected '
                           '[\'0000-3333-1238-6873\', \'Vanessa M. Higa\']',
                'advice': None
            }
        ]

        for i, item in enumerate(expected_output):
            with self.subTest(i):
                self.assertDictEqual(messages[i], item)
