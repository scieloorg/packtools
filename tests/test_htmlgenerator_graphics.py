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
        <p>
            {text}
        </p>
        <p>
        <graphic xlink:href="imagem2.jpg"/>
        </p>
        </sec>
      </body>
    </article>"""
    )
    et = get_xml_tree_from_string(xml)
    return domain.HTMLGenerator.parse(et, valid_only=False).generate('pt')


class HTMLGenerator_Graphic_Tiff_Tests(unittest.TestCase):
    def setUp(self):
        xml = """
            <graphic xlink:href="figure1.tif" />
        """
        self.html = _get_xml(xml)

    def test_modal_presentation(self):
        nodes = self.html.xpath(
            '//div[@class="modal fade ModalFigs" and @id="ModalImgfigure1"]'
            '/div[@class="modal-dialog modal-lg"]'
            '/div[@class="modal-content"]'
            '/div[@class="modal-body"]'
            '/img[@src="figure1.jpg"]'
        )
        self.assertEqual(len(nodes), 1)

    def test_thumbnail_presentation(self):
        nodes = self.html.xpath(
            '//div[@class="row fig" and @id="figure1"]'
            '/div[@class="col-md-4 col-sm-4"]'
            '/a[@data-target="#ModalImgfigure1"]'
            '/div/img[@src="figure1.jpg"]'
        )
        self.assertEqual(len(nodes), 1)

    def test_original_presentation(self):
        nodes = self.html.xpath(
            '//div[@class="modal fade ModalFigs" and @id="ModalImgfigure1"]'
            '//div[@class="modal-header"]'
            '/a[@class="link-newWindow showTooltip" and @target="_blank"]'
        )
        self.assertEqual(nodes[0].get("href"), "figure1.jpg")


class HTMLGenerator_Graphic_Png_Tests(unittest.TestCase):
    def setUp(self):
        xml = """
            <graphic xlink:href="figure1.png"/>
        """
        self.html = _get_xml(xml)

    def test_modal_presentation(self):
        nodes = self.html.xpath(
            '//div[@class="modal fade ModalFigs" and @id="ModalImgfigure1"]'
            '/div[@class="modal-dialog modal-lg"]'
            '/div[@class="modal-content"]'
            '/div[@class="modal-body"]'
            '/img[@src="figure1.png"]'
        )
        self.assertEqual(len(nodes), 1)

    def test_thumbnail_presentation(self):
        nodes = self.html.xpath(
            '//div[@class="row fig" and @id="figure1"]'
            '/div[@class="col-md-4 col-sm-4"]'
            '/a[@data-target="#ModalImgfigure1"]'
            '/div/img[@src="figure1.png"]'
        )
        self.assertEqual(len(nodes), 1)

    def test_original_presentation(self):
        nodes = self.html.xpath(
            '//div[@class="modal fade ModalFigs" and @id="ModalImgfigure1"]'
            '//div[@class="modal-header"]'
            '/a[@class="link-newWindow showTooltip" and @target="_blank"]'
        )
        self.assertEqual(nodes[0].get("href"), "figure1.png")


class HTMLGenerator_Graphic_NoExtension_Tests(unittest.TestCase):
    def setUp(self):
        xml = """
            <graphic xlink:href="figure1"/>
        """
        self.html = _get_xml(xml)

    def test_modal_presentation(self):
        nodes = self.html.xpath(
            '//div[@class="modal fade ModalFigs" and @id="ModalImgfigure1"]'
            '/div[@class="modal-dialog modal-lg"]'
            '/div[@class="modal-content"]'
            '/div[@class="modal-body"]'
            '/img[@src="figure1.jpg"]'
        )
        self.assertEqual(len(nodes), 1)

    def test_thumbnail_presentation(self):
        nodes = self.html.xpath(
            '//div[@class="row fig" and @id="figure1"]'
            '/div[@class="col-md-4 col-sm-4"]'
            '/a[@data-target="#ModalImgfigure1"]'
            '/div/img[@src="figure1.jpg"]'
        )
        self.assertEqual(len(nodes), 1)

    def test_original_presentation(self):
        nodes = self.html.xpath(
            '//div[@class="modal fade ModalFigs" and @id="ModalImgfigure1"]'
            '//div[@class="modal-header"]'
            '/a[@class="link-newWindow showTooltip" and @target="_blank"]'
        )
        self.assertEqual(nodes[0].get("href"), "figure1.jpg")


class HTMLGenerator_Graphic_SVG_Tests(unittest.TestCase):
    def setUp(self):
        xml = """
            <graphic xlink:href="figure1.svg"/>
        """
        self.html = _get_xml(xml)

    def test_modal_presentation(self):
        nodes = self.html.xpath(
            '//div[@class="modal fade ModalFigs" and @id="ModalImgfigure1"]'
            '/div[@class="modal-dialog modal-lg"]'
            '/div[@class="modal-content"]'
            '/div[@class="modal-body"]'
            '/object[@data="figure1.svg"]'
        )
        self.assertEqual(len(nodes), 1)

    def test_thumbnail_presentation(self):
        _print_debug(self.html)

        nodes = self.html.xpath(
            '//div[@class="row fig" and @id="figure1"]'
            '/div[@class="col-md-4 col-sm-4"]'
            '/a[@data-target="#ModalImgfigure1"]'
            '/div/object[@data="figure1.svg"]'

        )
        self.assertEqual(len(nodes), 1)

    def test_original_presentation(self):
        nodes = self.html.xpath(
            '//div[@class="modal fade ModalFigs" and @id="ModalImgfigure1"]'
            '//div[@class="modal-header"]'
            '/a[@class="link-newWindow showTooltip" and @target="_blank"]'
        )
        self.assertEqual(nodes[0].get("href"), "figure1.svg")


class HTMLGenerator_Alternatives_Graphics_Tests(unittest.TestCase):
    def setUp(self):
        xml = """

    <p>
      <alternatives>
        <graphic xlink:href="original.tiff"/>
        <graphic xlink:href="ampliada.png" specific-use="scielo-web"/>
        <graphic xlink:href="miniatura.jpg" specific-use="scielo-web" content-type="scielo-267x140"/>
      </alternatives>
    </p>
        """
        self.html = _get_xml(xml)

    def test_modal_presentation(self):
        nodes = self.html.xpath(
            '//div[@class="modal fade ModalFigs" and @id="ModalImgampliada"]'
            '/div[@class="modal-dialog modal-lg"]'
            '/div[@class="modal-content"]'
            '/div[@class="modal-body"]'
            '/img[@src="ampliada.png"]'
        )
        self.assertEqual(len(nodes), 1)

    def test_thumbnail_presentation(self):
        nodes = self.html.xpath(
            '//div[@class="row fig" and @id="ampliada"]'
            '/div[@class="col-md-4 col-sm-4"]'
            '/a[@data-target="#ModalImgampliada"]'
            '/div/img[@src="miniatura.jpg"]'
        )
        self.assertEqual(len(nodes), 1)

    def test_original_presentation(self):
        nodes = self.html.xpath(
            '//div[@class="modal fade ModalFigs" and @id="ModalImgampliada"]'
            '//div[@class="modal-header"]'
            '/a[@class="link-newWindow showTooltip" and @target="_blank"]'
        )
        self.assertEqual(nodes[0].get("href"), "original.tiff")
