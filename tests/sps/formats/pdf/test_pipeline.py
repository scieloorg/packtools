"""Pipeline completo sobre os fixtures: nenhum texto do XML pode faltar no DOCX."""

import re
import shutil
import tempfile
import unittest
import zipfile
from pathlib import Path

from lxml import etree

from packtools.sps.formats.pdf.pipeline import pipeline_docx
from packtools.sps.utils import xml_utils

FIXTURES_DIR = Path(__file__).resolve().parents[3] / 'fixtures' / 'pdf'
DATA = {'base_layout': str(FIXTURES_DIR / 'layout.docx'), 'assets_dir': str(FIXTURES_DIR)}
FIXTURES = ('a1.xml', 'a2.xml', 'a3.xml', 'a4.xml')

# texto que não vai para o DOCX como está: fórmula (vira OMML), representações
# alternativas e o rótulo da nota "como citar" (substituído por "CITE AS:")
_NOT_LITERAL = {'math', 'tex-math', 'alt-text'}
_CITE_AS_LABEL = re.compile(r'como citar|how to cite', re.IGNORECASE)


def _fragments(root):
    """Cada .text/.tail não vazio de body, back e sub-articles (exceto tradução)."""
    found = []

    def walk(node):
        name = etree.QName(node).localname if isinstance(node.tag, str) else None
        duplicate_citation = name == 'element-citation' and node.getparent().find('mixed-citation') is not None
        if name and name not in _NOT_LITERAL and not duplicate_citation:
            if node.text and node.text.strip():
                found.append(node.text)
            for child in node:
                walk(child)
        if node.tail and node.tail.strip():
            found.append(node.tail)

    for part in root.xpath('body|back|sub-article[@article-type!="translation"]'):
        for child in part:
            walk(child)
    return [f for f in found if not _CITE_AS_LABEL.search(f)]


def _docx_text(document):
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / 'out.docx'
        document.save(path)
        with zipfile.ZipFile(path) as package:
            texts = [t for name in package.namelist() if name.startswith('word/') and name.endswith('.xml')
                     for t in etree.fromstring(package.read(name)).xpath('//*[local-name()="t"]/text()')]
    return re.sub(r'\s+', '', ''.join(texts))


def _no_space(text):
    return re.sub(r'\s+', '', text)


class NoDataLossTest(unittest.TestCase):
    def test_every_text_fragment_reaches_the_docx(self):
        for name in FIXTURES:
            with self.subTest(name):
                root = xml_utils.get_xml_tree(str(FIXTURES_DIR / name))
                text = _docx_text(pipeline_docx(root, dict(DATA)))
                missing = [f.strip() for f in _fragments(root) if _no_space(f) not in text]
                self.assertEqual(missing, [])


class InternalLinksTest(unittest.TestCase):
    def test_every_internal_link_has_a_target(self):
        w = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
        for name in FIXTURES:
            with self.subTest(name):
                root = xml_utils.get_xml_tree(str(FIXTURES_DIR / name))
                with tempfile.TemporaryDirectory() as tmp:
                    path = Path(tmp) / 'out.docx'
                    pipeline_docx(root, dict(DATA)).save(path)
                    with zipfile.ZipFile(path) as package:
                        body = etree.fromstring(package.read('word/document.xml'))
                marks = {b.get(w + 'name') for b in body.iter(w + 'bookmarkStart')}
                links = [h.get(w + 'anchor') for h in body.iter(w + 'hyperlink') if h.get(w + 'anchor')]
                # um link por <xref> com @rid
                self.assertEqual(len(links), len(root.xpath('//xref[@rid]')))
                self.assertEqual([l for l in links if l not in marks], [])


class RenderTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.doc = pipeline_docx(xml_utils.get_xml_tree(str(FIXTURES_DIR / 'a1.xml')), dict(DATA))

    def test_layout_styles_are_used(self):
        used = {p.style.name for p in self.doc.paragraphs if p.style is not None}
        for style in ('SCL Article Title', 'SCL Author', 'SCL Affiliation', 'SCL Abstract Title',
                      'SCL Paragraph Abstract', 'SCL Paragraph Keywords', 'SCL Section Title',
                      'SCL Paragraph', 'SCL Paragraph Reference', 'SCL Table Heading', 'SCL Figure Caption'):
            self.assertIn(style, used)

    def test_headers_footers_and_page_numbering(self):
        first = self.doc.sections[0]
        self.assertIn('Acta', first.first_page_header.tables[0].cell(0, 0).text)
        self.assertIn('10.1590/1809-4392202202951', first.first_page_header.tables[0].cell(0, 1).text)
        self.assertTrue(first.first_page_footer.paragraphs[0].text.startswith('CITE AS: '))
        self.assertIn('VOL. 53 (4) 2023: 271-280', first.first_page_footer.paragraphs[1].text)
        for section in self.doc.sections:
            self.assertEqual(section._sectPr.xpath('./w:pgNumType/@w:start'), ['271'])

    def test_body_in_two_columns_and_annex_in_one(self):
        columns = [s._sectPr.xpath('./w:cols/@w:num') for s in self.doc.sections]
        self.assertEqual(columns[1], ['2'])
        self.assertEqual(columns[-1], ['1'])

    def test_without_base_layout_still_renders(self):
        root = xml_utils.get_xml_tree(str(FIXTURES_DIR / 'a2.xml'))
        document = pipeline_docx(root, {'assets_dir': str(FIXTURES_DIR)})
        self.assertGreater(len(document.paragraphs), 50)


def _libreoffice():
    return shutil.which('libreoffice') or shutil.which('soffice')


@unittest.skipUnless(_libreoffice() and shutil.which('pdftotext'), 'requer LibreOffice e pdftotext')
class RenderedPdfTest(unittest.TestCase):
    """O corpo começa na página 1 e a página 2 tem a numeração editorial (#1295, #1302)."""

    def _pages(self, name):
        import subprocess
        from packtools.sps.formats.pdf.convert import convert_docx_to_pdf

        with tempfile.TemporaryDirectory() as tmp:
            docx_path = Path(tmp) / 'out.docx'
            pipeline_docx(xml_utils.get_xml_tree(str(FIXTURES_DIR / name)), dict(DATA)).save(docx_path)
            pdf = convert_docx_to_pdf(str(docx_path), _libreoffice())
            return [subprocess.run(['pdftotext', '-f', str(p), '-l', str(p), '-layout', pdf, '-'],
                                   capture_output=True, text=True, check=True).stdout for p in (1, 2)]

    def test_editorial_numbering(self):
        page1, page2 = self._pages('a1.xml')
        self.assertIn('271 | VOL.', page1)
        self.assertIn('272 | VOL.', page2)
        self.assertIn('biodiversity', page1.lower())

    def test_natural_numbering_without_fpage(self):
        page1, page2 = self._pages('a4.xml')
        self.assertIn('1 | VOL.', page1)
        self.assertIn('2 | VOL.', page2)
