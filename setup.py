#!/usr/bin/env python
import sys
from setuptools import setup, find_packages


install_requires = [
    'lxml >= 3.3.4',
    'picles.plumber >= 0.10',
]


tests_require = ['mocker']
PY2 = sys.version_info[0] == 2
if PY2:
    tests_require.append('mock')


setup(
    name="packtools",
    version='0.6',
    description="Handle SPS packages like a breeze.",
    long_description=open('README.md').read() + '\n\n' +
                     open('HISTORY.md').read(),
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
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    tests_require=tests_require,
    test_suite='tests',
    install_requires=install_requires,
    entry_points="""
    [console_scripts]
    stylechecker = packtools.stylechecker:main
    packbuilder = packtools.packbuilder:main
    """)

