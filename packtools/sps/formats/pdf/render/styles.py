"""Estilos do layout.docx: cópia para o documento novo e aplicação tolerante a estilo ausente."""

from docx.enum.style import WD_STYLE_TYPE
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from packtools.sps.formats.pdf.config.styles import STYLES

_COPIED_TYPES = (WD_STYLE_TYPE.PARAGRAPH, WD_STYLE_TYPE.CHARACTER, WD_STYLE_TYPE.TABLE)
_FONT_ATTRS = (
    "bold",
    "italic",
    "underline",
    "strike",
    "all_caps",
    "highlight_color",
    "superscript",
    "subscript",
)
_PARAGRAPH_ATTRS = (
    "left_indent",
    "right_indent",
    "first_line_indent",
    "keep_together",
    "keep_with_next",
    "page_break_before",
    "widow_control",
    "space_before",
    "space_after",
    "line_spacing",
    "line_spacing_rule",
)


def get(doc, role):
    """Estilo do papel (chave de STYLES) ou nome direto; None se o layout não o tiver."""
    name = STYLES.get(role, role)
    try:
        return doc.styles[name]
    except KeyError:
        return None


def apply(element, doc, role):
    """Atribui o estilo a parágrafo/run se existir; devolve o estilo (ou None)."""
    style = get(doc, role)
    if style is not None:
        element.style = style
    return style


def copy_styles(source, target):
    """Copia estilos de parágrafo, caractere e tabela de source para target (fonte e parágrafo)."""
    for style in source.styles:
        if style.type not in _COPIED_TYPES:
            continue
        if style.name in target.styles:
            target.styles[style.name].delete()
        new = target.styles.add_style(style.name, style.type)
        new.base_style = style.base_style
        for attr in ("hidden", "priority", "quick_style", "unhide_when_used"):
            setattr(new, attr, getattr(style, attr))
        if style.type == WD_STYLE_TYPE.TABLE:
            continue
        _copy_font(style.font, new.font)
        if style.type == WD_STYLE_TYPE.PARAGRAPH:
            _copy_paragraph_format(style.paragraph_format, new.paragraph_format)


def _copy_font(src, dst):
    """Copia nome, tamanho, cor e atributos de fonte de um estilo para outro."""
    if src.name:
        dst.name = src.name
    if src.size:
        dst.size = src.size
    for attr in _FONT_ATTRS:
        setattr(dst, attr, getattr(src, attr))
    if src.color.rgb:
        dst.color.rgb = src.color.rgb
    if src.color.theme_color:
        dst.color.theme_color = src.color.theme_color


def _copy_paragraph_format(src, dst):
    """Copia alinhamento, recuos, espaçamentos e controles de quebra do parágrafo."""
    try:
        dst.alignment = src.alignment
    except ValueError:
        dst.alignment = WD_PARAGRAPH_ALIGNMENT.JUSTIFY
    for attr in _PARAGRAPH_ATTRS:
        setattr(dst, attr, getattr(src, attr))
