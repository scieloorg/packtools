from unittest import TestCase

from lxml import etree

from packtools.sps.models.article_license import ArticleLicense


class ArticleLicenseTest(TestCase):
    def setUp(self):
        xml = ("""
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
                """)
        xmltree = etree.fromstring(xml)
        self.article_license = ArticleLicense(xmltree)

    def test_get_licenses(self):
        expected = [
            {
                'lang': 'en',
                'link': 'http://creativecommons.org/licenses/by/4.0/',
                'licence_p': 'This is an article published in open access under a Creative Commons license.'
            },
            {
                'lang': 'pt',
                'link': 'http://creativecommons.org/licenses/by/4.0/',
                'licence_p': 'Este é um artigo publicado em acesso aberto sob uma licença Creative Commons.'
            },
            {
                'lang': 'es',
                'link': 'http://creativecommons.org/licenses/by/4.0/',
                'licence_p': 'Este es un artículo publicado en acceso abierto bajo una licencia Creative Commons.'
            }
        ]

        self.assertEqual(expected, self.article_license.licenses)

    def test_get_license_p(self):
        expected = {
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

        self.assertEqual(expected, self.article_license.licenses_by_lang)
