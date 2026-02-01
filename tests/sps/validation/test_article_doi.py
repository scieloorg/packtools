import unittest
from unittest.mock import patch

from lxml import etree

from packtools.sps.validation.article_doi import ArticleDoiValidation


class TestArticleDoiValidation(unittest.TestCase):
    def setUp(self):
        self.sample_xml = """
        <article xmlns:mml="http://www.w3.org/1998/Math/MathML" 
                xmlns:xlink="http://www.w3.org/1999/xlink"
                article-type="research-article" 
                specific-use="sps-1.9" 
                xml:lang="en">
            <front>
                <article-meta>
                    <article-id pub-id-type="publisher-id" specific-use="scielo-v3">TPg77CCrGj4wcbLCh9vG8bS</article-id>
                    <article-id pub-id-type="publisher-id" specific-use="scielo-v2">S0104-11692020000100303</article-id>
                    <article-id pub-id-type="doi">10.1590/1518-8345.2927.3231</article-id>
                    <article-id pub-id-type="other">00303</article-id>
                    <title-group>
                        <article-title>Main article title</article-title>
                        <trans-title-group xml:lang="pt">
                            <trans-title>Título do artigo em português</trans-title>
                        </trans-title-group>
                    </title-group>
                    <contrib-group>
                        <contrib contrib-type="author">
                            <n>
                                <surname>Smith</surname>
                                <given-names>John</given-names>
                            </n>
                        </contrib>
                        <contrib contrib-type="author">
                            <n>
                                <surname>Johnson</surname>
                                <given-names>Mary</given-names>
                            </n>
                        </contrib>
                    </contrib-group>
                </article-meta>
            </front>
            <sub-article article-type="translation" id="s1" xml:lang="pt">
                <front-stub>
                    <article-id pub-id-type="doi">10.1590/2176-4573e59270</article-id>
                    <title-group>
                        <article-title>Título do artigo em português</article-title>
                    </title-group>
                </front-stub>
            </sub-article>
        </article>
        """
        self.xmltree = etree.fromstring(self.sample_xml.encode("utf-8"))
        self.validator = ArticleDoiValidation(self.xmltree)

    def test_initialization(self):
        """Test the initialization of ArticleDoiValidation"""
        self.assertIsNotNone(self.validator)
        self.assertEqual(self.validator.params.get("skip_doi_check"), False)
        self.assertIsNotNone(self.validator.articles)
        self.assertIsNotNone(self.validator.doi)

    def test_validate_doi_exists(self):
        """Test validation of DOI existence"""
        results = list(self.validator.validate_doi_exists())
        errors = [r for r in results if r["response"] != "OK"]
        self.assertEqual(len(errors), 0)

    def test_validate_doi_exists_missing_doi(self):
        """Test validation when DOI is missing"""
        xml_without_doi = """
        <article article-type="research-article" xml:lang="en">
            <front>
                <article-meta>
                    <article-id pub-id-type="other">00303</article-id>
                </article-meta>
            </front>
        </article>
        """
        xmltree = etree.fromstring(xml_without_doi.encode("utf-8"))
        validator = ArticleDoiValidation(xmltree)

        results = list(validator.validate_doi_exists())
        errors = [r for r in results if r["response"] != "OK"]

        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0]["response"], "CRITICAL")
        self.assertIn('Mark DOI', errors[0]["advice"])

    def test_validate_doi_exists_all_subarticles(self):
        """Test validation of DOI in ALL sub-article types"""
        xml_with_multiple_subarticles = """
        <article article-type="research-article" xml:lang="en">
            <front>
                <article-meta>
                    <article-id pub-id-type="doi">10.1590/main-doi</article-id>
                </article-meta>
            </front>
            <sub-article article-type="translation" id="s1" xml:lang="pt">
                <front-stub>
                    <article-id pub-id-type="doi">10.1590/translation-doi</article-id>
                </front-stub>
            </sub-article>
            <sub-article article-type="reviewer-report" id="s2" xml:lang="en">
                <front-stub>
                    <!-- Missing DOI -->
                </front-stub>
            </sub-article>
        </article>
        """
        xmltree = etree.fromstring(xml_with_multiple_subarticles.encode("utf-8"))
        validator = ArticleDoiValidation(xmltree)

        results = list(validator.validate_doi_exists_all_subarticles())
        errors = [r for r in results if r["response"] != "OK"]

        # Should detect missing DOI in reviewer-report
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0]["parent_article_type"], "reviewer-report")

    def test_validate_all_dois_are_unique(self):
        """Test validation of DOI uniqueness"""
        results = list(self.validator.validate_all_dois_are_unique())
        errors = [r for r in results if r["response"] != "OK"]
        self.assertEqual(len(errors), 0)

    def test_validate_all_dois_are_unique_with_duplicates(self):
        """Test validation when there are duplicate DOIs"""
        xml_with_duplicate_doi = """
        <article article-type="research-article" xml:lang="en">
            <front>
                <article-meta>
                    <article-id pub-id-type="doi">10.1590/same-doi</article-id>
                </article-meta>
            </front>
            <sub-article article-type="translation" id="s1" xml:lang="pt">
                <front-stub>
                    <article-id pub-id-type="doi">10.1590/same-doi</article-id>
                </front-stub>
            </sub-article>
        </article>
        """
        xmltree = etree.fromstring(xml_with_duplicate_doi.encode("utf-8"))
        validator = ArticleDoiValidation(xmltree)

        results = list(validator.validate_all_dois_are_unique())
        errors = [r for r in results if r["response"] != "OK"]

        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0]["response"], "CRITICAL")
        self.assertIn("10.1590/same-doi", errors[0]["advice"])

    @patch("packtools.sps.validation.utils.check_doi_is_registered")
    def test_validate_doi_registered_correct_logic(self, mock_check_doi):
        """Test that skip_doi_check logic works correctly (bug fix)"""
        mock_check_doi.return_value = {
            "valid": False,
            "registered": {
                "article title": "Different Title",
                "authors": ["Different Author"],
            },
        }

        # FIXED: skip_doi_check=False should EXECUTE validation
        self.validator.params["skip_doi_check"] = False

        results = list(self.validator.validate_doi_registered(mock_check_doi))

        # Should have results (validation executed)
        self.assertEqual(len(results), 2)  # Main article + translation

    @patch("packtools.sps.validation.utils.check_doi_is_registered")
    def test_validate_doi_registered_skip(self, mock_check_doi):
        """Test that skip_doi_check=True skips validation"""
        mock_check_doi.return_value = {"valid": True}

        # skip_doi_check=True should SKIP validation
        self.validator.params["skip_doi_check"] = True

        results = list(self.validator.validate_doi_registered(mock_check_doi))

        # Should have NO results (validation skipped)
        self.assertEqual(len(results), 0)

    def test_validate_different_doi_in_translation(self):
        """Test validation of different DOIs in translations"""
        results = list(self.validator.validate_different_doi_in_translation())
        errors = [r for r in results if r["response"] != "OK"]
        self.assertEqual(len(errors), 0)

    def test_validate_different_doi_in_translation_with_duplicate(self):
        """Test validation when translation has same DOI as main article"""
        xml_with_duplicate = """
        <article article-type="research-article" xml:lang="en">
            <front>
                <article-meta>
                    <article-id pub-id-type="doi">10.1590/same-doi</article-id>
                </article-meta>
            </front>
            <sub-article article-type="translation" id="s1" xml:lang="pt">
                <front-stub>
                    <article-id pub-id-type="doi">10.1590/same-doi</article-id>
                </front-stub>
            </sub-article>
        </article>
        """
        xmltree = etree.fromstring(xml_with_duplicate.encode("utf-8"))
        validator = ArticleDoiValidation(xmltree)

        results = list(validator.validate_different_doi_in_translation())
        errors = [r for r in results if r["response"] != "OK"]

        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0]["response"], "WARNING")

    def test_validate_doi_format_valid(self):
        """Test DOI format validation with valid DOI"""
        results = list(self.validator.validate_doi_format())
        errors = [r for r in results if r["response"] != "OK"]
        self.assertEqual(len(errors), 0)

    def test_validate_doi_format_invalid_characters(self):
        """Test DOI format validation with invalid characters"""
        xml_with_invalid_doi = """
        <article article-type="research-article" xml:lang="en">
            <front>
                <article-meta>
                    <article-id pub-id-type="doi">10.1590/artigo\\invalido</article-id>
                </article-meta>
            </front>
        </article>
        """
        xmltree = etree.fromstring(xml_with_invalid_doi.encode("utf-8"))
        validator = ArticleDoiValidation(xmltree)

        results = list(validator.validate_doi_format())
        errors = [r for r in results if r["response"] != "OK"]

        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0]["response"], "ERROR")
        self.assertIn("inválido", errors[0]["advice"].lower())

    def test_validate_doi_format_with_allowed_special_chars(self):
        """Test DOI format validation with all allowed special characters"""
        xml_with_special_chars = """
        <article article-type="research-article" xml:lang="en">
            <front>
                <article-meta>
                    <article-id pub-id-type="doi">10.1590/test-article_2024;(part1)/section</article-id>
                </article-meta>
            </front>
        </article>
        """
        xmltree = etree.fromstring(xml_with_special_chars.encode("utf-8"))
        validator = ArticleDoiValidation(xmltree)

        results = list(validator.validate_doi_format())
        errors = [r for r in results if r["response"] != "OK"]

        # Should be valid (all chars are allowed: - _ ; ( ) /)
        self.assertEqual(len(errors), 0)


if __name__ == "__main__":
    unittest.main()
