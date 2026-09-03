import json
from pathlib import Path

from docx.enum.section import WD_ORIENT, WD_SECTION
from docx.shared import Pt

_DEFAULT_PATH = Path(__file__).parent / "default_layout.json"

_ORIENTATION_MAP = {
    "portrait": WD_ORIENT.PORTRAIT,
    "landscape": WD_ORIENT.LANDSCAPE,
}

_START_TYPE_MAP = {
    "continuous": WD_SECTION.CONTINUOUS,
    "new_page": WD_SECTION.NEW_PAGE,
    "even_page": WD_SECTION.EVEN_PAGE,
    "odd_page": WD_SECTION.ODD_PAGE,
}


def load_page_attributes(path=None):
    """
    Load page/layout attributes from a layout-config JSON, returning a dict
    shaped like the legacy PAGE_ATTRIBUTES (Pt/Cm Length objects and
    python-docx enums), for drop-in use wherever PAGE_ATTRIBUTES is passed
    today.

    `path` lets a caller point at a different file; defaults to the
    packaged default_layout.json. Not wired to the CLI/API yet - that
    comes with per-journal config support.
    """
    data = json.loads(Path(path or _DEFAULT_PATH).read_text())
    page = data["page"]

    return {
        "top_margin": Pt(page["top_margin_pt"]),
        "left_margin": Pt(page["left_margin_pt"]),
        "right_margin": Pt(page["right_margin_pt"]),
        "bottom_margin": Pt(page["bottom_margin_pt"]),
        "header_distance": Pt(page["header_distance_pt"]),
        "footer_distance": Pt(page["footer_distance_pt"]),
        "gutter": Pt(page["gutter_pt"]),
        "orientation": _ORIENTATION_MAP[page["orientation"]],
        "page_width": Pt(page["page_width_pt"]),
        "page_height": Pt(page["page_height_pt"]),
        "different_first_page_header_footer": page["different_first_page_header_footer"],
        "start_type": _START_TYPE_MAP[page["body_start_type"]],
        "default_column_count": page["default_column_count"],
    }


def load_column_spacing_twips(path=None):
    """
    Load the column spacing (in twips, 1/20 of a point) from the same
    layout-config JSON used by load_page_attributes.
    """
    data = json.loads(Path(path or _DEFAULT_PATH).read_text())
    return round(data["page"]["column_spacing_pt"] * 20)
