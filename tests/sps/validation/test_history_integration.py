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
        """Test that valid history XML passes validation."""
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
    
    def test_only_received_and_accepted_are_required(self):
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
                        <date date-type="accepted">
                            <day>12</day>
                            <month>03</month>
                            <year>2024</year>
                        </date>
                    </history>
                </article-meta>
            </front>
        </article>
        """
        tree = etree.fromstring(xml)
        rules = get_default_rules()

        for group_result in validate_xml_content(tree, rules):
            if group_result['group'] == 'history':
                items = list(group_result['items'])
                errors = [item for item in items if item and item.get('response') != 'OK']
                self.assertEqual(errors, [])
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


class TestReceivedAcceptedReportedOnce(TestCase):
    def _non_ok(self, xml):
        tree = etree.fromstring(xml)
        results = {}
        for group_result in validate_xml_content(tree, get_default_rules()):
            if group_result['group'] in ('history', 'article dates'):
                results[group_result['group']] = [
                    (item['title'], item['response'])
                    for item in group_result['items']
                    if item and item['title'] in (
                        'missing events',
                        'required date: received',
                        'required date: accepted',
                    ) and item['response'] != 'OK'
                ]
        return results

    def test_missing_received_is_reported_only_in_history(self):
        results = self._non_ok("""
        <article article-type="research-article">
            <front>
                <article-meta>
                    <history>
                        <date date-type="accepted">
                            <day>12</day><month>03</month><year>2024</year>
                        </date>
                    </history>
                </article-meta>
            </front>
        </article>
        """)
        self.assertEqual(
            results,
            {
                'article dates': [],
                'history': [('required date: received', 'CRITICAL')],
            },
        )

    def test_addendum_without_history_has_no_missing_dates(self):
        results = self._non_ok("""
        <article article-type="addendum">
            <front>
                <article-meta>
                    <related-article related-article-type="addended-article"
                        id="ra1" ext-link-type="doi"
                        xmlns:xlink="http://www.w3.org/1999/xlink"
                        xlink:href="10.1590/xxx"/>
                </article-meta>
            </front>
        </article>
        """)
        self.assertEqual(results, {'article dates': [], 'history': []})


class TestArticleDatesKnownDateTypes(TestCase):
    def _history_events(self, xml):
        tree = etree.fromstring(xml)
        for group_result in validate_xml_content(tree, get_default_rules()):
            if group_result['group'] == 'article dates':
                return [
                    (item['title'], item['response'])
                    for item in group_result['items']
                    if item and item['title'] in (
                        'missing events', 'unexpected events', 'ordered events'
                    )
                ]

    def test_reviewer_report_with_reviewer_report_received(self):
        results = self._history_events("""
        <article article-type="reviewer-report">
            <front>
                <article-meta>
                    <history>
                        <date date-type="reviewer-report-received">
                            <day>28</day><month>09</month><year>2025</year>
                        </date>
                    </history>
                </article-meta>
            </front>
        </article>
        """)
        self.assertEqual(
            results,
            [
                ('ordered events', 'OK'),
                ('unexpected events', 'OK'),
                ('missing events', 'OK'),
            ],
        )

    def test_expression_of_concern_date_is_expected(self):
        results = self._history_events("""
        <article article-type="research-article">
            <front>
                <article-meta>
                    <related-article related-article-type="expression-of-concern"
                        id="ra1" ext-link-type="doi"
                        xmlns:xlink="http://www.w3.org/1999/xlink"
                        xlink:href="10.1590/xxx"/>
                    <history>
                        <date date-type="received">
                            <day>15</day><month>01</month><year>2024</year>
                        </date>
                        <date date-type="accepted">
                            <day>12</day><month>03</month><year>2024</year>
                        </date>
                        <date date-type="expression-of-concern">
                            <day>10</day><month>05</month><year>2025</year>
                        </date>
                    </history>
                </article-meta>
            </front>
        </article>
        """)
        self.assertEqual(
            results,
            [
                ('ordered events', 'OK'),
                ('unexpected events', 'OK'),
                ('missing events', 'OK'),
            ],
        )


class TestConditionalHistoryDates(TestCase):
    XML = """
    <article article-type="{article_type}" xmlns:xlink="http://www.w3.org/1999/xlink">
        <front>
            <article-meta>
                <related-article related-article-type="{related_type}"
                    id="ra1" ext-link-type="doi" xlink:href="10.1590/xxx"/>
                <history>
                    <date date-type="received">
                        <day>15</day><month>01</month><year>2024</year>
                    </date>
                    <date date-type="accepted">
                        <day>12</day><month>03</month><year>2024</year>
                    </date>
                </history>
            </article-meta>
        </front>
    </article>
    """

    def _missing_events(self, article_type, related_type):
        tree = etree.fromstring(
            self.XML.format(article_type=article_type, related_type=related_type)
        )
        for group_result in validate_xml_content(tree, get_default_rules()):
            if group_result['group'] == 'article dates':
                for item in group_result['items']:
                    if item and item['title'] == 'missing events':
                        if item['response'] == 'OK':
                            return []
                        return item['adv_params']['missing_events']

    def test_related_article_types_that_require_a_date(self):
        cases = [
            ('addendum', 'corrected'),
            ('correction-forward', 'corrected'),
            ('retraction-forward', 'retracted'),
            ('partial-retraction', 'retracted'),
            ('expression-of-concern', 'expression-of-concern'),
            ('preprint', 'preprint'),
        ]
        for related_type, date_type in cases:
            with self.subTest(related_type=related_type):
                self.assertEqual(
                    self._missing_events('research-article', related_type),
                    [date_type],
                )

    def test_related_article_types_without_required_date(self):
        cases = [
            ('article-commentary', 'commentary-article'),
            ('correction', 'corrected-article'),
            ('retraction', 'retracted-article'),
            ('letter', 'article'),
        ]
        for article_type, related_type in cases:
            with self.subTest(related_type=related_type):
                self.assertEqual(
                    self._missing_events(article_type, related_type), []
                )
