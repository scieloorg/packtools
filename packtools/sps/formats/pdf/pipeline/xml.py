import string
import warnings

from packtools.sps.formats.pdf.extract import figures, tables
from packtools.sps.formats.pdf.layout import table_layout
from packtools.sps.formats.pdf.ooxml import formula
from packtools.sps.formats.pdf.utils import xml_utils

# Módulo de compatibilidade em transição (docs/pdf_generator_architecture.md):
# as funções já movidas continuam acessíveis por aqui, com DeprecationWarning.
_METADATA = 'packtools.sps.formats.pdf.extract.metadata'
_FIGURES = 'packtools.sps.formats.pdf.extract.figures'
_REFERENCES = 'packtools.sps.formats.pdf.extract.references'
_ACKNOWLEDGMENTS = 'packtools.sps.formats.pdf.extract.acknowledgments'
_CITATION = 'packtools.sps.formats.pdf.extract.citation'
_TABLES = 'packtools.sps.formats.pdf.extract.tables'
_MOVED = {
    'extract_article_main_language': _METADATA,
    'extract_article_type': _METADATA,
    'extract_journal_title': _METADATA,
    'extract_doi': _METADATA,
    'extract_category': _METADATA,
    'extract_article_title': _METADATA,
    'extract_contrib_data': _METADATA,
    'extract_abstract_data': _METADATA,
    'extract_trans_abstract_data': _METADATA,
    'extract_keywords_data': _METADATA,
    'extract_footer_data': _METADATA,
    'extract_figure_data': _FIGURES,
    'extract_references_data': _REFERENCES,
    'extract_acknowledgment_data': _ACKNOWLEDGMENTS,
    'extract_cite_as_part_one': _CITATION,
    'CITATION_STYLE_VANCOUVER': _CITATION,
    'build_full_citation': _CITATION,
    'extract_table_data': _TABLES,
}


def __getattr__(name):
    if name in _MOVED:
        import importlib
        warnings.warn(
            f"{name} has moved to {_MOVED[name]}. "
            f"Importing from packtools.sps.formats.pdf.pipeline.xml is deprecated.",
            DeprecationWarning,
            stacklevel=2,
        )
        return getattr(importlib.import_module(_MOVED[name]), name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def determine_table_layout(table_wrap, override=None):
    """Depreciado: use layout.table_layout.determine_table_layout, que recebe
    os dados de extract.tables.read_table_wrap em vez do <table-wrap>."""
    warnings.warn(
        "determine_table_layout has moved to packtools.sps.formats.pdf.layout.table_layout "
        "and now takes extract.tables.read_table_wrap(table_wrap). "
        "Importing from packtools.sps.formats.pdf.pipeline.xml is deprecated.",
        DeprecationWarning,
        stacklevel=2,
    )
    return table_layout.determine_table_layout(tables.read_table_wrap(table_wrap), override=override)


def _int_to_roman(number):
    """Converts a positive int to a lowercase roman numeral string."""
    values = (1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1)
    symbols = ('m', 'cm', 'd', 'cd', 'c', 'xc', 'l', 'xl', 'x', 'ix', 'v', 'iv', 'i')
    result = []
    for value, symbol in zip(values, symbols):
        count, number = divmod(number, value)
        result.append(symbol * count)
    return ''.join(result)


def _list_item_marker(list_type, index):
    """
    Returns the text marker (e.g. "1. ", "a. ") for a <list-item> at
    position `index` (1-based) of a <list list-type="...">, or '' for a
    list-type with no visual marker ("simple", the type used when a list's
    own items already carry their numbering some other way, e.g. a
    <disp-formula>'s own <label> - see issue #1365/a5.xml) or an
    unrecognized/absent list-type.
    """
    if list_type == 'bullet':
        return '• '
    if list_type in ('order', 'arabic'):
        return f'{index}. '
    if list_type == 'roman-lower':
        return f'{_int_to_roman(index)}. '
    if list_type == 'roman-upper':
        return f'{_int_to_roman(index).upper()}. '
    if list_type == 'alpha-lower':
        return f'{string.ascii_lowercase[(index - 1) % 26]}. '
    if list_type == 'alpha-upper':
        return f'{string.ascii_uppercase[(index - 1) % 26]}. '
    return ''


def _plain_text_segment(text):
    """An unstyled text segment, in the shape get_segments_from_node returns."""
    return {'type': 'text', 'text': text, 'italic': False, 'bold': False, 'superscript': False, 'subscript': False}


_INLINE_FORMULA_TAGS = {'inline-formula'}


def _inline_formula_segment(inline_formula):
    """Converte o MathML de um <inline-formula> (fórmula no meio de texto corrido) em um segmento 'formula'.

    Ao contrário de <disp-formula>, não carrega <label> próprio (fase 2 de
    #1347, issue #1353).

    Args:
        inline_formula (ElementTree): The <inline-formula> element.

    Returns:
        dict, or None when there's no MathML descendant or
        formula.mathml_to_omml couldn't convert it (unsupported construct) -
        the caller (xml_utils.get_segments_from_node) falls back to
        flattening it as plain text, same as any unrecognized tag.
    """
    math_node = inline_formula.find('.//{http://www.w3.org/1998/Math/MathML}math')
    if math_node is None:
        return None
    omml_element = formula.mathml_to_omml(math_node)
    if omml_element is None:
        return None
    return {'type': 'formula', 'omml': omml_element}


def _disp_formula_segments(disp_formula):
    """Converte o MathML de um <disp-formula> em um segmento 'formula', mais um segmento de texto para o <label>, se houver.

    O segmento de fórmula leva 'display': True (fórmula em bloco); o renderer
    usa essa marca para separá-la do texto e distingui-la de fórmula inline.

    Args:
        disp_formula (ElementTree): The <disp-formula> element.

    Returns:
        list[dict], or None when there's no MathML descendant or
        formula.mathml_to_omml couldn't convert it (unsupported construct) -
        callers should fall back to the existing flattened-text paragraph
        in that case, never drop the formula silently.
    """
    math_node = disp_formula.find('.//{http://www.w3.org/1998/Math/MathML}math')
    if math_node is None:
        return None
    omml_element = formula.mathml_to_omml(math_node)
    if omml_element is None:
        return None

    segments = [{'type': 'formula', 'omml': omml_element, 'display': True}]
    label = disp_formula.find('label')
    if label is not None:
        label_text = ''.join(label.itertext()).strip()
        if label_text:
            segments.append(_plain_text_segment(f' {label_text}'))
    return segments


def _paragraph_with_trailing_formula(p_node):
    """Trata <p>texto:<disp-formula>...</disp-formula></p>: fórmula em bloco com texto simples antes, no mesmo parágrafo.

    Escopo restrito: um <p> com mais de um <disp-formula>, ou com
    conteúdo depois da fórmula, retorna None (o chamador cai no fallback).

    Args:
        p_node (ElementTree): The <p> element.

    Returns:
        list[dict], or None when `p_node` doesn't match this specific shape.
    """
    formulas = p_node.findall('disp-formula')
    if len(formulas) != 1:
        return None
    formula = formulas[0]
    siblings = list(p_node)
    if siblings[-1] is not formula:
        return None
    if (formula.tail or '').strip():
        return None

    formula_segments = _disp_formula_segments(formula)
    if formula_segments is None:
        return None

    leading_segments = xml_utils.get_segments_from_node(
        p_node, skip_tags={'disp-formula'},
        formula_tags=_INLINE_FORMULA_TAGS, formula_converter=_inline_formula_segment,
    )
    return leading_segments + formula_segments


def _extract_list_paragraphs(list_node):
    """
    Extracts a <list>'s <list-item>s as paragraph entries (issue #1365):
    one per item, each the same list-of-segments shape as any other
    paragraph, with a bullet/number/letter marker (see _list_item_marker)
    prepended as its own leading segment - or no marker for list-type
    "simple" (used when the items already carry their own numbering some
    other way, e.g. each <disp-formula>'s own <label>) or an unrecognized
    list-type.

    Um <disp-formula> ao final do <p> de um <list-item> recebe conversão
    OMML real via _paragraph_with_trailing_formula, em vez do texto
    achatado ambíguo que a recursão comum de get_segments_from_node
    produziria. Uma fórmula só-imagem (sem MathML) aninhada nesse nível
    ainda é descartada silenciosamente (não vista no corpus de testes).

    Args:
        list_node (ElementTree): The <list> element.

    Returns:
        list[list[dict]]: One entry per non-empty <list-item> paragraph.
    """
    list_type = list_node.get('list-type', '')
    paragraphs = []
    for index, item in enumerate(list_node.findall('list-item'), start=1):
        marker = _list_item_marker(list_type, index)
        for item_p in item.findall('p'):
            item_segments = _paragraph_with_trailing_formula(item_p)
            if item_segments is None:
                item_segments = xml_utils.get_segments_from_node(
                    item_p, skip_tags={'fig', 'table-wrap'},
                    formula_tags=_INLINE_FORMULA_TAGS, formula_converter=_inline_formula_segment,
                )
            if not item_segments:
                continue
            if marker:
                item_segments = [_plain_text_segment(marker)] + item_segments
                marker = ''
            paragraphs.append(item_segments)
    return paragraphs


def extract_body_data(xml_tree, table_layout_overrides=None):
    """
    Extracts the body data from an XML tree, including section titles, paragraphs, and tables.

    Excludes any <sec> nested inside <abstract> or <trans-abstract> - those
    are structured-abstract subsections handled by extract_abstract_data /
    extract_trans_abstract_data, and would otherwise be picked up twice by
    a plain './/sec' search.

    Also excludes a <sec> that IS the supplementary-material section -
    identified structurally as a <sec> with a <supplementary-material>
    descendant and no <sec> of its own (not by @sec-type, which varies
    across the corpus: "supplementary-material", "materials|supplementary-
    material", "supplementary" or absent entirely) - handled separately by
    supplementary_material.extract_data, which already renders it under its
    own heading; leaving it in here too would duplicate the content. The
    "no <sec> of its own" guard matters: a real body section (e.g.
    "Discussion") that merely references supplementary material somewhere
    inside one of its own subsections is not a supplementary-material
    section and must stay in the body (issue #1375 review).

    Also excludes <sec> nested inside <app-group> (an appendix section):
    supplementary_material.extract_data renders each <app> with its own
    <sec> as subsections, so keeping them here too would render the same
    title, paragraphs and tables twice (issue #1372).

    Also excludes <sec> nested inside a translation <sub-article>
    (article-type="translation" - its own <sec> tree would otherwise
    duplicate the whole body in another language) (issue #1372). A
    non-translation <sub-article> (e.g. article-type
    "reviewer-report" or "reply") is left untouched - its <sec> is real,
    published body content, not a duplicate. Deliberately narrow: a
    <back><sec> that's neither of those (e.g. a bare
    sec-type="data-availability" statement, ~68% of a real 593-article
    corpus) is left as-is, matching the pre-existing, already-documented
    behavior from issue #1351 rather than the issue's own literal
    body-only wording - a full <body>-only scope would silently drop that
    content instead, since nothing else in the pipeline extracts a bare
    <back><sec>.

    Falls back to treating <body> itself as an extra, untitled section when
    <body> has no <sec> of its own (valid JATS pattern for unsectioned
    short communications/brief reports) - otherwise its content would be
    silently dropped even though an unrelated <sec> elsewhere in the
    document (e.g. a data-availability statement under <back>) keeps the
    section search from returning empty.

    Args:
        xml_tree (ElementTree): The XML tree to extract the body data from.
        table_layout_overrides (dict, optional): Maps a table-wrap @id to a forced
            layout ('single-column-layout' or 'double-column-layout'), bypassing
            `determine_table_layout`'s heuristic for that specific table.

    Returns:
        list: A list of dictionaries, where each dictionary represents a section in the body of the document. Each dictionary has the following keys:
            - 'level': The nesting level of the section.
            - 'title': The title of the section, if present.
            - 'paragraphs': A list of paragraphs, each a list of style-tagged
              text segments (see xml_utils.get_segments_from_node) preserving
              inline <italic>/<bold>/<sup>/<sub> markup, and converting any
              <inline-formula> found in running text to a real OMML formula
              segment (issue #1353, fase 2 de #1347) instead of flattening
              its MathML to ambiguous text. Also includes any
              <disp-formula> found as a direct sibling of a <p>, since a
              structured formula isn't always wrapped in one - as a single
              plain-text segment (no MathML->OMML conversion yet, see issue
              #1347's phased plan). Also includes each <list-item> of a
              direct-child <list>, one per item, with a bullet/number/letter
              marker prepended as its own leading segment (see
              _list_item_marker; nothing prepended for list-type "simple" or
              unrecognized). Excludes paragraphs that contain table/figure
              references or wrappers.
            - 'tables': A list of dictionaries representing the tables in the section, as returned by the `extract_table_data` function.
            - 'figures': A list of dictionaries representing figures in the section, as returned by the `extract_figure_data` function
              (also includes any <disp-formula> that is a graphic rather than
              MathML/text - whether a direct sibling of a <p> or, since a
              <label> would otherwise make it look like flattenable text,
              carrying its own <label> - since there's nothing to flatten
              into a paragraph).
    """
    data = []
    seen_fig_keys = set()

    body_sections = xml_tree.xpath(
        './/sec[not(ancestor::abstract) and not(ancestor::trans-abstract)'
        ' and not(.//supplementary-material and not(sec)) and not(ancestor::app-group)'
        ' and not(ancestor::sub-article[@article-type="translation"])]'
    )
    body = xml_tree.find('.//body')
    if body is not None and body.find('.//sec') is None:
        body_sections = [body] + body_sections

    for document_section in body_sections:
        data.append(extract_section_data(document_section, xml_tree, seen_fig_keys, table_layout_overrides))

    return data


def extract_section_data(document_section, xml_tree, seen_fig_keys, table_layout_overrides=None, level=None):
    """
    Extrai título, parágrafos, tabelas e figuras de um único nó de seção
    (<sec>, <body> sem <sec> ou <app>), no formato descrito em
    extract_body_data. seen_fig_keys é compartilhado entre as seções de
    um mesmo bloco para não repetir figuras; level, quando informado,
    substitui a profundidade do nó na árvore.
    """
    sec = {'paragraphs': [], 'tables': [], 'figures': []}
    sec['level'] = level if level is not None else xml_utils.get_node_level(document_section, xml_tree)
    sec['title'] = document_section.find('title')

    if sec['title'] is not None:
        sec['title'] = ''.join(sec['title'].itertext()).strip()

    # Collect textual paragraphs but exclude figure/table elements. Uses
    # get_text_from_node (tail-preserving) rather than a bare
    # `.xpath('.//text()...')` + `' '.join(...)`, which inserted an
    # artificial space between every text-node fragment regardless of
    # whether the source had one there (e.g. "(<xref>...</xref>)" came
    # out as "( ... )", and "<xref/>; <xref/>" as "... ; ...").
    #
    # <disp-formula> isn't always nested inside a <p> - it's often a
    # direct sibling of one - so a plain `findall('p')` silently drops
    # it. Walking direct children instead of just `<p>` catches that
    # case too. This still only flattens the formula's text (no
    # MathML->OMML conversion yet, see issue #1347's phased plan), but
    # flattened-and-present beats silently missing.
    for child in document_section:
        if child.tag == 'p':
            # <p>texto:<disp-formula>...</disp-formula></p>: tratado antes do
            # achatamento genérico, para gerar um segmento OMML real
            formula_paragraph_segments = _paragraph_with_trailing_formula(child)
            if formula_paragraph_segments is not None:
                sec['paragraphs'].append(formula_paragraph_segments)
                continue
            # <list> can also occur as a child of <p> rather than as its
            # own sibling (issue #1365, seen in a28.xml: the JATS source
            # wraps a <list> of research propositions in a <p> with no
            # other content). skip_tags drops it from the flattened text
            # the same way it already does for <fig>/<table-wrap> -
            # get_segments_from_node has no special handling for <list>,
            # so leaving it in would silently flatten it to nothing -
            # and its items are extracted separately right after.
            nested_lists = child.findall('list')
            skip_tags = {'fig', 'table-wrap', 'list'} if nested_lists else {'fig', 'table-wrap'}
            para_segments = xml_utils.get_segments_from_node(
                child, skip_tags=skip_tags,
                formula_tags=_INLINE_FORMULA_TAGS, formula_converter=_inline_formula_segment,
            )
            if para_segments:
                sec['paragraphs'].append(para_segments)
            for nested_list in nested_lists:
                sec['paragraphs'].extend(_extract_list_paragraphs(nested_list))
            continue
        elif child.tag == 'disp-formula':
            # A formula rendered as an image (<graphic>, no MathML) has to
            # be identified by shape, not by "no flattenable text": a
            # <label> sibling of <graphic> (e.g. "(1)") makes
            # get_text_from_node return non-empty even though the
            # <graphic> itself has nothing to flatten, so checking
            # `not para_text` alone let a labeled graphic formula fall
            # through and drop its <graphic> as a bare label paragraph
            # (issue #1365).
            has_graphic = child.find('.//graphic') is not None
            has_math = bool(child.xpath('.//*[local-name()="math"]'))
            if has_graphic and not has_math:
                # extract_figure_data reads the same label/caption/graphic
                # shape <fig> has, so a <disp-formula> with a <graphic>
                # can reuse it as-is and render like any other figure
                # instead of vanishing.
                formula_fig = figures.extract_figure_data(child)
                formula_key = child.get('id') or formula_fig.get('href') or ''
                if not formula_key or formula_key not in seen_fig_keys:
                    sec['figures'].append(formula_fig)
                    if formula_key:
                        seen_fig_keys.add(formula_key)
                continue
            if has_math:
                formula_segments = _disp_formula_segments(child)
                if formula_segments is not None:
                    sec['paragraphs'].append(formula_segments)
                    continue
            # fallback: sem MathML ou conversao falhou - texto achatado,
            # ambiguo mas presente e melhor que descartado silenciosamente
            para_text = xml_utils.get_text_from_node(child).strip()
            para_segments = xml_utils.get_segments_from_node(child) if para_text else []
        elif child.tag == 'list':
            # A <list> as a direct sibling of <p> - not visited at all
            # otherwise, falling to the `else: continue` below and
            # dropping the whole list (issue #1365; a5.xml loses both
            # its plain bullet lists and the Equations 3-10, which live
            # one level deeper inside <list-item><p><disp-formula>).
            sec['paragraphs'].extend(_extract_list_paragraphs(child))
            continue
        else:
            continue
        if para_segments:
            sec['paragraphs'].append(para_segments)

    for table_wrap in document_section.findall('.//table-wrap'):
        closest_sec = table_wrap.xpath('ancestor::sec[1]')
        if closest_sec and closest_sec[0] is not document_section:
            continue
        table_id = table_wrap.get('id') or table_wrap.get('xml:id')
        override_layout = (table_layout_overrides or {}).get(table_id)
        sec['tables'].extend(tables.extract_table_data(table_wrap, override_layout=override_layout))

    # Figures within the section (deduplicated across the body)
    for fig in document_section.findall('.//fig'):
        # Build a deduplication key: prefer @id; fallback to first href found
        fig_id = fig.get('id') or fig.get('xml:id')
        href = None
        g = fig.find('.//graphic')
        if g is not None:
            href = (
                g.get('{http://www.w3.org/1999/xlink}href')
                or g.get('xlink:href')
                or g.get('href')
            )
        key = fig_id or (href or '')
        if key and key in seen_fig_keys:
            continue
        fig_data = figures.extract_figure_data(fig)
        sec['figures'].append(fig_data)
        if key:
            seen_fig_keys.add(key)

    return sec


# -----------------
# Private helpers
# -----------------


