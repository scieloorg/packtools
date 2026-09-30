import ast
import unittest
from pathlib import Path

import packtools.sps.formats.pdf as pdf_package
from packtools.sps.formats.pdf.renderer.docx import style

PDF_DIR = Path(pdf_package.__file__).parent
STYLE_MODULE = PDF_DIR / 'renderer' / 'docx' / 'style.py'


def _docstring_nodes(tree):
    nodes = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            if node.body and isinstance(node.body[0], ast.Expr) and isinstance(node.body[0].value, ast.Constant):
                nodes.add(id(node.body[0].value))
    return nodes


class TestStyleNames(unittest.TestCase):

    def test_scl_style_names_only_in_style_module(self):
        for path in sorted(PDF_DIR.rglob('*.py')):
            if path == STYLE_MODULE:
                continue
            tree = ast.parse(path.read_text())
            docstrings = _docstring_nodes(tree)
            for node in ast.walk(tree):
                if (
                    isinstance(node, ast.Constant)
                    and isinstance(node.value, str)
                    and node.value.startswith('SCL ')
                    and id(node) not in docstrings
                ):
                    with self.subTest(file=str(path.relative_to(PDF_DIR)), line=node.lineno):
                        self.fail(f"use renderer.docx.style em vez de {node.value!r}")

    def test_level_to_style(self):
        self.assertEqual(style.level_to_style(2), style.SCL_SECTION_TITLE)
        self.assertEqual(style.level_to_style(3), style.SCL_SUBSECTION_TITLE)
        self.assertEqual(style.level_to_style(4), style.SCL_PARAGRAPH)


if __name__ == '__main__':
    unittest.main()
