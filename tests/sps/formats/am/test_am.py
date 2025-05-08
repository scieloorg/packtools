import unittest

from packtools.sps.utils import xml_utils
from packtools.sps.formats.am import am


class BaseTest(unittest.TestCase):
    def setUp(self):
        self.xml_tree = xml_utils.get_xml_tree(
            "tests/sps/formats/am/examples/S0104-11692025000100300.xml"
        )

        self.data = {
            "v999": "../bases-work/rlae/rlae",
            "v38": "GRA",
            "v992": "scl",
            "v35": "0104-1169",
            "v42": "1",
            "v49": "RLAE350",
            "v706": "h",
            "collection": "scl",
            "v2": "S0104-1169(25)03300000300",
            "v91": "20250203",
            "v701": "1",
            "v700": "2",
            "v702": "rlae/v33/1518-8345-rlae-33-e4434.xml",
            "v705": "S",
            "processing_date": "2025-02-03",
            "v265": [
                {"k": "real", "s": "xml", "v": "20250127"},
                {"k": "expected", "s": "xml", "v": "202500"},
            ],
            "v708": "1",
            "v3": "1518-8345-rlae-33-e4434.xml",
            "v936": {"i": "0104-1169", "y": "2025", "o": "1"},
        }


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

    def test_field_v62(self):
        obtained = am.get_journal(self.xml_tree)
        self.assertIsInstance(obtained, dict)
        self.assertIn("v62", obtained)
        expected = [
            {"_": "Escola de Enfermagem de Ribeirão Preto / Universidade de São Paulo"}
        ]
        self.assertEqual(obtained["v62"], expected)

    def test_field_v435(self):
        obtained = am.get_journal(self.xml_tree)
        self.assertIsInstance(obtained, dict)
        self.assertIn("v435", obtained)
        expected = [{"_": "1518-8345", "t": "epub"}]
        self.assertEqual(obtained["v435"], expected)

    def test_field_v100(self):
        obtained = am.get_journal(self.xml_tree)
        self.assertIsInstance(obtained, dict)
        self.assertIn("v100", obtained)
        expected = [{"_": "Revista Latino-Americana de Enfermagem"}]
        self.assertEqual(obtained["v100"], expected)

    def test_field_v35(self):
        obtained = am.get_journal(self.xml_tree, self.data)
        self.assertIsInstance(obtained, dict)
        self.assertIn("v35", obtained)
        self.assertEqual(obtained["v35"], [{"_": "0104-1169"}])


class TestGetArticlemetaIssue(BaseTest):
    def test_field_v31(self):
        obtained = am.get_articlemeta_issue(self.xml_tree)
        self.assertIsInstance(obtained, dict)
        self.assertIn("v31", obtained)
        self.assertEqual(obtained["v31"], [{"_": "33"}])

    def test_field_v121(self):
        obtained = am.get_articlemeta_issue(self.xml_tree)
        self.assertIsInstance(obtained, dict)
        self.assertIn("v121", obtained)
        self.assertEqual(obtained["v121"], [{"_": "00300"}])

    def test_field_v882(self):
        obtained = am.get_articlemeta_issue(self.xml_tree)
        self.assertIsInstance(obtained, dict)
        self.assertIn("v882", obtained)
        self.assertEqual(obtained["v882"], [{"v": "33", "_": ""}])

    def test_field_v14(self):
        obtained = am.get_articlemeta_issue(self.xml_tree)
        self.assertIsInstance(obtained, dict)
        self.assertIn("v14", obtained)
        self.assertEqual(obtained["v14"], [{"e": "e4434", "_": ""}])

    def test_field_v4(self):
        obtained = am.get_articlemeta_issue(self.xml_tree)
        self.assertIsInstance(obtained, dict)
        self.assertIn("v4", obtained)
        self.assertEqual(obtained["v4"], [{"_": "V33"}])

    def test_field_v709(self):
        obtained = am.get_articlemeta_issue(self.xml_tree)
        self.assertIsInstance(obtained, dict)
        self.assertIn("v709", obtained)
        self.assertEqual(obtained["v709"], [{"_": "article"}])


class TestGetIds(BaseTest):
    def test_code(self):
        obtained = am.get_ids(self.xml_tree)
        self.assertIsInstance(obtained, dict)
        self.assertIn("code", obtained)
        expected = "S0104-11692025000100300"
        self.assertEqual(obtained["code"], expected)

    def test_field_v880(self):
        obtained = am.get_ids(self.xml_tree)
        self.assertIsInstance(obtained, dict)
        self.assertIn("v880", obtained)
        expected = [{"_": "S0104-11692025000100300"}]
        self.assertEqual(obtained["v880"], expected)

    def test_field_v237(self):
        obtained = am.get_ids(self.xml_tree)
        self.assertIsInstance(obtained, dict)
        self.assertIn("v237", obtained)
        expected = [{"_": "10.1590/1518-8345.7320.4434"}]
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
        author = next(
            (a for a in obtained["v10"] if a["k"] == "0000-0002-4201-0624"), None
        )
        self.assertIsNotNone(author)
        expected_author = {
            "n": "Janaina Recanello",
            "s": "Begui",
            "1": "aff1",
            "r": "ND",
        }
        for key, value in expected_author.items():
            self.assertEqual(author[key], value)


class TestGetAffs(BaseTest):
    def test_field_v70(self):
        obtained = am.get_affs(self.xml_tree)
        self.assertIsInstance(obtained, dict)
        self.assertIn("v70", obtained)
        self.assertEqual(len(obtained["v70"]), 4)

        aff = obtained["v70"][0]
        expected_keys = {"c", "i", "l", "1", "p", "s", "_"}
        self.assertTrue(expected_keys.issubset(aff.keys()))

    def test_field_v240(self):
        obtained = am.get_affs(self.xml_tree)
        self.assertIsInstance(obtained, dict)
        self.assertIn("v240", obtained)
        self.assertEqual(len(obtained["v240"]), 4)

        aff = obtained["v240"][0]
        expected_keys = {"c", "i", "p", "s", "_"}
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
        expected = [{"_": "20240811"}]
        self.assertEqual(obtained["v114"], expected)

    def test_field_v112(self):
        obtained = am.get_dates(self.xml_tree)
        self.assertIsInstance(obtained, dict)
        self.assertIn("v112", obtained)
        expected = [{"_": "20240208"}]
        self.assertEqual(obtained["v112"], expected)

    def test_field_v65(self):
        obtained = am.get_dates(self.xml_tree)
        self.assertIsInstance(obtained, dict)
        self.assertIn("v65", obtained)
        expected = [{"_": "20250000"}]
        self.assertEqual(obtained["v65"], expected)

    def test_field_v223(self):
        obtained = am.get_dates(self.xml_tree)
        self.assertIsInstance(obtained, dict)
        self.assertIn("v223", obtained)
        expected = [{"_": "20250127"}]
        self.assertEqual(obtained["v223"], expected)


class TestGetArticleAndSubarticle(BaseTest):
    def test_field_v40(self):
        obtained = am.get_article_and_subarticle(self.xml_tree)
        self.assertIsInstance(obtained, dict)
        self.assertIn("v40", obtained)

        self.assertEqual(obtained["v40"], [{"_": "en"}])

    def test_field_v120(self):
        obtained = am.get_article_and_subarticle(self.xml_tree)
        self.assertIsInstance(obtained, dict)
        self.assertIn("v120", obtained)

        self.assertEqual(obtained["v120"], [{"_": "XML_1.1"}])

    def test_field_v601(self):
        obtained = am.get_article_and_subarticle(self.xml_tree)
        self.assertIsInstance(obtained, dict)
        self.assertIn("v601", obtained)

        self.assertEqual(obtained["v601"], [{"_": "es"}, {"_": "pt"}])

    def test_field_v337(self):
        obtained = am.get_article_and_subarticle(self.xml_tree)
        self.assertIsInstance(obtained, dict)
        self.assertIn("v337", obtained)
        self.assertEqual(len(obtained["v337"]), 3)

        self.assertEqual(
            obtained["v337"][0],
            {"d": "10.1590/1518-8345.7320.4434", "l": "en", "_": ""},
        )

    def test_field_v71(self):
        obtained = am.get_article_and_subarticle(self.xml_tree)
        self.assertIsInstance(obtained, dict)
        self.assertIn("v71", obtained)

        self.assertEqual(obtained["v71"], [{"_": "oa"}])


class TestGetArticleAbstract(BaseTest):
    def test_field_v83(self):
        obtained = am.get_article_abstract(self.xml_tree)
        self.assertIsInstance(obtained, dict)
        self.assertIn("v83", obtained)
        self.assertGreater(len(obtained["v83"]), 0)

        abstract = obtained["v83"][0]
        expected_keys = {"a", "l", "_"}
        self.assertTrue(expected_keys.issubset(abstract.keys()))


class TestGetKeyWord(BaseTest):
    def test_field_v85(self):
        obtained = am.get_keyword(self.xml_tree)
        self.assertIsInstance(obtained, dict)
        self.assertIn("v85", obtained)
        self.assertGreater(len(obtained["v85"]), 0)

        keyword = obtained["v85"][0]
        expected_keys = {"k", "l", "_"}
        self.assertTrue(expected_keys.issubset(keyword.keys()))


class TestGetTitle(BaseTest):
    def test_field_v12(self):
        obtained = am.get_title(self.xml_tree)
        self.assertIsInstance(obtained, dict)
        self.assertIn("v12", obtained)
        self.assertEqual(len(obtained["v12"]), 3)

        title = obtained["v12"][0]
        expected_keys = {"l", "_"}
        self.assertTrue(expected_keys.issubset(title.keys()))
        self.assertEqual(title["l"], "en")
        self.assertEqual(
            title["_"],
            "Play Nicely Program in the prevention of violence against children: "
            "strengthening sustainable development",
        )


class TestExternalFields(BaseTest):
    def test_field_v999(self):
        obtained = am.get_external_fields(self.data)
        self.assertIsInstance(obtained, dict)
        self.assertIn("v999", obtained)
        self.assertEqual(obtained["v999"], [{"_": "../bases-work/rlae/rlae"}])

    def test_field_v38(self):
        obtained = am.get_external_fields(self.data)
        self.assertIsInstance(obtained, dict)
        self.assertIn("v38", obtained)
        self.assertEqual(obtained["v38"], [{"_": "GRA"}])

    def test_field_v992(self):
        obtained = am.get_external_fields(self.data)
        self.assertIsInstance(obtained, dict)
        self.assertIn("v992", obtained)
        self.assertEqual(obtained["v992"], [{"_": "scl"}])

    def test_field_v42(self):
        obtained = am.get_external_fields(self.data)
        self.assertIsInstance(obtained, dict)
        self.assertIn("v42", obtained)
        self.assertEqual(obtained["v42"], [{"_": "1"}])

    def test_field_v49(self):
        obtained = am.get_external_fields(self.data)
        self.assertIsInstance(obtained, dict)
        self.assertIn("v49", obtained)
        self.assertEqual(obtained["v49"], [{"_": "RLAE350"}])

    def test_field_v706(self):
        obtained = am.get_external_fields(self.data)
        self.assertIsInstance(obtained, dict)
        self.assertIn("v706", obtained)
        self.assertEqual(obtained["v706"], [{"_": "h"}])

    def test_field_collection(self):
        obtained = am.get_external_fields(self.data)
        self.assertIsInstance(obtained, dict)
        self.assertIn("collection", obtained)
        self.assertEqual(obtained["collection"], "scl")

    def test_field_v2(self):
        obtained = am.get_external_fields(self.data)
        self.assertIsInstance(obtained, dict)
        self.assertIn("v2", obtained)
        self.assertEqual(obtained["v2"], [{"_": "S0104-1169(25)03300000300"}])

    def test_field_v91(self):
        obtained = am.get_external_fields(self.data)
        self.assertIsInstance(obtained, dict)
        self.assertIn("v91", obtained)
        self.assertEqual(obtained["v91"], [{"_": "20250203"}])

    def test_field_v701(self):
        obtained = am.get_external_fields(self.data)
        self.assertIsInstance(obtained, dict)
        self.assertIn("v701", obtained)
        self.assertEqual(obtained["v701"], [{"_": "1"}])


if __name__ == "__main__":
    unittest.main()
