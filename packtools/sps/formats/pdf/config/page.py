"""
Configuração de página: lê o JSON de layout (padrão: default_layout.json,
nesta pasta) e define os nomes dos dois layouts de tabela/figura.

Só lê e converte a configuração; as medidas derivadas dela (largura útil,
largura de coluna, altura útil) ficam em ``layout.page``.
"""

import json
from pathlib import Path

from docx.enum.section import WD_ORIENT, WD_SECTION
from docx.shared import Pt

DEFAULT_LAYOUT_PATH = Path(__file__).parent / "default_layout.json"

SINGLE_COLUMN = "single-column-layout"
DOUBLE_COLUMN = "double-column-layout"

_ORIENTATION = {"portrait": WD_ORIENT.PORTRAIT, "landscape": WD_ORIENT.LANDSCAPE}
_START_TYPE = {
    "continuous": WD_SECTION.CONTINUOUS,
    "new_page": WD_SECTION.NEW_PAGE,
    "even_page": WD_SECTION.EVEN_PAGE,
    "odd_page": WD_SECTION.ODD_PAGE,
}


def load_page(path=None):
    """Atributos de página (Length/enums do python-docx) a partir do JSON de layout."""
    page = json.loads(Path(path or DEFAULT_LAYOUT_PATH).read_text())["page"]
    return {
        "top_margin": Pt(page["top_margin_pt"]),
        "left_margin": Pt(page["left_margin_pt"]),
        "right_margin": Pt(page["right_margin_pt"]),
        "bottom_margin": Pt(page["bottom_margin_pt"]),
        "header_distance": Pt(page["header_distance_pt"]),
        "footer_distance": Pt(page["footer_distance_pt"]),
        "gutter": Pt(page["gutter_pt"]),
        "orientation": _ORIENTATION[page["orientation"]],
        "page_width": Pt(page["page_width_pt"]),
        "page_height": Pt(page["page_height_pt"]),
        "different_first_page_header_footer": page[
            "different_first_page_header_footer"
        ],
        "start_type": _START_TYPE[page["body_start_type"]],
        "column_count": max(1, page["default_column_count"]),
        # twips (1/20 de ponto)
        "column_spacing": round(page["column_spacing_pt"] * 20),
    }

