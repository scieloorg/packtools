from packtools.sps.formats.pdf.pipeline.xml import extract_table_data

_DEFAULT_APP_GROUP_TITLE = 'Appendix'
_DEFAULT_SUPPLEMENTARY_MATERIAL_TITLE = 'Supplementary Material'


def extract_data(xml_tree):
    """
    Extracts appendix (<app-group>) and supplementary material
    (<supplementary-material>) data from an XML tree.

    SPS 1.10 treats these as distinct concepts ("<app-group> e <app> não
    comportam <supplementary-material>"), so each gets its own section
    with its own title, instead of a single title shared between both.

    An <app-group> with more than one <app> gets one section per <app>
    when at least one of them has its own <title>/<label> - a single
    shared title would mislabel every app after the first (e.g. three
    annexes "A"/"B"/"C" all rendered as "Appendix"). When none of the
    group's <app> has a title/label to tell them apart, they stay merged
    under one section, as before (issue #1375 review).

    Args:
        xml_tree (ElementTree): The XML tree to extract the data from.

    Returns:
        list[dict]: Section dicts (one per split <app>, one for the
        remaining/merged app-groups, one for supplementary material -
        only for the ones with content), each with the keys:
            - 'title': The section title.
            - 'elements': A list of dicts, one per extracted element.
    """
    sections = []

    app_groups = xml_tree.findall('.//app-group')
    split_groups = [
        app_group for app_group in app_groups
        if len(app_group.findall('app')) > 1
        and any(_app_own_title(app) for app in app_group.findall('app'))
    ]
    other_groups = [app_group for app_group in app_groups if app_group not in split_groups]

    for app_group in split_groups:
        for index, app in enumerate(app_group.findall('app'), start=1):
            elements = _extract_single_app_elements(app)
            if elements:
                sections.append({'title': _app_title(app, index), 'elements': elements})

    other_elements = _extract_app_group_elements(other_groups)
    if other_elements:
        title = _app_group_title(other_groups)
        # Nenhum app-group tem <title> proprio: se ha exatamente um <app> ao
        # todo (o caso mais comum), cai para app/title -> app/label antes do
        # padrao em ingles (issue #1375 review, ex. tests/fixtures/pdf/a1.xml,
        # <app><label>SUPPLEMENTARY MATERIAL</label></app> sem <title>). Com
        # mais de um <app> sem titulo de grupo, mantem o padrao: usar o
        # titulo de um so app atribuiria erroneamente um nome unico aos
        # demais, mesmo problema que a divisao por app acima evita.
        if title == _DEFAULT_APP_GROUP_TITLE:
            other_apps = [app for app_group in other_groups for app in app_group.findall('app')]
            if len(other_apps) == 1:
                title = _app_own_title(other_apps[0]) or title
        sections.append({'title': title, 'elements': other_elements})

    supplementary_material_elements = (
        _extract_supplementary_sec_notes(xml_tree) + _extract_supplementary_material_elements(xml_tree)
    )
    if supplementary_material_elements:
        sections.append({
            'title': _DEFAULT_SUPPLEMENTARY_MATERIAL_TITLE,
            'elements': supplementary_material_elements,
        })

    return sections


def format_item(element):
    """Monta 'Rótulo (Legenda): arquivo (tipo/subtipo). Descrição' a partir de um item extraído de <supplementary-material>, sem partes ausentes."""
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
    return text


# -----------------
# Private helpers
# -----------------

def _app_group_title(app_groups):
    """SPS 1.10: <app-group><title> é opcional e a terminologia (Apêndice/Anexo/etc.) varia por periódico - usa o primeiro título não vazio entre os grupos informados, ou o padrão em inglês."""
    for app_group in app_groups:
        title = app_group.find('title')
        if title is not None:
            title_text = ''.join(title.itertext()).strip()
            if title_text:
                return title_text
    return _DEFAULT_APP_GROUP_TITLE


def _extract_app_group_elements(app_groups):
    elements = []
    for app_group in app_groups:
        for element in app_group:
            if element.text:
                elements.append({'content': element.text, 'type': 'text'})

            for table_wrap in element.findall('.//table-wrap'):
                for table_data in extract_table_data(table_wrap):
                    elements.append({
                        'type': 'table',
                        'content': table_data
                    })
    return elements


def _app_own_title(app):
    """Texto de <app>/<title> ou <app>/<label>, o que vier primeiro e não vazio - vazio quando o <app> não tem nenhum dos dois."""
    for tag in ('title', 'label'):
        node = app.find(tag)
        if node is not None:
            text = ''.join(node.itertext()).strip()
            if text:
                return text
    return ''


def _app_title(app, index):
    """Título de um <app> num app-group com mais de um <app>, cada um com sua própria seção: app/title -> app/label -> padrão numerado (issue #1375 review)."""
    return _app_own_title(app) or f'{_DEFAULT_APP_GROUP_TITLE} {index}'


def _extract_single_app_elements(app):
    """
    Extrai texto solto e tabelas de um único <app>, usado quando o
    app-group tem mais de um <app> e cada um vira sua própria seção.
    Mesma limitação de _extract_app_group_elements: só lê o texto
    imediatamente após a tag <app>, não o que está dentro de <p>
    (issue #1375, follow-up).
    """
    elements = []
    if app.text:
        elements.append({'content': app.text, 'type': 'text'})
    for table_wrap in app.findall('.//table-wrap'):
        for table_data in extract_table_data(table_wrap):
            elements.append({'type': 'table', 'content': table_data})
    return elements


def _extract_supplementary_sec_notes(xml_tree):
    """
    Extrai o <title> (via caller) e os <p> diretos da <sec> de material
    suplementar - a frase de disponibilidade/DOI que a exclusão dessa
    <sec> do corpo (extract_body_data) removia sem recapturar em lugar
    nenhum (issue #1375 review). Pula o <p> que só envolve um
    <supplementary-material> sem outro texto ao redor - seu conteúdo já
    vira um item em _extract_supplementary_material_elements.
    """
    elements = []
    for sec in xml_tree.xpath('.//sec[.//supplementary-material and not(sec)]'):
        for p in sec.findall('p'):
            if p.find('.//supplementary-material') is not None:
                continue
            text = ''.join(p.itertext()).strip()
            if text:
                elements.append({'content': text, 'type': 'text'})
    return elements


def _extract_supplementary_material_elements(xml_tree):
    elements = []
    for supplementary_material in xml_tree.findall('.//supplementary-material'):
        label = supplementary_material.find('label')
        label_text = ''.join(label.itertext()).strip() if label is not None else ''
        caption_title = supplementary_material.find('caption/title')
        caption_text = ''.join(caption_title.itertext()).strip() if caption_title is not None else ''

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
        elements.append({
            'type': 'supplementary_item',
            'label': label_text,
            'caption': caption_text,
            'filename': href,
            'mimetype': mimetype,
            'mime_subtype': mime_subtype,
            'description': description,
        })
    return elements
