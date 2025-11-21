# coding: utf-8
import unittest

from lxml import etree

from packtools.sps.utils.xml_fixer import complete_pub_date


class TestCompletePubDate(unittest.TestCase):
    """Test suite for complete_pub_date function."""
    
    def test_complete_pub_date_only_year(self):
        """Test completing pub-date with only year element."""
        xml = """<article>
            <front>
                <article-meta>
                    <pub-date pub-type="pub">
                        <year>2024</year>
                    </pub-date>
                </article-meta>
            </front>
        </article>"""
        
        tree = etree.fromstring(xml)
        changes = complete_pub_date(tree)
        
        # Should add both month and day
        self.assertEqual(len(changes), 2)
        self.assertEqual(changes[0]['element_added'], 'month')
        self.assertEqual(changes[0]['value'], '6')
        self.assertEqual(changes[1]['element_added'], 'day')
        self.assertEqual(changes[1]['value'], '15')
        
        # Verify XML structure
        pub_date = tree.find('.//pub-date')
        self.assertEqual(pub_date.findtext('year'), '2024')
        self.assertEqual(pub_date.findtext('month'), '6')
        self.assertEqual(pub_date.findtext('day'), '15')
        
        # Verify order: year, month, day
        elements = [elem.tag for elem in pub_date]
        self.assertEqual(elements, ['year', 'month', 'day'])
    
    def test_complete_pub_date_year_and_month(self):
        """Test completing pub-date with year and month elements."""
        xml = """<article>
            <front>
                <article-meta>
                    <pub-date pub-type="pub">
                        <year>2024</year>
                        <month>3</month>
                    </pub-date>
                </article-meta>
            </front>
        </article>"""
        
        tree = etree.fromstring(xml)
        changes = complete_pub_date(tree)
        
        # Should add only day
        self.assertEqual(len(changes), 1)
        self.assertEqual(changes[0]['element_added'], 'day')
        self.assertEqual(changes[0]['value'], '15')
        
        # Verify XML structure
        pub_date = tree.find('.//pub-date')
        self.assertEqual(pub_date.findtext('year'), '2024')
        self.assertEqual(pub_date.findtext('month'), '3')
        self.assertEqual(pub_date.findtext('day'), '15')
        
        # Verify order
        elements = [elem.tag for elem in pub_date]
        self.assertEqual(elements, ['year', 'month', 'day'])
    
    def test_complete_pub_date_already_complete(self):
        """Test that complete pub-date is not modified."""
        xml = """<article>
            <front>
                <article-meta>
                    <pub-date pub-type="pub">
                        <year>2024</year>
                        <month>3</month>
                        <day>20</day>
                    </pub-date>
                </article-meta>
            </front>
        </article>"""
        
        tree = etree.fromstring(xml)
        changes = complete_pub_date(tree)
        
        # Should not add anything
        self.assertEqual(len(changes), 0)
        
        # Verify XML structure unchanged
        pub_date = tree.find('.//pub-date')
        self.assertEqual(pub_date.findtext('year'), '2024')
        self.assertEqual(pub_date.findtext('month'), '3')
        self.assertEqual(pub_date.findtext('day'), '20')
    
    def test_complete_pub_date_with_publication_format_electronic(self):
        """Test completing pub-date with publication-format='electronic'."""
        xml = """<article>
            <front>
                <article-meta>
                    <pub-date publication-format="electronic" date-type="pub">
                        <year>2024</year>
                    </pub-date>
                </article-meta>
            </front>
        </article>"""
        
        tree = etree.fromstring(xml)
        changes = complete_pub_date(tree)
        
        # Should add both month and day
        self.assertEqual(len(changes), 2)
        self.assertEqual(changes[0]['element_added'], 'month')
        self.assertEqual(changes[1]['element_added'], 'day')
        
        # Verify XML structure
        pub_date = tree.find('.//pub-date')
        self.assertEqual(pub_date.findtext('month'), '6')
        self.assertEqual(pub_date.findtext('day'), '15')
    
    def test_complete_pub_date_ignores_other_pub_types(self):
        """Test that pub-date with other pub-types are ignored."""
        xml = """<article>
            <front>
                <article-meta>
                    <pub-date pub-type="collection">
                        <year>2024</year>
                    </pub-date>
                </article-meta>
            </front>
        </article>"""
        
        tree = etree.fromstring(xml)
        changes = complete_pub_date(tree)
        
        # Should not add anything
        self.assertEqual(len(changes), 0)
        
        # Verify pub-date is unchanged
        pub_date = tree.find('.//pub-date')
        self.assertIsNone(pub_date.find('month'))
        self.assertIsNone(pub_date.find('day'))
    
    def test_complete_pub_date_custom_defaults(self):
        """Test completing pub-date with custom default values."""
        xml = """<article>
            <front>
                <article-meta>
                    <pub-date pub-type="pub">
                        <year>2024</year>
                    </pub-date>
                </article-meta>
            </front>
        </article>"""
        
        tree = etree.fromstring(xml)
        changes = complete_pub_date(tree, default_day=1, default_month=1)
        
        # Should add both month and day with custom values
        self.assertEqual(len(changes), 2)
        self.assertEqual(changes[0]['value'], '1')
        self.assertEqual(changes[1]['value'], '1')
        
        # Verify XML structure
        pub_date = tree.find('.//pub-date')
        self.assertEqual(pub_date.findtext('month'), '1')
        self.assertEqual(pub_date.findtext('day'), '1')
    
    def test_complete_pub_date_invalid_day(self):
        """Test that invalid default_day raises ValueError."""
        xml = """<article>
            <front>
                <article-meta>
                    <pub-date pub-type="pub">
                        <year>2024</year>
                    </pub-date>
                </article-meta>
            </front>
        </article>"""
        
        tree = etree.fromstring(xml)
        
        # Test day < 1
        with self.assertRaises(ValueError) as context:
            complete_pub_date(tree, default_day=0, default_month=6)
        self.assertIn("default_day must be between 1 and 31", str(context.exception))
        
        # Test day > 31
        with self.assertRaises(ValueError) as context:
            complete_pub_date(tree, default_day=32, default_month=6)
        self.assertIn("default_day must be between 1 and 31", str(context.exception))
    
    def test_complete_pub_date_invalid_month(self):
        """Test that invalid default_month raises ValueError."""
        xml = """<article>
            <front>
                <article-meta>
                    <pub-date pub-type="pub">
                        <year>2024</year>
                    </pub-date>
                </article-meta>
            </front>
        </article>"""
        
        tree = etree.fromstring(xml)
        
        # Test month < 1
        with self.assertRaises(ValueError) as context:
            complete_pub_date(tree, default_day=15, default_month=0)
        self.assertIn("default_month must be between 1 and 12", str(context.exception))
        
        # Test month > 12
        with self.assertRaises(ValueError) as context:
            complete_pub_date(tree, default_day=15, default_month=13)
        self.assertIn("default_month must be between 1 and 12", str(context.exception))
    
    def test_complete_pub_date_multiple_pub_dates(self):
        """Test completing multiple pub-date elements."""
        xml = """<article>
            <front>
                <article-meta>
                    <pub-date pub-type="pub">
                        <year>2024</year>
                    </pub-date>
                    <pub-date publication-format="electronic" date-type="collection">
                        <year>2023</year>
                        <month>12</month>
                    </pub-date>
                </article-meta>
            </front>
        </article>"""
        
        tree = etree.fromstring(xml)
        changes = complete_pub_date(tree)
        
        # Should add month and day to first, day to second
        self.assertEqual(len(changes), 3)
        
        # Verify first pub-date
        pub_dates = tree.findall('.//pub-date')
        self.assertEqual(pub_dates[0].findtext('month'), '6')
        self.assertEqual(pub_dates[0].findtext('day'), '15')
        
        # Verify second pub-date
        self.assertEqual(pub_dates[1].findtext('month'), '12')
        self.assertEqual(pub_dates[1].findtext('day'), '15')
    
    def test_complete_pub_date_no_year(self):
        """Test that pub-date without year is not processed."""
        xml = """<article>
            <front>
                <article-meta>
                    <pub-date pub-type="pub">
                        <month>6</month>
                    </pub-date>
                </article-meta>
            </front>
        </article>"""
        
        tree = etree.fromstring(xml)
        changes = complete_pub_date(tree)
        
        # Should not process this pub-date
        self.assertEqual(len(changes), 0)
        
        # Verify pub-date is unchanged
        pub_date = tree.find('.//pub-date')
        self.assertIsNone(pub_date.find('year'))
        self.assertIsNone(pub_date.find('day'))
    
    def test_complete_pub_date_xpath_in_changes(self):
        """Test that changes include correct xpath."""
        xml = """<article>
            <front>
                <article-meta>
                    <pub-date pub-type="pub">
                        <year>2024</year>
                    </pub-date>
                </article-meta>
            </front>
        </article>"""
        
        tree = etree.fromstring(xml)
        changes = complete_pub_date(tree)
        
        # Verify xpath is present in changes
        self.assertIn('xpath', changes[0])
        self.assertIn('pub-date', changes[0]['xpath'])
    
    def test_complete_pub_date_preserves_other_elements(self):
        """Test that other elements in pub-date are preserved."""
        xml = """<article>
            <front>
                <article-meta>
                    <pub-date pub-type="pub">
                        <year>2024</year>
                        <season>Spring</season>
                    </pub-date>
                </article-meta>
            </front>
        </article>"""
        
        tree = etree.fromstring(xml)
        changes = complete_pub_date(tree)
        
        # Should add month and day
        self.assertEqual(len(changes), 2)
        
        # Verify season is preserved
        pub_date = tree.find('.//pub-date')
        self.assertEqual(pub_date.findtext('season'), 'Spring')


if __name__ == '__main__':
    unittest.main()
