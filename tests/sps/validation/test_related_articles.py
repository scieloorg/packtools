from unittest import TestCase
from lxml import etree

from packtools.sps.validation.related_articles import RelatedArticlesValidation


class RelatedArticlesValidationTest(TestCase):
    def test_validate_related_article_types_match(self):
        xmltree = etree.fromstring(
            '''<article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink" 
            article-type="correction" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
            <front>
            <related-article ext-link-type="doi" id="ra1" related-article-type="corrected-article" xlink:href="10.1590/1808-057x202090350"/>
            </front>
            </article>'''
        )
        params = {
            'correspondence_list': [
                {
                    'article-type': 'correction',
                    'related-article-types': ['corrected-article']
                },
                {
                    'article-type': 'retraction',
                    'related-article-types': ['retracted-article']
                }
            ],
            'error_level': 'ERROR'
        }
        validator = RelatedArticlesValidation(xmltree, params)
        result = list(validator.validate_related_article_types())[0]

        self.assertEqual(result['response'], 'OK')
        self.assertEqual(result['got_value'], 'corrected-article')
        self.assertEqual(result['expected_value'], ['corrected-article'])
        self.assertIsNone(result['advice'])
        self.assertEqual(result['parent_article_type'], 'correction')

    def test_validate_related_article_types_not_match(self):
        xmltree = etree.fromstring(
            '''<article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink" 
            article-type="retraction" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
            <front>
            <related-article ext-link-type="doi" id="ra1" related-article-type="retraction-forward" xlink:href="10.1590/1808-057x202090350"/>
            </front>
            </article>'''
        )
        params = {
            'correspondence_list': [
                {
                    'article-type': 'correction',
                    'related-article-types': ['corrected-article']
                },
                {
                    'article-type': 'retraction',
                    'related-article-types': ['retracted-article', 'article-retracted']
                }
            ],
            'error_level': 'ERROR'
        }
        validator = RelatedArticlesValidation(xmltree, params)
        result = list(validator.validate_related_article_types())[0]

        self.assertEqual(result['response'], 'ERROR')
        self.assertEqual(result['got_value'], 'retraction-forward')
        self.assertEqual(result['expected_value'], ['retracted-article', 'article-retracted'])
        self.assertTrue(result['advice'].startswith('The article-type: retraction'))
        self.assertEqual(result['parent_article_type'], 'retraction')

    def test_validate_related_article_doi_exists(self):
        xmltree = etree.fromstring(
            '''<article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink" 
            article-type="correction-forward" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
            <front>
            <related-article ext-link-type="doi" id="ra1" related-article-type="corrected-article" xlink:href="10.1590/1808-057x202090350"/>
            </front>
            </article>'''
        )
        validator = RelatedArticlesValidation(xmltree, {'error_level': 'ERROR'})
        result = list(validator.validate_related_article_doi())[0]

        self.assertEqual(result['response'], 'OK')
        self.assertEqual(result['got_value'], '10.1590/1808-057x202090350')
        self.assertEqual(result['expected_value'], '10.1590/1808-057x202090350')
        self.assertIsNone(result['advice'])
        self.assertEqual(result['parent_article_type'], 'correction-forward')
        self.assertEqual(result['validation_type'], 'exist')

    def test_validate_related_article_doi_not_exists(self):
        xmltree = etree.fromstring(
            '''<article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink" 
            article-type="correction-forward" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
            <front>
            <related-article ext-link-type="doi" id="ra1" related-article-type="corrected-article" />
            </front>
            </article>'''
        )
        validator = RelatedArticlesValidation(xmltree, {'error_level': 'ERROR'})
        result = list(validator.validate_related_article_doi())[0]

        self.assertEqual(result['response'], 'ERROR')
        self.assertIsNone(result['got_value'])
        self.assertEqual(result['expected_value'], 'A valid DOI or URI for related-article/@xlink:href')
        self.assertTrue(result['advice'].startswith('Provide a valid DOI'))
        self.assertEqual(result['parent_article_type'], 'correction-forward')
        self.assertEqual(result['validation_type'], 'exist')


if __name__ == '__main__':
    unittest.main()