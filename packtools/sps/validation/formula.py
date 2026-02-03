import logging
from gettext import gettext as _

from packtools.sps.models.formula import ArticleFormulas
from packtools.sps.validation.utils import build_response
from packtools.sps.validation.xml_validator_rules import get_group_rules


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
        self.article_type = xml_tree.find(".").get("article-type")

    def validate(self):
        """
        Performs validation for <disp-formula> elements in the article.

        Yields:
            dict: A dictionary containing the validation results for each <disp-formula> element.
        """
        if not self.elements:
            yield build_response(
                title="disp-formula",
                parent={"parent": "article", "parent_id": None, "parent_article_type": self.xml_tree.get("article-type"), "parent_lang": self.xml_tree.get("{http://www.w3.org/XML/1998/namespace}lang")},
                item="disp-formula",
                sub_item=None,
                validation_type="exist",
                is_valid=False,
                expected="disp-formula",
                obtained=None,
                advice=_('No <disp-formula> found in XML'),
                data=None,
                error_level=self.rules["absent_error_level"],
                advice_text=_('No <disp-formula> found in XML'),
                advice_params={},
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
        self.rules = self.get_default_params()
        self.rules.update(rules or {})
        self.eq_id = self.data.get("id")
        self.article_type = self.data.get("article-type")
        self.xml = f'<disp-formula id="{self.eq_id}">' if self.eq_id else '<disp-formula>'

    def get_default_params(self):
        return {
            "absent_error_level": "WARNING",
            "id_error_level": "CRITICAL",
            "id_prefix_error_level": "ERROR",
            "label_error_level": "WARNING",
            "codification_error_level": "CRITICAL",
            "mml_math_id_error_level": "CRITICAL",
            "mml_math_id_prefix_error_level": "ERROR",
            "alternatives_error_level": "CRITICAL"
        }

    def validate(self):
        """
        Validates <disp-formula> elements according to specified rules.

        Returns:
            list: A list of validation results for specific <disp-formula> attributes.
        """

        validations = [
            self.validate_id,
            self.validate_id_prefix,
            self.validate_label,
            self.validate_codification,
            self.validate_mml_math_id,
            self.validate_mml_math_id_prefix,
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
        return build_response(
            title="@id",
            parent=self.data,
            item="@id",
            sub_item=None,
            validation_type="exist",
            is_valid=is_valid,
            expected="@id",
            obtained=formula_id,
            advice=_('Add the formula ID with id="" in <disp-formula>: <disp-formula id="">. Consult SPS documentation for more detail.'),
            data=self.data,
            error_level=self.rules["id_error_level"],
            advice_text=_('Add the formula ID with id="" in <disp-formula>: <disp-formula id="">. Consult SPS documentation for more detail.'),
            advice_params={},
        )

    def validate_id_prefix(self):
        """
        Validates that the '@id' attribute in a <disp-formula> element starts with prefix 'e'.

        Returns:
            dict or None: A validation result dictionary if the validation fails; otherwise, None.
        """
        formula_id = self.data.get("id")

        # Se não há ID, não valida prefixo (já validado em validate_id)
        if not formula_id:
            return None

        is_valid = formula_id.startswith("e")
        expected = _("id starting with 'e'")

        return build_response(
            title="@id prefix",
            parent=self.data,
            item="@id",
            sub_item=None,
            validation_type="format",
            is_valid=is_valid,
            expected=expected,
            obtained=formula_id,
            advice=_('The @id of <disp-formula> must start with prefix "e". Change {id} to e{id} in <disp-formula id="{id}">. Consult SPS documentation for more detail.').format(id=formula_id),
            data=self.data,
            error_level=self.rules["id_prefix_error_level"],
            advice_text=_('The @id of <disp-formula> must start with prefix "e". Change {id} to e{id} in <disp-formula id="{id}">. Consult SPS documentation for more detail.'),
            advice_params={"id": formula_id},
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

        return build_response(
            title="label",
            parent=self.data,
            item="label",
            sub_item=None,
            validation_type="exist",
            is_valid=is_valid,
            expected="label",
            obtained=label,
            advice=_('Mark each label with <label> inside <disp-formula id="{id}">. Consult SPS documentation for more detail.').format(id=item_id),
            data=self.data,
            error_level=self.rules["label_error_level"],
            advice_text=_('Mark each label with <label> inside <disp-formula id="{id}">. Consult SPS documentation for more detail.'),
            advice_params={"id": item_id},
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

        obtained = " and ".join(found) if found else _("not found codification formula")

        is_valid = count == 1
        item_id = self.data.get("id")
        return build_response(
            title="mml:math or tex-math",
            parent=self.data,
            item="mml:math or tex-math",
            sub_item=None,
            validation_type="exist",
            is_valid=is_valid,
            expected="mml:math or tex-math",
            obtained=obtained,
            advice=_('Mark each formula codification with <mml:math> or <tex-math> inside <disp-formula id="{id}">. Consult SPS documentation for more detail.').format(id=item_id),
            data=self.data,
            error_level=self.rules["codification_error_level"],
            advice_text=_('Mark each formula codification with <mml:math> or <tex-math> inside <disp-formula id="{id}">. Consult SPS documentation for more detail.'),
            advice_params={"id": item_id},
        )

    def validate_mml_math_id(self):
        """
        Validates the presence of '@id' attribute in <mml:math> element.

        Returns:
            dict or None: A validation result dictionary if the validation fails; otherwise, None.
        """
        # Só valida se houver mml:math
        if not self.data.get("mml_math"):
            return None

        mml_math_id = self.data.get("mml_math_id")
        is_valid = bool(mml_math_id)
        item_id = self.data.get("id")

        return build_response(
            title="mml:math @id",
            parent=self.data,
            item="mml:math @id",
            sub_item=None,
            validation_type="exist",
            is_valid=is_valid,
            expected="@id in mml:math",
            obtained=mml_math_id,
            advice=_('Add the @id attribute in <mml:math> inside <disp-formula id="{formula_id}">: <mml:math id="">. Consult SPS documentation for more detail.').format(formula_id=item_id),
            data=self.data,
            error_level=self.rules["mml_math_id_error_level"],
            advice_text=_('Add the @id attribute in <mml:math> inside <disp-formula id="{formula_id}">: <mml:math id="">. Consult SPS documentation for more detail.'),
            advice_params={"formula_id": item_id},
        )

    def validate_mml_math_id_prefix(self):
        """
        Validates that the '@id' attribute in <mml:math> starts with prefix 'm'.

        Returns:
            dict or None: A validation result dictionary if the validation fails; otherwise, None.
        """
        # Só valida se houver mml:math com id
        if not self.data.get("mml_math") or not self.data.get("mml_math_id"):
            return None

        mml_math_id = self.data.get("mml_math_id")
        is_valid = mml_math_id.startswith("m")
        expected = _("id starting with 'm'")
        item_id = self.data.get("id")

        return build_response(
            title="mml:math @id prefix",
            parent=self.data,
            item="mml:math @id",
            sub_item=None,
            validation_type="format",
            is_valid=is_valid,
            expected=expected,
            obtained=mml_math_id,
            advice=_('The @id of <mml:math> must start with prefix "m". Change {mml_id} to m{mml_id} in <mml:math id="{mml_id}"> inside <disp-formula id="{formula_id}">. Consult SPS documentation for more detail.').format(mml_id=mml_math_id, formula_id=item_id),
            data=self.data,
            error_level=self.rules["mml_math_id_prefix_error_level"],
            advice_text=_('The @id of <mml:math> must start with prefix "m". Change {mml_id} to m{mml_id} in <mml:math id="{mml_id}"> inside <disp-formula id="{formula_id}">. Consult SPS documentation for more detail.'),
            advice_params={"mml_id": mml_math_id, "formula_id": item_id},
        )

    def validate_alternatives(self):
        """
        Validates the presence of the 'alternatives' attribute in a <disp-formula> element.

        Returns:
            dict or None: A validation result dictionary if the validation fails; otherwise, None.
        """

        mml = 1 if self.data.get("mml_math") else 0
        tex = 1 if self.data.get("tex_math") else 0
        graphic = self.data.get("graphic") or []
        alternatives = self.data.get("alternative_elements")

        found = "tex-math" if tex else "mml:math"

        if mml + tex + len(graphic) > 1 and len(alternatives) == 0:
            expected = "alternatives"
            obtained = None
            advice = _('Wrap <tex-math> and <mml:math> with <alternatives> inside <disp-formula>')
            advice_text = _('Wrap <tex-math> and <mml:math> with <alternatives> inside <disp-formula>')
            advice_params = {}
            valid = False
        elif mml + tex + len(graphic) == 1 and len(alternatives) > 0:
            expected = None
            obtained = "alternatives"
            advice = _('Remove the <alternatives> from <disp-formula> and keep <{found}> inside <disp-formula>').format(found=found)
            advice_text = _('Remove the <alternatives> from <disp-formula> and keep <{found}> inside <disp-formula>')
            advice_params = {"found": found}
            valid = False
        elif len(alternatives) == 1:
            expected = None
            obtained = "alternatives"
            advice = _('Remove the <alternatives> from <disp-formula> and keep <{found}> inside <disp-formula>').format(found=found)
            advice_text = _('Remove the <alternatives> from <disp-formula> and keep <{found}> inside <disp-formula>')
            advice_params = {"found": found}
            valid = False
        else:
            expected = "alternatives"
            obtained = "alternatives"
            advice = None
            advice_text = None
            advice_params = None
            valid = True

        return build_response(
            title="alternatives",
            parent=self.data,
            item="alternatives",
            sub_item=None,
            validation_type="exist",
            is_valid=valid,
            expected=expected,
            obtained=obtained,
            advice=advice,
            data=self.data,
            error_level=self.rules["alternatives_error_level"],
            advice_text=advice_text,
            advice_params=advice_params or {},
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
        self.article_type = xml_tree.find(".").get("article-type")

    def validate(self):
        """
        Performs validation for <inline-formula> elements in the article.

        Yields:
            dict: A dictionary containing the validation results for each <inline-formula> element.
        """

        if not self.elements:
            yield build_response(
                title="inline-formula",
                parent={"parent": "article", "parent_id": None, "parent_article_type": self.xml_tree.get("article-type"), "parent_lang": self.xml_tree.get("{http://www.w3.org/XML/1998/namespace}lang")},
                item="inline-formula",
                sub_item=None,
                validation_type="exist",
                is_valid=False,
                expected="inline-formula",
                obtained=None,
                advice=_('No <inline-formula> found in XML'),
                data=None,
                error_level=self.rules["absent_error_level"],
                advice_text=_('No <inline-formula> found in XML'),
                advice_params={},
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
        self.rules = self.get_default_params()
        self.rules.update(rules or {})

    def get_default_params(self):
        try:
            data = get_group_rules("formula")
            return data["inline_formula_rules"]
        except Exception as e:
            logging.exception(e)
            return {
                "absent_error_level": "WARNING",
                "id_error_level": "CRITICAL",
                "id_prefix_error_level": "ERROR",
                "label_error_level": "WARNING",
                "codification_error_level": "CRITICAL",
                "mml_math_id_error_level": "CRITICAL",
                "mml_math_id_prefix_error_level": "ERROR",
                "alternatives_error_level": "CRITICAL"
            }

    def validate(self):
        """
        Validates <inline-formula> elements according to specified rules.

        Returns:
            list: A list of validation results for specific <inline-formula> attributes.
        """

        validations = [
            self.validate_id,
            self.validate_id_prefix,
            self.validate_codification,
            self.validate_mml_math_id,
            self.validate_mml_math_id_prefix,
            self.validate_alternatives
        ]
        return [response for validate in validations if (response := validate())]

    def validate_id(self):
        """
        Validates the presence of the '@id' attribute in an <inline-formula> element.

        Returns:
            dict or None: A validation result dictionary if the validation fails; otherwise, None.
        """

        formula_id = self.data.get("id")
        is_valid = bool(formula_id)
        return build_response(
            title="@id",
            parent=self.data,
            item="@id",
            sub_item=None,
            validation_type="exist",
            is_valid=is_valid,
            expected="@id",
            obtained=formula_id,
            advice=_('Add the formula ID with id="" in <inline-formula>: <inline-formula id="">. Consult SPS documentation for more detail.'),
            data=self.data,
            error_level=self.rules["id_error_level"],
            advice_text=_('Add the formula ID with id="" in <inline-formula>: <inline-formula id="">. Consult SPS documentation for more detail.'),
            advice_params={},
        )

    def validate_id_prefix(self):
        """
        Validates that the '@id' attribute in an <inline-formula> element starts with prefix 'e'.

        Returns:
            dict or None: A validation result dictionary if the validation fails; otherwise, None.
        """
        formula_id = self.data.get("id")

        # Se não há ID, não valida prefixo (já validado em validate_id)
        if not formula_id:
            return None

        is_valid = formula_id.startswith("e")
        expected = _("id starting with 'e'")

        return build_response(
            title="@id prefix",
            parent=self.data,
            item="@id",
            sub_item=None,
            validation_type="format",
            is_valid=is_valid,
            expected=expected,
            obtained=formula_id,
            advice=_('The @id of <inline-formula> must start with prefix "e". Change {id} to e{id} in <inline-formula id="{id}">. Consult SPS documentation for more detail.').format(id=formula_id),
            data=self.data,
            error_level=self.rules["id_prefix_error_level"],
            advice_text=_('The @id of <inline-formula> must start with prefix "e". Change {id} to e{id} in <inline-formula id="{id}">. Consult SPS documentation for more detail.'),
            advice_params={"id": formula_id},
        )

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

        obtained = " and ".join(found) if found else _("not found codification formula")

        is_valid = count == 1

        return build_response(
            title="mml:math or tex-math",
            parent=self.data,
            item="mml:math or tex-math",
            sub_item=None,
            validation_type="exist",
            is_valid=is_valid,
            expected="mml:math or tex-math",
            obtained=obtained,
            advice=_('Mark each formula codification with <mml:math> or <tex-math> inside <inline-formula>. Consult SPS documentation for more detail.'),
            data=self.data,
            error_level=self.rules["codification_error_level"],
            advice_text=_('Mark each formula codification with <mml:math> or <tex-math> inside <inline-formula>. Consult SPS documentation for more detail.'),
            advice_params={},
        )

    def validate_mml_math_id(self):
        """
        Validates the presence of '@id' attribute in <mml:math> element.

        Returns:
            dict or None: A validation result dictionary if the validation fails; otherwise, None.
        """
        # Só valida se houver mml:math
        if not self.data.get("mml_math"):
            return None

        mml_math_id = self.data.get("mml_math_id")
        is_valid = bool(mml_math_id)
        item_id = self.data.get("id")

        return build_response(
            title="mml:math @id",
            parent=self.data,
            item="mml:math @id",
            sub_item=None,
            validation_type="exist",
            is_valid=is_valid,
            expected="@id in mml:math",
            obtained=mml_math_id,
            advice=_('Add the @id attribute in <mml:math> inside <inline-formula id="{formula_id}">: <mml:math id="">. Consult SPS documentation for more detail.').format(formula_id=item_id),
            data=self.data,
            error_level=self.rules["mml_math_id_error_level"],
            advice_text=_('Add the @id attribute in <mml:math> inside <inline-formula id="{formula_id}">: <mml:math id="">. Consult SPS documentation for more detail.'),
            advice_params={"formula_id": item_id},
        )

    def validate_mml_math_id_prefix(self):
        """
        Validates that the '@id' attribute in <mml:math> starts with prefix 'm'.

        Returns:
            dict or None: A validation result dictionary if the validation fails; otherwise, None.
        """
        # Só valida se houver mml:math com id
        if not self.data.get("mml_math") or not self.data.get("mml_math_id"):
            return None

        mml_math_id = self.data.get("mml_math_id")
        is_valid = mml_math_id.startswith("m")
        expected = _("id starting with 'm'")
        item_id = self.data.get("id")

        return build_response(
            title="mml:math @id prefix",
            parent=self.data,
            item="mml:math @id",
            sub_item=None,
            validation_type="format",
            is_valid=is_valid,
            expected=expected,
            obtained=mml_math_id,
            advice=_('The @id of <mml:math> must start with prefix "m". Change {mml_id} to m{mml_id} in <mml:math id="{mml_id}"> inside <inline-formula id="{formula_id}">. Consult SPS documentation for more detail.').format(mml_id=mml_math_id, formula_id=item_id),
            data=self.data,
            error_level=self.rules["mml_math_id_prefix_error_level"],
            advice_text=_('The @id of <mml:math> must start with prefix "m". Change {mml_id} to m{mml_id} in <mml:math id="{mml_id}"> inside <inline-formula id="{formula_id}">. Consult SPS documentation for more detail.'),
            advice_params={"mml_id": mml_math_id, "formula_id": item_id},
        )

    def validate_alternatives(self):
        """
        Validates the presence of alternatives in a <inline-formula> element.

        Returns:
            dict or None: A validation result dictionary if the validation fails; otherwise, None.
        """

        mml = 1 if self.data.get("mml_math") else 0
        tex = 1 if self.data.get("tex_math") else 0
        graphic = self.data.get("graphic") or []
        alternatives = self.data.get("alternative_elements")

        found = "tex-math" if tex else "mml:math"

        if mml + tex + len(graphic) > 1 and len(alternatives) == 0:
            expected = "alternatives"
            obtained = None
            advice = _('Wrap <tex-math> and <mml:math> with <alternatives> inside <inline-formula>')
            advice_text = _('Wrap <tex-math> and <mml:math> with <alternatives> inside <inline-formula>')
            advice_params = {}
            valid = False
        elif mml + tex + len(graphic) == 1 and len(alternatives) > 0:
            expected = None
            obtained = "alternatives"
            advice = _('Remove the <alternatives> from <inline-formula> and keep <{found}> inside <inline-formula>').format(found=found)
            advice_text = _('Remove the <alternatives> from <inline-formula> and keep <{found}> inside <inline-formula>')
            advice_params = {"found": found}
            valid = False
        elif len(alternatives) == 1:
            expected = None
            obtained = "alternatives"
            advice = _('Remove the <alternatives> from <inline-formula> and keep <{found}> inside <inline-formula>').format(found=found)
            advice_text = _('Remove the <alternatives> from <inline-formula> and keep <{found}> inside <inline-formula>')
            advice_params = {"found": found}
            valid = False
        else:
            expected = "alternatives"
            obtained = "alternatives"
            advice = None
            advice_text = None
            advice_params = None
            valid = True

        return build_response(
            title="alternatives",
            parent=self.data,
            item="alternatives",
            sub_item=None,
            validation_type="exist",
            is_valid=valid,
            expected=expected,
            obtained=obtained,
            advice=advice,
            data=self.data,
            error_level=self.rules["alternatives_error_level"],
            advice_text=advice_text,
            advice_params=advice_params or {},
        )
