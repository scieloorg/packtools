#coding: utf-8
from __future__ import unicode_literals
import types
import unittest
import zipfile
from tempfile import NamedTemporaryFile
import functools

from lxml import etree

from packtools.catalogs import SCHEMAS
from packtools.domain import XMLValidator


DTD = SCHEMAS['JATS-journalpublishing1.dtd']


def make_test_archive(arch_data):
    fp = NamedTemporaryFile()
    with zipfile.ZipFile(fp, 'w') as zipfp:
        for archive, data in arch_data:
            zipfp.writestr(archive, data.encode('utf-8'))

    return fp


class SPSPackage(unittest.TestCase):
    XMLValidatorStub = functools.partial(XMLValidator, sps_version='sps-1.1')

    def _makeOne(self, fname):
        """Make a SPSPackage instance with its XMLValidator association set to
        perform validations against a predefined sps version and dtd.
        """
        import packtools
        dtd = etree.DTD(packtools.catalogs.SCHEMAS['JATS-journalpublishing1.dtd'])
        packtools.SPSPackage.XMLValidator = self.XMLValidatorStub
        pack = packtools.SPSPackage(fname)
        pack.xml_validator.dtd = dtd
        return pack

    def test_xml_returns_fileobject(self):
        data = [('bar.xml', u'<root><name>bar</name></root>')]
        arch = make_test_archive(data)
        pkg = self._makeOne(arch.name)

        self.assertTrue(hasattr(pkg.xml_fp, 'read'))

    def test_xml_raises_AttributeError_when_multiple_xmls(self):
        import packtools
        data = [
            ('bar.xml', u'<root><name>bar</name></root>'),
            ('baz.xml', u'<root><name>baz</name></root>'),
        ]
        arch = make_test_archive(data)
        pkg = packtools.SPSPackage(arch.name)  # cannot use _makeOne to get the error

        self.assertRaises(AttributeError, lambda: pkg.xml)

    def test_meta_journal_title_data_is_fetched(self):
        data = [
            ('bar.xml', u'<article><front><journal-meta><journal-title-group><journal-title>foo</journal-title></journal-title-group></journal-meta></front></article>'),
        ]
        arch = make_test_archive(data)
        pkg = self._makeOne(arch.name)

        self.assertEqual(pkg.meta['journal_title'], 'foo')

    def test_meta_journal_title_is_None_if_not_present(self):
        data = [
            ('bar.xml', u'<article></article>'),
        ]
        arch = make_test_archive(data)
        pkg = self._makeOne(arch.name)

        self.assertIsNone(pkg.meta['journal_title'])

    def test_meta_journal_eissn_data_is_fetched(self):
        data = [
            ('bar.xml', u'<article><front><journal-meta><issn pub-type="epub">1234-1234</issn></journal-meta></front></article>'),
        ]
        arch = make_test_archive(data)
        pkg = self._makeOne(arch.name)

        self.assertEqual(pkg.meta['journal_eissn'], '1234-1234')

    def test_meta_journal_eissn_is_None_if_not_present(self):
        data = [
            ('bar.xml', u'<article></article>'),
        ]
        arch = make_test_archive(data)
        pkg = self._makeOne(arch.name)

        self.assertIsNone(pkg.meta['journal_eissn'])

    def test_meta_journal_pissn_data_is_fetched(self):
        data = [
            ('bar.xml', u'<article><front><journal-meta><issn pub-type="ppub">1234-1234</issn></journal-meta></front></article>'),
        ]
        arch = make_test_archive(data)
        pkg = self._makeOne(arch.name)

        self.assertEqual(pkg.meta['journal_pissn'], '1234-1234')

    def test_meta_journal_pissn_is_None_if_not_present(self):
        data = [
            ('bar.xml', u'<article></article>'),
        ]
        arch = make_test_archive(data)
        pkg = self._makeOne(arch.name)

        self.assertIsNone(pkg.meta['journal_pissn'])

    def test_meta_article_title_data_is_fetched(self):
        data = [
            ('bar.xml', u'<article><front><article-meta><title-group><article-title>bar</article-title></title-group></article-meta></front></article>'),
        ]
        arch = make_test_archive(data)
        pkg = self._makeOne(arch.name)

        self.assertEqual(pkg.meta['article_title'], 'bar')

    def test_meta_article_title_is_None_if_not_present(self):
        data = [
            ('bar.xml', u'<article></article>'),
        ]
        arch = make_test_archive(data)
        pkg = self._makeOne(arch.name)

        self.assertIsNone(pkg.meta['article_title'])

    def test_meta_issue_year_data_is_fetched(self):
        data = [
            ('bar.xml', u'<article><front><article-meta><pub-date><year>2013</year></pub-date></article-meta></front></article>'),
        ]
        arch = make_test_archive(data)
        pkg = self._makeOne(arch.name)

        self.assertEqual(pkg.meta['issue_year'], '2013')

    def test_meta_issue_year_is_None_if_not_present(self):
        data = [
            ('bar.xml', u'<article></article>'),
        ]
        arch = make_test_archive(data)
        pkg = self._makeOne(arch.name)

        self.assertIsNone(pkg.meta['issue_year'])

    def test_meta_issue_volume_data_is_fetched(self):
        data = [
            ('bar.xml', u'<article><front><article-meta><volume>2</volume></article-meta></front></article>'),
        ]
        arch = make_test_archive(data)
        pkg = self._makeOne(arch.name)

        self.assertEqual(pkg.meta['issue_volume'], '2')

    def test_meta_issue_volume_is_None_if_not_present(self):
        data = [
            ('bar.xml', u'<article></article>'),
        ]
        arch = make_test_archive(data)
        pkg = self._makeOne(arch.name)

        self.assertIsNone(pkg.meta['issue_volume'])

    def test_meta_issue_number_data_is_fetched(self):
        data = [
            ('bar.xml', u'<article><front><article-meta><issue>2</issue></article-meta></front></article>'),
        ]
        arch = make_test_archive(data)
        pkg = self._makeOne(arch.name)

        self.assertEqual(pkg.meta['issue_number'], '2')

    def test_meta_issue_number_is_None_if_not_present(self):
        data = [
            ('bar.xml', u'<article></article>'),
        ]
        arch = make_test_archive(data)
        pkg = self._makeOne(arch.name)

        self.assertIsNone(pkg.meta['issue_number'])

    def test_is_valid_schema_with_valid_xml(self):
        data = [('bar.xml', u'''<?xml version="1.0" encoding="utf-8"?>
                <!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "JATS-journalpublishing1.dtd">
                <article article-type="in-brief" dtd-version="1.0" xml:lang="en" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML">
                <front>
                    <journal-meta>
                        <journal-id journal-id-type="nlm-ta">Bull World Health Organ</journal-id>
                        <journal-title-group>
                            <journal-title>Bulletin of the World Health Organization</journal-title>
                            <abbrev-journal-title abbrev-type="pubmed">Bull. World Health Organ.</abbrev-journal-title>
                        </journal-title-group>
                        <issn pub-type="ppub">0042-9686</issn>
                        <publisher>
                            <publisher-name>World Health Organization</publisher-name>
                        </publisher>
                    </journal-meta>
                    <article-meta>
                        <article-id pub-id-type="publisher-id">BLT.13.000813</article-id>
                        <article-id pub-id-type="doi">10.2471/BLT.13.000813</article-id>
                        <article-categories>
                            <subj-group subj-group-type="heading">
                                <subject> In This Month´s Bulletin</subject>
                            </subj-group>
                        </article-categories>
                        <title-group>
                            <article-title>In this month's <italic>Bulletin</italic>
                            </article-title>
                        </title-group>
                        <pub-date pub-type="ppub">
                            <month>08</month>
                            <year>2013</year>
                        </pub-date>
                        <volume>91</volume>
                        <issue>8</issue>
                        <fpage>545</fpage>
                        <lpage>545</lpage>
                        <permissions>
                            <copyright-statement>(c) World Health Organization (WHO) 2013. All rights reserved.</copyright-statement>
                            <copyright-year>2013</copyright-year>
                        </permissions>
                    </article-meta>
                </front>
                <body>
                    <p>In the editorial section, David B Evans and colleagues (546) discuss the dimensions of universal health coverage. In the news, Gary Humphreys &#x26; Catherine Fiankan-Bokonga (549&#x2013;550) report on the approach France is taking to counter trends in childhood obesity. Fiona Fleck (551&#x2013;552) interviews Philip James on how the global obesity epidemic started and what should be done to reverse it.</p>
                    <sec sec-type="other1">
                        <title>Nigeria</title>
                    </sec>
                </body>
            </article>
            ''')]
        arch = make_test_archive(data)
        pkg = self._makeOne(arch.name)
        xml_validator = pkg.xml_validator

        self.assertTrue(xml_validator.validate()[0])

    def test_is_valid_schema_with_invalid_xml(self):
        data = [('bar.xml', u'''<?xml version="1.0" encoding="utf-8"?>
                <!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "JATS-journalpublishing1.dtd">
                <article article-type="in-brief" dtd-version="1.0" xml:lang="en" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML">
                <front>
                    <journal-meta>
                        <journal-title-group>
                            <journal-title>Bulletin of the World Health Organization</journal-title>
                            <abbrev-journal-title abbrev-type="pubmed">Bull. World Health Organ.</abbrev-journal-title>
                        </journal-title-group>
                        <issn pub-type="ppub">0042-9686</issn>
                        <publisher>
                            <publisher-name>World Health Organization</publisher-name>
                        </publisher>
                    </journal-meta>
                    <article-meta>
                        <article-id pub-id-type="publisher-id">BLT.13.000813</article-id>
                        <article-id pub-id-type="doi">10.2471/BLT.13.000813</article-id>
                        <article-categories>
                            <subj-group subj-group-type="heading">
                                <subject> In This Month´s Bulletin</subject>
                            </subj-group>
                        </article-categories>
                        <title-group>
                            <article-title>In this month's <italic>Bulletin</italic>
                            </article-title>
                        </title-group>
                        <pub-date pub-type="ppub">
                            <month>08</month>
                            <year>2013</year>
                        </pub-date>
                        <volume>91</volume>
                        <issue>8</issue>
                        <fpage>545</fpage>
                        <lpage>545</lpage>
                        <permissions>
                            <copyright-statement>(c) World Health Organization (WHO) 2013. All rights reserved.</copyright-statement>
                            <copyright-year>2013</copyright-year>
                        </permissions>
                    </article-meta>
                </front>
                <body>
                    <p>In the editorial section, David B Evans and colleagues (546) discuss the dimensions of universal health coverage. In the news, Gary Humphreys &#x26; Catherine Fiankan-Bokonga (549&#x2013;550) report on the approach France is taking to counter trends in childhood obesity. Fiona Fleck (551&#x2013;552) interviews Philip James on how the global obesity epidemic started and what should be done to reverse it.</p>
                    <sec sec-type="other1">
                        <title>Nigeria</title>
                    </sec>
                </body>
            </article>
            ''')]
        arch = make_test_archive(data)
        pkg = self._makeOne(arch.name)
        xml_validator = pkg.xml_validator

        self.assertFalse(xml_validator.validate()[0])

    def test_is_valid_schema_with_wrong_tag(self):
        data = [('bar.xml', u'''<?xml version="1.0" encoding="utf-8"?>
                <!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "JATS-journalpublishing1.dtd">
                <article article-type="in-brief" dtd-version="1.0" xml:lang="en" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML">
                <front>
                    <a>wrong</a>
                    <journal-meta>
                        <journal-title-group>
                            <journal-title>Bulletin of the World Health Organization</journal-title>
                            <abbrev-journal-title abbrev-type="pubmed">Bull. World Health Organ.</abbrev-journal-title>
                        </journal-title-group>
                        <issn pub-type="ppub">0042-9686</issn>
                        <publisher>
                            <publisher-name>World Health Organization</publisher-name>
                        </publisher>
                    </journal-meta>
                    <article-meta>
                        <article-id pub-id-type="publisher-id">BLT.13.000813</article-id>
                        <article-id pub-id-type="doi">10.2471/BLT.13.000813</article-id>
                        <article-categories>
                            <subj-group subj-group-type="heading">
                                <subject> In This Month´s Bulletin</subject>
                            </subj-group>
                        </article-categories>
                        <title-group>
                            <article-title>In this month's <italic>Bulletin</italic>
                            </article-title>
                        </title-group>
                        <pub-date pub-type="ppub">
                            <month>08</month>
                            <year>2013</year>
                        </pub-date>
                        <volume>91</volume>
                        <issue>8</issue>
                        <fpage>545</fpage>
                        <lpage>545</lpage>
                        <permissions>
                            <copyright-statement>(c) World Health Organization (WHO) 2013. All rights reserved.</copyright-statement>
                            <copyright-year>2013</copyright-year>
                        </permissions>
                    </article-meta>
                </front>
                <body>
                    <p>In the editorial section, David B Evans and colleagues (546) discuss the dimensions of universal health coverage. In the news, Gary Humphreys &#x26; Catherine Fiankan-Bokonga (549&#x2013;550) report on the approach France is taking to counter trends in childhood obesity. Fiona Fleck (551&#x2013;552) interviews Philip James on how the global obesity epidemic started and what should be done to reverse it.</p>
                    <sec sec-type="other1">
                        <title>Nigeria</title>
                    </sec>
                </body>
            </article>
            ''')]
        arch = make_test_archive(data)
        pkg = self._makeOne(arch.name)
        xml_validator = pkg.xml_validator

        self.assertFalse(xml_validator.validate()[0])


class XrayTests(unittest.TestCase):

    def _make_test_archive(self, arch_data):
        fp = NamedTemporaryFile()
        with zipfile.ZipFile(fp, 'w') as zipfp:
            for archive, data in arch_data:
                zipfp.writestr(archive, data)

        return fp

    def _makeOne(self, file):
        from packtools.xray import Xray
        return Xray(file)

    def test_non_zip_archive_raises_ValueError(self):
        fp = NamedTemporaryFile()
        self.assertRaises(ValueError, lambda: self._makeOne(fp.name))

    def test_get_ext_returns_member_names(self):
        arch = make_test_archive(
            [('bar.xml', u'<root><name>bar</name></root>')])

        xray = self._makeOne(arch.name)

        self.assertEqual(xray.get_ext('xml'), ['bar.xml'])

    def test_get_ext_returns_empty_when_ext_doesnot_exist(self):
        arch = make_test_archive(
            [('bar.xml', u'<root><name>bar</name></root>')])

        xray = self._makeOne(arch.name)

        self.assertEqual(xray.get_ext('jpeg'), [])

    def test_get_fps_returns_an_iterable(self):
        arch = make_test_archive(
            [('bar.xml', u'<root><name>bar</name></root>')])

        xray = self._makeOne(arch.name)

        fps = xray.get_fps('xml')
        self.assertTrue(isinstance(fps, types.GeneratorType))

    def test_get_fpd_yields_ZipExtFile_instances(self):
        arch = make_test_archive(
            [('bar.xml', u'<root><name>bar</name></root>')])

        xray = self._makeOne(arch.name)

        fps = xray.get_fps('xml')
        self.assertIsInstance(next(fps), zipfile.ZipExtFile)

    def test_get_fps_swallow_exceptions_when_ext_doesnot_exist(self):
        arch = make_test_archive(
            [('bar.xml', u'<root><name>bar</name></root>')])

        xray = self._makeOne(arch.name)
        fps = xray.get_fps('jpeg')

        self.assertRaises(StopIteration, lambda: next(fps))

    def test_package_checksum_is_calculated(self):
        import hashlib
        data = [('bar.xml', u'<root><name>bar</name></root>')]
        arch1 = make_test_archive(data)
        arch2 = make_test_archive(data)

        self.assertEqual(
            self._makeOne(arch1.name).checksum(hashlib.sha1),
            self._makeOne(arch2.name).checksum(hashlib.sha1)
        )

    def test_get_members(self):
        arch = make_test_archive(
            [('bar.xml', u'<root><name>bar</name></root>'),
             ('jar.xml', u'<root><name>bar</name></root>')])

        xray = self._makeOne(arch.name)

        self.assertEqual(xray.get_members(), ['bar.xml', 'jar.xml'])

    def test_get_members_returns_empty(self):
        arch = make_test_archive([])

        xray = self._makeOne(arch.name)

        self.assertEqual(xray.get_members(), [])

    def test_get_fp(self):
        arch = make_test_archive(
            [('bar.xml', u'<root><name>bar</name></root>'),
             ('jar.xml', u'<root><name>bar</name></root>')])

        xray = self._makeOne(arch.name)

        self.assertIsInstance(xray.get_fp('bar.xml'),
            zipfile.ZipExtFile)

    def test_get_fp_nonexisting_members(self):
        arch = make_test_archive(
            [('bar.xml', u'<root><name>bar</name></root>'),
             ('jar.xml', u'<root><name>bar</name></root>')])

        xray = self._makeOne(arch.name)

        self.assertRaises(ValueError, lambda: xray.get_fp('foo.xml'))

    def test_get_classified_members(self):
        arch = make_test_archive(
            [('bar.xml', u'<root><name>bar</name></root>'),
             ('jar.xml', u'<root><name>bar</name></root>')])

        xray = self._makeOne(arch.name)

        self.assertEqual(xray.get_classified_members(), {'xml': ['bar.xml', 'jar.xml']})

    def test_get_ext_is_caseinsensitive(self):
        arch = make_test_archive(
            [('bar.xml', u'<root><name>bar</name></root>'),
             ('jar.XML', u'<root><name>bar</name></root>')])

        xray = self._makeOne(arch.name)

        self.assertEqual(xray.get_ext('xml'), ['bar.xml', 'jar.XML'])

    def test_get_ext_arg_is_caseinsensitive(self):
        arch = make_test_archive(
            [('bar.xml', u'<root><name>bar</name></root>'),
             ('jar.XML', u'<root><name>bar</name></root>')])

        xray = self._makeOne(arch.name)

        self.assertEqual(xray.get_ext('XML'), ['bar.xml', 'jar.XML'])

    def test_get_classified_members_is_caseinsensitive(self):
        arch = make_test_archive(
            [('bar.xml', u'<root><name>bar</name></root>'),
             ('jar.XML', u'<root><name>bar</name></root>')])

        xray = self._makeOne(arch.name)

        self.assertEqual(xray.get_classified_members(), {'xml': ['bar.xml', 'jar.XML']})

    def test_get_fps_is_caseinsensitive(self):
        arch = make_test_archive(
            [('bar.xml', u'<root><name>bar</name></root>'),
             ('jar.XML', u'<root><name>bar</name></root>')])

        xray = self._makeOne(arch.name)
        fps = xray.get_fps('xml')

        self.assertEqual([fp.name for fp in fps], ['bar.xml', 'jar.XML'])

    def test_get_fps_arg_is_caseinsensitive(self):
        arch = make_test_archive(
            [('bar.xml', u'<root><name>bar</name></root>'),
             ('jar.XML', u'<root><name>bar</name></root>')])

        xray = self._makeOne(arch.name)
        fps = xray.get_fps('XML')

        self.assertEqual([fp.name for fp in fps], ['bar.xml', 'jar.XML'])

