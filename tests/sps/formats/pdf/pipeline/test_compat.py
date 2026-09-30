import importlib
import unittest
import warnings

from lxml import etree

from packtools.sps.formats.pdf import enum as pdf_enum
from packtools.sps.formats.pdf.pipeline import formula as formula_pipe
from packtools.sps.formats.pdf.pipeline import supplementary_material as supplementary_material_pipe
from packtools.sps.formats.pdf.pipeline import xml as xml_pipe


class _CompatModuleTests:
    """Um módulo de compatibilidade reexporta os nomes movidos, com DeprecationWarning."""

    module = None
    # nomes públicos do módulo no master, antes da reorganização
    public_names = ()

    def test_public_names_before_reorganization_are_still_available(self):
        for name in self.public_names:
            with self.subTest(name=name):
                with warnings.catch_warnings():
                    warnings.simplefilter('ignore', DeprecationWarning)
                    self.assertTrue(hasattr(self.module, name))

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
    public_names = (
        'extract_article_main_language', 'extract_article_type', 'extract_journal_title',
        'extract_doi', 'extract_category', 'extract_article_title', 'extract_contrib_data',
        'extract_abstract_data', 'extract_trans_abstract_data', 'extract_keywords_data',
        'extract_footer_data', 'extract_cite_as_part_one', 'CITATION_STYLE_VANCOUVER',
        'build_full_citation', 'extract_body_data', 'extract_section_data',
        'extract_figure_data', 'extract_acknowledgment_data', 'extract_references_data',
        'extract_table_data', 'determine_table_layout',
    )

    def test_get_table_column_info_was_removed(self):
        with self.assertRaises(AttributeError):
            xml_pipe.get_table_column_info

    def test_determine_table_layout_still_takes_table_wrap(self):
        cells = ''.join(f'<td>{i}</td>' for i in range(5))
        table_wrap = etree.fromstring(f'<table-wrap><table><tbody><tr>{cells}</tr></tbody></table></table-wrap>')
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter('always')
            layout = xml_pipe.determine_table_layout(table_wrap)
        self.assertEqual(layout, pdf_enum.SINGLE_COLUMN_PAGE_LABEL)
        self.assertEqual([w.category for w in caught], [DeprecationWarning])


class TestPipelineFormulaCompat(_CompatModuleTests, unittest.TestCase):
    module = formula_pipe
    public_names = ('normalize_empty_base_superscripts', 'match_paragraph_font', 'mathml_to_omml')


class TestPipelineSupplementaryMaterialCompat(_CompatModuleTests, unittest.TestCase):
    module = supplementary_material_pipe
    public_names = ('extract_data', 'extract_supplementary_items', 'format_item')


if __name__ == '__main__':
    unittest.main()
