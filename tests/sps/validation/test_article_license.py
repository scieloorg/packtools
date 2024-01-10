from unittest import TestCase
from lxml import etree

from packtools.sps.validation.article_license import ArticleLicenseValidation


class ArticleLicenseValidationTest(TestCase):
    def test_validate_license_3_expected_3_obtained_ok(self):
        self.maxDiff = None
        xmltree = etree.fromstring(
            """
            <article xmlns:xlink="http://www.w3.org/1999/xlink">
            <front>
            <article-meta>
                <permissions>
                    <license license-type="open-access" 
                    xlink:href="http://creativecommons.org/licenses/by/4.0/" 
                    xml:lang="en">
                        <license-p>This is an article published in open access under a Creative Commons license.</license-p>
                    </license>
                    <license license-type="open-access" 
                    xlink:href="http://creativecommons.org/licenses/by/4.0/" 
                    xml:lang="pt">
                        <license-p>Este é um artigo publicado em acesso aberto sob uma licença Creative Commons.</license-p>
                    </license>
                    <license license-type="open-access" 
                    xlink:href="http://creativecommons.org/licenses/by/4.0/" 
                    xml:lang="es">
                        <license-p>Este es un artículo publicado en acceso abierto bajo una licencia Creative Commons.</license-p>
                    </license>
                </permissions>
            </article-meta>
            </front>
            </article>
            """
        )
        self.article_license = ArticleLicenseValidation(xmltree)
        expected = [
            {
                'title': 'Article license validation',
                'xpath': './permissions//license',
                'validation_type': 'value',
                'response': 'OK',
                'expected_value': {
                    'lang': 'en',
                    'link': 'http://creativecommons.org/licenses/by/4.0/',
                    'license_p': 'This is an article published in open access under a Creative Commons license.'
                    },
                'got_value': {
                    'lang': 'en',
                    'link': 'http://creativecommons.org/licenses/by/4.0/',
                    'license_p': 'This is an article published in open access under a Creative Commons license.'
                    },
                'message': "Got {"
                           "'lang': 'en', "
                           "'link': 'http://creativecommons.org/licenses/by/4.0/', "
                           "'license_p': 'This is an article published in open access under a Creative Commons license.'"
                           "}, expected: {"
                           "'lang': 'en', "
                           "'link': 'http://creativecommons.org/licenses/by/4.0/', "
                           "'license_p': 'This is an article published in open access under a Creative Commons license.'"
                           "}",
                'advice': None
            },
            {
                'title': 'Article license validation',
                'xpath': './permissions//license',
                'validation_type': 'value',
                'response': 'OK',
                'expected_value': {
                    'lang': 'pt',
                    'link': 'http://creativecommons.org/licenses/by/4.0/',
                    'license_p': 'Este é um artigo publicado em acesso aberto sob uma licença Creative Commons.'
                },
                'got_value': {
                    'lang': 'pt',
                    'link': 'http://creativecommons.org/licenses/by/4.0/',
                    'license_p': 'Este é um artigo publicado em acesso aberto sob uma licença Creative Commons.'
                },
                'message': "Got {"
                           "'lang': 'pt', "
                           "'link': 'http://creativecommons.org/licenses/by/4.0/', "
                           "'license_p': 'Este é um artigo publicado em acesso aberto sob uma licença Creative Commons.'"
                           "}, expected: {"
                           "'lang': 'pt', "
                           "'link': 'http://creativecommons.org/licenses/by/4.0/', "
                           "'license_p': 'Este é um artigo publicado em acesso aberto sob uma licença Creative Commons.'"
                           "}",
                'advice': None
            },
            {
                'title': 'Article license validation',
                'xpath': './permissions//license',
                'validation_type': 'value',
                'response': 'OK',
                'expected_value': {
                    'lang': 'es',
                    'link': 'http://creativecommons.org/licenses/by/4.0/',
                    'license_p': 'Este es un artículo publicado en acceso abierto bajo una licencia Creative Commons.'
                },
                'got_value': {
                    'lang': 'es',
                    'link': 'http://creativecommons.org/licenses/by/4.0/',
                    'license_p': 'Este es un artículo publicado en acceso abierto bajo una licencia Creative Commons.'
                },
                'message': "Got {"
                           "'lang': 'es', "
                           "'link': 'http://creativecommons.org/licenses/by/4.0/', "
                           "'license_p': 'Este es un artículo publicado en acceso abierto bajo una licencia Creative Commons.'"
                           "}, expected: {"
                           "'lang': 'es', "
                           "'link': 'http://creativecommons.org/licenses/by/4.0/', "
                           "'license_p': 'Este es un artículo publicado en acceso abierto bajo una licencia Creative Commons.'"
                           "}",
                'advice': None
            },
        ]
        obtained = self.article_license.validate_license(
            {
                'en': {
                    'lang': 'en',
                    'link': 'http://creativecommons.org/licenses/by/4.0/',
                    'license_p': 'This is an article published in open access under a Creative Commons license.'
                },
                'pt': {
                    'lang': 'pt',
                    'link': 'http://creativecommons.org/licenses/by/4.0/',
                    'license_p': 'Este é um artigo publicado em acesso aberto sob uma licença Creative Commons.'
                },
                'es': {
                    'lang': 'es',
                    'link': 'http://creativecommons.org/licenses/by/4.0/',
                    'license_p': 'Este es un artículo publicado en acceso abierto bajo una licencia Creative Commons.'
                }
            }
        )
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

    def test_validate_license_3_expected_1_obtained_ok(self):
        self.maxDiff = None
        xmltree = etree.fromstring(
            """
            <article xmlns:xlink="http://www.w3.org/1999/xlink">
            <front>
            <article-meta>
                <permissions>
                    <license license-type="open-access" 
                    xlink:href="http://creativecommons.org/licenses/by/4.0/" 
                    xml:lang="en">
                        <license-p>This is an article published in open access under a Creative Commons license.</license-p>
                    </license>
                </permissions>
            </article-meta>
            </front>
            </article>
            """
        )
        self.article_license = ArticleLicenseValidation(xmltree)
        expected = [
            {
                'title': 'Article license validation',
                'xpath': './permissions//license',
                'validation_type': 'value',
                'response': 'OK',
                'expected_value': {
                    'lang': 'en',
                    'link': 'http://creativecommons.org/licenses/by/4.0/',
                    'license_p': 'This is an article published in open access under a Creative Commons license.'
                },
                'got_value': {
                    'lang': 'en',
                    'link': 'http://creativecommons.org/licenses/by/4.0/',
                    'license_p': 'This is an article published in open access under a Creative Commons license.'
                },
                'message': "Got {"
                           "'lang': 'en', "
                           "'link': 'http://creativecommons.org/licenses/by/4.0/', "
                           "'license_p': 'This is an article published in open access under a Creative Commons license.'"
                           "}, expected: {"
                           "'lang': 'en', "
                           "'link': 'http://creativecommons.org/licenses/by/4.0/', "
                           "'license_p': 'This is an article published in open access under a Creative Commons license.'"
                           "}",
                'advice': None
            },
        ]
        obtained = self.article_license.validate_license(
            {
                'en': {
                    'lang': 'en',
                    'link': 'http://creativecommons.org/licenses/by/4.0/',
                    'license_p': 'This is an article published in open access under a Creative Commons license.'
                },
                'pt': {
                    'lang': 'pt',
                    'link': 'http://creativecommons.org/licenses/by/4.0/',
                    'license_p': 'Este é um artigo publicado em acesso aberto sob uma licença Creative Commons.'
                },
                'es': {
                    'lang': 'es',
                    'link': 'http://creativecommons.org/licenses/by/4.0/',
                    'license_p': 'Este es un artículo publicado en acceso abierto bajo una licencia Creative Commons.'
                }
            }
        )
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

    def test_validate_license_3_expected_3_obtained_not_ok(self):
        self.maxDiff = None
        xmltree = etree.fromstring(
            """
            <article xmlns:xlink="http://www.w3.org/1999/xlink">
            <front>
            <article-meta>
                <permissions>
                    <license license-type="open-access" 
                    xlink:href="http://creativecommons.org/licenses/by/4.0/" 
                    xml:lang="en">
                        <license-p>This is an article published in open access under a Creative Commons license.</license-p>
                    </license>
                    <license license-type="open-access" 
                    xlink:href="http://creativecommons.org/licenses/by/4.0/" 
                    xml:lang="pt">
                        <license-p>Este é um artigo publicado em acesso aberto sob uma licença Creative Commons.</license-p>
                    </license>
                    <license license-type="open-access" 
                    xlink:href="http://creativecommons.org/licenses/by/4.0/" 
                    xml:lang="es">
                        <license-p>Este es un artículo publicado en acceso abierto bajo una licencia Creative Commons.</license-p>
                    </license>
                </permissions>
            </article-meta>
            </front>
            </article>
            """
        )
        self.article_license = ArticleLicenseValidation(xmltree)
        expected = [
            {
                'title': 'Article license validation',
                'xpath': './permissions//license',
                'validation_type': 'value',
                'response': 'ERROR',
                'expected_value': 'License data that matches the language en',
                'got_value': {
                    'lang': 'en',
                    'link': 'http://creativecommons.org/licenses/by/4.0/',
                    'license_p': 'This is an article published in open access under a Creative Commons license.'
                    },
                'message': "Got {"
                           "'lang': 'en', "
                           "'link': 'http://creativecommons.org/licenses/by/4.0/', "
                           "'license_p': 'This is an article published in open access under a Creative Commons license.'"
                           "}, expected: License data that matches the language en",
                'advice': 'Provide license data that is consistent with the language: en and standard adopted by the journal'
            },
            {
                'title': 'Article license validation',
                'xpath': './permissions//license',
                'validation_type': 'value',
                'response': 'OK',
                'expected_value': {
                    'lang': 'pt',
                    'link': 'http://creativecommons.org/licenses/by/4.0/',
                    'license_p': 'Este é um artigo publicado em acesso aberto sob uma licença Creative Commons.'
                },
                'got_value': {
                    'lang': 'pt',
                    'link': 'http://creativecommons.org/licenses/by/4.0/',
                    'license_p': 'Este é um artigo publicado em acesso aberto sob uma licença Creative Commons.'
                },
                'message': "Got {"
                           "'lang': 'pt', "
                           "'link': 'http://creativecommons.org/licenses/by/4.0/', "
                           "'license_p': 'Este é um artigo publicado em acesso aberto sob uma licença Creative Commons.'"
                           "}, expected: {"
                           "'lang': 'pt', "
                           "'link': 'http://creativecommons.org/licenses/by/4.0/', "
                           "'license_p': 'Este é um artigo publicado em acesso aberto sob uma licença Creative Commons.'"
                           "}",
                'advice': None
            },
            {
                'title': 'Article license validation',
                'xpath': './permissions//license',
                'validation_type': 'value',
                'response': 'OK',
                'expected_value': {
                    'lang': 'es',
                    'link': 'http://creativecommons.org/licenses/by/4.0/',
                    'license_p': 'Este es un artículo publicado en acceso abierto bajo una licencia Creative Commons.'
                },
                'got_value': {
                    'lang': 'es',
                    'link': 'http://creativecommons.org/licenses/by/4.0/',
                    'license_p': 'Este es un artículo publicado en acceso abierto bajo una licencia Creative Commons.'
                },
                'message': "Got {"
                           "'lang': 'es', "
                           "'link': 'http://creativecommons.org/licenses/by/4.0/', "
                           "'license_p': 'Este es un artículo publicado en acceso abierto bajo una licencia Creative Commons.'"
                           "}, expected: {"
                           "'lang': 'es', "
                           "'link': 'http://creativecommons.org/licenses/by/4.0/', "
                           "'license_p': 'Este es un artículo publicado en acceso abierto bajo una licencia Creative Commons.'"
                           "}",
                'advice': None
            },
        ]
        obtained = self.article_license.validate_license(
            {
                'pt': {
                    'lang': 'pt',
                    'link': 'http://creativecommons.org/licenses/by/4.0/',
                    'license_p': 'Este é um artigo publicado em acesso aberto sob uma licença Creative Commons.'
                },
                'es': {
                    'lang': 'es',
                    'link': 'http://creativecommons.org/licenses/by/4.0/',
                    'license_p': 'Este es un artículo publicado en acceso abierto bajo una licencia Creative Commons.'
                }
            }
        )
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

    def test_validate_license_3_expected_1_obtained_not_ok(self):
        self.maxDiff = None
        xmltree = etree.fromstring(
            """
            <article xmlns:xlink="http://www.w3.org/1999/xlink">
            <front>
            <article-meta>
                <permissions>
                    <license license-type="open-access" 
                    xlink:href="http://creativecommons.org/licenses/by/4.0/" 
                    xml:lang="en">
                        <license-p>This is an article published in open access under a Creative Commons license.</license-p>
                    </license>
                </permissions>
            </article-meta>
            </front>
            </article>
            """
        )
        self.article_license = ArticleLicenseValidation(xmltree)
        expected = [
            {
                'title': 'Article license validation',
                'xpath': './permissions//license',
                'validation_type': 'value',
                'response': 'ERROR',
                'expected_value': 'License data that matches the language en',
                'got_value': {
                    'lang': 'en',
                    'link': 'http://creativecommons.org/licenses/by/4.0/',
                    'license_p': 'This is an article published in open access under a Creative Commons license.'
                    },
                'message': "Got {"
                           "'lang': 'en', "
                           "'link': 'http://creativecommons.org/licenses/by/4.0/', "
                           "'license_p': 'This is an article published in open access under a Creative Commons license.'"
                           "}, expected: License data that matches the language en",
                'advice': 'Provide license data that is consistent with the language: en and standard adopted by the journal'
            },
        ]
        obtained = self.article_license.validate_license(
            {
                'pt': {
                    'lang': 'pt',
                    'link': 'http://creativecommons.org/licenses/by/4.0/',
                    'license_p': 'Este é um artigo publicado em acesso aberto sob uma licença Creative Commons.'
                },
                'es': {
                    'lang': 'es',
                    'link': 'http://creativecommons.org/licenses/by/4.0/',
                    'license_p': 'Este es un artículo publicado en acceso abierto bajo una licencia Creative Commons.'
                }
            }
        )
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

    def test_validate_license_code_ok(self):
        self.maxDiff = None
        xmltree = etree.fromstring(
            """
            <article xmlns:xlink="http://www.w3.org/1999/xlink">
            <front>
            <article-meta>
                <permissions>
                    <license license-type="open-access" 
                    xlink:href="http://creativecommons.org/licenses/by/4.0/" 
                    xml:lang="en">
                        <license-p>This is an article published in open access under a Creative Commons license.</license-p>
                    </license>
                    <license license-type="open-access" 
                    xlink:href="http://creativecommons.org/licenses/by/4.0/" 
                    xml:lang="pt">
                        <license-p>Este é um artigo publicado em acesso aberto sob uma licença Creative Commons.</license-p>
                    </license>
                    <license license-type="open-access" 
                    xlink:href="http://creativecommons.org/licenses/by/4.0/" 
                    xml:lang="es">
                        <license-p>Este es un artículo publicado en acceso abierto bajo una licencia Creative Commons.</license-p>
                    </license>
                </permissions>
            </article-meta>
            </front>
            </article>
            """
        )
        self.article_license = ArticleLicenseValidation(xmltree)
        expected = [
            {
                'title': 'Article license code validation',
                'xpath': './permissions//license',
                'validation_type': 'value',
                'response': 'OK',
                'expected_value': 'by',
                'got_value': 'by',
                'message': f"Got: by, expected: by",
                'advice': None
            },
            {
                'title': 'Article license code validation',
                'xpath': './permissions//license',
                'validation_type': 'value',
                'response': 'OK',
                'expected_value': 'by',
                'got_value': 'by',
                'message': f"Got: by, expected: by",
                'advice': None
            },
            {
                'title': 'Article license code validation',
                'xpath': './permissions//license',
                'validation_type': 'value',
                'response': 'OK',
                'expected_value': 'by',
                'got_value': 'by',
                'message': f"Got: by, expected: by",
                'advice': None
            },
            ]
        obtained = self.article_license.validate_license_code('by')
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

    def test_validate_license_code_not_ok(self):
        self.maxDiff = None
        xmltree = etree.fromstring(
            """
            <article xmlns:xlink="http://www.w3.org/1999/xlink">
            <front>
            <article-meta>
                <permissions>
                    <license license-type="open-access" 
                    xlink:href="http://creativecommons.org/licenses/by/4.0/" 
                    xml:lang="en">
                        <license-p>This is an article published in open access under a Creative Commons license.</license-p>
                    </license>
                    <license license-type="open-access" 
                    xlink:href="http://creativecommons.org/licenses/by/4.0/" 
                    xml:lang="pt">
                        <license-p>Este é um artigo publicado em acesso aberto sob uma licença Creative Commons.</license-p>
                    </license>
                    <license license-type="open-access" 
                    xlink:href="http://creativecommons.org/licenses/by/4.0/" 
                    xml:lang="es">
                        <license-p>Este es un artículo publicado en acceso abierto bajo una licencia Creative Commons.</license-p>
                    </license>
                </permissions>
            </article-meta>
            </front>
            </article>
            """
        )
        self.article_license = ArticleLicenseValidation(xmltree)
        expected = [
            {
                'title': 'Article license code validation',
                'xpath': './permissions//license',
                'validation_type': 'value',
                'response': 'ERROR',
                'expected_value': 'bye',
                'got_value': 'by',
                'message': f"Got: by, expected: bye",
                'advice': 'Provide bye code license information'
            },
            {
                'title': 'Article license code validation',
                'xpath': './permissions//license',
                'validation_type': 'value',
                'response': 'ERROR',
                'expected_value': 'bye',
                'got_value': 'by',
                'message': f"Got: by, expected: bye",
                'advice': 'Provide bye code license information'
            },
            {
                'title': 'Article license code validation',
                'xpath': './permissions//license',
                'validation_type': 'value',
                'response': 'ERROR',
                'expected_value': 'bye',
                'got_value': 'by',
                'message': f"Got: by, expected: bye",
                'advice': 'Provide bye code license information'
            },
            ]
        obtained = self.article_license.validate_license_code('bye')
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)
