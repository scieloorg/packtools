"""
data = {
    "formula-id": "e01",
    "label": "(1)",
    "codification": "mml:math",
    "codification-id": "m1",
    "formula": "<mml:mrow><mml:msub><mml:mi>q</mml:mi><mml:mi>c</mml:mi></mml:msub><mml:mo>=</mml:mo><mml:mi>h</mml:mi>
    <mml:mrow><mml:mo>(</mml:mo><mml:mrow><mml:mi>T</mml:mi><mml:mo>−</mml:mo><mml:msub><mml:mi>T</mml:mi><mml:mn>0
    </mml:mn></mml:msub></mml:mrow><mml:mo>)</mml:mo></mml:mrow></mml:mrow></mml:math>",
    "alternative-link": "0103-507X-rbti-26-02-0089-ee10.svg"
}
"""

import xml.etree.ElementTree as ET


def build_disp_formula(data):
    required_fields = ["formula-id", "codification", "codification-id", "formula"]
    missing_fields = [field for field in required_fields if not data.get(field)]

    if missing_fields:
        raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")

    disp_formula_elem = ET.Element("disp-formula", attrib={"id": data["formula-id"]})

    if label := data.get("label"):
        label_elem = ET.SubElement(disp_formula_elem, "label")
        label_elem.text = label

    codification_elem = ET.Element(data["codification"], attrib={"id": data["codification-id"]})
    codification_elem.text = data["formula"]

    if alternative_link := data.get("alternative-link"):
        alternative_elem = ET.SubElement(disp_formula_elem, "alternatives")
        alternative_elem.append(codification_elem)
        ET.SubElement(alternative_elem, "graphic", attrib={"xlink:href": alternative_link})
    else:
        disp_formula_elem.append(codification_elem)

    return disp_formula_elem
