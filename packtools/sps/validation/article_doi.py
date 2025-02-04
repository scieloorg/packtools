from packtools.sps.models.article_and_subarticles import ArticleAndSubArticles
from packtools.sps.models.article_contribs import ArticleContribs
from packtools.sps.models.article_doi_with_lang import DoiWithLang
from packtools.sps.models.article_titles import ArticleTitles
from packtools.sps.validation.similarity_utils import how_similar
from packtools.sps.validation.utils import format_response, get_doi_information


def _callable_extern_validate_default(doi):
    raise NotImplementedError


class ArticleDoiValidation:
    def __init__(self, xmltree):
        self.xmltree = xmltree
        self.articles = ArticleAndSubArticles(self.xmltree)
        self.doi = DoiWithLang(self.xmltree)
        self.titles = ArticleTitles(self.xmltree).article_title_dict
        self.authors = [
            item
            for item in ArticleContribs(self.xmltree).contribs
            if item.get("parent") == "article"
        ]

    def validate_doi_exists(self, error_level="CRITICAL"):
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
        <sub-article article-type="translation" id="s1" xml:lang="pt">
            <front-stub>
                <article-id pub-id-type="doi">10.1590/2176-4573e59270</article-id>
            </front-stub>
        </sub-article>
        </article>

        Params
        ------
        error_level : str, optional
            The severity level of the validation error, by default "CRITICAL".

        Returns
        -------
        list of dict
            A list of dictionaries, such as:
            [
                {
                    'title': 'article DOI element',
                    'parent': 'article',
                    'parent_article_type': 'research-article',
                    'parent_id': None,
                    'parent_lang': 'en',
                    'item': 'article-id',
                    'sub_item': '@pub-id-type="doi"',
                    'validation_type': 'exist',
                    'response': 'OK',
                    'expected_value': '10.1590/1518-8345.2927.3231',
                    'got_value': '10.1590/1518-8345.2927.3231',
                    'message': 'Got 10.1590/1518-8345.2927.3231, expected 10.1590/1518-8345.2927.3231',
                    'advice': None,
                    'data': [
                        {
                            'lang': 'en',
                            'parent': 'article',
                            'parent_article_type': 'research-article',
                            'value': '10.1590/1518-8345.2927.3231'
                        },
                        {
                            'lang': 'pt',
                            'parent': 'sub-article',
                            'parent_article_type': 'translation',
                            'parent_id': 's1',
                            'value': '10.1590/2176-4573e59270'
                        }
                    ],
                },...
            ]
        """
        for doi in self.doi.data:
            yield format_response(
                title="Article DOI element exists",
                parent=doi.get("parent"),
                parent_id=doi.get("parent_id"),
                parent_article_type=doi.get("parent_article_type"),
                parent_lang=doi.get("lang"),
                item="article-id",
                sub_item='@pub-id-type="doi"',
                validation_type="exist",
                is_valid=bool(doi.get("value")),
                expected=doi.get("value") or "article DOI",
                obtained=doi.get("value"),
                advice=f'Provide a valid DOI for the {doi.get("parent")} represented by the following tag: '
                f'<{doi.get("parent")} article-type="{doi.get("parent_article_type")}" '
                f'id="{doi.get("parent_id")}" xml:lang="{doi.get("lang")}">',
                data=self.doi.data,
                error_level=error_level,
            )

    def validate_all_dois_are_unique(self, error_level="CRITICAL"):
        """
        Checks if values for DOI are unique.

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

        Params
        ------
        error_level : str, optional
            The severity level of the validation error, by default "CRITICAL".

        Returns
        -------
        list of dict
            A list of dictionaries, such as:
            [
                {
                    'title': 'Article DOI element is unique',
                    'parent': 'article',
                    'parent_article_type': 'research-article',
                    'parent_id': None,
                    'parent_lang': 'pt',
                    'item': 'article-id',
                    'sub_item': '@pub-id-type="doi"',
                    'validation_type': 'exist/verification',
                    'response': 'OK',
                    'expected_value': 'Unique DOI values',
                    'got_value': ['10.1590/2176-4573p59270', '10.1590/2176-4573e59270'],
                    'message': "Got ['10.1590/2176-4573p59270', '10.1590/2176-4573e59270'], expected Unique DOI values",
                    'advice': None,
                    'data': [
                        {
                            'lang': 'pt',
                            'parent': 'article',
                            'parent_article_type': 'research-article',
                            'value': '10.1590/2176-4573p59270'
                        },
                        {
                            'lang': 'en',
                            'parent': 'sub-article',
                            'parent_article_type': 'translation',
                            'parent_id': 's1',
                            'value': '10.1590/2176-4573e59270'
                        }
                    ],
                }
            ]
        """
        validated = True
        dois = {}
        for item in self.doi.data:
            if item["value"] in dois:
                validated = False
                dois[item["value"]] += 1
            else:
                dois[item["value"]] = 1

        diff = [doi for doi, freq in dois.items() if freq > 1]

        yield format_response(
            title="Article DOI element is unique",
            parent="article",
            parent_id=None,
            parent_article_type=self.articles.main_article_type,
            parent_lang=self.articles.main_lang,
            item="article-id",
            sub_item='@pub-id-type="doi"',
            validation_type="unique",
            is_valid=validated,
            expected="Unique DOI values",
            obtained=list(dois.keys()),
            advice="Consider replacing the following DOIs that are not unique: {}".format(
                " | ".join(diff)
            ),
            data=self.doi.data,
            error_level=error_level,
        )

    def validate_doi_registered(self, callable_get_data, error_level="CRITICAL"):
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
        error_level : str, optional
            The severity level of the validation error, by default "CRITICAL".

        Returns
        -------
        list of dict
            A list of dictionaries, such as:
            [
                {
                    'title': 'Registered DOI (lang: en, element: doi)',
                    'xpath': './article-id[@pub-id-type="doi"]',
                    'validation_type': 'exist',
                    'response': 'OK',
                    'expected_value': '10.1590/2176-4573p59270',
                    'got_value': '10.1590/2176-4573p59270',
                    'message': 'Got 10.1590/2176-4573p59270 expected 10.1590/2176-4573p59270',
                    'advice': None
                },
                ...
            ]
        """
        callable_get_data = callable_get_data or get_doi_information
        if not callable_get_data:
            return

        for doi_data in self.doi.data:
            xml_doi = doi_data.get("value")
            lang = doi_data.get("lang")
            xml_title = self.titles.get(lang).get("html_text")
            xml_authors = []
            for author in self.authors:
                try:
                    contrib_name = author["contrib_name"]
                    fullname = (
                        f'{contrib_name["surname"]}, {contrib_name["given-names"]}'
                    )
                    xml_authors.append(fullname)
                except KeyError:
                    pass
            got = {
                "title": xml_title,
                "authors": xml_authors,
            }
            registered = callable_get_data(xml_doi)
            if not registered.get("exception_msg"):
                registered_title = registered.get(lang).get("title")
                registered_authors = registered.get("authors") or []
                expected = {
                    "title": registered_title,
                    "authors": registered_authors,
                }
                similarity = how_similar(str(expected), str(got))
                similar = similarity > 0.98
                doi_data["similarity"] = similarity
                yield format_response(
                    title="Registered DOI",
                    parent=doi_data.get("parent"),
                    parent_id=doi_data.get("parent_id"),
                    parent_article_type=doi_data.get("parent_article_type"),
                    parent_lang=doi_data.get("lang"),
                    item="article-id",
                    sub_item='@pub-id-type="doi"',
                    validation_type="registered",
                    is_valid=similar,
                    expected=expected,
                    obtained=got,
                    advice="Check the DOI number",
                    data=doi_data,
                    error_level=error_level,
                )
            else:
                # Resposta para o caso de não haver identificação do DOI
                yield format_response(
                    title="Registered DOI",
                    parent=doi_data.get("parent"),
                    parent_id=doi_data.get("parent_id"),
                    parent_article_type=doi_data.get("parent_article_type"),
                    parent_lang=doi_data.get("lang"),
                    item="article-id",
                    sub_item='@pub-id-type="doi"',
                    validation_type="registered",
                    is_valid=False,
                    expected="Data registered to the DOI {}".format(xml_doi),
                    obtained=got,
                    advice="Consult again after DOI has been registered",
                    data=doi_data,
                    error_level=error_level,
                )

    def validate_different_doi_in_translation(self, error_level="WARNING"):
        article_doi = self.doi.main_doi
        for doi in self.doi.data:
            if (
                doi["parent_article_type"] == "translation"
                and doi["value"] == article_doi
            ):
                yield format_response(
                    title="Different DOIs for translation",
                    parent=doi.get("parent"),
                    parent_id=doi.get("parent_id"),
                    parent_article_type=doi.get("parent_article_type"),
                    parent_lang=doi.get("lang"),
                    item="article-id",
                    sub_item='@pub-id-type="doi"',
                    validation_type="match",
                    is_valid=False,
                    expected="use unique DOIs for articles and sub-articles",
                    obtained=f"article DOI: {article_doi}, sub-article DOI: {doi['value']}",
                    advice="consider using different DOIs for article and sub-article",
                    data=self.doi.data,
                    error_level=error_level,
                )
