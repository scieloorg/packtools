# coding: utf-8
from __future__ import unicode_literals
import unittest
import io
import os
from tempfile import NamedTemporaryFile
from lxml import etree

from packtools import domain


NAMESPACES = {
    "xlink": "http://www.w3.org/1999/xlink",
}


def _get_ns_attr(node, attr):
    if node is not None:
        ns, attr = attr.split(":")
        ns = "{" + f'{NAMESPACES.get(ns)}' + "}"
        return node.attrib.get(ns + attr)


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


def get_xml_tree_from_string(text='<a><b>bar</b></a>'):
    return etree.parse(io.BytesIO(text.encode('utf-8')))


def get_xml_tree_from_file(filename):
    return etree.parse(os.path.join(SAMPLES_PATH, filename))


class HTMLGeneratorTests(unittest.TestCase):

    @setup_tmpfile
    def test_initializes_with_filepath(self):
        self.assertTrue(domain.HTMLGenerator.parse(self.valid_tmpfile.name, valid_only=False))

    def test_initializes_with_etree(self):
        et = get_xml_tree_from_string('<a><b>bar</b></a>')
        self.assertTrue(domain.HTMLGenerator.parse(et, valid_only=False))

    def test_languages(self):
        sample = u"""<article xml:lang="pt">
                       <sub-article xml:lang="en" article-type="translation" id="S01">
                       </sub-article>
                       <sub-article xml:lang="es" article-type="translation" id="S02">
                       </sub-article>
                    </article>
                 """
        et = get_xml_tree_from_string(sample)
        self.assertEqual(domain.HTMLGenerator.parse(et, valid_only=False).languages, ['pt', 'en', 'es'])

    def test_language(self):
        sample = u"""<article xml:lang="pt">
                       <sub-article xml:lang="en" article-type="translation" id="S01">
                       </sub-article>
                       <sub-article xml:lang="es" article-type="translation" id="S02">
                       </sub-article>
                    </article>
                 """
        et = get_xml_tree_from_string(sample)
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
        et = get_xml_tree_from_string(sample)
        self.assertEqual(domain.HTMLGenerator.parse(
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
        et = get_xml_tree_from_string(sample)

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
        et = get_xml_tree_from_string(sample)

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

        et = get_xml_tree_from_string(sample)

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

        et = get_xml_tree_from_string(sample)

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

        et = get_xml_tree_from_string(sample)

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

        et = get_xml_tree_from_string(sample)

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

        et = get_xml_tree_from_string(sample)

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

        et = get_xml_tree_from_string(sample)

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

        et = get_xml_tree_from_string(sample)

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

        et = get_xml_tree_from_string(sample)

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

        et = get_xml_tree_from_string(sample)

        html = domain.HTMLGenerator.parse(et, valid_only=False).generate('en')

        html_string = etree.tostring(html, encoding='unicode', method='html')

        self.assertIn('<img style="max-width:100%" src="2175-8239-jbn-2018-0058-vf01-EN.jpg">', html_string)

    def test_if_history_section_is_present_in_primary_language(self):

      et = get_xml_tree_from_file('0034-7094-rba-69-03-0227.xml')
      html = domain.HTMLGenerator.parse(et, valid_only=False).generate('en')
      html_string = etree.tostring(html, encoding='unicode', method='html')

      self.assertIn('<h1 class="articleSectionTitle">History</h1>', html_string)
      self.assertIn('<strong>Received</strong><br>9 July 2018</li>', html_string)
      self.assertIn('<strong>Accepted</strong><br>14 Jan 2019</li>', html_string)
      self.assertIn('<strong>Published</strong><br>26 Apr 2019</li>', html_string)

    def test_if_history_section_is_present_in_sub_article(self):
      et = get_xml_tree_from_file('0034-7094-rba-69-03-0227.xml')

      html = domain.HTMLGenerator.parse(et, valid_only=False).generate('pt')
      html_string = etree.tostring(html, encoding='unicode', method='html')

      self.assertIn('<h1 class="articleSectionTitle">Histórico</h1>', html_string)
      self.assertIn('<strong>Recebido</strong><br>9 Jul 2018</li>', html_string)
      self.assertIn('<strong>Aceito</strong><br>14 Jan 2019</li>', html_string)
      self.assertIn('<strong>Publicado</strong><br>31 Maio 2019</li>', html_string)

    @unittest.skip("""A caixa de retratação está sendo gerada pela aplicação, caso deseje que seja gerado pelo XSLT descomentar a linha 24 do arquivo article.xsl""")
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

      et = get_xml_tree_from_string(sample)
      html = domain.HTMLGenerator.parse(et, valid_only=False).generate('pt')
      html_string = etree.tostring(html, encoding='unicode', method='html')

      self.assertIn(u'Esta retratação retrata o documento', html_string)
      self.assertIn(
        u'<ul><li><a href="https://doi.org/10.1590/2236-8906-34/2018" target="_blank">10.1590/2236-8906-34/2018</a></li>',
        html_string
      )

    @unittest.skip("""A caixa de retratação está sendo gerada pela aplicação, caso deseje que seja gerado pelo XSLT descomentar a linha 24 do arquivo article.xsl""")
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
      et = get_xml_tree_from_string(sample)
      html = domain.HTMLGenerator.parse(et, valid_only=False).generate('en')
      html_string = etree.tostring(html, encoding='unicode', method='html')

      self.assertIn(u'This retraction retracts the following document', html_string)

    @unittest.skip("""A caixa de retratação está sendo gerada pela aplicação, caso deseje que seja gerado pelo XSLT descomentar a linha 24 do arquivo article.xsl""")
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

        et = get_xml_tree_from_string(sample)
        html = domain.HTMLGenerator.parse(et, valid_only=False).generate('pt')
        html_string = etree.tostring(html, encoding='unicode', method='html')

        self.assertNotIn(u'This retraction retracts the following document', html_string)

    @unittest.skip("""A caixa de retratação está sendo gerada pela aplicação, caso deseje que seja gerado pelo XSLT descomentar a linha 24 do arquivo article.xsl""")
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

      et = get_xml_tree_from_string(sample)
      html = domain.HTMLGenerator.parse(et, valid_only=False).generate('pt')
      html_string = etree.tostring(html, encoding='unicode', method='html')

      self.assertIn(u'Esta retratação retrata o documento', html_string)
      self.assertIn(
        u'<ul><li><a href="https://doi.org/10.1590/2236-8906-34/2018" target="_blank">10.1590/2236-8906-34/2018</a></li>',
        html_string
      )

    @unittest.skip("""A caixa de retratação está sendo gerada pela aplicação, caso deseje que seja gerado pelo XSLT descomentar a linha 24 do arquivo article.xsl""")
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

      et = get_xml_tree_from_string(sample)
      html = domain.HTMLGenerator.parse(et, valid_only=False).generate('pt')
      html_string = etree.tostring(html, encoding='unicode', method='html')

      self.assertIn(u'Esta retratação retrata o documento', html_string)
      self.assertIn(
        u'<ul><li><a href="/article/S0864-34662016000200003" target="_blank">S0864-34662016000200003</a></li>',
        html_string
      )

    @unittest.skip("""A caixa de retratação está sendo gerada pela aplicação, caso deseje que seja gerado pelo XSLT descomentar a linha 24 do arquivo article.xsl""")
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

      et = get_xml_tree_from_string(sample)
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
      et = get_xml_tree_from_string(sample)
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
      et = get_xml_tree_from_string(sample)
      html = domain.HTMLGenerator.parse(et, valid_only=False).generate("en")
      html_string = etree.tostring(html, encoding="unicode", method="html")

      article_header_dois = html.xpath("//span[contains(@class, 'group-doi')]//a[contains(@class, '_doi')]")
      self.assertEqual(len(article_header_dois), 1)


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
        et = get_xml_tree_from_string(self.sample.format(graphic1=graphic1, graphic2=graphic2))
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
        et = get_xml_tree_from_string(self.sample.format(graphic1=graphic1, graphic2=graphic2))
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
        et = get_xml_tree_from_string(self.sample.format(graphic1=graphic1, graphic2=graphic2))
        html = domain.HTMLGenerator.parse(et, valid_only=False).generate('pt')
        thumb_tag = html.xpath(
            '//div[@class="articleSection"]/div[@class="row fig"]//a[@data-toggle="modal"]/'
            'div[@class="thumbImg"]/img'
        )
        self.assertTrue(len(thumb_tag) > 0)

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
        et = get_xml_tree_from_string(self.sample.format(graphic1=graphic1, graphic2=graphic2))
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
        et = get_xml_tree_from_string(self.sample.format(graphic1=graphic1, graphic2=graphic2))
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
        et = get_xml_tree_from_string(self.sample.format(graphic1=graphic1, graphic2=graphic2))
        html = domain.HTMLGenerator.parse(et, valid_only=False).generate('pt')
        thumb_tag = html.xpath(
            '//div[@class="articleSection"]/div[@class="row fig"]//a[@data-toggle="modal"]/'
            'div[@class="thumbImg"]/img'
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
        et = get_xml_tree_from_string(self.sample.format(graphic1=graphic1, graphic2=graphic2))
        html = domain.HTMLGenerator.parse(et, valid_only=False).generate('pt')
        modal_body = html.find(
            '//div[@class="modal-body"]/a/img[@src="1234-5678-rctb-45-05-0110-e01.png"]'
        )
        self.assertIsNotNone(modal_body)

    def test_graphic_tiff_image_href_must_be_replaces_by_jpeg_file_extension_in_modal_disp_formula(self):
        graphic1 = """
        <disp-formula id="e01">
            <graphic xlink:href="1234-5678-rctb-45-05-0110-e01.tif" />
        </disp-formula>
        """
        graphic2 = '<inline-graphic xlink:href="1234-5678-rctb-45-05-0110-e02.tiff"/>'
        et = get_xml_tree_from_string(self.sample.format(graphic1=graphic1, graphic2=graphic2))
        html = domain.HTMLGenerator.parse(et, valid_only=False).generate('pt')
        modal_body = html.find(
            '//div[@class="modal-body"]/a/img[@src="1234-5678-rctb-45-05-0110-e01.jpg"]'
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
        et = get_xml_tree_from_string(self.sample.format(graphic1=graphic1, graphic2=graphic2))
        html = domain.HTMLGenerator.parse(et, valid_only=False).generate('pt')
        modal_body = html.find(
            '//div[@class="modal-body"]/a//img[@src="1234-5678-rctb-45-05-0110-e01.png"]'
        )
        self.assertIsNotNone(modal_body)

    def test_graphic_tiff_image_href_must_be_replaces_by_jpeg_file_extension_in_modal_fig(self):
        graphic1 = """
        <fig id="e01">
            <graphic xlink:href="1234-5678-rctb-45-05-0110-e01.tif" />
        </fig>
        """
        graphic2 = '<inline-graphic xlink:href="1234-5678-rctb-45-05-0110-e02.tiff"/>'
        et = get_xml_tree_from_string(self.sample.format(graphic1=graphic1, graphic2=graphic2))
        html = domain.HTMLGenerator.parse(et, valid_only=False).generate('pt')
        modal_body = html.find(
            '//div[@class="modal-body"]/a/img[@src="1234-5678-rctb-45-05-0110-e01.jpg"]'
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
        et = get_xml_tree_from_string(self.sample.format(graphic1=graphic1, graphic2=graphic2))
        html = domain.HTMLGenerator.parse(et, valid_only=False).generate('pt')
        modal_body = html.find(
            '//div[@class="modal-body"]/a/img[@src="1234-5678-rctb-45-05-0110-e01.png"]'
        )
        self.assertIsNotNone(modal_body)

    def test_graphic_tiff_image_href_must_be_replaces_by_jpeg_file_extension_in_modal_table_wrap(self):
        graphic1 = """
        <table-wrap id="e01">
            <graphic xlink:href="1234-5678-rctb-45-05-0110-e01.tif" />
        </table-wrap>
        """
        graphic2 = '<inline-graphic xlink:href="1234-5678-rctb-45-05-0110-e02.tiff"/>'
        et = get_xml_tree_from_string(self.sample.format(graphic1=graphic1, graphic2=graphic2))
        html = domain.HTMLGenerator.parse(et, valid_only=False).generate('pt')
        modal_body = html.find(
            '//div[@class="modal-body"]/a/img[@src="1234-5678-rctb-45-05-0110-e01.jpg"]'
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

    def get_xml_tree_from_string(self, graphic1, graphic2):
        return get_xml_tree_from_string(
          self.sample.format(graphic1=graphic1, graphic2=graphic2))

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
        et = self.get_xml_tree_from_string(graphic1=graphic1, graphic2=graphic2)
        html = domain.HTMLGenerator.parse(et, valid_only=False).generate('pt')
        thumb_tag = html.xpath(
            '//div[@class="articleSection"]/div[@class="row fig"]//a[@data-toggle="modal"]/'
            'div[@class="thumbImg"]/img'
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
        et = self.get_xml_tree_from_string(graphic1=graphic1, graphic2=graphic2)
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
        et = self.get_xml_tree_from_string(graphic1=graphic1, graphic2=graphic2)
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
        et = self.get_xml_tree_from_string(graphic1=graphic1, graphic2=graphic2)
        html = domain.HTMLGenerator.parse(et, valid_only=False).generate('pt')
        thumb_tag = html.xpath(
            '//div[@class="articleSection"]/div[@class="row fig"]//a[@data-toggle="modal"]/'
            'div[@class="thumbImg"]/img'
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
        et = self.get_xml_tree_from_string(graphic1=graphic1, graphic2=graphic2)
        html = domain.HTMLGenerator.parse(et, valid_only=False).generate('pt')
        modal_body = html.find(
            '//div[@class="modal-body"]//img[@src="1234-5678-rctb-45-05-0110-e01.png"]'
        )
        self.assertIsNotNone(modal_body)

    def test_graphic_tiff_image_href_must_be_replaces_by_jpeg_file_extension_in_modal_fig(self):
        graphic1 = """
        <fig id="e01">
            <graphic xlink:href="1234-5678-rctb-45-05-0110-e01.tif" />
        </fig>
        """
        graphic2 = '<inline-graphic xlink:href="1234-5678-rctb-45-05-0110-e02.tiff"/>'
        et = self.get_xml_tree_from_string(graphic1=graphic1, graphic2=graphic2)
        html = domain.HTMLGenerator.parse(et, valid_only=False).generate('pt')
        modal_body = html.find(
            '//div[@class="modal-body"]/a/img[@src="1234-5678-rctb-45-05-0110-e01.jpg"]'
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
        et = self.get_xml_tree_from_string(graphic1=graphic1, graphic2=graphic2)
        html = domain.HTMLGenerator.parse(et, valid_only=False).generate('pt')
        thumb_tag = html.xpath(
            '//div[@class="row fig"]'
            '//div[@class="thumbImg"]/img'
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
        et = self.get_xml_tree_from_string(graphic1=graphic1, graphic2=graphic2)
        html = domain.HTMLGenerator.parse(et, valid_only=False).generate('pt')
        thumb_tag = html.xpath(
            '//div[@class="row fig"]'
            '//div[@class="thumbImg"]/img'
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
        et = self.get_xml_tree_from_string(graphic1=graphic1, graphic2=graphic2)
        html = domain.HTMLGenerator.parse(et, valid_only=False).generate('pt')
        thumb_tag = html.xpath(
            '//div[@class="row fig"]'
            '//div[@class="thumbImg"]/img'
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
        et = self.get_xml_tree_from_string(graphic1=graphic1, graphic2=graphic2)
        html = domain.HTMLGenerator.parse(et, valid_only=False).generate('pt')
        thumb_tag = html.xpath(
            '//div[@class="row fig"]'
            '//div[@class="thumbImg"]/img'
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
        et = self.get_xml_tree_from_string(graphic1=graphic1, graphic2=graphic2)
        html = domain.HTMLGenerator.parse(et, valid_only=False).generate('pt')
        img = html.xpath(
            '//div[@class="modal-body"]//img[@src="'
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
        et = self.get_xml_tree_from_string(graphic1=graphic1, graphic2=graphic2)
        html = domain.HTMLGenerator.parse(et, valid_only=False).generate('pt')
        img_tag = html.xpath(
            '//div[@class="modal-body"]//img[@src="'
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
        et = self.get_xml_tree_from_string(graphic1=graphic1, graphic2=graphic2)
        html = domain.HTMLGenerator.parse(et, valid_only=False).generate('pt')
        img_tag = html.xpath(
            '//div[@class="modal-body"]//img[@src="'
            '1234-5678-rctb-45-05-0110-e01.jpg'
            '"]'
        )
        self.assertTrue(len(img_tag) > 0)


def get_html(filename, gs_abstract_lang):
    et = get_xml_tree_from_file(filename)
    return domain.HTMLGenerator.parse(
      et, gs_abstract=True,
      valid_only=False).generate(gs_abstract_lang)


class TestHTMLGeneratorGSAbstractLang(unittest.TestCase):

    def test_generate_html_for_en_abstract(self):
        html = get_html(
          "article-abstract-en-sub-articles-pt-es.xml", "en")
        find_text = (
          'the correlations between these two years were high in all th'
          'e dimensions analyzed. The evaluation of competence progress'
          'ion in the context of clinical practice in nursing universit'
          'y studies allows us to optimize these practices to the maxim'
          'um and establish professional profiles with a greater degree'
          ' of adaptation to the professional future. '
        )
        p_texts = [p.text for p in html.findall('//p')]
        self.assertIn(find_text, p_texts)

    def test_generate_html_for_es_abstract_in_subarticle(self):
        html = get_html(
          "article-abstract-en-sub-articles-pt-es.xml", "es")
        find_text = (
          ' las correlaciones entre estos dos años fueron altas en toda'
          's las dimensiones analizadas. La evaluación de la progresión'
          ' de competencias, en el contexto de la práctica clínica, en '
          'los estudios universitarios de enfermería, nos permite optim'
          'izar estas prácticas al máximo y establecer perfiles profesi'
          'onales con un mayor grado de adaptación al futuro profesiona'
          'l.'
        )
        p_texts = [p.text for p in html.findall('//p')]
        self.assertIn(find_text, p_texts)

    def test_generate_html_for_pt_abstract_in_subarticle(self):
        html = get_html(
          "article-abstract-en-sub-articles-pt-es.xml", "pt")
        find_text = (
          'este estudo transversal descritivo foi realizado no contexto'
          ' das disciplinas de prática clínica do curso de enfermagem. '
          'O desenvolvimento de competências de 323 alunos foi analisad'
          'o usando um questionário '
        )
        p_texts = [p.text for p in html.findall('//p')]
        self.assertIn(find_text, p_texts)

    def test_generate_html_for_pt_trans_abstract(self):
        html = get_html(
          "article-abstract-and-trans-abstract.xml", "pt")
        find_text = (
            'Estudo multicêntrico, transversal, que ocorreu entre 2008 e '
            '2009 em 10 cidades brasileiras. Foram recrutados 3.746 homen'
            's que fazem sexo com homens pela técnica amostral Respondent'
            ' Driven Sampling. O conhecimento em HIV/Aids foi apurado a p'
            'artir de dez afirmativas da entrevista realizada face a face'
            ' e os escores foram obtidos utilizando o modelo logístico de'
            ' dois parâmetros (discriminação e dificuldade) da Teoria de '
            'Resposta ao Item. O funcionamento diferencial dos itens foi '
            'verificado, analisando as curvas características dos itens p'
            'ela idade e escolaridade.'
        )
        p_texts = [p.text for p in html.findall('//p')]
        self.assertIn(find_text, p_texts)


class HTMLGeneratorTableGroupTests(unittest.TestCase):

    def setUp(self):
        sample = u"""<article
                      xmlns:mml="http://www.w3.org/1998/Math/MathML"
                      xmlns:xlink="http://www.w3.org/1999/xlink"
                      xml:lang="pt">
                      <body>
        <table-wrap-group id="t1">
        <table-wrap xml:lang="pt">
        <label>Tabela 1</label>
        <caption>
        <title>Classifica&#x00E7;&#x00E3;o Sucessional adotada por alguns autores ao longo dos anos.</title>
        </caption>
        </table-wrap>
        <table-wrap xml:lang="en">
        <label>Table 1</label>
        <caption>
        <title>Sucessional classification adopted by some authors over the years.</title>
        </caption>
        <table>
        <thead>
        <tr>
        <th valign="top" align="left">Ano</th>
        <th valign="top" align="center">Autor</th>
        <th valign="top" align="center">Classifica&#x00E7;&#x00E3;o</th>
        </tr>
        </thead>
        <tbody>
        <tr>
        <td valign="top" align="left">1965</td>
        <td valign="top" align="center">Budowski</td>
        <td valign="top" align="center">Pioneira, secund&#x00E1;ria inicial, secund&#x00E1;ria tardia e cl&#x00ED;max</td>
        </tr>
        <tr>
        <td valign="top" align="left">1971</td>
        <td valign="top" align="center">G&#x00F3;mez-Pompa</td>
        <td valign="top" align="center">Prim&#x00E1;ria e secund&#x00E1;ria</td>
        </tr>
        <tr>
        <td valign="top" align="left">2017</td>
        <td valign="top" align="center">Moura &#x0026; Mantovani</td>
        <td valign="top" align="center">Pioneira, secund&#x00E1;ria inicial, secund&#x00E1;ria tardia e sub-bosque</td>
        </tr>
        </tbody>
        </table>
        </table-wrap>
        </table-wrap-group>
        </body></article>
        """
        et = get_xml_tree_from_string(sample)
        self.html = domain.HTMLGenerator.parse(et, valid_only=False).generate('pt')

    def test_table_wrap_group_modal(self):
        div_modal_tables = self.html.xpath(
            '//div[@id="ModalTablet1"]'
        )
        self.assertIsNotNone(div_modal_tables)
        table = div_modal_tables[0].find(
            './/div[@class="modal-body"]//table'
        )
        self.assertIsNotNone(table)
        found_text = div_modal_tables[0].findtext(
            './/div[@class="modal-body"]//table/thead/tr/th'
        )
        self.assertEqual("Ano", found_text)
        found_nodes = div_modal_tables[0].findall(
            './/h4[@class="modal-title"]//strong'
        )
        self.assertEqual("Tabela 1", found_nodes[0].text)
        self.assertEqual("Table 1", found_nodes[1].text)

    def test_table_wrap_group_thumbnail(self):
        div_thumbnail = self.html.find(
            '//div[@id="t1"]'
        )
        self.assertIsNotNone(div_thumbnail)
        div_thumbnail_divs = div_thumbnail.findall(
            'div'
        )
        self.assertIsNotNone(div_thumbnail_divs)
        texts = etree.tostring(div_thumbnail_divs[1], encoding="utf-8").decode("utf-8")
        self.assertIn("Tabela 1", texts)
        self.assertIn("Classificação Sucessional adotada por alguns autores ao longo dos anos.", texts)
        self.assertIn("Tabela 1", texts)
        self.assertIn("Sucessional classification adopted by some authors over the years.", texts)


class HTMLGeneratorFigGroupTests(unittest.TestCase):

    def setUp(self):
        sample = u"""<article
                      xmlns:mml="http://www.w3.org/1998/Math/MathML"
                      xmlns:xlink="http://www.w3.org/1999/xlink"
                      xml:lang="pt">
                      <body>
        <fig-group id="f1">
            <fig xml:lang="pt">
                <label>Figura 1</label>
                <caption>
                    <title>Mapa com a localiza&#x00E7;&#x00E3;o das tr&#x00EA;s &#x00E1;reas de estudo, Parque Estadual da Cantareira, S&#x00E3;o Paulo, SP, Brasil. Elaborado por Marina Kanashiro, 2019.</title>
                </caption>
            </fig>
            <fig xml:lang="en">
                <label>Figure 1</label>
                <caption>
                    <title>Map with the location of the three study areas, Parque Estadual da Cantareira, S&#x00E3;o Paulo, S&#x00E3;o Paulo State, Brasil. Prepared by Marina Kanashiro, 2019.</title>
                </caption>
                <graphic xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="2236-8906-hoehnea-49-e1082020-gf01.tif"/>
            </fig>
        </fig-group>
        </body></article>
        """
        et = get_xml_tree_from_string(sample)
        self.html = domain.HTMLGenerator.parse(et, valid_only=False).generate('pt')

    def test_fig_group_modal(self):
        div_modal_figs = self.html.xpath(
            '//div[@id="ModalFigf1"]'
        )
        self.assertIsNotNone(div_modal_figs)
        # fig = div_modal_figs[0].find(
        #     './/div[@class="modal-body"]//img'
        # )
        # self.assertIsNotNone(fig)
        text = etree.tostring(
            div_modal_figs[0].find('.//h4[@class="modal-title"]'),
            encoding="utf-8"
        ).decode("utf-8")
        self.assertIn("Figura 1", text)
        self.assertIn("Figure 1", text)

    def test_fig_group_thumbnail(self):
        div_thumbnail = self.html.find(
            '//div[@id="f1"]'
        )
        self.assertIsNotNone(div_thumbnail)
        div_thumbnail_divs = div_thumbnail.findall(
            'div'
        )
        self.assertIsNotNone(div_thumbnail_divs)
        texts = etree.tostring(div_thumbnail_divs[1], encoding="utf-8").decode("utf-8")
        self.assertIn("Figura 1", texts)
        self.assertIn("Mapa com a localização das três áreas de estudo, Parque Estadual da Cantareira, São Paulo, SP, Brasil. Elaborado por Marina Kanashiro, 2019.", texts)
        self.assertIn("Figure 1", texts)
        self.assertIn("Map with the location of the three study areas, Parque Estadual da Cantareira, São Paulo, São Paulo State, Brasil. Prepared by Marina Kanashiro, 2019.", texts)


class HTMLGeneratorFigWithoutIdTests(unittest.TestCase):

    def setUp(self):
        sample = u"""<article
                      xmlns:mml="http://www.w3.org/1998/Math/MathML"
                      xmlns:xlink="http://www.w3.org/1999/xlink"
                      xml:lang="pt">
                      <body>
        <fig>
            <label>Figura 1.</label>
            <caption>
                <title>Correlação entre o teor de fenóis totais e CE50 de espécies de <italic>Senna</italic> Mill. (Fabaceae). Símbolos cheios: folhas. Símbolos vazados: caule.</title>
            </caption>
            <graphic xlink:href="2236-8906-hoehnea-49-e1112020-gf1.jpg"/>
            <attrib><xref ref-type="fig" rid="f1">Figure 1</xref>. Correlation between total phenol content and EC50 of Senna Mill species. (Fabaceae). Symbols filled: leaves. Hollow symbols: stem.</attrib>
        </fig>
        </body></article>
        """
        et = get_xml_tree_from_string(sample)
        self.html = domain.HTMLGenerator.parse(et, valid_only=False).generate('pt')
        # print(etree.tostring(self.html))

    def test_fig_modal(self):
        """
        Test de modal
        <div class="modal fade ModalFigs" id="ModalFig" tabindex="-1" role="dialog" aria-hidden="true">
            <div class="modal-dialog modal-lg">
            <div class="modal-content">
                <div class="modal-header">
                    <button type="button" class="close" data-dismiss="modal">
                    <span aria-hidden="true">×</span><span class="sr-only">Close</span></button>
                    <a class="link-newWindow showTooltip" target="_blank" data-placement="left" title="Abrir em nova janela" href="2236-8906-hoehnea-49-e1112020-gf1.jpg">
                        <span class="sci-ico-newWindow"></span>
                    </a>
                    <h4 class="modal-title">
                        <span class="sci-ico-fileFigure"></span>Figura 1.   Correlação entre o teor de fenóis totais e CE50 de espécies de <i>Senna</i> Mill. (Fabaceae). Símbolos cheios: folhas. Símbolos vazados: caule.<br>
                    </h4>
                </div>
                <div class="modal-body">
                    <a href="2236-8906-hoehnea-49-e1112020-gf1.jpg">
                        <img style="max-width:100%" src="2236-8906-hoehnea-49-e1112020-gf1.jpg">
                    </a>
                    <small>
                        <a href="" class="open-asset-modal" data-toggle="modal" data-target="#ModalFigf1">
                            <span class="sci-ico-fileFigure"></span>Figure 1</a>. Correlation between total phenol content and EC50 of Senna Mill species. (Fabaceae). Symbols filled: leaves. Hollow symbols: stem.</small>
                </div>
            </div>
            </div>
        </div>
        """
        # div[@id='ModalFig'] (sem id)
        div_modal_fig = self.html.find('.//div[@id="ModalFig"]')

        # class="modal-header" has href with figure path
        self.assertEqual(
            "2236-8906-hoehnea-49-e1112020-gf1.jpg",
            div_modal_fig.find(".//div[@class='modal-header']/a").get("href")
        )

        # class="modal-title" has label and caption content
        text = etree.tostring(
            div_modal_fig.find('.//h4[@class="modal-title"]'),
            encoding="utf-8"
        ).decode("utf-8")

        self.assertIn("Figura 1", text)
        self.assertIn("Correlação entre o teor de fenóis totais e CE50 de espécies de <i>Senna</i> Mill. (Fabaceae). Símbolos cheios: folhas. Símbolos vazados: caule.", text)

        # class="modal-body" has link to image path
        self.assertEqual(
            "2236-8906-hoehnea-49-e1112020-gf1.jpg",
            div_modal_fig.find(".//div[@class='modal-body']/a").get("href")
        )

        # class="modal-body" has src with image path
        self.assertEqual(
            "2236-8906-hoehnea-49-e1112020-gf1.jpg",
            div_modal_fig.find(".//div[@class='modal-body']/a/img").get("src")
        )

        # class="modal-body" has `attrib` text presented inner `<small/>`
        small = div_modal_fig.find(".//div[@class='modal-body']/small")
        self.assertIn(
            "Correlation between total phenol content and EC50 of Senna Mill species. (Fabaceae). Symbols filled: leaves. Hollow symbols: stem.",
            etree.tostring(small, encoding="utf-8").decode("utf-8")
        )

    def test_fig_in_text__thumbnail_and_label(self):
        """
        Test the html expected to display thumbnail, label and caption
        in the text

        <div class="row fig" id="">
            <a name=""></a>
            <div class="col-md-4 col-sm-4">
                <a href="2236-8906-hoehnea-49-e1112020-gf1.jpg" data-toggle="modal" data-target="#ModalFig">
                    <div class="thumbImg">
                        <img src="2236-8906-hoehnea-49-e1112020-gf1.jpg">
                        <div class="zoom"><span class="sci-ico-zoom"></span></div>
                    </div>
                </a>
            </div>
            <div class="col-md-8 col-sm-8">
                <strong>Figura 1.</strong>
                <br>Correlação entre o teor de fenóis totais e CE50 de espécies de <i>Senna</i> Mill. (Fabaceae). Símbolos cheios: folhas. Símbolos vazados: caule.<br>
            </div>
        </div>
        """
        div_row_fig = self.html.find(
            '//div[@class="row fig"]'
        )
        self.assertEqual("", div_row_fig.get("id"))
        div_row_fig_divs = div_row_fig.xpath("div")

        div_modal_fig_0_a = div_row_fig_divs[0].find("a")

        # div_row_fig_divs[0] has link to image path
        self.assertEqual(
            "",
            div_modal_fig_0_a.get("href")
        )
        # div_row_fig_divs[0] has `@data-target` = #ModalFig
        self.assertEqual(
            "#ModalFig",
            div_modal_fig_0_a.get("data-target")
        )

        # div_row_fig_divs[0] must have div[@class='thumbImg'] to display image
        # as thumbnail
        self.assertEqual(
            "2236-8906-hoehnea-49-e1112020-gf1.jpg",
            div_modal_fig_0_a.find("div[@class='thumbImg']/img").get("src")
        )

        # div_modal_fig[1] has label and caption texts
        texts = etree.tostring(
            div_row_fig_divs[1], encoding="utf-8").decode("utf-8")
        self.assertIn("Figura 1", texts)
        self.assertIn(
            "Correlação entre o teor de fenóis totais e CE50 de espécies de <i>Senna</i> Mill. (Fabaceae). Símbolos cheios: folhas. Símbolos vazados: caule.", texts)

    def test_fig_in_pannel_content(self):
        """
        Test de modal em tabs

        <div class="tab-content">
            <div role="tabpanel" class="tab-pane active" id="figures">

        <div class="row fig">
            <div class="col-md-4">
                <a data-toggle="modal" data-target="#ModalFig">
                    <div class="thumbImg">
                        <img src="2236-8906-hoehnea-49-e1112020-gf1.jpg">
                        Thumbnail
                        <div class="zoom">
                            <span class="sci-ico-zoom"></span>
                        </div>
                    </div>
                </a>
            </div>
            <div class="col-md-8">
                <strong>Figura 1.</strong><br>Correlação entre o teor de fenóis totais e CE50 de espécies de <i>Senna</i> Mill. (Fabaceae). Símbolos cheios: folhas. Símbolos vazados: caule.</div>
        </div>
        </div>
        """
        div_tab_panel = self.html.find(
            './/div[@class="tab-content"]'
        )
        div_tab_panel = div_tab_panel.find(
            './/div[@class="tab-pane active"]'
        )
        self.assertEqual("figures", div_tab_panel.get("id"))

        div_row_fig = div_tab_panel.find(
            './/div[@class="row fig"]'
        )
        div_row_fig_divs = div_row_fig.xpath("./div")

        div_row_fig_div_0_a = div_row_fig_divs[0].find("a")

        # div_row_fig_divs[0] has link to image path
        self.assertEqual(
            "modal",
            div_row_fig_div_0_a.get("data-toggle")
        )
        # div_row_fig_divs[0] has `@data-target` = #ModalFig
        self.assertEqual(
            "#ModalFig",
            div_row_fig_div_0_a.get("data-target")
        )

        # div_row_fig_divs[0] must have div[@class='thumbImg'] to display image
        # as thumbnail
        self.assertEqual(
            "2236-8906-hoehnea-49-e1112020-gf1.jpg",
            div_row_fig_div_0_a.find("div[@class='thumbImg']/img").get("src")
        )

        # div_modal_fig[1] has label and caption texts
        texts = etree.tostring(
            div_row_fig_divs[1], encoding="utf-8").decode("utf-8")
        self.assertIn("Figura 1", texts)
        self.assertIn(
            "Correlação entre o teor de fenóis totais e CE50 de espécies de <i>Senna</i> Mill. (Fabaceae). Símbolos cheios: folhas. Símbolos vazados: caule.", texts)


class HTMLGeneratorFigWithIdTests(unittest.TestCase):

    def setUp(self):
        sample = u"""<article
                      xmlns:mml="http://www.w3.org/1998/Math/MathML"
                      xmlns:xlink="http://www.w3.org/1999/xlink"
                      xml:lang="pt">
                      <body>
        <fig id="f1">
            <label>Figura 1.</label>
            <caption>
                <title>Correlação entre o teor de fenóis totais e CE50 de espécies de <italic>Senna</italic> Mill. (Fabaceae). Símbolos cheios: folhas. Símbolos vazados: caule.</title>
            </caption>
            <graphic xlink:href="2236-8906-hoehnea-49-e1112020-gf1.jpg"/>
            <attrib><xref ref-type="fig" rid="f1">Figure 1</xref>. Correlation between total phenol content and EC50 of Senna Mill species. (Fabaceae). Symbols filled: leaves. Hollow symbols: stem.</attrib>
        </fig>
        </body></article>
        """
        et = get_xml_tree_from_string(sample)
        self.html = domain.HTMLGenerator.parse(et, valid_only=False).generate('pt')
        # print(etree.tostring(self.html))

    def test_fig_modal(self):
        """
        Test de modal
        <div class="modal fade ModalFigs" id="ModalFigf1" tabindex="-1" role="dialog" aria-hidden="true">
            <div class="modal-dialog modal-lg">
            <div class="modal-content">
                <div class="modal-header">
                    <button type="button" class="close" data-dismiss="modal">
                    <span aria-hidden="true">×</span><span class="sr-only">Close</span></button>
                    <a class="link-newWindow showTooltip" target="_blank" data-placement="left" title="Abrir em nova janela" href="2236-8906-hoehnea-49-e1112020-gf1.jpg">
                        <span class="sci-ico-newWindow"></span>
                    </a>
                    <h4 class="modal-title">
                        <span class="sci-ico-fileFigure"></span>Figura 1.   Correlação entre o teor de fenóis totais e CE50 de espécies de <i>Senna</i> Mill. (Fabaceae). Símbolos cheios: folhas. Símbolos vazados: caule.<br>
                    </h4>
                </div>
                <div class="modal-body">
                    <a href="2236-8906-hoehnea-49-e1112020-gf1.jpg">
                        <img style="max-width:100%" src="2236-8906-hoehnea-49-e1112020-gf1.jpg">
                    </a>
                    <small>
                        <a href="" class="open-asset-modal" data-toggle="modal" data-target="#ModalFigf1">
                            <span class="sci-ico-fileFigure"></span>Figure 1</a>. Correlation between total phenol content and EC50 of Senna Mill species. (Fabaceae). Symbols filled: leaves. Hollow symbols: stem.</small>
                </div>
            </div>
            </div>
        </div>
        """
        # div[@id='ModalFig'] (sem id)
        div_modal_fig = self.html.find('.//div[@id="ModalFigf1"]')

        # class="modal-header" has href with figure path
        self.assertEqual(
            "2236-8906-hoehnea-49-e1112020-gf1.jpg",
            div_modal_fig.find(".//div[@class='modal-header']/a").get("href")
        )

        # class="modal-title" has label and caption content
        text = etree.tostring(
            div_modal_fig.find('.//h4[@class="modal-title"]'),
            encoding="utf-8"
        ).decode("utf-8")

        self.assertIn("Figura 1", text)
        self.assertIn("Correlação entre o teor de fenóis totais e CE50 de espécies de <i>Senna</i> Mill. (Fabaceae). Símbolos cheios: folhas. Símbolos vazados: caule.", text)

        # class="modal-body" has link to image path
        self.assertEqual(
            "2236-8906-hoehnea-49-e1112020-gf1.jpg",
            div_modal_fig.find(".//div[@class='modal-body']/a").get("href")
        )

        # class="modal-body" has src with image path
        self.assertEqual(
            "2236-8906-hoehnea-49-e1112020-gf1.jpg",
            div_modal_fig.find(".//div[@class='modal-body']/a/img").get("src")
        )

        # class="modal-body" has `attrib` text presented inner `<small/>`
        small = div_modal_fig.find(".//div[@class='modal-body']/small")
        self.assertIn(
            "Correlation between total phenol content and EC50 of Senna Mill species. (Fabaceae). Symbols filled: leaves. Hollow symbols: stem.",
            etree.tostring(small, encoding="utf-8").decode("utf-8")
        )

    def test_fig_in_text__thumbnail_and_label(self):
        """
        Test the html expected to display thumbnail, label and caption
        in the text

        <div class="row fig" id="">
            <a name=""></a>
            <div class="col-md-4 col-sm-4">
                <a href="" data-toggle="modal" data-target="#ModalFig">
                    <div class="thumbImg">
                        <img src="2236-8906-hoehnea-49-e1112020-gf1.jpg">
                        <div class="zoom"><span class="sci-ico-zoom"></span></div>
                    </div>
                </a>
            </div>
            <div class="col-md-8 col-sm-8">
                <strong>Figura 1.</strong>
                <br>Correlação entre o teor de fenóis totais e CE50 de espécies de <i>Senna</i> Mill. (Fabaceae). Símbolos cheios: folhas. Símbolos vazados: caule.<br>
            </div>
        </div>
        """
        div_row_fig = self.html.find(
            '//div[@class="row fig"]'
        )
        self.assertEqual("f1", div_row_fig.get("id"))
        div_row_fig_divs = div_row_fig.xpath("div")

        div_modal_fig_0_a = div_row_fig_divs[0].find("a")

        # div_row_fig_divs[0] has link to image path
		
        self.assertEqual(
            "",
            div_modal_fig_0_a.get("href")
        )
        # div_row_fig_divs[0] has `@data-target` = #ModalFig
        self.assertEqual(
            "#ModalFigf1",
            div_modal_fig_0_a.get("data-target")
        )

        # div_row_fig_divs[0] must have div[@class='thumbImg'] to display image
        # as thumbnail
        self.assertEqual(
            "2236-8906-hoehnea-49-e1112020-gf1.jpg",
            div_modal_fig_0_a.find("div[@class='thumbImg']/img").get("src")
        )

        # div_modal_fig[1] has label and caption texts
        texts = etree.tostring(
            div_row_fig_divs[1], encoding="utf-8").decode("utf-8")
        self.assertIn("Figura 1", texts)
        self.assertIn(
            "Correlação entre o teor de fenóis totais e CE50 de espécies de <i>Senna</i> Mill. (Fabaceae). Símbolos cheios: folhas. Símbolos vazados: caule.", texts)

    def test_fig_in_pannel_content(self):
        """
        Test de modal em tabs

        <div class="tab-content">
            <div role="tabpanel" class="tab-pane active" id="figures">

        <div class="row fig">
            <div class="col-md-4">
                <a data-toggle="modal" data-target="#ModalFig">
                    <div class="thumbImg">
                        <img src="2236-8906-hoehnea-49-e1112020-gf1.jpg">
                        Thumbnail
                        <div class="zoom">
                            <span class="sci-ico-zoom"></span>
                        </div>
                    </div>
                </a>
            </div>
            <div class="col-md-8">
                <strong>Figura 1.</strong><br>Correlação entre o teor de fenóis totais e CE50 de espécies de <i>Senna</i> Mill. (Fabaceae). Símbolos cheios: folhas. Símbolos vazados: caule.</div>
        </div>
        </div>
        """
        div_tab_panel = self.html.find(
            './/div[@class="tab-content"]'
        )
        div_tab_panel = div_tab_panel.find(
            './/div[@class="tab-pane active"]'
        )
        self.assertEqual("figures", div_tab_panel.get("id"))

        div_row_fig = div_tab_panel.find(
            './/div[@class="row fig"]'
        )
        div_row_fig_divs = div_row_fig.xpath("./div")

        div_row_fig_div_0_a = div_row_fig_divs[0].find("a")

        # div_row_fig_divs[0] has link to image path
        self.assertEqual(
            "modal",
            div_row_fig_div_0_a.get("data-toggle")
        )
        # div_row_fig_divs[0] has `@data-target` = #ModalFig
        self.assertEqual(
            "#ModalFigf1",
            div_row_fig_div_0_a.get("data-target")
        )

        # div_row_fig_divs[0] must have div[@class='thumbImg'] to display image
        # as thumbnail
        self.assertEqual(
            "2236-8906-hoehnea-49-e1112020-gf1.jpg",
            div_row_fig_div_0_a.find("div[@class='thumbImg']/img").get("src")
        )

        # div_modal_fig[1] has label and caption texts
        texts = etree.tostring(
            div_row_fig_divs[1], encoding="utf-8").decode("utf-8")
        self.assertIn("Figura 1", texts)
        self.assertIn(
            "Correlação entre o teor de fenóis totais e CE50 de espécies de <i>Senna</i> Mill. (Fabaceae). Símbolos cheios: folhas. Símbolos vazados: caule.", texts)


class HTMLGeneratorTableWrapWithIdTests(unittest.TestCase):

    def setUp(self):
        sample = u"""<article
                      xmlns:mml="http://www.w3.org/1998/Math/MathML"
                      xmlns:xlink="http://www.w3.org/1999/xlink"
                      xml:lang="pt">
                      <body>
        <table-wrap id="t1">
            <label>Tabela 1.</label>
            <caption>
                <title>Identificação das espécies de <italic>Senna</italic> Mill. (Fabaceae) coletadas em diferentes locais da região noroeste do Estado do Ceará. <sup>*</sup>Exótica, <sup>**</sup>Endêmica do Brasil. Fonte: Herbário Francisco José de Abreu Matos (HUVA).</title>
            </caption>
            <table>
                <colgroup>
                    <col/>
                    <col/>
                    <col/>
                    <col/>
                </colgroup>
                <thead>
                    <tr>
                        <th align="left">Espécies</th>
                        <th align="left">Nome popular</th>
                        <th align="center">Local de coleta</th>
                        <th align="center">No. HUVA</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td align="left"><italic>S. alata</italic> (L.) Roxb.</td>
                        <td align="left">fedegoso-gigante</td>
                        <td align="center">Sobral</td>
                        <td align="center">21547</td>
                    </tr>
                    <tr>
                        <td align="left"><italic>S. obtusifolia</italic> (L.) H.S.Irwin &amp; Barneby</td>
                        <td align="left">fedegoso-brando</td>
                        <td align="center">Graça</td>
                        <td align="center">21775</td>
                    </tr>
                    <tr>
                        <td align="left"><italic>S. occidentalis</italic> (L.) Link</td>
                        <td align="left">café-negro</td>
                        <td align="center">Graça</td>
                        <td align="center">21774</td>
                    </tr>
                    <tr>
                        <td align="left"><italic>S. siamea</italic> (Lam.) H.S.Irwin &amp; Barneby<sup>*</sup></td>
                        <td align="left">cássia-de-sião</td>
                        <td align="center">Sobral</td>
                        <td align="center">21578</td>
                    </tr>
                    <tr>
                        <td align="left"><italic>S. trachypus</italic> (Benth.) H.S.Irwin &amp; Barneby<sup>**</sup></td>
                        <td align="left">pau-de-besouro</td>
                        <td align="center">Graça</td>
                        <td align="center">21776</td>
                    </tr>
                </tbody>
            </table>
            <table-wrap-foot>
                <fn id="TFN1">
                    <p><xref ref-type="table" rid="t1">Table 1</xref>Identification of <italic>Senna Senna</italic> Mill. (Fabaceae) species collected in different locations in northwestern Ceará State. <sup>*</sup> Exotic, <sup>**</sup> Endemic to Brazil. Source: Herbário Francisco José de Abreu Matos (HUVA).</p>
                </fn>
            </table-wrap-foot>
        </table-wrap>

        </body></article>
        """
        et = get_xml_tree_from_string(sample)
        self.html = domain.HTMLGenerator.parse(et, valid_only=False).generate('pt')
        # print(etree.tostring(self.html))

    def test_table_wrap_modal(self):
        """
        Test de modal

        <div class="modal fade ModalTables" id="ModalTablet1" tabindex="-1" role="dialog" aria-hidden="true"><div class="modal-dialog modal-lg"><div class="modal-content">
        <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">×</span><span class="sr-only">Close</span></button><h4 class="modal-title">
        <span class="sci-ico-fileTable"></span><strong>Tabela 1.</strong>    Identificação das espécies de <i>Senna</i> Mill. (Fabaceae) coletadas em diferentes locais da região noroeste do Estado do Ceará. <sup>*</sup>Exótica, <sup>**</sup>Endêmica do Brasil. Fonte: Herbário Francisco José de Abreu Matos (HUVA).<br>
        </h4>
        </div>
        <div class="modal-body"><div class="table table-hover"><table>
        <colgroup>
        <col>
        <col>
        <col>
        <col>
        </colgroup>
        <thead><tr>
        <th align="left">Espécies</th>
        <th align="left">Nome popular</th>
        <th align="center">Local de coleta</th>
        <th align="center">No. HUVA</th>
        </tr></thead>
        <tbody>
        <tr>
        <td align="left">
        <i>S. alata</i> (L.) Roxb.</td>
        <td align="left">fedegoso-gigante</td>
        <td align="center">Sobral</td>
        <td align="center">21547</td>
        </tr>
        </tbody>
        </table></div></div>
        <div class="modal-footer"><div class="ref-list"><ul class="refList footnote"><li><div>
        <a href="" class="open-asset-modal" data-toggle="modal" data-target="#ModalTablet1"><span class="sci-ico-fileTable"></span>Table 1</a>Identification of <i>Senna Senna</i> Mill. (Fabaceae) species collected in different locations in northwestern Ceará State. <sup>*</sup> Exotic, <sup>**</sup> Endemic to Brazil. Source: Herbário Francisco José de Abreu Matos (HUVA).</div></li></ul></div></div>
        </div></div></div>
        """
        # div[@id='ModalFig'] (sem id)
        div_modal = self.html.find('.//div[@id="ModalTablet1"]')

        # class="modal-title" has label and caption content
        text = etree.tostring(
            div_modal.find('.//h4[@class="modal-title"]'),
            encoding="utf-8"
        ).decode("utf-8")

        self.assertIn("Tabela 1", text)
        self.assertIn("Identificação das espécies de <i>Senna</i> Mill. (Fabaceae) coletadas em diferentes locais da região noroeste do Estado do Ceará. <sup>*</sup>Exótica, <sup>**</sup>Endêmica do Brasil. Fonte: Herbário Francisco José de Abreu Matos (HUVA).", text)

        # class="modal-body" has link to image path
        self.assertIsNotNone(
            div_modal.find(".//div[@class='modal-body']//table")
        )

        # class="modal-body" has `attrib` text presented inner `<small/>`
        footer = div_modal.find(".//div[@class='modal-footer']")
        self.assertIn(
            "Identification of <i>Senna Senna</i> Mill. (Fabaceae) species collected in different locations in northwestern Ceará State. <sup>*</sup> Exotic, <sup>**</sup> Endemic to Brazil. Source: Herbário Francisco José de Abreu Matos (HUVA).",
            etree.tostring(footer, encoding="utf-8").decode("utf-8")
        )

    def test_table_wrap_in_text__thumbnail_and_label(self):
        """
        Test the html expected to display thumbnail, label and caption
        in the text

        <div class="row table" id="t1">
            <a name="t1"></a>
            <div class="col-md-4 col-sm-4">
                <a data-toggle="modal" data-target="#ModalTablet1">
                    <div class="thumbOff">
                        Thumbnail
                        <div class="zoom"><span class="sci-ico-zoom"></span></div>
                    </div>
                </a>
            </div>
            <div class="col-md-8 col-sm-8">
            <strong><strong>Tabela 1.</strong></strong><br> Identificação das espécies de <i>Senna</i> Mill. (Fabaceae) coletadas em diferentes locais da região noroeste do Estado do Ceará. <sup>*</sup>Exótica, <sup>**</sup>Endêmica do Brasil. Fonte: Herbário Francisco José de Abreu Matos (HUVA).<br>
            </div>
        </div>
        """
        div_row_table = self.html.find(
            '//div[@class="row table"]'
        )
        self.assertEqual("t1", div_row_table.get("id"))
        div_row_table_divs = div_row_table.xpath("div")

        div_modal_table_0_a = div_row_table_divs[0].find("a")

        # div_row_table_divs[0] has `@data-target` = #ModalTablet1
        self.assertEqual(
            "#ModalTablet1",
            div_modal_table_0_a.get("data-target")
        )

        # div_row_table_divs[0] must have div[@class='thumbImg'] to display image
        # as thumbnail
        self.assertIsNotNone(
            div_modal_table_0_a.find("div[@class='thumbOff']")
        )

        # div_modal_table[1] has label and caption texts
        texts = etree.tostring(
            div_row_table_divs[1], encoding="utf-8").decode("utf-8")
        self.assertIn("Tabela 1.", texts)
        self.assertIn(
            "Identificação das espécies de <i>Senna</i> Mill. (Fabaceae) coletadas em diferentes locais da região noroeste do Estado do Ceará. <sup>*</sup>Exótica, <sup>**</sup>Endêmica do Brasil. Fonte: Herbário Francisco José de Abreu Matos (HUVA).", texts)

    def test_table_wrap_in_pannel_content(self):
        """
        Test de modal em tabs

        <div role="tabpanel" class="tab-pane " id="tables">
            <div class="row table">
                <div class="col-md-4">
                    <a data-toggle="modal" data-target="#ModalTablet1">
                        <div class="thumbOff">
                            Thumbnail
                            <div class="zoom"><span class="sci-ico-zoom"></span></div>
                        </div>
                    </a>
                </div>
                <div class="col-md-8">
                    <strong><strong>Tabela 1.</strong></strong><br> Identificação das espécies de <i>Senna</i> Mill. (Fabaceae) coletadas em diferentes locais da região noroeste do Estado do Ceará. <sup>*</sup>Exótica, <sup>**</sup>Endêmica do Brasil. Fonte: Herbário Francisco José de Abreu Matos (HUVA).</div>
            </div>
        </div>
        """
        div_tab_panel = self.html.find(
            './/div[@class="tab-content"]'
        )
        div_tab_panel = div_tab_panel.find(
            './/div[@class="tab-pane active"]'
        )
        self.assertEqual("tables", div_tab_panel.get("id"))

        div_row_table = div_tab_panel.find(
            './/div[@class="row table"]'
        )
        div_row_table_divs = div_row_table.xpath("./div")

        div_row_table_div_0_a = div_row_table_divs[0].find("a")

        # div_row_table_divs[0] has link to image path
        self.assertEqual(
            "modal",
            div_row_table_div_0_a.get("data-toggle")
        )
        # div_row_table_divs[0] has `@data-target` = #ModalFig
        self.assertEqual(
            "#ModalTablet1",
            div_row_table_div_0_a.get("data-target")
        )

        # div_row_table_divs[0] must have div[@class='thumbOff'] to display image
        # as thumbnail
        self.assertIsNotNone(
            div_row_table_div_0_a.find("div[@class='thumbOff']")
        )

        # div_modal_table[1] has label and caption texts
        texts = etree.tostring(
            div_row_table_divs[1], encoding="utf-8").decode("utf-8")
        self.assertIn("Tabela 1.", texts)
        self.assertIn(
            "Identificação das espécies de <i>Senna</i> Mill. (Fabaceae) coletadas em diferentes locais da região noroeste do Estado do Ceará. <sup>*</sup>Exótica, <sup>**</sup>Endêmica do Brasil. Fonte: Herbário Francisco José de Abreu Matos (HUVA).", texts)



class HTMLGeneratorModalWithFiguresAndTablesTests(unittest.TestCase):

    def setUp(self):
        sample = u"""<article
                      xmlns:mml="http://www.w3.org/1998/Math/MathML"
                      xmlns:xlink="http://www.w3.org/1999/xlink"
                      xml:lang="pt">
                      <body>
        <fig id="f1">
            <label>Figura 1.</label>
            <caption>
                <title>Correlação entre o teor de fenóis totais e CE50 de espécies de <italic>Senna</italic> Mill. (Fabaceae). Símbolos cheios: folhas. Símbolos vazados: caule.</title>
            </caption>
            <graphic xlink:href="2236-8906-hoehnea-49-e1112020-gf1.jpg"/>
            <attrib><xref ref-type="fig" rid="f1">Figure 1</xref>. Correlation between total phenol content and EC50 of Senna Mill species. (Fabaceae). Symbols filled: leaves. Hollow symbols: stem.</attrib>
        </fig>
        <table-wrap id="t1">
            <label>Tabela 1.</label>
            <caption>
                <title>Identificação das espécies de <italic>Senna</italic> Mill. (Fabaceae) coletadas em diferentes locais da região noroeste do Estado do Ceará. <sup>*</sup>Exótica, <sup>**</sup>Endêmica do Brasil. Fonte: Herbário Francisco José de Abreu Matos (HUVA).</title>
            </caption>
            <table>
                <colgroup>
                    <col/>
                    <col/>
                    <col/>
                    <col/>
                </colgroup>
                <thead>
                    <tr>
                        <th align="left">Espécies</th>
                        <th align="left">Nome popular</th>
                        <th align="center">Local de coleta</th>
                        <th align="center">No. HUVA</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td align="left"><italic>S. alata</italic> (L.) Roxb.</td>
                        <td align="left">fedegoso-gigante</td>
                        <td align="center">Sobral</td>
                        <td align="center">21547</td>
                    </tr>
                    <tr>
                        <td align="left"><italic>S. obtusifolia</italic> (L.) H.S.Irwin &amp; Barneby</td>
                        <td align="left">fedegoso-brando</td>
                        <td align="center">Graça</td>
                        <td align="center">21775</td>
                    </tr>
                    <tr>
                        <td align="left"><italic>S. occidentalis</italic> (L.) Link</td>
                        <td align="left">café-negro</td>
                        <td align="center">Graça</td>
                        <td align="center">21774</td>
                    </tr>
                    <tr>
                        <td align="left"><italic>S. siamea</italic> (Lam.) H.S.Irwin &amp; Barneby<sup>*</sup></td>
                        <td align="left">cássia-de-sião</td>
                        <td align="center">Sobral</td>
                        <td align="center">21578</td>
                    </tr>
                    <tr>
                        <td align="left"><italic>S. trachypus</italic> (Benth.) H.S.Irwin &amp; Barneby<sup>**</sup></td>
                        <td align="left">pau-de-besouro</td>
                        <td align="center">Graça</td>
                        <td align="center">21776</td>
                    </tr>
                </tbody>
            </table>
            <table-wrap-foot>
                <fn id="TFN1">
                    <p><xref ref-type="table" rid="t1">Table 1</xref>Identification of <italic>Senna Senna</italic> Mill. (Fabaceae) species collected in different locations in northwestern Ceará State. <sup>*</sup> Exotic, <sup>**</sup> Endemic to Brazil. Source: Herbário Francisco José de Abreu Matos (HUVA).</p>
                </fn>
            </table-wrap-foot>
        </table-wrap>
        </body></article>
        """
        et = get_xml_tree_from_string(sample)
        self.html = domain.HTMLGenerator.parse(et, valid_only=False).generate('pt')
        # print(etree.tostring(self.html))

    def test_tabs_modal(self):
        """
        Test de modal
        
        <div class="modal fade ModalDefault" id="ModalTablesFigures" tabindex="-1" role="dialog" aria-hidden="true">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <button type="button" class="close" data-dismiss="modal">
                            <span aria-hidden="true">×</span>
                            <span class="sr-only">Close</span>
                        </button>
                        <h4 class="modal-title">Figuras | Tabelas</h4>
                    </div>
                    <div class="modal-body">
                        <ul class="nav nav-tabs md-tabs" role="tablist">
                            <li role="presentation" class="col-md-4 col-sm-4 active">
                                <a href="#figures" aria-controls="figures" role="tab" data-toggle="tab">Figuras (1)</a>
                            </li>
                            <li role="presentation" class="col-md-4 col-sm-4 ">
                                <a href="#tables" aria-controls="tables" role="tab" data-toggle="tab">Tabelas (1)</a></li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
        """
        # div[@id='ModalFig'] (sem id)
        div_modal = self.html.find('.//div[@id="ModalTablesFigures"]')

        h4 = div_modal.find(".//div[@class='modal-header']/h4")
        text = etree.tostring(h4, encoding="utf-8").decode("utf-8")
        self.assertIn("Figuras | Tabelas", text)

        # class="modal-title" has label and caption content
        text = etree.tostring(
            div_modal.find('.//h4[@class="modal-title"]'),
            encoding="utf-8"
        ).decode("utf-8")

        # modal-body
        modal_body = div_modal.find('.//div[@class="modal-body"]')
        li = modal_body.findall(".//li")
        self.assertEqual(len(li), 2)

        fig_text = etree.tostring(li[0], encoding="utf-8").decode("utf-8")
        fig_text = " ".join([w for w in fig_text.split()])
        self.assertIn("Figuras (1)", fig_text)

        a = li[0].find("a")
        self.assertEqual(a.get("href"), "#figures")
        self.assertEqual(a.get("aria-controls"), "figures")
        self.assertEqual(a.get("data-toggle"), "tab")

        table_text = etree.tostring(li[1], encoding="utf-8").decode("utf-8")
        table_text = " ".join([w for w in table_text.split()])
        self.assertIn("Tabelas (1)", table_text)

        a = li[1].find("a")
        self.assertEqual(a.get("href"), "#tables")
        self.assertEqual(a.get("aria-controls"), "tables")
        self.assertEqual(a.get("data-toggle"), "tab")
