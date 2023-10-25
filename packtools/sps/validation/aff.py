from packtools.sps.models.aff import Affiliation
from packtools.translator import _


def _get_affiliation_original(affiliation):
    value = affiliation.get('original')
    item = {
        'title': 'aff/institution element original attribute validation',
        'xpath': './/aff/institution[@content-type="original"]',
        'validation_type': 'exist',
        'response': 'OK' if value else 'ERROR',
        'expected_value': _('original affiliation'),
        'got_value': value,
        'message': _('Got {}, expected original affiliation').format(value),
        'advice': None if value else _('provide the original affiliation')
    }
    return item


def _get_affiliation_orgname(affiliation):
    value = affiliation.get('orgname')
    item = {
        'title': 'aff/institution element orgname attribute validation',
        'xpath': './/aff/institution[@content-type="orgname"]',
        'validation_type': 'exist',
        'response': 'OK' if value else 'ERROR',
        'expected_value': _('orgname affiliation'),
        'got_value': value,
        'message': _('Got {}, expected orgname affiliation').format(value),
        'advice': None if value else _('provide the orgname affiliation')
    }
    return item


def _get_affiliation_country(affiliation):
    value = affiliation.get('country_name')
    item = {
        'title': 'aff element country attribute validation',
        'xpath': './/aff/country',
        'validation_type': 'exist',
        'response': 'OK' if value else 'ERROR',
        'expected_value': _('country affiliation'),
        'got_value': value,
        'message': _('Got {}, expected country affiliation').format(value),
        'advice': None if value else _('provide the country affiliation')
    }
    return item


def _get_affiliation_country_code(affiliation, country_codes):
    if country_codes:
        value = affiliation.get('country_code')
        item = {
            'title': 'aff element @country attribute validation',
            'xpath': './/aff/@country',
            'validation_type': 'value in list',
            'response': 'OK' if value else 'ERROR',
            'expected_value': country_codes,
            'got_value': value,
            'message': _('Got {}, expected {}').format(value, country_codes),
            'advice': None if value else _('provide a valid @country affiliation')
        }
        return item


def _get_affiliation_state(affiliation):
    value = affiliation.get('state')
    item = {
        'title': 'aff/addr-line element state attribute validation',
        'xpath': './/aff/addr-line/named-content[@content-type="state"]',
        'validation_type': 'exist',
        'response': 'OK' if value else 'ERROR',
        'expected_value': _('state affiliation'),
        'got_value': value,
        'message': _('Got {}, expected state affiliation').format(value),
        'advice': None if value else _('provide the state affiliation')
    }
    return item


def _get_affiliation_city(affiliation):
    value = affiliation.get('city')
    item = {
        'title': 'aff/addr-line element city attribute validation',
        'xpath': './/aff/addr-line/named-content[@content-type="city"]',
        'validation_type': 'exist',
        'response': 'OK' if value else 'ERROR',
        'expected_value': _('city affiliation'),
        'got_value': value,
        'message': _('Got {}, expected city affiliation').format(value),
        'advice': None if value else _('provide the city affiliation')
    }
    return item


class AffiliationValidation:
    def __init__(self, xmltree):
        self.xmltree = xmltree
        self.data = Affiliation(self.xmltree).affiliation_list

    def validate_affiliation(self, country_codes):
        resp = []

        for affiliation in self.data:
            resp.append(_get_affiliation_original(affiliation))
            resp.append(_get_affiliation_orgname(affiliation))
            resp.append(_get_affiliation_country(affiliation))
            resp.append(_get_affiliation_country_code(affiliation, country_codes))
            resp.append(_get_affiliation_state(affiliation))
            resp.append(_get_affiliation_city(affiliation))
        return resp

    def validate(self, data):
        """
        Função que executa as validações da classe AffiliationValidation.

        Returns:
            dict: Um dicionário contendo os resultados das validações realizadas.
        
        """
        return {
            'affiliation_validation': self.validate_affiliation,
        }
