import importlib
import unittest
import warnings

from packtools.sps.formats.pdf.pipeline import xml as xml_pipe


class TestPipelineXmlCompat(unittest.TestCase):
    """pipeline/xml.py reexporta as funções movidas, com DeprecationWarning."""

    def test_moved_names_resolve_to_new_module(self):
        for name, module_name in xml_pipe._MOVED.items():
            with self.subTest(name=name):
                with warnings.catch_warnings(record=True) as caught:
                    warnings.simplefilter('always')
                    obj = getattr(xml_pipe, name)
                self.assertIs(obj, getattr(importlib.import_module(module_name), name))
                self.assertEqual([w.category for w in caught], [DeprecationWarning])
                self.assertIn(module_name, str(caught[0].message))

    def test_moved_names_are_not_defined_in_compat_module(self):
        for name in xml_pipe._MOVED:
            with self.subTest(name=name):
                self.assertNotIn(name, vars(xml_pipe))

    def test_unknown_name_raises_attribute_error(self):
        with self.assertRaises(AttributeError):
            xml_pipe.does_not_exist


if __name__ == '__main__':
    unittest.main()
