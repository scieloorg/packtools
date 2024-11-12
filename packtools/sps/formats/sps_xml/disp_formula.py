import xml.etree.ElementTree as ET


def build_formula(data):
    """
    data = {
        "mml:math": "fórmula no formato mml",
        "id": "m1"
    }
    """
    for cod_type in ("mml:math", "tex-math", "graphic"):
        if (cod_value := data.get(cod_type)) and (cod_id := data.get("id")):
            break
    else:
        raise ValueError(f"A valid codification type and ID are required.")

    if cod_type == "graphic":
        attributes = {"xlink:href": cod_value, "id": cod_id}
    else:
        attributes = {"id": cod_id}

    formula_elem = ET.Element(cod_type, attrib=attributes)

    if cod_type != "graphic":
        formula_elem.text = cod_value

    return formula_elem


def build_disp_formula(data):
    """
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
