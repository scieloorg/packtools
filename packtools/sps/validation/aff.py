from packtools.sps.models.v2.aff import ArticleAffiliations
from packtools.sps.validation.exceptions import (
    AffiliationValidationValidateCountryCodeException,
)
from packtools.sps.validation.utils import format_response
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
        self.affiliations = ArticleAffiliations(xml_tree)
        self.affiliations_list = list(self.affiliations.article_affs()) + list(self.affiliations.sub_article_translation_affs())
        self.country_codes_list = country_codes_list

    def validade_affiliations_list(self, country_codes_list=None):
        """
        Validate the list of affiliations against a list of country codes.

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
        if not country_codes_list:
            raise AffiliationValidationValidateCountryCodeException(
                "Function requires list of country codes"
            )
        for affiliation in self.affiliations_list:
            yield from AffiliationValidation(
                affiliation, country_codes_list
            ).validate_affiliation()

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
        yield from self.validade_affiliations_list(country_codes_list)

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
        article_count = len(list(self.affiliations.article_affs()))
        sub_article_count = len(list(self.affiliations.sub_article_translation_affs()))

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
            data={
                "article_count": article_count,
                "sub_article_count": sub_article_count,
            },
            error_level=error_level,
        )


class AffiliationValidation:
    """
    Class for validating a single affiliation within an XML document.

    Parameters
    ----------
    affiliation : dict
        A dictionary containing the affiliation data.
    country_codes_list : list, optional
        List of valid country codes for validation.
    """

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
        yield format_response(
            title="Affiliation validation",
            parent=self.affiliation.get("parent"),
            parent_id=self.affiliation.get("parent_id"),
            parent_article_type=self.affiliation.get("parent_article_type"),
            parent_lang=self.affiliation.get("parent_lang"),
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
        yield format_response(
            title="Affiliation validation",
            parent=self.affiliation.get("parent"),
            parent_id=self.affiliation.get("parent_id"),
            parent_article_type=self.affiliation.get("parent_article_type"),
            parent_lang=self.affiliation.get("parent_lang"),
            item="institution",
            sub_item='@content-type="orgname"',
            validation_type="exist",
            is_valid=bool(orgname),
            expected=_("orgname affiliation"),
            obtained=orgname,
            advice=_("provide the orgname affiliation"),
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
        yield format_response(
            title="Affiliation validation",
            parent=self.affiliation.get("parent"),
            parent_id=self.affiliation.get("parent_id"),
            parent_article_type=self.affiliation.get("parent_article_type"),
            parent_lang=self.affiliation.get("parent_lang"),
            item="aff",
            sub_item="country",
            validation_type="exist",
            is_valid=bool(country),
            expected=_("country affiliation"),
            obtained=country,
            advice=_("provide the country affiliation"),
            data=self.affiliation,
            error_level=error_level,
        )

    def validate_country_code(self, country_codes_list=None, error_level=None):
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
        country_codes_list = country_codes_list or self.country_codes_list
        if not country_codes_list:
            raise AffiliationValidationValidateCountryCodeException(
                "Function requires list of country codes"
            )
        country_code = self.affiliation.get("country_code")
        error_level = error_level or "CRITICAL"
        yield format_response(
            title="Affiliation validation",
            parent=self.affiliation.get("parent"),
            parent_id=self.affiliation.get("parent_id"),
            parent_article_type=self.affiliation.get("parent_article_type"),
            parent_lang=self.affiliation.get("parent_lang"),
            item="country",
            sub_item="@country",
            validation_type="value in list",
            is_valid=country_code in country_codes_list,
            expected=self.country_codes_list,
            obtained=country_code,
            advice=_("provide a valid @country affiliation"),
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
        yield format_response(
            title="Affiliation validation",
            parent=self.affiliation.get("parent"),
            parent_id=self.affiliation.get("parent_id"),
            parent_article_type=self.affiliation.get("parent_article_type"),
            parent_lang=self.affiliation.get("parent_lang"),
            item="addr-line",
            sub_item="state",
            validation_type="exist",
            is_valid=bool(state),
            expected=_("state affiliation"),
            obtained=state,
            advice=_("provide the state affiliation"),
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
        yield format_response(
            title="Affiliation validation",
            parent=self.affiliation.get("parent"),
            parent_id=self.affiliation.get("parent_id"),
            parent_article_type=self.affiliation.get("parent_article_type"),
            parent_lang=self.affiliation.get("parent_lang"),
            item="addr-line",
            sub_item="city",
            validation_type="exist",
            is_valid=bool(city),
            expected=_("city affiliation"),
            obtained=city,
            advice=_("provide the city affiliation"),
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
        yield format_response(
            title="Affiliation validation",
            parent=self.affiliation.get("parent"),
            parent_id=self.affiliation.get("parent_id"),
            parent_article_type=self.affiliation.get("parent_article_type"),
            parent_lang=self.affiliation.get("parent_lang"),
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

    def validate_affiliation(self):
        """
        Validate the affiliation based on its parent type.

        Yields
        ------
        dict
            A dictionary containing the validation results for the affiliation.
        """
        if self.affiliation.get("parent") == "article":
            yield from self.validate_original()
            yield from self.validate_orgname()
            yield from self.validate_country()
            yield from self.validate_country_code()
            yield from self.validate_state()
            yield from self.validate_city()
        elif self.affiliation.get("parent_article_type") == "translation":
            yield from self.validate_original()
