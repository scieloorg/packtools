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
                    <supplement>2</supplement>
                </article-meta>
            </front>
        </article>
        """
        xml_tree = etree.fromstring(xml_str)
        obtained = IssueValidation(xml_tree).validate_article_issue()

        expected = [
            {
                'title': 'Article-meta issue element validation',
                'xpath': './/front/article-meta/issue',
                'validation_type': 'format',
                'response': 'ERROR',
                'expected_value': 'a valid value to article issue',
                'got_value': None,
                'message': 'Got None expected a valid value to article issue',
                'advice': 'Provide values according to the following examples: 4, spe1, 4 suppl 1 or suppl 1',

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
                    <supplement>2</supplement>
                </article-meta>
            </front>
        </article>
        """
        xml_tree = etree.fromstring(xml_str)
        obtained = IssueValidation(xml_tree).validate_article_issue()

        expected = [
            {
                'title': 'Article-meta issue element validation',
                'xpath': './/front/article-meta/issue',
                'validation_type': 'format',
                'response': 'ERROR',
                'expected_value': 'a valid value to article issue',
                'got_value': 'vol 4',
                'message': 'Got vol 4 expected a valid value to article issue',
                'advice': 'Provide values according to the following examples: 4, spe1, 4 suppl 1 or suppl 1',

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
