from packtools.sps.models.funding_group import FundingGroup




class FundingGroupValidation:
    def __init__(self, xml_tree):
        self.xml_tree = xml_tree
        self.funding_sources = FundingGroup(xml_tree).award_groups
        self.principal_award_recipients = FundingGroup(xml_tree).principal_award_recipients
        self.principal_investigator = FundingGroup(xml_tree).principal_investigators

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
