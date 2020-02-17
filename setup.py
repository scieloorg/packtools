#!/usr/bin/env python
#coding:utf-8
from __future__ import unicode_literals
from setuptools import setup
import setuptools
import codecs
import sys


if sys.version_info[0:2] < (2, 7):
    raise RuntimeError('Requires Python 2.7 or newer')


# adds version to the local namespace
VERSION = {}
with open('packtools/version.py') as fp:
    exec(fp.read(), VERSION)


INSTALL_REQUIRES = [
    'lxml>=4.2.0',
    'picles.plumber>=0.11',
    'Pillow~=6.2',
]


EXTRAS_REQUIRE = {
    'webapp':[
        'Flask',
        'Flask-BabelEx',
        'Flask-WTF',
        'Werkzeug==0.16.1',
    ]
}


TESTS_REQUIRE = [
    'Flask-Testing>=0.6.2',
    'Flask-BabelEx',
    'Flask-WTF',
]


# from https://hynek.me/articles/conditional-python-dependencies/
# basically, binary wheels built using setuptools version < 18 do not support
# the syntax for conditional dependencies used below.
if int(setuptools.__version__.split('.', 1)[0]) < 18:
    assert "bdist_wheel" not in sys.argv, "setuptools 18 required for wheels."
    if sys.version_info[0:2] < (3, 4):
        INSTALL_REQUIRES.append('pathlib>=1.0.1')
else:
    EXTRAS_REQUIRE[':python_version<"3.4"'] = ['pathlib>=1.0.1']

if sys.version_info[0:2] == (2, 7):
    TESTS_REQUIRE.append('mock')

setup(
    name="packtools",
    version=VERSION['__version__'],
    description="Handle SPS packages like a breeze.",
    long_description=codecs.open('README.md', mode='r', encoding='utf-8').read() + '\n\n' +
                     codecs.open('HISTORY.md', mode='r', encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    author="SciELO",
    author_email="scielo-dev@googlegroups.com",
    maintainer="Gustavo Fonseca",
    maintainer_email="gustavo.fonseca@scielo.org",
    license="BSD License",
    url="http://docs.scielo.org",
    packages=setuptools.find_packages(
        exclude=["*.tests", "*.tests.*", "tests.*", "tests", "docs"]
    ),
    include_package_data=True,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
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
        ]
    }
)
