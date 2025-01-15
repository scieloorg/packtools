from lxml import etree
from unittest import TestCase, skip

from packtools.sps.validation.alternatives import AlternativesValidation
from packtools.sps.validation.exceptions import ValidationAlternativesException


class AlternativesValidationTest(TestCase):
    @skip("Teste pendente de correção e/ou ajuste")
    def test_validation_success(self):
        self.maxDiff = None
        self.xml_tree = etree.fromstring(
            """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" 
            dtd-version="1.0" article-type="research-article" xml:lang="pt">
                <body>
                    <table-wrap>
                        <alternatives>
                            <graphic xlink:href="nomedaimagemdatabela.svg"/>
                            <table />
                        </alternatives>
                    </table-wrap>
                </body>
                <sub-article article-type="translation" xml:lang="en" id="TRen">
                    <body>
                        <fig>
                            <alternatives>
                                <graphic xlink:href="nomedaimagemdatabela.svg"/>
                                <media />
                            </alternatives>
                        </fig>
                    </body>
                </sub-article>
            </article>
            """
        )
        params = {
            "table-wrap": ["graphic", "table"],
            "fig": ["graphic", "media"]
        }
        obtained = list(AlternativesValidation(self.xml_tree, params).validate())
        expected = [
            {
                'title': 'Alternatives validation',
                'parent': 'sub-article',
                'parent_article_type': 'translation',
                'parent_id': 'TRen',
                'parent_lang': 'en',
                'item': 'fig',
                'sub_item': 'alternatives',
                'validation_type': 'value in list',
                'response': 'OK',
                'expected_value': ['graphic', 'media'],
                'got_value': ['graphic', 'media'],
                'message': "Got ['graphic', 'media'], expected ['graphic', 'media']",
                'advice': None,
                'data': {
                    'alternative_elements': ['graphic', 'media'],
                    'alternative_parent': 'fig',
                    'caption_text': '',
                    'fig_id': None,
                    'fig_type': None,
                    'graphic_href': 'nomedaimagemdatabela.svg',
                    'label': None,
                    'parent': 'sub-article',
                    'parent_article_type': 'translation',
                    'parent_id': 'TRen',
                    'parent_lang': 'en',
                    'source_attrib': None
                },
            },
            {
                'title': 'Alternatives validation',
                'parent': 'article',
                'parent_article_type': 'research-article',
                'parent_id': None,
                'parent_lang': 'pt',
                'item': 'table-wrap',
                'sub_item': 'alternatives',
                'validation_type': 'value in list',
                'response': 'OK',
                'expected_value': ['graphic', 'table'],
                'got_value': ['graphic', 'table'],
                'message': "Got ['graphic', 'table'], expected ['graphic', 'table']",
                'advice': None,
                'data': {
                    'caption': '',
                    'footnote': '',
                    'footnote_id': None,
                    'footnote_label': None,
                    'label': None,
                    'alternative_elements': ['graphic', 'table'],
                    'alternative_parent': 'table-wrap',
                    'table_wrap_id': None,
                    'parent': 'article',
                    'parent_article_type': 'research-article',
                    'parent_id': None,
                    'parent_lang': 'pt'
                },
            }
        ]
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(item, obtained[i])

    @skip("Teste pendente de correção e/ou ajuste")
    def test_validation_children_fail(self):
        self.maxDiff = None
        self.xml_tree = etree.fromstring(
            """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML"
            dtd-version="1.0" article-type="research-article" xml:lang="pt">
                <body>
                    <table-wrap>
                        <alternatives>
                            <p />
                        </alternatives>
                    </table-wrap>
                </body>
                <sub-article article-type="translation" xml:lang="en" id="TRen">
                    <body>
                        <fig>
                            <alternatives>
                                <title />
                                <abstract />
                            </alternatives>
                        </fig>
                    </body>
                </sub-article>
            </article>
            """
        )
        params = {
            "table-wrap": ["graphic", "table"],
            "fig": ["graphic", "media"]
        }
        obtained = list(AlternativesValidation(self.xml_tree, params).validate())
        expected = [
            {
                'title': 'Alternatives validation',
                'parent': 'sub-article',
                'parent_id': 'TRen',
                'parent_article_type': 'translation',
                'parent_lang': 'en',
                'item': 'fig',
                'sub_item': 'alternatives',
                'validation_type': 'value in list',
                'expected_value': ['graphic', 'media'],
                'got_value': ['title', 'abstract'],
                'response': 'CRITICAL',
                'message': "Got ['title', 'abstract'], expected ['graphic', 'media']",
                'advice': "Add ['graphic', 'media'] as sub-elements of fig/alternatives",
                'data': {
                    'caption_text': '',
                    'fig_id': None,
                    'fig_type': None,
                    'graphic_href': None,
                    'label': None,
                    'source_attrib': None,
                    'alternative_elements': ['title', 'abstract'],
                    'alternative_parent': 'fig',
                    'parent': 'sub-article',
                    'parent_id': 'TRen',
                    'parent_lang': 'en',
                    'parent_article_type': 'translation'
                }
            },
            {
                'title': 'Alternatives validation',
                'parent': 'article',
                'parent_id': None,
                'parent_article_type': 'research-article',
                'parent_lang': 'pt',
                'item': 'table-wrap',
                'sub_item': 'alternatives',
                'validation_type': 'value in list',
                'expected_value': ['graphic', 'table'],
                'got_value': ['p'],
                'response': 'CRITICAL',
                'message': "Got ['p'], expected ['graphic', 'table']",
                'advice': "Add ['graphic', 'table'] as sub-elements of table-wrap/alternatives",
                'data': {
                    'table_wrap_id': None,
                    'caption': '',
                    'footnote': '',
                    'footnote_id': None,
                    'footnote_label': None,
                    'label': None,
                    'alternative_elements': ['p'],
                    'alternative_parent': 'table-wrap',
                    'parent': 'article',
                    'parent_lang': 'pt',
                    'parent_id': None,
                    'parent_article_type': 'research-article'
                }
            }
        ]
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(item, obtained[i])

    @skip("Teste pendente de correção e/ou ajuste")
    def test_validation_parent_fail(self):
        self.maxDiff = None
        self.xml_tree = etree.fromstring(
            """
                <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML"
                dtd-version="1.0" article-type="research-article" xml:lang="pt">
                    <body>
                        <inline-formula>
                            <alternatives>
                                <mml:math />
                                <tex-math />
                            </alternatives>
                        </inline-formula>
                    </body>
                </article>
                """
        )
        params = {
            "table-wrap": ["graphic", "table"],
            "fig": ["graphic", "media"]
        }
        obtained = AlternativesValidation(self.xml_tree, params)
        with self.assertRaises(ValidationAlternativesException) as context:
            next(obtained.validate())
        self.assertEqual("The element 'inline-formula' is not configured to use 'alternatives'. Provide alternatives "
                         "parent and children", str(context.exception))
