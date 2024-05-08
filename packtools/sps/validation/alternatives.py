from packtools.sps.models.alternatives import ArticleAlternatives
from packtools.sps.validation.utils import format_response
from packtools.sps.validation.exceptions import ValidationAlternativesException


class AlternativeValidation:
    def __init__(self, alternative, children_list):
        self.alternative = alternative
        self.obtained_children = alternative.get("alternative_children")
        self.children_list = children_list


    def validate_children(self):
        for tag in self.obtained_children:
            if tag not in (self.parent_children_dict.get(self.obtained_parent) or []):
                yield self.create_validation_response(
                    expected=self.parent_children_dict.get(self.obtained_parent),
                    obtained=self.obtained_children,
                    advice=f"Provide child tags according to the list: {self.parent_children_dict.get(self.obtained_parent)}"
                )

    def create_validation_response(self, expected, obtained, advice):
        return format_response(
            title="Alternatives validation",
            parent=self.alternative.get("parent"),
            parent_id=self.alternative.get("parent_id"),
            item=self.obtained_parent,
            sub_item="alternatives",
            validation_type="value in list",
            is_valid=False,
            expected=expected,
            obtained=obtained,
            advice=advice,
            data=self.alternative
        )

    def validation(self):
        yield from self.validate_parent()
        yield from self.validate_children()


class AlternativesValidation:
    def __init__(self, xmltree, parent_children_dict=None):
        self.xmltree = xmltree
        self.parent_children_dict = parent_children_dict
        self.alternatives = ArticleAlternatives(xmltree).alternatives()

    def validation(self, parent_children_dict=None):
        parent_children_dict = parent_children_dict or self.parent_children_dict
        if not parent_children_dict:
            raise ValidationAlternativesException("Function requires dict of parent tag (key) and child tags list (value)")
        for alternative in self.alternatives:
            parent = alternative.get("alternative_parent")
            children_list = parent_children_dict.get(parent)
            if children_list is None:
                raise ValidationAlternativesException(f"Tag {parent} is not provided in the function parameters")
            yield from AlternativeValidation(alternative, children_list).validation()


