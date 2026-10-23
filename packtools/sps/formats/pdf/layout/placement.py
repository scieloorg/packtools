"""
Diagramação de tabelas e figuras: em que largura cada uma entra e com que
medidas finais.

Duas decisões, nesta ordem:

1. **Layout**: se o elemento cabe numa coluna do corpo (DOUBLE_COLUMN) ou
   se ocupa a largura toda da página (SINGLE_COLUMN). ``table_layout`` e
   ``figure_layout``.
2. **Medidas**, já sabendo o layout: largura da tabela e de cada coluna
   dela (``column_widths``); largura e altura da figura
   (``layout.page.fit_image``).

``place`` aplica as duas e **só anota** os resultados nos blocos (em EMU).
O render apenas os aplica: não decide largura nenhuma e não troca de
layout por conta própria. A troca de seção (abrir/fechar a seção de
coluna única) continua no render, porque depende do estado do documento
em construção (``render.document.State``), não do bloco.

Contrato com o render (chaves que ``place`` acrescenta):

    tabela  {"layout", "width", "column_widths"}
    figura  {"layout", "width", "height"}   (height None = imagem ilegível)

Nenhuma função aqui usa python-docx: são testáveis só com dicts.
"""

from packtools.sps.formats.pdf.config.page import DOUBLE_COLUMN, SINGLE_COLUMN
from packtools.sps.formats.pdf.extract.table import max_cell_length
from packtools.sps.formats.pdf.layout.page import (
    EMU_PER_POINT,
    block_width,
    column_width,
    content_height,
    fit_image,
)

# Herdado do old_pdf: acima disso a tabela não cabe numa coluna
MAX_COLUMNS_IN_ONE_COLUMN = 4
# Herdado do old_pdf: uma única célula tão longa estoura a coluna mesmo com
# poucas colunas (o número de colunas sozinho não detecta esse caso)
MAX_CELL_LENGTH_IN_ONE_COLUMN = 400
# Herdado do old_pdf: figura mais larga que coluna * fator vai para a largura
# toda; o fator > 1 tolera imagem um pouco maior que a coluna (ela é reduzida)
FIGURE_WIDTH_FACTOR = 1.1

# Herdado do old_pdf (_calculate_column_widths): peso de cada coluna = maior
# texto estimado x 6pt, limitado a [50, 200]pt, para uma coluna curta (números)
# não ficar estreita demais nem uma coluna de texto longo engolir a tabela.
POINTS_PER_CHARACTER = 6
MIN_COLUMN_WEIGHT = 50
MAX_COLUMN_WEIGHT = 200
# Herdado do old_pdf: coluna sem conteúdo fica com a largura mínima
# (0.381cm, em EMU).
EMPTY_COLUMN_WIDTH = 137160


# -----------------
# 1. Layout: coluna do corpo ou largura toda
# -----------------


def table_layout(panels):
    """
    Largura toda se tiver colunas demais ou uma célula longa demais para uma coluna do corpo.

    panels: os blocos de tabela de um mesmo <table-wrap> (um por <table>),
    decididos juntos para os painéis não ficarem em larguras diferentes.
    """
    ncols = max((p["ncols"] for p in panels), default=0)
    longest = max((max_cell_length(p) for p in panels), default=0)
    if ncols > MAX_COLUMNS_IN_ONE_COLUMN or longest > MAX_CELL_LENGTH_IN_ONE_COLUMN:
        return SINGLE_COLUMN
    return DOUBLE_COLUMN


def figure_layout(block, page, assets, factor=FIGURE_WIDTH_FACTOR):
    """Pela largura natural da imagem (DPI do arquivo); imagem ilegível vai para a largura toda."""
    # Herdado do old_pdf: sem conseguir ler a imagem, a largura toda é a
    # escolha segura (nunca estoura a coluna).
    width = assets.natural_width(block["href"])
    if width is None or width >= factor * column_width(page):
        return SINGLE_COLUMN
    return DOUBLE_COLUMN


# -----------------
# 2. Medidas das tabelas
# -----------------


def _text_width(text):
    """
    Estima a largura de um texto em "caracteres médios".

    Parâmetros
    ----------
    text : str
        Texto de uma linha da célula.

    Retorna
    -------
    float
        Soma das larguras relativas: maiúscula 1.2, "i j l" 0.5, "m w M W"
        1.5, demais 1.0 (herdado do old_pdf, _estimate_text_width).
    """
    width = 0.0
    for char in " ".join(text.split()):
        if char in "mwMW":
            width += 1.5
        elif char in "ijl":
            width += 0.5
        elif char.isupper():
            width += 1.2
        else:
            width += 1.0
    return width


def _cell_measures(runs, image_width=None):
    """
    Mede o conteúdo de uma célula em "caracteres médios" (ver ``_text_width``).

    Parâmetros
    ----------
    runs : list of dict
        Runs da célula (ver extract.runs).
    image_width : callable, opcional
        href -> largura natural da imagem em EMU, ou None se ilegível
        (ver ``Assets.natural_width``).

    Retorna
    -------
    tuple of (float, float)
        ``(linha, palavra)``: a linha mais longa e a maior palavra. Fórmula
        e imagem contam como uma palavra que não quebra: a fórmula pelo
        texto do OMML, a imagem pela largura natural. Imagem sem largura
        conta pelo texto que o render escreve no lugar dela (alt ou href).
    """
    lines = [["", 0.0]]  # [texto, largura das fórmulas] de cada linha
    word = 0.0
    for run in runs:
        if run.get("break"):
            lines.append(["", 0.0])
        elif "omml" in run or "image" in run:
            width = _atom_width(run, image_width)
            lines[-1][1] += width
            word = max(word, width)
        elif "text" in run:
            lines[-1][0] += run["text"]
    line = max(_text_width(text) + atoms for text, atoms in lines)
    words = [_text_width(w) for text, _ in lines for w in text.split()]
    return line, max(words + [word])


def _atom_width(run, image_width):
    """Largura (caracteres médios) de uma fórmula ou imagem, que não quebra (ver ``_cell_measures``)."""
    if "omml" in run:
        return _text_width("".join(t.strip() for t in run["omml"].itertext()))
    natural = image_width(run["image"]) if image_width else None
    if natural is None:
        return _text_width(run.get("alt") or run["image"])
    return natural / EMU_PER_POINT / POINTS_PER_CHARACTER


def column_weights(grid, image_width=None):
    """
    Calcula o peso relativo de cada coluna pelo conteúdo que ela tem.

    Parâmetros
    ----------
    grid : dict
        Bloco de tabela (ver extract.table.grid e extract.table_wrap).
    image_width : callable, opcional
        href -> largura natural da imagem em EMU (ver ``_cell_measures``).

    Retorna
    -------
    tuple of (list, list)
        ``(weights, word_widths)``, um valor por coluna, em pt.
        weights: maior linha x 6pt, limitado a [MIN, MAX]_COLUMN_WEIGHT
        (cálculo herdado do old_pdf). word_widths: maior palavra x 6pt, o
        mínimo para a coluna não quebrar palavras, usado por
        ``column_widths`` quando a tabela não cabe com os pesos. None nas
        duas listas = coluna sem conteúdo, que fica com a largura mínima.

    Notas
    -----
    O texto de uma célula mesclada (ex. um cabeçalho "Brasil" sobre as
    colunas "n" e "%") é dividido entre as colunas que ela ocupa; no old_pdf
    ele alargava só a primeira. Para célula com quebra de linha, vale a
    linha mais longa. Fórmula e imagem contam (ver ``_cell_measures``): uma
    coluna só com fórmulas ou imagens não é vazia.
    """
    longest = [None] * grid["ncols"]
    longest_word = [None] * grid["ncols"]
    for cell in grid["cells"]:
        size, word = _cell_measures(cell["runs"], image_width)
        if not size:
            continue
        cols = range(cell["col"], min(cell["col"] + cell["colspan"], grid["ncols"]))
        # célula mesclada divide sua largura entre as colunas que ocupa
        for col in cols:
            longest[col] = max(longest[col] or 0, size / len(cols))
            longest_word[col] = max(longest_word[col] or 0, word / len(cols))
    weights = [
        (
            None
            if size is None
            else min(
                MAX_COLUMN_WEIGHT, max(MIN_COLUMN_WEIGHT, size * POINTS_PER_CHARACTER)
            )
        )
        for size in longest
    ]
    word_widths = [
        None if size is None else max(1, size) * POINTS_PER_CHARACTER
        for size in longest_word
    ]
    return weights, word_widths


def column_widths(weights, word_widths, width):
    """
    Converte os pesos das colunas em larguras (EMU) que somam a largura da tabela.

    Parâmetros
    ----------
    weights, word_widths : list
        Saída de ``column_weights`` (pt; None = coluna vazia).
    width : int
        Largura da tabela, em EMU (ver ``layout.page.block_width``).

    Retorna
    -------
    list of int
        Uma largura por coluna: coluna vazia com EMPTY_COLUMN_WIDTH e as
        demais proporcionais ao peso, repartindo o que sobra. Se todas as
        colunas forem vazias, ou as colunas vazias sozinhas já ocuparem a
        tabela, larguras iguais.

    Notas
    -----
    Quando os pesos (que têm mínimo de 50pt por coluna) somam mais que a
    largura disponível, eles igualariam colunas curtas e longas, e a coluna
    de rótulos quebraria palavras ("Tot/al"). Nesse caso a proporção passa
    a ser a da maior palavra de cada coluna (``word_widths``).
    """
    ncols = len(weights)
    if not ncols:
        return []
    filled = [w for w in weights if w is not None]
    remaining = int(width) - EMPTY_COLUMN_WIDTH * (ncols - len(filled))
    if not filled or remaining <= 0:
        return [int(width) // ncols] * ncols
    if word_widths and sum(filled) * EMU_PER_POINT > remaining:
        weights = word_widths
        filled = [w for w in weights if w is not None]
    total = sum(filled)
    return [
        EMPTY_COLUMN_WIDTH if w is None else int(remaining * w / total)
        for w in weights
    ]


# -----------------
# Aplicação nos blocos
# -----------------


def place(blocks, page, assets, overrides=None, force=None):
    """
    Decide o layout e as medidas finais de tabelas e figuras e os anota nos blocos.

    Parâmetros
    ----------
    blocks : list of dict
        Blocos de uma parte do artigo (ver extract.flow); alterados no lugar.
    page : dict
        Atributos de página (ver config.page.load_page).
    assets : assets.Assets
        Para ler o tamanho natural das imagens.
    overrides : dict, opcional
        ``{id do table-wrap/fig: SINGLE_COLUMN | DOUBLE_COLUMN}``: força o
        layout de um elemento; valor inválido é ignorado (vale o calculado).
    force : str, opcional
        Um layout para todos os elementos (capa e anexos, que já são de
        coluna única).

    Retorna
    -------
    list of dict
        Os próprios ``blocks``, com as chaves do contrato descrito no
        docstring do módulo.

    Notas
    -----
    Os painéis de um mesmo <table-wrap> (bloco com panel 0 e os seguintes
    com panel > 0) recebem o mesmo layout, decidido com o painel 0; as
    larguras das colunas, porém, são de cada painel, pois cada <table> tem
    a sua grade.
    """
    overrides = overrides or {}
    measured = set()  # id() dos painéis já medidos junto com o seu painel 0
    for index, block in enumerate(blocks):
        if block["type"] not in ("table", "figure") or id(block) in measured:
            continue
        layout = force or overrides.get(block.get("id"))
        if layout not in (SINGLE_COLUMN, DOUBLE_COLUMN):
            layout = (
                table_layout(_panels(blocks, index))
                if block["type"] == "table"
                else figure_layout(block, page, assets)
            )
        if block["type"] == "table":
            for panel in _panels(blocks, index):
                _measure_table(panel, layout, page, assets)
                measured.add(id(panel))
        else:
            _measure_figure(block, layout, page, assets)
    return blocks


def _measure_table(block, layout, page, assets):
    """Anota layout, largura da tabela e larguras das colunas (EMU) num painel."""
    block["layout"] = layout
    block["width"] = block_width(page, layout)
    image_width = assets.natural_width if assets else None
    block["column_widths"] = column_widths(
        *column_weights(block, image_width), block["width"]
    )


def _measure_figure(block, layout, page, assets):
    """
    Anota layout, largura e altura (EMU) da figura: o tamanho natural,
    reduzido para caber na largura do layout e na altura útil da página
    (ver layout.page.fit_image; height None = imagem ilegível).
    """
    block["layout"] = layout
    block["width"], block["height"] = fit_image(
        assets.natural_size(block["href"]),
        block_width(page, layout),
        content_height(page),
    )


def _panels(blocks, index):
    """O bloco de tabela em ``index`` (painel 0) e os painéis seguintes do mesmo <table-wrap>."""
    panels = [blocks[index]]
    for block in blocks[index + 1:]:
        if block["type"] != "table" or not block["panel"]:
            break
        panels.append(block)
    return panels
