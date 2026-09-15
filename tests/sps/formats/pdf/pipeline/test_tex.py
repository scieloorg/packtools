import unittest

from lxml import etree

from packtools.sps.formats.pdf.pipeline import tex

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
        result = tex.normalize_empty_base_superscripts(math)
        # The msub is no longer a direct sibling of msup - it's now msup's
        # own base (first child), and the empty mrow placeholder is gone.
        top_level_tags = [etree.QName(c).localname for c in result]
        self.assertEqual(top_level_tags, ['msup'])
        msup = result[0]
        self.assertEqual(etree.QName(msup[0]).localname, 'msub')
        self.assertEqual(''.join(msup[1].itertext()), '0.5')

    def test_leaves_normal_msup_untouched(self):
        math = _mathml('<msup><mi>x</mi><mn>2</mn></msup>')
        result = tex.normalize_empty_base_superscripts(math)
        msup = result[0]
        self.assertEqual(etree.QName(msup[0]).localname, 'mi')
        self.assertEqual(msup[0].text, 'x')

    def test_msup_with_no_preceding_sibling_is_left_untouched(self):
        # No element to merge with - left as-is (still produces an empty
        # box if converted, but that's an edge case out of this phase's
        # scope: not seen in the real corpus).
        math = _mathml('<msup><mrow/><mrow><mn>0.5</mn></mrow></msup>')
        result = tex.normalize_empty_base_superscripts(math)
        msup = result[0]
        self.assertEqual(etree.QName(msup[0]).localname, 'mrow')
        self.assertEqual(len(msup[0]), 0)

    def test_does_not_mutate_the_input_element(self):
        math = _mathml(
            '<msub><mi>x</mi><mn>1</mn></msub>'
            '<msup><mrow/><mrow><mn>0.5</mn></mrow></msup>'
        )
        original_tags = [etree.QName(c).localname for c in math]
        tex.normalize_empty_base_superscripts(math)
        self.assertEqual([etree.QName(c).localname for c in math], original_tags)

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
        result = tex.normalize_empty_base_superscripts(math)
        top_level_tags = [etree.QName(c).localname for c in result]
        self.assertEqual(top_level_tags, ['msup', 'msup'])
        for msup in result:
            self.assertEqual(etree.QName(msup[0]).localname, 'msub')


class TestMathmlToOmml(unittest.TestCase):

    def test_converts_simple_expression_to_omath(self):
        math = _mathml('<mi>Y</mi><mo>=</mo><mn>1</mn>')
        omml = tex.mathml_to_omml(math)
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
        omml = tex.mathml_to_omml(math)
        self.assertIsNotNone(omml)
        omml_str = etree.tostring(omml, encoding='unicode')
        # A leftover empty base would show up as an <m:e/> with no
        # children right before the superscript's own <m:sup> - assert
        # there's no completely empty <m:e></m:e> anywhere in the output.
        self.assertNotIn('<m:e></m:e>', omml_str)
        self.assertNotIn('<m:e/>', omml_str)

    def test_returns_none_for_unsupported_construct(self):
        # mathml2omml raises NotImplementedError for a tag it doesn't
        # recognize - mathml_to_omml must swallow that and return None
        # rather than let it propagate (one bad formula must not abort
        # the whole article's generation, same principle as issue #1371).
        math = _mathml('<not-a-real-mathml-tag/>')
        self.assertIsNone(tex.mathml_to_omml(math))
