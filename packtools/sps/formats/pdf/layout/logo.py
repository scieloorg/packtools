"""Decisões de tamanho e posição do logo do periódico (sem python-docx)."""

from dataclasses import dataclass

POSITIONS = ('left', 'right', 'full_width')

# Caixa padrão por posição, a partir da mediana dos logos em PDFs publicados.
# None na largura da faixa = largura do texto.
DEFAULT_BOX_MM = {
    'left': (40.0, 20.0),
    'right': (40.0, 20.0),
    'full_width': (None, 15.0),
}

EMU_PER_MM = 36000

# Abaixo disso o PNG sai borrado na impressão; só gera aviso.
MIN_PNG_DPI = 150


@dataclass(frozen=True)
class LogoSpec:
    path: str
    position: str = 'left'
    max_width_mm: float = None
    max_height_mm: float = None
    show_title: bool = True
    # PNG de reserva para logo em SVG (opcional).
    fallback_path: str = None


def normalize_logo_spec(raw):
    """
    Converte o dict recebido em `data['journal_logo']` em LogoSpec, com os
    padrões da posição preenchidos. Retorna None se não houver logo.
    """
    if not raw:
        return None
    if isinstance(raw, str):
        raw = {'path': raw}
    path = raw.get('path')
    if not path:
        return None
    position = raw.get('position') or 'left'
    if position not in POSITIONS:
        raise ValueError(f"posição de logo inválida: {position!r} (use {', '.join(POSITIONS)})")
    default_w, default_h = DEFAULT_BOX_MM[position]
    max_w = raw.get('max_width_mm')
    max_h = raw.get('max_height_mm')
    return LogoSpec(
        path=path,
        position=position,
        max_width_mm=float(max_w) if max_w is not None else default_w,
        max_height_mm=float(max_h) if max_h is not None else default_h,
        show_title=bool(raw.get('show_title', True)),
        fallback_path=raw.get('fallback_path') or None,
    )


def box_emu(spec, content_width_emu):
    """Caixa máxima em EMU; a largura nunca passa da largura do texto."""
    max_w = content_width_emu if spec.max_width_mm is None else int(spec.max_width_mm * EMU_PER_MM)
    max_w = min(max_w, int(content_width_emu))
    max_h = int(spec.max_height_mm * EMU_PER_MM)
    return max_w, max_h


def fit_logo_emu(px_width, px_height, max_width_emu, max_height_emu):
    """
    Maior tamanho que cabe na caixa mantendo a proporção. Ignora o dpi do
    arquivo de propósito: o tamanho vem só da caixa.
    """
    if px_width <= 0 or px_height <= 0:
        raise ValueError('imagem sem dimensões válidas')
    scale = min(max_width_emu / px_width, max_height_emu / px_height)
    return int(px_width * scale), int(px_height * scale)


def effective_dpi(px_width, width_emu):
    """Pixels por polegada do PNG no tamanho em que ele sai no PDF."""
    return px_width / (width_emu / EMU_PER_MM / 25.4)
