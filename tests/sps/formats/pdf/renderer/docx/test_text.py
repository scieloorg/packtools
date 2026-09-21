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
        '<m:r><m:rPr/><m:t>x</m:t></m:r>'
        '</m:oMath>'
    )


class TestAddParagraphWithSegmentsFormula(unittest.TestCase):
    """Segmento 'formula' carrega um OMML pronto e é inserido como XML bruto no parágrafo, não como run."""

    def test_formula_segment_is_appended_as_raw_xml_not_a_run(self):
        docx = _docx_with_layout_styles()
        omml = _omml_element()
        segments = [{'type': 'formula', 'omml': omml}]

        para = add_paragraph_with_segments(docx, segments)

        self.assertEqual(len(para.runs), 0)
        self.assertIn(omml, list(para._p))

    def test_formula_segment_gets_paragraph_font_size_and_family(self):
        docx = _docx_with_layout_styles()
        omml = _omml_element()
        segments = [{'type': 'formula', 'omml': omml}]

        add_paragraph_with_segments(docx, segments, style_name='SCL Paragraph')

        w_ns = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
        run = omml.find(f'{{{_OMML_NS}}}r')
        w_rpr = run.find(f'{{{w_ns}}}rPr')
        self.assertIsNotNone(w_rpr)
        sz = w_rpr.find(f'{{{w_ns}}}sz')
        self.assertIsNotNone(sz)
        rfonts = w_rpr.find(f'{{{w_ns}}}rFonts')
        self.assertEqual(rfonts.get(f'{{{w_ns}}}ascii'), 'Noto Serif')

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


def _text_segment(text):
    return {'type': 'text', 'text': text, 'italic': False, 'bold': False,
            'superscript': False, 'subscript': False}


def _formula_segment(display=False):
    segment = {'type': 'formula', 'omml': _omml_element()}
    if display:
        segment['display'] = True
    return segment


class TestAddParagraphWithSegmentsFormulaStyle(unittest.TestCase):
    """
    Fórmula em bloco fica em parágrafo próprio, no estilo "SCL Formula" (à
    esquerda, sem recuo de primeira linha), separada do texto que a antecede;
    fórmula inline continua no parágrafo do texto. Ver issue #1385.
    """

    def test_display_formula_alone_uses_formula_style(self):
        docx = _docx_with_layout_styles()
        n_before = len(docx.paragraphs)

        para = add_paragraph_with_segments(docx, [_formula_segment(display=True)])

        self.assertEqual(len(docx.paragraphs) - n_before, 1)
        self.assertEqual(para.style.name, 'SCL Formula')

    def test_text_before_display_formula_goes_to_its_own_paragraph(self):
        docx = _docx_with_layout_styles()
        n_before = len(docx.paragraphs)
        segments = [_text_segment('Total plant biomass:'), _formula_segment(display=True), _text_segment(' (3)')]

        para = add_paragraph_with_segments(docx, segments)

        added = docx.paragraphs[n_before:]
        self.assertEqual(len(added), 2)
        self.assertEqual(added[0].style.name, 'SCL Paragraph')
        self.assertEqual(added[0].text, 'Total plant biomass:')
        self.assertEqual(added[1].style.name, 'SCL Formula')
        self.assertEqual(added[1].text, ' (3)')
        self.assertIs(para._p, added[1]._p)

    def test_blank_text_before_display_formula_does_not_create_empty_paragraph(self):
        docx = _docx_with_layout_styles()
        n_before = len(docx.paragraphs)

        add_paragraph_with_segments(docx, [_text_segment('  '), _formula_segment(display=True)])

        self.assertEqual(len(docx.paragraphs) - n_before, 1)

    def test_inline_formula_before_display_formula_is_kept(self):
        docx = _docx_with_layout_styles()
        n_before = len(docx.paragraphs)
        inline = _formula_segment()

        add_paragraph_with_segments(docx, [inline, _formula_segment(display=True)])

        added = docx.paragraphs[n_before:]
        self.assertEqual(len(added), 2)
        self.assertIn(inline['omml'], list(added[0]._p))

    def test_inline_formula_keeps_text_paragraph_and_default_style(self):
        docx = _docx_with_layout_styles()
        n_before = len(docx.paragraphs)
        segments = [_text_segment('Where '), _formula_segment(), _text_segment(' is the mean value.')]

        para = add_paragraph_with_segments(docx, segments)

        self.assertEqual(len(docx.paragraphs) - n_before, 1)
        self.assertEqual(para.style.name, 'SCL Paragraph')

    def test_paragraph_without_formula_keeps_default_style(self):
        docx = _docx_with_layout_styles()

        para = add_paragraph_with_segments(docx, [_text_segment('Plain paragraph.')])

        self.assertEqual(para.style.name, 'SCL Paragraph')

    def test_explicit_non_default_style_is_not_overridden(self):
        docx = _docx_with_layout_styles()
        n_before = len(docx.paragraphs)

        para = add_paragraph_with_segments(
            docx, [_text_segment('x'), _formula_segment(display=True)], style_name='SCL Paragraph Reference'
        )

        self.assertEqual(len(docx.paragraphs) - n_before, 1)
        self.assertEqual(para.style.name, 'SCL Paragraph Reference')

    def test_falls_back_to_requested_style_when_formula_style_missing_from_template(self):
        """Older templates without "SCL Formula" keep the previous (single, justified) paragraph."""
        from docx import Document
        from docx.enum.style import WD_STYLE_TYPE

        docx = Document()
        docx.styles.add_style('SCL Paragraph', WD_STYLE_TYPE.PARAGRAPH)

        para = add_paragraph_with_segments(docx, [_text_segment('x'), _formula_segment(display=True)])

        self.assertNotIn('SCL Formula', docx.styles)
        self.assertEqual(len(docx.paragraphs), 1)
        self.assertEqual(para.style.name, 'SCL Paragraph')
