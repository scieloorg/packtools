from docx import Document

from packtools.sps.formats.pdf.renderer.docx.style import copy_styles


def init_docx(data):
    """Initialize a DOCX document with optional base layout and context."""
    source_layout = data.get('base_layout')
    if not source_layout:
        docx = Document()
    else:
        source_docx = Document(source_layout)
        docx = Document()
        copy_styles(source_docx, docx)

    try:
        docx._scl_context = {
            'assets_dir': data.get('assets_dir'),
            'download_cache_dir': None,
        }
    except Exception:
        pass
    return docx
