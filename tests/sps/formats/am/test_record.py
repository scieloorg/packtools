import unittest

from packtools.sps.utils import xml_utils
from packtools.sps.formats.am import am


class BaseTest(unittest.TestCase):
    def setUp(self):
        self.xml_tree = xml_utils.get_xml_tree(
            "tests/sps/formats/am/examples/S0104-11692025000100300.xml"
        )


class TestGetJournal(BaseTest):
    def test_field_v30(self):
        obtained = am.get_journal(self.xml_tree)
        self.assertIsInstance(obtained, dict)
        self.assertIn("v30", obtained)
        expected = [{"_": "Rev. Latino-Am. Enfermagem"}]
        self.assertEqual(obtained["v30"], expected)

    def test_field_v421(self):
        obtained = am.get_journal(self.xml_tree)
        self.assertIsInstance(obtained, dict)
        self.assertIn("v421", obtained)
        expected = [{"_": "Rev Lat Am Enfermagem"}]
        self.assertEqual(obtained["v421"], expected)


class TestGetArticlemetaIssue(BaseTest):
    def test_field_v31(self):
        obtained = am.get_articlemeta_issue(self.xml_tree)
        self.assertIsInstance(obtained, dict)
        self.assertIn("v31", obtained)
        expected = [{'_': '33'}]
        self.assertEqual(obtained["v31"], expected)

    def test_field_v121(self):
        obtained = am.get_articlemeta_issue(self.xml_tree)
        self.assertIsInstance(obtained, dict)
        self.assertIn("v121", obtained)
        expected = [{'_': '00300'}]
        self.assertEqual(obtained["v121"], expected)

    def test_field_v882(self):
        obtained = am.get_articlemeta_issue(self.xml_tree)
        self.assertIsInstance(obtained, dict)
        self.assertIn("v882", obtained)
        expected = [{"v": "33", "_": ""}]
        self.assertEqual(obtained["v882"], expected)

    def test_field_v14(self):
        obtained = am.get_articlemeta_issue(self.xml_tree)
        self.assertIsInstance(obtained, dict)
        self.assertIn("v14", obtained)
        expected = [{"e": "e4434", "_": ""}]
        self.assertEqual(obtained["v14"], expected)


class TestGetIds(BaseTest):
    def test_code(self):
        obtained = am.get_ids(self.xml_tree)
        self.assertIsInstance(obtained, dict)
        self.assertIn("code", obtained)
        expected = 'S0104-11692025000100300'
        self.assertEqual(obtained["code"], expected)

    def test_field_v880(self):
        obtained = am.get_ids(self.xml_tree)
        self.assertIsInstance(obtained, dict)
        self.assertIn("v880", obtained)
        expected = [{'_': 'S0104-11692025000100300'}]
        self.assertEqual(obtained["v880"], expected)

    def test_field_v237(self):
        obtained = am.get_ids(self.xml_tree)
        self.assertIsInstance(obtained, dict)
        self.assertIn("v237", obtained)
        expected = [{'_': '10.1590/1518-8345.7320.4434'}]
        self.assertEqual(obtained["v237"], expected)


class TestGetContribs(BaseTest):
    def test_field_v10(self):
        obtained = am.get_contribs(self.xml_tree)
        self.assertIsInstance(obtained, dict)
        self.assertIn("v10", obtained)
        self.assertGreater(len(obtained["v10"]), 0)

        author = obtained["v10"][0]
        expected_keys = {"k", "n", "1", "s", "r", "_"}
        self.assertTrue(expected_keys.issubset(author.keys()))

    def test_field_v10_includes_specific_author(self):
        obtained = am.get_contribs(self.xml_tree)
        author = next((a for a in obtained["v10"] if a["k"] == "0000-0002-4201-0624"), None)
        self.assertIsNotNone(author)
        expected_author = {
            "n": "Janaina Recanello",
            "s": "Begui",
            "1": "aff1",
            "r": "ND"
        }
        for key, value in expected_author.items():
            self.assertEqual(author[key], value)


class TestGetAffs(BaseTest):
    def test_field_v70(self):
        obtained = am.get_affs(self.xml_tree)
        self.assertIsInstance(obtained, dict)
        self.assertIn("v70", obtained)
        self.assertGreater(len(obtained["v70"]), 0)

        aff = obtained["v70"][0]
        expected_keys = {"c", "i", "l", "1", "p", "s", "_"}
        self.assertTrue(expected_keys.issubset(aff.keys()))


class TestGetReferences(BaseTest):
    def test_field_v72(self):
        obtained = am.get_references(self.xml_tree)
        self.assertIsInstance(obtained, dict)
        self.assertIn("v72", obtained)
        expected = [{"_": 35}]
        self.assertEqual(obtained["v72"], expected)


class TestGetDates(BaseTest):
    def test_field_v114(self):
        obtained = am.get_dates(self.xml_tree)
        self.assertIsInstance(obtained, dict)
        self.assertIn("v114", obtained)
        expected = [{'_': '20240811'}]
        self.assertEqual(obtained["v114"], expected)

    def test_field_v112(self):
        obtained = am.get_dates(self.xml_tree)
        self.assertIsInstance(obtained, dict)
        self.assertIn("v112", obtained)
        expected = [{'_': '20240208'}]
        self.assertEqual(obtained["v112"], expected)

    def test_field_v65(self):
        obtained = am.get_dates(self.xml_tree)
        self.assertIsInstance(obtained, dict)
        self.assertIn("v65", obtained)
        expected = [{'_': '20250000'}]
        self.assertEqual(obtained["v65"], expected)


class TestGetArticleAndSubarticle(BaseTest):
    def test_field_v40(self):
        obtained = am.get_article_and_subarticle(self.xml_tree)
        self.assertIsInstance(obtained, dict)
        self.assertIn("v40", obtained)
        expected = [{'_': 'en'}]
        self.assertEqual(obtained["v40"], expected)


class TestGetArticleAbstract(BaseTest):
    def test_field_v83(self):
        obtained = am.get_article_abstract(self.xml_tree)
        self.assertIsInstance(obtained, dict)
        self.assertIn("v83", obtained)
        self.assertGreater(len(obtained["v83"]), 0)

        abstract = obtained["v83"][0]
        expected_keys = {"a", "l", "_"}
        self.assertTrue(expected_keys.issubset(abstract.keys()))


if __name__ == "__main__":
    unittest.main()
