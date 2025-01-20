import unittest

from packtools.sps.utils.xml_utils import get_xml_tree
from packtools.sps.validation.funding_group import FundingGroupValidation


def callable_validation_success(award_id):
    """Função auxiliar para simular validação bem-sucedida de award_id"""
    return True


def callable_validation_fail(award_id):
    """Função auxiliar para simular validação falha de award_id"""
    return False


class FundingGroupValidationTest(unittest.TestCase):
    def test_funding_sources_exist_validation_empty_xml(self):
        """Testa validação quando não há informações de funding no XML"""
        xml_str = """
            <article article-type="research-article" xml:lang="pt">
                <front><article-meta></article-meta></front>
            </article>
            """
        xml_tree = get_xml_tree(xml_str)
        obtained = list(FundingGroupValidation(xml_tree).funding_sources_exist_validation())
        self.assertEqual([], obtained)

    def test_funding_sources_exist_validation_with_award_group(self):
        """Testa validação com award-group contendo funding_source e award_id"""
        xml_str = """
            <article article-type="research-article" xml:lang="pt">
                <front>
                    <article-meta>
                        <funding-group>
                            <award-group>
                                <funding-source>Natural Science Foundation</funding-source>
                                <award-id>2019JJ40269</award-id>
                            </award-group>
                        </funding-group>
                    </article-meta>
                </front>
            </article>
            """
        xml_tree = get_xml_tree(xml_str)
        validator = FundingGroupValidation(xml_tree)
        obtained = list(validator.funding_sources_exist_validation())
        
        self.assertEqual(len(obtained), 1)
        result = obtained[0]
        
        # Verifica campos básicos
        self.assertEqual(result['title'], 'Funding source element validation')
        self.assertEqual(result['item'], 'award-group')
        self.assertEqual(result['sub_item'], 'funding-source')
        self.assertEqual(result['response'], 'OK')
        
        # Verifica a estrutura de dados
        data = result['data']
        self.assertEqual(data['article_type'], 'research-article')
        self.assertEqual(data['article_lang'], 'pt')
        self.assertEqual(len(data['award_groups']), 1)
        self.assertEqual(data['award_groups'][0]['funding-source'], ['Natural Science Foundation'])
        self.assertEqual(data['award_groups'][0]['award-id'], ['2019JJ40269'])

    def test_funding_sources_exist_validation_with_financial_disclosure(self):
        """Testa validação com fn-type='financial-disclosure'"""
        xml_str = """
            <article article-type="research-article" xml:lang="pt">
                <back>
                    <fn-group>
                        <fn fn-type="financial-disclosure">
                            <p>Research Foundation</p>
                            <p>Grant No: 123-456</p>
                        </fn>
                    </fn-group>
                </back>
            </article>
            """
        xml_tree = get_xml_tree(xml_str)
        params = {
            'special_chars_award_id': ['-']
        }
        validator = FundingGroupValidation(xml_tree, params)
        obtained = list(validator.funding_sources_exist_validation())
        
        self.assertEqual(len(obtained), 1)
        result = obtained[0]
        
        # Verifica campos específicos de financial-disclosure
        self.assertEqual(result['item'], 'fn')
        self.assertEqual(result['sub_item'], "@fn-type='financial-disclosure'")
        self.assertEqual('Research Foundation Grant No: 123-456', result['data']['financial_disclosure'][0]['text'])
        self.assertEqual('123-456', result['data']['financial_disclosure'][0]['look-like-award-id'])

    def test_award_id_format_validation_success(self):
        """Testa validação bem-sucedida de formato de award_id"""
        xml_str = """
            <article article-type="research-article" xml:lang="pt">
                <front>
                    <article-meta>
                        <funding-group>
                            <award-group>
                                <funding-source>Foundation</funding-source>
                                <award-id>2019JJ40269</award-id>
                            </award-group>
                        </funding-group>
                    </article-meta>
                </front>
            </article>
            """
        xml_tree = get_xml_tree(xml_str)
        params = {
            'callable_validation': callable_validation_success
        }
        validator = FundingGroupValidation(xml_tree, params)
        obtained = list(validator.award_id_format_validation())
        
        self.assertEqual(len(obtained), 1)
        result = obtained[0]
        self.assertEqual(result['response'], 'OK')
        self.assertEqual(result['got_value'], '2019JJ40269')

    def test_award_id_format_validation_fail(self):
        """Testa falha na validação de formato de award_id"""
        xml_str = """
            <article article-type="research-article" xml:lang="pt">
                <front>
                    <article-meta>
                        <funding-group>
                            <award-group>
                                <funding-source>Foundation</funding-source>
                                <award-id>invalid-format</award-id>
                            </award-group>
                        </funding-group>
                    </article-meta>
                </front>
            </article>
            """
        xml_tree = get_xml_tree(xml_str)
        params = {
            'callable_validation': callable_validation_fail,
            'error_level': "ERROR"
        }
        validator = FundingGroupValidation(xml_tree, params)
        obtained = list(validator.award_id_format_validation())
        
        self.assertEqual(len(obtained), 1)
        result = obtained[0]
        self.assertEqual(result['response'], 'ERROR')
        self.assertEqual(result['got_value'], 'invalid-format')
        self.assertEqual(result['expected_value'], 'a valid value for award id')

    def test_award_id_format_validation_no_award_id(self):
        """Testa validação quando não há award_id no XML"""
        xml_str = """
            <article article-type="research-article" xml:lang="pt">
                <front>
                    <article-meta>
                        <funding-group>
                            <award-group>
                                <funding-source>Foundation</funding-source>
                            </award-group>
                        </funding-group>
                    </article-meta>
                </front>
            </article>
            """
        xml_tree = get_xml_tree(xml_str)
        validator = FundingGroupValidation(xml_tree)
        obtained = list(validator.award_id_format_validation())
        self.assertEqual([], obtained)