"""
Geometria do cabeçalho da 1ª página: tamanho do logo do periódico e
larguras das colunas de logo, título e DOI (sem python-docx).

O render lê só o tamanho em pixels do arquivo (render.logo.read_logo_size)
e chama ``logo_header``; todo o resto (caixa máxima, redução para caber,
divisão das colunas, avisos de redução e de resolução) é decidido aqui.

Todas as medidas de saída são em EMU (36000 por mm).
"""

import logging
import math
from dataclasses import dataclass

from packtools.sps.formats.pdf.layout.page import split_width

logger = logging.getLogger(__name__)

POSITIONS = ("left", "right", "full_width")

# (largura, altura) por posição; None na largura = largura do texto.
DEFAULT_BOX_MM = {
    "left": (40.0, 20.0),
    "right": (40.0, 20.0),
    "full_width": (None, 15.0),
}

EMU_PER_MM = 36000

# Herdado do old_pdf: fração da largura do cabeçalho para o título do
# periódico. O DOI é curto e de tamanho quase constante (até ~55 caracteres
# no corpus de testes); o título usa fonte grande e precisa do espaço. Com
# 50/50, títulos reais (ex. "Urbe. Revista Brasileira de Gestão Urbana")
# passavam de 2 para 3 linhas sem ganho para o DOI.
JOURNAL_TITLE_DOI_SPLIT = 0.65
# Espaço (EMU, 0.4cm) entre o logo e o título na mesma linha do cabeçalho.
LOGO_GAP = int(4 * EMU_PER_MM)

# Abaixo disso o PNG sai borrado na impressão; só gera aviso.
MIN_PNG_DPI = 150


@dataclass(frozen=True)
class LogoSpec:
    """Logo do periódico já normalizado: arquivo, posição, caixa máxima (mm), título visível e PNG de reserva."""

    path: str
    position: str = "left"
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
        raw = {"path": raw}
    path = raw.get("path")
    if not path:
        return None
    position = raw.get("position") or "left"
    if position not in POSITIONS:
        raise ValueError(
            f"posição de logo inválida: {position!r} (use {', '.join(POSITIONS)})"
        )
    default_w, default_h = DEFAULT_BOX_MM[position]
    return LogoSpec(
        path=path,
        position=position,
        max_width_mm=_positive_mm(raw, "max_width_mm", default_w),
        max_height_mm=_positive_mm(raw, "max_height_mm", default_h),
        show_title=bool(raw.get("show_title", True)),
        fallback_path=raw.get("fallback_path") or None,
    )


def _positive_mm(raw, key, default):
    """Lê raw[key] como número positivo em mm; ausente devolve default; inválido levanta ValueError."""
    value = raw.get(key)
    if value is None:
        return default
    try:
        number = float(value)
    except (TypeError, ValueError):
        number = math.nan
    if not math.isfinite(number) or number <= 0:
        raise ValueError(f"{key} inválido: {value!r} (use um número maior que zero)")
    return number


def box_emu(spec, content_width_emu):
    """Caixa máxima em EMU; a largura nunca passa da largura do texto."""
    max_w = (
        content_width_emu
        if spec.max_width_mm is None
        else int(spec.max_width_mm * EMU_PER_MM)
    )
    max_w = min(max_w, int(content_width_emu))
    max_h = int(spec.max_height_mm * EMU_PER_MM)
    return max_w, max_h


def min_title_width_emu(content_width_emu, doi_width_emu, gap_emu):
    """Largura do título ao lado do logo à esquerda na caixa padrão."""
    default_logo_width = int(DEFAULT_BOX_MM["left"][0] * EMU_PER_MM)
    return int(content_width_emu - doi_width_emu - gap_emu - default_logo_width)


def max_logo_width_emu(spec, content_width_emu, doi_width_emu, gap_emu):
    """Maior largura de logo que deixa espaço para o DOI e, com título, para min_title_width_emu."""
    if spec.position == "full_width":
        return int(content_width_emu)
    title_width = (
        min_title_width_emu(content_width_emu, doi_width_emu, gap_emu)
        if spec.show_title
        else 0
    )
    if spec.position == "left":
        return int(content_width_emu - doi_width_emu - gap_emu - title_width)
    return int(content_width_emu - gap_emu - max(title_width, doi_width_emu))


def fit_logo_emu(px_width, px_height, max_width_emu, max_height_emu):
    """
    Maior tamanho que cabe na caixa mantendo a proporção. Ignora o dpi do
    arquivo de propósito: o tamanho vem só da caixa.
    """
    if px_width <= 0 or px_height <= 0:
        raise ValueError("imagem sem dimensões válidas")
    scale = min(max_width_emu / px_width, max_height_emu / px_height)
    return int(px_width * scale), int(px_height * scale)


def effective_dpi(px_width, width_emu):
    """Pixels por polegada do PNG no tamanho em que ele sai no PDF."""
    return px_width / (width_emu / EMU_PER_MM / 25.4)


# -----------------
# Cabeçalho da 1ª página
# -----------------


def title_doi_columns(content_width_emu):
    """Larguras [título, DOI] (EMU) do cabeçalho da 1ª página, na proporção JOURNAL_TITLE_DOI_SPLIT."""
    return split_width(content_width_emu, JOURNAL_TITLE_DOI_SPLIT)


@dataclass(frozen=True)
class LogoHeader:
    """
    Medidas finais (EMU) do cabeçalho da 1ª página com logo.

    width, height : int
        Tamanho do logo.
    columns : tuple of int
        Larguras das colunas da tabela do cabeçalho, da esquerda para a
        direita, por posição do logo:

        ============  ===========  ===============================
        position      show_title   columns
        ============  ===========  ===============================
        left          True         (logo, título, DOI)
        left          False        (logo, DOI)
        right         —            (título e DOI empilhados, logo)
        full_width    True         (título, DOI) abaixo do logo
        full_width    False        () — logo e DOI em parágrafos
        ============  ===========  ===============================
    """

    width: int
    height: int
    columns: tuple


def logo_header(spec, kind, px_width, px_height, content_width_emu):
    """
    Decide o tamanho do logo e as larguras das colunas do cabeçalho.

    Parâmetros
    ----------
    spec : LogoSpec
        Logo normalizado (ver normalize_logo_spec).
    kind : str
        "png" ou "svg" (ver render.logo.read_logo_size); só PNG tem aviso de
        resolução, pois SVG é vetorial.
    px_width, px_height : int
        Tamanho do arquivo em pixels (SVG: pela viewBox/width/height).
    content_width_emu : int
        Largura útil da página (ver layout.page.content_width).

    Retorna
    -------
    LogoHeader

    Notas
    -----
    Passos:

    1. o logo é encaixado na caixa máxima de ``spec`` (box_emu), mantendo a
       proporção;
    2. se ficar mais largo do que o cabeçalho comporta ao lado do DOI e do
       título (max_logo_width_emu), é reduzido de novo, com aviso;
    3. PNG que, no tamanho final, fica abaixo de MIN_PNG_DPI gera aviso
       (sai borrado na impressão), mas é usado assim mesmo.

    Os avisos vão para o logger deste módulo.
    """
    doi_width = title_doi_columns(content_width_emu)[1]
    max_w, max_h = box_emu(spec, content_width_emu)
    logo_w, logo_h = fit_logo_emu(px_width, px_height, max_w, max_h)
    limit = max_logo_width_emu(spec, content_width_emu, doi_width, LOGO_GAP)
    if logo_w > limit:
        logo_w, logo_h = fit_logo_emu(px_width, px_height, limit, max_h)
        logger.warning(
            "logo reduzido para %.1f mm de largura para caber no cabeçalho: %s",
            logo_w / EMU_PER_MM,
            spec.path,
        )
    if kind == "png" and effective_dpi(px_width, logo_w) < MIN_PNG_DPI:
        logger.warning(
            "logo PNG com %.0f dpi no tamanho impresso (mínimo recomendado %d): %s",
            effective_dpi(px_width, logo_w),
            MIN_PNG_DPI,
            spec.path,
        )
    return LogoHeader(
        logo_w, logo_h, _header_columns(spec, logo_w, content_width_emu, doi_width)
    )


def _header_columns(spec, logo_width, content_width_emu, doi_width):
    """Larguras das colunas do cabeçalho por posição (ver LogoHeader.columns)."""
    width = int(content_width_emu)
    # a coluna do logo inclui o espaço que o separa do texto ao lado
    logo_col = logo_width + LOGO_GAP
    if spec.position == "full_width":
        return (width - doi_width, doi_width) if spec.show_title else ()
    if spec.position == "left":
        if spec.show_title:
            return (logo_col, width - logo_col - doi_width, doi_width)
        return (width - doi_width, doi_width)
    return (width - logo_col, logo_col)
