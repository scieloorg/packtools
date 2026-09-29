"""Regras de dependência entre os pacotes do gerador de PDF (docs/pdf_generator_architecture.md)."""

import ast
import unittest
from pathlib import Path

import packtools.sps.formats.pdf as pdf_package

PDF_DIR = Path(pdf_package.__file__).parent
PDF = 'packtools.sps.formats.pdf'

FORBIDDEN = {
    'extract': ('docx', f'{PDF}.pipeline', f'{PDF}.renderer'),
    'layout': (f'{PDF}.extract', f'{PDF}.pipeline', f'{PDF}.renderer'),
    'ooxml': ('docx', f'{PDF}.extract', f'{PDF}.pipeline', f'{PDF}.renderer', f'{PDF}.layout'),
    'renderer': (f'{PDF}.pipeline', f'{PDF}.extract'),
}


def _module_name(path):
    return '.'.join((PDF,) + path.relative_to(PDF_DIR).with_suffix('').parts)


def _imported_modules(path):
    """Nomes absolutos dos módulos importados diretamente por `path`."""
    package = _module_name(path).rsplit('.', 1)[0]
    names = []
    for node in ast.walk(ast.parse(path.read_text())):
        if isinstance(node, ast.Import):
            names.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            if node.level:
                base = package.rsplit('.', node.level - 1)[0] if node.level > 1 else package
                module = f'{base}.{node.module}' if node.module else base
            else:
                module = node.module
            names.append(module)
            # `from pacote import modulo` também importa pacote.modulo
            names.extend(f'{module}.{alias.name}' for alias in node.names)
    return names


def _matches(name, prefix):
    return name == prefix or name.startswith(prefix + '.')


class TestModuleDependencies(unittest.TestCase):

    def test_packages_do_not_import_forbidden_modules(self):
        for package, forbidden in FORBIDDEN.items():
            for path in sorted((PDF_DIR / package).rglob('*.py')):
                for name in _imported_modules(path):
                    for prefix in forbidden:
                        with self.subTest(module=_module_name(path), imports=name):
                            self.assertFalse(
                                _matches(name, prefix),
                                f'{_module_name(path)} não pode importar {prefix}',
                            )

    def test_production_code_does_not_import_compat_modules(self):
        compat = (f'{PDF}.pipeline.xml', f'{PDF}.pipeline.formula')
        for path in sorted(PDF_DIR.rglob('*.py')):
            if _module_name(path) in compat:
                continue
            for name in _imported_modules(path):
                for prefix in compat:
                    with self.subTest(module=_module_name(path), imports=name):
                        self.assertFalse(_matches(name, prefix))

    def test_detects_forbidden_import(self):
        # garante que a verificação acima não passa por não enxergar nada
        names = _imported_modules(PDF_DIR / 'pipeline' / 'docx.py')
        self.assertIn(f'{PDF}.renderer', names)
        self.assertIn('docx.shared', names)
        self.assertIn(f'{PDF}.extract.body', names)


if __name__ == '__main__':
    unittest.main()
