"""
Diagramação: decide **onde** e **em que tamanho** cada coisa entra na página,
sem escrever o DOCX (nenhum módulo daqui usa python-docx).

Fica entre ``extract`` (o que o artigo diz) e ``render`` (como se escreve o
DOCX). Entrada: os blocos (dicts) da extração e a configuração de página
(``config.page.load_page``). Saída: as mesmas estruturas com as decisões
anotadas, em EMU, prontas para o render só aplicar.

Módulos
-------
page
    Geometria da página: largura útil, largura de coluna, altura útil e o
    encaixe de uma imagem nelas.
placement
    Tabelas e figuras: coluna do corpo ou largura toda, largura das
    colunas das tabelas e tamanho final das figuras (``place``).
logo
    Cabeçalho da 1ª página: normalização da configuração do logo, tamanho
    do logo e larguras das colunas de logo, título e DOI.

O que fica no render, de propósito
----------------------------------
- abrir/fechar a seção de coluna única e decidir se uma tabela flutua:
  dependem do estado do documento em construção (``render.document.State``),
  não do bloco;
- ler o tamanho em pixels do arquivo do logo (``render.logo``), que exige
  abrir PNG/SVG; o layout recebe só os números;
- a largura de imagens inline (runs, não blocos): ``place`` só percorre
  blocos, então o render chama ``layout.page.fit_width`` na hora de escrever.
"""
