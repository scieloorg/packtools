import unittest
from lxml import etree

from packtools.sps.models.tablewrap import TableWrap, ArticleTableWrappers


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


class ArticleTableWrappersTest(unittest.TestCase):
    def setUp(self):
        xml = (
            """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" dtd-version="1.0" article-type="research-article" xml:lang="pt">
                <body>
                    <table-wrap id="t2">
                        <label>Tabela 2:</label>
                        <caption>
                            <title>Produção de tecidos de algodão da Fábrica Votorantim, do estado de São Paulo e do restante do Brasil, 1918-1930 - em milhões de metros</title>
                        </caption>
                        <alternatives>
                            <graphic xlink:href="1980-5381-neco-28-02-579-gt02.svg"/>
                            <table>
                                <colgroup>
                                    <col/>
                                    <col/>
                                    <col/>
                                    <col/>
                                    <col/>
                                    <col/>
                                    <col/>
                                    <col/>
                                    <col/>
                                    <col/>
                                </colgroup>
                                <thead>
                                    <tr>
                                        <th align="left"> </th>
                                        <th align="center">1918</th>
                                        <th align="center">1919</th>
                                        <th align="center">1920</th>
                                        <th align="center">1921</th>
                                        <th align="center">1922</th>
                                        <th align="center">1923</th>
                                        <th align="center">1925</th>
                                        <th align="center">1929</th>
                                        <th align="center">1930</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr>
                                        <td align="left">Resto do país</td>
                                        <td align="center">347</td>
                                        <td align="center">409</td>
                                        <td align="center">400</td>
                                        <td align="center">355</td>
                                        <td align="center">410</td>
                                        <td align="center">452</td>
                                        <td align="center">330</td>
                                        <td align="center">329</td>
                                        <td align="center">341</td>
                                    </tr>
                                    <tr>
                                        <td align="left">Estado de São Paulo</td>
                                        <td align="center">147</td>
                                        <td align="center">175</td>
                                        <td align="center">187</td>
                                        <td align="center">198</td>
                                        <td align="center">217</td>
                                        <td align="center">488</td>
                                        <td align="center">206</td>
                                        <td align="center">149</td>
                                        <td align="center">135</td>
                                    </tr>
                                    <tr>
                                        <td align="left">Votorantim</td>
                                        <td align="center">13</td>
                                        <td align="center">11</td>
                                        <td align="center">16</td>
                                        <td align="center">16</td>
                                        <td align="center">21</td>
                                        <td align="center">24</td>
                                        <td align="center">20</td>
                                        <td align="center">16</td>
                                        <td align="center">17</td>
                                    </tr>
                                </tbody>
                            </table>
                        </alternatives>
                        <table-wrap-foot>
                            <fn id="TFN3">
                                <label>*</label>
                                <p>Fonte: Cano (1981, p. 293); SÃO PAULO. <italic>Diário Oficial do Estado de São Paulo</italic>, 30/06/1922, p. 1922; 15/02/1923, p. 1923; 14/02/1925, p. 1233; 12/02/1926, p. 1243; 22/03/1931 p. 2327.</p>
                            </fn>
                        </table-wrap-foot>
                    </table-wrap>
            
                    <table-wrap id="t3">
                        <label>Tabela 3:</label>
                        <caption>
                            <title>Produção de tecidos de algodão da Fábrica XYZ, do estado de Minas Gerais e do restante do Brasil, 1931-1940 - em milhões de metros</title>
                        </caption>
                        <alternatives>
                            <graphic xlink:href="1980-5381-neco-28-02-579-gt03.svg"/>
                            <table>
                                <colgroup>
                                    <col/>
                                    <col/>
                                    <col/>
                                    <col/>
                                    <col/>
                                    <col/>
                                    <col/>
                                    <col/>
                                    <col/>
                                    <col/>
                                </colgroup>
                                <thead>
                                    <tr>
                                        <th align="left"> </th>
                                        <th align="center">1931</th>
                                        <th align="center">1932</th>
                                        <th align="center">1933</th>
                                        <th align="center">1934</th>
                                        <th align="center">1935</th>
                                        <th align="center">1936</th>
                                        <th align="center">1937</th>
                                        <th align="center">1938</th>
                                        <th align="center">1939</th>
                                        <th align="center">1940</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr>
                                        <td align="left">Resto do país</td>
                                        <td align="center">357</td>
                                        <td align="center">419</td>
                                        <td align="center">410</td>
                                        <td align="center">365</td>
                                        <td align="center">420</td>
                                        <td align="center">462</td>
                                        <td align="center">340</td>
                                        <td align="center">339</td>
                                        <td align="center">351</td>
                                    </tr>
                                    <tr>
                                        <td align="left">Estado de Minas Gerais</td>
                                        <td align="center">157</td>
                                        <td align="center">185</td>
                                        <td align="center">197</td>
                                        <td align="center">208</td>
                                        <td align="center">227</td>
                                        <td align="center">498</td>
                                        <td align="center">216</td>
                                        <td align="center">159</td>
                                        <td align="center">145</td>
                                    </tr>
                                    <tr>
                                        <td align="left">XYZ</td>
                                        <td align="center">23</td>
                                        <td align="center">21</td>
                                        <td align="center">26</td>
                                        <td align="center">26</td>
                                        <td align="center">31</td>
                                        <td align="center">34</td>
                                        <td align="center">30</td>
                                        <td align="center">26</td>
                                        <td align="center">27</td>
                                    </tr>
                                </tbody>
                            </table>
                        </alternatives>
                        <table-wrap-foot>
                            <fn id="TFN4">
                                <label>*</label>
                                <p>Fonte: Autor (2023, p. 123); MINAS GERAIS. <italic>Diário Oficial do Estado de Minas Gerais</italic>, 10/01/1932, p. 1932; 20/03/1933, p. 1933; 25/05/1934, p. 1333; 30/06/1935, p. 1343; 15/07/1936 p. 1437.</p>
                            </fn>
                        </table-wrap-foot>
                    </table-wrap>
                </body>
            
                <sub-article article-type="translation" xml:lang="en">
                    <body>
                        <table-wrap id="t4">
                            <label>Table 4:</label>
                            <caption>
                                <title>Production of cotton fabrics by XYZ Factory, state of Minas Gerais and the rest of Brazil, 1941-1950 - in millions of meters</title>
                            </caption>
                            <alternatives>
                                <graphic xlink:href="1980-5381-neco-28-02-579-gt04.svg"/>
                                <table>
                                    <colgroup>
                                        <col/>
                                        <col/>
                                        <col/>
                                        <col/>
                                        <col/>
                                        <col/>
                                        <col/>
                                        <col/>
                                        <col/>
                                        <col/>
                                    </colgroup>
                                    <thead>
                                        <tr>
                                            <th align="left"> </th>
                                            <th align="center">1941</th>
                                            <th align="center">1942</th>
                                            <th align="center">1943</th>
                                            <th align="center">1944</th>
                                            <th align="center">1945</th>
                                            <th align="center">1946</th>
                                            <th align="center">1947</th>
                                            <th align="center">1948</th>
                                            <th align="center">1949</th>
                                            <th align="center">1950</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <tr>
                                            <td align="left">Rest of the country</td>
                                            <td align="center">367</td>
                                            <td align="center">429</td>
                                            <td align="center">420</td>
                                            <td align="center">375</td>
                                            <td align="center">430</td>
                                            <td align="center">472</td>
                                            <td align="center">350</td>
                                            <td align="center">349</td>
                                            <td align="center">361</td>
                                        </tr>
                                        <tr>
                                            <td align="left">State of Minas Gerais</td>
                                            <td align="center">167</td>
                                            <td align="center">195</td>
                                            <td align="center">207</td>
                                            <td align="center">218</td>
                                            <td align="center">237</td>
                                            <td align="center">508</td>
                                            <td align="center">226</td>
                                            <td align="center">169</td>
                                            <td align="center">155</td>
                                        </tr>
                                        <tr>
                                            <td align="left">XYZ</td>
                                            <td align="center">33</td>
                                            <td align="center">31</td>
                                            <td align="center">36</td>
                                            <td align="center">36</td>
                                            <td align="center">41</td>
                                            <td align="center">44</td>
                                            <td align="center">40</td>
                                            <td align="center">36</td>
                                            <td align="center">37</td>
                                        </tr>
                                    </tbody>
                                </table>
                            </alternatives>
                            <table-wrap-foot>
                                <fn id="TFN5">
                                    <label>*</label>
                                    <p>Source: Author (2023, p. 123); MINAS GERAIS. <italic>Official Journal of the State of Minas Gerais</italic>, 10/01/1942, p. 1942; 20/03/1943, p. 1943; 25/05/1944, p. 1433; 30/06/1945, p. 1443; 15/07/1946 p. 1537.</p>
                                </fn>
                            </table-wrap-foot>
                        </table-wrap>
            
                        <table-wrap id="t5">
                            <label>Table 5:</label>
                            <caption>
                                <title>Production of cotton fabrics by ABC Factory, state of Rio de Janeiro and the rest of Brazil, 1951-1960 - in millions of meters</title>
                            </caption>
                            <alternatives>
                                <graphic xlink:href="1980-5381-neco-28-02-579-gt05.svg"/>
                                <table>
                                    <colgroup>
                                        <col/>
                                        <col/>
                                        <col/>
                                        <col/>
                                        <col/>
                                        <col/>
                                        <col/>
                                        <col/>
                                        <col/>
                                        <col/>
                                    </colgroup>
                                    <thead>
                                        <tr>
                                            <th align="left"> </th>
                                            <th align="center">1951</th>
                                            <th align="center">1952</th>
                                            <th align="center">1953</th>
                                            <th align="center">1954</th>
                                            <th align="center">1955</th>
                                            <th align="center">1956</th>
                                            <th align="center">1957</th>
                                            <th align="center">1958</th>
                                            <th align="center">1959</th>
                                            <th align="center">1960</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <tr>
                                            <td align="left">Rest of the country</td>
                                            <td align="center">377</td>
                                            <td align="center">439</td>
                                            <td align="center">430</td>
                                            <td align="center">385</td>
                                            <td align="center">440</td>
                                            <td align="center">482</td>
                                            <td align="center">360</td>
                                            <td align="center">359</td>
                                            <td align="center">371</td>
                                        </tr>
                                        <tr>
                                            <td align="left">State of Rio de Janeiro</td>
                                            <td align="center">177</td>
                                            <td align="center">205</td>
                                            <td align="center">217</td>
                                            <td align="center">228</td>
                                            <td align="center">247</td>
                                            <td align="center">518</td>
                                            <td align="center">236</td>
                                            <td align="center">179</td>
                                            <td align="center">165</td>
                                        </tr>
                                        <tr>
                                            <td align="left">ABC</td>
                                            <td align="center">43</td>
                                            <td align="center">41</td>
                                            <td align="center">46</td>
                                            <td align="center">46</td>
                                            <td align="center">51</td>
                                            <td align="center">54</td>
                                            <td align="center">50</td>
                                            <td align="center">46</td>
                                            <td align="center">47</td>
                                        </tr>
                                    </tbody>
                                </table>
                            </alternatives>
                            <table-wrap-foot>
                                <fn id="TFN6">
                                    <label>*</label>
                                    <p>Source: Author (2023, p. 123); RIO DE JANEIRO. <italic>Official Journal of the State of Rio de Janeiro</italic>, 10/01/1952, p. 1952; 20/03/1953, p. 1953; 25/05/1954, p. 1533; 30/06/1955, p. 1543; 15/07/1956 p. 1637.</p>
                                </fn>
                            </table-wrap-foot>
                        </table-wrap>
                    </body>
                </sub-article>
            </article>

            """
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
                    "footnote": "* Fonte: Cano (1981, p. 293); SÃO PAULO. Diário Oficial do Estado de São Paulo, "
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
                {
                    'alternative_elements': ['graphic', 'table'],
                    'alternative_parent': 'table-wrap',
                    'caption': 'Produção de tecidos de algodão da Fábrica XYZ, do estado de Minas '
                               'Gerais e do restante do Brasil, 1931-1940 - em milhões de metros',
                    'footnote': '* Fonte: Autor (2023, p. 123); MINAS GERAIS. Diário Oficial do '
                                'Estado de Minas Gerais, 10/01/1932, p. 1932; 20/03/1933, p. '
                                '1933; 25/05/1934, p. 1333; 30/06/1935, p. 1343; 15/07/1936 p. '
                                '1437.',
                    'footnote_id': 'TFN4',
                    'footnote_label': '*',
                    'label': 'Tabela 3:',
                    'parent': 'article',
                    'parent_article_type': 'research-article',
                    'parent_id': None,
                    'parent_lang': 'pt',
                    'table_wrap_id': 't3'
                }
        ]

        self.assertEqual(len(obtained), 2)
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(item, obtained[i])

    def test_get_sub_article_translation_table_wrappers(self):
        self.maxDiff = None
        obtained = list(ArticleTableWrappers(self.xml_tree).get_sub_article_translation_table_wrappers)

        expected = [
                {
                    'alternative_elements': ['graphic', 'table'],
                    'alternative_parent': 'table-wrap',
                    'caption': 'Production of cotton fabrics by XYZ Factory, state of Minas '
                               'Gerais and the rest of Brazil, 1941-1950 - in millions of meters',
                    'footnote': '* Source: Author (2023, p. 123); MINAS GERAIS. Official Journal '
                                'of the State of Minas Gerais, 10/01/1942, p. 1942; 20/03/1943, '
                                'p. 1943; 25/05/1944, p. 1433; 30/06/1945, p. 1443; 15/07/1946 p. '
                                '1537.',
                    'footnote_id': 'TFN5',
                    'footnote_label': '*',
                    'label': 'Table 4:',
                    'parent': 'sub-article',
                    'parent_article_type': 'translation',
                    'parent_id': None,
                    'parent_lang': 'en',
                    'table_wrap_id': 't4'
                },
                {
                    'alternative_elements': ['graphic', 'table'],
                     'alternative_parent': 'table-wrap',
                     'caption': 'Production of cotton fabrics by ABC Factory, state of Rio de '
                                'Janeiro and the rest of Brazil, 1951-1960 - in millions of meters',
                     'footnote': '* Source: Author (2023, p. 123); RIO DE JANEIRO. Official '
                                    'Journal of the State of Rio de Janeiro, 10/01/1952, p. 1952; '
                                    '20/03/1953, p. 1953; 25/05/1954, p. 1533; 30/06/1955, p. 1543; '
                                    '15/07/1956 p. 1637.',
                     'footnote_id': 'TFN6',
                     'footnote_label': '*',
                     'label': 'Table 5:',
                     'parent': 'sub-article',
                     'parent_article_type': 'translation',
                     'parent_id': None,
                     'parent_lang': 'en',
                     'table_wrap_id': 't5'
                }
        ]

        self.assertEqual(len(obtained), 2)
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(item, obtained[i])

    def test_get_sub_article_non_translation_table_wrappers(self):
        self.maxDiff = None
        obtained = list(ArticleTableWrappers(self.xml_tree).get_sub_article_non_translation_table_wrappers)

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
                "footnote": "* Fonte: Cano (1981, p. 293); SÃO PAULO. Diário Oficial do Estado de São Paulo, "
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
            {
                'alternative_elements': ['graphic', 'table'],
                'alternative_parent': 'table-wrap',
                'caption': 'Produção de tecidos de algodão da Fábrica XYZ, do estado de Minas '
                           'Gerais e do restante do Brasil, 1931-1940 - em milhões de metros',
                'footnote': '* Fonte: Autor (2023, p. 123); MINAS GERAIS. Diário Oficial do '
                            'Estado de Minas Gerais, 10/01/1932, p. 1932; 20/03/1933, p. '
                            '1933; 25/05/1934, p. 1333; 30/06/1935, p. 1343; 15/07/1936 p. '
                            '1437.',
                'footnote_id': 'TFN4',
                'footnote_label': '*',
                'label': 'Tabela 3:',
                'parent': 'article',
                'parent_article_type': 'research-article',
                'parent_id': None,
                'parent_lang': 'pt',
                'table_wrap_id': 't3'
            },
            {
                'alternative_elements': ['graphic', 'table'],
                'alternative_parent': 'table-wrap',
                'caption': 'Production of cotton fabrics by XYZ Factory, state of Minas '
                           'Gerais and the rest of Brazil, 1941-1950 - in millions of meters',
                'footnote': '* Source: Author (2023, p. 123); MINAS GERAIS. Official Journal '
                            'of the State of Minas Gerais, 10/01/1942, p. 1942; 20/03/1943, '
                            'p. 1943; 25/05/1944, p. 1433; 30/06/1945, p. 1443; 15/07/1946 p. '
                            '1537.',
                'footnote_id': 'TFN5',
                'footnote_label': '*',
                'label': 'Table 4:',
                'parent': 'sub-article',
                'parent_article_type': 'translation',
                'parent_id': None,
                'parent_lang': 'en',
                'table_wrap_id': 't4'
            },
            {
                'alternative_elements': ['graphic', 'table'],
                'alternative_parent': 'table-wrap',
                'caption': 'Production of cotton fabrics by ABC Factory, state of Rio de '
                           'Janeiro and the rest of Brazil, 1951-1960 - in millions of meters',
                'footnote': '* Source: Author (2023, p. 123); RIO DE JANEIRO. Official '
                            'Journal of the State of Rio de Janeiro, 10/01/1952, p. 1952; '
                            '20/03/1953, p. 1953; 25/05/1954, p. 1533; 30/06/1955, p. 1543; '
                            '15/07/1956 p. 1637.',
                'footnote_id': 'TFN6',
                'footnote_label': '*',
                'label': 'Table 5:',
                'parent': 'sub-article',
                'parent_article_type': 'translation',
                'parent_id': None,
                'parent_lang': 'en',
                'table_wrap_id': 't5'
            }
        ]

        self.assertEqual(len(obtained), 4)
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(item, obtained[i])


if __name__ == '__main__':
    unittest.main()
