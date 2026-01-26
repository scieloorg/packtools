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
        expected_advice = f"alt-text has {len(response['got_value'])} characters in <alt-text>This is an alternative text that is intentionally made longer than one hundred and twenty characters to ensure that the validation fails as expected.</alt-text>. Provide text with up to 120 characters."
        self.assertEqual(response["advice"], expected_advice)

        # Verificar internacionalização
        self.assertIn("msg_text", response)
        self.assertIn("msg_params", response)
        self.assertIn("adv_text", response)
        self.assertIn("adv_params", response)

        # Verificar parâmetros de advice
        self.assertIsNotNone(response["adv_text"])
        self.assertIsInstance(response["adv_params"], dict)
        self.assertIn("length", response["adv_params"])
        self.assertEqual(response["adv_params"]["length"], len(response['got_value']))

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

        # Filtrar por título
        long_desc_results = [r for r in results if r["title"] == "<long-desc>" and r.get("sub_item") is None]
        self.assertEqual(len(long_desc_results), 1)
        response = long_desc_results[0]

        self.assertEqual(response["response"], "CRITICAL")
        expected_advice = f"long-desc has {len(response['got_value'])} characters in <long-desc>Short description.</long-desc>. Provide text with more than 120 characters."
        self.assertEqual(response["advice"], expected_advice)

        # Verificar internacionalização
        self.assertIn("adv_text", response)
        self.assertIn("adv_params", response)
        self.assertIsNotNone(response["adv_text"])
        self.assertIn("length", response["adv_params"])

    def test_validate_transcript_failure(self):
        """Fails when a transcript is missing."""
        xml_content = """
        <body>
            <media>
                <alt-text>Valid alternative text.</alt-text>
                <long-desc>{}</long-desc>
            </media>
        </body>
        """.format("x" * 130)
        xml_node = etree.fromstring(xml_content)
        validator = XMLAccessibilityDataValidation(xml_node, self.params)
        results = list(validator.validate())

        # Filtrar por título ao invés de usar índice fixo
        transcript_results = [r for r in results if r["title"] == "Transcript validation"]
        self.assertEqual(len(transcript_results), 1)
        response = transcript_results[0]

        self.assertEqual(response["response"], "WARNING")
        expected_advice = (
            'The transcript is missing in the media element. Add a <sec sec-type="transcript"> section to provide accessible text alternatives. '
            'Refer to SPS 1.10 docs for details.'
        )
        self.assertEqual(response["advice"], expected_advice)

        # Verificar internacionalização
        self.assertIn("adv_text", response)
        self.assertIn("adv_params", response)

    def test_validate_content_type_failure(self):
        """Fails when @content-type is not an allowed value."""
        xml_content = """
        <body>
            <media>
                <alt-text content-type="manual">Valid alternative text.</alt-text>
            </media>
        </body>
        """
        xml_node = etree.fromstring(xml_content)
        validator = XMLAccessibilityDataValidation(xml_node, self.params)
        results = list(validator.validate())

        # Filtrar por título e sub_item
        content_type_results = [r for r in results if r["title"] == "@content-type" and r["item"] == "alt-text"]
        self.assertEqual(len(content_type_results), 1)
        response = content_type_results[0]

        self.assertEqual(response["response"], "CRITICAL")
        expected_advice = ('The value \'manual\' is invalid in <alt-text content-type="manual">Valid alternative text.</alt-text>. '
                           'Replace it with one of the accepted values: [\'machine-generated\'].')
        self.assertEqual(response["advice"], expected_advice)

        # Verificar internacionalização
        self.assertIn("adv_text", response)
        self.assertIn("adv_params", response)
        self.assertIn("value", response["adv_params"])

    def test_validate_content_type_missing_is_valid(self):
        """NOVO: Passa quando @content-type está ausente (atributo opcional)."""
        xml_content = """
        <body>
            <graphic>
                <alt-text>Valid alternative text without content-type.</alt-text>
            </graphic>
        </body>
        """
        xml_node = etree.fromstring(xml_content)
        validator = XMLAccessibilityDataValidation(xml_node, self.params)
        results = list(validator.validate())

        # Deve ter apenas 1 resultado (validação de alt-text), não validação de content-type
        alt_text_results = [r for r in results if r["item"] == "alt-text" and r.get("sub_item") is None]
        self.assertEqual(len(alt_text_results), 1)
        self.assertEqual(alt_text_results[0]["response"], "OK")

    def test_validate_speaker_and_speech_failure(self):
        """Fails when no <speaker> and <speech> elements are present."""
        xml_content = """
        <body>
            <media>
                <sec sec-type="transcript">
                    <!-- Speaker and Speech missing -->
                </sec>
            </media>
        </body>
        """
        xml_node = etree.fromstring(xml_content)
        validator = XMLAccessibilityDataValidation(xml_node, self.params)
        results = list(validator.validate())

        # Filtrar por título
        speaker_results = [r for r in results if r["title"] == "<speaker> and <speech> validation"]
        self.assertEqual(len(speaker_results), 1)
        response = speaker_results[0]

        self.assertEqual(response["response"], "WARNING")
        # Verificar que a mensagem contém as informações principais
        self.assertIn("Dialog elements are missing", response["advice"])
        self.assertIn("<speaker>", response["advice"])
        self.assertIn("<speech>", response["advice"])

        # Verificar internacionalização
        self.assertIn("adv_text", response)
        self.assertIn("adv_params", response)

    def test_long_desc_multiple_occurrences_failure(self):
        """ATUALIZADO: Múltiplas ocorrências de long-desc devem gerar ERROR

        Este teste agora valida que a contagem é feita corretamente usando
        node.findall() em vez de contar strings no XML truncado.
        """
        xml_content = """
        <body>
            <graphic>
                <long-desc>First detailed description with more than 121 characters to pass the minimum length validation requirement for long-desc</long-desc>
                <long-desc>Second detailed description with more than 121 characters to pass the minimum length validation requirement for long-desc</long-desc>
            </graphic>
        </body>
        """
        xml_node = etree.fromstring(xml_content)
        validator = XMLAccessibilityDataValidation(xml_node, self.params)
        results = list(validator.validate())

        occurrence = [r for r in results if "occurrence" in str(r.get("sub_item", "")) and r["item"] == "long-desc"]
        self.assertEqual(len(occurrence), 1)
        self.assertEqual(occurrence[0]["response"], "ERROR")
        self.assertIn("2 <long-desc> elements", occurrence[0]["advice"])

        # Verificar internacionalização
        self.assertIn("adv_text", occurrence[0])
        self.assertIn("adv_params", occurrence[0])
        self.assertIn("count", occurrence[0]["adv_params"])
        self.assertEqual(occurrence[0]["adv_params"]["count"], 2)

    def test_long_desc_single_occurrence_valid(self):
        """ATUALIZADO: Uma única ocorrência de long-desc é válida

        Valida que quando há apenas 1 long-desc, a contagem correta é retornada
        e nenhum erro de ocorrência é gerado.
        """
        xml_content = """
        <body>
            <graphic>
                <long-desc>Single detailed description with more than 121 characters to pass the minimum length validation requirement for long-desc element</long-desc>
            </graphic>
        </body>
        """
        xml_node = etree.fromstring(xml_content)
        validator = XMLAccessibilityDataValidation(xml_node, self.params)
        results = list(validator.validate())

        occurrence = [r for r in results if "occurrence" in str(r.get("sub_item", "")) and r["item"] == "long-desc"]
        # Não deve haver erro de ocorrência quando há apenas 1 long-desc
        self.assertEqual(len(occurrence), 0)

    def test_long_desc_no_occurrence_valid(self):
        """NOVO: Zero ocorrências de long-desc é válido (elemento opcional)

        Valida que quando não há long-desc, a contagem é 0 e não há erro.
        """
        xml_content = """
        <body>
            <graphic>
                <alt-text>Valid alternative text for the graphic.</alt-text>
            </graphic>
        </body>
        """
        xml_node = etree.fromstring(xml_content)
        validator = XMLAccessibilityDataValidation(xml_node, self.params)
        results = list(validator.validate())

        occurrence = [r for r in results if "occurrence" in str(r.get("sub_item", "")) and r["item"] == "long-desc"]
        # Não deve haver erro de ocorrência quando não há long-desc (é opcional)
        self.assertEqual(len(occurrence), 0)

    def test_long_desc_count_with_large_content(self):
        """
        Valida contagem com conteúdo > 200 caracteres
        """
        # Cria long-desc com conteúdo muito longo (> 200 chars cada)
        large_text = "x" * 250
        xml_content = f"""
        <body>
            <graphic>
                <long-desc>{large_text}</long-desc>
                <long-desc>{large_text}</long-desc>
                <long-desc>{large_text}</long-desc>
            </graphic>
        </body>
        """
        xml_node = etree.fromstring(xml_content)
        validator = XMLAccessibilityDataValidation(xml_node, self.params)
        results = list(validator.validate())

        occurrence = [r for r in results if "occurrence" in str(r.get("sub_item", "")) and r["item"] == "long-desc"]
        self.assertEqual(len(occurrence), 1)
        self.assertEqual(occurrence[0]["response"], "ERROR")

        # A contagem deve ser correta (3), não truncada
        self.assertIn("count", occurrence[0]["adv_params"])
        self.assertEqual(occurrence[0]["adv_params"]["count"], 3)
        self.assertIn("3 <long-desc> elements", occurrence[0]["advice"])

    def test_long_desc_count_with_nested_elements(self):
        """NOVO: Valida que a contagem não inclui long-desc aninhados

        node.findall() conta apenas filhos diretos, não descendentes.
        """
        xml_content = """
        <body>
            <graphic>
                <long-desc>First valid description with more than 121 characters to pass validation requirements</long-desc>
                <caption>
                    <p>Some caption text</p>
                </caption>
            </graphic>
        </body>
        """
        xml_node = etree.fromstring(xml_content)
        validator = XMLAccessibilityDataValidation(xml_node, self.params)
        results = list(validator.validate())

        occurrence = [r for r in results if "occurrence" in str(r.get("sub_item", "")) and r["item"] == "long-desc"]
        # Não deve haver erro - apenas 1 long-desc como filho direto
        self.assertEqual(len(occurrence), 0)

    def test_long_desc_with_null_alt_text_failure(self):
        """NOVA: long-desc combinado com alt-text="null" deve gerar WARNING"""
        xml_content = """
        <body>
            <graphic>
                <alt-text>null</alt-text>
                <long-desc>Detailed description with more than 121 characters to pass the minimum length validation requirement for the long-desc element in this test</long-desc>
            </graphic>
        </body>
        """
        xml_node = etree.fromstring(xml_content)
        validator = XMLAccessibilityDataValidation(xml_node, self.params)
        results = list(validator.validate())

        incompatibility = [r for r in results if "null alt-text incompatibility" in str(r.get("sub_item", ""))]
        self.assertEqual(len(incompatibility), 1)
        self.assertEqual(incompatibility[0]["response"], "WARNING")
        self.assertIn("alt-text>null", incompatibility[0]["advice"])

        # Verificar internacionalização
        self.assertIn("adv_text", incompatibility[0])
        self.assertIn("adv_params", incompatibility[0])

    def test_long_desc_with_regular_alt_text_valid(self):
        """NOVA: long-desc combinado com alt-text normal é válido"""
        xml_content = """
        <body>
            <graphic>
                <alt-text>Brief description</alt-text>
                <long-desc>Detailed description with more than 121 characters to pass the minimum length validation requirement for the long-desc element in this test</long-desc>
            </graphic>
        </body>
        """
        xml_node = etree.fromstring(xml_content)
        validator = XMLAccessibilityDataValidation(xml_node, self.params)
        results = list(validator.validate())

        # Não deve haver erro de incompatibilidade
        incompatibility = [r for r in results if "null alt-text incompatibility" in str(r.get("sub_item", ""))]
        self.assertEqual(len(incompatibility), 0)

    def test_long_desc_without_alt_text_valid(self):
        """NOVA: long-desc sem alt-text é válido"""
        xml_content = """
        <body>
            <graphic>
                <long-desc>Detailed description with more than 121 characters to pass the minimum length validation requirement for the long-desc element in this test</long-desc>
            </graphic>
        </body>
        """
        xml_node = etree.fromstring(xml_content)
        validator = XMLAccessibilityDataValidation(xml_node, self.params)
        results = list(validator.validate())

        # Não deve haver erro de incompatibilidade
        incompatibility = [r for r in results if "null alt-text incompatibility" in str(r.get("sub_item", ""))]
        self.assertEqual(len(incompatibility), 0)

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

        duplication = [r for r in results if "duplication" in str(r.get("sub_item", ""))]
        self.assertEqual(len(duplication), 1)
        self.assertEqual(duplication[0]["response"], "WARNING")


class TestInternationalization(unittest.TestCase):
    """Testes específicos para verificar internacionalização"""

    def setUp(self):
        self.params = {
            "alt_text_exist_error_level": "WARNING",
            "alt_text_content_error_level": "CRITICAL",
            "alt_text_media_restriction_error_level": "ERROR",
            "alt_text_duplication_error_level": "WARNING",
            "decorative_alt_text_error_level": "WARNING",
            "long_desc_exist_error_level": "WARNING",
            "long_desc_content_error_level": "CRITICAL",
            "transcript_error_level": "WARNING",
            "content_type_error_level": "CRITICAL",
            "speaker_speech_error_level": "WARNING",
            "structure_error_level": "CRITICAL",
            "content_types": ["machine-generated"],
        }

    def test_response_has_internationalization_fields(self):
        """Verifica que todas as respostas têm os 4 campos de internacionalização"""
        xml_content = """
        <body>
            <media>
                <alt-text>""" + "x" * 150 + """</alt-text>
            </media>
        </body>
        """
        xml_node = etree.fromstring(xml_content)
        validator = XMLAccessibilityDataValidation(xml_node, self.params)
        results = list(validator.validate())

        for result in results:
            # Verificar que todos os campos obrigatórios estão presentes
            self.assertIn("message", result)
            self.assertIn("msg_text", result)
            self.assertIn("msg_params", result)
            self.assertIn("advice", result)
            self.assertIn("adv_text", result)
            self.assertIn("adv_params", result)

            # msg_text e msg_params nunca são None
            self.assertIsNotNone(result["msg_text"])
            self.assertIsNotNone(result["msg_params"])
            self.assertIsInstance(result["msg_params"], dict)

            # adv_text e adv_params são None quando response é OK
            if result["response"] == "OK":
                self.assertIsNone(result["adv_text"])
                self.assertIsNone(result["adv_params"])
            else:
                # Se houver erro, deve ter advice internacionalizado
                if result["advice"]:
                    self.assertIsNotNone(result["adv_text"])
                    self.assertIsInstance(result["adv_params"], dict)

    def test_msg_params_contain_correct_values(self):
        """Verifica que msg_params contém os valores corretos"""
        xml_content = """
        <body>
            <graphic>
                <alt-text>Short text</alt-text>
            </graphic>
        </body>
        """
        xml_node = etree.fromstring(xml_content)
        validator = XMLAccessibilityDataValidation(xml_node, self.params)
        results = list(validator.validate())

        for result in results:
            msg_params = result["msg_params"]
            self.assertIn("obtained", msg_params)
            self.assertIn("expected", msg_params)

            # Verificar que os valores em msg_params são strings
            self.assertIsInstance(msg_params["obtained"], str)
            self.assertIsInstance(msg_params["expected"], str)


if __name__ == "__main__":
    unittest.main()
