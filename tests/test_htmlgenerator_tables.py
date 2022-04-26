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
        <p>The Eh measurements... <xref ref-type="table" rid="t01">Tabela 1</xref>:</p>
        <p>
            {text}
        </p>
        <p>
        <table-wrap id="t02">
            <label>Tabela 2</label>
            <caption>
                <title>Caption Tabela 2</title>
            </caption>
            <table/>
            <table-wrap-foot>
                <fn-group>
                    <fn id="TF2-150"><p>Nota 1</p></fn>
                    <fn id="TF2-151"><p>NOta 2</p></fn>
                </fn-group>
            </table-wrap-foot>
        </table-wrap>
        </p>
        </sec>
      </body>
    </article>"""
    )
    et = get_xml_tree_from_string(xml)
    return domain.HTMLGenerator.parse(et, valid_only=False).generate('pt')


class HTMLGenerator_TableWrap_LabelAndCaption_Footnote_Tests(unittest.TestCase):

    def setUp(self):
        xml = """
            <table-wrap id="t01">
                <label>Tabela 1</label>
                <caption>
                    <title>Caption Tabela 1</title>
                </caption>
                <table-wrap-foot>
                    <fn-group>
                        <fn id="TF1-150"><p>Data not available for 1 trial.</p></fn>
                        <fn id="TF1-151"><p>P&#x003C;0.05 (random effects model).</p></fn>
                    </fn-group>
                </table-wrap-foot>
            </table-wrap>
            """
        self.html = _get_xml(xml)

    def test_table_wrap_foot_must_not_generate_articleSection_footnotes(self):
        """
        Test table-wrap-foot must NOT generate footnotes as article footnotes

            ```
            <div class="articleSection">
              <h2/>
              <div class="ref-list">
                <ul class="refList footnote">
                  <li>
                    <div>Data not available for 1 trial.</div>
                  </li>
                  <li>
                    <div>P&lt;0.05 (random effects model).</div>
                  </li>
                  <li>
                    <div>Nota 1</div>
                  </li>
                  <li>
                    <div>NOta 2</div>
                  </li>
                </ul>
              </div>
            </div>
            ```
        """
        nodes = self.html.xpath(
            '//div[@class="articleSection"]'
            '/div[@class="ref-list"]'
            '/ul[@class="refList footnote"]'
            '/li/div'
        )
        self.assertEqual(len(nodes), 0)

    def test_thumbnail_label(self):
        nodes = self.html.xpath(
            '//div[@class="row table" and @id="t01"]'
            '/div[@class="col-md-8 col-sm-8"]'
            '/strong'
        )
        self.assertEqual(nodes[0].text, 'Tabela 1')

    def test_thumbnail_caption(self):
        nodes = self.html.xpath(
            '//div[@class="row table" and @id="t01"]'
            '/div[@class="col-md-8 col-sm-8"]'
            '/br'
        )
        self.assertEqual(nodes[0].tail.strip(), 'Caption Tabela 1')

    def test_total_in_tabpanel(self):
        nodes = self.html.xpath(
            '//a[@href="#tables" and @role="tab"]'
        )
        self.assertIn("(2)", nodes[0].text)

    def test_thumbnail_label_in_tabpanel(self):
        nodes = self.html.xpath(
            '//div[@class="modal fade ModalDefault" and @id="ModalTablesFigures"]'
            '//div[@class="tab-content"]'
            '/div[@role="tabpanel" and @id="tables"]'
            '//div[@class="row table"]'
            '/div[@class="col-md-8"]'
            '/strong'
        )
        self.assertEqual(nodes[0].text, 'Tabela 1')

    def test_thumbnail_caption_in_tabpanel(self):
        nodes = self.html.xpath(
            '//div[@class="modal fade ModalDefault" and @id="ModalTablesFigures"]'
            '//div[@class="tab-content"]'
            '/div[@role="tabpanel" and @id="tables"]'
            '//div[@class="row table"]'
            '/div[@class="col-md-8"]'
            '/br'
        )
        self.assertEqual(nodes[0].tail.strip(), 'Caption Tabela 1')

    def test_thumbnail_presentation(self):
        nodes = self.html.xpath(
            '//div[@class="row table" and @id="t01"]'
            '/div[@class="col-md-4 col-sm-4"]'
            '/a'
            '/div[@class="thumbOff"]'
        )
        # _print_debug(self.html)
        self.assertEqual(len(nodes), 1)

    def test_footnotes(self):
        nodes = self.html.xpath(
            '//div[@class="modal fade ModalTables" and @id="ModalTablet01"]'
            '/div[@class="modal-dialog modal-lg"]'
            '/div[@class="modal-content"]'
            '/div[@class="modal-footer"]'
            '/div[@class="ref-list"]'
            '/ul[@class="refList footnote"]'
            '/li'
            '/div'
        )
        self.assertEqual(nodes[0].text.strip(), 'Data not available for 1 trial.')
        self.assertEqual(nodes[1].text.strip(), 'P<0.05 (random effects model).')

    def test_xref_presentation(self):
        nodes = self.html.xpath(
            '//a[@href="" and @class="open-asset-modal" and @data-target="#ModalTablet01"]'
        )
        self.assertEqual(len(nodes), 1)


class HTMLGenerator_TableWrap_Graphic_Tiff_Tests(unittest.TestCase):
    def setUp(self):
        xml = """
            <table-wrap id="t01">
                <label>Tabela 1</label>
                <caption>
                    <title>Caption Tabela 1</title>
                </caption>
                <graphic xlink:href="table1.tif" />
                <table-wrap-foot>
                    <fn-group>
                        <fn id="TF1-150"><p>Data not available for 1 trial.</p></fn>
                        <fn id="TF1-151"><p>P&#x003C;0.05 (random effects model).</p></fn>
                    </fn-group>
                </table-wrap-foot>
            </table-wrap>
        """
        self.html = _get_xml(xml)

    def test_enlarged_presentation(self):
        nodes = self.html.xpath(
            '//div[@class="modal fade ModalTables" and @id="ModalTablet01"]'
            '/div[@class="modal-dialog modal-lg"]'
            '/div[@class="modal-content"]'
            '/div[@class="modal-body"]'
            '/a[@href="table1.jpg"]'
            '/img[@src="table1.jpg"]'
        )
        self.assertEqual(len(nodes), 1)


class HTMLGenerator_TableWrap_Graphic_Png_Tests(unittest.TestCase):
    def setUp(self):
        xml = """
            <table-wrap id="t01">
                <label>Tabela 1</label>
                <caption>
                    <title>Caption Tabela 1</title>
                </caption>
                <graphic xlink:href="table1.png"/>
                <table-wrap-foot>
                    <fn-group>
                        <fn id="TF1-150"><p>Data not available for 1 trial.</p></fn>
                        <fn id="TF1-151"><p>P&#x003C;0.05 (random effects model).</p></fn>
                    </fn-group>
                </table-wrap-foot>
            </table-wrap>
        """
        self.html = _get_xml(xml)

    def test_enlarged_presentation(self):
        nodes = self.html.xpath(
            '//div[@class="modal fade ModalTables" and @id="ModalTablet01"]'
            '/div[@class="modal-dialog modal-lg"]'
            '/div[@class="modal-content"]'
            '/div[@class="modal-body"]'
            '/a[@href="table1.png"]'
            '/img[@src="table1.png"]'
        )
        self.assertEqual(len(nodes), 1)


class HTMLGenerator_TableWrap_Graphic_NoExtension_Tests(unittest.TestCase):
    def setUp(self):
        xml = """
            <table-wrap id="t01">
                <label>Tabela 1</label>
                <caption>
                    <title>Caption Tabela 1</title>
                </caption>
                <graphic xlink:href="table1"/>
                <table-wrap-foot>
                    <fn-group>
                        <fn id="TF1-150"><p>Data not available for 1 trial.</p></fn>
                        <fn id="TF1-151"><p>P&#x003C;0.05 (random effects model).</p></fn>
                    </fn-group>
                </table-wrap-foot>
            </table-wrap>
        """
        self.html = _get_xml(xml)
        _print_debug(self.html)

    def test_enlarged_presentation(self):
        nodes = self.html.xpath(
            '//div[@class="modal fade ModalTables" and @id="ModalTablet01"]'
            '/div[@class="modal-dialog modal-lg"]'
            '/div[@class="modal-content"]'
            '/div[@class="modal-body"]'
            '/a'
            '/img[@src="table1.jpg"]'
        )
        self.assertEqual(len(nodes), 1)


class HTMLGenerator_TableWrap_Graphic_SVG_Tests(unittest.TestCase):
    def setUp(self):
        xml = """
            <table-wrap id="t01">
                <label>Tabela 1</label>
                <caption>
                    <title>Caption Tabela 1</title>
                </caption>
                <graphic xlink:href="table1.svg"/>
                <table-wrap-foot>
                    <fn-group>
                        <fn id="TF1-150"><p>Data not available for 1 trial.</p></fn>
                        <fn id="TF1-151"><p>P&#x003C;0.05 (random effects model).</p></fn>
                    </fn-group>
                </table-wrap-foot>
            </table-wrap>
        """
        self.html = _get_xml(xml)

    def test_enlarged_presentation(self):
        nodes = self.html.xpath(
            '//div[@class="modal fade ModalTables" and @id="ModalTablet01"]'
            '/div[@class="modal-dialog modal-lg"]'
            '/div[@class="modal-content"]'
            '/div[@class="modal-body"]'
            '//object[@data="table1.svg"]'
        )
        self.assertEqual(len(nodes), 1)


class HTMLGenerator_TableWrap_Table_Tests(unittest.TestCase):
    def setUp(self):
        xml = """
            <table-wrap id="t01">
                <label>Tabela 1</label>
                <caption>
                    <title>Caption Tabela 1</title>
                </caption>
                <table><tr><td>conteudo A</td></tr></table>
                <table-wrap-foot>
                    <fn-group>
                        <fn id="TF1-150"><p>Data not available for 1 trial.</p></fn>
                        <fn id="TF1-151"><p>P&#x003C;0.05 (random effects model).</p></fn>
                    </fn-group>
                </table-wrap-foot>
            </table-wrap>
        """
        self.html = _get_xml(xml)

    def test_enlarged_presentation(self):
        nodes = self.html.xpath(
            '//div[@class="modal fade ModalTables" and @id="ModalTablet01"]'
            '/div[@class="modal-dialog modal-lg"]'
            '/div[@class="modal-content"]'
            '/div[@class="modal-body"]'
            '//table'
        )
        self.assertEqual(len(nodes), 1)

    def test_original_presentation(self):
        nodes = self.html.xpath(
            '//div[@class="modal fade ModalTables" and @id="ModalTablet01"]'
            '//div[@class="modal-header"]'
            '/a[@class="link-newWindow showTooltip" and @target="_blank"]'
        )
        self.assertEqual(len(nodes), 0)


class HTMLGenerator_TableWrap_Alternatives_TableAndGraphic_Tests(unittest.TestCase):
    def setUp(self):
        xml = """
            <table-wrap id="t01">
                <label>Tabela 1</label>
                <caption>
                    <title>Caption Tabela 1</title>
                </caption>
                <alternatives>
                    <table>
                        <tr><td>Conteúdo da tabela</td></tr>
                    </table>
                    <graphic xlink:href="original.svg" />
                </alternatives>
                <table-wrap-foot>
                    <fn-group>
                        <fn id="TF1-150"><p>Data not available for 1 trial.</p></fn>
                        <fn id="TF1-151"><p>P&#x003C;0.05 (random effects model).</p></fn>
                    </fn-group>
                </table-wrap-foot>
            </table-wrap>
        """
        self.html = _get_xml(xml)

    def test_enlarged_presentation(self):
        nodes = self.html.xpath(
            '//div[@class="modal fade ModalTables" and @id="ModalTablet01"]'
            '/div[@class="modal-dialog modal-lg"]'
            '/div[@class="modal-content"]'
            '/div[@class="modal-body"]'
            '//table'
        )
        self.assertEqual(len(nodes), 1)

    def test_thumbnail_presentation(self):
        nodes = self.html.xpath(
            '//div[@class="row table" and @id="t01"]'
            '/div[@class="col-md-4 col-sm-4"]'
            '/a'
            '/div[@class="thumbOff"]'
        )
        self.assertEqual(len(nodes), 1)

    def test_original_presentation(self):
        nodes = self.html.xpath(
            '//div[@class="modal fade ModalTables" and @id="ModalTablet01"]'
            '//div[@class="modal-header"]'
            '/a[@class="link-newWindow showTooltip" and @target="_blank"]'
        )
        self.assertEqual(nodes[0].get("href"), "original.svg")


class HTMLGenerator_TableWrap_Alternatives_GraphicAndTable_Tests(unittest.TestCase):
    def setUp(self):
        xml = """
            <table-wrap id="t01">
                <label>Tabela 1</label>
                <caption>
                    <title>Caption Tabela 1</title>
                </caption>
                <alternatives>
                    <graphic xlink:href="original1.svg" />
                    <table>
                        <tr><td>Conteúdo da tabela</td></tr>
                    </table>
                </alternatives>
                <table-wrap-foot>
                    <fn-group>
                        <fn id="TF1-150"><p>Data not available for 1 trial.</p></fn>
                        <fn id="TF1-151"><p>P&#x003C;0.05 (random effects model).</p></fn>
                    </fn-group>
                </table-wrap-foot>
            </table-wrap>
        """
        self.html = _get_xml(xml)

    def test_enlarged_presentation(self):
        nodes = self.html.xpath(
            '//div[@class="modal fade ModalTables" and @id="ModalTablet01"]'
            '/div[@class="modal-dialog modal-lg"]'
            '/div[@class="modal-content"]'
            '/div[@class="modal-body"]'
            '//object[@data="original1.svg"]'
        )
        self.assertEqual(len(nodes), 1)

    def test_original_presentation(self):
        nodes = self.html.xpath(
            '//div[@class="modal fade ModalTables" and @id="ModalTablet01"]'
            '//div[@class="modal-header"]'
            '/a[@class="link-newWindow showTooltip" and @target="_blank"]'
        )
        self.assertEqual(nodes[0].get("href"), "original1.svg")


class HTMLGenerator_TableWrap_Alternatives_Graphics_Tests(unittest.TestCase):
    def setUp(self):
        xml = """
            <table-wrap id="t01">
                <label>Tabela 1</label>
                <caption>
                    <title>Caption Tabela 1</title>
                </caption>
                <alternatives>
                    <graphic xlink:href="original.tif" />
                    <graphic xlink:href="ampliada.png" specific-use="scielo-web" />
                    <graphic xlink:href="miniatura.jpg" specific-use="scielo-web" content-type="scielo-20x20" />
                </alternatives>
                <table-wrap-foot>
                    <fn-group>
                        <fn id="TF1-150"><p>Data not available for 1 trial.</p></fn>
                        <fn id="TF1-151"><p>P&#x003C;0.05 (random effects model).</p></fn>
                    </fn-group>
                </table-wrap-foot>
            </table-wrap>
        """
        self.html = _get_xml(xml)

    def test_enlarged_presentation(self):
        nodes = self.html.xpath(
            '//div[@class="modal fade ModalTables" and @id="ModalTablet01"]'
            '/div[@class="modal-dialog modal-lg"]'
            '/div[@class="modal-content"]'
            '/div[@class="modal-body"]'
            '/a[@href="ampliada.png"]'
            '/img[@src="ampliada.png"]'
        )
        self.assertEqual(len(nodes), 1)

    def test_thumbnail_presentation(self):
        nodes = self.html.xpath(
            '//div[@class="row table" and @id="t01"]'
            '/div[@class="col-md-4 col-sm-4"]'
            '/a'
            '/div[@class="thumbOff"]'
        )
        self.assertEqual(len(nodes), 1)

    def test_original_presentation(self):
        nodes = self.html.xpath(
            '//div[@class="modal fade ModalTables" and @id="ModalTablet01"]'
            '//div[@class="modal-header"]'
            '/a[@class="link-newWindow showTooltip" and @target="_blank"]'
        )
        self.assertEqual(nodes[0].get("href"), "original.tif")


class HTMLGenerator_TableWrapGroup_Label_Caption_Footnotes_Tests(unittest.TestCase):

    def setUp(self):
        xml = ("""
            <table-wrap-group id="t01">
                <table-wrap xml:lang="pt">
                    <label>Tabela 1</label>
                    <caption>
                        <title>Caption Tabela PT</title>
                    </caption>
                    <table-wrap-foot>
                        <fn id="TFN1a">
                            <p>Nota da tabela em pt</p>
                        </fn>
                    </table-wrap-foot>
                </table-wrap>
                <table-wrap xml:lang="en">
                    <label>Table 1</label>
                    <caption>
                        <title>Caption Tabela EN</title>
                    </caption>
                    <table-wrap-foot>
                        <fn id="TFN1">
                            <p><xref ref-type="table" rid="t01">Table 1</xref> Identification of <italic>Senna Senna</italic> Mill. (Fabaceae) species collected in different locations in northwestern Ceará State. <sup>*</sup> Exotic, <sup>**</sup> Endemic to Brazil. Source: Herbário Francisco José de Abreu Matos (HUVA).</p>
                        </fn>
                    </table-wrap-foot>
                </table-wrap>
            </table-wrap-group>
        """)
        self.html = _get_xml(xml)

    def test_thumbnail_label(self):
        nodes = self.html.xpath(
            '//div[@class="row table" and @id="t01"]'
            '/div[@class="col-md-8 col-sm-8"]'
            '/strong'
        )
        self.assertEqual(nodes[0].text, 'Tabela 1')
        self.assertEqual(nodes[1].text, 'Table 1')

    def test_thumbnail_caption(self):
        nodes = self.html.xpath(
            '//div[@class="row table" and @id="t01"]'
            '/div[@class="col-md-8 col-sm-8"]'
        )
        text = etree.tostring(nodes[0], encoding="utf-8").decode("utf-8")
        self.assertIn('Caption Tabela PT', text)
        self.assertIn('Caption Tabela EN', text)

    def test_thumbnail_label_in_tabpanel(self):
        nodes = self.html.xpath(
            '//div[@class="row table"]'
            '/div[@class="col-md-8"]'
            '/strong'
        )
        self.assertEqual(nodes[0].text, 'Tabela 1')
        self.assertEqual(nodes[1].text, 'Table 1')

    def test_thumbnail_caption_in_tabpanel(self):
        nodes = self.html.xpath(
            '//div[@class="row table"]'
            '/div[@class="col-md-8"]'
            '/br'
        )
        self.assertEqual(
            nodes[0].tail.strip(),
            'Caption Tabela PT')
        self.assertEqual(
            nodes[1].tail.strip(),
            'Caption Tabela EN')

    def test_footnotes(self):
        nodes = self.html.xpath(
            '//div[@class="modal fade ModalTables" and @id="ModalTablet01"]'
            '/div[@class="modal-dialog modal-lg"]'
            '/div[@class="modal-content"]'
            '/div[@class="modal-footer"]'
            '/div[@class="ref-list"]'
            '/ul[@class="refList footnote"]'
        )
        texts = [
            etree.tostring(node, encoding="utf-8").decode("utf-8")
            for node in nodes
        ]
        texts[1] = " ".join([w.strip() for w in texts[1].split()])
        expected_ten = (
            """<div><a href="" class="open-asset-modal" data-toggle="modal" data-target="#ModalTablet01"><span class="sci-ico-fileTable"/>Table 1</a> Identification of <i>Senna Senna</i> Mill. (Fabaceae) species collected in different locations in northwestern Ceará State. <sup>*</sup> Exotic, <sup>**</sup> Endemic to Brazil. Source: Herbário Francisco José de Abreu Matos (HUVA).</div>"""
        )
        self.assertIn("Nota da tabela em pt", texts[0])
        self.assertIn(expected_ten, texts[1])


class HTMLGenerator_TableWrapGroup_Table_Tests(unittest.TestCase):

    def setUp(self):
        xml = ("""
            <table-wrap-group id="t01">
                <table-wrap xml:lang="pt">
                    <label>Tabela 1</label>
                    <caption>
                        <title>Caption Tabela PT</title>
                    </caption>
                    <table-wrap-foot>
                        <fn id="TFN1a">
                            <p>Nota da tabela em pt</p>
                        </fn>
                    </table-wrap-foot>
                </table-wrap>
                <table-wrap xml:lang="en">
                    <label>Table 1</label>
                    <caption>
                        <title>Caption Tabela EN</title>
                    </caption>
                    <table-wrap-foot>
                        <fn id="TFN1">
                            <p><xref ref-type="table" rid="t01">Table 1</xref> Identification of <italic>Senna Senna</italic> Mill. (Fabaceae) species collected in different locations in northwestern Ceará State. <sup>*</sup> Exotic, <sup>**</sup> Endemic to Brazil. Source: Herbário Francisco José de Abreu Matos (HUVA).</p>
                        </fn>
                    </table-wrap-foot>
                </table-wrap>
                <table></table>
            </table-wrap-group>
        """)
        self.html = _get_xml(xml)

    def test_enlarged_presentation(self):
        nodes = self.html.xpath(
            '//div[@class="modal fade ModalTables" and @id="ModalTablet01"]'
            '/div[@class="modal-dialog modal-lg"]'
            '/div[@class="modal-content"]'
            '/div[@class="modal-body"]'
            '/div[@class="table table-hover"]'
            '/table'
        )
        self.assertEqual(len(nodes), 1)


class HTMLGenerator_TableWrapGroup_Graphic_Tests(unittest.TestCase):

    def setUp(self):
        xml = ("""
            <table-wrap-group id="t01">
                <table-wrap xml:lang="pt">
                    <label>Tabela 1</label>
                    <caption>
                        <title>Caption Tabela PT</title>
                    </caption>
                    <table-wrap-foot>
                        <fn id="TFN1a">
                            <p>Nota da tabela em pt</p>
                        </fn>
                    </table-wrap-foot>
                </table-wrap>
                <table-wrap xml:lang="en">
                    <label>Table 1</label>
                    <caption>
                        <title>Caption Tabela EN</title>
                    </caption>
                    <table-wrap-foot>
                        <fn id="TFN1">
                            <p><xref ref-type="table" rid="t01">Table 1</xref> Identification of <italic>Senna Senna</italic> Mill. (Fabaceae) species collected in different locations in northwestern Ceará State. <sup>*</sup> Exotic, <sup>**</sup> Endemic to Brazil. Source: Herbário Francisco José de Abreu Matos (HUVA).</p>
                        </fn>
                    </table-wrap-foot>
                </table-wrap>
                <graphic xlink:href="original"/>
            </table-wrap-group>
        """)
        self.html = _get_xml(xml)

    def test_enlarged_presentation(self):
        nodes = self.html.xpath(
            '//div[@class="modal fade ModalTables" and @id="ModalTablet01"]'
            '/div[@class="modal-dialog modal-lg"]'
            '/div[@class="modal-content"]'
            '/div[@class="modal-body"]'
            '/a[@href="original.jpg"]'
            '/img[@src="original.jpg"]'
        )
        self.assertEqual(len(nodes), 1)

    def test_original_presentation(self):
        # _print_debug(self.html)
        nodes = self.html.xpath(
            '//div[@class="modal fade ModalTables" and @id="ModalTablet01"]'
            '//div[@class="modal-header"]'
            '/a[@class="link-newWindow showTooltip" and @target="_blank"]'
        )
        self.assertEqual(nodes[0].get("href"), "original.jpg")


class HTMLGenerator_TableWrapGroup_Alternatives_TableAndGraphic_Tests(unittest.TestCase):

    def setUp(self):
        xml = ("""
            <table-wrap-group id="t01">
                <table-wrap xml:lang="pt">
                    <label>Tabela 1</label>
                    <caption>
                        <title>Caption Tabela PT</title>
                    </caption>
                    <table-wrap-foot>
                        <fn id="TFN1a">
                            <p>Nota da tabela em pt</p>
                        </fn>
                    </table-wrap-foot>

                </table-wrap>
                <table-wrap xml:lang="en">
                    <label>Table 1</label>
                    <caption>
                        <title>Caption Tabela EN</title>
                    </caption>
                    <table-wrap-foot>
                        <fn id="TFN1">
                            <p><xref ref-type="table" rid="t01">Table 1</xref> Identification of <italic>Senna Senna</italic> Mill. (Fabaceae) species collected in different locations in northwestern Ceará State. <sup>*</sup> Exotic, <sup>**</sup> Endemic to Brazil. Source: Herbário Francisco José de Abreu Matos (HUVA).</p>
                        </fn>
                    </table-wrap-foot>
                </table-wrap>
                <alternatives>
                    <table>
                        <tr><td>Conteúdo da tabela</td></tr>
                    </table>
                    <graphic xlink:href="original.svg" />
                </alternatives>
            </table-wrap-group>
        """)
        self.html = _get_xml(xml)

    def test_enlarged_presentation(self):
        nodes = self.html.xpath(
            '//div[@class="modal fade ModalTables" and @id="ModalTablet01"]'
            '/div[@class="modal-dialog modal-lg"]'
            '/div[@class="modal-content"]'
            '/div[@class="modal-body"]'
            '/div[@class="table table-hover"]'
            '/table'
        )
        self.assertEqual(len(nodes), 1)

    def test_original_presentation(self):
        nodes = self.html.xpath(
            '//div[@class="modal fade ModalTables" and @id="ModalTablet01"]'
            '//div[@class="modal-header"]'
            '/a[@class="link-newWindow showTooltip" and @target="_blank"]'
        )
        self.assertEqual(nodes[0].get("href"), "original.svg")


class HTMLGenerator_TableWrapGroup_Alternatives_Graphics_Tests(unittest.TestCase):

    def setUp(self):
        xml = ("""
            <table-wrap-group id="t01">
                <table-wrap xml:lang="pt">
                    <label>Tabela 1</label>
                    <caption>
                        <title>Caption Tabela PT</title>
                    </caption>
                    <table-wrap-foot>
                        <fn id="TFN1a">
                            <p>Nota da tabela em pt</p>
                        </fn>
                    </table-wrap-foot>
                </table-wrap>
                <table-wrap xml:lang="en">
                    <label>Table 1</label>
                    <caption>
                        <title>Caption Tabela EN</title>
                    </caption>
                    <table-wrap-foot>
                        <fn id="TFN1">
                            <p><xref ref-type="table" rid="t01">Table 1</xref> Identification of <italic>Senna Senna</italic> Mill. (Fabaceae) species collected in different locations in northwestern Ceará State. <sup>*</sup> Exotic, <sup>**</sup> Endemic to Brazil. Source: Herbário Francisco José de Abreu Matos (HUVA).</p>
                        </fn>
                    </table-wrap-foot>
                </table-wrap>
                <alternatives>
                    <graphic xlink:href="original.tif" />
                    <graphic xlink:href="ampliada.png" specific-use="scielo-web" />
                    <graphic xlink:href="miniatura.jpg" specific-use="scielo-web" content-type="scielo-20x20" />
                </alternatives>
            </table-wrap-group>
        """)
        self.html = _get_xml(xml)

    def test_enlarged_presentation(self):
        nodes = self.html.xpath(
            '//div[@class="modal fade ModalTables" and @id="ModalTablet01"]'
            '/div[@class="modal-dialog modal-lg"]'
            '/div[@class="modal-content"]'
            '/div[@class="modal-body"]'
            '/a[@href="ampliada.png"]'
            '/img[@src="ampliada.png"]'
        )
        self.assertEqual(len(nodes), 1)

    def test_original_presentation(self):
        nodes = self.html.xpath(
            '//div[@class="modal fade ModalTables" and @id="ModalTablet01"]'
            '//div[@class="modal-header"]'
            '/a[@class="link-newWindow showTooltip" and @target="_blank"]'
        )
        self.assertEqual(nodes[0].get("href"), "original.tif")


class HTMLGenerator_TableWrapGroup_TableWrap_Table_Tests(unittest.TestCase):

    def setUp(self):
        xml = ("""
            <table-wrap-group id="t01">
                <table-wrap xml:lang="pt">
                    <label>Tabela 1</label>
                    <caption>
                        <title>Caption Tabela PT</title>
                    </caption>
                    <table-wrap-foot>
                        <fn id="TFN1a">
                            <p>Nota da tabela em pt</p>
                        </fn>
                    </table-wrap-foot>
                </table-wrap>
                <table-wrap xml:lang="en">
                    <label>Table 1</label>
                    <caption>
                        <title>Caption Tabela EN</title>
                    </caption>
                    <table></table>
                    <table-wrap-foot>
                        <fn id="TFN1">
                            <p><xref ref-type="table" rid="t01">Table 1</xref> Identification of <italic>Senna Senna</italic> Mill. (Fabaceae) species collected in different locations in northwestern Ceará State. <sup>*</sup> Exotic, <sup>**</sup> Endemic to Brazil. Source: Herbário Francisco José de Abreu Matos (HUVA).</p>
                        </fn>
                    </table-wrap-foot>
                </table-wrap>
            </table-wrap-group>
        """)
        self.html = _get_xml(xml)

    def test_enlarged_presentation(self):
        nodes = self.html.xpath(
            '//div[@class="modal fade ModalTables" and @id="ModalTablet01"]'
            '/div[@class="modal-dialog modal-lg"]'
            '/div[@class="modal-content"]'
            '/div[@class="modal-body"]'
            '/div[@class="table table-hover"]'
            '/table'
        )
        self.assertEqual(len(nodes), 1)


class HTMLGenerator_TableWrapGroup_TableWrap_Graphic_Tests(unittest.TestCase):
    def setUp(self):
        xml = ("""
            <table-wrap-group id="t01">
                <table-wrap xml:lang="pt">
                    <label>Tabela 1</label>
                    <caption>
                        <title>Caption Tabela PT</title>
                    </caption>
                    <table-wrap-foot>
                        <fn id="TFN1a">
                            <p>Nota da tabela em pt</p>
                        </fn>
                    </table-wrap-foot>
                </table-wrap>
                <table-wrap xml:lang="en">
                    <label>Table 1</label>
                    <caption>
                        <title>Caption Tabela EN</title>
                    </caption>
                    <graphic xlink:href="original"/>
                    <table-wrap-foot>
                        <fn id="TFN1">
                            <p><xref ref-type="table" rid="t01">Table 1</xref> Identification of <italic>Senna Senna</italic> Mill. (Fabaceae) species collected in different locations in northwestern Ceará State. <sup>*</sup> Exotic, <sup>**</sup> Endemic to Brazil. Source: Herbário Francisco José de Abreu Matos (HUVA).</p>
                        </fn>
                    </table-wrap-foot>
                </table-wrap>
            </table-wrap-group>
        """)
        self.html = _get_xml(xml)

    def test_enlarged_presentation(self):
        nodes = self.html.xpath(
            '//div[@class="modal fade ModalTables" and @id="ModalTablet01"]'
            '/div[@class="modal-dialog modal-lg"]'
            '/div[@class="modal-content"]'
            '/div[@class="modal-body"]'
            '/a[@href="original.jpg"]'
            '/img[@src="original.jpg"]'
        )
        self.assertEqual(len(nodes), 1)

    def test_original_presentation(self):
        nodes = self.html.xpath(
            '//div[@class="modal fade ModalTables" and @id="ModalTablet01"]'
            '//div[@class="modal-header"]'
            '/a[@class="link-newWindow showTooltip" and @target="_blank"]'
        )
        self.assertEqual(nodes[0].get("href"), "original.jpg")


class HTMLGenerator_TableWrapGroup_TableWrap_Alternatives_TableAndGraphic_Tests(unittest.TestCase):
    def setUp(self):
        xml = ("""
            <table-wrap-group id="t01">
                <table-wrap xml:lang="pt">
                    <label>Tabela 1</label>
                    <caption>
                        <title>Caption Tabela PT</title>
                    </caption>
                    <table-wrap-foot>
                        <fn id="TFN1a">
                            <p>Nota da tabela em pt</p>
                        </fn>
                    </table-wrap-foot>
                </table-wrap>
                <table-wrap xml:lang="en">
                    <label>Table 1</label>
                    <caption>
                        <title>Caption Tabela EN</title>
                    </caption>
                    <alternatives>
                        <table>
                            <tr><td>Conteúdo da tabela</td></tr>
                        </table>
                        <graphic xlink:href="original.svg" />
                    </alternatives>
                    <table-wrap-foot>
                        <fn id="TFN1">
                            <p><xref ref-type="table" rid="t01">Table 1</xref> Identification of <italic>Senna Senna</italic> Mill. (Fabaceae) species collected in different locations in northwestern Ceará State. <sup>*</sup> Exotic, <sup>**</sup> Endemic to Brazil. Source: Herbário Francisco José de Abreu Matos (HUVA).</p>
                        </fn>
                    </table-wrap-foot>
                </table-wrap>
            </table-wrap-group>
        """)
        self.html = _get_xml(xml)

    def test_enlarged_presentation(self):
        nodes = self.html.xpath(
            '//div[@class="modal fade ModalTables" and @id="ModalTablet01"]'
            '/div[@class="modal-dialog modal-lg"]'
            '/div[@class="modal-content"]'
            '/div[@class="modal-body"]'
            '/div[@class="table table-hover"]'
            '/table'
        )
        self.assertEqual(len(nodes), 1)

    def test_original_presentation(self):
        nodes = self.html.xpath(
            '//div[@class="modal fade ModalTables" and @id="ModalTablet01"]'
            '//div[@class="modal-header"]'
            '/a[@class="link-newWindow showTooltip" and @target="_blank"]'
        )
        self.assertEqual(nodes[0].get("href"), "original.svg")


class HTMLGenerator_TableWrapGroup_TableWrap_Alternatives_Graphics_Tests(unittest.TestCase):

    def setUp(self):
        xml = ("""
            <table-wrap-group id="t01">
                <table-wrap xml:lang="pt">
                    <label>Tabela 1</label>
                    <caption>
                        <title>Caption Tabela PT</title>
                    </caption>
                    <table-wrap-foot>
                        <fn id="TFN1a">
                            <p>Nota da tabela em pt</p>
                        </fn>
                    </table-wrap-foot>
                </table-wrap>
                <table-wrap xml:lang="en">
                    <label>Table 1</label>
                    <caption>
                        <title>Caption Tabela EN</title>
                    </caption>
                    <alternatives>
                        <graphic xlink:href="original.tif" />
                        <graphic xlink:href="ampliada.png" specific-use="scielo-web" />
                        <graphic xlink:href="miniatura.jpg" specific-use="scielo-web" content-type="scielo-20x20" />
                    </alternatives>
                    <table-wrap-foot>
                        <fn id="TFN1">
                            <p><xref ref-type="table" rid="t01">Table 1</xref> Identification of <italic>Senna Senna</italic> Mill. (Fabaceae) species collected in different locations in northwestern Ceará State. <sup>*</sup> Exotic, <sup>**</sup> Endemic to Brazil. Source: Herbário Francisco José de Abreu Matos (HUVA).</p>
                        </fn>
                    </table-wrap-foot>
                </table-wrap>
            </table-wrap-group>
        """)
        self.html = _get_xml(xml)

    def test_enlarged_presentation(self):
        nodes = self.html.xpath(
            '//div[@class="modal fade ModalTables" and @id="ModalTablet01"]'
            '/div[@class="modal-dialog modal-lg"]'
            '/div[@class="modal-content"]'
            '/div[@class="modal-body"]'
            '/a[@href="ampliada.png"]'
            '/img[@src="ampliada.png"]'
        )
        self.assertEqual(len(nodes), 1)

    def test_thumbnail_presentation(self):
        nodes = self.html.xpath(
            '//div[@class="row table" and @id="t01"]'
            '/div[@class="col-md-4 col-sm-4"]'
            '/a'
            '/div[@class="thumbOff"]'
        )
        self.assertEqual(len(nodes), 1)

    def test_original_presentation(self):
        nodes = self.html.xpath(
            '//div[@class="modal fade ModalTables" and @id="ModalTablet01"]'
            '//div[@class="modal-header"]'
            '/a[@class="link-newWindow showTooltip" and @target="_blank"]'
        )
        self.assertEqual(nodes[0].get("href"), "original.tif")
