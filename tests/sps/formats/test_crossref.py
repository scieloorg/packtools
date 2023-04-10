from packtools.sps.formats.crossref import (
    pipeline_crossref,
    setupdoibatch_pipe,
    xml_head_pipe,
    xml_doibatchid_pipe,
    xml_timestamp_pipe,
    xml_depositor_pipe,
    xml_registrant_pipe,
    xml_body_pipe,
    xml_journal_pipe,
    xml_journalmetadata_pipe,
    xml_journaltitle_pipe,
    xml_abbreviatedjournaltitle_pipe,
    xml_issn_pipe,
    xml_journalissue_pipe,
    xml_pubdate_pipe,
    xml_journalvolume_pipe,
    xml_volume_pipe,
    xml_issue_pipe,

)
from unittest import TestCase
from lxml import etree as ET


class PipelineCrossref(TestCase):

    def test_setupdoibatch_pipe(self):
        expected = (
            '<doi_batch xmlns:ai="http://www.crossref.org/AccessIndicators.xsd" '
            'xmlns:jats="http://www.ncbi.nlm.nih.gov/JATS1" '
            'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" version="4.4.0" '
            'xmlns="http://www.crossref.org/schema/4.4.0" '
            'xsi:schemaLocation="http://www.crossref.org/schema/4.4.0 '
            'http://www.crossref.org/schemas/crossref4.4.0.xsd"/>'
        )

        result = setupdoibatch_pipe()
        obtained = ET.tostring(result, encoding="utf-8").decode("utf-8")

        self.assertEqual(expected, obtained)

    def test_xmlhead_pipe(self):
        xml_crossref = setupdoibatch_pipe()
        xml_head_pipe(xml_crossref)

        self.assertIsNotNone(xml_crossref.find('head'))

    def test_xml_doibatchid_pipe(self):
        expected = (
            "<head>"
            "<doi_batch_id>49d374553c5d48c0bdd54d25080e0045</doi_batch_id>"
            "</head>"
        )

        data = {
            "doi_batch_id": "49d374553c5d48c0bdd54d25080e0045"
        }

        xml_crossref = setupdoibatch_pipe()
        xml_head_pipe(xml_crossref)
        xml_doibatchid_pipe(xml_crossref, data)

        self.obtained = ET.tostring(xml_crossref, encoding="utf-8").decode("utf-8")

        self.assertIn(expected, self.obtained)

    def test_xml_timestamp_pipe(self):
        expected = (
            "<head>"
            "<timestamp>20230405112328</timestamp>"
            "</head>"
        )

        data = {
            "timestamp": "20230405112328"
        }

        xml_crossref = setupdoibatch_pipe()
        xml_head_pipe(xml_crossref)
        xml_timestamp_pipe(xml_crossref, data)

        self.obtained = ET.tostring(xml_crossref, encoding="utf-8").decode("utf-8")

        self.assertIn(expected, self.obtained)

    def test_xml_depositor_pipe(self):
        expected = (
            "<head>"
            "<depositor>"
            "<depositor_name>depositor</depositor_name>"
            "<email_address>name@domain.com</email_address>"
            "</depositor>"
            "</head>"
        )

        data = {
            "depositor_name": "depositor",
            "depositor_email_address": "name@domain.com"
        }

        xml_crossref = setupdoibatch_pipe()
        xml_head_pipe(xml_crossref)
        xml_depositor_pipe(xml_crossref, data)

        self.obtained = ET.tostring(xml_crossref, encoding="utf-8").decode("utf-8")

        self.assertIn(expected, self.obtained)

    def test_xml_registrant_pipe(self):
        expected = (
            "<head>"
            "<registrant>registrant</registrant>"
            "</head>"
        )

        data = {
            "registrant": "registrant"
        }

        xml_crossref = setupdoibatch_pipe()
        xml_head_pipe(xml_crossref)
        xml_registrant_pipe(xml_crossref, data)

        self.obtained = ET.tostring(xml_crossref, encoding="utf-8").decode("utf-8")

        self.assertIn(expected, self.obtained)

    def test_xml_body_pipe(self):
        xml_crossref = setupdoibatch_pipe()
        xml_body_pipe(xml_crossref)

        self.assertIsNotNone(xml_crossref.find('body'))

    def test_xml_journal_pipe(self):
        xml_crossref = setupdoibatch_pipe()
        xml_body_pipe(xml_crossref)
        xml_journal_pipe(xml_crossref)

        self.assertIsNotNone(xml_crossref.find('./body/journal'))

