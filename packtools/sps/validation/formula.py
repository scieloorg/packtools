from packtools.sps.models.formula import ArticleFormulas
from packtools.sps.validation.utils import format_response


class ArticleDispFormulaValidation:
    """
    Validates the presence and attributes of <disp-formula> elements in an XML tree.

    Attributes:
        xml_tree (ElementTree): The XML tree representing the article.
        elements (list): A list of <disp-formula> elements and their associated data.
        rules (dict): Validation rules specifying error levels and expected criteria.
    """
    def __init__(self, xml_tree, rules):
        if not hasattr(xml_tree, "get"):
            raise ValueError("xml_tree must be a valid XML object.")
        if not isinstance(rules, dict):
            raise ValueError("rules must be a dictionary containing error levels.")
        try:
            self.elements = list(ArticleFormulas(xml_tree).disp_formula_items)
        except Exception as e:
            raise RuntimeError(f"Error processing formula: {e}")
        self.xml_tree = xml_tree
        self.rules = rules

    def validate(self):
        """
        Performs validation for <disp-formula> elements in the article.

        Yields:
            dict: A dictionary containing the validation results for each <disp-formula> element.
        """
        if not self.elements:
            yield format_response(
                title="disp-formula",
                parent="article",
                parent_id=None,
                parent_article_type=self.xml_tree.get("article-type"),
                parent_lang=self.xml_tree.get(
                    "{http://www.w3.org/XML/1998/namespace}lang"
                ),
                item="disp-formula",
                sub_item=None,
                validation_type="exist",
                is_valid=False,
                expected="disp-formula",
                obtained=None,
                advice='Mark each formula inside <body> using <disp-formula>. Consult SPS documentation for more detail.',
                data=None,
                error_level=self.rules["absent_error_level"],
            )
        else:
            for data in self.elements:
                yield from DispFormulaValidation(data, self.rules).validate()


class DispFormulaValidation:
    """
    Validates individual <formula> elements and their attributes.

    Attributes:
        data (dict): Data associated with a specific <formula> element or group.
        rules (dict): Validation rules specifying error levels and expected criteria.
    """
    def __init__(self, data, rules):
        if not isinstance(data, dict):
            raise ValueError("data must be a dictionary.")
        self.data = data
        self.rules = rules

    def validate(self):
        """
        Validates <disp-formula> elements according to specified rules.

        Returns:
            list: A list of validation results for specific <disp-formula> attributes.
        """

        validations = [
            self.validate_id,
            self.validate_label,
            self.validate_codification,
            self.validate_alternatives
        ]
        return [response for validate in validations if (response := validate())]

    def validate_id(self):
        """
        Validates the presence of the '@id' attribute in a <disp-formula> element.

        Returns:
            dict or None: A validation result dictionary if the validation fails; otherwise, None.
        """

        formula_id = self.data.get("id")
        is_valid = bool(formula_id)
        return format_response(
            title="@id",
            parent=self.data.get("parent"),
            parent_id=self.data.get("parent_id"),
            parent_article_type=self.data.get("parent_article_type"),
            parent_lang=self.data.get("parent_lang"),
            item="@id",
            sub_item=None,
            validation_type="exist",
            is_valid=is_valid,
            expected="@id",
            obtained=formula_id,
            advice='Add the formula ID with id="" in <disp-formula>: <disp-formula id="">. Consult SPS documentation for more detail.',
            data=self.data,
            error_level=self.rules["id_error_level"],
        )

    def validate_label(self):
        """
        Validates the presence of the 'label' attribute in a <disp-formula> element.

        Returns:
            dict or None: A validation result dictionary if the validation fails; otherwise, None.
        """

        label = self.data.get("label")
        is_valid = bool(label)
        item_id = self.data.get("id")

        return format_response(
            title="label",
            parent=self.data.get("parent"),
            parent_id=self.data.get("parent_id"),
            parent_article_type=self.data.get("parent_article_type"),
            parent_lang=self.data.get("parent_lang"),
            item="label",
            sub_item=None,
            validation_type="exist",
            is_valid=is_valid,
            expected="label",
            obtained=label,
            advice=f'Mark each label with <label> inside <disp-formula id="{item_id}">. Consult SPS documentation for more detail.',
            data=self.data,
            error_level=self.rules["label_error_level"],
        )

    def validate_codification(self):
        """
        Validates the presence of the 'codification' attribute in a <disp-formula> element.

        Returns:
            dict or None: A validation result dictionary if the validation fails; otherwise, None.
        """
        count = 0
        found = []
        if self.data.get("mml_math"):
            count += 1
            found.append("mml:math")
        if self.data.get("tex_math"):
            count += 1
            found.append("tex-math")

        obtained = " and ".join(found) if found else "not found codification formula"

        is_valid = count == 1
        item_id = self.data.get("id")
        return format_response(
            title="mml:math or tex-math",
            parent=self.data.get("parent"),
            parent_id=self.data.get("parent_id"),
            parent_article_type=self.data.get("parent_article_type"),
            parent_lang=self.data.get("parent_lang"),
            item="mml:math or tex-math",
            sub_item=None,
            validation_type="exist",
            is_valid=is_valid,
            expected="mml:math or tex-math",
            obtained=obtained,
            advice=f'Mark each formula codification with <mml:math> or <tex-math> inside <disp-formula id="{item_id}">. Consult SPS documentation for more detail.',
            data=self.data,
            error_level=self.rules["codification_error_level"],
        )

    def validate_alternatives(self):
        """
        Validates the presence of the 'alternatives' attribute in a <disp-formula> element.

        Returns:
            dict or None: A validation result dictionary if the validation fails; otherwise, None.
        """

        mml = 1 if self.data.get("mml_math") else 0 # self.data.get("mml_math") retorna uma codificação mml:math se houver
        tex = 1 if self.data.get("tex_math") else 0 # self.data.get("tex_math") retorna uma codificação tex-math se houver
        graphic = self.data.get("graphic") or [] # self.data.get("graphic") retorna uma lista com variações de graphic se houverem
        alternatives = self.data.get("alternative_elements") # uma lista com as tags internas à <alternatives>

        found = "tex-math" if tex else "mml:math"

        # forma do usuario identificar qual disp-formula tem o problema
        item_id = self.data.get("id")

        if mml + tex + len(graphic) > 1 and len(alternatives) == 0:
            expected = "alternatives"
            obtained = None
            advice = f'Wrap <tex-math> and <mml:math> with <alternatives> inside <disp-formula id="{item_id}">'
            valid = False
        elif mml + tex + len(graphic) == 1 and len(alternatives) > 0:
            expected = None
            obtained = "alternatives"
            advice = f'{item_id}: Remove the <alternatives> from <disp-formula id="{item_id}"> and keep <{found}> inside <disp-formula id="{item_id}">'
            valid = False
        elif len(alternatives) == 1:
            expected = None
            obtained = "alternatives"
            advice = f'{item_id}: Remove the <alternatives> from <disp-formula id="{item_id}"> and keep <{found}> inside <disp-formula id="{item_id}">'
            valid = False
        else:
            expected = "alternatives"
            obtained = "alternatives"
            advice = None
            valid = True

        return format_response(
            title="alternatives",
            parent=self.data.get("parent"),
            parent_id=self.data.get("parent_id"),
            parent_article_type=self.data.get("parent_article_type"),
            parent_lang=self.data.get("parent_lang"),
            item="alternatives",
            sub_item=None,
            validation_type="exist",
            is_valid=valid,
            expected=expected,
            obtained=obtained,
            advice=advice,
            data=self.data,
            error_level=self.rules["alternatives_error_level"],
        )



class ArticleInlineFormulaValidation:
    """
    Validates the presence and attributes of <inline-formula> elements in an XML tree.

    Attributes:
        xml_tree (ElementTree): The XML tree representing the article.
        rules (dict): Validation rules specifying error levels and expected criteria.
        elements (list): A list of dictionaries containing data of <inline-formula> elements.
    """

    def __init__(self, xml_tree, rules):
        if not hasattr(xml_tree, "get"):
            raise ValueError("xml_tree must be a valid XML object.")
        if not isinstance(rules, dict):
            raise ValueError("rules must be a dictionary containing error levels.")
        try:
            self.elements = list(ArticleFormulas(xml_tree).inline_formula_items)
        except Exception as e:
            raise RuntimeError(f"Error processing formula: {e}")
        self.xml_tree = xml_tree
        self.rules = rules

    def validate(self):
        """
        Performs validation for <inline-formula> elements in the article.

        Yields:
            dict: A dictionary containing the validation results for each <inline-formula> element.
        """

        if not self.elements:
            yield format_response(
                title="inline-formula",
                parent="article",
                parent_id=None,
                parent_article_type=self.xml_tree.get("article-type"),
                parent_lang=self.xml_tree.get(
                    "{http://www.w3.org/XML/1998/namespace}lang"
                ),
                item="inline-formula",
                sub_item=None,
                validation_type="exist",
                is_valid=False,
                expected="inline-formula",
                obtained=None,
                advice="Add <inline-formula> elements to properly represent mathematical expressions in the content.",
                data=None,
                error_level=self.rules["absent_error_level"],
            )
        else:
            for data in self.elements:
                yield from InlineFormulaValidation(data, self.rules).validate()


class InlineFormulaValidation:
    """
    Validates individual <formula> elements and their attributes.

    Attributes:
        data (dict): Data associated with a specific <formula> element or group.
        rules (dict): Validation rules specifying error levels and expected criteria.
    """
    def __init__(self, data, rules):
        if not isinstance(data, dict):
            raise ValueError("data must be a dictionary.")
        self.data = data
        self.rules = rules

    def validate(self):
        """
        Validates <inline-formula> elements according to specified rules.

        Returns:
            list: A list of validation results for specific <inline-formula> attributes.
        """

        validations = [
            self.validate_codification,
            self.validate_alternatives
        ]
        return [response for validate in validations if (response := validate())]

    def validate_codification(self):
        """
        Validates the presence of codification (mml:math or tex-math) in a <inline-formula> element.

        Returns:
            dict or None: A validation result dictionary if the validation fails; otherwise, None.
        """

        count = 0
        found = []
        if self.data.get("mml_math"):
            count += 1
            found.append("mml:math")
        if self.data.get("tex_math"):
            count += 1
            found.append("tex-math")

        obtained = " and ".join(found) if found else "not found codification formula"

        is_valid = count == 1

        return format_response(
            title="mml:math or tex-math",
            parent=self.data.get("parent"),
            parent_id=self.data.get("parent_id"),
            parent_article_type=self.data.get("parent_article_type"),
            parent_lang=self.data.get("parent_lang"),
            item="mml:math or tex-math",
            sub_item=None,
            validation_type="exist",
            is_valid=is_valid,
            expected="mml:math or tex-math",
            obtained=obtained,
            advice=f'Mark each formula codification with <mml:math> or <tex-math> inside <inline-formula>. Consult SPS documentation for more detail.',
            data=self.data,
            error_level=self.rules["codification_error_level"],
        )

    def validate_alternatives(self):
        """
        Validates the presence of alternatives in a <inline-formula> element.

        Returns:
            dict or None: A validation result dictionary if the validation fails; otherwise, None.
        """

        mml = 1 if self.data.get("mml_math") else 0  # self.data.get("mml_math") retorna uma codificação mml:math se houver
        tex = 1 if self.data.get("tex_math") else 0  # self.data.get("tex_math") retorna uma codificação tex-math se houver
        graphic = self.data.get("graphic") or []  # self.data.get("graphic") retorna uma lista com variações de graphic se houverem
        alternatives = self.data.get("alternative_elements")  # uma lista com as tags internas à <alternatives>

        found = "tex-math" if tex else "mml:math"

        if mml + tex + len(graphic) > 1 and len(alternatives) == 0:
            expected = "alternatives"
            obtained = None
            advice = f'Wrap <tex-math> and <mml:math> with <alternatives> inside <inline-formula>'
            valid = False
        elif mml + tex + len(graphic) == 1 and len(alternatives) > 0:
            expected = None
            obtained = "alternatives"
            advice = f'Remove the <alternatives> from <inline-formula> and keep <{found}> inside <inline-formula>'
            valid = False
        elif len(alternatives) == 1:
            expected = None
            obtained = "alternatives"
            advice = f'Remove the <alternatives> from <inline-formula> and keep <{found}> inside <inline-formula>'
            valid = False
        else:
            expected = "alternatives"
            obtained = "alternatives"
            advice = None
            valid = True

        return format_response(
            title="alternatives",
            parent=self.data.get("parent"),
            parent_id=self.data.get("parent_id"),
            parent_article_type=self.data.get("parent_article_type"),
            parent_lang=self.data.get("parent_lang"),
            item="alternatives",
            sub_item=None,
            validation_type="exist",
            is_valid=valid,
            expected=expected,
            obtained=obtained,
            advice=advice,
            data=self.data,
            error_level=self.rules["alternatives_error_level"],
        )
