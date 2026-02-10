import gettext

from packtools.sps.models.fig import ArticleFigs
from packtools.sps.validation.utils import build_response

_ = gettext.gettext


class ArticleFigValidation:
    def __init__(self, xml_tree, rules):
        self.xml_tree = xml_tree
        self.rules = rules
        self.article_types_requires = rules["article_types_requires"]
        self.article_type = xml_tree.find(".").get("article-type")
        self.required = self.article_type in self.article_types_requires
        self.elements = list(ArticleFigs(xml_tree).get_all_figs)

    def validate(self):
        if self.elements:
            for element in self.elements:
                yield from FigValidation(element, self.rules).validate()

        else:
            advice = f'({self.article_type}) No <fig> found in XML'
            advice_text = _('({article_type}) No <fig> found in XML')
            advice_params = {
                "article_type": self.article_type
            }
            
            parent_data = {
                "parent": "article",
                "parent_id": None,
                "parent_article_type": self.xml_tree.get("article-type"),
                "parent_lang": self.xml_tree.get(
                    "{http://www.w3.org/XML/1998/namespace}lang"
                ),
            }
            
            yield build_response(
                title="fig presence",
                parent=parent_data,
                item="fig",
                sub_item=None,
                validation_type="exist",
                is_valid=False,
                expected="<fig>",
                obtained=None,
                advice=advice,
                data=None,
                error_level=self.rules["absent_error_level"],
                advice_text=advice_text,
                advice_params=advice_params,
            )


class FigValidation:
    def __init__(self, data, rules):
        self.data = data
        self.rules = self.get_default_params()
        self.rules.update(rules or {})

    def get_default_params(self):
        return {
            "alternatives_error_level": "CRITICAL",
            "error_level": "WARNING",
            "required_error_level": "CRITICAL",
            "absent_error_level": "WARNING",
            "id_error_level": "CRITICAL",
            "label_error_level": "CRITICAL",
            "caption_error_level": "CRITICAL",
            "content_error_level": "CRITICAL",
            "file_extension_error_level": "CRITICAL",
            "allowed file extensions": ["tif", "jpg", "png", "svg"]
        }

    def validate(self):
        yield from self._validate_item("id")
        yield from self._validate_item("label")
        yield from self._validate_item("caption")
        yield from self.validate_content()
        yield from self.validate_file_extension()

    def _validate_item(self, name):
        obtained = self.data.get(name)
        is_valid = bool(obtained)
        key_error_level = f"{name}_error_level"
        advice = f'Mark each figure {name} inside <body> using <fig><{name}>. Consult SPS documentation for more detail.'
        yield build_response(
            title=name,
            parent=self.data,
            item="fig",
            sub_item=name,
            validation_type="exist",
            is_valid=is_valid,
            expected=name,
            obtained=obtained,
            advice=advice,
            data=self.data,
            error_level=self.rules[key_error_level],
        )

    def validate_content(self):
        is_valid = bool(self.data.get("graphic") or self.data.get("alternatives"))
        name = "graphic or alternatives"
        yield build_response(
            title=name,
            parent=self.data,
            item="fig",
            sub_item=name,
            validation_type="exist",
            is_valid=is_valid,
            expected=name,
            obtained=None,
            advice='Ensure that the figure contains either <graphic> or <alternatives> inside <fig>. Consult SPS documentation for more detail.',
            data=self.data,
            error_level=self.rules["content_error_level"],
        )

    def validate_file_extension(self):
        file_extension = self.data.get("file_extension")
        file_path = self.data.get('graphic')
        allowed_file_extensions = self.rules["allowed file extensions"]
        is_valid = file_extension in allowed_file_extensions
        if file_extension:
            advice = f'In <fig><graphic xlink:href="{file_path}"/> replace {file_extension} with one of {allowed_file_extensions}'
        else:
            advice = f'In <fig><graphic xlink:href="{file_path}"/> specify a valid file extension from: {allowed_file_extensions}'
        yield build_response(
            title="file extension",
            parent=self.data,
            item="fig",
            sub_item="file extension",
            validation_type="value in list",
            is_valid=is_valid,
            expected=allowed_file_extensions,
            obtained=file_extension,
            advice=advice,
            data=self.data,
            error_level=self.rules["file_extension_error_level"],
        )
