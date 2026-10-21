"""XML SPS -> DOCX: extração (extract), decisões de página (layout) e escrita (render)."""

from packtools.sps.formats.pdf.config import page as page_config
from packtools.sps.formats.pdf.assets import Assets
from packtools.sps.formats.pdf.extract.article import extract_article
from packtools.sps.formats.pdf.extract.languages import document_for, languages
from packtools.sps.formats.pdf.layout import logo as logo_layout
from packtools.sps.formats.pdf.layout.placement import place
from packtools.sps.formats.pdf.render.document import render


def pipeline_docx(xml_tree, data, lang=None):
    """
    Gera o python-docx Document do artigo no idioma ``lang``.

    lang: idioma do texto (ver extract.languages); None = idioma principal.
    Uma tradução usa o front do artigo com o front-stub da tradução, o body
    da tradução e o back do artigo com o back da tradução.

    data (todas as chaves opcionais):
        base_layout: .docx com os estilos SCL
        assets_dir: pasta das imagens referenciadas no XML
        page_layout: JSON de página (padrão: default_layout.json)
        journal_logo: caminho do PNG/SVG ou dict (ver layout.logo.normalize_logo_spec)
        table_layout_overrides: {id do table-wrap/fig: 'single-column-layout' | 'double-column-layout'}
        citation_style: estilo da citação do rodapé (padrão: 'vancouver')
    """
    page = page_config.load_page(data.get("page_layout"))
    assets = Assets(data.get("assets_dir"))

    article = extract_article(
        document_for(xml_tree, lang),
        citation_style=data.get("citation_style", "vancouver"),
    )
    place(article["main"], page, assets, overrides=data.get("table_layout_overrides"))
    place(article["annex"], page, assets, force=page_config.SINGLE_COLUMN)
    place(article["front"], page, assets, force=page_config.SINGLE_COLUMN)

    return render(
        article,
        page,
        assets,
        base_layout=data.get("base_layout"),
        logo_spec=logo_layout.normalize_logo_spec(data.get("journal_logo")),
    )


def pipeline_docx_by_language(xml_tree, data):
    """
    Gera um Document por idioma do texto, como o htmlgenerator.

    Parâmetros
    ----------
    xml_tree : lxml.etree._ElementTree or lxml.etree._Element
        Artigo SPS.
    data : dict
        Mesmas opções de ``pipeline_docx``.

    Retorna
    -------
    generator of (str, docx.document.Document)
        ``(idioma, documento)``, o idioma principal primeiro.
    """
    # sem xml:lang no <article>, gera só o documento principal
    for lang in languages(xml_tree) or [None]:
        yield lang, pipeline_docx(xml_tree, data, lang)
