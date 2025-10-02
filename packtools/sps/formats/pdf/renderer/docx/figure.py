import os

from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Cm

from packtools.sps.formats.pdf import enum as pdf_enum
from packtools.sps.formats.pdf.utils.request_utils import download_remote_asset
from packtools.sps.formats.pdf.utils.file_utils import resolve_asset_path


def add_figure(docx, figure_data, header_style_name='SCL Table Heading', page_attributes=pdf_enum.PAGE_ATTRIBUTES):
    """
    Insert a figure with caption into the document. Scales image to fit page content width.

    figure_data keys: label, caption, href, alt
    """
    content_width = _compute_content_width(page_attributes)

    layout = figure_data.get('layout') if isinstance(figure_data, dict) else None
    if not layout:
        layout = decide_figure_layout(docx, figure_data, page_attributes=page_attributes)

    single_col_width = _compute_single_column_width(page_attributes)

    target_width = content_width if layout == pdf_enum.SINGLE_COLUMN_PAGE_LABEL else single_col_width
    context = _get_docx_context(docx)
    href, alt = _extract_figure_meta(figure_data)
    img_path = _resolve_image_path(href, context)

    picture_added = _try_insert_picture(docx, img_path, target_width, page_attributes)
    if not picture_added:
        _add_alt_paragraph(docx, alt)

    _add_caption(docx, figure_data, header_style_name)
