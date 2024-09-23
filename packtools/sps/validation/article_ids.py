from packtools.sps.validation.utils import format_response
from packtools.sps.models.article_ids import ArticleIds


class ArticleIdsValidation:
    def __init__(self, xml_tree):
        self.xml_tree = xml_tree
        self.article_ids = ArticleIds(xml_tree)
        self.pub_type_id_other = self.article_ids.other

    def pub_type_id_other_has_five_digits(self):
        if len(self.pub_type_id_other) != 5:
            yield format_response(
                title="pub-type-id=other has five digits",
                parent="article",
                parent_id=None,
                parent_article_type=self.xml_tree.find(".").get("article-type"),
                parent_lang=self.xml_tree.find(".").get("{http://www.w3.org/XML/1998/namespace}lang"),
                item="article-id",
                sub_item="@pub-id-type='other'",
                validation_type="format",
                is_valid=False,
                expected="Five digits",
                obtained=self.pub_type_id_other,
                advice="Provide a value with five digits for <article-id pub-id-type='other'>",
                data=None,
                error_level="ERROR",
            )

    def pub_type_id_other_is_numeric(self):
        if not self.pub_type_id_other.isdigit():
            yield format_response(
                title="pub-type-id=other is numeric",
                parent="article",
                parent_id=None,
                parent_article_type=self.xml_tree.find(".").get("article-type"),
                parent_lang=self.xml_tree.find(".").get("{http://www.w3.org/XML/1998/namespace}lang"),
                item="article-id",
                sub_item="@pub-id-type='other'",
                validation_type="format",
                is_valid=False,
                expected="numeric value",
                obtained=self.pub_type_id_other,
                advice="Provide a numeric value for <article-id pub-id-type='other'>",
                data=None,
                error_level="ERROR",
            )
