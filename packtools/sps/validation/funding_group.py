from packtools.sps.models.funding_group import FundingGroup


def _callable_extern_validate_default(award_id):
    raise NotImplementedError


def _create_response(title, xpath, validation_type, is_valid, expected, obtained, message, advice):
    return {
                'title': title,
                'xpath': xpath,
                'validation_type': validation_type,
                'response': 'OK' if is_valid else 'ERROR',
                'expected_value': expected,
                'got_value': obtained,
                'message': message,
                'advice': advice
            }


class FundingGroupValidation:
    def __init__(self, xml_tree, special_chars_funding=[], special_chars_award_id=[]):
        self.xml_tree = xml_tree
        self.funding_group_object = FundingGroup(xml_tree)
        self.funding_group = self.funding_group_object.award_groups
        self.funding_fn = self.funding_group_object.fn_financial_information(special_chars_funding, special_chars_award_id)

    def funding_sources_exist_validation(self):
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
            message = 'Got {} {} and {} {}'.format(
                funding_list,
                'that look like funding source' if fn_type else 'as funding source',
                award_list,
                'that look like award id' if fn_type else 'as award id'
            )

            xpath = f".//fn-group/fn[@fn-type='{fn_type}']//p" if fn_type else './/funding-group/award-group/funding-source'
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

            yield _create_response(title, xpath, validation_type, is_valid, expected, obtained, message, advice)

    def award_id_format_validation(self, callable_validation=None):
        callable_validation = callable_validation or _callable_extern_validate_default
        for funding in self.funding_group:
            for award_id in funding.get("award-id"):
                is_valid = callable_validation(award_id)
                yield {
                    'title': 'Funding source element validation',
                    'xpath': './/funding-group/award-group/award-id',
                    'validation_type': 'format',
                    'response': 'OK' if is_valid else 'ERROR',
                    'expected_value': award_id if is_valid else 'a valid value for award id',
                    'got_value': award_id,
                    'message': 'Got {} expected {}'.format(
                        award_id, award_id if is_valid else 'a valid value for award id'),
                    'advice': None if is_valid else 'Provide a valid value for award id'
                }
