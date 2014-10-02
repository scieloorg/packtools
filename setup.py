#!/usr/bin/env python
from setuptools import setup, find_packages


# adds version to the local namespace
version = {}
with open('packtools/version.py') as fp:
    exec(fp.read(), version)


install_requires = [
    'lxml >= 3.3.4',
    'picles.plumber >= 0.10',
]


tests_require = []


setup(
    name="packtools",
    version=version['__version__'],
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
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
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

