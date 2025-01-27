from unittest import TestCase

from lxml import etree as ET

from packtools.sps.validation.article_abstract import (
    HighlightValidation,
    HighlightsValidation,
    VisualAbstractValidation,
    VisualAbstractsValidation,
    ArticleAbstractsValidation,
)
from packtools.sps.models.article_abstract import (
    ArticleHighlights,
    ArticleVisualAbstracts,
)

VALIDATE_EXISTS_PARAMS = {
    "article_type_requires": [],
    "article_type_unexpects": [
        "addendum",
        "article-commentary",
        "book-review",
        "brief-report",
        "correction",
        "editorial",
        "letter",
        "obituary",
        "partial-retraction",
        "product-review",
        "rapid-communication",
        "reply",
        "retraction",
        "other",
    ],
    "article_type_neutral": [
        "reviewer-report",
        "data-article",
    ],
    "article_type_accepts": [
        "case-report",
        "research-article",
        "review-article",
    ],
}


class HighlightsValidationTest(TestCase):
    def test_highlight_validate_exists(self):
        self.maxDiff = None
        xml_tree = ET.fromstring(
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

        obtained = HighlightsValidation(xml_tree).validate_exists(
            **VALIDATE_EXISTS_PARAMS
        )

        expected = {
            "title": "abstracts (key-points)",
            "parent": "article",
            "parent_id": None,
            "parent_article_type": "research-article",
            "parent_lang": "en",
            "item": "abstracts (key-points)",
            "sub_item": None,
            "validation_type": "exist",
            "response": "OK",
            "expected_value": [],
            "got_value": [],
            "message": "Got [], expected abstracts (key-points) is acceptable",
            "advice": None,
            "data": [],
        }

        self.assertDictEqual(expected, obtained)

    def test_highlight_validate_tag_list_in_abstract(self):
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

        obtained = []
        for abstract in ArticleHighlights(xmltree).article_abstracts():
            obtained.append(
                HighlightValidation(abstract).validate_tag_list_in_abstract()
            )

        expected = [
            {
                "title": "list",
                "parent": "article",
                "parent_article_type": "research-article",
                "parent_id": None,
                "parent_lang": "en",
                "validation_type": "exist",
                "response": "ERROR",
                "item": "abstract (key-points)",
                "sub_item": "list",
                "expected_value": None,
                "got_value": ["highlight 1", "highlight 2"],
                "message": "Got ['highlight 1', 'highlight 2'], expected None",
                "advice": "Remove <list> and add <p>",
                "data": {
                    "abstract_type": "key-points",
                    "highlights": [],
                    "kwds": [],
                    "list": ["highlight 1", "highlight 2"],
                    "parent": "article",
                    "parent_article_type": "research-article",
                    "parent_id": None,
                    "parent_lang": "en",
                    "title": "HIGHLIGHTS",
                },
            },
            {
                "title": "list",
                "parent": "sub-article",
                "parent_article_type": "translation",
                "parent_id": "01",
                "parent_lang": "es",
                "validation_type": "exist",
                "response": "ERROR",
                "item": "abstract (key-points)",
                "sub_item": "list",
                "expected_value": None,
                "got_value": ["highlight 1", "highlight 2"],
                "message": "Got ['highlight 1', 'highlight 2'], expected None",
                "advice": "Remove <list> and add <p>",
                "data": {
                    "abstract_type": "key-points",
                    "highlights": [],
                    "kwds": [],
                    "list": ["highlight 1", "highlight 2"],
                    "parent": "sub-article",
                    "parent_article_type": "translation",
                    "parent_id": "01",
                    "parent_lang": "es",
                    "title": "HIGHLIGHTS",
                },
            },
        ]

        self.assertEqual(len(obtained), 2)
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(item, obtained[i])

    def test_highlight_validate_tag_p_in_abstract(self):
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

        obtained = []
        for abstract in ArticleHighlights(xmltree).article_abstracts():
            obtained.append(HighlightValidation(abstract).validate_tag_p_in_abstract())

        expected = [
            {
                "title": "p",
                "parent": "article",
                "parent_article_type": "research-article",
                "parent_id": None,
                "parent_lang": "en",
                "validation_type": "exist",
                "response": "ERROR",
                "item": "abstract (key-points)",
                "sub_item": "p",
                "expected_value": "p",
                "got_value": ["highlight 1"],
                "message": "Got ['highlight 1'], expected p",
                "advice": "Provide more than one p",
                "data": {
                    "abstract_type": "key-points",
                    "highlights": ["highlight 1"],
                    "list": [],
                    "kwds": [],
                    "parent": "article",
                    "parent_article_type": "research-article",
                    "parent_id": None,
                    "parent_lang": "en",
                    "title": "HIGHLIGHTS",
                },
            }
        ]

        self.assertEqual(len(obtained), 2)
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(item, obtained[i])

    def test_highlight_validate_unexpected_kwd(self):
        self.maxDiff = None
        xmltree = ET.fromstring(
            """
            <article article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
                <front>
                    <article-meta>
                        <abstract abstract-type="key-points">
                            <kwd-group xml:lang="en">
                                <kwd>kwd_01</kwd>
                                <kwd>kwd_02</kwd>
                            </kwd-group>
                        </abstract>
                    </article-meta>
                </front>
            </article>
            """
        )

        obtained = []
        for abstract in ArticleHighlights(xmltree).article_abstracts():
            obtained.append(HighlightValidation(abstract).validate_unexpected_kwd())

        expected = [
            {
                "title": "unexpected kwd",
                "parent": "article",
                "parent_article_type": "research-article",
                "parent_id": None,
                "parent_lang": "en",
                "validation_type": "exist",
                "response": "ERROR",
                "item": "abstract (key-points)",
                "sub_item": "kwd",
                "expected_value": None,
                "got_value": ["kwd_01", "kwd_02"],
                "message": "Got ['kwd_01', 'kwd_02'], expected None",
                "advice": "Remove keywords (<kwd>) from <abstract abstract-type='key-points'>",
                "data": {
                    "abstract_type": "key-points",
                    "highlights": [],
                    "list": [],
                    "kwds": ["kwd_01", "kwd_02"],
                    "parent": "article",
                    "parent_article_type": "research-article",
                    "parent_id": None,
                    "parent_lang": "en",
                    "title": None,
                },
            }
        ]

        self.assertEqual(len(obtained), 1)
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(item, obtained[i])

    def test_highlight_validate_tag_title_in_abstract(self):
        self.maxDiff = None
        xmltree = ET.fromstring(
            """
            <article article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
                <front>
                    <article-meta>
                        <abstract abstract-type="key-points">
                            <p>highlight 1</p>
                        </abstract>
                    </article-meta>
                </front>
                <sub-article article-type="translation" id="01" xml:lang="es">
                    <front-stub>
                        <abstract abstract-type="key-points">
                            <p>highlight 1</p>
                        </abstract>
                    </front-stub>
                </sub-article>
            </article>
            """
        )

        obtained = []
        for abstract in ArticleHighlights(xmltree).article_abstracts():
            obtained.append(
                HighlightValidation(abstract).validate_tag_title_in_abstract()
            )

        expected = [
            {
                "title": "title",
                "parent": "article",
                "parent_article_type": "research-article",
                "parent_id": None,
                "parent_lang": "en",
                "validation_type": "exist",
                "response": "ERROR",
                "item": "abstract (key-points)",
                "sub_item": "title",
                "expected_value": "title",
                "got_value": None,
                "message": "Got None, expected title",
                "advice": "Provide title",
                "data": {
                    "abstract_type": "key-points",
                    "highlights": ["highlight 1"],
                    "list": [],
                    "kwds": [],
                    "parent": "article",
                    "parent_article_type": "research-article",
                    "parent_id": None,
                    "parent_lang": "en",
                    "title": None,
                },
            }
        ]

        self.assertEqual(len(obtained), 2)
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(item, obtained[i])


class VisualAbstractsValidationTest(TestCase):
    def test_visual_abstracts_validate_exists(self):
        self.maxDiff = None
        xml_tree = ET.fromstring(
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

        obtained = VisualAbstractsValidation(xml_tree).validate_exists(
            **VALIDATE_EXISTS_PARAMS
        )

        expected = {
            "title": "abstracts (graphical)",
            "parent": "article",
            "parent_id": None,
            "parent_article_type": "research-article",
            "parent_lang": "en",
            "item": "abstracts (graphical)",
            "sub_item": None,
            "validation_type": "exist",
            "response": "OK",
            "expected_value": [],
            "got_value": [],
            "message": "Got [], expected abstracts (graphical) is acceptable",
            "advice": None,
            "data": [],
        }

        self.assertDictEqual(obtained, expected)

    def test_visual_abstracts_validate_unexpected_kwd(self):
        self.maxDiff = None
        xml_tree = ET.fromstring(
            """
            <article article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
                <front>
                    <article-meta>
                        <abstract abstract-type="graphical">
                            <kwd-group xml:lang="en">
                                <kwd>kwd_01</kwd>
                                <kwd>kwd_02</kwd>
                            </kwd-group>
                        </abstract>
                    </article-meta>
                </front>
            </article>
            """
        )

        obtained = []
        for abstract in ArticleVisualAbstracts(xml_tree).article_abstracts():
            obtained.append(
                VisualAbstractValidation(abstract).validate_unexpected_kwd()
            )

        expected = [
            {
                "title": "unexpected kwd",
                "parent": "article",
                "parent_article_type": "research-article",
                "parent_id": None,
                "parent_lang": "en",
                "validation_type": "exist",
                "response": "ERROR",
                "item": "abstract (graphical)",
                "sub_item": "kwd",
                "expected_value": None,
                "got_value": ["kwd_01", "kwd_02"],
                "message": "Got ['kwd_01', 'kwd_02'], expected None",
                "advice": "Remove keywords (<kwd>) from <abstract abstract-type='graphical'>",
                "data": {
                    "abstract_type": "graphical",
                    "caption": None,
                    "fig_id": None,
                    "graphic": None,
                    "kwds": ["kwd_01", "kwd_02"],
                    "parent": "article",
                    "parent_article_type": "research-article",
                    "parent_id": None,
                    "parent_lang": "en",
                    "title": None,
                },
            }
        ]

        self.assertEqual(len(obtained), 1)
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(item, obtained[i])

    def test_visual_abstracts_validate_tag_title_in_abstract(self):
        self.maxDiff = None
        xml_tree = ET.fromstring(
            """
            <article article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
                <front>
                    <article-meta>
                        <abstract abstract-type="graphical">
                            <kwd-group xml:lang="en">
                                <kwd>kwd_01</kwd>
                                <kwd>kwd_02</kwd>
                            </kwd-group>
                        </abstract>
                    </article-meta>
                </front>
            </article>
            """
        )

        obtained = []
        for abstract in ArticleVisualAbstracts(xml_tree).article_abstracts():
            obtained.append(
                VisualAbstractValidation(abstract).validate_tag_title_in_abstract()
            )

        expected = [
            {
                "title": "title",
                "parent": "article",
                "parent_article_type": "research-article",
                "parent_id": None,
                "parent_lang": "en",
                "validation_type": "exist",
                "response": "ERROR",
                "item": "abstract (graphical)",
                "sub_item": "title",
                "expected_value": "title",
                "got_value": None,
                "message": "Got None, expected title",
                "advice": "Provide title",
                "data": {
                    "abstract_type": "graphical",
                    "caption": None,
                    "fig_id": None,
                    "graphic": None,
                    "kwds": ["kwd_01", "kwd_02"],
                    "parent": "article",
                    "parent_article_type": "research-article",
                    "parent_id": None,
                    "parent_lang": "en",
                    "title": None,
                },
            }
        ]

        self.assertEqual(len(obtained), 1)
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(item, obtained[i])

    def test_visual_abstracts_validate_tag_graphic_in_abstract(self):
        self.maxDiff = None
        xml_tree = ET.fromstring(
            """
            <article article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
                <front>
                    <article-meta>
                        <abstract abstract-type="graphical">
                            <kwd-group xml:lang="en">
                                <kwd>kwd_01</kwd>
                                <kwd>kwd_02</kwd>
                            </kwd-group>
                        </abstract>
                    </article-meta>
                </front>
            </article>
            """
        )

        obtained = []
        for abstract in ArticleVisualAbstracts(xml_tree).article_abstracts():
            obtained.append(
                VisualAbstractValidation(abstract).validate_tag_graphic_in_abstract()
            )

        expected = [
            {
                "title": "graphic",
                "parent": "article",
                "parent_article_type": "research-article",
                "parent_id": None,
                "parent_lang": "en",
                "validation_type": "exist",
                "response": "ERROR",
                "item": "abstract (graphical)",
                "sub_item": "graphic",
                "expected_value": "graphic",
                "got_value": None,
                "message": "Got None, expected graphic",
                "advice": "Provide graphic",
                "data": {
                    "abstract_type": "graphical",
                    "caption": None,
                    "fig_id": None,
                    "graphic": None,
                    "kwds": ["kwd_01", "kwd_02"],
                    "parent": "article",
                    "parent_article_type": "research-article",
                    "parent_id": None,
                    "parent_lang": "en",
                    "title": None,
                },
            }
        ]

        self.assertEqual(len(obtained), 1)
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(item, obtained[i])


class ArticleAbstractValidationTest(TestCase):
    def test_abstract_type_validation(self):
        self.maxDiff = None
        xml_tree = ET.fromstring(
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

        obtained = list(
            ArticleAbstractsValidation(xml_tree).validate_abstracts_type(
                expected_abstract_type_list=["key-points", "graphical"]
            )
        )

        expected = [
            {
                "title": "@abstract-type",
                "parent": "article",
                "parent_article_type": "research-article",
                "parent_id": None,
                "parent_lang": "en",
                "item": "abstract",
                "sub_item": "@abstract-type",
                "validation_type": "value in list",
                "response": "ERROR",
                "got_value": "invalid-value",
                "expected_value": "one of ['key-points', 'graphical']",
                "message": "Got invalid-value, expected one of ['key-points', 'graphical']",
                "advice": "Use one of ['key-points', 'graphical'] as abstract-type",
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
                "title": "@abstract-type",
                "parent": "sub-article",
                "parent_article_type": "translation",
                "parent_id": "01",
                "parent_lang": "es",
                "item": "abstract",
                "sub_item": "@abstract-type",
                "validation_type": "value in list",
                "response": "ERROR",
                "got_value": "invalid-value",
                "expected_value": "one of ['key-points', 'graphical']",
                "message": "Got invalid-value, expected one of ['key-points', 'graphical']",
                "advice": "Use one of ['key-points', 'graphical'] as abstract-type",
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
            },
        ]

        self.assertEqual(len(obtained), 2)
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(item, obtained[i])
