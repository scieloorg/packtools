from packtools.sps.models.article_and_subarticles import ArticleAndSubArticles
from packtools.sps.models.article_doi_with_lang import DoiWithLang
from packtools.sps.models.article_authors import Authors
from packtools.sps.models.article_titles import ArticleTitles


def _callable_extern_validate_default(doi):
    raise NotImplementedError


class ArticleDoiValidation:
    def __init__(self, xmltree):
        self.xmltree = xmltree
        self.articles = ArticleAndSubArticles(self.xmltree)
        self.doi = DoiWithLang(self.xmltree).main_doi
        self.dois = DoiWithLang(self.xmltree).data
        self.authors = Authors(self.xmltree).contribs
        self.titles = ArticleTitles(self.xmltree).article_title_dict

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
        list of dict
            A list of dictionaries, such as:
            [
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
            ]
        """
        return [
            {
                'title': 'Article DOI element',
                'xpath': './article-id[@pub-id-type="doi"]',
                'validation_type': 'exist',
                'response': 'OK' if self.doi else 'ERROR',
                'expected_value': self.doi or 'article DOI',
                'got_value': self.doi,
                'message': 'Got {} expected {}'.format(self.doi, self.doi if self.doi else 'a DOI'),
                'advice': None if self.doi else 'Provide a valid DOI for the {}'.format(self.articles.main_article_type)
            }
        ]

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
        list of dict
            A list of dictionaries, such as:
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

        doi_map = {d['lang']: d['value'] for d in self.dois}

        for sub_article in self.articles.data:
            if sub_article['article_type'] == 'translation':
                lang = sub_article['lang']
                article_id = sub_article['article_id']
                doi = doi_map.get(lang)
                yield {
                    'title': 'Sub-article translation DOI element',
                    'xpath': './sub-article[@article-type="translation"]',
                    'validation_type': 'exist',
                    'response': 'OK' if doi else 'ERROR',
                    'expected_value': doi if doi else 'sub-article DOI',
                    'got_value': doi,
                    'message': 'Got {} expected {}'.format(doi, doi if doi else 'sub-article DOI'),
                    'advice': None if doi else 'Provide a valid DOI for the sub-article represented by the following'
                                               ' tag: <sub-article article-type="translation" id="{}" xml:lang="{}">'.format(
                        article_id,
                        lang
                    )
                }

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
        list of dict
            A list of dictionaries, such as:
            [
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
            ]
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

        return [
            {
                'title': 'Article DOI element is unique',
                'xpath': './article-id[@pub-id-type="doi"]',
                'validation_type': 'exist/verification',
                'response': 'OK' if validated else 'ERROR',
                'expected_value': 'Unique DOI values',
                'got_value': list(dois.keys()),
                'message': 'Got DOIs and frequencies {}'.format(
                    " | ".join([str((doi, freq)) for doi, freq in dois.items()])),
                'advice': None if validated else 'Consider replacing the following DOIs that are not unique: {}'.format(
                    " | ".join(diff))
            }
        ]

    def validate_doi_registered(self, callable_get_data=None):
        """
        Checks whether a DOI is registered as valid.

        XML input
        ---------
        <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink"
            article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
            <front>
                <article-meta>
                <article-id specific-use="previous-pid" pub-id-type="publisher-id">S2176-45732023005002205</article-id>
                <article-id specific-use="scielo-v3" pub-id-type="publisher-id">PqQCH4JjQTWmwYF97s4YGKv</article-id>
                <article-id specific-use="scielo-v2" pub-id-type="publisher-id">S2176-45732023000200226</article-id>
                <article-id pub-id-type="doi">10.1590/2176-4573p59270</article-id>
                <title-group>
                    <article-title>Analysis of the evolution of competences in the clinical practice of the nursing degree</article-title>
                </title-group>
                <contrib-group>
                    <contrib contrib-type="author">
                      <contrib-id contrib-id-type="orcid">0000-0002-5364-5270</contrib-id>
                      <name>
                        <surname>Martínez-Momblán</surname>
                        <given-names>Maria Antonia</given-names>
                      </name>
                      <xref ref-type="aff" rid="aff1">1</xref>
                    </contrib>
                    <contrib contrib-type="author">
                      <contrib-id contrib-id-type="orcid">0000-0002-6406-0120</contrib-id>
                      <name>
                        <surname>Colina-Torralva</surname>
                        <given-names>Javier</given-names>
                      </name>
                      <xref ref-type="aff" rid="aff1">1</xref>
                    </contrib>
                </contrib-group>
                </article-meta>
            </front>
            <sub-article article-type="reviewer-report" id="s2" xml:lang="pt" />
            <sub-article article-type="reviewer-report" id="s3" xml:lang="pt" />
            <sub-article article-type="translation" id="s1" xml:lang="pt">
                <front-stub>
                    <article-id pub-id-type="doi">10.1590/2176-4573e59270</article-id>
                        <title-group>
                            <article-title>Análise da evolução de competências da prática clínica no curso de enfermagem</article-title>
                        </title-group>
                        <contrib-group>
                            <contrib contrib-type="author">
                            <contrib-id contrib-id-type="orcid">0000-0002-5364-5270</contrib-id>
                                <name>
                                <surname>Martínez-Momblán</surname>
                                <given-names>Maria Antonia</given-names>
                                </name>
                            <xref ref-type="aff" rid="aff2">1</xref>
                            </contrib>
                            <contrib contrib-type="author">
                            <contrib-id contrib-id-type="orcid">0000-0002-6406-0120</contrib-id>
                                <name>
                                <surname>Colina-Torralva</surname>
                                <given-names>Javier</given-names>
                                </name>
                            <xref ref-type="aff" rid="aff2">1</xref>
                            </contrib>
                        </contrib-group>
                </front-stub>
            </sub-article>
            </article>

        Params

        ------
        callable_get_validation : function
            A function that will be passed as an argument.
            This function must have the signature 'def callable_get_validate(doi_name):' and returns a dict, such as:
            {
                'en': {
                        'title': 'Analysis of the evolution of competences in the clinical practice of the nursing degree',
                        'doi': '10.1590/2176-4573p59270'
                    },
                'pt': {
                        'title': 'Análise da evolução de competências da prática clínica no curso de enfermagem',
                        'doi': '10.1590/2176-4573e59270'
                    },
                'authors': ['Martínez-Momblán, Maria Antonia', 'Colina-Torralva, Javier']
            }

        Returns
        -------
        list of dict
            A list of dictionaries, such as:
            [
                {
                    'title': 'Article DOI element is registered',
                    'xpath': './article-id[@pub-id-type="doi"]',
                    'validation_type': 'exist',
                    'response': 'OK',
                    'expected_value': [
                        'en',
                        '10.1590/2176-4573p59270',
                        'Analysis of the evolution of competences in the clinical practice of the nursing degree',
                        ['Martínez-Momblán, Maria Antonia', 'Colina-Torralva, Javier']
                    ],
                    'got_value': [
                        'en',
                        '10.1590/2176-4573p59270',
                        'Analysis of the evolution of competences in the clinical practice of the nursing degree',
                        ['Martínez-Momblán, Maria Antonia', 'Colina-Torralva, Javier']
                    ],
                    'message': "Got "
                               "['en', '10.1590/2176-4573p59270', "
                               "'Analysis of the evolution of competences in the clinical practice of the nursing degree', "
                               "['Martínez-Momblán, Maria Antonia', 'Colina-Torralva, Javier']] expected "
                               "['en', '10.1590/2176-4573p59270', "
                               "'Analysis of the evolution of competences in the clinical practice of the nursing degree', "
                               "['Martínez-Momblán, Maria Antonia', 'Colina-Torralva, Javier']]",
                    'advice': None
                },...
            ]
        """
        callable_get_validate = callable_get_validate or _callable_extern_validate_default

        obtained_authors = list(f"{author.get('surname')}, {author.get('given_names')}" for author in self.authors)

        for doi in self.dois:
            lang = doi.get('lang')

            obtained_doi = doi.get('value')
            obtained_title = self.titles.get(lang)

            expected = callable_get_validate(doi)
            expected_doi = expected.get(lang).get('doi')
            expected_title = expected.get(lang).get('title')
            expected_authors = expected.get('authors')

            is_valid = obtained_doi == expected_doi and obtained_title == expected_title and obtained_authors == expected_authors

            expected_msg = [lang, expected_doi, expected_title, expected_authors]
            obtained_msg = [lang, obtained_doi, obtained_title, obtained_authors]

            yield {
                'title': 'Article DOI element is registered',
                'xpath': './article-id[@pub-id-type="doi"]',
                'validation_type': 'exist',
                'response': 'OK' if is_valid else 'ERROR',
                'expected_value': expected_msg,
                'got_value': obtained_msg,
                'message': 'Got {} expected {}'.format(obtained_msg, expected_msg),
                'advice': None if is_valid else 'DOI not registered or validator not found, provide a registered DOI or '
                                                'check validator'
            }
