from packtools.sps.models.article_and_subarticles import ArticleAndSubArticles
from packtools.sps.models.article_doi_with_lang import DoiWithLang
from packtools.sps.validation.utils import (
    check_doi_is_registered,
    build_response,
    validate_doi_format as validate_doi_format_util,
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
        Checks for the existence of DOI in article and translation sub-articles.

        This method validates only article and translation sub-articles.
        For validation of ALL sub-article types, use validate_doi_exists_all_subarticles().

        Params
        ------
        error_level : str, optional
            The severity level of the validation error, by default "CRITICAL".

        Returns
        -------
        generator of dict
            Yields validation results for each article/sub-article.
        """
        for doi in self.doi.data:
            if text_id := doi.get("parent_id"):
                text = f'<sub-article id="{text_id}">'
            else:
                text = f"<article>"

            advice = f'Mark DOI for {text} with <article-id pub-id-type="doi"></article-id>'
            advice_text = 'Mark DOI for {text} with <article-id pub-id-type="doi"></article-id>'
            advice_params = {"text": text}

            # Preparar dicionário parent para build_response
            parent = {
                "parent": doi.get("parent"),
                "parent_id": doi.get("parent_id"),
                "parent_article_type": doi.get("parent_article_type"),
                "parent_lang": doi.get("lang"),
            }

            yield build_response(
                title="DOI",
                parent=parent,
                item="article-id",
                sub_item='@pub-id-type="doi"',
                validation_type="exist",
                is_valid=bool(doi.get("value")),
                expected="valid DOI",
                obtained=doi.get("value"),
                advice=advice,
                data=doi,
                error_level=error_level,
                advice_text=advice_text,
                advice_params=advice_params,
            )

    def validate_doi_exists_all_subarticles(self, error_level="CRITICAL"):
        """
        Checks for the existence of DOI in article and ALL types of sub-articles.

        This method validates article and all sub-article types including:
        - translation
        - reviewer-report
        - correction
        - addendum
        - retraction
        - etc.

        Mandatory rule: DOI is REQUIRED for all documents in SciELO collection.

        Params
        ------
        error_level : str, optional
            The severity level of the validation error, by default "CRITICAL".

        Returns
        -------
        generator of dict
            Yields validation results for each article/sub-article.
        """
        for doi in self.doi.all_data:
            if text_id := doi.get("parent_id"):
                text = f'<sub-article id="{text_id}">'
            else:
                text = f"<article>"

            advice = f'Mark DOI for {text} with <article-id pub-id-type="doi"></article-id>'
            advice_text = 'Mark DOI for {text} with <article-id pub-id-type="doi"></article-id>'
            advice_params = {"text": text}

            parent = {
                "parent": doi.get("parent"),
                "parent_id": doi.get("parent_id"),
                "parent_article_type": doi.get("parent_article_type"),
                "parent_lang": doi.get("lang"),
            }

            yield build_response(
                title="DOI",
                parent=parent,
                item="article-id",
                sub_item='@pub-id-type="doi"',
                validation_type="exist",
                is_valid=bool(doi.get("value")),
                expected="valid DOI",
                obtained=doi.get("value"),
                advice=advice,
                data=doi,
                error_level=error_level,
                advice_text=advice_text,
                advice_params=advice_params,
            )

    def validate_all_dois_are_unique(self, error_level="CRITICAL"):
        """
        Checks if values for DOI are unique.

        Params
        ------
        error_level : str, optional
            The severity level of the validation error, by default "CRITICAL".

        Returns
        -------
        generator of dict
            Yields validation result.
        """
        dois = {}
        for item in self.doi.data:
            k = item["value"]
            if k:
                dois.setdefault(k, 0)
                dois[k] += 1

        diff = [doi for doi, freq in dois.items() if freq > 1]

        advice = f"Fix doi to be unique. Found repetition: {diff}"
        advice_text = "Fix doi to be unique. Found repetition: {diff}"
        advice_params = {"diff": str(diff)}

        parent = {
            "parent": "article",
            "parent_id": None,
            "parent_article_type": self.articles.main_article_type,
            "parent_lang": self.articles.main_lang,
        }

        yield build_response(
            title="uniqueness of DOI",
            parent=parent,
            item="article-id",
            sub_item='@pub-id-type="doi"',
            validation_type="unique",
            is_valid=bool(not diff),
            expected="Unique DOI",
            obtained=str(dois),
            advice=advice,
            data=dois,
            error_level=error_level,
            advice_text=advice_text,
            advice_params=advice_params,
        )

    def validate_doi_registered(self, callable_get_data=None, error_level="CRITICAL"):
        """
        Validates if DOI is registered in CrossRef and matches article metadata.

        FIXED: Corrected inverted logic bug (skip_doi_check now works correctly).
        """
        # FIXED: Removed "not" - logic was inverted
        if self.params.get("skip_doi_check"):
            return

        callable_get_data = callable_get_data or check_doi_is_registered

        for doi_data in self.doi.data:
            # FIXED: Reset error_level for each iteration to prevent mutation bug
            current_error_level = error_level

            xml_doi = doi_data.get("value")
            if not xml_doi:  # Skip empty DOIs
                continue

            result = callable_get_data(doi_data)
            expected = {
                "article title": doi_data.get("article_title"),
                "authors": doi_data.get("authors"),
            }

            advice = None
            advice_text = None
            advice_params = {}

            if not result.get("valid"):
                if registered := result.get("registered"):
                    advice = f'Check doi (<article-id pub-id-type="doi">{xml_doi}</article-id>) is not registered for {expected}. It is registered for {registered}'
                    advice_text = 'Check doi (<article-id pub-id-type="doi">{xml_doi}</article-id>) is not registered for {expected}. It is registered for {registered}'
                    advice_params = {
                        "xml_doi": xml_doi,
                        "expected": str(expected),
                        "registered": str(registered)
                    }
                else:
                    current_error_level = "WARNING"
                    advice = f"Unable to check if {xml_doi} is registered for {expected}"
                    advice_text = "Unable to check if {xml_doi} is registered for {expected}"
                    advice_params = {
                        "xml_doi": xml_doi,
                        "expected": str(expected)
                    }

            parent = {
                "parent": doi_data.get("parent"),
                "parent_id": doi_data.get("parent_id"),
                "parent_article_type": doi_data.get("parent_article_type"),
                "parent_lang": doi_data.get("lang"),
            }

            yield build_response(
                title="registered DOI",
                parent=parent,
                item="article-id",
                sub_item='@pub-id-type="doi"',
                validation_type="registered",
                is_valid=result.get("valid", False),
                expected=f"DOI registered for {expected}",
                obtained=xml_doi,
                advice=advice,
                data=result,
                error_level=current_error_level,
                advice_text=advice_text,
                advice_params=advice_params,
            )

    def validate_different_doi_in_translation(self, error_level="WARNING"):
        """
        Checks if translation has a different DOI from the main article and other translations.

        Params
        ------
        error_level : str, optional
            The severity level of the validation error, by default "WARNING".

        Returns
        -------
        generator of dict
            Yields validation results for each translation.
        """
        doi_list = []

        # First, collect DOIs from main article (non-translation)
        for item in self.doi.data:
            doi = item["value"]
            if doi and item["parent_article_type"] != "translation":
                doi_list.append(doi)

        # Then validate translation DOIs against the list
        for item in self.doi.data:
            doi = item["value"]
            if item["parent_article_type"] == "translation" and doi:
                valid = doi not in doi_list
                if valid:
                    doi_list.append(doi)
                parent_id = item.get("parent_id")
                parent_tag = item.get("parent")
                xml = f'<{parent_tag} id="{parent_id}"><article-id pub-id-type="doi">{doi}</article-id>'

                advice = f"Change {doi} in {xml} for a DOI different from {doi_list}"
                advice_text = "Change {doi} in {xml} for a DOI different from {doi_list}"
                advice_params = {
                    "doi": doi,
                    "xml": xml,
                    "doi_list": str(doi_list)
                }

                yield build_response(
                    title="unique DOI",
                    parent=item,
                    item="article-id",
                    sub_item='@pub-id-type="doi"',
                    validation_type="uniqueness",
                    is_valid=valid,
                    expected=f"unique DOI in XML. {doi} not in {doi_list}",
                    obtained=doi,
                    advice=advice,
                    data=self.doi.data,
                    error_level=error_level,
                    advice_text=advice_text,
                    advice_params=advice_params,
                )

    def validate_doi_format(self, error_level="ERROR"):
        """
        Validates DOI format according to CrossRef rules.

        Mandatory rule: DOI must use only allowed characters: a-zA-Z0-9-._; ()/

        Format:
        - Must start with "10."
        - Must have 4-5 digits after "10."
        - Must have "/" separator
        - Suffix can only contain: a-z, A-Z, 0-9, -, ., _, ;, (, ), /

        Params
        ------
        error_level : str, optional
            The severity level of the validation error, by default "ERROR".

        Returns
        -------
        generator of dict
            Yields validation results for each DOI.
        """
        for doi_data in self.doi.all_data:
            doi_value = doi_data.get("value")
            if not doi_value:
                continue

            # Use validate_doi_format_util from utils
            result = validate_doi_format_util(doi_value)
            is_valid = result["valido"]

            advice = None if is_valid else result["mensagem"]
            advice_text = result["mensagem"]
            advice_params = {"doi": doi_value}

            parent = {
                "parent": doi_data.get("parent"),
                "parent_id": doi_data.get("parent_id"),
                "parent_article_type": doi_data.get("parent_article_type"),
                "parent_lang": doi_data.get("lang"),
            }

            yield build_response(
                title="DOI format",
                parent=parent,
                item="article-id",
                sub_item='@pub-id-type="doi"',
                validation_type="format",
                is_valid=is_valid,
                expected="DOI with format 10.XXXX/[a-zA-Z0-9.-_;()/]+",
                obtained=doi_value,
                advice=advice,
                data=doi_data,
                error_level=error_level,
                advice_text=advice_text,
                advice_params=advice_params,
            )
