from packtools.sps.models.aff import Affiliation
from packtools.sps.validation.exceptions import AffiliationValidationValidateCountryCodeException

from packtools.translator import _


class AffiliationsListValidation:
    def __init__(self, xml_tree, country_codes_list=None):
        self.affiliations_list = Affiliation(xml_tree).affiliation_list
        self.country_codes_list = country_codes_list

    def validade_affiliations_list(self, country_codes_list=None):
        country_codes_list = country_codes_list or self.country_codes_list
        if not country_codes_list:
            raise AffiliationValidationValidateCountryCodeException("Function requires list of country codes")
        for affiliation in self.affiliations_list:
            yield from AffiliationValidation(affiliation, country_codes_list).validate_affiliation()

    def validate(self, data):
        country_codes_list = data['country_codes_list'] or self.country_codes_list
        if not country_codes_list:
            raise AffiliationValidationValidateCountryCodeException("Function requires list of country codes")
        yield from self.validade_affiliations_list(country_codes_list)


class AffiliationValidation:
    def __init__(self, affiliation, country_codes_list=None):
        self.affiliation = affiliation
        self.country_codes_list = country_codes_list

    def validate_original(self):
        original = self.affiliation.get('original')
        yield {
            'title': 'aff/institution element original attribute validation',
            'xpath': './/aff/institution[@content-type="original"]',
            'validation_type': 'exist',
            'response': 'OK' if original else 'ERROR',
            'expected_value': _('original affiliation'),
            'got_value': original,
            'message': _('Got {}, expected original affiliation').format(original),
            'advice': None if original else _('provide the original affiliation')
        }

    def validate_orgname(self):
        orgname = self.affiliation.get('orgname')
        yield {
            'title': 'aff/institution element orgname attribute validation',
            'xpath': './/aff/institution[@content-type="orgname"]',
            'validation_type': 'exist',
            'response': 'OK' if orgname else 'ERROR',
            'expected_value': _('orgname affiliation'),
            'got_value': orgname,
            'message': _('Got {}, expected orgname affiliation').format(orgname),
            'advice': None if orgname else _('provide the orgname affiliation')
        }

    def validate_country(self):
        country = self.affiliation.get('country_name')
        yield {
            'title': 'aff element country attribute validation',
            'xpath': './/aff/country',
            'validation_type': 'exist',
            'response': 'OK' if country else 'ERROR',
            'expected_value': _('country affiliation'),
            'got_value': country,
            'message': _('Got {}, expected country affiliation').format(country),
            'advice': None if country else _('provide the country affiliation')
        }

    def validate_country_code(self, country_codes_list=None):
        country_codes_list = country_codes_list or self.country_codes_list
        if not country_codes_list:
            raise AffiliationValidationValidateCountryCodeException(
                "Function requires list of country codes"
            )
        country_code = self.affiliation.get('country_code')
        yield {
            'title': 'aff element @country attribute validation',
            'xpath': './/aff/@country',
            'validation_type': 'value in list',
            'response': 'OK' if country_code in country_codes_list else 'ERROR',
            'expected_value': self.country_codes_list,
            'got_value': country_code,
            'message': _('Got {}, expected one item of this list: {}').format(country_code, country_codes_list),
            'advice': None if country_code in country_codes_list else _('provide a valid @country affiliation')
        }

    def validate_state(self):
        state = self.affiliation.get('state')
        yield {
            'title': 'aff/addr-line element state attribute validation',
            'xpath': './/aff/addr-line/named-content[@content-type="state"] or .//aff/addr-line/state',
            'validation_type': 'exist',
            'response': 'OK' if state else 'ERROR',
            'expected_value': _('state affiliation'),
            'got_value': state,
            'message': _('Got {}, expected state affiliation').format(state),
            'advice': None if state else _('provide the state affiliation')
        }

    def validate_city(self):
        city = self.affiliation.get('city')
        yield {
            'title': 'aff/addr-line element city attribute validation',
            'xpath': './/aff/addr-line/named-content[@content-type="city"] or .//aff/addr-line/city',
            'validation_type': 'exist',
            'response': 'OK' if city else 'ERROR',
            'expected_value': _('city affiliation'),
            'got_value': city,
            'message': _('Got {}, expected city affiliation').format(city),
            'advice': None if city else _('provide the city affiliation')
        }

    def validate_affiliation(self):
        yield from self.validate_original()
        yield from self.validate_orgname()
        yield from self.validate_country()
        yield from self.validate_country_code()
        yield from self.validate_state()
        yield from self.validate_city()
