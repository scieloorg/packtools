from unittest import TestCase
from packtools.sps.models import sps_package
from packtools.sps import sps_maker

import zipfile


class Test_get_xml_uri_and_name(TestCase):

    def test__get_xml_uri_and_name(self):
        xml_sps = sps_package.SPS_Package("./tests/sps/fixtures/document2.xml")
        xml_uri = 'https://kernel.scielo.br/documents/ywDM7t6mxHzCRWp7kGF9rXQ'
        
        xml_uri_and_name = sps_maker._get_xml_uri_and_name(xml_sps, xml_uri)
        expected = {'name': '1414-431X-bjmbr-54-10-e11439.xml', 'uri': 'https://kernel.scielo.br/documents/ywDM7t6mxHzCRWp7kGF9rXQ'}

        self.assertDictEqual(expected, xml_uri_and_name)
