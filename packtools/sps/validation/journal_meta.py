import gettext

from packtools.sps.models.journal_meta import ISSN, Acronym, Title, Publisher, JournalID
from packtools.sps.validation.exceptions import (
    ValidationPublisherException,
    ValidationIssnsException,
    ValidationJournalMetaException
)
from packtools.sps.validation.utils import build_response

_ = gettext.gettext


class ISSNValidation:
    def __init__(self, xmltree, issns_dict=None):
        self.xmltree = xmltree
        self.journal_issns = ISSN(xmltree)
        self.issns_dict = issns_dict

    def validate_issn(self, issns_dict, error_level="CRITICAL"):
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
            name = "electronic" if tp == "epub" else "print"
            is_valid = issn_expected == issn_obtained
            
            advice = 'Mark {} ISSN with <issn pub-type="{}">{}</issn> inside <journal-meta>'.format(name, tp, issn_expected)
            advice_text = _('Mark {name} ISSN with <issn pub-type="{pub_type}">{issn}</issn> inside <journal-meta>')
            advice_params = {"name": name, "pub_type": tp, "issn": issn_expected}
            
            parent_data = {
                "parent": "article",
                "parent_id": None,
                "parent_article_type": self.xmltree.get("article-type"),
                "parent_lang": self.xmltree.get("{http://www.w3.org/XML/1998/namespace}lang"),
            }
            
            yield build_response(
                title='Journal ISSN',
                parent=parent_data,
                item='issn',
                sub_item='pub-type',
                validation_type='value',
                is_valid=is_valid,
                expected='<issn pub-type="{}">{}</issn>'.format(tp, issn_expected),
                obtained='<issn pub-type="{}">{}</issn>'.format(tp, issn_obtained),
                advice=advice,
                advice_text=advice_text,
                advice_params=advice_params,
                data=self.journal_issns.data,
                error_level=error_level,
            )


class AcronymValidation:
    def __init__(self, xmltree):
        self.xmltree = xmltree
        self.journal_acronym = Acronym(xmltree)

    def acronym_validation(self, expected_value, error_level="CRITICAL"):
        if not expected_value:
            raise ValidationJournalMetaException('Function requires a value to acronym')
        is_valid = self.journal_acronym.text == expected_value
        
        advice = 'Mark journal acronym with <journal-id journal-id-type="publisher-id">{}</journal-id> inside <journal-meta>'.format(expected_value)
        advice_text = _('Mark journal acronym with <journal-id journal-id-type="publisher-id">{acronym}</journal-id> inside <journal-meta>')
        advice_params = {"acronym": expected_value}
        
        parent_data = {
            "parent": "article",
            "parent_id": None,
            "parent_article_type": self.xmltree.get("article-type"),
            "parent_lang": self.xmltree.get("{http://www.w3.org/XML/1998/namespace}lang"),
        }
        
        yield build_response(
            title='Journal acronym',
            parent=parent_data,
            item='journal-id',
            sub_item='@journal-id-type="publisher-id"',
            validation_type='value',
            is_valid=is_valid,
            expected=expected_value,
            obtained=self.journal_acronym.text,
            advice=advice,
            advice_text=advice_text,
            advice_params=advice_params,
            data={'acronym': self.journal_acronym.text},
            error_level=error_level,
        )


class TitleValidation:
    def __init__(self, xmltree):
        self.xmltree = xmltree
        self.journal_titles = Title(xmltree)

    def journal_title_validation(self, expected_value, error_level="CRITICAL"):
        if not expected_value:
            raise ValidationJournalMetaException('Function requires a value to journal title')
        is_valid = self.journal_titles.journal_title == expected_value
        
        advice = 'Mark journal title with <journal-title> inside <journal-title-group>'
        advice_text = _('Mark journal title with <journal-title> inside <journal-title-group>')
        advice_params = {}
        
        parent_data = {
            "parent": "article",
            "parent_id": None,
            "parent_article_type": self.xmltree.get("article-type"),
            "parent_lang": self.xmltree.get("{http://www.w3.org/XML/1998/namespace}lang"),
        }
        
        yield build_response(
            title='Journal title',
            parent=parent_data,
            item='journal-title-group',
            sub_item='journal-title',
            validation_type='value',
            is_valid=is_valid,
            expected=expected_value,
            obtained=self.journal_titles.journal_title,
            advice=advice,
            advice_text=advice_text,
            advice_params=advice_params,
            data={
                item.get("type"): item.get("value")
                for item in self.journal_titles.data
            },
            error_level=error_level,
        )

    def abbreviated_journal_title_validation(self, expected_value, error_level="CRITICAL"):
        if not expected_value:
            raise ValidationJournalMetaException('Function requires a value to abbreviated journal title')
        is_valid = self.journal_titles.abbreviated_journal_title == expected_value
        
        advice = 'Mark abbreviated journal title with <abbrev-journal-title> inside <journal-title-group>'
        advice_text = _('Mark abbreviated journal title with <abbrev-journal-title> inside <journal-title-group>')
        advice_params = {}
        
        parent_data = {
            "parent": "article",
            "parent_id": None,
            "parent_article_type": self.xmltree.get("article-type"),
            "parent_lang": self.xmltree.get("{http://www.w3.org/XML/1998/namespace}lang"),
        }
        
        yield build_response(
            title='Abbreviated journal title element validation',
            parent=parent_data,
            item="journal-title-group",
            sub_item="abbrev-journal-title",
            validation_type="value",
            is_valid=is_valid,
            expected=expected_value,
            obtained=self.journal_titles.abbreviated_journal_title,
            advice=advice,
            advice_text=advice_text,
            advice_params=advice_params,
            data={
                item.get("type"): item.get("value")
                for item in self.journal_titles.data
            },
            error_level=error_level,
        )


class PublisherNameValidation:
    def __init__(self, xmltree, publisher_name_list=None):
        self.xmltree = xmltree
        self.publisher = Publisher(self.xmltree)
        self.publisher_name_list = publisher_name_list

    def validate_publisher_names(self, publisher_name_list, error_level="CRITICAL"):
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
        error_level : str, optional
            The severity level of the validation error, by default "CRITICAL".

        Returns
        -------
        list of dict
            A list of dictionaries, such as:
            [
                {
                    'title': 'Publisher name element validation',
                    'parent': 'article',
                    'parent_article_type': 'research-article',
                    'parent_id': None,
                    'parent_lang': 'pt',
                    'item': 'publisher',
                    'sub_item': 'publisher-name',
                    'validation_type': 'value',
                    'response': 'OK',
                    'expected_value': 'Fundação Oswaldo Cruz',
                    'got_value': 'Fundação Oswaldo Cruz',
                    'message': 'Got Fundação Oswaldo Cruz, expected Fundação Oswaldo Cruz',
                    'advice': None,
                    'data': None,
                },...
            ]
        """
        publisher_name_list = publisher_name_list or self.publisher_name_list
        if not publisher_name_list:
            raise ValidationPublisherException("Function requires a list of publisher names")

        expected_list = publisher_name_list
        obtained_list = self.publisher.publishers_names

        for expected, obtained in zip(expected_list, obtained_list):
            is_valid = expected == obtained
            
            advice = f'Mark publisher name with <publisher><publisher-name>{expected}</publisher-name></publisher> inside <journal-meta>'
            advice_text = _('Mark publisher name with <publisher><publisher-name>{publisher}</publisher-name></publisher> inside <journal-meta>')
            advice_params = {"publisher": expected}
            
            parent_data = {
                "parent": "article",
                "parent_id": None,
                "parent_article_type": self.xmltree.get("article-type"),
                "parent_lang": self.xmltree.get("{http://www.w3.org/XML/1998/namespace}lang"),
            }
            
            yield build_response(
                title='Publisher name',
                parent=parent_data,
                item="publisher",
                sub_item="publisher-name",
                validation_type="value",
                is_valid=is_valid,
                expected=expected,
                obtained=obtained,
                advice=advice,
                advice_text=advice_text,
                advice_params=advice_params,
                data=None,
                error_level=error_level,
            )

        if len(obtained_list) != len(expected_list):
            if len(expected_list) > len(obtained_list):
                diff = expected_list[len(obtained_list):]
                item_description = 'missing'
                action = ('Complete', 'in')
            else:
                diff = obtained_list[len(expected_list):]
                item_description = 'not expected'
                action = ('Remove', 'from')

            diff_str = ' | '.join(diff)
            message = f'The following items is / are {item_description} in the XML: {diff_str}'
            advice = f'{action[0]} the following items {action[1]} the XML: {diff_str}'
            advice_text = _('{action} the following items {position} the XML: {items}')
            advice_params = {"action": action[0], "position": action[1], "items": diff_str}
            
            parent_data = {
                "parent": "article",
                "parent_id": None,
                "parent_article_type": self.xmltree.get("article-type"),
                "parent_lang": self.xmltree.get("{http://www.w3.org/XML/1998/namespace}lang"),
            }

            yield build_response(
                title='Publisher name',
                parent=parent_data,
                item="publisher",
                sub_item="publisher-name",
                validation_type="value",
                is_valid=False,
                expected=expected_list,
                obtained=obtained_list,
                advice=advice,
                advice_text=advice_text,
                advice_params=advice_params,
                data=None,
                error_level=error_level,
            )


class JournalIdValidation:
    def __init__(self, xmltree):
        self.xmltree = xmltree
        self.nlm_ta = JournalID(xmltree).nlm_ta

    def nlm_ta_id_validation(self, expected_value, error_level="CRITICAL"):
        """
        Checks whether the NLM TA ID value is as expected.

        XML input
        ---------
        <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink"
        article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="pt">
            <front>
                <journal-meta>
                    <journal-id journal-id-type="nlm-ta">Rev Saude Publica</journal-id>
                </journal-meta>
            </front>
        </article>

        Params
        ------
        expected_value : str
            The expected NLM TA ID value to validate against.
        error_level : str, optional
            The severity level of the validation error, by default "CRITICAL".

        Returns
        -------
        list of dict
            A list of dictionaries, such as:
            [
                {
                    'title': 'Journal ID element validation',
                    'parent': 'article',
                    'parent_article_type': "research-article",
                    'parent_id': None,
                    'parent_lang': 'pt',
                    'item': 'journal-meta',
                    'sub_item': 'journal-id',
                    'validation_type': 'value',
                    'response': 'OK',
                    'expected_value': 'Rev Saude Publica',
                    'got_value': 'Rev Saude Publica',
                    'message': 'Got Rev Saude Publica, expected Rev Saude Publica',
                    'advice': None,
                    'data': None,
                },...
            ]
        """
        is_valid = self.nlm_ta == expected_value
        
        advice = f'Mark an nlm-ta value with <journal-id journal-id-type="nlm-ta">{expected_value}</journal-id> inside <journal-meta>'
        advice_text = _('Mark an nlm-ta value with <journal-id journal-id-type="nlm-ta">{nlm_ta}</journal-id> inside <journal-meta>')
        advice_params = {"nlm_ta": expected_value}
        
        parent_data = {
            "parent": "article",
            "parent_id": None,
            "parent_article_type": self.xmltree.get("article-type"),
            "parent_lang": self.xmltree.get("{http://www.w3.org/XML/1998/namespace}lang"),
        }
        
        yield build_response(
            title='Journal ID',
            parent=parent_data,
            item="journal-meta",
            sub_item="journal-id",
            validation_type="value",
            is_valid=is_valid,
            expected=expected_value,
            obtained=self.nlm_ta,
            advice=advice,
            advice_text=advice_text,
            advice_params=advice_params,
            data=None,
            error_level=error_level,
        )


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
        'publisher-name': ['Casa de Oswaldo Cruz, Fundação Oswaldo Cruz'],
        'nlm-ta': 'Rev Saude Publica'
        }
        '''

        issn = ISSNValidation(self.xmltree)
        acronym = AcronymValidation(self.xmltree)
        title = TitleValidation(self.xmltree)
        publisher = PublisherNameValidation(self.xmltree)
        nlm_ta = JournalIdValidation(self.xmltree)

        resp_journal_meta = list(issn.validate_issn(expected_values['issns'])) + \
                            list(acronym.acronym_validation(expected_values['acronym'])) + \
                            list(title.journal_title_validation(expected_values['journal-title'])) + \
                            list(title.abbreviated_journal_title_validation(expected_values['abbrev-journal-title'])) + \
                            list(publisher.validate_publisher_names(expected_values['publisher-name'])) + \
                            list(nlm_ta.nlm_ta_id_validation(expected_values['nlm-ta']))

        return resp_journal_meta
