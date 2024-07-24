from unittest import TestCase
from packtools.sps.utils import xml_utils


from packtools.sps.models.formula import Formula
from lxml import etree


class FormulasTest(TestCase):
    def test_formula(self):
        xml = (r"""
			<article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" dtd-version="1.0" article-type="research-article" xml:lang="en">
				<front>
					<article-meta>
                        <disp-formula id="e3">
                            <mml:math id="m1" display="block">
                                <mml:mrow>
                                <mml:msub>
                                    <mml:mi>q</mml:mi>
                                    <mml:mi>c</mml:mi>
                                </mml:msub>
                                <mml:mo>=</mml:mo>
                                <mml:mi>h</mml:mi>
                                <mml:mrow>
                                    <mml:mo>(</mml:mo>
                                    <mml:mrow>
                                    <mml:mi>T</mml:mi>
                                    <mml:mo>−</mml:mo>
                                    <mml:msub>
                                        <mml:mi>T</mml:mi>
                                        <mml:mn>0</mml:mn>
                                    </mml:msub>
                                    </mml:mrow>
                                    <mml:mo>)</mml:mo>
                                </mml:mrow>
                                </mml:mrow>
                            </mml:math>
                            <label>(3)</label>
                        </disp-formula>
                        <disp-formula id="e10">
                            <label>(1)</label>
                            <tex-math id="tx1">
                                \documentclass {article}
                                \usepackage{wasysym}
                                \usepackage[substack]{amsmath}
                                \usepackage{amsfonts}
                                \usepackage{amssymb}
                                \usepackage{amsbsy}
                                \usepackage[mathscr]{eucal}
                                \usepackage{mathrsfs}
                                \usepackage{pmc}
                                \usepackage[Euler]{upgreek}
                                \pagestyle{empty}
                                \oddsidemargin -1.0in
                                \begin{document}
                                \[E_it=α_i+Z_it γ+W_it δ+C_it θ+∑_i^n EFind_i+∑_t^n EFtemp_t+ ε_it                                 \]
                                \end{document}
                            </tex-math>
                        </disp-formula>
                        <disp-formula id="e1">
                            <graphic xlink:href="1234-5678-rctb-45-05-0110-e01.tif"/>
                        </disp-formula>
					</article-meta>
				</front>
			</article>
		""")

        xml = xml_utils.get_xml_tree(xml)
        extract = Formula(xml).extract_disp_formula

        expected_output = {
            'formulas': [
            {
            'disp_formula_id': 'e3', 
            'disp_formula_label': '(3)', 
            'equation': {
                'id': 'm1', 
                'eq': '<mml:mrow xmlns:mml="http://www.w3.org/1998/Math/MathML"><mml:msub><mml:mi>q</mml:mi><mml:mi>c</mml:mi></mml:msub><mml:mo>=</mml:mo><mml:mi>h</mml:mi><mml:mrow><mml:mo>(</mml:mo><mml:mrow><mml:mi>T</mml:mi><mml:mo>−</mml:mo><mml:msub><mml:mi>T</mml:mi><mml:mn>0</mml:mn></mml:msub></mml:mrow><mml:mo>)</mml:mo></mml:mrow></mml:mrow>'}
            }, 
            {
            'disp_formula_id': 'e10', 
            'disp_formula_label': '(1)', 
            'equation': {
                'id': 'tx1', 
                'eq': '\n                                \\documentclass {article}\n                                \\usepackage{wasysym}\n                                \\usepackage[substack]{amsmath}\n                                \\usepackage{amsfonts}\n                                \\usepackage{amssymb}\n                                \\usepackage{amsbsy}\n                                \\usepackage[mathscr]{eucal}\n                                \\usepackage{mathrsfs}\n                                \\usepackage{pmc}\n                                \\usepackage[Euler]{upgreek}\n                                \\pagestyle{empty}\n                                \\oddsidemargin -1.0in\n                                \\begin{document}\n                                \\[E_it=α_i+Z_it γ+W_it δ+C_it θ+∑_i^n EFind_i+∑_t^n EFtemp_t+ ε_it                                 \\]\n                                \\end{document}\n                            '}
            }, 
            {
            'disp_formula_id': 'e1', 
            'disp_formula_label': '', 
            'equation': {
                'id': '', 
                'graphic': '1234-5678-rctb-45-05-0110-e01.tif'}
            }
            ]
        }