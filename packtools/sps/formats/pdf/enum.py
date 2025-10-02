from docx.enum.style import WD_STYLE_TYPE
from docx.enum.section import WD_ORIENT, WD_SECTION
from docx.shared import Cm


NAMESPACES = {'xml': 'http://www.w3.org/XML/1998/namespace'}

PAGE_ATTRIBUTES = {
    "top_margin": Cm(3.5), 
    "left_margin": Cm(2),
    "right_margin": Cm(2), 
    "bottom_margin": Cm(2), 
    "header_distance": Cm(1), 
    "footer_distance": Cm(1), 
    "gutter": Cm(0), 
    "orientation": WD_ORIENT.PORTRAIT,
    "page_width": Cm(21.0),
    "page_height": Cm(29.7),
    "different_first_page_header_footer": True,
    "start_type": WD_SECTION.NEW_PAGE,
}

SUPPORTED_STYLES = [
    WD_STYLE_TYPE.CHARACTER,
    WD_STYLE_TYPE.PARAGRAPH,
    WD_STYLE_TYPE.TABLE,
]

# TWO_COLUMNS_SPACING is the space between two columns in twocolumn layout, measured in twips (1/20 of a point).
# 300 twips = 15 points = ~5.29 mm
TWO_COLUMNS_SPACING = 300

SINGLE_COLUMN_PAGE_LABEL = 'single-column-layout'
DOUBLE_COLUMN_PAGE_LABEL = 'double-column-layout'
