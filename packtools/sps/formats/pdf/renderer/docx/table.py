import re

from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ROW_HEIGHT_RULE, WD_CELL_VERTICAL_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt, Cm

from packtools.sps.formats.pdf import enum as pdf_enum


def style_cell(cell, bold=False, font_size=7, font_color=None, align='center', bg_color=None):
	"""Style a single table cell with tight spacing and alignment."""
	paragraph = _prepare_cell_paragraph(cell)
	run = _ensure_single_run(paragraph)

	_apply_run_font(run, bold=bold, font_size=font_size, font_color=font_color)
	_apply_paragraph_spacing(paragraph)
	_apply_paragraph_alignment(paragraph, align)

	if bg_color:
		_apply_cell_background(cell, bg_color)

	_apply_cell_margins(cell)

def add_table(docx, table_data, header_style_name='SCL Table Heading', page_attributes=pdf_enum.PAGE_ATTRIBUTES):
	"""Adds a table with caption and normalized spacing to a DOCX document."""
	# Caption
	caption = _add_caption_paragraph(docx, table_data, header_style_name)

	headers, rows, header_spans, row_spans = _extract_table_data(table_data)
	num_cols = _determine_num_cols(headers, rows, header_spans, row_spans)
	if num_cols == 0:
		return

	empty_cols = _detect_empty_columns(headers, rows, num_cols)

	header_lines = len(headers)
	total_rows = header_lines + len(rows)
	table = docx.add_table(rows=max(1, total_rows), cols=num_cols)

	content_width, table_width, layout = _compute_table_width(page_attributes, table_data)
	_configure_table_properties(table, table_width, layout)

	col_widths = _compute_column_widths(num_cols, table_width, empty_cols)
	_set_column_widths(table, col_widths)

	_populate_headers(table, headers, num_cols)
	_populate_rows(table, rows, header_lines, num_cols)

	_adjust_row_heights(table)

	_apply_spans(table, header_spans, row_spans, header_lines, total_rows, num_cols)

	_finalize_table_appearance(table)

	if layout == pdf_enum.SINGLE_COLUMN_PAGE_LABEL:
		wrap_distance_twips = int(table_data.get('wrap_distance_twips', 0))
		_make_table_full_width_floating(table, wrap_distance_twips=wrap_distance_twips)
