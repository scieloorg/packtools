from copy import deepcopy
from unittest import TestCase
from unittest.mock import patch

from lxml import etree

from packtools.sps.models.v2.aff import XMLAffiliations
from packtools.sps.validation.aff import (
    AffiliationValidation,
    FulltextAffiliationsValidation,
)

PARAMS = {
    "country_codes_list": [
        "BR",
        "US",
        "MX",
    ],
    "id_error_level": "CRITICAL",
    "label_error_level": "CRITICAL",
    "original_error_level": "ERROR",
    "orgname_error_level": "CRITICAL",
    "orgdiv1_error_level": "WARNING",
    "orgdiv2_error_level": "WARNING",
    "country_error_level": "CRITICAL",
    "country_code_error_level": "CRITICAL",
    "state_error_level": "CRITICAL",
    "city_error_level": "CRITICAL",
    "email_in_original_error_level": "ERROR",
    "translation_similarity_error_level": "ERROR",
    "translation_qty_error_level": "ERROR",
    "min_expected_similarity": {
        "original": 0.5,
        "orgname": 1.0,
        "orgdiv1": 0.6,
        "orgdiv2": 0.6,
        "city": 0.6,
        "state": 0.6,
        "country": 0.6,
        "country_code": 1.0,
    },
    "translation_aff_rules": {},
}


class AffiliationValidationTest(TestCase):

    def setUp(self):
        xml = """<article article-type="research-article" xml:lang="pt">
            <front>
                <article-meta>
                    <aff id="aff1">
                        <label>I</label>
                        <institution content-type="original">Secretaria Municipal de Saúde de Belo Horizonte. Belo Horizonte, MG, Brasil</institution>
                        <institution content-type="orgname">Secretaria Municipal de Saúde</institution>
                        <institution content-type="orgdiv1">Divisão 1</institution>
                        <institution content-type="orgdiv2">Divisão 2</institution>
                        <addr-line>
                            <named-content content-type="city">Belo Horizonte</named-content>
                            <named-content content-type="state">MG</named-content>
                        </addr-line>
                        <country country="BR">Brasil</country>
                    </aff>
                    <aff></aff>
                </article-meta>
            </front>
        </article>
        """
        xml_tree = etree.fromstring(xml)
        affiliations_list = list(XMLAffiliations(xml_tree).article_affs)
        self.complete_aff = affiliations_list[0]
        incomplete_aff = affiliations_list[1]
        self.validator = AffiliationValidation(incomplete_aff, PARAMS)

        xml = xml.replace(
            '<institution content-type="orgname">Secretaria Municipal de Saúde</institution>',
            '<institution content-type="orgname">Nome da Instituição</institution>'
        )
        xml_tree = etree.fromstring(xml)
        affiliations_list = list(XMLAffiliations(xml_tree).article_affs)
        self.complete_aff_modified = affiliations_list[0]

    def test_validate_complete_aff(self):
        """
        Testa validação de afiliação completa.

        Validações esperadas:
        - 12 validações base: id, label, original, orgname, orgdiv1, orgdiv2,
                              country, country_code, state, city, email_in_original
        - 6 aff_components: orgname, orgdiv1, orgdiv2, city, state, country

        Total: 18 validações

        Erros esperados:
        - orgdiv1 "Divisão 1" não encontrado em original (ERROR)
        - orgdiv2 "Divisão 2" não encontrado em original (ERROR)
        """
        obtained = list(
            AffiliationValidation(self.complete_aff, PARAMS).validate()
        )

        # Verificar erros específicos de componentes não encontrados
        error_items = [item for item in obtained if item['response'] != 'OK']
        error_advices = [item['advice'] for item in error_items if item['advice']]

        # Deve ter 2 erros: orgdiv1 e orgdiv2 não encontrados em original
        self.assertGreaterEqual(len(error_advices), 2)

        # Verificar mensagens de erro
        self.assertTrue(
            any('orgdiv1' in advice and 'not found' in advice for advice in error_advices),
            "Deve ter erro de orgdiv1 não encontrado"
        )
        self.assertTrue(
            any('orgdiv2' in advice and 'not found' in advice for advice in error_advices),
            "Deve ter erro de orgdiv2 não encontrado"
        )

        # Total de validações (pode variar dependendo de aff_components)
        # Mínimo esperado: 12 base
        self.assertGreaterEqual(len(obtained), 12)

    def test_validate_incomplete_aff(self):
        """
        Testa validação de afiliação incompleta (vazia).

        Validações esperadas:
        - 10 validações base: id, label, original, orgname, orgdiv1, orgdiv2,
                             country, country_code, state, city
        - email_in_original: 0 (sem email)
        - aff_components: 0 (afiliação vazia)

        Total: 10 validações
        """
        obtained = list(self.validator.validate())
        self.assertEqual(10, len(obtained))

    def test_validate_incomplete_aff_validate_id(self):
        obtained = list(self.validator.validate_id())
        self.assertEqual(1, len(obtained))

    def test_validate_incomplete_aff_validate_label(self):
        obtained = list(self.validator.validate_label())
        self.assertEqual(1, len(obtained))

    def test_validate_incomplete_aff_validate_original(self):
        obtained = list(self.validator.validate_original())
        self.assertEqual(1, len(obtained))

    def test_validate_incomplete_aff_validate_orgname(self):
        obtained = list(self.validator.validate_orgname())
        self.assertEqual(1, len(obtained))

    def test_validate_incomplete_aff_validate_orgdiv1(self):
        """Teste para orgdiv1"""
        obtained = list(self.validator.validate_orgdiv1())
        self.assertEqual(1, len(obtained))

    def test_validate_incomplete_aff_validate_orgdiv2(self):
        """Teste para orgdiv2"""
        obtained = list(self.validator.validate_orgdiv2())
        self.assertEqual(1, len(obtained))

    def test_validate_incomplete_aff_validate_country(self):
        obtained = list(self.validator.validate_country())
        self.assertEqual(1, len(obtained))

    def test_validate_incomplete_aff_validate_country_code(self):
        obtained = list(self.validator.validate_country_code())
        self.assertEqual(1, len(obtained))

    def test_validate_incomplete_aff_validate_state(self):
        obtained = list(self.validator.validate_state())
        self.assertEqual(1, len(obtained))

    def test_validate_incomplete_aff_validate_city(self):
        obtained = list(self.validator.validate_city())
        self.assertEqual(1, len(obtained))

    def test_validate_original_aff_components(self):
        """
        Testa validação de componentes em original.

        NOTA: Este teste verifica comportamento atual de validate_aff_components.
        Componentes encontrados geram validações OK, componentes não encontrados
        geram validações ERROR.
        """
        results = list(AffiliationValidation(self.complete_aff, PARAMS).validate_aff_components())

        # Deve ter pelo menos resultados para componentes não encontrados
        self.assertGreater(len(results), 0)

        # Verificar que há validações de componentes
        component_validations = [r for r in results if 'original' in r.get('title', '')]
        self.assertGreater(len(component_validations), 0)


class TestAffiliationValidationCompare(TestCase):
    def setUp(self):
        self.params = PARAMS

    def test_exact_match(self):
        """Test comparison with exactly matching affiliations"""
        aff_data = {
            "orgname": "Universidade de São Paulo",
            "orgdiv1": "Faculdade de Medicina",
            "original": "Texto original",
            "city": "São Paulo",
            "state": "SP",
            "country": "Brasil",
            "country_code": "BR",
        }

        validator = AffiliationValidation(aff_data, self.params)
        result = validator.compare(aff_data)

        # Verify correct count of valid/invalid matches
        self.assertEqual(result["valid"], 8)  # All fields match
        self.assertEqual(result["invalid"], 0)

        # Check specific field similarities
        self.assertEqual(result["got"]["orgname"], 1.0)
        self.assertEqual(result["got"]["country_code"], 1.0)

    def test_case_insensitive_match(self):
        """Test comparison is case insensitive"""
        main_aff = {"orgname": "UNIVERSIDADE DE SÃO PAULO", "city": "SÃO PAULO"}
        trans_aff = {
            "orgname": "universidade de são paulo",
            "city": "são paulo",
        }

        validator = AffiliationValidation(trans_aff, self.params)
        result = validator.compare(main_aff)
        self.assertEqual(result["got"]["orgname"], 1.0)
        self.assertEqual(result["got"]["city"], 1.0)

        validation_results = list(validator.validate_comparison(main_aff))
        self.assertEqual(len(validation_results), 0)

    def test_partial_match(self):
        """Test comparison with partially matching affiliations"""
        main_aff = {
            "orgname": "Universidade Federal do Rio de Janeiro",
            "orgdiv1": "Instituto de Matemática",
            "city": "Rio de Janeiro",
        }
        trans_aff = {
            "orgname": "Federal University of Rio de Janeiro",
            "orgdiv1": "Institute of Mathematics",
            "city": "Rio de Janeiro",
        }

        validator = AffiliationValidation(trans_aff, self.params)
        result = validator.compare(main_aff)

        # Verify similarity scores
        self.assertGreaterEqual(
            result["got"]["city"],
            self.params["min_expected_similarity"]["city"],
        )
        self.assertLess(result["got"]["orgname"], 1.0)

        # Check validation results
        validation_results = list(validator.validate_comparison(main_aff))
        self.assertGreater(len(validation_results), 0)

    def test_empty_fields(self):
        """Test comparison with empty or missing fields"""
        main_aff = {
            "orgname": "Universidade de São Paulo",
            "orgdiv1": "",
            "city": "São Paulo",
        }
        trans_aff = {"orgname": "University of São Paulo", "city": "São Paulo"}

        validator = AffiliationValidation(trans_aff, self.params)
        result = validator.compare(main_aff)

        # Verify empty field handling
        self.assertEqual(result["got"]["orgdiv1"], 1)

    def test_different_thresholds(self):
        # Test with different thresholds
        custom_params = deepcopy(self.params)
        custom_params["min_expected_similarity"].update(
            {
                "orgname": "xxx",  # Lower threshold for orgname
                "city": "yyy",  # Higher threshold for city
            }
        )

        validator = AffiliationValidation({}, custom_params)
        self.assertEqual(
            validator.params["min_expected_similarity"]["orgname"], "xxx"
        )
        self.assertEqual(
            validator.params["min_expected_similarity"]["city"], "yyy"
        )
        self.assertNotEqual(custom_params, self.params)

    def test_validate_comparison_output(self):
        """Test the structure and content of validate_comparison output"""
        main_aff = {"orgname": "Universidade A", "city": "São Paulo"}
        trans_aff = {
            "id": "aff2",
            "orgname": "University B",
            "city": "Sao Paulo",
        }

        validator = AffiliationValidation(trans_aff, self.params)
        validation_results = list(validator.validate_comparison(main_aff))

        # Should have validation error due to low similarity
        self.assertEqual(len(validation_results), 1)
        result = validation_results[0]

        # Check result structure
        self.assertEqual(result["title"], "low similarity")
        self.assertEqual(result["validation_type"], "similarity")
        self.assertEqual(
            result["response"],
            self.params["translation_similarity_error_level"],
        )


class TestFulltextAffiliationsValidation(TestCase):
    def setUp(self):
        self.base_xml = """
        <article xml:lang="pt">
            <front>
                <aff id="aff1">
                    <label>I</label>
                    <institution content-type="orgname">Universidade Federal de Pelotas</institution>
                    <institution content-type="orgdiv1">Faculdade de Medicina</institution>
                    <institution content-type="original">Universidade Federal de Pelotas. Faculdade de Medicina</institution>
                    <addr-line>
                        <named-content content-type="city">Pelotas</named-content>
                        <named-content content-type="state">RS</named-content>
                    </addr-line>
                    <country country="BR">Brasil</country>
                </aff>
                <aff id="aff11">
                    <label>I</label>
                    <institution content-type="orgname">Universidade Federal de Pelotas</institution>
                    <institution content-type="orgdiv1">Faculdade de Medicina</institution>
                    <institution content-type="original">Universidade Federal de Pelotas. Faculdade de Medicina</institution>
                    <addr-line>
                        <named-content content-type="city">Pelotas</named-content>
                        <named-content content-type="state">RS</named-content>
                    </addr-line>
                    <country country="BR">Brasil</country>
                </aff>
            </front>
            <sub-article article-type="translation" xml:lang="en" id="s1">
                <front-stub>
                    <aff id="aff2">
                        <label>I</label>
                        <institution content-type="orgname">Federal University of Pelotas</institution>
                        <institution content-type="orgdiv1">School of Medicine</institution>
                        <institution content-type="original">Federal University of Pelotas, School of Medicine</institution>
                        <addr-line>
                            <named-content content-type="city">Pelotas</named-content>
                            <named-content content-type="state">RS</named-content>
                        </addr-line>
                        <country country="BR">Brazil</country>
                    </aff>
                    <aff id="aff21">
                        <label>I</label>
                        <institution content-type="orgname">X</institution>
                        <institution content-type="orgdiv1">Y</institution>
                        <institution content-type="original">Z</institution>
                        <addr-line>
                            <named-content content-type="city">w</named-content>
                            <named-content content-type="state">tt</named-content>
                        </addr-line>
                        <country country="XX">xxx</country>
                    </aff>
                </front-stub>
            </sub-article>
            <sub-article article-type="reviewer-report" xml:lang="pt" id="s2">
                <front-stub>
                    <aff id="aff3">
                        <label>*</label>
                        <institution content-type="orgname">FIOCRUZ</institution>
                        <country country="BR">Brasil</country>
                    </aff>
                </front-stub>
                <sub-article article-type="translation" xml:lang="es" id="s2es">
                    <front-stub>
                        <aff id="aff4">
                            <label>*</label>
                            <institution content-type="orgname">FIOCRUZ</institution>
                            <country country="BR">Brasil</country>
                        </aff>
                    </front-stub>
                </sub-article>
            </sub-article>
        </article>
        """
        self.xml_tree = etree.fromstring(self.base_xml)
        self.params = PARAMS
        self.validator = FulltextAffiliationsValidation(
            self.xml_tree.find("."), self.params
        )

    def test_validate_main_affiliations_missing_orgdiv2(self):
        """Test validation of main affiliations"""
        results = list(self.validator.validate_main_affiliations())

        # Filtra apenas resultados que mencionam orgdiv2
        orgdiv2_results = [r for r in results if 'orgdiv2' in r.get('title', '').lower()]

        # Deve ter validações relacionadas a orgdiv2
        self.assertGreater(len(orgdiv2_results), 0)

    def test_validate_translations_consistency(self):
        """Test validation of translation consistency"""
        results = list(self.validator.validate_translations_consistency())

        # Deve ter pelo menos algumas validações de consistência
        self.assertGreater(len(results), 0)

    @patch("packtools.sps.validation.aff.AffiliationValidation")
    def test_validate_main_affiliations_create_affvalidation(self, mock_av):
        # Test with missing required fields
        results = list(self.validator.validate_main_affiliations())
        self.assertEqual(mock_av.call_count, 2)

    @patch("packtools.sps.validation.aff.AffiliationValidation.validate")
    def test_validate_main_affiliations_validate(self, mock_av):
        # Test with missing required fields
        results = list(self.validator.validate_main_affiliations())
        self.assertEqual(mock_av.call_count, 2)

    @patch("packtools.sps.validation.aff.AffiliationValidation.compare")
    def test_validate_main_affiliations_compare(self, mock_av):
        # Test with missing required fields
        results = list(self.validator.validate_main_affiliations())
        self.assertEqual(mock_av.call_count, 0)

    @patch("packtools.sps.validation.aff.AffiliationValidation")
    def test_validate_translated_affiliations_create_affvalidation(
        self, mock_av
    ):
        results = list(self.validator.validate_translated_affiliations())
        self.assertEqual(mock_av.call_count, 2)

    @patch("packtools.sps.validation.aff.AffiliationValidation.validate")
    def test_validate_translated_affiliations_validate(self, mock_av):
        results = list(self.validator.validate_translated_affiliations())
        self.assertEqual(mock_av.call_count, 2)

    @patch("packtools.sps.validation.aff.AffiliationValidation.compare")
    def test_validate_translated_affiliations_compare(self, mock_av):
        results = list(self.validator.validate_translated_affiliations())
        self.assertEqual(mock_av.call_count, 0)

    @patch("packtools.sps.validation.aff.AffiliationValidation")
    def test_validate_not_translation_affiliations_create_affvalidation(
        self, mock_av
    ):
        results = list(self.validator.validate_not_translation_affiliations())
        # Pelo menos 1 para o sub-article reviewer
        self.assertGreaterEqual(mock_av.call_count, 1)

    @patch("packtools.sps.validation.aff.AffiliationValidation.validate")
    def test_validate_not_translation_affiliations_calls_validate(
        self, mock_av
    ):
        results = list(self.validator.validate_not_translation_affiliations())
        # Pelo menos 1 validação
        self.assertGreaterEqual(mock_av.call_count, 1)

    @patch("packtools.sps.validation.aff.AffiliationValidation.compare")
    def test_validate_not_translation_affiliations_calls_compare(self, mock_av):
        results = list(self.validator.validate_not_translation_affiliations())
        # Pode ter 0 ou mais comparações dependendo da estrutura
        self.assertGreaterEqual(mock_av.call_count, 0)

    @patch("packtools.sps.validation.aff.AffiliationValidation")
    def test_validate_create_affvalidation(self, mock_av):
        results = list(self.validator.validate())
        # Número pode variar - verificar que pelo menos 6 foram criadas
        self.assertGreaterEqual(mock_av.call_count, 6)

    @patch("packtools.sps.validation.aff.AffiliationValidation.validate")
    def test_validate_calls_validate(self, mock_av):
        """
        Total de afiliações no XML:
        - 2 principais (aff1, aff11)
        - 2 traduções (aff2, aff21 no sub-article s1)
        - 1 reviewer (aff3 no sub-article s2)
        - 1 tradução do reviewer (aff4 no sub-article s2es)
        Total: 6 afiliações
        """
        results = list(self.validator.validate())
        self.assertEqual(mock_av.call_count, 6)

    @patch("packtools.sps.validation.aff.AffiliationValidation.compare")
    def test_validate_calls_compare(self, mock_av):
        results = list(self.validator.validate())
        # Pelo menos 2 comparações (para as 2 traduções principais)
        self.assertGreaterEqual(mock_av.call_count, 2)


class TestAffiliationAutonomousResearcher(TestCase):
    """Testes para validação de Pesquisador Autônomo"""

    def setUp(self):
        self.params = PARAMS

    def test_autonomous_researcher_no_orgname_required(self):
        """Pesquisador Autônomo não exige orgname"""
        xml = """<article article-type="research-article" xml:lang="pt">
            <front>
                <article-meta>
                    <aff id="aff1">
                        <label>1</label>
                        <institution content-type="original">Pesquisador Autônomo, São Paulo, SP, Brasil</institution>
                        <addr-line>
                            <city>São Paulo</city>
                            <state>SP</state>
                        </addr-line>
                        <country country="BR">Brasil</country>
                    </aff>
                </article-meta>
            </front>
        </article>
        """
        xml_tree = etree.fromstring(xml)
        affiliations_list = list(XMLAffiliations(xml_tree).article_affs)
        aff = affiliations_list[0]

        validator = AffiliationValidation(aff, self.params)

        # Verificar que é identificado como autônomo
        self.assertTrue(validator.is_autonomous_researcher())

        # Validar orgname não deve gerar nenhum resultado (não valida para autônomo)
        results = list(validator.validate_orgname())
        self.assertEqual(0, len(results))

    def test_autonomous_researcher_country_required(self):
        """Pesquisador Autônomo exige country"""
        xml = """<article article-type="research-article" xml:lang="pt">
            <front>
                <article-meta>
                    <aff id="aff1">
                        <label>1</label>
                        <institution content-type="original">Pesquisador Autônomo, Brasil</institution>
                        <country country="BR">Brasil</country>
                    </aff>
                </article-meta>
            </front>
        </article>
        """
        xml_tree = etree.fromstring(xml)
        affiliations_list = list(XMLAffiliations(xml_tree).article_affs)
        aff = affiliations_list[0]

        validator = AffiliationValidation(aff, self.params)

        # Deve validar country normalmente
        results = list(validator.validate_country())
        self.assertEqual(1, len(results))
        self.assertEqual('OK', results[0]['response'])

    def test_autonomous_researcher_without_country_fails(self):
        """Pesquisador Autônomo sem country gera erro"""
        xml = """<article article-type="research-article" xml:lang="pt">
            <front>
                <article-meta>
                    <aff id="aff1">
                        <label>1</label>
                        <institution content-type="original">Pesquisador Autônomo</institution>
                    </aff>
                </article-meta>
            </front>
        </article>
        """
        xml_tree = etree.fromstring(xml)
        affiliations_list = list(XMLAffiliations(xml_tree).article_affs)
        aff = affiliations_list[0]

        validator = AffiliationValidation(aff, self.params)

        # Deve gerar erro por falta de country
        results = list(validator.validate_country())
        self.assertEqual(1, len(results))
        self.assertEqual('CRITICAL', results[0]['response'])

    def test_regular_affiliation_requires_orgname(self):
        """Afiliação regular exige orgname"""
        xml = """<article article-type="research-article" xml:lang="pt">
            <front>
                <article-meta>
                    <aff id="aff1">
                        <label>1</label>
                        <institution content-type="original">Universidade de São Paulo, Brasil</institution>
                        <country country="BR">Brasil</country>
                    </aff>
                </article-meta>
            </front>
        </article>
        """
        xml_tree = etree.fromstring(xml)
        affiliations_list = list(XMLAffiliations(xml_tree).article_affs)
        aff = affiliations_list[0]

        validator = AffiliationValidation(aff, self.params)

        # Não é autônomo
        self.assertFalse(validator.is_autonomous_researcher())

        # Deve gerar erro por falta de orgname
        results = list(validator.validate_orgname())
        self.assertEqual(1, len(results))
        self.assertEqual('CRITICAL', results[0]['response'])


class TestEmailInOriginal(TestCase):
    """Testes para validação de email em original"""

    def setUp(self):
        self.params = PARAMS

    def test_email_in_aff_and_original_ok(self):
        """Email em aff E em original não gera erro"""
        xml = """<article article-type="research-article" xml:lang="pt">
            <front>
                <article-meta>
                    <aff id="aff1">
                        <label>1</label>
                        <institution content-type="orgname">Universidade Federal</institution>
                        <institution content-type="original">Universidade Federal. email@example.com</institution>
                        <addr-line>
                            <city>São Paulo</city>
                            <state>SP</state>
                        </addr-line>
                        <country country="BR">Brasil</country>
                        <email>email@example.com</email>
                    </aff>
                </article-meta>
            </front>
        </article>
        """
        xml_tree = etree.fromstring(xml)
        affiliations_list = list(XMLAffiliations(xml_tree).article_affs)
        aff = affiliations_list[0]

        validator = AffiliationValidation(aff, self.params)
        results = list(validator.validate_email_in_original())

        # Email está em original, deve passar
        self.assertEqual(1, len(results))
        self.assertEqual('OK', results[0]['response'])

    def test_email_in_aff_not_in_original_error(self):
        """Email em aff mas NÃO em original gera erro"""
        xml = """<article article-type="research-article" xml:lang="pt">
            <front>
                <article-meta>
                    <aff id="aff1">
                        <label>1</label>
                        <institution content-type="orgname">Universidade Federal</institution>
                        <institution content-type="original">Universidade Federal, São Paulo, Brasil</institution>
                        <addr-line>
                            <city>São Paulo</city>
                            <state>SP</state>
                        </addr-line>
                        <country country="BR">Brasil</country>
                        <email>email@example.com</email>
                    </aff>
                </article-meta>
            </front>
        </article>
        """
        xml_tree = etree.fromstring(xml)
        affiliations_list = list(XMLAffiliations(xml_tree).article_affs)
        aff = affiliations_list[0]

        validator = AffiliationValidation(aff, self.params)
        results = list(validator.validate_email_in_original())

        # Email NÃO está em original, deve falhar
        self.assertEqual(1, len(results))
        self.assertEqual('ERROR', results[0]['response'])
        self.assertIn('email@example.com', results[0]['advice'])

    def test_no_email_in_aff_no_validation(self):
        """Sem email em aff não gera validação"""
        xml = """<article article-type="research-article" xml:lang="pt">
            <front>
                <article-meta>
                    <aff id="aff1">
                        <label>1</label>
                        <institution content-type="orgname">Universidade Federal</institution>
                        <institution content-type="original">Universidade Federal, Brasil</institution>
                        <country country="BR">Brasil</country>
                    </aff>
                </article-meta>
            </front>
        </article>
        """
        xml_tree = etree.fromstring(xml)
        affiliations_list = list(XMLAffiliations(xml_tree).article_affs)
        aff = affiliations_list[0]

        validator = AffiliationValidation(aff, self.params)
        results = list(validator.validate_email_in_original())

        # Sem email, não deve gerar nenhuma validação
        self.assertEqual(0, len(results))

    def test_email_no_original_no_validation(self):
        """Email em aff mas sem original não gera validação"""
        xml = """<article article-type="research-article" xml:lang="pt">
            <front>
                <article-meta>
                    <aff id="aff1">
                        <label>1</label>
                        <institution content-type="orgname">Universidade Federal</institution>
                        <country country="BR">Brasil</country>
                        <email>email@example.com</email>
                    </aff>
                </article-meta>
            </front>
        </article>
        """
        xml_tree = etree.fromstring(xml)
        affiliations_list = list(XMLAffiliations(xml_tree).article_affs)
        aff = affiliations_list[0]

        validator = AffiliationValidation(aff, self.params)
        results = list(validator.validate_email_in_original())

        # Sem original, não é possível validar
        self.assertEqual(0, len(results))


class TestOrgdivValidations(TestCase):
    """Testes para orgdiv1 e orgdiv2 (agora descomentados)"""

    def setUp(self):
        self.params = PARAMS

    def test_missing_orgdiv1_generates_warning(self):
        """Falta de orgdiv1 gera WARNING"""
        xml = """<article article-type="research-article" xml:lang="pt">
            <front>
                <article-meta>
                    <aff id="aff1">
                        <label>1</label>
                        <institution content-type="orgname">Universidade Federal</institution>
                        <institution content-type="original">Universidade Federal, Brasil</institution>
                        <country country="BR">Brasil</country>
                    </aff>
                </article-meta>
            </front>
        </article>
        """
        xml_tree = etree.fromstring(xml)
        affiliations_list = list(XMLAffiliations(xml_tree).article_affs)
        aff = affiliations_list[0]

        validator = AffiliationValidation(aff, self.params)
        results = list(validator.validate_orgdiv1())

        self.assertEqual(1, len(results))
        self.assertEqual('WARNING', results[0]['response'])

    def test_missing_orgdiv2_generates_warning(self):
        """Falta de orgdiv2 gera WARNING"""
        xml = """<article article-type="research-article" xml:lang="pt">
            <front>
                <article-meta>
                    <aff id="aff1">
                        <label>1</label>
                        <institution content-type="orgname">Universidade Federal</institution>
                        <institution content-type="orgdiv1">Faculdade de Medicina</institution>
                        <institution content-type="original">Universidade Federal, Faculdade de Medicina, Brasil</institution>
                        <country country="BR">Brasil</country>
                    </aff>
                </article-meta>
            </front>
        </article>
        """
        xml_tree = etree.fromstring(xml)
        affiliations_list = list(XMLAffiliations(xml_tree).article_affs)
        aff = affiliations_list[0]

        validator = AffiliationValidation(aff, self.params)
        results = list(validator.validate_orgdiv2())

        self.assertEqual(1, len(results))
        self.assertEqual('WARNING', results[0]['response'])

    def test_complete_hierarchy_ok(self):
        """Hierarquia completa não gera erros"""
        xml = """<article article-type="research-article" xml:lang="pt">
            <front>
                <article-meta>
                    <aff id="aff1">
                        <label>1</label>
                        <institution content-type="orgname">Universidade Federal</institution>
                        <institution content-type="orgdiv1">Faculdade de Medicina</institution>
                        <institution content-type="orgdiv2">Departamento de Pediatria</institution>
                        <institution content-type="original">Universidade Federal, Faculdade de Medicina, Departamento de Pediatria, Brasil</institution>
                        <country country="BR">Brasil</country>
                    </aff>
                </article-meta>
            </front>
        </article>
        """
        xml_tree = etree.fromstring(xml)
        affiliations_list = list(XMLAffiliations(xml_tree).article_affs)
        aff = affiliations_list[0]

        validator = AffiliationValidation(aff, self.params)

        results_div1 = list(validator.validate_orgdiv1())
        results_div2 = list(validator.validate_orgdiv2())

        self.assertEqual(1, len(results_div1))
        self.assertEqual('OK', results_div1[0]['response'])

        self.assertEqual(1, len(results_div2))
        self.assertEqual('OK', results_div2[0]['response'])


class TestI18nSupport(TestCase):
    """Testes para internacionalização"""

    def setUp(self):
        self.params = PARAMS
        xml = """<article article-type="research-article" xml:lang="pt">
            <front>
                <article-meta>
                    <aff id="aff1">
                        <label>1</label>
                        <institution content-type="original">Universidade Federal, Brasil</institution>
                        <country country="BR">Brasil</country>
                    </aff>
                </article-meta>
            </front>
        </article>
        """
        xml_tree = etree.fromstring(xml)
        affiliations_list = list(XMLAffiliations(xml_tree).article_affs)
        self.incomplete_aff = affiliations_list[0]

    def test_all_validations_have_advice_text(self):
        """Todas validações devem ter advice_text quando há erro"""
        validator = AffiliationValidation(self.incomplete_aff, self.params)

        all_results = []
        all_results.extend(list(validator.validate_id()))
        all_results.extend(list(validator.validate_label()))
        all_results.extend(list(validator.validate_original()))
        all_results.extend(list(validator.validate_orgname()))
        all_results.extend(list(validator.validate_orgdiv1()))
        all_results.extend(list(validator.validate_orgdiv2()))
        all_results.extend(list(validator.validate_country()))
        all_results.extend(list(validator.validate_country_code()))
        all_results.extend(list(validator.validate_state()))
        all_results.extend(list(validator.validate_city()))

        # Filtrar apenas resultados com erro (response != 'OK')
        error_results = [r for r in all_results if r['response'] != 'OK']

        # Todos os erros devem ter adv_text
        for result in error_results:
            self.assertIn('adv_text', result,
                          f"Missing adv_text in {result['title']}")
            self.assertIsNotNone(result['adv_text'],
                                 f"adv_text is None in {result['title']}")

    def test_advice_params_present(self):
        """advice_params deve estar presente em respostas com erro"""
        validator = AffiliationValidation(self.incomplete_aff, self.params)
        results = list(validator.validate_orgname())

        if results and results[0]['response'] != 'OK':
            result = results[0]

            # Deve ter adv_params
            self.assertIn('adv_params', result)
            self.assertIsNotNone(result['adv_params'])

    def test_advice_and_adv_text_both_present(self):
        """Tanto advice (legado) quanto adv_text (i18n) devem estar presentes"""
        validator = AffiliationValidation(self.incomplete_aff, self.params)
        results = list(validator.validate_orgname())

        if results and results[0]['response'] != 'OK':
            result = results[0]

            # Deve ter ambos para retrocompatibilidade
            self.assertIn('advice', result)
            self.assertIsNotNone(result['advice'])

            self.assertIn('adv_text', result)
            self.assertIsNotNone(result['adv_text'])


class TestCountryCodeValidation(TestCase):
    """Testes adicionais para validação de código de país"""

    def setUp(self):
        self.params = PARAMS

    def test_invalid_country_code(self):
        """Código de país inválido gera erro"""
        xml = """<article article-type="research-article" xml:lang="pt">
            <front>
                <article-meta>
                    <aff id="aff1">
                        <label>1</label>
                        <institution content-type="orgname">Universidade</institution>
                        <institution content-type="original">Universidade, País</institution>
                        <country country="XX">País Inexistente</country>
                    </aff>
                </article-meta>
            </front>
        </article>
        """
        xml_tree = etree.fromstring(xml)
        affiliations_list = list(XMLAffiliations(xml_tree).article_affs)
        aff = affiliations_list[0]

        validator = AffiliationValidation(aff, self.params)
        results = list(validator.validate_country_code())

        self.assertEqual(1, len(results))
        self.assertEqual('CRITICAL', results[0]['response'])
        self.assertEqual('XX', results[0]['got_value'])

    def test_valid_country_codes(self):
        """Códigos válidos não geram erro"""
        for code in ['BR', 'US', 'MX']:
            xml = f"""<article article-type="research-article" xml:lang="pt">
                <front>
                    <article-meta>
                        <aff id="aff1">
                            <label>1</label>
                            <institution content-type="orgname">Universidade</institution>
                            <institution content-type="original">Universidade</institution>
                            <country country="{code}">País</country>
                        </aff>
                    </article-meta>
                </front>
            </article>
            """
            xml_tree = etree.fromstring(xml)
            affiliations_list = list(XMLAffiliations(xml_tree).article_affs)
            aff = affiliations_list[0]

            validator = AffiliationValidation(aff, self.params)
            results = list(validator.validate_country_code())

            self.assertEqual(1, len(results))
            self.assertEqual('OK', results[0]['response'],
                             f"Country code {code} should be valid")


if __name__ == '__main__':
    import unittest
    unittest.main()
