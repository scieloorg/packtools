import unittest

from lxml import etree

from packtools.sps.formats.pdf.pipeline import formula

_MML_NS = 'http://www.w3.org/1998/Math/MathML'


def _mathml(body):
    return etree.fromstring(f'<math xmlns="{_MML_NS}">{body}</math>')


class TestNormalizeEmptyBaseSuperscripts(unittest.TestCase):
    """
    Regression for issue #1352: a5.xml's real MathML represents "x1^0.5"
    as <msub>x,1</msub> followed by a *separate* <msup> with an empty
    <mrow/> base, relying on visual adjacency - a literal conversion of
    that shape renders as a visible empty box glyph in Word/LibreOffice
    (confirmed by rendering a real PDF before this fix existed).
    """

    def test_merges_empty_base_msup_with_preceding_sibling(self):
        math = _mathml(
            '<msub><mi>x</mi><mn>1</mn></msub>'
            '<msup><mrow/><mrow><mn>0.5</mn></mrow></msup>'
        )
        result = formula.normalize_empty_base_superscripts(math)
        # The msub is no longer a direct sibling of msup - it's now msup's
        # own base (first child), and the empty mrow placeholder is gone.
        top_level_tags = [etree.QName(c).localname for c in result]
        self.assertEqual(top_level_tags, ['msup'])
        msup = result[0]
        self.assertEqual(etree.QName(msup[0]).localname, 'msub')
        self.assertEqual(''.join(msup[1].itertext()), '0.5')

    def test_leaves_normal_msup_untouched(self):
        math = _mathml('<msup><mi>x</mi><mn>2</mn></msup>')
        result = formula.normalize_empty_base_superscripts(math)
        msup = result[0]
        self.assertEqual(etree.QName(msup[0]).localname, 'mi')
        self.assertEqual(msup[0].text, 'x')

    def test_msup_with_no_preceding_sibling_is_left_untouched(self):
        # No element to merge with - left as-is (still produces an empty
        # box if converted, but that's an edge case out of this phase's
        # scope: not seen in the real corpus).
        math = _mathml('<msup><mrow/><mrow><mn>0.5</mn></mrow></msup>')
        result = formula.normalize_empty_base_superscripts(math)
        msup = result[0]
        self.assertEqual(etree.QName(msup[0]).localname, 'mrow')
        self.assertEqual(len(msup[0]), 0)

    def test_does_not_mutate_the_input_element(self):
        math = _mathml(
            '<msub><mi>x</mi><mn>1</mn></msub>'
            '<msup><mrow/><mrow><mn>0.5</mn></mrow></msup>'
        )
        original_tags = [etree.QName(c).localname for c in math]
        formula.normalize_empty_base_superscripts(math)
        self.assertEqual([etree.QName(c).localname for c in math], original_tags)

    def test_ignores_comment_nodes_in_the_tree(self):
        # comentário tem tag não-string; etree.QName() levantaria ValueError sem o filtro
        math = _mathml('<msup><mi>x</mi><mn>2</mn></msup><!-- nota -->')
        result = formula.normalize_empty_base_superscripts(math)
        top_level_tags = [etree.QName(c).localname for c in result if isinstance(c.tag, str)]
        self.assertEqual(top_level_tags, ['msup'])

    def test_handles_multiple_occurrences_in_the_same_math_element(self):
        # Regression: iterating root.iter() while mutating the tree in the
        # same pass skipped every other match - confirmed empirically
        # while validating this fix against a5.xml's real formulas (only
        # alternating x1^0.5/x2^0.5 terms got fixed before materializing
        # the candidate list up front).
        math = _mathml(
            '<msub><mi>x</mi><mn>1</mn></msub>'
            '<msup><mrow/><mrow><mn>0.5</mn></mrow></msup>'
            '<msub><mi>x</mi><mn>2</mn></msub>'
            '<msup><mrow/><mrow><mn>0.5</mn></mrow></msup>'
        )
        result = formula.normalize_empty_base_superscripts(math)
        top_level_tags = [etree.QName(c).localname for c in result]
        self.assertEqual(top_level_tags, ['msup', 'msup'])
        for msup in result:
            self.assertEqual(etree.QName(msup[0]).localname, 'msub')


class TestMathmlToOmml(unittest.TestCase):

    def test_converts_simple_expression_to_omath(self):
        math = _mathml('<mi>Y</mi><mo>=</mo><mn>1</mn>')
        omml = formula.mathml_to_omml(math)
        self.assertIsNotNone(omml)
        self.assertEqual(etree.QName(omml).localname, 'oMath')
        text = ''.join(omml.itertext())
        self.assertIn('Y', text)
        self.assertIn('1', text)

    def test_applies_empty_base_superscript_normalization(self):
        math = _mathml(
            '<msub><mi>x</mi><mn>1</mn></msub>'
            '<msup><mrow/><mrow><mn>0.5</mn></mrow></msup>'
        )
        omml = formula.mathml_to_omml(math)
        self.assertIsNotNone(omml)
        omml_str = etree.tostring(omml, encoding='unicode')
        # A leftover empty base would show up as an <m:e/> with no
        # children right before the superscript's own <m:sup> - assert
        # there's no completely empty <m:e></m:e> anywhere in the output.
        self.assertNotIn('<m:e></m:e>', omml_str)
        self.assertNotIn('<m:e/>', omml_str)

    def test_returns_none_for_unsupported_construct(self):
        # mathml2omml raises NotImplementedError para tag desconhecida; deve virar None, não propagar
        math = _mathml('<not-a-real-mathml-tag/>')
        self.assertIsNone(formula.mathml_to_omml(math))

    def test_does_not_abort_when_the_tree_contains_a_comment_node(self):
        math = _mathml('<mi>Y</mi><mo>=</mo><mn>1</mn><!-- nota -->')
        omml = formula.mathml_to_omml(math)
        self.assertIsNotNone(omml)

    def test_ignores_the_math_elements_own_tail_text(self):
        # texto após </math> no XML original vira .tail; não pode entrar na conversão
        container = etree.fromstring(
            f'<container xmlns="{_MML_NS}"><math><mi>Y</mi></math>, resto do texto</container>'
        )
        math = container[0]
        omml = formula.mathml_to_omml(math)
        self.assertIsNotNone(omml)

    def test_normalizes_plain_style_runs_from_mo_operators_in_table_rows(self):
        # <mo>+</mo> como último filho de <mtd> gera m:sty val="p"; o
        # LibreOffice não quebra a linha entre linhas de m:m/m:eqArr quando
        # o último run da linha tem esse estilo (glyph corrompido, linha
        # seguinte gruda na mesma linha e estoura a coluna)
        math = _mathml(
            '<mtable>'
            '<mtr><mtd><mi>a</mi><mo>+</mo></mtd></mtr>'
            '<mtr><mtd><mi>b</mi></mtd></mtr>'
            '</mtable>'
        )
        omml = formula.mathml_to_omml(math)
        self.assertIsNotNone(omml)
        omml_str = etree.tostring(omml, encoding='unicode')
        self.assertNotIn('m:val="p"', omml_str)


class TestNormalizePlainStyleRuns(unittest.TestCase):

    def _run_with_style(self, style_xml):
        return etree.fromstring(
            f'<m:oMath xmlns:m="{formula._OMML_NS}">'
            f'<m:r><m:rPr>{style_xml}</m:rPr><m:t>+</m:t></m:r>'
            f'</m:oMath>'
        )

    def test_replaces_plain_style_with_nor(self):
        omml = self._run_with_style('<m:sty m:val="p"/>')
        result = formula._normalize_plain_style_runs(omml)
        result_str = etree.tostring(result, encoding='unicode')
        self.assertNotIn('m:val="p"', result_str)
        self.assertIn('<m:nor/>', result_str)

    def test_leaves_other_styles_untouched(self):
        omml = self._run_with_style('<m:sty m:val="i"/>')
        result = formula._normalize_plain_style_runs(omml)
        result_str = etree.tostring(result, encoding='unicode')
        self.assertIn('m:val="i"', result_str)


class TestMatchParagraphFont(unittest.TestCase):

    def test_sets_size_and_font_on_every_run(self):
        math = _mathml('<mi>Y</mi><mo>=</mo><mn>1</mn>')
        omml = formula.mathml_to_omml(math)
        formula.match_paragraph_font(omml, 8.0, 'Noto Serif')

        w_ns = formula._W_NS
        runs = omml.findall(f'.//{{{formula._OMML_NS}}}r')
        self.assertGreater(len(runs), 0)
        for run in runs:
            # w:rPr é irmão de m:rPr dentro de m:r (schema CT_R), não filho dele
            w_rpr = run.find(f'{{{w_ns}}}rPr')
            self.assertIsNotNone(w_rpr)
            sz = w_rpr.find(f'{{{w_ns}}}sz')
            self.assertEqual(sz.get(f'{{{w_ns}}}val'), '16')
            rfonts = w_rpr.find(f'{{{w_ns}}}rFonts')
            self.assertEqual(rfonts.get(f'{{{w_ns}}}ascii'), 'Noto Serif')

    def test_rounds_half_point_size(self):
        omml = etree.fromstring(f'<m:oMath xmlns:m="{formula._OMML_NS}"><m:r><m:rPr/><m:t>x</m:t></m:r></m:oMath>')
        formula.match_paragraph_font(omml, 8.3, 'Arial')
        w_ns = formula._W_NS
        sz = omml.find(f'.//{{{w_ns}}}sz')
        self.assertEqual(sz.get(f'{{{w_ns}}}val'), '17')
