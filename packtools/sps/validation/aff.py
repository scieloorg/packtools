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

    return item


class AffiliationValidation:
    def __init__(self, xmltree):
        self.xmltree = xmltree
        self.data = Affiliation(self.xmltree).affiliation_list

    def validate_affiliation(self, default_values=None):
        resp = {'validation': []}

        for affiliation in self.data:
            resp['validation'].append(_get_affiliation_data(
                affiliation=affiliation,
                element='aff/institution',
                attrib_label='original',
                attrib_source='original',
                xpath='.//aff/institution[@content-type="original"]',
                default_values=None
            ))
            resp['validation'].append(_get_affiliation_data(
                affiliation=affiliation,
                element='aff/institution',
                attrib_label='orgname',
                attrib_source='orgname',
                xpath='.//aff/institution[@content-type="orgname"]',
                default_values=None
            ))
            resp['validation'].append(_get_affiliation_data(
                affiliation=affiliation,
                element='aff',
                attrib_label='country',
                attrib_source='country_name',
                xpath='.//aff/country',
                default_values=None
            ))
            resp['validation'].append(_get_affiliation_data(
                affiliation=affiliation,
                element='aff',
                attrib_label='@country',
                attrib_source='country_code',
                xpath='.//aff/@country',
                default_values=default_values
            ))
            resp['validation'].append(_get_affiliation_data(
                affiliation=affiliation,
                element='aff/addr-line',
                attrib_label='state',
                attrib_source='state',
                xpath='.//aff/addr-line/named-content[@content-type="state"]',
                default_values=None
            ))
            resp['validation'].append(_get_affiliation_data(
                affiliation=affiliation,
                element='aff/addr-line',
                attrib_label='city',
                attrib_source='city',
                xpath='.//aff/addr-line/named-content[@content-type="city"]',
                default_values=None
            ))
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
