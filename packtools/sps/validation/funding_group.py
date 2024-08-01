from packtools.sps.models.funding_group import FundingGroup
from packtools.sps.validation.utils import format_response


def _callable_extern_validate_default(award_id):
    raise NotImplementedError


class FundingGroupValidation:
    def __init__(self, xml_tree, special_chars_funding=None, special_chars_award_id=None):
        self.xml_tree = xml_tree
        self.funding_group_object = FundingGroup(xml_tree)
        self.funding_group = self.funding_group_object.award_groups
        self.funding_fn = self.funding_group_object.fn_financial_information(special_chars_funding, special_chars_award_id)
        self.special_chars_funding = special_chars_funding
        self.special_chars_award_id = special_chars_award_id

    def funding_sources_exist_validation(self, error_level="ERROR"):
        title = 'Funding source element validation'
        validation_type = 'exist'
        for funding in self.funding_group + self.funding_fn:
            fn_type = funding.get('fn-type')
            is_valid = False
            advice = None
            funding_list = funding.get("funding-source") or funding.get("look-like-funding-source") or []
            award_list = funding.get("award-id") or funding.get("look-like-award-id") or []
            has_funding = len(funding_list) > 0
            has_award = len(award_list) > 0
            obtained = '{} values {} and {} values {}'.format(
                len(funding_list),
                'that look like funding source' if fn_type else 'for funding source',
                len(award_list),
                'that look like award id' if fn_type else 'for award id'
            )

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
            data = self.funding_group_object.extract_funding_data(self.special_chars_funding, self.special_chars_award_id)
            yield format_response(
                title=title,
                parent="article",
                parent_id=None,
                parent_article_type=data.get("article_type"),
                parent_lang=data.get("article_lang"),
                item=item,
                sub_item=sub_item,
                validation_type=validation_type,
                is_valid=is_valid,
                expected=expected,
                obtained=obtained,
                advice=advice,
                data=data,
                error_level=error_level,
            )

    def award_id_format_validation(self, callable_validation=None, error_level="ERROR"):
        callable_validation = callable_validation or _callable_extern_validate_default
        data = self.funding_group_object.extract_funding_data(self.special_chars_funding, self.special_chars_award_id)
        for funding in self.funding_group:
            for award_id in funding.get("award-id"):
                is_valid = callable_validation(award_id)
                yield format_response(
                    title="Funding source element validation",
                    parent="article",
                    parent_id=None,
                    parent_article_type=data.get("article_type"),
                    parent_lang=data.get("article_lang"),
                    item="award-group",
                    sub_item="award-id",
                    validation_type="format",
                    is_valid=is_valid,
                    expected=award_id if is_valid else 'a valid value for award id',
                    obtained=award_id,
                    advice='Provide a valid value for award id',
                    data=data,
                    error_level=error_level,
                )
