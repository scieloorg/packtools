import unittest
from lxml import etree as ET
from packtools.sps.formats.sps_xml.disp_formula import build_disp_formula



class TestBuildDispFormulaId(unittest.TestCase):
    def test_build_disp_formula_id(self):
        data = {
            "formula-id": "e01",
            "formulas": [
                {
                    "{http://www.w3.org/1998/Math/MathML}math": "fórmula no formato mml",
                    "id": "m1"
                }
            ]
        }
        expected_xml_str = (
            '<disp-formula id="e01">'
            '<ns0:math xmlns:ns0="http://www.w3.org/1998/Math/MathML" id="m1">'
            'fórmula no formato mml'
            '</ns0:math>'
            '</disp-formula>'
        )
        disp_formula_elem = build_disp_formula(data)
        generated_xml_str = ET.tostring(disp_formula_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())

    def test_build_disp_formula_id_None(self):
        data = {
            "formula-id": None,
            "formulas": [
                {
                    "{http://www.w3.org/1998/Math/MathML}math": "fórmula no formato mml",
                    "id": "m1"
                }
            ]
        }
        with self.assertRaises(ValueError) as e:
            build_disp_formula(data)
        self.assertEqual(str(e.exception), "formula-id is required")


class TestBuildDispFormulaLabel(unittest.TestCase):
    def test_build_disp_formula_label(self):
        data = {
            "formula-id": "e01",
            "label": "(1)",
            "formulas": [
                {
                    "{http://www.w3.org/1998/Math/MathML}math": "fórmula no formato mml",
                    "id": "m1"
                }
            ]
        }
        expected_xml_str = (
            '<disp-formula id="e01">'
            '<label>(1)</label>'
            '<ns0:math xmlns:ns0="http://www.w3.org/1998/Math/MathML" id="m1">'
            'fórmula no formato mml'
            '</ns0:math>'
            '</disp-formula>'
        )
        disp_formula_elem = build_disp_formula(data)
        generated_xml_str = ET.tostring(disp_formula_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())

    def test_build_disp_formula_label_None(self):
        data = {
            "formula-id": "e01",
            "label": None,
            "formulas": [
                {
                    "{http://www.w3.org/1998/Math/MathML}math": "fórmula no formato mml",
                    "id": "m1"
                }
            ]
        }
        expected_xml_str = (
            '<disp-formula id="e01">'
            '<ns0:math xmlns:ns0="http://www.w3.org/1998/Math/MathML" id="m1">'
            'fórmula no formato mml'
            '</ns0:math>'
            '</disp-formula>'
        )
        disp_formula_elem = build_disp_formula(data)
        generated_xml_str = ET.tostring(disp_formula_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())


class TestBuildDispFormula(unittest.TestCase):
    def test_build_disp_formula_codification_None(self):
        data = {
            "formula-id": "e01",
            "label": "(1)",
            "formulas": None
        }
        with self.assertRaises(ValueError) as e:
            build_disp_formula(data)
        self.assertEqual(str(e.exception), "At least one representation of the formula is required")

    def test_build_disp_formula_codification_id_None(self):
        data = {
            "formula-id": "e01",
            "formulas": [
                {
                    "{http://www.w3.org/1998/Math/MathML}math": "fórmula no formato mml",
                    "id": None
                }
            ]
        }
        expected_xml_str = (
            '<disp-formula id="e01">'
            '<ns0:math xmlns:ns0="http://www.w3.org/1998/Math/MathML">'
            'fórmula no formato mml'
            '</ns0:math>'
            '</disp-formula>'
        )
        disp_formula_elem = build_disp_formula(data)
        generated_xml_str = ET.tostring(disp_formula_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())

    def test_build_disp_formula_formula_None(self):
        data = {
            "formula-id": "e01",
            "label": "(1)",
            "formulas": [
                {
                    "{http://www.w3.org/1998/Math/MathML}math": None,
                    "id": "m1"
                }
            ]
        }
        with self.assertRaises(ValueError) as e:
            build_disp_formula(data)
        self.assertEqual(str(e.exception), "A valid codification type is required.")


class TestBuildDispFormulaAlternatives(unittest.TestCase):
    def test_build_disp_formula_alternatives(self):
        self.maxDiff = None
        data = {
            "formula-id": "e01",
            "label": "(1)",
            "formulas": [
                {
                    "{http://www.w3.org/1998/Math/MathML}math": "fórmula no formato mml",
                    "id": "m1"
                },
                {
                    "tex-math": "fórmula no formato tex",
                    "id": "t1"
                },
                {
                    "graphic": "0103-507X-rbti-26-02-0089-ee10.svg"
                }
            ]
        }
        expected_xml_str = (
            '<disp-formula id="e01">'
            '<label>(1)</label>'
            '<alternatives>'
            '<ns0:math xmlns:ns0="http://www.w3.org/1998/Math/MathML" id="m1">'
            'fórmula no formato mml'
            '</ns0:math>'
            '<tex-math id="t1">'
            'fórmula no formato tex'
            '</tex-math>'
            '<graphic xmlns:ns0="http://www.w3.org/1999/xlink" '
            'ns0:href="0103-507X-rbti-26-02-0089-ee10.svg"/>'
            '</alternatives>'
            '</disp-formula>'
        )
        disp_formula_elem = build_disp_formula(data)
        generated_xml_str = ET.tostring(disp_formula_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())
