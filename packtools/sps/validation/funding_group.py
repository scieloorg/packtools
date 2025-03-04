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

    def validate_funding_statement(self):
        """
        Validates the existence of funding sources and award IDs.

        Yields
        ------
        dict
            Validation results for each funding source and award ID.
        """
        if self.funding.award_groups:
            for lang, statements in self.funding.statements_by_lang.items():
                parent_id = statements.get("parent_id")
                xml = f'<sub-article id="{parent_id}">' if parent_id else "<article>"
                advice = None
                funding_statement = statements["funding_statement"]
                items = {k: v for k, v in statements["texts"].items() if v}
                texts = []
                valid = False
                if items:
                    texts = list(items.values())

                if funding_statement and texts:
                    best_score, best_matches = most_similar(similarity(texts, funding_statement, 0.8))

                    if best_matches:
                        valid = True
                    else:
                        valid = False
                        advice = f'Replace <funding-statement>{funding_statement}</funding-statement> by <funding-statement>{texts[0]}</funding-statement> for {xml}'
                elif texts:
                    valid = False
                    advice = f'Add <funding-statement>{texts[0]}</funding-statement> in <funding-group> for {xml}. Consult SPS documentation for more detail'
                else:
                    valid = False
                    advice = f'Add funding statement with <funding-statement> inside <funding-group> for {xml}. Consult SPS documentation for more detail'

                yield build_response(
                    title="funding-statement",
                    parent=statements,
                    item="funding-statement",
                    sub_item=None,
                    validation_type="match",
                    is_valid=valid,
                    expected="funding-statement",
                    obtained=statements,
                    advice=advice,
                    data=statements,
                    error_level=self.params["funding_statement_error_level"],
                )
