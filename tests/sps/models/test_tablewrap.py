import unittest
from lxml import etree

from packtools.sps.models.tablewrap import TableWrap, ArticleTableWrappers


class TableWrapTest(unittest.TestCase):
    def setUp(self):
        xml = (
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'dtd-version="1.0" article-type="research-article" xml:lang="pt">'
            "<body>"
            '<table-wrap id="t2">'
            "<label>Tabela 2:</label>"
            "<caption>"
            "<title>Produção de tecidos de algodão da Fábrica Votorantim, do estado de São Paulo e do restante do Brasil, 1918-1930 - em milhões de metros</title>"
            "</caption>"
            "<alternatives>"
            '<graphic xlink:href="1980-5381-neco-28-02-579-gt02.svg"/>'
            "<table>"
            "<thead>"
            "<tr>"
            "<th>Posição</th>"
            "</tr>"
            "</thead>"
            "</table>"
            "</alternatives>"
            "<table-wrap-foot>"
            '<fn id="TFN3">'
            "<label>*</label>"
            "<p>Fonte: Cano (1981, p. 293); SÃO PAULO. <italic>Diário Oficial do Estado de São Paulo</italic>, "
            "30/06/1922, p. 1922; 15/02/1923, p. 1923; 14/02/1925, p. 1233; 12/02/1926, p. 1243; 22/03/1931 p. "
            "2327.</p>"
            "</fn>"
            "</table-wrap-foot>"
            "</table-wrap>"
            "</body>"
            "</article>"
        )
        self.xml_tree = etree.fromstring(xml)
        self.table_wrap_element = self.xml_tree.xpath("//table-wrap")[0]
        self.table_wrap_obj = TableWrap(self.table_wrap_element)

    def test_str_main_tag(self):
        self.assertEqual(self.table_wrap_obj.str_main_tag(), '<table-wrap id="t2">')

    def test_str(self):
        self.maxDiff = None
        self.assertEqual(
            str(self.table_wrap_obj),
            """<table-wrap xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" id="t2"><label>Tabela 2:</label><caption><title>Produção de tecidos de algodão da Fábrica Votorantim, do estado de São Paulo e do restante do Brasil, 1918-1930 - em milhões de metros</title></caption><alternatives><graphic xlink:href="1980-5381-neco-28-02-579-gt02.svg"/><table><thead><tr><th>Posição</th></tr></thead></table></alternatives><table-wrap-foot><fn id="TFN3"><label>*</label><p>Fonte: Cano (1981, p. 293); SÃO PAULO. <italic>Diário Oficial do Estado de São Paulo</italic>, 30/06/1922, p. 1922; 15/02/1923, p. 1923; 14/02/1925, p. 1233; 12/02/1926, p. 1243; 22/03/1931 p. 2327.</p></fn></table-wrap-foot></table-wrap>""",
        )

    def test_xml(self):
        self.maxDiff = None
        self.assertEqual(
            self.table_wrap_obj.xml(),
            """<table-wrap xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" id="t2">
  <label>Tabela 2:</label>
  <caption>
    <title>Produção de tecidos de algodão da Fábrica Votorantim, do estado de São Paulo e do restante do Brasil, 1918-1930 - em milhões de metros</title>
  </caption>
  <alternatives>
    <graphic xlink:href="1980-5381-neco-28-02-579-gt02.svg"/>
    <table>
      <thead>
        <tr>
          <th>Posição</th>
        </tr>
      </thead>
    </table>
  </alternatives>
  <table-wrap-foot>
    <fn id="TFN3">
      <label>*</label>
      <p>Fonte: Cano (1981, p. 293); SÃO PAULO. <italic>Diário Oficial do Estado de São Paulo</italic>, 30/06/1922, p. 1922; 15/02/1923, p. 1923; 14/02/1925, p. 1233; 12/02/1926, p. 1243; 22/03/1931 p. 2327.</p>
    </fn>
  </table-wrap-foot>
</table-wrap>
"""
        )

    def test_table_wrap_id(self):
        self.assertEqual(self.table_wrap_obj.table_wrap_id, "t2")

    def test_label(self):
        self.assertEqual(self.table_wrap_obj.label, "Tabela 2:")

    def test_caption(self):
        self.assertEqual(
            self.table_wrap_obj.caption,
            "Produção de tecidos de algodão da Fábrica Votorantim, do estado de São Paulo e do restante do Brasil, "
            "1918-1930 - em milhões de metros",
        )

    def test_footnote(self):
        self.assertEqual(
            self.tablewrap_obj.footnote,
            "*Fonte: Cano (1981, p. 293); SÃO PAULO. Diário Oficial do Estado de São Paulo, "
            "30/06/1922, p. 1922; 15/02/1923, p. 1923; 14/02/1925, p. 1233; 12/02/1926, p. 1243; 22/03/1931 p. 2327.",
        )

    def test_footnote_id(self):
        self.assertEqual(self.tablewrap_obj.footnote_id, "TFN3")

    def test_footnote_label(self):
        self.assertEqual(self.tablewrap_obj.footnote_label, "*")

    def test_alternative_elements(self):
        self.assertListEqual(
            self.tablewrap_obj.alternative_elements, ["graphic", "table"]
        )

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
            "alternative_elements": ["graphic", "table"],
            "table": "table codification",
            "graphic": "1980-5381-neco-28-02-579-gt02.svg",
        }
        self.assertDictEqual(self.tablewrap_obj.data, expected_data)


class ArticleTableWrappersTest(unittest.TestCase):
    def setUp(self):
        xml = (
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" dtd-version="1.0" article-type="research-article" xml:lang="pt">'
            "<body>"
            '<table-wrap id="t2">'
            "<label>Tabela 2:</label>"
            "<caption>"
            "<title>Produção de tecidos de algodão da Fábrica Votorantim, do estado de São Paulo e do restante do Brasil, 1918-1930 - em milhões de metros</title>"
            "</caption>"
            "<alternatives>"
            '<graphic xlink:href="1980-5381-neco-28-02-579-gt02.svg"/>'
            "<table>"
            "table codification"
            "</table>"
            "</alternatives>"
            "<table-wrap-foot>"
            '<fn id="TFN3">'
            "<label>*</label>"
            "<p>Fonte: Cano (1981, p. 293); SÃO PAULO. <italic>Diário Oficial do Estado de São Paulo</italic>, 30/06/1922, p. 1922; 15/02/1923, p. 1923; 14/02/1925, p. 1233; 12/02/1926, p. 1243; 22/03/1931 p. 2327.</p>"
            "</fn>"
            "</table-wrap-foot>"
            "</table-wrap>"
            '<table-wrap id="t3">'
            "<label>Tabela 3:</label>"
            "<caption>"
            "<title>Produção de tecidos de algodão da Fábrica XYZ, do estado de Minas Gerais e do restante do Brasil, 1931-1940 - em milhões de metros</title>"
            "</caption>"
            "<alternatives>"
            '<graphic xlink:href="1980-5381-neco-28-02-579-gt03.svg"/>'
            "<table>"
            "table codification"
            "</table>"
            "</alternatives>"
            "<table-wrap-foot>"
            '<fn id="TFN4">'
            "<label>*</label>"
            "<p>Fonte: Autor (2023, p. 123); MINAS GERAIS. <italic>Diário Oficial do Estado de Minas Gerais</italic>, 10/01/1932, p. 1932; 20/03/1933, p. 1933; 25/05/1934, p. 1333; 30/06/1935, p. 1343; 15/07/1936 p. 1437.</p>"
            "</fn>"
            "</table-wrap-foot>"
            "</table-wrap>"
            "</body>"
            '<sub-article article-type="translation" xml:lang="en">'
            "<body>"
            '<table-wrap id="t4">'
            "<label>Table 4:</label>"
            "<caption>"
            "<title>Production of cotton fabrics by XYZ Factory, state of Minas Gerais and the rest of Brazil, 1941-1950 - in millions of meters</title>"
            "</caption>"
            "<alternatives>"
            '<graphic xlink:href="1980-5381-neco-28-02-579-gt04.svg"/>'
            "<table>"
            "table codification"
            "</table>"
            "</alternatives>"
            "<table-wrap-foot>"
            '<fn id="TFN5">'
            "<label>*</label>"
            "<p>Source: Author (2023, p. 123); MINAS GERAIS. <italic>Official Journal of the State of Minas Gerais</italic>, 10/01/1942, p. 1942; 20/03/1943, p. 1943; 25/05/1944, p. 1433; 30/06/1945, p. 1443; 15/07/1946 p. 1537.</p>"
            "</fn>"
            "</table-wrap-foot>"
            "</table-wrap>"
            '<table-wrap id="t5">'
            "<label>Table 5:</label>"
            "<caption>"
            "<title>Production of cotton fabrics by ABC Factory, state of Rio de Janeiro and the rest of Brazil, 1951-1960 - in millions of meters</title>"
            "</caption>"
            "<alternatives>"
            '<graphic xlink:href="1980-5381-neco-28-02-579-gt05.svg"/>'
            "<table>"
            "table codification"
            "</table>"
            "</alternatives>"
            "<table-wrap-foot>"
            '<fn id="TFN6">'
            "<label>*</label>"
            "<p>Source: Author (2023, p. 123); RIO DE JANEIRO. <italic>Official Journal of the State of Rio de Janeiro</italic>, 10/01/1952, p. 1952; 20/03/1953, p. 1953; 25/05/1954, p. 1533; 30/06/1955, p. 1543; 15/07/1956 p. 1637.</p>"
            "</fn>"
            "</table-wrap-foot>"
            "</table-wrap>"
            "</body>"
            "</sub-article>"
            "</article>"
        )
        self.xml_tree = etree.fromstring(xml)

    def test_get_article_table_wrappers(self):
        self.maxDiff = None
        obtained = list(ArticleTableWrappers(self.xml_tree).get_article_table_wrappers)

        expected = [
            {
                "alternative_parent": "table-wrap",
                "table_wrap_id": "t2",
                "caption": "Produção de tecidos de algodão da Fábrica Votorantim, do estado de São Paulo e do "
                "restante do Brasil, 1918-1930 - em milhões de metros",
                "footnote": "*Fonte: Cano (1981, p. 293); SÃO PAULO. Diário Oficial do Estado de São Paulo, "
                "30/06/1922, p. 1922; 15/02/1923, p. 1923; 14/02/1925, p. 1233; 12/02/1926, p. 1243; 22/03/1931 p. 2327.",
                "label": "Tabela 2:",
                "footnote_id": "TFN3",
                "footnote_label": "*",
                "alternative_elements": ["graphic", "table"],
                "parent": "article",
                "parent_article_type": "research-article",
                "parent_id": None,
                "parent_lang": "pt",
                "table": "table codification",
                "graphic": "1980-5381-neco-28-02-579-gt02.svg",
            },
            {
                "alternative_elements": ["graphic", "table"],
                "alternative_parent": "table-wrap",
                "caption": "Produção de tecidos de algodão da Fábrica XYZ, do estado de Minas "
                "Gerais e do restante do Brasil, 1931-1940 - em milhões de metros",
                "footnote": "*Fonte: Autor (2023, p. 123); MINAS GERAIS. Diário Oficial do "
                "Estado de Minas Gerais, 10/01/1932, p. 1932; 20/03/1933, p. "
                "1933; 25/05/1934, p. 1333; 30/06/1935, p. 1343; 15/07/1936 p. "
                "1437.",
                "footnote_id": "TFN4",
                "footnote_label": "*",
                "label": "Tabela 3:",
                "parent": "article",
                "parent_article_type": "research-article",
                "parent_id": None,
                "parent_lang": "pt",
                "table_wrap_id": "t3",
                "table": "table codification",
                "graphic": "1980-5381-neco-28-02-579-gt03.svg",
            },
        ]

        self.assertEqual(len(obtained), 2)
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(item, obtained[i])

    def test_get_sub_article_translation_table_wrappers(self):
        self.maxDiff = None
        obtained = list(
            ArticleTableWrappers(
                self.xml_tree
            ).get_sub_article_translation_table_wrappers
        )

        expected = [
            {
                "alternative_elements": ["graphic", "table"],
                "alternative_parent": "table-wrap",
                "caption": "Production of cotton fabrics by XYZ Factory, state of Minas "
                "Gerais and the rest of Brazil, 1941-1950 - in millions of meters",
                "footnote": "*Source: Author (2023, p. 123); MINAS GERAIS. Official Journal "
                "of the State of Minas Gerais, 10/01/1942, p. 1942; 20/03/1943, "
                "p. 1943; 25/05/1944, p. 1433; 30/06/1945, p. 1443; 15/07/1946 p. "
                "1537.",
                "footnote_id": "TFN5",
                "footnote_label": "*",
                "label": "Table 4:",
                "parent": "sub-article",
                "parent_article_type": "translation",
                "parent_id": None,
                "parent_lang": "en",
                "table_wrap_id": "t4",
                "table": "table codification",
                "graphic": "1980-5381-neco-28-02-579-gt04.svg",
            },
            {
                "alternative_elements": ["graphic", "table"],
                "alternative_parent": "table-wrap",
                "caption": "Production of cotton fabrics by ABC Factory, state of Rio de "
                "Janeiro and the rest of Brazil, 1951-1960 - in millions of meters",
                "footnote": "*Source: Author (2023, p. 123); RIO DE JANEIRO. Official "
                "Journal of the State of Rio de Janeiro, 10/01/1952, p. 1952; "
                "20/03/1953, p. 1953; 25/05/1954, p. 1533; 30/06/1955, p. 1543; "
                "15/07/1956 p. 1637.",
                "footnote_id": "TFN6",
                "footnote_label": "*",
                "label": "Table 5:",
                "parent": "sub-article",
                "parent_article_type": "translation",
                "parent_id": None,
                "parent_lang": "en",
                "table_wrap_id": "t5",
                "table": "table codification",
                "graphic": "1980-5381-neco-28-02-579-gt05.svg",
            },
        ]

        self.assertEqual(len(obtained), 2)
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(item, obtained[i])

    def test_get_sub_article_non_translation_table_wrappers(self):
        self.maxDiff = None
        obtained = list(
            ArticleTableWrappers(
                self.xml_tree
            ).get_sub_article_non_translation_table_wrappers
        )

        self.assertEqual(len(obtained), 0)

    def test_get_all_table_wrappers(self):
        self.maxDiff = None
        obtained = list(ArticleTableWrappers(self.xml_tree).get_all_table_wrappers)

        expected = [
            {
                "alternative_parent": "table-wrap",
                "table_wrap_id": "t2",
                "caption": "Produção de tecidos de algodão da Fábrica Votorantim, do estado de São Paulo e do "
                "restante do Brasil, 1918-1930 - em milhões de metros",
                "footnote": "*Fonte: Cano (1981, p. 293); SÃO PAULO. Diário Oficial do Estado de São Paulo, "
                "30/06/1922, p. 1922; 15/02/1923, p. 1923; 14/02/1925, p. 1233; 12/02/1926, p. 1243; 22/03/1931 p. 2327.",
                "label": "Tabela 2:",
                "footnote_id": "TFN3",
                "footnote_label": "*",
                "alternative_elements": ["graphic", "table"],
                "parent": "article",
                "parent_article_type": "research-article",
                "parent_id": None,
                "parent_lang": "pt",
                "table": "table codification",
                "graphic": "1980-5381-neco-28-02-579-gt02.svg",
            },
            {
                "alternative_elements": ["graphic", "table"],
                "alternative_parent": "table-wrap",
                "caption": "Produção de tecidos de algodão da Fábrica XYZ, do estado de Minas "
                "Gerais e do restante do Brasil, 1931-1940 - em milhões de metros",
                "footnote": "*Fonte: Autor (2023, p. 123); MINAS GERAIS. Diário Oficial do "
                "Estado de Minas Gerais, 10/01/1932, p. 1932; 20/03/1933, p. "
                "1933; 25/05/1934, p. 1333; 30/06/1935, p. 1343; 15/07/1936 p. "
                "1437.",
                "footnote_id": "TFN4",
                "footnote_label": "*",
                "label": "Tabela 3:",
                "parent": "article",
                "parent_article_type": "research-article",
                "parent_id": None,
                "parent_lang": "pt",
                "table_wrap_id": "t3",
                "table": "table codification",
                "graphic": "1980-5381-neco-28-02-579-gt03.svg",
            },
            {
                "alternative_elements": ["graphic", "table"],
                "alternative_parent": "table-wrap",
                "caption": "Production of cotton fabrics by XYZ Factory, state of Minas "
                "Gerais and the rest of Brazil, 1941-1950 - in millions of meters",
                "footnote": "*Source: Author (2023, p. 123); MINAS GERAIS. Official Journal "
                "of the State of Minas Gerais, 10/01/1942, p. 1942; 20/03/1943, "
                "p. 1943; 25/05/1944, p. 1433; 30/06/1945, p. 1443; 15/07/1946 p. "
                "1537.",
                "footnote_id": "TFN5",
                "footnote_label": "*",
                "label": "Table 4:",
                "parent": "sub-article",
                "parent_article_type": "translation",
                "parent_id": None,
                "parent_lang": "en",
                "table_wrap_id": "t4",
                "table": "table codification",
                "graphic": "1980-5381-neco-28-02-579-gt04.svg",
            },
            {
                "alternative_elements": ["graphic", "table"],
                "alternative_parent": "table-wrap",
                "caption": "Production of cotton fabrics by ABC Factory, state of Rio de "
                "Janeiro and the rest of Brazil, 1951-1960 - in millions of meters",
                "footnote": "*Source: Author (2023, p. 123); RIO DE JANEIRO. Official "
                "Journal of the State of Rio de Janeiro, 10/01/1952, p. 1952; "
                "20/03/1953, p. 1953; 25/05/1954, p. 1533; 30/06/1955, p. 1543; "
                "15/07/1956 p. 1637.",
                "footnote_id": "TFN6",
                "footnote_label": "*",
                "label": "Table 5:",
                "parent": "sub-article",
                "parent_article_type": "translation",
                "parent_id": None,
                "parent_lang": "en",
                "table_wrap_id": "t5",
                "table": "table codification",
                "graphic": "1980-5381-neco-28-02-579-gt05.svg",
            },
        ]

        self.assertEqual(len(obtained), 4)
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(item, obtained[i])


if __name__ == "__main__":
    unittest.main()
