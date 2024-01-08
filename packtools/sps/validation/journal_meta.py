from ..models.journal_meta import ISSN, Acronym, Title, Publisher
from packtools.sps.validation.exceptions import ValidationIssnsException


class ISSNValidation:
    def __init__(self, xmltree, issns_dict=None):
        self.xmltree = xmltree
        self.journal_issns = ISSN(xmltree)
        self.issns_dict = issns_dict

    def validate_issn(self, issns_dict=None):
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
                    'xpath': './/journal-meta//issn[@pub-type=*]',
                    'validation_type': 'value in list',
                    'response': 'OK',
                    'expected_value': {'epub': '1518-8787', 'ppub': '0034-8910'},
                    'got_value': '0034-8910',
                    'message': 'Got <issn pub-type="ppub">0034-8910</issn> expected one item of this list: ppub: 0034-8910 | epub: 1518-8787',
                    'advice': None
                },...
            ]
        """
        issns_dict = issns_dict or self.issns_dict
        if not issns_dict or type(issns_dict) is not dict:
            raise ValidationIssnsException("The function requires a list of ISSNs in dictionary format")

        for issn in self.journal_issns:
            issn_value = issn.get('value')
            issn_type = issn.get('type')
            is_valid = issn_value == issns_dict.get(issn_type)
            yield {
                'title': 'Journal ISSN element validation',
                'xpath': './/journal-meta//issn[@pub-type=*]',
                'validation_type': 'value in list',
                'response': 'OK' if is_valid else 'ERROR',
                'expected_value': issns_dict,
                'got_value': issn_value,
                'message': 'Got <issn pub-type="{}">{}</issn> expected one item of this list: {}'.format(
                    issn_type,
                    issn_value,
                    " | ".join([f"{t}: {v}" for t, v in issns_dict.items()])
                ),
                'advice': None if is_valid else 'Provide a ISSN value as per the list: {}'.format(
                    " | ".join([f"{t}: {v}" for t, v in issns_dict.items()]))
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


class PublisherValidation:
    def __init__(self, xmltree):
        self.xmltree = xmltree
        self.publisher = Publisher(xmltree)

    def validate_publishers_names(self, expected_values):
        resp_publishers_names = dict(
            object='publishers names',
            output_expected=expected_values,
            output_obteined=self.publisher.publishers_names,
            match=(expected_values == self.publisher.publishers_names)
        )
        return resp_publishers_names


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
        publisher = PublisherValidation(self.xmltree)

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
