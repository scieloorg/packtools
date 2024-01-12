from ..models.front_articlemeta_issue import ArticleMetaIssue


def _is_number(value):
    # a numeric value for issue cannot start with zero
    # <issue>4</issue>
    return value.isnumeric() and not value.startswith('0')


def _is_special_number(value):
    # a special number cannot contain a space or dot
    # <issue>spe1</issue>
    splitted_value = value.split('spe')
    return splitted_value[0] is '' and _is_number(splitted_value[1])


def _is_supplement(value):
    # supplement cannot have a dot
    # <issue>4 suppl 1</issue>
    # <issue>suppl 1</issue>
    splitted_value = value.split('suppl')
    if splitted_value[0]:
        return _is_number(splitted_value[0].strip()) and _is_number(splitted_value[1].strip())
    else:
        return _is_number(splitted_value[1].strip())


def _validate_number(obtained):
    if not _is_number(obtained):
        return False, 'a numeric value that does not start with zero', 'Provide a valid numeric value'
    else:
        return _success(obtained)


def _validate_special_number(obtained):
    if not _is_special_number(obtained):
        return False, 'spe() where () is a valid numeric value', 'Provide a valid value to special number'
    else:
        return _success(obtained)


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

    def validate_issue(self, expected_value):
        """
        Checks the correctness of a issue.

        Parameters
        ----------
        expected_value : str
            Correct value for issue.

        Returns
        -------
        dict
            A dictionary as described in the example.

        Examples
        --------
        >>> validate_issue('4')

        {
            'object': 'issue',
            'output_expected': '4',
            'output_obteined': '4',
            'match': True
        }
        """
        resp_issue = dict(
            object='issue',
            output_expected=expected_value,
            output_obteined=self.article_issue.issue,
            match=(expected_value == self.article_issue.issue)
        )
        return resp_issue

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