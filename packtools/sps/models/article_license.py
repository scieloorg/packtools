from ..utils import xml_utils

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

    def licenses(self,
                 tags_to_keep=None,
                 tags_to_keep_with_content=None,
                 tags_to_remove_with_content=None,
                 tags_to_convert_to_html=None,
                 ):
        _licenses = []
        for _license in self.xmltree.xpath('//article-meta//permissions//license'):
            _license_p = _license.find('license-p')
            if _license_p is not None:
                _licenses.append(
                    {
                        'lang': _license.attrib.get('{http://www.w3.org/XML/1998/namespace}lang'),
                        'link': _license.attrib.get('{http://www.w3.org/1999/xlink}href'),
                        'license_p': {
                            'plain_text': xml_utils.node_plain_text(_license_p),
                            'xml_format': xml_utils.node_text_without_xref(_license_p),
                            'html_format': xml_utils.process_subtags(_license_p, tags_to_keep,
                                                                     tags_to_keep_with_content,
                                                                     tags_to_remove_with_content,
                                                                     tags_to_convert_to_html)
                        }
                    }
                )
        return _licenses

    def licenses_by_lang(self,
                         tags_to_keep=None,
                         tags_to_keep_with_content=None,
                         tags_to_remove_with_content=None,
                         tags_to_convert_to_html=None,
                         ):
        return {
            item['lang']: item
            for item in self.licenses(tags_to_keep=tags_to_keep, tags_to_keep_with_content=tags_to_keep_with_content,
                                      tags_to_remove_with_content=tags_to_remove_with_content,
                                      tags_to_convert_to_html=tags_to_convert_to_html)
        }
