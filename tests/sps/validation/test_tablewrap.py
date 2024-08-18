import unittest
from lxml import etree
from packtools.sps.utils import xml_utils

from packtools.sps.validation.tablewrap import TableWrapValidation


class TableWrapValidationTest(unittest.TestCase):
    def test_tablewrap_validation_no_tablewrap_elements(self):
        self.maxDiff = None
        xmltree = etree.fromstring(
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'dtd-version="1.0" article-type="research-article" xml:lang="pt">'
            "<body>"
            "<p>Some text content without table wraps.</p>"
            "</body>"
            "</article>"
        )
        obtained = list(TableWrapValidation(xmltree).validate_tablewrap_existence())

        expected = [
            {
                "title": "table-wrap presence",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "research-article",
                "parent_lang": "pt",
                "item": "table-wrap",
                "sub_item": None,
                "validation_type": "exist",
                "response": "WARNING",
                "expected_value": "<table-wrap> element",
                "got_value": None,
                "message": "Got None, expected <table-wrap> element",
                "advice": "Add <table-wrap> element to properly illustrate the content.",
                "data": None,
            }
        ]

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(item, obtained[i])

    def test_tablewrap_validation_with_tablewrap_elements(self):
        self.maxDiff = None
        xmltree = etree.fromstring(
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'dtd-version="1.0" article-type="research-article" xml:lang="pt">'
            "<body>"
            '<table-wrap id="t01">'
            "<label>Table 1</label>"
            '<caption>Table caption</caption>'
            "<alternatives>"
            '<graphic xlink:href="image1-lowres.png" mime-subtype="low-resolution"/>'
            '<graphic xlink:href="image1-highres.png" mime-subtype="high-resolution"/>'
            "</alternatives>"
            "</table-wrap>"
            "</body>"
            '<sub-article article-type="translation" xml:lang="en">'
            "<body>"
            '<table-wrap id="t01">'
            "<label>Table 1:</label>"
            "<caption>Table caption</caption>"
            "<alternatives>"
            '<graphic xlink:href="image1-lowres.png" mime-subtype="low-resolution"/>'
            '<graphic xlink:href="image1-highres.png" mime-subtype="high-resolution"/>'
            "</alternatives>"
            "</table-wrap>"
            "</body>"
            "</sub-article>"
            "</article>"
        )
        obtained = list(TableWrapValidation(xmltree).validate_tablewrap_existence())

        expected = [
            {
                "title": "table-wrap presence",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "research-article",
                "parent_lang": "pt",
                "item": "table-wrap",
                "sub_item": None,
                "validation_type": "exist",
                "response": "OK",
                'expected_value': '<table-wrap> element',
                'got_value': '<table-wrap xmlns:xlink="http://www.w3.org/1999/xlink" '
                             'xmlns:mml="http://www.w3.org/1998/Math/MathML" '
                             'id="t01"><label>Table 1</label><caption>Table '
                             'caption</caption><alternatives><graphic '
                             'xlink:href="image1-lowres.png" '
                             'mime-subtype="low-resolution"/><graphic '
                             'xlink:href="image1-highres.png" '
                             'mime-subtype="high-resolution"/></alternatives></table-wrap>',

                'message': 'Got <table-wrap xmlns:xlink="http://www.w3.org/1999/xlink" '
                           'xmlns:mml="http://www.w3.org/1998/Math/MathML" '
                           'id="t01"><label>Table 1</label><caption>Table '
                           'caption</caption><alternatives><graphic '
                           'xlink:href="image1-lowres.png" '
                           'mime-subtype="low-resolution"/><graphic '
                           'xlink:href="image1-highres.png" '
                           'mime-subtype="high-resolution"/></alternatives></table-wrap>, '
                           'expected <table-wrap> element',
                "advice": None,
                "data": {
                    "alternative_parent": "table-wrap",
                    "table_wrap_id": "t01",
                    "label": "Table 1",
                    "caption": "Table caption",
                    "footnote": "",
                    "footnote_id": None,
                    "footnote_label": None,
                    "alternative_elements": ["graphic", "graphic"],
                    "parent": "article",
                    "parent_id": None,
                    "parent_article_type": "research-article",
                    "parent_lang": "pt",
                },
            }
        ]

        # Remover a chave "node" dos dados obtidos
        for item in obtained:
            if item.get("data"):
                item["data"].pop("node", None)

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(item, obtained[i])

    def test_fig_validation_with_fig_elements_fix_bug(self):
        self.maxDiff = None
        xml_tree = xml_utils.get_xml_tree(
            "tests/fixtures/htmlgenerator/table_wrap_group_and_fig_group/2236-8906"
            "-hoehnea-49-e1082020/2236-8906-hoehnea-49-e1082020.xml"
        )
        obtained = list(TableWrapValidation(xml_tree).validate_tablewrap_existence())

        # Remover a chave "node" dos dados obtidos
        for item in obtained:
            if item.get("data"):
                item["data"].pop("node", None)

        expected = [
            {
                "advice": None,
                "data": {
                    "alternative_elements": [],
                    "alternative_parent": "table-wrap",
                    "caption": "Classificação Sucessional adotada por alguns autores ao "
                               "longo dos anos.",
                    "footnote": "",
                    "footnote_id": None,
                    "footnote_label": None,
                    "label": "Tabela 1",
                    "parent": "article",
                    "parent_article_type": "research-article",
                    "parent_id": None,
                    "parent_lang": "pt",
                    "table_wrap_id": None,
                },
                "expected_value": "<table-wrap> element",
                "got_value": '<table-wrap xmlns:mml="http://www.w3.org/1998/Math/MathML" '
                             'xmlns:xlink="http://www.w3.org/1999/xlink" '
                             'xml:lang="pt"><label>Tabela '
                             "1</label><caption><title>Classificação Sucessional adotada por "
                             "alguns autores ao longo dos "
                             "anos.</title></caption></table-wrap>",
                "item": "table-wrap",
                "message": 'Got <table-wrap xmlns:mml="http://www.w3.org/1998/Math/MathML" '
                           'xmlns:xlink="http://www.w3.org/1999/xlink" '
                           'xml:lang="pt"><label>Tabela '
                           "1</label><caption><title>Classificação Sucessional adotada por "
                           "alguns autores ao longo dos anos.</title></caption></table-wrap>, "
                           "expected <table-wrap> element",
                "parent": "article",
                "parent_article_type": "research-article",
                "parent_id": None,
                "parent_lang": "pt",
                "response": "OK",
                "sub_item": None,
                "title": "table-wrap presence",
                "validation_type": "exist",
            },
            {
                "advice": None,
                "data": {
                    "alternative_elements": [],
                    "alternative_parent": "table-wrap",
                    "caption": "List of threatened species and their classification in "
                               "the lists of São Paulo, 2016, Brazil, 2019c and IUCN, "
                               "2019. VU categories: Vulnerable, EN: Endangered and EX: "
                               "Extinct.",
                    "footnote": "",
                    "footnote_id": None,
                    "footnote_label": None,
                    "label": "Table 4",
                    "parent": "article",
                    "parent_article_type": "research-article",
                    "parent_id": None,
                    "parent_lang": "pt",
                    "table_wrap_id": None,
                },
                "expected_value": "<table-wrap> element",
                "got_value": '<table-wrap xmlns:mml="http://www.w3.org/1998/Math/MathML" '
                             'xmlns:xlink="http://www.w3.org/1999/xlink" '
                             'xml:lang="en"><label>Table 4</label><caption><title>List of '
                             "threatened species and their classification in the lists of "
                             '<xref ref-type="bibr" rid="B48">São Paulo, 2016</xref>, Brazil, '
                             "2019c and IUCN, 2019. VU categories: Vulnerable, EN: Endangered "
                             "and EX: Extinct.</title></caption><table><thead><tr><th "
                             'rowspan="2" align="left">Espécie</th><th align="left"/><th '
                             'align="center">Listas</th><th align="left"/></tr><tr><th '
                             'align="center">São Paulo</th><th align="center">Brasil</th><th '
                             'align="center">IUCN</th></tr></thead><tbody><tr><td '
                             'align="left"><italic>Ocotea catharinensis</italic> Mez</td><td '
                             'align="center">VU</td><td align="center">VU</td><td '
                             'align="center">VU</td></tr><tr><td align="left"><italic>Cedrela '
                             'fissilis</italic> Vell.</td><td align="center">VU</td><td '
                             'align="center">VU</td><td align="center">EN</td></tr><tr><td '
                             'align="left"><italic>Trichilia silvatica</italic> C.DC.</td><td '
                             'align="center">-</td><td align="center">-</td><td '
                             'align="center">VU</td></tr><tr><td align="left"><italic>Virola '
                             "bicuhyba</italic> (Schott ex Spreng.) Warb.</td><td "
                             'align="center">EN</td><td align="center">EN</td><td '
                             'align="center">-</td></tr><tr><td align="left"><italic>Eugenia '
                             'prasina</italic> O.Berg</td><td align="center">-</td><td '
                             'align="center">-</td><td align="center">VU</td></tr><tr><td '
                             'align="left"><italic>Euplassa cantareirae</italic> '
                             'Sleumer</td><td align="center">EX</td><td '
                             'align="center">EN</td><td align="center">-</td></tr><tr><td '
                             'align="left"><italic>Pouteria bullata</italic> (S.Moore) '
                             'Baehni</td><td align="center">EN</td><td '
                             'align="center">EN</td><td '
                             'align="center">VU</td></tr></tbody></table></table-wrap>',
                "item": "table-wrap",
                "message": 'Got <table-wrap xmlns:mml="http://www.w3.org/1998/Math/MathML" '
                           'xmlns:xlink="http://www.w3.org/1999/xlink" '
                           'xml:lang="en"><label>Table 4</label><caption><title>List of '
                           "threatened species and their classification in the lists of <xref "
                           'ref-type="bibr" rid="B48">São Paulo, 2016</xref>, Brazil, 2019c '
                           "and IUCN, 2019. VU categories: Vulnerable, EN: Endangered and EX: "
                           'Extinct.</title></caption><table><thead><tr><th rowspan="2" '
                           'align="left">Espécie</th><th align="left"/><th '
                           'align="center">Listas</th><th align="left"/></tr><tr><th '
                           'align="center">São Paulo</th><th align="center">Brasil</th><th '
                           'align="center">IUCN</th></tr></thead><tbody><tr><td '
                           'align="left"><italic>Ocotea catharinensis</italic> Mez</td><td '
                           'align="center">VU</td><td align="center">VU</td><td '
                           'align="center">VU</td></tr><tr><td align="left"><italic>Cedrela '
                           'fissilis</italic> Vell.</td><td align="center">VU</td><td '
                           'align="center">VU</td><td align="center">EN</td></tr><tr><td '
                           'align="left"><italic>Trichilia silvatica</italic> C.DC.</td><td '
                           'align="center">-</td><td align="center">-</td><td '
                           'align="center">VU</td></tr><tr><td align="left"><italic>Virola '
                           "bicuhyba</italic> (Schott ex Spreng.) Warb.</td><td "
                           'align="center">EN</td><td align="center">EN</td><td '
                           'align="center">-</td></tr><tr><td align="left"><italic>Eugenia '
                           'prasina</italic> O.Berg</td><td align="center">-</td><td '
                           'align="center">-</td><td align="center">VU</td></tr><tr><td '
                           'align="left"><italic>Euplassa cantareirae</italic> '
                           'Sleumer</td><td align="center">EX</td><td '
                           'align="center">EN</td><td align="center">-</td></tr><tr><td '
                           'align="left"><italic>Pouteria bullata</italic> (S.Moore) '
                           'Baehni</td><td align="center">EN</td><td '
                           'align="center">EN</td><td '
                           'align="center">VU</td></tr></tbody></table></table-wrap>, '
                           "expected <table-wrap> element",
                "parent": "article",
                "parent_article_type": "research-article",
                "parent_id": None,
                "parent_lang": "pt",
                "response": "OK",
                "sub_item": None,
                "title": "table-wrap presence",
                "validation_type": "exist",
            }

        ]

        self.assertEqual(len(obtained), 8)
        # showing only the first and last record for the table
        self.assertDictEqual(expected[0], obtained[0])
        self.assertDictEqual(expected[1], obtained[7])


if __name__ == "__main__":
    unittest.main()
