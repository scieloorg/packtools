import unittest

from lxml import etree

from packtools.sps.formats.pdf.extract import formula_segments

_MML = 'xmlns:mml="http://www.w3.org/1998/Math/MathML"'
_MATH = '<mml:math><mml:mi>x</mml:mi></mml:math>'


def _xml(body):
    return etree.fromstring(f'<root {_MML}>{body}</root>')[0]


class TestInlineFormulaSegment(unittest.TestCase):

    def test_converts_mathml(self):
        segment = formula_segments.inline_formula_segment(_xml(f'<inline-formula>{_MATH}</inline-formula>'))
        self.assertEqual(segment['type'], 'formula')
        self.assertEqual(etree.QName(segment['omml']).localname, 'oMath')
        self.assertNotIn('display', segment)

    def test_none_without_mathml(self):
        self.assertIsNone(formula_segments.inline_formula_segment(_xml('<inline-formula>x</inline-formula>')))


class TestDispFormulaSegments(unittest.TestCase):

    def test_formula_then_label(self):
        segments = formula_segments.disp_formula_segments(
            _xml(f'<disp-formula><label>(1)</label>{_MATH}</disp-formula>')
        )
        self.assertEqual(segments[0]['type'], 'formula')
        self.assertTrue(segments[0]['display'])
        self.assertEqual(segments[1]['text'], ' (1)')

    def test_without_label(self):
        segments = formula_segments.disp_formula_segments(_xml(f'<disp-formula>{_MATH}</disp-formula>'))
        self.assertEqual(len(segments), 1)

    def test_none_without_mathml(self):
        self.assertIsNone(formula_segments.disp_formula_segments(_xml('<disp-formula><graphic/></disp-formula>')))


class TestParagraphWithTrailingFormula(unittest.TestCase):

    def test_leading_text_then_formula(self):
        segments = formula_segments.paragraph_with_trailing_formula(
            _xml(f'<p>Onde: <disp-formula>{_MATH}</disp-formula></p>')
        )
        self.assertEqual(segments[0]['text'], 'Onde:')
        self.assertEqual(segments[-1]['type'], 'formula')

    def test_none_when_content_follows_formula(self):
        self.assertIsNone(formula_segments.paragraph_with_trailing_formula(
            _xml(f'<p>a <disp-formula>{_MATH}</disp-formula> b</p>')
        ))

    def test_none_with_two_formulas(self):
        self.assertIsNone(formula_segments.paragraph_with_trailing_formula(
            _xml(f'<p><disp-formula>{_MATH}</disp-formula><disp-formula>{_MATH}</disp-formula></p>')
        ))

    def test_none_without_formula(self):
        self.assertIsNone(formula_segments.paragraph_with_trailing_formula(_xml('<p>text</p>')))


if __name__ == '__main__':
    unittest.main()
