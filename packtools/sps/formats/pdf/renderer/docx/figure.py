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

def decide_figure_layout(docx, figure_data, page_attributes=pdf_enum.PAGE_ATTRIBUTES, threshold: float = 1.1):
    """
    Decide whether a figure should occupy the full page width (double-column-layout) or a single column (single-column-layout).

    Heuristic:
    - Compute the natural width of the image in centimeters using Pillow and its DPI metadata (tries dpi, jfif_density; defaults to 150 DPI when missing).
    - Compute the available content width (page width minus margins) and the single-column width ((content - column_spacing)/2).
    - If natural image width >= threshold * single-column width, return 'double-column-layout'; otherwise 'single-column-layout'.

    Args:
        docx: The Document, used to read `_scl_context` for assets_dir and cache.
        figure_data: Dict with at least 'href' (and optionally 'alt').
        page_attributes: Dict containing Cm values for page_width, margins, and optionally TWO_COLUMNS_SPACING in twips via pdf_enum.
        threshold: Float in (0,1.5] to bias decision; higher means prefer double-column for larger images. Default 0.9.

    Returns:
        str: 'double-column-layout' or 'single-column-layout'
    """
    # Per-figure overrides
    if isinstance(figure_data, dict):
        # If layout is explicitly provided, respect it
        forced = figure_data.get('layout')
        if forced in (pdf_enum.SINGLE_COLUMN_PAGE_LABEL, pdf_enum.DOUBLE_COLUMN_PAGE_LABEL):
            return forced
        # Allow per-figure threshold override
        try:
            override = figure_data.get('layout_threshold')
            if override is not None:
                threshold = float(override)
        except Exception:
            pass

    try:
        from PIL import Image
    except Exception:
        # If Pillow is unavailable at runtime, fallback conservatively
        return pdf_enum.SINGLE_COLUMN_PAGE_LABEL

    # Compute layout widths (in Cm)
    page_width = page_attributes.get('page_width', Cm(21.0))
    left_margin = page_attributes.get('left_margin', Cm(2.0))
    right_margin = page_attributes.get('right_margin', Cm(2.0))
    content_width = page_width - left_margin - right_margin

    # Convert TWO_COLUMNS_SPACING (twips) to Cm, mirroring table_utils logic
    column_spacing_twips = getattr(pdf_enum, 'TWO_COLUMNS_SPACING', 300)
    column_spacing_cm = Cm(column_spacing_twips / 567.0)
    single_col_width = (content_width - column_spacing_cm) / 2

    # Resolve image path (local or download)
    context = _get_docx_context(docx)
    href = figure_data.get('href') if isinstance(figure_data, dict) else None
    img_path = _resolve_image_path(href, context)
    if not img_path:
        return pdf_enum.SINGLE_COLUMN_PAGE_LABEL

    # Open image and compute its natural width in Cm using DPI (default 72 DPI)
    if not os.path.exists(img_path):
        return pdf_enum.SINGLE_COLUMN_PAGE_LABEL
    try:
        with Image.open(img_path) as im:
            px_w = im.width
            dpi = _infer_image_dpi(im)
            # width in inches then to Cm
            width_in_cm = (px_w / max(1.0, dpi)) * 2.54
    except Exception:
        return pdf_enum.SINGLE_COLUMN_PAGE_LABEL

    # If the image is wider than a single column by the threshold factor, prefer a single-column-layout (full width). Otherwise, keep double-column-layout.
    return pdf_enum.SINGLE_COLUMN_PAGE_LABEL if width_in_cm >= float(threshold) * float(single_col_width) else pdf_enum.DOUBLE_COLUMN_PAGE_LABEL

