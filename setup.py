#!/usr/bin/env python
#coding:utf-8
from __future__ import unicode_literals
from setuptools import setup, find_packages
import codecs
import sys


if sys.version_info[0:2] < (2, 7):
    raise RuntimeError('Requires Python 2.7 or newer')


# adds version to the local namespace
version = {}
with open('packtools/version.py') as fp:
    exec(fp.read(), version)


install_requires = [
    'lxml >= 3.3.4',
    'picles.plumber >= 0.11',
]


if sys.version_info[0] == 2:
    install_requires.append('pathlib2 >= 2.1.0')


tests_require = []


setup(
    name="packtools",
    version=version['__version__'],
    description="Handle SPS packages like a breeze.",
    long_description=codecs.open('README.rst', mode='r', encoding='utf-8').read() + '\n\n' +
                     codecs.open('HISTORY.rst', mode='r', encoding='utf-8').read(),
    author="SciELO",
    author_email="scielo-dev@googlegroups.com",
    maintainer="Gustavo Fonseca",
    maintainer_email="gustavo.fonseca@scielo.org",
    license="BSD License",
    url="http://docs.scielo.org",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    tests_require=tests_require,
    test_suite='tests',
    install_requires=install_requires,
    entry_points="""
    [console_scripts]
    stylechecker = packtools.stylechecker:main
    htmlgenerator = packtools.htmlgenerator:main
    """)

