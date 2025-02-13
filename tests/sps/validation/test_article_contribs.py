from unittest import TestCase
from unittest.mock import MagicMock, Mock, patch

from lxml import etree

from packtools.sps.models.article_contribs import XMLContribs
from packtools.sps.validation.article_contribs import (
    CollabListValidation,
    ContribRoleValidation,
    ContribValidation,
    XMLContribsValidation,
)

import unittest
from unittest.mock import Mock, patch
from lxml import etree


class TestContribValidation(unittest.TestCase):
    def setUp(self):
        self.sample_xml = """<?xml version="1.0" encoding="utf-8"?>
        <article article-type="research-article">
            <front>
                <article-meta>
                    <contrib-group>
                        <contrib contrib-type="author">
                            <name>
                                <surname>Smith</surname>
                                <given-names>John</given-names>
                            </name>
                            <role specific-use="author">
                                <text>Writing – original draft</text>
                            </role>
                            <xref ref-type="aff" rid="aff1"/>
                            <contrib-id contrib-id-type="orcid">0000-0002-1234-5678</contrib-id>
                        </contrib>
                        <contrib contrib-type="author">
                            <collab>Research Group A</collab>
                        </contrib>
                        <aff id="aff1">
                            <institution>University Example</institution>
                        </aff>
                    </contrib-group>
                </article-meta>
            </front>
        </article>
        """
        self.xmltree = etree.fromstring(self.sample_xml.encode('utf-8'))
        self.contrib_data = {
            "contrib_full_name": "Smith, John",
            "contrib_name": {"surname": "Smith", "given-names": "John"},
            "contrib_type": "author",
            "contrib_ids": {"orcid": "0000-0002-1234-5678"},
            "contrib_role": [{
                "specific-use": "author",
                "text": "Writing – original draft"
            }],
            "affs": [{"id": "aff1"}]
        }
        self.validator = ContribValidation(self.contrib_data, {})

    def test_validate_role_success(self):
        """Test validate_role with valid contributor role"""
        results = list(self.validator.validate_role())
        errors = [r for r in results if r['response'] != 'OK']
        self.assertEqual(len(errors), 1)

    def test_validate_role_missing(self):
        """Test validate_role with missing role"""
        contrib_data = self.contrib_data.copy()
        del contrib_data["contrib_role"]
        validator = ContribValidation(contrib_data, {
            "parent": "article",
            "parent_article_type": "research-article"
        })
        
        results = list(validator.validate_role())
        errors = [r for r in results if r['response'] != 'OK']
        
        self.assertEqual(len(errors), 1)
        responses = [error['response'] for error in errors]
        advices = [error['advice'] for error in errors]
        
        expected_responses = ['ERROR']
        expected_advices = ['Mark the contrib role. Consult SPS documentation for detailed instructions']
        
        self.assertEqual(responses, expected_responses)
        self.assertEqual(advices, expected_advices)

    def test_validate_orcid_format_success(self):
        """Test validate_orcid_format with valid ORCID"""
        results = list(self.validator.validate_orcid_format())
        errors = [r for r in results if r['response'] != 'OK']
        self.assertEqual(len(errors), 0)

    def test_validate_orcid_format_invalid(self):
        """Test validate_orcid_format with invalid ORCID"""
        contrib_data = self.contrib_data.copy()
        contrib_data["contrib_ids"] = {"orcid": "invalid-orcid"}
        validator = ContribValidation(contrib_data, {})
        
        results = list(validator.validate_orcid_format())
        errors = [r for r in results if r['response'] != 'OK']
        
        self.assertEqual(len(errors), 1)
        responses = [error['response'] for error in errors]
        advices = [error['advice'] for error in errors]
        
        expected_responses = ['ERROR']
        expected_advices = ['Fix ORCID format <contrib-id contrib-id-type="orcid">invalid-orcid</contrib-id>']
        
        self.assertEqual(responses, expected_responses)
        self.assertEqual(advices, expected_advices)

    def test_validate_orcid_is_registered_success(self):
        """Test validate_orcid_is_registered with registered ORCID"""
        mock_orcid_validator = Mock(return_value={"status": "registered"})
        self.validator.data["is_orcid_registered"] = mock_orcid_validator
        
        results = list(self.validator.validate_orcid_is_registered())
        errors = [r for r in results if r['response'] != 'OK']
        self.assertEqual(len(errors), 0)

    def test_validate_orcid_is_registered_not_found(self):
        """Test validate_orcid_is_registered with unregistered ORCID"""
        mock_orcid_validator = Mock(return_value={"status": "not_found"})
        self.validator.data["is_orcid_registered"] = mock_orcid_validator
        
        results = list(self.validator.validate_orcid_is_registered())
        errors = [r for r in results if r['response'] != 'OK']
        
        self.assertEqual(len(errors), 1)
        responses = [error['response'] for error in errors]
        advices = [error['advice'] for error in errors]
        
        expected_responses = ['ERROR']
        expected_advices = ['Check ORCID <contrib-id contrib-id-type="orcid">0000-0002-1234-5678</contrib-id> belongs to Smith, John']
        
        self.assertEqual(responses, expected_responses)
        self.assertEqual(advices, expected_advices)


class TestContribRoleValidation(unittest.TestCase):
    def setUp(self):
        self.contrib_data = {
            "contrib_full_name": "Smith, John",
            "contrib_type": "author"
        }
        self.role_data = {
            "specific-use": "author",
            "content-type": "http://credit.niso.org/contributor-roles/writing-original-draft/",
            "text": "Writing – original draft"
        }
        self.validator = ContribRoleValidation(self.contrib_data, self.role_data, {})

    def test_validate_credit_success(self):
        """Test validate_credit with valid CRediT taxonomy"""
        results = list(self.validator.validate_credit())
        errors = [r for r in results if r['response'] != 'OK']
        self.assertEqual(len(errors), 0)

    def test_validate_credit_invalid_uri(self):
        """Test validate_credit with invalid URI"""
        role_data = self.role_data.copy()
        role_data["content-type"] = "invalid-uri"
        validator = ContribRoleValidation(self.contrib_data, role_data, {})
        
        results = list(validator.validate_credit())
        errors = [r for r in results if r['response'] != 'OK']
        
        self.assertEqual(len(errors), 1)  # Should fail both URI and term validation
        responses = [error['response'] for error in errors]
        expected_responses = ['ERROR']
        self.assertEqual(responses, expected_responses)

    def test_validate_role_specific_use_success(self):
        """Test validate_role_specific_use with valid role"""
        results = list(self.validator.validate_role_specific_use())
        errors = [r for r in results if r['response'] != 'OK']
        self.assertEqual(len(errors), 0)

    def test_validate_role_specific_use_invalid(self):
        """Test validate_role_specific_use with invalid role"""
        role_data = self.role_data.copy()
        role_data["specific-use"] = "invalid-role"
        validator = ContribRoleValidation(self.contrib_data, role_data, {})
        
        results = list(validator.validate_role_specific_use())
        errors = [r for r in results if r['response'] != 'OK']
        
        self.assertEqual(len(errors), 1)
        responses = [error['response'] for error in errors]
        advices = [error['advice'] for error in errors]
        
        expected_responses = ['ERROR']
        expected_advices = ["Replace invalid-role in <role specific-use=\"invalid-role\"> with ['author', 'editor', 'reviewer', 'translator']"]
        
        self.assertEqual(responses, expected_responses)
        self.assertEqual(advices, expected_advices)


class TestXMLContribsValidation(unittest.TestCase):
    def setUp(self):
        self.sample_xml = """<?xml version="1.0" encoding="utf-8"?>
        <article article-type="research-article">
            <front>
                <article-meta>
                    <contrib-group>
                        <contrib contrib-type="author">
                            <name>
                                <surname>Smith</surname>
                                <given-names>John</given-names>
                            </name>
                            <contrib-id contrib-id-type="orcid">0000-0002-1234-5678</contrib-id>
                        </contrib>
                        <contrib contrib-type="author">
                            <name>
                                <surname>Johnson</surname>
                                <given-names>Mary</given-names>
                            </name>
                            <contrib-id contrib-id-type="orcid">0000-0002-8765-4321</contrib-id>
                        </contrib>
                    </contrib-group>
                </article-meta>
            </front>
        </article>
        """
        self.xmltree = etree.fromstring(self.sample_xml.encode('utf-8'))
        self.validator = XMLContribsValidation(self.xmltree, {})

    def test_validate_orcid_is_unique_success(self):
        """Test validate_orcid_is_unique with unique ORCIDs"""
        results = list(self.validator.validate_orcid_is_unique())
        errors = [r for r in results if r['response'] != 'OK']
        self.assertEqual(len(errors), 0)

    def test_validate_orcid_is_unique_duplicate(self):
        """Test validate_orcid_is_unique with duplicate ORCIDs"""
        xml_with_duplicate = """<?xml version="1.0" encoding="utf-8"?>
        <article article-type="research-article">
            <front>
                <article-meta>
                    <contrib-group>
                        <contrib contrib-type="author">
                            <name>
                                <surname>Smith</surname>
                                <given-names>John</given-names>
                            </name>
                            <contrib-id contrib-id-type="orcid">0000-0002-1234-5678</contrib-id>
                        </contrib>
                        <contrib contrib-type="author">
                            <name>
                                <surname>Johnson</surname>
                                <given-names>Mary</given-names>
                            </name>
                            <contrib-id contrib-id-type="orcid">0000-0002-1234-5678</contrib-id>
                        </contrib>
                    </contrib-group>
                </article-meta>
            </front>
        </article>
        """
        xmltree = etree.fromstring(xml_with_duplicate.encode('utf-8'))
        validator = XMLContribsValidation(xmltree, {})
        
        results = list(validator.validate_orcid_is_unique())
        errors = [r for r in results if r['response'] != 'OK']
        
        self.assertEqual(len(errors), 1)
        responses = [error['response'] for error in errors]
        advices = [error['advice'] for error in errors]
        
        expected_responses = ['ERROR']
        expected_advices = ['ORCID must be unique. 0000-0002-1234-5678 is assigned to [\'John Smith\', \'Mary Johnson\']']
        
        self.assertEqual(responses, expected_responses)
        self.assertEqual(advices, expected_advices)


if __name__ == '__main__':
    unittest.main()