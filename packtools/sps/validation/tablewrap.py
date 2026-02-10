import gettext

from packtools.sps.models.tablewrap import ArticleTableWrappers
from packtools.sps.validation.utils import build_response

_ = gettext.gettext


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
            advice = f'({self.article_type}) No <table-wrap> found in XML'
            advice_text = _('({article_type}) No <table-wrap> found in XML')
            advice_params = {'article_type': self.article_type}
            
            parent_data = {
                'parent': 'article',
                'parent_id': None,
                'parent_article_type': self.xml_tree.get("article-type"),
                'parent_lang': self.xml_tree.get("{http://www.w3.org/XML/1998/namespace}lang")
            }
            
            yield build_response(
                title="table-wrap presence",
                parent=parent_data,
                item="table-wrap",
                sub_item=None,
                validation_type="exist",
                is_valid=False,
                expected="<table-wrap> element",
                obtained=None,
                advice=advice,
                advice_text=advice_text,
                advice_params=advice_params,
                data=None,
                error_level=self.rules["absent_error_level"],
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
            "label_error_level": "CRITICAL",
            "caption_error_level": "CRITICAL",
            "table_error_level": "CRITICAL",
            "alternatives_error_level": "CRITICAL"
        }

    def validate(self):
        """
        Validates the attributes of the <table-wrap>.
        Returns a generator with validation results.
        """
        validations = [
            self.validate_id,
            self.validate_label,
            self.validate_caption,
            self.validate_table,
            self.validate_alternatives,
        ]
        return [response for validate in validations if (response := validate())]

    def validate_id(self):
        """
        Validates the presence of ID in the <table-wrap>.

        Returns:
            The validation result in the expected format.
        """
        is_valid = bool(self.table_id)
        advice = 'Add the table ID with id="" in <table-wrap>: <table-wrap id="">. Consult SPS documentation for more detail.'
        advice_text = _('Add the table ID with id="" in <table-wrap>: <table-wrap id="">. Consult SPS documentation for more detail.')
        advice_params = {}
        
        return build_response(
            title="id",
            parent=self.data,
            item="table-wrap",
            sub_item="id",
            validation_type="exist",
            is_valid=is_valid,
            expected="id",
            obtained=self.table_id,
            advice=advice,
            advice_text=advice_text,
            advice_params=advice_params,
            data=self.data,
            error_level=self.rules["id_error_level"],
        )

    def validate_label(self):
        """
        Validates the presence of label in the <table-wrap>.

        Returns:
            The validation result in the expected format.
        """
        label = self.data.get("label")
        is_valid = bool(label)
        table_id = self.data.get("table_wrap_id")
        advice = f'Wrap each label with <label> inside {self.xml}. Consult SPS documentation for more detail.'
        advice_text = _('Wrap each label with <label> inside {xml}. Consult SPS documentation for more detail.')
        advice_params = {'xml': self.xml}

        return build_response(
            title="label",
            parent=self.data,
            item="table-wrap",
            sub_item="label",
            validation_type="exist",
            is_valid=is_valid,
            expected="label",
            obtained=label,
            advice=advice,
            advice_text=advice_text,
            advice_params=advice_params,
            data=self.data,
            error_level=self.rules["label_error_level"],
        )

    def validate_caption(self):
        """
        Validates the presence of caption in the <table-wrap>.

        Returns:
            The validation result in the expected format.
        """
        caption = self.data.get("caption")
        is_valid = bool(caption)
        table_id = self.data.get("table_wrap_id")
        advice = f'Wrap each caption with <caption> inside {self.xml}. Consult SPS documentation for more detail.'
        advice_text = _('Wrap each caption with <caption> inside {xml}. Consult SPS documentation for more detail.')
        advice_params = {'xml': self.xml}
        
        return build_response(
            title="caption",
            parent=self.data,
            item="table-wrap",
            sub_item="caption",
            validation_type="exist",
            is_valid=is_valid,
            expected="caption",
            obtained=caption,
            advice=advice,
            advice_text=advice_text,
            advice_params=advice_params,
            data=self.data,
            error_level=self.rules["caption_error_level"],
        )

    def validate_table(self):
        """
        Validates the presence of table in the <table-wrap>.

        Returns:
            The validation result in the expected format.
        """
        table = self.data.get("table")
        is_valid = bool(table)
        table_id = self.data.get("table_wrap_id")
        advice = f'Wrap each table with <table> inside {self.xml}. Consult SPS documentation for more detail.'
        advice_text = _('Wrap each table with <table> inside {xml}. Consult SPS documentation for more detail.')
        advice_params = {'xml': self.xml}
        
        return build_response(
            title="table",
            parent=self.data,
            item="table-wrap",
            sub_item="table",
            validation_type="exist",
            is_valid=is_valid,
            expected="table",
            obtained=table,
            advice=advice,
            advice_text=advice_text,
            advice_params=advice_params,
            data=self.data,
            error_level=self.rules["table_error_level"],
        )

    def validate_alternatives(self):
        """
        Validates the presence of alternatives in the <table-wrap>.

        Returns:
            The validation result in the expected format.
        """
        graphic = 1 if self.data.get("graphic") else 0 # self.data.get("graphic") retorna uma referência para uma representação da tabela, se houver
        table = 1 if self.data.get("table") else 0 # self.data.get("table") retorna uma codificação de tabela, se houver
        alternatives = self.data.get("alternative_elements") # uma lista com as tags internas à <alternatives>

        table_id = self.data.get("table_wrap_id")

        if graphic + table > 1 and len(alternatives) == 0:
            expected = "alternatives"
            obtained = None
            advice = f'Wrap <table> and <graphic> with <alternatives> inside {self.xml} '
            advice_text = _('Wrap <table> and <graphic> with <alternatives> inside {xml} ')
            advice_params = {'xml': self.xml}
            valid = False
        elif graphic + table == 1 and len(alternatives) > 0:
            expected = None
            obtained = "alternatives"
            advice = f'Remove the <alternatives> from {self.xml}.'
            advice_text = _('Remove the <alternatives> from {xml}.')
            advice_params = {'xml': self.xml}
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
            parent=self.data,
            item="table-wrap",
            sub_item="alternatives",
            validation_type="exist",
            is_valid=valid,
            expected=expected,
            obtained=obtained,
            advice=advice,
            advice_text=advice_text,
            advice_params=advice_params,
            data=self.data,
            error_level=self.rules["alternatives_error_level"],
        )
