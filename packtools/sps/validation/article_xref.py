from ..models.article_xref import ArticleXref


class ArticleXrefValidation:
    def __init__(self, xmltree):
        self.xmltree = xmltree
        self.article_xref = ArticleXref(xmltree)

    def validate_citing_elements(self):
        """
        Checks if all citing elements (source) have the respective cited elements (destination)

        Returns
        -------
        dict
            A dictionary that registers the citing elements, cited elements, the difference between them and a message.

        Examples
        --------
        >>> validate_citing_elements()

        {
            'citing_elements': {'aff1', 'fig1', 'table1'},
            'cited_elements': {'aff1', 'fig1'},
            'diff': {'table1'},
            'msg': 'ERROR: the citing elements {'table1'} do not have the respective cited elements'
        }
        """
        diff = self.reference_without_destiny
        if diff == set():
            msg = "OK: all citing elements have the respective cited elements"
        else:
            msg = f"ERROR: the citing elements {diff} do not have the respective cited elements"
        resp = dict(
            citing_elements=self.article_xref.all_xref_rids,
            cited_elements=self.article_xref.all_ids,
            diff=diff,
            msg=msg
        )
        return resp

    def validate_cited_elements(self):
        """
                Checks if all cited elements (destination) have the respective citing elements (source)

                Returns
                -------
                dict
                    A dictionary that registers the citing elements, cited elements, the difference between them and a message.

                Examples
                --------
                >>> validate_cited_elements()

                {
                    'citing_elements': {'aff1', 'fig1'},
                    'cited_elements': {'aff1', 'fig1', 'table1'},
                    'diff': {'table1'},
                    'msg': 'ERROR: the cited elements {'table1'} do not have the respective citing elements'
                }
                """
        diff = self.reference_without_origin
        if diff == set():
            msg = "OK: all cited elements have the respective citing elements"
        else:
            msg = f"ERROR: the cited elements {diff} do not have the respective citing elements"
        resp = dict(
            citing_elements=self.article_xref.all_xref_rids,
            cited_elements=self.article_xref.all_ids,
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

    def validate_parity_between_citing_and_cited_elements(self, expected_value):
        union = self.reference_without_destiny.union(self.reference_without_origin)
        resp = dict(
            expected_value=expected_value,
            obteined_value=union,
            match=(expected_value == union)
        )
        return resp
