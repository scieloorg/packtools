from packtools.sps.models.funding_group import FundingGroup
from packtools.sps.validation.utils import build_response


def _callable_extern_validate_default(award_id):
    raise NotImplementedError


class FundingGroupValidation:
    """
    Validation class for funding information in XML documents.
    
    Parameters
    ----------
    xml_tree : lxml.etree.Element
        XML tree to validate
    params : dict
        Dictionary containing parameters for validation:
        - special_chars_award_id: List of special characters allowed in award IDs
        - callable_validation: Function to validate award IDs format
        - error_level: Error level for validation messages ("ERROR" or "WARNING")
    """
    def __init__(self, xml_tree, params=None):
        self.xml_tree = xml_tree
        self.params = {
            'special_chars_award_id': ['/', '.', '-'],
            'callable_validation': _callable_extern_validate_default,
            'error_level': "ERROR"
        }
        self.params.update(params or {})
        self.funding = FundingGroup(xml_tree, self.params)

    def funding_sources_exist_validation(self):
        """
        Validates the existence of funding sources and award IDs.
        
        Yields
        ------
        dict
            Validation results for each funding source and award ID.
        """
        title = 'Funding source element validation'
        validation_type = 'exist'
        funding_data = self.funding.data
        
        parent = {
            "parent": "article",
            "parent_id": None,
            "parent_article_type": funding_data.get("article_type"),
            "parent_lang": funding_data.get("article_lang"),
        }

        # Combina os resultados de award_groups e notas financeiras
        financial_items = self.funding.financial_disclosure + self.funding.supported_by
        for funding in self.funding.award_groups + financial_items:
            fn_type = funding.get('fn-type')
            is_valid = False
            advice = None
            
            # Lista de fontes de financiamento
            funding_list = funding.get("funding-source") or []
            # Lista de IDs de financiamento
            award_list = funding.get("award-id") or funding.get("look-like-award-id") or []
            
            has_funding = len(funding_list) > 0
            has_award = len(award_list) > 0
            
            obtained = f"{len(funding_list)} values for funding source and {len(award_list)} values for award id"

            if fn_type:
                item = "fn"
                sub_item = f"@fn-type='{fn_type}'"
            else:
                item = "award-group"
                sub_item = "funding-source"

            if fn_type == 'supported-by':
                expected = 'at least 1 value for funding source'
                if not has_funding:
                    advice = 'Provide value for funding source'
                else:
                    is_valid = True
            else:
                expected = 'at least 1 value for funding source and at least 1 value for award id'
                if not has_award and not has_funding:
                    advice = 'Provide values for award id and funding source'
                elif not has_award and has_funding:
                    advice = 'Provide value for award id or move funding source to <fn fn-type="supported-by">'
                elif has_award and not has_funding:
                    advice = 'Provide value for funding source'
                else:
                    is_valid = True

            yield build_response(
                title=title,
                parent=parent,
                item=item,
                sub_item=sub_item,
                validation_type=validation_type,
                is_valid=is_valid,
                expected=expected,
                obtained=obtained,
                advice=advice,
                data=funding_data,
                error_level=self.params.get('error_level', "ERROR")
            )

    def award_id_format_validation(self):
        """
        Validates the format of award IDs using the provided validation function.
        
        Yields
        ------
        dict
            Validation results for each award ID.
        """
        callable_validation = self.params.get('callable_validation', _callable_extern_validate_default)
        data = self.funding.data
        
        parent = {
            "parent": "article",
            "parent_id": None,
            "parent_article_type": data.get("article_type"),
            "parent_lang": data.get("article_lang"),
        }

        # Valida IDs em award_groups
        for funding in self.funding.award_groups:
            for award_id in funding.get("award-id", []):
                is_valid = callable_validation(award_id)
                yield build_response(
                    title="Funding source element validation",
                    parent=parent,
                    item="award-group",
                    sub_item="award-id",
                    validation_type="format",
                    is_valid=is_valid,
                    expected=award_id if is_valid else 'a valid value for award id',
                    obtained=award_id,
                    advice='Provide a valid value for award id',
                    data=data,
                    error_level=self.params.get('error_level', "ERROR")
                )