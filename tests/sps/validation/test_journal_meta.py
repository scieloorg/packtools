from unittest import TestCase
from lxml import etree

from packtools.sps.validation.journal_meta import ISSNValidation, AcronymValidation, TitleValidation, \
    PublisherValidation, JournalMetaValidation


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

    def test_acronym_match(self):
        expected = dict(
            object='journal acronym',
            output_expected='hcsm',
            output_obteined='hcsm',
            match=True
        )
        obtained = self.acronym.validate_text('hcsm')
        self.assertDictEqual(expected, obtained)

    def test_acronym_no_match(self):
        expected = dict(
            object='journal acronym',
            output_expected='hcs',
            output_obteined='hcsm',
            match=False
        )
        obtained = self.acronym.validate_text('hcs')
        self.assertDictEqual(expected, obtained)


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

    def test_journal_title_match(self):
        expected = dict(
            object='journal title',
            output_expected='História, Ciências, Saúde-Manguinhos',
            output_obteined='História, Ciências, Saúde-Manguinhos',
            match=True
        )
        obtained = self.title.validate_journal_title('História, Ciências, Saúde-Manguinhos')
        self.assertDictEqual(expected, obtained)

    def test_journal_title_no_match(self):
        expected = dict(
            object='journal title',
            output_expected='História, Ciências, Saúde-Manguinho',
            output_obteined='História, Ciências, Saúde-Manguinhos',
            match=False
        )
        obtained = self.title.validate_journal_title('História, Ciências, Saúde-Manguinho')
        self.assertDictEqual(expected, obtained)

    def test_abbreviated_journal_title_match(self):
        expected = dict(
            object='abbreviated journal title',
            output_expected='Hist. cienc. saude-Manguinhos',
            output_obteined='Hist. cienc. saude-Manguinhos',
            match=True
        )
        obtained = self.title.validate_abbreviated_journal_title('Hist. cienc. saude-Manguinhos')
        self.assertDictEqual(expected, obtained)

    def test_abbreviated_journal_title_no_match(self):
        expected = dict(
            object='abbreviated journal title',
            output_expected='Hist. cienc. saude-Manguinho',
            output_obteined='Hist. cienc. saude-Manguinhos',
            match=False
        )
        obtained = self.title.validate_abbreviated_journal_title('Hist. cienc. saude-Manguinho')
        self.assertDictEqual(expected, obtained)


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
                                <publisher-name>Casa de Oswaldo Cruz, Fundação Oswaldo Cruz</publisher-name>
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
                                <publisher-name>Casa de Oswaldo Cruz, Fundação Oswaldo Cruz</publisher-name>
                                <publisher-name>Programa de Pós-Graduação em Educação para a Ciência, Universidade Estadual Paulista (UNESP), Faculdade de Ciências, campus de Bauru.</publisher-name>
                            </publisher>
                        </journal-meta>
                    </front>
                </article>
            """
        )
        self.one_publisher = PublisherValidation(self.xmltree_one_publisher)
        self.more_than_one_publisher = PublisherValidation(self.xmltree_more_than_one_publisher)

    def test_one_publisher_match(self):
        expected = dict(
            object='publishers names',
            output_expected=['Casa de Oswaldo Cruz, Fundação Oswaldo Cruz'],
            output_obteined=['Casa de Oswaldo Cruz, Fundação Oswaldo Cruz'],
            match=True
        )
        obtained = self.one_publisher.validate_publishers_names(['Casa de Oswaldo Cruz, Fundação Oswaldo Cruz'])
        self.assertDictEqual(expected, obtained)

    def test_one_publisher_no_match(self):
        expected = dict(
            object='publishers names',
            output_expected=['Casa de Oswaldo Cruz - Fundação Oswaldo Cruz'],
            output_obteined=['Casa de Oswaldo Cruz, Fundação Oswaldo Cruz'],
            match=False
        )
        obtained = self.one_publisher.validate_publishers_names(['Casa de Oswaldo Cruz - Fundação Oswaldo Cruz'])
        self.assertDictEqual(expected, obtained)

    def test_more_than_one_publisher_match(self):
        expected = dict(
            object='publishers names',
            output_expected=[
                'Casa de Oswaldo Cruz, Fundação Oswaldo Cruz',
                'Programa de Pós-Graduação em Educação para a Ciência, Universidade Estadual Paulista (UNESP), Faculdade de Ciências, campus de Bauru.'
            ],
            output_obteined=[
                'Casa de Oswaldo Cruz, Fundação Oswaldo Cruz',
                'Programa de Pós-Graduação em Educação para a Ciência, Universidade Estadual Paulista (UNESP), Faculdade de Ciências, campus de Bauru.'
            ],
            match=True
        )
        obtained = self.more_than_one_publisher.validate_publishers_names([
            'Casa de Oswaldo Cruz, Fundação Oswaldo Cruz',
            'Programa de Pós-Graduação em Educação para a Ciência, Universidade Estadual Paulista (UNESP), Faculdade de Ciências, campus de Bauru.'
        ])
        self.assertDictEqual(expected, obtained)

    def test_more_than_one_publisher_no_match(self):
        expected = dict(
            object='publishers names',
            output_expected=[
                'Casa de Oswaldo Cruz, Fundação Oswaldo Cruz',
                'Programa de Pós-Graduação em Educação para a Ciência, Universidade Estadual Paulista (UNESP).'
            ],
            output_obteined=[
                'Casa de Oswaldo Cruz, Fundação Oswaldo Cruz',
                'Programa de Pós-Graduação em Educação para a Ciência, Universidade Estadual Paulista (UNESP), Faculdade de Ciências, campus de Bauru.'
            ],
            match=False
        )
        obtained = self.more_than_one_publisher.validate_publishers_names([
            'Casa de Oswaldo Cruz, Fundação Oswaldo Cruz',
            'Programa de Pós-Graduação em Educação para a Ciência, Universidade Estadual Paulista (UNESP).'
        ])
        self.assertDictEqual(expected, obtained)


class JournalMetaValidationTest(TestCase):
    def setUp(self):
        self.xmltree = etree.fromstring(
            """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="en">
                <front>
                    <journal-meta>
                        <issn pub-type="ppub">0103-5053</issn>
                        <issn pub-type="epub">1678-4790</issn>
                        <journal-id journal-id-type="nlm-ta">Hist Cienc Saude Manguinhos</journal-id>
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
            dict(
                object='journal acronym',
                output_expected='hcsm',
                output_obteined='hcsm',
                match=True
            ),
            dict(
                object='journal title',
                output_expected='História, Ciências, Saúde-Manguinhos',
                output_obteined='História, Ciências, Saúde-Manguinhos',
                match=True
            ),
            dict(
                object='abbreviated journal title',
                output_expected='Hist. cienc. saude-Manguinhos',
                output_obteined='Hist. cienc. saude-Manguinhos',
                match=True
            ),
            dict(
                object='publishers names',
                output_expected=['Casa de Oswaldo Cruz, Fundação Oswaldo Cruz'],
                output_obteined=['Casa de Oswaldo Cruz, Fundação Oswaldo Cruz'],
                match=True
            )
        ]
        obtained = self.journal_meta.validate({
            'issns': {
                'ppub': '0103-5053',
                'epub': '1678-4790'
            },
            'acronym': 'hcsm',
            'journal-title': 'História, Ciências, Saúde-Manguinhos',
            'abbrev-journal-title': 'Hist. cienc. saude-Manguinhos',
            'publisher-name': ['Casa de Oswaldo Cruz, Fundação Oswaldo Cruz']
        })
        self.assertListEqual(expected, obtained)
