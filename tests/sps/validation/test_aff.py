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
    ],
    "id_error_level": "CRITICAL",
    "label_error_level": "CRITICAL",
    "original_error_level": "ERROR",
    "orgname_error_level": "CRITICAL",
    "orgdiv1_error_level": "WARNING",
    "orgdiv2_error_level": "WARNING",
    "country_error_level": "CRITICAL",
    "country_code_error_level": "CRITICAL",
    "state_error_level": "ERROR",
    "city_error_level": "ERROR",
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
        obtained = list(
            AffiliationValidation(self.complete_aff, PARAMS).validate()
        )
        self.assertEqual(0, len(obtained))

    def test_validate_incomplete_aff(self):
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
        obtained = list(AffiliationValidation(self.complete_aff, PARAMS).validate_original_aff_components())[0]
        self.assertEqual(obtained["got_value"], "Secretaria Municipal de Saúde de Belo Horizonte. Belo Horizonte, MG, Brasil")
        self.assertEqual(obtained["advice"], 'Mark the complete original affiliation with '
                                             '<institution content-type="original"> in <aff> and '
                                             'add Divisão 1 (orgdiv1), Divisão 2 (orgdiv2) in <institution content-type="original">')

    def test_validate_original_aff_components_value(self):
        self.maxDiff = None
        obtained = list(AffiliationValidation(self.complete_aff_modified, PARAMS).validate_original_aff_components_value())[0]
        self.assertEqual(obtained["got_value"], "Secretaria Municipal de Saúde de Belo Horizonte. Belo Horizonte, MG, Brasil")
        self.assertEqual(obtained["advice"], 'Mark the complete original affiliation with <institution content-type="original"> '
                                             'in <aff> and add missing words: [\'Secretaria\', \'Municipal\', \'de\', \'Saúde\', \'de\'].')


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
        self.assertEqual(result["advice"], "Review affiliation (aff2)")
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

        # Count results for main affiliation
        self.assertEqual(len(results), 2)
        self.assertEqual(
            "provide the orgdiv2 affiliation", results[0]["advice"]
        )
        self.assertEqual(
            "provide the orgdiv2 affiliation", results[1]["advice"]
        )

    def test_validate_translations_consistency(self):
        """Test validation of translation consistency"""
        results = list(self.validator.validate_translations_consistency())
        self.assertEqual(2, len(results))  # All fields being compared

        self.assertEqual(results[0]["advice"], "Review affiliation (aff2)")
        self.assertEqual(results[1]["advice"], "Review affiliation (aff21)")

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
        self.assertEqual(mock_av.call_count, 0)

    @patch("packtools.sps.validation.aff.AffiliationValidation.compare")
    def test_validate_translated_affiliations_compare(self, mock_av):
        results = list(self.validator.validate_translated_affiliations())
        self.assertEqual(mock_av.call_count, 0)

    @patch("packtools.sps.validation.aff.AffiliationValidation")
    def test_validate_not_translation_affiliations_create_affvalidation(
        self, mock_av
    ):
        results = list(self.validator.validate_not_translation_affiliations())
        # 1 para cada aff, 1 para executar compare
        self.assertEqual(mock_av.call_count, 3)

    @patch("packtools.sps.validation.aff.AffiliationValidation.validate")
    def test_validate_not_translation_affiliations_calls_validate(
        self, mock_av
    ):
        results = list(self.validator.validate_not_translation_affiliations())
        # 1 para cada aff, 1 para executar compare
        self.assertEqual(mock_av.call_count, 2)

    @patch("packtools.sps.validation.aff.AffiliationValidation.compare")
    def test_validate_not_translation_affiliations_calls_compare(self, mock_av):
        results = list(self.validator.validate_not_translation_affiliations())
        # 1 para cada aff, 1 para executar compare
        self.assertEqual(mock_av.call_count, 1)

    @patch("packtools.sps.validation.aff.AffiliationValidation")
    def test_validate_create_affvalidation(self, mock_av):
        results = list(self.validator.validate())
        # 1 para cada aff, 1 para executar compare
        self.assertEqual(mock_av.call_count, 9)

    @patch("packtools.sps.validation.aff.AffiliationValidation.validate")
    def test_validate_calls_validate(self, mock_av):
        results = list(self.validator.validate())
        # 1 para cada aff, 1 para executar compare
        self.assertEqual(mock_av.call_count, 9)

    @patch("packtools.sps.validation.aff.AffiliationValidation.compare")
    def test_validate_calls_compare(self, mock_av):
        results = list(self.validator.validate())
        # 1 para cada aff, 1 para executar compare
        self.assertEqual(mock_av.call_count, 3)
