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
