from ..models.front_articlemeta_issue import ArticleMetaIssue


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

    def validate_volume(self, expected_value):
        """
        Checks the correctness of a volume.

        Parameters
        ----------
        expected_value : str
            Correct value for volume.

        Returns
        -------
        dict
            A dictionary as described in the example.

        Examples
        --------
        >>> validate_volume('23')

        {
            'object': 'volume',
            'output_expected': '23',
            'output_obteined': '23',
            'match': True
        }
        """
        resp_vol = dict(
            object='volume',
            output_expected=expected_value,
            output_obteined=self.article_issue.volume,
            match=(expected_value == self.article_issue.volume)
        )
        return resp_vol

    def validate_article_issue(self):
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
                    'xpath': './/front/article-meta/issue',
                    'validation_type': 'format',
                    'response': 'OK',
                    'expected_value': '4',
                    'got_value': '4',
                    'message': 'Got 4 expected 4',
                    'advice': None
                }
            ]
        """
        obtained = self.article_issue.issue

        if obtained:
            if 'spe' in obtained:
                is_valid, expected, advice = _validate_special_number(obtained)
            elif 'suppl' in obtained:
                is_valid, expected, advice = _validate_supplement(obtained)
            else:
                is_valid, expected, advice = _validate_issue_identifier(obtained)

            return [
                {
                    'title': 'Article-meta issue element validation',
                    'xpath': './/front/article-meta/issue',
                    'validation_type': 'format',
                    'response': 'OK' if is_valid else 'ERROR',
                    'expected_value': expected,
                    'got_value': obtained,
                    'message': 'Got {} expected {}'.format(obtained, expected),
                    'advice': advice
                }
            ]
        else:
            expected = 'an identifier for the publication issue'
            return [
                {
                    'title': 'Article-meta issue element validation',
                    'xpath': './/front/article-meta/issue',
                    'validation_type': 'exist',
                    'response': 'ERROR',
                    'expected_value': expected,
                    'got_value': None,
                    'message': 'Got None expected {}'.format(expected),
                    'advice': 'Provide an identifier for the publication issue'
                }
            ]

    def validate_supplement(self, expected_value):
        """
        Checks the correctness of a supplement.

        Parameters
        ----------
        expected_value : str
            Correct value for supplement.

        Returns
        -------
        dict
            A dictionary as described in the example.

        Examples
        --------
        >>> validate_supplement('5')

        {
            'object': 'supplement',
            'output_expected': '5',
            'output_obteined': '5b',
            'match': False
        }
        """
        resp_suppl = dict(
            object='supplement',
            output_expected=expected_value,
            output_obteined=self.article_issue.suppl,
            match=(expected_value == self.article_issue.suppl)
        )
        return resp_suppl

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