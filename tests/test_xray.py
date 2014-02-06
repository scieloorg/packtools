#coding: utf-8
import zipfile
from tempfile import NamedTemporaryFile
from lxml import etree

import mocker
import unittest

from packtools import xray as x_ray


class SPSMixinTests(mocker.MockerTestCase):

    def _make_test_archive(self, arch_data):
        fp = NamedTemporaryFile()
        with zipfile.ZipFile(fp, 'w') as zipfp:
            for archive, data in arch_data:
                zipfp.writestr(archive, data)

        return fp

    def _makeOne(self, fname):
        class Foo(x_ray.SPSMixin, x_ray.Xray):
            pass

        return Foo(fname)

    def test_xmls_yields_etree_instances(self):
        data = [('bar.xml', b'<root><name>bar</name></root>')]
        arch = self._make_test_archive(data)
        pkg = self._makeOne(arch.name)

        xmls = pkg.xmls
        self.assertIsInstance(xmls.next(), etree._ElementTree)

    def test_xml_returns_etree_instance(self):
        data = [('bar.xml', b'<root><name>bar</name></root>')]
        arch = self._make_test_archive(data)
        pkg = self._makeOne(arch.name)

        self.assertIsInstance(pkg.xml, etree._ElementTree)

    def test_xml_raises_AttributeError_when_multiple_xmls(self):
        data = [
            ('bar.xml', b'<root><name>bar</name></root>'),
            ('baz.xml', b'<root><name>baz</name></root>'),
        ]
        arch = self._make_test_archive(data)
        pkg = self._makeOne(arch.name)

        self.assertRaises(AttributeError, lambda: pkg.xml)

    def test_meta_journal_title_data_is_fetched(self):
        data = [
            ('bar.xml', b'<root><journal-meta><journal-title-group><journal-title>foo</journal-title></journal-title-group></journal-meta></root>'),
        ]
        arch = self._make_test_archive(data)
        pkg = self._makeOne(arch.name)

        self.assertEqual(pkg.meta['journal_title'], 'foo')

    def test_meta_journal_title_is_None_if_not_present(self):
        data = [
            ('bar.xml', b'<root></root>'),
        ]
        arch = self._make_test_archive(data)
        pkg = self._makeOne(arch.name)

        self.assertIsNone(pkg.meta['journal_title'])

    def test_meta_journal_eissn_data_is_fetched(self):
        data = [
            ('bar.xml', b'<root><journal-meta><issn pub-type="epub">1234-1234</issn></journal-meta></root>'),
        ]
        arch = self._make_test_archive(data)
        pkg = self._makeOne(arch.name)

        self.assertEqual(pkg.meta['journal_eissn'], '1234-1234')

    def test_meta_journal_eissn_is_None_if_not_present(self):
        data = [
            ('bar.xml', b'<root></root>'),
        ]
        arch = self._make_test_archive(data)
        pkg = self._makeOne(arch.name)

        self.assertIsNone(pkg.meta['journal_eissn'])

    def test_meta_journal_pissn_data_is_fetched(self):
        data = [
            ('bar.xml', b'<root><journal-meta><issn pub-type="ppub">1234-1234</issn></journal-meta></root>'),
        ]
        arch = self._make_test_archive(data)
        pkg = self._makeOne(arch.name)

        self.assertEqual(pkg.meta['journal_pissn'], '1234-1234')

    def test_meta_journal_pissn_is_None_if_not_present(self):
        data = [
            ('bar.xml', b'<root></root>'),
        ]
        arch = self._make_test_archive(data)
        pkg = self._makeOne(arch.name)

        self.assertIsNone(pkg.meta['journal_pissn'])

    def test_meta_article_title_data_is_fetched(self):
        data = [
            ('bar.xml', b'<root><article-meta><title-group><article-title>bar</article-title></title-group></article-meta></root>'),
        ]
        arch = self._make_test_archive(data)
        pkg = self._makeOne(arch.name)

        self.assertEqual(pkg.meta['article_title'], 'bar')

    def test_meta_article_title_is_None_if_not_present(self):
        data = [
            ('bar.xml', b'<root></root>'),
        ]
        arch = self._make_test_archive(data)
        pkg = self._makeOne(arch.name)

        self.assertIsNone(pkg.meta['article_title'])

    def test_meta_issue_year_data_is_fetched(self):
        data = [
            ('bar.xml', b'<root><article-meta><pub-date><year>2013</year></pub-date></article-meta></root>'),
        ]
        arch = self._make_test_archive(data)
        pkg = self._makeOne(arch.name)

        self.assertEqual(pkg.meta['issue_year'], '2013')

    def test_meta_issue_year_is_None_if_not_present(self):
        data = [
            ('bar.xml', b'<root></root>'),
        ]
        arch = self._make_test_archive(data)
        pkg = self._makeOne(arch.name)

        self.assertIsNone(pkg.meta['issue_year'])

    def test_meta_issue_volume_data_is_fetched(self):
        data = [
            ('bar.xml', b'<root><article-meta><volume>2</volume></article-meta></root>'),
        ]
        arch = self._make_test_archive(data)
        pkg = self._makeOne(arch.name)

        self.assertEqual(pkg.meta['issue_volume'], '2')

    def test_meta_issue_volume_is_None_if_not_present(self):
        data = [
            ('bar.xml', b'<root></root>'),
        ]
        arch = self._make_test_archive(data)
        pkg = self._makeOne(arch.name)

        self.assertIsNone(pkg.meta['issue_volume'])

    def test_meta_issue_number_data_is_fetched(self):
        data = [
            ('bar.xml', b'<root><article-meta><issue>2</issue></article-meta></root>'),
        ]
        arch = self._make_test_archive(data)
        pkg = self._makeOne(arch.name)

        self.assertEqual(pkg.meta['issue_number'], '2')

    def test_meta_issue_number_is_None_if_not_present(self):
        data = [
            ('bar.xml', b'<root></root>'),
        ]
        arch = self._make_test_archive(data)
        pkg = self._makeOne(arch.name)

        self.assertIsNone(pkg.meta['issue_number'])

    def test_meta_is_not_valid(self):
        data = [
            ('bar.xml', b'<root></root>'),
        ]
        arch = self._make_test_archive(data)
        pkg = self._makeOne(arch.name)

        self.assertFalse(pkg.is_valid_meta())

    def test_meta_is_valid(self):
        data = [
            ('bar.xml', b'<root><journal-meta><issn pub-type="ppub">12-34</issn></journal-meta><article-meta><issue>3</issue><title-group><article-title>Titulo de artigo</article-title></title-group></article-meta></root>'),
        ]
        arch = self._make_test_archive(data)
        pkg = self._makeOne(arch.name)

        self.assertTrue(pkg.is_valid_meta())

    def test_is_valid_schema_with_valid_xml(self):
        data = [('bar.xml', b'''<?xml version="1.0" encoding="utf-8"?>
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
        arch = self._make_test_archive(data)
        pkg = self._makeOne(arch.name)

        self.assertTrue(pkg.is_valid_schema())

    def test_is_valid_schema_with_invalid_xml(self):
        data = [('bar.xml', b'''<?xml version="1.0" encoding="utf-8"?>
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
        arch = self._make_test_archive(data)
        pkg = self._makeOne(arch.name)

        self.assertFalse(pkg.is_valid_schema())

    def test_is_valid_schema_with_wrong_tag(self):
        data = [('bar.xml', b'''<?xml version="1.0" encoding="utf-8"?>
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
        arch = self._make_test_archive(data)
        pkg = self._makeOne(arch.name)

        self.assertFalse(pkg.is_valid_schema())


class XrayTests(mocker.MockerTestCase):

    def _make_test_archive(self, arch_data):
        fp = NamedTemporaryFile()
        with zipfile.ZipFile(fp, 'w') as zipfp:
            for archive, data in arch_data:
                zipfp.writestr(archive, data)

        return fp

    def test_non_zip_archive_raises_ValueError(self):
        fp = NamedTemporaryFile()
        self.assertRaises(ValueError, lambda: x_ray.Xray(fp.name))

    def test_get_ext_returns_member_names(self):
        arch = self._make_test_archive(
            [('bar.xml', b'<root><name>bar</name></root>')])

        xray = x_ray.Xray(arch.name)

        self.assertEquals(xray.get_ext('xml'), ['bar.xml'])

    def test_get_ext_returns_empty_when_ext_doesnot_exist(self):
        arch = self._make_test_archive(
            [('bar.xml', b'<root><name>bar</name></root>')])

        xray = x_ray.Xray(arch.name)

        self.assertEquals(xray.get_ext('jpeg'), [])

    def test_get_fps_returns_an_iterable(self):
        arch = self._make_test_archive(
            [('bar.xml', b'<root><name>bar</name></root>')])

        xray = x_ray.Xray(arch.name)

        fps = xray.get_fps('xml')
        self.assertTrue(hasattr(fps, 'next'))

    def test_get_fpd_yields_ZipExtFile_instances(self):
        arch = self._make_test_archive(
            [('bar.xml', b'<root><name>bar</name></root>')])

        xray = x_ray.Xray(arch.name)

        fps = xray.get_fps('xml')
        self.assertIsInstance(fps.next(), zipfile.ZipExtFile)

    def test_get_fps_swallow_exceptions_when_ext_doesnot_exist(self):
        arch = self._make_test_archive(
            [('bar.xml', b'<root><name>bar</name></root>')])

        xray = x_ray.Xray(arch.name)
        fps = xray.get_fps('jpeg')

        self.assertRaises(StopIteration, lambda: fps.next())

    def test_package_checksum_is_calculated(self):
        data = [('bar.xml', b'<root><name>bar</name></root>')]
        arch1 = self._make_test_archive(data)
        arch2 = self._make_test_archive(data)

        self.assertEquals(
            x_ray.Xray(arch1.name).checksum,
            x_ray.Xray(arch2.name).checksum
        )

    def test_get_members(self):
        arch = self._make_test_archive(
            [('bar.xml', b'<root><name>bar</name></root>'),
             ('jar.xml', b'<root><name>bar</name></root>')])

        xray = x_ray.Xray(arch.name)

        self.assertEquals(xray.get_members(), ['bar.xml', 'jar.xml'])

    def test_get_members_returns_empty(self):
        arch = self._make_test_archive([])

        xray = x_ray.Xray(arch.name)

        self.assertEquals(xray.get_members(), [])

    def test_get_fp(self):
        arch = self._make_test_archive(
            [('bar.xml', b'<root><name>bar</name></root>'),
             ('jar.xml', b'<root><name>bar</name></root>')])

        xray = x_ray.Xray(arch.name)

        self.assertIsInstance(xray.get_fp('bar.xml'),
            zipfile.ZipExtFile)

    def test_get_fp_nonexisting_members(self):
        arch = self._make_test_archive(
            [('bar.xml', b'<root><name>bar</name></root>'),
             ('jar.xml', b'<root><name>bar</name></root>')])

        xray = x_ray.Xray(arch.name)

        self.assertRaises(ValueError, lambda: xray.get_fp('foo.xml'))

