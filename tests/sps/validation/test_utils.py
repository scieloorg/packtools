import unittest
from unittest import skip
from unittest.mock import patch

from packtools.sps.validation.utils import (
    get_doi_information,
    handle_doi_response,
    is_valid_url_format,
)
from packtools.sps.utils import xml_utils


class MyTestCase(unittest.TestCase):
    @patch("packtools.sps.validation.utils.fetch_data")
    def test_get_doi_information(self, mock_fetch_data):
        doi = "10.1016/j.joi.2018.08.004"
        expected = {
            "status": "ok",
            "message": {
                "DOI": doi,
                "title": [
                    "Topological metrics in academic genealogy graphs"
                ],
            },
        }
        mock_fetch_data.return_value = expected

        obtained = get_doi_information(doi)

        self.assertEqual(expected, obtained)
        mock_fetch_data.assert_called_once_with(
            url=f"https://api.crossref.org/works/{doi}",
            json=True,
        )

    def test_handle_doi_response(self):
        item = {
            "title": ["English title"],
            "original-title": ["Título original"],
            "author": [
                {
                    "family": "Rossi",
                    "given": "Luciano",
                },
                {
                    "family": "Damaceno",
                    "given": "Rafael J.P.",
                },
            ],
        }

        obtained = handle_doi_response(item)

        self.assertEqual(
            {
                "titles": ["English title"],
                "original_titles": ["Título original"],
                "all_titles": ["English title", "Título original"],
                "authors": [
                    "Rossi, Luciano",
                    "Damaceno, Rafael J.P.",
                ],
            },
            obtained,
        )

    @patch("packtools.sps.validation.utils.fetch_data")
    def test_get_doi_information_request_error(self, mock_fetch_data):
        mock_fetch_data.side_effect = RuntimeError("Crossref unavailable")

        obtained = get_doi_information("10.1234/example")

        self.assertEqual(
            {
                "exception_msg": "Crossref unavailable",
                "exception_type": "<class 'RuntimeError'>",
            },
            obtained,
        )

    @skip("Teste pendente de correção e/ou ajuste")
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
