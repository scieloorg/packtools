import xml.etree.ElementTree as ET


def build_formula(data):
    """
    Builds an XML element for a formula representation.

    Args:
        data (dict): A dictionary containing formula details with the following keys:
            - "mml:math" (str): Formula in MathML format (optional).
            - "tex-math" (str): Formula in TeX format (optional).
            - "graphic" (str): Path to a graphical representation of the formula (optional).
            - "id" (str): Unique identifier for the formula (required).

    Returns:
        xml.etree.ElementTree.Element: An XML element representing the formula.

    Raises:
        ValueError: If neither a valid formula representation nor an "id" is provided.

    Example input:
        data = {
            "mml:math": "fórmula no formato mml",
            "id": "m1"
        }

    Example output:
        <mml:math id="m1">fórmula no formato mml</mml:math>

    """
    for cod_type in ("mml:math", "tex-math", "graphic"):
        if cod_value := data.get(cod_type):
            cod_id = data.get("id")
            break
    else:
        raise ValueError("A valid codification type is required.")

    attributes = {}
    if cod_type == "graphic":
        attributes["xlink:href"] = cod_value
    elif cod_id:
        attributes["id"] = cod_id

    formula_elem = ET.Element(cod_type, attrib=attributes)

    if cod_type != "graphic":
        formula_elem.text = cod_value

    return formula_elem


def build_disp_formula(data):
    """
    Builds an XML element for a display formula, including its label and alternative representations.

    Args:
        data (dict): A dictionary containing details of the display formula with the following keys:
            - "formula-id" (str): Unique identifier for the display formula (required).
            - "label" (str): Label associated with the formula, e.g., "(1)" (optional).
            - "formulas" (list): A list of dictionaries, each representing a formula in one of the formats
              (see `build_formula` for the format details). At least one formula representation is required.

    Returns:
        xml.etree.ElementTree.Element: An XML element representing the display formula.

    Raises:
        ValueError: If "formula-id" is missing or if no formulas are provided.

    Example input:
        data = {
            "formula-id": "e01",
            "label": "(1)",
            "formulas": [
                {
                    "mml:math": "fórmula no formato mml",
                    "id": "m1"
                },
                {
                    "tex-math": "fórmula no formato tex",
                    "id": "t1"
                },
                {
                    "graphic": "0103-507X-rbti-26-02-0089-ee10.svg",
                    "id": "g1"
                }
            ]
        }

    Example output:
        <disp-formula id="e01">
            <label>(1)</label>
            <alternatives>
                <mml:math id="m1">fórmula no formato mml</mml:math>
                <tex-math id="t1">fórmula no formato tex</tex-math>
                <graphic xlink:href="0103-507X-rbti-26-02-0089-ee10.svg" id="g1" />
            </alternatives>
        </disp-formula>
    """
    # build disp-formula
    if not (formula_id := data.get("formula-id")):
        raise ValueError("formula-id is required")

    disp_formula_elem = ET.Element("disp-formula", attrib={"id": formula_id})

    # add label
    if label := data.get("label"):
        ET.SubElement(disp_formula_elem, "label").text = label

    formulas = data.get("formulas", [])
    if not formulas:
        raise ValueError("At least one representation of the formula is required")

    if len(formulas) == 1:
        # add one formula
        disp_formula_elem.append(build_formula(formulas[0]))
    else:
        # add alternatives (many formulas)
        alternatives_elem = ET.SubElement(disp_formula_elem, "alternatives")
        for formula in formulas:
            alternatives_elem.append(build_formula(formula))

    return disp_formula_elem
