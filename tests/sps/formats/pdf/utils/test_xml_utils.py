import unittest

from lxml import etree

from packtools.sps.formats.pdf.utils import xml_utils


class TestGetTextFromNode(unittest.TestCase):

    def test_get_text_from_node_with_xref_and_italic(self):
        xmltree = etree.fromstring(
            '<p>Start <xref ref-type="bibr">Text <italic>Emphasized</italic> more</xref> end.</p>'
        )
        expected = 'Start Text Emphasized more end.'
        result = xml_utils.get_text_from_node(xmltree)
        self.assertEqual(expected, result)

    def test_get_text_from_node_empty_elements(self):
        xmltree = etree.fromstring(
            '<p><xref ref-type="bibr"></xref><italic></italic></p>'
        )
        expected = ''
        result = xml_utils.get_text_from_node(xmltree)
        self.assertEqual(result, expected)

    def test_get_text_from_node_nested_elements(self):
        xmltree = etree.fromstring(
            '<p>This part is <bold>bold text only</bold>, and this part is both <bold><italic>bold and italic</italic></bold> text.</p>'
        )
        expected = 'This part is bold text only, and this part is both bold and italic text.'
        result = xml_utils.get_text_from_node(xmltree)
        self.assertEqual(expected, result)

    def test_get_text_from_node_semicolon_formatting(self):
        xmltree = etree.fromstring(
            '<p>Text; with; semicolons</p>'
        )
        expected = 'Text; with; semicolons'
        result = xml_utils.get_text_from_node(xmltree)
        self.assertEqual(expected, result)

    def test_get_text_from_node_mixed_content(self):
        xmltree = etree.fromstring(
            '<p>Start <xref ref-type="bibr">1</xref> middle <italic>emphasized</italic> end.</p>'
        )
        expected = 'Start 1 middle emphasized end.'
        result = xml_utils.get_text_from_node(xmltree)
        self.assertEqual(expected, result)

    def test_get_text_from_node_multiple_xref_italic(self):
        xmltree = etree.fromstring(
            '<p><xref ref-type="bibr">1<italic>st</italic> ref</xref> and <xref ref-type="bibr">2<italic>nd</italic> ref</xref></p>'
        )
        expected = '1st ref and 2nd ref'
        result = xml_utils.get_text_from_node(xmltree)
        self.assertEqual(expected, result)

    def test_get_text_from_node_preserves_parenthesis_adjacency(self):
        # No space should be inserted between "(" and the xref text, or
        # between the xref text and ")", when none exists in the source.
        xmltree = etree.fromstring(
            '<p>seen (<xref ref-type="bibr">Author, 2020</xref>; '
            '<xref ref-type="bibr">Other, 2021</xref>) here</p>'
        )
        expected = 'seen (Author, 2020; Other, 2021) here'
        result = xml_utils.get_text_from_node(xmltree)
        self.assertEqual(expected, result)

    def test_get_text_from_node_skip_tags_drops_content_but_keeps_tail(self):
        xmltree = etree.fromstring(
            '<p>Before <fig id="f1"><label>Figure 1</label></fig> after</p>'
        )
        result = xml_utils.get_text_from_node(xmltree, skip_tags={'fig'})
        self.assertEqual('Before after', result)

    def test_get_text_from_node_skip_tags_collapses_tail_whitespace(self):
        xmltree = etree.fromstring(
            '<p>Before\n<table-wrap id="t1"><label>Table 1</label></table-wrap>\n   after</p>'
        )
        result = xml_utils.get_text_from_node(xmltree, skip_tags={'table-wrap'})
        self.assertEqual('Before after', result)

    def test_get_text_from_node_without_skip_tags_keeps_fig_content(self):
        xmltree = etree.fromstring(
            '<p>Before <fig id="f1"><label>Figure 1</label></fig> after</p>'
        )
        result = xml_utils.get_text_from_node(xmltree)
        self.assertEqual('Before Figure 1 after', result)

    def test_get_text_from_node_with_sup_inside_xref(self):
        xmltree = etree.fromstring(
            '<p>Author <xref ref-type="bibr"><sup>1,2</sup></xref> stated</p>'
        )
        self.assertEqual('Author 1,2 stated', xml_utils.get_text_from_node(xmltree))

    def test_get_text_from_node_nested_formatting_with_tail(self):
        xmltree = etree.fromstring(
            '<p>Start <bold>bold <italic>and italic</italic> still bold</bold> end</p>'
        )
        self.assertEqual(
            'Start bold and italic still bold end',
            xml_utils.get_text_from_node(xmltree),
        )

    def test_get_text_from_node_normalizes_spaces_around_parentheses_and_punctuation(self):
        xmltree = etree.fromstring(
            '<p>Studies ( <xref ref-type="bibr">Author, 2020</xref> ; '
            '<xref ref-type="bibr">Other, 2021</xref> ) and [ <xref ref-type="bibr">1</xref> ] '
            'with comma ( <xref ref-type="bibr">Foo, 2019</xref> , more).</p>'
        )
        self.assertEqual(
            'Studies (Author, 2020; Other, 2021) and [1] with comma (Foo, 2019, more).',
            xml_utils.get_text_from_node(xmltree),
        )


def _seg(text, italic=False, bold=False, superscript=False, subscript=False):
    return {
        'type': 'text',
        'text': text,
        'italic': italic,
        'bold': bold,
        'superscript': superscript,
        'subscript': subscript,
    }


class TestGetSegmentsFromNode(unittest.TestCase):
    """
    Regression/coverage for get_segments_from_node (item 04 of the
    pdf_generator backlog): unlike get_text_from_node, inline
    <italic>/<bold>/<sup>/<sub> markup must be preserved as style flags
    on each segment instead of being flattened away.
    """

    def test_plain_text_is_a_single_unstyled_segment(self):
        xmltree = etree.fromstring('<p>Plain text only.</p>')
        result = xml_utils.get_segments_from_node(xmltree)
        self.assertEqual(result, [_seg('Plain text only.')])

    def test_italic_segment_gets_its_own_run(self):
        xmltree = etree.fromstring('<p>A <italic>Genus species</italic> name.</p>')
        result = xml_utils.get_segments_from_node(xmltree)
        self.assertEqual(result, [
            _seg('A '),
            _seg('Genus species', italic=True),
            _seg(' name.'),
        ])

    def test_bold_sup_sub_segments(self):
        xmltree = etree.fromstring('<p><bold>Bold</bold> and <sup>sup</sup> and <sub>sub</sub>.</p>')
        result = xml_utils.get_segments_from_node(xmltree)
        self.assertEqual(result, [
            _seg('Bold', bold=True),
            _seg(' and '),
            _seg('sup', superscript=True),
            _seg(' and '),
            _seg('sub', subscript=True),
            _seg('.'),
        ])

    def test_nested_styles_combine_regardless_of_order(self):
        xmltree = etree.fromstring(
            '<p>A <sup><italic>one</italic></sup> and <italic><sup>two</sup></italic> case.</p>'
        )
        result = xml_utils.get_segments_from_node(xmltree)
        self.assertEqual(result, [
            _seg('A '),
            _seg('one', italic=True, superscript=True),
            _seg(' and '),
            _seg('two', italic=True, superscript=True),
            _seg(' case.'),
        ])

    def test_adjacent_unstyled_fragments_merge_into_one_segment(self):
        # <xref> carries no style of its own, so its text and tail merge
        # with the surrounding plain text into a single segment rather
        # than fragmenting the run needlessly.
        xmltree = etree.fromstring(
            '<p>Start <xref ref-type="bibr">Text</xref> end.</p>'
        )
        result = xml_utils.get_segments_from_node(xmltree)
        self.assertEqual(result, [_seg('Start Text end.')])

    def test_punctuation_spacing_normalized_like_get_text_from_node(self):
        xmltree = etree.fromstring(
            '<p>seen (<xref ref-type="bibr">Author, 2020</xref>; '
            '<xref ref-type="bibr">Other, 2021</xref>) here</p>'
        )
        result = xml_utils.get_segments_from_node(xmltree)
        self.assertEqual(result, [_seg('seen (Author, 2020; Other, 2021) here')])

    def test_skip_tags_drops_content_but_keeps_tail(self):
        xmltree = etree.fromstring(
            '<p>Before <fig id="f1"><label>Figure 1</label></fig> after</p>'
        )
        result = xml_utils.get_segments_from_node(xmltree, skip_tags={'fig'})
        self.assertEqual(result, [_seg('Before after')])

    def test_leading_and_trailing_whitespace_stripped(self):
        xmltree = etree.fromstring('<p>  padded text  </p>')
        result = xml_utils.get_segments_from_node(xmltree)
        self.assertEqual(result, [_seg('padded text')])

    def test_empty_node_returns_no_segments(self):
        xmltree = etree.fromstring('<p><italic></italic></p>')
        result = xml_utils.get_segments_from_node(xmltree)
        self.assertEqual(result, [])


class TestGetTextFromMixedCitationNode(unittest.TestCase):

    def test_get_text_from_mixed_citation_node_with_simple_text(self):
        xml = etree.fromstring(
            '<mixed-citation>Simple reference text</mixed-citation>'
        )
        expected = 'Simple reference text.'
        result = xml_utils.get_text_from_mixed_citation_node(xml)
        self.assertEqual(expected, result)

    def test_get_text_from_mixed_citation_node_with_italic(self):
        xml = etree.fromstring(
            '<mixed-citation>Text with <italic>italicized</italic> content</mixed-citation>'
        )
        expected = 'Text with italicized content.'
        result = xml_utils.get_text_from_mixed_citation_node(xml)
        self.assertEqual(expected, result)

    def test_get_text_from_mixed_citation_node_with_multiple_elements(self):
        xml = etree.fromstring(
            '<mixed-citation>Author A, <italic>Title B</italic>, <bold>Journal C</bold></mixed-citation>'
        )
        expected = 'Author A, Title B, Journal C.'
        result = xml_utils.get_text_from_mixed_citation_node(xml)
        self.assertEqual(expected, result)

    def test_get_text_from_mixed_citation_node_with_empty_elements(self):
        xml = etree.fromstring(
            '<mixed-citation>Text <italic></italic> with <bold></bold> empty elements</mixed-citation>'
        )
        expected = 'Text with empty elements.'
        result = xml_utils.get_text_from_mixed_citation_node(xml)
        self.assertEqual(expected, result)

    def test_get_text_from_mixed_citation_node_already_has_period(self):
        xml = etree.fromstring(
            '<mixed-citation>Reference ending with period.</mixed-citation>'
        )
        expected = 'Reference ending with period.'
        result = xml_utils.get_text_from_mixed_citation_node(xml)
        self.assertEqual(expected, result)

    def test_get_text_from_mixed_citation_node_with_nested_tail_text(self):
        xml = etree.fromstring(
            '<mixed-citation>Start <italic>italic</italic> middle <bold>bold</bold> end</mixed-citation>'
        )
        expected = 'Start italic middle bold end.'
        result = xml_utils.get_text_from_mixed_citation_node(xml)
        self.assertEqual(expected, result)


class TestGetNodeLevel(unittest.TestCase):

    def test_get_node_level_root_element(self):
        xmltree = etree.fromstring("<root><a><b>text</b></a></root>")
        result = xml_utils.get_node_level(xmltree, xmltree)
        self.assertEqual(0, result)

    def test_get_node_level_first_level(self):
        xmltree = etree.fromstring("<root><a><b>text</b></a></root>")
        element = xmltree.find(".//a")
        result = xml_utils.get_node_level(element, xmltree)
        self.assertEqual(1, result)

    def test_get_node_level_second_level(self):
        xmltree = etree.fromstring("<root><a><b>text</b></a></root>")
        element = xmltree.find(".//b")
        result = xml_utils.get_node_level(element, xmltree)
        self.assertEqual(2, result)

    def test_get_node_level_deep_nesting(self):
        xmltree = etree.fromstring("<root><a><b><c><d>text</d></c></b></a></root>")
        element = xmltree.find(".//d")
        result = xml_utils.get_node_level(element, xmltree)
        self.assertEqual(4, result)

    def test_get_node_level_sibling_elements(self):
        xmltree = etree.fromstring("<root><a>text1</a><b>text2</b></root>")
        element = xmltree.find(".//b")
        result = xml_utils.get_node_level(element, xmltree)
        self.assertEqual(1, result)

    def test_get_node_level_detached_element(self):
        xmltree = etree.fromstring("<root><a><b>text</b></a></root>")
        detached = etree.Element("detached")
        result = xml_utils.get_node_level(detached, xmltree)
        self.assertEqual(0, result)

    def test_get_node_level_complex_structure(self):
        xmltree = etree.fromstring(
            """
            <root>
                <section>
                    <title>Title</title>
                    <para>
                        <bold>Text</bold>
                        <italic>More text</italic>
                    </para>
                </section>
            </root>
            """
        )
        element = xmltree.find(".//bold")
        result = xml_utils.get_node_level(element, xmltree)
        self.assertEqual(3, result)