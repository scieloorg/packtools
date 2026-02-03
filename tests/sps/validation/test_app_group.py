import unittest
from lxml import etree

from packtools.sps.validation.app_group import AppValidation


class AppValidationTest(unittest.TestCase):
    def setUp(self):
        self.params = {
            "app_existence_error_level": "WARNING",
            "app_id_error_level": "CRITICAL",
            "app_label_error_level": "CRITICAL",
            "app_group_wrapper_error_level": "CRITICAL",
            "app_group_occurrence_error_level": "CRITICAL",
        }

    def test_app_validation_no_app_elements(self):
        """Teste de validação quando não há elementos <app>"""
        self.maxDiff = None
        xmltree = etree.fromstring(
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'dtd-version="1.0" article-type="research-article" xml:lang="pt">'
            "<body>"
            "<p>Some text content without apps.</p>"
            "</body>"
            "</article>"
        )
        obtained = list(AppValidation(xmltree, self.params).validate_app_existence())

        self.assertEqual(len(obtained), 1)
        self.assertEqual(obtained[0]["response"], "WARNING")
        self.assertIn("app", obtained[0]["title"].lower())

    def test_app_validation_with_app_elements(self):
        """Teste de validação com elementos <app> válidos"""
        self.maxDiff = None
        xmltree = etree.fromstring(
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'dtd-version="1.0" article-type="research-article" xml:lang="pt">'
            "<back>"
            "<app-group>"
            '<app id="app1">'
            "<label>Appendix 1</label>"
            "<p>Some supplementary content.</p>"
            "</app>"
            "</app-group>"
            "</back>"
            "</article>"
        )
        obtained = list(AppValidation(xmltree, self.params).validate_app_existence())

        self.assertEqual(len(obtained), 1)
        self.assertEqual(obtained[0]["response"], "OK")
        self.assertEqual(obtained[0]["got_value"], "app1")


class TestAppIdValidation(unittest.TestCase):
    """Testes para validação de @id obrigatório em <app>"""

    def setUp(self):
        self.params = {
            "app_existence_error_level": "WARNING",
            "app_id_error_level": "CRITICAL",
            "app_label_error_level": "CRITICAL",
            "app_group_wrapper_error_level": "CRITICAL",
            "app_group_occurrence_error_level": "CRITICAL",
        }

    def test_app_with_id_valid(self):
        """<app> com @id válido"""
        xml = etree.fromstring(
            '<article xmlns:xlink="http://www.w3.org/1999/xlink">'
            "<back>"
            "<app-group>"
            '<app id="app1">'
            "<label>Appendix 1</label>"
            "</app>"
            "</app-group>"
            "</back>"
            "</article>"
        )
        obtained = list(AppValidation(xml, self.params).validate_app_id())

        self.assertEqual(len(obtained), 1)
        self.assertEqual(obtained[0]["response"], "OK")
        self.assertEqual(obtained[0]["got_value"], "app1")

    def test_app_without_id_invalid(self):
        """<app> sem @id deve gerar erro CRITICAL"""
        xml = etree.fromstring(
            '<article xmlns:xlink="http://www.w3.org/1999/xlink">'
            "<back>"
            "<app-group>"
            "<app>"  # Sem @id
            "<label>Appendix 1</label>"
            "</app>"
            "</app-group>"
            "</back>"
            "</article>"
        )
        obtained = list(AppValidation(xml, self.params).validate_app_id())

        self.assertEqual(len(obtained), 1)
        self.assertEqual(obtained[0]["response"], "CRITICAL")
        self.assertIn("@id", obtained[0]["title"])

    def test_multiple_apps_with_and_without_id(self):
        """Múltiplos <app>, alguns sem @id"""
        xml = etree.fromstring(
            '<article xmlns:xlink="http://www.w3.org/1999/xlink">'
            "<back>"
            "<app-group>"
            '<app id="app1"><label>App 1</label></app>'
            "<app><label>App 2</label></app>"  # Sem @id
            '<app id="app3"><label>App 3</label></app>'
            "</app-group>"
            "</back>"
            "</article>"
        )
        obtained = list(AppValidation(xml, self.params).validate_app_id())

        self.assertEqual(len(obtained), 3)

        # app1: OK
        self.assertEqual(obtained[0]["response"], "OK")

        # app2: CRITICAL (sem id)
        self.assertEqual(obtained[1]["response"], "CRITICAL")

        # app3: OK
        self.assertEqual(obtained[2]["response"], "OK")


class TestAppLabelValidation(unittest.TestCase):
    """Testes para validação de <label> obrigatório em <app>"""

    def setUp(self):
        self.params = {
            "app_existence_error_level": "WARNING",
            "app_id_error_level": "CRITICAL",
            "app_label_error_level": "CRITICAL",
            "app_group_wrapper_error_level": "CRITICAL",
            "app_group_occurrence_error_level": "CRITICAL",
        }

    def test_app_with_label_valid(self):
        """<app> com <label> válido"""
        xml = etree.fromstring(
            '<article xmlns:xlink="http://www.w3.org/1999/xlink">'
            "<back>"
            "<app-group>"
            '<app id="app1">'
            "<label>Appendix 1</label>"
            "</app>"
            "</app-group>"
            "</back>"
            "</article>"
        )
        obtained = list(AppValidation(xml, self.params).validate_app_label())

        self.assertEqual(len(obtained), 1)
        self.assertEqual(obtained[0]["response"], "OK")
        self.assertEqual(obtained[0]["got_value"], "Appendix 1")

    def test_app_without_label_invalid(self):
        """<app> sem <label> deve gerar erro CRITICAL"""
        xml = etree.fromstring(
            '<article xmlns:xlink="http://www.w3.org/1999/xlink">'
            "<back>"
            "<app-group>"
            '<app id="app1">'
            "<p>Content without label</p>"
            "</app>"
            "</app-group>"
            "</back>"
            "</article>"
        )
        obtained = list(AppValidation(xml, self.params).validate_app_label())

        self.assertEqual(len(obtained), 1)
        self.assertEqual(obtained[0]["response"], "CRITICAL")
        self.assertIn("label", obtained[0]["title"].lower())


class TestAppGroupWrapperValidation(unittest.TestCase):
    """Testes para validação de <app-group> como wrapper obrigatório"""

    def setUp(self):
        self.params = {
            "app_existence_error_level": "WARNING",
            "app_id_error_level": "CRITICAL",
            "app_label_error_level": "CRITICAL",
            "app_group_wrapper_error_level": "CRITICAL",
            "app_group_occurrence_error_level": "CRITICAL",
        }

    def test_app_inside_app_group_valid(self):
        """<app> dentro de <app-group> é válido"""
        xml = etree.fromstring(
            '<article xmlns:xlink="http://www.w3.org/1999/xlink">'
            "<back>"
            "<app-group>"
            '<app id="app1"><label>App</label></app>'
            "</app-group>"
            "</back>"
            "</article>"
        )
        obtained = list(AppValidation(xml, self.params).validate_app_group_wrapper())

        # Não deve gerar erro
        errors = [r for r in obtained if r["response"] != "OK"]
        self.assertEqual(len(errors), 0)

    def test_orphan_app_invalid(self):
        """<app> órfão (fora de <app-group>) deve gerar erro CRITICAL"""
        xml = etree.fromstring(
            '<article xmlns:xlink="http://www.w3.org/1999/xlink">'
            "<back>"
            '<app id="app1"><label>Orphan App</label></app>'
            "</back>"
            "</article>"
        )
        obtained = list(AppValidation(xml, self.params).validate_app_group_wrapper())

        self.assertGreater(len(obtained), 0)
        self.assertEqual(obtained[0]["response"], "CRITICAL")
        self.assertIn("wrapper", obtained[0]["title"].lower())

    def test_multiple_app_groups_invalid(self):
        """Múltiplos <app-group> devem gerar erro CRITICAL"""
        xml = etree.fromstring(
            '<article xmlns:xlink="http://www.w3.org/1999/xlink">'
            "<back>"
            "<app-group>"
            '<app id="app1"><label>App 1</label></app>'
            "</app-group>"
            "<app-group>"
            '<app id="app2"><label>App 2</label></app>'
            "</app-group>"
            "</back>"
            "</article>"
        )
        obtained = list(AppValidation(xml, self.params).validate_app_group_wrapper())

        self.assertGreater(len(obtained), 0)
        # Deve ter erro sobre múltiplos app-groups
        multiple_errors = [r for r in obtained if "Single" in r.get("title", "")]
        self.assertGreater(len(multiple_errors), 0)
        self.assertEqual(multiple_errors[0]["response"], "CRITICAL")

    def test_single_app_needs_app_group(self):
        """Mesmo um único <app> precisa estar em <app-group>"""
        xml = etree.fromstring(
            '<article xmlns:xlink="http://www.w3.org/1999/xlink">'
            "<back>"
            '<app id="app1"><label>Single App</label></app>'
            "</back>"
            "</article>"
        )
        obtained = list(AppValidation(xml, self.params).validate_app_group_wrapper())

        self.assertGreater(len(obtained), 0)
        self.assertEqual(obtained[0]["response"], "CRITICAL")

    def test_orphan_app_and_multiple_app_groups(self):
        """Apps órfãos E múltiplos <app-group> devem gerar ambos os erros"""
        xml = etree.fromstring(
            '<article xmlns:xlink="http://www.w3.org/1999/xlink">'
            "<back>"
            '<app id="orphan"><label>Orphan App</label></app>'
            "<app-group>"
            '<app id="app1"><label>App 1</label></app>'
            "</app-group>"
            "<app-group>"
            '<app id="app2"><label>App 2</label></app>'
            "</app-group>"
            "</back>"
            "</article>"
        )

        obtained = list(AppValidation(xml, self.params).validate_app_group_wrapper())

        # Deve ter pelo menos 2 erros (órfão + múltiplos app-groups)
        self.assertGreaterEqual(len(obtained), 2)

        # Deve ter erro sobre app órfão
        orphan_errors = [r for r in obtained if "wrapper required" in r.get("title", "")]
        self.assertEqual(len(orphan_errors), 1)
        self.assertEqual(orphan_errors[0]["response"], "CRITICAL")

        # Deve ter erro sobre múltiplos app-groups
        multiple_errors = [r for r in obtained if "Single" in r.get("title", "")]
        self.assertEqual(len(multiple_errors), 1)
        self.assertEqual(multiple_errors[0]["response"], "CRITICAL")


class TestI18nSupport(unittest.TestCase):
    """Testes para suporte de internacionalização"""

    def setUp(self):
        self.params = {
            "app_existence_error_level": "WARNING",
            "app_id_error_level": "CRITICAL",
            "app_label_error_level": "CRITICAL",
            "app_group_wrapper_error_level": "CRITICAL",
            "app_group_occurrence_error_level": "CRITICAL",
        }

    def test_all_validations_have_advice_text(self):
        """Todas validações devem ter advice_text quando inválidas"""
        xml = etree.fromstring(
            '<article xmlns:xlink="http://www.w3.org/1999/xlink">'
            "<back>"
            "<app-group>"
            "<app>"  # Sem id, sem label
            "<p>Content</p>"
            "</app>"
            "</app-group>"
            "</back>"
            "</article>"
        )
        obtained = list(AppValidation(xml, self.params).validate())

        # Filtrar validações com erro
        errors = [v for v in obtained if v["response"] not in ["OK", "WARNING"]]

        # Todas devem ter adv_text
        for validation in errors:
            self.assertIn("adv_text", validation)
            if validation["adv_text"]:  # Se não for None
                self.assertIsInstance(validation["adv_text"], str)

    def test_advice_params_present(self):
        """Validações devem ter advice_params quando inválidas"""
        xml = etree.fromstring(
            '<article xmlns:xlink="http://www.w3.org/1999/xlink">'
            "<back>"
            '<app id="app1">'  # Sem label
            "<p>Content</p>"
            "</app>"
            "</back>"
            "</article>"
        )
        obtained = list(AppValidation(xml, self.params).validate())

        errors = [v for v in obtained if v["response"] != "OK"]

        for validation in errors:
            self.assertIn("adv_params", validation)
            if validation["adv_params"]:  # Se não for None
                self.assertIsInstance(validation["adv_params"], dict)


class TestCompleteValidation(unittest.TestCase):
    """Testes de validação completa"""

    def setUp(self):
        self.params = {
            "app_existence_error_level": "WARNING",
            "app_id_error_level": "CRITICAL",
            "app_label_error_level": "CRITICAL",
            "app_group_wrapper_error_level": "CRITICAL",
            "app_group_occurrence_error_level": "CRITICAL",
        }

    def test_perfect_app_group(self):
        """<app-group> perfeito deve passar em todas validações"""
        xml = etree.fromstring(
            '<article xmlns:xlink="http://www.w3.org/1999/xlink">'
            "<back>"
            "<app-group>"
            '<app id="app1">'
            "<label>Appendix 1</label>"
            "<p>Perfect content</p>"
            "</app>"
            "</app-group>"
            "</back>"
            "</article>"
        )
        obtained = list(AppValidation(xml, self.params).validate())

        # Deve ter validações OK
        ok_validations = [v for v in obtained if v["response"] == "OK"]
        self.assertGreater(len(ok_validations), 0)

        # Não deve ter CRITICAL
        critical_errors = [v for v in obtained if v["response"] == "CRITICAL"]
        self.assertEqual(len(critical_errors), 0)


if __name__ == "__main__":
    unittest.main()
