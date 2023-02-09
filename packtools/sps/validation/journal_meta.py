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


