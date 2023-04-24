from unittest import TestCase
from packtools.validation_report import ValidationReportXML


class TestReportXML(TestCase):
    def setUp(self):
        self.xml_path = 'tests/samples/0034-7094-rba-69-03-0227.xml'

    def test_report(self):
        validation_report_xml = ValidationReportXML(self.xml_path)
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
        for expected, result in zip(expected_result, result_generator):
            self.assertEqual(expected, list(result.keys())[0])
