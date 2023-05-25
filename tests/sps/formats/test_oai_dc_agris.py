import unittest
from unittest.mock import patch

from lxml import etree as ET
from packtools.sps.utils import xml_utils
from packtools.sps.models.dates import ArticleDates
from packtools.sps.formats.oai_dc_agris import (
    xml_oai_dc_agris_record_pipe,
    xml_oai_dc_agris_header_pipe,
    get_identifier,
    add_identifier,
    add_set_spec,
    get_issn,
    xml_oai_dc_agris_metadata_pipe,
    xml_oai_dc_agris_resouce_pipe,
    xml_oai_dc_agris_title_pipe,
    xml_oai_dc_agris_creator_pipe,
    xml_oai_dc_agris_publisher_pipe,
    xml_oai_dc_agris_date_pipe,
    xml_oai_dc_agris_subject_pipe,
    xml_oai_dc_agris_description_pipe,
    xml_oai_dc_agris_identifier_pipe,
    xml_oai_dc_agris_type_pipe,
    xml_oai_dc_agris_format_pipe,
    xml_oai_dc_agris_language_pipe,
    xml_oai_dc_agris_availability_pipe,
    xml_oai_dc_agris_citation_pipe,
)


class TestPipelineOaiDcAgris(unittest.TestCase):
    def test_xml_oai_dc_agris_record_pipe(self):
        expected = (
            '<record/>'
        )

        xml_oai_dc_agris = xml_oai_dc_agris_record_pipe()

        self.obtained = ET.tostring(xml_oai_dc_agris, encoding="utf-8").decode("utf-8")

        self.assertIn(expected, self.obtained)

