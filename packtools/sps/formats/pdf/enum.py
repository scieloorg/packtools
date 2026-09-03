from docx.enum.style import WD_STYLE_TYPE
from docx.enum.section import WD_ORIENT, WD_SECTION

from packtools.sps.formats.pdf import layout_config


NAMESPACES = {'xml': 'http://www.w3.org/XML/1998/namespace'}

# Page/layout attributes and column spacing come from default_layout.json
# (packaged alongside this module) instead of being hardcoded here, so a
# journal-specific layout can eventually override them by pointing the
# loader at a different file.
PAGE_ATTRIBUTES = layout_config.load_page_attributes()

# TWO_COLUMNS_SPACING is the space between two columns in twocolumn layout, measured in twips (1/20 of a point).
TWO_COLUMNS_SPACING = layout_config.load_column_spacing_twips()

SUPPORTED_STYLES = [
    WD_STYLE_TYPE.CHARACTER,
    WD_STYLE_TYPE.PARAGRAPH,
    WD_STYLE_TYPE.TABLE,
]

SINGLE_COLUMN_PAGE_LABEL = 'single-column-layout'
DOUBLE_COLUMN_PAGE_LABEL = 'double-column-layout'
