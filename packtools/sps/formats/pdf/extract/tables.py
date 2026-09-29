"""Tabelas (<table-wrap>): leitura do XML e montagem da estrutura pronta para renderização.

A decisão de layout e as larguras de coluna ficam em layout/table_layout.py,
que recebe os dados já extraídos aqui (ARCHITECTURE.md).
"""

from packtools.sps.formats.pdf.layout import table_layout


def extract_table_data(table_wrap, override_layout=None):
    """
    Extracts table data from an XML table-wrap element, handling merged cells.

    A <table-wrap> can contain more than one <table> (e.g. side-by-side
    "Program A"/"Program B"/"Program C" panels sharing one caption - real
    corpus pattern, issue #1368). Only the first used to be read; now every
    <table> is extracted as its own dict, so callers get one renderable
    table per <table> element instead of silently losing every table past
    the first. The shared <label>/<title> caption is attached only to the
    first dict (repeating it before every panel would look wrong), and any
    <table-wrap-foot> notes only to the last (read as applying to the whole
    group, once, after the last panel) - the ones in between get empty
    label/title/foot.

    Args:
        table_wrap (ElementTree): The XML table-wrap element to extract data from.
        override_layout (str, optional): Forces 'layout' to this value instead of
            running `table_layout.determine_table_layout`'s heuristic. Must be one of
            pdf_enum.SINGLE_COLUMN_PAGE_LABEL/DOUBLE_COLUMN_PAGE_LABEL, otherwise ignored.

    Returns:
        list[dict]: One dict per <table> in the table-wrap (or a single
        empty-shell dict if the table-wrap has no <table> at all), each
        with the following keys:
            - 'label': The text content of the table label element, or an empty string if not found.
            - 'title': The text content of the table title element, or an empty string if not found.
            - 'headers': A list of lists, where each inner list represents the text content of the table header cells.
            - 'rows': A list of lists, where each inner list represents the text content of the table data cells.
            - 'layout': A string indicating the table layout ('single-column-layout' or 'double-column-layout').
            - 'column_widths': A list of calculated column widths based on content.
            - 'foot': A list of footnote/attribution strings from <table-wrap-foot>, if present.
    """
    data = read_table_wrap(table_wrap)
    layout = table_layout.determine_table_layout(data, override=override_layout)

    tables = data['tables']
    if not tables:
        return [{
            'label': data['label'],
            'title': data['title'],
            'headers': [],
            'rows': [],
            'layout': layout,
            'column_widths': [],
            'header_spans': [],
            'row_spans': [],
            'foot': data['foot'],
        }]

    results = []
    for i, table in enumerate(tables):
        headers = table['headers']
        rows = table['rows']
        column_widths = table_layout.calculate_column_widths(headers, rows)
        results.append({
            'label': data['label'] if i == 0 else '',
            'title': data['title'] if i == 0 else '',
            'headers': headers,
            'rows': rows,
            'layout': layout,
            'column_widths': column_widths,
            'header_spans': table['header_spans'],
            'row_spans': table['row_spans'],
            'foot': data['foot'] if i == len(tables) - 1 else [],
        })
    return results


def read_table_wrap(table_wrap):
    """
    Reads a <table-wrap> from the XML, without deciding its layout.

    This is the input of layout/table_layout.py: every <table> in the wrap
    is read, so the layout decision covers the whole wrap (issue #1368).

    Args:
        table_wrap (ElementTree): The XML table-wrap element to read.

    Returns:
        dict: With the following keys:
            - 'label': The text of the first <label>, or an empty string.
            - 'title': The text of the first <title>, or an empty string.
            - 'foot': The <table-wrap-foot> strings (see _extract_table_foot).
            - 'tables': One dict per <table>, with 'headers', 'header_spans',
              'rows', 'row_spans' (see _extract_single_table_rows) and
              'cell_texts' - the text of every <td>/<th> in the <table>,
              including the ones the header/body grids don't take (e.g. in
              <tfoot>), used to spot a pathologically long cell.
    """
    table_label = table_wrap.find('.//label')
    label_text = table_label.text if table_label is not None else ""

    table_title = table_wrap.find('.//title')
    title_text = table_title.text if table_title is not None else ""

    tables = []
    for table in table_wrap.findall('.//table'):
        headers, header_spans, rows, row_spans = _extract_single_table_rows(table)
        tables.append({
            'headers': headers,
            'header_spans': header_spans,
            'rows': rows,
            'row_spans': row_spans,
            'cell_texts': [''.join(cell.itertext()).strip() for cell in table.xpath('.//td | .//th')],
        })

    return {
        'label': label_text,
        'title': title_text,
        'foot': _extract_table_foot(table_wrap),
        'tables': tables,
    }


def _extract_single_table_rows(table):
    """Extracts headers/rows/spans for a single <table> element."""
    headers = []
    rows = []
    header_spans = []
    row_spans = []

    thead = table.find('.//thead')
    if thead is not None:
        header_rows = thead.findall('.//tr')
        headers = _extract_table_rows_with_merged_cells(header_rows, 'th')
        header_spans = _extract_table_spans(header_rows, 'th')

    tbody = table.find('.//tbody')
    if tbody is not None:
        body_rows = tbody.findall('.//tr')
        rows = _extract_table_rows_with_merged_cells(body_rows, 'td')
        row_spans = _extract_table_spans(body_rows, 'td')
    elif thead is None:
        # <tr> as direct children of <table>, no <thead>/<tbody> wrapper at
        # all - valid JATS/NLM table shape (issue #1368; real example: a
        # structured radiology-report-style table). Without this fallback
        # the whole table body was silently dropped. Accept both <td> and
        # <th> cells since a bare table sometimes still marks a cell with
        # <th> without a <thead> wrapper.
        body_rows = table.findall('.//tr')
        if body_rows:
            rows = _extract_table_rows_with_merged_cells(body_rows, ('td', 'th'))
            row_spans = _extract_table_spans(body_rows, ('td', 'th'))

    return headers, header_spans, rows, row_spans


def _find_cells(el, cell_tag):
    """Finds cell elements under el, in document order.

    cell_tag is normally a single tag ('td' or 'th'), preserving the exact
    prior behavior via findall(). It can also be a tuple of tags (used by
    the bare-<tr>-no-thead/tbody fallback, issue #1368, where a row's own
    cells might be marked <td> or <th> with no wrapper to tell them apart)
    - lxml's xpath union operator returns matches in document order, same
    guarantee findall gives for a single tag.
    """
    if isinstance(cell_tag, str):
        return el.findall(f'.//{cell_tag}')
    return el.xpath(' | '.join(f'.//{tag}' for tag in cell_tag))


def _extract_table_rows_with_merged_cells(row_elements, cell_tag):
    """
    Extracts table rows handling merged cells (colspan/rowspan).

    Args:
        row_elements (list): The <tr> elements to extract, in document order.
        cell_tag (str or tuple[str]): The cell tag(s) to look for ('td', 'th', or both).

    Returns:
        list: A list of lists representing the table rows with merged cells properly handled.
    """
    rows = []

    if not row_elements:
        return rows

    # Create a matrix to track occupied positions
    max_cols = _count_row_columns(row_elements, cell_tag)
    occupied = [[False] * max_cols for _ in range(len(row_elements))]

    for row_idx, tr in enumerate(row_elements):
        row_data = [''] * max_cols
        col_idx = 0

        for cell in _find_cells(tr, cell_tag):
            # Find next available column
            while col_idx < max_cols and occupied[row_idx][col_idx]:
                col_idx += 1
            
            if col_idx >= max_cols:
                break
                
            # Get cell content
            cell_text = ''.join(cell.itertext()).strip() if cell.text or len(list(cell)) > 0 else ''
            
            # Get colspan and rowspan
            colspan = int(cell.get('colspan', 1))
            rowspan = int(cell.get('rowspan', 1))
            
            # Fill the cell and mark occupied positions
            row_data[col_idx] = cell_text
            for r in range(row_idx, min(row_idx + rowspan, len(row_elements))):
                for c in range(col_idx, min(col_idx + colspan, max_cols)):
                    occupied[r][c] = True
            
            col_idx += colspan
        
        rows.append(row_data)
    
    return rows


def _extract_table_spans(row_elements, cell_tag):
    """
    Builds a grid describing cell spans (colspan/rowspan) for a set of rows.

    Each entry is either None (no cell starts here) or a dict with keys:
      - 'colspan': int
      - 'rowspan': int
      - 'text': str (cell text)

    The grid has dimensions [number_of_rows][max_columns] where max_columns
    takes into account merged cells.

    Args:
        row_elements (list): The <tr> elements to extract, in document order.
        cell_tag (str or tuple[str]): The cell tag(s) to look for ('td', 'th', or both).
    """
    spans = []
    if not row_elements:
        return spans

    max_cols = _count_row_columns(row_elements, cell_tag)
    # Track occupied positions due to spans
    occupied = [[False] * max_cols for _ in range(len(row_elements))]

    for row_idx, tr in enumerate(row_elements):
        row_spans = [None] * max_cols
        col_idx = 0

        for cell in _find_cells(tr, cell_tag):
            # Advance to next free column
            while col_idx < max_cols and occupied[row_idx][col_idx]:
                col_idx += 1
            if col_idx >= max_cols:
                break

            cell_text = ''.join(cell.itertext()).strip() if cell.text or len(list(cell)) > 0 else ''
            colspan = int(cell.get('colspan', 1))
            rowspan = int(cell.get('rowspan', 1))

            row_spans[col_idx] = {
                'colspan': colspan,
                'rowspan': rowspan,
                'text': cell_text,
            }

            for r in range(row_idx, min(row_idx + rowspan, len(row_elements))):
                for c in range(col_idx, min(col_idx + colspan, max_cols)):
                    occupied[r][c] = True

            col_idx += colspan

        spans.append(row_spans)

    return spans


def _count_row_columns(row_elements, cell_tag):
    """
    Calculates the maximum number of columns across a set of rows, considering merged cells.

    Args:
        row_elements (list): The <tr> elements to consider.
        cell_tag (str or tuple[str]): The cell tag(s) to look for ('td', 'th', or both).

    Returns:
        int: The maximum number of columns.
    """
    max_cols = 0

    for tr in row_elements:
        current_cols = 0
        for cell in _find_cells(tr, cell_tag):
            colspan = int(cell.get('colspan', 1))
            current_cols += colspan
        max_cols = max(max_cols, current_cols)

    return max_cols


def _extract_table_foot(table_wrap):
    """
    Extracts footnote/attribution text from a table's <table-wrap-foot>, if present.

    Args:
        table_wrap (ElementTree): The XML table-wrap element to extract from.

    Returns:
        list: One string per <p>, <fn> or <attrib> child found, in document order.
    """
    notes = []
    foot = table_wrap.find('.//table-wrap-foot')
    if foot is None:
        return notes

    for node in foot.xpath('./p | ./fn | ./attrib | ./fn-group/fn'):
        text = ' '.join(' '.join(node.itertext()).split()).strip()
        if text:
            notes.append(text)

    return notes
