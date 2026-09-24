import copy

from lxml import etree

from packtools.sps.formats.pdf.pipeline.xml import (
    _plain_text_segment,
    extract_figure_data,
    extract_section_data,
)
from packtools.sps.formats.pdf.utils import xml_utils

_DEFAULT_APP_GROUP_TITLE = 'Appendix'
_DEFAULT_SUPPLEMENTARY_MATERIAL_TITLE = 'Supplementary Material'

# sub-article de tradução repete apêndice e material suplementar em outro idioma
_NOT_IN_TRANSLATION = 'not(ancestor::sub-article[@article-type="translation"])'

_SUPPLEMENTARY_SEC_XPATH = f'.//sec[.//supplementary-material and not(sec) and {_NOT_IN_TRANSLATION}]'


def extract_data(xml_tree):
    """
    Extracts appendix (<app-group>) and supplementary material
    (<supplementary-material>) data from an XML tree.

    SPS 1.10 treats these as distinct concepts ("<app-group> e <app> não
    comportam <supplementary-material>"), so each gets its own heading,
    instead of a single title shared between both.

    Each <app> is read like a body <sec> (extract_section_data):
    paragraphs, lists, formulas, tables and figures, plus its nested <sec>
    as subsections. Headings:
        - <app-group> with its own <title>: that title, then each <app>
          with its own <title>/<label> as a subsection (skipped when it
          repeats the group title, e.g. "Appendix"/"Appendix");
        - no group title, more than one <app>, at least one titled: one
          heading per <app> (app/title -> app/label -> "Appendix N"), so a
          single shared title doesn't mislabel every app after the first;
        - otherwise: a single heading (the lone <app>'s own title, or the
          default), the apps' content below it.

    The supplementary-material heading comes from the <sec> that holds the
    <supplementary-material> (sec/title -> sec/label -> default); its
    loose <p> (availability/DOI statements) and one line per item follow,
    in document order.

    <app-group>/<supplementary-material> inside a translation <sub-article>
    are skipped: they repeat the main article's in another language.

    Args:
        xml_tree (ElementTree): The XML tree to extract the data from.

    Returns:
        list[dict]: Sections in rendering order, each with the keys of a
        body section ('title', 'level', 'paragraphs', 'tables', 'figures').
    """
    sections = _extract_appendix_sections(xml_tree)
    supplementary_section = _extract_supplementary_section(xml_tree)
    if supplementary_section is not None:
        sections.append(supplementary_section)
    return sections


def extract_supplementary_items(xml_tree):
    """Um dict por <supplementary-material> fora de sub-article de tradução (ver _extract_item)."""
    return [
        _extract_item(supplementary_material)
        for supplementary_material in xml_tree.xpath(f'.//supplementary-material[{_NOT_IN_TRANSLATION}]')
    ]


def format_item(element):
    """Monta 'Rótulo (Legenda): arquivo (tipo/subtipo). Descrição. Notas' a partir de um item extraído de <supplementary-material>, sem partes ausentes."""
    text = element['label'] or _DEFAULT_SUPPLEMENTARY_MATERIAL_TITLE
    if element.get('caption'):
        text = f"{text} ({element['caption']})"
    if element['filename']:
        mimetype, mime_subtype = element['mimetype'], element['mime_subtype']
        media_type = f"{mimetype}/{mime_subtype}" if mimetype and mime_subtype else (mimetype or mime_subtype)
        suffix = f" ({media_type})" if media_type else ''
        text = f"{text}: {element['filename']}{suffix}"
    if element.get('description'):
        text = f"{text}. {element['description']}"
    if element.get('notes'):
        text = f"{text}. {element['notes']}"
    return text


# -----------------
# Private helpers
# -----------------

def _section(title, level):
    return {'title': title, 'level': level, 'paragraphs': [], 'tables': [], 'figures': []}


def _has_content(section):
    return bool(section['paragraphs'] or section['tables'] or section['figures'])


def _node_text(node):
    return ' '.join(''.join(node.itertext()).split()) if node is not None else ''


def _app_own_title(app):
    """Texto de <app>/<title> ou <app>/<label>, o que vier primeiro e não vazio - vazio quando o <app> não tem nenhum dos dois."""
    for tag in ('title', 'label'):
        text = _node_text(app.find(tag))
        if text:
            return text
    return ''


def _extract_appendix_sections(xml_tree):
    sections = []
    seen_fig_keys = set()
    for app_group in xml_tree.xpath(f'.//app-group[{_NOT_IN_TRANSLATION}]'):
        apps = app_group.findall('app')
        group_title = _node_text(app_group.find('title'))
        own_titles = [_app_own_title(app) for app in apps]

        if group_title:
            sections.append(_app_group_direct_section(app_group, xml_tree, seen_fig_keys, group_title))
            for app, own_title in zip(apps, own_titles):
                title = own_title if own_title and own_title.casefold() != group_title.casefold() else None
                sections.extend(_app_sections(app, xml_tree, seen_fig_keys, title, 3 if title else 2))
        elif len(apps) > 1 and any(own_titles):
            direct = _app_group_direct_section(app_group, xml_tree, seen_fig_keys, _DEFAULT_APP_GROUP_TITLE)
            if _has_content(direct):
                sections.append(direct)
            for index, (app, own_title) in enumerate(zip(apps, own_titles), start=1):
                title = own_title or f'{_DEFAULT_APP_GROUP_TITLE} {index}'
                sections.extend(_app_sections(app, xml_tree, seen_fig_keys, title, 2))
        else:
            title = (own_titles[0] if len(apps) == 1 else '') or _DEFAULT_APP_GROUP_TITLE
            sections.append(_app_group_direct_section(app_group, xml_tree, seen_fig_keys, title))
            for app in apps:
                sections.extend(_app_sections(app, xml_tree, seen_fig_keys, None, 2))

    return _drop_empty_headings(_merge_untitled(sections))


def _app_group_direct_section(app_group, xml_tree, seen_fig_keys, title):
    """Conteúdo solto direto em <app-group> (fora de <app>), sob o título do grupo."""
    direct = etree.Element('app-group')
    for child in app_group:
        if child.tag not in ('app', 'title'):
            direct.append(copy.deepcopy(child))
    section = extract_section_data(direct, xml_tree, seen_fig_keys, level=2)
    section['title'] = title
    return section


def _app_sections(app, xml_tree, seen_fig_keys, title, level):
    """Seção do <app> e, em seguida, suas <sec> aninhadas, um nível abaixo por profundidade."""
    # da <sec> mais interna para fora: cada figura fica na subseção onde está,
    # e não na seção-mãe (extract_section_data busca figuras em .//fig)
    base_depth = len(app.xpath('ancestor::sec'))
    nested_sections = []
    for sec in reversed(app.xpath('.//sec')):
        depth = len(sec.xpath('ancestor::sec')) - base_depth
        nested_sections.insert(0, extract_section_data(sec, xml_tree, seen_fig_keys, level=level + 1 + depth))

    app_section = extract_section_data(app, xml_tree, seen_fig_keys, level=level)
    app_section['title'] = title
    # <app> cujo conteúdo é só um <graphic> direto, sem <fig>
    for graphic in app.findall('graphic'):
        fig = etree.Element('fig')
        fig.append(copy.deepcopy(graphic))
        app_section['figures'].append(extract_figure_data(fig))
    return [app_section] + nested_sections


def _merge_untitled(sections):
    """Junta a seção sem título (ex. <app> sem título sob o título do grupo) ao conteúdo da seção anterior."""
    merged = []
    for section in sections:
        if not section['title'] and merged:
            for key in ('paragraphs', 'tables', 'figures'):
                merged[-1][key].extend(section[key])
        else:
            merged.append(section)
    return merged


def _drop_empty_headings(sections):
    """Remove seção vazia, exceto o título seguido de subseção (ex. <app> cujo conteúdo está todo em <sec>)."""
    kept = []
    for index, section in enumerate(sections):
        following = sections[index + 1] if index + 1 < len(sections) else None
        if _has_content(section) or (following is not None and following['level'] > section['level']):
            kept.append(section)
    return kept


def _extract_supplementary_section(xml_tree):
    supplementary_secs = xml_tree.xpath(_SUPPLEMENTARY_SEC_XPATH)
    nodes = xml_tree.xpath(
        f'.//supplementary-material[{_NOT_IN_TRANSLATION}]'
        f' | {_SUPPLEMENTARY_SEC_XPATH}/p[not(.//supplementary-material)]'
    )
    if not nodes:
        return None

    title = ''
    for sec in supplementary_secs:
        title = _node_text(sec.find('title')) or _node_text(sec.find('label'))
        if title:
            break

    section = _section(title or _DEFAULT_SUPPLEMENTARY_MATERIAL_TITLE, 2)
    for node in nodes:
        if node.tag == 'supplementary-material':
            section['paragraphs'].append([_plain_text_segment(format_item(_extract_item(node)))])
        else:
            segments = xml_utils.get_segments_from_node(node)
            if segments:
                section['paragraphs'].append(segments)
    return section


def _text_with_link_targets(node):
    """Texto do nó, com o endereço de cada <ext-link> entre parênteses quando o texto do link não o mostra (ex. "click here")."""
    parts = [node.text or '']
    for child in node:
        parts.append(_text_with_link_targets(child))
        if child.tag == 'ext-link':
            href = child.get('{http://www.w3.org/1999/xlink}href') or ''
            if href and href not in ''.join(child.itertext()):
                parts.append(f' ({href})')
        parts.append(child.tail or '')
    return ' '.join(''.join(parts).split())


def _extract_item(supplementary_material):
    label_text = _node_text(supplementary_material.find('label'))
    caption_text = _node_text(supplementary_material.find('caption/title'))

    # SPS 1.10: dentro de <supplementary-material> o item e um <media>
    # (video, pdf, planilha etc.) ou um <graphic> (figura) - so um dos dois.
    media = supplementary_material.find('.//media')
    graphic = supplementary_material.find('.//graphic') if media is None else None
    asset = media if media is not None else graphic

    href = ''
    mimetype = ''
    mime_subtype = ''
    description = ''
    if asset is not None:
        href = (
            asset.get('{http://www.w3.org/1999/xlink}href')
            or asset.get('xlink:href')
            or asset.get('href')
            or ''
        )
        if media is not None:
            mimetype = media.get('mimetype') or ''
            mime_subtype = media.get('mime-subtype') or ''
        # SPS 1.10: <long-desc> (descricao detalhada) e <alt-text> (breve,
        # ate 120 caracteres) sao alternativas de acessibilidade em
        # <media>/<graphic>; prefere a mais completa quando ambas existem.
        long_desc = asset.find('long-desc')
        alt_text = asset.find('alt-text')
        if long_desc is not None and (long_desc.text or '').strip():
            description = long_desc.text.strip()
        elif alt_text is not None and (alt_text.text or '').strip():
            description = alt_text.text.strip()

    notes = ' '.join(
        text for text in (_text_with_link_targets(p) for p in supplementary_material.findall('p')) if text
    )
    return {
        'type': 'supplementary_item',
        'label': label_text,
        'caption': caption_text,
        'filename': href,
        'mimetype': mimetype,
        'mime_subtype': mime_subtype,
        'description': description,
        'notes': notes,
    }
