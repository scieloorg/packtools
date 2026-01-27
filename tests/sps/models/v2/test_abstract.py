from unittest import TestCase
from lxml import etree

from packtools.sps.models.v2.abstract import Abstract


class AbstractTextWithSectionsTest(TestCase):
    """Test the text property when abstract has sections"""

    def setUp(self):
        xml = """
        <abstract xml:lang="en">
            <title>Abstract</title>
            <sec>
                <title>Objective</title>
                <p>To examine the effectiveness of day hospital attendance in prolonging independent living for elderly people.</p>
            </sec>
            <sec>
                <title>Design</title>
                <p>Systematic review of 12 controlled clinical trials (available by January 1997) comparing day hospital care with comprehensive care (five trials), domiciliary care (four trials), or no comprehensive care (three trials).</p>
            </sec>
        </abstract>
        """
        self.node = etree.fromstring(xml)
        self.abstract = Abstract(
            self.node, lang="en", 
            tags_to_keep=None, tags_to_keep_with_content=None,
            tags_to_remove_with_content=None, tags_to_convert_to_html=None
        )

    def test_text_property_with_sections(self):
        """Test that text property includes title and p from each section"""
        expected = "Objective To examine the effectiveness of day hospital attendance in prolonging independent living for elderly people. Design Systematic review of 12 controlled clinical trials (available by January 1997) comparing day hospital care with comprehensive care (five trials), domiciliary care (four trials), or no comprehensive care (three trials)."
        self.assertEqual(self.abstract.text, expected)

    def test_data_contains_text_key(self):
        """Test that data dictionary contains the text key"""
        data = self.abstract.data
        self.assertIn("text", data)
        self.assertIsInstance(data["text"], str)

    def test_data_text_value_with_sections(self):
        """Test that data['text'] has correct value for abstract with sections"""
        expected = "Objective To examine the effectiveness of day hospital attendance in prolonging independent living for elderly people. Design Systematic review of 12 controlled clinical trials (available by January 1997) comparing day hospital care with comprehensive care (five trials), domiciliary care (four trials), or no comprehensive care (three trials)."
        self.assertEqual(self.abstract.data["text"], expected)


class AbstractTextWithoutSectionsTest(TestCase):
    """Test the text property when abstract has no sections"""

    def setUp(self):
        xml = """
        <abstract xml:lang="en">
            <title>Abstract</title>
            <p>To examine the effectiveness of day hospital attendance in prolonging independent living for elderly people.</p>
            <p>Systematic review of 12 controlled clinical trials (available by January 1997) comparing day hospital care with comprehensive care (five trials), domiciliary care (four trials), or no comprehensive care (three trials).</p>
        </abstract>
        """
        self.node = etree.fromstring(xml)
        self.abstract = Abstract(
            self.node, lang="en", 
            tags_to_keep=None, tags_to_keep_with_content=None,
            tags_to_remove_with_content=None, tags_to_convert_to_html=None
        )

    def test_text_property_without_sections(self):
        """Test that text property includes only p elements when no sections"""
        expected = "To examine the effectiveness of day hospital attendance in prolonging independent living for elderly people. Systematic review of 12 controlled clinical trials (available by January 1997) comparing day hospital care with comprehensive care (five trials), domiciliary care (four trials), or no comprehensive care (three trials)."
        self.assertEqual(self.abstract.text, expected)

    def test_data_text_value_without_sections(self):
        """Test that data['text'] has correct value for abstract without sections"""
        expected = "To examine the effectiveness of day hospital attendance in prolonging independent living for elderly people. Systematic review of 12 controlled clinical trials (available by January 1997) comparing day hospital care with comprehensive care (five trials), domiciliary care (four trials), or no comprehensive care (three trials)."
        self.assertEqual(self.abstract.data["text"], expected)


class AbstractTextWithInlineTagsTest(TestCase):
    """Test the text property handles inline formatting tags correctly"""

    def setUp(self):
        xml = """
        <abstract xml:lang="en">
            <sec>
                <title>Objective</title>
                <p>To examine the <italic>effectiveness</italic> of day hospital attendance.</p>
            </sec>
            <sec>
                <title>Design</title>
                <p>Systematic review of <bold>12 controlled</bold> clinical trials.</p>
            </sec>
        </abstract>
        """
        self.node = etree.fromstring(xml)
        self.abstract = Abstract(
            self.node, lang="en", 
            tags_to_keep=None, tags_to_keep_with_content=None,
            tags_to_remove_with_content=None, tags_to_convert_to_html=None
        )

    def test_text_property_strips_inline_formatting(self):
        """Test that inline formatting tags are removed but text is preserved"""
        expected = "Objective To examine the effectiveness of day hospital attendance. Design Systematic review of 12 controlled clinical trials."
        self.assertEqual(self.abstract.text, expected)


class AbstractTextEmptyTest(TestCase):
    """Test the text property with edge cases"""

    def test_empty_abstract_with_sections(self):
        """Test abstract with sections but no content"""
        xml = """
        <abstract xml:lang="en">
            <sec>
                <title></title>
                <p></p>
            </sec>
        </abstract>
        """
        node = etree.fromstring(xml)
        abstract = Abstract(
            node, lang="en", 
            tags_to_keep=None, tags_to_keep_with_content=None,
            tags_to_remove_with_content=None, tags_to_convert_to_html=None
        )
        self.assertEqual(abstract.text, "")

    def test_empty_abstract_without_sections(self):
        """Test abstract without sections and no content"""
        xml = """
        <abstract xml:lang="en">
            <p></p>
        </abstract>
        """
        node = etree.fromstring(xml)
        abstract = Abstract(
            node, lang="en", 
            tags_to_keep=None, tags_to_keep_with_content=None,
            tags_to_remove_with_content=None, tags_to_convert_to_html=None
        )
        self.assertEqual(abstract.text, "")

    def test_abstract_with_only_title_no_sections(self):
        """Test abstract with only title, no sections or paragraphs"""
        xml = """
        <abstract xml:lang="en">
            <title>Abstract</title>
        </abstract>
        """
        node = etree.fromstring(xml)
        abstract = Abstract(
            node, lang="en", 
            tags_to_keep=None, tags_to_keep_with_content=None,
            tags_to_remove_with_content=None, tags_to_convert_to_html=None
        )
        self.assertEqual(abstract.text, "")


class AbstractTextMultipleParagraphsTest(TestCase):
    """Test the text property with multiple paragraphs in sections"""

    def test_single_paragraph_per_section(self):
        """Test with one paragraph per section (standard case)"""
        xml = """
        <abstract xml:lang="en">
            <sec>
                <title>First</title>
                <p>First paragraph.</p>
            </sec>
            <sec>
                <title>Second</title>
                <p>Second paragraph.</p>
            </sec>
        </abstract>
        """
        node = etree.fromstring(xml)
        abstract = Abstract(
            node, lang="en", 
            tags_to_keep=None, tags_to_keep_with_content=None,
            tags_to_remove_with_content=None, tags_to_convert_to_html=None
        )
        expected = "First First paragraph. Second Second paragraph."
        self.assertEqual(abstract.text, expected)

    def test_section_without_title(self):
        """Test section without title but with paragraph"""
        xml = """
        <abstract xml:lang="en">
            <sec>
                <p>Only paragraph.</p>
            </sec>
        </abstract>
        """
        node = etree.fromstring(xml)
        abstract = Abstract(
            node, lang="en", 
            tags_to_keep=None, tags_to_keep_with_content=None,
            tags_to_remove_with_content=None, tags_to_convert_to_html=None
        )
        expected = "Only paragraph."
        self.assertEqual(abstract.text, expected)

    def test_section_without_paragraph(self):
        """Test section with title but no paragraph"""
        xml = """
        <abstract xml:lang="en">
            <sec>
                <title>Only Title</title>
            </sec>
        </abstract>
        """
        node = etree.fromstring(xml)
        abstract = Abstract(
            node, lang="en", 
            tags_to_keep=None, tags_to_keep_with_content=None,
            tags_to_remove_with_content=None, tags_to_convert_to_html=None
        )
        expected = "Only Title"
        self.assertEqual(abstract.text, expected)


class AbstractTextLanguageTest(TestCase):
    """Test the text property with different languages"""

    def test_portuguese_abstract_with_sections(self):
        """Test Portuguese abstract with sections"""
        xml = """
        <abstract xml:lang="pt">
            <sec>
                <title>Objetivo</title>
                <p>Avaliar o efeito de intervenção educativa domiciliar.</p>
            </sec>
            <sec>
                <title>Método</title>
                <p>Ensaio Clínico Randomizado.</p>
            </sec>
        </abstract>
        """
        node = etree.fromstring(xml)
        abstract = Abstract(
            node, lang="pt", 
            tags_to_keep=None, tags_to_keep_with_content=None,
            tags_to_remove_with_content=None, tags_to_convert_to_html=None
        )
        expected = "Objetivo Avaliar o efeito de intervenção educativa domiciliar. Método Ensaio Clínico Randomizado."
        self.assertEqual(abstract.text, expected)

    def test_spanish_abstract_without_sections(self):
        """Test Spanish abstract without sections"""
        xml = """
        <abstract xml:lang="es">
            <p>Evaluar el efecto de intervenciones de atención domiciliaria.</p>
            <p>Ensayo Clínico Aleatorizado.</p>
        </abstract>
        """
        node = etree.fromstring(xml)
        abstract = Abstract(
            node, lang="es", 
            tags_to_keep=None, tags_to_keep_with_content=None,
            tags_to_remove_with_content=None, tags_to_convert_to_html=None
        )
        expected = "Evaluar el efecto de intervenciones de atención domiciliaria. Ensayo Clínico Aleatorizado."
        self.assertEqual(abstract.text, expected)
