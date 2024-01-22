from unittest import TestCase
from lxml import etree

from packtools.sps.validation.front_articlemeta_issue import IssueValidation


class IssueTest(TestCase):
    def test_volume_matches(self):
        xml = (
            '''
            <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="en">
                <front>
                    <article-meta>
                        <volume>56</volume>
                        <issue>4</issue>
                    </article-meta>
                </front>
            </article>
            '''
        )
        xmltree = etree.fromstring(xml)

        expected = dict(
            object='volume',
            output_expected='56',
            output_obteined='56',
            match=True
        )
        obtained = IssueValidation(xmltree).validate_volume('56')
        self.assertDictEqual(expected, obtained)

    def test_volume_no_matches(self):
        xml = (
            '''
            <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="en">
                <front>
                    <article-meta>
                        <volume> 56 </volume>
                        <issue>4</issue>
                    </article-meta>
                </front>
            </article>
            '''
        )
        xmltree = etree.fromstring(xml)

        expected = dict(
            object='volume',
            output_expected='56',
            output_obteined=' 56 ',
            match=False
        )
        obtained = IssueValidation(xmltree).validate_volume('56')
        self.assertDictEqual(expected, obtained)

    def test_volume_no_volume(self):
        xml = (
            '''
            <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="en">
                <front>
                    <article-meta>
                        <issue>4</issue>
                    </article-meta>
                </front>
            </article>
            '''
        )
        xmltree = etree.fromstring(xml)

        expected = dict(
            object='volume',
            output_expected='56',
            output_obteined=None,
            match=False
        )
        obtained = IssueValidation(xmltree).validate_volume('56')
        self.assertDictEqual(expected, obtained)

    def test_validate_article_issue_without_value(self):
        self.maxDiff = None
        xml_str = """
        <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="en">
            <front>
                <article-meta>
                    <volume>56</volume>
                </article-meta>
            </front>
        </article>
        """
        xml_tree = etree.fromstring(xml_str)
        obtained = IssueValidation(xml_tree).validate_article_issue('WARNING')

        expected = [
            {
                'title': 'Article-meta issue element validation',
                'xpath': './/front/article-meta/issue',
                'validation_type': 'exist',
                'response': 'WARNING',
                'expected_value': 'an identifier for the publication issue',
                'got_value': None,
                'message': 'Got None expected an identifier for the publication issue',
                'advice': 'Provide an identifier for the publication issue'

            }
        ]
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

    def test_validate_article_issue_out_of_pattern_value(self):
        self.maxDiff = None
        xml_str = """
        <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="en">
            <front>
                <article-meta>
                    <issue>vol 4</issue>
                </article-meta>
            </front>
        </article>
        """
        xml_tree = etree.fromstring(xml_str)
        obtained = IssueValidation(xml_tree).validate_article_issue('WARNING')

        expected = [
            {
                'title': 'Article-meta issue element validation',
                'xpath': './/front/article-meta/issue',
                'validation_type': 'format',
                'response': 'ERROR',
                'expected_value': 'a alphanumeric value that does not contain space or dot',
                'got_value': 'vol 4',
                'message': 'Got vol 4 expected a alphanumeric value that does not contain space or dot',
                'advice': 'Provide a valid alphanumeric value',

            }
        ]
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

    def test_validate_article_issue_number_success(self):
        self.maxDiff = None
        xml_str = """
        <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="en">
            <front>
                <article-meta>
                    <volume>56</volume>
                    <issue>4</issue>
                </article-meta>
            </front>
        </article>
        """
        xml_tree = etree.fromstring(xml_str)
        obtained = IssueValidation(xml_tree).validate_article_issue('WARNING')

        expected = [
            {
                'title': 'Article-meta issue element validation',
                'xpath': './/front/article-meta/issue',
                'validation_type': 'format',
                'response': 'OK',
                'expected_value': '4',
                'got_value': '4',
                'message': 'Got 4 expected 4',
                'advice': None

            }
        ]
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

    def test_validate_article_issue_number_fail_start_with_zero(self):
        self.maxDiff = None
        xml_str = """
        <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="en">
            <front>
                <article-meta>
                    <volume>56</volume>
                    <issue>04</issue>
                </article-meta>
            </front>
        </article>
        """
        xml_tree = etree.fromstring(xml_str)
        obtained = IssueValidation(xml_tree).validate_article_issue('WARNING')

        expected = [
            {
                'title': 'Article-meta issue element validation',
                'xpath': './/front/article-meta/issue',
                'validation_type': 'format',
                'response': 'ERROR',
                'expected_value': 'a numeric value that does not start with zero',
                'got_value': '04',
                'message': 'Got 04 expected a numeric value that does not start with zero',
                'advice': 'Provide a valid numeric value',

            }
        ]
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

    def test_validate_article_issue_number_success_value_is_not_numeric(self):
        self.maxDiff = None
        xml_str = """
        <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="en">
            <front>
                <article-meta>
                    <volume>56</volume>
                    <issue>4a</issue>
                </article-meta>
            </front>
        </article>
        """
        xml_tree = etree.fromstring(xml_str)
        obtained = IssueValidation(xml_tree).validate_article_issue('WARNING')

        expected = [
            {
                'title': 'Article-meta issue element validation',
                'xpath': './/front/article-meta/issue',
                'validation_type': 'format',
                'response': 'OK',
                'expected_value': '4a',
                'got_value': '4a',
                'message': 'Got 4a expected 4a',
                'advice': None

            }
        ]
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

    def test_validate_article_issue_special_number_success(self):
        self.maxDiff = None
        xml_str = """
        <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="en">
            <front>
                <article-meta>
                    <volume>56</volume>
                    <issue>spe1</issue>
                </article-meta>
            </front>
        </article>
        """
        xml_tree = etree.fromstring(xml_str)
        obtained = IssueValidation(xml_tree).validate_article_issue('WARNING')

        expected = [
            {
                'title': 'Article-meta issue element validation',
                'xpath': './/front/article-meta/issue',
                'validation_type': 'format',
                'response': 'OK',
                'expected_value': 'spe1',
                'got_value': 'spe1',
                'message': 'Got spe1 expected spe1',
                'advice': None

            }
        ]
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

    def test_validate_article_issue_special_number_success_without_value(self):
        self.maxDiff = None
        xml_str = """
        <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="en">
            <front>
                <article-meta>
                    <volume>56</volume>
                    <issue>spe</issue>
                </article-meta>
            </front>
        </article>
        """
        xml_tree = etree.fromstring(xml_str)
        obtained = IssueValidation(xml_tree).validate_article_issue('WARNING')

        expected = [
            {
                'title': 'Article-meta issue element validation',
                'xpath': './/front/article-meta/issue',
                'validation_type': 'format',
                'response': 'OK',
                'expected_value': 'spe',
                'got_value': 'spe',
                'message': 'Got spe expected spe',
                'advice': None

            }
        ]
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

    def test_validate_article_issue_special_number_fail_with_dot(self):
        self.maxDiff = None
        xml_str = """
        <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="en">
            <front>
                <article-meta>
                    <volume>56</volume>
                    <issue>spe.1</issue>
                </article-meta>
            </front>
        </article>
        """
        xml_tree = etree.fromstring(xml_str)
        obtained = IssueValidation(xml_tree).validate_article_issue('WARNING')

        expected = [
            {
                'title': 'Article-meta issue element validation',
                'xpath': './/front/article-meta/issue',
                'validation_type': 'format',
                'response': 'ERROR',
                'expected_value': 'speX where X is a valid alphanumeric value or None',
                'got_value': 'spe.1',
                'message': 'Got spe.1 expected speX where X is a valid alphanumeric value or None',
                'advice': 'Provide a valid value to special number',

            }
        ]
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

    def test_validate_article_issue_special_number_fail_with_space(self):
        self.maxDiff = None
        xml_str = """
        <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="en">
            <front>
                <article-meta>
                    <volume>56</volume>
                    <issue> spe 1</issue>
                </article-meta>
            </front>
        </article>
        """
        xml_tree = etree.fromstring(xml_str)
        obtained = IssueValidation(xml_tree).validate_article_issue('WARNING')

        expected = [
            {
                'title': 'Article-meta issue element validation',
                'xpath': './/front/article-meta/issue',
                'validation_type': 'format',
                'response': 'ERROR',
                'expected_value': 'speX where X is a valid alphanumeric value or None',
                'got_value': ' spe 1',
                'message': 'Got  spe 1 expected speX where X is a valid alphanumeric value or None',
                'advice': 'Provide a valid value to special number',

            }
        ]
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

    def test_validate_article_issue_volume_supplement_success(self):
        self.maxDiff = None
        xml_str = """
        <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="en">
            <front>
                <article-meta>
                    <volume>56</volume>
                    <issue>suppl 1</issue>
                </article-meta>
            </front>
        </article>
        """
        xml_tree = etree.fromstring(xml_str)
        obtained = IssueValidation(xml_tree).validate_article_issue('WARNING')

        expected = [
            {
                'title': 'Article-meta issue element validation',
                'xpath': './/front/article-meta/issue',
                'validation_type': 'format',
                'response': 'OK',
                'expected_value': 'suppl 1',
                'got_value': 'suppl 1',
                'message': 'Got suppl 1 expected suppl 1',
                'advice': None

            }
        ]
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

    def test_validate_article_issue_volume_supplement_fail_with_dot(self):
        self.maxDiff = None
        xml_str = """
        <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="en">
            <front>
                <article-meta>
                    <volume>56</volume>
                    <issue>suppl a.</issue>
                </article-meta>
            </front>
        </article>
        """
        xml_tree = etree.fromstring(xml_str)
        obtained = IssueValidation(xml_tree).validate_article_issue('WARNING')

        expected = [
            {
                'title': 'Article-meta issue element validation',
                'xpath': './/front/article-meta/issue',
                'validation_type': 'format',
                'response': 'ERROR',
                'expected_value': 'X suppl Y where X and Y are alphanumeric value',
                'got_value': 'suppl a.',
                'message': 'Got suppl a. expected X suppl Y where X and Y are alphanumeric value',
                'advice': 'Provide a valid value to supplement',

            }
        ]
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

    def test_validate_article_issue_volume_supplement_fail_number_starts_with_zero(self):
        self.maxDiff = None
        xml_str = """
        <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="en">
            <front>
                <article-meta>
                    <volume>56</volume>
                    <issue>suppl 04</issue>
                </article-meta>
            </front>
        </article>
        """
        xml_tree = etree.fromstring(xml_str)
        obtained = IssueValidation(xml_tree).validate_article_issue('WARNING')

        expected = [
            {
                'title': 'Article-meta issue element validation',
                'xpath': './/front/article-meta/issue',
                'validation_type': 'format',
                'response': 'ERROR',
                'expected_value': 'X suppl Y where X and Y are alphanumeric value',
                'got_value': 'suppl 04',
                'message': 'Got suppl 04 expected X suppl Y where X and Y are alphanumeric value',
                'advice': 'Provide a valid value to supplement',

            }
        ]
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

    def test_validate_article_issue_number_supplement_success(self):
        self.maxDiff = None
        xml_str = """
        <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="en">
            <front>
                <article-meta>
                    <volume>56</volume>
                    <issue>4 suppl 1</issue>
                </article-meta>
            </front>
        </article>
        """
        xml_tree = etree.fromstring(xml_str)
        obtained = IssueValidation(xml_tree).validate_article_issue('WARNING')

        expected = [
            {
                'title': 'Article-meta issue element validation',
                'xpath': './/front/article-meta/issue',
                'validation_type': 'format',
                'response': 'OK',
                'expected_value': '4 suppl 1',
                'got_value': '4 suppl 1',
                'message': 'Got 4 suppl 1 expected 4 suppl 1',
                'advice': None

            }
        ]
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

    def test_validate_article_issue_number_supplement_fail_with_dot_and_space(self):
        self.maxDiff = None
        xml_str = """
        <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="en">
            <front>
                <article-meta>
                    <volume>56</volume>
                    <issue> a suppl b.</issue>
                </article-meta>
            </front>
        </article>
        """
        xml_tree = etree.fromstring(xml_str)
        obtained = IssueValidation(xml_tree).validate_article_issue('WARNING')

        expected = [
            {
                'title': 'Article-meta issue element validation',
                'xpath': './/front/article-meta/issue',
                'validation_type': 'format',
                'response': 'ERROR',
                'expected_value': 'X suppl Y where X and Y are alphanumeric value',
                'got_value': ' a suppl b.',
                'message': 'Got  a suppl b. expected X suppl Y where X and Y are alphanumeric value',
                'advice': 'Provide a valid value to supplement'

            }
        ]
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

    def test_suppl_matches(self):
        xml = (
            '''
            <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="en">
                <front>
                    <article-meta>
                        <volume>56</volume>
                        <issue>4</issue>
                        <supplement>2</supplement>
                    </article-meta>
                </front>
            </article>
            '''
        )
        xmltree = etree.fromstring(xml)

        expected = dict(
            object='supplement',
            output_expected='2',
            output_obteined='2',
            match=True
        )
        obtained = IssueValidation(xmltree).validate_supplement('2')
        self.assertDictEqual(expected, obtained)

    def test_suppl_no_matches(self):
        xml = (
            '''
            <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="en">
                <front>
                    <article-meta>
                        <volume>56</volume>
                        <issue>4</issue>
                        <supplement>2b</supplement>
                    </article-meta>
                </front>
            </article>
            '''
        )
        xmltree = etree.fromstring(xml)

        expected = dict(
            object='supplement',
            output_expected='2',
            output_obteined='2b',
            match=False
        )
        obtained = IssueValidation(xmltree).validate_supplement('2')
        self.assertDictEqual(expected, obtained)

    def test_suppl_implicit(self):
        xml = (
            '''
            <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="en">
                <front>
                    <article-meta>
                        <volume>56</volume>
                        <issue>4 suppl 2</issue>
                    </article-meta>
                </front>
            </article>
            '''
        )
        xmltree = etree.fromstring(xml)

        expected = dict(
            object='supplement',
            output_expected='2',
            output_obteined='2',
            match=True
        )
        obtained = IssueValidation(xmltree).validate_supplement('2')
        self.assertDictEqual(expected, obtained)
