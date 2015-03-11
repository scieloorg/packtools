#coding: utf-8
from __future__ import unicode_literals
import unittest

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

