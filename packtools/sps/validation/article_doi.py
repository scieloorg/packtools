from packtools.sps.models.article_and_subarticles import ArticleAndSubArticles
from packtools.sps.models.article_doi_with_lang import DoiWithLang


class ArticleDoiValidation:
    def __init__(self, xmltree):
        self.xmltree = xmltree
        self.articles = ArticleAndSubArticles(self.xmltree)
        self.doi = DoiWithLang(self.xmltree).main_doi
        self.dois = DoiWithLang(self.xmltree).data

    def validate_main_article_doi_exists(self):
        """
        Checks for the existence of DOI.

        XML input
        ---------
        <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink"
            article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
            <front>
            <article-id pub-id-type="publisher-id" specific-use="scielo-v3">TPg77CCrGj4wcbLCh9vG8bS</article-id>
            <article-id pub-id-type="publisher-id" specific-use="scielo-v2">S0104-11692020000100303</article-id>
            <article-id pub-id-type="doi">10.1590/1518-8345.2927.3231</article-id>
            <article-id pub-id-type="other">00303</article-id>
            </front>
        </article>

        Returns
        -------
        dict
            Such as:
            {
                'title': 'Article DOI element',
                'xpath': './article-id[@pub-id-type="doi"]',
                'validation_type': 'exist',
                'response': 'OK',
                'expected_value': 'article DOI',
                'got_value': '10.1590/1518-8345.2927.3231',
                'message': 'Got 10.1590/1518-8345.2927.3231 expected a DOI',
                'advice': 'XML research-article does not present a DOI'
            }
        """
        validated = self.doi
        return {
            'title': 'Article DOI element',
            'xpath': './article-id[@pub-id-type="doi"]',
            'validation_type': 'exist',
            'response': 'OK' if validated else 'ERROR',
            'expected_value': 'article DOI',
            'got_value': self.doi,
            'message': 'Got {} expected a DOI'.format(self.doi),
            'advice': None if validated else 'XML {} does not present a DOI'.format(
                self.articles.main_article_type)
        }

