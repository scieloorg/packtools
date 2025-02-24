from packtools.sps.models.funding_group import FundingGroup
from packtools.sps.validation.utils import build_response


def _callable_extern_validate_default(award_id):
    raise NotImplementedError


class FundingGroupValidation:
    """
    Validation class for funding information in XML documents.

    Parameters
    ----------
    xml_tree : lxml.etree.Element
        XML tree to validate
    params : dict
        Dictionary containing parameters for validation:
        - special_chars_award_id: List of special characters allowed in award IDs
        - error_level: Error level for validation messages ("ERROR" or "WARNING")
    """

    def __init__(self, xml_tree, params=None):
        self.xml_tree = xml_tree
        self.params = {
            "special_chars_award_id": ["/", ".", "-"],
            "error_level": "ERROR",
        }
        self.params.update(params or {})

        self.funding = FundingGroup(xml_tree, self.params)

    def validate_required_award_ids(self):
        """
        Validates the existence of funding sources and award IDs.

        Yields
        ------
        dict
            Validation results for each funding source and award ID.
        """
        funding_data = self.funding.data
        parent = {
            "parent": "article",
            "parent_id": None,
            "parent_article_type": funding_data.get("article_type"),
            "parent_lang": funding_data.get("article_lang"),
        }

        if bool(self.funding.award_ids):
            yield build_response(
                title="Funding information validation",
                parent=parent,
                item="award-group",
                sub_item="award-id",
                validation_type="exist",
                is_valid=True,
                expected="award-id and funding-source in award-group",
                obtained="Valid award-id and funding-source found",
                advice=None,
                data=None,
                error_level="INFO",
            )

        errors = []
        if items := self.funding.ack:
            for ack in items:
                for item in ack.get("p") or []:
                    if item.get("look-like-award-id"):
                        item["context"] = "ack"
                        errors.append(item)
        if items := self.funding.financial_disclosure:
            for item in items or []:
                if item.get("look-like-award-id"):
                    item["context"] = "fn[@fn-type='financial-disclosure']"
                    errors.append(item)
        if items := self.funding.supported_by:
            for item in items or []:
                if item.get("look-like-award-id"):
                    item["context"] = "fn[@fn-type='supported-by']"
                    errors.append(item)
        if funding_statement_data := self.funding.funding_statement_data:
            if funding_statement_data.get("look-like-award-id"):
                funding_statement_data["context"] = (
                    "funding-group/funding-statement"
                )
                errors.append(funding_statement_data)

        for error in errors:
            yield build_response(
                title="Required funding-group/award-group with award-id and funding-source",
                parent=parent,
                item="award-group",
                sub_item="award-id",
                validation_type="exist",
                is_valid=False,
                expected="award-id and funding-source in award-group",
                obtained=None,
                advice="If {} is a project contract number, make it with <award-id> and the corresponding financial "
                       "sponsors with <funding-source> in <funding-group>. Consult the SPS documentation "
                       "for more detail".format(error["look-like-award-id"]),
                data=error,
                error_level=self.params["error_level"],
            )

    def validate_funding_statement(self):
        """
        Validates if funding-related information from <ack>, <fn> (financial-disclosure or supported-by)
        is properly replicated in <funding-statement>.
        """
        funding_statement_text = self.funding.funding_statement_data.get(
            "text") if self.funding.funding_statement_data else ""
        parent = {
            "parent": "article",
            "parent_id": None,
            "parent_article_type": self.funding.data.get("article_type"),
            "parent_lang": self.funding.data.get("article_lang"),
        }

        errors = []
        sources = {
            "ack": self.funding.ack,
            "financial-disclosure": self.funding.financial_disclosure,
            "supported-by": self.funding.supported_by,
        }

        for context, items in sources.items():
            for item in items or []:
                for award_id in item.get("p") or []:
                    text = award_id.get("text").strip()
                    if text and text not in funding_statement_text:
                        errors.append({
                            "context": context,
                            "missing_text": text,
                        })

        if not errors:
            yield build_response(
                title="Funding statement validation",
                parent=parent,
                item="funding-statement",
                sub_item="text",
                validation_type="consistency",
                is_valid=True,
                expected="Text from <ack>, <fn> (financial-disclosure or supported-by) should be present in <funding-statement>",
                obtained="Funding statement correctly includes all necessary information.",
                advice=None,
                data=None,
                error_level="INFO",
            )
        else:
            for error in errors:
                yield build_response(
                    title="Missing funding information in funding-statement",
                    parent=parent,
                    item="funding-statement",
                    sub_item="text",
                    validation_type="consistency",
                    is_valid=False,
                    expected=f"Text from {error["context"]} should be present in <funding-statement>",
                    obtained=f"Missing text: '{error["missing_text"]}'",
                    advice=f"Ensure that funding information '{error["missing_text"]}' from {error['context']} is replicated in <funding-statement>.",
                    data=error,
                    error_level=self.params["error_level"],
                )
