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
    def __init__(self, xml_tree):
        self.xml_tree = xml_tree
        self.funding_group_object = FundingGroup(xml_tree)
        self.funding_group = self.funding_group_object.award_groups
        self.funding_fn = self.funding_group_object.fn_financial_information

    def funding_sources_exist_validation(self):
        for funding in self.funding_sources or [None]:
            funding_list = funding.get("funding-source") if funding else []
            award_list = funding.get("award-id") if funding else []
            funding_length = len(funding_list)
            award_length = len(award_list)
            is_valid = funding_length > 0 and award_length > 0
            obtained = '{} values to <funding-source> and {} values to <award-id>'.format(funding_length, award_length)
            advice = []
            if funding_length == 0:
                advice.append('<funding-source>')
            if award_length == 0:
                advice.append('<award-id>')

            yield {
                'title': 'Funding source element validation',
                'xpath': './/funding-group/award-group/funding-source',
                'validation_type': 'exist',
                'response': 'OK' if is_valid else 'ERROR',
                'expected_value': 'at leats 1 value to <funding-source> and at least 1 value to <award-id>',
                'got_value': obtained,
                'message': 'Got {} as <funding-source> {} as <award-id>'.format(
                    funding_list, award_list),
                'advice': None if is_valid else 'Provide values to {}'.format(' and '.join(advice))
            }

    def principal_award_recipient_exist_validation(self):
        for principal in self.principal_award_recipients or [None]:
            is_valid = principal is not None
            expected = principal if is_valid else 'value to <principal-award-recipient>'
            yield {
                'title': 'Principal award recipient element validation',
                'xpath': './/funding-group/award-group/principal-award-recipient',
                'validation_type': 'exist',
                'response': 'OK' if is_valid else 'ERROR',
                'expected_value': expected,
                'got_value': principal,
                'message': 'Got {} expected {}'.format(principal, expected),
                'advice': None if is_valid else 'Provide {}'.format(expected)
            }

    def principal_investigator_exist_validation(self):
        for principal in self.principal_investigator or [None]:
            is_valid = principal is not None
            expected = principal if is_valid else 'value to <principal-investigator>'
            yield {
                'title': 'Principal investigator element validation',
                'xpath': './/funding-group/award-group/principal-investigator/string-name',
                'validation_type': 'exist',
                'response': 'OK' if is_valid else 'ERROR',
                'expected_value': expected,
                'got_value': principal,
                'message': 'Got {} expected {}'.format(principal, expected),
                'advice': None if is_valid else 'Provide {}'.format(expected)
            }

    def award_id_format_validation(self, callable_validation=None):
        callable_validation = callable_validation or _callable_extern_validate_default

        for funding in self.funding_sources or [None]:
            for award_id in funding.get("award-id") if funding else []:
                is_valid = callable_validation(award_id)
                yield {
                    'title': 'Funding source element validation',
                    'xpath': './/funding-group/award-group/award-id',
                    'validation_type': 'format',
                    'response': 'OK' if is_valid else 'ERROR',
                    'expected_value': award_id if is_valid else 'a valid value for <award-id>',
                    'got_value': award_id,
                    'message': 'Got {} expected {}'.format(
                        award_id, award_id if is_valid else 'a valid value for <award-id>'),
                    'advice': None if is_valid else 'Provide a valid value for <award-id>'
                }

    def ack_exist_validation(self):
        for ack in self.ack or [None]:
            is_valid = ack is not None
            expected = ack if is_valid else 'value to <ack>'
            yield {
                'title': 'Acknowledgment element validation',
                'xpath': './/back//ack',
                'validation_type': 'exist',
                'response': 'OK' if is_valid else 'ERROR',
                'expected_value': expected,
                'got_value': ack,
                'message': 'Got {} expected {}'.format(ack, expected),
                'advice': None if is_valid else 'Provide {}'.format(expected)
            }

    def funding_statement_exist_validation(self):
        is_valid = self.funding_statement is not None
        expected = self.funding_statement if is_valid else 'value to <funding-statement>'
        return [
            {
                'title': 'Funding statement element validation',
                'xpath': './/funding-group/funding-statement',
                'validation_type': 'exist',
                'response': 'OK' if is_valid else 'ERROR',
                'expected_value': expected,
                'got_value': self.funding_statement,
                'message': 'Got {} expected {}'.format(self.funding_statement, expected),
                'advice': None if is_valid else 'Provide {}'.format(expected)
            }
        ]
