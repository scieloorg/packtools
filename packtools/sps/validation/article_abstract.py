from packtools.sps.models.article_abstract import VisualAbstracts, Highlights
from packtools.sps.validation.utils import format_response


class HighlightsValidation:
    def __init__(self, xmltree):
        self.highlights = list(Highlights(xmltree).highlights)

    def highlight_validation(self, response_type_for_absent=None):
        if not self.highlights:
            resp = format_response(
                title="Article highlights validation",
                parent=None,
                parent_id=None,
                item="abstract",
                sub_item='@abstract-type="key-points"',
                validation_type="exist",
                is_valid=False,
                expected="article highlights",
                obtained=None,
                advice=None,
                data=None
            )
            if response_type_for_absent is not None:
                resp["response"] = response_type_for_absent
            yield resp
        else:
            for highlight in self.highlights:
                yield format_response(
                    title="Article highlights validation",
                    parent=highlight.get("parent"),
                    parent_id=highlight.get("parent_id"),
                    item="abstract",
                    sub_item='@abstract-type="key-points"',
                    validation_type="exist",
                    is_valid=True,
                    expected=highlight.get("highlights"),
                    obtained=highlight.get("highlights"),
                    advice=None,
                    data=highlight
                )


class VisualAbstractsValidation:
    def __init__(self, xmltree):
        self.visual_abstracts = list(VisualAbstracts(xmltree).visual_abstracts)

    def visual_abstracts_validation(self, response_type_for_absent=None):
        if not self.visual_abstracts:
            resp = format_response(
                title="Article visual abstracts validation",
                parent=None,
                parent_id=None,
                item="abstract",
                sub_item='@abstract-type="graphical"',
                validation_type="exist",
                is_valid=False,
                expected="article visual abstracts",
                obtained=None,
                advice=None,
                data=None
            )
            if response_type_for_absent is not None:
                resp["response"] = response_type_for_absent
            yield resp
        else:
            for visual_abstract in self.visual_abstracts:
                yield format_response(
                    title="Article visual abstracts validation",
                    parent=visual_abstract.get("parent"),
                    parent_id=visual_abstract.get("parent_id"),
                    item="abstract",
                    sub_item='@abstract-type="graphical"',
                    validation_type="exist",
                    is_valid=True,
                    expected=visual_abstract.get("graphic"),
                    obtained=visual_abstract.get("graphic"),
                    advice=None,
                    data=visual_abstract
                )
