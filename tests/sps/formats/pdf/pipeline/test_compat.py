import importlib
import unittest
import warnings

from packtools.sps.formats.pdf.pipeline import formula as formula_pipe
from packtools.sps.formats.pdf.pipeline import xml as xml_pipe


class _CompatModuleTests:
    """Um módulo de compatibilidade reexporta os nomes movidos, com DeprecationWarning."""

    module = None

    def test_moved_names_resolve_to_new_module(self):
        for name, module_name in self.module._MOVED.items():
            with self.subTest(name=name):
                with warnings.catch_warnings(record=True) as caught:
                    warnings.simplefilter('always')
                    obj = getattr(self.module, name)
                self.assertIs(obj, getattr(importlib.import_module(module_name), name))
                self.assertEqual([w.category for w in caught], [DeprecationWarning])
                self.assertIn(module_name, str(caught[0].message))

    def test_moved_names_are_not_defined_in_compat_module(self):
        for name in self.module._MOVED:
            with self.subTest(name=name):
                self.assertNotIn(name, vars(self.module))

    def test_unknown_name_raises_attribute_error(self):
        with self.assertRaises(AttributeError):
            self.module.does_not_exist


class TestPipelineXmlCompat(_CompatModuleTests, unittest.TestCase):
    module = xml_pipe


class TestPipelineFormulaCompat(_CompatModuleTests, unittest.TestCase):
    module = formula_pipe


if __name__ == '__main__':
    unittest.main()
