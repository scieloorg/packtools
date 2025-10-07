# coding: utf-8
import unittest
from lxml import etree

from packtools.sps.utils import xml_fixer


class TestFixInlineGraphicInCaptionAndLabel(unittest.TestCase):
    """Testes para a função fix_inline_graphic_in_caption_and_label."""

    def test_simple_inline_graphic_in_caption_title(self):
        """Testa correção de inline-graphic simples dentro de caption/title."""
        xml = etree.fromstring(
            b"""<fig id="f1">
                <label>Figura 1</label>
                <caption>
                    <title>T\xc3\xadtulo da figura<inline-graphic xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="img1.jpg"/></title>
                </caption>
            </fig>"""
        )
        
        changes = xml_fixer.fix_inline_graphic_in_caption_and_label(xml)
        
        # Verifica que houve uma mudança
        self.assertEqual(len(changes), 1)
        self.assertEqual(changes[0]['action'], 'moved_and_renamed')
        self.assertEqual(changes[0]['old_parent'], 'title')
        self.assertEqual(changes[0]['new_parent'], 'fig')
        
        # Verifica que inline-graphic foi removido de caption
        inline_graphics_in_caption = xml.xpath(".//caption//inline-graphic")
        self.assertEqual(len(inline_graphics_in_caption), 0)
        
        # Verifica que graphic foi adicionado ao fig
        graphics = xml.findall(".//graphic")
        self.assertEqual(len(graphics), 1)
        
        # Verifica que o atributo foi preservado
        graphic = graphics[0]
        self.assertEqual(
            graphic.get("{http://www.w3.org/1999/xlink}href"), 
            "img1.jpg"
        )

    def test_inline_graphic_in_label(self):
        """Testa correção de inline-graphic dentro de label."""
        xml = etree.fromstring(
            b"""<fig id="f2">
                <label>Figura 2<inline-graphic xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="icon.png"/></label>
                <caption><title>T\xc3\xadtulo</title></caption>
            </fig>"""
        )
        
        changes = xml_fixer.fix_inline_graphic_in_caption_and_label(xml)
        
        # Verifica que houve uma mudança
        self.assertEqual(len(changes), 1)
        self.assertEqual(changes[0]['action'], 'moved_and_renamed')
        self.assertEqual(changes[0]['old_parent'], 'label')
        self.assertEqual(changes[0]['new_parent'], 'fig')
        
        # Verifica que inline-graphic foi removido de label
        inline_graphics_in_label = xml.xpath(".//label//inline-graphic")
        self.assertEqual(len(inline_graphics_in_label), 0)
        
        # Verifica que graphic foi adicionado
        graphics = xml.findall(".//graphic")
        self.assertEqual(len(graphics), 1)

    def test_multiple_inline_graphics(self):
        """Testa correção de múltiplos inline-graphics."""
        xml = etree.fromstring(
            b"""<article>
                <body>
                    <fig id="f1">
                        <label>Figura 1</label>
                        <caption>
                            <title>T\xc3\xadtulo 1<inline-graphic xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="img1.jpg"/></title>
                        </caption>
                    </fig>
                    <table-wrap id="t1">
                        <label>Tabela 1</label>
                        <caption>
                            <title>T\xc3\xadtulo 2<inline-graphic xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="img2.jpg"/></title>
                        </caption>
                    </table-wrap>
                </body>
            </article>"""
        )
        
        changes = xml_fixer.fix_inline_graphic_in_caption_and_label(xml)
        
        # Verifica que houve duas mudanças
        self.assertEqual(len(changes), 2)
        
        # Verifica que não há mais inline-graphics em caption
        inline_graphics_in_caption = xml.xpath(".//caption//inline-graphic")
        self.assertEqual(len(inline_graphics_in_caption), 0)
        
        # Verifica que foram criados dois graphics
        graphics = xml.findall(".//graphic")
        self.assertEqual(len(graphics), 2)
        
        # Verifica que estão nos lugares corretos
        fig_graphic = xml.find(".//fig[@id='f1']/graphic")
        self.assertIsNotNone(fig_graphic)
        
        table_graphic = xml.find(".//table-wrap[@id='t1']/graphic")
        self.assertIsNotNone(table_graphic)

    def test_graphic_already_exists(self):
        """Testa que não modifica quando graphic já existe no pai."""
        xml = etree.fromstring(
            b"""<fig id="f3">
                <label>Figura 3</label>
                <caption>
                    <title>T\xc3\xadtulo<inline-graphic xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="img_wrong.jpg"/></title>
                </caption>
                <graphic xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="img_correct.jpg"/>
            </fig>"""
        )
        
        changes = xml_fixer.fix_inline_graphic_in_caption_and_label(xml)
        
        # Verifica que não houve mudanças
        self.assertEqual(len(changes), 0)
        
        # Verifica que inline-graphic ainda está em caption
        inline_graphics_in_caption = xml.xpath(".//caption//inline-graphic")
        self.assertEqual(len(inline_graphics_in_caption), 1)
        
        # Verifica que graphic original permanece
        graphics = xml.findall(".//graphic")
        self.assertEqual(len(graphics), 1)
        self.assertEqual(
            graphics[0].get("{http://www.w3.org/1999/xlink}href"),
            "img_correct.jpg"
        )

    def test_table_wrap_context(self):
        """Testa correção em contexto de table-wrap."""
        xml = etree.fromstring(
            b"""<table-wrap id="t1">
                <label>Tabela 1</label>
                <caption>
                    <title>T\xc3\xadtulo da tabela<inline-graphic xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="table_img.jpg"/></title>
                </caption>
                <table>
                    <tbody>
                        <tr><td>Dados</td></tr>
                    </tbody>
                </table>
            </table-wrap>"""
        )
        
        changes = xml_fixer.fix_inline_graphic_in_caption_and_label(xml)
        
        # Verifica que houve uma mudança
        self.assertEqual(len(changes), 1)
        self.assertEqual(changes[0]['new_parent'], 'table-wrap')
        
        # Verifica que graphic foi adicionado a table-wrap
        graphics = xml.findall(".//graphic")
        self.assertEqual(len(graphics), 1)

    def test_boxed_text_context(self):
        """Testa correção em contexto de boxed-text."""
        xml = etree.fromstring(
            b"""<boxed-text id="bx1">
                <label>Box 1</label>
                <caption>
                    <title>T\xc3\xadtulo do box<inline-graphic xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="box_img.jpg"/></title>
                </caption>
                <p>Conte\xc3\xbado do box</p>
            </boxed-text>"""
        )
        
        changes = xml_fixer.fix_inline_graphic_in_caption_and_label(xml)
        
        # Verifica que houve uma mudança
        self.assertEqual(len(changes), 1)
        self.assertEqual(changes[0]['new_parent'], 'boxed-text')
        
        # Verifica que graphic foi adicionado
        graphics = xml.findall(".//graphic")
        self.assertEqual(len(graphics), 1)

    def test_preserves_all_attributes(self):
        """Testa que todos os atributos são preservados."""
        xml = etree.fromstring(
            b"""<fig id="f4">
                <label>Figura 4</label>
                <caption>
                    <title>T\xc3\xadtulo<inline-graphic id="ig1" xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="img.jpg" content-type="image/jpeg"/></title>
                </caption>
            </fig>"""
        )
        
        changes = xml_fixer.fix_inline_graphic_in_caption_and_label(xml)
        
        # Verifica que houve uma mudança
        self.assertEqual(len(changes), 1)
        
        # Verifica que todos os atributos foram preservados
        graphic = xml.find(".//graphic")
        self.assertIsNotNone(graphic)
        self.assertEqual(graphic.get("id"), "ig1")
        self.assertEqual(
            graphic.get("{http://www.w3.org/1999/xlink}href"),
            "img.jpg"
        )
        self.assertEqual(graphic.get("content-type"), "image/jpeg")

    def test_preserves_namespaces(self):
        """Testa que namespaces são preservados."""
        xml = etree.fromstring(
            b"""<fig id="f5" xmlns:xlink="http://www.w3.org/1999/xlink">
                <label>Figura 5</label>
                <caption>
                    <title>T\xc3\xadtulo<inline-graphic xlink:href="img.jpg"/></title>
                </caption>
            </fig>"""
        )
        
        changes = xml_fixer.fix_inline_graphic_in_caption_and_label(xml)
        
        # Verifica que houve uma mudança
        self.assertEqual(len(changes), 1)
        
        # Verifica que namespace foi preservado
        graphic = xml.find(".//graphic")
        self.assertIsNotNone(graphic)
        self.assertEqual(
            graphic.get("{http://www.w3.org/1999/xlink}href"),
            "img.jpg"
        )

    def test_caption_without_title(self):
        """Testa correção quando inline-graphic está diretamente em caption sem title."""
        xml = etree.fromstring(
            b"""<fig id="f6">
                <label>Figura 6</label>
                <caption>
                    <p>Par\xc3\xa1grafo<inline-graphic xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="img.jpg"/></p>
                </caption>
            </fig>"""
        )
        
        changes = xml_fixer.fix_inline_graphic_in_caption_and_label(xml)
        
        # Verifica que houve uma mudança
        self.assertEqual(len(changes), 1)
        
        # Verifica que graphic foi adicionado
        graphics = xml.findall(".//graphic")
        self.assertEqual(len(graphics), 1)

    def test_no_inline_graphics(self):
        """Testa que retorna lista vazia quando não há inline-graphics para corrigir."""
        xml = etree.fromstring(
            b"""<fig id="f7">
                <label>Figura 7</label>
                <caption><title>T\xc3\xadtulo</title></caption>
                <graphic xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="img.jpg"/>
            </fig>"""
        )
        
        changes = xml_fixer.fix_inline_graphic_in_caption_and_label(xml)
        
        # Verifica que não houve mudanças
        self.assertEqual(len(changes), 0)

    def test_inline_graphic_outside_caption_label_not_affected(self):
        """Testa que inline-graphics fora de caption/label não são afetados."""
        xml = etree.fromstring(
            b"""<article>
                <body>
                    <fig id="f8">
                        <label>Figura 8</label>
                        <caption><title>T\xc3\xadtulo</title></caption>
                    </fig>
                    <p>Par\xc3\xa1grafo com <inline-graphic xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="icon.png"/> inline</p>
                </body>
            </article>"""
        )
        
        changes = xml_fixer.fix_inline_graphic_in_caption_and_label(xml)
        
        # Verifica que não houve mudanças
        self.assertEqual(len(changes), 0)
        
        # Verifica que inline-graphic ainda está no parágrafo
        inline_graphics = xml.xpath(".//p//inline-graphic")
        self.assertEqual(len(inline_graphics), 1)


if __name__ == "__main__":
    unittest.main()
