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


# -----------------
# Private helpers: cell styling
# -----------------

def _prepare_cell_paragraph(cell):
	"""Prepare the cell paragraph by removing excess paragraphs and returning the first one."""
	paragraphs = cell.paragraphs
	
	for i in range(len(paragraphs) - 1, 0, -1):
		p = paragraphs[i]._element
		p.getparent().remove(p)

	return cell.paragraphs[0]

def _ensure_single_run(paragraph):
	"""Ensure the paragraph has a single run, removing any extras, and return it."""
	if len(paragraph.runs) == 0:
		return paragraph.add_run()
	
	run = paragraph.runs[0]
	
	for i in range(len(paragraph.runs) - 1, 0, -1):
		r = paragraph.runs[i]._element
		r.getparent().remove(r)
	
	return run

def _apply_run_font(run, bold=False, font_size=7, font_color=None):
	"""Apply font styling to a run."""
	font = run.font
	font.bold = bold
	font.size = Pt(font_size)

	if font_color:
		font.color.rgb = font_color

def _apply_paragraph_spacing(paragraph):
	"""Apply spacing to the paragraph."""
	paragraph.space_before = Pt(0)
	paragraph.space_after = Pt(0)
	paragraph.line_spacing = 1.0
	pf = paragraph.paragraph_format
	pf.space_before = Pt(0)
	pf.space_after = Pt(0)
	pf.line_spacing = 1.0
	pf.keep_together = True
	pf.keep_with_next = False
	pf.page_break_before = False
	pf.widow_control = False
	
	try:
		pPr = paragraph._element.get_or_add_pPr()
		existing = pPr.find(qn('w:spacing'))
		if existing is not None:
			pPr.remove(existing)
		spacing = OxmlElement('w:spacing')
		spacing.set(qn('w:before'), '0')
		spacing.set(qn('w:after'), '0')
		spacing.set(qn('w:lineRule'), 'auto')
		pPr.append(spacing)
	except Exception:
		pass

def _apply_paragraph_alignment(paragraph, align):
	"""Apply alignment to the paragraph."""
	if align == 'center':
		paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
	elif align == 'left':
		paragraph.alignment = WD_ALIGN_PARAGRAPH.LEFT
	elif align == 'right':
		paragraph.alignment = WD_ALIGN_PARAGRAPH.RIGHT

def _apply_cell_background(cell, bg_color):
	"""Apply background shading to the cell."""
	shading_elm = OxmlElement('w:shd')
	shading_elm.set(qn('w:fill'), bg_color)
	cell._element.get_or_add_tcPr().append(shading_elm)

def _apply_cell_margins(cell):
	"""Apply zero margins to the cell."""
	tc = cell._element
	tcPr = tc.get_or_add_tcPr()
	existing_spacing = tcPr.find(qn('w:tcMar'))

	if existing_spacing is not None:
		tcPr.remove(existing_spacing)

	tcMar = OxmlElement('w:tcMar')

	for margin_name in ['top', 'left', 'bottom', 'right']:
		margin_elem = OxmlElement(f'w:{margin_name}')
		margin_elem.set(qn('w:w'), '0')
		margin_elem.set(qn('w:type'), 'dxa')
		tcMar.append(margin_elem)

	tcPr.append(tcMar)
