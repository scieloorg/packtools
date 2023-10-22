from packtools.sps.models.aff import Affiliation
from packtools.translator import _


def _get_affiliation_data(affiliation, element, attrib_label, attrib_source, xpath, default_values=None):
    value = affiliation.get(attrib_source)
    item = {
        'title': _('{} element {} attribute validation').format(element, attrib_label),
        'xpath': xpath,
        'got_value': value
    }
    if default_values:
        item['validation_type'] = _('value in list')
        item['response'] = 'OK' if value in default_values else 'ERROR'
        item['expected_value'] = _('{} affiliation valid').format(attrib_label)
        item['message'] = _('{} affiliation is valid').format(attrib_label) \
            if value in default_values \
            else _('{} affiliation is not valid').format(attrib_label)
        item['advice'] = None if value else _('provide a valid {} affiliation').format(attrib_label)
    else:
        item['validation_type'] = _('exist')
        item['response'] = 'OK' if value else 'ERROR'
        item['expected_value'] = _('{} affiliation').format(attrib_label)
        item['message'] = _('{} affiliation exists').format(attrib_label) \
            if value \
            else _('{} affiliation does not exist').format(attrib_label)
        item['advice'] = None if value else _('provide the {} affiliation').format(attrib_label)

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
                xpath='.//aff/institution[@content-type="original"]'
            ))
            resp['validation'].append(_get_affiliation_data(
                affiliation=affiliation,
                element='aff/institution',
                attrib_label='orgname',
                attrib_source='orgname',
                xpath='.//aff/institution[@content-type="orgname"]'
            ))
            resp['validation'].append(_get_affiliation_data(
                affiliation=affiliation,
                element='aff',
                attrib_label='country',
                attrib_source='country_name',
                xpath='.//aff/country'
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
                xpath='.//aff/addr-line/named-content[@content-type="state"]'
            ))
            resp['validation'].append(_get_affiliation_data(
                affiliation=affiliation,
                element='aff/addr-line',
                attrib_label='city',
                attrib_source='city',
                xpath='.//aff/addr-line/named-content[@content-type="city"]'
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
