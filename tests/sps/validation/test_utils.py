import unittest
from lxml import etree

from packtools.sps.utils import xml_utils
from packtools.sps.validation.utils import get_doi_information, is_valid_url_format, extract_urls_from_node


def _get_all_ext_links(xml_node):
    ext_links = []
    if xml_node.tag == 'ext-link':
        href = xml_node.attrib.get('href', None)
        if href:
            ext_links.append(href)
    for child in xml_node:
        ext_links.extend(_get_all_ext_links(child))

    return ext_links


class MyTestCase(unittest.TestCase):
    def test_get_doi_information(self):
        self.maxDiff = None
        expected = [
            {
                'authors': [
                    'Rossi, Luciano',
                    'Damaceno, Rafael J.P.',
                    'Freire, Igor L.',
                    'Bechara, Etelvino J.H.',
                    'Mena-Chalco, Jesús P.'
                ],
                'en': {
                    'doi': '10.1016/j.joi.2018.08.004',
                    'title': 'Topological metrics in academic genealogy graphs'
                }
            },
            {
                'authors': [
                    'Carlos de Carvalho, João'
                ],
                'en': {
                    'doi': '10.1590/2176-4573p59270',
                    'title': 'The Jewish Amazon by Moacyr Scliar: The Word of the Other as Affirmation of the '
                             'Noncoincidence of the Other in Oneself'},
                'pt': {
                    'doi': '10.1590/2176-4573p59270',
                    'title': 'A Amazônia judaica de Moacyr Scliar: a palavra alheia como afirmação da '
                             'não-coincidência do outro em si'
                }
            }
            ]

        dois = ["10.1016/j.joi.2018.08.004", "10.1590/2176-4573p59270"]

        for i, doi in enumerate(dois):
            with self.subTest(i):
                obtained = get_doi_information(doi)
                self.assertDictEqual(expected[i], obtained)

    def test_is_valid_url_format(self):
        self.maxDiff = None
        xml_tree = xml_utils.get_xml_tree('tests/samples/artigo-com-links-invalidos.xml')
        ext_links = _get_all_ext_links(xml_tree)

        obtained = [
            (link, is_valid_url_format(link))
            for link in ext_links
        ]

        expected = [
            ('Disponible%20en%3A%20http%3A//bvs.sld.cu/aci/vol10_6_01/aci030602.htm', False),
            ('%3A%20http%3A//www.informaticamedica.org.ar', False),
            ('http://www.informaticamedica.org.ar', True),
            ('http://www.thejcdp.com/issue008/day/index_nlm.htm', True),
            ('http://bvs.sld.cu/revistas/aci/vol10_5_02/aci050502.htm%20%5B', True),
            ('http://db.doyma.es/pdf/27/27v29n4a13027627pdf001.pdf%20%5B', True),
            ('http://www.jamia.org/cgi/content/full/9/1/73%20%5B', True),
            ('http://bmj.com/cgi/content/full/317/7171/1496%20%5B', True),
            ('Disponible%20en%3A%20http%3A//www.informaticamedica.com.ar.', False),
            ('http://www.jmir.org. [', False),
            ('http://www.ama-assn.org/pub/category/1905.html%20%5B', True),
            ('http://www.doc6.es/iwe%20%5B', True),
            ('Disponible%20en%3A%20http%3A//www.doc6.es/iwe%20%5B', False),
            ('http://www.doc6.es/iwe', True),
            ('http://www.ub.es/bid/06frang2.htm', True),
            ('http://bvs.sld.cu/revistas/aci/vol8_2_00/aci10200.html', True)
        ]

        self.assertEqual(obtained, expected)

    def test_extract_url_from_node(self):
        xml_data = '''
        <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink" 
        article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
            <front>
                <article-meta>
                    <permissions>
                        <license license-type="open-access" xlink:href="https://creativecommons.org/licenses/by/4.0/" xml:lang="en">
                            <license-p>This is an Open Access article distributed under the terms of the Creative Commons Attribution License, which permits unrestricted use, distribution, and reproduction in any medium, provided the original work is properly cited.</license-p>
                        </license>
                    </permissions>
                </article-meta>
            </front>
            <body>
                <sec sec-type="results">
                    <p>
                        <fig id="f1">
                            <alternatives>
                                <graphic xlink:href=""/>
                                <graphic xlink:href="https://minio.scielo.br/documentstore/1518-8345/TPg77CCrGj4wcbLCh9vG8bS/93646bf6194a04743642b91240adef621257b46f.jpg"/>
                            </alternatives>
                        </fig>
                    </p>
                </sec>
            </body>
            <back>
                <ref-list>
                    <ref id="B1">
                    <comment>Disponible en: <ext-link ext-link-type="uri" xlink:href="https://hdl.handle.net/11441/69000">https://hdl.handle.net/11441/69000</ext-link>
                    </comment>
                    </ref>
                </ref-list>
            </back>
        </article>
        '''
        xml_tree = etree.fromstring(xml_data)

        # Teste para o nó raiz
        url = extract_urls_from_node(xml_tree)
        self.assertEqual(
            url,
            {
                "license": ["https://creativecommons.org/licenses/by/4.0/"],
                "graphic": ["https://minio.scielo.br/documentstore/1518-8345/TPg77CCrGj4wcbLCh9vG8bS/93646bf6194a04743642b91240adef621257b46f.jpg"],
                "ext-link": ["https://hdl.handle.net/11441/69000"]
            }
        )

        # Teste para o nó <license>
        node_license = xml_tree.xpath(".//license")[0]
        url = extract_urls_from_node(node_license)
        self.assertEqual(
            url,
            {"license": ["https://creativecommons.org/licenses/by/4.0/"]}
        )

        # Teste para o nó <graphic> com a imagem
        node_graphic = xml_tree.xpath(".//graphic")[1]
        url = extract_urls_from_node(node_graphic)
        self.assertEqual(
            url,
            {"graphic": ["https://minio.scielo.br/documentstore/1518-8345/TPg77CCrGj4wcbLCh9vG8bS/93646bf6194a04743642b91240adef621257b46f.jpg"]}
        )

        # Teste para o nó <ext-link>
        node_ext_link = xml_tree.xpath(".//ext-link")[0]
        url = extract_urls_from_node(node_ext_link)
        self.assertEqual(
            url,
            {"ext-link": ["https://hdl.handle.net/11441/69000"]}
        )


if __name__ == '__main__':
    unittest.main()
