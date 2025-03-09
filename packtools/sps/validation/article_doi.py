from packtools.sps.models.article_and_subarticles import ArticleAndSubArticles
from packtools.sps.models.article_doi_with_lang import DoiWithLang
from packtools.sps.validation.utils import (
    format_response,
    check_doi_is_registered,
    build_response,
)


def _callable_extern_validate_default(doi):
    raise NotImplementedError


class ArticleDoiValidation:
    def __init__(self, xmltree, params=None):
        self.params = params or {}
        self.params.setdefault("skip_doi_check", False)
        self.xmltree = xmltree
        self.articles = ArticleAndSubArticles(self.xmltree)
        self.doi = DoiWithLang(self.xmltree)

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
            if text_id := doi.get("parent_id"):
                text = f'<sub-article id="{text_id}">'
            else:
                text = f"<article>"
            advice = (
                f'Mark DOI for {text} with<article-id pub-id-type="doi"></article-id>'
            )
            yield format_response(
                title="DOI",
                parent=doi.get("parent"),
                parent_id=doi.get("parent_id"),
                parent_article_type=doi.get("parent_article_type"),
                parent_lang=doi.get("lang"),
                item="article-id",
                sub_item='@pub-id-type="doi"',
                validation_type="exist",
                is_valid=bool(doi.get("value")),
                expected="valid DOI",
                obtained=doi.get("value"),
                advice=advice,
                data=doi,
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
        dois = {}
        for item in self.doi.data:
            k = item["value"]
            if k:
                dois.setdefault(k, 0)
                dois[k] += 1

        diff = [doi for doi, freq in dois.items() if freq > 1]

        yield format_response(
            title="uniqueness of DOI",
            parent="article",
            parent_id=None,
            parent_article_type=self.articles.main_article_type,
            parent_lang=self.articles.main_lang,
            item="article-id",
            sub_item='@pub-id-type="doi"',
            validation_type="unique",
            is_valid=bool(not diff),
            expected="Unique DOI",
            obtained=str(dois),
            advice=f"Fix doi to be unique. Found repetition: {diff}",
            data=dois,
            error_level=error_level,
        )

    def validate_doi_registered(self, callable_get_data, error_level="CRITICAL"):
        if not self.params.get("skip_doi_check"):
            return

        callable_get_data = callable_get_data or check_doi_is_registered
        if not callable_get_data:
            return

        for doi_data in self.doi.data:
            xml_doi = doi_data.get("value")
            result = check_doi_is_registered(doi_data)
            expected = {
                "article title": doi_data.get("article_title"),
                "authors": doi_data.get("authors"),
            }

            advice = None
            if not result.get("valid"):
                if registered := result.get("registered"):
                    advice = f'Check doi (<article-id pub-id-type="doi">{xml_doi}</article-id>) is not registered for {expected}. It is registered for {registered}'
                else:
                    error_level = "WARNING"
                    advice = (
                        f"Unable to check if {xml_doi} is registered for {expected}"
                    )

            yield format_response(
                title="Registered DOI",
                parent=doi_data.get("parent"),
                parent_id=doi_data.get("parent_id"),
                parent_article_type=doi_data.get("parent_article_type"),
                parent_lang=doi_data.get("lang"),
                item="article-id",
                sub_item='@pub-id-type="doi"',
                validation_type="registered",
                is_valid=result.get("valid"),
                expected=expected,
                obtained=result.get("registered"),
                advice=advice,
                data=doi_data,
                error_level=error_level,
            )

    def validate_different_doi_in_translation(self, error_level="WARNING"):
        doi_list = [self.doi.main_doi]

        for item in self.doi.data:
            doi = item["value"]
            if item["parent_article_type"] == "translation" and doi:
                valid = doi not in doi_list
                if valid:
                    doi_list.append(doi)
                parent_id = item.get("parent_id")
                parent_tag = item.get("parent")
                xml = f'<{parent_tag} id="{parent_id}"><article-id pub-id-type="doi">{doi}</article-id>'
                yield build_response(
                    title="unique DOI",
                    parent=item,
                    item="article-id",
                    sub_item='@pub-id-type="doi"',
                    validation_type="uniqueness",
                    is_valid=valid,
                    expected=f"unique DOI in XML. {doi} not in {doi_list}",
                    obtained=doi,
                    advice=f"Change {doi} in {xml} for a DOI different from {doi_list}",
                    data=self.doi.data,
                    error_level=error_level,
                )
