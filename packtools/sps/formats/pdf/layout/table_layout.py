"""Layout de tabela: 1 ou 2 colunas e larguras, a partir dos dados já extraídos.

Recebe a estrutura montada por extract/tables.py::read_table_wrap, nunca o XML.
"""

from packtools.sps.formats.pdf import enum as pdf_enum


_PATHOLOGICAL_CELL_LENGTH = 400


def determine_table_layout(table_wrap_data, override=None):
    """
    Determines the layout of a table based on the number of columns it contains,
    considering merged cells, with an escape hatch for an explicit override and a
    guard against a single excessively long cell (which the column-count heuristic
    alone can't catch: a table can have few columns and still need full width).

    Args:
        table_wrap_data (dict): The whole <table-wrap>, as returned by
            extract/tables.py::read_table_wrap - its 'tables' list holds one
            entry per <table>, each with 'headers', 'rows' and 'cell_texts'.
        override (str, optional): Forces this layout instead of running the heuristic.
            Must be one of pdf_enum.SINGLE_COLUMN_PAGE_LABEL/DOUBLE_COLUMN_PAGE_LABEL,
            otherwise ignored.

    Returns:
        str: A string indicating the table layout. Possible values are 'single-column-layout' and 'double-column-layout'.
    """
    if override in (pdf_enum.SINGLE_COLUMN_PAGE_LABEL, pdf_enum.DOUBLE_COLUMN_PAGE_LABEL):
        return override

    # A table-wrap can hold more than one <table> (issue #1368); the layout
    # decision is for the wrap as a whole, so it has to look at every
    # <table> in it, not just the first - otherwise a wrap whose first
    # panel happens to be narrow could still get double-column-layout even
    # though a later panel needs the full width.
    tables = table_wrap_data['tables']

    if _calculate_max_columns(tables) > 4:
        return pdf_enum.SINGLE_COLUMN_PAGE_LABEL

    if _max_cell_text_length(tables) > _PATHOLOGICAL_CELL_LENGTH:
        return pdf_enum.SINGLE_COLUMN_PAGE_LABEL

    return pdf_enum.DOUBLE_COLUMN_PAGE_LABEL


def _calculate_max_columns(tables):
    """
    Returns the widest column count among the tables' header and body grids.

    Each grid row already has one slot per column, colspan included (see
    extract/tables.py::_extract_table_rows_with_merged_cells), so a row's
    length is the column count of its group of rows.
    """
    return max(
        (len(row) for table in tables for row in table['headers'] + table['rows']),
        default=0,
    )


def _max_cell_text_length(tables):
    """Returns the character length of the longest single cell's text in the tables."""
    return max(
        (len(text) for table in tables for text in table['cell_texts']),
        default=0,
    )


def calculate_column_widths(headers, rows, min_width=50, max_width=200):
    """
    Calculates optimal column widths based on content length.
    
    Args:
        headers (list): List of header rows.
        rows (list): List of data rows.
        min_width (int): Minimum column width in points. Defaults to 50.
        max_width (int): Maximum column width in points. Defaults to 200.
    
    Returns:
        list: A list of calculated column widths.
    """
    if not headers and not rows:
        return []
    
    # Determine number of columns
    num_cols = 0
    if headers:
        num_cols = max(num_cols, max(len(row) for row in headers) if headers else 0)
    if rows:
        num_cols = max(num_cols, max(len(row) for row in rows) if rows else 0)
    
    if num_cols == 0:
        return []
    
    # Calculate max content length for each column
    column_max_lengths = [0] * num_cols
    
    # Check headers
    for header_row in headers:
        for col_idx, cell_content in enumerate(header_row):
            if col_idx < num_cols and cell_content:
                column_max_lengths[col_idx] = max(
                    column_max_lengths[col_idx], 
                    _estimate_text_width(cell_content)
                )
    
    # Check data rows
    for data_row in rows:
        for col_idx, cell_content in enumerate(data_row):
            if col_idx < num_cols and cell_content:
                column_max_lengths[col_idx] = max(
                    column_max_lengths[col_idx], 
                    _estimate_text_width(cell_content)
                )
    
    # Apply min/max constraints and convert to points
    column_widths = []
    for max_length in column_max_lengths:
        # Base calculation: approximately 6 points per character
        base_width = max_length * 6
        
        # Apply constraints
        width = max(min_width, min(base_width, max_width))
        column_widths.append(width)
    
    # Normalize to ensure reasonable distribution
    total_width = sum(column_widths)
    if total_width > 500:  # If total is too wide, proportionally reduce
        scaling_factor = 500 / total_width
        column_widths = [int(width * scaling_factor) for width in column_widths]
    
    return column_widths


def _estimate_text_width(text):
    """
    Estimates the display width of text content.
    
    Args:
        text (str): The text to measure.
    
    Returns:
        int: Estimated width in characters.
    """
    if not text:
        return 0
    
    # Remove extra whitespace and count actual display characters
    clean_text = ' '.join(text.split())
    
    # Account for different character widths (rough approximation)
    width = 0
    for char in clean_text:
        if char.isupper():
            width += 1.2  # Uppercase letters are typically wider
        elif char.isdigit():
            width += 1.0  # Numbers are consistent width
        elif char in 'ijl':
            width += 0.5  # These letters are narrower
        elif char in 'mwMW':
            width += 1.5  # These letters are wider
        else:
            width += 1.0  # Standard character width
    
    return int(width)
