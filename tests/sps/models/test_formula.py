import unittest
from lxml import etree

from packtools.sps.models.formula import Formula, ArticleFormulas


class DispFormulaTest(unittest.TestCase):
    def setUp(self):
        xml = (
            r'<article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            r'dtd-version="1.0" article-type="research-article" xml:lang="pt">'
            r"<body>"
            r'<disp-formula id="e10">'
            r"<label>(1)</label>"
            r"<alternatives>"
            r'<tex-math id="tx1">'
            r"\documentclass {article}"
            r"\usepackage{wasysym}"
            r"\usepackage[substack]{amsmath}"
            r"\usepackage{amsfonts}"
            r"\usepackage{amssymb}"
            r"\usepackage{amsbsy}"
            r"\usepackage[mathscr]{eucal}"
            r"\usepackage{mathrsfs}"
            r"\usepackage{pmc}"
            r"\usepackage[Euler]{upgreek}"
            r"\pagestyle{empty}\oddsidemargin -1.0in"
            r"\begin{document}"
            r"\[E_it=α_i+Z_it γ+W_it δ+C_it θ+∑_i^n EFind_i+∑_t^n EFtemp_t+ ε_it\]"
            r"\end{document}"
            r"</tex-math>"
            r'<graphic xlink:href="nomedaimagemdatabela.svg"/>'
            r"</alternatives>"
            r"</disp-formula>"
            r"</body>"
            r"</article>"
        )

        self.xmltree = etree.fromstring(xml)
        self.disp_formula_element = self.xmltree.xpath("//disp-formula")[0]
        self.disp_formula_obj = Formula(self.disp_formula_element)

    def test_disp_formula_id(self):
        self.assertEqual(self.disp_formula_obj.formula_id, "e10")

    def test_disp_formula_label(self):
        self.assertEqual(self.disp_formula_obj.formula_label, "(1)")

    def test_alternative_elements(self):
        self.assertListEqual(
            self.disp_formula_obj.alternative_elements, ["tex-math", "graphic"]
        )

    def test_data(self):
        self.maxDiff = None
        expected_data = {
            "alternative_parent": "disp-formula",
            "id": "e10",
            "label": "(1)",
            "alternative_elements": ["tex-math", "graphic"],
            "mml_math": None,
            "mml_math_id": None,
            "tex_math": '\\documentclass {article}'
                        '\\usepackage{wasysym}'
                        '\\usepackage[substack]{amsmath}'
                        '\\usepackage{amsfonts}'
                        '\\usepackage{amssymb}'
                        '\\usepackage{amsbsy}'
                        '\\usepackage[mathscr]{eucal}'
                        '\\usepackage{mathrsfs}'
                        '\\usepackage{pmc}'
                        '\\usepackage[Euler]{upgreek}'
                        '\\pagestyle{empty}'
                        '\\oddsidemargin -1.0in'
                        '\\begin{document}'
                        '\\[E_it=α_i+Z_it γ+W_it δ+C_it θ+∑_i^n EFind_i+∑_t^n EFtemp_t+ ε_it'
                        '\\]'
                        '\\end{document}',
            "tex_math_id": "tx1",
            "graphic": ["nomedaimagemdatabela.svg"],
        }
        self.assertDictEqual(self.disp_formula_obj.data, expected_data)


class InLineFormulaTest(unittest.TestCase):
    def setUp(self):
        xml = (
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'dtd-version="1.0" article-type="research-article" xml:lang="pt">'
            "<body>"
            "<inline-formula>"
            "<alternatives>"
            '<mml:math id="e03">'
            "<mml:mrow>"
            "<mml:msup>"
            '<mml:mover accent="true">'
            "<mml:mi>σ</mml:mi>"
            "<mml:mo>ˆ</mml:mo>"
            "</mml:mover>"
            "<mml:mn>2</mml:mn>"
            "</mml:msup>"
            "</mml:mrow>"
            "</mml:math>"
            '<graphic xlink:href="nomedaimagemdatabela.svg"/>'
            "</alternatives>"
            "</inline-formula>"
            "</body>"
            "</article>"
        )

        self.xmltree = etree.fromstring(xml)
        self.inline_formula_element = self.xmltree.xpath("//inline-formula")[0]
        self.inline_formula_obj = Formula(self.inline_formula_element)

    def test_alternative_elements(self):
        self.assertListEqual(
            self.inline_formula_obj.alternative_elements,
            ["{http://www.w3.org/1998/Math/MathML}math", "graphic"],
        )

    def test_data(self):
        self.maxDiff = None
        expected_data = {
            "alternative_parent": "inline-formula",
            "id": None,
            "label": None,
            "alternative_elements": [
                "{http://www.w3.org/1998/Math/MathML}math",
                "graphic",
            ],
            "mml_math": "σˆ2",
            "mml_math_id": "e03",
            "tex_math": None,
            "tex_math_id": None,
            "graphic": ["nomedaimagemdatabela.svg"],
        }
        self.assertDictEqual(self.inline_formula_obj.data, expected_data)


class ArticleFormulasTest(unittest.TestCase):
    def setUp(self):
        xml = (
            r'<article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            r'dtd-version="1.0" article-type="research-article" xml:lang="pt">'
            r"<body>"
            r'<disp-formula id="e10">'
            r"<label>(1)</label>"
            r"<alternatives>"
            r'<tex-math id="tx1">'
            r"\documentclass {article}"
            r"\usepackage{wasysym}"
            r"\usepackage[substack]{amsmath}"
            r"\usepackage{amsfonts}"
            r"\usepackage{amssymb}"
            r"\usepackage{amsbsy}"
            r"\usepackage[mathscr]{eucal}"
            r"\usepackage{mathrsfs}"
            r"\usepackage{pmc}"
            r"\usepackage[Euler]{upgreek}"
            r"\pagestyle{empty}\oddsidemargin -1.0in"
            r"\begin{document}"
            r"\[E_it=α_i+Z_it γ+W_it δ+C_it θ+∑_i^n EFind_i+∑_t^n EFtemp_t+ ε_it\]"
            r"\end{document}"
            r"</tex-math>"
            r'<graphic xlink:href="nomedaimagemdatabela.svg"/>'
            r"</alternatives>"
            r"</disp-formula>"
            r"</body>"
            r"</article>"
        )
        self.xmltree = etree.fromstring(xml)

    def test_disp_formula_items(self):
        self.maxDiff = None
        obtained =list(ArticleFormulas(self.xmltree).disp_formula_items)

        expected = [
            {
                "alternative_parent": "disp-formula",
                "id": "e10",
                "label": "(1)",
                "mml_math": None,
                "mml_math_id": None,
                "alternative_elements": ["tex-math", "graphic"],
                "parent": "article",
                "parent_article_type": "research-article",
                "parent_id": None,
                "parent_lang": "pt",
                "tex_math": '\\documentclass {article}'
                            '\\usepackage{wasysym}'
                            '\\usepackage[substack]{amsmath}'
                            '\\usepackage{amsfonts}'
                            '\\usepackage{amssymb}'
                            '\\usepackage{amsbsy}'
                            '\\usepackage[mathscr]{eucal}'
                            '\\usepackage{mathrsfs}'
                            '\\usepackage{pmc}'
                            '\\usepackage[Euler]{upgreek}'
                            '\\pagestyle{empty}'
                            '\\oddsidemargin -1.0in'
                            '\\begin{document}'
                            '\\[E_it=α_i+Z_it γ+W_it δ+C_it θ+∑_i^n EFind_i+∑_t^n EFtemp_t+ ε_it'
                            '\\]'
                            '\\end{document}',
                "tex_math_id": "tx1",
                "graphic": ["nomedaimagemdatabela.svg"],
            },
        ]

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(item, obtained[i])

    def test_disp_formula_items_by_lang(self):
        self.maxDiff = None
        obtained = ArticleFormulas(self.xmltree).disp_formula_items_by_lang

        expected = {
            "pt": {
                "alternative_parent": "disp-formula",
                "id": "e10",
                "label": "(1)",
                "mml_math": None,
                "mml_math_id": None,
                "alternative_elements": ["tex-math", "graphic"],
                "parent": "article",
                "parent_article_type": "research-article",
                "parent_id": None,
                "parent_lang": "pt",
                "tex_math": '\\documentclass {article}'
                            '\\usepackage{wasysym}'
                            '\\usepackage[substack]{amsmath}'
                            '\\usepackage{amsfonts}'
                            '\\usepackage{amssymb}'
                            '\\usepackage{amsbsy}'
                            '\\usepackage[mathscr]{eucal}'
                            '\\usepackage{mathrsfs}'
                            '\\usepackage{pmc}'
                            '\\usepackage[Euler]{upgreek}'
                            '\\pagestyle{empty}'
                            '\\oddsidemargin -1.0in'
                            '\\begin{document}'
                            '\\[E_it=α_i+Z_it γ+W_it δ+C_it θ+∑_i^n EFind_i+∑_t^n EFtemp_t+ ε_it'
                            '\\]'
                            '\\end{document}',
                "tex_math_id": "tx1",
                "graphic": ["nomedaimagemdatabela.svg"],
            },
        }

        for lang, item in expected.items():
            with self.subTest(lang):
                self.assertDictEqual(item, obtained[lang])


if __name__ == "__main__":
    unittest.main()
