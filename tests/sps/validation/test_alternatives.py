from lxml import etree
from unittest import TestCase

from packtools.sps.validation.alternatives import AlternativesValidation
from packtools.sps.validation.exceptions import ValidationAlternativesException


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
                </article>
                """
        )
        params = {
            "table-wrap": ["graphic", "table"],
            "fig": ["graphic", "media"]
        }
        obtained = AlternativesValidation(self.xmltree, params)
        with self.assertRaises(ValidationAlternativesException) as context:
            next(obtained.validation())
        self.assertEqual("Tag inline-formula is not provided in the function parameters", str(context.exception))
