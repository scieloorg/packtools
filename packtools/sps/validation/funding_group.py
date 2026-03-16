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
        Validates that each <funding-group> has a <funding-statement> consistent
        with the reference texts found in the document (fn elements, ack, etc.).

        Each <funding-group> is evaluated individually so that a second group
        without <funding-statement> is not silently skipped (bug C6). Reference
        texts are whitespace-normalised before use in advice strings to avoid
        raw concatenated whitespace from multiple <fn> elements (bug C7).

        Yields
        ------
        dict
            Validation result per <funding-group> node.
        """
        if not self.funding.award_groups:
            return

        funding_groups = self.xml_tree.xpath(".//article-meta/funding-group")
        if not funding_groups:
            return

        funding_data = self.funding.data

        # Collect document-level reference texts (fn elements, ack, etc.)
        # and normalise whitespace to prevent C7 (raw concatenated whitespace
        # from multiple <fn> nodes appearing in advice strings).
        all_texts = []
        for lang, statements in self.funding.statements_by_lang.items():
            items = {k: v for k, v in statements["texts"].items() if v}
            for v in items.values():
                normalized = " ".join(v.split())
                if normalized:
                    all_texts.append(normalized)

        # Iterate each <funding-group> individually (C6 fix: each node is
        # evaluated; the second group is no longer silently skipped).
        for fg_node in funding_groups:
            # Infer parent context from the node itself so that sub-article
            # scopes are correctly reported (mirrors validate_funding_group_uniqueness).
            article_meta = fg_node.getparent()
            parent_elem = article_meta.getparent() if article_meta is not None else None
            if parent_elem is not None:
                parent_tag = parent_elem.tag
                if "}" in parent_tag:
                    parent_tag = parent_tag.split("}", 1)[1]
                parent_id = parent_elem.get("id")
            else:
                parent_tag = "article"
                parent_id = None
            parent = {
                "parent": parent_tag,
                "parent_id": parent_id,
                "parent_article_type": funding_data.get("article_type"),
                "parent_lang": funding_data.get("article_lang"),
            }

            fs_nodes = fg_node.xpath("funding-statement")
            funding_statement = None
            if fs_nodes:
                # Concatenate text from ALL <funding-statement> nodes in this group
                # (not just the first) to avoid false-negatives when multiple nodes
                # are present — mirrors the approach in validate_funding_statement_presence().
                raw = "".join("".join(node.itertext()) for node in fs_nodes)
                funding_statement = " ".join(raw.split()) or None

            texts = all_texts
            valid = False
            advice = None

            if funding_statement and texts:
                # Both a <funding-statement> and reference texts exist: compare them.
                best_score, best_matches = most_similar(
                    similarity(texts, funding_statement, 0.8)
                )
                if best_matches:
                    valid = True
                else:
                    advice = (
                        f"Replace <funding-statement>{funding_statement}</funding-statement>"
                        f" by <funding-statement>{texts[0]}</funding-statement>"
                    )
            elif funding_statement and not texts:
                # <funding-statement> is present but no reference texts (fn/ack) were
                # found to compare against.  We cannot invalidate the statement, so
                # treat as valid and emit an informational advice only.
                valid = True
                advice = (
                    "No reference texts (fn/ack elements) were found to compare with"
                    " <funding-statement>. Verify manually that the statement is correct."
                )
            elif texts:
                # Reference texts exist but <funding-statement> is absent.
                advice = (
                    f"Add <funding-statement>{texts[0]}</funding-statement>"
                    " in <funding-group>. Consult SPS documentation for more detail"
                )
            else:
                # Neither <funding-statement> nor reference texts are present.
                advice = (
                    "Add funding statement with <funding-statement> inside"
                    " <funding-group>. Consult SPS documentation for more detail"
                )

            yield build_response(
                title="funding-statement",
                parent=parent,
                item="funding-statement",
                sub_item=None,
                validation_type="match",
                is_valid=valid,
                expected="funding-statement",
                obtained=funding_statement or "None",
                advice=advice,
                data={"funding_statement": funding_statement, "texts": texts},
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
        article_metas = self.xml_tree.xpath(".//article-meta")
        funding_data = self.funding.data

        for article_meta in article_metas:
            funding_groups = article_meta.xpath("./funding-group")
            count = len(funding_groups)

            parent_elem = article_meta.getparent()
            if parent_elem is not None:
                parent_tag = parent_elem.tag
                if "}" in parent_tag:
                    parent_tag = parent_tag.split("}", 1)[1]
                parent_id = parent_elem.get("id")
            else:
                parent_tag = "article"
                parent_id = None

            parent = {
                "parent": parent_tag,
                "parent_id": parent_id,
                "parent_article_type": funding_data.get("article_type"),
                "parent_lang": funding_data.get("article_lang"),
            }

            is_valid = count <= 1
            advice = None
            if not is_valid:
                advice = (
                    f"Found {count} <funding-group> elements in <article-meta>. "
                    "Only one is allowed. Merge them into a single <funding-group>."
                )

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
        Rule 2: Validates that <funding-statement> is present in EACH <funding-group>.
        
        According to SPS 1.10, <funding-statement> is mandatory in all cases.
        Each <funding-group> must have its own <funding-statement>.
        
        Params
        ------
        error_level : str, optional
            The severity level of the validation error, by default "CRITICAL".
        
        Yields
        ------
        dict
            Validation result for funding-statement presence in each funding-group.
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
        
        # Validate each funding-group individually
        for idx, funding_group_node in enumerate(funding_groups):
            funding_statements = funding_group_node.xpath("funding-statement")
            is_valid = len(funding_statements) > 0
            
            if is_valid:
                # Get the text from funding-statement(s)
                text_parts = []
                for fs in funding_statements:
                    raw_text = "".join(fs.itertext())
                    cleaned = " ".join(raw_text.split())
                    if cleaned:
                        text_parts.append(cleaned)
                funding_statement_text = " ".join(text_parts)
                obtained = funding_statement_text if funding_statement_text else "Present but empty"
                advice = None
            else:
                obtained = "None"
                advice = f"Add <funding-statement> element inside <funding-group> (index {idx + 1}). It is mandatory according to SPS 1.10."
            
            yield build_response(
                title="funding-statement presence",
                parent=parent,
                item="funding-statement",
                sub_item=None,
                validation_type="exist",
                is_valid=is_valid,
                expected="<funding-statement> present in <funding-group>",
                obtained=obtained,
                advice=advice,
                data={"funding_group_index": idx + 1, "has_funding_statement": is_valid},
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
            data={
                "count": count,
                "labels": [
                    text
                    for label in labels
                    for text in [" ".join(label.itertext()).strip()]
                    if text
                ],
            },
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
            data={
                "count": count,
                "titles": [
                    text
                    for title in titles
                    for text in [" ".join(title.itertext()).strip()]
                    if text
                ],
            },
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
