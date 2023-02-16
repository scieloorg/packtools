from ..models.front_articlemeta_issue import ArticleMetaIssue


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
