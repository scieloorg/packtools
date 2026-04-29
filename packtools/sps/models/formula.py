import lxml.etree as ET

from packtools.sps.utils.xml_utils import get_parent_context, put_parent_context


class Formula:
    """
    Represents a formula element within an XML document.

    Parameters:
        element (xml.etree.ElementTree.Element): The XML element representing the formula.
    """

    def __init__(self, element):
        """
        Initializes a Formula object.

        **Parameters:**
            element (xml.etree.ElementTree.Element): The XML element representing the formula.
        """
        self.element = element

    @property
    def formula_id(self):
        """
        Returns the ID of the formula from the 'id' attribute of the element.

        Returns:
            str: The ID of the formula, or None if the 'id' attribute is not found.
        """
        return self.element.get("id")

    @property
    def formula_label(self):
        """
        Returns the label of the formula.

        Returns:
            str: The text content of the <label> element, or None if the element is not found.
        """
        return self.element.findtext("label")

    @property
    def alternative_elements(self):
        """
        Returns a list of element names within the alternatives element.

        Returns:
            list: A list of tag names of the elements within the <alternatives> element,
                  or an empty list if the element is not found.
        """
        alternatives_element = self.element.find('.//alternatives')
        if alternatives_element is not None:
            return [child.tag for child in alternatives_element]
        return []

    @property
    def mml_math(self):
        """
        Returns the MathML representation of the formula, if available.

        Returns:
            str or None: The MathML content as a string, or None if no MathML elements are found.
        """
        namespace = "{http://www.w3.org/1998/Math/MathML}"
        formula = self.element.find(f".//{namespace}math")
        if formula is not None:
            return ET.tostring(formula, encoding="unicode", method="text").strip()

    @property
    def mml_math_id(self):
        """
        Returns the ID attribute of the MathML element, if available.

        Returns:
            str or None: The ID of the mml:math element, or None if not found.
        """
        namespace = "{http://www.w3.org/1998/Math/MathML}"
        formula = self.element.find(f".//{namespace}math")
        if formula is not None:
            return formula.get("id")

    @property
    def tex_math(self):
        """
        Returns the TeX math representation of the formula, if available.

        Returns:
            str or None: The TeX math content as a string, or None if no TeX math elements are found.
        """
        formula = self.element.find(".//tex-math")
        if formula is not None:
            return ET.tostring(formula, encoding="unicode", method="text").strip()

    @property
    def tex_math_id(self):
        """
        Returns the ID attribute of the TeX math element, if available.

        Returns:
            str or None: The ID of the tex-math element, or None if not found.
        """
        formula = self.element.find(".//tex-math")
        if formula is not None:
            return formula.get("id")

    @property
    def graphic(self):
        """
        Returns a list of graphics linked to the formula.

        Returns:
            list: A list of hrefs (as strings) from graphic elements, or an empty list if no graphics are found.
        """
        namespace = "{http://www.w3.org/1999/xlink}"
        return [
            formula.get(f"{namespace}href", "").strip()
            for formula in self.element.findall(".//graphic")
            if formula is not None and formula.get(f"{namespace}href") is not None
        ]

    @property
    def graphic_alt_text(self):
        """
        Extracts alt-text from graphic within alternatives.

        Returns:
            str or None: The text content of <alt-text> if present, None otherwise.
        """
        graphic = self.element.find(".//alternatives/graphic")
        if graphic is not None:
            alt_text_elem = graphic.find("alt-text")
            if alt_text_elem is not None:
                return alt_text_elem.text
        return None

    @property
    def graphic_long_desc(self):
        """
        Extracts long-desc from graphic within alternatives.

        Returns:
            str or None: The text content of <long-desc> if present, None otherwise.
        """
        graphic = self.element.find(".//alternatives/graphic")
        if graphic is not None:
            long_desc_elem = graphic.find("long-desc")
            if long_desc_elem is not None:
                return long_desc_elem.text
        return None

    @property
    def data(self):
        """
        Returns a dictionary containing the formula's data.

        Returns:
            dict: A dictionary with the following keys:
                - 'alternative_parent' (str): The tag name of the parent formula element.
                - 'id' (str or None): The formula ID.
                - 'label' (str or None): The formula label.
                - 'alternative_elements' (list): A list of alternative element names.
                - 'mml_math' (str or None): The MathML content, if available.
                - 'mml_math_id' (str or None): The MathML ID, if available.
                - 'tex_math' (str or None): The TeX math content, if available.
                - 'tex_math_id' (str or None): The TeX math ID, if available.
                - 'graphic' (list): A list of hrefs from graphic elements.
                - 'graphic_alt_text' (str or None): The alt-text from graphic in alternatives.
                - 'graphic_long_desc' (str or None): The long-desc from graphic in alternatives.
        """
        alternative_parent = self.element.tag  # 'disp-formula' or 'inline-formula'
        return {
            "alternative_parent": alternative_parent,
            "id": self.formula_id,
            "label": self.formula_label,
            "alternative_elements": self.alternative_elements,
            "mml_math": self.mml_math,
            "mml_math_id": self.mml_math_id,
            "tex_math": self.tex_math,
            "tex_math_id": self.tex_math_id,
            "graphic": self.graphic
        }


import warnings as _warnings


def __getattr__(name):
    _moved = {
        "ArticleFormulas": "packtools.sps.validation.models.formula",
    }
    if name in _moved:
        import importlib
        _warnings.warn(
            f"{name} has moved to {_moved[name]}. "
            f"Importing from packtools.sps.models.formula is deprecated.",
            DeprecationWarning,
            stacklevel=2,
        )
        mod = importlib.import_module(_moved[name])
        return getattr(mod, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
