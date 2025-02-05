from packtools.sps.models.fig import ArticleFigs
from packtools.sps.validation.utils import format_response, build_response


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
            # fig is absent
            if self.required:
                yield format_response(
                    title="fig presence",
                    parent="article",
                    parent_id=None,
                    parent_article_type=self.xml_tree.get("article-type"),
                    parent_lang=self.xml_tree.get(
                        "{http://www.w3.org/XML/1998/namespace}lang"
                    ),
                    item="fig",
                    sub_item=None,
                    validation_type="exist",
                    is_valid=False,
                    expected="<fig/>",
                    obtained=None,
                    advice=f"article-type={self.article_type} requires <fig/>. Found 0. Identify the fig or check if article-type is correct",
                    data=None,
                    error_level=self.rules["required_error_level"],
                )
            else:
                yield format_response(
                    title="fig presence",
                    parent="article",
                    parent_id=None,
                    parent_article_type=self.xml_tree.get("article-type"),
                    parent_lang=self.xml_tree.get(
                        "{http://www.w3.org/XML/1998/namespace}lang"
                    ),
                    item="fig",
                    sub_item=None,
                    validation_type="exist",
                    is_valid=False,
                    expected=None,
                    obtained=None,
                    advice=f"article-type={self.article_type}, found 0 figures",
                    data=None,
                    error_level=self.rules["absent_error_level"],
                )


class FigValidation:
    def __init__(self, data, rules):
        self.data = data
        self.rules = rules

    def validate(self):
        yield from self._validate_item("id")
        yield from self._validate_item("label")
        yield from self._validate_item("caption")
        yield from self.validate_content()
        yield from self.validate_file_extension()

    def _validate_item(self, name):
        if not self.data.get(name):
            key_error_level = f"{name}_error_level"
            yield build_response(
                title=name,
                parent=self.data,
                item="fig",
                sub_item=name,
                validation_type="exist",
                is_valid=False,
                expected=name,
                obtained=None,
                advice=f"Identify the {name}",
                data=self.data,
                error_level=self.rules[key_error_level],
            )

    def validate_content(self):
        if not self.data.get("graphic") and not self.data.get("alternatives"):
            name = "graphic or alternatives"
            yield build_response(
                title=name,
                parent=self.data,
                item="fig",
                sub_item=name,
                validation_type="exist",
                is_valid=False,
                expected=name,
                obtained=None,
                advice=f"Identify the {name}",
                data=self.data,
                error_level=self.rules["content_error_level"],
            )

    def validate_file_extension(self):
        file_extension = self.data.get("file_extension")
        allowed_file_extensions = self.rules["allowed file extensions"]
        if file_extension not in allowed_file_extensions:
            yield build_response(
                title="file extension",
                parent=self.data,
                item="fig",
                sub_item="file extension",
                validation_type="value in list",
                is_valid=False,
                expected=allowed_file_extensions,
                obtained=file_extension,
                advice=f"provide a file with one of the following extensions {allowed_file_extensions}",
                data=self.data,
                error_level=self.rules["file_extension_error_level"],
            )
