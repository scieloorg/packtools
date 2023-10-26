from packtools.sps.models.aff import Affiliation

from packtools.translator import _




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
