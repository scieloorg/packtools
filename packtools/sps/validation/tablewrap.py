from packtools.sps.models.tablewrap import ArticleTableWrappers
from packtools.sps.validation.utils import build_response


class ArticleTableWrapValidation:
    """
    Validates the <table-wrap> elements in an XML article.

    Args:
        xml_tree: XML object representing the article.
        rules: Dictionary containing validation rules.
    """

    def __init__(self, xml_tree, rules):
        if not hasattr(xml_tree, "get"):
            raise ValueError("xml_tree must be a valid XML object.")
        if not isinstance(rules, dict):
            raise ValueError("rules must be a dictionary containing error levels.")
        try:
            self.elements = list(ArticleTableWrappers(xml_tree).get_all_table_wrappers)
        except Exception as e:
            raise RuntimeError(f"Error processing table-wraps: {e}")
        self.xml_tree = xml_tree
        self.rules = rules
        self.article_type = self.xml_tree.get("article-type")

    def validate(self):
        """
        Performs validations on the article.
        Returns a generator with validation results.
        """
        if not self.elements:
            yield build_response(
                title="table-wrap presence",
                parent={
                    "parent": "article",
                    "parent_id": None,
                    "parent_article_type": self.xml_tree.get("article-type"),
                    "parent_lang": self.xml_tree.get(
                        "{http://www.w3.org/XML/1998/namespace}lang"
                    ),
                },
                item="table-wrap",
                sub_item=None,
                validation_type="exist",
                is_valid=False,
                expected="<table-wrap> element",
                obtained=None,
                advice=f'({self.article_type}) No <table-wrap> found in XML',
                data=None,
                error_level=self.rules["absent_error_level"],
                advice_text='({article_type}) No <table-wrap> found in XML',
                advice_params={"article_type": self.article_type},
            )
        else:
            for element in self.elements:
                yield from TableWrapValidation(element, self.rules).validate()


class TableWrapValidation:
    """
    Validates the attributes of a <table-wrap> element.

    Args:
        data: Dictionary containing the element's data.
        rules: Dictionary containing validation rules.
    """

    def __init__(self, data, rules):
        if not isinstance(data, dict):
            raise ValueError("data must be a dictionary.")
        self.data = data
        self.rules = self.get_default_params()
        self.rules.update(rules or {})
        self.table_id = self.data.get("table_wrap_id")
        self.xml = f'<table-wrap id="{self.table_id}">' if self.table_id else '<table-wrap>'

    def get_default_params(self):
        return {
            "absent_error_level": "WARNING",
            "id_error_level": "CRITICAL",
            "label_or_caption_error_level": "CRITICAL",
            "label_error_level": "CRITICAL",
            "caption_error_level": "CRITICAL",
            "table_error_level": "CRITICAL",
            "alternatives_error_level": "CRITICAL",
            "tr_in_table_error_level": "ERROR",
            "th_in_thead_error_level": "ERROR",
            "td_in_tbody_error_level": "ERROR",
            "tbody_error_level": "WARNING",
        }

    def validate(self):
        """
        Validates the attributes of the <table-wrap>.
        Returns a generator with validation results.
        """
        validations = [
            self.validate_id,
            self.validate_label_or_caption,
            self.validate_table,
            self.validate_alternatives,
            self.validate_tr_not_in_table,
            self.validate_th_in_thead,
            self.validate_td_in_tbody,
            self.validate_tbody,
        ]
        return [response for validate in validations if (response := validate())]

    def validate_id(self):
        """
        Validates the presence of ID in the <table-wrap>.

        Returns:
            The validation result in the expected format.
        """
        is_valid = bool(self.table_id)
        return build_response(
            title="id",
            parent={
                "parent": self.data.get("parent"),
                "parent_id": self.data.get("parent_id"),
                "parent_article_type": self.data.get("parent_article_type"),
                "parent_lang": self.data.get("parent_lang"),
            },
            item="table-wrap",
            sub_item="id",
            validation_type="exist",
            is_valid=is_valid,
            expected="id",
            obtained=self.table_id,
            advice='Add the table ID with id="" in <table-wrap>: <table-wrap id="">. Consult SPS documentation for more detail.',
            data=self.data,
            error_level=self.rules["id_error_level"],
            advice_text='Add the table ID with id="" in <table-wrap>: <table-wrap id="">. Consult SPS documentation for more detail.',
            advice_params={},
        )

    def validate_label_or_caption(self):
        """
        Validates the presence of <label> or <caption> in the <table-wrap>.
        At least one of <label> or <caption> with <title> must be present.

        Returns:
            The validation result in the expected format.
        """
        label = self.data.get("label")
        caption = self.data.get("caption")
        is_valid = bool(label) or bool(caption)
        obtained = []
        if label:
            obtained.append(f"label={label}")
        if caption:
            obtained.append(f"caption={caption}")
        obtained_str = ", ".join(obtained) if obtained else None
        advice = f'Add <label> or <caption> with <title> inside {self.xml}. Consult SPS documentation for more detail.'

        return build_response(
            title="label or caption",
            parent={
                "parent": self.data.get("parent"),
                "parent_id": self.data.get("parent_id"),
                "parent_article_type": self.data.get("parent_article_type"),
                "parent_lang": self.data.get("parent_lang"),
            },
            item="table-wrap",
            sub_item="label or caption",
            validation_type="exist",
            is_valid=is_valid,
            expected="<label> or <caption> with <title>",
            obtained=obtained_str,
            advice=advice,
            data=self.data,
            error_level=self.rules["label_or_caption_error_level"],
            advice_text='Add <label> or <caption> with <title> inside {xml}. Consult SPS documentation for more detail.',
            advice_params={"xml": self.xml},
        )

    def validate_table(self):
        """
        Validates the presence of table in the <table-wrap>.

        Returns:
            The validation result in the expected format.
        """
        table = self.data.get("table")
        is_valid = bool(table)
        return build_response(
            title="table",
            parent={
                "parent": self.data.get("parent"),
                "parent_id": self.data.get("parent_id"),
                "parent_article_type": self.data.get("parent_article_type"),
                "parent_lang": self.data.get("parent_lang"),
            },
            item="table-wrap",
            sub_item="table",
            validation_type="exist",
            is_valid=is_valid,
            expected="table",
            obtained=table,
            advice=f'Wrap each table with <table> inside {self.xml}. Consult SPS documentation for more detail.',
            data=self.data,
            error_level=self.rules["table_error_level"],
            advice_text='Wrap each table with <table> inside {xml}. Consult SPS documentation for more detail.',
            advice_params={"xml": self.xml},
        )

    def validate_alternatives(self):
        """
        Validates the presence of alternatives in the <table-wrap>.

        Returns:
            The validation result in the expected format.
        """
        graphic = 1 if self.data.get("graphic") else 0
        table = 1 if self.data.get("table") else 0
        alternatives = self.data.get("alternative_elements")

        if graphic + table > 1 and len(alternatives) == 0:
            expected = "alternatives"
            obtained = None
            advice = f'Wrap <table> and <graphic> with <alternatives> inside {self.xml} '
            advice_text = 'Wrap <table> and <graphic> with <alternatives> inside {xml} '
            advice_params = {"xml": self.xml}
            valid = False
        elif graphic + table == 1 and len(alternatives) > 0:
            expected = None
            obtained = "alternatives"
            advice = f'Remove the <alternatives> from {self.xml}.'
            advice_text = 'Remove the <alternatives> from {xml}.'
            advice_params = {"xml": self.xml}
            valid = False
        else:
            expected = "alternatives"
            obtained = "alternatives"
            advice = None
            advice_text = None
            advice_params = {}
            valid = True

        return build_response(
            title="alternatives",
            parent={
                "parent": self.data.get("parent"),
                "parent_id": self.data.get("parent_id"),
                "parent_article_type": self.data.get("parent_article_type"),
                "parent_lang": self.data.get("parent_lang"),
            },
            item="table-wrap",
            sub_item="alternatives",
            validation_type="exist",
            is_valid=valid,
            expected=expected,
            obtained=obtained,
            advice=advice,
            data=self.data,
            error_level=self.rules["alternatives_error_level"],
            advice_text=advice_text,
            advice_params=advice_params,
        )

    def validate_tr_not_in_table(self):
        """
        Validates that <tr> is not a direct child of <table>.
        The first level of <table> must not contain <tr> (NISO JATS model).

        Returns:
            The validation result in the expected format, or None if no <table> exists.
        """
        if not self.data.get("table"):
            return None
        has_tr = self.data.get("has_tr_in_table")
        is_valid = not has_tr
        return build_response(
            title="table structure",
            parent={
                "parent": self.data.get("parent"),
                "parent_id": self.data.get("parent_id"),
                "parent_article_type": self.data.get("parent_article_type"),
                "parent_lang": self.data.get("parent_lang"),
            },
            item="table-wrap",
            sub_item="table/tr",
            validation_type="exist",
            is_valid=is_valid,
            expected="<tr> must not be a direct child of <table>",
            obtained="<table><tr>..." if has_tr else "<tr> not found as direct child of <table>",
            advice=f'Remove <tr> as a direct child of <table> in {self.xml}. Use <thead> or <tbody> to wrap <tr> elements.',
            data=self.data,
            error_level=self.rules["tr_in_table_error_level"],
            advice_text='Remove <tr> as a direct child of <table> in {xml}. Use <thead> or <tbody> to wrap <tr> elements.',
            advice_params={"xml": self.xml},
        )

    def validate_th_in_thead(self):
        """
        Validates that <th> only appears as a descendant of <thead>.

        Returns:
            The validation result in the expected format, or None if no <table> exists.
        """
        if not self.data.get("table"):
            return None
        has_th_outside = self.data.get("has_th_outside_thead")
        is_valid = not has_th_outside
        return build_response(
            title="th in thead",
            parent={
                "parent": self.data.get("parent"),
                "parent_id": self.data.get("parent_id"),
                "parent_article_type": self.data.get("parent_article_type"),
                "parent_lang": self.data.get("parent_lang"),
            },
            item="table-wrap",
            sub_item="th",
            validation_type="exist",
            is_valid=is_valid,
            expected="<th> only as descendant of <thead>",
            obtained="<th> found outside <thead>" if has_th_outside else "<th> only in <thead>",
            advice=f'Move <th> elements to be inside <thead> in {self.xml}. Consult SPS documentation for more detail.',
            data=self.data,
            error_level=self.rules["th_in_thead_error_level"],
            advice_text='Move <th> elements to be inside <thead> in {xml}. Consult SPS documentation for more detail.',
            advice_params={"xml": self.xml},
        )

    def validate_td_in_tbody(self):
        """
        Validates that <td> only appears as a descendant of <tbody>.

        Returns:
            The validation result in the expected format, or None if no <table> exists.
        """
        if not self.data.get("table"):
            return None
        has_td_outside = self.data.get("has_td_outside_tbody")
        is_valid = not has_td_outside
        return build_response(
            title="td in tbody",
            parent={
                "parent": self.data.get("parent"),
                "parent_id": self.data.get("parent_id"),
                "parent_article_type": self.data.get("parent_article_type"),
                "parent_lang": self.data.get("parent_lang"),
            },
            item="table-wrap",
            sub_item="td",
            validation_type="exist",
            is_valid=is_valid,
            expected="<td> only as descendant of <tbody>",
            obtained="<td> found outside <tbody>" if has_td_outside else "<td> only in <tbody>",
            advice=f'Move <td> elements to be inside <tbody> in {self.xml}. Consult SPS documentation for more detail.',
            data=self.data,
            error_level=self.rules["td_in_tbody_error_level"],
            advice_text='Move <td> elements to be inside <tbody> in {xml}. Consult SPS documentation for more detail.',
            advice_params={"xml": self.xml},
        )

    def validate_tbody(self):
        """
        Validates the presence of <tbody> in <table>.

        Returns:
            The validation result in the expected format, or None if no <table> exists.
        """
        if not self.data.get("table"):
            return None
        has_tbody = self.data.get("has_tbody")
        is_valid = bool(has_tbody)
        return build_response(
            title="tbody",
            parent={
                "parent": self.data.get("parent"),
                "parent_id": self.data.get("parent_id"),
                "parent_article_type": self.data.get("parent_article_type"),
                "parent_lang": self.data.get("parent_lang"),
            },
            item="table-wrap",
            sub_item="tbody",
            validation_type="exist",
            is_valid=is_valid,
            expected="<tbody> element in <table>",
            obtained="<tbody>" if has_tbody else None,
            advice=f'Add <tbody> inside <table> in {self.xml}. Consult SPS documentation for more detail.',
            data=self.data,
            error_level=self.rules["tbody_error_level"],
            advice_text='Add <tbody> inside <table> in {xml}. Consult SPS documentation for more detail.',
            advice_params={"xml": self.xml},
        )
