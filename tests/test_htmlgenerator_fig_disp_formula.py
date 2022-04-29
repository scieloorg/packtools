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
        <p>The Eh measurements... <xref ref-type="fig" rid="f01">Figura 1</xref>:</p>
        <p>
            {text}
        </p>
        <p>
        <fig id="f02">
            <label>Figura 2</label>
            <caption>
                <title>Caption Figura 2</title>
            </caption>
            <graphic xlink:href="figura2.jpg"/>
            <attrib>Fonte: Dados originais da pesquisa</attrib>
        </fig>
        </p>
        </sec>
      </body>
    </article>"""
    )
    et = get_xml_tree_from_string(xml)
    return domain.HTMLGenerator.parse(et, valid_only=False).generate('pt')


class HTMLGenerator_Fig_DispFormula_Graphic_Tiff_Tests(unittest.TestCase):
    def setUp(self):
        xml = """
            <fig id="f01">
                <label>Figura 1</label>
                <caption>
                    <title>Caption Figura 1</title>
                </caption>
                <disp-formula><graphic xlink:href="figure1.tif" /></disp-formula>
                <attrib>Fonte: Dados originais da pesquisa</attrib>
            </fig>
        """
        self.html = _get_xml(xml)

    def test_enlarged_presentation(self):
        nodes = self.html.xpath(
            '//div[@class="modal fade ModalFigs" and @id="ModalFigf01"]'
            '/div[@class="modal-dialog modal-lg"]'
            '/div[@class="modal-content"]'
            '/div[@class="modal-body"]'
            '/div[@class="row formula"]'
            '/div[@class="col-md-12"]'
            '/div[@class="formula-container"]'
            '/a[@href="figure1.jpg"]'
            '/img[@src="figure1.jpg"]'
        )
        self.assertEqual(len(nodes), 1)


class HTMLGenerator_Fig_DispFormula_Graphic_Png_Tests(unittest.TestCase):
    def setUp(self):
        xml = """
            <fig id="f01">
                <label>Figura 1</label>
                <caption>
                    <title>Caption Figura 1</title>
                </caption>
                <disp-formula><graphic xlink:href="figure1.png"/></disp-formula>
                <attrib>Fonte: Dados originais da pesquisa</attrib>
            </fig>
        """
        self.html = _get_xml(xml)

    def test_enlarged_presentation(self):
        nodes = self.html.xpath(
            '//div[@class="modal fade ModalFigs" and @id="ModalFigf01"]'
            '/div[@class="modal-dialog modal-lg"]'
            '/div[@class="modal-content"]'
            '/div[@class="modal-body"]'
            '/div[@class="row formula"]'
            '/div[@class="col-md-12"]'
            '/div[@class="formula-container"]'
            '/a[@href="figure1.png"]'
            '/img[@src="figure1.png"]'
        )
        self.assertEqual(len(nodes), 1)


class HTMLGenerator_Fig_DispFormula_Graphic_NoExtension_Tests(unittest.TestCase):
    def setUp(self):
        xml = """
            <fig id="f01">
                <label>Figura 1</label>
                <caption>
                    <title>Caption Figura 1</title>
                </caption>
                <disp-formula><graphic xlink:href="figure1"/></disp-formula>
                <attrib>Fonte: Dados originais da pesquisa</attrib>
            </fig>
        """
        self.html = _get_xml(xml)

    def test_enlarged_presentation(self):
        nodes = self.html.xpath(
            '//div[@class="modal fade ModalFigs" and @id="ModalFigf01"]'
            '/div[@class="modal-dialog modal-lg"]'
            '/div[@class="modal-content"]'
            '/div[@class="modal-body"]'
            '/div[@class="row formula"]'
            '/div[@class="col-md-12"]'
            '/div[@class="formula-container"]'
            '/a'
            '/img[@src="figure1.jpg"]'
        )
        self.assertEqual(len(nodes), 1)


class HTMLGenerator_Fig_DispFormula_Graphic_SVG_Tests(unittest.TestCase):
    def setUp(self):
        xml = """
            <fig id="f01">
                <label>Figura 1</label>
                <caption>
                    <title>Caption Figura 1</title>
                </caption>
                <disp-formula><graphic xlink:href="figure1.svg"/></disp-formula>
                <attrib>Fonte: Dados originais da pesquisa</attrib>
            </fig>
        """
        self.html = _get_xml(xml)

    def test_enlarged_presentation(self):
        nodes = self.html.xpath(
            '//div[@class="modal fade ModalFigs" and @id="ModalFigf01"]'
            '/div[@class="modal-dialog modal-lg"]'
            '/div[@class="modal-content"]'
            '/div[@class="modal-body"]'
            '//object[@data="figure1.svg"]'
        )
        self.assertEqual(len(nodes), 1)


class HTMLGenerator_Fig_Alternatives_Graphics_Tests(unittest.TestCase):
    def setUp(self):
        xml = """
            <fig id="f01">
                <label>Figura 1</label>
                <caption>
                    <title>Caption Figura 1</title>
                </caption>
                <disp-formula>
                <alternatives>
                    <graphic xlink:href="original.tif" />
                    <graphic xlink:href="ampliada.png" specific-use="scielo-web" />
                    <graphic xlink:href="miniatura.jpg" specific-use="scielo-web" content-type="scielo-20x20" />
                </alternatives>
                </disp-formula>
                <attrib>Fonte: Dados originais da pesquisa</attrib>
            </fig>
        """
        self.html = _get_xml(xml)

    def test_enlarged_presentation(self):
        nodes = self.html.xpath(
            '//div[@class="modal fade ModalFigs" and @id="ModalFigf01"]'
            '/div[@class="modal-dialog modal-lg"]'
            '/div[@class="modal-content"]'
            '/div[@class="modal-body"]'
            '/div[@class="row formula"]'
            '/div[@class="col-md-12"]'
            '/div[@class="formula-container"]'
            '/a[@href="ampliada.png"]'
            '/img[@src="ampliada.png"]'
        )
        self.assertEqual(len(nodes), 1)

    def test_thumbnail_presentation(self):
        nodes = self.html.xpath(
            '//div[@class="row fig" and @id="f01"]'
            '/div[@class="col-md-4 col-sm-4"]'
            '/a[@data-target="#ModalFigf01"]'
            '/div[@class="thumbImg"]'
            '/img[@src="miniatura.jpg"]'
        )
        self.assertEqual(len(nodes), 1)

    def test_original_presentation(self):
        nodes = self.html.xpath(
            '//div[@class="modal fade ModalFigs" and @id="ModalFigf01"]'
            '//div[@class="modal-header"]'
            '/a[@class="link-newWindow showTooltip" and @target="_blank"]'
        )
        self.assertEqual(nodes[0].get("href"), "original.tif")


class HTMLGenerator_FigGroup_Graphic_Tests(unittest.TestCase):

    def setUp(self):
        xml = ("""
            <fig-group id="f01">
                <fig xml:lang="pt">
                    <label>Figura 1</label>
                    <caption>
                        <title>Caption Figura PT</title>
                    </caption>
                    <attrib>
                       <p>Nota da tabela em pt</p>
                    </attrib>
                </fig>
                <fig xml:lang="en">
                    <label>Figure 1</label>
                    <caption>
                        <title>Caption Figura EN</title>
                    </caption>
                    <attrib>
                        <p><xref ref-type="fig" rid="f01">Figure 1</xref> Identification of <italic>Senna Senna</italic> Mill. (Fabaceae) species collected in different locations in northwestern Ceará State. <sup>*</sup> Exotic, <sup>**</sup> Endemic to Brazil. Source: Herbário Francisco José de Abreu Matos (HUVA).</p>
                    </attrib>
                </fig>
                <disp-formula><graphic xlink:href="original"/></disp-formula>
            </fig-group>
        """)
        self.html = _get_xml(xml)

    def test_enlarged_presentation(self):
        nodes = self.html.xpath(
            '//div[@class="modal fade ModalFigs" and @id="ModalFigf01"]'
            '/div[@class="modal-dialog modal-lg"]'
            '/div[@class="modal-content"]'
            '/div[@class="modal-body"]'
            '/div[@class="row formula"]'
            '/div[@class="col-md-12"]'
            '/div[@class="formula-container"]'
            '/a[@href="original.jpg"]'
            '/img[@src="original.jpg"]'
        )
        self.assertEqual(len(nodes), 1)

    def test_original_presentation(self):
        # _print_debug(self.html)
        nodes = self.html.xpath(
            '//div[@class="modal fade ModalFigs" and @id="ModalFigf01"]'
            '//div[@class="modal-header"]'
            '/a[@class="link-newWindow showTooltip" and @target="_blank"]'
        )
        self.assertEqual(nodes[0].get("href"), "original.tif")


class HTMLGenerator_FigGroup_Alternatives_Graphics_Tests(unittest.TestCase):

    def setUp(self):
        xml = ("""
            <fig-group id="f01">
                <fig xml:lang="pt">
                    <label>Figura 1</label>
                    <caption>
                        <title>Caption Figura PT</title>
                    </caption>
                    <attrib>
                       <p>Nota da tabela em pt</p>
                    </attrib>
                </fig>
                <fig xml:lang="en">
                    <label>Figure 1</label>
                    <caption>
                        <title>Caption Figura EN</title>
                    </caption>
                    <attrib>
                      <p><xref ref-type="fig" rid="f01">Figure 1</xref> Identification of <italic>Senna Senna</italic> Mill. (Fabaceae) species collected in different locations in northwestern Ceará State. <sup>*</sup> Exotic, <sup>**</sup> Endemic to Brazil. Source: Herbário Francisco José de Abreu Matos (HUVA).</p>
                    </attrib>
                </fig>
                <disp-formula>
                <alternatives>
                    <graphic xlink:href="original.tif" />
                    <graphic xlink:href="ampliada.png" specific-use="scielo-web" />
                    <graphic xlink:href="miniatura.jpg" specific-use="scielo-web" content-type="scielo-20x20" />
                </alternatives>
                </disp-formula>
            </fig-group>
        """)
        self.html = _get_xml(xml)

    def test_enlarged_presentation(self):
        nodes = self.html.xpath(
            '//div[@class="modal fade ModalFigs" and @id="ModalFigf01"]'
            '/div[@class="modal-dialog modal-lg"]'
            '/div[@class="modal-content"]'
            '/div[@class="modal-body"]'
            '/div[@class="row formula"]'
            '/div[@class="col-md-12"]'
            '/div[@class="formula-container"]'
            '/a[@href="ampliada.png"]'
            '/img[@src="ampliada.png"]'
        )
        self.assertEqual(len(nodes), 1)

    def test_original_presentation(self):
        nodes = self.html.xpath(
            '//div[@class="modal fade ModalFigs" and @id="ModalFigf01"]'
            '//div[@class="modal-header"]'
            '/a[@class="link-newWindow showTooltip" and @target="_blank"]'
        )
        self.assertEqual(nodes[0].get("href"), "original.tif")


class HTMLGenerator_FigGroup_Fig_DispFormula_Graphic_Tests(unittest.TestCase):
    def setUp(self):
        xml = ("""
            <fig-group id="f01">
                <fig xml:lang="pt">
                    <label>Figura 1</label>
                    <caption>
                        <title>Caption Figura PT</title>
                    </caption>
                    <attrib>
                       <p>Nota da tabela em pt</p>
                    </attrib>
                </fig>
                <fig xml:lang="en">
                    <label>Figure 1</label>
                    <caption>
                        <title>Caption Figura EN</title>
                    </caption>
                    <disp-formula><graphic xlink:href="original"/></disp-formula>
                    <attrib>
                      <p><xref ref-type="fig" rid="f01">Figure 1</xref> Identification of <italic>Senna Senna</italic> Mill. (Fabaceae) species collected in different locations in northwestern Ceará State. <sup>*</sup> Exotic, <sup>**</sup> Endemic to Brazil. Source: Herbário Francisco José de Abreu Matos (HUVA).</p>
                    </attrib>
                </fig>
            </fig-group>
        """)
        self.html = _get_xml(xml)

    def test_enlarged_presentation(self):
        nodes = self.html.xpath(
            '//div[@class="modal fade ModalFigs" and @id="ModalFigf01"]'
            '/div[@class="modal-dialog modal-lg"]'
            '/div[@class="modal-content"]'
            '/div[@class="modal-body"]'
            '/div[@class="row formula"]'
            '/div[@class="col-md-12"]'
            '/div[@class="formula-container"]'
            '/a[@href="original.jpg"]'
            '/img[@src="original.jpg"]'
        )
        self.assertEqual(len(nodes), 1)

    def test_original_presentation(self):
        nodes = self.html.xpath(
            '//div[@class="modal fade ModalFigs" and @id="ModalFigf01"]'
            '//div[@class="modal-header"]'
            '/a[@class="link-newWindow showTooltip" and @target="_blank"]'
        )
        self.assertEqual(nodes[0].get("href"), "original.tif")


class HTMLGenerator_FigGroup_Fig_Alternatives_Graphics_Tests(unittest.TestCase):

    def setUp(self):
        xml = ("""
            <fig-group id="f01">
                <fig xml:lang="pt">
                    <label>Figura 1</label>
                    <caption>
                        <title>Caption Figura PT</title>
                    </caption>
                    <attrib>
                       <p>Nota da tabela em pt</p>
                    </attrib>
                </fig>
                <fig xml:lang="en">
                    <label>Figure 1</label>
                    <caption>
                        <title>Caption Figura EN</title>
                    </caption>
                    <disp-formula>
                    <alternatives>
                        <graphic xlink:href="original.tif" />
                        <graphic xlink:href="ampliada.png" specific-use="scielo-web" />
                        <graphic xlink:href="miniatura.jpg" specific-use="scielo-web" content-type="scielo-20x20" />
                    </alternatives>
                    </disp-formula>
                    <attrib>
                      <p><xref ref-type="fig" rid="f01">Figure 1</xref> Identification of <italic>Senna Senna</italic> Mill. (Fabaceae) species collected in different locations in northwestern Ceará State. <sup>*</sup> Exotic, <sup>**</sup> Endemic to Brazil. Source: Herbário Francisco José de Abreu Matos (HUVA).</p>
                    </attrib>
                </fig>
            </fig-group>
        """)
        self.html = _get_xml(xml)

    def test_enlarged_presentation(self):
        nodes = self.html.xpath(
            '//div[@class="modal fade ModalFigs" and @id="ModalFigf01"]'
            '/div[@class="modal-dialog modal-lg"]'
            '/div[@class="modal-content"]'
            '/div[@class="modal-body"]'
            '/div[@class="row formula"]'
            '/div[@class="col-md-12"]'
            '/div[@class="formula-container"]'
            '/a[@href="ampliada.png"]'
            '/img[@src="ampliada.png"]'
        )
        self.assertEqual(len(nodes), 1)

    def test_thumbnail_presentation(self):
        nodes = self.html.xpath(
            '//div[@class="row fig" and @id="f01"]'
            '/div[@class="col-md-4 col-sm-4"]'
            '/a[@data-target="#ModalFigf01"]'
            '/div[@class="thumbImg"]'
            '/img[@src="miniatura.jpg"]'
        )
        self.assertEqual(len(nodes), 1)

    def test_original_presentation(self):
        nodes = self.html.xpath(
            '//div[@class="modal fade ModalFigs" and @id="ModalFigf01"]'
            '//div[@class="modal-header"]'
            '/a[@class="link-newWindow showTooltip" and @target="_blank"]'
        )
        self.assertEqual(nodes[0].get("href"), "original.tif")


class HTMLGenerator_Fig_Alternatives_TexAndSVG_Tests(unittest.TestCase):
    def setUp(self):
        xml = """
            <fig id="f01">
                <label>Figura 1</label>
                <caption>
                    <title>Caption Figura 1</title>
                </caption>
                <disp-formula>
                <alternatives>
<tex-math id="tx2"> \\documentclass {article} \\usepackage{wasysym} \\usepackage[substack]{amsmath} \\usepackage{amsfonts} \\usepackage{amssymb} \\usepackage{amsbsy} \\usepackage[mathscr]{eucal} \\usepackage{mathrsfs} \\usepackage{pmc} \\usepackage[Euler]{upgreek} \\pagestyle{empty} \\oddsidemargin -1.0in \\begin{document} \\[E\\widehat{Y\\left( 0 \\right)|D=1}=\\frac{\\mathop{\\sum }_{\\{i|D=0\\}}{{Y}_{i}}{{d}_{i}}}{\\mathop{\\sum }_{\\{i|D=0\\}}{{d}_{i}}}\\] \\end{document} </tex-math>
                <graphic xlink:href="original.svg"/>
                </alternatives>
                </disp-formula>
                <attrib>Fonte: Dados originais da pesquisa</attrib>
            </fig>
        """
        self.html = _get_xml(xml)

    def test_enlarged_presentation(self):
        nodes = self.html.xpath(
            '//div[@class="modal fade ModalFigs" and @id="ModalFigf01"]'
            '/div[@class="modal-dialog modal-lg"]'
            '/div[@class="modal-content"]'
            '/div[@class="modal-body"]'
            '/div[@class="row formula"]'
            '/div[@class="col-md-12"]'
            '/div[@class="formula-container"]'
            '/span[@class="formula-body"]'
            '/span'
        )
        self.assertEqual(nodes[0].text, "\\[E\\widehat{Y\\left( 0 \\right)|D=1}=\\frac{\\mathop{\\sum }_{\\{i|D=0\\}}{{Y}_{i}}{{d}_{i}}}{\\mathop{\\sum }_{\\{i|D=0\\}}{{d}_{i}}}\\]")

    def test_thumbnail_presentation(self):
        nodes = self.html.xpath(
            '//div[@class="row fig" and @id="f01"]'
            '/div[@class="col-md-4 col-sm-4"]'
            '/a[@data-target="#ModalFigf01"]'
            '/div[@class="thumbOff"]'
        )
        self.assertEqual(len(nodes), 1)

    def test_original_presentation(self):
        nodes = self.html.xpath(
            '//div[@class="modal fade ModalFigs" and @id="ModalFigf01"]'
            '//div[@class="modal-header"]'
            '/a[@class="link-newWindow showTooltip" and @target="_blank"]'
        )
        self.assertEqual(nodes[0].get("href"), "original.svg")


class HTMLGenerator_Fig_Alternatives_MathAndSVG_Tests(unittest.TestCase):
    def setUp(self):
        xml = """
            <fig id="f01">
                <label>Figura 1</label>
                <caption>
                    <title>Caption Figura 1</title>
                </caption>
                <disp-formula>
                <alternatives><mml:math><mml:mi>τ</mml:mi><mml:mo>=</mml:mo><mml:mi>E</mml:mi><mml:mfenced close="]" open="[" separators="|"><mml:mrow><mml:mi>Y</mml:mi><mml:mfenced separators="|"><mml:mrow><mml:mn>1</mml:mn></mml:mrow></mml:mfenced></mml:mrow><mml:mrow><mml:mi>D</mml:mi><mml:mo>=</mml:mo><mml:mn>1</mml:mn></mml:mrow></mml:mfenced><mml:mo>-</mml:mo><mml:mi>E</mml:mi><mml:mo>[</mml:mo><mml:mi>Y</mml:mi><mml:mo>(</mml:mo><mml:mn>0</mml:mn><mml:mo>)</mml:mo><mml:mo>|</mml:mo><mml:mi>D</mml:mi><mml:mo>=</mml:mo><mml:mn>1</mml:mn><mml:mo>]</mml:mo></mml:math><graphic xlink:href="original.svg"/></alternatives>
                </disp-formula>
                <attrib>Fonte: Dados originais da pesquisa</attrib>
            </fig>
        """
        self.html = _get_xml(xml)

    def test_enlarged_presentation(self):
        nodes = self.html.xpath(
            '//div[@class="modal fade ModalFigs" and @id="ModalFigf01"]'
            '/div[@class="modal-dialog modal-lg"]'
            '/div[@class="modal-content"]'
            '/div[@class="modal-body"]'
            '/div[@class="row formula"]'
            '/div[@class="col-md-12"]'
            '/div[@class="formula-container"]'
            '/math'
        )
        self.assertEqual(len(nodes), 1)

    def test_thumbnail_presentation(self):
        nodes = self.html.xpath(
            '//div[@class="row fig" and @id="f01"]'
            '/div[@class="col-md-4 col-sm-4"]'
            '/a[@data-target="#ModalFigf01"]'
            '/div[@class="thumbOff"]'
        )
        self.assertEqual(len(nodes), 1)

    def test_original_presentation(self):
        nodes = self.html.xpath(
            '//div[@class="modal fade ModalFigs" and @id="ModalFigf01"]'
            '//div[@class="modal-header"]'
            '/a[@class="link-newWindow showTooltip" and @target="_blank"]'
        )
        self.assertEqual(nodes[0].get("href"), "original.svg")


class HTMLGenerator_Fig_DispFormula_Tex_Tiff_Tests(unittest.TestCase):
    def setUp(self):
        xml = """
            <fig id="f01">
                <label>Figura 1</label>
                <caption>
                    <title>Caption Figura 1</title>
                </caption>
                <disp-formula>
<tex-math id="tx2"> \\documentclass {article} \\usepackage{wasysym} \\usepackage[substack]{amsmath} \\usepackage{amsfonts} \\usepackage{amssymb} \\usepackage{amsbsy} \\usepackage[mathscr]{eucal} \\usepackage{mathrsfs} \\usepackage{pmc} \\usepackage[Euler]{upgreek} \\pagestyle{empty} \\oddsidemargin -1.0in \\begin{document} \\[E\\widehat{Y\\left( 0 \\right)|D=1}=\\frac{\\mathop{\\sum }_{\\{i|D=0\\}}{{Y}_{i}}{{d}_{i}}}{\\mathop{\\sum }_{\\{i|D=0\\}}{{d}_{i}}}\\] \\end{document} </tex-math>
                </disp-formula>
                <attrib>Fonte: Dados originais da pesquisa</attrib>
            </fig>
        """
        self.html = _get_xml(xml)

    def test_enlarged_presentation(self):
        nodes = self.html.xpath(
            '//div[@class="modal fade ModalFigs" and @id="ModalFigf01"]'
            '/div[@class="modal-dialog modal-lg"]'
            '/div[@class="modal-content"]'
            '/div[@class="modal-body"]'
            '/div[@class="row formula"]'
            '/div[@class="col-md-12"]'
            '/div[@class="formula-container"]'
            '/span[@class="formula-body"]'
            '/span'
        )
        self.assertEqual(len(nodes), 1)
