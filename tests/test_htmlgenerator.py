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

    def test_no_abstract_title_if_there_is_a_title_for_abstract(self):
        sample = u"""<article
                      xmlns:mml="http://www.w3.org/1998/Math/MathML"
                      xmlns:xlink="http://www.w3.org/1999/xlink"
                      xml:lang="en">
                      <front>
                        <article-meta>
                          <abstract>
                            <title>Abstract</title>
                            <p>Abstract Content</p>
                          </abstract>
                        </article-meta>
                      </front>
                    </article>"""

        fp = io.BytesIO(sample.encode('utf-8'))
        et = etree.parse(fp)

        html = domain.HTMLGenerator.parse(et, valid_only=False).generate('en')

        title_tags = html.findall('//h1[@class="articleSectionTitle"]')
        self.assertEqual(len(title_tags), 1)
        self.assertEqual(title_tags[0].text, "Abstract")

    def test_abstract_title_if_no_title_for_abstract(self):
        sample = u"""<article
                      xmlns:mml="http://www.w3.org/1998/Math/MathML"
                      xmlns:xlink="http://www.w3.org/1999/xlink"
                      xml:lang="en">
                      <front>
                        <article-meta>
                          <abstract>
                            <p>Abstract Content</p>
                          </abstract>
                        </article-meta>
                      </front>
                    </article>"""

        fp = io.BytesIO(sample.encode('utf-8'))
        et = etree.parse(fp)

        html = domain.HTMLGenerator.parse(et, valid_only=False).generate('en')

        title_tags = html.findall('//h1[@class="articleSectionTitle"]')
        self.assertEqual(len(title_tags), 1)
        self.assertEqual(title_tags[0].text, "Abstract")

    def test_no_abstract_title_if_there_are_titles_for_abstracts(self):
        sample = u"""<article
                      xmlns:mml="http://www.w3.org/1998/Math/MathML"
                      xmlns:xlink="http://www.w3.org/1999/xlink"
                      xml:lang="en">
                      <front>
                        <article-meta>
                          <abstract>
                            <title>Abstract</title>
                            <p>Abstract Content</p>
                          </abstract>
                          <trans-abstract xml:lang="es">
                            <title>Resumen</title>
                            <p>Contenido del Resumen</p>
                          </trans-abstract>
                        </article-meta>
                      </front>
                      <sub-article article-type="translation" xml:lang="pt">
                        <front-stub>
                          <abstract>
                            <title>Resumo</title>
                            <p>Conteúdo do Resumo</p>
                          </abstract>
                        </front-stub>
                      </sub-article>
                    </article>"""

        fp = io.BytesIO(sample.encode('utf-8'))
        et = etree.parse(fp)

        html = domain.HTMLGenerator.parse(et, valid_only=False).generate('en')

        title_tags = html.findall('//h1[@class="articleSectionTitle"]')
        self.assertEqual(len(title_tags), 3)
        self.assertEqual(
            {title_tag.text for title_tag in title_tags},
            set(["Abstract", "Resumen", "Resumo"])
        )

    def test_abstract_title_if_no_titles_for_abstracts(self):
        sample = u"""<article
                      xmlns:mml="http://www.w3.org/1998/Math/MathML"
                      xmlns:xlink="http://www.w3.org/1999/xlink"
                      xml:lang="en">
                      <front>
                        <article-meta>
                          <abstract>
                            <p>Abstract Content</p>
                          </abstract>
                          <trans-abstract xml:lang="es">
                            <p>Contenido del Resumen</p>
                          </trans-abstract>
                        </article-meta>
                      </front>
                      <sub-article article-type="translation" xml:lang="pt">
                        <front-stub>
                          <abstract>
                            <p>Conteúdo do Resumo</p>
                          </abstract>
                        </front-stub>
                      </sub-article>
                    </article>"""

        fp = io.BytesIO(sample.encode('utf-8'))
        et = etree.parse(fp)

        html = domain.HTMLGenerator.parse(et, valid_only=False).generate('en')

        title_tags = html.findall('//h1[@class="articleSectionTitle"]')
        self.assertEqual(len(title_tags), 1)
        self.assertEqual(title_tags[0].text, "Abstracts")

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

    def test_show_retraction_box_if_article_is_an_retraction(self):
      sample = u"""<article article-type="retraction" dtd-version="1.1"
        specific-use="sps-1.8" xml:lang="pt"
        xmlns:mml="http://www.w3.org/1998/Math/MathML"
        xmlns:xlink="http://www.w3.org/1999/xlink">
        <front>
          <article-meta>
            <article-id pub-id-type="doi">10.1590/2236-8906-34/2018-retratacao</article-id>
            <related-article ext-link-type="doi" id="r01" related-article-type="retracted-article"
              xlink:href="10.1590/2236-8906-34/2018"/>
          </article-meta>
        </front>
      </article>"""

      fp = io.BytesIO(sample.encode('utf-8'))
      et = etree.parse(fp)
      html = domain.HTMLGenerator.parse(et, valid_only=False).generate('pt')
      html_string = etree.tostring(html, encoding='unicode', method='html')

      self.assertIn(u'Esta retratação retrata o documento', html_string)
      self.assertIn(
        u'<ul><li><a href="https://doi.org/10.1590/2236-8906-34/2018" target="_blank">10.1590/2236-8906-34/2018</a></li>',
        html_string
      )

    def test_should_translate_retraction_to_english(self):
      sample = u"""<article article-type="retraction" dtd-version="1.1"
        specific-use="sps-1.8" xml:lang="en"
        xmlns:mml="http://www.w3.org/1998/Math/MathML"
        xmlns:xlink="http://www.w3.org/1999/xlink">
        <front>
          <article-meta>
            <article-id pub-id-type="doi">10.1590/2236-8906-34/2018-retratacao</article-id>
            <related-article ext-link-type="doi" id="r01" related-article-type="retracted-article"
              xlink:href="10.1590/2236-8906-34/2018"/>
          </article-meta>
        </front>
      </article>"""

      fp = io.BytesIO(sample.encode('utf-8'))
      et = etree.parse(fp)
      html = domain.HTMLGenerator.parse(et, valid_only=False).generate('en')
      html_string = etree.tostring(html, encoding='unicode', method='html')

      self.assertIn(u'This retraction retracts the following document', html_string)

    def test_do_not_show_retraction_box_if_article_is_not_a_retraction(self):
        sample = u"""<article article-type="research-article" dtd-version="1.1"
          specific-use="sps-1.8" xml:lang="pt"
          xmlns:mml="http://www.w3.org/1998/Math/MathML"
          xmlns:xlink="http://www.w3.org/1999/xlink">
          <front>
            <article-meta>
              <article-id pub-id-type="doi">10.1590/2236-8906-34/2018-retratacao</article-id>
              <related-article ext-link-type="doi" id="r01" related-article-type="retracted-article"
                xlink:href="10.1590/2236-8906-34/2018"/>
            </article-meta>
          </front>
        </article>"""

        fp = io.BytesIO(sample.encode('utf-8'))
        et = etree.parse(fp)
        html = domain.HTMLGenerator.parse(et, valid_only=False).generate('pt')
        html_string = etree.tostring(html, encoding='unicode', method='html')

        self.assertNotIn(u'This retraction retracts the following document', html_string)

    def test_show_retraction_box_if_article_is_an_partial_retraction(self):
      sample = u"""<article article-type="partial-retraction" dtd-version="1.1"
        specific-use="sps-1.8" xml:lang="pt"
        xmlns:mml="http://www.w3.org/1998/Math/MathML"
        xmlns:xlink="http://www.w3.org/1999/xlink">
        <front>
          <article-meta>
            <article-id pub-id-type="doi">10.1590/2236-8906-34/2018-retratacao</article-id>
            <related-article ext-link-type="doi" id="r01" related-article-type="partial-retraction"
              xlink:href="10.1590/2236-8906-34/2018"/>
          </article-meta>
        </front>
      </article>"""

      fp = io.BytesIO(sample.encode('utf-8'))
      et = etree.parse(fp)
      html = domain.HTMLGenerator.parse(et, valid_only=False).generate('pt')
      html_string = etree.tostring(html, encoding='unicode', method='html')

      self.assertIn(u'Esta retratação retrata o documento', html_string)
      self.assertIn(
        u'<ul><li><a href="https://doi.org/10.1590/2236-8906-34/2018" target="_blank">10.1590/2236-8906-34/2018</a></li>',
        html_string
      )

    def test_presents_link_to_retreted_document_using_pid(self):
      sample = u"""<article article-type="partial-retraction" dtd-version="1.1"
        specific-use="sps-1.8" xml:lang="pt"
        xmlns:mml="http://www.w3.org/1998/Math/MathML"
        xmlns:xlink="http://www.w3.org/1999/xlink">
        <front>
          <article-meta>
            <article-id pub-id-type="doi">10.1590/2236-8906-34/2018-retratacao</article-id>
            <related-article ext-link-type="scielo-pid" id="r01" related-article-type="partial-retraction"
              xlink:href="S0864-34662016000200003"/>
          </article-meta>
        </front>
      </article>"""

      fp = io.BytesIO(sample.encode('utf-8'))
      et = etree.parse(fp)
      html = domain.HTMLGenerator.parse(et, valid_only=False).generate('pt')
      html_string = etree.tostring(html, encoding='unicode', method='html')

      self.assertIn(u'Esta retratação retrata o documento', html_string)
      self.assertIn(
        u'<ul><li><a href="/article/S0864-34662016000200003" target="_blank">S0864-34662016000200003</a></li>',
        html_string
      )

    def test_presents_link_to_retreted_document_using_aid(self):
      sample = u"""<article article-type="partial-retraction" dtd-version="1.1"
        specific-use="sps-1.8" xml:lang="pt"
        xmlns:mml="http://www.w3.org/1998/Math/MathML"
        xmlns:xlink="http://www.w3.org/1999/xlink">
        <front>
          <article-meta>
            <article-id pub-id-type="doi">10.1590/2236-8906-34/2018-retratacao</article-id>
            <related-article ext-link-type="scielo-aid" id="r01" related-article-type="partial-retraction"
              xlink:href="12345567799"/>
          </article-meta>
        </front>
      </article>"""

      fp = io.BytesIO(sample.encode('utf-8'))
      et = etree.parse(fp)
      html = domain.HTMLGenerator.parse(et, valid_only=False).generate('pt')
      html_string = etree.tostring(html, encoding='unicode', method='html')

      self.assertIn(u'Esta retratação retrata o documento', html_string)
      self.assertIn(
        u'<ul><li><a href="/article/12345567799" target="_blank">12345567799</a></li>',
        html_string
      )

    def test_presents_in_how_to_cite_collab_and_et_al_if_contrib_quantity_is_greater_than_3(self):
      sample = u"""<article article-type="partial-retraction" dtd-version="1.1"
        specific-use="sps-1.8" xml:lang="pt"
        xmlns:mml="http://www.w3.org/1998/Math/MathML"
        xmlns:xlink="http://www.w3.org/1999/xlink">
        <front>
          <article-meta>
            <article-id pub-id-type="doi">10.1590/2175-7860201869402</article-id>
            <article-categories>
                    <subj-group subj-group-type="heading">
                            <subject>GSPC - Global Strategy for Plant Conservation</subject>
                    </subj-group>
            </article-categories>
            <title-group>
                    <article-title>Brazilian Flora 2020: Innovation and collaboration to meet Target 1 of the Global Strategy for Plant Conservation (GSPC)</article-title>
            </title-group>
            <contrib-group>
                    <contrib contrib-type="author">
                            <collab>The Brazil Flora Group</collab>
                            <xref ref-type="aff" rid="aff1"/>
                    </contrib>
                    <contrib contrib-type="author">
                            <name>
                                    <surname>Filardi</surname>
                                    <given-names>Fabiana L. Ranzato</given-names>
                            </name>
                            <xref ref-type="aff" rid="aff1"/>
                            <xref ref-type="corresp" rid="c1">1</xref>
                    </contrib>
                    <contrib contrib-type="author">
                            <name>
                                    <surname>Barros</surname>
                                    <given-names>Fábio de</given-names>
                            </name>
                            <xref ref-type="aff" rid="aff1"/>
                    </contrib>
                    <contrib contrib-type="author">
                            <name>
                                    <surname>Bicudo</surname>
                                    <given-names>Carlos E.M.</given-names>
                            </name>
                            <xref ref-type="aff" rid="aff1"/>
                    </contrib>
                    <contrib contrib-type="author">
                            <name>
                                    <surname>Cavalcanti</surname>
                                    <given-names>Taciana B.</given-names>
                            </name>
                            <xref ref-type="aff" rid="aff1"/>
                    </contrib>
            </contrib-group>
            <author-notes>
                    <corresp id="c1">
                            <label>1</label>Author for correspondence: <email>rafaela@jbrj.gov.br</email>, <email>floradobrasil2020@jbrj.gov.br</email>
                    </corresp>
                    <fn fn-type="edited-by">
                            <p>Editor de área: Dr. Renato Pereira</p>
                    </fn>
            </author-notes>
            <pub-date pub-type="epub-ppub">
                    <season>Oct-Dec</season>
                    <year>2018</year>
            </pub-date>
            <volume>69</volume>
            <issue>04</issue>
            <fpage>1513</fpage>
            <lpage>1527</lpage>
          </article-meta>
        </front>
      </article>"""
      fp = io.BytesIO(sample.encode('utf-8'))
      et = etree.parse(fp)
      html = domain.HTMLGenerator.parse(et, valid_only=False).generate('pt')
      html_string = etree.tostring(html, encoding='unicode', method='html')
      self.assertIn(
        u'The Brazil Flora Group et al',
        html_string
      )

    def test_article_meta_doi_should_be_an_explicit_link(self):
      sample = u"""<article article-type="research-article" dtd-version="1.1"
        specific-use="sps-1.8" xml:lang="en"
        xmlns:xlink="http://www.w3.org/1999/xlink">
        <front>
          <article-meta>
            <article-id pub-id-type="doi">10.1590/r</article-id>
          </article-meta>
        </front>
      </article>"""
      fp = io.BytesIO(sample.encode("utf-8"))
      et = etree.parse(fp)
      html = domain.HTMLGenerator.parse(et, valid_only=False).generate("en")
      html_string = etree.tostring(html, encoding="unicode", method="html")

      article_header_dois = html.xpath("//span[contains(@class, 'group-doi')]//a[contains(@class, '_doi')]")
      self.assertEquals(len(article_header_dois), 1)


class HTMLGeneratorDispFormulaTests(unittest.TestCase):
    def setUp(self):
        self.sample = u"""<article article-type="research-article" dtd-version="1.1"
        specific-use="sps-1.8" xml:lang="pt"
        xmlns:mml="http://www.w3.org/1998/Math/MathML"
        xmlns:xlink="http://www.w3.org/1999/xlink">
        <front>
          <article-meta>
            <article-id pub-id-type="doi">10.1590/2175-7860201869402</article-id>
            <title-group>
                <article-title>
                    Article Title
                </article-title>
            </title-group>
            <pub-date pub-type="epub-ppub">
                <season>Oct-Dec</season>
                <year>2018</year>
            </pub-date>
            <supplementary-material mimetype="application"
                                    mime-subtype="tiff"
                                    xlink:href="1234-5678-rctb-45-05-0110-suppl02.tif"/>
          </article-meta>
        </front>
          <body>
            <sec>
              <p>The Eh measurements... <xref ref-type="disp-formula" rid="e01">equation 1</xref>(in mV):</p>
              {graphic1}
              <p>We also used an... {graphic2}.</p>
            </sec>
          </body>
      </article>"""

    def test_graphic_images_alternatives_must_prioritize_scielo_web_in_disp_formula(self):
        graphic1 = """
        <disp-formula id="e01">
            <alternatives>
                <graphic xlink:href="1234-5678-rctb-45-05-0110-e01.tif" />
                <graphic specific-use="scielo-web" xlink:href="1234-5678-rctb-45-05-0110-e01.png" />
                <graphic specific-use="scielo-web" content-type="scielo-20x20" xlink:href="1234-5678-rctb-45-05-0110-e01.thumbnail.jpg" />
            </alternatives>
        </disp-formula>
        """
        graphic2 = '<alternatives><inline-graphic xlink:href="1234-5678-rctb-45-05-0110-e02.tiff" /><inline-graphic specific-use="scielo-web" xlink:href="1234-5678-rctb-45-05-0110-e02.png" /></alternatives>'
        fp = io.BytesIO(
            self.sample.format(graphic1=graphic1, graphic2=graphic2).encode('utf-8')
        )
        et = etree.parse(fp)
        html = domain.HTMLGenerator.parse(et, valid_only=False).generate('pt')
        self.assertIsNotNone(
            html.find(
                '//div[@class="formula-container"]//img[@src="1234-5678-rctb-45-05-0110-e01.png"]'
            )
        )
        self.assertIsNotNone(
            html.find('//p//img[@src="1234-5678-rctb-45-05-0110-e02.png"]')
        )

    def test_graphic_tiff_image_href_must_be_replaces_by_jpeg_file_extension_in_disp_formula(self):
        graphic1 = """
        <disp-formula id="e01">
            <graphic xlink:href="1234-5678-rctb-45-05-0110-e01.tif" />
        </disp-formula>
        """
        graphic2 = '<inline-graphic xlink:href="1234-5678-rctb-45-05-0110-e02.tiff"/>'
        fp = io.BytesIO(
            self.sample.format(graphic1=graphic1, graphic2=graphic2).encode('utf-8')
        )
        et = etree.parse(fp)
        html = domain.HTMLGenerator.parse(et, valid_only=False).generate('pt')
        self.assertIsNotNone(
            html.find(
                '//div[@class="formula-container"]//img[@src="1234-5678-rctb-45-05-0110-e01.jpg"]'
            )
        )
        self.assertIsNotNone(
            html.find('//p//img[@src="1234-5678-rctb-45-05-0110-e02.jpg"]')
        )

    def test_graphic_images_alternatives_must_prioritize_scielo_web_and_content_type_in_fig_when_thumb(self):
        graphic1 = """
        <fig id="e01">
            <alternatives>
                <graphic xlink:href="1234-5678-rctb-45-05-0110-e01.tif" />
                <graphic specific-use="scielo-web" xlink:href="1234-5678-rctb-45-05-0110-e01.png" />
                <graphic specific-use="scielo-web" content-type="scielo-20x20" xlink:href="1234-5678-rctb-45-05-0110-e01.thumbnail.jpg" />
            </alternatives>
        </fig>
        """
        graphic2 = '<alternatives><inline-graphic xlink:href="1234-5678-rctb-45-05-0110-e02.tiff" /><inline-graphic specific-use="scielo-web" xlink:href="1234-5678-rctb-45-05-0110-e02.png" /></alternatives>'
        fp = io.BytesIO(
            self.sample.format(graphic1=graphic1, graphic2=graphic2).encode('utf-8')
        )
        et = etree.parse(fp)
        html = domain.HTMLGenerator.parse(et, valid_only=False).generate('pt')
        thumb_tag = html.xpath(
            '//div[@class="articleSection"]/div[@class="row fig"]//a[@data-toggle="modal"]/'
            'div[@class="thumb" and @style="background-image: url(1234-5678-rctb-45-05-0110-e01.thumbnail.jpg);"]'
        )
        self.assertTrue(len(thumb_tag) > 0
          )

    def test_graphic_images_alternatives_must_prioritize_scielo_web_attribute_in_modal(self):
        graphic1 = """
        <fig id="e01">
            <alternatives>
                <graphic xlink:href="1234-5678-rctb-45-05-0110-e01.png" />
                <graphic xlink:href="1234-5678-rctb-45-05-0110-e03.png" specific-use="scielo-web" />
                <graphic specific-use="scielo-web" content-type="scielo-20x20" xlink:href="1234-5678-rctb-45-05-0110-e01.thumbnail.jpg" />
            </alternatives>
        </fig>
        """
        graphic2 = '<alternatives><inline-graphic xlink:href="1234-5678-rctb-45-05-0110-e02.png" /></alternatives>'
        fp = io.BytesIO(
            self.sample.format(graphic1=graphic1, graphic2=graphic2).encode('utf-8')
        )
        et = etree.parse(fp)
        html = domain.HTMLGenerator.parse(et, valid_only=False).generate('pt')
        thumb_tag = html.xpath(
            '//div[@id="ModalFige01"]//img[@src="1234-5678-rctb-45-05-0110-e03.png"]'
        )
        self.assertTrue(len(thumb_tag) > 0)


    def test_graphic_images_alternatives_must_get_first_graphic_in_modal_when_not_scielo_web_and_not_content_type_atribute(self):
        graphic1 = """
        <fig id="e01">
            <alternatives>
                <graphic xlink:href="1234-5678-rctb-45-05-0110-e01.png"/>
                <graphic specific-use="scielo-web" content-type="scielo-20x20" xlink:href="1234-5678-rctb-45-05-0110-e01.thumbnail.jpg" />
            </alternatives>
        </fig>
        """
        graphic2 = '<alternatives><inline-graphic xlink:href="1234-5678-rctb-45-05-0110-e02.png" /></alternatives>'
        fp = io.BytesIO(
            self.sample.format(graphic1=graphic1, graphic2=graphic2).encode('utf-8')
        )
        et = etree.parse(fp)
        html = domain.HTMLGenerator.parse(et, valid_only=False).generate('pt')
        thumb_tag = html.xpath(
            '//div[@id="ModalFige01"]//img[@src="1234-5678-rctb-45-05-0110-e01.png"]'
        )
        self.assertTrue(len(thumb_tag) > 0)

    def test_graphic_tiff_image_href_must_be_replaces_by_jpeg_file_extension_in_fig(self):
        graphic1 = """
        <fig id="e01">
            <graphic xlink:href="1234-5678-rctb-45-05-0110-e01.tif" />
        </fig>
        """
        graphic2 = '<inline-graphic xlink:href="1234-5678-rctb-45-05-0110-e02.tiff"/>'
        fp = io.BytesIO(
            self.sample.format(graphic1=graphic1, graphic2=graphic2).encode('utf-8')
        )
        et = etree.parse(fp)
        html = domain.HTMLGenerator.parse(et, valid_only=False).generate('pt')
        thumb_tag = html.xpath(
            '//div[@class="articleSection"]/div[@class="row fig"]//a[@data-toggle="modal"]/'
            'div[@class="thumb" and @style="background-image: url(1234-5678-rctb-45-05-0110-e01.jpg);"]'
        )
        self.assertTrue(len(thumb_tag) > 0)

    def test_graphic_images_alternatives_must_prioritize_scielo_web_in_modal_disp_formula(self):
        graphic1 = """
        <disp-formula id="e01">
            <alternatives>
                <graphic xlink:href="1234-5678-rctb-45-05-0110-e01.tif" />
                <graphic specific-use="scielo-web" xlink:href="1234-5678-rctb-45-05-0110-e01.png" />
                <graphic specific-use="scielo-web" content-type="scielo-20x20" xlink:href="1234-5678-rctb-45-05-0110-e01.thumbnail.jpg" />
            </alternatives>
        </disp-formula>
        """
        graphic2 = '<inline-graphic xlink:href="1234-5678-rctb-45-05-0110-e02.tiff"/>'
        fp = io.BytesIO(
            self.sample.format(graphic1=graphic1, graphic2=graphic2).encode('utf-8')
        )
        et = etree.parse(fp)
        html = domain.HTMLGenerator.parse(et, valid_only=False).generate('pt')
        modal_body = html.find(
            '//div[@class="modal-body"]/img[@src="1234-5678-rctb-45-05-0110-e01.png"]'
        )
        self.assertIsNotNone(modal_body)

    def test_graphic_tiff_image_href_must_be_replaces_by_jpeg_file_extension_in_modal_disp_formula(self):
        graphic1 = """
        <disp-formula id="e01">
            <graphic xlink:href="1234-5678-rctb-45-05-0110-e01.tif" />
        </disp-formula>
        """
        graphic2 = '<inline-graphic xlink:href="1234-5678-rctb-45-05-0110-e02.tiff"/>'
        fp = io.BytesIO(
            self.sample.format(graphic1=graphic1, graphic2=graphic2).encode('utf-8')
        )
        et = etree.parse(fp)
        html = domain.HTMLGenerator.parse(et, valid_only=False).generate('pt')
        modal_body = html.find(
            '//div[@class="modal-body"]/img[@src="1234-5678-rctb-45-05-0110-e01.jpg"]'
        )
        self.assertIsNotNone(modal_body)

    def test_graphic_images_alternatives_must_prioritize_scielo_web_in_modal_fig(self):
        graphic1 = """
        <fig id="e01">
            <alternatives>
                <graphic xlink:href="1234-5678-rctb-45-05-0110-e01.tif" />
                <graphic specific-use="scielo-web" xlink:href="1234-5678-rctb-45-05-0110-e01.png" />
                <graphic specific-use="scielo-web" content-type="scielo-20x20" xlink:href="1234-5678-rctb-45-05-0110-e01.thumbnail.jpg" />
            </alternatives>
        </fig>
        """
        graphic2 = '<inline-graphic xlink:href="1234-5678-rctb-45-05-0110-e02.tiff"/>'
        fp = io.BytesIO(
            self.sample.format(graphic1=graphic1, graphic2=graphic2).encode('utf-8')
        )
        et = etree.parse(fp)
        html = domain.HTMLGenerator.parse(et, valid_only=False).generate('pt')
        modal_body = html.find(
            '//div[@class="modal-body"]/img[@src="1234-5678-rctb-45-05-0110-e01.png"]'
        )
        self.assertIsNotNone(modal_body)

    def test_graphic_tiff_image_href_must_be_replaces_by_jpeg_file_extension_in_modal_fig(self):
        graphic1 = """
        <fig id="e01">
            <graphic xlink:href="1234-5678-rctb-45-05-0110-e01.tif" />
        </fig>
        """
        graphic2 = '<inline-graphic xlink:href="1234-5678-rctb-45-05-0110-e02.tiff"/>'
        fp = io.BytesIO(
            self.sample.format(graphic1=graphic1, graphic2=graphic2).encode('utf-8')
        )
        et = etree.parse(fp)
        html = domain.HTMLGenerator.parse(et, valid_only=False).generate('pt')
        modal_body = html.find(
            '//div[@class="modal-body"]/img[@src="1234-5678-rctb-45-05-0110-e01.jpg"]'
        )
        self.assertIsNotNone(modal_body)

    def test_graphic_images_alternatives_must_prioritize_scielo_web_in_modal_table_wrap(self):
        graphic1 = """
        <table-wrap id="e01">
            <alternatives>
                <graphic xlink:href="1234-5678-rctb-45-05-0110-e01.tif" />
                <graphic specific-use="scielo-web" xlink:href="1234-5678-rctb-45-05-0110-e01.png" />
                <graphic specific-use="scielo-web" content-type="scielo-20x20" xlink:href="1234-5678-rctb-45-05-0110-e01.thumbnail.jpg" />
            </alternatives>
        </table-wrap>
        """
        graphic2 = '<inline-graphic xlink:href="1234-5678-rctb-45-05-0110-e02.tiff"/>'
        fp = io.BytesIO(
            self.sample.format(graphic1=graphic1, graphic2=graphic2).encode('utf-8')
        )
        et = etree.parse(fp)
        html = domain.HTMLGenerator.parse(et, valid_only=False).generate('pt')
        modal_body = html.find(
            '//div[@class="modal-body"]/img[@src="1234-5678-rctb-45-05-0110-e01.png"]'
        )
        self.assertIsNotNone(modal_body)

    def test_graphic_tiff_image_href_must_be_replaces_by_jpeg_file_extension_in_modal_table_wrap(self):
        graphic1 = """
        <table-wrap id="e01">
            <graphic xlink:href="1234-5678-rctb-45-05-0110-e01.tif" />
        </table-wrap>
        """
        graphic2 = '<inline-graphic xlink:href="1234-5678-rctb-45-05-0110-e02.tiff"/>'
        fp = io.BytesIO(
            self.sample.format(graphic1=graphic1, graphic2=graphic2).encode('utf-8')
        )
        et = etree.parse(fp)
        html = domain.HTMLGenerator.parse(et, valid_only=False).generate('pt')
        modal_body = html.find(
            '//div[@class="modal-body"]/img[@src="1234-5678-rctb-45-05-0110-e01.jpg"]'
        )
        self.assertIsNotNone(modal_body)


class HTMLGeneratorFigTests(unittest.TestCase):
    def setUp(self):
        self.sample = u"""<article article-type="research-article" dtd-version="1.1"
        specific-use="sps-1.8" xml:lang="pt"
        xmlns:mml="http://www.w3.org/1998/Math/MathML"
        xmlns:xlink="http://www.w3.org/1999/xlink">
        <front>
          <article-meta>
            <article-id pub-id-type="doi">10.1590/2175-7860201869402</article-id>
            <title-group>
                <article-title>
                    Article Title
                </article-title>
            </title-group>
            <pub-date pub-type="epub-ppub">
                <season>Oct-Dec</season>
                <year>2018</year>
            </pub-date>
            <supplementary-material mimetype="application"
                                    mime-subtype="tiff"
                                    xlink:href="1234-5678-rctb-45-05-0110-suppl02.tif"/>
          </article-meta>
        </front>
          <body>
            <sec>
              <p>The Eh measurements... <xref ref-type="disp-formula" rid="e01">equation 1</xref>(in mV):</p>
              {graphic1}
              <p>We also used an... {graphic2}.</p>
            </sec>
          </body>
      </article>"""

    def test_graphic_images_alternatives_must_prioritize_scielo_web_and_content_type_in_fig_when_thumb(self):
        graphic1 = """
        <fig id="e01">
            <alternatives>
                <graphic xlink:href="1234-5678-rctb-45-05-0110-e01.tif" />
                <graphic specific-use="scielo-web" xlink:href="1234-5678-rctb-45-05-0110-e01.png" />
                <graphic specific-use="scielo-web" content-type="scielo-20x20" xlink:href="1234-5678-rctb-45-05-0110-e01.thumbnail.jpg" />
            </alternatives>
        </fig>
        """
        graphic2 = '<alternatives><inline-graphic xlink:href="1234-5678-rctb-45-05-0110-e02.tiff" /><inline-graphic specific-use="scielo-web" xlink:href="1234-5678-rctb-45-05-0110-e02.png" /></alternatives>'
        fp = io.BytesIO(
            self.sample.format(graphic1=graphic1, graphic2=graphic2).encode('utf-8')
        )
        et = etree.parse(fp)
        html = domain.HTMLGenerator.parse(et, valid_only=False).generate('pt')
        thumb_tag = html.xpath(
            '//div[@class="articleSection"]/div[@class="row fig"]//a[@data-toggle="modal"]/'
            'div[@class="thumb" and @style="background-image: url(1234-5678-rctb-45-05-0110-e01.thumbnail.jpg);"]'
        )
        self.assertTrue(len(thumb_tag) > 0
          )

    def test_graphic_images_alternatives_must_prioritize_scielo_web_attribute_in_modal(self):
        graphic1 = """
        <fig id="e01">
            <alternatives>
                <graphic xlink:href="1234-5678-rctb-45-05-0110-e01.png" />
                <graphic xlink:href="1234-5678-rctb-45-05-0110-e03.png" specific-use="scielo-web" />
                <graphic specific-use="scielo-web" content-type="scielo-20x20" xlink:href="1234-5678-rctb-45-05-0110-e01.thumbnail.jpg" />
            </alternatives>
        </fig>
        """
        graphic2 = '<alternatives><inline-graphic xlink:href="1234-5678-rctb-45-05-0110-e02.png" /></alternatives>'
        fp = io.BytesIO(
            self.sample.format(graphic1=graphic1, graphic2=graphic2).encode('utf-8')
        )
        et = etree.parse(fp)
        html = domain.HTMLGenerator.parse(et, valid_only=False).generate('pt')
        thumb_tag = html.xpath(
            '//div[@id="ModalFige01"]//img[@src="1234-5678-rctb-45-05-0110-e03.png"]'
        )
        self.assertTrue(len(thumb_tag) > 0)


    def test_graphic_images_alternatives_must_get_first_graphic_in_modal_when_not_scielo_web_and_not_content_type_atribute(self):
        graphic1 = """
        <fig id="e01">
            <alternatives>
                <graphic xlink:href="1234-5678-rctb-45-05-0110-e01.png"/>
                <graphic specific-use="scielo-web" content-type="scielo-20x20" xlink:href="1234-5678-rctb-45-05-0110-e01.thumbnail.jpg" />
            </alternatives>
        </fig>
        """
        graphic2 = '<alternatives><inline-graphic xlink:href="1234-5678-rctb-45-05-0110-e02.png" /></alternatives>'
        fp = io.BytesIO(
            self.sample.format(graphic1=graphic1, graphic2=graphic2).encode('utf-8')
        )
        et = etree.parse(fp)
        html = domain.HTMLGenerator.parse(et, valid_only=False).generate('pt')
        thumb_tag = html.xpath(
            '//div[@id="ModalFige01"]//img[@src="1234-5678-rctb-45-05-0110-e01.png"]'
        )
        self.assertTrue(len(thumb_tag) > 0)

    def test_graphic_tiff_image_href_must_be_replaces_by_jpeg_file_extension_in_fig(self):
        graphic1 = """
        <fig id="e01">
            <graphic xlink:href="1234-5678-rctb-45-05-0110-e01.tif" />
        </fig>
        """
        graphic2 = '<inline-graphic xlink:href="1234-5678-rctb-45-05-0110-e02.tiff"/>'
        fp = io.BytesIO(
            self.sample.format(graphic1=graphic1, graphic2=graphic2).encode('utf-8')
        )
        et = etree.parse(fp)
        html = domain.HTMLGenerator.parse(et, valid_only=False).generate('pt')
        thumb_tag = html.xpath(
            '//div[@class="articleSection"]/div[@class="row fig"]//a[@data-toggle="modal"]/'
            'div[@class="thumb" and @style="background-image: url(1234-5678-rctb-45-05-0110-e01.jpg);"]'
        )
        self.assertTrue(len(thumb_tag) > 0)

    def test_graphic_images_alternatives_must_prioritize_scielo_web_in_modal_fig(self):
        graphic1 = """
        <fig id="e01">
            <alternatives>
                <graphic xlink:href="1234-5678-rctb-45-05-0110-e01.tif" />
                <graphic specific-use="scielo-web" xlink:href="1234-5678-rctb-45-05-0110-e01.png" />
                <graphic specific-use="scielo-web" content-type="scielo-20x20" xlink:href="1234-5678-rctb-45-05-0110-e01.thumbnail.jpg" />
            </alternatives>
        </fig>
        """
        graphic2 = '<inline-graphic xlink:href="1234-5678-rctb-45-05-0110-e02.tiff"/>'
        fp = io.BytesIO(
            self.sample.format(graphic1=graphic1, graphic2=graphic2).encode('utf-8')
        )
        et = etree.parse(fp)
        html = domain.HTMLGenerator.parse(et, valid_only=False).generate('pt')
        modal_body = html.find(
            '//div[@class="modal-body"]/img[@src="1234-5678-rctb-45-05-0110-e01.png"]'
        )
        self.assertIsNotNone(modal_body)

    def test_graphic_tiff_image_href_must_be_replaces_by_jpeg_file_extension_in_modal_fig(self):
        graphic1 = """
        <fig id="e01">
            <graphic xlink:href="1234-5678-rctb-45-05-0110-e01.tif" />
        </fig>
        """
        graphic2 = '<inline-graphic xlink:href="1234-5678-rctb-45-05-0110-e02.tiff"/>'
        fp = io.BytesIO(
            self.sample.format(graphic1=graphic1, graphic2=graphic2).encode('utf-8')
        )
        et = etree.parse(fp)
        html = domain.HTMLGenerator.parse(et, valid_only=False).generate('pt')
        modal_body = html.find(
            '//div[@class="modal-body"]/img[@src="1234-5678-rctb-45-05-0110-e01.jpg"]'
        )
        self.assertIsNotNone(modal_body)

    def test_article_text_alternatives_mode_file_location_thumb_must_choose_graphic_with_xlink_href_not_empty(self):
        graphic1 = """
          <fig id="f01">
            <alternatives>
              <graphic xlink:href=""/>
              <graphic xlink:href="https://minio.scielo.br/documentstore/1678-992X/Wfy9dhFgfVFZgBbxg4WGVQM/a.jpg"/>
              <graphic xlink:href="https://minio.scielo.br/documentstore/1678-992X/Wfy9dhFgfVFZgBbxg4WGVQM/b.jpg"/>
          </alternatives>
          </fig>
          """
        graphic2 = ""
        fp = io.BytesIO(
              self.sample.format(graphic1=graphic1, graphic2=graphic2).encode('utf-8')
          )
        et = etree.parse(fp)
        html = domain.HTMLGenerator.parse(et, valid_only=False).generate('pt')
        thumb_tag = html.xpath(
            '//div[@class="row fig"]'
            '//div[@class="thumb" and @style="background-image: url('
            'https://minio.scielo.br/documentstore/1678-992X/'
            'Wfy9dhFgfVFZgBbxg4WGVQM/a.jpg'
            ');"]'
        )
        self.assertTrue(len(thumb_tag) > 0)

    def test_article_text_alternatives_mode_file_location_thumb_must_choose_graphic_with_scielo_web_and_no_content_type_because_xlink_href_is_empty(self):
        graphic1 = """
          <fig id="f01">
            <alternatives>
                <graphic xlink:href="1234-5678-rctb-45-05-0110-e01.tif" />
                <graphic specific-use="scielo-web" xlink:href="1234-5678-rctb-45-05-0110-e01.png" />
                <graphic specific-use="scielo-web" content-type="scielo-20x20" xlink:href="" />
            </alternatives>
          </fig>
          """
        graphic2 = ""
        fp = io.BytesIO(
              self.sample.format(graphic1=graphic1, graphic2=graphic2).encode('utf-8')
          )
        et = etree.parse(fp)
        html = domain.HTMLGenerator.parse(et, valid_only=False).generate('pt')
        thumb_tag = html.xpath(
            '//div[@class="row fig"]'
            '//div[@class="thumb" and @style="background-image: url('
            '1234-5678-rctb-45-05-0110-e01.png'
            ');"]'
        )
        self.assertTrue(len(thumb_tag) > 0)

    def test_article_text_alternatives_mode_file_location_thumb_must_choose_graphic_with_no_scielo_web_and_no_content_type_because_xlink_href_is_empty(self):
        graphic1 = """
          <fig id="f01">
            <alternatives>
                <graphic xlink:href="1234-5678-rctb-45-05-0110-e01.jpg" />
                <graphic specific-use="scielo-web" xlink:href="" />
                <graphic specific-use="scielo-web" content-type="scielo-20x20" xlink:href="" />
            </alternatives>
          </fig>
          """
        graphic2 = ""
        fp = io.BytesIO(
              self.sample.format(graphic1=graphic1, graphic2=graphic2).encode('utf-8')
          )
        et = etree.parse(fp)
        html = domain.HTMLGenerator.parse(et, valid_only=False).generate('pt')
        thumb_tag = html.xpath(
            '//div[@class="row fig"]'
            '//div[@class="thumb" and @style="background-image: url('
            '1234-5678-rctb-45-05-0110-e01.jpg'
            ');"]'
        )
        self.assertTrue(len(thumb_tag) > 0)

    def test_article_text_alternatives_mode_file_location_thumb_must_choose_graphic_with_no_scielo_web_and_no_content_type_because_xlink_href_is_absent(self):
        graphic1 = """
          <fig id="f01">
            <alternatives>
                <graphic xlink:href="1234-5678-rctb-45-05-0110-e01.jpg" />
                <graphic specific-use="scielo-web" />
                <graphic specific-use="scielo-web" content-type="scielo-20x20" />
            </alternatives>
          </fig>
          """
        graphic2 = ""
        fp = io.BytesIO(
              self.sample.format(graphic1=graphic1, graphic2=graphic2).encode('utf-8')
          )
        et = etree.parse(fp)
        html = domain.HTMLGenerator.parse(et, valid_only=False).generate('pt')
        thumb_tag = html.xpath(
            '//div[@class="row fig"]'
            '//div[@class="thumb" and @style="background-image: url('
            '1234-5678-rctb-45-05-0110-e01.jpg'
            ');"]'
        )
        self.assertTrue(len(thumb_tag) > 0)

    def test_article_text_alternatives_mode_file_location_must_choose_graphic_with_xlink_href_not_empty(self):
        graphic1 = """
          <fig id="f01">
            <alternatives>
              <graphic xlink:href="" />
              <graphic xlink:href="1234-5678-rctb-45-05-0110-e01.png" />
              <graphic xlink:href="1234-5678-rctb-45-05-0110-e01.jpg" />
          </alternatives>
          </fig>
          """
        graphic2 = ""
        fp = io.BytesIO(
              self.sample.format(graphic1=graphic1, graphic2=graphic2).encode('utf-8')
          )
        et = etree.parse(fp)
        html = domain.HTMLGenerator.parse(et, valid_only=False).generate('pt')
        img = html.xpath(
            '//div[@class="modal-body"]/img[@src="'
            '1234-5678-rctb-45-05-0110-e01.png'
            '"]'
        )
        self.assertTrue(len(img) > 0)
        img = html.xpath(
            '//div[@class="modal-body"]/img[@src="'
            '1234-5678-rctb-45-05-0110-e01.jpg'
            '"]'
        )
        self.assertTrue(len(img) == 0)

    def test_article_text_alternatives_chooses_graphic_with_no_scielo_web_and_no_content_type_because_xlink_href_is_empty(self):
        graphic1 = """
          <fig id="f01">
            <alternatives>
                <graphic xlink:href="1234-5678-rctb-45-05-0110-e01.png" />
                <graphic specific-use="scielo-web" xlink:href="" />
                <graphic specific-use="scielo-web" content-type="scielo-20x20" xlink:href="1234-5678-rctb-45-05-0110-e01.jpg" />
            </alternatives>
          </fig>
          """
        graphic2 = ""
        fp = io.BytesIO(
              self.sample.format(graphic1=graphic1, graphic2=graphic2).encode('utf-8')
          )
        et = etree.parse(fp)
        html = domain.HTMLGenerator.parse(et, valid_only=False).generate('pt')
        img_tag = html.xpath(
            '//div[@class="modal-body"]/img[@src="'
            '1234-5678-rctb-45-05-0110-e01.png'
            '"]'
        )
        self.assertTrue(len(img_tag) > 0)

    def test_article_text_alternatives_chooses_graphic_with_no_scielo_web_and_no_content_type_because_xlink_href_is_absent(self):
        graphic1 = """
          <fig id="f01">
            <alternatives>
                <graphic xlink:href="1234-5678-rctb-45-05-0110-e01.jpg" />
                <graphic specific-use="scielo-web" />
            </alternatives>
          </fig>
          """
        graphic2 = ""
        fp = io.BytesIO(
              self.sample.format(graphic1=graphic1, graphic2=graphic2).encode('utf-8')
          )
        et = etree.parse(fp)
        html = domain.HTMLGenerator.parse(et, valid_only=False).generate('pt')
        img_tag = html.xpath(
            '//div[@class="modal-body"]/img[@src="'
            '1234-5678-rctb-45-05-0110-e01.jpg'
            '"]'
        )
        self.assertTrue(len(img_tag) > 0)
