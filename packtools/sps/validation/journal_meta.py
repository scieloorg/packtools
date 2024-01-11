from ..models.journal_meta import ISSN, Acronym, Title, Publisher
from packtools.sps.validation.exceptions import ValidationPublisherException
from packtools.sps.validation.exceptions import ValidationIssnsException


class ISSNValidation:
    def __init__(self, xmltree, issns_dict=None):
        self.xmltree = xmltree
        self.journal_issns = ISSN(xmltree)
        self.issns_dict = issns_dict

    def validate_issn(self, issns_dict):
        """
        Checks whether the ISSN value is as expected.

        XML input
        ---------
        <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" dtd-version="1.0" article-type="research-article" xml:lang="pt">
            <front>
                <journal-meta>
                    <issn pub-type="ppub">0034-8910</issn>
			        <issn pub-type="epub">1518-8787</issn>
                </journal-meta>
            </front>
        </article>

        Params
        ------
        issns_dict : dict, such as:
            {
            'ppub': '0034-8910',
            'epub': '1518-8787'
            }

        Returns
        -------
        list of dictionaries, such as:
            [
                {
                    'title': 'Journal ISSN element validation',
                    'xpath': './/journal-meta//issn[@pub-type="ppub"]',
                    'validation_type': 'value',
                    'response': 'OK',
                    'expected_value': '<issn pub-type="ppub">0034-8910</issn>',
                    'got_value': '<issn pub-type="ppub">0034-8910</issn>',
                    'message': 'Got <issn pub-type="ppub">0034-8910</issn> expected <issn pub-type="ppub">0034-8910</issn>',
                    'advice': None
                },
                {
                    'title': 'Journal ISSN element validation',
                    'xpath': './/journal-meta//issn[@pub-type="epub"]',
                    'validation_type': 'value',
                    'response': 'OK',
                    'expected_value': '<issn pub-type="epub">1518-8787</issn>',
                    'got_value': '<issn pub-type="epub">1518-8787</issn>',
                    'message': 'Got <issn pub-type="epub">1518-8787</issn> expected <issn pub-type="epub">1518-8787</issn>',
                    'advice': None
                }
            ]
        """
        issns_dict = issns_dict or self.issns_dict
        if not issns_dict or type(issns_dict) is not dict:
            raise ValidationIssnsException("The function requires a list of ISSNs in dictionary format")

        for tp, issn_expected in issns_dict.items():
            issn_obtained = self.journal_issns.epub if tp == "epub" else self.journal_issns.ppub
            is_valid = issn_expected == issn_obtained
            yield {
                'title': 'Journal ISSN element validation',
                'xpath': './/journal-meta//issn[@pub-type="{}"]'.format(tp),
                'validation_type': 'value',
                'response': 'OK' if is_valid else 'ERROR',
                'expected_value': '<issn pub-type="{}">{}</issn>'.format(tp, issn_expected),
                'got_value': '<issn pub-type="{}">{}</issn>'.format(tp, issn_obtained),
                'message': 'Got <issn pub-type="{}">{}</issn> expected <issn pub-type="{}">{}</issn>'.format(
                    tp, issn_obtained, tp, issn_expected
                ),
                'advice': None if is_valid else 'Provide an ISSN value as expected: <issn pub-type="{}">{}</issn>'.format(tp, issn_expected),
            }


class AcronymValidation:
    def __init__(self, xmltree):
        self.xmltree = xmltree
        self.journal_acronym = Acronym(xmltree)

    def validate_text(self, expected_value):
        resp_text = dict(
            object='journal acronym',
            output_expected=expected_value,
            output_obteined=self.journal_acronym.text,
            match=(expected_value == self.journal_acronym.text)
        )
        return resp_text


class TitleValidation:
    def __init__(self, xmltree):
        self.xmltree = xmltree
        self.journal_titles = Title(xmltree)

    def validate_journal_title(self, expected_value):
        resp_journal_title = dict(
            object='journal title',
            output_expected=expected_value,
            output_obteined=self.journal_titles.journal_title,
            match=(expected_value == self.journal_titles.journal_title)
        )
        return resp_journal_title

    def validate_abbreviated_journal_title(self, expected_value):
        resp_abbreviated_journal_title = dict(
            object='abbreviated journal title',
            output_expected=expected_value,
            output_obteined=self.journal_titles.abbreviated_journal_title,
            match=(expected_value == self.journal_titles.abbreviated_journal_title)
        )
        return resp_abbreviated_journal_title


class PublisherNameValidation:
    def __init__(self, xmltree, publisher_name_list=None):
        self.xmltree = xmltree
        self.publisher = Publisher(self.xmltree)
        self.publisher_name_list = publisher_name_list

    def validate_publisher_names(self, publisher_name_list):
        """
        Checks whether the publisher name is as expected.

        XML input
        ---------
        <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" dtd-version="1.0" article-type="research-article" xml:lang="pt">
            <front>
                <journal-meta>
                    <publisher>
                        <publisher-name>Faculdade de Saúde Pública da Universidade de São Paulo</publisher-name>
                    </publisher>
                </journal-meta>
            </front>
        </article>

        Params
        ------
        publisher_name_list : list

        Returns
        -------
        list of dict
            A list of dictionaries, such as:
            [
                {
                    'title': 'Publisher name element validation',
                    'xpath': './/publisher//publisher-name',
                    'validation_type': 'value',
                    'response': 'OK',
                    'expected_value': 'Faculdade de Saúde Pública da Universidade de São Paulo',
                    'got_value': 'Faculdade de Saúde Pública da Universidade de São Paulo',
                    'message': 'Got Faculdade de Saúde Pública da Universidade de São Paulo, expected
                     Faculdade de Saúde Pública da Universidade de São Paulo',
                    'advice': None
                },...
            ]
        """
        publisher_name_list = publisher_name_list or self.publisher_name_list
        if not publisher_name_list:
            raise ValidationPublisherException("Function requires a list of publisher names")
        validations = []
        expected = set(publisher_name_list)
        obtained = set(self.publisher.publishers_names)

        for value in sorted(list(expected.intersection(obtained))):
            validations.append((True, value, value, None))
        for value in sorted(list(expected.difference(obtained))):
            validations.append((False, value, None, f'Add {value} as publisher name in XML'))
        for value in sorted(list(obtained.difference(expected))):
            validations.append((False, None, value, f'Remove {value} as publisher name in XML'))

        for validation in validations:
            yield {
                    'title': 'Publisher name element validation',
                    'xpath': './/publisher//publisher-name',
                    'validation_type': 'value',
                    'response': 'OK' if validation[0] else 'ERROR',
                    'expected_value': validation[1],
                    'got_value': validation[2],
                    'message': 'Got {} expected {}'.format(validation[2], validation[1]),
                    'advice': validation[3]
                }


class JournalMetaValidation:
    def __init__(self, xmltree):
        self.xmltree = xmltree

    def validate(self, expected_values):
        '''
        expected_values is a dict like:
        {
        'issns': {
                    'ppub': '0103-5053',
                    'epub': '1678-4790'
                },
        'acronym': 'hcsm',
        'journal-title': 'História, Ciências, Saúde-Manguinhos',
        'abbrev-journal-title': 'Hist. cienc. saude-Manguinhos',
        'publisher-name': ['Casa de Oswaldo Cruz, Fundação Oswaldo Cruz']
        }
        '''

        issn = ISSNValidation(self.xmltree)
        acronym = AcronymValidation(self.xmltree)
        title = TitleValidation(self.xmltree)
        publisher = PublisherNameValidation(self.xmltree)

        resp_journal_meta = list(issn.validate_issn(expected_values['issns']))

        resp_journal_meta.extend(
            [
                acronym.validate_text(expected_values['acronym']),
                title.validate_journal_title(expected_values['journal-title']),
                title.validate_abbreviated_journal_title(expected_values['abbrev-journal-title']),
                publisher.validate_publishers_names(expected_values['publisher-name'])
            ]
        )
        return resp_journal_meta
