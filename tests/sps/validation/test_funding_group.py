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
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["response"], "OK")


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
            result["data"]["context"], "financial-disclosure"
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
        self.assertEqual(result["data"]["context"], "supported-by")
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
        self.assertEqual(result["data"]["context"], "funding-statement")
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
        self.assertIn("funding-statement", contexts)
        self.assertIn("ack", contexts)
        self.assertIn("financial-disclosure", contexts)
        self.assertIn("supported-by", contexts)

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
        params["award_id_error_level"] = "WARNING"
        validator = FundingGroupValidation(self.xml_tree, params)
        results = list(validator.validate_required_award_ids())
        self.assertEqual(results[0]["response"], "WARNING")

    def test_info_level(self):
        params = dict(self.params)
        params["award_id_error_level"] = "INFO"
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

    def test_sub_article_each_with_one_funding_group_no_false_positive(self):
        """
        Sugestão 1: Two sub-articles, each with its own <article-meta> containing
        exactly one <funding-group>, must NOT trigger a uniqueness error.
        The old implementation (global count) would yield count=2 and raise a
        false positive. The corrected implementation validates per article-meta.
        """
        xml = """
            <article article-type="research-article" xml:lang="pt">
                <front>
                    <article-meta>
                        <funding-group>
                            <funding-statement>Funded by CNPq</funding-statement>
                        </funding-group>
                    </article-meta>
                </front>
                <sub-article article-type="translation" xml:lang="en" id="s1">
                    <front-stub>
                        <article-meta>
                            <funding-group>
                                <funding-statement>Funded by CNPq</funding-statement>
                            </funding-group>
                        </article-meta>
                    </front-stub>
                </sub-article>
            </article>
        """
        xml_tree = etree.fromstring(xml)
        validator = FundingGroupValidation(xml_tree, self.params)
        results = list(validator.validate_funding_group_uniqueness())

        # Two article-meta nodes → two results, both OK
        self.assertEqual(len(results), 2)
        for result in results:
            self.assertEqual(result["response"], "OK")

    def test_sub_article_with_multiple_funding_groups_invalid(self):
        """
        A sub-article <article-meta> with two <funding-group> must be flagged,
        while the main article-meta (with one) remains OK.
        """
        xml = """
            <article article-type="research-article" xml:lang="pt">
                <front>
                    <article-meta>
                        <funding-group>
                            <funding-statement>Funded by CNPq</funding-statement>
                        </funding-group>
                    </article-meta>
                </front>
                <sub-article article-type="translation" xml:lang="en" id="s1">
                    <front-stub>
                        <article-meta>
                            <funding-group>
                                <funding-statement>Funding A</funding-statement>
                            </funding-group>
                            <funding-group>
                                <funding-statement>Funding B</funding-statement>
                            </funding-group>
                        </article-meta>
                    </front-stub>
                </sub-article>
            </article>
        """
        xml_tree = etree.fromstring(xml)
        validator = FundingGroupValidation(xml_tree, self.params)
        results = list(validator.validate_funding_group_uniqueness())

        self.assertEqual(len(results), 2)
        # Main article-meta: OK
        self.assertEqual(results[0]["response"], "OK")
        # Sub-article article-meta: ERROR
        self.assertEqual(results[1]["response"], "ERROR")
        self.assertIn("2 <funding-group>", results[1]["advice"])


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

    def test_multiple_funding_groups_second_missing_statement(self):
        """
        Case C1: Multiple funding-groups, second one missing funding-statement.
        This test validates that each funding-group is checked individually.
        """
        xml = """
            <article article-type="research-article" xml:lang="en">
                <front>
                    <article-meta>
                        <funding-group>
                            <award-group>
                                <funding-source>FAPESP</funding-source>
                            </award-group>
                            <funding-statement>First funding statement</funding-statement>
                        </funding-group>
                        <funding-group>
                            <award-group>
                                <funding-source>CNPq</funding-source>
                            </award-group>
                        </funding-group>
                    </article-meta>
                </front>
            </article>
        """
        xml_tree = etree.fromstring(xml)
        validator = FundingGroupValidation(xml_tree, self.params)
        results = list(validator.validate_funding_statement_presence())
        
        # Should get 2 results: one OK for first funding-group, one CRITICAL for second
        self.assertEqual(len(results), 2)
        
        # First funding-group should be OK
        self.assertEqual(results[0]["response"], "OK")
        self.assertIn("First funding statement", results[0]["got_value"])
        
        # Second funding-group should be CRITICAL (missing funding-statement)
        self.assertEqual(results[1]["response"], "CRITICAL")
        self.assertIn("Add <funding-statement>", results[1]["advice"])
        self.assertIn("index 2", results[1]["advice"])


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


class TestValidateFundingStatement(TestFundingValidationBase):
    """
    Tests for validate_funding_statement — covers the two bugs fixed on 06/03/2026:

    C6 — second <funding-group> without <funding-statement> was silently skipped
         because the old implementation iterated statements_by_lang (one entry
         per language) instead of per <funding-group> node.
    C7 — whitespace from multiple <fn> elements was concatenated raw into the
         advice string; fixed by normalising with " ".join(v.split()).
    """

    # XML with two <funding-group>: first has a statement, second does not (C6)
    XML_TWO_FG_SECOND_MISSING = """
        <article article-type="research-article" xml:lang="pt">
            <front>
                <article-meta>
                    <funding-group>
                        <award-group>
                            <funding-source>FAPESP</funding-source>
                            <award-id>2022/12345-6</award-id>
                        </award-group>
                        <funding-statement>Financiado pela FAPESP processo 2022/12345-6</funding-statement>
                    </funding-group>
                    <funding-group>
                        <award-group>
                            <funding-source>CNPq</funding-source>
                            <award-id>123456</award-id>
                        </award-group>
                    </funding-group>
                </article-meta>
            </front>
            <back>
                <fn-group>
                    <fn fn-type="financial-disclosure" id="fn-fd1">
                        <p>Financiado pela FAPESP processo 2022/12345-6</p>
                    </fn>
                    <fn fn-type="financial-disclosure" id="fn-fd2">
                        <p>Apoio CNPq 123456</p>
                    </fn>
                </fn-group>
            </back>
        </article>
    """

    # XML with a single <funding-group> whose statement matches the fn text (valid)
    XML_SINGLE_FG_VALID = """
        <article article-type="research-article" xml:lang="pt">
            <front>
                <article-meta>
                    <funding-group>
                        <award-group>
                            <funding-source>FAPESP</funding-source>
                            <award-id>2022/12345-6</award-id>
                        </award-group>
                        <funding-statement>Financiado pela FAPESP processo 2022/12345-6</funding-statement>
                    </funding-group>
                </article-meta>
            </front>
            <back>
                <fn-group>
                    <fn fn-type="financial-disclosure" id="fn-fd1">
                        <p>Financiado pela FAPESP processo 2022/12345-6</p>
                    </fn>
                </fn-group>
            </back>
        </article>
    """

    # XML where the fn text has multi-line / extra whitespace (C7 scenario)
    XML_WHITESPACE_FN = """
        <article article-type="research-article" xml:lang="pt">
            <front>
                <article-meta>
                    <funding-group>
                        <award-group>
                            <funding-source>FAPESP</funding-source>
                            <award-id>2022/12345-6</award-id>
                        </award-group>
                        <funding-statement>Outro texto completamente diferente</funding-statement>
                    </funding-group>
                </article-meta>
            </front>
            <back>
                <fn-group>
                    <fn fn-type="financial-disclosure" id="fn-fd1">
                        <p>Financiado
                           pela   FAPESP
                           processo   2022/12345-6</p>
                    </fn>
                    <fn fn-type="financial-disclosure" id="fn-fd2">
                        <p>Apoio   CNPq   123456</p>
                    </fn>
                </fn-group>
            </back>
        </article>
    """

    def test_c6_second_funding_group_without_statement_is_flagged(self):
        """
        C6: When two <funding-group> exist and the second has no
        <funding-statement>, validate_funding_statement must yield TWO results
        — one OK for the first group and one ERROR/CRITICAL for the second.
        The old implementation only yielded one result (silently skipping C6).
        """
        xml_tree = etree.fromstring(self.XML_TWO_FG_SECOND_MISSING)
        validator = FundingGroupValidation(xml_tree, self.params)
        results = list(validator.validate_funding_statement())

        self.assertEqual(len(results), 2, "Must yield one result per <funding-group>")
        # First group has a matching statement → OK
        self.assertEqual(results[0]["response"], "OK")
        # Second group has no statement → should be invalid
        self.assertNotEqual(results[1]["response"], "OK")
        self.assertIsNotNone(results[1]["advice"])
        self.assertIn("<funding-statement>", results[1]["advice"])

    def test_c7_advice_string_has_no_raw_whitespace(self):
        """
        C7: When the reference text in an <fn> element contains extra/multi-line
        whitespace, the advice string must NOT contain sequences of multiple
        spaces or newline characters. Normalization via ' '.join(v.split()) is
        required before building the advice.
        """
        xml_tree = etree.fromstring(self.XML_WHITESPACE_FN)
        validator = FundingGroupValidation(xml_tree, self.params)
        results = list(validator.validate_funding_statement())

        self.assertEqual(len(results), 1)
        result = results[0]
        advice = result.get("advice", "") or ""
        # Must not contain raw runs of whitespace / newlines in the advice
        self.assertNotIn("\n", advice, "Advice must not contain newline characters")
        self.assertNotRegex(advice, r"  +", "Advice must not contain consecutive spaces")

    def test_valid_matching_statement_yields_ok(self):
        """
        When the <funding-statement> closely matches the reference fn text,
        the result must be OK and advice must be None.
        """
        xml_tree = etree.fromstring(self.XML_SINGLE_FG_VALID)
        validator = FundingGroupValidation(xml_tree, self.params)
        results = list(validator.validate_funding_statement())

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["response"], "OK")
        self.assertIsNone(results[0]["advice"])

    def test_early_exit_when_no_award_groups(self):
        """
        When there are no <award-group> elements, validate_funding_statement
        must yield nothing (early return).
        """
        xml = """
            <article article-type="research-article" xml:lang="pt">
                <front>
                    <article-meta>
                        <funding-group>
                            <funding-statement>Estudo realizado sem apoio financeiro externo.</funding-statement>
                        </funding-group>
                    </article-meta>
                </front>
            </article>
        """
        xml_tree = etree.fromstring(xml)
        validator = FundingGroupValidation(xml_tree, self.params)
        results = list(validator.validate_funding_statement())

        self.assertEqual(len(results), 0, "No award-groups → no results expected")


# ========================================
# Sugestão 3: Testes para o orquestrador validate_funding_data
# Requer: from packtools.sps.validation.xml_validations import validate_funding_data
# ========================================


class TestValidateFundingDataOrchestrator(TestFundingValidationBase):
    """
    Sugestão 3: Testes de integração para validate_funding_data em xml_validations.py.

    Verificam que:
      (a) todas as novas validações SPS 1.10 são emitidas pelo orquestrador;
      (b) os níveis configuráveis via funding_data_rules são propagados corretamente,
          especialmente a chave funding_statement_error_level (não
          funding_statement_presence_error_level, que era o nome incorreto no PR).
    """

    # Importação condicional: o teste é ignorado se xml_validations não estiver disponível
    try:
        from packtools.sps.validation.xml_validations import validate_funding_data as _vfd
        _orchestrator_available = True
    except ImportError:
        _orchestrator_available = False

    def setUp(self):
        self.xml_full = """
            <article article-type="research-article" xml:lang="en">
                <front>
                    <article-meta>
                        <funding-group>
                            <award-group>
                                <funding-source>FAPESP</funding-source>
                                <award-id>04/08142-0</award-id>
                            </award-group>
                            <funding-statement>Funded by FAPESP grant 04/08142-0</funding-statement>
                        </funding-group>
                    </article-meta>
                </front>
            </article>
        """
        self.xml_missing_statement = """
            <article article-type="research-article" xml:lang="en">
                <front>
                    <article-meta>
                        <funding-group>
                            <award-group>
                                <funding-source>CNPq</funding-source>
                                <award-id>123456</award-id>
                            </award-group>
                        </funding-group>
                    </article-meta>
                </front>
            </article>
        """

    @unittest.skipUnless(_orchestrator_available, "xml_validations não disponível no path")
    def test_orchestrator_emits_all_new_validations(self):
        """
        Sugestão 3a: validate_funding_data deve emitir resultados para todas as
        validações SPS 1.10 (uniqueness, statement presence, source in award-group,
        label absence, title absence, consistency).
        """
        from packtools.sps.validation.xml_validations import validate_funding_data

        xml_tree = etree.fromstring(self.xml_full)
        params = {
            "funding_data_rules": {
                "special_chars_award_id": ["/", ".", "-"],
                "award_id_error_level": "CRITICAL",
                "funding_statement_error_level": "CRITICAL",
                "funding_group_uniqueness_error_level": "ERROR",
                "funding_source_in_award_group_error_level": "CRITICAL",
                "label_absence_error_level": "ERROR",
                "title_absence_error_level": "ERROR",
                "award_id_consistency_error_level": "WARNING",
            }
        }
        results = list(validate_funding_data(xml_tree, params))
        titles = {r["title"] for r in results}

        self.assertIn("funding-group uniqueness", titles)
        self.assertIn("funding-statement presence", titles)
        self.assertIn("funding-source in award-group", titles)
        self.assertIn("label absence in funding-group", titles)
        self.assertIn("title absence in funding-group", titles)
        self.assertIn("award-id and funding-source consistency", titles)

    @unittest.skipUnless(_orchestrator_available, "xml_validations não disponível no path")
    def test_orchestrator_propagates_funding_statement_error_level(self):
        """
        Sugestão 3b / Sugestão 2: o orquestrador deve ler a chave
        'funding_statement_error_level' (não 'funding_statement_presence_error_level').
        Configurar como WARNING e verificar que o resultado reflete WARNING,
        não o fallback CRITICAL.
        """
        from packtools.sps.validation.xml_validations import validate_funding_data

        xml_tree = etree.fromstring(self.xml_missing_statement)
        params = {
            "funding_data_rules": {
                "special_chars_award_id": ["/", ".", "-"],
                "award_id_error_level": "CRITICAL",
                "funding_statement_error_level": "WARNING",   # chave correta
            }
        }
        results = list(validate_funding_data(xml_tree, params))
        statement_results = [r for r in results if r["title"] == "funding-statement presence"]

        self.assertTrue(
            len(statement_results) > 0,
            "Nenhum resultado de 'funding-statement presence' emitido pelo orquestrador"
        )
        for r in statement_results:
            self.assertEqual(
                r["response"], "WARNING",
                "O nível configurado via 'funding_statement_error_level' não foi propagado "
                "como WARNING; provavelmente o orquestrador ainda usa a chave incorreta "
                "'funding_statement_presence_error_level' ou está caindo no fallback CRITICAL."
            )

    @unittest.skipUnless(_orchestrator_available, "xml_validations não disponível no path")
    def test_orchestrator_propagates_uniqueness_error_level(self):
        """
        Sugestão 3b: funding_group_uniqueness_error_level configurado como WARNING
        deve ser refletido no resultado de uniqueness.
        """
        from packtools.sps.validation.xml_validations import validate_funding_data

        xml_duplicate = """
            <article article-type="research-article" xml:lang="en">
                <front>
                    <article-meta>
                        <funding-group><funding-statement>A</funding-statement></funding-group>
                        <funding-group><funding-statement>B</funding-statement></funding-group>
                    </article-meta>
                </front>
            </article>
        """
        xml_tree = etree.fromstring(xml_duplicate)
        params = {
            "funding_data_rules": {
                "special_chars_award_id": ["/", ".", "-"],
                "funding_group_uniqueness_error_level": "WARNING",
            }
        }
        results = list(validate_funding_data(xml_tree, params))
        uniqueness_results = [r for r in results if r["title"] == "funding-group uniqueness"]

        invalid = [r for r in uniqueness_results if r["response"] != "OK"]
        self.assertTrue(len(invalid) > 0)
        for r in invalid:
            self.assertEqual(r["response"], "WARNING")


if __name__ == "__main__":
    unittest.main()
