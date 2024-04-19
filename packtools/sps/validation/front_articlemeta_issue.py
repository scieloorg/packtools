from ..models.front_articlemeta_issue import ArticleMetaIssue
from ..validation.exceptions import ValidationIssueMissingValue
from packtools.sps.validation.utils import format_response


def _issue_identifier_is_valid(value):
    if value.isnumeric():
        return str(int(value)) == value
    else:
        return not('.' in value or ' ' in value)


def _issue_special_number_is_valid(value):
    """
    a special number value cannot contain a space or dot
    <issue>spe1</issue>
    <issue>spe</issue>
    """
    anterior, posterior = value.split('spe')
    return anterior == '' and (_issue_identifier_is_valid(posterior) or posterior == '')


def _issue_supplement_is_valid(value):
    """
    supplement cannot have a dot
    <issue>4 suppl 1</issue>
    <issue>suppl 1</issue>
    """
    anterior, posterior = value.split('suppl')
    if anterior:
        return _issue_identifier_is_valid(anterior.strip()) and _issue_identifier_is_valid(posterior.strip())
    else:
        return _issue_identifier_is_valid(posterior.strip())


def _validate_issue_identifier(obtained):
    if obtained.isnumeric():
        message = 'a numeric value that does not start with zero'
        advice = 'Provide a valid numeric value'
    else:
        message = 'a alphanumeric value that does not contain space or dot'
        advice = 'Provide a valid alphanumeric value'
    if not _issue_identifier_is_valid(obtained):
        return False, message, advice
    else:
        return _successful_validation(obtained)


def _validate_special_number(obtained):
    if not _issue_special_number_is_valid(obtained):
        return False, 'speX where X is a valid alphanumeric value or None', 'Provide a valid value to special number'
    else:
        return _successful_validation(obtained)


def _validate_supplement(obtained):
    if not _issue_supplement_is_valid(obtained):
        return False, 'X suppl Y where X and Y are alphanumeric value', 'Provide a valid value to supplement'
    else:
        return _successful_validation(obtained)


def _successful_validation(obtained):
    return True, obtained, None


class IssueValidation:
    def __init__(self, xmltree):
        self.xmltree = xmltree
        self.article_issue = ArticleMetaIssue(xmltree)

    def validate_volume(self, expected_value=None):
        """
        Checks the correctness of a volume.

        XML input
        ---------
        <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="en">
            <front>
                <article-meta>
                    <volume>56</volume>
                    <issue>4</issue>
                </article-meta>
            </front>
        </article>

        Parameters
        ----------
        expected_value : str or None
            Correct value for volume, when a value for volume is not expected, this parameter should not be passed.

        Returns
        -------
        dict
            A dictionary as described in the example:
            [
                {
                    'title': 'Article-meta issue element validation',
                    'parent': 'article-meta',
                    'parent_id': None,
                    'item': 'article-meta',
                    'sub_item': 'volume',
                    'validation_type': 'value',
                    'response': 'OK',
                    'expected_value': '56',
                    'got_value': '56',
                    'message': 'Got 56, expected 56',
                    'advice': None,
                    'data': {'number': '4', 'volume': '56'}
                }
            ]
        """
        yield format_response(
            title='Article-meta issue element validation',
            is_valid=expected_value == self.article_issue.volume,
            validation_type='value',
            obtained=self.article_issue.volume,
            expected=expected_value,
            item='article-meta',
            sub_item='volume',
            parent='article-meta',
            advice=f'provide {expected_value} as value for volume',
            data=self.article_issue.data
        )

    def validate_article_issue(self, response_type_for_absent_issue):
        """
        Checks whether the format of a value for issue is valid.

        XML input
        ---------
        <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="en">
            <front>
                <article-meta>
                    <volume>56</volume>
                    <issue>4</issue>
                    <supplement>2</supplement>
                </article-meta>
            </front>
        </article>

        Parameters
        ----------
        response_type_for_absent_issue : str
            Response type for absent value.

        Returns
        -------
        list of dict
            A list of dictionaries, such as:
            [
                {
                    'title': 'Article-meta issue element validation',
                    'parent': 'article-meta',
                    'parent_id': None,
                    'item': 'article-meta',
                    'sub_item': 'issue',
                    'validation_type': 'format',
                    'response': 'OK',
                    'expected_value': '4',
                    'got_value': '4',
                    'message': 'Got 4, expected 4',
                    'advice': None,
                    'data': {'number': '4', 'volume': '56'},
                }
            ]
        """
        if not response_type_for_absent_issue:
            raise ValidationIssueMissingValue("Function requires response type for absent value")

        obtained = self.article_issue.issue

        if obtained:
            if 'spe' in obtained:
                is_valid, expected, advice = _validate_special_number(obtained)
            elif 'suppl' in obtained:
                is_valid, expected, advice = _validate_supplement(obtained)
            else:
                is_valid, expected, advice = _validate_issue_identifier(obtained)

            yield format_response(
                title='Article-meta issue element validation',
                is_valid=is_valid,
                validation_type='format',
                obtained=obtained,
                expected=expected,
                item='article-meta',
                sub_item='issue',
                parent='article-meta',
                advice=advice,
                data=self.article_issue.data
            )
        else:
            expected = 'an identifier for the publication issue'

            response = format_response(
                title='Article-meta issue element validation',
                validation_type='exist',
                obtained=obtained,
                expected=expected,
                item='article-meta',
                sub_item='issue',
                parent='article-meta',
                advice='Provide an identifier for the publication issue',
                data=self.article_issue.data
            )

            response['response'] = response_type_for_absent_issue
            yield response

    def validate_supplement(self, expected_value=None):
        """
        Checks the correctness of a supplement.

        XML input
        ---------
        <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="en">
            <front>
                <article-meta>
                    <volume>56</volume>
                    <issue>4</issue>
                    <supplement>2</supplement>
                </article-meta>
            </front>
        </article>

        Parameters
        ----------
        expected_value : str or None
            Correct value for supplement, when a value for supplement is not expected, this parameter should not be passed.

        Returns
        -------
        dict
            A dictionary as described in the example:
            [
            {
                'title': 'Article-meta issue element validation',
                'parent': 'article-meta',
                'parent_id': None,
                'item': 'article-meta',
                'sub_item': 'supplement',
                'validation_type': 'format',
                'response': 'OK',
                'expected_value': '2',
                'got_value': '2',
                'message': 'Got 2, expected 2',
                'advice': None,
                'data': {'number': '4', 'suppl': '2', 'volume': '56'},
            }
        ]
        """
        yield format_response(
            title='Article-meta issue element validation',
            is_valid=expected_value == self.article_issue.suppl,
            validation_type='format',
            obtained=self.article_issue.suppl,
            expected=expected_value,
            item='article-meta',
            sub_item='supplement',
            parent='article-meta',
            advice=f'provide {expected_value} as value for supplement',
            data=self.article_issue.data
        )

    def validate(self, data):
        """
        Performs the validation functions of class IssueValidation.

        XML input
        ---------
        <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="en">
            <front>
                <article-meta>
                    <volume>56</volume>
                    <issue>4</issue>
                    <supplement>2</supplement>
                </article-meta>
            </front>
        </article>

        Parameters
        ----------
        date : dict
            data={
                'expected_value_volume': '56',
                'response_type_for_absent_issue': 'WARNING',
                'expected_value_supplement': '1'
            }

        Returns
        -------
        list
            A list of dictionary as described in the example:
            [
                {
                    'title': 'Article-meta issue element validation',
                    'parent': 'article-meta',
                    'parent_id': None,
                    'item': 'article-meta',
                    'sub_item': 'volume',
                    'validation_type': 'value',
                    'response': 'OK',
                    'expected_value': '56',
                    'got_value': '56',
                    'message': 'Got 56, expected 56',
                    'advice': None,
                    'data': {'number': '4', 'suppl': '1', 'volume': '56'},
                },...
            ]
        """
                      
        yield from self.validate_volume(data['expected_value_volume'])
        yield from self.validate_article_issue(data['response_type_for_absent_issue'])
        yield from self.validate_supplement(data['expected_value_supplement'])
