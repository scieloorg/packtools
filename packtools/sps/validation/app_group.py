from packtools.sps.models.app_group import XmlAppGroup
from packtools.sps.validation.utils import format_response


class AppValidation:
    def __init__(self, xmltree, params):
        self.xmltree = xmltree
        self.apps = list(XmlAppGroup(xmltree).data)
        self.params = params

    def validate(self):
        yield from self.validate_app_existence()

    def validate_app_existence(self):
        if not self.apps:
            yield format_response(
                title="<app>",
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
                error_level=self.params["app_existence_error_level"],
            )
        else:
            for app in self.apps:
                yield format_response(
                    title="<app>",
                    parent=app.get("parent"),
                    parent_id=app.get("parent_id"),
                    parent_article_type=app.get("parent_article_type"),
                    parent_lang=app.get("parent_lang"),
                    item="app-group",
                    sub_item="app",
                    validation_type="exist",
                    is_valid=True,
                    expected=app.get("id"),
                    obtained=app.get("id"),
                    advice=None,
                    data=app,
                    error_level=self.params["app_existence_error_level"],
                )
