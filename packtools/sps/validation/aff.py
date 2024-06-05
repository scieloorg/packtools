from packtools.sps.models.aff import Affiliation
from packtools.sps.validation.exceptions import (
    AffiliationValidationValidateCountryCodeException,
)
from packtools.sps.validation.utils import format_response

from packtools.translator import _


class AffiliationsListValidation:
    def __init__(self, xml_tree, country_codes_list=None):
        self.affiliations_list = Affiliation(xml_tree).affiliation_list
        self.country_codes_list = country_codes_list

    def validade_affiliations_list(self, country_codes_list=None):
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
        country_codes_list = data["country_codes_list"] or self.country_codes_list
        if not country_codes_list:
            raise AffiliationValidationValidateCountryCodeException(
                "Function requires list of country codes"
            )
        yield from self.validade_affiliations_list(country_codes_list)


class AffiliationValidation:
    def __init__(self, affiliation, country_codes_list=None):
        self.affiliation = affiliation
        self.country_codes_list = country_codes_list

    def validate_original(self):
        original = self.affiliation.get("original")
        yield format_response(
            title="Affiliation validation",
            parent=self.affiliation.get("parent"),
            parent_id=self.affiliation.get("parent_id"),
            item="institution",
            sub_item='@content-type="original"',
            validation_type="exist",
            is_valid=bool(original),
            expected=_("original affiliation"),
            obtained=original,
            advice=_("provide the original affiliation"),
            data=self.affiliation,
        )

    def validate_orgname(self):
        orgname = self.affiliation.get("orgname")
        resp = format_response(
            title="Affiliation validation",
            parent=self.affiliation.get("parent"),
            parent_id=self.affiliation.get("parent_id"),
            item="institution",
            sub_item='@content-type="orgname"',
            validation_type="exist",
            is_valid=bool(orgname),
            expected=_("orgname affiliation"),
            obtained=orgname,
            advice=_("provide the orgname affiliation"),
            data=self.affiliation,
        )
        if not bool(orgname):
            resp["response"] = "CRITICAL"
        yield resp

    def validate_country(self):
        country = self.affiliation.get("country_name")
        resp = format_response(
            title="Affiliation validation",
            parent=self.affiliation.get("parent"),
            parent_id=self.affiliation.get("parent_id"),
            item="aff",
            sub_item="country",
            validation_type="exist",
            is_valid=bool(country),
            expected=_("country affiliation"),
            obtained=country,
            advice=_("provide the country affiliation"),
            data=self.affiliation,
        )
        if not bool(country):
            resp["response"] = "CRITICAL"
        yield resp

    def validate_country_code(self, country_codes_list=None):
        country_codes_list = country_codes_list or self.country_codes_list
        if not country_codes_list:
            raise AffiliationValidationValidateCountryCodeException(
                "Function requires list of country codes"
            )
        country_code = self.affiliation.get("country_code")
        resp = format_response(
            title="Affiliation validation",
            parent=self.affiliation.get("parent"),
            parent_id=self.affiliation.get("parent_id"),
            item="country",
            sub_item="@country",
            validation_type="value in list",
            is_valid=country_code in country_codes_list,
            expected=self.country_codes_list,
            obtained=country_code,
            advice=_("provide a valid @country affiliation"),
            data=self.affiliation,
        )
        if not bool(country_code):
            resp["response"] = "CRITICAL"
        yield resp

    def validate_state(self):
        state = self.affiliation.get("state")
        yield format_response(
            title="Affiliation validation",
            parent=self.affiliation.get("parent"),
            parent_id=self.affiliation.get("parent_id"),
            item="addr-line",
            sub_item="state",
            validation_type="exist",
            is_valid=bool(state),
            expected=_("state affiliation"),
            obtained=state,
            advice=_("provide the state affiliation"),
            data=self.affiliation,
        )

    def validate_city(self):
        city = self.affiliation.get("city")
        yield format_response(
            title="Affiliation validation",
            parent=self.affiliation.get("parent"),
            parent_id=self.affiliation.get("parent_id"),
            item="addr-line",
            sub_item="city",
            validation_type="exist",
            is_valid=bool(city),
            expected=_("city affiliation"),
            obtained=city,
            advice=_("provide the city affiliation"),
            data=self.affiliation,
        )

    def validate_id(self):
        aff_id = self.affiliation.get("id")
        resp = format_response(
            title="Affiliation validation",
            parent=self.affiliation.get("parent"),
            parent_id=self.affiliation.get("parent_id"),
            item="aff",
            sub_item="@id",
            validation_type="exist",
            is_valid=bool(aff_id),
            expected=_("city affiliation"),
            obtained=aff_id,
            advice=_("provide the city affiliation"),
            data=self.affiliation,
        )
        if not bool(aff_id):
            resp["response"] = "CRITICAL"
        yield resp

    def validate_affiliation(self):
        yield from self.validate_original()
        yield from self.validate_orgname()
        yield from self.validate_country()
        yield from self.validate_country_code()
        yield from self.validate_state()
        yield from self.validate_city()
