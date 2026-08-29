import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

from packtools.sps.formats.pdf.pipeline import docx as docx_pipe
from packtools.sps.formats.pdf.utils import file_utils
from packtools.sps.utils import xml_utils

FIXTURES_DIR = Path(__file__).resolve().parents[3] / "fixtures" / "pdf"


def _find_libreoffice_binary():
    return shutil.which("libreoffice") or shutil.which("soffice")


def _render_page_texts(xml_filename, tmp_dir, pages=(1, 2)):
    """
    Runs the real pipeline (XML -> docx -> PDF via LibreOffice) and returns
    the extracted text of each requested page, so assertions check what a
    reader actually sees in the rendered PDF, not just the docx object's
    XML structure.
    """
    xml_path = FIXTURES_DIR / xml_filename
    xml_tree = xml_utils.get_xml_tree(str(xml_path))
    data = {"base_layout": str(FIXTURES_DIR / "layout.docx"), "assets_dir": str(FIXTURES_DIR)}
    document = docx_pipe.pipeline_docx(xml_tree, data)

    docx_path = tmp_dir / "out.docx"
    pdf_path = tmp_dir / "out.pdf"
    document.save(docx_path)
    file_utils.convert_docx_to_pdf(str(docx_path), _find_libreoffice_binary())

    page_texts = []
    for page in pages:
        result = subprocess.run(
            ["pdftotext", "-f", str(page), "-l", str(page), "-layout", str(pdf_path), "-"],
            capture_output=True, text=True, check=True,
        )
        page_texts.append(result.stdout)
    return page_texts


@unittest.skipUnless(
    _find_libreoffice_binary() and shutil.which("pdftotext"),
    "requires a real LibreOffice binary and pdftotext to render and inspect the PDF",
)
class TestBodyStartsPageOneRenderedPageNumbers(unittest.TestCase):
    """
    Integration check for the #1295/#1296 fix: the article body must start
    flowing on page 1 (continuous section break, not a forced page break)
    AND page 2 must carry the correct editorial page number. A prior
    version of this fix made these trade off against each other under
    LibreOffice's DOCX->PDF conversion - fixing one silently broke the
    other, invisible to structural assertions on the docx object, since
    the .docx XML looked correct either way. Only inspecting the actual
    rendered PDF catches that.

    The no-fpage expectation below was revised by #1302: #1295/#1296 had
    landed on "page 2 shows 1" (the first physical sheet left unnumbered)
    as a side effect of fixing the layout issue, not a deliberate choice
    about numbering. #1302 supersedes that: sheets are numbered in their
    natural order starting at 1, so the first physical sheet must show 1.
    """

    def test_body_starts_page_one_with_editorial_numbering(self):
        with tempfile.TemporaryDirectory() as tmp:
            page1_text, page2_text = _render_page_texts("a1.xml", Path(tmp))

            # a1.xml has fpage=271: page 1 keeps 271, page 2 must be 272.
            self.assertIn("271 | VOL.", page1_text)
            self.assertIn("272 | VOL.", page2_text)
            # Body content (not just front matter) must already be on page 1.
            self.assertIn("biodiversity", page1_text.lower())

    def test_body_starts_page_one_without_fpage_numbers_sheets_naturally(self):
        with tempfile.TemporaryDirectory() as tmp:
            page1_text, page2_text = _render_page_texts("a4.xml", Path(tmp))

            # a4.xml has no fpage: sheets follow their natural order (#1302).
            self.assertIn("1 | VOL.", page1_text)
            self.assertIn("2 | VOL.", page2_text)
