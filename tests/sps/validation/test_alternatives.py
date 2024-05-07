from lxml import etree
from unittest import TestCase

from packtools.sps.validation.alternatives import AlternativesValidation


class AlternativesValidationTest(TestCase):
    def test_validation_success(self):
        self.maxDiff = None
        self.xmltree = etree.fromstring(
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
        obtained = list(AlternativesValidation(self.xmltree, params).validation())
        expected = []
        self.assertListEqual(obtained, expected)

    def test_validation_children_fail(self):
        self.maxDiff = None
        self.xmltree = etree.fromstring(
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
        obtained = list(AlternativesValidation(self.xmltree, params).validation())
        expected = [
            {
                'title': 'Alternatives validation',
                'parent': 'article',
                'parent_id': None,
                'item': 'table-wrap',
                'sub_item': 'alternatives',
                'validation_type': 'value in list',
                'expected_value': ['graphic', 'table'],
                'got_value': ['p'],
                'response': 'ERROR',
                'message': "Got ['p'], expected ['graphic', 'table']",
                'advice': "Provide child tags according to the list: ['graphic', 'table']",
                'data': {
                    'alternative_children': ['p'],
                    'alternative_parent': 'table-wrap',
                    'parent': 'article',
                    'parent_id': None
                }
            },
            {
                'title': 'Alternatives validation',
                'parent': 'sub-article',
                'parent_id': 'TRen',
                'item': 'fig',
                'sub_item': 'alternatives',
                'validation_type': 'value in list',
                'expected_value': ['graphic', 'media'],
                'got_value': ['title', 'abstract'],
                'response': 'ERROR',
                'message': "Got ['title', 'abstract'], expected ['graphic', 'media']",
                'advice': "Provide child tags according to the list: ['graphic', 'media']",
                'data': {
                    'alternative_children': ['title', 'abstract'],
                    'alternative_parent': 'fig',
                    'parent': 'sub-article',
                    'parent_id': 'TRen'
                }
            }
        ]
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(item, obtained[i])

    def test_validation_parent_fail(self):
        self.maxDiff = None
        self.xmltree = etree.fromstring(
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
                    <sub-article article-type="translation" xml:lang="en" id="TRen">
                        <body>
                            <disp-formula>
                                <alternatives>
                                    <mml:math />
                                    <tex-math />
                                </alternatives>
                            </disp-formula>
                        </body>
                    </sub-article>
                </article>
                """
        )
        params = {
            "table-wrap": ["graphic", "table"],
            "fig": ["graphic", "media"]
        }
        obtained = list(AlternativesValidation(self.xmltree, params).validation())
        expected = [
            {
                'title': 'Alternatives validation',
                'parent': 'article',
                'parent_id': None,
                'item': 'inline-formula',
                'sub_item': 'alternatives',
                'validation_type': 'value in list',
                'expected_value': ['table-wrap', 'fig'],
                'got_value': 'inline-formula',
                'response': 'ERROR',
                'message': "Got inline-formula, expected ['table-wrap', 'fig']",
                'advice': "Provide parent tag according to the list: ['table-wrap', 'fig']",
                'data': {
                    'alternative_children': ['{http://www.w3.org/1998/Math/MathML}math', 'tex-math'],
                    'alternative_parent': 'inline-formula',
                    'parent': 'article',
                    'parent_id': None
                }
            },
            {
                'title': 'Alternatives validation',
                'parent': 'article',
                'parent_id': None,
                'item': 'inline-formula',
                'sub_item': 'alternatives',
                'validation_type': 'value in list',
                'expected_value': None,
                'got_value': ['{http://www.w3.org/1998/Math/MathML}math', 'tex-math'],
                'response': 'ERROR',
                'message': "Got ['{http://www.w3.org/1998/Math/MathML}math', 'tex-math'], expected None",
                'advice': 'Provide child tags according to the list: None',
                'data': {
                    'alternative_children': ['{http://www.w3.org/1998/Math/MathML}math', 'tex-math'],
                    'alternative_parent': 'inline-formula',
                    'parent': 'article',
                    'parent_id': None
                }
            }
        ]
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(item, obtained[i])