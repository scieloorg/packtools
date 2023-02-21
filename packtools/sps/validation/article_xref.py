from ..models.article_xref import ArticleXref


class ArticleXrefValidation:
    def __init__(self, xmltree):
        self.xmltree = xmltree
        self.article_xref = ArticleXref(xmltree)

    def validate_citing_elements(self, expected_value):
        resp = dict(
            expected_value=expected_value,
            obteined_value=self.article_xref.all_ids,
            match=(expected_value == self.article_xref.all_ids)
        )
        return resp

    def validate_cited_elements(self, expected_value):
        resp = dict(
            expected_value=expected_value,
            obteined_value=self.article_xref.all_xref_rids,
            match=(expected_value == self.article_xref.all_xref_rids)
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
