# coding: utf-8
from __future__ import unicode_literals
import unittest
import io
from lxml import etree

from packtools import domain


NAMESPACES = {
    "xlink": "http://www.w3.org/1999/xlink",
}


def _get_text_node(node):
    return etree.tostring(node, pretty_print=True).decode("utf-8")


def _print_debug(node):
    print(_get_text_node(node))


def get_xml_tree_from_string(text='<a><b>bar</b></a>'):
    return etree.parse(io.BytesIO(text.encode('utf-8')))


def _get_xml(text):
    xml = (
    f"""<article article-type="research-article" dtd-version="1.1"
    specific-use="sps-1.8" xml:lang="pt"
    xmlns:mml="http://www.w3.org/1998/Math/MathML"
    xmlns:xlink="http://www.w3.org/1999/xlink">
      <body>
        <sec>
        <p>The Eh measurements... <xref ref-type="disp-formula" rid="e01">Equação 1</xref>:</p>
        <p>
            {text}
        </p>
        <p>
        <disp-formula id="e02">
          <label>(2)</label>
          <mml:math xmlns:mml="http://www.w3.org/1998/Math/MathML" display="block">
            <mml:mrow>
              <mml:mrow>
                <mml:mrow>
                  <mml:mi>i</mml:mi>
                  <mml:mo>⁢</mml:mo>
                  <mml:mi mathvariant="normal">ℏ</mml:mi>
                  <mml:mo>⁢</mml:mo>
                  <mml:mfrac>
                    <mml:mrow>
                      <mml:mo>∂</mml:mo>
                      <mml:mo>⁡</mml:mo>
                      <mml:mi>ψ</mml:mi>
                    </mml:mrow>
                    <mml:mrow>
                      <mml:mo>∂</mml:mo>
                      <mml:mo>⁡</mml:mo>
                      <mml:mi>t</mml:mi>
                    </mml:mrow>
                  </mml:mfrac>
                </mml:mrow>
                <mml:mo>=</mml:mo>
                <mml:mrow>
                  <mml:mrow>
                    <mml:mo>-</mml:mo>
                    <mml:mrow>
                      <mml:mfrac>
                        <mml:msup>
                          <mml:mi mathvariant="normal">ℏ</mml:mi>
                          <mml:mn>2</mml:mn>
                        </mml:msup>
                        <mml:mrow>
                          <mml:mn>2</mml:mn>
                          <mml:mo>⁢</mml:mo>
                          <mml:mi>m</mml:mi>
                        </mml:mrow>
                      </mml:mfrac>
                      <mml:mo>⁢</mml:mo>
                      <mml:mrow>
                        <mml:msup>
                          <mml:mo>∇</mml:mo>
                          <mml:mn>2</mml:mn>
                        </mml:msup>
                        <mml:mo>⁡</mml:mo>
                        <mml:mi>ψ</mml:mi>
                      </mml:mrow>
                    </mml:mrow>
                  </mml:mrow>
                  <mml:mo>+</mml:mo>
                  <mml:mrow>
                    <mml:mi>U</mml:mi>
                    <mml:mo>⁢</mml:mo>
                    <mml:mi>ψ</mml:mi>
                  </mml:mrow>
                </mml:mrow>
              </mml:mrow>
              <mml:mo>.</mml:mo>
            </mml:mrow>
          </mml:math>
        </disp-formula>
        </p>
        </sec>
      </body>
    </article>"""
    )
    et = get_xml_tree_from_string(xml)
    return domain.HTMLGenerator.parse(et, valid_only=False).generate('pt')


class HTMLGenerator_LabelAndCaption_Tests(unittest.TestCase):

    def setUp(self):
        xml = """
            <disp-formula id="e01">
                <label>(1)</label>
                <graphic xlink:href="equation1.tif" />
            </disp-formula>
            """
        self.html = _get_xml(xml)

    def test_label_presentation(self):
        """
        <div class="row formula" id="ee01">
            <a name="e01"></a>
            <div class="col-md-12">
            <div class="formula-container">
                <math id="m1"><mrow><mi>D</mi><mo>=</mo><mfrac><mi>γ</mi><mrow><msqrt><mrow><msup><mi>β</mi><mn>2</mn></msup><mo>+</mo><mo> </mo><msubsup><mi>β</mi><mrow><mi>s</mi><mi>t</mi><mi>d</mi></mrow><mn>2</mn></msubsup><mo> </mo><mo> </mo><mi>c</mi><mi>o</mi><mi>s</mi><mi>θ</mi></mrow></msqrt></mrow></mfrac></mrow></math>
                <span class="label">(1)</span>
            </div>
        </div>
        """
        nodes = self.html.xpath(
            '//p'
            '/div[@class="row formula" and @id="ee01"]'
            '/div[@class="col-md-12"]'
            '/div[@class="formula-container"]'
            '/span[@class="label"]'
        )
        self.assertEqual(nodes[0].text, "(1)")

    def test_total_in_tabpanel(self):
        nodes = self.html.xpath(
            '//a[@href="#schemes" and @role="tab"]'
        )
        self.assertIn("(2)", nodes[0].text)

    @unittest.skip("skipping")  
    def test_thumbnail_label_in_tabpanel(self):
        """
        <div class="modal fade ModalDefault" id="ModalTablesFigures" tabindex="-1" role="dialog" aria-hidden="true">
            <div class="tab-content">
                <div role="tabpanel" class="tab-pane " id="schemes">
                    <div class="row fig">
                        <div class="col-md-4">
                            <a data-toggle="modal" data-target="#ModalSchemee1">
                                <div class="thumbOff">
                                        Thumbnail
                                    <div class="zoom">
                                        <span class="sci-ico-zoom"></span>
                                    </div>
                                </div>
                            </a>
                        </div>
                        <div class="col-md-8"><strong>(1)</strong></div>
        """
        nodes = self.html.xpath(
            '//div[@class="modal fade ModalDefault" and @id="ModalTablesFigures"]'
            '//div[@class="tab-content"]'
            '/div[@role="tabpanel" and @id="schemes"]'
            '//div[@class="row fig"]'
            '/div[@class="col-md-8"]'
            '/strong'
        )
        self.assertEqual(nodes[0].text, '(1)')

    def test_xref_presentation(self):
        nodes = self.html.xpath(
            '//a[@href="" and @class="open-asset-modal" and @data-target="#ModalSchemee01"]'
        )
        self.assertEqual(len(nodes), 1)


class HTMLGenerator_DispFormula_Graphic_Tiff_Tests(unittest.TestCase):
    def setUp(self):
        xml = """
            <disp-formula id="e01">
                <label>(1)</label>
                <graphic xlink:href="equation1.tif" />
            </disp-formula>
        """
        self.html = _get_xml(xml)

    def test_enlarged_presentation(self):
        nodes = self.html.xpath(
            '//div[@class="row formula" and @id="ee01"]'
            '/div[@class="col-md-12"]'
            '/div[@class="formula-container"]'
            '/img[@src="equation1.jpg"]'
        )
        self.assertEqual(len(nodes), 1)

    def test_enlarged_presentation_in_modal(self):
        nodes = self.html.xpath(
            '//div[@class="modal fade ModalFigs" and @id="ModalSchemee01"]'
            '/div[@class="modal-dialog modal-lg"]'
            '/div[@class="modal-content"]'
            '/div[@class="modal-body"]'
            '/img[@src="equation1.jpg"]'
        )
        self.assertEqual(len(nodes), 1)

    def test_thumbnail_presentation_in_tabpanel(self):
        nodes = self.html.xpath(
            '//div[@role="tabpanel" and @id="schemes"]'
            '/div[@class="row fig"]'
            '/div[@class="col-md-4"]'
            '/a[@data-target="#ModalSchemee01"]'
            '/div[@class="thumbOff"]'
        )
        self.assertEqual(len(nodes), 1)

    def test_original_presentation(self):
        nodes = self.html.xpath(
            '//div[@class="modal fade ModalFigs" and @id="ModalSchemee01"]'
            '//div[@class="modal-header"]'
            '/a[@class="link-newWindow showTooltip" and @target="_blank"]'
        )
        self.assertEqual(nodes[0].get("href"), "equation1.jpg")


class HTMLGenerator_DispFormula_Graphic_Png_Tests(unittest.TestCase):
    def setUp(self):
        xml = """
            <disp-formula id="e01">
                <label>(1)</label>
                <graphic xlink:href="equation1.png" />
            </disp-formula>
        """
        self.html = _get_xml(xml)

    def test_enlarged_presentation(self):
        nodes = self.html.xpath(
            '//div[@class="row formula" and @id="ee01"]'
            '/div[@class="col-md-12"]'
            '/div[@class="formula-container"]'
            '/img[@src="equation1.png"]'
        )
        self.assertEqual(len(nodes), 1)

    def test_enlarged_presentation_in_modal(self):
        nodes = self.html.xpath(
            '//div[@class="modal fade ModalFigs" and @id="ModalSchemee01"]'
            '/div[@class="modal-dialog modal-lg"]'
            '/div[@class="modal-content"]'
            '/div[@class="modal-body"]'
            '/img[@src="equation1.png"]'
        )
        self.assertEqual(len(nodes), 1)

    def test_thumbnail_presentation_in_tabpanel(self):
        nodes = self.html.xpath(
            '//div[@role="tabpanel" and @id="schemes"]'
            '/div[@class="row fig"]'
            '/div[@class="col-md-4"]'
            '/a[@data-target="#ModalSchemee01"]'
            '/div[@class="thumbOff"]'
        )
        self.assertEqual(len(nodes), 1)

    def test_original_presentation(self):
        nodes = self.html.xpath(
            '//div[@class="modal fade ModalFigs" and @id="ModalFigf01"]'
            '//div[@class="modal-header"]'
            '/a[@class="link-newWindow showTooltip" and @target="_blank"]'
        )
        self.assertEqual(len(nodes), 0)


class HTMLGenerator_DispFormula_Graphic_NoExtension_Tests(unittest.TestCase):
    def setUp(self):
        xml = """
            <disp-formula id="e01">
                <label>(1)</label>
                <graphic xlink:href="equation1" />
            </disp-formula>
        """
        self.html = _get_xml(xml)

    def test_enlarged_presentation(self):
        nodes = self.html.xpath(
            '//div[@class="row formula" and @id="ee01"]'
            '/div[@class="col-md-12"]'
            '/div[@class="formula-container"]'
            '/img[@src="equation1.jpg"]'
        )
        self.assertEqual(len(nodes), 1)

    def test_enlarged_presentation_in_modal(self):
        nodes = self.html.xpath(
            '//div[@class="modal fade ModalFigs" and @id="ModalSchemee01"]'
            '/div[@class="modal-dialog modal-lg"]'
            '/div[@class="modal-content"]'
            '/div[@class="modal-body"]'
            '/img[@src="equation1.jpg"]'
        )
        self.assertEqual(len(nodes), 1)

    def test_thumbnail_presentation_in_tabpanel(self):
        nodes = self.html.xpath(
            '//div[@role="tabpanel" and @id="schemes"]'
            '/div[@class="row fig"]'
            '/div[@class="col-md-4"]'
            '/a[@data-target="#ModalSchemee01"]'
            '/div[@class="thumbOff"]'
        )
        self.assertEqual(len(nodes), 1)

    def test_original_presentation(self):
        nodes = self.html.xpath(
            '//div[@class="modal fade ModalFigs" and @id="ModalSchemee01"]'
            '//div[@class="modal-header"]'
            '/a[@class="link-newWindow showTooltip" and @target="_blank"]'
        )
        self.assertEqual(nodes[0].get("href"), "equation1.jpg")


class HTMLGenerator_DispFormula_Graphic_SVG_Tests(unittest.TestCase):
    def setUp(self):
        xml = """
            <disp-formula id="e01">
                <label>(1)</label>
                <graphic xlink:href="equation1.svg" />
            </disp-formula>
        """
        self.html = _get_xml(xml)

    def test_enlarged_presentation(self):
        nodes = self.html.xpath(
            '//div[@class="row formula" and @id="ee01"]'
            '/div[@class="col-md-12"]'
            '/div[@class="formula-container"]'
            '//object[@data="equation1.svg"]'
        )
        self.assertEqual(len(nodes), 1)

    def test_enlarged_presentation_in_modal(self):
        nodes = self.html.xpath(
            '//div[@class="modal fade ModalFigs" and @id="ModalSchemee01"]'
            '/div[@class="modal-dialog modal-lg"]'
            '/div[@class="modal-content"]'
            '/div[@class="modal-body"]'
            '//object[@data="equation1.svg"]'
        )
        self.assertEqual(len(nodes), 1)

    def test_thumbnail_presentation_in_tabpanel(self):
        nodes = self.html.xpath(
            '//div[@role="tabpanel" and @id="schemes"]'
            '/div[@class="row fig"]'
            '/div[@class="col-md-4"]'
            '/a[@data-target="#ModalSchemee01"]'
            '/div[@class="thumbOff"]'
        )
        self.assertEqual(len(nodes), 1)

    def test_original_presentation(self):
        nodes = self.html.xpath(
            '//div[@class="modal fade ModalFigs" and @id="ModalSchemee01"]'
            '//div[@class="modal-header"]'
            '/a[@class="link-newWindow showTooltip" and @target="_blank"]'
        )
        self.assertEqual(nodes[0].get("href"), "equation1.svg")


class HTMLGenerator_Dispformula_Alternatives_Graphics_Tests(unittest.TestCase):
    def setUp(self):
        xml = """
            <disp-formula id="e01">
                <label>(1)</label>
                <alternatives>
                    <graphic xlink:href="original.tif" />
                    <graphic xlink:href="ampliada.png" specific-use="scielo-web" />
                    <graphic xlink:href="miniatura.jpg" specific-use="scielo-web" content-type="scielo-20x20" />
                </alternatives>
            </disp-formula>
        """
        self.html = _get_xml(xml)

    def test_enlarged_presentation(self):
        nodes = self.html.xpath(
            '//div[@class="row formula" and @id="ee01"]'
            '/div[@class="col-md-12"]'
            '/div[@class="formula-container"]'
            '/img[@src="ampliada.png"]'
        )
        self.assertEqual(len(nodes), 1)

    def test_enlarged_presentation_in_modal(self):
        nodes = self.html.xpath(
            '//div[@class="modal fade ModalFigs" and @id="ModalSchemee01"]'
            '/div[@class="modal-dialog modal-lg"]'
            '/div[@class="modal-content"]'
            '/div[@class="modal-body"]'
            '/img[@src="ampliada.png"]'
        )
        self.assertEqual(len(nodes), 1)

    def test_thumbnail_presentation_in_tabpanel(self):
        nodes = self.html.xpath(
            '//div[@role="tabpanel" and @id="schemes"]'
            '/div[@class="row fig"]'
            '/div[@class="col-md-4"]'
            '/a[@data-target="#ModalSchemee01"]'
            '/div[@class="thumbImg"]'
            '/img[@src="miniatura.jpg"]'
        )
        self.assertEqual(len(nodes), 1)

    def test_original_presentation(self):
        nodes = self.html.xpath(
            '//div[@class="modal fade ModalFigs" and @id="ModalSchemee01"]'
            '//div[@class="modal-header"]'
            '/a[@class="link-newWindow showTooltip" and @target="_blank"]'
        )
        self.assertEqual(nodes[0].get("href"), "original.tif")


class HTMLGenerator_Fig_Alternatives_TexAndSVG_Tests(unittest.TestCase):
    def setUp(self):
        xml = """
            <disp-formula id="e01">
            <alternatives>
<tex-math id="tx2"> \\documentclass {article} \\usepackage{wasysym} \\usepackage[substack]{amsmath} \\usepackage{amsfonts} \\usepackage{amssymb} \\usepackage{amsbsy} \\usepackage[mathscr]{eucal} \\usepackage{mathrsfs} \\usepackage{pmc} \\usepackage[Euler]{upgreek} \\pagestyle{empty} \\oddsidemargin -1.0in \\begin{document} \\[E\\widehat{Y\\left( 0 \\right)|D=1}=\\frac{\\mathop{\\sum }_{\\{i|D=0\\}}{{Y}_{i}}{{d}_{i}}}{\\mathop{\\sum }_{\\{i|D=0\\}}{{d}_{i}}}\\] \\end{document} </tex-math>
            <graphic xlink:href="original.svg"/>
            </alternatives>
            </disp-formula>
        """
        self.html = _get_xml(xml)

    def test_enlarged_presentation(self):
        nodes = self.html.xpath(
            '//div[@class="row formula" and @id="ee01"]'
            '/div[@class="col-md-12"]'
            '/div[@class="formula-container"]'
            '/span[@class="formula-body"]'
            '/span'
        )
        self.assertEqual(nodes[0].text, "\\[E\\widehat{Y\\left( 0 \\right)|D=1}=\\frac{\\mathop{\\sum }_{\\{i|D=0\\}}{{Y}_{i}}{{d}_{i}}}{\\mathop{\\sum }_{\\{i|D=0\\}}{{d}_{i}}}\\]")

    def test_enlarged_presentation_in_modal(self):
        nodes = self.html.xpath(
            '//div[@class="modal fade ModalFigs" and @id="ModalSchemee01"]'
            '/div[@class="modal-dialog modal-lg"]'
            '/div[@class="modal-content"]'
            '/div[@class="modal-body"]'
            '/span/span'
        )
        self.assertEqual(len(nodes), 1)

    def test_thumbnail_presentation(self):
        nodes = self.html.xpath(
            '//div[@role="tabpanel" and @id="schemes"]'
            '/div[@class="row fig"]'
            '/div[@class="col-md-4"]'
            '/a[@data-target="#ModalSchemee01"]'
            '/div[@class="thumbOff"]'
        )
        self.assertEqual(len(nodes), 1)

    def test_original_presentation(self):
        nodes = self.html.xpath(
            '//div[@class="modal fade ModalFigs" and @id="ModalSchemee01"]'
            '//div[@class="modal-header"]'
            '/a[@class="link-newWindow showTooltip" and @target="_blank"]'
        )
        self.assertEqual(nodes[0].get("href"), "original.svg")


class HTMLGenerator_Fig_Alternatives_MathAndSVG_Tests(unittest.TestCase):
    def setUp(self):
        xml = """
            <fig id="e01">
                <label>(1)</label>
                <caption>
                    <title>Caption Equação 1</title>
                </caption>
                <disp-formula id="e01">
                <alternatives><mml:math><mml:mi>τ</mml:mi><mml:mo>=</mml:mo><mml:mi>E</mml:mi><mml:mfenced close="]" open="[" separators="|"><mml:mrow><mml:mi>Y</mml:mi><mml:mfenced separators="|"><mml:mrow><mml:mn>1</mml:mn></mml:mrow></mml:mfenced></mml:mrow><mml:mrow><mml:mi>D</mml:mi><mml:mo>=</mml:mo><mml:mn>1</mml:mn></mml:mrow></mml:mfenced><mml:mo>-</mml:mo><mml:mi>E</mml:mi><mml:mo>[</mml:mo><mml:mi>Y</mml:mi><mml:mo>(</mml:mo><mml:mn>0</mml:mn><mml:mo>)</mml:mo><mml:mo>|</mml:mo><mml:mi>D</mml:mi><mml:mo>=</mml:mo><mml:mn>1</mml:mn><mml:mo>]</mml:mo></mml:math><graphic xlink:href="original.svg"/></alternatives>
                </disp-formula>
                
            </fig>
        """
        self.html = _get_xml(xml)

    def test_enlarged_presentation(self):
        nodes = self.html.xpath(
            '//div[@class="row formula" and @id="ee01"]'
            '/div[@class="col-md-12"]'
            '/div[@class="formula-container"]'
            '/math'
        )
        self.assertEqual(len(nodes), 1)

    def test_enlarged_presentation_in_modal(self):
        nodes = self.html.xpath(
            '//div[@class="modal fade ModalFigs" and @id="ModalSchemee01"]'
            '/div[@class="modal-dialog modal-lg"]'
            '/div[@class="modal-content"]'
            '/div[@class="modal-body"]'
            '/math'
        )
        self.assertEqual(len(nodes), 1)

    def test_thumbnail_presentation(self):
        nodes = self.html.xpath(
            '//div[@role="tabpanel" and @id="schemes"]'
            '/div[@class="row fig"]'
            '/div[@class="col-md-4"]'
            '/a[@data-target="#ModalSchemee01"]'
            '/div[@class="thumbOff"]'
        )
        self.assertEqual(len(nodes), 1)

    def test_original_presentation(self):
        nodes = self.html.xpath(
            '//div[@class="modal fade ModalFigs" and @id="ModalSchemee01"]'
            '//div[@class="modal-header"]'
            '/a[@class="link-newWindow showTooltip" and @target="_blank"]'
        )
        self.assertEqual(nodes[0].get("href"), "original.svg")


class HTMLGenerator_DispFormula_Tex_Tests(unittest.TestCase):
    def setUp(self):
        xml = """
            <fig id="e01">
                <label>(1)</label>
                <caption>
                    <title>Caption Equação 1</title>
                </caption>
                <disp-formula id="e01">
<tex-math id="tx2"> \\documentclass {article} \\usepackage{wasysym} \\usepackage[substack]{amsmath} \\usepackage{amsfonts} \\usepackage{amssymb} \\usepackage{amsbsy} \\usepackage[mathscr]{eucal} \\usepackage{mathrsfs} \\usepackage{pmc} \\usepackage[Euler]{upgreek} \\pagestyle{empty} \\oddsidemargin -1.0in \\begin{document} \\[E\\widehat{Y\\left( 0 \\right)|D=1}=\\frac{\\mathop{\\sum }_{\\{i|D=0\\}}{{Y}_{i}}{{d}_{i}}}{\\mathop{\\sum }_{\\{i|D=0\\}}{{d}_{i}}}\\] \\end{document} </tex-math>
                </disp-formula>
                
            </fig>
        """
        self.html = _get_xml(xml)

    def test_enlarged_presentation(self):
        nodes = self.html.xpath(
            '//div[@class="row formula" and @id="ee01"]'
            '/div[@class="col-md-12"]'
            '/div[@class="formula-container"]'
            '/span[@class="formula-body"]'
            '/span'
        )
        self.assertEqual(len(nodes), 1)

    def test_enlarged_presentation_in_modal(self):
        nodes = self.html.xpath(
            '//div[@class="modal fade ModalFigs" and @id="ModalSchemee01"]'
            '/div[@class="modal-dialog modal-lg"]'
            '/div[@class="modal-content"]'
            '/div[@class="modal-body"]'
            '/span/span'
        )
        self.assertEqual(len(nodes), 1)

    def test_thumbnail_presentation(self):
        nodes = self.html.xpath(
            '//div[@role="tabpanel" and @id="schemes"]'
            '/div[@class="row fig"]'
            '/div[@class="col-md-4"]'
            '/a[@data-target="#ModalSchemee01"]'
            '/div[@class="thumbOff"]'
        )
        self.assertEqual(len(nodes), 1)

    def test_original_presentation(self):
        nodes = self.html.xpath(
            '//div[@class="modal fade ModalFigs" and @id="ModalSchemee01"]'
            '//div[@class="modal-header"]'
            '/a[@class="link-newWindow showTooltip" and @target="_blank"]'
        )
        self.assertEqual(len(nodes), 0)


class HTMLGenerator_DispFormula_Math_Tests(unittest.TestCase):
    def setUp(self):
        xml = """
            <disp-formula id="e01">
          <label>(1)</label>
          <mml:math xmlns:mml="http://www.w3.org/1998/Math/MathML" display="block">
            <mml:mrow>
              <mml:mrow>
                <mml:mrow>
                  <mml:msub>
                    <mml:mover accent="true">
                      <mml:mi>c</mml:mi>
                      <mml:mo stretchy="false">^</mml:mo>
                    </mml:mover>
                    <mml:mi>j</mml:mi>
                  </mml:msub>
                  <mml:mo>⁢</mml:mo>
                  <mml:mrow>
                    <mml:mo fence="true" stretchy="false">|</mml:mo>
                    <mml:mn>0</mml:mn>
                    <mml:mo stretchy="false">⟩</mml:mo>
                  </mml:mrow>
                </mml:mrow>
                <mml:mo>=</mml:mo>
                <mml:mn>0</mml:mn>
              </mml:mrow>
              <mml:mo>,</mml:mo>
            </mml:mrow>
          </mml:math>
        </disp-formula>
        """
        self.html = _get_xml(xml)

    def test_enlarged_presentation_in_text(self):
        nodes = self.html.xpath(
            '//p'
            '/div[@class="row formula" and @id="ee01"]'
            '/div[@class="col-md-12"]'
            '/div[@class="formula-container"]'
            '/math'
        )
        self.assertEqual(len(nodes), 1)

    def test_enlarged_presentation_in_modal(self):
        nodes = self.html.xpath(
            '//div[@class="modal fade ModalFigs" and @id="ModalSchemee01"]'
            '/div[@class="modal-dialog modal-lg"]'
            '/div[@class="modal-content"]'
            '/div[@class="modal-body"]'
            '/math'
        )
        self.assertEqual(len(nodes), 1)

    def test_thumbnail_presentation(self):
        nodes = self.html.xpath(
            '//div[@role="tabpanel" and @id="schemes"]'
            '/div[@class="row fig"]'
            '/div[@class="col-md-4"]'
            '/a[@data-target="#ModalSchemee01"]'
            '/div[@class="thumbOff"]'
        )
        self.assertEqual(len(nodes), 1)

    def test_original_presentation(self):
        nodes = self.html.xpath(
            '//div[@class="modal fade ModalFigs" and @id="ModalSchemee01"]'
            '//div[@class="modal-header"]'
            '/a[@class="link-newWindow showTooltip" and @target="_blank"]'
        )
        self.assertEqual(len(nodes), 0)
