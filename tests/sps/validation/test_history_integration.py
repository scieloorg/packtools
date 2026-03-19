"""
Integration tests for history validation in the orchestrator.

This module tests that the history validation is properly integrated
into the xml_validator orchestrator.
"""

from unittest import TestCase
from lxml import etree

from packtools.sps.validation.xml_validator import validate_xml_content
from packtools.sps.validation.xml_validator_rules import get_default_rules


class TestHistoryIntegration(TestCase):
    """Tests for history validation integration in the orchestrator."""
    
    def test_history_validation_group_exists(self):
        """Test that the history validation group is present in orchestrator."""
        xml = """
        <article article-type="research-article">
            <front>
                <article-meta>
                    <history>
                        <date date-type="received">
                            <day>15</day>
                            <month>03</month>
                            <year>2024</year>
                        </date>
                        <date date-type="accepted">
                            <day>12</day>
                            <month>05</month>
                            <year>2024</year>
                        </date>
                    </history>
                </article-meta>
            </front>
        </article>
        """
        tree = etree.fromstring(xml)
        rules = get_default_rules()
        
        # Check that history group exists
        groups = []
        for group_result in validate_xml_content(tree, rules):
            groups.append(group_result['group'])
        
        self.assertIn('history', groups, 
                     f"History group not found. Available groups: {groups}")
    
    def test_history_validation_with_valid_xml(self):
        """Test that valid history XML passes validation.

        The XML must include all date types marked as required=true in
        history_dates_rules.json: received, rev-request, rev-recd, accepted, pub.
        """
        xml = """
        <article article-type="research-article">
            <front>
                <article-meta>
                    <history>
                        <date date-type="received">
                            <day>15</day>
                            <month>01</month>
                            <year>2024</year>
                        </date>
                        <date date-type="rev-request">
                            <day>01</day>
                            <month>02</month>
                            <year>2024</year>
                        </date>
                        <date date-type="rev-recd">
                            <day>20</day>
                            <month>02</month>
                            <year>2024</year>
                        </date>
                        <date date-type="accepted">
                            <day>12</day>
                            <month>03</month>
                            <year>2024</year>
                        </date>
                        <date date-type="pub">
                            <year>2024</year>
                        </date>
                    </history>
                </article-meta>
            </front>
        </article>
        """
        tree = etree.fromstring(xml)
        rules = get_default_rules()
        
        # Get history validation results
        for group_result in validate_xml_content(tree, rules):
            if group_result['group'] == 'history':
                items = list(group_result['items'])
                errors = [item for item in items if item and item.get('response') != 'OK']
                
                # Should have no errors
                self.assertEqual(len(errors), 0, 
                               f"Expected no errors, but found: {errors}")
                # Should have some validations
                self.assertGreater(len(items), 0, 
                                 "Should have at least one validation")
                break
        else:
            self.fail("History validation group not found")
    
    def test_history_validation_with_invalid_xml(self):
        """Test that invalid history XML is caught by validation."""
        xml = """
        <article article-type="research-article">
            <front>
                <article-meta>
                    <history>
                        <date date-type="preprint">
                            <year>2023</year>
                        </date>
                    </history>
                </article-meta>
            </front>
        </article>
        """
        tree = etree.fromstring(xml)
        rules = get_default_rules()
        
        # Get history validation results
        for group_result in validate_xml_content(tree, rules):
            if group_result['group'] == 'history':
                items = list(group_result['items'])
                errors = [item for item in items if item and item.get('response') != 'OK']
                
                # Should have errors for missing required dates
                self.assertGreater(len(errors), 0, 
                                 "Expected errors for missing required dates")
                
                # Check for specific errors
                error_titles = [err.get('title') for err in errors]
                self.assertIn('required date: received', error_titles)
                self.assertIn('required date: accepted', error_titles)
                break
        else:
            self.fail("History validation group not found")
    
    def test_history_validation_with_multiple_history_elements(self):
        """Test that multiple history elements are caught."""
        xml = """
        <article article-type="research-article">
            <front>
                <article-meta>
                    <history>
                        <date date-type="received">
                            <day>15</day>
                            <month>03</month>
                            <year>2024</year>
                        </date>
                    </history>
                    <history>
                        <date date-type="accepted">
                            <day>12</day>
                            <month>05</month>
                            <year>2024</year>
                        </date>
                    </history>
                </article-meta>
            </front>
        </article>
        """
        tree = etree.fromstring(xml)
        rules = get_default_rules()
        
        # Get history validation results
        for group_result in validate_xml_content(tree, rules):
            if group_result['group'] == 'history':
                items = list(group_result['items'])
                errors = [item for item in items if item and item.get('response') != 'OK']
                
                # Should have error for duplicate history
                error_titles = [err.get('title') for err in errors]
                self.assertIn('history uniqueness', error_titles)
                break
        else:
            self.fail("History validation group not found")
    
    def test_history_validation_with_exempt_article_type(self):
        """Test that exempt article types don't require received/accepted dates."""
        xml = """
        <article article-type="retraction">
            <front>
                <article-meta>
                    <history>
                        <date date-type="retracted">
                            <day>20</day>
                            <month>06</month>
                            <year>2024</year>
                        </date>
                    </history>
                </article-meta>
            </front>
        </article>
        """
        tree = etree.fromstring(xml)
        rules = get_default_rules()
        
        # Get history validation results
        for group_result in validate_xml_content(tree, rules):
            if group_result['group'] == 'history':
                items = list(group_result['items'])
                errors = [item for item in items if item and item.get('response') != 'OK']
                
                # Should have no errors (retraction is exempt)
                self.assertEqual(len(errors), 0, 
                               f"Expected no errors for exempt article type, but found: {errors}")
                break
        else:
            self.fail("History validation group not found")
