#!/usr/bin/env python
#coding:utf-8
from __future__ import unicode_literals
from setuptools import setup
import setuptools
import codecs
import sys


if sys.version_info[0:2] < (3, 9):
    raise RuntimeError('Requires Python 3.9 or newer')


# adds version to the local namespace
VERSION = {}
with open('packtools/version.py') as fp:
    exec(fp.read(), VERSION)


INSTALL_REQUIRES = [
    'lxml>=4.9.2',
    'langcodes>=3.3.0',
    'picles.plumber>=0.11',
    'Pillow',
    'openpyxl>=3.1.5',
    'python-docx>=1.1.2',
]


EXTRAS_REQUIRE = {
    'webapp':[
        'Flask',
        'flask-babel',
        'Flask-WTF',
        'Werkzeug',
    ]
}


TESTS_REQUIRE = [
    'Flask-Testing>=0.6.2',
    'flask-babel',
    'Flask-WTF',
    'python-magic',
    'charset-normalizer<3.0',
    'aiohttp',
    'tenacity',
    'requests',
]


setup(
    name="packtools",
    version=VERSION['__version__'],
    description="Handle SPS packages like a breeze.",
    long_description=codecs.open('README.md', mode='r', encoding='utf-8').read() + '\n\n' +
                     codecs.open('HISTORY.md', mode='r', encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    author="SciELO",
    author_email="scielo-dev@googlegroups.com",
    maintainer="SciELO Team",
    maintainer_email="scielo-dev@googlegroups.com",
    license="BSD License",
    url="http://docs.scielo.org",
    packages=setuptools.find_packages(
        exclude=["*.tests", "*.tests.*", "tests.*", "tests", "docs"]
    ),
    include_package_data=True,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    tests_require=TESTS_REQUIRE,
    test_suite='tests',
    install_requires=INSTALL_REQUIRES,
    extras_require=EXTRAS_REQUIRE,
    entry_points={
        "console_scripts":[
            "stylechecker=packtools.stylechecker:main",
            "htmlgenerator=packtools.htmlgenerator:main",
            "package_optimiser=packtools.package_optimiser:main",
            "package_maker=packtools.package_maker:main",
            "pdf_generator=packtools.sps.formats.pdf_generator:main",
            "journal-extractor=packtools.journal_info_extractor:main",
        ]
    }
)
