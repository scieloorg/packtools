# Arquitetura do gerador de PDF (`packtools/sps/formats/pdf/`)

Este documento fixa a organização dos módulos que extraem dados do XML SPS
para gerar o DOCX/PDF, as regras de dependência entre eles e o protocolo
usado para garantir que uma reorganização não muda a saída.

## Fluxo

```text
XML SPS ──► extract/ ──► estrutura intermediária ──► pipeline/docx.py ──► renderer/docx/ ──► DOCX ──► LibreOffice ──► PDF
                │                                         (orquestração)       (emissão)
                ├─► layout/   (decisões de layout sobre dados já extraídos)
                └─► ooxml/    (MathML -> OMML)
```

## Árvore de módulos

```text
packtools/sps/formats/pdf/
├── extract/                       # XML -> estrutura intermediária voltada para a renderização atual
│   ├── metadata.py                # lang, article-type, title, doi, category, contribs,
│   │                              # abstract/trans-abstract, keywords, footer
│   ├── citation.py                # "como citar": nota editorial ou citação gerada via CSL
│   ├── body.py                    # sec/p/list + montagem dos parágrafos em segmentos
│   ├── formula_segments.py        # MathML -> segmento {'type': 'formula'} com OMML (disp/inline)
│   ├── tables.py                  # table-wrap -> dados da tabela + estrutura pronta para render
│   ├── figures.py                 # fig / fig-group / disp-formula só-imagem
│   ├── references.py              # ref-list / mixed-citation
│   ├── acknowledgments.py         # ack
│   └── supplementary_material.py  # app-group + supplementary-material
├── layout/
│   └── table_layout.py            # 1 ou 2 colunas e larguras, a partir dos dados JÁ EXTRAÍDOS
├── ooxml/
│   └── formula.py                 # MathML -> OMML, namespaces OOXML, match_paragraph_font
├── pipeline/
│   ├── docx.py                    # orquestração + funções de emissão DOCX (separação futura)
│   ├── xml.py                     # módulo de compatibilidade (depreciado)
│   └── formula.py                 # módulo de compatibilidade (depreciado)
├── renderer/docx/                 # emissão DOCX
│   └── style.py                   # única fonte dos nomes de estilo 'SCL *'
└── utils/                         # xml_utils (segmentos/normalização), file_utils
```

`extract/` **não** é independente do renderer: `formula_segments.py` produz
segmentos que já contêm OMML. O contrato é "XML → estrutura intermediária
voltada para a renderização atual"; a regra é não importar `python-docx`, não
evitar conceitos do DOCX. Manter MathML na estrutura e converter só no
renderer é uma mudança maior, fora do escopo.

## Regras de dependência

| módulo      | pode importar                                   | não pode importar                        |
|-------------|--------------------------------------------------|------------------------------------------|
| `extract/`  | `extract/`, `layout/`, `ooxml/`, `utils/`, `enum` | `python-docx`, `pipeline/`, `renderer/`  |
| `layout/`   | `enum`                                           | `extract/`, `pipeline/`, `renderer/`     |
| `ooxml/`    | `lxml`, `mathml2omml`                            | `extract/`, `pipeline/`, `renderer/`     |
| `renderer/` | `ooxml/`, `utils/`, `enum`, `python-docx`        | `pipeline/`, `extract/`                  |
| `pipeline/` | tudo acima                                       | —                                        |

- Cada constante fica no módulo dono do assunto; nomes de estilo `SCL *` só
  em `renderer/docx/style.py`.
- Cada arquivo de teste espelha o módulo
  (`extract/tables.py` → `tests/sps/formats/pdf/extract/test_tables.py`).
- As regras são verificadas por
  `tests/sps/formats/pdf/test_module_dependencies.py`.

## Tabela e layout

```text
XML (table-wrap)
   │  extract/tables.py::read_table_wrap — lê o XML (label, title, foot e,
   │  para cada <table>: headers, rows, spans e o texto de todas as células)
   ▼
dados do table-wrap inteiro (todas as <table>)
   │  layout/table_layout.py — funções só sobre esses dados:
   │  contagem de colunas, comprimento das células, decisão de layout, larguras
   ▼
decisão de layout (uma por table-wrap) + larguras (uma lista por <table>)
   │  extract/tables.py::extract_table_data — junta as duas etapas
   ▼
list[dict] no contrato atual  →  body.py / supplementary_material.py / docx.py
```

- `extract/tables.py` pode depender de `layout/table_layout.py`; o contrário
  não. `layout/` recebe os dados da tabela, **nunca o XML**, o que impede um
  ciclo `layout ↔ extract`.
- `determine_table_layout` recebe a estrutura do `table-wrap` inteiro (e não
  mais o elemento XML): um `table-wrap` com vários painéis tem uma única
  decisão de 1 ou 2 colunas.
- O número de colunas usado pela decisão é a largura da grade já montada pela
  extração (a mesma contagem com `colspan` de antes). O comprimento da maior
  célula considera o texto de todo `<td>`/`<th>` da `<table>` (inclusive
  `<tfoot>`), que a extração entrega em `cell_texts` justamente para manter a
  decisão igual à anterior.
- `docx.py` e `body.py` não decidem layout; só consomem a estrutura pronta.

## Decisões da Fase 0

### Compatibilidade de imports de `pipeline/xml.py` — opção (a)

`pipeline/xml.py` fica como **módulo de compatibilidade**: cada função movida
é resolvida por `__getattr__` a partir de um mapa `nome → novo módulo` e emite
`DeprecationWarning` ao ser acessada — o mesmo padrão de
`sps/models/formula.py` e `sps/models/supplementary_material.py`. O mapa é
atualizado a cada fase. Nenhum módulo de produção importa `pipeline.xml`; o
arquivo será removido quando a depreciação terminar (issue própria).

`pipeline/formula.py` segue o mesmo padrão, apontando para `ooxml/formula.py`.

`pipeline/supplementary_material.py` (#1384) ainda não saiu em nenhuma versão
publicada, então é movido para `extract/supplementary_material.py` **sem**
módulo de compatibilidade.

Funções privadas (`_nome`) não são reexportadas; testes e módulos internos
importam do novo lugar.

### Caminhos de `citation` e `supplementary_material`

- `packtools.sps.formats.pdf.extract.citation` (alinhar com o #1382).
- `packtools.sps.formats.pdf.extract.supplementary_material`.

### Reuso de `packtools/sps/models`

Avaliado e **não adotado nesta épica**. `sps/models` e `formats/sps_xml`
devolvem texto ou dicionários pensados para validação e HTML; o pipeline do
PDF precisa de segmentos com marcação inline (`italic`/`bold`/`sup`/`sub`),
OMML e marcadores próprios (`[^]` nos autores/afiliações). Trocar a fonte dos
dados muda a saída e não é uma mudança de lugar. Fica registrado como
possibilidade para issues futuras, campo a campo (ex.: contribs, keywords).

### Ordem de execução

A ordem da issue foi ajustada para que nenhum commit intermediário quebre as
regras de dependência:

1. Fase 1 — `metadata`, `figures`, `references`, `acknowledgments`; remove
   `get_table_column_info`.
2. Fase 2 — `citation` (inclui a escolha entre nota editorial e citação
   gerada, antes em `docx.py`).
3. Fase 5 — `ooxml/formula.py` (antes da Fase 3: `extract/formula_segments.py`
   não pode importar `pipeline/formula.py`).
4. Fase 4 — `extract/tables.py` e `layout/table_layout.py` (antes da Fase 3:
   `extract/body.py` não pode importar `extract_table_data` de `pipeline/`).
5. Fase 3 — `body`, `formula_segments`, `supplementary_material`.
6. Fase 6 — constantes (`SCL *`, números de layout), teste de dependências,
   testes restantes.

## Protocolo de comparação da saída

Uma fase de reorganização deve produzir **saída equivalente**. Como toda a
variação entre XML e PDF passa pelo DOCX, o critério primário é o DOCX:

1. **Corpus:** todos os XML em `tests/fixtures/**/*.xml` (59 arquivos hoje,
   incluindo `tests/fixtures/pdf/a1..a4.xml`), com
   `tests/fixtures/pdf/layout.docx` como layout base.
2. **Comparação:** gerar o DOCX de cada XML antes e depois da mudança e
   comparar, parte a parte do pacote ZIP, o conteúdo **byte a byte**, exceto
   `docProps/core.xml` (datas de criação/modificação). Limiar aceito:
   **nenhuma diferença**. DOCX idêntico implica PDF idêntico para a mesma
   versão do LibreOffice.
3. **Quando o DOCX mudar de propósito** (fora desta épica): converter com o
   LibreOffice e comparar número de páginas, texto extraído (`pdftotext
   -layout`) e diff visual por página (`pdftoppm -r 100` + `compare -metric
   AE`), com limiar de 0,1% dos pixels por página; igualdade byte a byte do PDF
   não é exigida, porque o LibreOffice grava metadados variáveis.
4. **Testes:** `python -m unittest discover -s tests/sps/formats/pdf -t .`
   verde.
