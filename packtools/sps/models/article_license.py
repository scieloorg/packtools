"""
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
"""


class ArticleLicense:
    def __init__(self, xmltree):
        self.xmltree = xmltree

    @property
    def link(self):
        _links = []
        for _link in self.xmltree.xpath('//article-meta//permissions//license'):
            d = {
                'text': _link.attrib.get('{http://www.w3.org/1999/xlink}href'),
                'lang': _link.attrib.get('{http://www.w3.org/XML/1998/namespace}lang')
            }
            _links.append(d)
        return _links

    @property
    def license_p(self):
        _licenses = []
        for _license in self.xmltree.xpath('//article-meta//permissions//license'):
            d = {
                'text': _license.find('license-p').text,
                'lang': _license.attrib.get('{http://www.w3.org/XML/1998/namespace}lang')
            }
            _licenses.append(d)
        return _licenses
