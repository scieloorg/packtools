import unittest

from lxml import etree

from packtools.sps.formats.pdf import enum as pdf_enum
from packtools.sps.formats.pdf.extract import tables


class TestExtractTableData(unittest.TestCase):

    def test_extract_table_data_complete(self):
        xml_str = """
            <table-wrap>
                <label>Table 1</label>
                <title>Sample Data</title>
                <table>
                    <thead>
                        <tr><th>Name</th><th>Age</th></tr>
                    </thead>
                    <tbody>
                        <tr><td>John</td><td>25</td></tr>
                        <tr><td>Jane</td><td>30</td></tr>
                    </tbody>
                </table>
            </table-wrap>
        """
        table_wrap = etree.fromstring(xml_str)
        expected = {
            'label': 'Table 1',
            'title': 'Sample Data',
            'headers': [['Name', 'Age']],
            'rows': [['John', '25'], ['Jane', '30']],
            'layout': 'double-column-layout',
            'column_widths': [50, 50],
            'header_spans': [[{'colspan': 1, 'rowspan': 1, 'text': 'Name'},
                               {'colspan': 1, 'rowspan': 1, 'text': 'Age'}]],
            'row_spans': [[{'colspan': 1, 'rowspan': 1, 'text': 'John'},
                           {'colspan': 1, 'rowspan': 1, 'text': '25'}],
                          [{'colspan': 1, 'rowspan': 1, 'text': 'Jane'},
                           {'colspan': 1, 'rowspan': 1, 'text': '30'}]],
            'foot': [],
        }
        result = tables.extract_table_data(table_wrap)
        self.assertEqual([expected], result)

    def test_extract_table_data_no_label_no_title(self):
        xml_str = """
            <table-wrap>
                <table>
                    <thead>
                        <tr><th>Col1</th></tr>
                    </thead>
                    <tbody>
                        <tr><td>Data1</td></tr>
                    </tbody>
                </table>
            </table-wrap>
        """
        table_wrap = etree.fromstring(xml_str)
        expected = {
            'label': '',
            'title': '',
            'headers': [['Col1']],
            'rows': [['Data1']],
            'layout': 'double-column-layout',
            'column_widths': [50],
            'header_spans': [[{'colspan': 1, 'rowspan': 1, 'text': 'Col1'}]],
            'row_spans': [[{'colspan': 1, 'rowspan': 1, 'text': 'Data1'}]],
            'foot': [],
        }
        result = tables.extract_table_data(table_wrap)
        self.assertEqual([expected], result)

    def test_extract_table_data_empty_table(self):
        xml_str = """
            <table-wrap>
                <label>Table 2</label>
                <title>Empty Table</title>
                <table>
                    <thead></thead>
                    <tbody></tbody>
                </table>
            </table-wrap>
        """
        table_wrap = etree.fromstring(xml_str)
        expected = {
            'label': 'Table 2',
            'title': 'Empty Table',
            'headers': [],
            'rows': [],
            'layout': 'double-column-layout',
            'column_widths': [],
            'header_spans': [],
            'row_spans': [],
            'foot': [],
        }
        result = tables.extract_table_data(table_wrap)
        self.assertEqual([expected], result)

    def test_extract_table_data_no_table(self):
        xml_str = """
            <table-wrap>
                <label>Table 3</label>
                <title>Missing Table</title>
            </table-wrap>
        """
        table_wrap = etree.fromstring(xml_str)
        expected = {
            'label': 'Table 3',
            'title': 'Missing Table',
            'headers': [],
            'rows': [],
            'layout': 'double-column-layout',
            'column_widths': [],
            'header_spans': [],
            'row_spans': [],
            'foot': [],
        }
        result = tables.extract_table_data(table_wrap)
        self.assertEqual([expected], result)

    def test_extract_table_data_multiple_header_rows(self):
        xml_str = """
            <table-wrap>
                <table>
                    <thead>
                        <tr><th>Col1</th><th>Col2</th></tr>
                        <tr><th>SubCol1</th><th>SubCol2</th></tr>
                    </thead>
                    <tbody>
                        <tr><td>Val1</td><td>Val2</td></tr>
                    </tbody>
                </table>
            </table-wrap>
        """
        table_wrap = etree.fromstring(xml_str)
        expected = {
            'label': '',
            'title': '',
            'headers': [['Col1', 'Col2'], ['SubCol1', 'SubCol2']],
            'rows': [['Val1', 'Val2']],
            'layout': 'double-column-layout',
            'column_widths': [50, 50],
            'header_spans': [[{'colspan': 1, 'rowspan': 1, 'text': 'Col1'},
                               {'colspan': 1, 'rowspan': 1, 'text': 'Col2'}],
                              [{'colspan': 1, 'rowspan': 1, 'text': 'SubCol1'},
                               {'colspan': 1, 'rowspan': 1, 'text': 'SubCol2'}]],
            'row_spans': [[{'colspan': 1, 'rowspan': 1, 'text': 'Val1'},
                           {'colspan': 1, 'rowspan': 1, 'text': 'Val2'}]],
            'foot': [],
        }
        result = tables.extract_table_data(table_wrap)
        self.assertEqual([expected], result)

    def test_extract_table_data_foot_with_fn_and_attrib(self):
        xml_str = """
            <table-wrap>
                <table>
                    <tbody><tr><td>Data</td></tr></tbody>
                </table>
                <table-wrap-foot>
                    <fn id="TFN1"><p>Source: Authors.</p></fn>
                    <fn id="TFN2"><p>* p &lt; 0.05.</p></fn>
                    <attrib>Adapted from Smith (2020).</attrib>
                </table-wrap-foot>
            </table-wrap>
        """
        table_wrap = etree.fromstring(xml_str)
        result = tables.extract_table_data(table_wrap)
        self.assertEqual(
            result[0]['foot'],
            ['Source: Authors.', '* p < 0.05.', 'Adapted from Smith (2020).'],
        )

    def test_extract_table_data_foot_with_direct_p_elements(self):
        # Regression: table-wrap-foot can hold <p> children directly, not
        # only wrapped in <fn> or <attrib> (e.g. Table 2 of a2.xml fixture).
        xml_str = """
            <table-wrap>
                <table>
                    <tbody><tr><td>Data</td></tr></tbody>
                </table>
                <table-wrap-foot>
                    <p>Legenda: Outros (BR): 87 titulos.</p>
                    <p>Fonte: Dados da pesquisa (Florianopolis, 2022).</p>
                </table-wrap-foot>
            </table-wrap>
        """
        table_wrap = etree.fromstring(xml_str)
        result = tables.extract_table_data(table_wrap)
        self.assertEqual(
            result[0]['foot'],
            ['Legenda: Outros (BR): 87 titulos.', 'Fonte: Dados da pesquisa (Florianopolis, 2022).'],
        )

    def test_extract_table_data_foot_preserves_mixed_document_order(self):
        xml_str = """
            <table-wrap>
                <table>
                    <tbody><tr><td>Data</td></tr></tbody>
                </table>
                <table-wrap-foot>
                    <p>Legenda solta.</p>
                    <fn id="TFN1"><p>Nota de rodape.</p></fn>
                    <attrib>Fonte: Autores.</attrib>
                </table-wrap-foot>
            </table-wrap>
        """
        table_wrap = etree.fromstring(xml_str)
        result = tables.extract_table_data(table_wrap)
        self.assertEqual(
            result[0]['foot'],
            ['Legenda solta.', 'Nota de rodape.', 'Fonte: Autores.'],
        )

    def test_extract_table_data_no_foot_defaults_to_empty_list(self):
        xml_str = "<table-wrap><table><tbody><tr><td>Data</td></tr></tbody></table></table-wrap>"
        table_wrap = etree.fromstring(xml_str)
        result = tables.extract_table_data(table_wrap)
        self.assertEqual(result[0]['foot'], [])

    def test_extract_table_data_override_layout_wins_over_heuristic(self):
        xml_str = "<table-wrap><table><tbody><tr><td>Data</td></tr></tbody></table></table-wrap>"
        table_wrap = etree.fromstring(xml_str)
        result = tables.extract_table_data(
            table_wrap, override_layout=pdf_enum.SINGLE_COLUMN_PAGE_LABEL
        )
        self.assertEqual(result[0]['layout'], pdf_enum.SINGLE_COLUMN_PAGE_LABEL)

    def test_extract_table_data_invalid_override_falls_back_to_heuristic(self):
        xml_str = "<table-wrap><table><tbody><tr><td>Data</td></tr></tbody></table></table-wrap>"
        table_wrap = etree.fromstring(xml_str)
        result = tables.extract_table_data(table_wrap, override_layout='not-a-real-layout')
        self.assertEqual(result[0]['layout'], pdf_enum.DOUBLE_COLUMN_PAGE_LABEL)


class TestExtractTableDataMultipleTables(unittest.TestCase):
    """
    Regression tests for issue #1368: a <table-wrap> can hold more than one
    <table> (real corpus pattern - side-by-side "Program A"/"Program B"
    panels sharing one caption). table_wrap.find('.//table') used to grab
    only the first, silently dropping every table past it. extract_table_data
    now returns one dict per <table>, the shared label/title only on the
    first and any <table-wrap-foot> notes only on the last.
    """

    def _two_table_xml(self):
        return """
            <table-wrap>
                <label>Table 1</label>
                <title>Two programs</title>
                <table>
                    <thead><tr><th>Program A</th></tr></thead>
                    <tbody><tr><td>A1</td></tr></tbody>
                </table>
                <table>
                    <thead><tr><th>Program B</th></tr></thead>
                    <tbody><tr><td>B1</td></tr></tbody>
                </table>
                <table-wrap-foot>
                    <p>Shared note.</p>
                </table-wrap-foot>
            </table-wrap>
        """

    def test_returns_one_dict_per_table(self):
        table_wrap = etree.fromstring(self._two_table_xml())
        result = tables.extract_table_data(table_wrap)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['rows'], [['A1']])
        self.assertEqual(result[1]['rows'], [['B1']])

    def test_caption_only_on_first_table(self):
        table_wrap = etree.fromstring(self._two_table_xml())
        result = tables.extract_table_data(table_wrap)
        self.assertEqual(result[0]['label'], 'Table 1')
        self.assertEqual(result[0]['title'], 'Two programs')
        self.assertEqual(result[1]['label'], '')
        self.assertEqual(result[1]['title'], '')

    def test_foot_only_on_last_table(self):
        table_wrap = etree.fromstring(self._two_table_xml())
        result = tables.extract_table_data(table_wrap)
        self.assertEqual(result[0]['foot'], [])
        self.assertEqual(result[1]['foot'], ['Shared note.'])

    def test_layout_considers_every_table_not_just_the_first(self):
        # First table has 1 narrow column; second has 5, past the
        # single-column-layout threshold. The wrap-level layout decision
        # must reflect the widest table, not just the first.
        xml_str = """
            <table-wrap>
                <table><tbody><tr><td>A</td></tr></tbody></table>
                <table><tbody><tr>
                    <td>1</td><td>2</td><td>3</td><td>4</td><td>5</td>
                </tr></tbody></table>
            </table-wrap>
        """
        table_wrap = etree.fromstring(xml_str)
        result = tables.extract_table_data(table_wrap)
        self.assertEqual(result[0]['layout'], pdf_enum.SINGLE_COLUMN_PAGE_LABEL)
        self.assertEqual(result[1]['layout'], pdf_enum.SINGLE_COLUMN_PAGE_LABEL)


class TestExtractTableDataBareRows(unittest.TestCase):
    """
    Regression tests for issue #1368: a <table> can have <tr> as direct
    children with no <thead>/<tbody> wrapper at all (valid JATS/NLM shape -
    real corpus example: a structured radiology-report table). Both were
    previously required for any content to be read, so the whole table body
    was silently dropped.
    """

    def test_bare_tr_rows_are_read_as_body(self):
        xml_str = """
            <table-wrap>
                <table>
                    <tr><td>PULMOES:</td><td>Sem alteracoes.</td></tr>
                    <tr><td>BACO:</td><td>Sem alteracoes.</td></tr>
                </table>
            </table-wrap>
        """
        table_wrap = etree.fromstring(xml_str)
        result = tables.extract_table_data(table_wrap)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['headers'], [])
        self.assertEqual(
            result[0]['rows'],
            [['PULMOES:', 'Sem alteracoes.'], ['BACO:', 'Sem alteracoes.']],
        )

    def test_bare_tr_accepts_th_cells_without_a_thead_wrapper(self):
        xml_str = """
            <table-wrap>
                <table>
                    <tr><th>Predictor</th><th>Value</th></tr>
                    <tr><td>Age</td><td>37</td></tr>
                </table>
            </table-wrap>
        """
        table_wrap = etree.fromstring(xml_str)
        result = tables.extract_table_data(table_wrap)
        self.assertEqual(
            result[0]['rows'],
            [['Predictor', 'Value'], ['Age', '37']],
        )


class TestReadTableWrap(unittest.TestCase):

    def test_reads_every_table_and_shared_caption(self):
        table_wrap = etree.fromstring(
            '<table-wrap><label>Table 1</label><caption><title>Programs</title></caption>'
            '<table><thead><tr><th colspan="2">A</th></tr></thead>'
            '<tbody><tr><td>1</td><td>2</td></tr></tbody>'
            '<tfoot><tr><td>foot cell</td></tr></tfoot></table>'
            '<table><tbody><tr><td>3</td></tr></tbody></table>'
            '<table-wrap-foot><p>Source: authors.</p></table-wrap-foot>'
            '</table-wrap>'
        )
        data = tables.read_table_wrap(table_wrap)
        self.assertEqual(data['label'], 'Table 1')
        self.assertEqual(data['title'], 'Programs')
        self.assertEqual(data['foot'], ['Source: authors.'])
        self.assertEqual(len(data['tables']), 2)
        self.assertEqual(data['tables'][0]['headers'], [['A', '']])
        self.assertEqual(data['tables'][0]['rows'], [['1', '2']])
        self.assertEqual(data['tables'][0]['cell_texts'], ['A', '1', '2', 'foot cell'])
        self.assertEqual(data['tables'][1]['rows'], [['3']])

    def test_no_table(self):
        data = tables.read_table_wrap(etree.fromstring('<table-wrap><label>T1</label></table-wrap>'))
        self.assertEqual(data['tables'], [])

