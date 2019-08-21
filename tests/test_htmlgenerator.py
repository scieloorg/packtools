# coding: utf-8
from __future__ import unicode_literals
import unittest
import io
import os
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

SAMPLES_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    'samples')


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

    def test_if_visual_abstract_image_present_in_html(self):
        sample = u"""<article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink" xml:lang="en">
                      <front>
                        <article-meta>
                          <abstract abstract-type="graphical">
                              <title>Visual Abstract</title>
                              <p>
                                  <fig id="vf01">
                                      <caption>
                                          <title>Caption em Inglês</title>
                                      </caption>
                                      <graphic xlink:href="2175-8239-jbn-2018-0058-vf01.jpg"/>
                                  </fig>
                              </p>
                          </abstract>
                        </article-meta>
                      </front>
                    </article>"""

        fp = io.BytesIO(sample.encode('utf-8'))
        et = etree.parse(fp)

        html = domain.HTMLGenerator.parse(et, valid_only=False).generate('en')

        html_string = etree.tostring(html, encoding='unicode', method='html')

        self.assertIn('<img style="max-width:100%" src="2175-8239-jbn-2018-0058-vf01.jpg">', html_string)

    def test_if_visual_abstract_caption_present_in_html(self):
        sample = u"""<article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink" xml:lang="pt">
                      <front>
                        <article-meta>
                          <abstract abstract-type="graphical">
                              <title>Resumo Visual</title>
                              <p>
                                  <fig id="vf01">
                                      <caption>
                                          <title>Caption em Português</title>
                                      </caption>
                                      <graphic xlink:href="2175-8239-jbn-2018-0058-vf01.jpg"/>
                                  </fig>
                              </p>
                          </abstract>
                        </article-meta>
                      </front>
                    </article>"""

        fp = io.BytesIO(sample.encode('utf-8'))
        et = etree.parse(fp)

        html = domain.HTMLGenerator.parse(et, valid_only=False).generate('pt')

        html_string = etree.tostring(html, encoding='unicode', method='html')

        self.assertIn('Caption em Português', html_string)

    def test_if_visual_abstract_anchor_section_present_in_html(self):
        sample = u"""<article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink" xml:lang="pt">
                      <front>
                        <article-meta>
                          <abstract abstract-type="graphical">
                              <title>Resumo Visual</title>
                              <p>
                                  <fig id="vf01">
                                      <caption>
                                          <title>Caption em Português</title>
                                      </caption>
                                      <graphic xlink:href="2175-8239-jbn-2018-0058-vf01.jpg"/>
                                  </fig>
                              </p>
                          </abstract>
                        </article-meta>
                      </front>
                    </article>"""

        fp = io.BytesIO(sample.encode('utf-8'))
        et = etree.parse(fp)

        html = domain.HTMLGenerator.parse(et, valid_only=False).generate('pt')

        html_string = etree.tostring(html, encoding='unicode', method='html')

        self.assertIn('<div class="articleSection" data-anchor="Resumo Visual">', html_string)

    def test_if_visual_abstract_section_present_in_html(self):
        sample = u"""<article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink" xml:lang="pt">
                      <front>
                        <article-meta>
                          <abstract abstract-type="graphical">
                              <title>Resumo Visual</title>
                              <p>
                                  <fig id="vf01">
                                      <caption>
                                          <title>Caption em Português</title>
                                      </caption>
                                      <graphic xlink:href="2175-8239-jbn-2018-0058-vf01.jpg"/>
                                  </fig>
                              </p>
                          </abstract>
                        </article-meta>
                      </front>
                    </article>"""

        fp = io.BytesIO(sample.encode('utf-8'))
        et = etree.parse(fp)

        html = domain.HTMLGenerator.parse(et, valid_only=False).generate('pt')

        html_string = etree.tostring(html, encoding='unicode', method='html')

        self.assertIn('Resumo Visual', html_string)

    def test_if_visual_abstract_image_from_another_language_is_present_in_html(self):
        sample = u"""<article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink" xml:lang="pt">
                      <sub-article article-type="translation" id="s1" xml:lang="en">
                        <front-stub>
                          <abstract abstract-type="graphical">
                              <title>Visual Abstract EN</title>
                              <p>
                                  <fig id="vf01">
                                      <caption>
                                          <title>Caption em Inglês</title>
                                      </caption>
                                      <graphic xlink:href="2175-8239-jbn-2018-0058-vf01-EN.jpg"/>
                                  </fig>
                              </p>
                          </abstract>
                        </front-stub>
                      </sub-article>
                    </article>"""

        fp = io.BytesIO(sample.encode('utf-8'))
        et = etree.parse(fp)

        html = domain.HTMLGenerator.parse(et, valid_only=False).generate('en')

        html_string = etree.tostring(html, encoding='unicode', method='html')

        self.assertIn('<img style="max-width:100%" src="2175-8239-jbn-2018-0058-vf01-EN.jpg">', html_string)

    def test_if_history_section_is_present_in_primary_language(self):
      sample = os.path.join(SAMPLES_PATH, '0034-7094-rba-69-03-0227.xml')
      et = etree.parse(sample)

      html = domain.HTMLGenerator.parse(et, valid_only=False).generate('en')
      html_string = etree.tostring(html, encoding='unicode', method='html')

      self.assertIn('<h1 class="articleSectionTitle">History</h1>', html_string)
      self.assertIn('<strong>Received</strong><br>9 July 2018</li>', html_string)
      self.assertIn('<strong>Accepted</strong><br>14 Jan 2019</li>', html_string)
      self.assertIn('<strong>Published</strong><br>26 Apr 2019</li>', html_string)

    def test_if_history_section_is_present_in_sub_article(self):
      sample = os.path.join(SAMPLES_PATH, '0034-7094-rba-69-03-0227.xml')
      et = etree.parse(sample)

      html = domain.HTMLGenerator.parse(et, valid_only=False).generate('pt')
      html_string = etree.tostring(html, encoding='unicode', method='html')

      self.assertIn('<h1 class="articleSectionTitle">Histórico</h1>', html_string)
      self.assertIn('<strong>Recebido</strong><br>9 Jul 2018</li>', html_string)
      self.assertIn('<strong>Aceito</strong><br>14 Jan 2019</li>', html_string)
      self.assertIn('<strong>Publicado</strong><br>31 Maio 2019</li>', html_string)
