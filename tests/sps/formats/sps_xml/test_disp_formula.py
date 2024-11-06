import unittest
import xml.etree.ElementTree as ET
from packtools.sps.formats.sps_xml.disp_formula import build_disp_formula



class TestBuildDispFormulaId(unittest.TestCase):
    def test_build_disp_formula_id(self):
        data = {
            "formula-id": "e01",
            "codification": "mml:math",
            "codification-id": "m1",
            "formula": "codificação da fórmula"
        }
        expected_xml_str = (
            '<disp-formula id="e01">'
            '<mml:math id="m1">codificação da fórmula</mml:math>'
            '</disp-formula>'
        )
        disp_formula_elem = build_disp_formula(data)
        generated_xml_str = ET.tostring(disp_formula_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())

    def test_build_disp_formula_id_None(self):
        data = {
            "formula-id": None,
            "codification": "mml:math",
            "codification-id": "m1",
            "formula": "codificação da fórmula"
        }
        with self.assertRaises(ValueError) as e:
            build_disp_formula(data)
        self.assertEqual(str(e.exception), "Missing required fields: formula-id")


class TestBuildDispFormulaLabel(unittest.TestCase):
    def test_build_disp_formula_label(self):
        data = {
            "formula-id": "e01",
            "label": "(1)",
            "codification": "mml:math",
            "codification-id": "m1",
            "formula": "codificação da fórmula"
        }
        expected_xml_str = (
            '<disp-formula id="e01">'
            '<label>(1)</label>'
            '<mml:math id="m1">codificação da fórmula</mml:math>'
            '</disp-formula>'
        )
        disp_formula_elem = build_disp_formula(data)
        generated_xml_str = ET.tostring(disp_formula_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())

    def test_build_disp_formula_label_None(self):
        data = {
            "formula-id": "e01",
            "label": None,
            "codification": "mml:math",
            "codification-id": "m1",
            "formula": "codificação da fórmula"
        }
        expected_xml_str = (
            '<disp-formula id="e01">'
            '<mml:math id="m1">codificação da fórmula</mml:math>'
            '</disp-formula>'
        )
        disp_formula_elem = build_disp_formula(data)
        generated_xml_str = ET.tostring(disp_formula_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())


class TestBuildDispFormula(unittest.TestCase):
    def test_build_disp_formula_codification_None(self):
        data = {
            "formula-id": "e01",
            "codification": None,
            "codification-id": "m1",
            "formula": "codificação da fórmula"
        }
        with self.assertRaises(ValueError) as e:
            build_disp_formula(data)
        self.assertEqual(str(e.exception), "Missing required fields: codification")

    def test_build_disp_formula_codification_id_None(self):
        data = {
            "formula-id": "e01",
            "codification": "tex-math",
            "codification-id": None,
            "formula": "codificação da fórmula"
        }
        with self.assertRaises(ValueError) as e:
            build_disp_formula(data)
        self.assertEqual(str(e.exception), "Missing required fields: codification-id")

    def test_build_disp_formula_formula_None(self):
        data = {
            "formula-id": "e01",
            "codification": "tex-math",
            "codification-id":"m1",
            "formula": None
        }
        with self.assertRaises(ValueError) as e:
            build_disp_formula(data)
        self.assertEqual(str(e.exception), "Missing required fields: formula")


class TestBuildDispFormulaAlternatives(unittest.TestCase):
    def test_build_disp_formula_alternatives(self):
        data = {
            "formula-id": "e01",
            "codification": "tex-math",
            "codification-id": "m1",
            "formula": "codificação da fórmula",
            "alternative-link": "0103-507X-rbti-26-02-0089-ee10.svg"
        }
        expected_xml_str = (
            '<disp-formula id="e01">'
            '<alternatives>'
            '<tex-math id="m1">codificação da fórmula</tex-math>'
            '<graphic xlink:href="0103-507X-rbti-26-02-0089-ee10.svg" />'
            '</alternatives>'
            '</disp-formula>'
        )
        disp_formula_elem = build_disp_formula(data)
        generated_xml_str = ET.tostring(disp_formula_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())
