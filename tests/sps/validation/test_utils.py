import unittest

from packtools.sps.validation.utils import get_doi_information, is_valid_url_format
from packtools.sps.utils import xml_utils


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

        ext_links = xml_tree.xpath('.//*[@href]')

        obtained = [
            (link.get('href'), is_valid_url_format(link.get('href')))
            for link in ext_links
        ]

        expected = [
            ('http://creativecommons.org/licenses/by-nc/4.0/', True),
            ('http://scielo.sld.cu/scielo.php?script=sci_issuetoc&pid=1024-943520030005&lng=en', True),
            ('http://scielo.sld.cu/scielo.php?script=sci_serial&pid=1024-9435&lng=en', True),
            ('http://scielo.sld.cu/scielo.php?script=sci_arttext&pid=S1024-94352003000500002&lng=en&tlng=en', True),
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


if __name__ == '__main__':
    unittest.main()
