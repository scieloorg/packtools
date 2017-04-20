#coding: utf-8
from __future__ import unicode_literals
import unittest
import io
from tempfile import NamedTemporaryFile

from lxml import etree, isoschematron

from packtools import domain, style_errors, exceptions


# valid: <a><b></b></a>
# invalid: anything else
sample_xsd = io.BytesIO(b'''\
<xsd:schema xmlns:xsd="http://www.w3.org/2001/XMLSchema">
<xsd:element name="a" type="AType"/>
<xsd:complexType name="AType">
  <xsd:sequence>
    <xsd:element name="b" type="xsd:string" />
  </xsd:sequence>
</xsd:complexType>
</xsd:schema>
''')


sample_sch = io.BytesIO(b'''\
<schema xmlns="http://purl.oclc.org/dsdl/schematron">
  <pattern id="sum_equals_100_percent">
    <title>Sum equals 100%.</title>
    <rule context="Total">
      <assert test="sum(//Percent)=100">Element 'Total': Sum is not 100%.</assert>
    </rule>
  </pattern>
</schema>
''')


def setup_tmpfile(method):
    def wrapper(self):
        valid_tmpfile = NamedTemporaryFile()
        valid_tmpfile.write(b'<a><b>bar</b></a>')
        valid_tmpfile.seek(0)
        self.valid_tmpfile = valid_tmpfile

        method(self)

        self.valid_tmpfile.close()
    return wrapper


class XMLValidatorTests(unittest.TestCase):

    @setup_tmpfile
    def test_initializes_with_filepath(self):
        self.assertTrue(domain.XMLValidator.parse(self.valid_tmpfile.name, no_doctype=True, sps_version='sps-1.1'))

    def test_initializes_with_etree(self):
        fp = io.BytesIO(b'<a><b>bar</b></a>')
        et = etree.parse(fp)

        self.assertTrue(domain.XMLValidator.parse(et, no_doctype=True, sps_version='sps-1.1'))

    def test_missing_sps_version(self):
        fp = io.BytesIO(b'<a><b>bar</b></a>')
        et = etree.parse(fp)

        self.assertRaises(ValueError, 
                lambda: domain.XMLValidator.parse(et, no_doctype=True))

    def test_unknown_sps_version(self):
        fp = io.BytesIO(b'<a specific-use="unknown"><b>bar</b></a>')
        et = etree.parse(fp)

        self.assertRaises(ValueError, 
                lambda: domain.XMLValidator.parse(et, no_doctype=True))

    def test_sps_version_discovery(self):
        fp = io.BytesIO(b'<a specific-use="sps-1.1"><b>bar</b></a>')
        et = etree.parse(fp)

        self.assertTrue(domain.XMLValidator.parse(et, no_doctype=True,
            supported_sps_versions=['sps-1.1', 'sps-1.2']))

    def test_unsupported_sps_version(self):
        fp = io.BytesIO(b'<a specific-use="pre-sps"><b>bar</b></a>')
        et = etree.parse(fp)

        self.assertRaises(ValueError, 
                lambda: domain.XMLValidator.parse(et, no_doctype=True))

    def test_validation(self):
        fp = etree.parse(io.BytesIO(b'<a><b>bar</b></a>'))
        dtd = etree.XMLSchema(etree.parse(sample_xsd))
        xml = domain.XMLValidator.parse(fp, no_doctype=True,
                sps_version='sps-1.1', dtd=dtd)

        result, errors = xml.validate()
        self.assertTrue(result)
        self.assertFalse(errors)

    def test_invalid(self):
        fp = etree.parse(io.BytesIO(b'<a><c>bar</c></a>'))
        dtd = etree.XMLSchema(etree.parse(sample_xsd))
        xml = domain.XMLValidator.parse(fp, no_doctype=True,
                sps_version='sps-1.1', dtd=dtd)

        result, _ = xml.validate()
        self.assertFalse(result)

    def test_invalid_errors(self):
        # Default lxml error log.
        fp = etree.parse(io.BytesIO(b'<a><c>bar</c></a>'))
        dtd = etree.XMLSchema(etree.parse(sample_xsd))
        xml = domain.XMLValidator.parse(fp, no_doctype=True,
                sps_version='sps-1.1', dtd=dtd)

        _, errors = xml.validate()
        for error in errors:
            self.assertIsInstance(error, style_errors.StyleErrorBase)

    def test_annotate_errors(self):
        fp = etree.parse(io.BytesIO(b'<a><c>bar</c></a>'))
        dtd = etree.XMLSchema(etree.parse(sample_xsd))
        xml = domain.XMLValidator.parse(fp, no_doctype=True, 
                sps_version='sps-1.1', dtd=dtd)

        err_xml = xml.annotate_errors()
        xml_text = etree.tostring(err_xml)

        self.assertIn(u"<!--SPS-ERROR: Element 'c': This element is not expected. Expected is ( b ).-->", xml_text.decode())

    def test_validation_schematron(self):
        fp = etree.parse(io.BytesIO(b'<Total><Percent>70</Percent><Percent>30</Percent></Total>'))
        schema = domain.SchematronValidator(
                isoschematron.Schematron(etree.parse(sample_sch)))
        xml = domain.XMLValidator(fp, style_validators=[schema])

        is_valid, errors = xml.validate_style()
        self.assertTrue(is_valid)
        self.assertEqual(len(errors), 0)

    def test_invalid_schematron(self):
        fp = etree.parse(io.BytesIO(b'<Total><Percent>60</Percent><Percent>30</Percent></Total>'))
        schema = domain.SchematronValidator(
                isoschematron.Schematron(etree.parse(sample_sch)))
        xml = domain.XMLValidator(fp, style_validators=[schema])

        result, errors = xml.validate_style()
        self.assertFalse(result)
        self.assertTrue(errors)

    def test_annotate_errors_schematron(self):
        fp = etree.parse(io.BytesIO(b'<Total><Percent>60</Percent><Percent>30</Percent></Total>'))
        schema = domain.SchematronValidator(
                isoschematron.Schematron(etree.parse(sample_sch)))
        dtd = domain.DTDValidator(etree.XMLSchema(etree.parse(sample_xsd)))
        xml = domain.XMLValidator(fp, style_validators=[schema])

        err_xml = xml.annotate_errors()
        xml_text = etree.tostring(err_xml)

        self.assertIn(u"<!--SPS-ERROR: Element 'Total': Sum is not 100%.-->", xml_text.decode())

    def test_fails_without_doctype_declaration(self):
        fp = io.BytesIO(b'<a><b>bar</b></a>')
        et = etree.parse(fp)

        self.assertRaises(ValueError, lambda: domain.XMLValidator.parse(et, no_doctype=False))

    def test_checks_allowed_doctype_public_ids(self):
        # JATS 1.0
        fp = io.BytesIO(b'<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "JATS-journalpublishing1.dtd"><a><b>bar</b></a>')
        et = etree.parse(fp)

        self.assertTrue(domain.XMLValidator.parse(et, no_doctype=False, sps_version='sps-1.2'))

    def test_checks_pmc3_not_allowed_doctype_public_ids(self):
        # PMC 3.0
        fp = io.BytesIO(b'<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE article PUBLIC "-//NLM//DTD Journal Publishing DTD v3.0 20080202//EN" "journalpublishing3.dtd"><a><b>bar</b></a>')
        et = etree.parse(fp)

        self.assertRaises(exceptions.XMLDoctypeError,
                lambda: domain.XMLValidator.parse(et, no_doctype=False, sps_version='sps-1.2'))

    def test_checks_allowed_doctype_public_ids_sps1_1(self):
        # JATS 1.0
        fp = io.BytesIO(b'<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "JATS-journalpublishing1.dtd"><a><b>bar</b></a>')
        et = etree.parse(fp)

        self.assertTrue(domain.XMLValidator.parse(et, no_doctype=False, sps_version='sps-1.1'))

        #PMC 3.0
        fp = io.BytesIO(b'<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE article PUBLIC "-//NLM//DTD Journal Publishing DTD v3.0 20080202//EN" "journalpublishing3.dtd"><a><b>bar</b></a>')
        et = etree.parse(fp)

        self.assertTrue(domain.XMLValidator.parse(et, no_doctype=False, sps_version='sps-1.1'))

    def test_list_assets(self):
        fp = io.BytesIO(b"""<?xml version="1.0" encoding="UTF-8"?>
<article xmlns:xlink="http://www.w3.org/1999/xlink"
         dtd-version="1.0"
         article-type="research-article"
         xml:lang="en">
  <front>
    <article-meta>
      <supplementary-material mimetype="application"
                              mime-subtype="pdf"
                              xlink:href="1234-5678-rctb-45-05-0110-suppl02.pdf"/>
    </article-meta>
  </front>
  <body>
    <sec>
      <p>The Eh measurements... <xref ref-type="disp-formula" rid="e01">equation 1</xref>(in mV):</p>
      <disp-formula id="e01">
        <graphic xlink:href="1234-5678-rctb-45-05-0110-e01.tif"/>
      </disp-formula>
      <p>We also used an... <inline-graphic xlink:href="1234-5678-rctb-45-05-0110-e02.tif"/>.</p>
    </sec>
  </body>
</article>""")
        et = etree.parse(fp)
        xml_validator = domain.XMLValidator.parse(et, no_doctype=True, sps_version='sps-1.1')
        expected_assets = ['1234-5678-rctb-45-05-0110-e01.tif',
                           '1234-5678-rctb-45-05-0110-e02.tif',
                           '1234-5678-rctb-45-05-0110-suppl02.pdf']

        self.assertEqual(sorted(xml_validator.assets), sorted(expected_assets))

    def test_empty_assets_list(self):
        fp = io.BytesIO(b"""<?xml version="1.0" encoding="UTF-8"?>
<article xmlns:xlink="http://www.w3.org/1999/xlink"
         dtd-version="1.0"
         article-type="research-article"
         xml:lang="en">
</article>""")
        et = etree.parse(fp)
        xml_validator = domain.XMLValidator.parse(et, no_doctype=True,
                sps_version='sps-1.1')

        self.assertEqual(xml_validator.assets, [])


class XMLValidatorExtraSchematronTests(unittest.TestCase):

    def test_extra_schematron_thru_parse(self):
        extra_sch = io.BytesIO(b'''\
        <schema xmlns="http://purl.oclc.org/dsdl/schematron">
          <pattern id="two_elements">
            <title>Max 2 elements allowed.</title>
            <rule context="Total">
              <assert test="count(//Percent) &lt; 3">Element 'Total': More than 2 elements.</assert>
            </rule>
          </pattern>
        </schema>
        ''')

        fp = etree.parse(io.BytesIO(b'<Total><Percent>70</Percent><Percent>20</Percent><Percent>10</Percent></Total>'))
        extra_sch_obj = isoschematron.Schematron(etree.parse(extra_sch))
        xml = domain.XMLValidator.parse(fp, no_doctype=True, 
                sps_version='sps-1.1', extra_sch_schemas=[extra_sch_obj])

        result, errors = xml.validate_style()
        self.assertFalse(result)
        self.assertTrue("Element 'Total': More than 2 elements." in 
                [err.message for err in errors]) 

