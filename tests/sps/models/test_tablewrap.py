import unittest
from lxml import etree

from packtools.sps.models.tablewrap import TableWrap, ArticleTableWraps


class TableWrapTest(unittest.TestCase):
    def setUp(self):
        xml = (
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'dtd-version="1.0" article-type="research-article" xml:lang="pt">'
            '<body>'
            '<table-wrap id="t2">'
            '<label>Tabela 2:</label>'
            '<caption>'
            '<title>Produção de tecidos de algodão da Fábrica Votorantim, do estado de São Paulo e do restante do Brasil, 1918-1930 - em milhões de metros</title>'
            '</caption>'
            '<alternatives>'
            '<graphic xlink:href="1980-5381-neco-28-02-579-gt02.svg"/>'
            '<table>'
            '<colgroup>'
            '<col/>'
            '<col/>'
            '<col/>'
            '<col/>'
            '<col/>'
            '<col/>'
            '<col/>'
            '<col/>'
            '<col/>'
            '<col/>'
            '</colgroup>'
            '<thead>'
            '<tr>'
            '<th align="left"> </th>'
            '<th align="center">1918</th>'
            '<th align="center">1919</th>'
            '<th align="center">1920</th>'
            '<th align="center">1921</th>'
            '<th align="center">1922</th>'
            '<th align="center">1923</th>'
            '<th align="center">1925</th>'
            '<th align="center">1929</th>'
            '<th align="center">1930</th>'
            '</tr>'
            '</thead>'
            '<tbody>'
            '<tr>'
            '<td align="left">Resto do país</td>'
            '<td align="center">347</td>'
            '<td align="center">409</td>'
            '<td align="center">400</td>'
            '<td align="center">355</td>'
            '<td align="center">410</td>'
            '<td align="center">452</td>'
            '<td align="center">330</td>'
            '<td align="center">329</td>'
            '<td align="center">341</td>'
            '</tr>'
            '<tr>'
            '<td align="left">Estado de São Paulo</td>'
            '<td align="center">147</td>'
            '<td align="center">175</td>'
            '<td align="center">187</td>'
            '<td align="center">198</td>'
            '<td align="center">217</td>'
            '<td align="center">488</td>'
            '<td align="center">206</td>'
            '<td align="center">149</td>'
            '<td align="center">135</td>'
            '</tr>'
            '<tr>'
            '<td align="left">Votorantim</td>'
            '<td align="center">13</td>'
            '<td align="center">11</td>'
            '<td align="center">16</td>'
            '<td align="center">16</td>'
            '<td align="center">21</td>'
            '<td align="center">24</td>'
            '<td align="center">20</td>'
            '<td align="center">16</td>'
            '<td align="center">17</td>'
            '</tr>'
            '</tbody>'
            '</table>'
            '</alternatives>'
            '<table-wrap-foot>'
            '<fn id="TFN3">'
            '<label>*</label>'
            '<p>Fonte: Cano (1981, p. 293); SÃO PAULO. <italic>Diário Oficial do Estado de São Paulo</italic>, '
            '30/06/1922, p. 1922; 15/02/1923, p. 1923; 14/02/1925, p. 1233; 12/02/1926, p. 1243; 22/03/1931 p. '
            '2327.</p>'
            '</fn>'
            '</table-wrap-foot>'
            '</table-wrap>'
            '</body>'
            '</article>'
        )
        self.xmltree = etree.fromstring(xml)
        self.tablewrap_element = self.xmltree.xpath("//table-wrap")[0]
        self.tablewrap_obj = TableWrap(self.tablewrap_element)

    def test_table_wrap_id(self):
        self.assertEqual(self.tablewrap_obj.table_wrap_id, "t2")

    def test_label(self):
        self.assertEqual(self.tablewrap_obj.label, "Tabela 2:")

    def test_caption(self):
        self.assertEqual(
            self.tablewrap_obj.caption,
            "Produção de tecidos de algodão da Fábrica Votorantim, do estado de São Paulo e do restante do Brasil, "
            "1918-1930 - em milhões de metros"
        )

    def test_footnote(self):
        self.assertEqual(
            self.tablewrap_obj.footnote,
            "*Fonte: Cano (1981, p. 293); SÃO PAULO. Diário Oficial do Estado de São Paulo, "
            "30/06/1922, p. 1922; 15/02/1923, p. 1923; 14/02/1925, p. 1233; 12/02/1926, p. 1243; 22/03/1931 p. 2327."
        )

    def test_footnote_id(self):
        self.assertEqual(self.tablewrap_obj.footnote_id, "TFN3")

    def test_footnote_label(self):
        self.assertEqual(self.tablewrap_obj.footnote_label, "*")

    def test_alternative_elements(self):
        self.assertListEqual(self.tablewrap_obj.alternative_elements, ['graphic', 'table'])

    def test_data(self):
        self.maxDiff = None
        expected_data = {
            "alternative_parent": "table-wrap",
            "table_wrap_id": "t2",
            "caption": "Produção de tecidos de algodão da Fábrica Votorantim, do estado de São Paulo e do "
                       "restante do Brasil, 1918-1930 - em milhões de metros",
            "footnote": "*Fonte: Cano (1981, p. 293); SÃO PAULO. Diário Oficial do Estado de São Paulo, "
                        "30/06/1922, p. 1922; 15/02/1923, p. 1923; 14/02/1925, p. 1233; 12/02/1926, p. 1243; 22/03/1931 p. 2327.",
            "label": "Tabela 2:",
            "footnote_id": "TFN3",
            "footnote_label": "*",
            "alternative_elements": ['graphic', 'table']
        }
        self.assertDictEqual(self.tablewrap_obj.data, expected_data)


class ArticleTableWrapsTest(unittest.TestCase):
    def setUp(self):
        xml = (
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'dtd-version="1.0" article-type="research-article" xml:lang="pt">'
            '<body>'
            '<table-wrap id="t2">'
            '<label>Tabela 2:</label>'
            '<caption>'
            '<title>Produção de tecidos de algodão da Fábrica Votorantim, do estado de São Paulo e do restante do Brasil, 1918-1930 - em milhões de metros</title>'
            '</caption>'
            '<alternatives>'
            '<graphic xlink:href="1980-5381-neco-28-02-579-gt02.svg"/>'
            '<table>'
            '<colgroup>'
            '<col/>'
            '<col/>'
            '<col/>'
            '<col/>'
            '<col/>'
            '<col/>'
            '<col/>'
            '<col/>'
            '<col/>'
            '<col/>'
            '</colgroup>'
            '<thead>'
            '<tr>'
            '<th align="left"> </th>'
            '<th align="center">1918</th>'
            '<th align="center">1919</th>'
            '<th align="center">1920</th>'
            '<th align="center">1921</th>'
            '<th align="center">1922</th>'
            '<th align="center">1923</th>'
            '<th align="center">1925</th>'
            '<th align="center">1929</th>'
            '<th align="center">1930</th>'
            '</tr>'
            '</thead>'
            '<tbody>'
            '<tr>'
            '<td align="left">Resto do país</td>'
            '<td align="center">347</td>'
            '<td align="center">409</td>'
            '<td align="center">400</td>'
            '<td align="center">355</td>'
            '<td align="center">410</td>'
            '<td align="center">452</td>'
            '<td align="center">330</td>'
            '<td align="center">329</td>'
            '<td align="center">341</td>'
            '</tr>'
            '<tr>'
            '<td align="left">Estado de São Paulo</td>'
            '<td align="center">147</td>'
            '<td align="center">175</td>'
            '<td align="center">187</td>'
            '<td align="center">198</td>'
            '<td align="center">217</td>'
            '<td align="center">488</td>'
            '<td align="center">206</td>'
            '<td align="center">149</td>'
            '<td align="center">135</td>'
            '</tr>'
            '<tr>'
            '<td align="left">Votorantim</td>'
            '<td align="center">13</td>'
            '<td align="center">11</td>'
            '<td align="center">16</td>'
            '<td align="center">16</td>'
            '<td align="center">21</td>'
            '<td align="center">24</td>'
            '<td align="center">20</td>'
            '<td align="center">16</td>'
            '<td align="center">17</td>'
            '</tr>'
            '</tbody>'
            '</table>'
            '</alternatives>'
            '<table-wrap-foot>'
            '<fn id="TFN3">'
            '<label>*</label>'
            '<p>Fonte: Cano (1981, p. 293); SÃO PAULO. <italic>Diário Oficial do Estado de São Paulo</italic>, '
            '30/06/1922, p. 1922; 15/02/1923, p. 1923; 14/02/1925, p. 1233; 12/02/1926, p. 1243; 22/03/1931 p. '
            '2327.</p>'
            '</fn>'
            '</table-wrap-foot>'
            '</table-wrap>'
            '</body>'
            '</article>'
        )
        self.xml_tree = etree.fromstring(xml)

    def test_items_by_language(self):
        self.maxDiff = None
        obtained = ArticleTableWraps(self.xml_tree).items_by_lang

        expected = {
            "pt": {
                "alternative_parent": "table-wrap",
                "table_wrap_id": "t2",
                "caption": "Produção de tecidos de algodão da Fábrica Votorantim, do estado de São Paulo e do "
                           "restante do Brasil, 1918-1930 - em milhões de metros",
                "footnote": "*Fonte: Cano (1981, p. 293); SÃO PAULO. Diário Oficial do Estado de São Paulo, "
                            "30/06/1922, p. 1922; 15/02/1923, p. 1923; 14/02/1925, p. 1233; 12/02/1926, p. 1243; 22/03/1931 p. 2327.",
                "label": "Tabela 2:",
                "footnote_id": "TFN3",
                "footnote_label": "*",
                "alternative_elements": ['graphic', 'table'],
                "parent": "article",
                "parent_article_type": "research-article",
                "parent_id": None,
                "parent_lang": "pt",
            },
        }

        for lang, item in expected.items():
            with self.subTest(lang):
                self.assertDictEqual(item, obtained[lang])


if __name__ == '__main__':
    unittest.main()
