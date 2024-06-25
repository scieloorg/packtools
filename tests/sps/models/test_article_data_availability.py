import unittest
from lxml import etree

from packtools.sps.models.article_data_availability import DataAvailability


class DataAvailabilityTest(unittest.TestCase):

    def test_specific_use_sec_and_fn(self):
        self.maxDiff = None
        xml = """
                <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article">
                    <back>
                        <sec sec-type="data-availability" specific-use="data-available-upon-request">
                            <label>Data availability statement</label>
                            <p>Data will be available upon request.</p>
                        </sec>
                        <fn-group>
                            <fn fn-type="data-availability" specific-use="data-available" id="fn1">
                                <label>Data Availability Statement</label>
                                <p>The data and code used to generate plots and perform statistical analyses have been
                                uploaded to the Open Science Framework archive: <ext-link ext-link-type="uri"
                                xlink:href="https://osf.io/jw6vg/?view_only=0335a15b6db3477f93d0ae636cdf3b4e">https://osf.io/j
                                w6vg/?view_only=0335a15b6db3477f93d0ae636cdf3b4e</ext-link>.</p>
                            </fn>
                        </fn-group>
                    </back>
                </article>
            """
        xmltree = etree.fromstring(xml)
        expected = [
            {
                'parent': 'article',
                'parent_article_type': 'research-article',
                'parent_id': None,
                'parent_lang': None,
                'tag': 'sec',
                'specific_use': 'data-available-upon-request'
            },
            {
                'parent': 'article',
                'parent_article_type': 'research-article',
                'parent_id': None,
                'parent_lang': None,
                'tag': 'fn',
                'specific_use': 'data-available'
            }
        ]
        obtained = list(DataAvailability(xmltree).specific_use)
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

    def test_specific_use_sec(self):
        self.maxDiff = None
        xml = """
                <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article">
                    <back>
                        <sec sec-type="data-availability" specific-use="data-available-upon-request">
                            <label>Data availability statement</label>
                            <p>Data will be available upon request.</p>
                        </sec>
                    </back>
                </article>
            """
        xmltree = etree.fromstring(xml)
        expected = [
            {
                'parent': 'article',
                'parent_article_type': 'research-article',
                'parent_id': None,
                'parent_lang': None,
                'tag': 'sec',
                'specific_use': 'data-available-upon-request'
            }
        ]
        obtained = list(DataAvailability(xmltree).specific_use)
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

    def test_specific_use_fn(self):
        self.maxDiff = None
        xml = """
                <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article">
                    <back>
                        <fn-group>
                            <fn fn-type="data-availability" specific-use="data-available" id="fn1">
                                <label>Data Availability Statement</label>
                                <p>The data and code used to generate plots and perform statistical analyses have been
                                uploaded to the Open Science Framework archive: <ext-link ext-link-type="uri"
                                xlink:href="https://osf.io/jw6vg/?view_only=0335a15b6db3477f93d0ae636cdf3b4e">https://osf.io/j
                                w6vg/?view_only=0335a15b6db3477f93d0ae636cdf3b4e</ext-link>.</p>
                            </fn>
                        </fn-group>
                    </back>
                </article>
            """
        xmltree = etree.fromstring(xml)
        expected = [
            {
                'parent': 'article',
                'parent_article_type': 'research-article',
                'parent_id': None,
                'parent_lang': None,
                'tag': 'fn',
                'specific_use': 'data-available'
            }
        ]
        obtained = list(DataAvailability(xmltree).specific_use)
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

    def test_specific_use_not_found(self):
        self.maxDiff = None
        xml = """
                <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article">
                    <back>
                    </back>
                </article>
            """
        xmltree = etree.fromstring(xml)
        expected = []
        obtained = list(DataAvailability(xmltree).specific_use)
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)


if __name__ == '__main__':
    unittest.main()
