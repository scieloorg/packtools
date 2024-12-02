import unittest
from lxml import etree as ET
from packtools.sps.formats.sps_xml.aff import build_aff


class TestBuildAffId(unittest.TestCase):
    def test_build_aff_aff_id(self):
        data = {
            "aff_id": "aff01"
        }
        expected_xml_str = (
            '<aff id="aff01"/>'
        )
        aff_elem = build_aff(data)
        generated_xml_str = ET.tostring(aff_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())

    def test_build_aff_aff_id_None(self):
        data = {
            "aff_id": None
        }

        aff_elem = build_aff(data)
        self.assertIsNone(aff_elem)


class TestBuildAffLabel(unittest.TestCase):
    def test_build_aff_label(self):
        data = {
            "aff_id": "aff01",
            "label": "1",
        }
        expected_xml_str = (
            '<aff id="aff01">'
            '<label>1</label>'
            '</aff>'
        )
        aff_elem = build_aff(data)
        generated_xml_str = ET.tostring(aff_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())

    def test_build_aff_label_None(self):
        data = {
            "aff_id": "aff01",
            "label": None,
        }

        expected_xml_str = (
            '<aff id="aff01"/>'
        )
        aff_elem = build_aff(data)
        generated_xml_str = ET.tostring(aff_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())


class TestBuildAffOrgname(unittest.TestCase):
    def test_build_aff_orgname(self):
        data = {
            "aff_id": "aff01",
            "orgname": "Fundação Oswaldo Cruz",
        }
        expected_xml_str = (
            '<aff id="aff01">'
            '<institution content-type="orgname">Fundação Oswaldo Cruz</institution>'
            '</aff>'
        )
        aff_elem = build_aff(data)
        generated_xml_str = ET.tostring(aff_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())

    def test_build_aff_orgname_None(self):
        data = {
            "aff_id": "aff01",
            "orgname": None,
        }

        expected_xml_str = (
            '<aff id="aff01"/>'
        )
        aff_elem = build_aff(data)
        generated_xml_str = ET.tostring(aff_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())


class TestBuildAffOrgdiv1(unittest.TestCase):
    def test_build_aff_orgdiv1(self):
        data = {
            "aff_id": "aff01",
            "orgdiv1": "Escola Nacional de Saúde Pública Sérgio Arouca"
        }
        expected_xml_str = (
            '<aff id="aff01">'
            '<institution content-type="orgdiv1">Escola Nacional de Saúde Pública Sérgio Arouca</institution>'
            '</aff>'
        )
        aff_elem = build_aff(data)
        generated_xml_str = ET.tostring(aff_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())

    def test_build_aff_orgdiv1_None(self):
        data = {
            "aff_id": "aff01",
            "orgdiv1": None
        }

        expected_xml_str = (
            '<aff id="aff01"/>'
        )
        aff_elem = build_aff(data)
        generated_xml_str = ET.tostring(aff_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())


class TestBuildAffOrgdiv2(unittest.TestCase):
    def test_build_aff_orgdiv2(self):
        data = {
            "aff_id": "aff01",
            "orgdiv2": "Centro de Estudos da Saúde do Trabalhador e Ecologia Humana"
        }
        expected_xml_str = (
            '<aff id="aff01">'
            '<institution content-type="orgdiv2">Centro de Estudos da Saúde do Trabalhador e Ecologia Humana</institution>'
            '</aff>'
        )
        aff_elem = build_aff(data)
        generated_xml_str = ET.tostring(aff_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())

    def test_build_aff_orgdiv2_None(self):
        data = {
            "aff_id": "aff01",
            "orgdiv2": None
        }

        expected_xml_str = (
            '<aff id="aff01"/>'
        )
        aff_elem = build_aff(data)
        generated_xml_str = ET.tostring(aff_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())


class TestBuildAffOriginal(unittest.TestCase):
    def test_build_aff_original(self):
        data = {
            "aff_id": "aff01",
            "original": "Prof. da Fundação Oswaldo Cruz"
        }
        expected_xml_str = (
            '<aff id="aff01">'
            '<institution content-type="original">Prof. da Fundação Oswaldo Cruz</institution>'
            '</aff>'
        )
        aff_elem = build_aff(data)
        generated_xml_str = ET.tostring(aff_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())

    def test_build_aff_original_None(self):
        data = {
            "aff_id": "aff01",
            "original": None
        }

        expected_xml_str = (
            '<aff id="aff01"/>'
        )
        aff_elem = build_aff(data)
        generated_xml_str = ET.tostring(aff_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())


class TestBuildAffCountry(unittest.TestCase):
    def test_build_aff_country(self):
        data = {
            "aff_id": "aff01",
            "country_code": "BR",
            "country_name": "Brazil",
        }
        expected_xml_str = (
            '<aff id="aff01">'
            '<country country="BR">Brazil</country>'
            '</aff>'
        )
        aff_elem = build_aff(data)
        generated_xml_str = ET.tostring(aff_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())

    def test_build_aff_country_None(self):
        data = {
            "aff_id": "aff01",
            "country_code": None,
            "country_name": None,
        }

        expected_xml_str = (
            '<aff id="aff01"/>'
        )
        aff_elem = build_aff(data)
        generated_xml_str = ET.tostring(aff_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())


class TestBuildAffAddrline(unittest.TestCase):
    def test_build_aff_addrline(self):
        data = {
            "aff_id": "aff01",
            "city": "Manguinhos",
            "state": "RJ",
        }
        expected_xml_str = (
            '<aff id="aff01">'
            '<addr-line>'
            '<city>Manguinhos</city>'
            '<state>RJ</state>'
            '</addr-line>'
            '</aff>'
        )
        aff_elem = build_aff(data)
        generated_xml_str = ET.tostring(aff_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())

    def test_build_aff_addrline_None(self):
        data = {
            "aff_id": "aff01",
            "city": None,
            "state": None
        }

        expected_xml_str = (
            '<aff id="aff01"/>'
        )
        aff_elem = build_aff(data)
        generated_xml_str = ET.tostring(aff_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())


class TestBuildAffEmail(unittest.TestCase):
    def test_build_aff_email(self):
        data = {
            "aff_id": "aff01",
            "email": "maurosilva@foo.com"
        }
        expected_xml_str = (
            '<aff id="aff01">'
            '<email>maurosilva@foo.com</email>'
            '</aff>'
        )
        aff_elem = build_aff(data)
        generated_xml_str = ET.tostring(aff_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())

    def test_build_aff_email_None(self):
        data = {
            "aff_id": "aff01",
            "email": None
        }

        expected_xml_str = (
            '<aff id="aff01"/>'
        )
        aff_elem = build_aff(data)
        generated_xml_str = ET.tostring(aff_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())
