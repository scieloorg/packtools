import xml.etree.ElementTree as ET


def build_formula(data):
    """
    data = {
        "codification": "mml:math",
        "id": "m1",
        "text": "fórmula no formato mml"
    }
    """
    required_fields = ("codification", "id", "text")
    missing_fields = [field for field in required_fields if not data.get(field)]

    if missing_fields:
        raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")

    codification = data["codification"]
    formula_id = data["id"]
    formula_text = data["text"]

    valid_codifications = ("mml:math", "tex-math", "graphic")

    if codification not in valid_codifications:
        raise KeyError(f"Invalid codification. Expected values are: {', '.join(valid_codifications)}")

    if codification == "graphic":
        attributes = {"xlink:href": formula_text, "id": formula_id}
    else:
        attributes = {"id": formula_id}

    formula_elem = ET.Element(codification, attrib=attributes)

    if codification != "graphic":
        formula_elem.text = formula_text

    return formula_elem


def build_disp_formula(data):
    """
    data = {
        "formula-id": "e01",
        "label": "(1)",
        "formulas": [
            {
                "codification": "mml:math",
                "id": "m1",
                "text": "fórmula no formato mml"
            },
            {
                "codification": "tex-math",
                "id": "t1",
                "text": "fórmula no formato tex"
            },
            {
                "codification": "graphic",
                "id": "g1",
                "text": "0103-507X-rbti-26-02-0089-ee10.svg"
            }
        ]
    }
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
