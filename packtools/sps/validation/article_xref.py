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
        diff = self.reference_without_destiny
        if diff == set():
            msg = "OK: all rid elements have the respective id elements"
        else:
            msg = f"ERROR: the rid elements {diff} do not have the respective id elements"
        resp = dict(
            rid_elements=self.article_xref.all_xref_rids,
            id_elements=self.article_xref.all_ids,
            diff=diff,
            msg=msg
        )
        return resp

    def validate_id_elements(self):
        """
                Checks if all id elements (destination) have the respective rid elements (source)

                Returns
                -------
                dict
                    A dictionary that registers the rid elements, id elements, the difference between them and a message.

                Examples
                --------
                >>> validate_id_elements()

                {
                    'rid_elements': {'aff1', 'fig1'},
                    'id_elements': {'aff1', 'fig1', 'table1'},
                    'diff': {'table1'},
                    'msg': 'ERROR: the id elements {'table1'} do not have the respective rid elements'
                }
                """
        diff = self.reference_without_origin
        if diff == set():
            msg = "OK: all id elements have the respective rid elements"
        else:
            msg = f"ERROR: the id elements {diff} do not have the respective rid elements"
        resp = dict(
            rid_elements=self.article_xref.all_xref_rids,
            id_elements=self.article_xref.all_ids,
            diff=diff,
            msg=msg
        )
        return resp

    @property
    def reference_without_origin(self):
        return self.article_xref.all_ids - self.article_xref.all_xref_rids

    @property
    def reference_without_destiny(self):
        return self.article_xref.all_xref_rids - self.article_xref.all_ids
