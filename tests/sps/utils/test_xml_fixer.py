import unittest
from lxml import etree

from packtools.sps.utils.xml_fixer import fix_inline_graphic_in_caption


class XMLFixerTest(unittest.TestCase):
    """Tests for fix_inline_graphic_in_caption"""

    def test_fix_inline_graphic_simple_case(self):
        """Basic test: inline-graphic inside caption"""
        xml = """<fig id="f1" xmlns:xlink="http://www.w3.org/1999/xlink">
          <label>Figure 1</label>
          <caption><title>Title<inline-graphic xlink:href="img1.jpg"/></title></caption>
        </fig>"""
        tree = etree.fromstring(xml)
        mods = fix_inline_graphic_in_caption(tree)

        self.assertEqual(len(mods), 1)
        self.assertEqual(mods[0]["action"], "moved_and_renamed")
        self.assertIsNotNone(tree.find(".//graphic"))
        self.assertIsNone(tree.find(".//inline-graphic"))

    def test_fix_inline_graphic_in_label(self):
        """Test: inline-graphic inside label"""
        xml = """<fig id="f1" xmlns:xlink="http://www.w3.org/1999/xlink">
          <label>Figure 1<inline-graphic xlink:href="img1.jpg"/></label>
          <caption><title>Figure title</title></caption>
        </fig>"""
        tree = etree.fromstring(xml)
        mods = fix_inline_graphic_in_caption(tree)

        self.assertEqual(len(mods), 1)
        self.assertEqual(mods[0]["old_parent"], "label")
        self.assertEqual(mods[0]["new_parent"], "fig")
        self.assertIsNotNone(tree.find(".//graphic"))
        self.assertIsNone(tree.find(".//inline-graphic"))

    def test_multiple_inline_graphics_different_containers(self):
        """Test: multiple inline-graphics in different containers"""
        xml = """<article xmlns:xlink="http://www.w3.org/1999/xlink">
          <fig id="f1">
            <label>Figure 1</label>
            <caption><title>Title<inline-graphic xlink:href="img1.jpg"/></title></caption>
          </fig>
          <fig id="f2">
            <label>Figure 2<inline-graphic xlink:href="img2.jpg"/></label>
            <caption><title>Another figure</title></caption>
          </fig>
        </article>"""
        tree = etree.fromstring(xml)
        mods = fix_inline_graphic_in_caption(tree)

        self.assertEqual(len(mods), 2)
        graphics = tree.findall(".//graphic")
        self.assertEqual(len(graphics), 2)
        self.assertIsNone(tree.find(".//inline-graphic"))

    def test_multiple_inline_graphics_same_container_no_modification(self):
        """Test: multiple inline-graphics in SAME container - should NOT modify"""
        xml = """<fig id="f1" xmlns:xlink="http://www.w3.org/1999/xlink">
          <label>Figure 1<inline-graphic xlink:href="img1.jpg"/></label>
          <caption><title>Title<inline-graphic xlink:href="img2.jpg"/></title></caption>
        </fig>"""
        tree = etree.fromstring(xml)
        mods = fix_inline_graphic_in_caption(tree)

        self.assertEqual(len(mods), 0)
        inline_graphics = tree.findall(".//inline-graphic")
        self.assertEqual(len(inline_graphics), 2)
        self.assertIsNone(tree.find(".//graphic"))

    def test_two_inline_graphics_in_caption(self):
        """Test: two inline-graphics inside caption - should NOT modify"""
        xml = """<fig id="f1" xmlns:xlink="http://www.w3.org/1999/xlink">
          <label>Figure 1</label>
          <caption>
            <title>Title<inline-graphic xlink:href="img1.jpg"/></title>
            <p>Text<inline-graphic xlink:href="img2.jpg"/></p>
          </caption>
        </fig>"""
        tree = etree.fromstring(xml)
        mods = fix_inline_graphic_in_caption(tree)

        self.assertEqual(len(mods), 0)
        inline_graphics = tree.findall(".//inline-graphic")
        self.assertEqual(len(inline_graphics), 2)
        self.assertIsNone(tree.find(".//graphic"))

    def test_graphic_already_exists(self):
        """Test: should not modify when graphic already exists"""
        xml = """<fig id="f1" xmlns:xlink="http://www.w3.org/1999/xlink">
          <label>Figure 1</label>
          <caption><title>Title<inline-graphic xlink:href="img1.jpg"/></title></caption>
          <graphic xlink:href="existing.jpg"/>
        </fig>"""
        tree = etree.fromstring(xml)
        mods = fix_inline_graphic_in_caption(tree)

        self.assertEqual(len(mods), 0)
        self.assertIsNotNone(tree.find(".//inline-graphic"))
        graphics = tree.findall(".//graphic")
        self.assertEqual(len(graphics), 1)

    def test_container_with_table_no_modification(self):
        """Test: container with table element should NOT be modified"""
        xml = """<table-wrap id="t1" xmlns:xlink="http://www.w3.org/1999/xlink">
          <label>Table 1</label>
          <caption><title>Title<inline-graphic xlink:href="table1.jpg"/></title></caption>
          <table>
            <tr><td>Data</td></tr>
          </table>
        </table-wrap>"""
        tree = etree.fromstring(xml)
        mods = fix_inline_graphic_in_caption(tree)

        self.assertEqual(len(mods), 0)
        self.assertIsNotNone(tree.find(".//inline-graphic"))
        self.assertIsNone(tree.find(".//graphic"))

    def test_container_with_mathml_no_modification(self):
        """Test: container with mathml element should NOT be modified"""
        xml = """<disp-formula id="eq1" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML">
          <label>(1)</label>
          <caption><title>Equation<inline-graphic xlink:href="eq1.jpg"/></title></caption>
          <mml:math><mml:mi>x</mml:mi></mml:math>
        </disp-formula>"""
        tree = etree.fromstring(xml)
        mods = fix_inline_graphic_in_caption(tree)

        self.assertEqual(len(mods), 0)
        self.assertIsNotNone(tree.find(".//inline-graphic"))
        self.assertIsNone(tree.find(".//graphic"))

    def test_container_with_paragraph_no_modification(self):
        """Test: container with paragraph element should NOT be modified"""
        xml = """<fig id="f1" xmlns:xlink="http://www.w3.org/1999/xlink">
          <label>Figure 1</label>
          <caption><title>Title<inline-graphic xlink:href="img1.jpg"/></title></caption>
          <p>Some description text</p>
        </fig>"""
        tree = etree.fromstring(xml)
        mods = fix_inline_graphic_in_caption(tree)

        self.assertEqual(len(mods), 0)
        self.assertIsNotNone(tree.find(".//inline-graphic"))
        self.assertIsNone(tree.find(".//graphic"))

    def test_table_wrap_context(self):
        """Test: inline-graphic in table-wrap context (no table element)"""
        xml = """<table-wrap id="t1" xmlns:xlink="http://www.w3.org/1999/xlink">
          <label>Table 1</label>
          <caption><title>Title<inline-graphic xlink:href="table1.jpg"/></title></caption>
        </table-wrap>"""
        tree = etree.fromstring(xml)
        mods = fix_inline_graphic_in_caption(tree)

        self.assertEqual(len(mods), 1)
        self.assertEqual(mods[0]["new_parent"], "table-wrap")
        self.assertIsNotNone(tree.find(".//graphic"))
        self.assertIsNone(tree.find(".//inline-graphic"))

    def test_disp_formula_context(self):
        """Test: inline-graphic in disp-formula context (no mathml)"""
        xml = """<disp-formula id="eq1" xmlns:xlink="http://www.w3.org/1999/xlink">
          <label>(1)</label>
          <caption><title>Equation<inline-graphic xlink:href="eq1.jpg"/></title></caption>
        </disp-formula>"""
        tree = etree.fromstring(xml)
        mods = fix_inline_graphic_in_caption(tree)

        self.assertEqual(len(mods), 1)
        self.assertEqual(mods[0]["new_parent"], "disp-formula")
        self.assertIsNotNone(tree.find(".//graphic"))
        self.assertIsNone(tree.find(".//inline-graphic"))

    def test_preserve_attributes(self):
        """Test: preservation of all attributes"""
        xml = """<fig id="f1" xmlns:xlink="http://www.w3.org/1999/xlink">
          <label>Figure 1</label>
          <caption><title>Title<inline-graphic xlink:href="img1.jpg" id="ig1" content-type="image/jpeg"/></title></caption>
        </fig>"""
        tree = etree.fromstring(xml)
        mods = fix_inline_graphic_in_caption(tree)

        graphic = tree.find(".//graphic")
        self.assertIsNotNone(graphic)
        self.assertEqual(graphic.get("{http://www.w3.org/1999/xlink}href"), "img1.jpg")
        self.assertEqual(graphic.get("id"), "ig1")
        self.assertEqual(graphic.get("content-type"), "image/jpeg")

    def test_preserve_child_elements(self):
        """Test: preservation of child elements"""
        xml = """<fig id="f1" xmlns:xlink="http://www.w3.org/1999/xlink">
          <label>Figure 1</label>
          <caption>
            <title>Title
              <inline-graphic xlink:href="img1.jpg">
                <alt-text>Alternative text</alt-text>
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
        self.assertEqual(alt_text.text, "Alternative text")

    def test_inline_graphic_position_after_caption(self):
        """Test: graphic is inserted after label and caption"""
        xml = """<fig id="f1" xmlns:xlink="http://www.w3.org/1999/xlink">
          <label>Figure 1</label>
          <caption><title>Title<inline-graphic xlink:href="img1.jpg"/></title></caption>
        </fig>"""
        tree = etree.fromstring(xml)
        mods = fix_inline_graphic_in_caption(tree)

        children = list(tree)
        self.assertEqual(children[0].tag, "label")
        self.assertEqual(children[1].tag, "caption")
        self.assertEqual(children[2].tag, "graphic")

    def test_position_after_label_only(self):
        """Test: graphic after label when there is no caption"""
        xml = """<fig id="f1" xmlns:xlink="http://www.w3.org/1999/xlink">
          <label>Figure 1<inline-graphic xlink:href="img1.jpg"/></label>
        </fig>"""
        tree = etree.fromstring(xml)
        mods = fix_inline_graphic_in_caption(tree)

        children = list(tree)
        self.assertEqual(children[0].tag, "label")
        self.assertEqual(children[1].tag, "graphic")

    def test_empty_modifications_no_inline_graphics(self):
        """Test: returns empty list when there are no inline-graphics"""
        xml = """<fig id="f1">
          <label>Figure 1</label>
          <caption><title>Title</title></caption>
          <graphic xlink:href="img1.jpg" xmlns:xlink="http://www.w3.org/1999/xlink"/>
        </fig>"""
        tree = etree.fromstring(xml)
        mods = fix_inline_graphic_in_caption(tree)

        self.assertEqual(len(mods), 0)

    def test_inline_graphic_outside_label_caption_ignored(self):
        """Test: inline-graphic outside label/caption is ignored"""
        xml = """<fig id="f1" xmlns:xlink="http://www.w3.org/1999/xlink">
          <label>Figure 1</label>
          <caption><title>Title</title></caption>
          <p><inline-graphic xlink:href="img1.jpg"/></p>
        </fig>"""
        tree = etree.fromstring(xml)
        mods = fix_inline_graphic_in_caption(tree)

        self.assertEqual(len(mods), 0)
        self.assertIsNotNone(tree.find(".//inline-graphic"))

    def test_none_xmltree_raises_error(self):
        """Test: None xmltree should raise ValueError"""
        with self.assertRaises(ValueError) as context:
            fix_inline_graphic_in_caption(None)

        self.assertIn("cannot be None", str(context.exception))

    def test_modification_record_structure(self):
        """Test: verifies modification record structure"""
        xml = """<fig id="f1" xmlns:xlink="http://www.w3.org/1999/xlink">
          <label>Figure 1</label>
          <caption><title>Title<inline-graphic xlink:href="img1.jpg"/></title></caption>
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
        """Test: preserves text and tail of inline-graphic"""
        xml = """<fig xmlns:xlink="http://www.w3.org/1999/xlink">
          <caption><title>Before<inline-graphic xlink:href="img.jpg"/>After</title></caption>
        </fig>"""
        tree = etree.fromstring(xml)

        inline = tree.find(".//inline-graphic")
        original_tail = inline.tail

        fix_inline_graphic_in_caption(tree)

        graphic = tree.find(".//graphic")
        self.assertIsNotNone(graphic)
        self.assertEqual(graphic.tail, original_tail)

    def test_complex_nested_structure(self):
        """Test: complex structure with multiple levels"""
        xml = """<article xmlns:xlink="http://www.w3.org/1999/xlink">
          <body>
            <sec>
              <fig id="f1">
                <label>Fig 1</label>
                <caption>
                  <title>Title</title>
                  <p>Description<inline-graphic xlink:href="img1.jpg"/></p>
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
        """Test: multiple containers with mixed scenarios"""
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

        # f1: should modify (does not have graphic)
        # f2: should not modify (already has graphic)
        # t1: should modify (does not have graphic)
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
        """Test: inline-graphic in non-container element is ignored"""
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

        # XPath does not find these elements because they are not valid containers
        self.assertEqual(len(mods), 0)
        # inline-graphics remain
        self.assertEqual(len(tree.findall(".//inline-graphic")), 2)

    def test_container_only_label_should_modify(self):
        """Test: container with only label should be modified"""
        xml = """<fig id="f1" xmlns:xlink="http://www.w3.org/1999/xlink">
          <label>Figure 1<inline-graphic xlink:href="img1.jpg"/></label>
        </fig>"""
        tree = etree.fromstring(xml)
        mods = fix_inline_graphic_in_caption(tree)

        self.assertEqual(len(mods), 1)
        self.assertIsNotNone(tree.find(".//graphic"))
        self.assertIsNone(tree.find(".//inline-graphic"))

    def test_container_only_caption_should_modify(self):
        """Test: container with only caption should be modified"""
        xml = """<fig id="f1" xmlns:xlink="http://www.w3.org/1999/xlink">
          <caption><title>Title<inline-graphic xlink:href="img1.jpg"/></title></caption>
        </fig>"""
        tree = etree.fromstring(xml)
        mods = fix_inline_graphic_in_caption(tree)

        self.assertEqual(len(mods), 1)
        self.assertIsNotNone(tree.find(".//graphic"))
        self.assertIsNone(tree.find(".//inline-graphic"))


if __name__ == "__main__":
    unittest.main()
