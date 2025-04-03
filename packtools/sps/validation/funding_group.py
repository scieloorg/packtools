from packtools.sps.models.funding_group import FundingGroup
from packtools.sps.validation.utils import build_response
from packtools.sps.validation.similarity_utils import most_similar, similarity

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
            "award_id_error_level": "CRITICAL",
            "funding_statement_error_level": "CRITICAL"
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
        award_ids = None
        found_award_ids = set()
        for item in self.funding.award_groups:
            funding_sources = item["funding-source"]
            award_ids = item["award-id"]
            found_award_ids.update(award_ids)
            
            if funding_sources and award_ids:
                valid = True
                advice = None
            elif award_ids:
                valid = False
                advice = f'Mark the sponsor institution with <funding-source> for <award-id> ({award_ids}). Consult SPS documentation for more detail'
            elif funding_sources:
                valid = False
                advice = f'Mark the contract number with <award-id> for <funding-source> ({funding_sources}). Consult SPS documentation for more detail'
            else:
                valid = False
                advice = f'Mark the contract number with <award-id> and the funding institution with <funding-source> insider <award-group>. Consult SPS documentation for more detail'
            yield build_response(
                title="award-id and funding-source",
                parent=parent,
                item="award-group",
                sub_item="award-id",
                validation_type="exist",
                is_valid=valid,
                expected="award-id and funding-source in award-group",
                obtained=item,
                advice=advice,
                data=item,
                error_level=self.params["award_id_error_level"],
            )
        numbers = set()
        for item in self.funding.look_like_award_ids:
            numbers.update(item["look-like-award-id"])
        if numbers == found_award_ids:
            return
        for item in self.funding.look_like_award_ids:
            context = item["context"]
            text = item["text"]
            look_like_award_ids = set(item["look-like-award-id"])
            missing_items = look_like_award_ids - found_award_ids
            if not missing_items:
                continue
            for missing in missing_items:
                yield build_response(
                    title="Required funding-group/award-group with award-id and funding-source",
                    parent=parent,
                    item="award-group",
                    sub_item="award-id",
                    validation_type="exist",
                    is_valid=False,
                    expected="award-id and funding-source in award-group",
                    obtained=None,
                    advice=f"Found {missing} in {text} ({context}), if {missing} is a contract number, add <award-id>{missing}</award-id> and the corresponding funding institution with <funding-source> inside <award-group>. Consult the SPS documentation for more detail",
                    data=item,
                    error_level=self.params["award_id_error_level"],
                )

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
