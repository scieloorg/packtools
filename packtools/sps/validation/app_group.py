from ..models.app_group import XmlAppGroup
from ..validation.utils import format_response


class AppValidation:
    def __init__(self, xmltree, params):
        self.xmltree = xmltree
        self.apps = XmlAppGroup(xmltree).data

    def validate_app_existence(self, error_level="WARNING"):
        for app in self.apps:
            yield format_response(
                title="validation of <app> elements",
                parent=app.get("parent"),
                parent_id=app.get("parent_id"),
                parent_article_type=app.get("parent_article_type"),
                parent_lang=app.get("parent_lang"),
                item="app-group",
                sub_item="app",
                validation_type="exist",
                is_valid=True,
                expected=app.get("app_id"),
                obtained=app.get("app_id"),
                advice=None,
                data=app,
                error_level="OK",
            )
        else:
            yield format_response(
                title="validation of <app> elements",
                parent="article",
                parent_id=None,
                parent_article_type=self.xmltree.get("article-type"),
                parent_lang=self.xmltree.get(
                    "{http://www.w3.org/XML/1998/namespace}lang"
                ),
                item="app-group",
                sub_item="app",
                validation_type="exist",
                is_valid=False,
                expected="<app> element",
                obtained=None,
                advice="Consider adding an <app> element to include additional content such as supplementary materials or appendices.",
                data=None,
                error_level=error_level,
            )
