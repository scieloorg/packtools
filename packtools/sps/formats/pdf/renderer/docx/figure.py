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


# -----------------
# Private helpers
# -----------------

def _infer_image_dpi(im) -> float:
    """Infer the horizontal DPI from a PIL Image, considering multiple metadata sources.

    Priority:
    - im.info['dpi']: tuple or number
    - im.info['jfif_unit'] and im.info['jfif_density'] (unit 1=inches, 2=cm)
    Fallback: 96 dpi
    """
    try:
        info = getattr(im, 'info', {}) or {}
        # Native 'dpi'
        dpi = info.get('dpi')

        if isinstance(dpi, tuple) and len(dpi) >= 1 and dpi[0]:
            return float(dpi[0])

        if isinstance(dpi, (int, float)) and dpi > 0:
            return float(dpi)

        # JFIF density
        unit = info.get('jfif_unit')  # 1 = dots per inch, 2 = dots per cm
        density = info.get('jfif_density')

        if isinstance(unit, int) and isinstance(density, tuple) and len(density) >= 1 and density[0]:
            if unit == 1:  # per inch
                return float(density[0])

            if unit == 2:  # per cm
                return float(density[0]) * 2.54
        return 96.0

    except Exception:
        return 96.0

def _add_paragraph_with_formatting(docx, text, style_name='SCL Paragraph'):
    """Minimal helper to add a paragraph with an optional style, avoiding circular imports."""
    p = docx.add_paragraph(text)
    try:
        p.style = docx.styles[style_name]
    except KeyError:
        pass
    return p

def _compute_content_width(page_attributes):
    """Compute the content width (page width minus left and right margins) in Cm."""
    page_width = page_attributes.get('page_width', Cm(21.0))
    left_margin = page_attributes.get('left_margin', Cm(2.0))
    right_margin = page_attributes.get('right_margin', Cm(2.0))
    return page_width - left_margin - right_margin

def _compute_single_column_width(page_attributes):
    """Compute the width of a single column in a two-column layout, accounting for column spacing."""
    content_width = _compute_content_width(page_attributes)
    column_spacing_twips = getattr(pdf_enum, 'TWO_COLUMNS_SPACING', 300)
    column_spacing_cm = Cm(column_spacing_twips / 567.0)
    return (content_width - column_spacing_cm) / 2

def _get_docx_context(docx):
    """Retrieve the _scl_context dictionary from the docx Document, if available."""
    return getattr(docx, '_scl_context', {}) if hasattr(docx, '_scl_context') else {}

def _extract_figure_meta(figure_data):
    """Extract href and alt text from figure_data dict."""
    href = figure_data.get('href')
    alt = figure_data.get('alt') or (figure_data.get('href') or '[Figure]')
    return href, alt

def _resolve_image_path(href, context):
    """Resolve the image path, handling local paths and remote URLs."""
    if not href:
        assets_dir = context.get('assets_dir')
    
    img_path = resolve_asset_path(href, assets_dir=assets_dir)
    if isinstance(img_path, str) and (img_path.startswith('http://') or img_path.startswith('https://')):
        downloaded = download_remote_asset(img_path, context)
        if downloaded:
            img_path = downloaded

    return img_path

def _try_insert_picture(docx, img_path, content_width, page_attributes):
    """Try to insert a picture into the document, scaling it to fit content width. Returns True if successful."""
    if not (img_path and os.path.exists(img_path)):
        return False
    try:
        pic_para = docx.add_paragraph()
        run = pic_para.add_run()
        picture = run.add_picture(img_path)
        
        _scale_picture_to_fit(picture, content_width, page_attributes)
        pic_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        return True
    except Exception:
        return False

def _scale_picture_to_fit(picture, content_width, page_attributes):
    """Scale the picture to fit within content_width and page height constraints, preserving aspect ratio."""
    try:
        orig_w = int(picture.width)
        orig_h = int(picture.height)
        max_w = int(content_width)
        page_height = page_attributes.get('page_height', Cm(29.7))
        top_margin = page_attributes.get('top_margin', Cm(3.5))
        bottom_margin = page_attributes.get('bottom_margin', Cm(2.0))
        max_h = int(page_height - top_margin - bottom_margin - Cm(2.0))
        scale_w = min(1.0, max_w / orig_w) if orig_w else 1.0
        scale_h = min(1.0, max_h / orig_h) if orig_h else 1.0
        scale = min(scale_w, scale_h)

        if scale < 1.0:
            picture.width = int(orig_w * scale)
            picture.height = int(orig_h * scale)

    except Exception:
        # Fallback to width-only clamp
        try:
            if picture.width and int(picture.width) > int(content_width):
                picture.width = int(content_width)
        except Exception:
            pass

def _add_alt_paragraph(docx, alt_text):
    """Add a paragraph with alt text when the image cannot be inserted."""
    _add_paragraph_with_formatting(docx, alt_text)

def _add_caption(docx, figure_data, header_style_name):
    """Add a caption paragraph below the figure, if label or caption is provided."""
    if not (figure_data.get('label') or figure_data.get('caption')):
        return
    
    p = docx.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    if figure_data.get('label'):
        r_label = p.add_run(figure_data['label'])
        r_label.bold = True
        if figure_data.get('caption'):
            p.add_run('. ')

    if figure_data.get('caption'):
        r_cap = p.add_run(figure_data['caption'])
        r_cap.bold = False

    try:
        p.style = docx.styles[header_style_name]
    except KeyError:
        pass
