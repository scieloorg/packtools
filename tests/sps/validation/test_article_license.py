from unittest import TestCase
from lxml import etree

from packtools.sps.validation.article_license import ArticleLicenseValidation


class ArticleLicenseValidationTest(TestCase):
    def test_validate_license_3_expected_3_obtained_ok(self):
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
        expected = {
            "obtained_value": {
                'en': {
                    'lang': 'en',
                    'link': 'http://creativecommons.org/licenses/by/4.0/',
                    'licence_p': 'This is an article published in open access under a Creative Commons license.'
                    },
                'pt': {
                    'lang': 'pt',
                    'link': 'http://creativecommons.org/licenses/by/4.0/',
                    'licence_p': 'Este é um artigo publicado em acesso aberto sob uma licença Creative Commons.'
                    },
                'es': {
                    'lang': 'es',
                    'link': 'http://creativecommons.org/licenses/by/4.0/',
                    'licence_p': 'Este es un artículo publicado en acceso abierto bajo una licencia Creative Commons.'
                    }
            },
            "expected_value": {
                'en': {
                    'lang': 'en',
                    'link': 'http://creativecommons.org/licenses/by/4.0/',
                    'licence_p': 'This is an article published in open access under a Creative Commons license.'
                    },
                'pt': {
                    'lang': 'pt',
                    'link': 'http://creativecommons.org/licenses/by/4.0/',
                    'licence_p': 'Este é um artigo publicado em acesso aberto sob uma licença Creative Commons.'
                    },
                'es': {
                    'lang': 'es',
                    'link': 'http://creativecommons.org/licenses/by/4.0/',
                    'licence_p': 'Este es un artículo publicado en acceso abierto bajo una licencia Creative Commons.'
                    }
            },
            "result": "ok",
            "message": [
                'ok, the license text for en does match the license text adopted by the journal',
                'ok, the license text for pt does match the license text adopted by the journal',
                'ok, the license text for es does match the license text adopted by the journal'
            ]
        }
        obtained = self.article_license.validate_license(
            {
                'en': {
                    'lang': 'en',
                    'link': 'http://creativecommons.org/licenses/by/4.0/',
                    'licence_p': 'This is an article published in open access under a Creative Commons license.'
                },
                'pt': {
                    'lang': 'pt',
                    'link': 'http://creativecommons.org/licenses/by/4.0/',
                    'licence_p': 'Este é um artigo publicado em acesso aberto sob uma licença Creative Commons.'
                },
                'es': {
                    'lang': 'es',
                    'link': 'http://creativecommons.org/licenses/by/4.0/',
                    'licence_p': 'Este es un artículo publicado en acceso abierto bajo una licencia Creative Commons.'
                }
            }
        )
        self.assertEqual(expected, obtained)

    def test_validate_license_3_expected_1_obtained_ok(self):
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
        expected = {
            "obtained_value": {
                'en': {
                    'lang': 'en',
                    'link': 'http://creativecommons.org/licenses/by/4.0/',
                    'licence_p': 'This is an article published in open access under a Creative Commons license.'
                }
            },
            "expected_value": {
                'en': {
                    'lang': 'en',
                    'link': 'http://creativecommons.org/licenses/by/4.0/',
                    'licence_p': 'This is an article published in open access under a Creative Commons license.'
                },
                'pt': {
                    'lang': 'pt',
                    'link': 'http://creativecommons.org/licenses/by/4.0/',
                    'licence_p': 'Este é um artigo publicado em acesso aberto sob uma licença Creative Commons.'
                },
                'es': {
                    'lang': 'es',
                    'link': 'http://creativecommons.org/licenses/by/4.0/',
                    'licence_p': 'Este es un artículo publicado en acceso abierto bajo una licencia Creative Commons.'
                }
            },
            "result": "ok",
            "message": [
                'ok, the license text for en does match the license text adopted by the journal'
            ]
        }
        obtained = self.article_license.validate_license(
            {
                'en': {
                    'lang': 'en',
                    'link': 'http://creativecommons.org/licenses/by/4.0/',
                    'licence_p': 'This is an article published in open access under a Creative Commons license.'
                },
                'pt': {
                    'lang': 'pt',
                    'link': 'http://creativecommons.org/licenses/by/4.0/',
                    'licence_p': 'Este é um artigo publicado em acesso aberto sob uma licença Creative Commons.'
                },
                'es': {
                    'lang': 'es',
                    'link': 'http://creativecommons.org/licenses/by/4.0/',
                    'licence_p': 'Este es un artículo publicado en acceso abierto bajo una licencia Creative Commons.'
                }
            }
        )
        self.assertEqual(expected, obtained)

    def test_validate_license_3_expected_3_obtained_not_ok(self):
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
        expected = {
            "obtained_value": {
                'en': {
                    'lang': 'en',
                    'link': 'http://creativecommons.org/licenses/by/4.0/',
                    'licence_p': 'This is an article published in open access under a Creative Commons license.'
                    },
                'pt': {
                    'lang': 'pt',
                    'link': 'http://creativecommons.org/licenses/by/4.0/',
                    'licence_p': 'Este é um artigo publicado em acesso aberto sob uma licença Creative Commons.'
                    },
                'es': {
                    'lang': 'es',
                    'link': 'http://creativecommons.org/licenses/by/4.0/',
                    'licence_p': 'Este es un artículo publicado en acceso abierto bajo una licencia Creative Commons.'
                    }
            },
            "expected_value": {
                'pt': {
                    'lang': 'pt',
                    'link': 'http://creativecommons.org/licenses/by/4.0/',
                    'licence_p': 'Este é um artigo publicado em acesso aberto sob uma licença Creative Commons.'
                    },
                'es': {
                    'lang': 'es',
                    'link': 'http://creativecommons.org/licenses/by/4.0/',
                    'licence_p': 'Este es un artículo publicado en acceso abierto bajo una licencia Creative Commons.'
                    }
            },
            "result": "error",
            "message": [
                'error, the language en is not foreseen by the journal',
                'ok, the license text for pt does match the license text adopted by the journal',
                'ok, the license text for es does match the license text adopted by the journal'
            ]
        }
        obtained = self.article_license.validate_license(
            {
                'pt': {
                    'lang': 'pt',
                    'link': 'http://creativecommons.org/licenses/by/4.0/',
                    'licence_p': 'Este é um artigo publicado em acesso aberto sob uma licença Creative Commons.'
                },
                'es': {
                    'lang': 'es',
                    'link': 'http://creativecommons.org/licenses/by/4.0/',
                    'licence_p': 'Este es un artículo publicado en acceso abierto bajo una licencia Creative Commons.'
                }
            }
        )
        self.assertEqual(expected, obtained)

    def test_validate_license_3_expected_1_obtained_not_ok(self):
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
        expected = {
            "obtained_value": {
                'en': {
                    'lang': 'en',
                    'link': 'http://creativecommons.org/licenses/by/4.0/',
                    'licence_p': 'This is an article published in open access under a Creative Commons license.'
                    }
            },
            "expected_value": {
                'pt': {
                    'lang': 'pt',
                    'link': 'http://creativecommons.org/licenses/by/4.0/',
                    'licence_p': 'Este é um artigo publicado em acesso aberto sob uma licença Creative Commons.'
                    },
                'es': {
                    'lang': 'es',
                    'link': 'http://creativecommons.org/licenses/by/4.0/',
                    'licence_p': 'Este es un artículo publicado en acceso abierto bajo una licencia Creative Commons.'
                    }
            },
            "result": "error",
            "message": [
                'error, the language en is not foreseen by the journal'
            ]
        }
        obtained = self.article_license.validate_license(
            {
                'pt': {
                    'lang': 'pt',
                    'link': 'http://creativecommons.org/licenses/by/4.0/',
                    'licence_p': 'Este é um artigo publicado em acesso aberto sob uma licença Creative Commons.'
                },
                'es': {
                    'lang': 'es',
                    'link': 'http://creativecommons.org/licenses/by/4.0/',
                    'licence_p': 'Este es un artículo publicado en acceso abierto bajo una licencia Creative Commons.'
                }
            }
        )
        self.assertEqual(expected, obtained)

    def test_validate_license_code_ok(self):
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
                "obtained_value": ('by', '4.0'),
                "expected_value": ('by', '4.0'),
                "result": "ok"
            },
            {
                "obtained_value": ('by', '4.0'),
                "expected_value": ('by', '4.0'),
                "result": "ok"
            },
            {
                "obtained_value": ('by', '4.0'),
                "expected_value": ('by', '4.0'),
                "result": "ok"
            },
            ]
        obtained = self.article_license.validate_license_code(
            'by', '4.0'
        )
        self.assertEqual(expected, obtained)

    def test_validate_license_code_not_ok(self):
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
                "obtained_value": (),
                "expected_value": ('by', '3.0'),
                "result": "error",
                "message": "the license code provided do not match the ones found"
            },
            {
                "obtained_value": (),
                "expected_value": ('by', '3.0'),
                "result": "error",
                "message": "the license code provided do not match the ones found"
            },
            {
                "obtained_value": (),
                "expected_value": ('by', '3.0'),
                "result": "error",
                "message": "the license code provided do not match the ones found"
            },
            ]
        obtained = self.article_license.validate_license_code(
            'by', '3.0'
        )
        self.assertEqual(expected, obtained)
