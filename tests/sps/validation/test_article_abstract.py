from unittest import TestCase

from lxml import etree as ET

from packtools.sps.validation.article_abstract import HighlightsValidation, VisualAbstractsValidation, ArticleAbstractValidation


class HighlightsValidationTest(TestCase):
    def test_highlight_validation_exist(self):
        self.maxDiff = None
        xmltree = ET.fromstring(
            """
            <article article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
                <front>
                    <article-meta>
                        <abstract abstract-type="key-points">
                            <title>HIGHLIGHTS</title>
                            <p>highlight 1</p>
                            <p>highlight 2</p>
                        </abstract>
                    </article-meta>
                </front>
                <sub-article article-type="translation" id="01" xml:lang="es">
                    <front-stub>
                        <abstract abstract-type="key-points">
                            <title>HIGHLIGHTS</title>
                            <p>highlight 1</p>
                            <p>highlight 2</p>
                        </abstract>
                    </front-stub>
                </sub-article>
            </article>
            """
        )

        obtained = list(HighlightsValidation(xmltree).highlight_validation())

        expected = [
            {
                'title': 'Article highlights validation',
                'parent': 'article',
                'parent_id': None,
                'parent_article_type': 'research-article',
                'parent_lang': 'en',
                'item': 'abstract',
                'sub_item': '@abstract-type="key-points"',
                'validation_type': 'exist',
                'response': 'OK',
                'expected_value': [
                    'highlight 1',
                    'highlight 2'
                ],
                'got_value': [
                    'highlight 1',
                    'highlight 2'
                ],
                'message': "Got ['highlight 1', 'highlight 2'], expected ['highlight 1', 'highlight 2']",
                'advice': None,
                'data': {
                    'highlights': ['highlight 1', 'highlight 2'],
                    'parent': 'article',
                    'parent_article_type': 'research-article',
                    'parent_id': None,
                    'parent_lang': 'en',
                    'title': 'HIGHLIGHTS',
                    "list": [],
                    'kwds': [],
                },
            },
            {
                'title': 'Article highlights validation',
                'parent': 'sub-article',
                'parent_id': '01',
                'parent_article_type': 'translation',
                'parent_lang': 'es',
                'item': 'abstract',
                'sub_item': '@abstract-type="key-points"',
                'validation_type': 'exist',
                'response': 'OK',
                'expected_value': [
                    'highlight 1',
                    'highlight 2'
                ],
                'got_value': [
                    'highlight 1',
                    'highlight 2'
                ],
                'message': "Got ['highlight 1', 'highlight 2'], expected ['highlight 1', 'highlight 2']",
                'advice': None,
                'data': {
                    'highlights': ['highlight 1', 'highlight 2'],
                    'parent': 'sub-article',
                    'parent_article_type': 'translation',
                    'parent_id': '01',
                    'parent_lang': 'es',
                    'title': 'HIGHLIGHTS',
                    "list": [],
                    'kwds': [],
                },
            }
        ]

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(item, obtained[i])

    def test_highlight_validation_not_exist(self):
        self.maxDiff = None
        xmltree = ET.fromstring(
            """
            <article article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
                <front>
                    <article-meta />
                </front>
                <sub-article article-type="translation" id="01" xml:lang="es">
                    <front-stub />
                </sub-article>
            </article>
            """
        )

        obtained = list(HighlightsValidation(xmltree).highlight_validation("WARNING"))

        expected = [
            {
                'title': 'Article highlights validation',
                'parent': None,
                'parent_id': None,
                'parent_article_type': None,
                'parent_lang': None,
                'item': 'abstract',
                'sub_item': '@abstract-type="key-points"',
                'validation_type': 'exist',
                'response': 'WARNING',
                'expected_value': 'article highlights',
                'got_value': None,
                'message': "Got None, expected article highlights",
                'advice': None,
                'data': None,
            }
        ]

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(item, obtained[i])

    def test_tag_list_in_abstract_validation(self):
        self.maxDiff = None
        xmltree = ET.fromstring(
            """
            <article article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
                <front>
                    <article-meta>
                        <abstract abstract-type="key-points">
                            <title>HIGHLIGHTS</title>
                            <list>
                                <item>highlight 1</item>
                                <item>highlight 2</item>
                            </list>
                        </abstract>
                    </article-meta>
                </front>
                <sub-article article-type="translation" id="01" xml:lang="es">
                    <front-stub>
                        <abstract abstract-type="key-points">
                            <title>HIGHLIGHTS</title>
                            <list>
                                <item>highlight 1</item>
                                <item>highlight 2</item>
                            </list>
                        </abstract>
                    </front-stub>
                </sub-article>
            </article>
            """
        )

        obtained = list(HighlightsValidation(xmltree).tag_list_in_abstract_validation())

        expected = [
            {
                "title": "tag <list> in abstract",
                "parent": "article",
                "parent_article_type": "research-article",
                "parent_id": None,
                "parent_lang": "en",
                "validation_type": "exist",
                "response": "ERROR",
                "item": "abstract",
                "sub_item": '@abstract-type="key-points"',
                "expected_value": '<title><p>highlight 1</p></title> for each item',
                "got_value": '<list><item>highlight 1</item></list> in each item',
                "message": 'Got <list><item>highlight 1</item></list> in each item, expected <title><p>highlight 1</p></title> for each item',
                "advice": 'Replace <list> + <item> for <title> + <p>',
                "data": {
                    "highlights": [],
                    'kwds': [],
                    "list": ['highlight 1', 'highlight 2'],
                    "parent": "article",
                    "parent_article_type": "research-article",
                    "parent_id": None,
                    "parent_lang": "en",
                    "title": "HIGHLIGHTS",
                }
            }
        ]

        self.assertEqual(len(obtained), 2)
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(item, obtained[i])

    def test_tag_p_in_abstract_validation(self):
        self.maxDiff = None
        xmltree = ET.fromstring(
            """
            <article article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
                <front>
                    <article-meta>
                        <abstract abstract-type="key-points">
                            <title>HIGHLIGHTS</title>
                            <p>highlight 1</p>
                        </abstract>
                    </article-meta>
                </front>
                <sub-article article-type="translation" id="01" xml:lang="es">
                    <front-stub>
                        <abstract abstract-type="key-points">
                            <title>HIGHLIGHTS</title>
                            <p>highlight 1</p>
                        </abstract>
                    </front-stub>
                </sub-article>
            </article>
            """
        )

        obtained = list(HighlightsValidation(xmltree).tag_p_in_abstract_validation())

        expected = [
            {
                "title": "tag <p> in abstract",
                "parent": "article",
                "parent_article_type": "research-article",
                "parent_id": None,
                "parent_lang": "en",
                "validation_type": "exist",
                "response": "ERROR",
                "item": "abstract",
                "sub_item": '@abstract-type="key-points"',
                "expected_value": 'more than one <title><p>item</p></title>',
                "got_value": '<title><p>highlight 1</p></title>',
                "message": 'Got <title><p>highlight 1</p></title>, expected more than one <title><p>item</p></title>',
                "advice": 'Provide more than one item like <title><p>item</p></title>',
                "data": {
                    "highlights": ['highlight 1'],
                    "list": [],
                    'kwds': [],
                    "parent": "article",
                    "parent_article_type": "research-article",
                    "parent_id": None,
                    "parent_lang": "en",
                    "title": "HIGHLIGHTS",
                }
            }
        ]

        self.assertEqual(len(obtained), 2)
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(item, obtained[i])


class VisualAbstractsValidationTest(TestCase):
    def test_visual_abstracts_validation_exist(self):
        self.maxDiff = None
        xmltree = ET.fromstring(
            """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" dtd-version="1.1" 
            specific-use="sps-1.9" xml:lang="en">
                <front>
                    <article-meta>
                        <abstract abstract-type="graphical">
                            <title>Visual Abstract</title>
                                <p>
                                    <fig id="vf01">
                                        <caption>
                                            <title>Título</title>
                                        </caption>
                                        <graphic xlink:href="1234-5678-zwy-12-04-0123-vs01.tif"/>
                                    </fig>
                                </p>
                        </abstract>
                    </article-meta>
                </front>
                <sub-article article-type="translation" id="01" xml:lang="es">
                    <front-stub>
                        <abstract abstract-type="graphical">
                            <title>Visual Abstract</title>
                                <p>
                                    <fig id="vf01">
                                        <caption>
                                            <title>Título</title>
                                        </caption>
                                        <graphic xlink:href="1234-5678-zwy-12-04-0123-vs01.tif"/>
                                    </fig>
                                </p>
                        </abstract>
                    </front-stub>
                </sub-article>
            </article>
            """
        )

        obtained = list(VisualAbstractsValidation(xmltree).visual_abstracts_validation())

        expected = [
            {
                'title': 'Article visual abstracts validation',
                'parent': 'article',
                'parent_id': None,
                'parent_article_type': 'research-article',
                'parent_lang': 'en',
                'item': 'abstract',
                'sub_item': '@abstract-type="graphical"',
                'validation_type': 'exist',
                'response': 'OK',
                'expected_value': '1234-5678-zwy-12-04-0123-vs01.tif',
                'got_value': '1234-5678-zwy-12-04-0123-vs01.tif',
                'message': 'Got 1234-5678-zwy-12-04-0123-vs01.tif, expected 1234-5678-zwy-12-04-0123-vs01.tif',
                'advice': None,
                'data': {
                    'title': 'Visual Abstract',
                    'fig_id': 'vf01',
                    'caption': 'Título',
                    'graphic': '1234-5678-zwy-12-04-0123-vs01.tif',
                    'parent': 'article',
                    'parent_id': None,
                    'parent_article_type': 'research-article',
                    'parent_lang': 'en',
                    'kwds': [],
                }
            },
            {
                'title': 'Article visual abstracts validation',
                'parent': 'sub-article',
                'parent_id': '01',
                'parent_article_type': 'translation',
                'parent_lang': 'es',
                'item': 'abstract',
                'sub_item': '@abstract-type="graphical"',
                'validation_type': 'exist',
                'response': 'OK',
                'expected_value': '1234-5678-zwy-12-04-0123-vs01.tif',
                'got_value': '1234-5678-zwy-12-04-0123-vs01.tif',
                'message': 'Got 1234-5678-zwy-12-04-0123-vs01.tif, expected 1234-5678-zwy-12-04-0123-vs01.tif',
                'advice': None,
                'data': {
                    'title': 'Visual Abstract',
                    'fig_id': 'vf01',
                    'caption': 'Título',
                    'graphic': '1234-5678-zwy-12-04-0123-vs01.tif',
                    'parent': 'sub-article',
                    'parent_id': '01',
                    'parent_article_type': 'translation',
                    'parent_lang': 'es',
                    'kwds': [],
                }
            }
        ]

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(item, obtained[i])

    def test_visual_abstracts_validation_not_exist(self):
        self.maxDiff = None
        xmltree = ET.fromstring(
            """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" dtd-version="1.1" 
            specific-use="sps-1.9" xml:lang="en">
                <front>
                    <article-meta />
                </front>
                <sub-article article-type="translation" id="01" xml:lang="es">
                    <front-stub />
                </sub-article>
            </article>
            """
        )

        obtained = list(VisualAbstractsValidation(xmltree).visual_abstracts_validation("WARNING"))

        expected = [
            {
                'title': 'Article visual abstracts validation',
                'parent': None,
                'parent_id': None,
                'parent_article_type': None,
                'parent_lang': None,
                'item': 'abstract',
                'sub_item': '@abstract-type="graphical"',
                'validation_type': 'exist',
                'response': 'WARNING',
                'expected_value': 'article visual abstracts',
                'got_value': None,
                'message': 'Got None, expected article visual abstracts',
                'advice': None,
                'data': None,
            }
        ]

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(item, obtained[i])


class ArticleAbstractValidationTest(TestCase):
    def test_abstract_type_validation(self):
        self.maxDiff = None
        xmltree = ET.fromstring(
            """
            <article article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
                <front>
                    <article-meta>
                        <abstract abstract-type="invalid-value">
                            <title>HIGHLIGHTS</title>
                            <p>highlight 1</p>
                            <p>highlight 2</p>
                        </abstract>
                    </article-meta>
                </front>
                <sub-article article-type="translation" id="01" xml:lang="es">
                    <front-stub>
                        <abstract abstract-type="invalid-value">
                            <title>HIGHLIGHTS</title>
                            <p>highlight 1</p>
                            <p>highlight 2</p>
                        </abstract>
                    </front-stub>
                </sub-article>
            </article>
            """
        )

        obtained = list(ArticleAbstractValidation(xmltree).abstract_type_validation())

        expected = [
            {
                "title": "abstract-type attribute",
                "parent": "article",
                "parent_article_type": "research-article",
                "parent_id": None,
                "parent_lang": "en",
                "item": "abstract",
                "sub_item": "@abstract-type",
                "validation_type": "value in list",
                "response": "ERROR",
                "got_value": '<abstract abstract-type="invalid-value">',
                "expected_value": '<abstract abstract-type="key-points"> or <abstract abstract-type="graphical">',
                "message": 'Got <abstract abstract-type="invalid-value">, expected <abstract abstract-type="key-points"> or <abstract abstract-type="graphical">',
                "advice": 'Provide <abstract abstract-type="key-points"> or <abstract abstract-type="graphical">',
                "data": {
                    "abstract_type": "invalid-value",
                    "html_text": "HIGHLIGHTS highlight 1 highlight 2",
                    "lang": "en",
                    "parent": "article",
                    "parent_article_type": "research-article",
                    "parent_id": None,
                    "parent_lang": "en",
                    "plain_text": "HIGHLIGHTS highlight 1 highlight 2",
                },
            },
            {
                "title": "abstract-type attribute",
                "parent": "sub-article",
                "parent_article_type": "translation",
                "parent_id": "01",
                "parent_lang": "es",
                "item": "abstract",
                "sub_item": "@abstract-type",
                "validation_type": "value in list",
                "response": "ERROR",
                "got_value": '<abstract abstract-type="invalid-value">',
                "expected_value": '<abstract abstract-type="key-points"> or <abstract abstract-type="graphical">',
                "message": 'Got <abstract abstract-type="invalid-value">, expected <abstract abstract-type="key-points"> or <abstract abstract-type="graphical">',
                "advice": 'Provide <abstract abstract-type="key-points"> or <abstract abstract-type="graphical">',
                "data": {
                    "abstract_type": "invalid-value",
                    "html_text": "HIGHLIGHTS highlight 1 highlight 2",
                    "id": "01",
                    "lang": "es",
                    "parent": "sub-article",
                    "parent_article_type": "translation",
                    "parent_id": "01",
                    "parent_lang": "es",
                    "plain_text": "HIGHLIGHTS highlight 1 highlight 2",
                },
            }

        ]

        self.assertEqual(len(obtained), 2)
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(item, obtained[i])
