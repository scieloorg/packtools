#!/usr/bin/env python
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


install_requires = [
    'lxml',
]

setup(
    name="packtools",
    version='0.1',
    description="Handle SPS packages like a breeze.",
    #long_description=open('README.md').read() + '\n\n' +
    #                 open('HISTORY.md').read(),
    author="SciELO",
    author_email="scielo-dev@googlegroups.com",
    maintainer="Gustavo Fonseca",
    maintainer_email="gustavo.fonseca@scielo.org",
    license="BSD License",
    url="http://docs.scielo.org",
    packages=['packtools'],
    package_data={'': ['LICENSE'], 'packtools': ['sps_xsd/*']},
    package_dir={'packtools': 'packtools'},
    include_package_data=True,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    setup_requires=["nose>=1.0", "coverage"],
    tests_require=["mocker"],
    test_suite='tests',
    install_requires=install_requires,
    entry_points="""
    [console_scripts]
    stylechecker = packtools.stylechecker:main
    """)

