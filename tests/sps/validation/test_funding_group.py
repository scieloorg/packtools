import unittest
from lxml import etree

from packtools.sps.validation.funding_group import FundingGroupValidation


class TestFundingValidationBase(unittest.TestCase):
    """Classe base para testes de FundingGroupValidation"""

    params = {
        "special_chars_award_id": ["/", ".", "-"],
        "callable_validation": lambda x: True,
        "error_level": "ERROR",
    }


class TestEmptyXML(TestFundingValidationBase):
    """Testa casos com XML vazio ou sem informações de funding"""

    def setUp(self):
        xml = """
            <article article-type="research-article" xml:lang="pt">
                <front><article-meta></article-meta></front>
                <back></back>
            </article>
        """
        self.xml_tree = etree.fromstring(xml)
        self.validator = FundingGroupValidation(self.xml_tree, self.params)

    def test_no_award_ids(self):
        results = list(self.validator.validate_required_award_ids())
        self.assertEqual(len(results), 0)


class TestProperAwardGroup(TestFundingValidationBase):
    """Testa casos com award-id corretamente em award-group"""

    def setUp(self):
        xml = """
            <article article-type="research-article" xml:lang="pt">
                <front>
                    <article-meta>
                        <funding-group>
                            <award-group>
                                <funding-source>CNPq</funding-source>
                                <award-id>123.456-7</award-id>
                            </award-group>
                        </funding-group>
                    </article-meta>
                </front>
            </article>
        """
        self.xml_tree = etree.fromstring(xml)
        self.validator = FundingGroupValidation(self.xml_tree, self.params)

    def test_proper_award_group(self):
        results = list(self.validator.validate_required_award_ids())
        self.assertEqual(len(results), 0)


class TestAwardInAck(TestFundingValidationBase):
    """Testa casos com award ID em acknowledgments"""

    def setUp(self):
        xml = """
            <article article-type="research-article" xml:lang="pt">
                <back>
                    <ack>
                        <title>Acknowledgments</title>
                        <p>Project funded by grant 123.456-7</p>
                    </ack>
                </back>
            </article>
        """
        self.xml_tree = etree.fromstring(xml)
        self.validator = FundingGroupValidation(self.xml_tree, self.params)

    def test_award_in_ack(self):
        results = list(self.validator.validate_required_award_ids())
        print(results)
        self.assertEqual(len(results), 1)
        result = results[0]
        self.assertEqual(result["data"]["context"], "ack")
        self.assertIn("123.456-7", str(result["data"]["look-like-award-id"]))


class TestAwardInFinancialDisclosure(TestFundingValidationBase):
    """Testa casos com award ID em financial disclosure"""

    def setUp(self):
        xml = """
            <article article-type="research-article" xml:lang="pt">
                <back>
                    <fn-group>
                        <fn fn-type="financial-disclosure">
                            <p>Grant: 123.456-7</p>
                        </fn>
                    </fn-group>
                </back>
            </article>
        """
        self.xml_tree = etree.fromstring(xml)
        self.validator = FundingGroupValidation(self.xml_tree, self.params)

    def test_award_in_financial_disclosure(self):
        results = list(self.validator.validate_required_award_ids())
        self.assertEqual(len(results), 1)
        result = results[0]
        self.assertEqual(
            result["data"]["context"], "fn[@fn-type='financial-disclosure']"
        )
        self.assertIn("123.456-7", str(result["data"]["look-like-award-id"]))


class TestAwardInSupportedBy(TestFundingValidationBase):
    """Testa casos com award ID em supported-by"""

    def setUp(self):
        xml = """
            <article article-type="research-article" xml:lang="pt">
                <back>
                    <fn-group>
                        <fn fn-type="supported-by">
                            <p>Support: 123.456-7</p>
                        </fn>
                    </fn-group>
                </back>
            </article>
        """
        self.xml_tree = etree.fromstring(xml)
        self.validator = FundingGroupValidation(self.xml_tree, self.params)

    def test_award_in_supported_by(self):
        results = list(self.validator.validate_required_award_ids())
        self.assertEqual(len(results), 1)
        result = results[0]
        self.assertEqual(result["data"]["context"], "fn[@fn-type='supported-by']")
        self.assertIn("123.456-7", str(result["data"]["look-like-award-id"]))


class TestAwardInFundingStatement(TestFundingValidationBase):
    """Testa casos com award ID em funding-statement"""

    def setUp(self):
        xml = """
            <article article-type="research-article" xml:lang="pt">
                <front>
                    <article-meta>
                        <funding-group>
                            <funding-statement>Project 123.456-7</funding-statement>
                        </funding-group>
                    </article-meta>
                </front>
            </article>
        """
        self.xml_tree = etree.fromstring(xml)
        self.validator = FundingGroupValidation(self.xml_tree, self.params)

    def test_award_in_funding_statement(self):
        results = list(self.validator.validate_required_award_ids())
        self.assertEqual(len(results), 1)
        result = results[0]
        self.assertEqual(result["data"]["context"], "funding-group/funding-statement")
        self.assertIn("123.456-7", str(result["data"]["look-like-award-id"]))


class TestAwardInAllLocations(TestFundingValidationBase):
    """Testa casos com award IDs em todos os locais possíveis"""

    def setUp(self):
        xml = """
            <article article-type="research-article" xml:lang="pt">
                <front>
                    <article-meta>
                        <funding-group>
                            <funding-statement>Project 123.456-7</funding-statement>
                        </funding-group>
                    </article-meta>
                </front>
                <back>
                    <ack>
                        <p>Project 234.567-8</p>
                    </ack>
                    <fn-group>
                        <fn fn-type="financial-disclosure">
                            <p>Grant: 345.678-9</p>
                        </fn>
                        <fn fn-type="supported-by">
                            <p>Support: 456.789-0</p>
                        </fn>
                    </fn-group>
                </back>
            </article>
        """
        self.xml_tree = etree.fromstring(xml)
        self.validator = FundingGroupValidation(self.xml_tree, self.params)

    def test_awards_in_all_locations(self):
        results = list(self.validator.validate_required_award_ids())

        # Verifica número total de resultados
        self.assertEqual(len(results), 4)

        # Verifica se encontrou award IDs em todos os contextos
        contexts = {r["data"]["context"] for r in results}
        self.assertEqual(len(contexts), 4)

        # Verifica cada contexto específico
        self.assertIn("funding-group/funding-statement", contexts)
        self.assertIn("ack", contexts)
        self.assertIn("fn[@fn-type='financial-disclosure']", contexts)
        self.assertIn("fn[@fn-type='supported-by']", contexts)

        # Verifica os award IDs encontrados
        award_ids = set()
        for r in results:
            award_ids.update(r["data"]["look-like-award-id"])

        expected_ids = {"123.456-7", "234.567-8", "345.678-9", "456.789-0"}
        self.assertEqual(award_ids, expected_ids)


class TestErrorLevels(TestFundingValidationBase):
    """Testa diferentes níveis de erro"""

    def setUp(self):
        self.xml = """
            <article article-type="research-article" xml:lang="pt">
                <back>
                    <ack><p>Project 123.456-7</p></ack>
                </back>
            </article>
        """
        self.xml_tree = etree.fromstring(self.xml)

    def test_warning_level(self):
        params = dict(self.params)
        params["error_level"] = "WARNING"
        validator = FundingGroupValidation(self.xml_tree, params)
        results = list(validator.validate_required_award_ids())
        self.assertEqual(results[0]["response"], "WARNING")

    def test_info_level(self):
        params = dict(self.params)
        params["error_level"] = "INFO"
        validator = FundingGroupValidation(self.xml_tree, params)
        results = list(validator.validate_required_award_ids())
        self.assertEqual(results[0]["response"], "INFO")


# ========================================
# New Tests for SPS 1.10 Validations
# ========================================


class TestFundingGroupUniqueness(TestFundingValidationBase):
    """Rule 1: Test <funding-group> uniqueness validation"""

    def test_single_funding_group_valid(self):
        """Single <funding-group> should be valid"""
        xml = """
            <article article-type="research-article" xml:lang="en">
                <front>
                    <article-meta>
                        <funding-group>
                            <funding-statement>No funding</funding-statement>
                        </funding-group>
                    </article-meta>
                </front>
            </article>
        """
        xml_tree = etree.fromstring(xml)
        validator = FundingGroupValidation(xml_tree, self.params)
        results = list(validator.validate_funding_group_uniqueness())
        
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["response"], "OK")

    def test_multiple_funding_groups_invalid(self):
        """Multiple <funding-group> elements should be invalid"""
        xml = """
            <article article-type="research-article" xml:lang="en">
                <front>
                    <article-meta>
                        <funding-group>
                            <funding-statement>Funding 1</funding-statement>
                        </funding-group>
                        <funding-group>
                            <funding-statement>Funding 2</funding-statement>
                        </funding-group>
                    </article-meta>
                </front>
            </article>
        """
        xml_tree = etree.fromstring(xml)
        validator = FundingGroupValidation(xml_tree, self.params)
        results = list(validator.validate_funding_group_uniqueness())
        
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["response"], "ERROR")
        self.assertIn("2 <funding-group>", results[0]["advice"])

    def test_no_funding_group_valid(self):
        """No <funding-group> should be valid (0 <= 1)"""
        xml = """
            <article article-type="research-article" xml:lang="en">
                <front>
                    <article-meta>
                    </article-meta>
                </front>
            </article>
        """
        xml_tree = etree.fromstring(xml)
        validator = FundingGroupValidation(xml_tree, self.params)
        results = list(validator.validate_funding_group_uniqueness())
        
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["response"], "OK")


class TestFundingStatementPresence(TestFundingValidationBase):
    """Rule 2: Test <funding-statement> presence validation"""

    def test_funding_statement_present_valid(self):
        """<funding-statement> present should be valid"""
        xml = """
            <article article-type="research-article" xml:lang="en">
                <front>
                    <article-meta>
                        <funding-group>
                            <funding-statement>This study was supported by FAPESP</funding-statement>
                        </funding-group>
                    </article-meta>
                </front>
            </article>
        """
        xml_tree = etree.fromstring(xml)
        validator = FundingGroupValidation(xml_tree, self.params)
        results = list(validator.validate_funding_statement_presence())
        
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["response"], "OK")

    def test_funding_statement_missing_invalid(self):
        """Missing <funding-statement> should be invalid"""
        xml = """
            <article article-type="research-article" xml:lang="en">
                <front>
                    <article-meta>
                        <funding-group>
                            <award-group>
                                <funding-source>FAPESP</funding-source>
                                <award-id>04/08142-0</award-id>
                            </award-group>
                        </funding-group>
                    </article-meta>
                </front>
            </article>
        """
        xml_tree = etree.fromstring(xml)
        validator = FundingGroupValidation(xml_tree, self.params)
        results = list(validator.validate_funding_statement_presence())
        
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["response"], "CRITICAL")
        self.assertIn("Add <funding-statement>", results[0]["advice"])

    def test_no_funding_group_no_validation(self):
        """No <funding-group> means no validation needed"""
        xml = """
            <article article-type="research-article" xml:lang="en">
                <front>
                    <article-meta>
                    </article-meta>
                </front>
            </article>
        """
        xml_tree = etree.fromstring(xml)
        validator = FundingGroupValidation(xml_tree, self.params)
        results = list(validator.validate_funding_statement_presence())
        
        self.assertEqual(len(results), 0)


class TestFundingSourceInAwardGroup(TestFundingValidationBase):
    """Rule 3: Test <funding-source> presence in <award-group> validation"""

    def test_funding_source_present_valid(self):
        """<funding-source> present in <award-group> should be valid"""
        xml = """
            <article article-type="research-article" xml:lang="en">
                <front>
                    <article-meta>
                        <funding-group>
                            <award-group>
                                <funding-source>FAPESP</funding-source>
                                <award-id>04/08142-0</award-id>
                            </award-group>
                            <funding-statement>Funded by FAPESP</funding-statement>
                        </funding-group>
                    </article-meta>
                </front>
            </article>
        """
        xml_tree = etree.fromstring(xml)
        validator = FundingGroupValidation(xml_tree, self.params)
        results = list(validator.validate_funding_source_in_award_group())
        
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["response"], "OK")

    def test_funding_source_missing_invalid(self):
        """Missing <funding-source> in <award-group> should be invalid"""
        xml = """
            <article article-type="research-article" xml:lang="en">
                <front>
                    <article-meta>
                        <funding-group>
                            <award-group>
                                <award-id>04/08142-0</award-id>
                            </award-group>
                            <funding-statement>Funded</funding-statement>
                        </funding-group>
                    </article-meta>
                </front>
            </article>
        """
        xml_tree = etree.fromstring(xml)
        validator = FundingGroupValidation(xml_tree, self.params)
        results = list(validator.validate_funding_source_in_award_group())
        
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["response"], "CRITICAL")
        self.assertIn("Add at least one <funding-source>", results[0]["advice"])

    def test_multiple_funding_sources_valid(self):
        """Multiple <funding-source> elements should be valid"""
        xml = """
            <article article-type="research-article" xml:lang="en">
                <front>
                    <article-meta>
                        <funding-group>
                            <award-group>
                                <funding-source>FAPESP</funding-source>
                                <funding-source>CAPES</funding-source>
                                <award-id>04/08142-0</award-id>
                            </award-group>
                            <funding-statement>Funded by FAPESP and CAPES</funding-statement>
                        </funding-group>
                    </article-meta>
                </front>
            </article>
        """
        xml_tree = etree.fromstring(xml)
        validator = FundingGroupValidation(xml_tree, self.params)
        results = list(validator.validate_funding_source_in_award_group())
        
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["response"], "OK")


class TestLabelAbsence(TestFundingValidationBase):
    """Rule 5: Test <label> absence validation"""

    def test_no_label_valid(self):
        """No <label> in <funding-group> should be valid"""
        xml = """
            <article article-type="research-article" xml:lang="en">
                <front>
                    <article-meta>
                        <funding-group>
                            <award-group>
                                <funding-source>FAPESP</funding-source>
                            </award-group>
                            <funding-statement>Funded by FAPESP</funding-statement>
                        </funding-group>
                    </article-meta>
                </front>
            </article>
        """
        xml_tree = etree.fromstring(xml)
        validator = FundingGroupValidation(xml_tree, self.params)
        results = list(validator.validate_label_absence())
        
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["response"], "OK")

    def test_label_present_invalid(self):
        """<label> in <funding-group> should be invalid"""
        xml = """
            <article article-type="research-article" xml:lang="en">
                <front>
                    <article-meta>
                        <funding-group>
                            <label>Funding</label>
                            <award-group>
                                <funding-source>FAPESP</funding-source>
                            </award-group>
                            <funding-statement>Funded by FAPESP</funding-statement>
                        </funding-group>
                    </article-meta>
                </front>
            </article>
        """
        xml_tree = etree.fromstring(xml)
        validator = FundingGroupValidation(xml_tree, self.params)
        results = list(validator.validate_label_absence())
        
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["response"], "ERROR")
        self.assertIn("Remove", results[0]["advice"])
        self.assertIn("<label>", results[0]["advice"])


class TestTitleAbsence(TestFundingValidationBase):
    """Rule 6: Test <title> absence validation"""

    def test_no_title_valid(self):
        """No <title> in <funding-group> should be valid"""
        xml = """
            <article article-type="research-article" xml:lang="en">
                <front>
                    <article-meta>
                        <funding-group>
                            <award-group>
                                <funding-source>FAPESP</funding-source>
                            </award-group>
                            <funding-statement>Funded by FAPESP</funding-statement>
                        </funding-group>
                    </article-meta>
                </front>
            </article>
        """
        xml_tree = etree.fromstring(xml)
        validator = FundingGroupValidation(xml_tree, self.params)
        results = list(validator.validate_title_absence())
        
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["response"], "OK")

    def test_title_present_invalid(self):
        """<title> in <funding-group> should be invalid"""
        xml = """
            <article article-type="research-article" xml:lang="en">
                <front>
                    <article-meta>
                        <funding-group>
                            <title>Funding Information</title>
                            <award-group>
                                <funding-source>FAPESP</funding-source>
                            </award-group>
                            <funding-statement>Funded by FAPESP</funding-statement>
                        </funding-group>
                    </article-meta>
                </front>
            </article>
        """
        xml_tree = etree.fromstring(xml)
        validator = FundingGroupValidation(xml_tree, self.params)
        results = list(validator.validate_title_absence())
        
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["response"], "ERROR")
        self.assertIn("Remove", results[0]["advice"])
        self.assertIn("<title>", results[0]["advice"])


class TestAwardIdFundingSourceConsistency(TestFundingValidationBase):
    """Rule 7: Test <award-id> and <funding-source> consistency validation"""

    def test_support_without_contract_valid(self):
        """Support without contract (0 award-ids) should be valid"""
        xml = """
            <article article-type="research-article" xml:lang="en">
                <front>
                    <article-meta>
                        <funding-group>
                            <award-group>
                                <funding-source>FAPESP</funding-source>
                            </award-group>
                            <funding-statement>Funded by FAPESP</funding-statement>
                        </funding-group>
                    </article-meta>
                </front>
            </article>
        """
        xml_tree = etree.fromstring(xml)
        validator = FundingGroupValidation(xml_tree, self.params)
        results = list(validator.validate_award_id_funding_source_consistency())
        
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["response"], "OK")

    def test_single_contract_valid(self):
        """Single contract (1 award-id) for multiple sources should be valid"""
        xml = """
            <article article-type="research-article" xml:lang="en">
                <front>
                    <article-meta>
                        <funding-group>
                            <award-group>
                                <funding-source>FAPESP</funding-source>
                                <funding-source>CAPES</funding-source>
                                <award-id>04/08142-0</award-id>
                            </award-group>
                            <funding-statement>Funded by FAPESP and CAPES</funding-statement>
                        </funding-group>
                    </article-meta>
                </front>
            </article>
        """
        xml_tree = etree.fromstring(xml)
        validator = FundingGroupValidation(xml_tree, self.params)
        results = list(validator.validate_award_id_funding_source_consistency())
        
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["response"], "OK")

    def test_matching_quantities_valid(self):
        """Matching quantities (N sources, N awards) should be valid"""
        xml = """
            <article article-type="research-article" xml:lang="en">
                <front>
                    <article-meta>
                        <funding-group>
                            <award-group>
                                <funding-source>FAPESP</funding-source>
                                <funding-source>CAPES</funding-source>
                                <award-id>04/08142-0</award-id>
                                <award-id>05/09876-5</award-id>
                            </award-group>
                            <funding-statement>Funded by FAPESP and CAPES</funding-statement>
                        </funding-group>
                    </article-meta>
                </front>
            </article>
        """
        xml_tree = etree.fromstring(xml)
        validator = FundingGroupValidation(xml_tree, self.params)
        results = list(validator.validate_award_id_funding_source_consistency())
        
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["response"], "OK")

    def test_inconsistent_quantities_warning(self):
        """Inconsistent quantities should trigger warning"""
        xml = """
            <article article-type="research-article" xml:lang="en">
                <front>
                    <article-meta>
                        <funding-group>
                            <award-group>
                                <funding-source>FAPESP</funding-source>
                                <award-id>04/08142-0</award-id>
                                <award-id>05/09876-5</award-id>
                                <award-id>06/12345-6</award-id>
                            </award-group>
                            <funding-statement>Funded by FAPESP</funding-statement>
                        </funding-group>
                    </article-meta>
                </front>
            </article>
        """
        xml_tree = etree.fromstring(xml)
        validator = FundingGroupValidation(xml_tree, self.params)
        results = list(validator.validate_award_id_funding_source_consistency())
        
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["response"], "WARNING")
        self.assertIn("Inconsistent quantities", results[0]["advice"])


class TestCompleteValidExamples(TestFundingValidationBase):
    """Test complete valid XML examples from the issue"""

    def test_example_1_funding_with_contract(self):
        """Example 1: Funding with contract number"""
        xml = """
            <article article-type="research-article" xml:lang="en">
                <front>
                    <article-meta>
                        <funding-group>
                            <award-group>
                                <funding-source>Fundação de Amparo à Pesquisa do Estado de São Paulo (FAPESP)</funding-source>
                                <award-id>04/08142-0</award-id>
                            </award-group>
                            <funding-statement>This study was supported by Fundação de Amparo à Pesquisa do Estado de São Paulo (FAPESP - Grant no. 04/08142-0; São Paulo, Brazil)</funding-statement>
                        </funding-group>
                    </article-meta>
                </front>
            </article>
        """
        xml_tree = etree.fromstring(xml)
        validator = FundingGroupValidation(xml_tree, self.params)
        
        # All validations should pass
        uniqueness = list(validator.validate_funding_group_uniqueness())
        statement = list(validator.validate_funding_statement_presence())
        source = list(validator.validate_funding_source_in_award_group())
        label = list(validator.validate_label_absence())
        title = list(validator.validate_title_absence())
        consistency = list(validator.validate_award_id_funding_source_consistency())
        
        self.assertEqual(uniqueness[0]["response"], "OK")
        self.assertEqual(statement[0]["response"], "OK")
        self.assertEqual(source[0]["response"], "OK")
        self.assertEqual(label[0]["response"], "OK")
        self.assertEqual(title[0]["response"], "OK")
        self.assertEqual(consistency[0]["response"], "OK")

    def test_example_6_negative_funding_declaration(self):
        """Example 6: Negative funding declaration"""
        xml = """
            <article article-type="research-article" xml:lang="en">
                <front>
                    <article-meta>
                        <funding-group>
                            <funding-statement>Não houve financiamento para esta publicação</funding-statement>
                        </funding-group>
                    </article-meta>
                </front>
            </article>
        """
        xml_tree = etree.fromstring(xml)
        validator = FundingGroupValidation(xml_tree, self.params)
        
        # Should pass all checks (no award-group means no source validation)
        uniqueness = list(validator.validate_funding_group_uniqueness())
        statement = list(validator.validate_funding_statement_presence())
        source = list(validator.validate_funding_source_in_award_group())
        label = list(validator.validate_label_absence())
        title = list(validator.validate_title_absence())
        
        self.assertEqual(uniqueness[0]["response"], "OK")
        self.assertEqual(statement[0]["response"], "OK")
        self.assertEqual(len(source), 0)  # No award-group, so no validation
        self.assertEqual(label[0]["response"], "OK")
        self.assertEqual(title[0]["response"], "OK")


if __name__ == "__main__":
    unittest.main()
