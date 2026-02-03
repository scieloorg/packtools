from lxml import etree
from unittest import TestCase, main

from packtools.sps.validation.alternatives import AlternativesValidation
from packtools.sps.validation.exceptions import ValidationAlternativesException


class BaseValidationTest(TestCase):
    """Base class with helper methods for validation tests"""

    def assert_validation_structure(self, validation,
                                    expected_response=None,
                                    expected_title=None):
        """
        Helper to validate standard validation response structure.

        Parameters
        ----------
        validation : dict
            Validation result to check
        expected_response : str, optional
            Expected response level (OK, WARNING, ERROR, CRITICAL)
        expected_title : str, optional
            Expected validation title (partial match allowed)

        Note
        ----
        The actual structure from build_response uses:
        - 'response': OK/WARNING/ERROR/CRITICAL
        - 'expected_value': what was expected
        - 'got_value': what was obtained
        NOT 'is_valid', 'expected', 'obtained'
        """
        # Campos obrigatórios
        required_fields = [
            'title', 'parent', 'item', 'validation_type',
            'response', 'expected_value', 'got_value', 'data'
        ]

        for field in required_fields:
            self.assertIn(field, validation,
                          f"Campo obrigatório '{field}' ausente no validation")

        # Validar tipos
        self.assertIsInstance(validation['title'], str)
        self.assertIn(validation['response'],
                      ['OK', 'WARNING', 'ERROR', 'CRITICAL'])

        # Validar valores esperados (se fornecidos)
        if expected_response:
            self.assertEqual(expected_response, validation['response'],
                           f"Expected response {expected_response}, got {validation['response']}")

        if expected_title:
            self.assertIn(expected_title.lower(), validation['title'].lower(),
                         f"Expected '{expected_title}' in title '{validation['title']}'")


class AlternativesValidationTest(BaseValidationTest):
    """Tests for AlternativesValidation - inherits helper from BaseValidationTest"""

    def test_validation_success(self):
        """Teste de validação bem-sucedida com elementos corretos"""
        self.maxDiff = None
        self.xml_tree = etree.fromstring(
            """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" 
            dtd-version="1.0" article-type="research-article" xml:lang="pt">
                <body>
                    <table-wrap>
                        <alternatives>
                            <graphic xlink:href="nomedaimagemdatabela.svg"/>
                            <table />
                        </alternatives>
                    </table-wrap>
                </body>
                <sub-article article-type="translation" xml:lang="en" id="TRen">
                    <body>
                        <fig>
                            <alternatives>
                                <graphic xlink:href="nomedaimagemdafigura.svg"/>
                                <media />
                            </alternatives>
                        </fig>
                    </body>
                </sub-article>
            </article>
            """
        )
        params = {
            "table-wrap": ["graphic", "table"],
            "fig": ["graphic", "media"]
        }
        obtained = list(AlternativesValidation(self.xml_tree, params).validate())

        # XML válido deve ter todas validações OK
        ok_validations = [v for v in obtained if v['response'] == 'OK']
        self.assertGreater(len(ok_validations), 0,
                          "XML válido deve gerar validações OK")

        # Usar helper para validar estrutura de pelo menos uma validação
        sample_validation = ok_validations[0]
        self.assert_validation_structure(
            sample_validation,
            expected_response='OK'
        )

        # Validar tipos dos campos
        self.assertIsInstance(sample_validation['title'], str)
        self.assertEqual(sample_validation['response'], 'OK')

        # Verificar que validações específicas estão presentes
        validation_titles = [v['title'].lower() for v in ok_validations]

        # Deve ter validação de SVG format
        self.assertTrue(
            any('svg format' in title for title in validation_titles),
            "Faltando validação de formato SVG"
        )

        # Deve ter validação de elementos esperados
        self.assertTrue(
            any('alternatives validation' in title or 'expected' in title
                for title in validation_titles),
            "Faltando validação de elementos esperados"
        )

    def test_validation_children_fail(self):
        """Teste de validação com elementos filhos incorretos"""
        self.maxDiff = None
        self.xml_tree = etree.fromstring(
            """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML"
            dtd-version="1.0" article-type="research-article" xml:lang="pt">
                <body>
                    <table-wrap>
                        <alternatives>
                            <p />
                        </alternatives>
                    </table-wrap>
                </body>
                <sub-article article-type="translation" xml:lang="en" id="TRen">
                    <body>
                        <fig>
                            <alternatives>
                                <title />
                                <abstract />
                            </alternatives>
                        </fig>
                    </body>
                </sub-article>
            </article>
            """
        )
        params = {
            "table-wrap": ["graphic", "table"],
            "fig": ["graphic", "media"]
        }
        obtained = list(AlternativesValidation(self.xml_tree, params).validate())

        # XML inválido deve gerar erros CRITICAL
        critical_errors = [v for v in obtained if v['response'] == 'CRITICAL']
        self.assertGreater(len(critical_errors), 0,
                          "XML inválido deve gerar erros CRITICAL")

        # Deve ter erro específico de elementos esperados
        expected_elem_errors = [
            e for e in critical_errors
            if 'alternatives validation' in e.get('title', '').lower() or
               'expected' in e.get('title', '').lower()
        ]
        self.assertGreater(len(expected_elem_errors), 0,
                          "Deve ter erro de 'expected elements'")

        # Validar estrutura completa do erro usando helper
        error = expected_elem_errors[0]
        self.assert_validation_structure(
            error,
            expected_response='CRITICAL'
        )

        # Validações específicas do erro
        self.assertEqual('CRITICAL', error['response'])

        # Verificar que mensagem menciona elementos corretos
        error_text = str(error.get('advice', '')) + str(error.get('expected_value', ''))
        self.assertTrue(
            'graphic' in error_text.lower() or 'table' in error_text.lower(),
            "Mensagem de erro deve mencionar elementos esperados"
        )

    def test_validation_parent_fail(self):
        """Teste de validação com parent não configurado"""
        self.maxDiff = None
        self.xml_tree = etree.fromstring(
            """
                <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML"
                dtd-version="1.0" article-type="research-article" xml:lang="pt">
                    <body>
                        <disp-formula>
                            <alternatives>
                                <mml:math />
                                <tex-math />
                            </alternatives>
                        </disp-formula>
                    </body>
                </article>
                """
        )
        params = {
            "table-wrap": ["graphic", "table"],
            "fig": ["graphic", "media"]
        }
        obtained = AlternativesValidation(self.xml_tree, params)
        with self.assertRaises(ValidationAlternativesException) as context:
            next(obtained.validate())
        self.assertEqual("The element 'disp-formula' is not configured to use 'alternatives'. Provide alternatives "
                         "parent and children", str(context.exception))


class TestSVGFormatValidation(BaseValidationTest):
    """Testes para validação de formato SVG obrigatório"""

    def test_svg_format_valid(self):
        """SVG válido não deve gerar erro"""
        xml = etree.fromstring(
            """
            <article xmlns:xlink="http://www.w3.org/1999/xlink">
                <body>
                    <table-wrap>
                        <alternatives>
                            <graphic xlink:href="tabela.svg"/>
                            <table />
                        </alternatives>
                    </table-wrap>
                </body>
            </article>
            """
        )
        params = {"table-wrap": ["graphic", "table"]}
        obtained = list(AlternativesValidation(xml, params).validate())

        # XML válido: todas validações devem ser OK
        ok_validations = [v for v in obtained if v['response'] == 'OK']

        # Com as correções implementadas, deve ter validações:
        # 1. SVG format
        # 2. No alt-text
        # 3. No long-desc
        # 4. Both versions (só yield quando erro, então não aparece aqui)
        # 5. Expected elements / Alternatives validation
        expected_min_validations = 4  # Mínimo esperado
        self.assertGreaterEqual(len(ok_validations), expected_min_validations,
                               f"XML válido deve gerar pelo menos {expected_min_validations} validações OK")

        # Verificar que cada tipo de validação esperado está presente
        validation_titles = [v['title'].lower() for v in ok_validations]

        # 1. SVG format
        self.assertTrue(
            any('svg format' in title for title in validation_titles),
            "Faltando validação de formato SVG"
        )

        # 2. No alt-text
        self.assertTrue(
            any('alt-text' in title for title in validation_titles),
            "Faltando validação de alt-text"
        )

        # 3. No long-desc
        self.assertTrue(
            any('long-desc' in title for title in validation_titles),
            "Faltando validação de long-desc"
        )

        # 5. Expected elements / Alternatives validation
        self.assertTrue(
            any('alternatives validation' in title or 'expected' in title
                for title in validation_titles),
            "Faltando validação de elementos esperados"
        )

        # Verificar estrutura de pelo menos uma validação usando helper
        sample = ok_validations[0]
        self.assert_validation_structure(
            sample,
            expected_response='OK'
        )

    def test_svg_format_invalid_png(self):
        """PNG deve gerar erro CRITICAL"""
        xml = etree.fromstring(
            """
            <article xmlns:xlink="http://www.w3.org/1999/xlink">
                <body>
                    <table-wrap>
                        <alternatives>
                            <graphic xlink:href="tabela.png"/>
                            <table />
                        </alternatives>
                    </table-wrap>
                </body>
            </article>
            """
        )
        params = {"table-wrap": ["graphic", "table"]}
        obtained = list(AlternativesValidation(xml, params).validate())

        # Deve ter erro de formato
        svg_errors = [v for v in obtained if 'SVG format' in v.get('title', '') and v['response'] != 'OK']
        self.assertGreater(len(svg_errors), 0)
        self.assertIn('tabela.png', svg_errors[0]['got_value'])

    def test_svg_format_invalid_jpg(self):
        """JPG deve gerar erro CRITICAL"""
        xml = etree.fromstring(
            """
            <article xmlns:xlink="http://www.w3.org/1999/xlink">
                <body>
                    <table-wrap>
                        <alternatives>
                            <graphic xlink:href="imagem.jpg"/>
                            <table />
                        </alternatives>
                    </table-wrap>
                </body>
            </article>
            """
        )
        params = {"table-wrap": ["graphic", "table"]}
        obtained = list(AlternativesValidation(xml, params).validate())

        svg_errors = [v for v in obtained if 'SVG format' in v.get('title', '') and v['response'] != 'OK']
        self.assertGreater(len(svg_errors), 0)


class TestAltTextValidation(TestCase):
    """Testes para validação de ausência de alt-text em alternatives"""

    def test_no_alt_text_valid(self):
        """Graphic sem alt-text é válido em alternatives"""
        xml = etree.fromstring(
            """
            <article xmlns:xlink="http://www.w3.org/1999/xlink">
                <body>
                    <table-wrap>
                        <alternatives>
                            <graphic xlink:href="tabela.svg"/>
                            <table />
                        </alternatives>
                    </table-wrap>
                </body>
            </article>
            """
        )
        params = {"table-wrap": ["graphic", "table"]}
        obtained = list(AlternativesValidation(xml, params).validate())

        # Não deve ter erro de alt-text
        alt_text_errors = [v for v in obtained if 'alt-text' in v.get('title', '').lower()]
        # Se houver validação, deve ser OK ou não deve existir
        for validation in alt_text_errors:
            self.assertEqual('OK', validation['response'])

    def test_alt_text_present_invalid(self):
        """Graphic COM alt-text deve gerar erro CRITICAL"""
        xml = etree.fromstring(
            """
            <article xmlns:xlink="http://www.w3.org/1999/xlink">
                <body>
                    <table-wrap>
                        <alternatives>
                            <graphic xlink:href="tabela.svg">
                                <alt-text>Descrição da tabela</alt-text>
                            </graphic>
                            <table />
                        </alternatives>
                    </table-wrap>
                </body>
            </article>
            """
        )
        params = {"table-wrap": ["graphic", "table"]}
        obtained = list(AlternativesValidation(xml, params).validate())

        # Deve ter erro de alt-text
        alt_text_errors = [v for v in obtained if 'alt-text' in v.get('title', '').lower() and v['response'] != 'OK']
        self.assertGreater(len(alt_text_errors), 0)


class TestLongDescValidation(TestCase):
    """Testes para validação de ausência de long-desc em alternatives"""

    def test_no_long_desc_valid(self):
        """Graphic sem long-desc é válido em alternatives"""
        xml = etree.fromstring(
            """
            <article xmlns:xlink="http://www.w3.org/1999/xlink">
                <body>
                    <table-wrap>
                        <alternatives>
                            <graphic xlink:href="tabela.svg"/>
                            <table />
                        </alternatives>
                    </table-wrap>
                </body>
            </article>
            """
        )
        params = {"table-wrap": ["graphic", "table"]}
        obtained = list(AlternativesValidation(xml, params).validate())

        # Não deve ter erro de long-desc
        long_desc_errors = [v for v in obtained if 'long-desc' in v.get('title', '').lower()]
        for validation in long_desc_errors:
            self.assertEqual('OK', validation['response'])

    def test_long_desc_present_invalid(self):
        """Graphic COM long-desc deve gerar erro CRITICAL"""
        xml = etree.fromstring(
            """
            <article xmlns:xlink="http://www.w3.org/1999/xlink">
                <body>
                    <table-wrap>
                        <alternatives>
                            <graphic xlink:href="tabela.svg">
                                <long-desc>Descrição longa da tabela</long-desc>
                            </graphic>
                            <table />
                        </alternatives>
                    </table-wrap>
                </body>
            </article>
            """
        )
        params = {"table-wrap": ["graphic", "table"]}
        obtained = list(AlternativesValidation(xml, params).validate())

        # Deve ter erro de long-desc
        long_desc_errors = [v for v in obtained if 'long-desc' in v.get('title', '').lower() and v['response'] != 'OK']
        self.assertGreater(len(long_desc_errors), 0)


class TestBothVersionsValidation(TestCase):
    """Testes para validação de presença de ambas versões (codificada + imagem)"""

    def test_both_versions_present_valid(self):
        """Ter ambas versões é válido"""
        xml = etree.fromstring(
            """
            <article xmlns:xlink="http://www.w3.org/1999/xlink">
                <body>
                    <table-wrap>
                        <alternatives>
                            <graphic xlink:href="tabela.svg"/>
                            <table />
                        </alternatives>
                    </table-wrap>
                </body>
            </article>
            """
        )
        params = {"table-wrap": ["graphic", "table"]}
        obtained = list(AlternativesValidation(xml, params).validate())

        # Filtrar validação de "both versions"
        both_validations = [
            v for v in obtained
            if 'both versions' in v.get('title', '').lower()
        ]

        # Note: Com validate_both_versions_present implementado, ele só faz yield quando há erro
        # Quando ambas versões estão presentes (caso válido), não há yield
        # Portanto, vamos verificar se NÃO há erro de "both versions"
        both_errors = [
            v for v in obtained
            if 'both versions' in v.get('title', '').lower() and
               v['response'] in ['ERROR', 'CRITICAL']
        ]

        # XML válido NÃO deve ter erros de "both versions"
        self.assertEqual(0, len(both_errors),
                        f"XML válido não deve ter erros de 'both versions'. Erros encontrados: {both_errors}")

    def test_missing_coded_version_invalid(self):
        """Falta versão codificada deve gerar erro"""
        xml = etree.fromstring(
            """
            <article xmlns:xlink="http://www.w3.org/1999/xlink">
                <body>
                    <table-wrap>
                        <alternatives>
                            <graphic xlink:href="tabela.svg"/>
                        </alternatives>
                    </table-wrap>
                </body>
            </article>
            """
        )
        params = {"table-wrap": ["graphic"]}  # Permite só graphic
        obtained = list(AlternativesValidation(xml, params).validate())

        # Deve ter erro de versão faltando
        version_errors = [v for v in obtained if 'Both versions' in v.get('title', '') and v['response'] == 'ERROR']
        self.assertGreater(len(version_errors), 0)

    def test_missing_image_version_invalid(self):
        """Falta versão imagem deve gerar erro"""
        xml = etree.fromstring(
            """
            <article xmlns:xlink="http://www.w3.org/1999/xlink">
                <body>
                    <table-wrap>
                        <alternatives>
                            <table />
                        </alternatives>
                    </table-wrap>
                </body>
            </article>
            """
        )
        params = {"table-wrap": ["table"]}  # Permite só table
        obtained = list(AlternativesValidation(xml, params).validate())

        # Deve ter erro de versão faltando
        version_errors = [v for v in obtained if 'Both versions' in v.get('title', '') and v['response'] == 'ERROR']
        self.assertGreater(len(version_errors), 0)


class TestInlineFormulaSupport(TestCase):
    """Testes para suporte a inline-formula"""

    def test_inline_formula_validated(self):
        """inline-formula deve ser validado"""
        xml = etree.fromstring(
            """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML">
                <body>
                    <p>
                        <inline-formula>
                            <alternatives>
                                <mml:math><mml:mi>x</mml:mi></mml:math>
                                <graphic xlink:href="formula.svg"/>
                            </alternatives>
                        </inline-formula>
                    </p>
                </body>
            </article>
            """
        )
        params = {
            "inline-formula": ["{http://www.w3.org/1998/Math/MathML}math", "graphic"]
        }
        obtained = list(AlternativesValidation(xml, params).validate())

        # Deve ter validações para inline-formula
        inline_validations = [v for v in obtained if v.get('item') == 'inline-formula']
        self.assertGreater(len(inline_validations), 0)


class TestI18nSupport(TestCase):
    """Testes para suporte de internacionalização"""

    def test_all_validations_have_advice_text(self):
        """Todas validações devem ter advice_text"""
        xml = etree.fromstring(
            """
            <article xmlns:xlink="http://www.w3.org/1999/xlink">
                <body>
                    <table-wrap>
                        <alternatives>
                            <graphic xlink:href="tabela.png"/>
                            <p />
                        </alternatives>
                    </table-wrap>
                </body>
            </article>
            """
        )
        params = {"table-wrap": ["graphic", "table"]}
        obtained = list(AlternativesValidation(xml, params).validate())

        # Filtrar validações com erro
        errors = [v for v in obtained if v['response'] != 'OK']

        # Todas devem ter adv_text
        for validation in errors:
            self.assertIn('adv_text', validation)
            self.assertIsNotNone(validation['adv_text'])

    def test_advice_params_present(self):
        """Validações devem ter advice_params"""
        xml = etree.fromstring(
            """
            <article xmlns:xlink="http://www.w3.org/1999/xlink">
                <body>
                    <table-wrap>
                        <alternatives>
                            <graphic xlink:href="tabela.jpg"/>
                            <table />
                        </alternatives>
                    </table-wrap>
                </body>
            </article>
            """
        )
        params = {"table-wrap": ["graphic", "table"]}
        obtained = list(AlternativesValidation(xml, params).validate())

        errors = [v for v in obtained if v['response'] != 'OK']

        for validation in errors:
            self.assertIn('adv_params', validation)
            self.assertIsNotNone(validation['adv_params'])


if __name__ == '__main__':
    main()
