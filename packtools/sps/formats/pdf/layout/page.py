"""
Geometria da página: larguras e alturas úteis, em EMU, e o encaixe de uma
imagem nelas.

Fica em ``layout`` (e não em ``config``) porque são decisões de
diagramação derivadas da configuração de página, não a configuração em si:
``config.page.load_page`` lê o JSON; este módulo responde "quanto espaço há".
Não usa python-docx: as medidas de ``page`` já chegam como inteiros (EMU)
de ``config.page.load_page`` e tudo aqui é aritmética.

Unidades
--------
EMU (English Metric Unit) é a unidade do DOCX: 914400 por polegada,
12700 por ponto, 635 por twip (1/20 de ponto). ``page["column_spacing"]``
vem em twips (é o valor que vai para ``w:cols/@w:space``); o resto, em EMU.
"""

from packtools.sps.formats.pdf.config.page import SINGLE_COLUMN

EMU_PER_POINT = 12700
EMU_PER_TWIP = 635

# Herdado do old_pdf: folga (56.7pt = 2cm) descontada da altura útil para
# que a legenda caiba na mesma página que a figura mais alta possível.
CAPTION_ALLOWANCE = int(56.7 * EMU_PER_POINT)


def content_width(page):
    """Largura útil (EMU): página menos as margens esquerda e direita."""
    return int(page["page_width"] - page["left_margin"] - page["right_margin"])


def column_width(page):
    """
    Largura (EMU) de uma coluna do corpo: a largura útil menos os
    espaçamentos entre colunas, dividida pelo número de colunas. Com uma
    coluna só, é a própria largura útil.
    """
    count = page["column_count"]
    spacing = page["column_spacing"] * EMU_PER_TWIP
    return int((content_width(page) - (count - 1) * spacing) / count)


def content_height(page):
    """Altura útil (EMU) para uma figura: página menos margens e a folga da legenda."""
    return int(
        page["page_height"]
        - page["top_margin"]
        - page["bottom_margin"]
        - CAPTION_ALLOWANCE
    )


def block_width(page, layout):
    """
    Largura (EMU) disponível para um bloco conforme o layout decidido em
    ``placement``: SINGLE_COLUMN ocupa a largura útil toda; qualquer outro
    valor (DOUBLE_COLUMN ou ausente) fica limitado a uma coluna do corpo.
    """
    return content_width(page) if layout == SINGLE_COLUMN else column_width(page)


def split_width(total, left_ratio):
    """
    Divide ``total`` (EMU) em duas larguras, [esquerda, direita], na
    proporção ``left_ratio``. A direita recebe o resto, para a soma ser
    exatamente ``total`` mesmo com o arredondamento.
    """
    left = int(total * left_ratio)
    return [left, int(total) - left]


def fit_width(natural, ceiling):
    """
    Largura (EMU) de uma imagem: a natural (ver ``Assets.natural_size``),
    limitada a ``ceiling``. Sem largura natural (imagem ilegível), usa o
    próprio teto: é a escolha que nunca estoura o espaço disponível.
    """
    return min(natural or ceiling, ceiling)


def fit_image(natural_size, max_width, max_height):
    """
    Tamanho (largura, altura) em EMU de uma imagem que não passa de
    ``max_width`` nem de ``max_height``, mantendo a proporção.

    Parâmetros
    ----------
    natural_size : tuple of (int, int) or None
        Tamanho natural da imagem (ver ``Assets.natural_size``).
    max_width, max_height : int
        Caixa disponível, em EMU.

    Retorna
    -------
    tuple of (int, int or None)
        Primeiro a largura é limitada a ``max_width`` (sem nunca ampliar a
        imagem); se a altura resultante passar de ``max_height``, as duas
        são reduzidas na mesma proporção. Sem tamanho natural, devolve
        ``(max_width, None)``: o render passa só a largura e o python-docx
        calcula a altura pela proporção que ele mesmo lê do arquivo, sem o
        limite de altura (que exige conhecer a proporção aqui).
    """
    if not natural_size or not all(natural_size):
        return max_width, None
    natural_w, natural_h = natural_size
    width = min(natural_w, max_width)
    height = natural_h * width / natural_w
    if height > max_height:
        width, height = width * max_height / height, max_height
    return int(width), int(height)
