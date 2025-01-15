import unittest
from unittest import skip

from packtools.sps.utils.xml_utils import get_xml_tree

from packtools.sps.validation.preprint import PreprintValidation


class PreprintValidationTest(unittest.TestCase):
    @skip("Teste pendente de correção e/ou ajuste")
    def test_preprint_validation_preprint_ok_and_date_ok(self):
        self.maxDiff = None
        xml_str = """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article">
            <front>
            <article-meta>
            <history>
            <date date-type="preprint">
            <day>18</day>
            <month>10</month>
            <year>2002</year>
            </date>
            </history>
            </article-meta>
            </front>
            <related-article id="pp1" related-article-type="preprint" ext-link-type="doi" xlink:href="10.1590/SciELOPreprints.1174"/>
            </article>
        """

        obtained = PreprintValidation(get_xml_tree(xml_str)).preprint_validation()

        expected = [
            {
                'title': 'Preprint validation',
                'xpath': './/related-article[@related-article-type="preprint"] .//history//date[@date-type="preprint"]',
                'validation_type': 'match',
                'response': 'OK',
                'expected_value': '2002-10-18',
                'got_value': '2002-10-18',
                'message': 'Got 2002-10-18 expected 2002-10-18',
                'advice': None

            }
        ]

        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

    def test_preprint_validation_preprint_ok_and_date_not_ok(self):
        self.maxDiff = None
        xml_str = """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article">
            <front>
            <article-meta>
            </article-meta>
            </front>
            <related-article id="pp1" related-article-type="preprint" ext-link-type="doi" xlink:href="10.1590/SciELOPreprints.1174"/>
            </article>
        """

        obtained = PreprintValidation(get_xml_tree(xml_str)).preprint_validation()

        expected = [
            {
                'title': 'Preprint validation',
                'xpath': './/related-article[@related-article-type="preprint"] .//history//date[@date-type="preprint"]',
                'validation_type': 'match',
                'response': 'ERROR',
                'expected_value': 'The preprint publication date',
                'got_value': None,
                'message': 'Got None expected The preprint publication date',
                'advice': 'Provide the publication date of the preprint'

            }
        ]

        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

    def test_preprint_validation_preprint_not_ok_and_date_ok(self):
        self.maxDiff = None
        xml_str = """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article">
            <front>
            <article-meta>
            <history>
            <date date-type="preprint">
            <day>18</day>
            <month>10</month>
            <year>2002</year>
            </date>
            </history>
            </article-meta>
            </front>
            </article>
        """

        obtained = PreprintValidation(get_xml_tree(xml_str)).preprint_validation()

        expected = [
            {
                'title': 'Preprint validation',
                'xpath': './/related-article[@related-article-type="preprint"] .//history//date[@date-type="preprint"]',
                'validation_type': 'match',
                'response': 'ERROR',
                'expected_value': None,
                'got_value': '2002-10-18',
                'message': 'Got 2002-10-18 expected None',
                'advice': 'The article does not reference the preprint, provide it as in the example: '
                          '<related-article id="pp1" related-article-type="preprint" ext-link-type="doi" '
                          'xlink:href="10.1590/SciELOPreprints.1174"/>'

            }
        ]

        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

    def test_preprint_validation_preprint_not_ok_and_date_not_ok(self):
        self.maxDiff = None
        xml_str = """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article">
            <front>
            <article-meta>
            </article-meta>
            </front>
            </article>
        """

        obtained = PreprintValidation(get_xml_tree(xml_str)).preprint_validation()

        self.assertEqual([], obtained)


if __name__ == '__main__':
    unittest.main()
