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


# --------------
# Private helpers: table creation and layout
# --------------

def _add_caption_paragraph(docx, table_data, header_style_name):
	"""Add a caption paragraph below the table, if label or title is provided. Returns the paragraph or None."""
	p = docx.add_paragraph()
	p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
	
	if table_data.get('label'):
		r = p.add_run(table_data['label'])
		r.bold = True
		if table_data.get('title'):
			p.add_run('. ')
	
	if table_data.get('title'):
		r = p.add_run(table_data['title'])
		r.bold = False
	
	try:
		p.style = docx.styles[header_style_name]
		p.paragraph_format.keep_with_next = True
	except Exception:
		pass
	
	return p

def _extract_table_data(table_data):
	"""Extract relevant data from the table_data dictionary."""
	headers = table_data.get('headers') or []
	rows = table_data.get('rows') or []
	header_spans = table_data.get('header_spans') or []
	row_spans = table_data.get('row_spans') or []

	return headers, rows, header_spans, row_spans

def _determine_num_cols(headers, rows, header_spans, row_spans):
	"""Determine the number of columns in the table based on headers, rows, and spans."""
	if header_spans:
		return max((len(r) for r in header_spans), default=0)

	if row_spans:
		return max((len(r) for r in row_spans), default=0)

	if headers:
		return max(len(r) for r in headers)

	if rows:
		return max(len(r) for r in rows)

	return 0

def _detect_empty_columns(headers, rows, num_cols):
	"""Detect which columns are empty based on headers and rows. Returns a list of booleans."""
	def _is_text_empty(v):
		return v is None or (isinstance(v, str) and v.strip() == '')

	empty_cols = [True] * num_cols

	for hdr_row in headers or []:
		for j in range(num_cols):
			h = hdr_row[j] if j < len(hdr_row) else None
			if not _is_text_empty(h):
				empty_cols[j] = False

	for r in rows or []:
		for j in range(num_cols):
			if not empty_cols[j]:
				continue
			v = r[j] if j < len(r) else None
			if not _is_text_empty(v):
				empty_cols[j] = False

	return empty_cols

def _compute_table_width(page_attributes, table_data):
	"""Compute content width and table width based on page attributes and table layout."""
	page_width = page_attributes.get('page_width', Cm(21.0))
	left_margin = page_attributes.get('left_margin', Cm(2.0))
	right_margin = page_attributes.get('right_margin', Cm(2.0))
	content_width = page_width - left_margin - right_margin

	layout = table_data.get('layout', pdf_enum.DOUBLE_COLUMN_PAGE_LABEL)
	if layout == pdf_enum.SINGLE_COLUMN_PAGE_LABEL:
		table_width = content_width
	else:
		column_spacing = getattr(pdf_enum, 'TWO_COLUMNS_SPACING', 300)
		column_spacing = Cm(column_spacing / 567.0)
		table_width = (content_width - column_spacing) // 2

	return content_width, table_width, layout

def _configure_table_properties(table, table_width, layout):
	"""Configure table properties such as width, autofit, borders, and alignment."""
	_set_table_width(table, table_width)
	_disable_table_autofit(table)
	tblPr = table._element.tblPr
	_set_tblW(tblPr, table_width)
	_set_zero_cell_spacing(tblPr)
	_set_zero_cell_margins(tblPr)
	_force_fixed_tbl_layout(tblPr)
	_reset_alignment_props(tblPr)
	_apply_center_alignment_if_needed(tblPr, layout)

def _compute_column_widths(num_cols, table_width, empty_cols):
	"""Compute column widths, giving minimum width to empty columns."""
	min_col_width = int(Cm(0.381))
	empty_count = sum(1 for b in empty_cols if b)
	if empty_count > 0 and num_cols > 0:
		total_min_width = min_col_width * empty_count
		remaining_width = int(table_width) - total_min_width
		non_empty_count = num_cols - empty_count
		if remaining_width <= 0 or non_empty_count <= 0:
			return [max(1, int(int(table_width) / max(1, num_cols)))] * num_cols
		base_non_empty_width = int(remaining_width / non_empty_count)
		return [
			(min_col_width if empty_cols[i] else base_non_empty_width)
			for i in range(num_cols)
		]
	return [int(int(table_width) / max(1, num_cols))] * num_cols

def _set_column_widths(table, col_widths):
	"""Set the widths of the table columns."""
	for j, col in enumerate(table.columns):
		if j < len(col_widths):
			try:
				col.width = int(col_widths[j])
			except Exception:
				col.width = col_widths[j]

def _populate_headers(table, headers, num_cols):
	"""Populate the table header rows with data and style them."""
	for r_idx in range(len(headers)):
		row = table.rows[r_idx]
		data_row = headers[r_idx]

		for c_idx in range(min(len(data_row), num_cols)):
			cell = row.cells[c_idx]

			try:
				cell.text = _norm(data_row[c_idx])
			except Exception:
				cell.text = ''

			style_cell(cell, bold=True, font_size=7, align=('center' if c_idx >= 1 else 'left'))

def _populate_rows(table, rows, header_lines, num_cols):
	"""Populate the table body rows with data and style them."""
	for i, row_data in enumerate(rows):
		row = table.rows[header_lines + i]

		for j in range(min(len(row_data), num_cols)):
			try:
				cell = row.cells[j]
				cell.text = _norm(row_data[j])
				style_cell(cell, font_size=7, align=('center' if j >= 1 else 'left'))
			except Exception:
				pass

def _adjust_row_heights(table):
	"""Adjust row heights, setting minimal height for empty rows with vertical merges."""
	try:
		for r in table.rows:
			r.height_rule = WD_ROW_HEIGHT_RULE.AT_LEAST
			r.height = Pt(0)

			for c in r.cells:
				c.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.TOP

		for r in table.rows:
			if _row_is_fully_empty_with_vmerge(r) or _row_is_placeholder_only(r):
				r.height_rule = WD_ROW_HEIGHT_RULE.EXACTLY
				r.height = Pt(1)
	except Exception:
		pass

def _apply_spans(table, header_spans, row_spans, header_lines, total_rows, num_cols):
	"""Apply horizontal and vertical spans to the table based on header and row span metadata."""
	_apply_header_spans(table, header_spans, header_lines, total_rows, num_cols)
	_apply_body_spans(table, row_spans, header_lines, total_rows, num_cols)

def _apply_header_spans(table, header_spans, header_lines, total_rows, num_cols):
	"""Apply header spans to the table based on header span metadata."""
	for r_idx, span_row in enumerate(header_spans):
		if r_idx >= header_lines:
			break
		row = table.rows[r_idx]

		for c_idx, meta in enumerate(span_row):
			if not meta:
				continue
			colspan = int(meta.get('colspan', 1))
			rowspan = int(meta.get('rowspan', 1))
			_merge_horizontally(row, c_idx, colspan, num_cols, is_header=True)
		
			if rowspan > 1:
				_merge_vertically(table, r_idx, c_idx, rowspan, total_rows, is_header=True)

def _apply_body_spans(table, row_spans, header_lines, total_rows, num_cols):
	"""Apply body spans to the table based on row span metadata."""
	for r_idx, span_row in enumerate(row_spans):
		abs_r = header_lines + r_idx
		if abs_r >= total_rows:
			break
		
		row = table.rows[abs_r]
		
		for c_idx, meta in enumerate(span_row):
			if not meta:
				continue
			colspan = int(meta.get('colspan', 1))
			rowspan = int(meta.get('rowspan', 1))
			_merge_horizontally(row, c_idx, colspan, num_cols, is_header=False)
		
			if rowspan > 1:
				_merge_vertically(table, abs_r, c_idx, rowspan, total_rows, is_header=False)

def _set_table_width(table, table_width):
	"""Set table width"""
	try:
		table.width = int(table_width)
	except Exception:
		table.width = table_width

def _disable_table_autofit(table):
	"""Diable table autofit"""
	try:
		table.autofit = False
		table.allow_autofit = False
	except Exception:
		pass

def _set_tblW(tblPr, table_width):
	"""Set """
	try:
		existing_tblW = tblPr.find(qn('w:tblW'))
		if existing_tblW is not None:
			tblPr.remove(existing_tblW)

		twips_val = str(int(int(table_width) / 635))

		tblW = OxmlElement('w:tblW')
		tblW.set(qn('w:w'), twips_val)
		tblW.set(qn('w:type'), 'dxa')

		tblPr.append(tblW)
	except Exception:
		pass

def _set_zero_cell_spacing(tblPr):
	"""Remove inner space from cells"""
	existing_spacing = tblPr.find(qn('w:tblCellSpacing'))
	if existing_spacing is not None:
		tblPr.remove(existing_spacing)
	
	tblCellSpacing = OxmlElement('w:tblCellSpacing')
	tblCellSpacing.set(qn('w:w'), '0')
	tblCellSpacing.set(qn('w:type'), 'dxa')
	tblPr.append(tblCellSpacing)

def _set_zero_cell_margins(tblPr):
	"""Remove margin from cells"""
	existing_cellMar = tblPr.find(qn('w:tblCellMar'))
	if existing_cellMar is not None:
		tblPr.remove(existing_cellMar)
	
	tblCellMar = OxmlElement('w:tblCellMar')
	
	for side in ['top', 'left', 'bottom', 'right']:
		m = OxmlElement(f'w:{side}')
		m.set(qn('w:w'), '0')
		m.set(qn('w:type'), 'dxa')
		tblCellMar.append(m)
	
	tblPr.append(tblCellMar)

def _force_fixed_tbl_layout(tblPr):
	"""Force tables to be fixed"""
	existing_layout = tblPr.find(qn('w:tblLayout'))
	if existing_layout is not None:
		tblPr.remove(existing_layout)

	tblLayout = OxmlElement('w:tblLayout')
	tblLayout.set(qn('w:type'), 'fixed')
	tblPr.append(tblLayout)

def _reset_alignment_props(tblPr):
	"""Reset aligment properties"""
	existing_indent = tblPr.find(qn('w:tblInd'))
	if existing_indent is not None:
		tblPr.remove(existing_indent)

	existing_jc = tblPr.find(qn('w:jc'))
	if existing_jc is not None:
		tblPr.remove(existing_jc)

def _apply_center_alignment_if_needed(tblPr, layout):
	"""Apply center alignment"""
	if layout != pdf_enum.SINGLE_COLUMN_PAGE_LABEL:
		jc = OxmlElement('w:jc')
		jc.set(qn('w:val'), 'center')
		tblPr.append(jc)

def _merge_horizontally(row, start_col, span, num_cols, is_header=False):
	"""Merge cells horizontally"""
	if span <= 1:
		return row.cells[start_col]

	end = min(start_col + span - 1, num_cols - 1)
	master = row.cells[start_col]
	cells_range = [row.cells[c] for c in range(start_col, end + 1)]

	master_text = _norm(master.text)
	if not master_text:
		pick_text = _first_non_empty_text(cells_range)
		if pick_text:
			_set_first_run_text(master, pick_text)

	for c in range(start_col + 1, end + 1):
		try:
			row.cells[c].text = ''
		except Exception:
			pass

	merged = master

	for c in range(start_col + 1, end + 1):
		try:
			merged = merged.merge(row.cells[c])
		except Exception:
			break
	align = ('center' if start_col >= 1 else 'left')
	style_cell(master, bold=is_header, font_size=7, align=align)

	return master

def _merge_vertically(table, start_row, col_idx, rowspan, total_rows, is_header=False):
	"""Merge cells vertically"""
	master_cell = table.cell(start_row, col_idx)
	last_row = min(start_row + rowspan - 1, total_rows - 1)

	try:
		below_cells = [table.cell(rr, col_idx) for rr in range(start_row, last_row + 1)]

		if not _norm(master_cell.text):
			pick_text = _first_non_empty_text(below_cells)
			if pick_text:
				_set_first_run_text(master_cell, pick_text)

		for rr in range(start_row + 1, last_row + 1):
			try:
				table.cell(rr, col_idx).text = ''
			except Exception:
				pass
			master_cell = master_cell.merge(table.cell(rr, col_idx))
	except Exception:
		pass

	align = ('center' if col_idx >= 1 else 'left')
	style_cell(master_cell, bold=is_header, font_size=7, align=align)

def _finalize_table_appearance(table):
	"""Finalize table appearance"""
	table.alignment = WD_TABLE_ALIGNMENT.CENTER
	table.style = 'Table Grid'
	_set_table_outer_borders(table, color='000000', size=8, space=0)

def _set_table_outer_borders(t, color='000000', size=8, space=0):
	"""Set table outer borders (top and botoom)"""
	try:
		t_el = t._element
		t_pr = t_el.tblPr
		existing = t_pr.find(qn('w:tblBorders'))

		if existing is not None:
			t_pr.remove(existing)

		borders = OxmlElement('w:tblBorders')

		for side in ('top', 'bottom',):
			b = OxmlElement(f'w:{side}')
			b.set(qn('w:val'), 'single')
			b.set(qn('w:sz'), str(size))
			b.set(qn('w:color'), color)
			b.set(qn('w:space'), str(space))
			borders.append(b)

		t_pr.append(borders)
	except Exception:
		pass
