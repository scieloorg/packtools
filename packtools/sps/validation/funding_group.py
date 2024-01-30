from packtools.sps.models.funding_group import FundingGroup


def equalize_list_sizes(list1, list2):
    len1, len2 = len(list1), len(list2)
    if len1 < len2:
        list1.extend([None] * (len2 - len1))
    elif len2 < len1:
        list2.extend([None] * (len1 - len2))
    return list1, list2


class FundingGroupValidation:
    def __init__(self, xml_tree):
        self.xml_tree = xml_tree
        self.funding_sources = FundingGroup(xml_tree).award_groups
        self.principal_award_recipients = FundingGroup(xml_tree).principal_award_recipients
        self.principal_investigator = FundingGroup(xml_tree).principal_investigators

    def funding_sources_validation(self):
        for funding in self.funding_sources or [None]:
            if funding:
                is_valid = funding.get("funding-source") != [] and funding.get("award-id") != []
                fundings, awards = equalize_list_sizes(funding.get("funding-source"), funding.get("award-id"))
                obtained = ' | '.join([f'{fund} ({award})' for fund, award in zip(fundings, awards)])
            else:
                is_valid = False
                obtained = None

            yield {
                'title': 'Funding source element validation',
                'xpath': './/funding-group/award-group/funding-source',
                'validation_type': 'exist',
                'response': 'OK' if is_valid else 'ERROR',
                'expected_value': obtained if is_valid else 'values to <funding-source> and <award-id>',
                'got_value': obtained,
                'message': 'Got {} expected {}'.format(
                    obtained, obtained if is_valid else 'values to <funding-source> and <award-id>'),
                'advice': None if is_valid else 'Provide values to <funding-source> and <award-id>'
            }

    def principal_award_recipient_validation(self):
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

