from ..models.front_articlemeta_issue import ArticleMetaIssue
from ..validation.exceptions import ValidationIssueMissingValue
from ..validation.utils import format_response


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
        return True, obtained, None


def _validate_special_number(obtained):
    if not _issue_special_number_is_valid(obtained):
        return False, 'speX where X is a valid alphanumeric value or None', 'Provide a valid value to special number'
    else:
        return True, obtained, None


def _validate_supplement(obtained):
    if not _issue_supplement_is_valid(obtained):
        return False, 'X suppl Y where X and Y are alphanumeric value', 'Provide a valid value to supplement'
    else:
        return True, obtained, None


class IssueValidation:
    def __init__(self, xmltree):
        self.xmltree = xmltree
        self.article_issue = ArticleMetaIssue(xmltree)

    def validate_volume(self, expected_value):
        """
        Checks the correctness of a volume.

        Parameters
        ----------
        expected_value : str
            Correct value for volume.

        Returns
        -------
        list of dict
            A list of dictionaries, such as:

            {
                'title': 'Article-meta volume element validation',
                'parent': None,
                'parent_id': None,
                'item': 'article-meta',
                'sub_item': 'volume',
                'validation_type': 'match',
                'response': 'OK',
                'expected_value': '56',
                'got_value': '56',
                'message': 'Got 56, expected 56',
                'advice': None,
                'data': {'number': '4', 'volume': '56'}
            }
        """
        yield format_response(
            title='Article-meta volume element validation',
            parent=None,
            parent_id=None,
            item='article-meta',
            sub_item='volume',
            validation_type='match',
            is_valid=expected_value == self.article_issue.volume,
            expected=expected_value,
            obtained=self.article_issue.volume,
            advice='Provide a value for volume that matches with expected value',
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

        Returns
        -------
        list of dict
            A list of dictionaries, such as:
            [
                {
                    'title': 'Article-meta issue element validation',
                    'parent': None,
                    'parent_id': None,
                    'item': 'article-meta',
                    'sub_item': 'issue',
                    'validation_type': 'format',
                    'response': 'OK',
                    'expected_value': '4',
                    'got_value': '4',
                    'message': 'Got 4, expected 4',
                    'advice': None,
                    'data': {'number': '4', 'volume': '56'}
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
                parent=None,
                parent_id=None,
                item='article-meta',
                sub_item='issue',
                validation_type='format',
                is_valid=is_valid,
                expected=expected,
                obtained=obtained,
                advice=advice,
                data=self.article_issue.data
            )
        else:
            expected = 'an identifier for the publication issue'
            resp = format_response(
                title='Article-meta issue element validation',
                parent=None,
                parent_id=None,
                item='article-meta',
                sub_item='issue',
                validation_type='exist',
                is_valid=False,
                expected=expected,
                obtained=None,
                advice='Provide an identifier for the publication issue',
                data=self.article_issue.data
            )
            resp['response'] = response_type_for_absent_issue
            yield resp

    def validate_supplement(self, expected_value):
        """
        Checks the correctness of a supplement.

        Parameters
        ----------
        expected_value : str
            Correct value for supplement.

        Returns
        -------
        list of dict
            A list of dictionaries, such as:
            [
                {
                    'title': 'Article-meta supplement element validation',
                    'parent': None,
                    'parent_id': None,
                    'item': 'article-meta',
                    'sub_item': 'supplement',
                    'validation_type': 'match',
                    'response': 'ERROR',
                    'expected_value': '2',
                    'got_value': '2b',
                    'message': 'Got 2b, expected 2',
                    'advice': 'Provide a value for supplement that matches with expected value',
                    'data': {'number': '4', 'suppl': '2b', 'volume': '56'}
                }
            ]
        """
        yield format_response(
            title='Article-meta supplement element validation',
            parent=None,
            parent_id=None,
            item='article-meta',
            sub_item='supplement',
            validation_type='match',
            is_valid=expected_value == self.article_issue.suppl,
            expected=expected_value,
            obtained=self.article_issue.suppl,
            advice='Provide a value for supplement that matches with expected value',
            data=self.article_issue.data
        )

    def validate(self, data):
        """
        Função que executa as validações da classe IssueValidation.

        Returns:
            dict: Um dicionário contendo os resultados das validações realizadas.
        
        """
                      
        vol_results = {
            'article_volume_validation': self.validate_volume(data['expected_value_volume'])
        }
        issue_results = { 
            'article_issue_validation': self.validate_issue(data['expected_value_issue'])
        }
        suppl_results = {
            'article_supplement_validation': self.validate_supplement(data['expected_value_supplment'])
        }
        vol_results.update(issue_results)
        vol_results.update(suppl_results)
        
        return vol_results


