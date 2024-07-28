from ..models.media import ArticleMedias
from ..validation.utils import format_response


class MediaValidation:
    def __init__(self, xmltree):
        self.xmltree = xmltree
        self.medias = ArticleMedias(xmltree).data()

    def validate_media_existence(self, error_level="WARNING"):
        for media in self.medias:
            yield format_response(
                title="validation of <media> elements",
                parent=media.get("parent"),
                parent_id=media.get("parent_id"),
                parent_article_type=media.get("parent_article_type"),
                parent_lang=media.get("parent_lang"),
                item="media",
                sub_item=None,
                validation_type="exist",
                is_valid=True,
                expected="media element",
                obtained="media element",
                advice=None,
                data=media,
                error_level="OK",
            )
        else:
            yield format_response(
                title="validation of <media> elements",
                parent="article",
                parent_id=None,
                parent_article_type=self.xmltree.get("article-type"),
                parent_lang=self.xmltree.get(
                    "{http://www.w3.org/XML/1998/namespace}lang"
                ),
                item="media",
                sub_item=None,
                validation_type="exist",
                is_valid=False,
                expected="<media> element",
                obtained=None,
                advice="Consider adding a <media> element to include multimedia content related to the article.",
                data=None,
                error_level=error_level,
            )
