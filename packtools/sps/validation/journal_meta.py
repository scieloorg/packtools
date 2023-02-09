from ..models.journal_meta import ISSN, Acronym, Title, Publisher


class ISSNValidation:
    def __init__(self, xmltree):
        self.xmltree = xmltree
        self.journal_issns = ISSN(xmltree)

    def validate_epub(self, expected_value):
        resp_epub = dict(
            attrib='issn_epub',
            input=self.xmltree,
            output_expected=expected_value,
            output_obteined=self.journal_issns.epub,
            match=True if expected_value == self.journal_issns.epub else False
        )
        return resp_epub

    def validate_ppub(self, expected_value):
        resp_ppub = dict(
            attrib='issn_ppub',
            input=self.xmltree,
            output_expected=expected_value,
            output_obteined=self.journal_issns.ppub,
            match=True if expected_value == self.journal_issns.ppub else False
        )
        return resp_ppub


class AcronymValidation:
    def __init__(self, xmltree):
        self.xmltree = xmltree
        self.journal_acronym = Acronym(xmltree)

    def validate_text(self, expected_value):
        resp_text = dict(
            attrib='acronym',
            input=self.xmltree,
            output_expected=expected_value,
            output_obteined=self.journal_acronym.text,
            match=True if expected_value == self.journal_acronym.text else False
        )
        return resp_text


class TitleValidation:
    def __init__(self, xmltree):
        self.xmltree = xmltree
        self.journal_titles = Title(xmltree)

    def validate_journal_title(self, expected_value):
        resp_journal_title = dict(
            attrib='journal_title',
            input=self.xmltree,
            output_expected=expected_value,
            output_obteined=self.journal_titles.journal_title,
            match=True if expected_value == self.journal_titles.journal_title else False
        )
        return resp_journal_title

    def validate_abbreviated_journal_title(self, expected_value):
        resp_abbreviated_journal_title = dict(
            attrib='abbreviated_journal_title',
            input=self.xmltree,
            output_expected=expected_value,
            output_obteined=self.journal_titles.abbreviated_journal_title,
            match=True if expected_value == self.journal_titles.abbreviated_journal_title else False
        )
        return resp_abbreviated_journal_title


class PublisherValidation:
    def __init__(self, xmltree):
        self.xmltree = xmltree
        self.publisher = Publisher(xmltree)

    def validate_publishers_names(self, expected_values):
        resp_publishers_names = dict(
            attrib='publishers_names',
            input=self.xmltree,
            output_expected=expected_values,
            output_obteined=self.publisher.publishers_names,
            match=True if expected_values == self.publisher.publishers_names else False
        )
        return resp_publishers_names


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
        publisher = PublisherValidation(self.xmltree)

        resp_journal_meta = [
            issn.validate_epub(expected_values['issn_epub']),
            issn.validate_ppub(expected_values['issn_ppub']),
            acronym.validate_text(expected_values['acronym']),
            title.validate_journal_title(expected_values['journal-title']),
            title.validate_abbreviated_journal_title(expected_values['abbrev-journal-title']),
            publisher.validate_publishers_names(expected_values['publisher-name'])
        ]
        return resp_journal_meta
