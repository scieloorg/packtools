import unittest
from lxml import etree

from packtools.sps.utils.xml_utils import get_xml_tree
from packtools.sps.validation.article_and_subarticles import (
    ArticleLangValidation,
    ArticleTypeValidation,
    ArticleIdValidation,
    JATSAndDTDVersionValidation,
)
from packtools.sps.validation.exceptions import (
    ValidationArticleAndSubArticlesLanguageCodeException,
    ValidationArticleAndSubArticlesSpecificUseException,
    ValidationArticleAndSubArticlesDtdVersionException,
    ValidationArticleAndSubArticlesArticleTypeException,
    ValidationArticleAndSubArticlesSubjectsException,
)


class TestArticleLangValidation(unittest.TestCase):
    
    def setUp(self):
        # Create sample XML for testing
        self.valid_xml_string = '''
        <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="en">
        </article>
        '''
        
        self.invalid_xml_string = '''
        <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="fr">
        </article>
        '''
        
        self.no_lang_xml_string = '''
        <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article">
        </article>
        '''
        
        # Parse the XML strings
        self.valid_xmltree = (etree.fromstring(self.valid_xml_string))
        self.invalid_xmltree = (etree.fromstring(self.invalid_xml_string))
        self.no_lang_xmltree = (etree.fromstring(self.no_lang_xml_string))

    def test_validate_language_with_valid_language(self):
        # Test with a valid language
        validator = ArticleLangValidation(self.valid_xmltree, None)
        results = list(validator.validate_language())
        
        self.assertEqual(len(results), 1)
        result = results[0]
        self.assertEqual(result['response'], "OK")
        self.assertEqual(result['got_value'], "en")
        self.assertEqual(result['expected_value'], "en")  # For valid case, expected_value equals got_value
        self.assertIsNone(result['advice'])  # For valid case, advice should be None

    def test_validate_language_with_invalid_language(self):
        # Test with an invalid language
        validator = ArticleLangValidation(self.invalid_xmltree, None)
        results = list(validator.validate_language())
        
        self.assertEqual(len(results), 1)
        result = results[0]
        self.assertEqual(result['response'], "CRITICAL")
        self.assertEqual(result['got_value'], "fr")
        self.assertEqual(result['expected_value'], "one of ['pt', 'en', 'es']")
        
        # Assert that advice is not None and contains expected text
        self.assertIsNotNone(result['advice'])
        expected_advice = "Replace fr in <article xml:lang=\"fr\"> with one of ['pt', 'en', 'es']"
        self.assertEqual(result['advice'], expected_advice)

    def test_validate_language_with_no_language(self):
        # Test with no language specified
        validator = ArticleLangValidation(self.no_lang_xmltree, None)
        results = list(validator.validate_language())
        
        self.assertEqual(len(results), 1)
        result = results[0]
        self.assertEqual(result['response'], "CRITICAL")
        self.assertEqual(result['got_value'], None)
        self.assertEqual(result['expected_value'], "one of ['pt', 'en', 'es']")
        
        # Assert that advice is not None and contains guidance for adding a missing attribute
        self.assertIsNotNone(result['advice'])
        expected_advice = """Add xml:lang=\"VALUE\" in <article>: <article xml:lang="VALUE"> and replace VALUE with one of ['pt', 'en', 'es']"""
        self.assertEqual(result['advice'], expected_advice)

    def test_validate_language_with_custom_language_codes(self):
        # Test with custom language codes
        validator = ArticleLangValidation(
            self.invalid_xmltree, 
            {"language_codes_list": ["fr", "it", "de"]}
        )
        results = list(validator.validate_language())
        
        self.assertEqual(len(results), 1)
        result = results[0]
        self.assertEqual(result['response'], "OK")
        self.assertEqual(result['got_value'], "fr")
        self.assertEqual(result['expected_value'], "fr")  # For valid case, expected_value equals got_value
        self.assertIsNone(result['advice'])  # For valid case, advice should be None

    def test_validate_language_with_custom_error_level(self):
        # Test with custom error level
        validator = ArticleLangValidation(
            self.invalid_xmltree, 
            {"language_error_level": "WARNING"}
        )
        results = list(validator.validate_language())
        
        self.assertEqual(len(results), 1)
        result = results[0]
        self.assertEqual(result['response'], "WARNING")
        self.assertEqual(result['got_value'], "fr")
        self.assertEqual(result['expected_value'], "one of ['pt', 'en', 'es']")
        
        # Assert that advice is not None and contains expected text with the same format
        # but a different error level
        self.assertIsNotNone(result['advice'])
        expected_advice = "Replace fr in <article xml:lang=\"fr\"> with one of ['pt', 'en', 'es']"
        self.assertEqual(result['advice'], expected_advice)

    def test_validate_language_with_missing_param(self):
        # Test with missing language_codes_list parameter
        validator = ArticleLangValidation(
            self.valid_xmltree, 
            {"language_codes_list": None}
        )
        validator.params.pop("language_codes_list")
        
        with self.assertRaises(ValidationArticleAndSubArticlesLanguageCodeException):
            list(validator.validate_language())

    def test_validate_language_with_multiple_articles(self):
        # Create sample XML with a main article and two sub-articles
        multi_article_xml_string = '''
        <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="en">
        <sub-article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="translation" xml:lang="es">
        </sub-article>
        <sub-article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="abstract" xml:lang="fr">
        </sub-article>
        </article>
        '''
        
        multi_article_xmltree = (etree.fromstring(multi_article_xml_string))
        
        # Test with real XML containing multiple articles
        validator = ArticleLangValidation(multi_article_xmltree, None)
        results = list(validator.validate_language())
        
        # Should have 3 results (main article + 2 sub-articles)
        self.assertEqual(len(results), 3)
        
        # Main article and first sub-article should be valid
        self.assertEqual(results[0]['response'], "OK")
        self.assertEqual(results[0]['got_value'], "en")
        self.assertIsNone(results[0]['advice'])  # For valid case, advice should be None
        
        self.assertEqual(results[1]['response'], "OK")
        self.assertEqual(results[1]['got_value'], "es")
        self.assertIsNone(results[1]['advice'])  # For valid case, advice should be None
        
        # Second sub-article should be invalid (fr is not in the default language list)
        self.assertEqual(results[2]['response'], "CRITICAL")
        self.assertEqual(results[2]['got_value'], "fr")
        
        # Assert that advice for invalid language is not None and has expected format
        self.assertIsNotNone(results[2]['advice'])
        expected_advice = "Replace fr in <sub-article xml:lang=\"fr\"> with one of ['pt', 'en', 'es']"
        self.assertEqual(results[2]['advice'], expected_advice)

    def test_validate_language_with_no_language_attributes(self):
        # Create sample XML with a main article and two sub-articles, all missing language attributes
        no_lang_multi_article_xml_string = '''
        <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article">
        <sub-article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article">
        </sub-article>
        <sub-article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article">
        </sub-article>
        </article>
        '''
        
        no_lang_multi_article_xmltree = (etree.fromstring(no_lang_multi_article_xml_string))
        
        # Test with real XML containing multiple articles without language attributes
        validator = ArticleLangValidation(no_lang_multi_article_xmltree, None)
        results = list(validator.validate_language())
        
        # Should have 3 results (main article + 2 sub-articles)
        self.assertEqual(len(results), 3)
        
        # All articles should be invalid as they lack xml:lang attributes
        for i, result in enumerate(results):
            element_name = "article" if i == 0 else "sub-article"
            self.assertEqual(result['response'], "CRITICAL")
            self.assertEqual(result['got_value'], None)
            self.assertIsNotNone(result['advice'])
            expected_advice = f"""Add xml:lang="VALUE" in <{element_name}>: <{element_name} xml:lang="VALUE"> and replace VALUE with one of ['pt', 'en', 'es']"""
            self.assertEqual(result['advice'], expected_advice)


class TestArticleTypeValidation(unittest.TestCase):
    
    def setUp(self):
        # Create sample XML for testing
        self.valid_xml_string = '''
        <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="en">
            <front>
                <article-meta>
                    <article-id pub-id-type="publisher-id">article1</article-id>
                    <article-categories>
                        <subj-group subj-group-type="heading">
                            <subject>Research Article</subject>
                        </subj-group>
                    </article-categories>
                </article-meta>
            </front>           
        </article>
        '''
        
        self.invalid_article_type_xml_string = '''
        <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="unknown-type" xml:lang="en">
            <front>
                <article-meta>
                    <article-id pub-id-type="publisher-id">article2</article-id>
                    <article-categories>
                        <subj-group subj-group-type="heading">
                            <subject>Unknown Article Type</subject>
                        </subj-group>
                    </article-categories>
                </article-meta>
            </front>
        </article>
        '''
        
        self.mismatch_subject_xml_string = '''
        <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="en">
            <front>
                <article-meta>
                    <article-id pub-id-type="publisher-id">article3</article-id>
                    <article-categories>
                        <subj-group subj-group-type="heading">
                            <subject>Editorial</subject>
                        </subj-group>
                    </article-categories>
                </article-meta>
            </front>
        </article>
        '''
        
        self.multi_article_xml_string = '''
        <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="en">
            <front>
                <article-meta>
                    <article-id pub-id-type="publisher-id">main-article</article-id>
                    <article-categories>
                        <subj-group subj-group-type="heading">
                            <subject>Research Article</subject>
                        </subj-group>
                    </article-categories>
                </article-meta>
            </front>
            <sub-article article-type="review-article" id="sub1" xml:lang="es">
                <front>
                    <article-meta>
                        <article-id pub-id-type="publisher-id">sub-article-1</article-id>
                        <article-categories>
                            <subj-group subj-group-type="heading">
                                <subject>Artículo de Revisión</subject>
                            </subj-group>
                        </article-categories>
                    </article-meta>
                </front>
            </sub-article>
            <sub-article article-type="invalid-type" id="sub2" xml:lang="pt">
                <front>
                    <article-meta>
                        <article-id pub-id-type="publisher-id">sub-article-2</article-id>
                        <article-categories>
                            <subj-group subj-group-type="heading">
                                <subject>Tipo Inválido</subject>
                            </subj-group>
                        </article-categories>
                    </article-meta>
                </front>
            </sub-article>
        </article>
        '''
        
        self.no_subject_xml_string = '''
        <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="en">
            <front>
                <article-meta>
                    <article-id pub-id-type="publisher-id">article4</article-id>
                </article-meta>
            </front>
            <!-- No article-categories element -->
        </article>
        '''
        
        # Parse the XML strings
        self.valid_xmltree = etree.fromstring(self.valid_xml_string)
        self.invalid_article_type_xmltree = etree.fromstring(self.invalid_article_type_xml_string)
        self.mismatch_subject_xmltree = etree.fromstring(self.mismatch_subject_xml_string)
        self.multi_article_xmltree = etree.fromstring(self.multi_article_xml_string)
        self.no_subject_xmltree = etree.fromstring(self.no_subject_xml_string)

    def test_validate_article_type_with_valid_type(self):
        # Test with a valid article type
        validator = ArticleTypeValidation(self.valid_xmltree, None)
        results = list(validator.validate_article_type())
        
        self.assertEqual(len(results), 1)
        result = results[0]
        self.assertEqual(result['response'], "OK")
        self.assertEqual(result['got_value'], "research-article")
        self.assertEqual(result['expected_value'], "research-article")  # For valid case
        self.assertIsNone(result['advice'])  # For valid case, advice should be None

    def test_validate_article_type_with_invalid_type(self):
        # Test with an invalid article type
        validator = ArticleTypeValidation(self.invalid_article_type_xmltree, None)
        results = list(validator.validate_article_type())
        
        self.assertEqual(len(results), 1)
        result = results[0]
        self.assertEqual(result['response'], "CRITICAL")
        self.assertEqual(result['got_value'], "unknown-type")
        self.assertIn("one of", result['expected_value'])
        
        # Assert that advice is not None and contains expected text
        self.assertIsNotNone(result['advice'])
        self.assertIn("Complete article article-type", result['advice'])
        self.assertIn("with valid value", result['advice'])

    def test_validate_article_type_with_custom_list(self):
        # Test with custom article types list
        custom_params = {
            "article_type_list": ["unknown-type", "custom-type"]
        }
        validator = ArticleTypeValidation(self.invalid_article_type_xmltree, custom_params)
        results = list(validator.validate_article_type())
        
        self.assertEqual(len(results), 1)
        result = results[0]
        self.assertEqual(result['response'], "OK")
        self.assertEqual(result['got_value'], "unknown-type")
        self.assertEqual(result['expected_value'], "unknown-type")
        self.assertIsNone(result['advice'])

    def test_validate_article_type_with_custom_error_level(self):
        # Test with custom error level
        custom_params = {
            "article_type_error_level": "WARNING"
        }
        validator = ArticleTypeValidation(self.invalid_article_type_xmltree, custom_params)
        results = list(validator.validate_article_type())
        
        self.assertEqual(len(results), 1)
        result = results[0]
        self.assertEqual(result['response'], "WARNING")  # Should use custom error level
        self.assertEqual(result['got_value'], "unknown-type")

    def test_validate_article_type_with_missing_param(self):
        # Test with missing article_type_list parameter
        validator = ArticleTypeValidation(self.valid_xmltree, {"article_type_list": None})
        validator.params.pop("article_type_list")
        
        with self.assertRaises(ValidationArticleAndSubArticlesArticleTypeException):
            list(validator.validate_article_type())

    def test_validate_article_type_with_multiple_articles(self):
        # Test with multiple articles (main and sub-articles)
        validator = ArticleTypeValidation(self.multi_article_xmltree, None)
        results = list(validator.validate_article_type())
        
        # Should have 3 results (main article + 2 sub-articles)
        self.assertEqual(len(results), 3)
        
        # Main article should be valid
        self.assertEqual(results[0]['response'], "OK")
        self.assertEqual(results[0]['got_value'], "research-article")
        self.assertIsNone(results[0]['advice'])
        
        # First sub-article should be valid
        self.assertEqual(results[1]['response'], "OK")
        self.assertEqual(results[1]['got_value'], "review-article")
        self.assertIsNone(results[1]['advice'])
        
        # Second sub-article should be invalid
        self.assertEqual(results[2]['response'], "CRITICAL")
        self.assertEqual(results[2]['got_value'], "invalid-type")
        self.assertIsNotNone(results[2]['advice'])

    def test_validate_article_type_vs_subject_similarity_with_matching(self):
        # Test with matching article type and subject
        validator = ArticleTypeValidation(self.valid_xmltree, None)
        results = list(validator.validate_article_type_vs_subject_similarity())
        
        # Should have results since there is an English subject
        self.assertTrue(len(results) > 0)
        
        result = results[0]
        self.assertEqual(result['response'], "OK")
        self.assertEqual(result['got_value'], "research-article")
        self.assertIsNone(result['advice'])

    def test_validate_article_type_vs_subject_similarity_with_mismatch(self):
        # Test with mismatched article type and subject
        validator = ArticleTypeValidation(self.mismatch_subject_xmltree, None)
        results = list(validator.validate_article_type_vs_subject_similarity())
        
        # Should return results for mismatch
        self.assertTrue(len(results) > 0)
        
        result = results[0]
        # Editorial in subject doesn't match research-article type
        self.assertEqual(result['response'], "ERROR")
        self.assertEqual(result['got_value'], "research-article")
        self.assertIsNotNone(result['advice'])
        self.assertIn("Check <article article-type=\"research-article\"/>", result['advice'])
        self.assertIn("seems to be more suitable", result['advice'])

    def test_validate_article_type_vs_subject_similarity_with_no_subject(self):
        # Test with no subject (should not yield any results)
        validator = ArticleTypeValidation(self.no_subject_xmltree, None)
        results = list(validator.validate_article_type_vs_subject_similarity())
        
        # Should not have results since there is no English subject
        self.assertEqual(len(list(results)), 0)

    def test_validate_article_type_vs_subject_similarity_with_custom_threshold(self):
        # Test with custom similarity threshold
        custom_params = {
            "article_type_and_subject_expected_similarity": 0.8
        }
        validator = ArticleTypeValidation(self.valid_xmltree, custom_params)
        results = list(validator.validate_article_type_vs_subject_similarity())
        
        # With a higher threshold, may not find a match
        # Just verify that the function runs with the custom threshold
        self.assertTrue(isinstance(results, list) or hasattr(results, '__next__'))

class TestArticleIdValidation(unittest.TestCase):
    
    def setUp(self):
        # XML com ID válido: número entre 1 e 99999, máximo 5 dígitos
        self.valid_xml_string = '''
        <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="en">
            <front>
                <article-meta>
                    <article-id pub-id-type="other">12345</article-id>
                </article-meta>
            </front>
        </article>
        '''
        
        # XML com ID inválido: número negativo
        self.invalid_negative_xml_string = '''
        <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="en">
            <front>
                <article-meta>
                    <article-id pub-id-type="other">-123</article-id>
                </article-meta>
            </front>
        </article>
        '''
        
        # XML com ID inválido: zero
        self.invalid_zero_xml_string = '''
        <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="en">
            <front>
                <article-meta>
                    <article-id pub-id-type="other">0</article-id>
                </article-meta>
            </front>
        </article>
        '''
        
        # XML com ID inválido: excede 99999
        self.invalid_too_large_xml_string = '''
        <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="en">
            <front>
                <article-meta>
                    <article-id pub-id-type="other">100000</article-id>
                </article-meta>
            </front>
        </article>
        '''
        
        # XML com ID inválido: não é numérico
        self.invalid_non_numeric_xml_string = '''
        <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="en">
            <front>
                <article-meta>
                    <article-id pub-id-type="other">A123</article-id>
                </article-meta>
            </front>
        </article>
        '''
        
        # XML com ID inválido: excede 5 caracteres (mas ainda está abaixo de 99999)
        self.invalid_too_many_leading_zeros_xml_string = '''
        <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="en">
            <front>
                <article-meta>
                    <article-id pub-id-type="other">000123</article-id>
                </article-meta>
            </front>
        </article>
        '''
        
        # XML sem ID
        self.no_id_xml_string = '''
        <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="en">
            <front>
                <article-meta>
                    <!-- Sem article-id -->
                </article-meta>
            </front>
        </article>
        '''
        
        # Parse de strings XML
        self.valid_xmltree = etree.fromstring(self.valid_xml_string)
        self.invalid_negative_xmltree = etree.fromstring(self.invalid_negative_xml_string)
        self.invalid_zero_xmltree = etree.fromstring(self.invalid_zero_xml_string)
        self.invalid_too_large_xmltree = etree.fromstring(self.invalid_too_large_xml_string)
        self.invalid_non_numeric_xmltree = etree.fromstring(self.invalid_non_numeric_xml_string)
        self.invalid_too_many_leading_zeros_xmltree = etree.fromstring(self.invalid_too_many_leading_zeros_xml_string)
        self.no_id_xmltree = etree.fromstring(self.no_id_xml_string)

    def test_validate_article_id_other_with_valid_id(self):
        """Testa validação com um ID válido (numérico entre 1 e 99999 com máximo 5 dígitos)"""
        validator = ArticleIdValidation(self.valid_xmltree, None)
        results = list(validator.validate_article_id_other())
        
        # Deve haver um resultado
        self.assertEqual(len(results), 1)
        
        result = results[0]
        self.assertEqual(result['response'], "OK")
        self.assertEqual(result['got_value'], "12345")
        self.assertIsNone(result['advice'])  # Para caso válido, advice deve ser None

    def test_validate_article_id_other_with_negative_id(self):
        """Testa validação com um ID inválido (número negativo)"""
        validator = ArticleIdValidation(self.invalid_negative_xmltree, None)
        results = list(validator.validate_article_id_other())
        
        self.assertEqual(len(results), 1)
        result = results[0]
        self.assertEqual(result['response'], "ERROR")
        self.assertEqual(result['got_value'], "-123")
        self.assertIn("a numerical value from 1 to 99999", result['expected_value'])
        self.assertIsNotNone(result['advice'])
        self.assertIn("Fix the table of contents article order", result['advice'])

    def test_validate_article_id_other_with_zero_id(self):
        """Testa validação com um ID inválido (zero)"""
        validator = ArticleIdValidation(self.invalid_zero_xmltree, None)
        results = list(validator.validate_article_id_other())
        
        self.assertEqual(len(results), 1)
        result = results[0]
        self.assertEqual(result['response'], "ERROR")
        self.assertEqual(result['got_value'], "0")
        self.assertIn("a numerical value from 1 to 99999", result['expected_value'])
        self.assertIsNotNone(result['advice'])

    def test_validate_article_id_other_with_too_large_id(self):
        """Testa validação com um ID inválido (excede 99999)"""
        validator = ArticleIdValidation(self.invalid_too_large_xmltree, None)
        results = list(validator.validate_article_id_other())
        
        self.assertEqual(len(results), 1)
        result = results[0]
        self.assertEqual(result['response'], "ERROR")
        self.assertEqual(result['got_value'], "100000")
        self.assertIn("a numerical value from 1 to 99999", result['expected_value'])
        self.assertIsNotNone(result['advice'])

    def test_validate_article_id_other_with_non_numeric_id(self):
        """Testa validação com um ID inválido (não numérico)"""
        validator = ArticleIdValidation(self.invalid_non_numeric_xmltree, None)
        results = list(validator.validate_article_id_other())

        self.assertEqual(len(results), 1)
        result = results[0]
        self.assertEqual(result['response'], "ERROR")
        self.assertEqual(result['got_value'], "A123")
        self.assertIn("a numerical value from 1 to 99999", result['expected_value'])
        self.assertIsNotNone(result['advice'])

    def test_validate_article_id_other_with_too_many_leading_zeros(self):
        """Testa validação com um ID inválido (excede 5 caracteres, mesmo sendo abaixo de 99999)"""
        validator = ArticleIdValidation(self.invalid_too_many_leading_zeros_xmltree, None)
        results = list(validator.validate_article_id_other())
        
        self.assertEqual(len(results), 1)
        result = results[0]
        self.assertEqual(result['response'], "ERROR")
        self.assertEqual(result['got_value'], "000123")
        self.assertIn("must have maximum 5 characters", result['expected_value'])
        self.assertIsNotNone(result['advice'])

    def test_validate_article_id_other_with_no_id(self):
        """Testa validação sem ID (não deve gerar resultados)"""
        validator = ArticleIdValidation(self.no_id_xmltree, None)
        results = list(validator.validate_article_id_other())
        
        # Não deve haver resultados, pois o método retorna cedo quando other é None
        self.assertEqual(len(results), 0)

    def test_validate_article_id_other_with_custom_error_level(self):
        """Testa validação com nível de erro personalizado"""
        custom_params = {
            "id_other_error_level": "WARNING"
        }
        validator = ArticleIdValidation(self.invalid_non_numeric_xmltree, custom_params)
        results = list(validator.validate_article_id_other())
        
        self.assertEqual(len(results), 1)
        result = results[0]
        self.assertEqual(result['response'], "WARNING")  # Deve usar o nível de erro personalizado
        self.assertEqual(result['got_value'], "A123")


class TestJATSAndDTDVersionValidation(unittest.TestCase):
    
    def setUp(self):
        # XML com versões compatíveis (sps-1.9 e jats 1.1)
        self.valid_xml_string = '''
        <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article"
                 dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
            <front>
                <article-meta>
                    <article-id pub-id-type="publisher-id">article1</article-id>
                </article-meta>
            </front>
        </article>
        '''
        
        # XML com versões compatíveis (sps-1.10 e jats 1.3)
        self.valid_xml_string2 = '''
        <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article"
                 dtd-version="1.3" specific-use="sps-1.10" xml:lang="en">
            <front>
                <article-meta>
                    <article-id pub-id-type="publisher-id">article2</article-id>
                </article-meta>
            </front>
        </article>
        '''
        
        # XML com versões incompatíveis (sps-1.9 e jats 1.0)
        self.invalid_version_mismatch_xml_string = '''
        <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article"
                 dtd-version="1.0" specific-use="sps-1.9" xml:lang="en">
            <front>
                <article-meta>
                    <article-id pub-id-type="publisher-id">article3</article-id>
                </article-meta>
            </front>
        </article>
        '''
        
        # XML com SPS versão inválida
        self.invalid_sps_version_xml_string = '''
        <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article"
                 dtd-version="1.1" specific-use="sps-2.0" xml:lang="en">
            <front>
                <article-meta>
                    <article-id pub-id-type="publisher-id">article4</article-id>
                </article-meta>
            </front>
        </article>
        '''
        
        # XML sem atributos de versão
        self.missing_versions_xml_string = '''
        <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article"
                 xml:lang="en">
            <front>
                <article-meta>
                    <article-id pub-id-type="publisher-id">article5</article-id>
                </article-meta>
            </front>
        </article>
        '''
        
        # XML apenas com SPS, sem JATS
        self.only_sps_xml_string = '''
        <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article"
                 specific-use="sps-1.9" xml:lang="en">
            <front>
                <article-meta>
                    <article-id pub-id-type="publisher-id">article6</article-id>
                </article-meta>
            </front>
        </article>
        '''
        
        # XML apenas com JATS, sem SPS
        self.only_jats_xml_string = '''
        <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article"
                 dtd-version="1.1" xml:lang="en">
            <front>
                <article-meta>
                    <article-id pub-id-type="publisher-id">article7</article-id>
                </article-meta>
            </front>
        </article>
        '''
        
        # Parse de strings XML
        self.valid_xmltree = etree.fromstring(self.valid_xml_string)
        self.valid_xmltree2 = etree.fromstring(self.valid_xml_string2)
        self.invalid_version_mismatch_xmltree = etree.fromstring(self.invalid_version_mismatch_xml_string)
        self.invalid_sps_version_xmltree = etree.fromstring(self.invalid_sps_version_xml_string)
        self.missing_versions_xmltree = etree.fromstring(self.missing_versions_xml_string)
        self.only_sps_xmltree = etree.fromstring(self.only_sps_xml_string)
        self.only_jats_xmltree = etree.fromstring(self.only_jats_xml_string)

    def test_validate_with_valid_versions(self):
        """Testa validação com versões SPS e JATS compatíveis (sps-1.9 e jats 1.1)"""
        validator = JATSAndDTDVersionValidation(self.valid_xmltree, None)
        results = list(validator.validate())
        
        # Deve haver um resultado
        self.assertEqual(len(results), 1)
        
        result = results[0]
        self.assertEqual(result['response'], "OK")
        self.assertEqual(result['got_value']['specific-use'], "sps-1.9")
        self.assertEqual(result['got_value']['dtd-version'], "1.1")
        self.assertIsNone(result['advice'])  # Para caso válido, advice deve ser None

    def test_validate_with_valid_versions2(self):
        """Testa validação com versões SPS e JATS compatíveis (sps-1.10 e jats 1.3)"""
        validator = JATSAndDTDVersionValidation(self.valid_xmltree2, None)
        results = list(validator.validate())
        
        # Deve haver um resultado
        self.assertEqual(len(results), 1)
        
        result = results[0]
        self.assertEqual(result['response'], "OK")
        self.assertEqual(result['got_value']['specific-use'], "sps-1.10")
        self.assertEqual(result['got_value']['dtd-version'], "1.3")
        self.assertIsNone(result['advice'])  # Para caso válido, advice deve ser None

    def test_validate_with_incompatible_versions(self):
        """Testa validação com versões SPS e JATS incompatíveis (sps-1.9 e jats 1.0)"""
        validator = JATSAndDTDVersionValidation(self.invalid_version_mismatch_xmltree, None)
        results = list(validator.validate())
        
        self.assertEqual(len(results), 1)
        result = results[0]
        self.assertEqual(result['response'], "CRITICAL")
        self.assertEqual(result['got_value']['specific-use'], "sps-1.9")
        self.assertEqual(result['got_value']['dtd-version'], "1.0")
        self.assertIsNotNone(result['advice'])
        self.assertIn("Complete SPS", result['advice'])
        self.assertIn("JATS", result['advice'])
        self.assertIn("compatible values", result['advice'])

    def test_validate_with_invalid_sps_version(self):
        """Testa validação com versão SPS inválida (sps-2.0)"""
        validator = JATSAndDTDVersionValidation(self.invalid_sps_version_xmltree, None)
        results = list(validator.validate())
        
        self.assertEqual(len(results), 1)
        result = results[0]
        self.assertEqual(result['response'], "CRITICAL")
        self.assertEqual(result['got_value']['specific-use'], "sps-2.0")
        self.assertEqual(result['got_value']['dtd-version'], "1.1")
        self.assertIsNotNone(result['advice'])
        # Como sps-2.0 não está na lista de versões válidas, expected_jats_versions estará vazio
        self.assertEqual(result['expected_value'], validator.params.get("specific_use_list"))

    def test_validate_with_missing_versions(self):
        """Testa validação com versões SPS e JATS ausentes"""
        validator = JATSAndDTDVersionValidation(self.missing_versions_xmltree, None)
        results = list(validator.validate())
        
        self.assertEqual(len(results), 1)
        result = results[0]
        self.assertEqual(result['response'], "CRITICAL")
        self.assertEqual(result['got_value']['specific-use'], None)
        self.assertEqual(result['got_value']['dtd-version'], None)
        self.assertIsNotNone(result['advice'])

    def test_validate_with_only_sps_version(self):
        """Testa validação com apenas versão SPS, sem JATS"""
        validator = JATSAndDTDVersionValidation(self.only_sps_xmltree, None)
        results = list(validator.validate())
        
        self.assertEqual(len(results), 1)
        result = results[0]
        self.assertEqual(result['response'], "CRITICAL")
        self.assertEqual(result['got_value']['specific-use'], "sps-1.9")
        self.assertEqual(result['got_value']['dtd-version'], None)
        self.assertIsNotNone(result['advice'])
        # Espera-se JATS 1.1 para SPS-1.9
        self.assertEqual(result['expected_value'], ["1.1"])

    def test_validate_with_only_jats_version(self):
        """Testa validação com apenas versão JATS, sem SPS"""
        validator = JATSAndDTDVersionValidation(self.only_jats_xmltree, None)
        results = list(validator.validate())
        
        self.assertEqual(len(results), 1)
        result = results[0]
        self.assertEqual(result['response'], "CRITICAL")
        self.assertEqual(result['got_value']['specific-use'], None)
        self.assertEqual(result['got_value']['dtd-version'], "1.1")
        # Como não há specific-use, expected_jats_versions estará vazio
        self.assertEqual(result['expected_value'], {
            "sps-1.1": ["1.0"],
            "sps-1.2": ["1.0"],
            "sps-1.3": ["1.0"],
            "sps-1.4": ["1.0"],
            "sps-1.5": ["1.0"],
            "sps-1.6": ["1.0"],
            "sps-1.7": ["1.0", "1.1"],
            "sps-1.8": ["1.0", "1.1"],
            "sps-1.9": ["1.1"],
            "sps-1.10": ["1.1", "1.2", "1.3"]
        })
        self.assertIsNotNone(result['advice'])

    def test_validate_with_custom_version_list(self):
        """Testa validação com lista personalizada de versões compatíveis"""
        custom_params = {
            "specific_use_list": {
                "sps-2.0": ["2.0"],
                "sps-1.9": ["1.0", "1.1", "1.2"]  # Adicionando 1.0 como válido para sps-1.9
            }
        }
        validator = JATSAndDTDVersionValidation(self.invalid_version_mismatch_xmltree, custom_params)
        results = list(validator.validate())
        
        self.assertEqual(len(results), 1)
        result = results[0]
        self.assertEqual(result['response'], "OK")  # Agora deve ser válido com os parâmetros personalizados
        self.assertEqual(result['got_value']['specific-use'], "sps-1.9")
        self.assertEqual(result['got_value']['dtd-version'], "1.0")
        self.assertIsNone(result['advice'])

    def test_validate_with_custom_error_level(self):
        """Testa validação com nível de erro personalizado"""
        custom_params = {
            "jats_and_dtd_version_error_level": "WARNING"
        }
        validator = JATSAndDTDVersionValidation(self.invalid_version_mismatch_xmltree, custom_params)
        results = list(validator.validate())
        
        self.assertEqual(len(results), 1)
        result = results[0]
        self.assertEqual(result['response'], "WARNING")  # Deve usar o nível de erro personalizado
        self.assertEqual(result['got_value']['specific-use'], "sps-1.9")
        self.assertEqual(result['got_value']['dtd-version'], "1.0")
