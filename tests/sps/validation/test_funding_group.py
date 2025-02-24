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


class TestFundingValidation(unittest.TestCase):
    def setUp(self):
        self.xml_success = """
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
                        <p>Project 123.456-7</p>
                    </ack>
                </back>
            </article>
        """

        self.xml_failure = """
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
                        <p>Project 987.654-3</p>
                    </ack>
                </back>
            </article>
        """
        self.params = {"special_chars_award_id": ["/", ".", "-"], "error_level": "ERROR"}

    def test_validate_funding_statement_success(self):
        xml_tree = etree.fromstring(self.xml_success)
        validator = FundingGroupValidation(xml_tree, self.params)
        results = list(validator.validate_funding_statement())
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["response"], "OK")
        self.assertIsNone(results[0]["advice"])

    def test_validate_funding_statement_failure(self):
        xml_tree = etree.fromstring(self.xml_failure)
        validator = FundingGroupValidation(xml_tree, self.params)
        results = list(validator.validate_funding_statement())
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["response"], "ERROR")
        self.assertEqual(results[0]["advice"], "Ensure that funding information 'Project 987.654-3' from ack is replicated in <funding-statement>.")



if __name__ == "__main__":
    unittest.main()
