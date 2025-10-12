import unittest
from lxml import etree

from packtools.sps.utils.xml_fixer import fix_inline_graphic_in_caption


class XMLFixerTest(unittest.TestCase):
    """Testes para fix_inline_graphic_in_caption - Abordagem 1"""

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

    def test_disp_formula_context(self):
        """Teste: inline-graphic em contexto de disp-formula"""
        xml = """<disp-formula id="eq1" xmlns:xlink="http://www.w3.org/1999/xlink">
          <label>(1)</label>
          <caption><title>Equação<inline-graphic xlink:href="eq1.jpg"/></title></caption>
        </disp-formula>"""
        tree = etree.fromstring(xml)
        mods = fix_inline_graphic_in_caption(tree)

        self.assertEqual(len(mods), 1)
        self.assertEqual(mods[0]["new_parent"], "disp-formula")
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

    def test_preserve_child_elements(self):
        """Teste: preservação de elementos filhos"""
        xml = """<fig id="f1" xmlns:xlink="http://www.w3.org/1999/xlink">
          <label>Figura 1</label>
          <caption>
            <title>Título
              <inline-graphic xlink:href="img1.jpg">
                <alt-text>Texto alternativo</alt-text>
              </inline-graphic>
            </title>
          </caption>
        </fig>"""
        tree = etree.fromstring(xml)
        mods = fix_inline_graphic_in_caption(tree)

        graphic = tree.find(".//graphic")
        self.assertIsNotNone(graphic)
        alt_text = graphic.find(".//alt-text")
        self.assertIsNotNone(alt_text)
        self.assertEqual(alt_text.text, "Texto alternativo")

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

    def test_position_after_label_only(self):
        """Teste: graphic após label quando não há caption"""
        xml = """<fig id="f1" xmlns:xlink="http://www.w3.org/1999/xlink">
          <label>Figura 1<inline-graphic xlink:href="img1.jpg"/></label>
          <p>Algum texto</p>
        </fig>"""
        tree = etree.fromstring(xml)
        mods = fix_inline_graphic_in_caption(tree)

        children = list(tree)
        self.assertEqual(children[0].tag, "label")
        self.assertEqual(children[1].tag, "graphic")
        self.assertEqual(children[2].tag, "p")

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

    def test_inline_graphic_outside_label_caption_ignored(self):
        """Teste: inline-graphic fora de label/caption é ignorado"""
        xml = """<fig id="f1" xmlns:xlink="http://www.w3.org/1999/xlink">
          <label>Figura 1</label>
          <caption><title>Título</title></caption>
          <p><inline-graphic xlink:href="img1.jpg"/></p>
        </fig>"""
        tree = etree.fromstring(xml)
        mods = fix_inline_graphic_in_caption(tree)

        self.assertEqual(len(mods), 0)
        self.assertIsNotNone(tree.find(".//inline-graphic"))

    def test_none_xmltree_raises_error(self):
        """Teste: xmltree None deve levantar ValueError"""
        with self.assertRaises(ValueError) as context:
            fix_inline_graphic_in_caption(None)

        self.assertIn("não pode ser None", str(context.exception))

    def test_modification_record_structure(self):
        """Teste: verifica estrutura do registro de modificação"""
        xml = """<fig id="f1" xmlns:xlink="http://www.w3.org/1999/xlink">
          <label>Figura 1</label>
          <caption><title>Título<inline-graphic xlink:href="img1.jpg"/></title></caption>
        </fig>"""
        tree = etree.fromstring(xml)
        mods = fix_inline_graphic_in_caption(tree)

        self.assertEqual(len(mods), 1)
        mod = mods[0]

        self.assertIn("xpath", mod)
        self.assertIn("action", mod)
        self.assertIn("old_parent", mod)
        self.assertIn("new_parent", mod)

        self.assertEqual(mod["action"], "moved_and_renamed")
        self.assertEqual(mod["old_parent"], "title")
        self.assertEqual(mod["new_parent"], "fig")
        self.assertIsInstance(mod["xpath"], str)

    def test_preserve_text_and_tail(self):
        """Teste: preserva text e tail do inline-graphic"""
        xml = """<fig xmlns:xlink="http://www.w3.org/1999/xlink">
          <caption><title>Antes<inline-graphic xlink:href="img.jpg"/>Depois</title></caption>
        </fig>"""
        tree = etree.fromstring(xml)

        inline = tree.find(".//inline-graphic")
        original_tail = inline.tail

        fix_inline_graphic_in_caption(tree)

        graphic = tree.find(".//graphic")
        self.assertIsNotNone(graphic)
        self.assertEqual(graphic.tail, original_tail)

    def test_complex_nested_structure(self):
        """Teste: estrutura complexa com múltiplos níveis"""
        xml = """<article xmlns:xlink="http://www.w3.org/1999/xlink">
          <body>
            <sec>
              <fig id="f1">
                <label>Fig 1</label>
                <caption>
                  <title>Título</title>
                  <p>Descrição<inline-graphic xlink:href="img1.jpg"/></p>
                </caption>
              </fig>
            </sec>
          </body>
        </article>"""
        tree = etree.fromstring(xml)
        mods = fix_inline_graphic_in_caption(tree)

        self.assertEqual(len(mods), 1)
        fig = tree.find(".//fig")
        self.assertIsNotNone(fig.find(".//graphic"))
        self.assertIsNone(fig.find(".//inline-graphic"))

    def test_multiple_containers_mixed_scenarios(self):
        """Teste: múltiplos containers com cenários mistos"""
        xml = """<article xmlns:xlink="http://www.w3.org/1999/xlink">
          <fig id="f1">
            <caption><inline-graphic xlink:href="img1.jpg"/></caption>
          </fig>
          <fig id="f2">
            <caption><inline-graphic xlink:href="img2.jpg"/></caption>
            <graphic xlink:href="existing.jpg"/>
          </fig>
          <table-wrap id="t1">
            <caption><inline-graphic xlink:href="img3.jpg"/></caption>
          </table-wrap>
        </article>"""
        tree = etree.fromstring(xml)
        mods = fix_inline_graphic_in_caption(tree)

        # f1: deve modificar (não tem graphic)
        # f2: não deve modificar (já tem graphic)
        # t1: deve modificar (não tem graphic)
        self.assertEqual(len(mods), 2)

        f1 = tree.find(".//fig[@id='f1']")
        f2 = tree.find(".//fig[@id='f2']")
        t1 = tree.find(".//table-wrap[@id='t1']")

        self.assertIsNotNone(f1.find("graphic"))
        self.assertIsNone(f1.find(".//inline-graphic"))

        self.assertIsNotNone(f2.find(".//inline-graphic"))
        self.assertEqual(len(f2.findall("graphic")), 1)

        self.assertIsNotNone(t1.find("graphic"))
        self.assertIsNone(t1.find(".//inline-graphic"))

    def test_no_valid_container_parent(self):
        """Teste: inline-graphic em elemento não-container é ignorado"""
        xml = """<article xmlns:xlink="http://www.w3.org/1999/xlink">
          <p>
            <caption><inline-graphic xlink:href="img1.jpg"/></caption>
          </p>
          <sec>
            <label><inline-graphic xlink:href="img2.jpg"/></label>
          </sec>
        </article>"""
        tree = etree.fromstring(xml)
        mods = fix_inline_graphic_in_caption(tree)

        # XPath não encontra estes elementos porque não são containers válidos
        self.assertEqual(len(mods), 0)
        # inline-graphics permanecem
        self.assertEqual(len(tree.findall(".//inline-graphic")), 2)


if __name__ == "__main__":
    unittest.main()
