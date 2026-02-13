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

    def validate_funding_group_uniqueness(self, error_level="ERROR"):
        """
        Rule 1: Validates that <funding-group> appears at most once in <article-meta>.
        
        According to SPS 1.10, only one <funding-group> is allowed per <article-meta>.
        
        Params
        ------
        error_level : str, optional
            The severity level of the validation error, by default "ERROR".
        
        Yields
        ------
        dict
            Validation result for funding-group uniqueness.
        """
        funding_groups = self.xml_tree.xpath(".//article-meta/funding-group")
        count = len(funding_groups)
        
        funding_data = self.funding.data
        parent = {
            "parent": "article",
            "parent_id": None,
            "parent_article_type": funding_data.get("article_type"),
            "parent_lang": funding_data.get("article_lang"),
        }
        
        is_valid = count <= 1
        advice = None
        if not is_valid:
            advice = f"Found {count} <funding-group> elements in <article-meta>. Only one is allowed. Merge them into a single <funding-group>."
        
        yield build_response(
            title="funding-group uniqueness",
            parent=parent,
            item="funding-group",
            sub_item=None,
            validation_type="unique",
            is_valid=is_valid,
            expected="At most one <funding-group> in <article-meta>",
            obtained=f"{count} <funding-group> element(s) found",
            advice=advice,
            data={"count": count},
            error_level=error_level,
        )

    def validate_funding_statement_presence(self, error_level="CRITICAL"):
        """
        Rule 2: Validates that <funding-statement> is present in <funding-group>.
        
        According to SPS 1.10, <funding-statement> is mandatory in all cases.
        
        Params
        ------
        error_level : str, optional
            The severity level of the validation error, by default "CRITICAL".
        
        Yields
        ------
        dict
            Validation result for funding-statement presence.
        """
        funding_groups = self.xml_tree.xpath(".//article-meta/funding-group")
        
        if not funding_groups:
            # No funding-group means no validation needed
            return
        
        funding_data = self.funding.data
        parent = {
            "parent": "article",
            "parent_id": None,
            "parent_article_type": funding_data.get("article_type"),
            "parent_lang": funding_data.get("article_lang"),
        }
        
        funding_statement = self.funding.funding_statement
        is_valid = funding_statement is not None
        
        advice = None
        if not is_valid:
            advice = "Add <funding-statement> element inside <funding-group>. It is mandatory according to SPS 1.10."
        
        yield build_response(
            title="funding-statement presence",
            parent=parent,
            item="funding-statement",
            sub_item=None,
            validation_type="exist",
            is_valid=is_valid,
            expected="<funding-statement> present in <funding-group>",
            obtained=funding_statement if funding_statement else "None",
            advice=advice,
            data={"funding_statement": funding_statement},
            error_level=error_level,
        )

    def validate_funding_source_in_award_group(self, error_level="CRITICAL"):
        """
        Rule 3: Validates that <funding-source> is present when <award-group> exists.
        
        According to SPS 1.10, when there are institutions declared via <award-group>,
        <funding-source> is mandatory.
        
        Params
        ------
        error_level : str, optional
            The severity level of the validation error, by default "CRITICAL".
        
        Yields
        ------
        dict
            Validation results for each award-group.
        """
        funding_data = self.funding.data
        parent = {
            "parent": "article",
            "parent_id": None,
            "parent_article_type": funding_data.get("article_type"),
            "parent_lang": funding_data.get("article_lang"),
        }
        
        for item in self.funding.award_groups:
            funding_sources = item["funding-source"]
            
            is_valid = len(funding_sources) > 0
            advice = None
            if not is_valid:
                advice = "Add at least one <funding-source> element inside this <award-group>. It is mandatory when <award-group> exists."
            
            yield build_response(
                title="funding-source in award-group",
                parent=parent,
                item="award-group",
                sub_item="funding-source",
                validation_type="exist",
                is_valid=is_valid,
                expected="At least one <funding-source> in <award-group>",
                obtained=f"{len(funding_sources)} <funding-source> element(s) found",
                advice=advice,
                data=item,
                error_level=error_level,
            )

    def validate_label_absence(self, error_level="ERROR"):
        """
        Rule 5: Validates that <label> is not present in <funding-group> or its descendants.
        
        According to SPS 1.10, <label> is not allowed inside <funding-group>.
        
        Params
        ------
        error_level : str, optional
            The severity level of the validation error, by default "ERROR".
        
        Yields
        ------
        dict
            Validation result for label absence.
        """
        labels = self.xml_tree.xpath(".//funding-group//label")
        count = len(labels)
        
        funding_data = self.funding.data
        parent = {
            "parent": "article",
            "parent_id": None,
            "parent_article_type": funding_data.get("article_type"),
            "parent_lang": funding_data.get("article_lang"),
        }
        
        is_valid = count == 0
        advice = None
        if not is_valid:
            advice = f"Remove {count} <label> element(s) from <funding-group>. <label> is not allowed according to SPS 1.10."
        
        yield build_response(
            title="label absence in funding-group",
            parent=parent,
            item="funding-group",
            sub_item="label",
            validation_type="forbidden",
            is_valid=is_valid,
            expected="No <label> elements in <funding-group>",
            obtained=f"{count} <label> element(s) found",
            advice=advice,
            data={"count": count, "labels": [label.text for label in labels]},
            error_level=error_level,
        )

    def validate_title_absence(self, error_level="ERROR"):
        """
        Rule 6: Validates that <title> is not present in <funding-group> or its descendants.
        
        According to SPS 1.10, <title> is not allowed inside <funding-group>.
        
        Params
        ------
        error_level : str, optional
            The severity level of the validation error, by default "ERROR".
        
        Yields
        ------
        dict
            Validation result for title absence.
        """
        titles = self.xml_tree.xpath(".//funding-group//title")
        count = len(titles)
        
        funding_data = self.funding.data
        parent = {
            "parent": "article",
            "parent_id": None,
            "parent_article_type": funding_data.get("article_type"),
            "parent_lang": funding_data.get("article_lang"),
        }
        
        is_valid = count == 0
        advice = None
        if not is_valid:
            advice = f"Remove {count} <title> element(s) from <funding-group>. <title> is not allowed according to SPS 1.10."
        
        yield build_response(
            title="title absence in funding-group",
            parent=parent,
            item="funding-group",
            sub_item="title",
            validation_type="forbidden",
            is_valid=is_valid,
            expected="No <title> elements in <funding-group>",
            obtained=f"{count} <title> element(s) found",
            advice=advice,
            data={"count": count, "titles": [title.text for title in titles]},
            error_level=error_level,
        )

    def validate_award_id_funding_source_consistency(self, error_level="WARNING"):
        """
        Rule 7: Validates consistency of <funding-source> and <award-id> quantities.
        
        According to SPS 1.10, in each <award-group>, the quantity of <award-id> should be:
        - 0: Support without contract
        - 1: One contract for one or more funding sources
        - N: Multiple contracts (should match number of funding sources in most cases)
        
        Params
        ------
        error_level : str, optional
            The severity level of the validation error, by default "WARNING".
        
        Yields
        ------
        dict
            Validation results for each award-group.
        """
        funding_data = self.funding.data
        parent = {
            "parent": "article",
            "parent_id": None,
            "parent_article_type": funding_data.get("article_type"),
            "parent_lang": funding_data.get("article_lang"),
        }
        
        for item in self.funding.award_groups:
            funding_sources = item["funding-source"]
            award_ids = item["award-id"]
            
            num_sources = len(funding_sources)
            num_awards = len(award_ids)
            
            # Valid cases: 0 awards (support), 1 award (single contract), or N awards matching N sources
            is_valid = num_awards == 0 or num_awards == 1 or num_awards == num_sources
            
            advice = None
            if not is_valid:
                if num_awards > 1 and num_awards != num_sources:
                    advice = f"Inconsistent quantities: {num_sources} <funding-source>(s) but {num_awards} <award-id>(s). When multiple <award-id> elements exist, they should typically match the number of <funding-source> elements, or use separate <award-group> elements."
            
            yield build_response(
                title="award-id and funding-source consistency",
                parent=parent,
                item="award-group",
                sub_item="award-id",
                validation_type="consistency",
                is_valid=is_valid,
                expected="Consistent quantities: 0 awards (support), 1 award (contract), or N awards matching N sources",
                obtained=f"{num_sources} funding-source(s), {num_awards} award-id(s)",
                advice=advice,
                data=item,
                error_level=error_level,
            )
