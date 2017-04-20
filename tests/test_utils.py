#coding: utf-8
from __future__ import unicode_literals
import unittest
import zipfile
from tempfile import NamedTemporaryFile

from packtools import utils


class CachedMethodTests(unittest.TestCase):
    def test_without_params(self):

        class A(object):
            def __init__(self):
                self.counter = 0

            @utils.cachedmethod
            def foo(self):
                self.counter += 1
                return 'bar'

        a = A()
        self.assertEqual(a.counter, 0)

        self.assertEqual(a.foo(), 'bar')
        self.assertEqual(a.counter, 1)

        self.assertEqual(a.foo(), 'bar')
        self.assertEqual(a.counter, 1)

    def test_with_params(self):

        class A(object):
            def __init__(self):
                self.counter = 0

            @utils.cachedmethod
            def sum(self, a, b):
                self.counter += 1
                return a + b

        a = A()
        self.assertEqual(a.counter, 0)

        self.assertEqual(a.sum(2, 2), 4)
        self.assertEqual(a.counter, 1)

        self.assertEqual(a.sum(2, 3), 5)
        self.assertEqual(a.counter, 2)

        self.assertEqual(a.sum(2, 2), 4)
        self.assertEqual(a.counter, 2)


class XrayTests(unittest.TestCase):

    def _make_test_archive(self, arch_data):
        fp = NamedTemporaryFile()
        with zipfile.ZipFile(fp, 'w') as zipfp:
            for archive, data in arch_data:
                zipfp.writestr(archive, data)

        return fp

    def test_members_are_shown(self):
        arch = self._make_test_archive(
            [('bar.xml', u'<root><name>bar</name></root>'),
             ('jar.xml', u'<root><name>bar</name></root>')])

        with utils.Xray.fromfile(arch.name) as xray:
            self.assertEqual(sorted(xray.show_members()),
                    sorted(['bar.xml', 'jar.xml']))

    def test_get_members_returns_empty(self):
        arch = self._make_test_archive([])

        with utils.Xray.fromfile(arch.name) as xray:
            self.assertEqual(xray.show_members(), [])

    def test_get_file(self):
        arch = self._make_test_archive(
            [('bar.xml', u'<root><name>bar</name></root>'),
             ('jar.xml', u'<root><name>bar</name></root>')])

        with utils.Xray.fromfile(arch.name) as xray:
            member = xray.get_file('bar.xml')
            self.assertEqual(member.read(), b'<root><name>bar</name></root>')

    def test_get_file_for_nonexisting_member(self):
        arch = self._make_test_archive(
            [('bar.xml', u'<root><name>bar</name></root>'),
             ('jar.xml', u'<root><name>bar</name></root>')])

        with utils.Xray.fromfile(arch.name) as xray:
            self.assertRaises(ValueError, lambda: xray.get_file('foo.xml'))

    def test_show_sorted_members(self):
        arch = self._make_test_archive(
            [('bar.xml', u'<root><name>bar</name></root>'),
             ('jar.xml', u'<root><name>bar</name></root>')])

        with utils.Xray.fromfile(arch.name) as xray:
            self.assertEqual(xray.show_sorted_members(),
                    {'xml': ['bar.xml', 'jar.xml']})

    def test_show_sorted_members_is_caseinsensitive(self):
        arch = self._make_test_archive(
            [('bar.xml', u'<root><name>bar</name></root>'),
             ('jar.XML', u'<root><name>bar</name></root>')])

        with utils.Xray.fromfile(arch.name) as xray:
            self.assertEqual(xray.show_sorted_members(),
                    {'xml': ['bar.xml', 'jar.XML']})


class ResolveSchematronFilepathTests(unittest.TestCase):
    def setUp(self):
        from packtools import catalogs
        self.sch_schemas = catalogs.SCH_SCHEMAS

    def test_builtin_lookup(self):
        for name, path in self.sch_schemas.items():
            self.assertEqual(utils.resolve_schematron_filepath('@'+name), path)

    def test_resolve_unsupported_types(self):
        self.assertRaises(TypeError,
                lambda: utils.resolve_schematron_filepath(None))

    def test_non_existing_builtin(self):
        self.assertRaises(ValueError, 
                lambda: utils.resolve_schematron_filepath('@notexists'))

    def test_existing_filepath(self):
        path = list(self.sch_schemas.values())[0]  # get the first item
        self.assertEqual(utils.resolve_schematron_filepath(path), path)

    def test_non_existing_filepath(self):
        path = list(self.sch_schemas.values())[0] + '.notexists'
        self.assertRaises(ValueError, 
                lambda: utils.resolve_schematron_filepath(path))

