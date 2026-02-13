import re
from packtools.sps.models.journal_meta import ISSN, Acronym, Title, Publisher, JournalID
from packtools.sps.validation.exceptions import (
    ValidationPublisherException,
    ValidationIssnsException,
    ValidationJournalMetaException
)
from packtools.sps.validation.utils import format_response


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
            yield format_response(
                title='Journal ISSN',
                parent='article',
                parent_id=None,
                parent_article_type=self.xmltree.get("article-type"),
                parent_lang=self.xmltree.get("{http://www.w3.org/XML/1998/namespace}lang"),
                item='issn',
                sub_item='pub-type',
                validation_type='value',
                is_valid=is_valid,
                expected='<issn pub-type="{}">{}</issn>'.format(tp, issn_expected),
                obtained='<issn pub-type="{}">{}</issn>'.format(tp, issn_obtained),
                advice='Mark {} ISSN with <issn pub-type="{}">{}</issn> inside <journal-meta>'.format(name, tp, issn_expected),
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
        yield format_response(
            title='Journal acronym',
            parent='article',
            parent_id=None,
            parent_article_type=self.xmltree.get("article-type"),
            parent_lang=self.xmltree.get("{http://www.w3.org/XML/1998/namespace}lang"),
            item='journal-id',
            sub_item='@journal-id-type="publisher-id"',
            validation_type='value',
            is_valid=is_valid,
            expected=expected_value,
            obtained=self.journal_acronym.text,
            advice='Mark journal acronym with <journal-id journal-id-type="publisher-id">{}</journal-id> inside <journal-meta>'.format(expected_value),
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
        yield format_response(
            title='Journal title',
            parent='article',
            parent_id=None,
            parent_article_type=self.xmltree.get("article-type"),
            parent_lang=self.xmltree.get("{http://www.w3.org/XML/1998/namespace}lang"),
            item='journal-title-group',
            sub_item='journal-title',
            validation_type='value',
            is_valid=is_valid,
            expected=expected_value,
            obtained=self.journal_titles.journal_title,
            advice='Mark journal title with <journal-title> inside <journal-title-group>',
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
        yield format_response(
            title='Abbreviated journal title element validation',
            parent='article',
            parent_id=None,
            parent_article_type=self.xmltree.get("article-type"),
            parent_lang=self.xmltree.get("{http://www.w3.org/XML/1998/namespace}lang"),
            item="journal-title-group",
            sub_item="abbrev-journal-title",
            validation_type="value",
            is_valid=is_valid,
            expected=expected_value,
            obtained=self.journal_titles.abbreviated_journal_title,
            advice='Mark abbreviated journal title with <abbrev-journal-title> inside <journal-title-group>',
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
            yield format_response(
                title='Publisher name',
                parent='article',
                parent_id=None,
                parent_article_type=self.xmltree.get("article-type"),
                parent_lang=self.xmltree.get("{http://www.w3.org/XML/1998/namespace}lang"),
                item="publisher",
                sub_item="publisher-name",
                validation_type="value",
                is_valid=is_valid,
                expected=expected,
                obtained=obtained,
                advice=f'Mark publisher name with <publisher><publisher-name>{expected}</publisher-name></publisher> inside <journal-meta>',
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

            yield format_response(
                title='Publisher name',
                parent='article',
                parent_id=None,
                parent_article_type=self.xmltree.get("article-type"),
                parent_lang=self.xmltree.get("{http://www.w3.org/XML/1998/namespace}lang"),
                item="publisher",
                sub_item="publisher-name",
                validation_type="value",
                is_valid=False,
                expected=expected_list,
                obtained=obtained_list,
                advice=advice,
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
        yield format_response(
            title='Journal ID',
            parent='article',
            parent_id=None,
            parent_article_type=self.xmltree.get("article-type"),
            parent_lang=self.xmltree.get("{http://www.w3.org/XML/1998/namespace}lang"),
            item="journal-meta",
            sub_item="journal-id",
            validation_type="value",
            is_valid=is_valid,
            expected=expected_value,
            obtained=self.nlm_ta,
            advice=f'Mark an nlm-ta value with <journal-id journal-id-type="nlm-ta">{expected_value}</journal-id> inside <journal-meta>',
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


class JournalMetaPresenceValidation:
    """
    Validates presence and uniqueness of journal-meta and its required elements.
    Implements SPS 1.10 rules for structural validation.
    """
    def __init__(self, xmltree):
        self.xmltree = xmltree

    def validate_journal_meta_presence(self, error_level="CRITICAL"):
        """
        Rule 1: Validates that <journal-meta> element exists in <front>.
        
        Returns
        -------
        generator of dict
            Validation result indicating presence of journal-meta.
        """
        journal_meta = self.xmltree.find('.//front/journal-meta')
        is_valid = journal_meta is not None
        
        yield format_response(
            title='Journal meta presence',
            parent='article',
            parent_id=None,
            parent_article_type=self.xmltree.get("article-type"),
            parent_lang=self.xmltree.get("{http://www.w3.org/XML/1998/namespace}lang"),
            item='journal-meta',
            sub_item=None,
            validation_type='exist',
            is_valid=is_valid,
            expected='<journal-meta> element',
            obtained='<journal-meta>' if is_valid else None,
            advice='Add <journal-meta> element inside <front>',
            data=None,
            error_level=error_level,
        )

    def validate_journal_meta_uniqueness(self, error_level="CRITICAL"):
        """
        Rule 2: Validates that <journal-meta> appears exactly once in <front>.
        
        Returns
        -------
        generator of dict
            Validation result indicating uniqueness of journal-meta.
        """
        journal_meta_list = self.xmltree.xpath('.//front/journal-meta')
        count = len(journal_meta_list)
        is_valid = count == 1
        
        if count == 0:
            obtained = 'No <journal-meta> found'
        elif count == 1:
            obtained = 'One <journal-meta> element'
        else:
            obtained = f'{count} <journal-meta> elements found'
        
        yield format_response(
            title='Journal meta uniqueness',
            parent='article',
            parent_id=None,
            parent_article_type=self.xmltree.get("article-type"),
            parent_lang=self.xmltree.get("{http://www.w3.org/XML/1998/namespace}lang"),
            item='journal-meta',
            sub_item=None,
            validation_type='exist',
            is_valid=is_valid,
            expected='exactly one <journal-meta> element',
            obtained=obtained,
            advice='Ensure exactly one <journal-meta> element exists inside <front>',
            data={'count': count},
            error_level=error_level,
        )

    def validate_publisher_id_presence(self, error_level="CRITICAL"):
        """
        Rule 3: Validates presence of <journal-id journal-id-type="publisher-id">.
        
        Returns
        -------
        generator of dict
            Validation result for publisher-id presence.
        """
        publisher_id = self.xmltree.findtext('.//journal-meta//journal-id[@journal-id-type="publisher-id"]')
        is_valid = publisher_id is not None and publisher_id.strip() != ''
        
        yield format_response(
            title='Journal publisher ID presence',
            parent='article',
            parent_id=None,
            parent_article_type=self.xmltree.get("article-type"),
            parent_lang=self.xmltree.get("{http://www.w3.org/XML/1998/namespace}lang"),
            item='journal-id',
            sub_item='@journal-id-type="publisher-id"',
            validation_type='exist',
            is_valid=is_valid,
            expected='<journal-id journal-id-type="publisher-id"> with non-empty value',
            obtained=publisher_id if is_valid else None,
            advice='Add <journal-id journal-id-type="publisher-id">ACRONYM</journal-id> inside <journal-meta>',
            data={'publisher_id': publisher_id},
            error_level=error_level,
        )

    def validate_journal_title_presence(self, error_level="CRITICAL"):
        """
        Rule 4: Validates presence of <journal-title>.
        
        Returns
        -------
        generator of dict
            Validation result for journal-title presence.
        """
        journal_title = self.xmltree.findtext('.//journal-meta//journal-title-group//journal-title')
        is_valid = journal_title is not None and journal_title.strip() != ''
        
        yield format_response(
            title='Journal title presence',
            parent='article',
            parent_id=None,
            parent_article_type=self.xmltree.get("article-type"),
            parent_lang=self.xmltree.get("{http://www.w3.org/XML/1998/namespace}lang"),
            item='journal-title-group',
            sub_item='journal-title',
            validation_type='exist',
            is_valid=is_valid,
            expected='<journal-title> with non-empty value',
            obtained=journal_title if is_valid else None,
            advice='Add <journal-title>Title</journal-title> inside <journal-title-group>',
            data={'journal_title': journal_title},
            error_level=error_level,
        )

    def validate_abbrev_journal_title_presence(self, error_level="CRITICAL"):
        """
        Rule 5: Validates presence of <abbrev-journal-title abbrev-type="publisher">.
        
        Returns
        -------
        generator of dict
            Validation result for abbreviated journal title presence.
        """
        abbrev_title = self.xmltree.findtext('.//journal-meta//journal-title-group//abbrev-journal-title[@abbrev-type="publisher"]')
        is_valid = abbrev_title is not None and abbrev_title.strip() != ''
        
        yield format_response(
            title='Abbreviated journal title presence',
            parent='article',
            parent_id=None,
            parent_article_type=self.xmltree.get("article-type"),
            parent_lang=self.xmltree.get("{http://www.w3.org/XML/1998/namespace}lang"),
            item='journal-title-group',
            sub_item='abbrev-journal-title',
            validation_type='exist',
            is_valid=is_valid,
            expected='<abbrev-journal-title abbrev-type="publisher"> with non-empty value',
            obtained=abbrev_title if is_valid else None,
            advice='Add <abbrev-journal-title abbrev-type="publisher">Abbrev. Title</abbrev-journal-title> inside <journal-title-group>',
            data={'abbrev_title': abbrev_title},
            error_level=error_level,
        )

    def validate_issn_presence(self, error_level="CRITICAL"):
        """
        Rule 6: Validates presence of at least one <issn> (epub or ppub).
        
        Returns
        -------
        generator of dict
            Validation result for ISSN presence.
        """
        issn_list = self.xmltree.xpath('.//journal-meta//issn')
        is_valid = len(issn_list) > 0
        
        issn_data = [{'type': node.get('pub-type'), 'value': node.text} for node in issn_list]
        
        yield format_response(
            title='ISSN presence',
            parent='article',
            parent_id=None,
            parent_article_type=self.xmltree.get("article-type"),
            parent_lang=self.xmltree.get("{http://www.w3.org/XML/1998/namespace}lang"),
            item='issn',
            sub_item=None,
            validation_type='exist',
            is_valid=is_valid,
            expected='at least one <issn> element',
            obtained=f'{len(issn_list)} ISSN(s) found' if is_valid else 'No ISSN found',
            advice='Add at least one <issn pub-type="epub">XXXX-XXXX</issn> or <issn pub-type="ppub">XXXX-XXXX</issn> inside <journal-meta>',
            data=issn_data,
            error_level=error_level,
        )

    def validate_publisher_name_presence(self, error_level="CRITICAL"):
        """
        Rule 7: Validates presence of <publisher-name>.
        
        Returns
        -------
        generator of dict
            Validation result for publisher-name presence.
        """
        publisher_name = self.xmltree.findtext('.//journal-meta//publisher//publisher-name')
        is_valid = publisher_name is not None and publisher_name.strip() != ''
        
        yield format_response(
            title='Publisher name presence',
            parent='article',
            parent_id=None,
            parent_article_type=self.xmltree.get("article-type"),
            parent_lang=self.xmltree.get("{http://www.w3.org/XML/1998/namespace}lang"),
            item='publisher',
            sub_item='publisher-name',
            validation_type='exist',
            is_valid=is_valid,
            expected='<publisher-name> with non-empty value',
            obtained=publisher_name if is_valid else None,
            advice='Add <publisher><publisher-name>Publisher Name</publisher-name></publisher> inside <journal-meta>',
            data={'publisher_name': publisher_name},
            error_level=error_level,
        )


class ISSNFormatValidation:
    """
    Validates ISSN format and attributes.
    Implements SPS 1.10 format validation rules.
    """
    def __init__(self, xmltree):
        self.xmltree = xmltree
        self.journal_issns = ISSN(xmltree)

    def validate_issn_format(self, error_level="ERROR"):
        """
        Rule 8: Validates ISSN format (XXXX-XXXX pattern).
        ISSN must be 4 digits, hyphen, 4 digits (last digit can be X).
        
        Returns
        -------
        generator of dict
            Validation results for each ISSN format.
        """
        # Regex pattern for ISSN: 4 digits, hyphen, 3 digits + (digit or X)
        issn_pattern = re.compile(r'^\d{4}-\d{3}[\dXx]$')
        
        for issn_data in self.journal_issns.data:
            issn_value = issn_data.get('value', '')
            issn_type = issn_data.get('type', '')
            
            is_valid = bool(issn_pattern.match(issn_value)) if issn_value else False
            
            yield format_response(
                title='ISSN format',
                parent='article',
                parent_id=None,
                parent_article_type=self.xmltree.get("article-type"),
                parent_lang=self.xmltree.get("{http://www.w3.org/XML/1998/namespace}lang"),
                item='issn',
                sub_item=f'@pub-type="{issn_type}"' if issn_type else None,
                validation_type='format',
                is_valid=is_valid,
                expected='ISSN with format XXXX-XXXX (where X can be a digit or letter X)',
                obtained=issn_value,
                advice=f'Correct ISSN format to XXXX-XXXX pattern. Current value: {issn_value}',
                data=issn_data,
                error_level=error_level,
            )


class JournalMetaAttributeValidation:
    """
    Validates allowed attribute values in journal-meta elements.
    Implements SPS 1.10 attribute validation rules.
    """
    def __init__(self, xmltree):
        self.xmltree = xmltree

    def validate_journal_id_type_values(self, error_level="ERROR"):
        """
        Rule 9: Validates allowed values for @journal-id-type (publisher-id, nlm-ta).
        
        Returns
        -------
        generator of dict
            Validation results for each journal-id type attribute.
        """
        allowed_types = ['publisher-id', 'nlm-ta']
        journal_ids = self.xmltree.xpath('.//journal-meta//journal-id')
        
        for journal_id in journal_ids:
            id_type = journal_id.get('journal-id-type')
            id_value = journal_id.text
            
            is_valid = id_type in allowed_types if id_type else False
            
            yield format_response(
                title='Journal ID type attribute',
                parent='article',
                parent_id=None,
                parent_article_type=self.xmltree.get("article-type"),
                parent_lang=self.xmltree.get("{http://www.w3.org/XML/1998/namespace}lang"),
                item='journal-id',
                sub_item='@journal-id-type',
                validation_type='value in list',
                is_valid=is_valid,
                expected=f'{allowed_types}',
                obtained=id_type,
                advice=f'Set @journal-id-type to one of {allowed_types}. Current value: {id_type}',
                data={'journal_id_type': id_type, 'value': id_value},
                error_level=error_level,
            )

    def validate_issn_pub_type_values(self, error_level="ERROR"):
        """
        Rule 10: Validates allowed values for @pub-type in <issn> (epub, ppub).
        
        Returns
        -------
        generator of dict
            Validation results for each ISSN pub-type attribute.
        """
        allowed_types = ['epub', 'ppub']
        issns = self.xmltree.xpath('.//journal-meta//issn')
        
        for issn in issns:
            pub_type = issn.get('pub-type')
            issn_value = issn.text
            
            is_valid = pub_type in allowed_types if pub_type else False
            
            yield format_response(
                title='ISSN pub-type attribute',
                parent='article',
                parent_id=None,
                parent_article_type=self.xmltree.get("article-type"),
                parent_lang=self.xmltree.get("{http://www.w3.org/XML/1998/namespace}lang"),
                item='issn',
                sub_item='@pub-type',
                validation_type='value in list',
                is_valid=is_valid,
                expected=f'{allowed_types}',
                obtained=pub_type,
                advice=f'Set @pub-type to one of {allowed_types}. Current value: {pub_type}',
                data={'pub_type': pub_type, 'value': issn_value},
                error_level=error_level,
            )

    def validate_issn_type_uniqueness(self, error_level="WARNING"):
        """
        Rule 11: Validates that there are no duplicate ISSN pub-types.
        
        Returns
        -------
        generator of dict
            Validation results for ISSN type uniqueness.
        """
        issns = self.xmltree.xpath('.//journal-meta//issn')
        pub_types = [issn.get('pub-type') for issn in issns if issn.get('pub-type')]
        
        # Count occurrences of each type
        type_counts = {}
        for pub_type in pub_types:
            type_counts[pub_type] = type_counts.get(pub_type, 0) + 1
        
        # Check for duplicates
        duplicates = [pt for pt, count in type_counts.items() if count > 1]
        is_valid = len(duplicates) == 0
        
        if duplicates:
            obtained = f'Duplicate pub-types found: {duplicates}'
        else:
            obtained = 'All ISSN pub-types are unique'
        
        yield format_response(
            title='ISSN type uniqueness',
            parent='article',
            parent_id=None,
            parent_article_type=self.xmltree.get("article-type"),
            parent_lang=self.xmltree.get("{http://www.w3.org/XML/1998/namespace}lang"),
            item='issn',
            sub_item='@pub-type',
            validation_type='uniqueness',
            is_valid=is_valid,
            expected='unique pub-type values for each ISSN',
            obtained=obtained,
            advice=f'Remove duplicate ISSN elements with same pub-type. Duplicates: {duplicates}' if duplicates else None,
            data={'type_counts': type_counts, 'duplicates': duplicates},
            error_level=error_level,
        )
