from unittest import TestCase
from lib.validator import ValidationReportXML


class TestReportXML(TestCase):
    def setUp(self):
        self.xml_path = 'tests/samples/0034-7094-rba-69-03-0227.xml'

    def test_report(self):
        validation_report_xml = ValidationReportXML(self.xml_path)
        expected_result = [
            'affliation_validation', 
            'authors_credit_terms_and_urls_validation',
            'authors_orcid_validation',
            'article_license_validation', 
            'article_code_license_validation',
            'article_toc_sections_validation',
            'article_title_validation', 
            'article_xref_id_validation',
            'article_xref_rid_validation', 
            'article_dates_required_order_events_validation', 
            'article_dates_are_complete_validation',
            'article_volume_validation',
            'article_issue_validation',
            'article_supplement_validation'
        ]

        result_generator_validation = validation_report_xml.validation_report()
        for result in result_generator_validation:
            self.assertIn(list(result.keys())[0], expected_result)
