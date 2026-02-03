import unittest
from lxml import etree
from packtools.sps.validation.accessibility_data import XMLAccessibilityDataValidation


class TestAccessibilityDataValidation(unittest.TestCase):

    def setUp(self):
        self.params = {
            "alt_text_exist_error_level": "WARNING",
            "alt_text_content_error_level": "CRITICAL",
            "alt_text_media_restriction_error_level": "ERROR",
            "alt_text_duplication_error_level": "WARNING",
            "decorative_alt_text_error_level": "WARNING",
            "long_desc_exist_error_level": "WARNING",
            "long_desc_content_error_level": "CRITICAL",
            "long_desc_media_restriction_error_level": "ERROR",
            "long_desc_duplication_error_level": "WARNING",
            "long_desc_occurrence_error_level": "ERROR",
            "long_desc_null_incompatibility_error_level": "WARNING",
            "transcript_error_level": "WARNING",
            "content_type_error_level": "CRITICAL",
            "speaker_speech_error_level": "WARNING",
            "structure_error_level": "CRITICAL",
            "content_types": ["machine-generated"],
        }

    def test_validate_alt_text_failure(self):
        """Fails when <alt-text> exceeds 120 characters."""
        xml_content = """
        <body>
            <media>
                <alt-text>This is an alternative text that is intentionally made longer than one hundred and twenty characters to ensure that the validation fails as expected.</alt-text>
            </media>
        </body>
        """
        xml_node = etree.fromstring(xml_content)
        validator = XMLAccessibilityDataValidation(xml_node, self.params)
        results = list(validator.validate())

        # Filtrar por título ao invés de usar índice fixo
        alt_text_results = [r for r in results if r["title"] == "<alt-text>" and r.get("sub_item") is None]
        self.assertEqual(len(alt_text_results), 1)
        response = alt_text_results[0]

        self.assertEqual(response["response"], "CRITICAL")

    def test_validate_long_desc_failure(self):
        """Fails when <long-desc> is shorter than 120 characters."""
        xml_content = """
        <body>
            <media>
                <long-desc>Short description.</long-desc>
            </media>
        </body>
        """
        xml_node = etree.fromstring(xml_content)
        validator = XMLAccessibilityDataValidation(xml_node, self.params)
        results = list(validator.validate())

        long_desc_results = [r for r in results if r["title"] == "<long-desc>" and r.get("sub_item") is None]
        self.assertEqual(len(long_desc_results), 1)
        response = long_desc_results[0]

        self.assertEqual(response["response"], "CRITICAL")

    # ========== NOVOS TESTES: DUPLICAÇÃO ==========

    def test_long_desc_duplication_with_label(self):
        """NOVO: Valida duplicação entre long-desc e label"""
        xml_content = """
        <body>
            <fig>
                <label>Figure 1</label>
                <graphic>
                    <long-desc>Figure 1</long-desc>
                </graphic>
            </fig>
        </body>
        """
        xml_node = etree.fromstring(xml_content)
        validator = XMLAccessibilityDataValidation(xml_node, self.params)
        results = list(validator.validate())

        duplication = [r for r in results if r.get("sub_item") == "label duplication"]
        self.assertEqual(len(duplication), 1)
        self.assertEqual(duplication[0]["response"], "WARNING")
        self.assertIn("duplicates <label>", duplication[0]["advice"])

    def test_long_desc_duplication_with_multiple_spaces(self):
        """Valida que espaços múltiplos não impedem detecção de duplicação"""
        xml_content = """
        <body>
            <fig>
                <graphic>
                    <long-desc>Figura  mostra  crescimento  da  população</long-desc>
                </graphic>
                <caption>
                    <title>Figura mostra crescimento da população</title>
                </caption>
            </fig>
        </body>
        """
        xml_node = etree.fromstring(xml_content)
        validator = XMLAccessibilityDataValidation(xml_node, self.params)
        results = list(validator.validate())

        caption_dup = [r for r in results if r.get("sub_item") == "caption duplication" and r["response"] == "WARNING"]
        self.assertEqual(len(caption_dup), 1)

    def test_long_desc_no_duplication_with_label(self):
        """NOVO: Valida que long-desc diferente de label não gera erro"""
        xml_content = """
        <body>
            <fig>
                <label>Figure 1</label>
                <graphic>
                    <long-desc>This is a detailed description that is completely different from the label and has more than 120 characters to pass validation</long-desc>
                </graphic>
            </fig>
        </body>
        """
        xml_node = etree.fromstring(xml_content)
        validator = XMLAccessibilityDataValidation(xml_node, self.params)
        results = list(validator.validate())

        # Com a correção, deve haver um resultado OK
        label_check = [r for r in results if r.get("sub_item") == "label duplication"]
        self.assertEqual(len(label_check), 1)
        self.assertEqual(label_check[0]["response"], "OK")

    def test_alt_text_not_duplicate_label(self):
        """NOVO: Valida duplicação entre alt-text e label"""
        xml_content = """
        <body>
            <fig>
                <label>Chart 1</label>
                <graphic>
                    <alt-text>Chart 1</alt-text>
                </graphic>
            </fig>
        </body>
        """
        xml_node = etree.fromstring(xml_content)
        validator = XMLAccessibilityDataValidation(xml_node, self.params)
        results = list(validator.validate())

        duplication = [r for r in results if r.get("sub_item") == "duplication check"]
        self.assertEqual(len(duplication), 1)
        self.assertEqual(duplication[0]["response"], "WARNING")

    def test_alt_text_not_duplicate_caption(self):
        """NOVO: Valida duplicação entre alt-text e caption"""
        xml_content = """
        <body>
            <fig>
                <graphic>
                    <alt-text>Growth chart</alt-text>
                </graphic>
                <caption>
                    <title>Growth chart</title>
                </caption>
            </fig>
        </body>
        """
        xml_node = etree.fromstring(xml_content)
        validator = XMLAccessibilityDataValidation(xml_node, self.params)
        results = list(validator.validate())

        duplication = [r for r in results if r.get("sub_item") == "duplication check"]
        self.assertEqual(len(duplication), 1)
        self.assertEqual(duplication[0]["response"], "WARNING")

    def test_alt_text_unique_content_valid(self):
        """NOVO: alt-text único (não copia label/caption) é válido"""
        xml_content = """
        <body>
            <fig>
                <label>Figure 1</label>
                <graphic>
                    <alt-text>Bar chart showing population growth</alt-text>
                </graphic>
                <caption>
                    <title>Population trends</title>
                </caption>
            </fig>
        </body>
        """
        xml_node = etree.fromstring(xml_content)
        validator = XMLAccessibilityDataValidation(xml_node, self.params)
        results = list(validator.validate())

        # Com a correção, deve retornar validação bem-sucedida
        duplication_check = [r for r in results if r.get("sub_item") == "duplication check"]
        self.assertEqual(len(duplication_check), 1)
        self.assertEqual(duplication_check[0]["response"], "OK")

    # ========== NOVOS TESTES: RESTRIÇÕES DE MÍDIA ==========

    def test_alt_text_media_restriction_valid_video(self):
        """NOVO: alt-text em video/mp4 é válido"""
        xml_content = """
        <body>
            <media mimetype="video" mime-subtype="mp4">
                <alt-text>Video demonstrating the procedure</alt-text>
            </media>
        </body>
        """
        xml_node = etree.fromstring(xml_content)
        validator = XMLAccessibilityDataValidation(xml_node, self.params)
        results = list(validator.validate())

        restriction = [r for r in results if r.get("sub_item") == "media restriction" and r["item"] == "alt-text"]
        self.assertEqual(len(restriction), 1)
        self.assertEqual(restriction[0]["response"], "OK")

    def test_alt_text_media_restriction_valid_audio(self):
        """NOVO: alt-text em audio/mp3 é válido"""
        xml_content = """
        <body>
            <media mimetype="audio" mime-subtype="mp3">
                <alt-text>Audio interview with researcher</alt-text>
            </media>
        </body>
        """
        xml_node = etree.fromstring(xml_content)
        validator = XMLAccessibilityDataValidation(xml_node, self.params)
        results = list(validator.validate())

        restriction = [r for r in results if r.get("sub_item") == "media restriction" and r["item"] == "alt-text"]
        self.assertEqual(len(restriction), 1)
        self.assertEqual(restriction[0]["response"], "OK")

    def test_alt_text_media_restriction_invalid_pdf(self):
        """NOVO: alt-text em application/pdf gera erro"""
        xml_content = """
        <body>
            <media mimetype="application" mime-subtype="pdf">
                <alt-text>PDF document</alt-text>
            </media>
        </body>
        """
        xml_node = etree.fromstring(xml_content)
        validator = XMLAccessibilityDataValidation(xml_node, self.params)
        results = list(validator.validate())

        restriction = [r for r in results if r.get("sub_item") == "media restriction" and r["item"] == "alt-text"]
        self.assertEqual(len(restriction), 1)
        self.assertEqual(restriction[0]["response"], "ERROR")
        self.assertIn("should only be used for video (mp4) or audio (mp3)", restriction[0]["advice"])

    def test_long_desc_media_restriction_valid_audio(self):
        """NOVO: long-desc em audio/mp3 é válido"""
        xml_content = """
        <body>
            <media mimetype="audio" mime-subtype="mp3">
                <long-desc>This audio recording contains an extensive interview discussing research methodologies with detailed explanations and examples provided throughout</long-desc>
            </media>
        </body>
        """
        xml_node = etree.fromstring(xml_content)
        validator = XMLAccessibilityDataValidation(xml_node, self.params)
        results = list(validator.validate())

        restriction = [r for r in results if r.get("sub_item") == "media restriction" and r["item"] == "long-desc"]
        self.assertEqual(len(restriction), 1)
        self.assertEqual(restriction[0]["response"], "OK")

    def test_long_desc_media_restriction_invalid_xlsx(self):
        """NOVO: long-desc em application/xlsx gera erro"""
        xml_content = """
        <body>
            <media mimetype="application" mime-subtype="xlsx">
                <long-desc>Spreadsheet containing detailed data analysis with multiple sheets showing statistical calculations and results formatted in tables</long-desc>
            </media>
        </body>
        """
        xml_node = etree.fromstring(xml_content)
        validator = XMLAccessibilityDataValidation(xml_node, self.params)
        results = list(validator.validate())

        restriction = [r for r in results if r.get("sub_item") == "media restriction" and r["item"] == "long-desc"]
        self.assertEqual(len(restriction), 1)
        self.assertEqual(restriction[0]["response"], "ERROR")

    # ========== NOVOS TESTES: FIGURAS DECORATIVAS ==========

    def test_decorative_figure_alt_text_warning(self):
        """NOVO: Figura sem label/caption com alt-text != null gera WARNING"""
        xml_content = """
        <body>
            <graphic>
                <alt-text>Decorative border</alt-text>
            </graphic>
        </body>
        """
        xml_node = etree.fromstring(xml_content)
        validator = XMLAccessibilityDataValidation(xml_node, self.params)
        results = list(validator.validate())

        decorative = [r for r in results if r.get("sub_item") == "decorative"]
        self.assertEqual(len(decorative), 1)
        self.assertEqual(decorative[0]["response"], "WARNING")
        self.assertIn("decorative figure", decorative[0]["advice"])

    def test_decorative_figure_alt_text_null_valid(self):
        """NOVO: Figura decorativa com alt-text=null é válida"""
        xml_content = """
        <body>
            <graphic>
                <alt-text>null</alt-text>
            </graphic>
        </body>
        """
        xml_node = etree.fromstring(xml_content)
        validator = XMLAccessibilityDataValidation(xml_node, self.params)
        results = list(validator.validate())

        decorative = [r for r in results if r.get("sub_item") == "decorative"]
        self.assertEqual(len(decorative), 1)
        self.assertEqual(decorative[0]["response"], "OK")

    def test_decorative_figure_alt_text_valid_with_caption(self):
        """NOVO: Figura com caption não é considerada decorativa"""
        xml_content = """
        <body>
            <fig>
                <graphic>
                    <alt-text>Scientific diagram</alt-text>
                </graphic>
                <caption>
                    <title>Figure 1</title>
                </caption>
            </fig>
        </body>
        """
        xml_node = etree.fromstring(xml_content)
        validator = XMLAccessibilityDataValidation(xml_node, self.params)
        results = list(validator.validate())

        # Com caption, a validação decorativa retorna OK
        decorative = [r for r in results if r.get("sub_item") == "decorative"]
        self.assertEqual(len(decorative), 1)
        self.assertEqual(decorative[0]["response"], "OK")

    # ========== NOVOS TESTES: ESTRUTURA ==========

    def test_accessibility_data_structure_valid_graphic(self):
        """NOVO: Dados de acessibilidade em <graphic> são válidos"""
        xml_content = """
        <body>
            <graphic>
                <alt-text>Valid graphic description</alt-text>
            </graphic>
        </body>
        """
        xml_node = etree.fromstring(xml_content)
        validator = XMLAccessibilityDataValidation(xml_node, self.params)
        results = list(validator.validate())

        structure = [r for r in results if r["title"] == "structure"]
        self.assertEqual(len(structure), 1)
        self.assertEqual(structure[0]["response"], "OK")

    def test_accessibility_data_structure_valid_media(self):
        """NOVO: Dados de acessibilidade em <media> são válidos"""
        xml_content = """
        <body>
            <media mimetype="video" mime-subtype="mp4">
                <alt-text>Video content</alt-text>
            </media>
        </body>
        """
        xml_node = etree.fromstring(xml_content)
        validator = XMLAccessibilityDataValidation(xml_node, self.params)
        results = list(validator.validate())

        structure = [r for r in results if r["title"] == "structure"]
        self.assertEqual(len(structure), 1)
        self.assertEqual(structure[0]["response"], "OK")

    # ========== NOVOS TESTES: OCCURRENCE ==========

    def test_long_desc_occurrence_always_returns(self):
        """NOVO: validate_long_desc_occurrence sempre retorna resultado"""
        xml_content = """
        <body>
            <graphic>
                <long-desc>Single description with more than 121 characters to meet the minimum length requirement for long-desc validation in this test case</long-desc>
            </graphic>
        </body>
        """
        xml_node = etree.fromstring(xml_content)
        validator = XMLAccessibilityDataValidation(xml_node, self.params)
        results = list(validator.validate())

        occurrence = [r for r in results if r.get("sub_item") == "occurrence"]
        self.assertEqual(len(occurrence), 1)
        self.assertEqual(occurrence[0]["response"], "OK")

    # ========== NOVOS TESTES: INCOMPATIBILIDADE NULL ==========

    def test_long_desc_with_null_alt_always_returns(self):
        """NOVO: validate_long_desc_incompatible_with_null_alt sempre retorna"""
        xml_content = """
        <body>
            <graphic>
                <alt-text>Valid description</alt-text>
                <long-desc>Detailed description with more than 121 characters to pass validation requirements for long-desc element content in this test case scenario</long-desc>
            </graphic>
        </body>
        """
        xml_node = etree.fromstring(xml_content)
        validator = XMLAccessibilityDataValidation(xml_node, self.params)
        results = list(validator.validate())

        incompatibility = [r for r in results if r.get("sub_item") == "null alt-text incompatibility"]
        self.assertEqual(len(incompatibility), 1)
        self.assertEqual(incompatibility[0]["response"], "OK")


if __name__ == "__main__":
    unittest.main()
