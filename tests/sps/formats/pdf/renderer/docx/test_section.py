import unittest

from docx import Document
from docx.enum.section import WD_SECTION

from packtools.sps.formats.pdf.renderer.docx.section import (
    get_or_create_second_section,
    get_default_header,
    docx_setup_sections,
)
from packtools.sps.formats.pdf import enum as pdf_enum


class TestGetOrCreateSecondSection(unittest.TestCase):
    """
    Regression test: the body section must use a continuous break, not a
    forced new-page break, so front matter and body can share page 1 when
    there is room for both.
    """

    def test_second_section_uses_continuous_break(self):
        docx = Document()
        section = get_or_create_second_section(docx)
        self.assertEqual(section.start_type, WD_SECTION.CONTINUOUS)

    def test_reuses_existing_second_section_without_adding_more(self):
        docx = Document()
        get_or_create_second_section(docx)
        get_or_create_second_section(docx)
        self.assertEqual(len(docx.sections), 2)

    def test_start_type_is_configurable(self):
        docx = Document()
        attrs = dict(pdf_enum.PAGE_ATTRIBUTES)
        attrs['start_type'] = WD_SECTION.NEW_PAGE
        section = get_or_create_second_section(docx, page_attributes=attrs)
        self.assertEqual(section.start_type, WD_SECTION.NEW_PAGE)


class TestDefaultHeaderInheritance(unittest.TestCase):
    """
    Regression test: the running header must live on the first section's
    default header (inherited by later linked sections), not on a
    separately unlinked header on the body section - LibreOffice does not
    render a header defined on a section that is both continuous and
    unlinked from the previous section.
    """

    def test_get_default_header_targets_first_section(self):
        docx = Document()
        header = get_default_header(docx)
        header.paragraphs[0].text = "RUNNING HEADER"
        self.assertEqual(docx.sections[0].header.paragraphs[0].text, "RUNNING HEADER")

    def test_second_section_header_stays_linked_after_setup(self):
        docx = Document()
        get_or_create_second_section(docx)
        docx_setup_sections(docx, page_attributes=pdf_enum.PAGE_ATTRIBUTES)
        self.assertTrue(docx.sections[1].header.is_linked_to_previous)


if __name__ == "__main__":
    unittest.main()
