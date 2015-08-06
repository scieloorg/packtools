# coding: utf-8
from __future__ import unicode_literals
import unittest
import io
from lxml import etree

from packtools import domain


class GeneratedTagsTests(unittest.TestCase):

    """ Tags gerais do html: <head>/<title>, <head>/<meta>, <html lang=?>, etc. """
    def test_mandatory_meta_tag_charset_for_encoding(self):
        """
        verifica que o tag meta seja o correto no html gerado. deve ser: <meta charset="utf-8"/>
        """
        sample = u"""<?xml version="1.0" encoding="UTF-8"?>
                    <!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "JATS-journalpublishing1.dtd">
                    <article xml:lang="pt">
                       <sub-article xml:lang="en" article-type="translation" id="S01">
                       </sub-article>
                       <sub-article xml:lang="es" article-type="translation" id="S02">
                       </sub-article>
                    </article>
                 """
        fp = io.BytesIO(sample.encode('utf-8'))
        et = etree.parse(fp)
        for lang, html_output in domain.HTMLGenerator(et, valid_only=False):
            meta_tag = html_output.xpath('/html/head/meta[@charset="utf-8"]')
            self.assertEqual(1, len(meta_tag))

    def test_html_tag_lang_attrib(self):
        """
        verifica que aparece o atributo "lang" no tag <html>, com o language certo.
        """
        sample = u"""<?xml version="1.0" encoding="UTF-8"?>
                    <!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "JATS-journalpublishing1.dtd">
                    <article xml:lang="pt">
                       <sub-article xml:lang="en" article-type="translation" id="S01">
                       </sub-article>
                       <sub-article xml:lang="es" article-type="translation" id="S02">
                       </sub-article>
                    </article>
                 """
        fp = io.BytesIO(sample.encode('utf-8'))
        et = etree.parse(fp)
        for lang, html_output in domain.HTMLGenerator(et, valid_only=False):
            html_lang_attribute = html_output.xpath('/html')[0].attrib['lang']
            self.assertEqual(lang, html_lang_attribute)

    def test_bibliographic_legend(self):
        """
        verifica que aparece o conteudo processado como "bibliographic_legend" no html
        """
        expected_legend_text = '[#BIBLIOGRAPHIC LEGEND#]'
        sample = u"""<?xml version="1.0" encoding="UTF-8"?>
                    <!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "JATS-journalpublishing1.dtd">
                    <article xml:lang="pt">
                       <sub-article xml:lang="en" article-type="translation" id="S01">
                       </sub-article>
                       <sub-article xml:lang="es" article-type="translation" id="S02">
                       </sub-article>
                    </article>
                 """
        fp = io.BytesIO(sample.encode('utf-8'))
        et = etree.parse(fp)
        for lang, html_output in domain.HTMLGenerator(et, valid_only=False):
            legend_span_tag = html_output.xpath('//span[@id="bibliographic_legend"]')
            self.assertEqual(1, len(legend_span_tag))
            self.assertEqual(expected_legend_text, legend_span_tag[0].text.strip())

    def test_css_path(self):
        """
        verifica que aparece o caminho ao css no html
        """
        expected_legend_text = '[#BIBLIOGRAPHIC LEGEND#]'
        sample = u"""<?xml version="1.0" encoding="UTF-8"?>
                    <!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "JATS-journalpublishing1.dtd">
                    <article xml:lang="pt">
                       <sub-article xml:lang="en" article-type="translation" id="S01">
                       </sub-article>
                       <sub-article xml:lang="es" article-type="translation" id="S02">
                       </sub-article>
                    </article>
                 """
        fp = io.BytesIO(sample.encode('utf-8'))
        et = etree.parse(fp)
        css_path = 'foo/bar.css'
        for lang, html_output in domain.HTMLGenerator(et, valid_only=False, css=css_path):
            css_links_tags = html_output.xpath('//link[@type="text/css"]')
            self.assertEqual(2, len(css_links_tags))
            self.assertIn('bootstrap', css_links_tags[0].attrib['href'])
            self.assertIn(css_path, css_links_tags[1].attrib['href'])


class GeneratedFloatingTagsTests(unittest.TestCase):

    # ************************** #
    # ***** TAGS FLUTUANTES **** #
    # ************************** #

    """ <XREF> """
    def test_xref_tag_inside_article_title_and_trans_title(self):
        """
        verifica que o tag xref (dentro do tag (<article-title />, e <trans-title/> nos <sub-article>), seja o correto.
        - - -
        <xref> aparece em:
        <article-title>, <trans-title>, <contrib>, <p>, th, td, <disp-quote>, table-wrap-foot/fn/p
        """
        xref_text = {
            'en': 'foo_ref_en',
            'pt': 'foo_ref_pt',
            'es': 'foo_ref_es',
        }
        sample = u"""<?xml version="1.0" encoding="UTF-8"?>
                    <!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "JATS-journalpublishing1.dtd">
                    <article xml:lang="en">
                        <front>
                            <article-meta>
                                <title-group>
                                    <article-title>
                                        Between spiritual wellbeing and spiritual distress
                                        <xref ref-type="bibr" rid="B1">%s</xref>
                                    </article-title>
                                    <trans-title-group xml:lang="pt">
                                        <trans-title>
                                            Entre o bem-estar espiritual e a angústia espiritual
                                            <xref ref-type="bibr" rid="B1">%s</xref>
                                        </trans-title>
                                    </trans-title-group>
                                    <trans-title-group xml:lang="es">
                                        <trans-title>
                                            Entre el bienestar espiritual y el sufrimiento espiritual
                                            <xref ref-type="bibr" rid="B1">%s</xref>
                                        </trans-title>
                                    </trans-title-group>
                                </title-group>
                            </article-meta>
                        </front>
                        <sub-article xml:lang="pt" article-type="translation" id="S01">
                        </sub-article>
                        <sub-article xml:lang="es" article-type="translation" id="S02">
                        </sub-article>
                    </article>
                 """ % (xref_text['en'], xref_text['pt'], xref_text['es'])
        fp = io.BytesIO(sample.encode('utf-8'))
        et = etree.parse(fp)
        for lang, html_output in domain.HTMLGenerator(et, valid_only=False):
            found_xrefs = html_output.xpath('//h1[@class="article-title"]//a[@class="xref_href"]')
            self.assertEqual(1, len(found_xrefs))
            found_xref = found_xrefs[0]
            self.assertEqual(xref_text[lang], found_xref.text)
            self.assertEqual({'href': '#B1', 'class': 'xref_href'}, found_xref.attrib)

    def test_xref_tag_inside_contrib(self):
        """
        verifica que o tag xref dentro de <contrib>, seja o correto.
        - - -
        <xref> aparece em:
        <article-title>, <trans-title>, <contrib>, <p>, th, td, <disp-quote>, table-wrap-foot/fn/p
        """
        sample = u"""<?xml version="1.0" encoding="UTF-8"?>
                <!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "JATS-journalpublishing1.dtd">
                <article xml:lang="en">
                    <front>
                        <article-meta>
                            <contrib-group>
                                <contrib contrib-type="author">
                                    <name>
                                        <surname>Foo</surname>
                                        <given-names>Bar Baz</given-names>
                                    </name>
                                    <xref ref-type="aff" rid="aff1">
                                        LOREM
                                    </xref>
                                </contrib>
                            </contrib-group>
                        </article-meta>
                    </front>
                    <sub-article xml:lang="pt" article-type="translation" id="S01">
                    </sub-article>
                    <sub-article xml:lang="es" article-type="translation" id="S02">
                    </sub-article>
                </article>
                """
        fp = io.BytesIO(sample.encode('utf-8'))
        et = etree.parse(fp)
        for lang, html_output in domain.HTMLGenerator(et, valid_only=False):
            found_xrefs = html_output.xpath('//a[@class="xref_href"]')
            self.assertEqual(1, len(found_xrefs))
            found_xref = found_xrefs[0]
            self.assertEqual('LOREM', found_xref.text.strip())
            self.assertEqual({'href': '#aff1', 'class': 'xref_href'}, found_xref.attrib)

    def test_xref_tag_inside_paragraph(self):
        """
        verifica que o tag xref dentro de <p> seja correto
        - - -
        <xref> aparece em:
        <article-title>, <trans-title>, <contrib>, <p>, th, td, <disp-quote>, table-wrap-foot/fn/p
        """
        xref_text = {
            'pt': 'FOO_PT',
            'en': 'FOO_EN',
        }
        sample = u"""<?xml version="1.0" encoding="UTF-8"?>
                <!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "JATS-journalpublishing1.dtd">
                <article xml:lang="pt">
                    <body>
                        <sec sec-type="intro">
                            <title>INTRODUÇÃO</title>
                            <p>A telessaúde tem sido aplicada em diferentes países com escopo abrangente
                                <xref ref-type="bibr" rid="B5">%s</xref>
                                Entretanto, os significados de telessaúde oscilam segundo ênfases.
                            </p>
                        </sec>
                    </body>
                    <sub-article xml:lang="en" article-type="translation" id="S01">
                        <body>
                            <sec sec-type="intro">
                                <title>INTRODUCTION</title>
                                <p>Telehealth has been used with a broad scope in different countries
                                    <xref ref-type="bibr" rid="B5">
                                        %s
                                    </xref> However, the meanings of telehealth vary according to emphasis
                                </p>
                            </sec>
                        </body>
                    </sub-article>
                </article>
                """ % (xref_text['pt'], xref_text['en'])
        fp = io.BytesIO(sample.encode('utf-8'))
        et = etree.parse(fp)
        for lang, html_output in domain.HTMLGenerator(et, valid_only=False):
            found_xrefs = html_output.xpath('//a[@class="xref_href"]')
            self.assertEqual(1, len(found_xrefs))
            found_xref = found_xrefs[0]
            self.assertEqual(xref_text[lang], found_xref.text.strip())
            self.assertEqual({'href': '#B5', 'class': 'xref_href'}, found_xref.attrib)

    def test_xref_tag_inside_table_header(self):
        """
        verifica que o tag xref dentro de <th> seja correto
        - - -
        <xref> aparece em:
        <article-title>, <trans-title>, <contrib>, <p>, th, td, <disp-quote>, table-wrap-foot/fn/p
        """
        xref_text = {
            'pt': 'FOO_PT',
            'en': 'FOO_EN',
        }
        sample = u"""<?xml version="1.0" encoding="UTF-8"?>
                    <!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "JATS-journalpublishing1.dtd">
                    <article xmlns:xlink="http://www.w3.org/1999/xlink" xml:lang="pt">
                        <body>
                            <sec sec-type="methods">
                                <p>
                                    <table-wrap id="t01">
                                        <table>
                                            <thead>
                                                <tr>
                                                    <th>Escola B <xref ref-type="fn" rid="fn1">%s</xref></th>
                                                </tr>
                                            </thead>
                                            <tbody>
                                                <tr>
                                                    <td>9,8</td>
                                                </tr>
                                            </tbody>
                                        </table>
                                    </table-wrap>
                                </p>
                            </sec>
                        </body>
                        <sub-article article-type="translation" id="TRen" xml:lang="en">
                            <body>
                                <sec sec-type="methods">
                                    <p>
                                        <table-wrap id="t01_en">
                                            <table>
                                                <thead>
                                                    <tr>
                                                        <th>School B <xref ref-type="fn" rid="fn1">%s</xref></th>
                                                    </tr>
                                                </thead>
                                                <tbody>
                                                    <tr><td>9.8</td></tr>
                                                </tbody>
                                            </table>
                                        </table-wrap>
                                    </p>
                                </sec>
                            </body>
                        </sub-article>
                    </article>
                """ % (xref_text['pt'], xref_text['en'])
        fp = io.BytesIO(sample.encode('utf-8'))
        et = etree.parse(fp)
        for lang, html_output in domain.HTMLGenerator(et, valid_only=False):
            found_xrefs = html_output.xpath('//a[@class="xref_href"]')
            self.assertEqual(2, len(found_xrefs))  # one xref-anchor on article body and another xref-anchor in table section
            found_xref = found_xrefs[0]
            self.assertEqual(xref_text[lang], found_xref.text.strip())
            self.assertEqual({'href': '#fn1', 'class': 'xref_href'}, found_xref.attrib)

    def test_xref_tag_inside_table_cell(self):
        """
        verifica que o tag xref dentro de <td> seja correto
        - - -
        <xref> aparece em:
        <article-title>, <trans-title>, <contrib>, <p>, th, td, <disp-quote>, table-wrap-foot/fn/p
        """
        xref_text = {
            'pt': 'FOO_PT',
            'en': 'FOO_EN',
        }
        sample = u"""<?xml version="1.0" encoding="UTF-8"?>
                    <!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "JATS-journalpublishing1.dtd">
                    <article xmlns:xlink="http://www.w3.org/1999/xlink" xml:lang="pt">
                        <body>
                            <sec sec-type="methods">
                                <p>
                                    <table-wrap id="t01">
                                        <table>
                                            <thead>
                                                <tr>
                                                    <th>Escola B</th>
                                                </tr>
                                            </thead>
                                            <tbody>
                                                <tr>
                                                    <td>9,8 <xref ref-type="fn" rid="fn1">%s</xref></td>
                                                </tr>
                                            </tbody>
                                        </table>
                                    </table-wrap>
                                </p>
                            </sec>
                        </body>
                        <sub-article article-type="translation" id="TRen" xml:lang="en">
                            <body>
                                <sec sec-type="methods">
                                    <p>
                                        <table-wrap id="t01_en">
                                            <table>
                                                <thead>
                                                    <tr>
                                                        <th>School B</th>
                                                    </tr>
                                                </thead>
                                                <tbody>
                                                    <tr><td>9.8<xref ref-type="fn" rid="fn1">%s</xref></td></tr>
                                                </tbody>
                                            </table>
                                        </table-wrap>
                                    </p>
                                </sec>
                            </body>
                        </sub-article>
                    </article>
                """ % (xref_text['pt'], xref_text['en'])
        fp = io.BytesIO(sample.encode('utf-8'))
        et = etree.parse(fp)
        for lang, html_output in domain.HTMLGenerator(et, valid_only=False):
            found_xrefs = html_output.xpath('//a[@class="xref_href"]')
            self.assertEqual(2, len(found_xrefs))  # one xref-anchor on article body and another xref-anchor in table section
            found_xref = found_xrefs[0]
            self.assertEqual(xref_text[lang], found_xref.text.strip())
            self.assertEqual({'href': '#fn1', 'class': 'xref_href'}, found_xref.attrib)

    def test_xref_tag_inside_disp_quote(self):
        """
        verifica que o tag xref dentro de <disp-quote> seja correto
        - - -
        <xref> aparece em:
        <article-title>, <trans-title>, <contrib>, <p>, th, td, <disp-quote>, table-wrap-foot/fn/p
        """
        xref_text = {
            'pt': 'FOO_PT',
            'en': 'FOO_EN',
        }
        sample = u"""<?xml version="1.0" encoding="UTF-8"?>
                    <!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "JATS-journalpublishing1.dtd">
                    <article xmlns:xlink="http://www.w3.org/1999/xlink" xml:lang="pt">
                        <body>
                            <sec sec-type="methods">
                                <p>
                                    <disp-quote>
                                        <p>
                                            Lorem ipsum dolor sit amet, consectetur adipisicing elit. <xref ref-type="fn" rid="fn1">%s</xref> Doloremque quos quibusdam quidem!
                                        </p>
                                    </disp-quote>
                                </p>
                            </sec>
                        </body>
                        <sub-article article-type="translation" id="TRen" xml:lang="en">
                            <body>
                                <sec sec-type="methods">
                                    <p>
                                        <disp-quote>
                                            <p>
                                                Lorem ipsum dolor sit amet, consectetur adipisicing elit. <xref ref-type="fn" rid="fn1">%s</xref> Doloremque quos quibusdam quidem!
                                            </p>
                                        </disp-quote>
                                    </p>
                                </sec>
                            </body>
                        </sub-article>
                    </article>
                """ % (xref_text['pt'], xref_text['en'])
        fp = io.BytesIO(sample.encode('utf-8'))
        et = etree.parse(fp)
        for lang, html_output in domain.HTMLGenerator(et, valid_only=False):
            found_xrefs = html_output.xpath('//a[@class="xref_href"]')
            self.assertEqual(1, len(found_xrefs))
            found_xref = found_xrefs[0]
            self.assertEqual(xref_text[lang], found_xref.text.strip())
            self.assertEqual({'href': '#fn1', 'class': 'xref_href'}, found_xref.attrib)

    def test_xref_tag_inside_table_wrap_foot_fn(self):
        """
        verifica que o tag xref dentro de <table-wrap-foot>/<fn>/<p> seja correto
        - - -
        <xref> aparece em:
        <article-title>, <trans-title>, <contrib>, <p>, th, td, <disp-quote>, table-wrap-foot/fn/p
        """
        xref_text = {
            'pt': 'FOO_PT',
            'en': 'FOO_EN',
        }

        sample = u"""<?xml version="1.0" encoding="UTF-8"?>
                    <!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "JATS-journalpublishing1.dtd">
                    <article xmlns:xlink="http://www.w3.org/1999/xlink" xml:lang="pt">
                        <body>
                            <sec sec-type="methods">
                                <p>
                                    <table-wrap id="t01">
                                        <table-wrap-foot>
                                            <fn id="TFN01">
                                                <label>*</label>
                                                <p>text <xref ref-type="fn" rid="fn1">%s</xref></p>
                                            </fn>
                                        </table-wrap-foot>
                                    </table-wrap>
                                </p>
                            </sec>
                        </body>
                        <sub-article article-type="translation" id="TRen" xml:lang="en">
                            <body>
                                <sec sec-type="methods">
                                    <p>
                                        <table-wrap id="t01_en">
                                            <table-wrap-foot>
                                                <fn id="TFN01">
                                                    <label>*</label>
                                                    <p>text <xref ref-type="fn" rid="fn1">%s</xref></p>
                                                </fn>
                                            </table-wrap-foot>
                                        </table-wrap>
                                    </p>
                                </sec>
                            </body>
                        </sub-article>
                    </article>
                """ % (xref_text['pt'], xref_text['en'])
        fp = io.BytesIO(sample.encode('utf-8'))
        et = etree.parse(fp)
        for lang, html_output in domain.HTMLGenerator(et, valid_only=False):
            found_xrefs = html_output.xpath('//a[@class="xref_href"]')
            self.assertEqual(4, len(found_xrefs))  # one xref-anchor on article body and another xref-anchor in table section and backlinks
            found_xref = found_xrefs[0]
            self.assertEqual(xref_text[lang], found_xref.text.strip())
            self.assertEqual({'href': '#fn1', 'class': 'xref_href'}, found_xref.attrib)

    """ <LABEL> """
    def test_label_tag_inside_aff(self):
        """
        verifica que o tag <label> dentro de <aff> seja correto
        - - -
        <label> tags aparece em:
        <aff>, <corresp>, <fn>, <fig>, <table-wrap>, <disp-formula>, <media>, <supplementary-material>, <list>, <list-item>, <ref>, <glossary>, <app>, <def-list>
        """
        label_text = 'LABEL_TEXT_FOO'
        sample = u"""<?xml version="1.0" encoding="UTF-8"?>
                <!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "JATS-journalpublishing1.dtd">
                <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" dtd-version="1.0" article-type="review-article" xml:lang="pt">
                    <front>
                        <article-meta>
                            <aff id="aff1">
                                <label>%s</label>
                                <institution content-type="orgdiv2">Laboratório de Telessaúde</institution>
                                <institution content-type="orgdiv1">Instituto Nacional de Saúde da Mulher, da Criança e do Adolescente Fernandes Figueira</institution>
                                <institution content-type="orgname">Fundação Oswaldo Cruz</institution>
                                <addr-line>
                                    <named-content content-type="city">Rio de Janeiro</named-content>
                                    <named-content content-type="state">RJ</named-content>
                                </addr-line>
                                <country>Brasil</country>
                                <institution content-type="original">Laboratório de Telessaúde. Instituto Nacional de Saúde da Mulher, da Criança e do Adolescente Fernandes Figueira. Fundação Oswaldo Cruz. Rio de Janeiro, RJ, Brasil</institution>
                            </aff>
                        </article-meta>
                    </front>
                </article>
                """ % label_text
        fp = io.BytesIO(sample.encode('utf-8'))
        et = etree.parse(fp)
        for lang, html_output in domain.HTMLGenerator(et, valid_only=False):
            # etree.tostring(html_output, method="html", pretty_print=True)
            found_labels = html_output.xpath('//li[@id="aff1"]//sup')
            self.assertEqual(1, len(found_labels))
            found_label = found_labels[0]
            self.assertEqual(label_text, found_label.text.strip())

    def test_label_tag_inside_corresp(self):
        """
        verifica que o tag <label> dentro de <corresp> seja correto
        - - -
        <label> tags aparece em:
        <aff>, <corresp>, <fn>, <fig>, <table-wrap>, <disp-formula>, <media>, <supplementary-material>, <list>, <list-item>, <ref>, <glossary>, <app>, <def-list>
        """
        label_text = 'LABEL_TEXT_FOO'
        sample = u"""<?xml version="1.0" encoding="UTF-8"?>
                <!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "JATS-journalpublishing1.dtd">
                <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" dtd-version="1.0" article-type="review-article" xml:lang="pt">
                    <front>
                        <article-meta>
                            <author-notes>
                                <corresp id="c01">
                                    <label>%s</label>:  <bold>Foo Bar Baz</bold> Laboratório de Lorem Ipsum - <email>foo@bar.edu.br</email>
                                </corresp>
                                <fn fn-type="conflict">
                                    <p>Os autores declaram não haver conflito de interesses.</p>
                                </fn>
                                <fn fn-type="other">
                                    <p>Artigo baseado na tese de doutorado de Lorem Ipsum apresentada à Escola Nacional de Saúde Pública Sergio Arouca/Fiocruz, em 2013.</p>
                                </fn>
                            </author-notes>
                        </article-meta>
                    </front>
                </article>
                """ % label_text
        fp = io.BytesIO(sample.encode('utf-8'))
        et = etree.parse(fp)
        for lang, html_output in domain.HTMLGenerator(et, valid_only=False):
            found_labels = html_output.xpath('//label[@for="c01"]')
            self.assertEqual(1, len(found_labels))
            found_label = found_labels[0]
            self.assertEqual(label_text, found_label.text.strip())

    def test_label_tag_inside_fn(self):
        """
        verifica que o tag <label> dentro de <fn> seja correto
        - - -
        <label> tags aparece em:
        <aff>, <corresp>, <fn>, <fig>, <table-wrap>, <disp-formula>, <media>, <supplementary-material>, <list>, <list-item>, <ref>, <glossary>, <app>, <def-list>
        """
        label_text = 'LABEL_TEXT_FOO'
        sample = u"""<?xml version="1.0" encoding="UTF-8"?>
                <!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "JATS-journalpublishing1.dtd">
                <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" dtd-version="1.0" article-type="review-article" xml:lang="pt">
                    <front>
                        <article-meta>
                            <author-notes>
                                <fn fn-type="conflict">
                                    <p>Os autores declaram não haver conflito de interesses.</p>
                                </fn>
                                <fn fn-type="other">
                                    <label>%s</label>:
                                    <p>Artigo baseado na tese de doutorado de Lorem Ipsum apresentada à Escola Nacional de Saúde Pública Sergio Arouca/Fiocruz, em 2013.</p>
                                </fn>
                            </author-notes>
                        </article-meta>
                    </front>
                </article>
                """ % label_text
        fp = io.BytesIO(sample.encode('utf-8'))
        et = etree.parse(fp)
        for lang, html_output in domain.HTMLGenerator(et, valid_only=False):
            found_labels = html_output.xpath('//label[@for=""]')
            self.assertEqual(1, len(found_labels))
            found_label = found_labels[0]
            self.assertEqual(label_text, found_label.text.strip())

    def test_label_tag_inside_fig(self):
        """
        verifica que o tag <label> dentro de <fig> seja correto
        - - -
        <label> tags aparece em:
        <aff>, <corresp>, <fn>, <fig>, <table-wrap>, <disp-formula>, <media>, <supplementary-material>, <list>, <list-item>, <ref>, <glossary>, <app>, <def-list>
        """
        label_text = {
            'pt': 'Figura 1',
            'en': 'Figure 1',
        }
        sample = u"""<?xml version="1.0" encoding="UTF-8"?>
                    <!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "JATS-journalpublishing1.dtd">
                    <article xmlns:xlink="http://www.w3.org/1999/xlink" xml:lang="pt">
                        <body>
                            <sec sec-type="methods">
                                <p>
                                    <fig id="f01">
                                        <label>%s</label>
                                        <caption>
                                            <title>Modelo das cinco etapas da pesquisa translacional.</title>
                                        </caption>
                                        <graphic xlink:href="0034-8910-rsp-48-2-0347-gf01"/>
                                    </fig>
                                </p>
                            </sec>
                        </body>
                        <sub-article article-type="translation" id="TRen" xml:lang="en">
                            <body>
                                <sec sec-type="methods">
                                    <p>
                                        <fig id="f01">
                                            <label>%s</label>
                                            <caption>
                                                <title>Model of the five stages of translational research.</title>
                                            </caption>
                                            <graphic xlink:href="0034-8910-rsp-48-2-0347-gf01-en"/>
                                        </fig>
                                    </p>
                                </sec>
                            </body>
                        </sub-article>
                    </article>
                """ % (label_text['pt'], label_text['en'])
        fp = io.BytesIO(sample.encode('utf-8'))
        et = etree.parse(fp)
        for lang, html_output in domain.HTMLGenerator(et, valid_only=False):
            found_labels = html_output.xpath('//label[@for="f01"]')
            self.assertEqual(1, len(found_labels))
            found_label = found_labels[0]
            self.assertEqual(label_text[lang], found_label.text.strip())

    def test_label_tag_inside_table_wrap(self):
        """
        verifica que o tag <label> dentro de <table-wrap> seja correto
        - - -
        <label> aparece em:
        <aff>, <corresp>, <fn>, <fig>, <table-wrap>, <disp-formula>, <media>, <supplementary-material>, <list>, <list-item>, <ref>, <glossary>, <app>, <def-list>
        """
        label_text = {
            'pt': 'Tabela 1',
            'en': 'Table 1',
        }
        sample = u"""<?xml version="1.0" encoding="UTF-8"?>
                    <!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "JATS-journalpublishing1.dtd">
                    <article xmlns:xlink="http://www.w3.org/1999/xlink" xml:lang="pt">
                        <body>
                            <sec sec-type="methods">
                                <p>
                                    <table-wrap id="t01">
                                        <label>%s</label>
                                    </table-wrap>
                                </p>
                            </sec>
                        </body>
                        <sub-article article-type="translation" id="TRen" xml:lang="en">
                            <body>
                                <sec sec-type="methods">
                                    <p>
                                        <table-wrap id="t01">
                                            <label>%s</label>
                                        </table-wrap>
                                    </p>
                                </sec>
                            </body>
                        </sub-article>
                    </article>
                """ % (label_text['pt'], label_text['en'])
        fp = io.BytesIO(sample.encode('utf-8'))
        et = etree.parse(fp)
        for lang, html_output in domain.HTMLGenerator(et, valid_only=False):
            found_labels = html_output.xpath('//label[@for="t01"]')
            self.assertEqual(2, len(found_labels))
            found_label = found_labels[0]
            self.assertEqual(label_text[lang], found_label.text.strip())

    def test_label_tag_inside_disp_formula(self):
        """
        verifica que o tag <label> dentro de <disp-formula> seja correto
        - - -
        <label> aparece em:
        <aff>, <corresp>, <fn>, <fig>, <table-wrap>, <disp-formula>, <media>, <supplementary-material>, <list>, <list-item>, <ref>, <glossary>, <app>, <def-list>
        """
        label_text = {
            'pt': 'PT FOO 1',
            'en': 'EN FOO 1',
        }
        sample = u"""<?xml version="1.0" encoding="UTF-8"?>
                    <!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "JATS-journalpublishing1.dtd">
                    <article xmlns:xlink="http://www.w3.org/1999/xlink" xml:lang="pt">
                        <body>
                            <sec sec-type="methods">
                                <p>As medições de Eh: <xref ref-type="disp-formula" rid="e01">1</xref>(em mV):</p>
                                <disp-formula id="e01">
                                    <label>%s</label>
                                    <graphic xlink:href="1234-5678-rctb-45-05-0110-e01.tif"/>
                                </disp-formula>
                            </sec>
                        </body>
                        <sub-article article-type="translation" id="TRen" xml:lang="en">
                            <body>
                                <sec sec-type="methods">
                                    <p>The Eh measurements: <xref ref-type="disp-formula" rid="e01">1</xref>(in mV):</p>
                                    <disp-formula id="e01">
                                        <label>%s</label>
                                        <graphic xlink:href="1234-5678-rctb-45-05-0110-e01.tif"/>
                                    </disp-formula>
                                </sec>
                            </body>
                        </sub-article>
                    </article>
                """ % (label_text['pt'], label_text['en'])
        fp = io.BytesIO(sample.encode('utf-8'))
        et = etree.parse(fp)
        for lang, html_output in domain.HTMLGenerator(et, valid_only=False):
            found_labels = html_output.xpath('//label[@for="e01"]')
            self.assertEqual(1, len(found_labels))
            found_label = found_labels[0]
            self.assertEqual(label_text[lang], found_label.text.strip())

    def test_label_tag_inside_media(self):
        """
        verifica que o tag <label> dentro de <media> seja correto
        - - -
        <label> aparece em:
        <aff>, <corresp>, <fn>, <fig>, <table-wrap>, <disp-formula>, <media>, <supplementary-material>, <list>, <list-item>, <ref>, <glossary>, <app>, <def-list>
        """
        label_text = {
            'pt': 'PT FOO 1',
            'en': 'EN FOO 1',
        }
        sample = u"""<?xml version="1.0" encoding="UTF-8"?>
                    <!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "JATS-journalpublishing1.dtd">
                    <article xmlns:xlink="http://www.w3.org/1999/xlink" xml:lang="pt">
                        <body>
                            <sec sec-type="methods">
                                <p>
                                    <media mimetype="video"
                                       mime-subtype="mp4"
                                       xlink:href="1234-5678-rctb-45-05-0110-m01.mp4">
                                       <label>%s</label>
                                    </media>
                                </p>
                            </sec>
                        </body>
                        <sub-article article-type="translation" id="TRen" xml:lang="en">
                            <body>
                                <sec sec-type="methods">
                                    <p>
                                        <media mimetype="video"
                                           mime-subtype="mp4"
                                           xlink:href="1234-5678-rctb-45-05-0110-m01.mp4">
                                           <label>%s</label>
                                        </media>
                                    </p>
                                </sec>
                            </body>
                        </sub-article>
                    </article>
                """ % (label_text['pt'], label_text['en'])
        fp = io.BytesIO(sample.encode('utf-8'))
        et = etree.parse(fp)
        for lang, html_output in domain.HTMLGenerator(et, valid_only=False):
            found_labels = html_output.xpath('//span[@class="media-label"]')
            self.assertEqual(1, len(found_labels))
            found_label = found_labels[0]
            self.assertEqual(label_text[lang], found_label.text.strip())

    def test_label_tag_inside_supplementary_material(self):
        """
        verifica que o tag <label> dentro de <supplementary-material> seja correto
        - - -
        <label> aparece em:
        <aff>, <corresp>, <fn>, <fig>, <table-wrap>, <disp-formula>, <media>, <supplementary-material>, <list>, <list-item>, <ref>, <glossary>, <app>, <def-list>
        """
        label_text = {
            'pt': 'Material Adicional',
            'en': 'Additional material',
        }
        sample = u"""<?xml version="1.0" encoding="UTF-8"?>
                    <!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "JATS-journalpublishing1.dtd">
                    <article xmlns:xlink="http://www.w3.org/1999/xlink" xml:lang="pt">
                        <body>
                            <sec sec-type="supplementary-material">
                                <title>Material Supplementario</title>
                                <supplementary-material id="S1" xmlns:xlink="http://www.w3.org/1999/xlink" xlink:title="local_file" xlink:href="1471-2105-1-1-s1.pdf" mimetype="application/pdf">
                                    <label>%s</label>
                                    <caption>
                                        <p>Arquivo PDF Suplementar disponibilizado pelos autors.</p>
                                    </caption>
                                </supplementary-material>
                            </sec>
                        </body>
                        <sub-article article-type="translation" id="TRen" xml:lang="en">
                            <body>
                                <sec sec-type="supplementary-material">
                                    <title>Material Supplementario</title>
                                    <supplementary-material id="S1" xmlns:xlink="http://www.w3.org/1999/xlink" xlink:title="local_file" xlink:href="1471-2105-1-1-s1.pdf" mimetype="application/pdf">
                                        <label>%s</label>
                                        <caption>
                                            <p>Supplementary PDF file supplied by authors.</p>
                                        </caption>
                                    </supplementary-material>
                                </sec>
                            </body>
                        </sub-article>
                    </article>
                """ % (label_text['pt'], label_text['en'])
        fp = io.BytesIO(sample.encode('utf-8'))
        et = etree.parse(fp)
        for lang, html_output in domain.HTMLGenerator(et, valid_only=False):
            found_labels = html_output.xpath('//label[@for="S1"]')
            self.assertEqual(1, len(found_labels))
            found_label = found_labels[0]
            self.assertEqual(label_text[lang], found_label.text.strip())

    def test_label_tag_inside_list(self):
        """
        verifica que o tag <label> dentro de <list> seja correto
        - - -
        <label> aparece em:
        <aff>, <corresp>, <fn>, <fig>, <table-wrap>, <disp-formula>, <media>, <supplementary-material>, <list>, <list-item>, <ref>, <glossary>, <app>, <def-list>
        """
        label_text = {
            'pt': 'Material Adicional',
            'en': 'Additional material',
        }
        sample = u"""<?xml version="1.0" encoding="UTF-8"?>
                    <!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "JATS-journalpublishing1.dtd">
                    <article xmlns:xlink="http://www.w3.org/1999/xlink" xml:lang="pt">
                        <body>
                            <sec sec-type="list">
                                <p>
                                    <list list-type="order">
                                        <title>Lista Númerica</title>
                                        <label>%s</label>
                                        <list-item>
                                            <p>Nullam gravida tellus eget condimentum egestas.</p>
                                        </list-item>
                                    </list>
                                </p>
                            </sec>
                        </body>
                        <sub-article article-type="translation" id="TRen" xml:lang="en">
                            <body>
                                <sec sec-type="supplementary-material">
                                    <p>
                                        <list list-type="order">
                                            <title>Numeric List</title>
                                            <label>%s</label>
                                            <list-item>
                                                <p>Nullam gravida tellus eget condimentum egestas.</p>
                                            </list-item>
                                        </list>
                                    </p>
                                </sec>
                            </body>
                        </sub-article>
                    </article>
                """ % (label_text['pt'], label_text['en'])
        fp = io.BytesIO(sample.encode('utf-8'))
        et = etree.parse(fp)
        for lang, html_output in domain.HTMLGenerator(et, valid_only=False):
            found_labels = html_output.xpath('//label[@for=""]')
            self.assertEqual(1, len(found_labels))
            found_label = found_labels[0]
            self.assertEqual(label_text[lang], found_label.text.strip())

    def test_label_tag_inside_list_item(self):
        """
        verifica que o tag <label> dentro de <list-item> seja correto
        - - -
        <label> aparece em:
        <aff>, <corresp>, <fn>, <fig>, <table-wrap>, <disp-formula>, <media>, <supplementary-material>, <list>, <list-item>, <ref>, <glossary>, <app>, <def-list>
        """
        label_text = {
            'pt': 'Material Adicional',
            'en': 'Additional material',
        }
        sample = u"""<?xml version="1.0" encoding="UTF-8"?>
                    <!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "JATS-journalpublishing1.dtd">
                    <article xmlns:xlink="http://www.w3.org/1999/xlink" xml:lang="pt">
                        <body>
                            <sec sec-type="list">
                                <p>
                                    <list list-type="order">
                                        <title>Lista Númerica</title>
                                        <list-item>
                                            <label>%s</label>
                                            <p>Nullam gravida tellus eget condimentum egestas.</p>
                                        </list-item>
                                    </list>
                                </p>
                            </sec>
                        </body>
                        <sub-article article-type="translation" id="TRen" xml:lang="en">
                            <body>
                                <sec sec-type="supplementary-material">
                                    <p>
                                        <list list-type="order">
                                            <title>Numeric List</title>
                                            <list-item>
                                                <label>%s</label>
                                                <p>Nullam gravida tellus eget condimentum egestas.</p>
                                            </list-item>
                                        </list>
                                    </p>
                                </sec>
                            </body>
                        </sub-article>
                    </article>
                """ % (label_text['pt'], label_text['en'])
        fp = io.BytesIO(sample.encode('utf-8'))
        et = etree.parse(fp)
        for lang, html_output in domain.HTMLGenerator(et, valid_only=False):
            found_labels = html_output.xpath('//label[@for=""]')
            self.assertEqual(1, len(found_labels))
            found_label = found_labels[0]
            self.assertEqual(label_text[lang], found_label.text.strip())

    def test_label_tag_inside_ref(self):
        """
        verifica que o tag <label> dentro de <ref> seja correto
        - - -
        <label> aparece em:
        <aff>, <corresp>, <fn>, <fig>, <table-wrap>, <disp-formula>, <media>, <supplementary-material>, <list>, <list-item>, <ref>, <glossary>, <app>, <def-list>
        """
        label_text = {
            'pt': 'Material Adicional',
            'en': 'Additional material',
        }
        sample = u"""<?xml version="1.0" encoding="UTF-8"?>
                    <!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "JATS-journalpublishing1.dtd">
                    <article xmlns:xlink="http://www.w3.org/1999/xlink" xml:lang="pt">
                        <back>
                            <ref-list>
                                <ref id="B3">
                                    <label>%s</label>
                                    <mixed-citation>. FOO em PT</mixed-citation>
                                </ref>
                            </ref-list>
                        </back>
                        <sub-article article-type="translation" id="TRen" xml:lang="en">
                            <back>
                                <ref-list>
                                    <ref id="B3">
                                        <label>%s</label>
                                        <mixed-citation>. FOO in EN</mixed-citation>
                                    </ref>
                                </ref-list>
                            </back>
                        </sub-article>
                    </article>
                """ % (label_text['pt'], label_text['en'])
        fp = io.BytesIO(sample.encode('utf-8'))
        et = etree.parse(fp)
        for lang, html_output in domain.HTMLGenerator(et, valid_only=False):
            found_ref_label_text = html_output.xpath('//div[@class="ref"]//sup[@class="xref big"]')
            self.assertEqual(1, len(found_ref_label_text))
            found_ref_anchor = html_output.xpath('//div[@class="ref"]//a[@id="B3"]')
            self.assertEqual(1, len(found_ref_anchor))
            self.assertEqual(label_text[lang], found_ref_label_text[0].text.strip())

    @unittest.skip('tag glossary não é exibida por enquanto')
    def test_label_tag_inside_glossary(self):
        """
        verifica que o tag <label> dentro de <glossary> seja correto
        - - -
        <label> aparece em:
        <aff>, <corresp>, <fn>, <fig>, <table-wrap>, <disp-formula>, <media>, <supplementary-material>, <list>, <list-item>, <ref>, <glossary>, <app>, <def-list>
        """
        label_text = {
            'pt': 'Material Adicional',
            'en': 'Additional material',
        }
        sample = u"""<?xml version="1.0" encoding="UTF-8"?>
                    <!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "JATS-journalpublishing1.dtd">
                    <article xmlns:xlink="http://www.w3.org/1999/xlink" xml:lang="pt">
                        <back>
                            <glossary id="gloss01">
                                <label>%s</label>
                                <def-list>
                                    <def-item>
                                        <term>Metabólito</term>
                                        <def><p>É qualquer intermediário ou produto resultante do metabolismo.</p></def>
                                    </def-item>
                                </def-list>
                            </glossary>
                        </back>

                        <sub-article article-type="translation" id="TRen" xml:lang="en">
                            <back>
                                <glossary id="gloss01">
                                    <label>%s</label>
                                    <def-list>
                                        <def-item>
                                            <term>Metabólite lipsum</term>
                                            <def><p>Foo Bar.</p></def>
                                        </def-item>
                                    </def-list>
                                </glossary>
                            </back>
                        </sub-article>
                    </article>
                """ % (label_text['pt'], label_text['en'])
        fp = io.BytesIO(sample.encode('utf-8'))
        et = etree.parse(fp)
        for lang, html_output in domain.HTMLGenerator(et, valid_only=False):
            # print etree.tostring(html_output, method="html", pretty_print=True)
            found_labels = html_output.xpath('//label[@for="gloss01"]')
            self.assertEqual(1, len(found_labels))
            found_label = found_labels[0]
            self.assertEqual(label_text[lang], found_label.text.strip())

    @unittest.skip('tag app/app-group não é exibida por enquanto')
    def test_label_tag_inside_app(self):
        """
        verifica que o tag <label> dentro de <app> seja correto
        - - -
        <label> aparece em:
        <aff>, <corresp>, <fn>, <fig>, <table-wrap>, <disp-formula>, <media>, <supplementary-material>, <list>, <list-item>, <ref>, <glossary>, <app>, <def-list>
        """
        label_text = {
            'pt': 'Apêndice 1',
            'en': 'Appendix 1',
        }
        sample = u"""<?xml version="1.0" encoding="UTF-8"?>
                    <!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "JATS-journalpublishing1.dtd">
                    <article xmlns:xlink="http://www.w3.org/1999/xlink" xml:lang="pt">
                        <back>
                            <app-group>
                                <app id="app01">
                                    <label>%s</label>
                                    <title>Questionário  para SciELO</title>
                                    <graphic xlink:href="1234-5678-rctb-45-05-0110-app01.tif"/>
                                </app>
                            </app-group>
                        </back>
                        <sub-article article-type="translation" id="TRen" xml:lang="en">
                            <back>
                                <app-group>
                                    <app id="app01">
                                        <label>%s</label>
                                        <title>Questionnaire for SciELO</title>
                                        <graphic xlink:href="1234-5678-rctb-45-05-0110-app01.tif"/>
                                    </app>
                                </app-group>
                            </back>
                        </sub-article>
                    </article>
                """ % (label_text['pt'], label_text['en'])
        fp = io.BytesIO(sample.encode('utf-8'))
        et = etree.parse(fp)
        for lang, html_output in domain.HTMLGenerator(et, valid_only=False):
            # print etree.tostring(html_output, method="html", pretty_print=True)
            found_labels = html_output.xpath('//label[@for="app01"]')
            self.assertEqual(1, len(found_labels))
            found_label = found_labels[0]
            self.assertEqual(label_text[lang], found_label.text.strip())

    @unittest.skip('tag def-list não é exibida por enquanto')
    def test_label_tag_inside_def_list(self):
        """
        verifica que o tag <label> dentro de <def-list> seja correto
        - - -
        <label> aparece em:
        <aff>, <corresp>, <fn>, <fig>, <table-wrap>, <disp-formula>, <media>, <supplementary-material>, <list>, <list-item>, <ref>, <glossary>, <app>, <def-list>
        """
        label_text = {
            'pt': 'Lista de Definições 1',
            'en': 'Definitions list 1',
        }
        sample = u"""<?xml version="1.0" encoding="UTF-8"?>
                    <!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "JATS-journalpublishing1.dtd">
                    <article xmlns:xlink="http://www.w3.org/1999/xlink" xml:lang="pt">
                        <back>
                            <def-list id="d01">
                                <label>%s</label>
                                <def-item>
                                    <term><bold>Angina pectoris (Angina de peito)</bold></term>
                                    <def><p>Sensação de angústia, de opressão torácica</p></def>
                                </def-item>
                            </def-list>
                        </back>
                        <sub-article article-type="translation" id="TRen" xml:lang="en">
                            <back>
                                <def-list id="d01">
                                    <label>%s</label>
                                    <def-item>
                                        <term><bold>Angina pectoris</bold></term>
                                        <def><p>Lorem ipsum dolor sit amet</p></def>
                                    </def-item>
                                </def-list>
                            </back>
                        </sub-article>
                    </article>
                """ % (label_text['pt'], label_text['en'])
        fp = io.BytesIO(sample.encode('utf-8'))
        et = etree.parse(fp)
        for lang, html_output in domain.HTMLGenerator(et, valid_only=False):
            found_labels = html_output.xpath('//label[@for="d01"]')
            self.assertEqual(1, len(found_labels))
            found_label = found_labels[0]
            self.assertEqual(label_text[lang], found_label.text.strip())

    """ <P> """
    def test_p_tag_inside_abstract(self):
        """
        verifica que o tag <p> dentro de <abstract> seja correto
        - - -
        <p> aparece em
        <abstract>, <sec>, <trans-abstract>, <fn>, <body>, <disp-quote>, list-item, sig, app, def
        """
        paragraph_text = {
            'pt': 'abstract em PT',
            'en': 'abstract em EN',
        }
        sample = u"""<?xml version="1.0" encoding="UTF-8"?>
                <!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "JATS-journalpublishing1.dtd">
                <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" dtd-version="1.0" article-type="review-article" xml:lang="pt">
                    <front>
                        <article-meta>
                            <abstract xml:lang="pt">
                                <p>%s</p>
                            </abstract>
                        </article-meta>
                    </front>
                    <sub-article article-type="translation" id="TRen" xml:lang="en">
                        <front-stub>
                            <abstract xml:lang="en">
                                <p>%s</p>
                            </abstract>
                        </front-stub>
                    </sub-article>
                </article>
                """ % (paragraph_text['pt'], paragraph_text['en'])
        fp = io.BytesIO(sample.encode('utf-8'))
        et = etree.parse(fp)
        for lang, html_output in domain.HTMLGenerator(et, valid_only=False):
            found_paragraphs = html_output.xpath('//div[@class="abstract"]//p[@class="abstract-p"]')
            self.assertEqual(1, len(found_paragraphs))
            found_paragraph = found_paragraphs[0]
            self.assertEqual(paragraph_text[lang], found_paragraph.text.strip())

    def test_p_tag_inside_sec(self):
        """
        verifica que o tag <p> dentro de <sec> seja correto
        - - -
        <p> aparece em
        <abstract>, <sec>, <trans-abstract>, <fn>, <body>, <disp-quote>, list-item, sig, app, def
        """
        paragraph_text = {
            'pt': 'texto em PT',
            'en': 'text in EN',
        }
        sample = u"""<?xml version="1.0" encoding="UTF-8"?>
                <!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "JATS-journalpublishing1.dtd">
                <article xmlns:xlink="http://www.w3.org/1999/xlink" dtd-version="1.0" article-type="review-article" xml:lang="pt">
                    <body>
                        <sec sec-type="intro">
                            <p>%s</p>
                        </sec>
                    </body>
                    <sub-article xml:lang="en" article-type="translation" id="S01">
                        <body>
                            <sec sec-type="intro">
                                <p>%s</p>
                            </sec>
                        </body>
                    </sub-article>
                </article>
                """ % (paragraph_text['pt'], paragraph_text['en'])
        fp = io.BytesIO(sample.encode('utf-8'))
        et = etree.parse(fp)
        for lang, html_output in domain.HTMLGenerator(et, valid_only=False):
            found_paragraphs = html_output.xpath('//article[@class="body-wrapper"]//p')
            self.assertEqual(1, len(found_paragraphs))
            found_paragraph = found_paragraphs[0]
            self.assertEqual(paragraph_text[lang], found_paragraph.text.strip())

    def test_p_tag_inside_fn(self):
        """
        verifica que o tag <p> dentro de <fn> seja correto
        - - -
        <p> aparece em
        <abstract>, <sec>, <trans-abstract>, <fn>, <body>, <disp-quote>, list-item, sig, app, def
        """
        paragraph_text = {
            'pt': 'Declaração: Sim',
            'en': 'Declaration: Yes',
        }
        sample = u"""<?xml version="1.0" encoding="UTF-8"?>
                <!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "JATS-journalpublishing1.dtd">
                <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" dtd-version="1.0" article-type="review-article" xml:lang="pt">
                    <back>
                        <fn-group>
                            <fn fn-type="financial-disclosure" id="fn01">
                                <label>1</label>
                                <p>%s</p>
                            </fn>
                        </fn-group>
                    </back>
                    <sub-article article-type="translation" id="TRen" xml:lang="en">
                        <back>
                            <fn-group>
                                <fn fn-type="financial-disclosure" id="fn01">
                                    <label>1</label>
                                    <p>%s</p>
                                </fn>
                            </fn-group>
                        </back>
                    </sub-article>
                </article>
                """ % (paragraph_text['pt'], paragraph_text['en'])
        fp = io.BytesIO(sample.encode('utf-8'))
        et = etree.parse(fp)
        for lang, html_output in domain.HTMLGenerator(et, valid_only=False):
            found_paragraphs = html_output.xpath('//div[@class="fn-content"]//p')
            self.assertEqual(1, len(found_paragraphs))
            found_paragraph = found_paragraphs[0]
            self.assertEqual(paragraph_text[lang], found_paragraph.text.strip())

    def test_p_tag_inside_body(self):
        """
        verifica que o tag <p> dentro de <body> seja correto
        - - -
        <p> aparece em
        <abstract>, <sec>, <trans-abstract>, <fn>, <body>, <disp-quote>, list-item, sig, app, def
        """
        paragraph_text = {
            'pt': 'texto em PT',
            'en': 'text in EN',
        }
        sample = u"""<?xml version="1.0" encoding="UTF-8"?>
                <!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "JATS-journalpublishing1.dtd">
                <article xmlns:xlink="http://www.w3.org/1999/xlink" dtd-version="1.0" article-type="review-article" xml:lang="pt">
                    <body>
                        <p>%s</p>
                    </body>
                    <sub-article xml:lang="en" article-type="translation" id="S01">
                        <body>
                            <p>%s</p>
                        </body>
                    </sub-article>
                </article>
                """ % (paragraph_text['pt'], paragraph_text['en'])
        fp = io.BytesIO(sample.encode('utf-8'))
        et = etree.parse(fp)
        for lang, html_output in domain.HTMLGenerator(et, valid_only=False):
            found_paragraphs = html_output.xpath('//article[@class="body-wrapper"]//p')
            self.assertEqual(1, len(found_paragraphs))
            found_paragraph = found_paragraphs[0]
            self.assertEqual(paragraph_text[lang], found_paragraph.text.strip())

    def test_p_tag_inside_disp_quote(self):
        """
        verifica que o tag <p> dentro de <disp-quote> seja correto
        - - -
        <p> aparece em
        <abstract>, <sec>, <trans-abstract>, <fn>, <body>, <disp-quote>, list-item, sig, app, def
        """
        paragraph_text = {
            'pt': 'texto em PT',
            'en': 'text in EN',
        }
        sample = u"""<?xml version="1.0" encoding="UTF-8"?>
                <!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "JATS-journalpublishing1.dtd">
                <article xmlns:xlink="http://www.w3.org/1999/xlink" dtd-version="1.0" article-type="review-article" xml:lang="pt">
                    <body>
                        <sec sec-type="methods">
                            <p>
                                <disp-quote>
                                    <p>%s</p>
                                </disp-quote>
                            </p>
                        </sec>
                    </body>
                    <sub-article xml:lang="en" article-type="translation" id="S01">
                        <body>
                            <sec sec-type="methods">
                                <p>
                                    <disp-quote>
                                        <p>%s</p>
                                    </disp-quote>
                                </p>
                            </sec>
                        </body>
                    </sub-article>
                </article>
                """ % (paragraph_text['pt'], paragraph_text['en'])
        fp = io.BytesIO(sample.encode('utf-8'))
        et = etree.parse(fp)
        for lang, html_output in domain.HTMLGenerator(et, valid_only=False):
            found_paragraphs = html_output.xpath('//blockquote[@class="disp-quote"]//p')
            self.assertEqual(1, len(found_paragraphs))
            found_paragraph = found_paragraphs[0]
            self.assertEqual(paragraph_text[lang], found_paragraph.text.strip())

    def test_p_tag_inside_list_item(self):
        """
        verifica que o tag <p> dentro de <list-item> seja correto
        - - -
        <p> aparece em:
        <abstract>, <sec>, <trans-abstract>, <fn>, <body>, <disp-quote>, list-item, sig, app, def
        """
        paragraph_text = {
            'pt': 'Material Adicional',
            'en': 'Additional material',
        }
        sample = u"""<?xml version="1.0" encoding="UTF-8"?>
                    <!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "JATS-journalpublishing1.dtd">
                    <article xmlns:xlink="http://www.w3.org/1999/xlink" xml:lang="pt">
                        <body>
                            <sec sec-type="list">
                                <p>
                                    <list list-type="order">
                                        <title>Lista Númerica</title>
                                        <list-item>
                                            <label>ITEM UM</label>
                                            <p>%s</p>
                                        </list-item>
                                    </list>
                                </p>
                            </sec>
                        </body>
                        <sub-article article-type="translation" id="TRen" xml:lang="en">
                            <body>
                                <sec sec-type="supplementary-material">
                                    <p>
                                        <list list-type="order">
                                            <title>Numeric List</title>
                                            <list-item>
                                                <label>ITEM ONE</label>
                                                <p>%s</p>
                                            </list-item>
                                        </list>
                                    </p>
                                </sec>
                            </body>
                        </sub-article>
                    </article>
                """ % (paragraph_text['pt'], paragraph_text['en'])
        fp = io.BytesIO(sample.encode('utf-8'))
        et = etree.parse(fp)
        for lang, html_output in domain.HTMLGenerator(et, valid_only=False):
            found_paragraphs = html_output.xpath('//div[@class="list-item-content"]//p')
            self.assertEqual(1, len(found_paragraphs))
            found_paragraph = found_paragraphs[0]
            self.assertEqual(paragraph_text[lang], found_paragraph.text.strip())

    def test_p_tag_inside_sig(self):
        """
        verifica que o tag <p> dentro de <sig> seja correto
        - - -
        <p> aparece em:
        <abstract>, <sec>, <trans-abstract>, <fn>, <body>, <disp-quote>, list-item, sig, app, def
        """
        paragraph_text = {
            'pt': 'Sig PT',
            'en': 'Sig EN',
        }
        sample = u"""<?xml version="1.0" encoding="UTF-8"?>
                    <!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "JATS-journalpublishing1.dtd">
                    <article xmlns:xlink="http://www.w3.org/1999/xlink" xml:lang="pt">
                        <body>
                            <sig-block>
                                <sig>
                                    <p>%s</p>
                                </sig>
                            </sig-block>
                        </body>
                        <sub-article article-type="translation" id="TRen" xml:lang="en">
                            <body>
                                <sig-block>
                                    <sig>
                                        <p>%s</p>
                                    </sig>
                                </sig-block>
                            </body>
                        </sub-article>
                    </article>
                """ % (paragraph_text['pt'], paragraph_text['en'])
        fp = io.BytesIO(sample.encode('utf-8'))
        et = etree.parse(fp)
        for lang, html_output in domain.HTMLGenerator(et, valid_only=False):
            found_paragraphs = html_output.xpath('//div[@class="sig-block"]//p')
            self.assertEqual(1, len(found_paragraphs))
            found_paragraph = found_paragraphs[0]
            self.assertEqual(paragraph_text[lang], found_paragraph.text.strip())

    @unittest.skip('tag app/app-group não é exibida por enquanto')
    def test_p_tag_inside_app(self):
        """
        verifica que o tag <p> dentro de <app> seja correto
        - - -
        <p> aparece em:
        <abstract>, <sec>, <trans-abstract>, <fn>, <body>, <disp-quote>, list-item, sig, app, def
        """
        paragraph_text = {
            'pt': 'texto PT',
            'en': 'text EN',
        }
        sample = u"""<?xml version="1.0" encoding="UTF-8"?>
                    <!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "JATS-journalpublishing1.dtd">
                    <article xmlns:xlink="http://www.w3.org/1999/xlink" xml:lang="pt">
                        <back>
                            <app-group>
                                <app id="app01">
                                    <label>App 01</label>
                                    <p>%s</p>
                                </app>
                            </app-group>
                        </back>
                        <sub-article article-type="translation" id="TRen" xml:lang="en">
                            <back>
                                <app-group>
                                    <app id="app01">
                                        <label>App 01</label>
                                        <p>%s</p>
                                    </app>
                                </app-group>
                            </back>
                        </sub-article>
                    </article>
                """ % (paragraph_text['pt'], paragraph_text['en'])
        fp = io.BytesIO(sample.encode('utf-8'))
        et = etree.parse(fp)
        for lang, html_output in domain.HTMLGenerator(et, valid_only=False):
            found_paragraphs = html_output.xpath('//div[@class="app-content"]//p')
            self.assertEqual(1, len(found_paragraphs))
            found_paragraph = found_paragraphs[0]
            self.assertEqual(paragraph_text[lang], found_paragraph.text.strip())

    @unittest.skip('tag def-list não é exibida por enquanto')
    def test_p_tag_inside_def(self):
        """
        verifica que o tag <p> dentro de <def> seja correto
        - - -
        <p> aparece em:
        <abstract>, <sec>, <trans-abstract>, <fn>, <body>, <disp-quote>, list-item, sig, app, def
        """
        paragraph_text = {
            'pt': 'texto PT',
            'en': 'text EN',
        }
        sample = u"""<?xml version="1.0" encoding="UTF-8"?>
                    <!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "JATS-journalpublishing1.dtd">
                    <article xmlns:xlink="http://www.w3.org/1999/xlink" xml:lang="pt">
                        <back>
                            <def-list id="d01">
                                <label>lista 01</label>
                                <def-item>
                                    <term><bold>Angina pectoris (Angina de peito)</bold></term>
                                    <def><p>%s</p></def>
                                </def-item>
                            </def-list>
                        </back>
                        <sub-article article-type="translation" id="TRen" xml:lang="en">
                            <back>
                                <def-list id="d01">
                                    <label>list 01</label>
                                    <def-item>
                                        <term><bold>Angina pectoris</bold></term>
                                        <def><p>%s</p></def>
                                    </def-item>
                                </def-list>
                            </back>
                        </sub-article>
                    </article>
                """ % (paragraph_text['pt'], paragraph_text['en'])
        fp = io.BytesIO(sample.encode('utf-8'))
        et = etree.parse(fp)
        for lang, html_output in domain.HTMLGenerator(et, valid_only=False):
            found_paragraphs = html_output.xpath('//dd[@class="def-list-item"]//p')
            self.assertEqual(1, len(found_paragraphs))
            found_paragraph = found_paragraphs[0]
            self.assertEqual(paragraph_text[lang], found_paragraph.text.strip())

    """ <EMAIL> """
    def test_email_tag(self):
        """
        generate the HTML, and then check the <email> tags appears correctly as a link
        """
        # with
        email_destination = 'foo.bar@baz.edu'
        email_href = 'mailto:%s' % email_destination
        sample = u"""<?xml version="1.0" encoding="UTF-8"?>
                    <!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "JATS-journalpublishing1.dtd">
                    <article xmlns:xlink="http://www.w3.org/1999/xlink" dtd-version="1.0" article-type="review-article" xml:lang="pt">
                        <front>
                            <article-meta>
                                <author-notes>
                                    <corresp>
                                        <label>Correspondência</label>:  Foo Bar dos Santos  Av. Dr. Lorem Ipsum Júnior, 1250  38064-200 Uberaba, MG, Brasil  E-mail: <email>%s</email>
                                    </corresp>
                                </author-notes>
                            </article-meta>
                        </front>
                        <sub-article xml:lang="en" article-type="translation" id="S01">
                            <front-stub>
                                <author-notes>
                                    <corresp>
                                        <label>Correspondence</label>:  Foo Bar dos Santos  Av. Dr. Lorem Ipsum Júnior, 1250  38064-200 Uberaba, MG, Brasil  E-mail: <email>%s</email>
                                    </corresp>
                                </author-notes>
                            </front-stub>
                        </sub-article>
                    </article>
                """ % (email_destination, email_destination)

        fp = io.BytesIO(sample.encode('utf-8'))
        et = etree.parse(fp)
        # when
        for lang, html_output in domain.HTMLGenerator(et, valid_only=False):
            emails_links = html_output.xpath('//div[@class="author-notes"]//a[@href="%s"]' % email_href)
            # then
            self.assertEqual(1, len(emails_links))
            found_email_link = emails_links[0]
            found_email_href = 'mailto:%s' % found_email_link.attrib['href']
            found_email_text = found_email_link.text
            self.assertIn(email_href, found_email_href)
            self.assertEqual(email_destination, found_email_text)

    """ <SUP> """
    def test_sup_tag_inside_xref(self):
        """
        generate the HTML, and then check the <sup> (inside xref) tags is correct
        """
        # with
        SUP_TEXT = 'FOO'
        sample = u"""<?xml version="1.0" encoding="UTF-8"?>
                <!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "JATS-journalpublishing1.dtd">
                <article xmlns:xlink="http://www.w3.org/1999/xlink" dtd-version="1.0" article-type="review-article" xml:lang="pt">
                    <body>
                        <sec sec-type="intro">
                            <p>lorem ipsum dolor sit amet, consectetur adipisicing elit, <xref ref-type="bibr" rid="B4"><sup>%s</sup></xref></p>
                        </sec>
                    </body>
                    <sub-article xml:lang="en" article-type="translation" id="S01">
                        <body>
                            <sec sec-type="intro">
                                <p>lorem ipsum dolor sit amet, consectetur adipisicing elit, <xref ref-type="bibr" rid="B4"><sup>%s</sup></xref></p>
                            </sec>
                        </body>
                    </sub-article>
                </article>
                """ % (SUP_TEXT, SUP_TEXT)

        fp = io.BytesIO(sample.encode('utf-8'))
        et = etree.parse(fp)
        # when
        for lang, html_output in domain.HTMLGenerator(et, valid_only=False):
            found_sup_nodes = html_output.xpath('//sup')
            # then
            self.assertEqual(1, len(found_sup_nodes))
            found_sup_node = found_sup_nodes[0]
            found_sup_text = found_sup_node.text
            self.assertEqual(SUP_TEXT, found_sup_text)

    def test_sup_tag_inside_p(self):
        """
        generate the HTML, and then check the <sup> (inside paragraphs) tags is correct
        """
        # with
        SUP_TEXT = 'FOO'
        sample = u"""<?xml version="1.0" encoding="UTF-8"?>
                <!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "JATS-journalpublishing1.dtd">
                <article xmlns:xlink="http://www.w3.org/1999/xlink" dtd-version="1.0" article-type="review-article" xml:lang="pt">
                    <body>
                        <sec sec-type="intro">
                            <p>lorem ipsum dolor sit amet, consectetur adipisicing elit, <sup>%s</sup></p>
                        </sec>
                    </body>
                    <sub-article xml:lang="en" article-type="translation" id="S01">
                        <body>
                            <sec sec-type="intro">
                                <p>lorem ipsum dolor sit amet, consectetur adipisicing elit, <sup>%s</sup></p>
                            </sec>
                        </body>
                    </sub-article>
                </article>
                """ % (SUP_TEXT, SUP_TEXT)

        fp = io.BytesIO(sample.encode('utf-8'))
        et = etree.parse(fp)
        # when
        for lang, html_output in domain.HTMLGenerator(et, valid_only=False):
            found_sup_nodes = html_output.xpath('//sup')
            # then
            self.assertEqual(1, len(found_sup_nodes))
            found_sup_node = found_sup_nodes[0]
            found_sup_text = found_sup_node.text
            self.assertEqual(SUP_TEXT, found_sup_text)

    """ <SUB> """
    def test_sub_tag_inside_xref(self):
        """
        generate the HTML, and then check the <sub> (inside xref) tags is correct
        """
        # with
        SUB_TEXT = 'FOO'
        sample = u"""<?xml version="1.0" encoding="UTF-8"?>
                <!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "JATS-journalpublishing1.dtd">
                <article xmlns:xlink="http://www.w3.org/1999/xlink" dtd-version="1.0" article-type="review-article" xml:lang="pt">
                    <body>
                        <sec sec-type="intro">
                            <p>lorem ipsum dolor sit amet, consectetur adipisicing elit, <xref ref-type="bibr" rid="B4"><sub>%s</sub></xref></p>
                        </sec>
                    </body>
                    <sub-article xml:lang="en" article-type="translation" id="S01">
                        <body>
                            <sec sec-type="intro">
                                <p>lorem ipsum dolor sit amet, consectetur adipisicing elit, <xref ref-type="bibr" rid="B4"><sub>%s</sub></xref></p>
                            </sec>
                        </body>
                    </sub-article>
                </article>
                """ % (SUB_TEXT, SUB_TEXT)

        fp = io.BytesIO(sample.encode('utf-8'))
        et = etree.parse(fp)
        # when
        for lang, html_output in domain.HTMLGenerator(et, valid_only=False):
            found_sub_nodes = html_output.xpath('//sub')
            # then
            self.assertEqual(1, len(found_sub_nodes))
            found_sub_node = found_sub_nodes[0]
            found_sub_text = found_sub_node.text
            self.assertEqual(SUB_TEXT, found_sub_text)

    def test_sub_tag_inside_p(self):
        """
        generate the HTML, and then check the <sub> (inside paragraphs) tags is correct
        """
        # with
        SUB_TEXT = 'FOO'
        sample = u"""<?xml version="1.0" encoding="UTF-8"?>
                <!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "JATS-journalpublishing1.dtd">
                <article xmlns:xlink="http://www.w3.org/1999/xlink" dtd-version="1.0" article-type="review-article" xml:lang="pt">
                    <body>
                        <sec sec-type="intro">
                            <p>lorem ipsum dolor sit amet, consectetur adipisicing elit, <sub>%s</sub></p>
                        </sec>
                    </body>
                    <sub-article xml:lang="en" article-type="translation" id="S01">
                        <body>
                            <sec sec-type="intro">
                                <p>lorem ipsum dolor sit amet, consectetur adipisicing elit, <sub>%s</sub></p>
                            </sec>
                        </body>
                    </sub-article>
                </article>
                """ % (SUB_TEXT, SUB_TEXT)

        fp = io.BytesIO(sample.encode('utf-8'))
        et = etree.parse(fp)
        # when
        for lang, html_output in domain.HTMLGenerator(et, valid_only=False):
            found_sub_nodes = html_output.xpath('//sub')
            # then
            self.assertEqual(1, len(found_sub_nodes))
            found_sub_node = found_sub_nodes[0]
            found_sub_text = found_sub_node.text
            self.assertEqual(SUB_TEXT, found_sub_text)
