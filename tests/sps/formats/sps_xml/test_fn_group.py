import unittest
from lxml import etree as ET
from packtools.sps.formats.sps_xml.fn_group import build_fn_group, build_fn


class TestBuildFnGroup(unittest.TestCase):
    def test_build_fn_group(self):
        data = {
            "title": None
        }
        expected_xml_str = (
            '<fn-group/>'
        )
        fn_group_elem = build_fn_group(data)
        generated_xml_str = ET.tostring(fn_group_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())

    def test_build_fn_group_title(self):
        data = {
            "title": "Notas",
        }
        expected_xml_str = (
            '<fn-group>'
            '<title>Notas</title>'
            '</fn-group>'
        )
        fn_group_elem = build_fn_group(data)
        generated_xml_str = ET.tostring(fn_group_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())

    def test_build_fn_group_fns(self):
        data = {
            "title": "Notas",
            "fns": [
                {
                    "fn_type": "supported-by",
                    "fn_id": "fn01",
                    "fn_label": "*",
                    "fn_p": "Vivamus sodales fermentum lorem,..."
                }
            ]
        }
        expected_xml_str = (
            '<fn-group>'
            '<title>Notas</title>'
            '<fn fn-type="supported-by" id="fn01">'
            '<label>*</label>'
            '<p>Vivamus sodales fermentum lorem,...</p>'
            '</fn>'
            '</fn-group>'
        )
        fn_group_elem = build_fn_group(data)
        generated_xml_str = ET.tostring(fn_group_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())


class TestBuildFnType(unittest.TestCase):
    def test_build_fn_type(self):
        data = {
            "fn_type": "supported-by",
        }
        expected_xml_str = (
            '<fn fn-type="supported-by"/>'
        )
        fn_elem = build_fn(data)
        generated_xml_str = ET.tostring(fn_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())

    def test_build_fn_type_None(self):
        data = {
            "fn_type": None,
        }
        with self.assertRaises(ValueError) as e:
            build_fn(data)
        self.assertEqual(str(e.exception), "fn type is required")


class TestBuildFnId(unittest.TestCase):
    def test_build_fn_id(self):
        data = {
            "fn_type": "supported-by",
            "fn_id": "fn01",
        }
        expected_xml_str = (
            '<fn fn-type="supported-by" id="fn01"/>'
        )
        fn_elem = build_fn(data)
        generated_xml_str = ET.tostring(fn_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())

    def test_build_fn_id_None(self):
        data = {
            "fn_type": "supported-by",
            "fn_id": None
        }
        expected_xml_str = (
            '<fn fn-type="supported-by"/>'
        )
        fn_elem = build_fn(data)
        generated_xml_str = ET.tostring(fn_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())


class TestBuildFnLabel(unittest.TestCase):
    def test_build_fn_label(self):
        data = {
            "fn_type": "supported-by",
            "fn_id": "fn01",
            "fn_label": "*",
        }
        expected_xml_str = (
            '<fn fn-type="supported-by" id="fn01">'
            '<label>*</label>'
            '</fn>'
        )
        fn_elem = build_fn(data)
        generated_xml_str = ET.tostring(fn_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())

    def test_build_fn_label_None(self):
        data = {
            "fn_type": "supported-by",
            "fn_id": "fn01",
            "fn_label": None,
        }
        expected_xml_str = (
            '<fn fn-type="supported-by" id="fn01"/>'
        )
        fn_elem = build_fn(data)
        generated_xml_str = ET.tostring(fn_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())


class TestBuildFnP(unittest.TestCase):
    def test_build_fn_p(self):
        data = {
            "fn_type": "supported-by",
            "fn_id": "fn01",
            "fn_p": "Vivamus sodales fermentum lorem,..."
        }
        expected_xml_str = (
            '<fn fn-type="supported-by" id="fn01">'
            '<p>Vivamus sodales fermentum lorem,...</p>'
            '</fn>'
        )
        fn_elem = build_fn(data)
        generated_xml_str = ET.tostring(fn_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())

    def test_build_fn_p_None(self):
        data = {
            "fn_type": "supported-by",
            "fn_id": "fn01",
            "fn_p": None
        }
        expected_xml_str = (
            '<fn fn-type="supported-by" id="fn01"/>'
        )
        fn_elem = build_fn(data)
        generated_xml_str = ET.tostring(fn_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())
