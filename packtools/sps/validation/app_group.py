import gettext

from packtools.sps.models.app_group import XmlAppGroup
from packtools.sps.validation.utils import build_response

_ = gettext.gettext


class AppValidation:
    def __init__(self, xmltree, params):
        self.xmltree = xmltree
        self.apps = list(XmlAppGroup(xmltree).data)
        self.params = params

    def validate(self):
        yield from self.validate_app_existence()

    def validate_app_existence(self):
        if not self.apps:
            advice = "Consider adding an <app> element to include additional content such as supplementary materials or appendices."
            advice_text = _(
                "Consider adding an <app> element to include additional content such as supplementary materials or appendices."
            )
            advice_params = {}
            
            parent_data = {
                "parent": "article",
                "parent_id": None,
                "parent_article_type": self.xmltree.get("article-type"),
                "parent_lang": self.xmltree.get(
                    "{http://www.w3.org/XML/1998/namespace}lang"
                ),
            }
            
            yield build_response(
                title="<app>",
                parent=parent_data,
                item="app-group",
                sub_item="app",
                validation_type="exist",
                is_valid=False,
                expected="<app> element",
                obtained=None,
                advice=advice,
                data=None,
                error_level=self.params["app_existence_error_level"],
                advice_text=advice_text,
                advice_params=advice_params,
            )
        else:
            for app in self.apps:
                yield build_response(
                    title="<app>",
                    parent=app,
                    item="app-group",
                    sub_item="app",
                    validation_type="exist",
                    is_valid=True,
                    expected=app.get("id"),
                    obtained=app.get("id"),
                    advice=None,
                    data=app,
                    error_level=self.params["app_existence_error_level"],
                    advice_text=None,
                    advice_params=None,
                )
