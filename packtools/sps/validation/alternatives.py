from packtools.sps.models.alternatives import Alternatives
from packtools.sps.validation.utils import ALTERNATIVES, format_response


class AlternativesValidation:
    def __init__(self, xmltree):
        self.xmltree = xmltree
        self.alternatives = list(Alternatives(xmltree).alternatives)

    def validation(self):
        for alternative in self.alternatives:
            alternative_parent = alternative.get("alternative_parent")
            alternative_children = alternative.get("alternative_children")
            for tag in alternative_children:
                if tag not in ALTERNATIVES.get(alternative_parent):
                    yield format_response(
                        title="Alternatives validation",
                        parent=alternative.get("parent"),
                        parent_id=alternative.get("parent_id"),
                        item=alternative_parent,
                        sub_item="alternative",
                        validation_type="match",
                        is_valid=False,
                        expected=ALTERNATIVES.get(alternative_parent),
                        obtained=alternative_children,
                        advice=f"Provide child tags according to the list: {ALTERNATIVES.get(alternative_parent)}",
                        data=alternative
                    )


