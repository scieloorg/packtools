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
                advice="Found `{}` in `{}` ({}). Verify if this refers to a project contract. "
                       "If so, add the award ID (`{}`) inside `<funding-group><award-group>`, "
                       "ensuring it includes the corresponding `<funding-source>`.".format(
                    error["look-like-award-id"],
                    error["text"],
                    error["context"],
                    error["look-like-award-id"]),
                data=error,
                error_level=self.params["error_level"],
            )
