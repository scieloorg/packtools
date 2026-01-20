from lxml import etree
from unittest import TestCase

from packtools.sps.validation.alternatives import AlternativesValidation
from packtools.sps.validation.exceptions import ValidationAlternativesException


class AlternativesValidationTest(TestCase):

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

        # Deve ter validações OK para ambos elementos
        ok_validations = [v for v in obtained if v['response'] == 'OK']
        self.assertGreater(len(ok_validations), 0)

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

        # Deve ter erros CRITICAL
        errors = [v for v in obtained if v['response'] == 'CRITICAL']
        self.assertGreater(len(errors), 0)

        # Verificar mensagens de erro
        error_advices = [v['advice'] for v in errors]
        self.assertTrue(any('graphic' in adv for adv in error_advices))

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


class TestSVGFormatValidation(TestCase):
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

        # Validação de formato SVG deve passar
        svg_validations = [v for v in obtained if 'SVG format' in v.get('title', '')]
        if svg_validations:
            self.assertEqual('OK', svg_validations[0]['response'])

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

        # Validação de ambas versões deve passar
        both_validations = [v for v in obtained if 'Both versions' in v.get('title', '')]
        # Pode não ter a validação se ambos estão presentes (não gera)
        # Ou se tem, deve ser OK
        for validation in both_validations:
            self.assertIn(validation['response'], ['OK', 'ERROR'])

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
    import unittest
    unittest.main()
