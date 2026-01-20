from itertools import chain

from packtools.sps.validation.utils import build_response
from packtools.sps.validation.exceptions import ValidationAlternativesException
from packtools.sps.models import fig, formula, tablewrap


class AlternativeValidation:
    """
    Represents the validation of alternative elements within a parent element in an XML document.

    **Attributes:**
        alternative_data (dict): Dictionary containing information about the alternative elements.
        obtained_elements (list): List of tags within the <alternatives> element.
        parent_element (str): The parent tag name containing the <alternatives> element.
        expected_elements (list): List of expected child tags within the <alternatives> element.
    """

    def __init__(self, alternative_data, expected_elements):
        """
        Initializes an AlternativeValidation object.

        **Parameters:**
            alternative_data (dict): Dictionary containing information about the alternative elements.
            expected_elements (list): List of expected child tags within the <alternatives> element.
        """
        self.alternative_data = alternative_data
        self.obtained_elements = alternative_data.get("alternative_elements")
        self.parent_element = alternative_data.get("alternative_parent")
        self.expected_elements = expected_elements

    def validate_expected_elements(self, error_level="CRITICAL"):
        """
        Checks whether the alternatives match the tag that contains them.

        **Parameters:**
            error_level (str): The level of error to be used in the validation response.

        **Returns:**
            generator: A generator that yields dictionaries with validation results.
        """
        is_valid = True

        for tag in self.obtained_elements:
            if tag not in self.expected_elements:
                is_valid = False
                break

        yield build_response(
            title="Alternatives validation",
            parent=self.alternative_data,  # Passar dicionário completo
            item=self.parent_element,
            sub_item="alternatives",
            validation_type="value in list",
            is_valid=is_valid,
            expected=self.expected_elements,
            obtained=self.obtained_elements,
            advice=f'Add {self.expected_elements} as sub-elements of {self.parent_element}/alternatives',
            data=self.alternative_data,
            error_level=error_level,
            advice_text='Add {expected} as sub-elements of {parent}/alternatives',
            advice_params={
                "expected": str(self.expected_elements),
                "parent": self.parent_element
            }
        )

    def validate_svg_format(self, error_level="CRITICAL"):
        """
        Validates that graphic files in alternatives have SVG format.

        SciELO Rule: "Em <alternatives> as imagens em <graphic> devem, obrigatoriamente,
        possuir o formato SVG"

        **Parameters:**
            error_level (str): The level of error to be used in the validation response.

        **Yields:**
            dict: Validation result
        """
        # Get graphic href - handle both string and list
        graphic = self.alternative_data.get("graphic")

        # Skip if no graphic in alternatives
        if not graphic:
            return

        # Handle list of graphics (from formula)
        graphics_to_check = graphic if isinstance(graphic, list) else [graphic]

        for graphic_href in graphics_to_check:
            if not graphic_href:
                continue

            is_valid = graphic_href.lower().endswith('.svg')

            yield build_response(
                title="SVG format in alternatives",
                parent=self.alternative_data,
                item=self.parent_element,
                sub_item="alternatives/graphic",
                validation_type="format",
                is_valid=is_valid,
                expected=".svg format",
                obtained=graphic_href,
                advice=f'Use SVG format for graphic in {self.parent_element}/alternatives. '
                       f'Got: {graphic_href}',
                data=self.alternative_data,
                error_level=error_level,
                advice_text='Use SVG format for graphic in {parent}/alternatives. Got: {obtained}',
                advice_params={
                    "parent": self.parent_element,
                    "obtained": graphic_href
                }
            )

    def validate_no_alt_text(self, error_level="CRITICAL"):
        """
        Validates that graphic in alternatives does NOT have alt-text.

        SciELO Rule: "as imagens em .svg em <alternatives> não devem possuir a marcação
        dos elementos <alt-text>"

        **Parameters:**
            error_level (str): The level of error to be used in the validation response.

        **Yields:**
            dict: Validation result
        """
        alt_text = self.alternative_data.get("graphic_alt_text")

        # Skip if no alt-text (valid case)
        if not alt_text:
            return

        # If alt-text exists, it's invalid
        is_valid = False

        yield build_response(
            title="No alt-text in alternatives",
            parent=self.alternative_data,
            item=self.parent_element,
            sub_item="alternatives/graphic",
            validation_type="exist",
            is_valid=is_valid,
            expected="no <alt-text> in alternatives/graphic",
            obtained=f"<alt-text> found: {alt_text}",
            advice=f'Remove <alt-text> from graphic in {self.parent_element}/alternatives. '
                   f'Alternative images do not require alt-text because the coded version '
                   f'(table/formula) is already accessible.',
            data=self.alternative_data,
            error_level=error_level,
            advice_text='Remove <alt-text> from graphic in {parent}/alternatives. '
                       'Alternative images do not require alt-text because the coded version '
                       '({coded_version}) is already accessible.',
            advice_params={
                "parent": self.parent_element,
                "coded_version": "table" if self.parent_element == "table-wrap" else "formula",
                "alt_text": alt_text
            }
        )

    def validate_no_long_desc(self, error_level="CRITICAL"):
        """
        Validates that graphic in alternatives does NOT have long-desc.

        SciELO Rule: "as imagens em .svg em <alternatives> não devem possuir a marcação
        dos elementos <long-desc>"

        **Parameters:**
            error_level (str): The level of error to be used in the validation response.

        **Yields:**
            dict: Validation result
        """
        long_desc = self.alternative_data.get("graphic_long_desc")

        # Skip if no long-desc (valid case)
        if not long_desc:
            return

        # If long-desc exists, it's invalid
        is_valid = False

        yield build_response(
            title="No long-desc in alternatives",
            parent=self.alternative_data,
            item=self.parent_element,
            sub_item="alternatives/graphic",
            validation_type="exist",
            is_valid=is_valid,
            expected="no <long-desc> in alternatives/graphic",
            obtained=f"<long-desc> found: {long_desc}",
            advice=f'Remove <long-desc> from graphic in {self.parent_element}/alternatives. '
                   f'Alternative images do not require long-desc because the coded version '
                   f'(table/formula) is already accessible.',
            data=self.alternative_data,
            error_level=error_level,
            advice_text='Remove <long-desc> from graphic in {parent}/alternatives. '
                       'Alternative images do not require long-desc because the coded version '
                       '({coded_version}) is already accessible.',
            advice_params={
                "parent": self.parent_element,
                "coded_version": "table" if self.parent_element == "table-wrap" else "formula",
                "long_desc": long_desc
            }
        )

    def validate_both_versions_present(self, error_level="ERROR"):
        """
        Validates that both coded version AND image are present in alternatives.

        SciELO Rule: "O elemento só poderá ser utilizado em dados que estão originalmente
        codificados tais como tabela ou equação e sua imagem equivalente"

        **Parameters:**
            error_level (str): The level of error to be used in the validation response.

        **Yields:**
            dict: Validation result
        """
        elements = self.alternative_data.get("alternative_elements", [])

        # Define what's expected based on parent
        if self.parent_element == "table-wrap":
            coded_version = "table"
            image_version = "graphic"
        elif self.parent_element in ["disp-formula", "inline-formula"]:
            # For formulas, accept mml:math or tex-math as coded version
            coded_version = "{http://www.w3.org/1998/Math/MathML}math"  # MathML
            image_version = "graphic"
        elif self.parent_element == "fig":
            # For fig, typically graphic + media
            coded_version = "media"
            image_version = "graphic"
        else:
            # Unknown parent, skip validation
            return

        # Check if both are present
        has_coded = coded_version in elements or (
            self.parent_element in ["disp-formula", "inline-formula"] and
            "tex-math" in elements
        )
        has_image = image_version in elements

        is_valid = has_coded and has_image

        if not is_valid:
            missing = []
            if not has_coded:
                missing.append(coded_version)
            if not has_image:
                missing.append(image_version)

            yield build_response(
                title="Both versions in alternatives",
                parent=self.alternative_data,
                item=self.parent_element,
                sub_item="alternatives",
                validation_type="exist",
                is_valid=is_valid,
                expected=f"both {coded_version} and {image_version}",
                obtained=f"found: {elements}, missing: {missing}",
                advice=f'Add both coded version ({coded_version}) and image ({image_version}) '
                       f'to {self.parent_element}/alternatives',
                data=self.alternative_data,
                error_level=error_level,
                advice_text='Add both coded version ({coded}) and image ({image}) to {parent}/alternatives',
                advice_params={
                    "coded": coded_version,
                    "image": image_version,
                    "parent": self.parent_element,
                    "missing": str(missing)
                }
            )

    def validate(self, error_level="CRITICAL"):
        """
        Runs all validations for alternative elements.

        **Parameters:**
            error_level (str): The level of error to be used in validation responses.

        **Yields:**
            dict: Validation results
        """
        yield from self.validate_expected_elements(error_level)
        yield from self.validate_svg_format(error_level)
        yield from self.validate_no_alt_text(error_level)
        yield from self.validate_no_long_desc(error_level)
        yield from self.validate_both_versions_present("ERROR")


class AlternativesValidation:
    """
    Represents the validation of alternative elements within figures, formulas, and table-wraps in an XML document.

    **Attributes:**
        xml_tree (xml.etree.ElementTree.ElementTree): The parsed XML document representing the article.
        parent_to_children (dict): Dictionary mapping parent tags to their expected child tags within <alternatives>.
        figures (dict): Dictionary of figures grouped by language.
        formulas (dict): Dictionary of formulas (disp-formula and inline-formula) grouped by language.
        table_wraps (dict): Dictionary of table-wraps grouped by language.
    """

    def __init__(self, xml_tree, parent_to_children=None):
        """
        Initializes an AlternativesValidation object.

        **Parameters:**
            xml_tree (xml.etree.ElementTree.ElementTree): The parsed XML document representing the article.
            parent_to_children (dict, optional): Dictionary mapping parent tags to their expected child tags within <alternatives>.
        """
        self.xml_tree = xml_tree
        self.parent_to_children = parent_to_children
        self.figures = fig.ArticleFigs(self.xml_tree).get_all_figs or {}

        # Include both disp-formula and inline-formula
        formula_obj = formula.ArticleFormulas(self.xml_tree)
        self.formulas = chain(
            formula_obj.disp_formula_items,
            formula_obj.inline_formula_items
        )

        self.table_wraps = tablewrap.ArticleTableWrappers(self.xml_tree).get_all_table_wrappers or {}

    def validate(self, parent_to_children=None):
        """
        Validates the alternative elements within figures, formulas, and table-wraps against the expected children.

        **Parameters:**
            parent_to_children (dict, optional): Dictionary mapping parent tags to their expected child tags within <alternatives>.

        **Yields:**
            dict: A dictionary with validation results for each alternative element.
        """
        parent_to_children = parent_to_children or self.parent_to_children

        for data in chain(self.figures, self.formulas, self.table_wraps):
            parent_element = data.get("alternative_parent")
            if not parent_to_children:
                raise ValidationAlternativesException(f"The element '{parent_element}' is not configured to use 'alternatives'."
                                                      " Provide alternatives parent and children")
            expected_elements = parent_to_children.get(parent_element)
            if expected_elements is None:
                raise ValidationAlternativesException(f"The element '{parent_element}' is not configured to use 'alternatives'."
                                                      " Provide alternatives parent and children")
            yield from AlternativeValidation(data, expected_elements).validate()
