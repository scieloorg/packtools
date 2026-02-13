from packtools.sps.models.fig import ArticleFigs
from packtools.sps.validation.utils import format_response, build_response


class ArticleFigValidation:
    def __init__(self, xml_tree, rules):
        self.xml_tree = xml_tree
        self.rules = rules
        self.article_types_requires = rules.get("article_types_requires", [])
        self.article_type = xml_tree.find(".").get("article-type")
        self.required = self.article_type in self.article_types_requires
        self.elements = list(ArticleFigs(xml_tree).get_all_figs)

    def validate(self):
        if self.elements:
            for element in self.elements:
                yield from FigValidation(element, self.rules).validate()
        elif self.required:
            yield format_response(
                title="fig presence",
                parent="article",
                parent_id=None,
                parent_article_type=self.article_type,
                parent_lang=self.xml_tree.get(
                    "{http://www.w3.org/XML/1998/namespace}lang"
                ),
                item="fig",
                sub_item=None,
                validation_type="exist",
                is_valid=False,
                expected="<fig>",
                obtained=None,
                advice=f'article-type={self.article_type} requires <fig>. Found 0. Identify the fig or check if article-type is correct',
                data=None,
                error_level=self.rules.get("absent_error_level", "WARNING"),
            )


class FigValidation:
    def __init__(self, data, rules):
        self.data = data
        self.rules = self.get_default_params()
        self.rules.update(rules or {})

    def get_default_params(self):
        return {
            "absent_error_level": "WARNING",
            "id_error_level": "CRITICAL",
            "graphic_error_level": "CRITICAL",
            "xlink_href_error_level": "CRITICAL",
            "file_extension_error_level": "ERROR",
            "fig_type_error_level": "ERROR",
            "xml_lang_in_fig_group_error_level": "ERROR",
            "accessibility_error_level": "WARNING",
            "alt_text_length_error_level": "WARNING",
            "allowed_file_extensions": ["jpg", "jpeg", "png", "tif", "tiff"],
            "allowed_fig_types": ["graphic", "chart", "diagram", "drawing", "illustration", "map"],
            "alt_text_max_length": 120,
            "article_types_requires": []
        }

    def validate(self):
        # P0 - Critical: Rule 1 - Validate @id presence
        yield self.validate_id()
        
        # P0 - Critical: Rule 2 - Validate <graphic> presence
        yield self.validate_graphic()
        
        # P0 - Critical: Rule 3 - Validate @xlink:href in <graphic>
        yield self.validate_xlink_href()
        
        # P0 - ERROR: Rule 4 - Validate file extension
        yield self.validate_file_extension()
        
        # P0 - ERROR: Rule 5 - Validate @fig-type values (only if present)
        if self.data.get("type"):
            yield self.validate_fig_type()
        
        # P1 - ERROR: Rule 6 - Validate @xml:lang in fig-group (only if in fig-group)
        if self.data.get("parent_name") == "fig-group":
            yield self.validate_xml_lang_in_fig_group()
        
        # P1 - WARNING: Rule 7 - Validate accessibility (alt-text or long-desc)
        yield self.validate_accessibility()
        
        # P1 - WARNING: Rule 8 - Validate alt-text length (only if alt-text present)
        if self.data.get("graphic_alt_text"):
            yield self.validate_alt_text_length()

    def validate_id(self):
        """Rule 1: Validate presence of @id (CRITICAL)"""
        obtained = self.data.get("id")
        is_valid = bool(obtained)
        return build_response(
            title="@id",
            parent=self.data,
            item="fig",
            sub_item="@id",
            validation_type="exist",
            is_valid=is_valid,
            expected="@id attribute",
            obtained=obtained,
            advice='Add @id attribute to <fig>. Example: <fig id="f01">. The @id attribute is mandatory.',
            data=self.data,
            error_level=self.rules["id_error_level"],
        )

    def validate_graphic(self):
        """Rule 2: Validate presence of <graphic> (CRITICAL)"""
        obtained = self.data.get("graphic")
        is_valid = bool(obtained)
        return build_response(
            title="<graphic>",
            parent=self.data,
            item="fig",
            sub_item="graphic",
            validation_type="exist",
            is_valid=is_valid,
            expected="<graphic> element",
            obtained=obtained,
            advice='Add <graphic> element inside <fig>. Example: <graphic xlink:href="image.jpg"/>. Every <fig> must contain at least one <graphic> element.',
            data=self.data,
            error_level=self.rules["graphic_error_level"],
        )

    def validate_xlink_href(self):
        """Rule 3: Validate @xlink:href in <graphic> (CRITICAL)"""
        graphic = self.data.get("graphic")
        is_valid = bool(graphic)
        return build_response(
            title="@xlink:href",
            parent=self.data,
            item="fig",
            sub_item="@xlink:href",
            validation_type="exist",
            is_valid=is_valid,
            expected="@xlink:href attribute in <graphic>",
            obtained=graphic,
            advice='Add @xlink:href attribute to <graphic>. Example: <graphic xlink:href="image.jpg"/>. The @xlink:href attribute is mandatory in <graphic>.',
            data=self.data,
            error_level=self.rules["xlink_href_error_level"],
        )

    def validate_file_extension(self):
        """Rule 4: Validate file extension (ERROR)"""
        file_extension = self.data.get("file_extension")
        graphic_href = self.data.get("graphic")
        allowed_extensions = self.rules["allowed_file_extensions"]
        alternative_elements = self.data.get("alternative_elements", [])
        
        # Check if file is SVG and if it's inside alternatives
        is_svg = file_extension == "svg"
        is_in_alternatives = len(alternative_elements) > 0
        
        # SVG is only allowed inside alternatives
        if is_svg:
            is_valid = is_in_alternatives
            if not is_valid:
                advice = f'SVG files are only allowed inside <alternatives>. Either use a different format ({", ".join(allowed_extensions)}) or wrap the graphic in <alternatives>.'
            else:
                advice = None
        else:
            is_valid = file_extension in allowed_extensions if file_extension else False
            if file_extension and not is_valid:
                advice = f'File extension "{file_extension}" is not allowed. Use one of: {", ".join(allowed_extensions)}. If using SVG, it must be inside <alternatives>.'
            elif not file_extension:
                advice = f'File "{graphic_href}" must have a valid extension. Allowed: {", ".join(allowed_extensions)}. SVG is only allowed inside <alternatives>.'
            else:
                advice = None
        
        return build_response(
            title="file extension",
            parent=self.data,
            item="fig",
            sub_item="file extension",
            validation_type="value in list",
            is_valid=is_valid,
            expected=f'{", ".join(allowed_extensions)} (.svg only in <alternatives>)',
            obtained=file_extension,
            advice=advice,
            data=self.data,
            error_level=self.rules["file_extension_error_level"],
        )

    def validate_fig_type(self):
        """Rule 5: Validate @fig-type values (ERROR)"""
        fig_type = self.data.get("type")
        allowed_types = self.rules["allowed_fig_types"]
        is_valid = fig_type in allowed_types
        
        return build_response(
            title="@fig-type",
            parent=self.data,
            item="fig",
            sub_item="@fig-type",
            validation_type="value in list",
            is_valid=is_valid,
            expected=f'one of {allowed_types}',
            obtained=fig_type,
            advice=f'Invalid @fig-type value "{fig_type}". Use one of: {", ".join(allowed_types)}.',
            data=self.data,
            error_level=self.rules["fig_type_error_level"],
        )

    def validate_xml_lang_in_fig_group(self):
        """Rule 6: Validate @xml:lang in <fig> inside <fig-group> (ERROR)"""
        xml_lang = self.data.get("xml_lang")
        is_valid = bool(xml_lang)
        
        return build_response(
            title="@xml:lang in fig-group",
            parent=self.data,
            item="fig",
            sub_item="@xml:lang",
            validation_type="exist",
            is_valid=is_valid,
            expected="@xml:lang attribute",
            obtained=xml_lang,
            advice='When <fig> is inside <fig-group>, the @xml:lang attribute is mandatory. Add xml:lang attribute to <fig>. Example: <fig xml:lang="en">.',
            data=self.data,
            error_level=self.rules["xml_lang_in_fig_group_error_level"],
        )

    def validate_accessibility(self):
        """Rule 7: Validate presence of alt-text or long-desc (WARNING)"""
        alt_text = self.data.get("graphic_alt_text")
        long_desc = self.data.get("graphic_long_desc")
        has_accessibility = bool(alt_text or long_desc)
        
        return build_response(
            title="accessibility",
            parent=self.data,
            item="fig",
            sub_item="alt-text or long-desc",
            validation_type="exist",
            is_valid=has_accessibility,
            expected="<alt-text> or <long-desc>",
            obtained="present" if has_accessibility else None,
            advice='For accessibility, add <alt-text> or <long-desc> inside <graphic>. Example: <graphic xlink:href="image.jpg"><alt-text>Brief description</alt-text></graphic>.',
            data=self.data,
            error_level=self.rules["accessibility_error_level"],
        )

    def validate_alt_text_length(self):
        """Rule 8: Validate alt-text character limit (WARNING)"""
        alt_text = self.data.get("graphic_alt_text")
        max_length = self.rules["alt_text_max_length"]
        current_length = len(alt_text)
        is_valid = current_length <= max_length
        
        return build_response(
            title="alt-text length",
            parent=self.data,
            item="fig",
            sub_item="alt-text length",
            validation_type="format",
            is_valid=is_valid,
            expected=f"≤ {max_length} characters",
            obtained=f"{current_length} characters",
            advice=f'The <alt-text> content has {current_length} characters, exceeding the recommended maximum of {max_length}. Please shorten the description.',
            data=self.data,
            error_level=self.rules["alt_text_length_error_level"],
        )

