#coding: utf-8
from __future__ import unicode_literals
import unittest
import io

from lxml import etree

from packtools import style_errors


class ElementNamePatternTests(unittest.TestCase):
    pattern = style_errors.EXPOSE_ELEMENTNAME_PATTERN

    def test_case1(self):
        message = "Element 'article', attribute 'dtd-version': [facet 'enumeration'] The value '3.0' is not an element of the set {'1.0'}."
        self.assertEqual(self.pattern.search(message).group(0), "'article'")


    def test_case2(self):
        message = "Element 'article', attribute 'dtd-version': '3.0' is not a valid value of the local atomic type."
        self.assertEqual(self.pattern.search(message).group(0), "'article'")

    def test_case3(self):
        message = "Element 'author-notes': This element is not expected. Expected is one of ( label, title, ack, app-group, bio, fn-group, glossary, ref-list, notes, sec )."
        self.assertEqual(self.pattern.search(message).group(0), "'author-notes'")

    def test_case4(self):
        message = "Element 'journal-title-group': This element is not expected. Expected is ( journal-id )."
        self.assertEqual(self.pattern.search(message).group(0), "'journal-title-group'")

    def test_case5(self):
        message = "Element 'contrib-group': This element is not expected. Expected is one of ( article-id, article-categories, title-group )."
        self.assertEqual(self.pattern.search(message).group(0), "'contrib-group'")


class SearchElementFunctionTests(unittest.TestCase):

    def test_find_root_element(self):
        fp = etree.parse(io.BytesIO(b'<a>\n<b>bar</b>\n</a>'))
        elem = style_errors.search_element(fp, '/a', 1)
        self.assertEqual(elem.tag, 'a')
        self.assertEqual(elem.sourceline, 1)

    def test_find(self):
        fp = etree.parse(io.BytesIO(b'<a>\n<b>bar</b>\n</a>'))
        elem = style_errors.search_element(fp, '//b', 2)
        self.assertEqual(elem.tag, 'b')
        self.assertEqual(elem.sourceline, 2)

    def test_find_missing(self):
        fp = etree.parse(io.BytesIO(b'<a>\n<b>bar</b>\n</a>'))
        self.assertRaises(ValueError, lambda: style_errors.search_element(fp, 'c', 2))

