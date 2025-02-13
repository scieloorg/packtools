import unittest
from unittest.mock import Mock, patch

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
                            <name>
                                <surname>Smith</surname>
                                <given-names>John</given-names>
                            </name>
                        </contrib>
                        <contrib contrib-type="author">
                            <name>
                                <surname>Johnson</surname>
                                <given-names>Mary</given-names>
                            </name>
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
                <article-id pub-id-type="other">00303</article-id>
            </front>
        </article>
        """
        xmltree = etree.fromstring(xml_without_doi.encode("utf-8"))
        validator = ArticleDoiValidation(xmltree)

        results = list(validator.validate_doi_exists())
        errors = [r for r in results if r["response"] != "OK"]

        self.assertEqual(len(errors), 1)

        responses = [error["response"] for error in errors]
        advices = [error["advice"] for error in errors]

        expected_responses = ["CRITICAL"]
        expected_advices = [
            'Mark DOI for <article> with<article-id pub-id-type="doi"></article-id>'
        ]

        self.assertEqual(responses, expected_responses)
        self.assertEqual(advices, expected_advices)

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
                <article-id pub-id-type="doi">10.1590/same-doi</article-id>
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

        responses = [error["response"] for error in errors]
        advices = [error["advice"] for error in errors]

        expected_responses = ["CRITICAL"]
        expected_advices = [
            "Fix doi to be unique. Found repetition: ['10.1590/same-doi']"
        ]

        self.assertEqual(responses, expected_responses)
        self.assertEqual(advices, expected_advices)

    @patch("packtools.sps.validation.utils.check_doi_is_registered")
    def test_validate_doi_registered(self, mock_check_doi):
        """Test validation of DOI registration"""
        # Configure the mock to return an error
        mock_check_doi.return_value = {
            "valid": False,
            "registered": {
                "article title": "Different Title",
                "authors": ["Different Author"],
            },
        }

        # Set skip_doi_check to True to enable validation
        self.validator.params["skip_doi_check"] = True

        results = list(self.validator.validate_doi_registered(mock_check_doi))
        errors = [r for r in results if r["response"] != "OK"]

        self.assertEqual(
            len(errors), 2
        )  # Should have errors for both main article and translation

        responses = [error["response"] for error in errors]
        advices = [error["advice"] for error in errors]

        expected_responses = ["CRITICAL", "CRITICAL"]
        expected_advices = [
            """Check doi (<article-id pub-id-type="doi">10.1590/1518-8345.2927.3231</article-id>) is not registered for {"article title": "Main article title", "authors": ["Smith, John", "Johnson, Mary"]}. It is registered for {"article title": "Different Title", "authors": ["Different Author"]}""",
            """Check doi (<article-id pub-id-type="doi">10.1590/2176-4573e59270</article-id>) is not registered for {"article title": "Título do artigo em português", "authors": ["Smith, John", "Johnson, Mary"]}. It is registered for {"article title": "Different Title", "authors": ["Different Author"]}""",
        ]

        for i, got in enumerate(expected_responses):
            with self.subTest(i):
                self.assertEqual(responses[i], got)
        for i, got in enumerate(expected_advices):
            with self.subTest(i):
                print(got)
                print(advices[i])
                self.assertEqual(advices[i], got)

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
                <article-id pub-id-type="doi">10.1590/same-doi</article-id>
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
        print(results)
        errors = [r for r in results if r["response"] != "OK"]

        self.assertEqual(len(errors), 1)

        responses = [error["response"] for error in errors]
        advices = [error["advice"] for error in errors]

        expected_responses = ["WARNING"]
        expected_advices = [
            'Change 10.1590/same-doi in <sub-article id="s1"><article-id pub-id-type="doi">10.1590/same-doi</article-id> for a DOI different from ["10.1590/same-doi"]'
        ]

        self.assertEqual(responses, expected_responses)
        self.assertEqual(advices, expected_advices)


if __name__ == "__main__":
    unittest.main()
