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
        return {
            'title': 'Article DOI element',
            'xpath': './article-id[@pub-id-type="doi"]',
            'validation_type': 'exist',
            'response': 'OK' if self.doi else 'ERROR',
            'expected_value': self.doi if self.doi else 'article DOI',
            'got_value': self.doi,
            'message': 'Got {} expected {}'.format(self.doi, self.doi if self.doi else 'a DOI'),
            'advice': None if self.doi else 'Provide a valid DOI for the {}'.format(self.articles.main_article_type)
        }

    def validate_translations_doi_exists(self):
        """
        Checks for the existence of DOI.

        XML input
        ---------
        <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink"
        article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="pt">
        <front>
            <article-id specific-use="previous-pid" pub-id-type="publisher-id">S2176-45732023005002205</article-id>
            <article-id specific-use="scielo-v3" pub-id-type="publisher-id">PqQCH4JjQTWmwYF97s4YGKv</article-id>
            <article-id specific-use="scielo-v2" pub-id-type="publisher-id">S2176-45732023000200226</article-id>
            <article-id pub-id-type="doi">10.1590/2176-4573p59270</article-id>
        </front>
        <sub-article article-type="reviewer-report" id="s2" xml:lang="pt" />
        <sub-article article-type="reviewer-report" id="s3" xml:lang="pt" />
        <sub-article article-type="translation" id="s1" xml:lang="en">
            <front-stub>
                <article-id pub-id-type="doi">10.1590/2176-4573e59270</article-id>
            </front-stub>
        </sub-article>
        </article>

        Returns
        -------
        dict
            Such as:
            [
                {
                    'title': 'Sub-article translation DOI element',
                    'xpath': './sub-article[@article-type="translation"]',
                    'validation_type': 'exist',
                    'response': 'OK',
                    'expected_value': '10.1590/2176-4573e59270',
                    'got_value': '10.1590/2176-4573e59270',
                    'message': 'Got 10.1590/2176-4573e59270 expected 10.1590/2176-4573e59270',
                    'advice': None
                }, ...
            ]
        """

        result = []

        doi_map = {d['lang']: d['value'] for d in self.dois}

        for sub_article in self.articles.data:
            if sub_article['article_type'] == 'translation':
                lang = sub_article['lang']
                article_id = sub_article['article_id']
                doi = doi_map.get(lang)
                result.append(
                    {
                        'title': 'Sub-article translation DOI element',
                        'xpath': './sub-article[@article-type="translation"]',
                        'validation_type': 'exist',
                        'response': 'OK' if doi else 'ERROR',
                        'expected_value': doi if doi else 'sub-article DOI',
                        'got_value': doi,
                        'message': 'Got {} expected {}'.format(doi, doi if doi else 'sub-article DOI'),
                        'advice': None if doi else 'Provide a valid DOI for the sub-article translation ({}) which '
                                                   'language is {}'.format(article_id, lang)
                    }
                )
        return result

    def validate_all_dois_are_unique(self):
        """
        Checks for the existence of DOI.

        XML input
        ---------
        <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink"
        article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="pt">
        <front>
            <article-id specific-use="previous-pid" pub-id-type="publisher-id">S2176-45732023005002205</article-id>
            <article-id specific-use="scielo-v3" pub-id-type="publisher-id">PqQCH4JjQTWmwYF97s4YGKv</article-id>
            <article-id specific-use="scielo-v2" pub-id-type="publisher-id">S2176-45732023000200226</article-id>
            <article-id pub-id-type="doi">10.1590/2176-4573p59270</article-id>
        </front>
        <sub-article article-type="reviewer-report" id="s2" xml:lang="pt" />
        <sub-article article-type="reviewer-report" id="s3" xml:lang="pt" />
        <sub-article article-type="translation" id="s1" xml:lang="en">
            <front-stub>
                <article-id pub-id-type="doi">10.1590/2176-4573e59270</article-id>
            </front-stub>
        </sub-article>
        </article>

        Returns
        -------
        dict
            Such as:
            {
                'title': 'Article DOI element is unique',
                'xpath': './article-id[@pub-id-type="doi"]',
                'validation_type': 'exist/verification',
                'response': 'OK',
                'expected_value': 'Unique DOI values',
                'got_value': 'DOIs identified: 10.1590/2176-4573p59270 | 10.1590/2176-4573e59270',
                'message': "Got DOIs and frequencies ('10.1590/2176-4573p59270', 1) | ('10.1590/2176-4573e59270', 1)",
                'advice': None
            }
        """
        validated = True
        dois = {}
        for item in self.dois:
            if item['value'] in dois:
                validated = False
                dois[item['value']] += 1
            else:
                dois[item['value']] = 1

        if not validated:
            diff = [doi for doi, freq in dois.items() if freq > 1]

        return {
            'title': 'Article DOI element is unique',
            'xpath': './article-id[@pub-id-type="doi"]',
            'validation_type': 'exist/verification',
            'response': 'OK' if validated else 'ERROR',
            'expected_value': 'Unique DOI values',
            'got_value': 'DOIs identified: {}'.format(" | ".join(list(dois.keys()))),
            'message': 'Got DOIs and frequencies {}'.format(" | ".join([str((doi, freq)) for doi, freq in dois.items()])),
            'advice': None if validated else 'Consider replacing the following DOIs that are not unique: {}'.format(" | ".join(diff))
        }
