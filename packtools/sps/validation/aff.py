import logging

from packtools.sps.models.v2.aff import ArticleAffiliations
from packtools.sps.validation.exceptions import (
    AffiliationValidationValidateCountryCodeException,
)
from packtools.sps.validation.utils import format_response, build_response
from packtools.translator import _


class AffiliationsListValidation:
    """
    Class for validating a list of affiliations within an XML document.

    Parameters
    ----------
    xml_tree : lxml.etree._ElementTree
        The parsed XML document representing the article.
    country_codes_list : list, optional
        List of valid country codes for validation.
    """

    def __init__(self, xml_tree, country_codes_list=None):
        """
        Initialize the AffiliationsListValidation object.

        Parameters
        ----------
        xml_tree : lxml.etree._ElementTree
            The parsed XML document representing the article.
        country_codes_list : list, optional
            List of valid country codes for validation.
        """
        self.xml_tree = xml_tree
        self.affiliations = ArticleAffiliations(xml_tree)
        self.affiliations_list = list(self.affiliations.article_affs()) + list(self.affiliations.sub_article_translation_affs())

        self.country_codes_list = country_codes_list

    def validate_affiliations_list(self, country_codes_list=None):
        """
        Validate all the document affiliations

        Parameters
        ----------
        country_codes_list : list, optional
            List of valid country codes for validation. If not provided, uses the instance's country_codes_list.

        Yields
        ------
        dict
            A dictionary containing the validation results for each affiliation.
        """
        country_codes_list = country_codes_list or self.country_codes_list
        yield from self.validate_main_affiliations(country_codes_list)
        yield from self.validate_translated_affiliations(country_codes_list)

    def validate_main_affiliations(self, country_codes_list=None, id_error_level=None, label_error_level=None, original_error_level=None, orgname_error_level=None, country_error_level=None, country_code_error_level=None, state_error_level=None, city_error_level=None):
        items = list(self.affiliations.article_affs())
        total = len(items)
        if total == 1:
            label_error_level = "INFO"
        for affiliation in items:
            yield from AffiliationValidation(
                affiliation, country_codes_list
            ).validate(
                id_error_level, label_error_level, original_error_level, orgname_error_level, country_error_level, country_code_error_level, state_error_level, city_error_level
            )

    def validate_translated_affiliations(self, country_codes_list=None, id_error_level=None, label_error_level=None, original_error_level=None, orgname_error_level=None, country_error_level=None, country_code_error_level=None, state_error_level=None, city_error_level=None):
        orgname_error_level = orgname_error_level or "INFO"
        country_error_level = country_error_level or "INFO"
        country_code_error_level = country_code_error_level or "INFO"
        state_error_level = state_error_level or "INFO"
        city_error_level = city_error_level or "INFO"

        items = list(self.affiliations.sub_article_translation_affs())
        total = len(items)
        if total == 1:
            label_error_level = "INFO"
        for affiliation in items:
            yield from AffiliationValidation(
                affiliation, country_codes_list
            ).validate(
                id_error_level, label_error_level, original_error_level, orgname_error_level, country_error_level, country_code_error_level, state_error_level, city_error_level
            )

    def validate(self, data):
        """
        Validate the affiliations using data provided in the dictionary.

        Parameters
        ----------
        data : dict
            A dictionary containing the data for validation, specifically the country_codes_list.

        Yields
        ------
        dict
            A dictionary containing the validation results for each affiliation.
        """
        country_codes_list = data["country_codes_list"] or self.country_codes_list
        if not country_codes_list:
            raise AffiliationValidationValidateCountryCodeException(
                "Function requires list of country codes"
            )
        yield from self.validate_affiliations_list(country_codes_list)

    def validate_affiliation_count_article_vs_sub_article(self, error_level="CRITICAL"):
        """
        Validate that the number of affiliations in articles matches the number in sub-articles.

        Parameters
        ----------
        error_level : str, optional
            The level of error to be reported in case of mismatch. Default is "CRITICAL".

        Yields
        ------
        dict
            A dictionary containing the validation result comparing the number of affiliations.
        """
        article_list = list(ArticleAffiliations(self.xml_tree).article_affs())
        article_count = len(article_list)
        sub_article_list = list(ArticleAffiliations(self.xml_tree).sub_article_translation_affs())
        sub_article_count = len(sub_article_list)

        yield format_response(
            title="Affiliation count validation",
            parent=None,
            parent_id=None,
            parent_article_type=None,
            parent_lang=None,
            item="aff",
            sub_item=None,
            validation_type="match",
            is_valid=article_count == sub_article_count,
            expected="equal counts in articles and sub-articles",
            obtained=f"articles: {article_count}, sub-articles: {sub_article_count}",
            advice="Ensure the number of affiliations in articles matches the number in sub-articles.",
            data=[
                {
                    "article": f'<aff id=\"{aff1.get("id")}\">',
                    "sub_article": f'<aff id=\"{aff2.get("id")}\">'
                }
                for aff1, aff2 in zip(article_list, sub_article_list)
            ],
            error_level=error_level,
        )


class AffiliationValidation:
    def __init__(self, affiliation, country_codes_list=None):
        """
        Initialize the AffiliationValidation object.

        Parameters
        ----------
        affiliation : dict
            A dictionary containing the affiliation data.
        country_codes_list : list, optional
            List of valid country codes for validation.
        """
        self.affiliation = affiliation
        self.country_codes_list = country_codes_list

    def validate_original(self, error_level=None):
        """
        Validate the presence of the original affiliation content.

        Parameters
        ----------
        error_level : str, optional
            The level of error to be reported. Default is "ERROR".

        Yields
        ------
        dict
            A dictionary containing the validation result for the original affiliation.
        """
        original = self.affiliation.get("original")
        error_level = error_level or "ERROR"
        if not original or error_level == "INFO":
            yield build_response(
                title="original",
                parent=self.affiliation,
                item="institution",
                sub_item='@content-type="original"',
                validation_type="exist",
                is_valid=bool(original),
                expected=_("original affiliation"),
                obtained=original,
                advice=_("provide the original affiliation"),
                data=self.affiliation,
                error_level=error_level,
            )

    def validate_orgname(self, error_level=None):
        """
        Validate the presence of the orgname affiliation content.

        Parameters
        ----------
        error_level : str, optional
            The level of error to be reported. Default is "CRITICAL".

        Yields
        ------
        dict
            A dictionary containing the validation result for the orgname affiliation.
        """
        orgname = self.affiliation.get("orgname")
        error_level = error_level or "CRITICAL"
        if not orgname or error_level == "INFO":
            yield build_response(
                title="orgname",
                parent=self.affiliation,
                item="institution",
                sub_item='@content-type="orgname"',
                validation_type="exist",
                is_valid=bool(orgname),
                expected=_("orgname"),
                obtained=orgname,
                advice=_("provide the orgname"),
                data=self.affiliation,
                error_level=error_level,
            )

    def validate_label(self, error_level=None):
        """
        Validate the presence of the label affiliation content.

        Parameters
        ----------
        error_level : str, optional
            The level of error to be reported. Default is "CRITICAL".

        Yields
        ------
        dict
            A dictionary containing the validation result for the orgname affiliation.
        """
        label = self.affiliation.get("label")
        error_level = error_level or "CRITICAL"
        if not label or error_level == "INFO":
            yield build_response(
                title="label",
                parent=self.affiliation,
                item="aff",
                sub_item="label",
                validation_type="exist",
                is_valid=bool(label),
                expected=_("label"),
                obtained=label,
                advice=_("provide the label"),
                data=self.affiliation,
                error_level=error_level,
            )

    def validate_country(self, error_level=None):
        """
        Validate the presence of the country affiliation content.

        Parameters
        ----------
        error_level : str, optional
            The level of error to be reported. Default is "CRITICAL".

        Yields
        ------
        dict
            A dictionary containing the validation result for the country affiliation.
        """
        country = self.affiliation.get("country_name")
        error_level = error_level or "CRITICAL"
        if not country or error_level == "INFO":
            yield build_response(
                title="country name",
                parent=self.affiliation,
                item="aff",
                sub_item="country",
                validation_type="exist",
                is_valid=bool(country),
                expected=_("country name"),
                obtained=country,
                advice=_("provide the country name"),
                data=self.affiliation,
                error_level=error_level,
            )

    def validate_country_code(self, error_level=None):
        """
        Validate the country code against a list of valid country codes.

        Parameters
        ----------
        country_codes_list : list, optional
            List of valid country codes for validation. If not provided, uses the instance's country_codes_list.
        error_level : str, optional
            The level of error to be reported. Default is "CRITICAL".

        Yields
        ------
        dict
            A dictionary containing the validation result for the country code.
        """
        country_codes_list = self.country_codes_list
        if not country_codes_list:
            raise AffiliationValidationValidateCountryCodeException(
                "Function requires list of country codes"
            )
        country_code = self.affiliation.get("country_code")
        error_level = error_level or "CRITICAL"
        if (not country_code in country_codes_list) or (error_level == "INFO"):
            yield build_response(
                title="country code",
                parent=self.affiliation,
                item="country",
                sub_item="@country",
                validation_type="value in list",
                is_valid=country_code in country_codes_list,
                expected=self.country_codes_list,
                obtained=country_code,
                advice=_("provide a valid @country"),
                data=self.affiliation,
                error_level=error_level,
            )

    def validate_state(self, error_level=None):
        """
        Validate the presence of the state affiliation content.

        Parameters
        ----------
        error_level : str, optional
            The level of error to be reported. Default is "ERROR".

        Yields
        ------
        dict
            A dictionary containing the validation result for the state affiliation.
        """
        state = self.affiliation.get("state")
        error_level = error_level or "ERROR"
        if not state or error_level == "INFO":
            yield build_response(
                title="state",
                parent=self.affiliation,
                item="addr-line",
                sub_item="state",
                validation_type="exist",
                is_valid=bool(state),
                expected=_("state"),
                obtained=state,
                advice=_("provide the state"),
                data=self.affiliation,
                error_level=error_level,
            )

    def validate_city(self, error_level=None):
        """
        Validate the presence of the city affiliation content.

        Parameters
        ----------
        error_level : str, optional
            The level of error to be reported. Default is "ERROR".

        Yields
        ------
        dict
            A dictionary containing the validation result for the city affiliation.
        """
        city = self.affiliation.get("city")
        error_level = error_level or "ERROR"
        if not city or error_level == "INFO":
            yield build_response(
                title="city",
                parent=self.affiliation,
                item="addr-line",
                sub_item="city",
                validation_type="exist",
                is_valid=bool(city),
                expected=_("city"),
                obtained=city,
                advice=_("provide the city"),
                data=self.affiliation,
                error_level=error_level,
            )

    def validate_id(self, error_level=None):
        """
        Validate the presence of the affiliation ID.

        Parameters
        ----------
        error_level : str, optional
            The level of error to be reported. Default is "CRITICAL".

        Yields
        ------
        dict
            A dictionary containing the validation result for the affiliation ID.
        """
        aff_id = self.affiliation.get("id")
        error_level = error_level or "CRITICAL"
        if not aff_id or error_level == "INFO":
            yield build_response(
                title="id",
                parent=self.affiliation,
                item="aff",
                sub_item="@id",
                validation_type="exist",
                is_valid=bool(aff_id),
                expected=_("affiliation ID"),
                obtained=aff_id,
                advice=_("provide the affiliation ID"),
                data=self.affiliation,
                error_level=error_level,
            )

    def validate(self, id_error_level=None, label_error_level=None, original_error_level=None, orgname_error_level=None, country_error_level=None, country_code_error_level=None, state_error_level=None, city_error_level=None):
        """
        Validate the affiliation

        Yields
        ------
        dict
            A dictionary containing the validation results for the affiliation.
        """
        yield from self.validate_id(id_error_level)
        yield from self.validate_label(label_error_level)
        yield from self.validate_original(original_error_level)
        yield from self.validate_orgname(orgname_error_level)
        yield from self.validate_country(country_error_level)
        yield from self.validate_country_code(country_code_error_level)
        yield from self.validate_state(state_error_level)
        yield from self.validate_city(city_error_level)
