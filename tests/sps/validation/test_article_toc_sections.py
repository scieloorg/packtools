import unittest
from unittest import TestCase
from lxml import etree
from packtools.sps.validation.article_toc_sections import XMLTocSectionsValidation, SubjectValidation
from packtools.sps.validation.exceptions import ValidationExpectedTocSectionsException


class ArticleTocSectionsTest(TestCase):
    def test_validate_success(self):
        self.maxDiff = None
        self.xmltree = etree.fromstring(
            """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML"
            dtd-version="1.0" article-type="research-article" xml:lang="en">
            <front>
                <article-meta>
                    <title-group>
                        <article-title>Título del artículo</article-title>
                    </title-group>
                    <article-categories>
                        <subj-group subj-group-type="heading">
                            <subject>Health Sciences</subject>
                        </subj-group>
                    </article-categories>
                </article-meta>
            </front>
            <sub-article article-type="translation" id="01" xml:lang="pt">
                <front-stub>
                    <article-categories>
                        <subj-group subj-group-type="heading">
                            <subject>Ciências da Saúde</subject>
                        </subj-group>
                    </article-categories>
                    <title-group>
                        <article-title>Article title</article-title>
                    </title-group>
                </front-stub>
            </sub-article>
            </article>
            """
        )
        params = {
            "toc_sections": {
                "en": ["Health Sciences"],
                "pt": ["Ciências da Saúde"]
            },
            "subj_group_type_error_level": "CRITICAL",
            "value_error_level": "CRITICAL"
        }
        validator = XMLTocSectionsValidation(self.xmltree, params)
        results = list(validator.validate())

        self.assertEqual(len(results), 8)
        
        # Verificando o resultado para seção em inglês
        result = results[2]
        self.assertEqual(result['response'], 'OK')
        self.assertEqual(result['got_value'], 'Health Sciences')
        self.assertIsNone(result['advice'])

        # Verificando o resultado para seção em português
        result = results[6]
        self.assertEqual(result['response'], 'OK')
        self.assertEqual(result['got_value'], 'Ciências da Saúde')
        self.assertIsNone(result['advice'])

    def test_validate_article_sections_with_invalid_subj_group_type(self):
        self.maxDiff = None
        self.xmltree = etree.fromstring(
            """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML"
            dtd-version="1.0" article-type="research-article" xml:lang="en">
            <front>
                <article-meta>
                    <title-group>
                        <article-title>Título del artículo</article-title>
                    </title-group>
                    <article-categories>
                        <subj-group subj-group-type="wrong-type">
                            <subject>Health Sciences</subject>
                        </subj-group>
                    </article-categories>
                </article-meta>
            </front>
            </article>
            """
        )
        params = {
            "toc_sections": {
                "en": ["Health Sciences"]
            },
            "subj_group_type_error_level": "CRITICAL"
        }
        validator = XMLTocSectionsValidation(self.xmltree, params)
        results = list(validator.validate())
        
        self.assertTrue(len(results) > 0)
        result = next(r for r in results if r['sub_item'] == '@subj-group-type')
        
        self.assertEqual(result['response'], 'CRITICAL')
        self.assertEqual(result['got_value'], 'wrong-type')
        self.assertEqual(
            result['advice'],
            'Replace <subject-group subj-group-type="wrong-type"><subject>Health Sciences</subject></subject-group> by <subject-group subj-group-type="heading"><subject>Health Sciences</subject></subject-group>'
        )

    def test_validate_article_title_similarity(self):
        self.maxDiff = None
        self.xmltree = etree.fromstring(
            """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML"
            dtd-version="1.0" article-type="research-article" xml:lang="en">
            <front>
                <article-meta>
                    <title-group>
                        <article-title>Health Sciences</article-title>
                    </title-group>
                    <article-categories>
                        <subj-group subj-group-type="heading">
                            <subject>Health Sciences</subject>
                        </subj-group>
                    </article-categories>
                </article-meta>
            </front>
            </article>
            """
        )
        params = {
            "article_title_and_toc_section_max_similarity": 0.7,
            "article_title_and_toc_section_are_similar_error_level": "ERROR"
        }
        validator = XMLTocSectionsValidation(self.xmltree, params)
        results = [item for item in list(validator.validate()) if item["title"] == "document title must be meaningful"]
        
        result = results[0]
        
        self.assertEqual(result['response'], 'ERROR')
        self.assertEqual(result['got_value'], 'Health Sciences')
        self.assertEqual(
            result['advice'],
            'The article title (Health Sciences) must represent its contents and must be different from the section title (Health Sciences) to get a better ranking in search results'
        )

    def test_validate_full_process(self):
        self.maxDiff = None
        self.xmltree = etree.fromstring(
            """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML"
            dtd-version="1.0" article-type="research-article" xml:lang="en">
            <front>
                <article-meta>
                    <title-group>
                        <article-title>Advanced Health Sciences Research</article-title>
                    </title-group>
                    <article-categories>
                        <subj-group subj-group-type="heading">
                            <subject>Health Sciences</subject>
                        </subj-group>
                    </article-categories>
                </article-meta>
            </front>
            </article>
            """
        )
        params = {
            "toc_sections": {
                "en": ["Health Sciences"]
            },
            "subj_group_type_error_level": "CRITICAL",
            "value_error_level": "CRITICAL",
            "article_title_and_toc_section_max_similarity": 0.7,
            "article_title_and_toc_section_are_similar_error_level": "ERROR"
        }
        validator = XMLTocSectionsValidation(self.xmltree, params)
        results = list(validator.validate())
        
        self.assertEqual(4, len(results))
        # Verificando resultados da validação de seção
        result = results[0]
        self.assertEqual(result['response'], 'OK')
        self.assertEqual(result['got_value'], 'heading')
        self.assertIsNone(result['advice'])
        
        # Verificando resultados da validação de seção / subseção
        result = results[1]
        self.assertEqual(result['response'], 'OK')
        self.assertEqual(result['got_value'], [])
        self.assertIsNone(result['advice'])

        # Verificando resultados da validação de título da seção
        result = results[2]
        self.assertEqual(result['response'], 'OK')
        self.assertEqual(result['got_value'], 'Health Sciences')
        self.assertIsNone(result['advice'])

        # Verificando resultados da validação de título do artigo
        result = results[3]
        self.assertEqual(result['response'], 'OK')
        self.assertEqual(result['got_value'], 'Advanced Health Sciences Research')
        self.assertIsNone(result['advice'])


class ArticleTocSectionsErrorTest(TestCase):
    def test_validate_invalid_section_value(self):
        """Testa quando a seção não está na lista de seções esperadas"""
        self.xmltree = etree.fromstring(
            """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML"
            dtd-version="1.0" article-type="research-article" xml:lang="en">
            <front>
                <article-meta>
                    <title-group>
                        <article-title>Research Article</article-title>
                    </title-group>
                    <article-categories>
                        <subj-group subj-group-type="heading">
                            <subject>Incorrect Section</subject>
                        </subj-group>
                    </article-categories>
                </article-meta>
            </front>
            </article>
            """
        )
        params = {
            "toc_sections": {
                "en": ["Health Sciences", "Biology"]
            },
            "value_error_level": "CRITICAL"
        }
        validator = XMLTocSectionsValidation(self.xmltree, params)
        results = list(validator.validate())
        
        result = next(r for r in results if r['sub_item'] == 'subject')
        self.assertEqual(result['response'], 'CRITICAL')
        self.assertEqual(result['got_value'], 'Incorrect Section')
        self.assertEqual(
            result['advice'], 
            'Incorrect Section is not registered as a table of contents section. Valid values: {\'en\': [\'Health Sciences\', \'Biology\']}'
        )

    def test_validate_missing_subj_group_type(self):
        """Testa quando o atributo subj-group-type está ausente"""
        self.xmltree = etree.fromstring(
            """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML"
            dtd-version="1.0" article-type="research-article" xml:lang="en">
            <front>
                <article-meta>
                    <title-group>
                        <article-title>Research Article</article-title>
                    </title-group>
                    <article-categories>
                        <subj-group>
                            <subject>Health Sciences</subject>
                        </subj-group>
                    </article-categories>
                </article-meta>
            </front>
            </article>
            """
        )
        params = {
            "toc_sections": {"en": ["Health Sciences"]},
            "subj_group_type_error_level": "CRITICAL"
        }
        validator = XMLTocSectionsValidation(self.xmltree, params)
        results = list(validator.validate())
        
        result = results[0]
        self.assertEqual(result['response'], 'CRITICAL')
        self.assertEqual(result['got_value'], None)
        self.assertEqual(
            result['advice'], 'Replace <subject-group><subject>Health Sciences</subject></subject-group> by <subject-group subj-group-type="heading"><subject>Health Sciences</subject></subject-group>'
        )

    def test_validate_very_similar_title_and_section(self):
        """Testa quando o título do artigo é muito similar à seção"""
        self.xmltree = etree.fromstring(
            """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML"
            dtd-version="1.0" article-type="research-article" xml:lang="en">
            <front>
                <article-meta>
                    <title-group>
                        <article-title>Health Sciences Study</article-title>
                    </title-group>
                    <article-categories>
                        <subj-group subj-group-type="heading">
                            <subject>Health Sciences</subject>
                        </subj-group>
                    </article-categories>
                </article-meta>
            </front>
            </article>
            """
        )
        params = {
            "article_title_and_toc_section_max_similarity": 0.5,
            "article_title_and_toc_section_are_similar_error_level": "ERROR"
        }
        validator = XMLTocSectionsValidation(self.xmltree, params)
        results = [item for item in list(validator.validate()) if item["title"] == "document title must be meaningful"]
        
        result = results[0]
        self.assertEqual(result['response'], 'ERROR')
        self.assertEqual(result['got_value'], 'Health Sciences Study')
        self.assertTrue(
            'must represent its contents and must be different from the section title' in result['advice']
        )

    def test_validate_multiple_sections_same_language(self):
        """Testa quando existem múltiplas seções para a mesma língua"""
        self.xmltree = etree.fromstring(
            """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML"
            dtd-version="1.0" article-type="research-article" xml:lang="en">
            <front>
                <journal-meta>
                    <journal-title-group>
                        <journal-title>Braz Journal ...</journal-title>
                    </journal-title-group>
                </journal-meta>
                <article-meta>
                    <title-group>
                        <article-title>Research Article</article-title>
                    </title-group>
                    <article-categories>
                        <subj-group subj-group-type="heading">
                            <subject>Health Sciences</subject>
                        </subj-group>
                        <subj-group subj-group-type="heading">
                            <subject>Biology</subject>
                        </subj-group>
                    </article-categories>
                </article-meta>
            </front>
            <sub-article article-type="translation"></sub-article>
            </article>
            """
        )
        params = {
            "error_level_section": "CRITICAL"
        }
        validator = XMLTocSectionsValidation(self.xmltree, params)
        results = list(validator.validate())
        
        responses = [item["response"] for item in results]
        advices = [item["advice"] for item in results]

        self.assertEqual(9, len(results))
        
        # validate_subj_group_type
        result = results[0]
        self.assertEqual(result['response'], 'OK')

        # validate_subsection
        result = results[1]
        self.assertEqual(result['response'], 'OK')

        # validate_section
        result = results[2]
        self.assertEqual(result['response'], 'CRITICAL')
        self.assertEqual(result['advice'], 'Unable to check if Health Sciences (<subject-group subj-group-type="heading"><subject>Health Sciences</subject></subject-group>) is a valid table of contents section because the journal (Braz Journal ...) sections were not informed'
        )

        # validade_article_title_is_different_from_section_title
        result = results[3]
        self.assertEqual(result['response'], 'OK')

        # validate_unexpected_item
        result = results[4]
        self.assertEqual(result['response'], 'CRITICAL')
        self.assertIn('unexpected', result['advice'])

        # validate_subj_group_type, validate_subsection, validate_section, validade_article_title_is_different_from_section_title
        self.assertEqual(responses[-4:], ["CRITICAL", "OK", "CRITICAL", "ERROR", ])


    def test_validate_section_with_subsections(self):
        """Testa quando uma seção tem subseções (estrutura não permitida)"""
        self.xmltree = etree.fromstring(
            """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML"
            dtd-version="1.0" article-type="research-article" xml:lang="en">
            <front>
                <article-meta>
                    <title-group>
                        <article-title>Research Article</article-title>
                    </title-group>
                    <article-categories>
                        <subj-group subj-group-type="heading">
                            <subject>Health Sciences</subject>
                            <subj-group>
                                <subject>Public Health</subject>
                            </subj-group>
                        </subj-group>
                    </article-categories>
                </article-meta>
            </front>
            </article>
            """
        )
        params = {
            "subsection_error_level": "CRITICAL"
        }
        validator = XMLTocSectionsValidation(self.xmltree, params)
        results = list(validator.validate())

        responses = [item["response"] for item in results]

        self.assertEqual(5, len(results))   
        self.assertEqual(2, responses.count("OK"))     

        result = results[1]
        self.assertEqual(result['response'], 'CRITICAL')
        self.assertEqual(result['got_value'], ['Public Health'])
        self.assertEqual(result['advice'], 'Write section and subsection in one subject: <subject-group subj-group-type="heading"><subject>Health Sciences: Public Health</subject></subject-group>. Remove <subject-group><subject>Public Health</subject></subject-group>')

    def test_validate_all_validation_types_with_errors(self):
        """Testa múltiplos tipos de erro em uma única validação"""
        self.xmltree = etree.fromstring(
            """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML"
            dtd-version="1.0" article-type="research-article" xml:lang="en">
            <front>
                <article-meta>
                    <title-group>
                        <article-title>Biology Research</article-title>
                    </title-group>
                    <article-categories>
                        <subj-group subj-group-type="invalid">
                            <subject>Biology</subject>
                            <subj-group>
                                <subject>Molecular Biology</subject>
                            </subj-group>
                        </subj-group>
                    </article-categories>
                </article-meta>
            </front>
            </article>
            """
        )
        params = {
            "toc_sections": {"en": ["Health Sciences"]},
            "subj_group_type_error_level": "CRITICAL",
            "value_error_level": "CRITICAL",
            "subsection_error_level": "CRITICAL"
        }
        validator = XMLTocSectionsValidation(self.xmltree, params)
        results = list(validator.validate())

        self.assertEqual(5, len(results))
        # Verifica erro de tipo de subj-group
        result = results[0]
        self.assertEqual(result['response'], 'CRITICAL')
        self.assertEqual(result['got_value'], 'invalid')
        self.assertEqual(result['advice'], 'Replace <subject-group subj-group-type="invalid"><subject>Biology</subject></subject-group> by <subject-group subj-group-type="heading"><subject>Biology</subject></subject-group>')
                
        # Verifica erro de valor da seção / subseção
        result = results[1]
        self.assertEqual(result['response'], 'CRITICAL')
        self.assertEqual(result['got_value'], ['Molecular Biology'])
        self.assertEqual(result['advice'], 'Write section and subsection in one subject: <subject-group subj-group-type="heading"><subject>Biology: Molecular Biology</subject></subject-group>. Remove <subject-group><subject>Molecular Biology</subject></subject-group>')


class TestUnexpectedItemValidation(unittest.TestCase):
    def setUp(self):
        self.data = {
            "parent_lang": "en",
            "subject": "Health Sciences",
            "subj_group_type": "heading",
            "parent": "article",
            "parent_id": None,
            "parent_article_type": "research-article",
        }
        self.params = {
            "unexpected_subj_group_error_level": "CRITICAL"
        }
        self.validator = SubjectValidation(self.data, self.params)

    def test_unexpected_item_with_heading(self):
        result = self.validator.validate_unexpected_item()
        
        self.assertEqual(
            result['got_value'], 
            self.data
        )
        self.assertEqual(
            result['advice'],
            'Remove <subject-group subj-group-type="heading"><subject>Health Sciences</subject></subject-group> because it is unexpected, only one subject-group is acceptable'
        )
        self.assertEqual(
            result['title'],
            'unexpected subject-group'
        )
        self.assertEqual(
            result['response'],
            'CRITICAL'
        )


class TestSubjGroupTypeValidation(unittest.TestCase):
    def setUp(self):
        self.data = {
            "parent_lang": "en",
            "subject": "Health Sciences",
            "subj_group_type": "invalid-type",
            "parent": "article",
            "parent_id": None,
            "parent_article_type": "research-article",
        }
        self.params = {
            "subj_group_type_error_level": "CRITICAL"
        }
        self.validator = SubjectValidation(self.data, self.params)

    def test_invalid_subj_group_type(self):
        result = self.validator.validate_subj_group_type()
        
        self.assertEqual(
            result['got_value'], 
            'invalid-type'
        )
        self.assertEqual(
            result['advice'],
            'Replace <subject-group subj-group-type="invalid-type"><subject>Health Sciences</subject></subject-group> by <subject-group subj-group-type="heading"><subject>Health Sciences</subject></subject-group>'
        )
        self.assertEqual(
            result['title'],
            'table of contents section'
        )
        self.assertEqual(
            result['response'],
            'CRITICAL'
        )


class TestSubsectionValidation(unittest.TestCase):
    def setUp(self):
        self.data = {
            "parent_lang": "en",
            "subject": "Biology",
            "section": "Biology",
            "subsections": ["Molecular Biology"],
            "subj_group_type": "heading",
            "parent": "article",
            "parent_id": None,
            "parent_article_type": "research-article",
        }
        self.params = {
            "subsection_error_level": "CRITICAL"
        }
        self.validator = SubjectValidation(self.data, self.params)

    def test_subsection_validation(self):
        result = self.validator.validate_subsection()
        
        self.assertEqual(
            result['got_value'], 
            ["Molecular Biology"]
        )
        self.assertEqual(
            result['advice'],
            'Write section and subsection in one subject: <subject-group subj-group-type="heading"><subject>Biology: Molecular Biology</subject></subject-group>. Remove <subject-group><subject>Molecular Biology</subject></subject-group>'
        )
        self.assertEqual(
            result['title'],
            'table of contents section with subsection'
        )
        self.assertEqual(
            result['response'],
            'CRITICAL'
        )


class TestSectionValidation(unittest.TestCase):
    def setUp(self):
        self.data = {
            "parent_lang": "en",
            "subject": "Invalid Science",
            "section": "Invalid Science",
            "subsections": [],
            "subj_group_type": "heading",
            "parent": "article",
            "parent_id": None,
            "parent_article_type": "research-article",
        }
        self.params = {
            "toc_sections": {
                "en": ["Health Sciences", "Biology"]
            },
            "value_error_level": "CRITICAL"
        }
        self.validator = SubjectValidation(self.data, self.params)

    def test_invalid_section(self):
        result = self.validator.validate_section()
        
        self.assertEqual(
            result['got_value'], 
            'Invalid Science'
        )
        self.assertEqual(
            result['advice'],
            'Invalid Science is not registered as a table of contents section. Valid values: {\'en\': [\'Health Sciences\', \'Biology\']}'
        )
        self.assertEqual(
            result['title'],
            'table of contents section'
        )
        self.assertEqual(
            result['response'],
            'CRITICAL'
        )

    def test_valid_section(self):
        self.data["subject"] = "Health Sciences"
        self.data["section"] = "Health Sciences"
        result = self.validator.validate_section()
        
        self.assertEqual(
            result['got_value'], 
            'Health Sciences'
        )
        self.assertIsNone(result['advice'])
        self.assertEqual(
            result['title'],
            'table of contents section'
        )
        self.assertEqual(
            result['response'],
            'OK'
        )


class TestTitleSimilarityValidation(unittest.TestCase):
    def setUp(self):
        self.data = {
            "parent_lang": "en",
            "subject": "Health Sciences",
            "section": "Health Sciences",
            "article_title": "Health Sciences Study",
            "subsections": [],
            "subj_group_type": "heading",
            "parent": "article",
            "parent_id": None,
            "parent_article_type": "research-article",
        }
        self.params = {
            "article_title_and_toc_section_max_similarity": 0.5,
            "article_title_and_toc_section_are_similar_error_level": "ERROR"
        }
        self.validator = SubjectValidation(self.data, self.params)

    def test_similar_title_and_section(self):
        result = self.validator.validade_article_title_is_different_from_section_title()
        
        self.assertEqual(
            result['got_value'], 
            'Health Sciences Study'
        )
        self.assertEqual(
            result['advice'],
            'The article title (Health Sciences Study) must represent its contents and must be different from the section title (Health Sciences) to get a better ranking in search results'
        )
        self.assertEqual(
            result['title'],
            'document title must be meaningful'
        )
        self.assertEqual(
            result['response'],
            'ERROR'
        )

    def test_different_title_and_section(self):
        self.data["article_title"] = "Effects of Exercise on Health"
        result = self.validator.validade_article_title_is_different_from_section_title()
        
        self.assertEqual(
            result['got_value'], 
            'Effects of Exercise on Health'
        )
        self.assertIsNone(result['advice'])
        self.assertEqual(
            result['title'],
            'document title must be meaningful'
        )
        self.assertEqual(
            result['response'],
            'OK'
        )


if __name__ == '__main__':
    unittest.main()