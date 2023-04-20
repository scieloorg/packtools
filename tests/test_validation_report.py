from unittest import TestCase
from packtools.validation_report import ValidationReportXML

from tests.sps.validation.test_article_authors import credit_terms_and_urls


class TestReportXML(TestCase):
    def setUp(self):
        self.xml_path = 'tests/samples/0034-7094-rba-69-03-0227.xml'

    def test_report(self):
        validation_report_xml = ValidationReportXML(self.xml_path)
        data = {
            'credit_terms_and_urls': credit_terms_and_urls,
            'expected_value_license': {
                'lang': 'pt',
                'link': 'http://creativecommons.org/licenses/by/4.0/',
                'licence_p': 'Este é um artigo publicado em acesso aberto sob uma licença Creative Commons.'
            },
            'expected_code': '4.0',
            'expected_version': 'by',
            'expected_toc_sections': {
                "es": ["Nome da seção do artigo em espanhol"],
                "en": ["Nome da seção do sub-artigo em inglês"]
            },
            'order': [
                "received", 
                "rev-request", 
                "rev-recd", 
                "accepted", 
                "approved"
            ],
            'required_events': [
                "received", 
                "approved"
            ],
            'expected_value_volume': '10',
            'expected_value_supplment': '10',
            'expected_value_issue': '10',
        }

        expected_result = [
            'affliation_validation', 
            'authors_role_orcid_validation', 
            'license_code_validation', 
            'toc_sections_and_title_validation', 
            'xref_id_rid_validation', 
            'date_validation', 
            'issue_validation'
        ]
        result_generator = validation_report_xml.validation_report()
        
        for expected, result in zip(expected_result, list(result_generator)):
            self.assertEqual(expected, list(result.keys())[0])


