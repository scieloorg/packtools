from packtools.sps.models.list import ArticleLists
from packtools.sps.validation.utils import build_response


class ArticleListValidation:
    def __init__(self, xml_tree, rules):
        self.xml_tree = xml_tree
        self.rules = rules
        self.elements = list(ArticleLists(xml_tree).get_all_lists)

    def validate(self):
        if self.elements:
            for element in self.elements:
                yield from ListValidation(element, self.rules).validate()


class ListValidation:
    def __init__(self, data, rules):
        self.data = data
        self.rules = self.get_default_params()
        self.rules.update(rules or {})

    def get_default_params(self):
        return {
            "list_type_presence_error_level": "CRITICAL",
            "list_type_value_error_level": "ERROR",
            "min_list_items_error_level": "ERROR",
            "label_in_list_item_error_level": "WARNING",
            "empty_list_item_error_level": "WARNING",
            "missing_title_error_level": "INFO",
            "allowed_list_types": [
                "order",
                "bullet",
                "alpha-lower",
                "alpha-upper",
                "roman-lower",
                "roman-upper",
                "simple",
            ],
            "min_list_items": 2,
        }

    def validate(self):
        yield from self.validate_list_type_presence()
        yield from self.validate_list_type_value()
        yield from self.validate_min_list_items()
        yield from self.validate_no_label_in_list_items()
        yield from self.validate_list_items_have_content()
        yield from self.validate_title_recommendation()

    def validate_list_type_presence(self):
        """
        P0 - Rule 1: Validate presence of @list-type attribute (CRITICAL)
        """
        list_type = self.data.get("list_type")
        is_valid = list_type is not None and list_type != ""
        
        if list_type is None:
            obtained = None
            advice = "Add list-type attribute to <list> element. Use one of: order, bullet, alpha-lower, alpha-upper, roman-lower, roman-upper, simple"
        elif list_type == "":
            obtained = '""'
            advice = "The @list-type attribute cannot be empty. Use one of: order, bullet, alpha-lower, alpha-upper, roman-lower, roman-upper, simple"
        else:
            obtained = list_type
            advice = None

        yield build_response(
            title="@list-type presence",
            parent=self.data,
            item="list",
            sub_item="@list-type",
            validation_type="exist",
            is_valid=is_valid,
            expected="@list-type",
            obtained=obtained,
            advice=advice,
            data=self.data,
            error_level=self.rules["list_type_presence_error_level"],
        )

    def validate_list_type_value(self):
        """
        P0 - Rule 2: Validate allowed values of @list-type (ERROR)
        """
        list_type = self.data.get("list_type")
        allowed_list_types = self.rules["allowed_list_types"]
        
        # Only validate value if list_type is present and not empty
        if list_type:
            is_valid = list_type in allowed_list_types
            
            if not is_valid:
                advice = f'Value "{list_type}" is not allowed for @list-type. Use one of: {", ".join(allowed_list_types)}'
            else:
                advice = None

            yield build_response(
                title="@list-type value",
                parent=self.data,
                item="list",
                sub_item="@list-type",
                validation_type="value in list",
                is_valid=is_valid,
                expected=allowed_list_types,
                obtained=list_type,
                advice=advice,
                data=self.data,
                error_level=self.rules["list_type_value_error_level"],
            )

    def validate_min_list_items(self):
        """
        P0 - Rule 3: Validate minimum presence of <list-item> (ERROR)
        """
        list_items_count = self.data.get("list_items_count", 0)
        min_items = self.rules["min_list_items"]
        is_valid = list_items_count >= min_items

        if not is_valid:
            advice = f"<list> must contain at least {min_items} <list-item> elements. Found {list_items_count}"
        else:
            advice = None

        yield build_response(
            title="minimum list items",
            parent=self.data,
            item="list",
            sub_item="list-item count",
            validation_type="exist",
            is_valid=is_valid,
            expected=f"at least {min_items} list-item elements",
            obtained=f"{list_items_count} list-item elements",
            advice=advice,
            data=self.data,
            error_level=self.rules["min_list_items_error_level"],
        )

    def validate_no_label_in_list_items(self):
        """
        P0 - Rule 4: Validate absence of <label> in <list-item> (WARNING)
        """
        has_label = self.data.get("has_label_in_items", False)
        is_valid = not has_label

        if not is_valid:
            advice = "For accessibility, do not use <label> in <list-item>. The @list-type attribute generates labels automatically"
        else:
            advice = None

        yield build_response(
            title="no label in list-item",
            parent=self.data,
            item="list",
            sub_item="label",
            validation_type="exist",
            is_valid=is_valid,
            expected="no <label> in <list-item>",
            obtained="<label> found in <list-item>" if has_label else "no <label>",
            advice=advice,
            data=self.data,
            error_level=self.rules["label_in_list_item_error_level"],
        )

    def validate_list_items_have_content(self):
        """
        P1 - Rule 5: Validate that each <list-item> has content (WARNING)
        """
        empty_count = self.data.get("empty_list_items_count", 0)
        is_valid = empty_count == 0

        if not is_valid:
            advice = f"Found {empty_count} empty <list-item> element(s). Each <list-item> should contain at least one child element (typically <p>)"
        else:
            advice = None

        yield build_response(
            title="list-item has content",
            parent=self.data,
            item="list",
            sub_item="list-item content",
            validation_type="exist",
            is_valid=is_valid,
            expected="all list-item elements with content",
            obtained=f"{empty_count} empty list-item(s)" if not is_valid else "all list-items have content",
            advice=advice,
            data=self.data,
            error_level=self.rules["empty_list_item_error_level"],
        )

    def validate_title_recommendation(self):
        """
        P1 - Rule 6: Recommend use of <title> when appropriate (INFO)
        """
        title = self.data.get("title")
        has_title = title is not None and title.strip() != ""
        is_valid = True  # This is just a recommendation, not a strict requirement

        if not has_title:
            advice = "Consider adding a <title> element if the list has a descriptive heading"
        else:
            advice = None

        yield build_response(
            title="list title recommendation",
            parent=self.data,
            item="list",
            sub_item="title",
            validation_type="exist",
            is_valid=is_valid,
            expected="<title> when list has a descriptive heading",
            obtained="<title> present" if has_title else "no <title>",
            advice=advice,
            data=self.data,
            error_level=self.rules["missing_title_error_level"],
        )
