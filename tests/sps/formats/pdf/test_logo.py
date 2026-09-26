import tempfile
import unittest
import zipfile
from pathlib import Path

from PIL import Image

from packtools.sps.formats.pdf import enum as pdf_enum
from packtools.sps.formats.pdf.layout import logo as logo_layout
from packtools.sps.formats.pdf.pipeline import docx as docx_pipe
from packtools.sps.formats.pdf.renderer import docx as docx_renderer
from packtools.sps.utils import xml_utils

FIXTURES_DIR = Path(__file__).resolve().parents[3] / "fixtures" / "pdf"
EMU_PER_MM = 36000


def _docx_with_layout_styles():
    return docx_renderer.builder.init_docx({"base_layout": str(FIXTURES_DIR / "layout.docx")})


def _content_width():
    attrs = pdf_enum.PAGE_ATTRIBUTES
    return int(attrs['page_width'] - attrs['left_margin'] - attrs['right_margin'])


class _WithImages(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls._tmp = tempfile.TemporaryDirectory()
        tmp = Path(cls._tmp.name)
        cls.png_wide = str(tmp / "wide.png")
        Image.new("RGBA", (500, 200), (14, 100, 112, 255)).save(cls.png_wide)
        cls.png_tall = str(tmp / "tall.png")
        Image.new("RGB", (300, 400), (14, 100, 112)).save(cls.png_tall)
        cls.png_banner = str(tmp / "banner.png")
        Image.new("RGB", (2100, 300), (14, 100, 112)).save(cls.png_banner)
        cls.png_low_res = str(tmp / "low.png")
        Image.new("RGB", (150, 60), (14, 100, 112)).save(cls.png_low_res)
        cls.jpg = str(tmp / "logo.jpg")
        Image.new("RGB", (500, 200), (14, 100, 112)).save(cls.jpg)
        rect = '<rect width="300" height="100" fill="#0e6470"/></svg>'
        svg_open = '<svg xmlns="http://www.w3.org/2000/svg"'
        cls.svg_viewbox = cls._write(tmp / "viewbox.svg", f'{svg_open} viewBox="0 0 300 100">{rect}')
        cls.svg_mm = cls._write(tmp / "mm.svg", f'{svg_open} width="40mm" height="10mm" viewBox="0 0 300 100">{rect}')
        cls.svg_percent = cls._write(tmp / "percent.svg", f'{svg_open} width="100%" height="100%" viewBox="0,0,200,100">{rect}')
        cls.svg_no_size = cls._write(tmp / "nosize.svg", f'{svg_open}>{rect}')
        cls.not_svg = cls._write(tmp / "page.svg", '<html><body><svg/></body></html>')
        cls.svg_entity = cls._write(
            tmp / "entity.svg",
            '<?xml version="1.0"?><!DOCTYPE svg [<!ENTITY x SYSTEM "file:///etc/passwd">]>'
            f'{svg_open} viewBox="0 0 300 100"><text>&x;</text>{rect}',
        )

    @staticmethod
    def _write(path, text):
        path.write_text(text, encoding="utf-8")
        return str(path)

    @classmethod
    def tearDownClass(cls):
        cls._tmp.cleanup()


class TestNormalizeLogoSpec(unittest.TestCase):

    def test_none_or_empty_means_no_logo(self):
        self.assertIsNone(logo_layout.normalize_logo_spec(None))
        self.assertIsNone(logo_layout.normalize_logo_spec({}))
        self.assertIsNone(logo_layout.normalize_logo_spec({'path': ''}))

    def test_plain_path_uses_left_defaults(self):
        spec = logo_layout.normalize_logo_spec('/x/logo.png')
        self.assertEqual(spec.position, 'left')
        self.assertEqual((spec.max_width_mm, spec.max_height_mm), (40.0, 20.0))
        self.assertTrue(spec.show_title)

    def test_full_width_defaults_to_content_width(self):
        spec = logo_layout.normalize_logo_spec({'path': 'a.png', 'position': 'full_width'})
        self.assertIsNone(spec.max_width_mm)
        self.assertEqual(spec.max_height_mm, 15.0)

    def test_explicit_none_box_values_keep_defaults(self):
        spec = logo_layout.normalize_logo_spec(
            {'path': 'a.png', 'position': 'right', 'max_width_mm': None, 'max_height_mm': 12}
        )
        self.assertEqual((spec.max_width_mm, spec.max_height_mm), (40.0, 12.0))

    def test_invalid_position_raises(self):
        with self.assertRaises(ValueError):
            logo_layout.normalize_logo_spec({'path': 'a.png', 'position': 'top'})


class TestFitLogo(unittest.TestCase):

    def test_width_bound_keeps_aspect_ratio(self):
        w, h = logo_layout.fit_logo_emu(500, 100, 40 * EMU_PER_MM, 20 * EMU_PER_MM)
        self.assertEqual(w, 40 * EMU_PER_MM)
        self.assertEqual(h, 8 * EMU_PER_MM)

    def test_height_bound_keeps_aspect_ratio(self):
        w, h = logo_layout.fit_logo_emu(300, 400, 40 * EMU_PER_MM, 20 * EMU_PER_MM)
        self.assertEqual(h, 20 * EMU_PER_MM)
        self.assertEqual(w, 15 * EMU_PER_MM)

    def test_box_width_never_exceeds_content(self):
        spec = logo_layout.normalize_logo_spec({'path': 'a.png', 'max_width_mm': 500})
        max_w, _ = logo_layout.box_emu(spec, 170 * EMU_PER_MM)
        self.assertEqual(max_w, 170 * EMU_PER_MM)

    def test_invalid_size_raises(self):
        with self.assertRaises(ValueError):
            logo_layout.fit_logo_emu(0, 10, 1, 1)


class TestEffectiveDpi(unittest.TestCase):

    def test_dpi_from_printed_width(self):
        self.assertAlmostEqual(logo_layout.effective_dpi(300, int(25.4 * EMU_PER_MM)), 300)


class TestReadPngSize(_WithImages):

    def test_png_size(self):
        self.assertEqual(docx_renderer.logo.read_png_size(self.png_wide), (500, 200))

    def test_rejects_jpeg(self):
        with self.assertRaises(ValueError):
            docx_renderer.logo.read_png_size(self.jpg)

    def test_rejects_missing_file(self):
        with self.assertRaises(ValueError):
            docx_renderer.logo.read_png_size('/nao/existe.png')


class TestReadLogoSize(_WithImages):

    def test_png(self):
        self.assertEqual(docx_renderer.logo.read_logo_size(self.png_wide), ('png', 500, 200))

    def test_svg_viewbox(self):
        self.assertEqual(docx_renderer.logo.read_logo_size(self.svg_viewbox), ('svg', 300.0, 100.0))

    def test_svg_absolute_units_win_over_viewbox(self):
        kind, w, h = docx_renderer.logo.read_logo_size(self.svg_mm)
        self.assertEqual(kind, 'svg')
        self.assertAlmostEqual(w / h, 4.0)

    def test_svg_percent_falls_back_to_viewbox(self):
        self.assertEqual(docx_renderer.logo.read_logo_size(self.svg_percent), ('svg', 200.0, 100.0))

    def test_svg_without_size_raises(self):
        with self.assertRaises(ValueError):
            docx_renderer.logo.read_logo_size(self.svg_no_size)

    def test_xml_that_is_not_svg_raises(self):
        with self.assertRaises(ValueError):
            docx_renderer.logo.read_logo_size(self.not_svg)

    def test_svg_external_entity_is_not_resolved(self):
        self.assertEqual(docx_renderer.logo.read_logo_size(self.svg_entity), ('svg', 300.0, 100.0))

    def test_jpeg_still_rejected(self):
        with self.assertRaises(ValueError):
            docx_renderer.logo.read_logo_size(self.jpg)


class TestDocxJournalLogoPipe(_WithImages):

    def _build(self, **spec):
        docx = _docx_with_layout_styles()
        spec = logo_layout.normalize_logo_spec(spec)
        ok = docx_pipe.docx_journal_logo_pipe(docx, spec, "Revista Hipotética de Testes", "10.1590/x")
        return docx, ok, docx_renderer.section.get_first_page_header(docx)

    def _pictures(self, container):
        return container._element.findall('.//{http://schemas.openxmlformats.org/drawingml/2006/picture}pic')

    def test_left_with_title_is_logo_title_doi(self):
        docx, ok, header = self._build(path=self.png_wide)
        self.assertTrue(ok)
        cells = header.tables[0].rows[0].cells
        self.assertEqual(len(cells), 3)
        self.assertEqual(len(self._pictures(cells[0])), 1)
        self.assertIn("Revista", cells[1].text)
        self.assertIn("10.1590/x", cells[2].text)

    def test_left_logo_size_follows_box(self):
        docx, ok, header = self._build(path=self.png_wide)
        pic = header.tables[0].rows[0].cells[0].paragraphs[0].runs[0]._r.find(
            './/{http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing}extent'
        )
        self.assertEqual(int(pic.get('cx')), 40 * EMU_PER_MM)
        self.assertEqual(int(pic.get('cy')), 16 * EMU_PER_MM)

    def test_logo_has_zero_wrap_distance(self):
        # sem dist*, o LibreOffice desloca a imagem 0,32 cm
        _, ok, header = self._build(path=self.png_wide)
        inline = header.tables[0].rows[0].cells[0].paragraphs[0].runs[0]._r.find(
            './/{http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing}inline'
        )
        for side in ('distT', 'distB', 'distL', 'distR'):
            self.assertEqual(inline.get(side), '0')

    def test_low_resolution_png_only_warns(self):
        # 150 px em 40 mm = 95 dpi
        with self.assertLogs(docx_pipe.logger, level='WARNING') as logs:
            _, ok, _ = self._build(path=self.png_low_res)
        self.assertTrue(ok)
        self.assertIn('95 dpi', logs.output[0])

    def test_enough_resolution_png_does_not_warn(self):
        # 500 px em 40 mm = 317 dpi
        with self.assertNoLogs(docx_pipe.logger, level='WARNING'):
            self._build(path=self.png_wide)

    def test_left_without_title_is_logo_doi(self):
        _, ok, header = self._build(path=self.png_wide, show_title=False)
        cells = header.tables[0].rows[0].cells
        self.assertEqual(len(cells), 2)
        self.assertNotIn("Revista", header.tables[0]._element.xpath('string(.)'))
        self.assertIn("10.1590/x", cells[1].text)

    def test_right_puts_title_and_doi_left_logo_right(self):
        _, ok, header = self._build(path=self.png_tall, position='right')
        cells = header.tables[0].rows[0].cells
        self.assertEqual(len(cells), 2)
        self.assertIn("Revista", cells[0].text)
        self.assertIn("10.1590/x", cells[0].text)
        self.assertEqual(len(self._pictures(cells[1])), 1)

    def test_full_width_banner_then_title_and_doi(self):
        _, ok, header = self._build(path=self.png_banner, position='full_width')
        self.assertEqual(len(self._pictures(header.paragraphs[0])), 1)
        cells = header.tables[0].rows[0].cells
        self.assertIn("Revista", cells[0].text)
        self.assertIn("10.1590/x", cells[1].text)

    def test_full_width_banner_fits_height_box(self):
        _, ok, header = self._build(path=self.png_banner, position='full_width')
        ext = header.paragraphs[0].runs[0]._r.find(
            './/{http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing}extent'
        )
        self.assertLessEqual(int(ext.get('cy')), 15 * EMU_PER_MM)
        self.assertLessEqual(int(ext.get('cx')), _content_width())

    def test_full_width_without_title_has_only_doi(self):
        _, ok, header = self._build(path=self.png_banner, position='full_width', show_title=False)
        self.assertEqual(len(header.tables), 0)
        self.assertIn("10.1590/x", header.paragraphs[-1].text)

    def _svg_blip(self, header):
        return header._element.find(
            './/{http://schemas.microsoft.com/office/drawing/2016/SVG/main}svgBlip'
        )

    def test_svg_logo_links_svg_part_from_header(self):
        _, ok, header = self._build(path=self.svg_viewbox)
        self.assertTrue(ok)
        svg_blip = self._svg_blip(header)
        self.assertIsNotNone(svg_blip)
        rid = svg_blip.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed')
        part = header.part.related_parts[rid]
        self.assertEqual(part.content_type, 'image/svg+xml')
        self.assertIn(b'viewBox="0 0 300 100"', part.blob)

    def test_svg_logo_size_follows_box(self):
        _, ok, header = self._build(path=self.svg_viewbox)
        ext = header.tables[0].rows[0].cells[0].paragraphs[0].runs[0]._r.find(
            './/{http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing}extent'
        )
        self.assertEqual(int(ext.get('cx')), 40 * EMU_PER_MM)
        self.assertEqual(int(ext.get('cy')), 40 * EMU_PER_MM // 3)

    def test_svg_logo_uses_given_png_fallback(self):
        _, ok, header = self._build(path=self.svg_viewbox, fallback_path=self.png_wide)
        blip = header._element.find('.//{http://schemas.openxmlformats.org/drawingml/2006/main}blip')
        rid = blip.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed')
        with open(self.png_wide, 'rb') as f:
            self.assertEqual(header.part.related_parts[rid].blob, f.read())

    def test_svg_logo_with_invalid_fallback_uses_transparent_png(self):
        with self.assertLogs('packtools.sps.formats.pdf.pipeline.docx', level='WARNING'):
            _, ok, header = self._build(path=self.svg_viewbox, fallback_path=self.jpg)
        self.assertTrue(ok)
        self.assertIsNotNone(self._svg_blip(header))

    def test_svg_logo_has_zero_wrap_distance(self):
        _, ok, header = self._build(path=self.svg_viewbox)
        inline = header._element.find(
            './/{http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing}inline'
        )
        for side in ('distT', 'distB', 'distL', 'distR'):
            self.assertEqual(inline.get(side), '0')

    def test_invalid_file_leaves_header_untouched(self):
        docx, ok, header = self._build(path=self.jpg)
        self.assertFalse(ok)
        self.assertEqual(len(header.tables), 0)
        self.assertEqual(len(self._pictures(header)), 0)


class TestPipelineDocxWithLogo(_WithImages):

    def _pipeline(self, journal_logo=None):
        xml_tree = xml_utils.get_xml_tree(str(FIXTURES_DIR / "a1.xml"))
        data = {"base_layout": str(FIXTURES_DIR / "layout.docx"), "assets_dir": str(FIXTURES_DIR)}
        if journal_logo is not None:
            data["journal_logo"] = journal_logo
        docx = docx_pipe.pipeline_docx(xml_tree, data)
        return docx_renderer.section.get_first_page_header(docx)

    def test_without_logo_keeps_two_column_text_header(self):
        header = self._pipeline()
        self.assertEqual(len(header.tables[0].rows[0].cells), 2)

    def test_with_logo_uses_three_column_header(self):
        header = self._pipeline({'path': self.png_wide})
        self.assertEqual(len(header.tables[0].rows[0].cells), 3)

    def test_svg_logo_is_saved_in_docx_package(self):
        xml_tree = xml_utils.get_xml_tree(str(FIXTURES_DIR / "a1.xml"))
        data = {"base_layout": str(FIXTURES_DIR / "layout.docx"), "assets_dir": str(FIXTURES_DIR),
                "journal_logo": {'path': self.svg_viewbox}}
        docx = docx_pipe.pipeline_docx(xml_tree, data)
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "out.docx"
            docx.save(str(out))
            with zipfile.ZipFile(out) as z:
                names = z.namelist()
                content_types = z.read('[Content_Types].xml').decode()
        self.assertTrue(any(n.startswith('word/media/') and n.endswith('.svg') for n in names))
        self.assertIn('image/svg+xml', content_types)

    def test_invalid_logo_falls_back_to_text_header(self):
        with self.assertLogs('packtools.sps.formats.pdf.pipeline.docx', level='WARNING'):
            header = self._pipeline({'path': self.jpg})
        self.assertEqual(len(header.tables[0].rows[0].cells), 2)


if __name__ == '__main__':
    unittest.main()
