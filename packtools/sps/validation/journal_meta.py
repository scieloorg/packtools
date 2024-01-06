from ..models.journal_meta import ISSN, Acronym, Title, Publisher
from packtools.sps.validation.exceptions import ValidationPublisherException


class ISSNValidation:
    def __init__(self, xmltree):
        self.xmltree = xmltree
        self.journal_issns = ISSN(xmltree)

    def validate_epub(self, expected_value):
        resp_epub = dict(
            object='issn epub',
            output_expected=expected_value,
            output_obteined=self.journal_issns.epub,
            match=(expected_value == self.journal_issns.epub)

        )
        return resp_epub

    def validate_ppub(self, expected_value):
        resp_ppub = dict(
            object='issn ppub',
            output_expected=expected_value,
            output_obteined=self.journal_issns.ppub,
            match=(expected_value == self.journal_issns.ppub)
        )
        return resp_ppub


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

    def validate_publishers_names(self, publisher_name_list):
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
        expected = " | ".join(sorted(publisher_name_list))
        obtained = " | ".join(sorted(self.publisher.publishers_names))

        is_valid = expected == obtained
        return [
            {
                'title': 'Publisher name element validation',
                'xpath': './/publisher//publisher-name',
                'validation_type': 'value',
                'response': 'OK' if is_valid else 'ERROR',
                'expected_value': expected,
                'got_value': obtained,
                'message': 'Got {} expected {}'.format(obtained, expected),
                'advice': None if is_valid else 'Provide a publisher name as expected {}'.format(expected)
            }
        ]


class JournalMetaValidation:
    def __init__(self, xmltree):
        self.xmltree = xmltree

    def validate(self, expected_values):
        '''
        expected_values is a dict like:
        {
        'issn_epub': '0103-5053',
        'issn_ppub': '1678-4790',
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

        resp_journal_meta = [
            issn.validate_epub(expected_values['issn_epub']),
            issn.validate_ppub(expected_values['issn_ppub']),
            acronym.validate_text(expected_values['acronym']),
            title.validate_journal_title(expected_values['journal-title']),
            title.validate_abbreviated_journal_title(expected_values['abbrev-journal-title']),
        ]
        resp_journal_meta.extend(publisher.validate_publishers_names(expected_values['publisher-name']))
        return resp_journal_meta
