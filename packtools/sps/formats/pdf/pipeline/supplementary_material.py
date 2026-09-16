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

    Args:
        xml_tree (ElementTree): The XML tree to extract the data from.

    Returns:
        list[dict]: Zero, one or two section dicts (app-group section,
        supplementary-material section - only for the ones with content),
        each with the keys:
            - 'title': The section title.
            - 'elements': A list of dicts, one per extracted element.
    """
    sections = []

    app_group_elements = _extract_app_group_elements(xml_tree)
    if app_group_elements:
        sections.append({
            'title': _app_group_title(xml_tree),
            'elements': app_group_elements,
        })

    supplementary_material_elements = _extract_supplementary_material_elements(xml_tree)
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

def _app_group_title(xml_tree):
    """SPS 1.10: <app-group><title> é opcional e a terminologia (Apêndice/Anexo/etc.) varia por periódico - só cai no padrão em inglês quando ausente."""
    app_group = xml_tree.find('.//app-group')
    title = app_group.find('title') if app_group is not None else None
    if title is not None:
        title_text = ''.join(title.itertext()).strip()
        if title_text:
            return title_text
    return _DEFAULT_APP_GROUP_TITLE


def _extract_app_group_elements(xml_tree):
    elements = []
    for app_group in xml_tree.findall('.//app-group'):
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
