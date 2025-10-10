import unittest

from lxml import etree

from packtools.sps.utils.xml_fixer import (
    fix_inline_graphic_in_caption,
    _find_inline_graphics_in_caption_or_label,
    _get_parent_container,
    _group_inline_graphics_by_container,
    _has_existing_graphic,
    _create_graphic_from_inline,
    _get_insert_position,
)


class XMLFixerHelperFunctionsTest(unittest.TestCase):
    """Testes para funções auxiliares"""

    def test_find_inline_graphics_in_caption_or_label(self):
        """Testa a busca de inline-graphics em caption e label"""
        xml = """<fig xmlns:xlink="http://www.w3.org/1999/xlink">
          <label>Label<inline-graphic xlink:href="img1.jpg"/></label>
          <caption><title>Title<inline-graphic xlink:href="img2.jpg"/></title></caption>
          <inline-graphic xlink:href="img3.jpg"/>
        </fig>"""
        tree = etree.fromstring(xml)
        result = _find_inline_graphics_in_caption_or_label(tree)

        self.assertEqual(len(result), 2)  # Apenas os 2 primeiros

    def test_get_parent_container_success(self):
        """Testa obtenção do container pai"""
        xml = """<fig xmlns:xlink="http://www.w3.org/1999/xlink">
          <caption><inline-graphic xlink:href="img1.jpg"/></caption>
        </fig>"""
        tree = etree.fromstring(xml)
        inline_graphic = tree.find(".//inline-graphic")
        container = _get_parent_container(inline_graphic)

        self.assertIsNotNone(container)
        self.assertEqual(container.tag, "fig")

    def test_get_parent_container_none(self):
        """Testa quando não há container válido"""
        xml = """<p xmlns:xlink="http://www.w3.org/1999/xlink">
          <inline-graphic xlink:href="img1.jpg"/>
        </p>"""
        tree = etree.fromstring(xml)
        inline_graphic = tree.find(".//inline-graphic")
        container = _get_parent_container(inline_graphic)

        self.assertIsNone(container)

    def test_group_inline_graphics_by_container(self):
        """Testa agrupamento por container"""
        xml = """<article xmlns:xlink="http://www.w3.org/1999/xlink">
          <fig id="f1">
            <caption><inline-graphic xlink:href="img1.jpg"/></caption>
          </fig>
          <fig id="f2">
            <label><inline-graphic xlink:href="img2.jpg"/></label>
            <caption><inline-graphic xlink:href="img3.jpg"/></caption>
          </fig>
        </article>"""
        tree = etree.fromstring(xml)
        inline_graphics = tree.findall(".//inline-graphic")
        grouped = _group_inline_graphics_by_container(inline_graphics)

        self.assertEqual(len(grouped), 2)  # 2 containers
        fig2 = tree.find(".//fig[@id='f2']")
        self.assertEqual(len(grouped[fig2]), 2)  # 2 inline-graphics no fig2

    def test_has_existing_graphic(self):
        """Testa verificação de graphic existente"""
        xml1 = """<fig><graphic xlink:href="img.jpg" xmlns:xlink="http://www.w3.org/1999/xlink"/></fig>"""
        xml2 = """<fig><caption><title>No graphic</title></caption></fig>"""

        tree1 = etree.fromstring(xml1)
        tree2 = etree.fromstring(xml2)

        self.assertTrue(_has_existing_graphic(tree1))
        self.assertFalse(_has_existing_graphic(tree2))

    def test_create_graphic_from_inline(self):
        """Testa criação de graphic preservando atributos"""
        xml = """<fig xmlns:xlink="http://www.w3.org/1999/xlink">
          <caption><inline-graphic xlink:href="img.jpg" id="ig1" content-type="image/jpeg"/></caption>
        </fig>"""
        tree = etree.fromstring(xml)
        inline_graphic = tree.find(".//inline-graphic")
        graphic = _create_graphic_from_inline(inline_graphic)

        self.assertEqual(graphic.tag, "graphic")
        self.assertEqual(graphic.get("{http://www.w3.org/1999/xlink}href"), "img.jpg")
        self.assertEqual(graphic.get("id"), "ig1")
        self.assertEqual(graphic.get("content-type"), "image/jpeg")

    def test_get_insert_position(self):
        """Testa cálculo da posição de inserção"""
        xml = """<fig>
          <label>Label</label>
          <caption>Caption</caption>
          <p>Paragraph</p>
        </fig>"""
        tree = etree.fromstring(xml)
        position = _get_insert_position(tree)

        self.assertEqual(position, 2)  # Após label e caption


class XMLFixerIntegrationTest(unittest.TestCase):
    """Testes de integração da função principal"""

    def test_fix_inline_graphic_simple_case(self):
        """Teste básico: inline-graphic dentro de caption"""
        xml = """<fig id="f1" xmlns:xlink="http://www.w3.org/1999/xlink">
          <label>Figura 1</label>
          <caption><title>Título<inline-graphic xlink:href="img1.jpg"/></title></caption>
        </fig>"""
        tree = etree.fromstring(xml)
        mods = fix_inline_graphic_in_caption(tree)

        self.assertEqual(len(mods), 1)
        self.assertEqual(mods[0]["action"], "moved_and_renamed")
        self.assertIsNotNone(tree.find(".//graphic"))
        self.assertIsNone(tree.find(".//inline-graphic"))

    def test_fix_inline_graphic_in_label(self):
        """Teste: inline-graphic dentro de label"""
        xml = """<fig id="f1" xmlns:xlink="http://www.w3.org/1999/xlink">
          <label>Figura 1<inline-graphic xlink:href="img1.jpg"/></label>
          <caption><title>Título da figura</title></caption>
        </fig>"""
        tree = etree.fromstring(xml)
        mods = fix_inline_graphic_in_caption(tree)

        self.assertEqual(len(mods), 1)
        self.assertEqual(mods[0]["old_parent"], "label")
        self.assertEqual(mods[0]["new_parent"], "fig")
        self.assertIsNotNone(tree.find(".//graphic"))
        self.assertIsNone(tree.find(".//inline-graphic"))

    def test_multiple_inline_graphics_different_containers(self):
        """Teste: múltiplos inline-graphics em diferentes containers"""
        xml = """<article xmlns:xlink="http://www.w3.org/1999/xlink">
          <fig id="f1">
            <label>Figura 1</label>
            <caption><title>Título<inline-graphic xlink:href="img1.jpg"/></title></caption>
          </fig>
          <fig id="f2">
            <label>Figura 2<inline-graphic xlink:href="img2.jpg"/></label>
            <caption><title>Outra figura</title></caption>
          </fig>
        </article>"""
        tree = etree.fromstring(xml)
        mods = fix_inline_graphic_in_caption(tree)

        self.assertEqual(len(mods), 2)
        graphics = tree.findall(".//graphic")
        self.assertEqual(len(graphics), 2)
        self.assertIsNone(tree.find(".//inline-graphic"))

    def test_multiple_inline_graphics_same_container_no_modification(self):
        """Teste: múltiplos inline-graphics no MESMO container - NÃO deve modificar"""
        xml = """<fig id="f1" xmlns:xlink="http://www.w3.org/1999/xlink">
          <label>Figura 1<inline-graphic xlink:href="img1.jpg"/></label>
          <caption><title>Título<inline-graphic xlink:href="img2.jpg"/></title></caption>
        </fig>"""
        tree = etree.fromstring(xml)
        mods = fix_inline_graphic_in_caption(tree)

        self.assertEqual(len(mods), 0)
        inline_graphics = tree.findall(".//inline-graphic")
        self.assertEqual(len(inline_graphics), 2)
        self.assertIsNone(tree.find(".//graphic"))

    def test_two_inline_graphics_in_caption(self):
        """Teste: dois inline-graphics dentro do caption - NÃO deve modificar"""
        xml = """<fig id="f1" xmlns:xlink="http://www.w3.org/1999/xlink">
          <label>Figura 1</label>
          <caption>
            <title>Título<inline-graphic xlink:href="img1.jpg"/></title>
            <p>Texto<inline-graphic xlink:href="img2.jpg"/></p>
          </caption>
        </fig>"""
        tree = etree.fromstring(xml)
        mods = fix_inline_graphic_in_caption(tree)

        self.assertEqual(len(mods), 0)
        inline_graphics = tree.findall(".//inline-graphic")
        self.assertEqual(len(inline_graphics), 2)
        self.assertIsNone(tree.find(".//graphic"))

    def test_graphic_already_exists(self):
        """Teste: não deve modificar quando graphic já existe"""
        xml = """<fig id="f1" xmlns:xlink="http://www.w3.org/1999/xlink">
          <label>Figura 1</label>
          <caption><title>Título<inline-graphic xlink:href="img1.jpg"/></title></caption>
          <graphic xlink:href="existing.jpg"/>
        </fig>"""
        tree = etree.fromstring(xml)
        mods = fix_inline_graphic_in_caption(tree)

        self.assertEqual(len(mods), 0)
        self.assertIsNotNone(tree.find(".//inline-graphic"))
        graphics = tree.findall(".//graphic")
        self.assertEqual(len(graphics), 1)

    def test_table_wrap_context(self):
        """Teste: inline-graphic em contexto de table-wrap"""
        xml = """<table-wrap id="t1" xmlns:xlink="http://www.w3.org/1999/xlink">
          <label>Tabela 1</label>
          <caption><title>Título<inline-graphic xlink:href="table1.jpg"/></title></caption>
        </table-wrap>"""
        tree = etree.fromstring(xml)
        mods = fix_inline_graphic_in_caption(tree)

        self.assertEqual(len(mods), 1)
        self.assertEqual(mods[0]["new_parent"], "table-wrap")
        self.assertIsNotNone(tree.find(".//graphic"))
        self.assertIsNone(tree.find(".//inline-graphic"))

    def test_preserve_attributes(self):
        """Teste: preservação de todos os atributos"""
        xml = """<fig id="f1" xmlns:xlink="http://www.w3.org/1999/xlink">
          <label>Figura 1</label>
          <caption><title>Título<inline-graphic xlink:href="img1.jpg" id="ig1" content-type="image/jpeg"/></title></caption>
        </fig>"""
        tree = etree.fromstring(xml)
        mods = fix_inline_graphic_in_caption(tree)

        graphic = tree.find(".//graphic")
        self.assertIsNotNone(graphic)
        self.assertEqual(graphic.get("{http://www.w3.org/1999/xlink}href"), "img1.jpg")
        self.assertEqual(graphic.get("id"), "ig1")
        self.assertEqual(graphic.get("content-type"), "image/jpeg")

    def test_inline_graphic_position_after_caption(self):
        """Teste: graphic é inserido após label e caption"""
        xml = """<fig id="f1" xmlns:xlink="http://www.w3.org/1999/xlink">
          <label>Figura 1</label>
          <caption><title>Título<inline-graphic xlink:href="img1.jpg"/></title></caption>
          <p>Algum texto</p>
        </fig>"""
        tree = etree.fromstring(xml)
        mods = fix_inline_graphic_in_caption(tree)

        children = list(tree)
        self.assertEqual(children[0].tag, "label")
        self.assertEqual(children[1].tag, "caption")
        self.assertEqual(children[2].tag, "graphic")
        self.assertEqual(children[3].tag, "p")

    def test_empty_modifications_no_inline_graphics(self):
        """Teste: retorna lista vazia quando não há inline-graphics"""
        xml = """<fig id="f1">
          <label>Figura 1</label>
          <caption><title>Título</title></caption>
          <graphic xlink:href="img1.jpg" xmlns:xlink="http://www.w3.org/1999/xlink"/>
        </fig>"""
        tree = etree.fromstring(xml)
        mods = fix_inline_graphic_in_caption(tree)

        self.assertEqual(len(mods), 0)


if __name__ == "__main__":
    unittest.main()
