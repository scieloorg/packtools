#!/usr/bin/env python
#coding:utf-8
from __future__ import unicode_literals
from pathlib import Path
from setuptools import setup
from setuptools.command.build_py import build_py as _build_py
import setuptools
import codecs
import sys


if sys.version_info[0:2] < (3, 9):
    raise RuntimeError('Requires Python 3.9 or newer')


LOCALE_DIR = Path(__file__).resolve().parent / "packtools" / "sps" / "locale"


def compile_sps_i18n_catalogs():
    """Compila packtools/sps/locale/*/LC_MESSAGES/*.po para .mo.

    MANIFEST.in so inclui *.mo (nao *.po) na distribuicao, entao sem esse
    passo os catalogos ficam de fora do sdist/wheel e
    packtools.sps.i18n.set_locale() nunca encontra traducao nenhuma - ver
    issue #1267.
    """
    from babel.messages.mofile import write_mo
    from babel.messages.pofile import read_po

    for po_path in sorted(LOCALE_DIR.glob("*/LC_MESSAGES/*.po")):
        with po_path.open("rb") as po_file:
            catalog = read_po(po_file)
        mo_path = po_path.with_suffix(".mo")
        with mo_path.open("wb") as mo_file:
            write_mo(mo_file, catalog)


class build_py(_build_py):
    def run(self):
        compile_sps_i18n_catalogs()
        super().run()


# adds version to the local namespace
VERSION = {}
with open('packtools/version.py') as fp:
    exec(fp.read(), VERSION)


INSTALL_REQUIRES = [
    'aiohttp>=3.9.1',
    'lxml>=4.9.2',
    'langcodes>=3.3.0',
    'langdetect>=1.0.9',
    'picles.plumber>=0.11',
    'Pillow',
    'requests>=2.32.0',
    'openpyxl>=3.1.5',
    'python-docx>=1.1.2',
    'tenacity>=8.2.3',
]


EXTRAS_REQUIRE = {
    'webapp':[
        'Flask',
        'flask-babel',
        'Flask-WTF>=1.2.0',
        'Werkzeug<3.0',
    ]
}


TESTS_REQUIRE = [
    'Flask-Testing>=0.6.2',
    'flask-babel',
    'Flask-WTF>=1.2.0',
    'python-magic',
    'charset-normalizer<3.0',
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
    cmdclass={"build_py": build_py},
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
        ]
    }
)
