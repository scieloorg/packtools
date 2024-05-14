from unittest import TestCase

from lxml import etree

from packtools.sps.models.footnotes import Footnote, ArticleFootnotes
from packtools.sps.utils import xml_utils


class FootnoteTest(TestCase):
    def setUp(self):
        xml = (
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'dtd-version="1.0" article-type="research-article" xml:lang="pt">'
            '<front>'
            '<article-meta>'
            '<author-notes>'
            '<corresp>'
            '<label>Correspondência</label>:  Roseana Mara Aredes Priuli  Av. Juscelino Kubistcheck de Oliveira, 1220, '
            'Jardim Panorama, Condomínio Recanto Real Rua 4, 440  15021-450 São José do Rio Preto, SP, Brasil  E-mail: '
            '<email>roseanap@gmail.com</email>'
            '</corresp>'
            '<fn id="fn_01" fn-type="conflict">'
            '<p>Os autores declaram não haver conflito de interesses.</p>'
            '</fn>'
            '</author-notes>'
            '</article-meta>'
            '</front>'
            '</article>'
        )
        xmltree = etree.fromstring(xml)
        self.fn = Footnote(xmltree.xpath(".//fn")[0])

    def test_fn_id(self):
        self.assertEqual(self.fn.fn_id, "fn_01")

    def test_fn_type(self):
        self.assertEqual(self.fn.fn_type, "conflict")

    def test_fn_parent(self):
        self.assertEqual(self.fn.fn_parent, "author-notes")

    def test_data(self):
        expected = {
            "fn_id": "fn_01",
            "fn_type": "conflict",
            "fn_parent": "author-notes"
        }
        self.assertDictEqual(self.fn.data, expected)


class FootnotesTest(TestCase):
    def test_footnotes(self):
        self.maxDiff = None
        xmltree = xml_utils.get_xml_tree('tests/samples/0034-8910-rsp-48-2-0225.xml')

        expected = [
            {
                'fn_id': None,
                'fn_type': 'conflict',
                'fn_parent': 'author-notes',
                'parent': 'article',
                'parent_id': None
            },
            {
                'fn_id': 'fn1',
                'fn_type': None,
                'fn_parent': 'fn-group',
                'parent': 'article',
                'parent_id': None
            },
            {
                'fn_id': 'fn2',
                'fn_type': None,
                'fn_parent': 'fn-group',
                'parent': 'article',
                'parent_id': None
            },
            {
                'fn_id': 'fn3',
                'fn_type': None,
                'fn_parent': 'fn-group',
                'parent': 'article',
                'parent_id': None
            },
            {
                'fn_id': 'fn4',
                'fn_type': 'financial-disclosure',
                'fn_parent': 'fn-group',
                'parent': 'article',
                'parent_id': None
            },
            {
                'fn_id': None,
                'fn_type': 'conflict',
                'fn_parent': 'author-notes',
                'parent': 'sub-article',
                'parent_id': 'TRen'
            },
            {
                'fn_id': 'fn1_en',
                'fn_type': None,
                'fn_parent': 'fn-group',
                'parent': 'sub-article',
                'parent_id': 'TRen'
            },
            {
                'fn_id': 'fn2_en',
                'fn_type': None,
                'fn_parent': 'fn-group',
                'parent': 'sub-article',
                'parent_id': 'TRen'
            },
            {
                'fn_id': 'fn3_en',
                'fn_type': None,
                'fn_parent': 'fn-group',
                'parent': 'sub-article',
                'parent_id': 'TRen'
            },
            {
                'fn_id': 'fn4_en',
                'fn_type': 'financial-disclosure',
                'fn_parent': 'fn-group',
                'parent': 'sub-article',
                'parent_id': 'TRen'
            }
        ]

        obtained = list(ArticleFootnotes(xmltree).article_footnotes)

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(item, obtained[i])
