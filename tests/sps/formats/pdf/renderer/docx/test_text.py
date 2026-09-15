import unittest
from pathlib import Path

from lxml import etree

from packtools.sps.formats.pdf.renderer import docx as docx_renderer
from packtools.sps.formats.pdf.renderer.docx.text import add_paragraph_with_segments

_OMML_NS = 'http://schemas.openxmlformats.org/officeDocument/2006/math'
_FIXTURES_DIR = Path(__file__).resolve().parents[5] / "fixtures" / "pdf"


def _docx_with_layout_styles():
    """A fresh Document carrying the named styles from the real layout.docx template."""
    return docx_renderer.builder.init_docx({"base_layout": str(_FIXTURES_DIR / "layout.docx")})


def _omml_element():
    return etree.fromstring(
        f'<m:oMath xmlns:m="{_OMML_NS}">'
        '<m:r><m:t>x</m:t></m:r>'
        '</m:oMath>'
    )


class TestAddParagraphWithSegmentsFormula(unittest.TestCase):
    """
    Regression for issue #1352 (Phase 1 of #1347's plan): a 'formula'
    segment carries a ready-made OMML element instead of text/style flags,
    and must be appended into the paragraph's raw XML rather than as a
    text run - python-docx's high-level API has no concept of a formula.
    """

    def test_formula_segment_is_appended_as_raw_xml_not_a_run(self):
        docx = _docx_with_layout_styles()
        omml = _omml_element()
        segments = [{'type': 'formula', 'omml': omml}]

        para = add_paragraph_with_segments(docx, segments)

        self.assertEqual(len(para.runs), 0)
        self.assertIn(omml, list(para._p))

    def test_text_segments_before_and_after_formula_still_render_as_runs(self):
        docx = _docx_with_layout_styles()
        omml = _omml_element()
        segments = [
            {'type': 'text', 'text': 'Total biomass:', 'italic': False, 'bold': False,
             'superscript': False, 'subscript': False},
            {'type': 'formula', 'omml': omml},
            {'type': 'text', 'text': ' (3)', 'italic': False, 'bold': False,
             'superscript': False, 'subscript': False},
        ]

        para = add_paragraph_with_segments(docx, segments)

        self.assertEqual([r.text for r in para.runs], ['Total biomass:', ' (3)'])
        self.assertIn(omml, list(para._p))
