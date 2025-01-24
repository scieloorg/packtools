import unittest
from lxml import etree
from packtools.sps.models.basenotes import BaseNoteGroup, BaseNoteGroups, Fn


class TestBaseNotes(unittest.TestCase):
    def test_fn_data(self):
        xml = etree.fromstring('''
            <fn id="f1" fn-type="conflict">
                <label>*</label>
                <title>Conflict of Interest</title>
                <bold>Important</bold>
                <p>This is a footnote.</p>
            </fn>
        ''')
        fn = Fn(xml)
        self.assertEqual(fn.data["fn_id"], "f1")
        self.assertEqual(fn.data["fn_type"], "conflict")
        self.assertEqual(fn.data["fn_label"], "*")
        self.assertEqual(fn.data["fn_title"], "Conflict of Interest")
        self.assertEqual(fn.data["fn_bold"], "Important")
        self.assertIn("This is a footnote.", fn.data["fn_text"])

    def test_base_note_group(self):
        xml = etree.fromstring('''
            <fn-group>
                <fn id="f1"><label>1</label></fn>
                <fn id="f2"><label>2</label></fn>
            </fn-group>
        ''')
        note_group = BaseNoteGroup(xml)
        items = list(note_group.items)
        self.assertEqual(len(items), 2)
        self.assertEqual(items[0]["fn_id"], "f1")
        self.assertEqual(items[1]["fn_label"], "2")

    def test_base_note_groups(self):
        xml = etree.fromstring('''
            <article>
                <front>
                    <fn-group>
                        <fn id="f1"><label>1</label></fn>
                    </fn-group>
                </front>
                <back>
                    <fn-group>
                        <fn id="f2"><label>2</label></fn>
                    </fn-group>
                </back>
            </article>
        ''')
        note_groups = BaseNoteGroups(xml, "fn-group", BaseNoteGroup)
        items = list(note_groups.items)
        self.assertEqual(len(items), 2)
        self.assertEqual(items[0]["fn_id"], "f1")
        self.assertEqual(items[1]["fn_id"], "f2")


if __name__ == "__main__":
    unittest.main()
