from unittest import TestCase
from lxml import etree

from packtools.sps.validation.article_license import ArticleLicenseValidation


class ArticleLicenseValidationTest(TestCase):
    def setUp(self):
        self.xmltree = etree.fromstring(
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
        self.article_license = ArticleLicenseValidation(self.xmltree)

    def test_validate_license_ok(self):
        expected = {
            "obtained_value": [
                {
                    'text': 'This is an article published in open access under a Creative Commons license.',
                    'lang': 'en'
                },
                {
                    'text': 'Este é um artigo publicado em acesso aberto sob uma licença Creative Commons.',
                    'lang': 'pt'
                },
                {
                    'text': 'Este es un artículo publicado en acceso abierto bajo una licencia Creative Commons.',
                    'lang': 'es'
                }
            ],
            "expected_value": [
                {
                    'text': 'This is an article published in open access under a Creative Commons license.',
                    'lang': 'en'
                },
                {
                    'text': 'Este é um artigo publicado em acesso aberto sob uma licença Creative Commons.',
                    'lang': 'pt'
                },
                {
                    'text': 'Este es un artículo publicado en acceso abierto bajo una licencia Creative Commons.',
                    'lang': 'es'
                }
            ],
            "result": "ok"
        }
        obtained = self.article_license.validate_license(
            [
                {
                    'text': 'This is an article published in open access under a Creative Commons license.',
                    'lang': 'en'
                },
                {
                    'text': 'Este é um artigo publicado em acesso aberto sob uma licença Creative Commons.',
                    'lang': 'pt'
                },
                {
                    'text': 'Este es un artículo publicado en acceso abierto bajo una licencia Creative Commons.',
                    'lang': 'es'
                }
            ]
        )
        self.assertEqual(expected, obtained)

    def test_validate_license_not_ok(self):
        expected = {
            "obtained_value": [
                {
                    'text': 'This is an article published in open access under a Creative Commons license.',
                    'lang': 'en'
                },
                {
                    'text': 'Este é um artigo publicado em acesso aberto sob uma licença Creative Commons.',
                    'lang': 'pt'
                },
                {
                    'text': 'Este es un artículo publicado en acceso abierto bajo una licencia Creative Commons.',
                    'lang': 'es'
                }
            ],
            "expected_value": [
                {
                    'text': 'Este é um artigo publicado em acesso aberto sob uma licença Creative Commons.',
                    'lang': 'pt'
                },
            ],
            "result": "error",
            "message": "the license text does not match the license text adopted by the journal"
        }
        obtained = self.article_license.validate_license(
            [
               {
                    'text': 'Este é um artigo publicado em acesso aberto sob uma licença Creative Commons.',
                    'lang': 'pt'
                }
            ]
        )
        self.assertEqual(expected, obtained)

    def test_validate_license_code_ok(self):
        expected = {
            "obtained_value": ['4.0', '4.0', '4.0'],
            "expected_value": ['4.0', '4.0', '4.0'],
            "result": "ok"
        }
        obtained = self.article_license.validate_license_code(
            ['4.0', '4.0', '4.0']
        )
        self.assertEqual(expected, obtained)

    def test_validate_license_code_not_ok(self):
        expected = {
            "obtained_value": ['4.0', '4.0', '4.0'],
            "expected_value": ['4.0', '4.0'],
            "result": "error",
            "message": "the license codes provided do not match the ones found"
        }
        obtained = self.article_license.validate_license_code(
            ['4.0', '4.0']
        )
        self.assertEqual(expected, obtained)
