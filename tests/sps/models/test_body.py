from unittest import TestCase

from lxml import etree
from packtools.sps.models.body import _get_texts, Body


class GetTextsTest(TestCase):

    def test_get_texts_text_only(self):
        xml = (
            """<article><body><p>texto </p></body></article>"""
        )
        xmltree = etree.fromstring(xml)
        node = xmltree.find(".//p")
        self.assertEqual("texto", _get_texts(node))

    def test_get_texts_with_bold(self):
        xml = (
            """<article><body><p>texto <bold>bold</bold> after bold </p></body></article>"""
        )
        xmltree = etree.fromstring(xml)
        node = xmltree.find(".//p")
        self.assertEqual("texto bold after bold", _get_texts(node))

    def test_get_texts_with_bold_and_italic_and_graphic(self):
        xml = (
            """<article><body>"""
            """<p>texto <bold>bold <italic>ITALIC</italic> after italic</bold> after bold """
            """<graphic/> after graphic </p>"""
            """</body></article>"""
        )
        xmltree = etree.fromstring(xml)
        node = xmltree.find(".//p")
        self.assertEqual("texto bold ITALIC after italic after bold after graphic", _get_texts(node))


class BodyTest(TestCase):

    def test_texts_text_only(self):
        xml = (
            """<article><body><p>texto </p></body></article>"""
        )
        xmltree = etree.fromstring(xml)
        body = Body(xmltree)
        self.assertEqual(["texto"], list(body.main_body_texts))

    def test_texts_with_bold(self):
        xml = (
            """<article><body><p>texto <bold>bold</bold> after bold </p></body></article>"""
        )
        xmltree = etree.fromstring(xml)
        body = Body(xmltree)
        self.assertEqual(
            ["texto bold after bold"],
            list(body.main_body_texts)
        )

    def test_texts_with_bold_and_italic_and_graphic(self):
        xml = (
            """<article><body>"""
            """<p>texto <bold>bold <italic>ITALIC</italic> after italic</bold> after bold """
            """<graphic/> after graphic </p>"""
            """</body></article>"""
        )
        xmltree = etree.fromstring(xml)
        body = Body(xmltree)
        self.assertEqual(
            ["texto bold ITALIC after italic after bold after graphic"],
            list(body.main_body_texts)
        )

    def test_texts_from_sec(self):
        xml = (
            """<article><body>"""
            """<sec><p>texto <bold>bold <italic>ITALIC</italic> after italic</bold> after bold """
            """<graphic/> after graphic </p>"""
            """</sec></body></article>"""
        )
        xmltree = etree.fromstring(xml)
        body = Body(xmltree)
        self.assertEqual(
            ["texto bold ITALIC after italic after bold after graphic"],
            list(body.main_body_texts)
        )

    def test_texts_from_sec_and_p(self):
        xml = (
            """<article><body>"""
            """<sec><p>texto <bold>bold <italic>ITALIC</italic> after italic</bold> after bold """
            """<graphic/> after graphic </p></sec>"""
            """<p>parágrafo 2 texto <bold>bold <italic>ITALIC</italic> after italic</bold> after bold """
            """<graphic/> after graphic </p>"""
            """</body></article>"""
        )
        xmltree = etree.fromstring(xml)
        body = Body(xmltree)
        self.assertEqual(
            ["texto bold ITALIC after italic after bold after graphic",
             "parágrafo 2 texto bold ITALIC after italic after bold after graphic"
            ],
            list(body.main_body_texts)
        )
