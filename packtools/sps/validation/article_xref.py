from ..models.article_xref import ArticleXref


class ArticleXrefValidation:
    def __init__(self, xmltree):
        self.xmltree = xmltree
        self.article_xref = ArticleXref(xmltree)

    def validate_citing_elements(self, expected_value):
        resp = dict(
            output_expected=expected_value,
            output_obteined=self.article_xref.all_ids,
            match=True if expected_value == self.article_xref.all_ids else False
        )
        return resp

    def validate_cited_elements(self, expected_value):
        resp = dict(
            output_expected=expected_value,
            output_obteined=self.article_xref.all_xref_rids,
            match=True if expected_value == self.article_xref.all_xref_rids else False
        )
        return resp

    def validate_parity_between_citing_and_cited_elements(self, expected_value):
        union = self.article_xref.reference_without_destiny.union(self.article_xref.reference_without_destiny)
        resp = dict(
            output_expected=expected_value,
            output_obteined=union,
            match=True if expected_value == union else False
        )
        return resp
