import unittest

from packtools.sps.utils.xml_utils import get_xml_tree

from packtools.sps.validation.article_doi import ArticleDoiValidation


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
        expected = {
            'title': 'Article DOI element',
            'xpath': './article-id[@pub-id-type="doi"]',
            'validation_type': 'exist',
            'response': 'OK',
            'expected_value': '10.1590/1518-8345.2927.3231',
            'got_value': '10.1590/1518-8345.2927.3231',
            'message': 'Got 10.1590/1518-8345.2927.3231 expected 10.1590/1518-8345.2927.3231',
            'advice': None
        }
        self.assertDictEqual(obtained, expected)

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
        expected = {
            'title': 'Article DOI element',
            'xpath': './article-id[@pub-id-type="doi"]',
            'validation_type': 'exist',
            'response': 'ERROR',
            'expected_value': 'article DOI',
            'got_value': None,
            'message': 'Got None expected a DOI',
            'advice': 'Provide a valid DOI for the research-article'
        }
        self.assertDictEqual(obtained, expected)

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
                'advice': 'Provide a valid DOI for the sub-article translation (s3) which language is es'
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
                'advice': 'Provide a valid DOI for the sub-article translation (s2) which language is fr'
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

        expected = {
            'title': 'Article DOI element is unique',
            'xpath': './article-id[@pub-id-type="doi"]',
            'validation_type': 'exist/verification',
            'response': 'OK',
            'expected_value': 'Unique DOI values',
            'got_value': 'DOIs identified: 10.1590/2176-4573p59270 | 10.1590/2176-4573e59270',
            'message': "Got DOIs and frequencies ('10.1590/2176-4573p59270', 1) | ('10.1590/2176-4573e59270', 1)",
            'advice': None
        }
        self.assertDictEqual(obtained, expected)

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

        expected = {
            'title': 'Article DOI element is unique',
            'xpath': './article-id[@pub-id-type="doi"]',
            'validation_type': 'exist/verification',
            'response': 'ERROR',
            'expected_value': 'Unique DOI values',
            'got_value': 'DOIs identified: 10.1590/2176-4573p59270 | 10.1590/2176-4573e59270',
            'message': "Got DOIs and frequencies ('10.1590/2176-4573p59270', 1) | ('10.1590/2176-4573e59270', 3)",
            'advice': 'Consider replacing the following DOIs that are not unique: 10.1590/2176-4573e59270'
        }
        self.assertDictEqual(obtained, expected)


if __name__ == '__main__':
    unittest.main()
