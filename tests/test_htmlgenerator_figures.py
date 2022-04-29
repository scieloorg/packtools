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


class HTMLGenerator_Fig_LabelAndCaption_Attrib_Tests(unittest.TestCase):

    def setUp(self):
        xml = """
            <fig id="f01">
                <label>Figura 1</label>
                <caption>
                    <title>Caption Figura 1</title>
                </caption>
                <attrib>Fonte: Dados originais da pesquisa</attrib>
            </fig>
            """
        self.html = _get_xml(xml)

    def test_thumbnail_label(self):
        nodes = self.html.xpath(
            '//div[@class="row fig" and @id="f01"]'
            '/div[@class="col-md-8 col-sm-8"]'
            '/strong'
        )
        self.assertEqual(nodes[0].text, 'Figura 1')

    def test_thumbnail_caption(self):
        nodes = self.html.xpath(
            '//div[@class="row fig" and @id="f01"]'
            '/div[@class="col-md-8 col-sm-8"]'
            '/br'
        )
        self.assertEqual(nodes[0].tail.strip(), 'Caption Figura 1')

    def test_total_in_tabpanel(self):
        nodes = self.html.xpath(
            '//a[@href="#figures" and @role="tab"]'
        )
        self.assertIn("(2)", nodes[0].text)

    def test_thumbnail_label_in_tabpanel(self):
        nodes = self.html.xpath(
            '//div[@class="modal fade ModalDefault" and @id="ModalTablesFigures"]'
            '//div[@class="tab-content"]'
            '/div[@role="tabpanel" and @id="figures"]'
            '//div[@class="row fig"]'
            '/div[@class="col-md-8"]'
            '/strong'
        )
        self.assertEqual(nodes[0].text, 'Figura 1')

    def test_thumbnail_caption_in_tabpanel(self):
        nodes = self.html.xpath(
            '//div[@class="modal fade ModalDefault" and @id="ModalTablesFigures"]'
            '//div[@class="tab-content"]'
            '/div[@role="tabpanel" and @id="figures"]'
            '//div[@class="row fig"]'
            '/div[@class="col-md-8"]'
            '/br'
        )
        self.assertEqual(nodes[0].tail.strip(), 'Caption Figura 1')

    def test_attrib(self):
        nodes = self.html.xpath(
            '//div[@class="modal fade ModalFigs" and @id="ModalFigf01"]'
            '/div[@class="modal-dialog modal-lg"]'
            '/div[@class="modal-content"]'
            '/div[@class="modal-body"]'
            '/small'
        )
        self.assertEqual(nodes[0].text.strip(), 'Fonte: Dados originais da pesquisa')

    def test_xref_presentation(self):
        nodes = self.html.xpath(
            '//a[@href="" and @class="open-asset-modal" and @data-target="#ModalFigf01"]'
        )
        self.assertEqual(len(nodes), 1)


class HTMLGenerator_Fig_Graphic_Tiff_Tests(unittest.TestCase):
    def setUp(self):
        xml = """
            <fig id="f01">
                <label>Figura 1</label>
                <caption>
                    <title>Caption Figura 1</title>
                </caption>
                <graphic xlink:href="figure1.tif" />
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
            '/a[@href="figure1.jpg"]'
            '/img[@src="figure1.jpg"]'
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
        self.assertEqual(nodes[0].get("href"), "figure1.tif")


class HTMLGenerator_Fig_Graphic_Png_Tests(unittest.TestCase):
    def setUp(self):
        xml = """
            <fig id="f01">
                <label>Figura 1</label>
                <caption>
                    <title>Caption Figura 1</title>
                </caption>
                <graphic xlink:href="figure1.png"/>
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
            '/a[@href="figure1.png"]'
            '/img[@src="figure1.png"]'
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
        self.assertEqual(nodes[0].get("href"), "figure1.png")


class HTMLGenerator_Fig_Graphic_NoExtension_Tests(unittest.TestCase):
    def setUp(self):
        xml = """
            <fig id="f01">
                <label>Figura 1</label>
                <caption>
                    <title>Caption Figura 1</title>
                </caption>
                <graphic xlink:href="figure1"/>
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
            '/a'
            '/img[@src="figure1.jpg"]'
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
        self.assertEqual(nodes[0].get("href"), "figure1.tif")


class HTMLGenerator_Fig_Graphic_SVG_Tests(unittest.TestCase):
    def setUp(self):
        xml = """
            <fig id="f01">
                <label>Figura 1</label>
                <caption>
                    <title>Caption Figura 1</title>
                </caption>
                <graphic xlink:href="figure1.svg"/>
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
        self.assertEqual(nodes[0].get("href"), "figure1.svg")


class HTMLGenerator_Fig_Alternatives_Graphics_Tests(unittest.TestCase):
    def setUp(self):
        xml = """
            <fig id="f01">
                <label>Figura 1</label>
                <caption>
                    <title>Caption Figura 1</title>
                </caption>
                <alternatives>
                    <graphic xlink:href="original.tif" />
                    <graphic xlink:href="ampliada.png" specific-use="scielo-web" />
                    <graphic xlink:href="miniatura.jpg" specific-use="scielo-web" content-type="scielo-20x20" />
                </alternatives>
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


class HTMLGenerator_FigGroup_Label_Caption_Attribs_Tests(unittest.TestCase):

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
            </fig-group>
        """)
        self.html = _get_xml(xml)

    def test_thumbnail_label(self):
        nodes = self.html.xpath(
            '//div[@class="row fig" and @id="f01"]'
            '/div[@class="col-md-8 col-sm-8"]'
            '/strong'
        )
        self.assertEqual(nodes[0].text, 'Figura 1')
        self.assertEqual(nodes[1].text, 'Figure 1')

    def test_thumbnail_caption(self):
        nodes = self.html.xpath(
            '//div[@class="row fig" and @id="f01"]'
            '/div[@class="col-md-8 col-sm-8"]'
        )
        text = etree.tostring(nodes[0], encoding="utf-8").decode("utf-8")
        self.assertIn('Caption Figura PT', text)
        self.assertIn('Caption Figura EN', text)

    def test_thumbnail_label_in_tabpanel(self):
        nodes = self.html.xpath(
            '//div[@class="row fig"]'
            '/div[@class="col-md-8"]'
            '/strong'
        )
        self.assertEqual(nodes[0].text, 'Figura 1')
        self.assertEqual(nodes[1].text, 'Figure 1')

    def test_thumbnail_caption_in_tabpanel(self):
        nodes = self.html.xpath(
            '//div[@class="row fig"]'
            '/div[@class="col-md-8"]'
            '/br'
        )
        self.assertEqual(
            nodes[0].tail.strip(),
            'Caption Figura PT')
        self.assertEqual(
            nodes[1].tail.strip(),
            'Caption Figura EN')

    def test_attrib(self):
        nodes = self.html.xpath(
            '//div[@class="modal fade ModalFigs" and @id="ModalFigf01"]'
            '/div[@class="modal-dialog modal-lg"]'
            '/div[@class="modal-content"]'
            '/div[@class="modal-body"]'
            '/small'
        )
        texts = [
            etree.tostring(node, encoding="utf-8").decode("utf-8")
            for node in nodes
        ]
        texts[1] = " ".join([w.strip() for w in texts[1].split()])
        expected_ten = (
            """<small> <p><a href="" class="open-asset-modal" data-toggle="modal" data-target="#ModalFigf01"><span class="sci-ico-fileFigure"/>Figure 1</a> Identification of <i>Senna Senna</i> Mill. (Fabaceae) species collected in different locations in northwestern Ceará State. <sup>*</sup> Exotic, <sup>**</sup> Endemic to Brazil. Source: Herbário Francisco José de Abreu Matos (HUVA).</p> </small>"""
        )
        self.assertIn("Nota da tabela em pt", texts[0])
        self.assertIn(expected_ten, texts[1])


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
                <graphic xlink:href="original"/>
            </fig-group>
        """)
        self.html = _get_xml(xml)

    def test_enlarged_presentation(self):
        nodes = self.html.xpath(
            '//div[@class="modal fade ModalFigs" and @id="ModalFigf01"]'
            '/div[@class="modal-dialog modal-lg"]'
            '/div[@class="modal-content"]'
            '/div[@class="modal-body"]'
            '/a[@href="original.jpg"]'
            '/img[@src="original.jpg"]'
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
                <alternatives>
                    <graphic xlink:href="original.tif" />
                    <graphic xlink:href="ampliada.png" specific-use="scielo-web" />
                    <graphic xlink:href="miniatura.jpg" specific-use="scielo-web" content-type="scielo-20x20" />
                </alternatives>
            </fig-group>
        """)
        self.html = _get_xml(xml)

    def test_enlarged_presentation(self):
        nodes = self.html.xpath(
            '//div[@class="modal fade ModalFigs" and @id="ModalFigf01"]'
            '/div[@class="modal-dialog modal-lg"]'
            '/div[@class="modal-content"]'
            '/div[@class="modal-body"]'
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


class HTMLGenerator_FigGroup_Fig_Graphic_Tests(unittest.TestCase):
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
                    <graphic xlink:href="original"/>
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
            '/a[@href="original.jpg"]'
            '/img[@src="original.jpg"]'
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
                    <alternatives>
                        <graphic xlink:href="original.tif" />
                        <graphic xlink:href="ampliada.png" specific-use="scielo-web" />
                        <graphic xlink:href="miniatura.jpg" specific-use="scielo-web" content-type="scielo-20x20" />
                    </alternatives>
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
