"""
Migração de tests/sps/formats/old_pdf/utils/test_xml_utils.py para formats/pdf.

As funções internas do old_pdf foram substituídas:

- get_text_from_node      -> normalize(inlines(node)) / runs_text, plain_text
- get_segments_from_node  -> normalize(inlines(node)) (runs com formato)
- get_text_from_mixed_citation_node -> parágrafo de <ref> (extract/ref_list.py)
- get_node_level          -> nível dos títulos (extract/sec.py, ctx["level"])

Diferença intencional geral: um run só traz os formatos ativos
(``{"text": "x", "italic": True}``), sem as chaves False nem ``"type"``.
"""

import unittest

from packtools.sps.formats.pdf.extract.inline import inlines, plain_text
from packtools.sps.formats.pdf.extract.runs import has_content, normalize, runs_text

from tests.sps.formats.pdf.helpers import NS, extract, texts, xml


def runs_of(text, skip_tags=()):
    """Runs normalizados de um trecho XML; skip_tags: tags dos filhos omitidos."""
    node = xml(text)
    skip = [child for child in node if child.tag in skip_tags]
    return normalize(inlines(node, skip=skip))


def text_of(text, skip_tags=()):
    """Texto normalizado de um trecho XML."""
    return runs_text(runs_of(text, skip_tags))


def reference(citation):
    """Bloco de parágrafo de uma <ref> com o conteúdo dado."""
    blocks = extract(xml(f'<back {NS}><ref-list><ref>{citation}</ref></ref-list></back>'))
    (block,) = blocks[1:]  # blocks[0] é o título "References"
    return block


def headings(body):
    """(nível, texto) dos títulos de um <body>."""
    return [(b['level'], runs_text(b['runs']))
            for b in extract(xml(f'<body>{body}</body>')) if b['type'] == 'heading']


class TextFromNodeTest(unittest.TestCase):
    """Texto de conteúdo misto (antigo get_text_from_node)."""

    def test_text_and_tails_of_inline_children(self):
        """
        old: TestGetTextFromNode.test_get_text_from_node_with_xref_and_italic
        old: TestGetTextFromNode.test_get_text_from_node_nested_elements
        old: TestGetTextFromNode.test_get_text_from_node_semicolon_formatting
        old: TestGetTextFromNode.test_get_text_from_node_mixed_content
        old: TestGetTextFromNode.test_get_text_from_node_multiple_xref_italic
        old: TestGetTextFromNode.test_get_text_from_node_preserves_parenthesis_adjacency
        old: TestGetTextFromNode.test_get_text_from_node_with_sup_inside_xref
        old: TestGetTextFromNode.test_get_text_from_node_nested_formatting_with_tail
        """
        cases = [
            ('<p>Start <xref ref-type="bibr">Text <italic>Emphasized</italic> more</xref> end.</p>',
             'Start Text Emphasized more end.'),
            ('<p>This part is <bold>bold text only</bold>, and this part is both '
             '<bold><italic>bold and italic</italic></bold> text.</p>',
             'This part is bold text only, and this part is both bold and italic text.'),
            ('<p>Text; with; semicolons</p>', 'Text; with; semicolons'),
            ('<p>Start <xref ref-type="bibr">1</xref> middle <italic>emphasized</italic> end.</p>',
             'Start 1 middle emphasized end.'),
            ('<p><xref ref-type="bibr">1<italic>st</italic> ref</xref> and '
             '<xref ref-type="bibr">2<italic>nd</italic> ref</xref></p>',
             '1st ref and 2nd ref'),
            ('<p>seen (<xref ref-type="bibr">Author, 2020</xref>; '
             '<xref ref-type="bibr">Other, 2021</xref>) here</p>',
             'seen (Author, 2020; Other, 2021) here'),
            ('<p>Author <xref ref-type="bibr"><sup>1,2</sup></xref> stated</p>',
             'Author 1,2 stated'),
            ('<p>Start <bold>bold <italic>and italic</italic> still bold</bold> end</p>',
             'Start bold and italic still bold end'),
        ]
        for source, expected in cases:
            with self.subTest(source=source):
                self.assertEqual(text_of(source), expected)
                self.assertEqual(plain_text(xml(source)), expected)

    def test_empty_elements_give_no_content(self):
        """old: TestGetTextFromNode.test_get_text_from_node_empty_elements"""
        runs = runs_of('<p><xref ref-type="bibr"></xref><italic></italic></p>')
        self.assertEqual(runs, [])
        self.assertFalse(has_content(runs))

    def test_spaces_around_parentheses_and_punctuation_normalized(self):
        """old: TestGetTextFromNode.test_get_text_from_node_normalizes_spaces_around_parentheses_and_punctuation"""
        source = ('<p>Studies ( <xref ref-type="bibr">Author, 2020</xref> ; '
                  '<xref ref-type="bibr">Other, 2021</xref> ) and [ <xref ref-type="bibr">1</xref> ] '
                  'with comma ( <xref ref-type="bibr">Foo, 2019</xref> , more).</p>')
        self.assertEqual(
            text_of(source),
            'Studies (Author, 2020; Other, 2021) and [1] with comma (Foo, 2019, more).',
        )

    def test_skipped_child_drops_content_but_keeps_tail(self):
        """
        old: TestGetTextFromNode.test_get_text_from_node_skip_tags_drops_content_but_keeps_tail
        old: TestGetTextFromNode.test_get_text_from_node_skip_tags_collapses_tail_whitespace

        diferença intencional: skip recebe os elementos (não nomes de tag).
        """
        cases = [
            ('<p>Before <fig id="f1"><label>Figure 1</label></fig> after</p>', 'fig'),
            ('<p>Before\n<table-wrap id="t1"><label>Table 1</label></table-wrap>\n   after</p>',
             'table-wrap'),
        ]
        for source, skip in cases:
            with self.subTest(skip=skip):
                self.assertEqual(text_of(source, skip_tags={skip}), 'Before after')

    def test_unskipped_fig_keeps_its_content(self):
        """
        old: TestGetTextFromNode.test_get_text_from_node_without_skip_tags_keeps_fig_content

        diferença intencional: no fluxo de blocos, a figura dentro do <p>
        divide o parágrafo (antes / legenda / depois), sem perder texto.
        """
        source = '<p>Before <fig id="f1"><label>Figure 1</label></fig> after</p>'
        self.assertEqual(text_of(source), 'Before Figure 1 after')
        self.assertEqual(texts(extract(xml(source))), ['Before', 'Figure 1', 'after'])


class SegmentsFromNodeTest(unittest.TestCase):
    """Runs com formato (antigo get_segments_from_node); diferença intencional: só flags True."""

    def test_formatting_becomes_run_flags(self):
        """
        old: TestGetSegmentsFromNode.test_plain_text_is_a_single_unstyled_segment
        old: TestGetSegmentsFromNode.test_italic_segment_gets_its_own_run
        old: TestGetSegmentsFromNode.test_bold_sup_sub_segments
        old: TestGetSegmentsFromNode.test_nested_styles_combine_regardless_of_order
        """
        cases = [
            ('<p>Plain text only.</p>', [{'text': 'Plain text only.'}]),
            ('<p>A <italic>Genus species</italic> name.</p>',
             [{'text': 'A '}, {'text': 'Genus species', 'italic': True}, {'text': ' name.'}]),
            ('<p><bold>Bold</bold> and <sup>sup</sup> and <sub>sub</sub>.</p>',
             [{'text': 'Bold', 'bold': True}, {'text': ' and '},
              {'text': 'sup', 'superscript': True}, {'text': ' and '},
              {'text': 'sub', 'subscript': True}, {'text': '.'}]),
            ('<p>A <sup><italic>one</italic></sup> and <italic><sup>two</sup></italic> case.</p>',
             [{'text': 'A '}, {'text': 'one', 'italic': True, 'superscript': True},
              {'text': ' and '}, {'text': 'two', 'italic': True, 'superscript': True},
              {'text': ' case.'}]),
        ]
        for source, expected in cases:
            with self.subTest(source=source):
                self.assertEqual(runs_of(source), expected)

    def test_adjacent_unstyled_fragments_merge(self):
        """
        old: TestGetSegmentsFromNode.test_adjacent_unstyled_fragments_merge_into_one_segment
        old: TestGetSegmentsFromNode.test_punctuation_spacing_normalized_like_get_text_from_node

        diferença intencional: <xref> com @rid vira link interno (anchor),
        então seu texto fica num run próprio.
        """
        cases = [
            ('<p>Start <xref ref-type="bibr">Text</xref> end.</p>', 'Start Text end.'),
            ('<p>seen (<xref ref-type="bibr">Author, 2020</xref>; '
             '<xref ref-type="bibr">Other, 2021</xref>) here</p>',
             'seen (Author, 2020; Other, 2021) here'),
        ]
        for source, expected in cases:
            with self.subTest(source=source):
                self.assertEqual(runs_of(source), [{'text': expected}])
        self.assertEqual(
            runs_of('<p>Start <xref ref-type="bibr" rid="B1 B2">Text</xref> end.</p>'),
            [{'text': 'Start '}, {'text': 'Text', 'anchor': 'B1'}, {'text': ' end.'}],
        )

    def test_skipped_child_drops_content_but_keeps_tail(self):
        """old: TestGetSegmentsFromNode.test_skip_tags_drops_content_but_keeps_tail"""
        self.assertEqual(
            runs_of('<p>Before <fig id="f1"><label>Figure 1</label></fig> after</p>', {'fig'}),
            [{'text': 'Before after'}],
        )

    def test_leading_and_trailing_whitespace_stripped(self):
        """old: TestGetSegmentsFromNode.test_leading_and_trailing_whitespace_stripped"""
        self.assertEqual(runs_of('<p>  padded text  </p>'), [{'text': 'padded text'}])

    def test_empty_node_returns_no_runs(self):
        """old: TestGetSegmentsFromNode.test_empty_node_returns_no_segments"""
        self.assertEqual(runs_of('<p><italic></italic></p>'), [])


MATH = '<mml:math><mml:mi>{}</mml:mi></mml:math>'


class InlineFormulaTest(unittest.TestCase):
    """
    Fórmula inline (antigo formula_tags/formula_converter).

    diferença intencional: não há conversor injetável; <inline-formula> e
    <mml:math> são sempre tratados por extract/formula.py e viram run
    {"omml": ...}; sem MathML, o conteúdo vira texto.
    """

    def formula_runs(self, body):
        """Runs normalizados de um <p> com o namespace mml."""
        return normalize(inlines(xml(f'<p {NS}>{body}</p>')))

    def shape(self, runs):
        """Runs com a fórmula reduzida a "omml" para comparação."""
        return ['omml' if 'omml' in r else r for r in runs]

    def test_formula_in_the_middle_of_text_is_its_own_run(self):
        """old: TestGetSegmentsFromNodeFormulaTags.test_formula_tag_in_the_middle_of_text_becomes_its_own_segment"""
        runs = self.formula_runs(
            f'where <inline-formula id="e1">{MATH.format("x")}</inline-formula> is the mean.')
        self.assertEqual(self.shape(runs), [{'text': 'where '}, 'omml', {'text': ' is the mean.'}])

    def test_multiple_formulas_are_not_merged(self):
        """old: TestGetSegmentsFromNodeFormulaTags.test_multiple_formula_tags_are_not_merged_with_each_other_or_with_text"""
        runs = self.formula_runs(
            f'If <inline-formula id="e1">{MATH.format("A")}</inline-formula> and '
            f'<inline-formula id="e2">{MATH.format("B")}</inline-formula> hold.')
        self.assertEqual(self.shape(runs), [
            {'text': 'If '}, 'omml', {'text': ' and '}, 'omml', {'text': ' hold.'},
        ])

    def test_formula_at_start_and_end_is_kept(self):
        """old: TestGetSegmentsFromNodeFormulaTags.test_formula_segment_at_start_and_end_of_node_does_not_get_stripped_or_dropped"""
        runs = self.formula_runs(
            f'<inline-formula id="e1">{MATH.format("A")}</inline-formula> in the middle '
            f'<inline-formula id="e2">{MATH.format("B")}</inline-formula>')
        self.assertEqual(self.shape(runs), ['omml', {'text': ' in the middle '}, 'omml'])

    def test_formula_without_mathml_falls_back_to_text(self):
        """
        old: TestGetSegmentsFromNodeFormulaTags.test_formula_converter_returning_none_falls_back_to_flattened_text
        old: TestGetSegmentsFromNodeFormulaTags.test_formula_tag_without_converter_falls_back_to_flattened_text
        old: TestGetSegmentsFromNodeFormulaTags.test_no_formula_tags_keeps_default_flattening_behavior
        """
        cases = [
            ('where <inline-formula id="e1"><bad/></inline-formula> is undefined.',
             [{'text': 'where is undefined.'}]),
            ('where <inline-formula>x</inline-formula> is x.', [{'text': 'where x is x.'}]),
            ('where <inline-formula><tex-math>\\alpha</tex-math></inline-formula> is a.',
             [{'text': 'where \\alpha is a.'}]),
        ]
        for body, expected in cases:
            with self.subTest(body=body):
                self.assertEqual(self.formula_runs(body), expected)


class MixedCitationTest(unittest.TestCase):
    """Parágrafo de referência a partir do <mixed-citation> (antigo get_text_from_mixed_citation_node)."""

    def test_reference_text_ends_with_period(self):
        """
        old: TestGetTextFromMixedCitationNode.test_get_text_from_mixed_citation_node_with_simple_text
        old: TestGetTextFromMixedCitationNode.test_get_text_from_mixed_citation_node_with_italic
        old: TestGetTextFromMixedCitationNode.test_get_text_from_mixed_citation_node_with_multiple_elements
        old: TestGetTextFromMixedCitationNode.test_get_text_from_mixed_citation_node_with_empty_elements
        old: TestGetTextFromMixedCitationNode.test_get_text_from_mixed_citation_node_already_has_period
        old: TestGetTextFromMixedCitationNode.test_get_text_from_mixed_citation_node_with_nested_tail_text
        old: TestGetTextFromMixedCitationNode.test_get_text_from_mixed_citation_node_keeps_nested_text_and_tail
        old: TestGetTextFromMixedCitationNode.test_get_text_from_mixed_citation_node_link_between_brackets
        old: TestGetTextFromMixedCitationNode.test_get_text_from_mixed_citation_node_keeps_balanced_nested_parentheses
        """
        cases = [
            ('Simple reference text', 'Simple reference text.'),
            ('Text with <italic>italicized</italic> content', 'Text with italicized content.'),
            ('Author A, <italic>Title B</italic>, <bold>Journal C</bold>',
             'Author A, Title B, Journal C.'),
            ('Text <italic></italic> with <bold></bold> empty elements',
             'Text with empty elements.'),
            ('Reference ending with period.', 'Reference ending with period.'),
            ('Start <italic>italic</italic> middle <bold>bold</bold> end',
             'Start italic middle bold end.'),
            ('Author. <italic>Title <sup>2</sup> part</italic>. City', 'Author. Title 2 part. City.'),
            ('Quim. Nova 2006, 29, 338. [<ext-link ext-link-type="uri" '
             'xlink:href="https://doi.org/10.1590/S0100-40422006000200028">Link</ext-link>]',
             'Quim. Nova 2006, 29, 338. [Link].'),
            ('Title ((A) and (B)). City', 'Title ((A) and (B)). City.'),
        ]
        for citation, expected in cases:
            with self.subTest(citation=citation):
                block = reference(f'<mixed-citation>{citation}</mixed-citation>')
                self.assertEqual(block['role'], 'reference')
                self.assertEqual(runs_text(block['runs']), expected)

    def test_reference_keeps_formatting_and_links(self):
        """
        old: TestGetTextFromMixedCitationNode.test_get_text_from_mixed_citation_node_with_multiple_elements
        old: TestGetTextFromMixedCitationNode.test_get_text_from_mixed_citation_node_keeps_nested_text_and_tail
        old: TestGetTextFromMixedCitationNode.test_get_text_from_mixed_citation_node_link_between_brackets

        diferença intencional: o old_pdf achatava em texto; agora itálico,
        negrito, sobrescrito e link ficam nos runs.
        """
        runs = reference('<mixed-citation>Author. <italic>Title <sup>2</sup> part</italic>. '
                         '<bold>J</bold> [<ext-link xlink:href="https://doi.org/x">Link</ext-link>]'
                         '</mixed-citation>')['runs']
        self.assertEqual(runs, [
            {'text': 'Author. '},
            {'text': 'Title ', 'italic': True},
            {'text': '2', 'italic': True, 'superscript': True},
            {'text': ' part', 'italic': True},
            {'text': '. '},
            {'text': 'J', 'bold': True},
            {'text': ' ['},
            {'text': 'Link', 'href': 'https://doi.org/x'},
            {'text': '].'},
        ])

    def test_link_nested_in_comment_is_kept(self):
        """
        old: TestGetTextFromMixedCitationNode.test_get_text_from_mixed_citation_node_keeps_link_nested_in_comment
        """
        url = 'https://metocean.com/wp-content/uploads/2017/09/iSPHERE-3.pdf'
        block = reference(
            '<mixed-citation>METOCEAN. 2017. iSPHERE. Nova Scotia, Dartmouth. Available from:\n'
            '  <comment>Available from:\n'
            f'    <ext-link ext-link-type="uri" xlink:href="{url}">{url}</ext-link>\n'
            '  </comment>. Access date: 2025 Mar. 27.</mixed-citation>')
        self.assertEqual(
            runs_text(block['runs']),
            'METOCEAN. 2017. iSPHERE. Nova Scotia, Dartmouth. Available from: Available from: '
            f'{url} . Access date: 2025 Mar. 27.',
        )
        self.assertIn({'text': url, 'href': url}, block['runs'])

    def test_link_in_comment_between_parentheses(self):
        """old: TestGetTextFromMixedCitationNode.test_get_text_from_mixed_citation_node_link_in_comment_between_parentheses"""
        url = 'https://CRAN.R-project.org/package=adiv'
        block = reference(
            '<mixed-citation>Pavoine, S. 2018. adiv: Analysis of Diversity. R package version 1.2. '
            f'(<comment> (<ext-link ext-link-type="uri" xlink:href="{url}">{url}</ext-link> '
            '</comment>). Accessed on July 2022.</mixed-citation>')
        self.assertEqual(
            runs_text(block['runs']),
            'Pavoine, S. 2018. adiv: Analysis of Diversity. R package version 1.2. '
            f'({url}). Accessed on July 2022.',
        )


class HeadingLevelTest(unittest.TestCase):
    """
    Nível de título (antigo get_node_level).

    diferença intencional: não há função de nível por profundidade no XML;
    o nível vem do aninhamento de <sec> (corpo = 1, <sec> = título 2,
    subseção = 3...). Só elementos de seção contam.
    """

    def test_body_without_sections_has_no_heading(self):
        """old: TestGetNodeLevel.test_get_node_level_root_element"""
        self.assertEqual(headings('<p>text</p>'), [])

    def test_nesting_sets_level(self):
        """
        old: TestGetNodeLevel.test_get_node_level_first_level
        old: TestGetNodeLevel.test_get_node_level_second_level
        old: TestGetNodeLevel.test_get_node_level_deep_nesting
        """
        self.assertEqual(
            headings('<sec><title>A</title><sec><title>B</title><sec><title>C</title>'
                     '<sec><title>D</title><p>text</p></sec></sec></sec></sec>'),
            [(2, 'A'), (3, 'B'), (4, 'C'), (5, 'D')],
        )

    def test_sibling_sections_share_level(self):
        """old: TestGetNodeLevel.test_get_node_level_sibling_elements"""
        self.assertEqual(
            headings('<sec><title>A</title><p>text1</p></sec><sec><title>B</title><p>text2</p></sec>'),
            [(2, 'A'), (2, 'B')],
        )

    def test_level_comes_from_context_not_from_tree_position(self):
        """
        old: TestGetNodeLevel.test_get_node_level_detached_element
        old: TestGetNodeLevel.test_get_node_level_complex_structure

        Seção solta ou dentro de elementos que não são seção recebe o nível
        do contexto + 1; o título mantém a formatação.
        """
        for wrapper, ctx in [('<x>{}</x>', {}), ('<x>{}</x>', {'level': 3}),
                             ('<body><wrapper><div>{}</div></wrapper></body>', {})]:
            with self.subTest(wrapper=wrapper, ctx=ctx):
                node = xml(wrapper.format(
                    '<sec><title><bold>Text</bold> <italic>More text</italic></title><p>x</p></sec>'))
                (heading,) = [b for b in extract(node, **ctx) if b['type'] == 'heading']
                self.assertEqual(heading['level'], ctx.get('level', 1) + 1)
                self.assertEqual(heading['runs'], [
                    {'text': 'Text', 'bold': True}, {'text': ' '},
                    {'text': 'More text', 'italic': True},
                ])


if __name__ == '__main__':
    unittest.main()
