from unittest import TestCase
from lxml import etree

from packtools.sps.validation.journal_meta import ISSNValidation, AcronymValidation, TitleValidation, \
    PublisherNameValidation, JournalMetaValidation, JournalIdValidation


class ISSNTest(TestCase):
    def setUp(self):
        self.xmltree = etree.fromstring(
            """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="en">
                <front>
                    <journal-meta>
                        <issn pub-type="ppub">0103-5053</issn>
                        <issn pub-type="epub">1678-4790</issn>
                    </journal-meta>
                </front>
            </article>
            """
        )
        self.issns = ISSNValidation(self.xmltree)

    def test_validate_issn_ok(self):
        self.maxDiff = None
        obtained = self.issns.validate_issn(
            {
                'ppub': '0103-5053',
                'epub': '1678-4790'
            }
        )

        expected = [
            {
                'title': 'Journal ISSN element validation',
                'xpath': './/journal-meta//issn[@pub-type="ppub"]',
                'validation_type': 'value',
                'response': 'OK',
                'expected_value': '<issn pub-type="ppub">0103-5053</issn>',
                'got_value': '<issn pub-type="ppub">0103-5053</issn>',
                'message': 'Got <issn pub-type="ppub">0103-5053</issn> expected <issn pub-type="ppub">0103-5053</issn>',
                'advice': None
            },
            {
                'title': 'Journal ISSN element validation',
                'xpath': './/journal-meta//issn[@pub-type="epub"]',
                'validation_type': 'value',
                'response': 'OK',
                'expected_value': '<issn pub-type="epub">1678-4790</issn>',
                'got_value': '<issn pub-type="epub">1678-4790</issn>',
                'message': 'Got <issn pub-type="epub">1678-4790</issn> expected <issn pub-type="epub">1678-4790</issn>',
                'advice': None
            }
        ]
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

    def test_validate_issn_not_ok(self):
        self.maxDiff = None
        obtained = self.issns.validate_issn(
            {
                'ppub': '0103-5054',
                'epub': '1678-4791'
            }
        )

        expected = [
            {
                'title': 'Journal ISSN element validation',
                'xpath': './/journal-meta//issn[@pub-type="ppub"]',
                'validation_type': 'value',
                'response': 'ERROR',
                'expected_value': '<issn pub-type="ppub">0103-5054</issn>',
                'got_value': '<issn pub-type="ppub">0103-5053</issn>',
                'message': 'Got <issn pub-type="ppub">0103-5053</issn> expected <issn pub-type="ppub">0103-5054</issn>',
                'advice': 'Provide an ISSN value as expected: <issn pub-type="ppub">0103-5054</issn>'
            },
            {
                'title': 'Journal ISSN element validation',
                'xpath': './/journal-meta//issn[@pub-type="epub"]',
                'validation_type': 'value',
                'response': 'ERROR',
                'expected_value': '<issn pub-type="epub">1678-4791</issn>',
                'got_value': '<issn pub-type="epub">1678-4790</issn>',
                'message': 'Got <issn pub-type="epub">1678-4790</issn> expected <issn pub-type="epub">1678-4791</issn>',
                'advice': 'Provide an ISSN value as expected: <issn pub-type="epub">1678-4791</issn>'
            }
        ]
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)


class AcronymTest(TestCase):
    def setUp(self):
        self.xmltree = etree.fromstring(
            """
            <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink" 
            article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="pt">
                <front>
                    <journal-meta>
                        <journal-id journal-id-type="nlm-ta">Hist Cienc Saude Manguinhos</journal-id>
                        <journal-id journal-id-type="publisher-id">hcsm</journal-id>
                    </journal-meta>
                </front>
            </article>
            """
        )
        self.acronym = AcronymValidation(self.xmltree)

    def test_acronym_validation_success(self):
        self.maxDiff = None
        expected = [
            {
                'title': 'Journal acronym element validation',
                'xpath': './/journal-meta//journal-id[@journal-id-type="publisher-id"]',
                'validation_type': 'value',
                'response': 'OK',
                'expected_value': 'hcsm',
                'got_value': 'hcsm',
                'message': 'Got hcsm expected hcsm',
                'advice': None
            }
        ]
        obtained = self.acronym.acronym_validation('hcsm')
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

    def test_acronym_validation_fail(self):
        self.maxDiff = None
        expected = [
            {
                'title': 'Journal acronym element validation',
                'xpath': './/journal-meta//journal-id[@journal-id-type="publisher-id"]',
                'validation_type': 'value',
                'response': 'ERROR',
                'expected_value': 'hcs',
                'got_value': 'hcsm',
                'message': 'Got hcsm expected hcs',
                'advice': 'Provide an acronym value as expected: hcs'
            }
        ]
        obtained = self.acronym.acronym_validation('hcs')
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)


class TitleTest(TestCase):
    def setUp(self):
        self.xmltree = etree.fromstring(
            """
            <!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.1 20151215//EN" 
            "https://jats.nlm.nih.gov/publishing/1.1/JATS-journalpublishing1.dtd">
                <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink" 
                article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="pt">
                    <front>
                        <journal-meta>
                            <journal-title-group>
                                <journal-title>História, Ciências, Saúde-Manguinhos</journal-title>
                                <abbrev-journal-title abbrev-type="publisher">Hist. cienc. saude-Manguinhos</abbrev-journal-title>
                            </journal-title-group>
                        </journal-meta>
                    </front>
                </article>
            """
        )
        self.title = TitleValidation(self.xmltree)

    def test_journal_title_validation_success(self):
        self.maxDiff = None
        expected = [
            {
                'title': 'Journal title element validation',
                'xpath': './journal-meta/journal-title-group/journal-title',
                'validation_type': 'value',
                'response': 'OK',
                'expected_value': 'História, Ciências, Saúde-Manguinhos',
                'got_value': 'História, Ciências, Saúde-Manguinhos',
                'message': 'Got História, Ciências, Saúde-Manguinhos expected História, Ciências, Saúde-Manguinhos',
                'advice': None
            }
        ]
        obtained = self.title.journal_title_validation('História, Ciências, Saúde-Manguinhos')
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

    def test_journal_title_validation_fail(self):
        self.maxDiff = None
        expected = [
            {
                'title': 'Journal title element validation',
                'xpath': './journal-meta/journal-title-group/journal-title',
                'validation_type': 'value',
                'response': 'ERROR',
                'expected_value': 'História, Ciências, Saúde Manguinhos',
                'got_value': 'História, Ciências, Saúde-Manguinhos',
                'message': 'Got História, Ciências, Saúde-Manguinhos expected História, Ciências, Saúde Manguinhos',
                'advice': 'Provide a journal title value as expected: História, Ciências, Saúde Manguinhos'
            }
        ]
        obtained = self.title.journal_title_validation('História, Ciências, Saúde Manguinhos')
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

    def test_abbreviated_journal_title_validation_success(self):
        self.maxDiff = None
        expected = [
            {
                'title': 'Abbreviated journal title element validation',
                'parent': 'article',
                'parent_article_type': 'research-article',
                'parent_id': None,
                'parent_lang': 'pt',
                'item': 'journal-title-group',
                'sub_item': 'abbrev-journal-title',
                'validation_type': 'value',
                'response': 'OK',
                'expected_value': 'Hist. cienc. saude-Manguinhos',
                'got_value': 'Hist. cienc. saude-Manguinhos',
                'message': 'Got Hist. cienc. saude-Manguinhos, expected Hist. cienc. saude-Manguinhos',
                'advice': None,
                'data': {
                    'main': 'História, Ciências, Saúde-Manguinhos',
                    'abbreviated': 'Hist. cienc. saude-Manguinhos'
                },
            }
        ]
        obtained = list(self.title.abbreviated_journal_title_validation('Hist. cienc. saude-Manguinhos'))
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

    def test_abbreviated_journal_title_validation_fail(self):
        self.maxDiff = None
        expected = [
            {
                'title': 'Abbreviated journal title element validation',
                'parent': 'article',
                'parent_article_type': 'research-article',
                'parent_id': None,
                'parent_lang': 'pt',
                'item': 'journal-title-group',
                'sub_item': 'abbrev-journal-title',
                'validation_type': 'value',
                'response': 'CRITICAL',
                'expected_value': 'Hist. cienc. saude Manguinhos',
                'got_value': 'Hist. cienc. saude-Manguinhos',
                'message': 'Got Hist. cienc. saude-Manguinhos, expected Hist. cienc. saude Manguinhos',
                'advice': 'Provide a journal title value as expected: Hist. cienc. saude Manguinhos',
                'data': {
                    'main': 'História, Ciências, Saúde-Manguinhos',
                    'abbreviated': 'Hist. cienc. saude-Manguinhos'
                },
            }
        ]
        obtained = list(self.title.abbreviated_journal_title_validation('Hist. cienc. saude Manguinhos'))
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)


class PublisherTest(TestCase):
    def setUp(self):
        self.xmltree_one_publisher = etree.fromstring(
            """
            <!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.1 20151215//EN" 
            "https://jats.nlm.nih.gov/publishing/1.1/JATS-journalpublishing1.dtd">
                <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink" 
                article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="pt">
                    <front>
                        <journal-meta>
                            <publisher>
                                <publisher-name>Fundação Oswaldo Cruz</publisher-name>
                            </publisher>
                        </journal-meta>
                    </front>
                </article>
            """
        )
        self.xmltree_more_than_one_publisher = etree.fromstring(
            """
            <!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.1 20151215//EN" 
            "https://jats.nlm.nih.gov/publishing/1.1/JATS-journalpublishing1.dtd">
                <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink" 
                article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="pt">
                    <front>
                        <journal-meta>
                            <publisher>
                                <publisher-name>Fundação Oswaldo Cruz</publisher-name>
                                <publisher-name>UNESP</publisher-name>
                            </publisher>
                        </journal-meta>
                    </front>
                </article>
            """
        )
        self.one_publisher = PublisherNameValidation(self.xmltree_one_publisher)
        self.more_than_one_publisher = PublisherNameValidation(self.xmltree_more_than_one_publisher)

    def test_validate_publisher_names_one_success(self):
        self.maxDiff = None
        expected = [
            {
                'title': 'Publisher name element validation',
                'parent': 'article',
                'parent_article_type': 'research-article',
                'parent_id': None,
                'parent_lang': 'pt',
                'item': 'publisher',
                'sub_item': 'publisher-name',
                'validation_type': 'value',
                'response': 'OK',
                'expected_value': 'Fundação Oswaldo Cruz',
                'got_value': 'Fundação Oswaldo Cruz',
                'message': 'Got Fundação Oswaldo Cruz, expected Fundação Oswaldo Cruz',
                'advice': None,
                'data': None,
            }
        ]
        obtained = list(self.one_publisher.validate_publisher_names(['Fundação Oswaldo Cruz']))
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

    def test_validate_publisher_names_one_fail(self):
        self.maxDiff = None
        expected = [
            {
                'title': 'Publisher name element validation',
                'parent': 'article',
                'parent_article_type': 'research-article',
                'parent_id': None,
                'parent_lang': 'pt',
                'item': 'publisher',
                'sub_item': 'publisher-name',
                'validation_type': 'value',
                'response': 'CRITICAL',
                'expected_value': 'Fund. Oswaldo Cruz',
                'got_value': 'Fundação Oswaldo Cruz',
                'message': 'Got Fundação Oswaldo Cruz, expected Fund. Oswaldo Cruz',
                'advice': 'Provide the expected publisher name: Fund. Oswaldo Cruz',
                'data': None,
            }
        ]
        obtained = list(self.one_publisher.validate_publisher_names(['Fund. Oswaldo Cruz']))
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

    def test_validate_publisher_names_more_than_one_sucess(self):
        self.maxDiff = None
        expected = [
            {
                'title': 'Publisher name element validation',
                'parent': 'article',
                'parent_article_type': 'research-article',
                'parent_id': None,
                'parent_lang': 'pt',
                'item': 'publisher',
                'sub_item': 'publisher-name',
                'validation_type': 'value',
                'response': 'OK',
                'expected_value': 'Fundação Oswaldo Cruz',
                'got_value': 'Fundação Oswaldo Cruz',
                'message': 'Got Fundação Oswaldo Cruz, expected Fundação Oswaldo Cruz',
                'advice': None,
                'data': None,
            },
            {
                'title': 'Publisher name element validation',
                'parent': 'article',
                'parent_article_type': 'research-article',
                'parent_id': None,
                'parent_lang': 'pt',
                'item': 'publisher',
                'sub_item': 'publisher-name',
                'validation_type': 'value',
                'response': 'OK',
                'expected_value': 'UNESP',
                'got_value': 'UNESP',
                'message': 'Got UNESP, expected UNESP',
                'advice': None,
                'data': None,
            }
        ]
        obtained = list(self.more_than_one_publisher.validate_publisher_names(['Fundação Oswaldo Cruz', 'UNESP']))
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

    def test_validate_publisher_names_more_than_one_fail(self):
        self.maxDiff = None
        expected = [
            {
                'title': 'Publisher name element validation',
                'parent': 'article',
                'parent_article_type': 'research-article',
                'parent_id': None,
                'parent_lang': 'pt',
                'item': 'publisher',
                'sub_item': 'publisher-name',
                'validation_type': 'value',
                'response': 'CRITICAL',
                'expected_value': 'Fund. Oswaldo Cruz',
                'got_value': 'Fundação Oswaldo Cruz',
                'message': 'Got Fundação Oswaldo Cruz, expected Fund. Oswaldo Cruz',
                'advice': 'Provide the expected publisher name: Fund. Oswaldo Cruz',
                'data': None,
            },
            {
                'title': 'Publisher name element validation',
                'parent': 'article',
                'parent_article_type': 'research-article',
                'parent_id': None,
                'parent_lang': 'pt',
                'item': 'publisher',
                'sub_item': 'publisher-name',
                'validation_type': 'value',
                'response': 'CRITICAL',
                'expected_value': 'UNIFESP',
                'got_value': 'UNESP',
                'message': 'Got UNESP, expected UNIFESP',
                'advice': 'Provide the expected publisher name: UNIFESP',
                'data': None,
            }
        ]
        obtained = list(self.more_than_one_publisher.validate_publisher_names(['Fund. Oswaldo Cruz', 'UNIFESP']))
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

    def test_validate_publisher_names_XML_has_not_expected_items(self):
        self.maxDiff = None
        expected = [
            {
                'title': 'Publisher name element validation',
                'parent': 'article',
                'parent_article_type': 'research-article',
                'parent_id': None,
                'parent_lang': 'pt',
                'item': 'publisher',
                'sub_item': 'publisher-name',
                'validation_type': 'value',
                'response': 'OK',
                'expected_value': 'Fundação Oswaldo Cruz',
                'got_value': 'Fundação Oswaldo Cruz',
                'message': 'Got Fundação Oswaldo Cruz, expected Fundação Oswaldo Cruz',
                'advice': None,
                'data': None,
            },
            {
                'title': 'Publisher name element validation',
                'parent': 'article',
                'parent_article_type': 'research-article',
                'parent_id': None,
                'parent_lang': 'pt',
                'item': 'publisher',
                'sub_item': 'publisher-name',
                'validation_type': 'value',
                'response': 'CRITICAL',
                'expected_value': ['Fundação Oswaldo Cruz'],
                'got_value': ['Fundação Oswaldo Cruz', 'UNESP'],
                'message': "Got ['Fundação Oswaldo Cruz', 'UNESP'], expected ['Fundação Oswaldo Cruz']",
                'advice': 'Remove the following items from the XML: UNESP',
                'data': None,
            }
        ]
        obtained = list(self.more_than_one_publisher.validate_publisher_names(['Fundação Oswaldo Cruz']))
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

    def test_validate_publisher_names_function_has_not_expected_items(self):
        self.maxDiff = None
        expected = [
            {
                'title': 'Publisher name element validation',
                'parent': 'article',
                'parent_article_type': 'research-article',
                'parent_id': None,
                'parent_lang': 'pt',
                'item': 'publisher',
                'sub_item': 'publisher-name',
                'validation_type': 'value',
                'response': 'OK',
                'expected_value': 'Fundação Oswaldo Cruz',
                'got_value': 'Fundação Oswaldo Cruz',
                'message': 'Got Fundação Oswaldo Cruz, expected Fundação Oswaldo Cruz',
                'advice': None,
                'data': None,
            },
            {
                'title': 'Publisher name element validation',
                'parent': 'article',
                'parent_article_type': 'research-article',
                'parent_id': None,
                'parent_lang': 'pt',
                'item': 'publisher',
                'sub_item': 'publisher-name',
                'validation_type': 'value',
                'response': 'CRITICAL',
                'expected_value': ['Fundação Oswaldo Cruz', 'UNESP'],
                'got_value': ['Fundação Oswaldo Cruz'],
                'message': "Got ['Fundação Oswaldo Cruz'], expected ['Fundação Oswaldo Cruz', 'UNESP']",
                'advice': 'Complete the following items in the XML: UNESP',
                'data': None,
            }
        ]
        obtained = list(self.one_publisher.validate_publisher_names(['Fundação Oswaldo Cruz', 'UNESP']))
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)


class JournalIdValidationTest(TestCase):
    def setUp(self):
        self.xmltree = etree.fromstring(
            """
            <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink" 
            article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="pt">
                <front>
                    <journal-meta>
                        <journal-id journal-id-type="nlm-ta">Rev Saude Publica</journal-id>
                    </journal-meta>
                </front>
            </article>
            """
        )

    def test_nlm_ta_id_validation_success(self):
        self.maxDiff = None
        expected = [
            {
                'title': 'Journal ID element validation',
                'parent': 'article',
                'parent_article_type': "research-article",
                'parent_id': None,
                'parent_lang': 'pt',
                'item': 'journal-meta',
                'sub_item': 'journal-id',
                'validation_type': 'value',
                'response': 'OK',
                'expected_value': 'Rev Saude Publica',
                'got_value': 'Rev Saude Publica',
                'message': 'Got Rev Saude Publica, expected Rev Saude Publica',
                'advice': None,
                'data': None,
            }
        ]
        obtained = list(JournalIdValidation(self.xmltree).nlm_ta_id_validation('Rev Saude Publica'))
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

    def test_nlm_ta_id_validation_fail(self):
        self.maxDiff = None
        expected = [
            {
                'title': 'Journal ID element validation',
                'parent': 'article',
                'parent_article_type': "research-article",
                'parent_id': None,
                'parent_lang': "pt",
                'item': 'journal-meta',
                'sub_item': 'journal-id',
                'validation_type': 'value',
                'response': 'CRITICAL',
                'expected_value': 'Rev de Saude Publica',
                'got_value': 'Rev Saude Publica',
                'message': 'Got Rev Saude Publica, expected Rev de Saude Publica',
                'advice': 'Provide an nlm-ta value as expected: Rev de Saude Publica',
                'data': None,
            }
        ]
        obtained = list(JournalIdValidation(self.xmltree).nlm_ta_id_validation('Rev de Saude Publica'))
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)


class JournalMetaValidationTest(TestCase):
    def setUp(self):
        self.xmltree = etree.fromstring(
            """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="en">
                <front>
                    <journal-meta>
                        <issn pub-type="ppub">0103-5053</issn>
                        <issn pub-type="epub">1678-4790</issn>
                        <journal-id journal-id-type="nlm-ta">Rev Saude Publica</journal-id>
                        <journal-id journal-id-type="publisher-id">hcsm</journal-id>
                        <journal-title-group>
                                <journal-title>História, Ciências, Saúde-Manguinhos</journal-title>
                                <abbrev-journal-title abbrev-type="publisher">Hist. cienc. saude-Manguinhos</abbrev-journal-title>
                        </journal-title-group>
                        <publisher>
                                <publisher-name>Casa de Oswaldo Cruz, Fundação Oswaldo Cruz</publisher-name>
                        </publisher>
                    </journal-meta>
                </front>
            </article>
            """
        )
        self.journal_meta = JournalMetaValidation(self.xmltree)

    def test_journal_meta_match(self):
        self.maxDiff = None
        expected = [
            {
                'title': 'Journal ISSN element validation',
                'xpath': './/journal-meta//issn[@pub-type="ppub"]',
                'validation_type': 'value',
                'response': 'OK',
                'expected_value': '<issn pub-type="ppub">0103-5053</issn>',
                'got_value': '<issn pub-type="ppub">0103-5053</issn>',
                'message': 'Got <issn pub-type="ppub">0103-5053</issn> expected <issn pub-type="ppub">0103-5053</issn>',
                'advice': None
            },
            {
                'title': 'Journal ISSN element validation',
                'xpath': './/journal-meta//issn[@pub-type="epub"]',
                'validation_type': 'value',
                'response': 'OK',
                'expected_value': '<issn pub-type="epub">1678-4790</issn>',
                'got_value': '<issn pub-type="epub">1678-4790</issn>',
                'message': 'Got <issn pub-type="epub">1678-4790</issn> expected <issn pub-type="epub">1678-4790</issn>',
                'advice': None
            },
            {
                'title': 'Journal acronym element validation',
                'xpath': './/journal-meta//journal-id[@journal-id-type="publisher-id"]',
                'validation_type': 'value',
                'response': 'OK',
                'expected_value': 'hcsm',
                'got_value': 'hcsm',
                'message': 'Got hcsm expected hcsm',
                'advice': None
            },
            {
                'title': 'Journal title element validation',
                'xpath': './journal-meta/journal-title-group/journal-title',
                'validation_type': 'value',
                'response': 'OK',
                'expected_value': 'História, Ciências, Saúde-Manguinhos',
                'got_value': 'História, Ciências, Saúde-Manguinhos',
                'message': 'Got História, Ciências, Saúde-Manguinhos expected História, Ciências, Saúde-Manguinhos',
                'advice': None
            },
            {
                'title': 'Abbreviated journal title element validation',
                'parent': 'article',
                'parent_article_type': 'research-article',
                'parent_id': None,
                'parent_lang': 'en',
                'item': 'journal-title-group',
                'sub_item': 'abbrev-journal-title',
                'validation_type': 'value',
                'response': 'OK',
                'expected_value': 'Hist. cienc. saude-Manguinhos',
                'got_value': 'Hist. cienc. saude-Manguinhos',
                'message': 'Got Hist. cienc. saude-Manguinhos, expected Hist. cienc. saude-Manguinhos',
                'advice': None,
                'data': {
                    'main': 'História, Ciências, Saúde-Manguinhos',
                    'abbreviated': 'Hist. cienc. saude-Manguinhos'
                },
            },
            {
                'title': 'Publisher name element validation',
                'parent': 'article',
                'parent_article_type': 'research-article',
                'parent_id': None,
                'parent_lang': 'en',
                'item': 'publisher',
                'sub_item': 'publisher-name',
                'validation_type': 'value',
                'response': 'OK',
                'expected_value': 'Casa de Oswaldo Cruz, Fundação Oswaldo Cruz',
                'got_value': 'Casa de Oswaldo Cruz, Fundação Oswaldo Cruz',
                'message': 'Got Casa de Oswaldo Cruz, Fundação Oswaldo Cruz, expected Casa de Oswaldo Cruz, Fundação Oswaldo Cruz',
                'advice': None,
                'data': None,
            },
            {
                'title': 'Journal ID element validation',
                'parent': 'article',
                'parent_article_type': 'research-article',
                'parent_id': None,
                'parent_lang': "en",
                'item': 'journal-meta',
                'sub_item': 'journal-id',
                'validation_type': 'value',
                'response': 'OK',
                'expected_value': 'Rev Saude Publica',
                'got_value': 'Rev Saude Publica',
                'message': 'Got Rev Saude Publica, expected Rev Saude Publica',
                'advice': None,
                'data': None,
            }
        ]
        obtained = list(self.journal_meta.validate({
            'issns': {
                'ppub': '0103-5053',
                'epub': '1678-4790'
            },
            'acronym': 'hcsm',
            'journal-title': 'História, Ciências, Saúde-Manguinhos',
            'abbrev-journal-title': 'Hist. cienc. saude-Manguinhos',
            'publisher-name': ['Casa de Oswaldo Cruz, Fundação Oswaldo Cruz'],
            'nlm-ta': 'Rev Saude Publica'
        }))

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)


class JournalMetaPresenceTest(TestCase):
    """Tests for JournalMetaPresenceValidation class"""
    
    def test_validate_journal_meta_presence_success(self):
        """Test journal-meta presence validation when element exists"""
        xmltree = etree.fromstring(
            """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="en">
                <front>
                    <journal-meta>
                        <journal-id journal-id-type="publisher-id">test</journal-id>
                    </journal-meta>
                </front>
            </article>
            """
        )
        from packtools.sps.validation.journal_meta import JournalMetaPresenceValidation
        validation = JournalMetaPresenceValidation(xmltree)
        result = list(validation.validate_journal_meta_presence())
        
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['response'], 'OK')
        self.assertEqual(result[0]['validation_type'], 'exist')

    def test_validate_journal_meta_presence_failure(self):
        """Test journal-meta presence validation when element is missing"""
        xmltree = etree.fromstring(
            """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="en">
                <front>
                </front>
            </article>
            """
        )
        from packtools.sps.validation.journal_meta import JournalMetaPresenceValidation
        validation = JournalMetaPresenceValidation(xmltree)
        result = list(validation.validate_journal_meta_presence())
        
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['response'], 'CRITICAL')
        self.assertIsNotNone(result[0]['advice'])

    def test_validate_journal_meta_uniqueness_success(self):
        """Test journal-meta uniqueness validation when exactly one exists"""
        xmltree = etree.fromstring(
            """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="en">
                <front>
                    <journal-meta>
                        <journal-id journal-id-type="publisher-id">test</journal-id>
                    </journal-meta>
                </front>
            </article>
            """
        )
        from packtools.sps.validation.journal_meta import JournalMetaPresenceValidation
        validation = JournalMetaPresenceValidation(xmltree)
        result = list(validation.validate_journal_meta_uniqueness())
        
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['response'], 'OK')
        self.assertEqual(result[0]['data']['count'], 1)

    def test_validate_journal_meta_uniqueness_failure_multiple(self):
        """Test journal-meta uniqueness validation when multiple exist"""
        xmltree = etree.fromstring(
            """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="en">
                <front>
                    <journal-meta>
                        <journal-id journal-id-type="publisher-id">test1</journal-id>
                    </journal-meta>
                    <journal-meta>
                        <journal-id journal-id-type="publisher-id">test2</journal-id>
                    </journal-meta>
                </front>
            </article>
            """
        )
        from packtools.sps.validation.journal_meta import JournalMetaPresenceValidation
        validation = JournalMetaPresenceValidation(xmltree)
        result = list(validation.validate_journal_meta_uniqueness())
        
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['response'], 'CRITICAL')
        self.assertEqual(result[0]['data']['count'], 2)

    def test_validate_publisher_id_presence_success(self):
        """Test publisher-id presence validation when element exists"""
        xmltree = etree.fromstring(
            """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="en">
                <front>
                    <journal-meta>
                        <journal-id journal-id-type="publisher-id">bjmbr</journal-id>
                    </journal-meta>
                </front>
            </article>
            """
        )
        from packtools.sps.validation.journal_meta import JournalMetaPresenceValidation
        validation = JournalMetaPresenceValidation(xmltree)
        result = list(validation.validate_publisher_id_presence())
        
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['response'], 'OK')
        self.assertEqual(result[0]['data']['publisher_id'], 'bjmbr')

    def test_validate_publisher_id_presence_failure(self):
        """Test publisher-id presence validation when element is missing"""
        xmltree = etree.fromstring(
            """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="en">
                <front>
                    <journal-meta>
                        <journal-id journal-id-type="nlm-ta">Test</journal-id>
                    </journal-meta>
                </front>
            </article>
            """
        )
        from packtools.sps.validation.journal_meta import JournalMetaPresenceValidation
        validation = JournalMetaPresenceValidation(xmltree)
        result = list(validation.validate_publisher_id_presence())
        
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['response'], 'CRITICAL')

    def test_validate_journal_title_presence_success(self):
        """Test journal-title presence validation when element exists"""
        xmltree = etree.fromstring(
            """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="en">
                <front>
                    <journal-meta>
                        <journal-title-group>
                            <journal-title>Test Journal</journal-title>
                        </journal-title-group>
                    </journal-meta>
                </front>
            </article>
            """
        )
        from packtools.sps.validation.journal_meta import JournalMetaPresenceValidation
        validation = JournalMetaPresenceValidation(xmltree)
        result = list(validation.validate_journal_title_presence())
        
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['response'], 'OK')

    def test_validate_abbrev_journal_title_presence_success(self):
        """Test abbreviated journal title presence validation"""
        xmltree = etree.fromstring(
            """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="en">
                <front>
                    <journal-meta>
                        <journal-title-group>
                            <abbrev-journal-title abbrev-type="publisher">Test J.</abbrev-journal-title>
                        </journal-title-group>
                    </journal-meta>
                </front>
            </article>
            """
        )
        from packtools.sps.validation.journal_meta import JournalMetaPresenceValidation
        validation = JournalMetaPresenceValidation(xmltree)
        result = list(validation.validate_abbrev_journal_title_presence())
        
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['response'], 'OK')

    def test_validate_issn_presence_success(self):
        """Test ISSN presence validation when at least one exists"""
        xmltree = etree.fromstring(
            """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="en">
                <front>
                    <journal-meta>
                        <issn pub-type="epub">1234-5678</issn>
                    </journal-meta>
                </front>
            </article>
            """
        )
        from packtools.sps.validation.journal_meta import JournalMetaPresenceValidation
        validation = JournalMetaPresenceValidation(xmltree)
        result = list(validation.validate_issn_presence())
        
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['response'], 'OK')

    def test_validate_issn_presence_failure(self):
        """Test ISSN presence validation when none exist"""
        xmltree = etree.fromstring(
            """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="en">
                <front>
                    <journal-meta>
                        <journal-id journal-id-type="publisher-id">test</journal-id>
                    </journal-meta>
                </front>
            </article>
            """
        )
        from packtools.sps.validation.journal_meta import JournalMetaPresenceValidation
        validation = JournalMetaPresenceValidation(xmltree)
        result = list(validation.validate_issn_presence())
        
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['response'], 'CRITICAL')

    def test_validate_publisher_name_presence_success(self):
        """Test publisher-name presence validation when element exists"""
        xmltree = etree.fromstring(
            """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="en">
                <front>
                    <journal-meta>
                        <publisher>
                            <publisher-name>Test Publisher</publisher-name>
                        </publisher>
                    </journal-meta>
                </front>
            </article>
            """
        )
        from packtools.sps.validation.journal_meta import JournalMetaPresenceValidation
        validation = JournalMetaPresenceValidation(xmltree)
        result = list(validation.validate_publisher_name_presence())
        
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['response'], 'OK')


class ISSNFormatTest(TestCase):
    """Tests for ISSNFormatValidation class"""
    
    def test_validate_issn_format_valid_standard(self):
        """Test ISSN format validation with valid standard format"""
        xmltree = etree.fromstring(
            """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="en">
                <front>
                    <journal-meta>
                        <issn pub-type="epub">1234-5678</issn>
                        <issn pub-type="ppub">0103-5053</issn>
                    </journal-meta>
                </front>
            </article>
            """
        )
        from packtools.sps.validation.journal_meta import ISSNFormatValidation
        validation = ISSNFormatValidation(xmltree)
        results = list(validation.validate_issn_format())
        
        self.assertEqual(len(results), 2)
        for result in results:
            self.assertEqual(result['response'], 'OK')
            self.assertEqual(result['validation_type'], 'format')

    def test_validate_issn_format_valid_with_x(self):
        """Test ISSN format validation with X as check digit"""
        xmltree = etree.fromstring(
            """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="en">
                <front>
                    <journal-meta>
                        <issn pub-type="epub">1234-567X</issn>
                    </journal-meta>
                </front>
            </article>
            """
        )
        from packtools.sps.validation.journal_meta import ISSNFormatValidation
        validation = ISSNFormatValidation(xmltree)
        results = list(validation.validate_issn_format())
        
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['response'], 'OK')

    def test_validate_issn_format_invalid_no_hyphen(self):
        """Test ISSN format validation with missing hyphen"""
        xmltree = etree.fromstring(
            """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="en">
                <front>
                    <journal-meta>
                        <issn pub-type="epub">12345678</issn>
                    </journal-meta>
                </front>
            </article>
            """
        )
        from packtools.sps.validation.journal_meta import ISSNFormatValidation
        validation = ISSNFormatValidation(xmltree)
        results = list(validation.validate_issn_format())
        
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['response'], 'ERROR')

    def test_validate_issn_format_invalid_wrong_length(self):
        """Test ISSN format validation with wrong length"""
        xmltree = etree.fromstring(
            """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="en">
                <front>
                    <journal-meta>
                        <issn pub-type="epub">123-456</issn>
                    </journal-meta>
                </front>
            </article>
            """
        )
        from packtools.sps.validation.journal_meta import ISSNFormatValidation
        validation = ISSNFormatValidation(xmltree)
        results = list(validation.validate_issn_format())
        
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['response'], 'ERROR')

    def test_validate_issn_format_invalid_lowercase_x(self):
        """Test ISSN format validation rejects lowercase x (must be uppercase X)"""
        xmltree = etree.fromstring(
            """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="en">
                <front>
                    <journal-meta>
                        <issn pub-type="epub">1234-567x</issn>
                    </journal-meta>
                </front>
            </article>
            """
        )
        from packtools.sps.validation.journal_meta import ISSNFormatValidation
        validation = ISSNFormatValidation(xmltree)
        results = list(validation.validate_issn_format())
        
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['response'], 'ERROR')




class JournalMetaAttributeTest(TestCase):
    """Tests for JournalMetaAttributeValidation class"""
    
    def test_validate_journal_id_type_valid(self):
        """Test journal-id-type validation with valid values"""
        xmltree = etree.fromstring(
            """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="en">
                <front>
                    <journal-meta>
                        <journal-id journal-id-type="publisher-id">bjmbr</journal-id>
                        <journal-id journal-id-type="nlm-ta">Rev Test</journal-id>
                    </journal-meta>
                </front>
            </article>
            """
        )
        from packtools.sps.validation.journal_meta import JournalMetaAttributeValidation
        validation = JournalMetaAttributeValidation(xmltree)
        results = list(validation.validate_journal_id_type_values())
        
        self.assertEqual(len(results), 2)
        for result in results:
            self.assertEqual(result['response'], 'OK')

    def test_validate_journal_id_type_invalid(self):
        """Test journal-id-type validation with invalid value"""
        xmltree = etree.fromstring(
            """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="en">
                <front>
                    <journal-meta>
                        <journal-id journal-id-type="invalid-type">test</journal-id>
                    </journal-meta>
                </front>
            </article>
            """
        )
        from packtools.sps.validation.journal_meta import JournalMetaAttributeValidation
        validation = JournalMetaAttributeValidation(xmltree)
        results = list(validation.validate_journal_id_type_values())
        
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['response'], 'ERROR')

    def test_validate_issn_pub_type_valid(self):
        """Test ISSN pub-type validation with valid values"""
        xmltree = etree.fromstring(
            """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="en">
                <front>
                    <journal-meta>
                        <issn pub-type="epub">1234-5678</issn>
                        <issn pub-type="ppub">0103-5053</issn>
                    </journal-meta>
                </front>
            </article>
            """
        )
        from packtools.sps.validation.journal_meta import JournalMetaAttributeValidation
        validation = JournalMetaAttributeValidation(xmltree)
        results = list(validation.validate_issn_pub_type_values())
        
        self.assertEqual(len(results), 2)
        for result in results:
            self.assertEqual(result['response'], 'OK')

    def test_validate_issn_pub_type_invalid(self):
        """Test ISSN pub-type validation with invalid value"""
        xmltree = etree.fromstring(
            """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="en">
                <front>
                    <journal-meta>
                        <issn pub-type="online">1234-5678</issn>
                    </journal-meta>
                </front>
            </article>
            """
        )
        from packtools.sps.validation.journal_meta import JournalMetaAttributeValidation
        validation = JournalMetaAttributeValidation(xmltree)
        results = list(validation.validate_issn_pub_type_values())
        
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['response'], 'ERROR')

    def test_validate_issn_type_uniqueness_success(self):
        """Test ISSN type uniqueness with unique types"""
        xmltree = etree.fromstring(
            """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="en">
                <front>
                    <journal-meta>
                        <issn pub-type="epub">1234-5678</issn>
                        <issn pub-type="ppub">0103-5053</issn>
                    </journal-meta>
                </front>
            </article>
            """
        )
        from packtools.sps.validation.journal_meta import JournalMetaAttributeValidation
        validation = JournalMetaAttributeValidation(xmltree)
        results = list(validation.validate_issn_type_uniqueness())
        
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['response'], 'OK')

    def test_validate_issn_type_uniqueness_failure(self):
        """Test ISSN type uniqueness with duplicate types"""
        xmltree = etree.fromstring(
            """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="en">
                <front>
                    <journal-meta>
                        <issn pub-type="epub">1234-5678</issn>
                        <issn pub-type="epub">8765-4321</issn>
                    </journal-meta>
                </front>
            </article>
            """
        )
        from packtools.sps.validation.journal_meta import JournalMetaAttributeValidation
        validation = JournalMetaAttributeValidation(xmltree)
        results = list(validation.validate_issn_type_uniqueness())
        
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['response'], 'WARNING')
        self.assertIn('epub', results[0]['data']['duplicates'])

    def test_validate_issn_format_invalid_lowercase_x(self):
        """Test ISSN format validation rejects lowercase x (must be uppercase X)"""
