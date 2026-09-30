"""Figuras (<fig>, e <disp-formula> só-imagem) para renderização como imagem com legenda."""

import re


def extract_figure_data(fig_node):
    """
    Extracts figure metadata from a <fig> node.

    Args:
        fig_node (ElementTree): The XML <fig> element.

    Returns:
        dict: A dictionary with keys:
            - 'label': Figure label (e.g., "Figure 1")
            - 'caption': Caption text (title + paragraphs if present)
            - 'href': Path/URL from graphic/@xlink:href (or alternatives)
            - 'alt': Alternative text if present
    """
    def _get_href_from_node(node):
        # Try common attribute forms
        return (
            node.get('{http://www.w3.org/1999/xlink}href')
            or node.get('xlink:href')
            or node.get('href')
        )

    label_el = fig_node.find('label')
    label = (label_el.text or '').strip() if label_el is not None else ''

    caption_texts = []
    caption_el = fig_node.find('caption')
    if caption_el is not None:
        # Prefer title then paragraphs
        title_el = caption_el.find('title')
        if title_el is not None:
            caption_texts.append(''.join(title_el.itertext()).strip())
        for p in caption_el.findall('p'):
            txt = ''.join(p.itertext()).strip()
            if txt:
                caption_texts.append(txt)
    caption = ' '.join([c for c in caption_texts if c])

    # graphic may be a direct child, or offered as several representations
    # inside <alternatives> - only match the direct child here so the latter
    # case falls through to the ranking logic below instead of grabbing the
    # first <graphic> in document order.
    href = None
    alt_text = None

    graphic = fig_node.find('graphic')
    if graphic is not None:
        href = _get_href_from_node(graphic)
        alt_text = graphic.get('alt') or graphic.get('alt-text')

    if href is None:
        alt = fig_node.find('.//alternatives')
        if alt is not None:
            preferred_ext_order = ('.png', '.jpg', '.jpeg', '.gif', '.tif', '.tiff')
            candidates = []
            for g in alt.findall('graphic'):
                _href = _get_href_from_node(g)
                if not _href:
                    continue
                # Extract potential size from content-type like 'scielo-267x140'
                ctype = (g.get('content-type') or '').lower()
                dims_area = 0
                m = re.search(r'(\d+)x(\d+)', ctype)
                if m:
                    try:
                        w = int(m.group(1))
                        h = int(m.group(2))
                        dims_area = w * h
                    except Exception:
                        dims_area = 0
                # Penalize obvious thumbnails
                is_thumbnail = '267x140' in ctype
                is_scielo_web = (g.get('specific-use') or '').lower() == 'scielo-web'
                ext_rank = len(preferred_ext_order)
                lu = _href.lower()
                for i, ext in enumerate(preferred_ext_order):
                    if lu.endswith(ext):
                        ext_rank = i
                        break
                candidates.append({
                    'href': _href,
                    'dims_area': dims_area,
                    'ext_rank': ext_rank,
                    'is_thumbnail': is_thumbnail,
                    'is_scielo_web': is_scielo_web,
                    'alt': g.get('alt') or g.get('alt-text')
                })
            if candidates:
                # Choose best: avoid thumbnails, prefer the SciELO Web
                # representation, larger area first, then better extension
                candidates.sort(key=lambda c: (
                    c['is_thumbnail'],           # False (0) before True (1)
                    not c['is_scielo_web'],       # scielo-web first
                    -c['dims_area'],              # larger first
                    c['ext_rank']                 # better extension first
                ))
                best = candidates[0]
                href = best['href']
                if alt_text is None:
                    alt_text = best.get('alt')

    return {
        'label': label,
        'caption': caption,
        'href': href,
        'alt': alt_text or '',
    }
