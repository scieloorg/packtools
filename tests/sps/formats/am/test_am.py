import unittest

from packtools.sps.utils import xml_utils
from packtools.sps.formats.am import am


class BaseTest(unittest.TestCase):
    def setUp(self):
        self.xml_tree = xml_utils.get_xml_tree(
            "tests/sps/formats/am/examples/S0104-11692025000100300/S0104-11692025000100300.xml"
        )

        self.external_data = {
            "v999": "../bases-work/rlae/rlae",
            "v992": "scl",
            "v35": "0104-1169",
            "v42": "1",
            "collection": "scl",
            "v701": "1",
            "v38": "GRA",
            "v49": "RLAE350",
            "v2": "S0104-1169(25)03300000300",
            "v91": "20250203",
            "v702": "rlae/v33/1518-8345-rlae-33-e4434.xml",
            "v705": "S",
            "processing_date": "2025-02-03",
            "citations_processing_date": "2025-04-28",
            "v265": [
                {"k": "real", "s": "xml", "v": "20250127"},
                {"k": "expected", "s": "xml", "v": "202500"},
            ],
            "v3": "1518-8345-rlae-33-e4434.xml",
            "v936": {"i": "0104-1169", "y": "2025", "o": "1"},
            "applicable": "True",
            "created_at": "2025-02-03",
            "sent_wos": "False",
            "validated_scielo": "False",
            "validated_wos": "False",
            "version": "xml",
        }


class TestGetJournal(BaseTest):
    def setUp(self):
        super().setUp()
        self.journal_data = am.get_journal(self.xml_tree)

    def test_field_v30(self):
        self.assertEqual(
            self.journal_data["v30"], [{"_": "Rev. Latino-Am. Enfermagem"}]
        )

    def test_field_v421(self):
        self.assertEqual(self.journal_data["v421"], [{"_": "Rev Lat Am Enfermagem"}])

    def test_field_v62(self):
        self.assertEqual(
            self.journal_data["v62"],
            [
                {
                    "_": "Escola de Enfermagem de Ribeirão Preto / Universidade de São Paulo"
                }
            ],
        )

    def test_field_v435(self):
        self.assertEqual(self.journal_data["v435"], [{"_": "1518-8345", "t": "epub"}])

    def test_field_v100(self):
        self.assertEqual(
            self.journal_data["v100"], [{"_": "Revista Latino-Americana de Enfermagem"}]
        )

    def test_journal_returns_expected_fields(self):
        self.assertTrue(
            {"v30", "v421", "v62", "v435", "v100"}.issubset(self.journal_data.keys())
        )


class TestGetArticlemetaIssue(BaseTest):
    def setUp(self):
        super().setUp()
        self.issue_data = am.get_articlemeta_issue(self.xml_tree)

    def test_field_v31(self):
        self.assertEqual(self.issue_data["v31"], [{"_": "33"}])

    def test_field_v121(self):
        self.assertEqual(self.issue_data["v121"], [{"_": "00300"}])

    def test_field_v14(self):
        self.assertEqual(self.issue_data["v14"], [{"e": "e4434", "_": ""}])

    def test_field_v709(self):
        self.assertEqual(self.issue_data["v709"], [{"_": "article"}])

    def test_issue_returns_expected_fields(self):
        self.assertTrue(
            {"v31", "v121", "v14", "v709"}.issubset(
                self.issue_data.keys()
            )
        )


class TestGetIds(BaseTest):
    def setUp(self):
        super().setUp()
        self.ids_data = am.get_ids(self.xml_tree)

    def test_field_v237(self):
        self.assertEqual(self.ids_data["v237"], [{"_": "10.1590/1518-8345.7320.4434"}])



class TestGetContribs(BaseTest):
    def setUp(self):
        super().setUp()
        self.contribs_data = am.get_contribs(self.xml_tree)

    def test_field_v10(self):
        self.assertIn("v10", self.contribs_data)
        self.assertGreater(len(self.contribs_data["v10"]), 0)

        author = self.contribs_data["v10"][0]
        self.assertTrue({"k", "n", "1", "s", "r", "_"}.issubset(author.keys()))

    def test_field_v10_includes_specific_author(self):
        author = next(
            (a for a in self.contribs_data["v10"] if a["k"] == "0000-0002-4201-0624"),
            None,
        )
        self.assertIsNotNone(author)

        self.assertEqual(author["n"], "Janaina Recanello")
        self.assertEqual(author["s"], "Begui")
        self.assertEqual(author["1"], "aff1")
        self.assertEqual(author["r"], "ND")


class TestGetAffs(BaseTest):
    def setUp(self):
        super().setUp()
        self.aff_data = am.get_affs(self.xml_tree)

    def test_field_v70(self):
        self.assertEqual(len(self.aff_data["v70"]), 4)

        aff = self.aff_data["v70"][0]
        self.assertTrue({"c", "i", "l", "1", "p", "s", "_"}.issubset(aff.keys()))

    def test_field_v240(self):
        self.assertEqual(len(self.aff_data["v240"]), 4)

        aff = self.aff_data["v240"][0]
        self.assertTrue({"c", "i", "p", "s", "_"}.issubset(aff.keys()))

    def test_affs_returns_expected_fields(self):
        self.assertTrue({"v70", "v240"}.issubset(self.aff_data.keys()))


class TestGetCitations(BaseTest):
    def setUp(self):
        super().setUp()
        self.am_format = am.build(self.xml_tree, self.external_data)
        self.first_ref = self.am_format["citations"][0]
        self.last_ref = self.am_format["citations"][-1]

    def test_field_v72(self):
        self.assertEqual(self.am_format["article"]["v72"], [{"_": "35"}])

    def test_references_structure(self):
        self.assertEqual(len(self.am_format["citations"]), 35)

    def test_field_v30(self):
        self.assertEqual(self.first_ref["v30"], [{"_": "Am J Psychiatry"}])

    def test_field_v31(self):
        self.assertEqual(self.first_ref["v31"], [{"_": "177"}])

    def test_field_v32(self):
        self.assertEqual(self.first_ref["v32"], [{"_": "1"}])

    def test_field_code(self):
        self.assertEqual(self.first_ref["code"], "S0104-1169202500010030000001")
        self.assertEqual(self.last_ref["code"], "S0104-1169202500010030000035")

    def test_field_v999(self):
        self.assertEqual(self.first_ref["v999"], [{"_": "../bases-work/rlae/rlae"}])

    def test_field_v37(self):
        self.assertEqual(
            self.first_ref["v37"],
            [{"_": "https://doi.org/10.1176/appi.ajp.2019.19010020"}],
        )

    def test_field_v12(self):
        self.assertEqual(
            self.first_ref["v12"],
            [
                {
                    "_": "The Devastating Clinical Consequences of Child Abuse and Neglect: Increased Disease Vulnerability and Poor Treatment Response in Mood Disorders"
                }
            ],
        )

    def test_field_v10(self):
        self.assertEqual(len(self.first_ref["v10"]), 2)
        self.assertEqual(self.first_ref["v10"][0]["n"], "E. T. C.")
        self.assertEqual(self.first_ref["v10"][0]["s"], "Lippard")
        self.assertEqual(self.first_ref["v10"][0]["r"], "ND")
        self.assertEqual(self.first_ref["v10"][0]["_"], "")

    def test_field_v71(self):
        self.assertEqual(self.first_ref["v71"], [{"_": "journal"}])

    def test_field_v14(self):
        self.assertEqual(self.first_ref["v14"], [{"_": "20-36"}])

    def test_field_v936(self):
        self.assertEqual(
            self.first_ref["v936"], [{"i": "0104-1169", "y": "2025", "o": "1"}]
        )

    def test_field_v880(self):
        self.assertEqual(self.first_ref["v880"], [{"_": "S0104-1169202500010030000001"}])
        self.assertEqual(self.last_ref["v880"], [{"_": "S0104-1169202500010030000035"}])

    def test_field_v865(self):
        self.assertEqual(self.first_ref["v865"], [{"_": "20250000"}])

    def test_field_v118(self):
        self.assertEqual(self.first_ref["v118"], [{"_": "1."}])

    def test_field_v706(self):
        self.assertEqual(self.first_ref["v706"], [{"_": "c"}])

    def test_field_v64(self):
        self.assertEqual(self.first_ref["v64"], [{"_": "2020"}])

    def test_field_v65(self):
        self.assertEqual(self.first_ref["v65"], [{"_": "20200000"}])

    def test_field_collection(self):
        self.assertEqual(self.first_ref["collection"], "scl")

    def test_field_v708(self):
        self.assertEqual(self.first_ref["v708"], [{"_": "35"}])

    def test_field_v2(self):
        self.assertEqual(self.first_ref["v2"], [{"_": "S0104-1169(25)03300000300"}])

    def test_field_v3(self):
        self.assertEqual(self.first_ref["v3"], [{"_": "1518-8345-rlae-33-e4434.xml"}])

    def test_field_v4(self):
        self.assertEqual(self.first_ref["v4"], [{"_": "V33"}])

    def test_field_v992(self):
        self.assertEqual(self.first_ref["v992"], [{"_": "scl"}])

    def test_field_v701(self):
        self.assertEqual(self.first_ref["v701"], [{"_": "1"}])

    def test_field_v702(self):
        self.assertEqual(
            self.first_ref["v702"], [{"_": "rlae/v33/1518-8345-rlae-33-e4434.xml"}]
        )

    def test_field_v705(self):
        self.assertEqual(self.first_ref["v705"], [{"_": "S"}])

    def test_field_processing_date(self):
        self.assertEqual(self.first_ref["processing_date"], "2025-04-28")

    def test_field_v514(self):
        self.assertEqual(self.first_ref["v514"], [{"_": "", "f": "20", "l": "36"}])
        self.assertEqual(self.last_ref["v514"], [{"_": "", "f": "226", "l": "55"}])

    def test_field_v882(self):
        self.assertEqual(self.first_ref["v882"], [{"_": "", "v": "33"}])


class TestGetDates(BaseTest):
    def setUp(self):
        super().setUp()
        self.dates_data = am.get_dates(self.xml_tree)

    def test_field_v114(self):
        self.assertEqual(self.dates_data["v114"], [{"_": "20240811"}])

    def test_field_v112(self):
        self.assertEqual(self.dates_data["v112"], [{"_": "20240208"}])

    def test_field_v65(self):
        self.assertEqual(self.dates_data["v65"], [{"_": "20250000"}])

    def test_field_v223(self):
        self.assertEqual(self.dates_data["v223"], [{"_": "20250127"}])


class TestGetArticleAndSubarticle(BaseTest):
    def setUp(self):
        super().setUp()
        self.article_data = am.get_article_and_subarticle(self.xml_tree)

    def test_field_v40(self):
        self.assertEqual(self.article_data["v40"], [{"_": "en"}])

    def test_field_v120(self):
        self.assertEqual(self.article_data["v120"], [{"_": "XML_1.1"}])

    def test_field_v601(self):
        self.assertEqual(self.article_data["v601"], [{"_": "es"}, {"_": "pt"}])

    def test_field_v337(self):
        self.assertEqual(len(self.article_data["v337"]), 3)
        self.assertEqual(
            self.article_data["v337"][0],
            {"d": "10.1590/1518-8345.7320.4434", "l": "en", "_": ""},
        )

    def test_field_v71(self):
        self.assertEqual(self.article_data["v71"], [{"_": "oa"}])


class TestGetArticleAbstract(BaseTest):
    def setUp(self):
        super().setUp()
        self.abstract_data = am.get_article_abstract(self.xml_tree)

    def test_field_v83(self):
        self.assertGreater(len(self.abstract_data["v83"]), 0)

        abstract = self.abstract_data["v83"][0]
        self.assertTrue({"a", "l", "_"}.issubset(abstract.keys()))


class TestGetKeyWord(BaseTest):
    def setUp(self):
        super().setUp()
        self.keyword_data = am.get_keyword(self.xml_tree)

    def test_field_v85(self):
        self.assertGreater(len(self.keyword_data["v85"]), 0)

        keyword = self.keyword_data["v85"][0]
        self.assertTrue({"k", "l", "_"}.issubset(keyword.keys()))


class TestGetTitle(BaseTest):
    def setUp(self):
        super().setUp()
        self.title_data = am.get_title(self.xml_tree)

    def test_field_v12(self):
        self.assertEqual(len(self.title_data["v12"]), 3)

        title = self.title_data["v12"][0]
        self.assertTrue({"l", "_"}.issubset(title.keys()))
        self.assertEqual(title["l"], "en")
        self.assertEqual(
            title["_"],
            "Play Nicely Program in the prevention of violence against children: "
            "strengthening sustainable development",
        )


class TestGetFunding(BaseTest):
    def setUp(self):
        self.xml_tree = xml_utils.get_xml_tree(
            "tests/sps/formats/am/examples/S0034-89102025000100200/S0034-89102025000100200.xml"
        )
        self.funding_data = am.get_funding(self.xml_tree)

    def test_field_v102(self):
        self.assertEqual(
            self.funding_data["v102"],
            [{"_": "Funding: Coordenação de Aperfeiçoamento Pessoal de Nível Superior (CAPES – PhD fellowship for AFF). "
            "Conselho Nacional de Desenvolvimento Científico e Tecnológico (CNPq – productivity fellowship for ANRJ)."}])


class TestExternalFields(BaseTest):
    def setUp(self):
        super().setUp()
        self.external_data_formated = am.get_external_article_data(self.external_data)
        self.external_data_common_formated = am.get_external_common_data(self.external_data)
        self.external_data_formated.update(self.external_data_common_formated)

    def test_field_v999(self):
        self.assertEqual(self.external_data_formated["v999"], [{"_": "../bases-work/rlae/rlae"}])

    def test_field_v38(self):
        self.assertEqual(self.external_data_formated["v38"], [{"_": "GRA"}])

    def test_field_v992(self):
        self.assertEqual(self.external_data_formated["v992"], [{"_": "scl"}])

    def test_field_v42(self):
        self.assertEqual(self.external_data_formated["v42"], [{"_": "1"}])

    def test_field_v49(self):
        self.assertEqual(self.external_data_formated["v49"], [{"_": "RLAE350"}])

    def test_field_collection(self):
        self.assertEqual(self.external_data_formated["collection"], "scl")

    def test_field_v2(self):
        self.assertEqual(self.external_data_formated["v2"], [{"_": "S0104-1169(25)03300000300"}])

    def test_field_v91(self):
        self.assertEqual(self.external_data_formated["v91"], [{"_": "20250203"}])

    def test_field_v701(self):
        self.assertEqual(self.external_data_formated["v701"], [{"_": "1"}])

    def test_field_v702(self):
        self.assertEqual(
            self.external_data_formated["v702"], [{"_": "rlae/v33/1518-8345-rlae-33-e4434.xml"}]
        )

    def test_field_v705(self):
        self.assertEqual(self.external_data_formated["v705"], [{"_": "S"}])

    def test_field_v3(self):
        self.assertEqual(
            self.external_data_formated["v3"], [{"_": "1518-8345-rlae-33-e4434.xml"}]
        )

    def test_field_v35_from_article_data(self):
        self.assertEqual(self.external_data_formated["v35"], [{"_": "0104-1169"}])

    def test_field_processing_date(self):
        self.assertEqual(self.external_data_formated["processing_date"], "2025-02-03")

    def test_field_v265(self):
        self.assertEqual(len(self.external_data_formated["v265"]), 2)
        self.assertEqual(
            self.external_data_formated["v265"][0], {"k": "real", "s": "xml", "v": "20250127"}
        )
        self.assertEqual(
            self.external_data_formated["v265"][1], {"k": "expected", "s": "xml", "v": "202500"}
        )

    def test_field_v936(self):
        self.assertEqual(
            self.external_data_formated["v936"], [{"i": "0104-1169", "y": "2025", "o": "1"}]
        )


if __name__ == "__main__":
    unittest.main()
