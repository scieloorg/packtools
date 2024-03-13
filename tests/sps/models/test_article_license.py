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
                            <license-p><bold>This is an article</bold> published in open access under a Creative Commons license.</license-p>
                        </license>
                        <license license-type="open-access" 
                        xlink:href="http://creativecommons.org/licenses/by/4.0/" 
                        xml:lang="pt">
                            <license-p>Este é um artigo publicado <bold>em acesso aberto sob uma licença</bold> Creative Commons.</license-p>
                        </license>
                        <license license-type="open-access" 
                        xlink:href="http://creativecommons.org/licenses/by/4.0/" 
                        xml:lang="es">
                            <license-p>Este es un artículo publicado en acceso abierto bajo <bold>una <italic>licencia</italic> Creative</bold> Commons.</license-p>
                        </license>
                    </permissions>
                </article-meta>
                </front>
                </article>
                """)
        xmltree = etree.fromstring(xml)
        self.article_license = ArticleLicense(xmltree, tags_to_convert_to_html={'bold': 'b'})

    def test_get_licenses(self):
        self.maxDiff = None
        expected = [
            {
                'lang': 'en',
                'link': 'http://creativecommons.org/licenses/by/4.0/',
                'license_p': {
                    'plain_text': 'This is an article published in open access under a Creative Commons license.',
                    'text': '<bold>This is an article</bold> published in open access under a Creative Commons license.',
                    'html_text': '<b>This is an article</b> published in open access under a Creative Commons license.'
                }
            },
            {
                'lang': 'pt',
                'link': 'http://creativecommons.org/licenses/by/4.0/',
                'license_p': {
                    'plain_text': 'Este é um artigo publicado em acesso aberto sob uma licença Creative Commons.',
                    'text': 'Este é um artigo publicado <bold>em acesso aberto sob uma licença</bold> Creative Commons.',
                    'html_text': 'Este é um artigo publicado <b>em acesso aberto sob uma licença</b> Creative Commons.'
                }
            },
            {
                'lang': 'es',
                'link': 'http://creativecommons.org/licenses/by/4.0/',
                'license_p': {
                    'plain_text': 'Este es un artículo publicado en acceso abierto bajo una licencia Creative Commons.',
                    'text': 'Este es un artículo publicado en acceso abierto bajo <bold>una <italic>licencia</italic> Creative</bold> Commons.',
                    'html_text': 'Este es un artículo publicado en acceso abierto bajo <b>una <i>licencia</i> Creative</b> Commons.'
                }
            }
        ]

        self.assertEqual(expected, self.article_license.licenses)

    def test_get_license_p(self):
        self.maxDiff = None
        expected = {
            'en': {
                'lang': 'en',
                'link': 'http://creativecommons.org/licenses/by/4.0/',
                'license_p': {
                    'plain_text': 'This is an article published in open access under a Creative Commons license.',
                    'text': '<bold>This is an article</bold> published in open access under a Creative Commons license.',
                    'html_text': '<b>This is an article</b> published in open access under a Creative Commons license.'
                }
            },
            'pt': {
                'lang': 'pt',
                'link': 'http://creativecommons.org/licenses/by/4.0/',
                'license_p': {
                    'plain_text': 'Este é um artigo publicado em acesso aberto sob uma licença Creative Commons.',
                    'text': 'Este é um artigo publicado <bold>em acesso aberto sob uma licença</bold> Creative Commons.',
                    'html_text': 'Este é um artigo publicado <b>em acesso aberto sob uma licença</b> Creative Commons.'
                }
            },
            'es': {
                'lang': 'es',
                'link': 'http://creativecommons.org/licenses/by/4.0/',
                'license_p': {
                    'plain_text': 'Este es un artículo publicado en acceso abierto bajo una licencia Creative Commons.',
                    'text': 'Este es un artículo publicado en acceso abierto bajo <bold>una <italic>licencia</italic> Creative</bold> Commons.',
                    'html_text': 'Este es un artículo publicado en acceso abierto bajo <b>una <i>licencia</i> Creative</b> Commons.'
                }
            }
        }

        self.assertEqual(expected, self.article_license.licenses_by_lang)
