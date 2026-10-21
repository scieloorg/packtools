"""Utilitários comuns dos testes do gerador de PDF (formats/pdf)."""

from pathlib import Path

from lxml import etree

from packtools.sps.formats.pdf.extract.article import extract_article
from packtools.sps.formats.pdf.extract.context import context
from packtools.sps.formats.pdf.extract.flow import flow
from packtools.sps.formats.pdf.extract.languages import document_for
from packtools.sps.formats.pdf.extract.runs import runs_text
from packtools.sps.formats.pdf.pipeline import pipeline_docx

FIXTURES_DIR = Path(__file__).resolve().parents[3] / 'fixtures' / 'pdf'
# layout base com os estilos SCL e pasta das imagens dos fixtures
DATA = {'base_layout': str(FIXTURES_DIR / 'layout.docx'), 'assets_dir': str(FIXTURES_DIR)}
NS = 'xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML"'


def xml(text):
    """Elemento lxml de um trecho XML."""
    return etree.fromstring(text)


def article_xml(front='', body='', back='', lang='pt', extra=''):
    """
    Artigo SPS mínimo.

    front: conteúdo do <article-meta>; body/back: conteúdo de <body>/<back>
    (omitidos se vazios); extra: elementos depois do <back> (sub-articles).
    """
    return xml(
        f'<article {NS} xml:lang="{lang}" article-type="research-article">'
        f'<front><journal-meta><journal-title-group><journal-title>Revista</journal-title>'
        f'</journal-title-group></journal-meta><article-meta>{front}</article-meta></front>'
        + (f'<body>{body}</body>' if body else '')
        + (f'<back>{back}</back>' if back else '')
        + extra + '</article>'
    )


def extract(node, **ctx):
    """Blocos de um fragmento XML, no contexto inicial (ou com as chaves dadas)."""
    return flow(node, context(**ctx))


def article(root, lang=None):
    """Artigo extraído: {'meta', 'front', 'main', 'annex'}."""
    return extract_article(document_for(root, lang))


def texts(blocks):
    """Texto de cada bloco com runs."""
    return [runs_text(b['runs']) for b in blocks if 'runs' in b]


def summary(blocks):
    """(papel ou tipo, texto) de cada bloco com runs: comparação plana nos testes."""
    return [(b.get('role', b['type']), runs_text(b['runs'])) for b in blocks if 'runs' in b]


def docx(root, **data):
    """python-docx Document gerado pelo pipeline, com o layout base dos fixtures."""
    return pipeline_docx(root, {**DATA, **data})


def paragraphs(document):
    """
    (estilo, texto) de cada parágrafo do corpo do documento.

    O parágrafo vazio que carrega cada quebra de seção não tem estilo (None).
    """
    return [(p.style.name if p.style is not None else None, p.text) for p in document.paragraphs]
