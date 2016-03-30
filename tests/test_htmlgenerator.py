# coding: utf-8
from __future__ import unicode_literals
import unittest
import io
from tempfile import NamedTemporaryFile
from lxml import etree

from packtools import domain


def setup_tmpfile(method):
    def wrapper(self):
        valid_tmpfile = NamedTemporaryFile()
        valid_tmpfile.write(b'<a><b>bar</b></a>')
        valid_tmpfile.seek(0)
        self.valid_tmpfile = valid_tmpfile

        method(self)

        self.valid_tmpfile.close()

    return wrapper


class HTMLGeneratorTests(unittest.TestCase):

    @setup_tmpfile
    def test_initializes_with_filepath(self):
        self.assertTrue(domain.HTMLGenerator.parse(self.valid_tmpfile.name, valid_only=False))

    def test_initializes_with_etree(self):
        fp = io.BytesIO(b'<a><b>bar</b></a>')
        et = etree.parse(fp)

        self.assertTrue(domain.HTMLGenerator.parse(et, valid_only=False))

    def test_languages(self):
        sample = u"""<article xml:lang="pt">
                       <sub-article xml:lang="en" article-type="translation" id="S01">
                       </sub-article>
                       <sub-article xml:lang="es" article-type="translation" id="S02">
                       </sub-article>
                    </article>
                 """
        fp = io.BytesIO(sample.encode('utf-8'))
        et = etree.parse(fp)

        self.assertEqual(domain.HTMLGenerator.parse(et, valid_only=False).languages, ['pt', 'en', 'es'])

    def test_language(self):
        sample = u"""<article xml:lang="pt">
                       <sub-article xml:lang="en" article-type="translation" id="S01">
                       </sub-article>
                       <sub-article xml:lang="es" article-type="translation" id="S02">
                       </sub-article>
                    </article>
                 """
        fp = io.BytesIO(sample.encode('utf-8'))
        et = etree.parse(fp)

        self.assertEqual(domain.HTMLGenerator.parse(et, valid_only=False).language, 'pt')

    def test_language_missing_data(self):
        """ This should not happen since the attribute is mandatory.
        """
        sample = u"""<article>
                       <sub-article xml:lang="en" article-type="translation" id="S01">
                       </sub-article>
                       <sub-article xml:lang="es" article-type="translation" id="S02">
                       </sub-article>
                    </article>
                 """
        fp = io.BytesIO(sample.encode('utf-8'))
        et = etree.parse(fp)

        self.assertEquals(domain.HTMLGenerator.parse(
            et, valid_only=False).language, None)

    @unittest.skip('aguardando definicao')
    def test_bibliographic_legend_epub_ppub(self):
        sample = u"""<article>
                      <front>
                        <journal-meta>
                          <journal-title-group>
                            <journal-title>Revista de Saude Publica</journal-title>
                            <abbrev-journal-title abbrev-type='publisher'>Rev. Saude Publica</abbrev-journal-title>
                          </journal-title-group>
                        </journal-meta>
                        <article-meta>
                          <pub-date pub-type="epub-ppub">
                            <day>17</day>
                            <month>03</month>
                            <year>2014</year>
                          </pub-date>
                          <volume>10</volume>
                          <issue>2</issue>
                        </article-meta>
                      </front>
                    </article>
                 """
        fp = io.BytesIO(sample.encode('utf-8'))
        et = etree.parse(fp)

        self.assertEqual(domain.HTMLGenerator.parse(et, valid_only=False)._get_bibliographic_legend(),
                         u'Rev. Saude Publica vol.10 no.2 Mar 17, 2014')

    @unittest.skip('aguardando definicao')
    def test_bibliographic_legend_with_season(self):
        pass

    @unittest.skip('aguardando definicao')
    def test_bibliographic_legend_epub_epub_ppub(self):
        pass

    @unittest.skip('aguardando definicao')
    def test_bibliographic_legend_ahead_of_print(self):
        pass

    def test_generation_unknown_language(self):
        sample = u"""<article xml:lang="pt">
                       <sub-article xml:lang="en" article-type="translation" id="S01">
                       </sub-article>
                       <sub-article xml:lang="es" article-type="translation" id="S02">
                       </sub-article>
                    </article>
                 """
        fp = io.BytesIO(sample.encode('utf-8'))
        et = etree.parse(fp)

        gen = domain.HTMLGenerator.parse(et, valid_only=False)

        self.assertRaises(ValueError, lambda: gen.generate('ru'))

