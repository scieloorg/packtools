import unittest
from lxml import etree

from packtools.sps.models.article_data_availability import DataAvailability


class DataAvailabilityTest(unittest.TestCase):

    def test_items_sec_and_fn(self):
        self.maxDiff = None
        xml = """
                <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" dtd-version="1.0" article-type="research-article" xml:lang="pt">
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

        # Get the actual items
        items = list(DataAvailability(xmltree).items)

        # Test the number of items found
        self.assertEqual(len(items), 2)

        # Test items content
        self.assertEqual(items[0]["tag"], "sec")
        self.assertEqual(items[0]["specific_use"], "data-available-upon-request")
        self.assertEqual(items[0]["parent_article_type"], "research-article")
        self.assertEqual(items[0]["parent_lang"], "pt")

        self.assertEqual(items[1]["tag"], "fn")
        self.assertEqual(items[1]["specific_use"], "data-available")
        self.assertEqual(items[1]["parent_article_type"], "research-article")
        self.assertEqual(items[1]["parent_lang"], "pt")

    def test_items_sec(self):
        self.maxDiff = None
        xml = """
                <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" dtd-version="1.0" article-type="research-article" xml:lang="pt">
                    <back>
                        <sec sec-type="data-availability" specific-use="data-available-upon-request">
                            <label>Data availability statement</label>
                            <p>Data will be available upon request.</p>
                        </sec>
                    </back>
                </article>
            """
        xmltree = etree.fromstring(xml)

        # Get the actual items
        items = list(DataAvailability(xmltree).items)

        # Test the number of items found
        self.assertEqual(len(items), 1)

        # Test item content
        self.assertEqual(items[0]["tag"], "sec")
        self.assertEqual(items[0]["specific_use"], "data-available-upon-request")
        self.assertEqual(items[0]["parent_article_type"], "research-article")
        self.assertEqual(items[0]["parent_lang"], "pt")

    def test_items_fn(self):
        self.maxDiff = None
        xml = """
                <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" dtd-version="1.0" article-type="research-article" xml:lang="pt">
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

        # Get the actual items
        items = list(DataAvailability(xmltree).items)

        # Test the number of items found
        self.assertEqual(len(items), 1)

        # Test item content
        self.assertEqual(items[0]["tag"], "fn")
        self.assertEqual(items[0]["specific_use"], "data-available")
        self.assertEqual(items[0]["parent_article_type"], "research-article")
        self.assertEqual(items[0]["parent_lang"], "pt")

    def test_items_not_found(self):
        self.maxDiff = None
        xml = """
                <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" dtd-version="1.0" article-type="research-article" xml:lang="pt">
                    <back>
                    </back>
                </article>
            """
        xmltree = etree.fromstring(xml)

        # Get the actual items
        items = list(DataAvailability(xmltree).items)

        # Test no items found
        self.assertEqual(len(items), 1)

    def test_items_by_lang(self):
        self.maxDiff = None
        xml = """
                <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" dtd-version="1.0" article-type="research-article" xml:lang="pt">
                    <back>
                        <sec sec-type="data-availability" specific-use="data-available-upon-request">
                            <label>Data availability statement</label>
                            <p>Data will be available upon request.</p>
                        </sec>
                        <fn-group>
                            <fn fn-type="data-availability" specific-use="data-available" id="fn1">
                                <label>Data Availability Statement</label>
                                <p>The data and code used to generate plots and perform statistical analyses have been uploaded to the Open Science Framework archive.</p>
                            </fn>
                        </fn-group>
                    </back>
                </article>
            """
        xmltree = etree.fromstring(xml)

        # Get items by language
        items_by_lang = DataAvailability(xmltree).items_by_lang

        # Test items by language
        self.assertIn("pt", items_by_lang)

        # Since items_by_lang only keeps one item per language, check that it contains one of the items
        # (in this case, the last one processed which should be the fn)
        self.assertEqual(items_by_lang["pt"][0]["tag"], "sec")
        self.assertEqual(
            items_by_lang["pt"][0]["text"], "Data will be available upon request."
        )
        self.assertEqual(items_by_lang["pt"][1]["tag"], "fn")
        self.assertEqual(
            items_by_lang["pt"][1]["text"],
            "The data and code used to generate plots and perform statistical analyses have been uploaded to the Open Science Framework archive.",
        )


if __name__ == "__main__":
    unittest.main()
