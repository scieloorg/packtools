from ..models.article_xref import ArticleXref


class ArticleXrefValidation:
    def __init__(self, xmltree):
        self.xmltree = xmltree
        self.article_xref = ArticleXref(xmltree)

    def validate_rid(self):
        """
        Checks if all rids (source) have the respective ids (destination)

        Returns
        -------
        dict
            A dictionary that registers the rids, ids, the difference between them and a message.

        Examples
        --------
        >>> validate_rid()

        {
            'expected_value': ['aff1', 'fig1', 'table1'],
            'obtained_value': ['aff1', 'fig1'],
            'result': ['table1'],
            'message': 'ERROR: the rids ['table1'] do not have the respective ids'
        }
        """
        diff = self.rids_without_ids
        if diff == set():
            message = "OK: all rids have the respective ids"
        else:
            message = f"ERROR: rids were found with the values {sorted(self.article_xref.all_xref_rids)}" \
                  f" but there were no ids with the corresponding values"
        resp = dict(
            expected_value=sorted(self.article_xref.all_xref_rids),
            obtained_value=sorted(self.article_xref.all_ids),
            result=sorted(diff),
            message=message
        )
        return resp

    def validate_id(self):
        """
        Checks if all ids (destination) have the respective rids (source)

        Returns
        -------
        dict
            A dictionary that registers the rids, ids, the difference between them and a message.

        Examples
        --------
        >>> validate_id()

        {
            'obtained_value': ['aff1', 'fig1'],
            'expected_value': ['aff1', 'fig1', 'table1'],
            'diff': ['table1'],
            'message': 'ERROR: the ids ['table1'] do not have the respective rids'
        }
        """
        diff = self.ids_without_rids
        if diff == set():
            message = "OK: all ids have the respective rids"
        else:
            message = f"ERROR: ids were found with the values {sorted(self.article_xref.all_ids)}" \
                  f" but there were no rids with the corresponding values"
        resp = dict(
            expected_value=sorted(self.article_xref.all_ids),
            obtained_value=sorted(self.article_xref.all_xref_rids),
            result=sorted(diff),
            message=message
        )
        return resp

    @property
    def reference_without_origin(self):
        return self.article_xref.all_ids - self.article_xref.all_xref_rids

    @property
    def reference_without_destiny(self):
        return self.article_xref.all_xref_rids - self.article_xref.all_ids
