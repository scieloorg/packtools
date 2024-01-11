import unittest

from packtools.sps.utils.xml_utils import get_xml_tree

from packtools.sps.validation.article_doi import ArticleDoiValidation


def callable_get_data_ok(doi):
    return {
        'en': {
                'title': 'Title in English',
                'doi': '10.1590/2176-4573e59270'
            },
        'pt': {
                'title': 'Título em Português',
                'doi': '10.1590/2176-4573p59270'
            },
        'authors': ['Martínez-Momblán, Maria Antonia', 'Colina-Torralva, Javier']
    }


def callable_get_data_one_author(doi):
    return {
        'en': {
            'title': 'Title in English',
            'doi': '10.1590/2176-4573e59270'
        },
        'pt': {
            'title': 'Título em Português',
            'doi': '10.1590/2176-4573p59270'
        },
        'authors': ['Colina-Torralva, Javier']
    }


def callable_get_data_not_registered(doi):
    return None


def callable_get_data_missing_title(doi):
    return {
        'en': {
                'doi': '10.1590/2176-4573e59270'
            },
        'pt': {
                'doi': '10.1590/2176-4573p59270'
            },
        'authors': ['Martínez-Momblán, Maria Antonia', 'Colina-Torralva, Javier']
    }


def callable_get_data_missing_authors(doi):
    return {
        'en': {
                'title': 'Title in English',
                'doi': '10.1590/2176-4573e59270'
            },
        'pt': {
                'title': 'Título em Português',
                'doi': '10.1590/2176-4573p59270'
            }
    }


class ArticleDoiTest(unittest.TestCase):
    def test_validate_article_has_doi(self):
        self.maxDiff = None
        xml_str = """
            <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink"
            article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
            <front>
            <article-id pub-id-type="publisher-id" specific-use="scielo-v3">TPg77CCrGj4wcbLCh9vG8bS</article-id>
            <article-id pub-id-type="publisher-id" specific-use="scielo-v2">S0104-11692020000100303</article-id>
            <article-id pub-id-type="doi">10.1590/1518-8345.2927.3231</article-id>
            <article-id pub-id-type="other">00303</article-id>
            </front>
            </article>
            """
        xml_tree = get_xml_tree(xml_str)
        obtained = ArticleDoiValidation(xml_tree).validate_main_article_doi_exists()
        expected = [
            {
                'title': 'Article DOI element',
                'xpath': './article-id[@pub-id-type="doi"]',
                'validation_type': 'exist',
                'response': 'OK',
                'expected_value': '10.1590/1518-8345.2927.3231',
                'got_value': '10.1590/1518-8345.2927.3231',
                'message': 'Got 10.1590/1518-8345.2927.3231 expected 10.1590/1518-8345.2927.3231',
                'advice': None
            }
        ]
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

    def test_validate_article_has_no_doi(self):
        self.maxDiff = None
        xml_str = """
            <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink"
            article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
            <front>
            <article-id pub-id-type="publisher-id" specific-use="scielo-v3">TPg77CCrGj4wcbLCh9vG8bS</article-id>
            <article-id pub-id-type="publisher-id" specific-use="scielo-v2">S0104-11692020000100303</article-id>
            <article-id pub-id-type="other">00303</article-id>
            </front>
            </article>
            """
        xml_tree = get_xml_tree(xml_str)
        obtained = ArticleDoiValidation(xml_tree).validate_main_article_doi_exists()
        expected = [
            {
                'title': 'Article DOI element',
                'xpath': './article-id[@pub-id-type="doi"]',
                'validation_type': 'exist',
                'response': 'ERROR',
                'expected_value': 'article DOI',
                'got_value': None,
                'message': 'Got None expected a DOI',
                'advice': 'Provide a valid DOI for the research-article'
            }
        ]
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

    def test_validate_translation_subarticle_has_one_translation_and_one_doi(self):
        self.maxDiff = None
        xml_str = """
            <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink"
            article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="pt">
            <front>
                <article-id specific-use="previous-pid" pub-id-type="publisher-id">S2176-45732023005002205</article-id>
                <article-id specific-use="scielo-v3" pub-id-type="publisher-id">PqQCH4JjQTWmwYF97s4YGKv</article-id>
                <article-id specific-use="scielo-v2" pub-id-type="publisher-id">S2176-45732023000200226</article-id>
                <article-id pub-id-type="doi">10.1590/2176-4573p59270</article-id>
            </front>
            <sub-article article-type="reviewer-report" id="s2" xml:lang="pt" />
            <sub-article article-type="reviewer-report" id="s3" xml:lang="pt" />
            <sub-article article-type="translation" id="s1" xml:lang="en">
                <front-stub>
                    <article-id pub-id-type="doi">10.1590/2176-4573e59270</article-id>
                </front-stub>
            </sub-article>
            </article>
            """
        xml_tree = get_xml_tree(xml_str)
        obtained = ArticleDoiValidation(xml_tree).validate_translations_doi_exists()

        expected = [
            {
                'title': 'Sub-article translation DOI element',
                'xpath': './sub-article[@article-type="translation"]',
                'validation_type': 'exist',
                'response': 'OK',
                'expected_value': '10.1590/2176-4573e59270',
                'got_value': '10.1590/2176-4573e59270',
                'message': 'Got 10.1590/2176-4573e59270 expected 10.1590/2176-4573e59270',
                'advice': None
            }
        ]
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

    def test_validate_translation_subarticle_has_two_translations_and_one_doi(self):
        self.maxDiff = None
        xml_str = """
            <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink"
            article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="pt">
            <front>
                <article-id specific-use="previous-pid" pub-id-type="publisher-id">S2176-45732023005002205</article-id>
                <article-id specific-use="scielo-v3" pub-id-type="publisher-id">PqQCH4JjQTWmwYF97s4YGKv</article-id>
                <article-id specific-use="scielo-v2" pub-id-type="publisher-id">S2176-45732023000200226</article-id>
                <article-id pub-id-type="doi">10.1590/2176-4573p59270</article-id>
            </front>
            <sub-article article-type="reviewer-report" id="s2" xml:lang="pt" />
            <sub-article article-type="translation" id="s3" xml:lang="es" />
            <sub-article article-type="translation" id="s1" xml:lang="en">
                <front-stub>
                    <article-id pub-id-type="doi">10.1590/2176-4573e59270</article-id>
                </front-stub>
            </sub-article>
            </article>
            """
        xml_tree = get_xml_tree(xml_str)
        obtained = ArticleDoiValidation(xml_tree).validate_translations_doi_exists()

        expected = [
            {
                'title': 'Sub-article translation DOI element',
                'xpath': './sub-article[@article-type="translation"]',
                'validation_type': 'exist',
                'response': 'ERROR',
                'expected_value': 'sub-article DOI',
                'got_value': None,
                'message': 'Got None expected sub-article DOI',
                'advice': 'Provide a valid DOI for the sub-article represented by the following '
                          'tag: <sub-article article-type="translation" id="s3" xml:lang="es">'
            },
            {
                'title': 'Sub-article translation DOI element',
                'xpath': './sub-article[@article-type="translation"]',
                'validation_type': 'exist',
                'response': 'OK',
                'expected_value': '10.1590/2176-4573e59270',
                'got_value': '10.1590/2176-4573e59270',
                'message': 'Got 10.1590/2176-4573e59270 expected 10.1590/2176-4573e59270',
                'advice': None
            }
        ]
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

    def test_validate_translation_subarticle_has_three_translations_and_two_doi(self):
        self.maxDiff = None
        xml_str = """
            <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink"
            article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="pt">
            <front>
                <article-id specific-use="previous-pid" pub-id-type="publisher-id">S2176-45732023005002205</article-id>
                <article-id specific-use="scielo-v3" pub-id-type="publisher-id">PqQCH4JjQTWmwYF97s4YGKv</article-id>
                <article-id specific-use="scielo-v2" pub-id-type="publisher-id">S2176-45732023000200226</article-id>
                <article-id pub-id-type="doi">10.1590/2176-4573p59270</article-id>
            </front>
            <sub-article article-type="translation" id="s2" xml:lang="fr" />
            <sub-article article-type="translation" id="s3" xml:lang="es">
                <front-stub>
                    <article-id pub-id-type="doi">10.1590/2176-4573e59270</article-id>
                </front-stub>
            </sub-article>
            <sub-article article-type="translation" id="s1" xml:lang="en">
                <front-stub>
                    <article-id pub-id-type="doi">10.1590/2176-4573e59270</article-id>
                </front-stub>
            </sub-article>
            </article>
            """
        xml_tree = get_xml_tree(xml_str)
        obtained = ArticleDoiValidation(xml_tree).validate_translations_doi_exists()

        expected = [
            {
                'title': 'Sub-article translation DOI element',
                'xpath': './sub-article[@article-type="translation"]',
                'validation_type': 'exist',
                'response': 'ERROR',
                'expected_value': 'sub-article DOI',
                'got_value': None,
                'message': 'Got None expected sub-article DOI',
                'advice': 'Provide a valid DOI for the sub-article represented by the following '
                          'tag: <sub-article article-type="translation" id="s2" xml:lang="fr">'
            },
            {
                'title': 'Sub-article translation DOI element',
                'xpath': './sub-article[@article-type="translation"]',
                'validation_type': 'exist',
                'response': 'OK',
                'expected_value': '10.1590/2176-4573e59270',
                'got_value': '10.1590/2176-4573e59270',
                'message': 'Got 10.1590/2176-4573e59270 expected 10.1590/2176-4573e59270',
                'advice': None
            },
            {
                'title': 'Sub-article translation DOI element',
                'xpath': './sub-article[@article-type="translation"]',
                'validation_type': 'exist',
                'response': 'OK',
                'expected_value': '10.1590/2176-4573e59270',
                'got_value': '10.1590/2176-4573e59270',
                'message': 'Got 10.1590/2176-4573e59270 expected 10.1590/2176-4573e59270',
                'advice': None
            }
        ]
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

    def test_validate_all_dois_are_unique(self):
        self.maxDiff = None
        xml_str = """
            <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink"
            article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="pt">
            <front>
                <article-id specific-use="previous-pid" pub-id-type="publisher-id">S2176-45732023005002205</article-id>
                <article-id specific-use="scielo-v3" pub-id-type="publisher-id">PqQCH4JjQTWmwYF97s4YGKv</article-id>
                <article-id specific-use="scielo-v2" pub-id-type="publisher-id">S2176-45732023000200226</article-id>
                <article-id pub-id-type="doi">10.1590/2176-4573p59270</article-id>
            </front>
            <sub-article article-type="reviewer-report" id="s2" xml:lang="pt" />
            <sub-article article-type="reviewer-report" id="s3" xml:lang="pt" />
            <sub-article article-type="translation" id="s1" xml:lang="en">
                <front-stub>
                    <article-id pub-id-type="doi">10.1590/2176-4573e59270</article-id>
                </front-stub>
            </sub-article>
            </article>
            """
        xml_tree = get_xml_tree(xml_str)
        obtained = ArticleDoiValidation(xml_tree).validate_all_dois_are_unique()

        expected = [
            {
                'title': 'Article DOI element is unique',
                'xpath': './article-id[@pub-id-type="doi"]',
                'validation_type': 'exist/verification',
                'response': 'OK',
                'expected_value': 'Unique DOI values',
                'got_value': ['10.1590/2176-4573p59270', '10.1590/2176-4573e59270'],
                'message': "Got DOIs and frequencies ('10.1590/2176-4573p59270', 1) | ('10.1590/2176-4573e59270', 1)",
                'advice': None
            }
        ]
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

    def test_validate_all_dois_are_not_unique(self):
        self.maxDiff = None
        xml_str = """
            <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink"
            article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="pt">
            <front>
                <article-id specific-use="previous-pid" pub-id-type="publisher-id">S2176-45732023005002205</article-id>
                <article-id specific-use="scielo-v3" pub-id-type="publisher-id">PqQCH4JjQTWmwYF97s4YGKv</article-id>
                <article-id specific-use="scielo-v2" pub-id-type="publisher-id">S2176-45732023000200226</article-id>
                <article-id pub-id-type="doi">10.1590/2176-4573p59270</article-id>
            </front>
            <sub-article article-type="translation" id="s2" xml:lang="fr">
                <front-stub>
                    <article-id pub-id-type="doi">10.1590/2176-4573e59270</article-id>
                </front-stub>
            </sub-article>
            <sub-article article-type="translation" id="s3" xml:lang="es">
                <front-stub>
                    <article-id pub-id-type="doi">10.1590/2176-4573e59270</article-id>
                </front-stub>
            </sub-article>
            <sub-article article-type="translation" id="s1" xml:lang="en">
                <front-stub>
                    <article-id pub-id-type="doi">10.1590/2176-4573e59270</article-id>
                </front-stub>
            </sub-article>
            </article>
            """
        xml_tree = get_xml_tree(xml_str)
        obtained = ArticleDoiValidation(xml_tree).validate_all_dois_are_unique()

        expected = [
            {
                'title': 'Article DOI element is unique',
                'xpath': './article-id[@pub-id-type="doi"]',
                'validation_type': 'exist/verification',
                'response': 'ERROR',
                'expected_value': 'Unique DOI values',
                'got_value': ['10.1590/2176-4573p59270', '10.1590/2176-4573e59270'],
                'message': "Got DOIs and frequencies ('10.1590/2176-4573p59270', 1) | ('10.1590/2176-4573e59270', 3)",
                'advice': 'Consider replacing the following DOIs that are not unique: 10.1590/2176-4573e59270'
            }
        ]
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

    def test_validate_doi_registered_success(self):
        self.maxDiff = None
        xml_str = """
            <article xml:lang="en">
            <front>
                <article-meta>
                <article-id pub-id-type="doi">10.1590/2176-4573e59270</article-id>
                <title-group>
                    <article-title>Title in English</article-title>
                </title-group>
                <contrib-group>
                    <contrib contrib-type="author">
                      <name>
                        <surname>Martínez-Momblán</surname>
                        <given-names>Maria Antonia</given-names>
                      </name>
                    </contrib>
                    <contrib contrib-type="author">
                      <name>
                        <surname>Colina-Torralva</surname>
                        <given-names>Javier</given-names>
                      </name>
                    </contrib>
                </contrib-group>
                </article-meta>
            </front>
            <sub-article article-type="translation" id="s1" xml:lang="pt">
                <front-stub>
                    <article-id pub-id-type="doi">10.1590/2176-4573p59270</article-id>
                        <title-group>
                            <article-title>Título em Português</article-title>
                        </title-group>
                        <contrib-group>
                            <contrib contrib-type="author">
                                <name>
                                <surname>Martínez-Momblán</surname>
                                <given-names>Maria Antonia</given-names>
                                </name>
                            </contrib>
                            <contrib contrib-type="author">
                                <name>
                                <surname>Colina-Torralva</surname>
                                <given-names>Javier</given-names>
                                </name>
                            </contrib>
                        </contrib-group>
                </front-stub>
            </sub-article>      
            </article>
            """
        xml_tree = get_xml_tree(xml_str)
        obtained = ArticleDoiValidation(xml_tree).validate_doi_registered(
            callable_get_data_ok
        )

        expected = [
            {
                'title': 'Article DOI is registered (lang: en, element: doi)',
                'xpath': './article-id[@pub-id-type="doi"]',
                'validation_type': 'exist',
                'response': 'OK',
                'expected_value': '10.1590/2176-4573e59270',
                'got_value': '10.1590/2176-4573e59270',
                'message': 'Got 10.1590/2176-4573e59270 expected 10.1590/2176-4573e59270',
                'advice': None
            },
            {
                'title': 'Article DOI is registered (lang: en, element: title)',
                'xpath': './article-id[@pub-id-type="doi"]',
                'validation_type': 'exist',
                'response': 'OK',
                'expected_value': 'Title in English',
                'got_value': 'Title in English',
                'message': 'Got Title in English expected Title in English',
                'advice': None
            },
            {
                'title': 'Article DOI is registered (lang: en, element: author)',
                'xpath': './article-id[@pub-id-type="doi"]',
                'validation_type': 'exist',
                'response': 'OK',
                'expected_value': 'Martínez-Momblán, Maria Antonia',
                'got_value': 'Martínez-Momblán, Maria Antonia',
                'message': 'Got Martínez-Momblán, Maria Antonia expected Martínez-Momblán, Maria Antonia',
                'advice': None
            },
            {
                'title': 'Article DOI is registered (lang: en, element: author)',
                'xpath': './article-id[@pub-id-type="doi"]',
                'validation_type': 'exist',
                'response': 'OK',
                'expected_value': 'Colina-Torralva, Javier',
                'got_value': 'Colina-Torralva, Javier',
                'message': 'Got Colina-Torralva, Javier expected Colina-Torralva, Javier',
                'advice': None
            },
            {
                'title': 'Article DOI is registered (lang: pt, element: doi)',
                'xpath': './article-id[@pub-id-type="doi"]',
                'validation_type': 'exist',
                'response': 'OK',
                'expected_value': '10.1590/2176-4573p59270',
                'got_value': '10.1590/2176-4573p59270',
                'message': 'Got 10.1590/2176-4573p59270 expected 10.1590/2176-4573p59270',
                'advice': None
            },
            {
                'title': 'Article DOI is registered (lang: pt, element: title)',
                'xpath': './article-id[@pub-id-type="doi"]',
                'validation_type': 'exist',
                'response': 'OK',
                'expected_value': 'Título em Português',
                'got_value': 'Título em Português',
                'message': 'Got Título em Português expected Título em Português',
                'advice': None
            },
            {
                'title': 'Article DOI is registered (lang: pt, element: author)',
                'xpath': './article-id[@pub-id-type="doi"]',
                'validation_type': 'exist',
                'response': 'OK',
                'expected_value': 'Martínez-Momblán, Maria Antonia',
                'got_value': 'Martínez-Momblán, Maria Antonia',
                'message': 'Got Martínez-Momblán, Maria Antonia expected Martínez-Momblán, Maria Antonia',
                'advice': None
            },
            {
                'title': 'Article DOI is registered (lang: pt, element: author)',
                'xpath': './article-id[@pub-id-type="doi"]',
                'validation_type': 'exist',
                'response': 'OK',
                'expected_value': 'Colina-Torralva, Javier',
                'got_value': 'Colina-Torralva, Javier',
                'message': 'Got Colina-Torralva, Javier expected Colina-Torralva, Javier',
                'advice': None
            }

        ]
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

    def test_validate_doi_registered_doi_is_not_registered(self):
        self.maxDiff = None
        xml_str = """
            <article xml:lang="en">
            <front>
                <article-meta>
                <article-id pub-id-type="doi">10.1590/2176-4573e59270</article-id>
                <title-group>
                    <article-title>Title in English</article-title>
                </title-group>
                <contrib-group>
                    <contrib contrib-type="author">
                      <name>
                        <surname>Martínez-Momblán</surname>
                        <given-names>Maria Antonia</given-names>
                      </name>
                    </contrib>
                    <contrib contrib-type="author">
                      <name>
                        <surname>Colina-Torralva</surname>
                        <given-names>Javier</given-names>
                      </name>
                    </contrib>
                </contrib-group>
                </article-meta>
            </front>
            <sub-article article-type="translation" id="s1" xml:lang="pt">
                <front-stub>
                    <article-id pub-id-type="doi">10.1590/2176-4573p59270</article-id>
                        <title-group>
                            <article-title>Título em Português</article-title>
                        </title-group>
                        <contrib-group>
                            <contrib contrib-type="author">
                                <name>
                                <surname>Martínez-Momblán</surname>
                                <given-names>Maria Antonia</given-names>
                                </name>
                            </contrib>
                            <contrib contrib-type="author">
                                <name>
                                <surname>Colina-Torralva</surname>
                                <given-names>Javier</given-names>
                                </name>
                            </contrib>
                        </contrib-group>
                </front-stub>
            </sub-article>      
            </article>
            """
        xml_tree = get_xml_tree(xml_str)
        obtained = ArticleDoiValidation(xml_tree).validate_doi_registered(
            callable_get_data_not_registered
        )

        expected = [
            {
                'title': 'Article DOI is registered',
                'xpath': './article-id[@pub-id-type="doi"]',
                'validation_type': 'exist',
                'response': 'ERROR',
                'expected_value': 'Data registered to the DOI 10.1590/2176-4573e59270',
                'got_value': None,
                'message': 'Got None expected data registered to the DOI 10.1590/2176-4573e59270',
                'advice': 'DOI not registered or validator not found, provide a DOI value that has a valid registration'
            },
            {
                'title': 'Article DOI is registered',
                'xpath': './article-id[@pub-id-type="doi"]',
                'validation_type': 'exist',
                'response': 'ERROR',
                'expected_value': 'Data registered to the DOI 10.1590/2176-4573p59270',
                'got_value': None,
                'message': 'Got None expected data registered to the DOI 10.1590/2176-4573p59270',
                'advice': 'DOI not registered or validator not found, provide a DOI value that has a valid registration'
            }
        ]
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

    def test_validate_doi_registered_only_doi_is_correct(self):
        self.maxDiff = None
        xml_str = """
            <article xml:lang="en">
            <front>
                <article-meta>
                <article-id pub-id-type="doi">10.1590/2176-4573e59270</article-id>
                <title-group>
                    <article-title>Title English</article-title>
                </title-group>
                <contrib-group>
                    <contrib contrib-type="author">
                      <name>
                        <surname>Martínez</surname>
                        <given-names>Maria Antonia</given-names>
                      </name>
                    </contrib>
                    <contrib contrib-type="author">
                      <name>
                        <surname>Colina</surname>
                        <given-names>Javier</given-names>
                      </name>
                    </contrib>
                </contrib-group>
                </article-meta>
            </front>
            </article>
            """
        xml_tree = get_xml_tree(xml_str)
        obtained = ArticleDoiValidation(xml_tree).validate_doi_registered(
            callable_get_data_ok
        )

        expected = [
            {
                'title': 'Article DOI is registered (lang: en, element: doi)',
                'xpath': './article-id[@pub-id-type="doi"]',
                'validation_type': 'exist',
                'response': 'OK',
                'expected_value': '10.1590/2176-4573e59270',
                'got_value': '10.1590/2176-4573e59270',
                'message': 'Got 10.1590/2176-4573e59270 expected 10.1590/2176-4573e59270',
                'advice': None
            },
            {
                'title': 'Article DOI is registered (lang: en, element: title)',
                'xpath': './article-id[@pub-id-type="doi"]',
                'validation_type': 'exist',
                'response': 'ERROR',
                'expected_value': 'Title in English',
                'got_value': 'Title English',
                'message': 'Got Title English expected Title in English',
                'advice': 'DOI not registered or validator not found, provide a value for title element that '
                          'matches the record for DOI.'
            },
            {
                'title': 'Article DOI is registered (lang: en, element: author)',
                'xpath': './article-id[@pub-id-type="doi"]',
                'validation_type': 'exist',
                'response': 'ERROR',
                'expected_value': 'Martínez-Momblán, Maria Antonia',
                'got_value': 'Martínez, Maria Antonia',
                'message': 'Got Martínez, Maria Antonia expected Martínez-Momblán, Maria Antonia',
                'advice': 'DOI not registered or validator not found, provide a value for author element that '
                          'matches the record for DOI.'
            },
            {
                'title': 'Article DOI is registered (lang: en, element: author)',
                'xpath': './article-id[@pub-id-type="doi"]',
                'validation_type': 'exist',
                'response': 'ERROR',
                'expected_value': 'Colina-Torralva, Javier',
                'got_value': 'Colina, Javier',
                'message': 'Got Colina, Javier expected Colina-Torralva, Javier',
                'advice': 'DOI not registered or validator not found, provide a value for author element that '
                          'matches the record for DOI.'
            }
        ]
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

    def test_validate_doi_registered_only_title_is_correct(self):
        self.maxDiff = None
        xml_str = """
            <article xml:lang="en">
            <front>
                <article-meta>
                <article-id pub-id-type="doi">10.1590/2176-4573e59271</article-id>
                <title-group>
                    <article-title>Title in English</article-title>
                </title-group>
                <contrib-group>
                    <contrib contrib-type="author">
                      <name>
                        <surname>Martínez</surname>
                        <given-names>Maria Antonia</given-names>
                      </name>
                    </contrib>
                    <contrib contrib-type="author">
                      <name>
                        <surname>Colina</surname>
                        <given-names>Javier</given-names>
                      </name>
                    </contrib>
                </contrib-group>
                </article-meta>
            </front>
            </article>
            """
        xml_tree = get_xml_tree(xml_str)
        obtained = ArticleDoiValidation(xml_tree).validate_doi_registered(
            callable_get_data_ok
        )

        expected = [
            {
                'title': 'Article DOI is registered (lang: en, element: doi)',
                'xpath': './article-id[@pub-id-type="doi"]',
                'validation_type': 'exist',
                'response': 'ERROR',
                'expected_value': '10.1590/2176-4573e59270',
                'got_value': '10.1590/2176-4573e59271',
                'message': 'Got 10.1590/2176-4573e59271 expected 10.1590/2176-4573e59270',
                'advice': 'DOI not registered or validator not found, provide a value for doi element that '
                          'matches the record for DOI.'
            },
            {
                'title': 'Article DOI is registered (lang: en, element: title)',
                'xpath': './article-id[@pub-id-type="doi"]',
                'validation_type': 'exist',
                'response': 'OK',
                'expected_value': 'Title in English',
                'got_value': 'Title in English',
                'message': 'Got Title in English expected Title in English',
                'advice': None
            },
            {
                'title': 'Article DOI is registered (lang: en, element: author)',
                'xpath': './article-id[@pub-id-type="doi"]',
                'validation_type': 'exist',
                'response': 'ERROR',
                'expected_value': 'Martínez-Momblán, Maria Antonia',
                'got_value': 'Martínez, Maria Antonia',
                'message': 'Got Martínez, Maria Antonia expected Martínez-Momblán, Maria Antonia',
                'advice': 'DOI not registered or validator not found, provide a value for author element that '
                          'matches the record for DOI.'
            },
            {
                'title': 'Article DOI is registered (lang: en, element: author)',
                'xpath': './article-id[@pub-id-type="doi"]',
                'validation_type': 'exist',
                'response': 'ERROR',
                'expected_value': 'Colina-Torralva, Javier',
                'got_value': 'Colina, Javier',
                'message': 'Got Colina, Javier expected Colina-Torralva, Javier',
                'advice': 'DOI not registered or validator not found, provide a value for author element that '
                          'matches the record for DOI.'
            }
        ]
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

    def test_validate_doi_registered_only_one_author_is_correct(self):
        self.maxDiff = None
        xml_str = """
            <article xml:lang="en">
            <front>
                <article-meta>
                <article-id pub-id-type="doi">10.1590/2176-4573e59271</article-id>
                <title-group>
                    <article-title>Title English</article-title>
                </title-group>
                <contrib-group>
                    <contrib contrib-type="author">
                      <name>
                        <surname>Martínez</surname>
                        <given-names>Maria Antonia</given-names>
                      </name>
                    </contrib>
                    <contrib contrib-type="author">
                      <name>
                        <surname>Colina-Torralva</surname>
                        <given-names>Javier</given-names>
                      </name>
                    </contrib>
                </contrib-group>
                </article-meta>
            </front>
            </article>
            """
        xml_tree = get_xml_tree(xml_str)
        obtained = ArticleDoiValidation(xml_tree).validate_doi_registered(
            callable_get_data_ok
        )

        expected = [
            {
                'title': 'Article DOI is registered (lang: en, element: doi)',
                'xpath': './article-id[@pub-id-type="doi"]',
                'validation_type': 'exist',
                'response': 'ERROR',
                'expected_value': '10.1590/2176-4573e59270',
                'got_value': '10.1590/2176-4573e59271',
                'message': 'Got 10.1590/2176-4573e59271 expected 10.1590/2176-4573e59270',
                'advice': 'DOI not registered or validator not found, provide a value for doi element that '
                          'matches the record for DOI.'
            },
            {
                'title': 'Article DOI is registered (lang: en, element: title)',
                'xpath': './article-id[@pub-id-type="doi"]',
                'validation_type': 'exist',
                'response': 'ERROR',
                'expected_value': 'Title in English',
                'got_value': 'Title English',
                'message': 'Got Title English expected Title in English',
                'advice': 'DOI not registered or validator not found, provide a value for title element that '
                          'matches the record for DOI.'
            },
            {
                'title': 'Article DOI is registered (lang: en, element: author)',
                'xpath': './article-id[@pub-id-type="doi"]',
                'validation_type': 'exist',
                'response': 'ERROR',
                'expected_value': 'Martínez-Momblán, Maria Antonia',
                'got_value': 'Martínez, Maria Antonia',
                'message': 'Got Martínez, Maria Antonia expected Martínez-Momblán, Maria Antonia',
                'advice': 'DOI not registered or validator not found, provide a value for author element that '
                          'matches the record for DOI.'
            },
            {
                'title': 'Article DOI is registered (lang: en, element: author)',
                'xpath': './article-id[@pub-id-type="doi"]',
                'validation_type': 'exist',
                'response': 'OK',
                'expected_value': 'Colina-Torralva, Javier',
                'got_value': 'Colina-Torralva, Javier',
                'message': 'Got Colina-Torralva, Javier expected Colina-Torralva, Javier',
                'advice': None
            }
        ]
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

    def test_validate_doi_registered_no_expected_authors(self):
        self.maxDiff = None
        xml_str = """
            <article xml:lang="en">
            <front>
                <article-meta>
                <article-id pub-id-type="doi">10.1590/2176-4573e59270</article-id>
                <title-group>
                    <article-title>Title in English</article-title>
                </title-group>
                <contrib-group>
                    <contrib contrib-type="author">
                      <name>
                        <surname>Martínez-Momblán</surname>
                        <given-names>Maria Antonia</given-names>
                      </name>
                    </contrib>
                    <contrib contrib-type="author">
                      <name>
                        <surname>Colina-Torralva</surname>
                        <given-names>Javier</given-names>
                      </name>
                    </contrib>
                </contrib-group>
                </article-meta>
            </front>
            </article>
            """
        xml_tree = get_xml_tree(xml_str)
        obtained = ArticleDoiValidation(xml_tree).validate_doi_registered(
            callable_get_data_missing_authors
        )

        expected = [
            {
                'title': 'Article DOI is registered (lang: en, element: doi)',
                'xpath': './article-id[@pub-id-type="doi"]',
                'validation_type': 'exist',
                'response': 'OK',
                'expected_value': '10.1590/2176-4573e59270',
                'got_value': '10.1590/2176-4573e59270',
                'message': 'Got 10.1590/2176-4573e59270 expected 10.1590/2176-4573e59270',
                'advice': None
            },
            {
                'title': 'Article DOI is registered (lang: en, element: title)',
                'xpath': './article-id[@pub-id-type="doi"]',
                'validation_type': 'exist',
                'response': 'OK',
                'expected_value': 'Title in English',
                'got_value': 'Title in English',
                'message': 'Got Title in English expected Title in English',
                'advice': None
            },
            {
                'title': 'Article DOI is registered (lang: en, element: authors)',
                'xpath': './article-id[@pub-id-type="doi"]',
                'validation_type': 'exist',
                'response': 'ERROR',
                'expected_value': [],
                'got_value': ['Martínez-Momblán, Maria Antonia', 'Colina-Torralva, Javier'],
                'message': 'The following items are surplus in the XML: Martínez-Momblán, Maria Antonia | Colina-Torralva, Javier',
                'advice': 'Remove the following items from the XML: Martínez-Momblán, Maria Antonia | Colina-Torralva, Javier',
            }
        ]
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

    def test_validate_doi_registered_no_obtained_authors(self):
        self.maxDiff = None
        xml_str = """
            <article xml:lang="en">
            <front>
                <article-meta>
                <article-id pub-id-type="doi">10.1590/2176-4573e59270</article-id>
                <title-group>
                    <article-title>Title in English</article-title>
                </title-group>
                </article-meta>
            </front>
            </article>
            """
        xml_tree = get_xml_tree(xml_str)
        obtained = ArticleDoiValidation(xml_tree).validate_doi_registered(
            callable_get_data_ok
        )

        expected = [
            {
                'title': 'Article DOI is registered (lang: en, element: doi)',
                'xpath': './article-id[@pub-id-type="doi"]',
                'validation_type': 'exist',
                'response': 'OK',
                'expected_value': '10.1590/2176-4573e59270',
                'got_value': '10.1590/2176-4573e59270',
                'message': 'Got 10.1590/2176-4573e59270 expected 10.1590/2176-4573e59270',
                'advice': None
            },
            {
                'title': 'Article DOI is registered (lang: en, element: title)',
                'xpath': './article-id[@pub-id-type="doi"]',
                'validation_type': 'exist',
                'response': 'OK',
                'expected_value': 'Title in English',
                'got_value': 'Title in English',
                'message': 'Got Title in English expected Title in English',
                'advice': None
            },
            {
                'title': 'Article DOI is registered (lang: en, element: authors)',
                'xpath': './article-id[@pub-id-type="doi"]',
                'validation_type': 'exist',
                'response': 'ERROR',
                'expected_value': ['Martínez-Momblán, Maria Antonia', 'Colina-Torralva, Javier'],
                'got_value': [],
                'message': 'The following items are not found in the XML: Martínez-Momblán, Maria Antonia | Colina-Torralva, Javier',
                'advice': 'Complete the following items in the XML: Martínez-Momblán, Maria Antonia | Colina-Torralva, Javier',
            }
        ]
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

    def test_validate_doi_registered_expected_one_author_obtained_two_authors(self):
        self.maxDiff = None
        xml_str = """
            <article xml:lang="en">
            <front>
                <article-meta>
                <article-id pub-id-type="doi">10.1590/2176-4573e59270</article-id>
                <title-group>
                    <article-title>Title in English</article-title>
                </title-group>
                <contrib-group>
                    <contrib contrib-type="author">
                      <name>
                        <surname>Martínez-Momblán</surname>
                        <given-names>Maria Antonia</given-names>
                      </name>
                    </contrib>
                    <contrib contrib-type="author">
                      <name>
                        <surname>Colina-Torralva</surname>
                        <given-names>Javier</given-names>
                      </name>
                    </contrib>
                </contrib-group>
                </article-meta>
            </front>  
            </article>
            """
        xml_tree = get_xml_tree(xml_str)
        obtained = ArticleDoiValidation(xml_tree).validate_doi_registered(
            callable_get_data_one_author
        )

        expected = [
            {
                'title': 'Article DOI is registered (lang: en, element: doi)',
                'xpath': './article-id[@pub-id-type="doi"]',
                'validation_type': 'exist',
                'response': 'OK',
                'expected_value': '10.1590/2176-4573e59270',
                'got_value': '10.1590/2176-4573e59270',
                'message': 'Got 10.1590/2176-4573e59270 expected 10.1590/2176-4573e59270',
                'advice': None
            },
            {
                'title': 'Article DOI is registered (lang: en, element: title)',
                'xpath': './article-id[@pub-id-type="doi"]',
                'validation_type': 'exist',
                'response': 'OK',
                'expected_value': 'Title in English',
                'got_value': 'Title in English',
                'message': 'Got Title in English expected Title in English',
                'advice': None
            },
            {
                'title': 'Article DOI is registered (lang: en, element: author)',
                'xpath': './article-id[@pub-id-type="doi"]',
                'validation_type': 'exist',
                'response': 'ERROR',
                'expected_value': 'Colina-Torralva, Javier',
                'got_value': 'Martínez-Momblán, Maria Antonia',
                'message': 'Got Martínez-Momblán, Maria Antonia expected Colina-Torralva, Javier',
                'advice': 'DOI not registered or validator not found, provide a value for author element that '
                          'matches the record for DOI.',
            },
            {
                'title': 'Article DOI is registered (lang: en, element: authors)',
                'xpath': './article-id[@pub-id-type="doi"]',
                'validation_type': 'exist',
                'response': 'ERROR',
                'expected_value': ['Colina-Torralva, Javier'],
                'got_value': ['Martínez-Momblán, Maria Antonia', 'Colina-Torralva, Javier'],
                'message': 'The following items are surplus in the XML: Colina-Torralva, Javier',
                'advice': 'Remove the following items from the XML: Colina-Torralva, Javier',
            }
        ]
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)


if __name__ == '__main__':
    unittest.main()
