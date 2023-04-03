from packtools.sps.models.aff import AffiliationExtractor


class AffiliationValidation:
    def __init__(self, xmltree):
        self.xmltree = xmltree
        self.data = AffiliationExtractor(self.xmltree).get_affiliation_data_from_multiple_tags(subtag=False)

    @property
    def validate_affiliation(self):
        
        result = []
        for affliation in self.data:
            if not affliation['institution'][0]['original']:
                result.append({
                    'result': 'error',
                    'error_type': f"No original found",
                    'message': f"The affiliation of id: {affliation['id']} does not have an original. Please add one.",
                })
            elif not affliation['country'][0]['name']:
                result.append({
                    'result': 'error',
                    'error_type': f"No country found",
                    'message': f"The affiliation of id: {affliation['id']} does not have a country. Please add one.",
                })
            else:
                result.append({
                    'result': 'success',
                    'message': f"The affiliation of id: {affliation['id']} is ok!"
                })
        return result