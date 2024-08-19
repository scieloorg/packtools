import unittest

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


if __name__ == '__main__':
    unittest.main()
