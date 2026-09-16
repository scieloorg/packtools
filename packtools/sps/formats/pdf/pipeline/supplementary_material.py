from packtools.sps.formats.pdf.pipeline.xml import extract_table_data


def extract_data(xml_tree):
    """
    Extracts supplementary data from an XML tree.

    Args:
        xml_tree (ElementTree): The XML tree to extract the supplementary data from.

    Returns:
        dict: A dictionary containing the supplementary data, with the following keys:
            - 'title': The title of the supplementary section, if present.
            - 'elements': A list of dicts, one per extracted element (app-group
              text/table, or a 'supplementary_item' from <supplementary-material>).
    """
    data = {'title': 'Supplementary Material', 'elements': []}

    app_groups = xml_tree.findall('.//app-group')
    if app_groups:
        for app_group in app_groups:
            for element in app_group:
                if element.text:
                    data['elements'].append({'content': element.text, 'type': 'text'})

                for table_wrap in element.findall('.//table-wrap'):
                    for table_data in extract_table_data(table_wrap):
                        data['elements'].append({
                            'type': 'table',
                            'content': table_data
                        })

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
        data['elements'].append({
            'type': 'supplementary_item',
            'label': label_text,
            'caption': caption_text,
            'filename': href,
            'mimetype': mimetype,
            'mime_subtype': mime_subtype,
        })

    return data


def format_item(element):
    """Monta 'Rótulo (Legenda): arquivo (tipo/subtipo)' a partir de um item extraído de <supplementary-material>, sem partes ausentes."""
    text = element['label'] or 'Supplementary Material'
    if element.get('caption'):
        text = f"{text} ({element['caption']})"
    if element['filename']:
        mimetype, mime_subtype = element['mimetype'], element['mime_subtype']
        media_type = f"{mimetype}/{mime_subtype}" if mimetype and mime_subtype else (mimetype or mime_subtype)
        suffix = f" ({media_type})" if media_type else ''
        text = f"{text}: {element['filename']}{suffix}"
    return text
