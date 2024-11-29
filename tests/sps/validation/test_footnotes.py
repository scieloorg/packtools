from unittest import TestCase
from lxml import etree

from packtools.sps.validation.footnotes import FnGroupValidation


class FnGroupValidationValidationTest(TestCase):
    def test_label(self):
        self.maxDiff = None
        xml_tree = etree.fromstring(
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'dtd-version="1.3" article-type="research-article" xml:lang="pt">'
            "<back>"
            "<fn-group>"
            "<title>Notas</title>"
            '<fn fn-type="supported-by" id="fn01">'
            "<p>Vivamus sodales fermentum lorem, consectetur mollis lacus sollicitudin quis</p>"
            "</fn>"
            "</fn-group>"
            "</back>"
            "</article>"
        )

        obtained = list(
            FnGroupValidation(
                xml_tree=xml_tree,
                rules={
                    "fn_label_error_level": "WARNING",
                },
            ).validate()
        )

        expected = [
            {
                "title": "label",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "research-article",
                "parent_lang": "pt",
                "item": "label",
                "sub_item": None,
                "validation_type": "exist",
                "response": "WARNING",
                "expected_value": "label",
                "got_value": None,
                "message": "Got None, expected label",
                "advice": "Identify the label",
                "data": {
                    "fn_bold": None,
                    "fn_id": "fn01",
                    "fn_label": None,
                    "fn_parent": "fn-group",
                    "fn_text": "Vivamus sodales fermentum lorem, consectetur mollis lacus sollicitudin quis",
                    "fn_title": None,
                    "fn_type": "supported-by",
                },
            }
        ]

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(item, obtained[i])

    def test_title(self):
        self.maxDiff = None
        xml_tree = etree.fromstring(
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'dtd-version="1.3" article-type="research-article" xml:lang="pt">'
            "<back>"
            "<fn-group>"
            "<title>Notas</title>"
            '<fn fn-type="supported-by" id="fn01">'
            "<label>*</label>"
            "<title>título</title>"
            "<p>Vivamus sodales fermentum lorem, consectetur mollis lacus sollicitudin quis</p>"
            "</fn>"
            "</fn-group>"
            "</back>"
            "</article>"
        )

        obtained = list(
            FnGroupValidation(
                xml_tree=xml_tree,
                rules={
                    "fn_title_error_level": "WARNING",
                },
            ).validate()
        )

        expected = [
            {
                "title": "title",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "research-article",
                "parent_lang": "pt",
                "item": "title",
                "sub_item": None,
                "validation_type": "exist",
                "response": "WARNING",
                "expected_value": "label",
                "got_value": "title",
                "message": "Got title, expected label",
                "advice": "Replace title by label",
                "data": {
                    "fn_bold": None,
                    "fn_id": "fn01",
                    "fn_label": "*",
                    "fn_parent": "fn-group",
                    "fn_text": "*títuloVivamus sodales fermentum lorem, consectetur mollis lacus sollicitudin quis",
                    "fn_title": "título",
                    "fn_type": "supported-by",
                },
            }
        ]

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(item, obtained[i])

    def test_bold(self):
        self.maxDiff = None
        xml_tree = etree.fromstring(
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'dtd-version="1.3" article-type="research-article" xml:lang="pt">'
            "<back>"
            "<fn-group>"
            "<title>Notas</title>"
            '<fn fn-type="supported-by" id="fn01">'
            "<label>*</label>"
            "<bold>negrito</bold>"
            "<p>Vivamus sodales fermentum lorem, consectetur mollis lacus sollicitudin quis</p>"
            "</fn>"
            "</fn-group>"
            "</back>"
            "</article>"
        )

        obtained = list(
            FnGroupValidation(
                xml_tree=xml_tree,
                rules={
                    "fn_bold_error_level": "WARNING",
                },
            ).validate()
        )

        expected = [
            {
                "title": "bold",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "research-article",
                "parent_lang": "pt",
                "item": "bold",
                "sub_item": None,
                "validation_type": "exist",
                "response": "WARNING",
                "expected_value": "label",
                "got_value": "bold",
                "message": "Got bold, expected label",
                "advice": "Replace bold by label",
                "data": {
                    "fn_bold": "negrito",
                    "fn_id": "fn01",
                    "fn_label": "*",
                    "fn_parent": "fn-group",
                    "fn_text": "*negritoVivamus sodales fermentum lorem, consectetur mollis lacus sollicitudin quis",
                    "fn_title": None,
                    "fn_type": "supported-by",
                },
            }
        ]

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(item, obtained[i])

    def test_type(self):
        self.maxDiff = None
        xml_tree = etree.fromstring(
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'dtd-version="1.3" article-type="research-article" xml:lang="pt">'
            "<back>"
            "<fn-group>"
            "<title>Notas</title>"
            '<fn id="fn01">'
            "<label>*</label>"
            "<p>Vivamus sodales fermentum lorem, consectetur mollis lacus sollicitudin quis</p>"
            "</fn>"
            "</fn-group>"
            "</back>"
            "</article>"
        )

        obtained = list(
            FnGroupValidation(
                xml_tree=xml_tree,
                rules={
                    "fn_type_error_level": "ERROR",
                },
            ).validate()
        )

        expected = [
            {
                "title": "type",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "research-article",
                "parent_lang": "pt",
                "item": "type",
                "sub_item": None,
                "validation_type": "exist",
                "response": "ERROR",
                "expected_value": "type",
                "got_value": None,
                "message": "Got None, expected type",
                "advice": "Identify the type",
                "data": {
                    "fn_bold": None,
                    "fn_id": "fn01",
                    "fn_label": "*",
                    "fn_parent": "fn-group",
                    "fn_text": "*Vivamus sodales fermentum lorem, consectetur mollis lacus sollicitudin quis",
                    "fn_title": None,
                    "fn_type": None,
                },
            }
        ]

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(item, obtained[i])

    def test_dtd_version(self):
        self.maxDiff = None
        xml_tree = etree.fromstring(
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'dtd-version="1.3" article-type="research-article" xml:lang="pt">'
            "<back>"
            "<fn-group>"
            "<title>Notas</title>"
            '<fn fn-type="conflict" id="fn01">'
            "<label>*</label>"
            "<p>Vivamus sodales fermentum lorem, consectetur mollis lacus sollicitudin quis</p>"
            "</fn>"
            "</fn-group>"
            "</back>"
            "</article>"
        )

        obtained = list(
            FnGroupValidation(
                xml_tree=xml_tree,
                rules={
                    "fn_dtd_version_error_level": "ERROR",
                },
            ).validate()
        )

        expected = [
            {
                "title": "dtd_version",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "research-article",
                "parent_lang": "pt",
                "item": "dtd_version",
                "sub_item": None,
                "validation_type": "exist",
                "response": "ERROR",
                "expected_value": '<fn fn-type="coi-statement">',
                "got_value": '<fn fn-type="conflict">',
                "message": 'Got <fn fn-type="conflict">, expected <fn fn-type="coi-statement">',
                "advice": "Replace conflict with coi-statement",
                "data": {
                    "fn_bold": None,
                    "fn_id": "fn01",
                    "fn_label": "*",
                    "fn_parent": "fn-group",
                    "fn_text": "*Vivamus sodales fermentum lorem, consectetur mollis lacus sollicitudin quis",
                    "fn_title": None,
                    "fn_type": "conflict",
                },
            }
        ]

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(item, obtained[i])
