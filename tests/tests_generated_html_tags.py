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


class GeneratedFrontTagsTests(unittest.TestCase):

    # **************** #
    # ***** FRONT **** #
    # **************** #

    """ <ISSN> """
    def test_issn_tag_for_epub_and_ppub(self):
        """
        verifica que o tag <issn> (epub e ppub) no seja correto no html
        """
        issn_text = {
            'epub': '1808-8686',
            'ppub': '1808-8694',
        }
        sample = u"""<?xml version="1.0" encoding="UTF-8"?>
                    <!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "JATS-journalpublishing1.dtd">
                    <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="review-article" xml:lang="pt">
                        <front>
                            <journal-meta>
                                <issn pub-type="epub">%s</issn>
                                <issn pub-type="ppub">%s</issn>
                            </journal-meta>
                        </front>
                    </article>
                """ % (issn_text['epub'], issn_text['ppub'])

        fp = io.BytesIO(sample.encode('utf-8'))
        et = etree.parse(fp)
        for lang, html_output in domain.HTMLGenerator(et, valid_only=False):
            found_issn = html_output.xpath('//span[@id="issn"]//span')
            self.assertEqual(2, len(found_issn))
            found_ppub = html_output.xpath('//span[@id="issn"]//span[@class="ppub"]')[0]
            found_epub = html_output.xpath('//span[@id="issn"]//span[@class="epub"]')[0]
            self.assertEqual(issn_text['ppub'], found_ppub.text.strip())
            self.assertEqual(issn_text['epub'], found_epub.text.strip())

    """ <DOI> """
    def test_doi_link(self):
        """
        verifica que o DOI e o link do DOI seja correto no html
        """
        # with
        doi = '10.1590/S0034-8910.2014048004923'
        sample = u"""<?xml version="1.0" encoding="UTF-8"?>
                    <!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "JATS-journalpublishing1.dtd">
                    <article xmlns:xlink="http://www.w3.org/1999/xlink" dtd-version="1.0" article-type="review-article" xml:lang="pt">
                        <front>
                            <article-meta>
                                <article-id pub-id-type="doi">%s</article-id>
                            </article-meta>
                        </front>
                        <sub-article xml:lang="en" article-type="translation" id="S01">
                        </sub-article>
                        <sub-article xml:lang="es" article-type="translation" id="S02">
                        </sub-article>
                    </article>
                """ % doi

        fp = io.BytesIO(sample.encode('utf-8'))
        et = etree.parse(fp)
        # when
        for lang, html_output in domain.HTMLGenerator(et, valid_only=False):
            doi_plain_texts = html_output.xpath('//span[@id="doi"]')
            doi_links = html_output.xpath('//span[@id="doi-link"]/a')
            # then
            self.assertEqual(1, len(doi_links))
            self.assertEqual(1, len(doi_plain_texts))

            doi_link = doi_links[0]
            doi_plain_text = doi_plain_texts[0]

            doi_link_href = doi_link.attrib['href']
            doi_link_text = doi_link.text
            self.assertIn(doi, doi_link_href)
            self.assertEqual("http://dx.doi.org/" + doi, doi_link_text.strip())

    """ <ARTICLE-CATEGORIES>, <SUBJ-GROUP>, <SUBJECT> """
    @unittest.skip('tag article-categories não é exibida por enquanto')
    def test_article_categories_and_subjects_tag(self):
        """
        verifica que o tag <article-categories> e <subject> seja correto no html.
        - - -
        <article-categories> aparece em: <article-meta>
        <subj-group> aparece em: <article-categories>
        <subject> aparece em: <subj-group>
        """
        subjects = {
            'pt': 'Biotecnologia',
            'en': 'Biotechnology',
        }
        sample = u"""<?xml version="1.0" encoding="UTF-8"?>
                    <!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "JATS-journalpublishing1.dtd">
                    <article xml:lang="pt">
                        <front>
                            <article-meta>
                                <article-categories>
                                    <subj-group subj-group-type="heading">
                                        <subject>%s</subject>
                                    </subj-group>
                                </article-categories>
                            </article-meta>
                        </front>
                        <sub-article xml:lang="en" article-type="translation" id="S01">
                            <front-stub>
                                <article-categories>
                                    <subj-group subj-group-type="heading">
                                        <subject>%s</subject>
                                    </subj-group>
                                </article-categories>
                            </front-stub>
                        </sub-article>
                    </article>
                 """ % (subjects['pt'], subjects['en'])
        fp = io.BytesIO(sample.encode('utf-8'))
        et = etree.parse(fp)
        for lang, html_output in domain.HTMLGenerator(et, valid_only=False):
            subject_tags = html_output.xpath('//ul[@class="article-categories"]/li')
            self.assertEqual(1, len(subject_tags))
            self.assertEqual(subjects[lang], subject_tags[0].text.strip())

    """ <TITLE-GROUP>, <ARTICLE-TITLE>, <TRANS-TITLE-GROUP>, <TRANS-TITLE>"""
    def test_article_title_tag_and_trans_title_tag(self):
        """
        verifica que o tag <article-title> (<trans-title-group> para as traduções) seja correto no tag <title> html.
        """
        titles = {
            'pt': 'titulo em PT',
            'en': 'titulo em EN',
            'es': 'titulo em ES',
        }
        sample = u"""<?xml version="1.0" encoding="UTF-8"?>
                    <!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "JATS-journalpublishing1.dtd">
                    <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="review-article" xml:lang="pt">
                        <front>
                            <journal-meta>
                                <journal-id journal-id-type="nlm-ta">Rev Saude Publica</journal-id>
                            </journal-meta>
                            <article-meta>
                                <title-group>
                                    <article-title>%s</article-title>
                                    <trans-title-group xml:lang="en">
                                        <trans-title>%s</trans-title>
                                    </trans-title-group>
                                    <trans-title-group xml:lang="es">
                                        <trans-title>%s</trans-title>
                                    </trans-title-group>
                                </title-group>
                            </article-meta>
                        </front>
                    </article>
                """ % (titles['pt'], titles['en'], titles['es'])

        fp = io.BytesIO(sample.encode('utf-8'))
        et = etree.parse(fp)
        for lang, html_output in domain.HTMLGenerator(et, valid_only=False):
            found_titles = html_output.xpath('/html/head/title')
            self.assertEqual(1, len(found_titles))
            found_title = found_titles[0]
            title_text = found_title.text.strip().replace('\n', ' ')
            expected_text = u'Rev Saude Publica - %s' % titles[lang]
            self.assertEqual(title_text, expected_text)

    """ <CONTRIB-GROUP>, <CONTRIB>, <NAME>"""
    def test_contrib_group_tag_and_contrib_tag_and_name(self):
        """
        verifica que o tag <contrib-group> e <contrib> e <name> seja correto no html.
        - - -
        <contrib-group> aparece em: <article-meta>
        <contrib> aparece em: <contrib-group>
        <name> aparece em: <contrib>
        """
        contrib_names = {
            'surname': 'Vader',
            'given_names': 'Darth',
        }
        sample = u"""<?xml version="1.0" encoding="UTF-8"?>
                    <!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "JATS-journalpublishing1.dtd">
                    <article xml:lang="pt">
                        <front>
                            <article-meta>
                                <contrib-group>
                                    <contrib contrib-type="author">
                                        <name>
                                            <surname>%s</surname>
                                            <given-names>%s</given-names>
                                        </name>
                                    </contrib>
                                </contrib-group>
                            </article-meta>
                        </front>
                    </article>
                 """ % (contrib_names['surname'], contrib_names['given_names'])
        fp = io.BytesIO(sample.encode('utf-8'))
        et = etree.parse(fp)
        for lang, html_output in domain.HTMLGenerator(et, valid_only=False):
            contrib_tags = html_output.xpath('//ul[@class="contrib-group list-inline"]/li[@class="contrib-type author"]')
            self.assertEqual(1, len(contrib_tags))
            surname_tag = contrib_tags[0].xpath('span[@class="name"]/span[@class="surname"]')[0]
            given_name_tag = contrib_tags[0].xpath('span[@class="name"]/span[@class="given_names"]')[0]
            self.assertEqual(contrib_names['surname'], surname_tag.text.strip())
            self.assertEqual(contrib_names['given_names'], given_name_tag.text.strip())

    """ <CONTRIB-GROUP>, <CONTRIB>, <COLLAB>"""
    def test_contrib_group_tag_and_contrib_tag_and_collab_tag(self):
        """
        verifica que o tag <contrib-group> e <contrib> e <collab> seja correto no html.
        - - -
        <contrib-group> aparece em: <article-meta>
        <contrib> aparece em: <contrib-group>
        <collab> aparece em: <contrib>
        """
        collab_text = 'lorem ipsum'
        sample = u"""<?xml version="1.0" encoding="UTF-8"?>
                    <!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "JATS-journalpublishing1.dtd">
                    <article xml:lang="pt">
                        <front>
                            <article-meta>
                                <contrib-group>
                                    <contrib contrib-type="author">
                                        <collab>%s</collab>
                                    </contrib>
                                </contrib-group>
                            </article-meta>
                        </front>
                    </article>
                 """ % collab_text
        fp = io.BytesIO(sample.encode('utf-8'))
        et = etree.parse(fp)
        for lang, html_output in domain.HTMLGenerator(et, valid_only=False):
            collab_tags = html_output.xpath('//div[@class="collab"]')
            self.assertEqual(1, len(collab_tags))
            collab_tag = collab_tags[0]
            self.assertEqual(collab_text, collab_tag.text.strip())

    """ <ON-BEHALF-OF> """
    def test_on_behalf_of_tag_inside_contrib_tag(self):
        """
        verifica que o tag <on-behalf-of> dentro de <contrib> seja correto no html.
        - - -
        <on-behalf-of> aparece em: <contrib-group>, <contrib>
        """
        behalf_text = 'lorem ipsum'
        sample = u"""<?xml version="1.0" encoding="UTF-8"?>
                    <!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "JATS-journalpublishing1.dtd">
                    <article xml:lang="pt">
                        <front>
                            <article-meta>
                                <contrib-group>
                                    <contrib contrib-type="author">
                                        <on-behalf-of>%s</on-behalf-of>
                                    </contrib>
                                </contrib-group>
                            </article-meta>
                        </front>
                    </article>
                 """ % behalf_text
        fp = io.BytesIO(sample.encode('utf-8'))
        et = etree.parse(fp)
        for lang, html_output in domain.HTMLGenerator(et, valid_only=False):
            behalf_tags = html_output.xpath('//div[@class="on_behalf_of"]')
            self.assertEqual(1, len(behalf_tags))
            behalf_tag = behalf_tags[0]
            self.assertEqual(behalf_text, behalf_tag.text.strip())

    def test_on_behalf_of_tag_inside_contrib_group_tag(self):
        """
        verifica que o tag <on-behalf-of> dentro de <contrib> seja correto no html.
        - - -
        <on-behalf-of> aparece em: <contrib-group>, <contrib>
        """
        behalf_text = 'lorem ipsum'
        sample = u"""<?xml version="1.0" encoding="UTF-8"?>
                    <!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "JATS-journalpublishing1.dtd">
                    <article xml:lang="pt">
                        <front>
                            <article-meta>
                                <contrib-group>
                                    <on-behalf-of>%s</on-behalf-of>
                                </contrib-group>
                            </article-meta>
                        </front>
                    </article>
                 """ % behalf_text
        fp = io.BytesIO(sample.encode('utf-8'))
        et = etree.parse(fp)
        for lang, html_output in domain.HTMLGenerator(et, valid_only=False):
            behalf_tags = html_output.xpath('//div[@class="on_behalf_of"]')
            self.assertEqual(1, len(behalf_tags))
            behalf_tag = behalf_tags[0]
            self.assertEqual(behalf_text, behalf_tag.text.strip())

    """ <ROLE> """
    def test_role_tag_inside_collab_tag(self):
        """
        verifica que o tag <role> dentro de <collab> seja correto no html.
        - - -
        <role> aparece em: <collab>, <contrib>, <contrib-group>, <element-citation>, <person-group>, <product>
        """
        role_text = 'lorem ipsum'
        sample = u"""<?xml version="1.0" encoding="UTF-8"?>
                    <!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "JATS-journalpublishing1.dtd">
                    <article xml:lang="pt">
                        <front>
                            <article-meta>
                                <contrib-group>
                                    <contrib contrib-type="author">
                                        <collab>
                                            <role>%s</role>
                                        </collab>
                                    </contrib>
                                </contrib-group>
                            </article-meta>
                        </front>
                    </article>
                 """ % role_text
        fp = io.BytesIO(sample.encode('utf-8'))
        et = etree.parse(fp)
        for lang, html_output in domain.HTMLGenerator(et, valid_only=False):
            role_tags = html_output.xpath('//span[@class="role"]')
            self.assertEqual(1, len(role_tags))
            role_tag = role_tags[0]
            self.assertEqual(role_text, role_tag.text.strip())

    def test_role_tag_inside_contrib_tag(self):
        """
        verifica que o tag <role> dentro de <contrib> seja correto no html.
        - - -
        <role> aparece em: <collab>, <contrib>, <contrib-group>, <element-citation>, <person-group>, <product>
        """
        role_text = 'lorem ipsum'
        sample = u"""<?xml version="1.0" encoding="UTF-8"?>
                    <!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "JATS-journalpublishing1.dtd">
                    <article xml:lang="pt">
                        <front>
                            <article-meta>
                                <contrib-group>
                                    <contrib contrib-type="author">
                                        <role>%s</role>
                                    </contrib>
                                </contrib-group>
                            </article-meta>
                        </front>
                    </article>
                 """ % role_text
        fp = io.BytesIO(sample.encode('utf-8'))
        et = etree.parse(fp)
        for lang, html_output in domain.HTMLGenerator(et, valid_only=False):
            role_tags = html_output.xpath('//span[@class="role"]')
            self.assertEqual(1, len(role_tags))
            role_tag = role_tags[0]
            self.assertEqual(role_text, role_tag.text.strip())

    def test_role_tag_inside_contrib_group_tag(self):
        """
        verifica que o tag <role> dentro de <collab> seja correto no html.
        - - -
        <role> aparece em: <collab>, <contrib>, <contrib-group>, <element-citation>, <person-group>, <product>
        """
        role_text = 'lorem ipsum'
        sample = u"""<?xml version="1.0" encoding="UTF-8"?>
                    <!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "JATS-journalpublishing1.dtd">
                    <article xml:lang="pt">
                        <front>
                            <article-meta>
                                <contrib-group>
                                    <role>%s</role>
                                </contrib-group>
                            </article-meta>
                        </front>
                    </article>
                 """ % role_text
        fp = io.BytesIO(sample.encode('utf-8'))
        et = etree.parse(fp)
        for lang, html_output in domain.HTMLGenerator(et, valid_only=False):
            role_tags = html_output.xpath('//span[@class="role"]')
            self.assertEqual(1, len(role_tags))
            role_tag = role_tags[0]
            self.assertEqual(role_text, role_tag.text.strip())

    def test_role_tag_inside_element_citation_tag(self):
        """
        verifica que o tag <role> dentro de <element-citation> seja correto no html.
        - - -
        <role> aparece em: <collab>, <contrib>, <contrib-group>, <element-citation>, <person-group>, <product>
        """
        role_text = {
            'pt': 'role em PT',
            'en': 'role em EN',
        }
        sample = u"""<?xml version="1.0" encoding="UTF-8"?>
                    <!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "JATS-journalpublishing1.dtd">
                    <article xml:lang="pt">
                        <back>
                            <ref-list>
                                <ref id="B3">
                                    <element-citation publication-type="journal">
                                        <role>%s</role>
                                    </element-citation>
                                </ref>
                            </ref-list>
                        </back>
                        <sub-article article-type="translation" id="TRen" xml:lang="en">
                            <back>
                                <ref-list>
                                    <ref id="B3">
                                        <element-citation publication-type="journal">
                                            <role>%s</role>
                                        </element-citation>
                                    </ref>
                                </ref-list>
                            </back>
                        </sub-article>
                    </article>
                 """ % (role_text['pt'], role_text['en'])
        fp = io.BytesIO(sample.encode('utf-8'))
        et = etree.parse(fp)
        for lang, html_output in domain.HTMLGenerator(et, valid_only=False):
            role_tags = html_output.xpath('//span[@class="role"]')
            self.assertEqual(1, len(role_tags))
            role_tag = role_tags[0]
            self.assertEqual(role_text[lang], role_tag.text.strip())

    def test_role_tag_inside_person_group_tag(self):
        """
        verifica que o tag <role> dentro de <person-group> seja correto no html.
        - - -
        <role> aparece em: <collab>, <contrib>, <contrib-group>, <element-citation>, <person-group>, <product>
        """
        role_text = {
            'pt': 'role em PT',
            'en': 'role em EN',
        }
        sample = u"""<?xml version="1.0" encoding="UTF-8"?>
                    <!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "JATS-journalpublishing1.dtd">
                    <article xml:lang="pt">
                        <back>
                            <ref-list>
                                <ref id="B3">
                                    <element-citation publication-type="journal">
                                        <person-group person-group-type="author">
                                            <role>%s</role>
                                        </person-group>
                                    </element-citation>
                                </ref>
                            </ref-list>
                        </back>
                        <sub-article article-type="translation" id="TRen" xml:lang="en">
                            <back>
                                <ref-list>
                                    <ref id="B3">
                                        <element-citation publication-type="journal">
                                            <person-group person-group-type="author">
                                                <role>%s</role>
                                            </person-group>
                                        </element-citation>
                                    </ref>
                                </ref-list>
                            </back>
                        </sub-article>
                    </article>
                 """ % (role_text['pt'], role_text['en'])
        fp = io.BytesIO(sample.encode('utf-8'))
        et = etree.parse(fp)
        for lang, html_output in domain.HTMLGenerator(et, valid_only=False):
            role_tags = html_output.xpath('//span[@class="role"]')
            self.assertEqual(1, len(role_tags))
            role_tag = role_tags[0]
            self.assertEqual(role_text[lang], role_tag.text.strip())

    @unittest.skip('tag product não é exibida por enquanto')
    def test_role_tag_inside_product_tag(self):
        """
        verifica que o tag <role> dentro de <product> seja correto no html.
        - - -
        <role> aparece em: <collab>, <contrib>, <contrib-group>, <element-citation>, <person-group>, <product>
        """
        role_text = {
            'pt': 'role em PT',
            'en': 'role em EN',
        }
        sample = u"""<?xml version="1.0" encoding="UTF-8"?>
                    <!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "JATS-journalpublishing1.dtd">
                    <article xml:lang="pt">
                        <front>
                            <article-meta>
                                <product product-type="book">
                                    <role>%s</role>
                                </product>
                            </article-meta>
                        </front>
                        <sub-article article-type="translation" id="TRen" xml:lang="en">
                            <front-stub>
                                <article-meta>
                                    <product product-type="book">
                                        <role>%s</role>
                                    </product>
                                </article-meta>
                            </front-stub>
                        </sub-article>
                    </article>
                 """ % (role_text['pt'], role_text['en'])
        fp = io.BytesIO(sample.encode('utf-8'))
        et = etree.parse(fp)
        for lang, html_output in domain.HTMLGenerator(et, valid_only=False):
            role_tags = html_output.xpath('//span[@class="role"]')
            self.assertEqual(1, len(role_tags))
            role_tag = role_tags[0]
            self.assertEqual(role_text[lang], role_tag.text.strip())

    """ <NAME> <SURNAME> <GIVEN-NAMES> <PREFIX> <SUFFIX> """
    def test_name_tag_inside_contrib_tag(self):
        """
        verifica que o tag <name> dentro de <contrib> seja correto no html.
        - - -
        <name> aparece em: <contrib>, <person-group>
        """
        name_data = {
            'prefix': 'Mr',
            'surname': 'Foo',
            'given_names': 'Bar',
            'suffix': 'Jr',
        }
        sample = u"""<?xml version="1.0" encoding="UTF-8"?>
                    <!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "JATS-journalpublishing1.dtd">
                    <article xml:lang="pt">
                        <front>
                            <article-meta>
                                <contrib-group>
                                    <contrib contrib-type="author">
                                        <name>
                                            <prefix>%s</prefix>
                                            <surname>%s</surname>
                                            <given-names>%s</given-names>
                                            <suffix>%s</suffix>
                                        </name>
                                    </contrib>
                                </contrib-group>
                            </article-meta>
                        </front>
                    </article>
                 """ % (name_data['prefix'], name_data['surname'], name_data['given_names'], name_data['suffix'])
        fp = io.BytesIO(sample.encode('utf-8'))
        et = etree.parse(fp)
        for lang, html_output in domain.HTMLGenerator(et, valid_only=False):
            name_tags = html_output.xpath('//span[@class="name"]')
            self.assertEqual(1, len(name_tags))

            prefix_tag = name_tags[0].find('span[@class="prefix"]')
            surname_tag = name_tags[0].find('span[@class="surname"]')
            given_name_tag = name_tags[0].find('span[@class="given_names"]')
            suffix_tag = name_tags[0].find('span[@class="suffix"]')

            self.assertEqual(name_data['prefix'], prefix_tag.text.strip())
            self.assertEqual(name_data['surname'], surname_tag.text.strip())
            self.assertEqual(name_data['given_names'], given_name_tag.text.strip())
            self.assertEqual(name_data['suffix'], suffix_tag.text.strip())

    def test_name_tag_inside_person_group_tag(self):
        """
        verifica que o tag <name> dentro de <contrib> seja correto no html.
        - - -
        <name> aparece em: <contrib>, <person-group>
        """
        name_data = {
            'prefix': 'Mr',
            'surname': 'Foo',
            'given_names': 'Bar',
            'suffix': 'Jr',
        }
        sample = u"""<?xml version="1.0" encoding="UTF-8"?>
                    <!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "JATS-journalpublishing1.dtd">
                    <article xml:lang="pt">
                        <back>
                            <ref-list>
                                <ref id="B3">
                                    <element-citation publication-type="journal">
                                        <person-group person-group-type="author">
                                            <name>
                                            <prefix>%s</prefix>
                                            <surname>%s</surname>
                                            <given-names>%s</given-names>
                                            <suffix>%s</suffix>
                                        </name>
                                        </person-group>
                                    </element-citation>
                                </ref>
                            </ref-list>
                        </back>
                    </article>
                 """ % (name_data['prefix'], name_data['surname'], name_data['given_names'], name_data['suffix'])
        fp = io.BytesIO(sample.encode('utf-8'))
        et = etree.parse(fp)
        for lang, html_output in domain.HTMLGenerator(et, valid_only=False):
            name_tags = html_output.xpath('//span[@class="name"]')
            self.assertEqual(1, len(name_tags))

            prefix_tag = name_tags[0].find('span[@class="prefix"]')
            surname_tag = name_tags[0].find('span[@class="surname"]')
            given_name_tag = name_tags[0].find('span[@class="given_names"]')
            suffix_tag = name_tags[0].find('span[@class="suffix"]')

            self.assertEqual(name_data['prefix'], prefix_tag.text.strip())
            self.assertEqual(name_data['surname'], surname_tag.text.strip())
            self.assertEqual(name_data['given_names'], given_name_tag.text.strip())
            self.assertEqual(name_data['suffix'], suffix_tag.text.strip())

    """ <AFF>, <INSTITUTION>, <ADDR-LINE>, <COUNTRY> """
    def test_aff_tag(self):
        """
        verifica que o tag <aff> dentro de <article-meta> seja correto no html.
        não são exibidos os tags:
        - orgname
        - orgdiv1
        - orgdiv2
        - city
        - state
        - country
        - - -
        <aff> aparece em <article-meta>
        """
        aff_data = {
            'label': '1',
            'institution_orgname': 'Fundação Oswaldo Cruz',
            'institution_orgdiv1': 'Escola Nacional de Saúde Pública Sérgio Arouca',
            'institution_orgdiv2': 'Centro de Estudos da Saúde do Trabalhador e Ecologia Humana',
            'addr_line_city': 'Manguinhos',
            'addr_line_state': 'RJ',
            'country': 'Brasil',
            'institution_original': 'Prof. da Fundação Oswaldo Cruz; da Escola Nacional de Saúde Pública Sérgio Arouca, do Centro de Estudos da Saúde do Trabalhador e Ecologia Humana. RJ - Manguinhos / Brasil.',
        }
        sample = u"""<?xml version="1.0" encoding="UTF-8"?>
                <!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "JATS-journalpublishing1.dtd">
                <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" dtd-version="1.0" article-type="review-article" xml:lang="pt">
                    <front>
                        <article-meta>
                            <aff id="aff1">
                                <label>{label}</label>
                                <institution content-type="orgname">{institution_orgname}</institution>
                                <institution content-type="orgdiv1">{institution_orgdiv1}</institution>
                                <institution content-type="orgdiv2">{institution_orgdiv2}</institution>
                                <addr-line>
                                    <named-content content-type="city">{addr_line_city}</named-content>
                                    <named-content content-type="state">{addr_line_state}</named-content>
                                </addr-line>
                                <country>{country}</country>
                                <institution content-type="original">{institution_original}</institution>
                            </aff>
                        </article-meta>
                    </front>
                </article>
                """.format(**aff_data)
        fp = io.BytesIO(sample.encode('utf-8'))
        et = etree.parse(fp)
        for lang, html_output in domain.HTMLGenerator(et, valid_only=False):
            found_affs = html_output.xpath('//li[@id="aff1"]/div')
            self.assertEqual(1, len(found_affs))

            label_tag = found_affs[0].find('sup[@class="xref big"]')
            institution_original_tag = found_affs[0].xpath('//span[@class="institution original"]')[0]

            self.assertEqual(aff_data['label'], label_tag.text.strip())
            self.assertEqual(aff_data['institution_original'], institution_original_tag.text.strip())

    """ <AUTHOR-NOTES> <FN> <CORRESP> """
    def test_author_notes_tag_inside_article_meta(self):
        """
        verifica que o tag <author-notes> dentro de <article-meta> seja correto no html.
        - - -
        <author-notes> aparece em <article-meta>
        """
        author_notes_data = {
            'corresp': 'Correspondence: - Cidade Universitária, 79070-192 Campo Grande - MS Brasil,',
            'fn_text': 'Conflict of interest: none',
        }
        sample = u"""<?xml version="1.0" encoding="UTF-8"?>
                <!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "JATS-journalpublishing1.dtd">
                <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" dtd-version="1.0" article-type="review-article" xml:lang="pt">
                    <front>
                        <article-meta>
                            <author-notes>
                                <corresp id="c01">{corresp}</corresp>
                                <fn fn-type="conflict">
                                    <p>{fn_text}</p>
                                </fn>
                            </author-notes>
                        </article-meta>
                    </front>
                    <sub-article xml:lang="en" article-type="translation" id="S01">
                        <front-stub>
                            <author-notes>
                                <corresp id="c01">{corresp}</corresp>
                                <fn fn-type="conflict">
                                    <p>{fn_text}</p>
                                </fn>
                            </author-notes>
                        </front-stub>
                    </sub-article>
                </article>
                """.format(**author_notes_data)

        fp = io.BytesIO(sample.encode('utf-8'))
        et = etree.parse(fp)
        for lang, html_output in domain.HTMLGenerator(et, valid_only=False):
            found_author_notes = html_output.xpath('//div[@class="author-notes"]')
            self.assertEqual(1, len(found_author_notes))

            found_author_note = found_author_notes[0]
            corresp_tag = found_author_note.xpath('//div[@class="corresp"]')
            fn_tag = found_author_note.xpath('//div[@class="author-notes-fn conflict"]/p')

            self.assertEqual(author_notes_data['corresp'], corresp_tag[0].text.strip())
            self.assertEqual(author_notes_data['fn_text'], fn_tag[0].text.strip())

    """ <PUB-DATE>, <DAY>, <MONTH>, <YEAR> """
    def test_pub_date_tag_inside_article_meta(self):
        """
        verifica que o tag <pub-date> dentro de <article-meta> seja correto no html.
        - - -
        <pub-date> aparece em <article-meta>
        """
        pub_date_data = {
            'day': '17',
            'month': '3',
            'year': '2015',
        }
        sample = u"""<?xml version="1.0" encoding="UTF-8"?>
                <!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "JATS-journalpublishing1.dtd">
                <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" dtd-version="1.0" article-type="review-article" xml:lang="pt">
                    <front>
                        <article-meta>
                            <pub-date pub-type="epub-ppub">
                                <day>{day}</day>
                                <month>{month}</month>
                                <year>{year}</year>
                            </pub-date>
                        </article-meta>
                    </front>
                    <sub-article xml:lang="en" article-type="translation" id="S01">
                        <front-stub>
                            <pub-date pub-type="epub-ppub">
                                <day>{day}</day>
                                <month>{month}</month>
                                <year>{year}</year>
                            </pub-date>
                        </front-stub>
                    </sub-article>
                </article>
                """.format(**pub_date_data)

        fp = io.BytesIO(sample.encode('utf-8'))
        et = etree.parse(fp)
        for lang, html_output in domain.HTMLGenerator(et, valid_only=False):
            found_pub_dates = html_output.xpath('//span[@class="pub_date"]')
            self.assertEqual(1, len(found_pub_dates))

            found_pub_date = found_pub_dates[0]
            pub_type = found_pub_date.xpath('//span[@class="pub_date_type"]')
            day_tag = found_pub_date.xpath('//span[@class="day"]')
            month_tag = found_pub_date.xpath('//span[@class="month"]')
            year_tag = found_pub_date.xpath('//span[@class="year"]')

            self.assertEqual(pub_date_data['day'] + "/", day_tag[0].text.strip())
            self.assertEqual(pub_date_data['month'] + "/", month_tag[0].text.strip())
            self.assertEqual(pub_date_data['year'], year_tag[0].text.strip())

    """ <SEASON> """
    def test_season_tag_inside_pub_date(self):
        """
        verifica que o tag <season> dentro de <pub-date> seja correto no html.
        - - -
        <season> aparece em <pub-date>, <product>, <element-citation>
        """
        season_text = 'Nov-Dec'
        sample = u"""<?xml version="1.0" encoding="UTF-8"?>
                <!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "JATS-journalpublishing1.dtd">
                <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" dtd-version="1.0" article-type="review-article" xml:lang="pt">
                    <front>
                        <article-meta>
                            <pub-date pub-type="epub-ppub">
                                <season>{season}</season>
                            </pub-date>
                        </article-meta>
                    </front>
                    <sub-article xml:lang="en" article-type="translation" id="S01">
                        <front-stub>
                            <pub-date pub-type="epub-ppub">
                                <season>{season}</season>
                            </pub-date>
                        </front-stub>
                    </sub-article>
                </article>
                """.format(season=season_text)

        fp = io.BytesIO(sample.encode('utf-8'))
        et = etree.parse(fp)
        for lang, html_output in domain.HTMLGenerator(et, valid_only=False):
            found_pub_dates = html_output.xpath('//span[@class="pub_date"]')
            self.assertEqual(1, len(found_pub_dates))

            found_pub_date = found_pub_dates[0]
            season_tag = found_pub_date.xpath('//span[@class="season"]')

            self.assertEqual(season_text, season_tag[0].text.strip())

    @unittest.skip('tag product não é exibida por enquanto')
    def test_season_tag_inside_product(self):
        """
        verifica que o tag <season> dentro de <product> seja correto no html.
        - - -
        <season> aparece em <pub-date>, <product>, <element-citation>
        """
        season_text = 'Nov-Dec'
        sample = u"""<?xml version="1.0" encoding="UTF-8"?>
                <!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "JATS-journalpublishing1.dtd">
                <article xml:lang="pt">
                    <front>
                        <article-meta>
                            <product product-type="book">
                                <season>{season}</season>
                            </product>
                        </article-meta>
                    </front>
                    <sub-article article-type="translation" id="TRen" xml:lang="en">
                        <front-stub>
                            <article-meta>
                                <product product-type="book">
                                    <season>{season}</season>
                                </product>
                            </article-meta>
                        </front-stub>
                    </sub-article>
                </article>
                """.format(season=season_text)

        fp = io.BytesIO(sample.encode('utf-8'))
        et = etree.parse(fp)
        for lang, html_output in domain.HTMLGenerator(et, valid_only=False):
            found_products = html_output.xpath('//div[@class="product book"]')
            self.assertEqual(1, len(found_products))

            found_product = found_products[0]
            season_tag = found_product.xpath('//div[@class="season"]')

            self.assertEqual(season_text, season_tag[0].text.strip())

    def test_season_tag_inside_element_citation_tag(self):
        """
        verifica que o tag <season> dentro de <element-citation> seja correto no html.
        - - -
        <season> aparece em <pub-date>, <product>, <element-citation>
        """
        season_text = 'Nov-Dec'
        sample = u"""<?xml version="1.0" encoding="UTF-8"?>
                <!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "JATS-journalpublishing1.dtd">
                <article xml:lang="pt">
                    <back>
                        <ref-list>
                            <ref id="B3">
                                <element-citation publication-type="journal">
                                    <season>{season}</season>
                                </element-citation>
                            </ref>
                        </ref-list>
                    </back>
                    <sub-article article-type="translation" id="TRen" xml:lang="en">
                        <back>
                            <ref-list>
                                <ref id="B3">
                                    <element-citation publication-type="journal">
                                        <season>{season}</season>
                                    </element-citation>
                                </ref>
                            </ref-list>
                        </back>
                    </sub-article>
                </article>
                """.format(season=season_text)

        fp = io.BytesIO(sample.encode('utf-8'))
        et = etree.parse(fp)
        for lang, html_output in domain.HTMLGenerator(et, valid_only=False):
            found_elements = html_output.xpath('//span[@class="element-citation journal"]')
            self.assertEqual(1, len(found_elements))
            found_element = found_elements[0]
            season_tag = found_element.xpath('//span[@class="season"]')
            self.assertEqual(season_text, season_tag[0].text.strip())

    """ <ISSUE> <VOLUME> """
    @unittest.skip('tags volume/number não são exibidas isoladamente por enquanto')
    def test_issue_and_volume_tag_inside_article_meta_tag(self):
        """
        verifica que o tag <issue> e <volume> dentro de <article-meta> seja correto no html.
        - - -
        <issue> aparece em <article-meta>, <element-citation>
        """
        issue_text = "5 suppl 1"
        volume_text = "99"
        sample = u"""<?xml version="1.0" encoding="UTF-8"?>
                <!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "JATS-journalpublishing1.dtd">
                <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" dtd-version="1.0" article-type="review-article" xml:lang="pt">
                    <front>
                        <article-meta>
                            <issue>{issue}</issue>
                            <volume>{volume}</volume>
                        </article-meta>
                    </front>
                    <sub-article xml:lang="en" article-type="translation" id="S01">
                    </sub-article>
                </article>
                """.format(issue=issue_text, volume=volume_text)

        fp = io.BytesIO(sample.encode('utf-8'))
        et = etree.parse(fp)
        for lang, html_output in domain.HTMLGenerator(et, valid_only=False):
            found_issue_labels = html_output.xpath('//span[@class="issue_label"]')
            self.assertEqual(1, len(found_issue_labels))
            expected_label = 'vol.%s n.%s' % (volume_text, issue_text)
            self.assertEqual(expected_label, found_issue_labels[0].text.strip())

    @unittest.skip('tags volume/number não é exibidas isoladamente por enquanto')
    def test_issue_and_volume_tag_as_ahead_of_print_inside_article_meta_tag(self):
        """
        verifica que o tag <issue> e <volume> (ahead of print) dentro de <article-meta> seja correto no html.
        - - -
        <issue>, e <volume> aparece em <article-meta>, <element-citation>
        """
        issue_text = "00"
        volume_text = "00"
        sample = u"""<?xml version="1.0" encoding="UTF-8"?>
                <!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "JATS-journalpublishing1.dtd">
                <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" dtd-version="1.0" article-type="review-article" xml:lang="pt">
                    <front>
                        <article-meta>
                            <issue>{issue}</issue>
                            <volume>{volume}</volume>
                        </article-meta>
                    </front>
                    <sub-article xml:lang="en" article-type="translation" id="S01">
                    </sub-article>
                </article>
                """.format(issue=issue_text, volume=volume_text)

        fp = io.BytesIO(sample.encode('utf-8'))
        et = etree.parse(fp)
        for lang, html_output in domain.HTMLGenerator(et, valid_only=False):
            found_issue_labels = html_output.xpath('//span[@class="issue_label"]')
            self.assertEqual(1, len(found_issue_labels))
            expected_label = 'ahead of print'
            self.assertEqual(expected_label, found_issue_labels[0].text.strip())

    def test_issue_and_volume_tag_inside_element_citation_tag(self):
        """
        verifica que o tag <issue> e <volume> dentro de  <element-citation> seja correto no html.
        - - -
        <issue>, e <volume> aparece em <article-meta>, <element-citation>
        """
        issue_text = "5 suppl 1"
        volume_text = "99"
        sample = u"""<?xml version="1.0" encoding="UTF-8"?>
                <!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "JATS-journalpublishing1.dtd">
                <article xml:lang="pt">
                    <back>
                        <ref-list>
                            <ref id="B3">
                                <element-citation publication-type="journal">
                                    <issue>{issue}</issue>
                                    <volume>{volume}</volume>
                                </element-citation>
                            </ref>
                        </ref-list>
                    </back>
                    <sub-article article-type="translation" id="TRen" xml:lang="en">
                        <back>
                            <ref-list>
                                <ref id="B3">
                                    <element-citation publication-type="journal">
                                        <issue>{issue}</issue>
                                        <volume>{volume}</volume>
                                    </element-citation>
                                </ref>
                            </ref-list>
                        </back>
                    </sub-article>
                </article>
                """.format(issue=issue_text, volume=volume_text)

        fp = io.BytesIO(sample.encode('utf-8'))
        et = etree.parse(fp)
        for lang, html_output in domain.HTMLGenerator(et, valid_only=False):
            found_elements = html_output.xpath('//span[@class="element-citation journal"]')
            self.assertEqual(1, len(found_elements))
            element_issue_volume = found_elements[0].xpath('//span[@class="element_issue_volume"]')[0].text.strip()
            expected_label = u'vol.%s n.%s' % (volume_text, issue_text)
            self.assertEqual(expected_label, element_issue_volume)

    def test_issue_and_volume_tag_as_ahead_of_print_inside_element_citation_tag(self):
        """
        verifica que o tag <issue> e <volume> (ahead of print) dentro de <element-citation> seja correto no html.
        - - -
        <issue>, e <volume> aparece em <article-meta>, <element-citation>
        """
        issue_text = "00"
        volume_text = "00"
        sample = u"""<?xml version="1.0" encoding="UTF-8"?>
                <!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "JATS-journalpublishing1.dtd">
                <article xml:lang="pt">
                    <back>
                        <ref-list>
                            <ref id="B3">
                                <element-citation publication-type="journal">
                                    <issue>{issue}</issue>
                                    <volume>{volume}</volume>
                                </element-citation>
                            </ref>
                        </ref-list>
                    </back>
                    <sub-article article-type="translation" id="TRen" xml:lang="en">
                        <back>
                            <ref-list>
                                <ref id="B3">
                                    <element-citation publication-type="journal">
                                        <issue>{issue}</issue>
                                        <volume>{volume}</volume>
                                    </element-citation>
                                </ref>
                            </ref-list>
                        </back>
                    </sub-article>
                </article>
                """.format(issue=issue_text, volume=volume_text)

        fp = io.BytesIO(sample.encode('utf-8'))
        et = etree.parse(fp)
        for lang, html_output in domain.HTMLGenerator(et, valid_only=False):
            found_elements = html_output.xpath('//span[@class="element-citation journal"]')
            self.assertEqual(1, len(found_elements))
            element_issue_volume = found_elements[0].xpath('//span[@class="element_issue_volume"]')[0].text.strip()
            expected_label = 'ahead of print'
            self.assertEqual(expected_label, element_issue_volume)

    """ <FPAGE> <LPAGE> """
    @unittest.skip('tags fpage/lpage não são exibidas isoladamente por enquanto')
    def test_fpage_and_lpage_tag_inside_article_meta_tag(self):
        """
        verifica que o tag <fpage> e <lpage> dentro de <article-meta> seja correto no html.
        - - -
        <fpage> e <lpage> aparece em <article-meta>, <element-citation>
        """
        fpage_text = "17"
        lpage_text = "21"
        sample = u"""<?xml version="1.0" encoding="UTF-8"?>
                <!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "JATS-journalpublishing1.dtd">
                <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" dtd-version="1.0" article-type="review-article" xml:lang="pt">
                    <front>
                        <article-meta>
                            <fpage>{fpage}</fpage>
                            <lpage>{lpage}</lpage>
                        </article-meta>
                    </front>
                    <sub-article xml:lang="en" article-type="translation" id="S01">
                    </sub-article>
                </article>
                """.format(fpage=fpage_text, lpage=lpage_text)

        fp = io.BytesIO(sample.encode('utf-8'))
        et = etree.parse(fp)
        for lang, html_output in domain.HTMLGenerator(et, valid_only=False):
            found_pages = html_output.xpath('//span[@class="pages"]')
            self.assertEqual(1, len(found_pages))
            found_fpage = found_pages[0].xpath('//span[@class="fpage"]')[0].text.strip()
            found_lpage = found_pages[0].xpath('//span[@class="lpage"]')[0].text.strip()
            self.assertEqual(fpage_text, found_fpage)
            self.assertEqual(lpage_text, found_lpage)

    @unittest.skip('tags fpage/lpage não são exibidas isoladamente por enquanto')
    def test_fpage_and_lpage_tag_as_ahead_of_print_inside_article_meta_tag(self):
        """
        verifica que o tag <fpage> e <lpage> dentro de <article-meta> seja correto no html.
        - - -
        <fpage> e <lpage> aparece em <article-meta>, <element-citation>
        """
        fpage_text = "00"
        lpage_text = "00"
        sample = u"""<?xml version="1.0" encoding="UTF-8"?>
                <!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "JATS-journalpublishing1.dtd">
                <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" dtd-version="1.0" article-type="review-article" xml:lang="pt">
                    <front>
                        <article-meta>
                            <fpage>{fpage}</fpage>
                            <lpage>{lpage}</lpage>
                        </article-meta>
                    </front>
                    <sub-article xml:lang="en" article-type="translation" id="S01">
                    </sub-article>
                </article>
                """.format(fpage=fpage_text, lpage=lpage_text)

        fp = io.BytesIO(sample.encode('utf-8'))
        et = etree.parse(fp)
        for lang, html_output in domain.HTMLGenerator(et, valid_only=False):
            found_pages = html_output.xpath('//span[@class="pages"]')
            found_fpages = html_output.xpath('//span[@class="fpage"]')
            found_lpages = html_output.xpath('//span[@class="lpage"]')
            self.assertEqual(0, len(found_pages))
            self.assertEqual(0, len(found_fpages))
            self.assertEqual(0, len(found_lpages))

    def test_fpage_and_lpage_tag_inside_element_citation_tag(self):
        """
        verifica que o tag <fpage> e <lpage> dentro de <element-citation> seja correto no html.
        - - -
        <fpage> e <lpage> aparece em <article-meta>, <element-citation>
        """
        fpage_text = "17"
        lpage_text = "21"
        sample = u"""<?xml version="1.0" encoding="UTF-8"?>
                <!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "JATS-journalpublishing1.dtd">
                <article xml:lang="pt">
                    <back>
                        <ref-list>
                            <ref id="B3">
                                <element-citation publication-type="journal">
                                    <fpage>{fpage}</fpage>
                                    <lpage>{lpage}</lpage>
                                </element-citation>
                            </ref>
                        </ref-list>
                    </back>
                    <sub-article article-type="translation" id="TRen" xml:lang="en">
                        <back>
                            <ref-list>
                                <ref id="B3">
                                    <element-citation publication-type="journal">
                                        <fpage>{fpage}</fpage>
                                        <lpage>{lpage}</lpage>
                                    </element-citation>
                                </ref>
                            </ref-list>
                        </back>
                    </sub-article>
                </article>
                """.format(fpage=fpage_text, lpage=lpage_text)

        fp = io.BytesIO(sample.encode('utf-8'))
        et = etree.parse(fp)
        for lang, html_output in domain.HTMLGenerator(et, valid_only=False):
            found_elements = html_output.xpath('//span[@class="element-citation journal"]')
            self.assertEqual(1, len(found_elements))
            element_pages = found_elements[0].xpath('//span[@class="element_pages"]')
            self.assertEqual(1, len(element_pages))
            element_fpage = element_pages[0].xpath('//span[@class="element_fpage"]')[0].text.strip()
            element_lpage = element_pages[0].xpath('//span[@class="element_lpage"]')[0].text.strip()
            self.assertEqual(fpage_text, element_fpage)
            self.assertEqual(lpage_text, element_lpage)

    def test_fpage_and_lpage_tag_as_ahead_of_print_inside_element_citation_tag(self):
        """
        verifica que o tag <fpage> e <lpage> dentro de <element-citation> seja correto no html.
        - - -
        <fpage> e <lpage> aparece em <article-meta>, <element-citation>
        """
        fpage_text = "00"
        lpage_text = "00"
        sample = u"""<?xml version="1.0" encoding="UTF-8"?>
                <!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "JATS-journalpublishing1.dtd">
                <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" dtd-version="1.0" article-type="review-article" xml:lang="pt">
                    <back>
                        <ref-list>
                            <ref id="B3">
                                <element-citation publication-type="journal">
                                    <fpage>{fpage}</fpage>
                                    <lpage>{lpage}</lpage>
                                </element-citation>
                            </ref>
                        </ref-list>
                    </back>
                    <sub-article article-type="translation" id="TRen" xml:lang="en">
                        <back>
                            <ref-list>
                                <ref id="B3">
                                    <element-citation publication-type="journal">
                                        <fpage>{fpage}</fpage>
                                        <lpage>{lpage}</lpage>
                                    </element-citation>
                                </ref>
                            </ref-list>
                        </back>
                    </sub-article>
                </article>
                """.format(fpage=fpage_text, lpage=lpage_text)

        fp = io.BytesIO(sample.encode('utf-8'))
        et = etree.parse(fp)
        for lang, html_output in domain.HTMLGenerator(et, valid_only=False):
            found_elements = html_output.xpath('//span[@class="element-citation journal"]')
            self.assertEqual(1, len(found_elements))
            element_pages = found_elements[0].xpath('//span[@class="element_pages"]')
            element_fpage = html_output.xpath('//span[@class="element_fpage"]')
            element_lpage = html_output.xpath('//span[@class="element_lpage"]')
            self.assertEqual(0, len(element_pages))
            self.assertEqual(0, len(element_fpage))
            self.assertEqual(0, len(element_lpage))

    """ <ELOCATION-ID> """
    @unittest.skip('tag elocation-id não é exibida por enquanto')
    def test_elocation_id_tag_inside_article_meta_tag(self):
        """
        verifica que o tag <elocation-id> dentro de <article-meta> seja correto no html.
        - - -
        <elocation-id> aparece em <article-meta>
        """
        elocation_id_text = "0102961"
        sample = u"""<?xml version="1.0" encoding="UTF-8"?>
                <!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "JATS-journalpublishing1.dtd">
                <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" dtd-version="1.0" article-type="review-article" xml:lang="pt">
                    <front>
                        <article-meta>
                            <elocation-id>{elocation_id}</elocation-id>
                        </article-meta>
                    </front>
                    <sub-article xml:lang="en" article-type="translation" id="S01">
                    </sub-article>
                </article>
                """.format(elocation_id=elocation_id_text)

        fp = io.BytesIO(sample.encode('utf-8'))
        et = etree.parse(fp)
        for lang, html_output in domain.HTMLGenerator(et, valid_only=False):
            elocation_ids = html_output.xpath('//span[@class="elocation_id"]')
            self.assertEqual(1, len(elocation_ids))
            elocation_id = elocation_ids[0].text.strip()
            self.assertEqual(elocation_id_text, elocation_id)

    """ <PRODUCT> """
    @unittest.skip('tag product não é exibida por enquanto')
    def test_product_tag_inside_article_meta_tag(self):
        """
        verifica que o tag <product> dentro de <article-meta> seja correto no html.
        - - -
        <product> aparece em <article-meta>
        """
        product_data = {
            # lang: pt
            'pt_product_surname': 'PT product surname',
            'pt_product_given_names': 'PT product given_names',
            'pt_product_source': 'PT product source',
            'pt_product_year': 'PT product year',
            'pt_product_publisher_name': 'PT product publisher_name',
            'pt_product_publisher_loc': 'PT product publisher_loc',
            'pt_product_size': 'PT product size',
            'pt_product_isbn': 'PT product isbn',
            'pt_product_inline_graphic': 'PT product inline_graphic',
            # lang: en
            'en_product_surname': 'EN product surname',
            'en_product_given_names': 'EN product given_names',
            'en_product_source': 'EN product source',
            'en_product_year': 'EN product year',
            'en_product_publisher_name': 'EN product publisher_name',
            'en_product_publisher_loc': 'EN product publisher_loc',
            'en_product_size': 'EN product size',
            'en_product_isbn': 'EN product isbn',
            'en_product_inline_graphic': 'EN product inline_graphic',
        }
        sample = u"""<?xml version="1.0" encoding="UTF-8"?>
                <!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "JATS-journalpublishing1.dtd">
                <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" dtd-version="1.0" article-type="review-article" xml:lang="pt">
                    <front>
                        <article-meta>
                            <product product-type="book">
                                <person-group person-group-type="author">
                                    <name>
                                        <surname>{pt_product_surname}</surname>
                                        <given-names>{pt_product_given_names}</given-names>
                                    </name>
                                </person-group>
                                <source>{pt_product_source}</source>
                                <year>{pt_product_year}</year>
                                <publisher-name>{pt_product_publisher_name}</publisher-name>
                                <publisher-loc>{pt_product_publisher_loc}</publisher-loc>
                                <size units="pages">{pt_product_size}</size>
                                <isbn>{pt_product_isbn}</isbn>
                                <inline-graphic>{pt_product_inline_graphic}</inline-graphic>
                            </product>
                        </article-meta>
                    </front>
                    <sub-article xml:lang="en" article-type="translation" id="S01">
                        <front-stub>
                            <article-meta>
                                <product product-type="book">
                                    <person-group person-group-type="author">
                                        <name>
                                            <surname>{en_product_surname}</surname>
                                            <given-names>{en_product_given_names}</given-names>
                                        </name>
                                    </person-group>
                                    <source>{en_product_source}</source>
                                    <year>{en_product_year}</year>
                                    <publisher-name>{en_product_publisher_name}</publisher-name>
                                    <publisher-loc>{en_product_publisher_loc}</publisher-loc>
                                    <size units="pages">{en_product_size}</size>
                                    <isbn>{en_product_isbn}</isbn>
                                    <inline-graphic>{en_product_inline_graphic}</inline-graphic>
                                </product>
                            </article-meta>
                        </front-stub>
                    </sub-article>
                </article>
                """.format(**product_data)

        fp = io.BytesIO(sample.encode('utf-8'))
        et = etree.parse(fp)
        for lang, html_output in domain.HTMLGenerator(et, valid_only=False):
            products = html_output.xpath('//div[@class="product book"]')
            self.assertEqual(1, len(products))
            product_surname = products[0].xpath('//span[@class="surname"]')[0].text.strip()
            self.assertEqual(product_data['%s_product_surname' % lang], product_surname)
            product_given_names = products[0].xpath('//span[@class="given_names"]')[0].text.strip()
            self.assertEqual(product_data['%s_product_given_names' % lang], product_given_names)
            product_source = products[0].xpath('//div[@class="source"]')[0].text.strip()
            self.assertEqual(product_data['%s_product_source' % lang], product_source)
            product_year = products[0].xpath('//div[@class="year"]')[0].text.strip()
            self.assertEqual(product_data['%s_product_year' % lang], product_year)
            product_publisher_name = products[0].xpath('//div[@class="publisher-name"]')[0].text.strip()
            self.assertEqual(product_data['%s_product_publisher_name' % lang], product_publisher_name)
            product_publisher_loc = products[0].xpath('//div[@class="publisher-loc"]')[0].text.strip()
            self.assertEqual(product_data['%s_product_publisher_loc' % lang], product_publisher_loc)
            product_size = products[0].xpath('//div[@class="size"]')[0].text.strip()
            self.assertEqual(product_data['%s_product_size' % lang], product_size)
            product_isbn = products[0].xpath('//div[@class="isbn"]')[0].text.strip()
            self.assertEqual(product_data['%s_product_isbn' % lang], product_isbn)

    """ <PERSON-GROUP> """
    @unittest.skip('tag product não é exibida por enquanto')
    def test_person_group_tag_inside_product_tag(self):
        """
        verifica que o tag <person-group> dentro de <product> seja correto no html.
        - - -
        <person-group> aparece em <product>, <element-citation>
        """
        person_data = {
            # lang: pt
            'pt_product_surname': 'PT product surname',
            'pt_product_given_names': 'PT product given_names',
            # lang: en
            'en_product_surname': 'EN product surname',
            'en_product_given_names': 'EN product given_names',
        }
        sample = u"""<?xml version="1.0" encoding="UTF-8"?>
                <!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "JATS-journalpublishing1.dtd">
                <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" dtd-version="1.0" article-type="review-article" xml:lang="pt">
                    <front>
                        <article-meta>
                            <product product-type="book">
                                <person-group person-group-type="author">
                                    <name>
                                        <surname>{pt_product_surname}</surname>
                                        <given-names>{pt_product_given_names}</given-names>
                                    </name>
                                </person-group>
                            </product>
                        </article-meta>
                    </front>
                    <sub-article xml:lang="en" article-type="translation" id="S01">
                        <front-stub>
                            <article-meta>
                                <product product-type="book">
                                    <person-group person-group-type="author">
                                        <name>
                                            <surname>{en_product_surname}</surname>
                                            <given-names>{en_product_given_names}</given-names>
                                        </name>
                                    </person-group>
                                </product>
                            </article-meta>
                        </front-stub>
                    </sub-article>
                </article>
                """.format(**person_data)

        fp = io.BytesIO(sample.encode('utf-8'))
        et = etree.parse(fp)
        for lang, html_output in domain.HTMLGenerator(et, valid_only=False):
            products = html_output.xpath('//div[@class="product book"]')
            self.assertEqual(1, len(products))
            product_surname = products[0].xpath('//span[@class="surname"]')[0].text.strip()
            self.assertEqual(person_data['%s_product_surname' % lang], product_surname)
            product_given_names = products[0].xpath('//span[@class="given_names"]')[0].text.strip()
            self.assertEqual(person_data['%s_product_given_names' % lang], product_given_names)

    def test_person_group_tag_inside_element_citation_tag(self):
        """
        verifica que o tag <person-group> dentro de <element-citation> seja correto no html.
        - - -
        <person-group> aparece em <product>, <element-citation>
        """
        person_data = {
            # lang: pt
            'pt_product_surname': 'PT product surname',
            'pt_product_given_names': 'PT product given_names',
            # lang: en
            'en_product_surname': 'EN product surname',
            'en_product_given_names': 'EN product given_names',
        }
        sample = u"""<?xml version="1.0" encoding="UTF-8"?>
                <!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "JATS-journalpublishing1.dtd">
                <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" dtd-version="1.0" article-type="review-article" xml:lang="pt">
                    <back>
                        <ref-list>
                            <ref id="B3">
                                <element-citation publication-type="journal">
                                    <person-group person-group-type="author">
                                        <name>
                                            <surname>{pt_product_surname}</surname>
                                            <given-names>{pt_product_given_names}</given-names>
                                        </name>
                                    </person-group>
                                </element-citation>
                            </ref>
                        </ref-list>
                    </back>
                    <sub-article xml:lang="en" article-type="translation" id="S01">
                        <back>
                            <ref-list>
                                <ref id="B3">
                                    <element-citation publication-type="journal">
                                        <person-group person-group-type="author">
                                            <name>
                                                <surname>{en_product_surname}</surname>
                                                <given-names>{en_product_given_names}</given-names>
                                            </name>
                                        </person-group>
                                    </element-citation>
                                </ref>
                            </ref-list>
                        </back>
                    </sub-article>
                </article>
                """.format(**person_data)

        fp = io.BytesIO(sample.encode('utf-8'))
        et = etree.parse(fp)
        for lang, html_output in domain.HTMLGenerator(et, valid_only=False):
            elements = html_output.xpath('//span[@class="element-citation journal"]')
            self.assertEqual(1, len(elements))
            product_surname = elements[0].xpath('//span[@class="surname"]')[0].text.strip()
            self.assertEqual(person_data['%s_product_surname' % lang], product_surname)
            product_given_names = elements[0].xpath('//span[@class="given_names"]')[0].text.strip()
            self.assertEqual(person_data['%s_product_given_names' % lang], product_given_names)

    """ <ETAL> """
    def test_etal_tag_inside_person_group_tag(self):
        """
        verifica que o tag <etal> dentro de <person-group> seja correto no html.
        - - -
        <etal> aparece em <person-group> <product>
        """
        person_data = {
            # lang: pt
            'pt_product_surname': 'PT product surname',
            'pt_product_given_names': 'PT product given_names',
            # lang: en
            'en_product_surname': 'EN product surname',
            'en_product_given_names': 'EN product given_names',
        }
        sample = u"""<?xml version="1.0" encoding="UTF-8"?>
                <!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "JATS-journalpublishing1.dtd">
                <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" dtd-version="1.0" article-type="review-article" xml:lang="pt">
                    <back>
                        <ref-list>
                            <ref id="B3">
                                <element-citation publication-type="journal">
                                    <person-group person-group-type="author">
                                        <name>
                                            <surname>{pt_product_surname}</surname>
                                            <given-names>{pt_product_given_names}</given-names>
                                        </name>
                                        <etal/>
                                    </person-group>
                                </element-citation>
                            </ref>
                        </ref-list>
                    </back>
                    <sub-article xml:lang="en" article-type="translation" id="S01">
                        <back>
                            <ref-list>
                                <ref id="B3">
                                    <element-citation publication-type="journal">
                                        <person-group person-group-type="author">
                                            <name>
                                                <surname>{en_product_surname}</surname>
                                                <given-names>{en_product_given_names}</given-names>
                                            </name>
                                            <etal/>
                                        </person-group>
                                    </element-citation>
                                </ref>
                            </ref-list>
                        </back>
                    </sub-article>
                </article>
                """.format(**person_data)

        fp = io.BytesIO(sample.encode('utf-8'))
        et = etree.parse(fp)
        for lang, html_output in domain.HTMLGenerator(et, valid_only=False):
            elements = html_output.xpath('//span[@class="element-citation journal"]')
            self.assertEqual(1, len(elements))
            product_surname = elements[0].xpath('//span[@class="surname"]')[0].text.strip()
            self.assertEqual(person_data['%s_product_surname' % lang], product_surname)
            product_given_names = elements[0].xpath('//span[@class="given_names"]')[0].text.strip()
            self.assertEqual(person_data['%s_product_given_names' % lang], product_given_names)
            etal = elements[0].xpath('//span[@class="et-al"]')[0].text.strip()
            self.assertEqual('et al.', etal)

    @unittest.skip('tag product não é exibida por enquanto')
    def test_etal_tag_inside_product_tag(self):
        """
        verifica que o tag <etal> dentro de <person-group> seja correto no html.
        - - -
        <etal> aparece em <person-group> <product>
        """

        sample = u"""<?xml version="1.0" encoding="UTF-8"?>
                <!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "JATS-journalpublishing1.dtd">
                <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" dtd-version="1.0" article-type="review-article" xml:lang="pt">
                    <front>
                        <article-meta>
                            <product product-type="book">
                                <etal/>
                            </product>
                        </article-meta>
                    </front>
                    <sub-article xml:lang="en" article-type="translation" id="S01">
                        <front-stub>
                            <article-meta>
                                <product product-type="book">
                                    <etal/>
                                </product>
                            </article-meta>
                        </front-stub>
                    </sub-article>
                </article>
                """

        fp = io.BytesIO(sample.encode('utf-8'))
        et = etree.parse(fp)
        for lang, html_output in domain.HTMLGenerator(et, valid_only=False):
            products = html_output.xpath('//div[@class="product book"]')
            self.assertEqual(1, len(products))
            etal = products[0].xpath('//span[@class="et-al"]')[0].text.strip()
            self.assertEqual('et al.', etal)

    """ <SIZE> """
    def test_size_tag_inside_element_citation_tag(self):
        """
        verifica que o tag <size> dentro de <element-citation> seja correto no html.
        - - -
        <size> aparece em <product>, <element-citation>
        """
        person_data = {
            # lang: pt
            'pt_product_surname': 'PT product surname',
            'pt_product_given_names': 'PT product given_names',
            'pt_size': 'PT product size',
            # lang: en
            'en_product_surname': 'EN product surname',
            'en_product_given_names': 'EN product given_names',
            'en_size': 'EN product size',
        }
        sample = u"""<?xml version="1.0" encoding="UTF-8"?>
                <!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "JATS-journalpublishing1.dtd">
                <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" dtd-version="1.0" article-type="review-article" xml:lang="pt">
                    <back>
                        <ref-list>
                            <ref id="B3">
                                <element-citation publication-type="journal">
                                    <person-group person-group-type="author">
                                        <name>
                                            <surname>{pt_product_surname}</surname>
                                            <given-names>{pt_product_given_names}</given-names>
                                        </name>
                                    </person-group>
                                    <size units="pages">{pt_size}</size>
                                </element-citation>
                            </ref>
                        </ref-list>
                    </back>
                    <sub-article xml:lang="en" article-type="translation" id="S01">
                        <back>
                            <ref-list>
                                <ref id="B3">
                                    <element-citation publication-type="journal">
                                        <person-group person-group-type="author">
                                            <name>
                                                <surname>{en_product_surname}</surname>
                                                <given-names>{en_product_given_names}</given-names>
                                            </name>
                                        </person-group>
                                        <size units="pages">{en_size}</size>
                                    </element-citation>
                                </ref>
                            </ref-list>
                        </back>
                    </sub-article>
                </article>
                """.format(**person_data)

        fp = io.BytesIO(sample.encode('utf-8'))
        et = etree.parse(fp)
        for lang, html_output in domain.HTMLGenerator(et, valid_only=False):
            elements = html_output.xpath('//span[@class="element-citation journal"]')
            self.assertEqual(1, len(elements))
            product_surname = elements[0].xpath('//span[@class="surname"]')[0].text.strip()
            self.assertEqual(person_data['%s_product_surname' % lang], product_surname)
            product_given_names = elements[0].xpath('//span[@class="given_names"]')[0].text.strip()
            self.assertEqual(person_data['%s_product_given_names' % lang], product_given_names)
            size = elements[0].xpath('//span[@class="size"]')[0].text.strip()
            self.assertEqual(person_data['%s_size' % lang], size)

    @unittest.skip('tag product não é exibida por enquanto')
    def test_size_tag_inside_product_tag(self):
        """
        verifica que o tag <size> dentro de <product> seja correto no html.
        - - -
        <size> aparece em <product>, <element-citation>
        """
        size_data = {
            # lang: pt
            'pt_size': 'PT product size',
            # lang: en
            'en_size': 'EN product size',
        }
        sample = u"""<?xml version="1.0" encoding="UTF-8"?>
                <!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "JATS-journalpublishing1.dtd">
                <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" dtd-version="1.0" article-type="review-article" xml:lang="pt">
                    <front>
                        <article-meta>
                            <product product-type="book">
                                <size units="pages">{pt_size}</size>
                            </product>
                        </article-meta>
                    </front>
                    <sub-article xml:lang="en" article-type="translation" id="S01">
                        <front-stub>
                            <article-meta>
                                <product product-type="book">
                                    <size units="pages">{en_size}</size>
                                </product>
                            </article-meta>
                        </front-stub>
                    </sub-article>
                </article>
                """.format(**size_data)

        fp = io.BytesIO(sample.encode('utf-8'))
        et = etree.parse(fp)
        for lang, html_output in domain.HTMLGenerator(et, valid_only=False):
            products = html_output.xpath('//div[@class="product book"]')
            self.assertEqual(1, len(products))
            size = products[0].xpath('//div[@class="size"]')[0].text.strip()
            self.assertEqual(size_data['%s_size' % lang], size)

    """ <PAGE-RANGE> """
    def test_page_range_tag_inside_element_citation_tag(self):
        """
        verifica que o tag <page-range> dentro de <element-citation> seja correto no html.
        - - -
        <page-range> aparece em <product>, <element-citation>
        """
        data = {
            # lang: pt
            'pt_page_range': '300-301, 305, 407-420',
            # lang: en
            'en_page_range': '300-301, 305, 407-420',
        }
        sample = u"""<?xml version="1.0" encoding="UTF-8"?>
                <!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "JATS-journalpublishing1.dtd">
                <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" dtd-version="1.0" article-type="review-article" xml:lang="pt">
                    <back>
                        <ref-list>
                            <ref id="B3">
                                <element-citation publication-type="journal">
                                    <page-range>{pt_page_range}</page-range>
                                </element-citation>
                            </ref>
                        </ref-list>
                    </back>
                    <sub-article xml:lang="en" article-type="translation" id="S01">
                        <back>
                            <ref-list>
                                <ref id="B3">
                                    <element-citation publication-type="journal">
                                        <page-range>{en_page_range}</page-range>
                                    </element-citation>
                                </ref>
                            </ref-list>
                        </back>
                    </sub-article>
                </article>
                """.format(**data)

        fp = io.BytesIO(sample.encode('utf-8'))
        et = etree.parse(fp)
        for lang, html_output in domain.HTMLGenerator(et, valid_only=False):
            elements = html_output.xpath('//span[@class="element-citation journal"]')
            self.assertEqual(1, len(elements))
            page_range = elements[0].xpath('//span[@class="element_page_range"]')[0].text.strip()
            self.assertEqual(data['%s_page_range' % lang], page_range)

    @unittest.skip('tag product não é exibida por enquanto')
    def test_page_range_tag_inside_product_tag(self):
        """
        verifica que o tag <page-range> dentro de <product> seja correto no html.
        - - -
        <page-range> aparece em <product>, <element-citation>
        """
        data = {
            # lang: pt
            'pt_page_range': '300-301, 305, 407-420',
            # lang: en
            'en_page_range': '300-301, 305, 407-420',
        }
        sample = u"""<?xml version="1.0" encoding="UTF-8"?>
                <!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "JATS-journalpublishing1.dtd">
                <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" dtd-version="1.0" article-type="review-article" xml:lang="pt">
                    <front>
                        <article-meta>
                            <product product-type="book">
                                <page-range>{pt_page_range}</page-range>
                            </product>
                        </article-meta>
                    </front>
                    <sub-article xml:lang="en" article-type="translation" id="S01">
                        <front-stub>
                            <article-meta>
                                <product product-type="book">
                                    <page-range>{en_page_range}</page-range>
                                </product>
                            </article-meta>
                        </front-stub>
                    </sub-article>
                </article>
                """.format(**data)

        fp = io.BytesIO(sample.encode('utf-8'))
        et = etree.parse(fp)
        for lang, html_output in domain.HTMLGenerator(et, valid_only=False):
            products = html_output.xpath('//div[@class="product book"]')
            self.assertEqual(1, len(products))
            page_range = products[0].xpath('//span[@class="product_page_range"]')[0].text.strip()
            self.assertEqual(data['%s_page_range' % lang], page_range)

    """ <ISBN> """
    def test_isbn_tag_inside_element_citation_tag(self):
        """
        verifica que o tag <isbn> dentro de <element-citation> seja correto no html.
        - - -
        <isbn> aparece em <product>, <element-citation>
        """
        data = {
            # lang: pt
            'pt_isbn': '978-3-16-148410-0',
            # lang: en
            'en_isbn': '123-4-56-789012-3',
        }
        sample = u"""<?xml version="1.0" encoding="UTF-8"?>
                <!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "JATS-journalpublishing1.dtd">
                <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" dtd-version="1.0" article-type="review-article" xml:lang="pt">
                    <back>
                        <ref-list>
                            <ref id="B3">
                                <element-citation publication-type="journal">
                                    <isbn>{pt_isbn}</isbn>
                                </element-citation>
                            </ref>
                        </ref-list>
                    </back>
                    <sub-article xml:lang="en" article-type="translation" id="S01">
                        <back>
                            <ref-list>
                                <ref id="B3">
                                    <element-citation publication-type="journal">
                                        <isbn>{en_isbn}</isbn>
                                    </element-citation>
                                </ref>
                            </ref-list>
                        </back>
                    </sub-article>
                </article>
                """.format(**data)

        fp = io.BytesIO(sample.encode('utf-8'))
        et = etree.parse(fp)
        for lang, html_output in domain.HTMLGenerator(et, valid_only=False):
            elements = html_output.xpath('//span[@class="element-citation journal"]')
            self.assertEqual(1, len(elements))
            isbn = elements[0].xpath('//span[@class="element_isbn"]')[0].text.strip()
            self.assertEqual(data['%s_isbn' % lang], isbn)

    @unittest.skip('tag product não é exibida por enquanto')
    def test_isbn_tag_inside_product_tag(self):
        """
        verifica que o tag <isbn> dentro de <product> seja correto no html.
        - - -
        <isbn> aparece em <product>, <element-citation>
        """
        data = {
            # lang: pt
            'pt_isbn': '978-3-16-148410-0',
            # lang: en
            'en_isbn': '123-4-56-789012-3',
        }
        sample = u"""<?xml version="1.0" encoding="UTF-8"?>
                <!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "JATS-journalpublishing1.dtd">
                <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" dtd-version="1.0" article-type="review-article" xml:lang="pt">
                    <front>
                        <article-meta>
                            <product product-type="book">
                                <isbn>{pt_isbn}</isbn>
                            </product>
                        </article-meta>
                    </front>
                    <sub-article xml:lang="en" article-type="translation" id="S01">
                        <front-stub>
                            <article-meta>
                                <product product-type="book">
                                    <isbn>{en_isbn}</isbn>
                                </product>
                            </article-meta>
                        </front-stub>
                    </sub-article>
                </article>
                """.format(**data)

        fp = io.BytesIO(sample.encode('utf-8'))
        et = etree.parse(fp)
        for lang, html_output in domain.HTMLGenerator(et, valid_only=False):
            products = html_output.xpath('//div[@class="product book"]')
            self.assertEqual(1, len(products))
            isbn = products[0].xpath('//div[@class="isbn"]')[0].text.strip()
            self.assertEqual(data['%s_isbn' % lang], isbn)

    """ <SOURCE> """
    def test_source_tag_inside_element_citation_tag(self):
        """
        verifica que o tag <source> dentro de <element-citation> seja correto no html.
        - - -
        <source> aparece em <product>, <element-citation>
        """
        data = {
            # lang: pt
            'pt_source': 'A comunidade filosófica, evidenciado por uma faculdade populares',
            # lang: en
            'en_source': 'The philosophical community, evidenced by a popular college',
        }
        sample = u"""<?xml version="1.0" encoding="UTF-8"?>
                <!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "JATS-journalpublishing1.dtd">
                <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" dtd-version="1.0" article-type="review-article" xml:lang="pt">
                    <back>
                        <ref-list>
                            <ref id="B3">
                                <element-citation publication-type="journal">
                                    <source>{pt_source}</source>
                                </element-citation>
                            </ref>
                        </ref-list>
                    </back>
                    <sub-article xml:lang="en" article-type="translation" id="S01">
                        <back>
                            <ref-list>
                                <ref id="B3">
                                    <element-citation publication-type="journal">
                                        <source>{en_source}</source>
                                    </element-citation>
                                </ref>
                            </ref-list>
                        </back>
                    </sub-article>
                </article>
                """.format(**data)

        fp = io.BytesIO(sample.encode('utf-8'))
        et = etree.parse(fp)
        for lang, html_output in domain.HTMLGenerator(et, valid_only=False):
            elements = html_output.xpath('//span[@class="element-citation journal"]')
            self.assertEqual(1, len(elements))
            source = elements[0].xpath('//span[@class="element_source"]')[0].text.strip()
            self.assertEqual(data['%s_source' % lang], source)

    @unittest.skip('tag product não é exibida por enquanto')
    def test_source_tag_inside_product_tag(self):
        """
        verifica que o tag <source> dentro de <product> seja correto no html.
        - - -
        <source> aparece em <product>, <element-citation>
        """
        data = {
            # lang: pt
            'pt_source': '978-3-16-148410-0',
            # lang: en
            'en_source': '123-4-56-789012-3',
        }
        sample = u"""<?xml version="1.0" encoding="UTF-8"?>
                <!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "JATS-journalpublishing1.dtd">
                <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" dtd-version="1.0" article-type="review-article" xml:lang="pt">
                    <front>
                        <article-meta>
                            <product product-type="book">
                                <source>{pt_source}</source>
                            </product>
                        </article-meta>
                    </front>
                    <sub-article xml:lang="en" article-type="translation" id="S01">
                        <front-stub>
                            <article-meta>
                                <product product-type="book">
                                    <source>{en_source}</source>
                                </product>
                            </article-meta>
                        </front-stub>
                    </sub-article>
                </article>
                """.format(**data)

        fp = io.BytesIO(sample.encode('utf-8'))
        et = etree.parse(fp)
        for lang, html_output in domain.HTMLGenerator(et, valid_only=False):
            products = html_output.xpath('//div[@class="product book"]')
            self.assertEqual(1, len(products))
            source = products[0].xpath('//div[@class="source"]')[0].text.strip()
            self.assertEqual(data['%s_source' % lang], source)

    """ <EDITION> """
    def test_edition_tag_inside_element_citation_tag(self):
        """
        verifica que o tag <edition> dentro de <element-citation> seja correto no html.
        - - -
        <edition> aparece em <product>, <element-citation>
        """
        data = {
            # lang: pt
            'pt_edition': 'A comunidade filosófica, evidenciado por uma faculdade populares',
            # lang: en
            'en_edition': 'The philosophical community, evidenced by a popular college',
        }
        sample = u"""<?xml version="1.0" encoding="UTF-8"?>
                <!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "JATS-journalpublishing1.dtd">
                <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" dtd-version="1.0" article-type="review-article" xml:lang="pt">
                    <back>
                        <ref-list>
                            <ref id="B3">
                                <element-citation publication-type="journal">
                                    <edition>{pt_edition}</edition>
                                </element-citation>
                            </ref>
                        </ref-list>
                    </back>
                    <sub-article xml:lang="en" article-type="translation" id="S01">
                        <back>
                            <ref-list>
                                <ref id="B3">
                                    <element-citation publication-type="journal">
                                        <edition>{en_edition}</edition>
                                    </element-citation>
                                </ref>
                            </ref-list>
                        </back>
                    </sub-article>
                </article>
                """.format(**data)

        fp = io.BytesIO(sample.encode('utf-8'))
        et = etree.parse(fp)
        for lang, html_output in domain.HTMLGenerator(et, valid_only=False):
            elements = html_output.xpath('//span[@class="element-citation journal"]')
            self.assertEqual(1, len(elements))
            edition = elements[0].xpath('//span[@class="element_edition"]')[0].text.strip()
            self.assertEqual(data['%s_edition' % lang], edition)

    @unittest.skip('tag product não é exibida por enquanto')
    def test_edition_tag_inside_product_tag(self):
        """
        verifica que o tag <edition> dentro de <product> seja correto no html.
        - - -
        <edition> aparece em <product>, <element-citation>
        """
        data = {
            # lang: pt
            'pt_edition': '978-3-16-148410-0',
            # lang: en
            'en_edition': '123-4-56-789012-3',
        }
        sample = u"""<?xml version="1.0" encoding="UTF-8"?>
                <!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "JATS-journalpublishing1.dtd">
                <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" dtd-version="1.0" article-type="review-article" xml:lang="pt">
                    <front>
                        <article-meta>
                            <product product-type="book">
                                <edition>{pt_edition}</edition>
                            </product>
                        </article-meta>
                    </front>
                    <sub-article xml:lang="en" article-type="translation" id="S01">
                        <front-stub>
                            <article-meta>
                                <product product-type="book">
                                    <edition>{en_edition}</edition>
                                </product>
                            </article-meta>
                        </front-stub>
                    </sub-article>
                </article>
                """.format(**data)

        fp = io.BytesIO(sample.encode('utf-8'))
        et = etree.parse(fp)
        for lang, html_output in domain.HTMLGenerator(et, valid_only=False):
            products = html_output.xpath('//div[@class="product book"]')
            self.assertEqual(1, len(products))
            edition = products[0].xpath('//div[@class="edition"]')[0].text.strip()
            self.assertEqual(data['%s_edition' % lang], edition)

    """ <PUBLISHER-NAME> """
    def test_publisher_name_tag_inside_element_citation_tag(self):
        """
        verifica que o tag <publisher-name> dentro de <element-citation> seja correto no html.
        - - -
        <publisher-name> aparece em <product>, <element-citation>
        """
        data = {
            # lang: pt
            'pt_publisher_name': 'Jornal British Medical',
            # lang: en
            'en_publisher_name': 'British Medical Journal',
        }
        sample = u"""<?xml version="1.0" encoding="UTF-8"?>
                <!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "JATS-journalpublishing1.dtd">
                <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" dtd-version="1.0" article-type="review-article" xml:lang="pt">
                    <back>
                        <ref-list>
                            <ref id="B3">
                                <element-citation publication-type="journal">
                                    <publisher-name>{pt_publisher_name}</publisher-name>
                                </element-citation>
                            </ref>
                        </ref-list>
                    </back>
                    <sub-article xml:lang="en" article-type="translation" id="S01">
                        <back>
                            <ref-list>
                                <ref id="B3">
                                    <element-citation publication-type="journal">
                                        <publisher-name>{en_publisher_name}</publisher-name>
                                    </element-citation>
                                </ref>
                            </ref-list>
                        </back>
                    </sub-article>
                </article>
                """.format(**data)

        fp = io.BytesIO(sample.encode('utf-8'))
        et = etree.parse(fp)
        for lang, html_output in domain.HTMLGenerator(et, valid_only=False):
            elements = html_output.xpath('//span[@class="element-citation journal"]')
            self.assertEqual(1, len(elements))
            publisher_name = elements[0].xpath('//span[@class="element_publisher_name"]')[0].text.strip()
            self.assertEqual(data['%s_publisher_name' % lang], publisher_name)

    @unittest.skip('tag product não é exibida por enquanto')
    def test_publisher_name_tag_inside_product_tag(self):
        """
        verifica que o tag <publisher-name> dentro de <product> seja correto no html.
        - - -
        <publisher-name> aparece em <product>, <element-citation>
        """
        data = {
            # lang: pt
            'pt_publisher_name': 'Jornal British Medical',
            # lang: en
            'en_publisher_name': 'British Medical Journal',
        }
        sample = u"""<?xml version="1.0" encoding="UTF-8"?>
                <!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "JATS-journalpublishing1.dtd">
                <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" dtd-version="1.0" article-type="review-article" xml:lang="pt">
                    <front>
                        <article-meta>
                            <product product-type="book">
                                <publisher-name>{pt_publisher_name}</publisher-name>
                            </product>
                        </article-meta>
                    </front>
                    <sub-article xml:lang="en" article-type="translation" id="S01">
                        <front-stub>
                            <article-meta>
                                <product product-type="book">
                                    <publisher-name>{en_publisher_name}</publisher-name>
                                </product>
                            </article-meta>
                        </front-stub>
                    </sub-article>
                </article>
                """.format(**data)

        fp = io.BytesIO(sample.encode('utf-8'))
        et = etree.parse(fp)
        for lang, html_output in domain.HTMLGenerator(et, valid_only=False):
            products = html_output.xpath('//div[@class="product book"]')
            self.assertEqual(1, len(products))
            publisher_name = products[0].xpath('//div[@class="publisher-name"]')[0].text.strip()
            self.assertEqual(data['%s_publisher_name' % lang], publisher_name)

    """ <PUBLISHER-LOC> """
    def test_publisher_loc_tag_inside_element_citation_tag(self):
        """
        verifica que o tag <publisher-loc> dentro de <element-citation> seja correto no html.
        - - -
        <publisher-loc> aparece em <product>, <element-citation>
        """
        data = {
            # lang: pt
            'pt_publisher_loc': 'Jornal British Medical',
            # lang: en
            'en_publisher_loc': 'British Medical Journal',
        }
        sample = u"""<?xml version="1.0" encoding="UTF-8"?>
                <!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "JATS-journalpublishing1.dtd">
                <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" dtd-version="1.0" article-type="review-article" xml:lang="pt">
                    <back>
                        <ref-list>
                            <ref id="B3">
                                <element-citation publication-type="journal">
                                    <publisher-loc>{pt_publisher_loc}</publisher-loc>
                                </element-citation>
                            </ref>
                        </ref-list>
                    </back>
                    <sub-article xml:lang="en" article-type="translation" id="S01">
                        <back>
                            <ref-list>
                                <ref id="B3">
                                    <element-citation publication-type="journal">
                                        <publisher-loc>{en_publisher_loc}</publisher-loc>
                                    </element-citation>
                                </ref>
                            </ref-list>
                        </back>
                    </sub-article>
                </article>
                """.format(**data)

        fp = io.BytesIO(sample.encode('utf-8'))
        et = etree.parse(fp)
        for lang, html_output in domain.HTMLGenerator(et, valid_only=False):
            elements = html_output.xpath('//span[@class="element-citation journal"]')
            self.assertEqual(1, len(elements))
            publisher_loc = elements[0].xpath('//span[@class="element_publisher_loc"]')[0].text.strip()
            self.assertEqual(data['%s_publisher_loc' % lang], publisher_loc)

    @unittest.skip('tag product não é exibida por enquanto')
    def test_publisher_loc_tag_inside_product_tag(self):
        """
        verifica que o tag <publisher-loc> dentro de <product> seja correto no html.
        - - -
        <publisher-loc> aparece em <product>, <element-citation>
        """
        data = {
            # lang: pt
            'pt_publisher_loc': 'Jornal British Medical',
            # lang: en
            'en_publisher_loc': 'British Medical Journal',
        }
        sample = u"""<?xml version="1.0" encoding="UTF-8"?>
                <!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "JATS-journalpublishing1.dtd">
                <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" dtd-version="1.0" article-type="review-article" xml:lang="pt">
                    <front>
                        <article-meta>
                            <product product-type="book">
                                <publisher-loc>{pt_publisher_loc}</publisher-loc>
                            </product>
                        </article-meta>
                    </front>
                    <sub-article xml:lang="en" article-type="translation" id="S01">
                        <front-stub>
                            <article-meta>
                                <product product-type="book">
                                    <publisher-loc>{en_publisher_loc}</publisher-loc>
                                </product>
                            </article-meta>
                        </front-stub>
                    </sub-article>
                </article>
                """.format(**data)

        fp = io.BytesIO(sample.encode('utf-8'))
        et = etree.parse(fp)
        for lang, html_output in domain.HTMLGenerator(et, valid_only=False):
            products = html_output.xpath('//div[@class="product book"]')
            self.assertEqual(1, len(products))
            publisher_loc = products[0].xpath('//div[@class="publisher-loc"]')[0].text.strip()
            self.assertEqual(data['%s_publisher_loc' % lang], publisher_loc)

    """ <HISTORY, DATE> """
    def test_history_and_data_tag_inside_article_meta_tag(self):
        """
        verifica que o tag <history> (e <date> dentro do <history>) dentro de <article-meta> seja correto no html.
        - - -
        <history> aparece em <article-meta>
        <date> aparece em <history>
        """
        data = {
            #  -*- lang: pt -*-
            # received
            'pt_received_date_day': '15',
            'pt_received_date_month': '03',
            'pt_received_date_year': '2013',
            # rev_recd
            'pt_rev_recd_date_day': '06',
            'pt_rev_recd_date_month': '11',
            'pt_rev_recd_date_year': '2013',
            # accepted
            'pt_accepted_date_day': '12',
            'pt_accepted_date_month': '05',
            'pt_accepted_date_year': '2014',
            #  -*- lang: en -*-
            # received
            'en_received_date_day': '15',
            'en_received_date_month': '03',
            'en_received_date_year': '2013',
            # rev_recd
            'en_rev_recd_date_day': '06',
            'en_rev_recd_date_month': '11',
            'en_rev_recd_date_year': '2013',
            # accepted
            'en_accepted_date_day': '12',
            'en_accepted_date_month': '05',
            'en_accepted_date_year': '2014',
        }
        sample = u"""<?xml version="1.0" encoding="UTF-8"?>
                <!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "JATS-journalpublishing1.dtd">
                <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" dtd-version="1.0" article-type="review-article" xml:lang="pt">
                    <front>
                        <article-meta>
                            <history>
                                <date date-type="received">
                                    <day>{pt_received_date_day}</day>
                                    <month>{pt_received_date_month}</month>
                                    <year>{pt_received_date_year}</year>
                                </date>
                                <date date-type="rev-recd">
                                    <day>{pt_rev_recd_date_day}</day>
                                    <month>{pt_rev_recd_date_month}</month>
                                    <year>{pt_rev_recd_date_year}</year>
                                </date>
                                <date date-type="accepted">
                                    <day>{pt_accepted_date_day}</day>
                                    <month>{pt_accepted_date_month}</month>
                                    <year>{pt_accepted_date_year}</year>
                                </date>
                            </history>
                        </article-meta>
                    </front>
                    <sub-article xml:lang="en" article-type="translation" id="S01">
                        <front-stub>
                            <history>
                                <date date-type="received">
                                    <day>{en_received_date_day}</day>
                                    <month>{en_received_date_month}</month>
                                    <year>{en_received_date_year}</year>
                                </date>
                                <date date-type="rev-recd">
                                    <day>{en_rev_recd_date_day}</day>
                                    <month>{en_rev_recd_date_month}</month>
                                    <year>{en_rev_recd_date_year}</year>
                                </date>
                                <date date-type="accepted">
                                    <day>{en_accepted_date_day}</day>
                                    <month>{en_accepted_date_month}</month>
                                    <year>{en_accepted_date_year}</year>
                                </date>
                            </history>
                        </front-stub>
                    </sub-article>
                </article>
                """.format(**data)

        fp = io.BytesIO(sample.encode('utf-8'))
        et = etree.parse(fp)
        for lang, html_output in domain.HTMLGenerator(et, valid_only=False):
            histories = html_output.xpath('//section[@class="history-wrapper"]/ul')
            self.assertEqual(1, len(histories))

            history = histories[0]
            for date_type in ['received', 'rev-recd', 'accepted', ]:
                date_type_undeline = date_type.replace('-', '_')
                # day
                d_day = history.xpath('//li[@class="date %s"]//span[@class="day"]' % date_type)[0].text.strip()
                self.assertEqual(data['%s_%s_date_day' % (lang, date_type_undeline)] + "/", d_day)
                # month
                d_month = history.xpath('//li[@class="date %s"]//span[@class="month"]' % date_type)[0].text.strip()
                self.assertEqual(data['%s_%s_date_month' % (lang, date_type_undeline)] + "/", d_month)
                # year
                d_year = history.xpath('//li[@class="date %s"]//span[@class="year"]' % date_type)[0].text.strip()
                self.assertEqual(data['%s_%s_date_year' % (lang, date_type_undeline)], d_year)

    """ <PERMISSIONS, LICENSE, LICENSE-P> """
    def test_permissions_and_license_tags_inside_article_meta_tag(self):
        """
        verifica que os tags <permissions> (e <license> dentro do <permissions>,  e <license-p> dentro de <license>) dentro de <article-meta> seja correto no html.
        - - -
        <permissions> aparece em <article-meta>
        <license> aparece em <permissions>
        <license-p> aparece em <license>
        """

        data = {
            #  -*- lang: pt -*-
            'pt_license_href': 'https://creativecommons.org/licenses/by/4.0/deed.pt_BR',
            'pt_license_p': 'Este é um artigo de acesso aberto distribuído sob os termos da Licença Creative Commons Attribution, que permite uso irrestrito, distribuição e reprodução em qualquer meio, desde que a obra original, devidamente citada.',
            #  -*- lang: en -*-
            'en_license_href': 'https://creativecommons.org/licenses/by/4.0/deed.en',
            'en_license_p': 'This is an open-access article distributed under the terms of the Creative Commons Attribution License, which permits unrestricted use, distribution, and reproduction in any medium, provided the original work is properlycited',
        }
        sample = u"""<?xml version="1.0" encoding="UTF-8"?>
                <!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "JATS-journalpublishing1.dtd">
                <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" dtd-version="1.0" article-type="review-article" xml:lang="pt">
                    <front>
                        <article-meta>
                            <permissions>
                                <license license-type="open-access" xlink:href="{pt_license_href}">
                                    <license-p>{pt_license_p}</license-p>
                                </license>
                            </permissions>
                        </article-meta>
                    </front>
                    <sub-article xml:lang="en" article-type="translation" id="S01">
                        <front-stub>
                            <permissions>
                                <license license-type="open-access" xlink:href="{en_license_href}">
                                    <license-p>{en_license_p}</license-p>
                                </license>
                            </permissions>
                        </front-stub>
                    </sub-article>
                </article>
                """.format(**data)

        fp = io.BytesIO(sample.encode('utf-8'))
        et = etree.parse(fp)
        for lang, html_output in domain.HTMLGenerator(et, valid_only=False):
            permissions = html_output.xpath('//div[@class="permissions"]')
            self.assertEqual(1, len(permissions))

            license = permissions[0].xpath('//div[@class="license"]')
            self.assertEqual(1, len(license))

            link = license[0].xpath('a')
            self.assertEqual(1, len(link))

            license_text = license[0].xpath('p')
            self.assertEqual(1, len(license_text))

            self.assertEqual(data['%s_license_href' % lang], link[0].attrib['href'])
            self.assertEqual(data['%s_license_p' % lang], license_text[0].text.strip())
            self.assertEqual("view the permissions of this license", link[0].text.strip())

    """ <PERMISSIONS, COPYRIGHT-STATEMENT, COPYRIGHT-YEAR> """
    def test_permissions_and_copyright_tags_inside_article_meta_tag(self):
        """
        verifica que os tags <permissions> (e <copyright-statement> e <copyright-year> dentro do <permissions>) dentro de <article-meta> seja correto no html.
        - - -
        <permissions> aparece em <article-meta>
        <copyright-statement> aparece em <permissions>
        <copyright-year> aparece em <permissions>
        """

        data = {
            #  -*- lang: pt -*-
            'pt_statement': '(c) 2013 Elsevier Editora Ltda.',
            'pt_year': '2013',
            #  -*- lang: en -*-
            'en_statement': '(c) 2013 Elsevier Editorial Ltda.',
            'en_year': '2013',
        }
        sample = u"""<?xml version="1.0" encoding="UTF-8"?>
                <!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "JATS-journalpublishing1.dtd">
                <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" dtd-version="1.0" article-type="review-article" xml:lang="pt">
                    <front>
                        <article-meta>
                            <permissions>
                                <copyright-statement>{pt_statement}</copyright-statement>
                                <copyright-year>{pt_year}</copyright-year>
                            </permissions>
                        </article-meta>
                    </front>
                    <sub-article xml:lang="en" article-type="translation" id="S01">
                        <front-stub>
                            <permissions>
                                <copyright-statement>{en_statement}</copyright-statement>
                                <copyright-year>{en_year}</copyright-year>
                            </permissions>
                        </front-stub>
                    </sub-article>
                </article>
                """.format(**data)

        fp = io.BytesIO(sample.encode('utf-8'))
        et = etree.parse(fp)
        for lang, html_output in domain.HTMLGenerator(et, valid_only=False):
            permissions = html_output.xpath('//div[@class="permissions"]')
            self.assertEqual(1, len(permissions))
            copyright = permissions[0].xpath('//div[@class="copyright"]')
            self.assertEqual(1, len(copyright))
            copyright_year = copyright[0].xpath('span[@class="copyright-year"]')
            copyright_statement = copyright[0].xpath('span[@class="copyright-statement"]')
            self.assertEqual(1, len(copyright_year))
            self.assertEqual(1, len(copyright_statement))
            self.assertEqual(data['%s_statement' % lang], copyright_statement[0].text.strip())
            self.assertEqual(data['%s_year' % lang], copyright_year[0].text.strip())

    """ <ABSTRACT> """
    def test_abstract_tag_simple_inside_article_meta_tag(self):
        """
        verifica que os tags <abstract> dentro de <article-meta> seja correto no html.
        Nos artigos publicados na SciELO normalmente apresentam-se em dois formatos:
        - Simples: Quando apresenta de forma sucinta os principais pontos do texto sem a divisão por seções.
        - Estruturado: Quando possui seções. Cada grupo apresentado no resumo será identificado como seção e cada seção terá seu título.
        - - -
        <abstract> aparece em <article-meta>
        """

        data = {
            #  -*- lang: pt -*-
            'pt_abstract_title': 'Resumo',
            'pt_abstract_text': 'Verificar a sensibilidade e especificidade das curvas de fluxo-volume na detecção de obstrução da via aérea central (OVAC)',
            #  -*- lang: en -*-
            'en_abstract_title': 'Summary:',
            'en_abstract_text': 'Check the sensitivity and specificity of the flow-volume curves in the obstruction detection of central air (OVAC)',
        }
        sample = u"""<?xml version="1.0" encoding="UTF-8"?>
                <!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "JATS-journalpublishing1.dtd">
                <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" dtd-version="1.0" article-type="review-article" xml:lang="pt">
                    <front>
                        <article-meta>
                            <abstract xml:lang="pt">
                                <title>{pt_abstract_title}</title>
                                <p>{pt_abstract_text}</p>
                            </abstract>
                        </article-meta>
                    </front>
                    <sub-article xml:lang="en" article-type="translation" id="S01">
                        <front-stub>
                            <abstract xml:lang="en">
                                <title>{en_abstract_title}</title>
                                <p>{en_abstract_text}</p>
                            </abstract>
                        </front-stub>
                    </sub-article>
                </article>
                """.format(**data)

        fp = io.BytesIO(sample.encode('utf-8'))
        et = etree.parse(fp)
        for lang, html_output in domain.HTMLGenerator(et, valid_only=False):
            abstract = html_output.xpath('//div[@class="abstract"]')
            self.assertEqual(1, len(abstract))
            title = abstract[0].xpath('//h4[@class="abstract-title"]')
            text = abstract[0].xpath('//p[@class="abstract-p"]')

            self.assertEqual(1, len(title))
            self.assertEqual(1, len(text))

            self.assertEqual(data['%s_abstract_title' % lang], title[0].text.strip())
            self.assertEqual(data['%s_abstract_text' % lang], text[0].text.strip())

    def test_abstract_tag_strucutured_with_section_inside_article_meta_tag(self):
        """
        verifica que os tags <abstract> dentro de <article-meta> seja correto no html.
        Nos artigos publicados na SciELO normalmente apresentam-se em dois formatos:
        - Simples: Quando apresenta de forma sucinta os principais pontos do texto sem a divisão por seções.
        - Estruturado: Quando possui seções. Cada grupo apresentado no resumo será identificado como seção e cada seção terá seu título.
        - - -
        <abstract> aparece em <article-meta>
        """

        data = {
            #  -*- lang: pt -*-
            'pt_abstract_title': 'Resumo',
            'pt_abstract_sec_title': 'Foo',
            'pt_abstract_text': 'Verificar a sensibilidade e especificidade das curvas de fluxo-volume na detecção de obstrução da via aérea central (OVAC)',
            #  -*- lang: en -*-
            'en_abstract_title': 'Summary:',
            'en_abstract_sec_title': 'Bar',
            'en_abstract_text': 'Check the sensitivity and specificity of the flow-volume curves in the obstruction detection of central air (OVAC)',
        }
        sample = u"""<?xml version="1.0" encoding="UTF-8"?>
                <!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "JATS-journalpublishing1.dtd">
                <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" dtd-version="1.0" article-type="review-article" xml:lang="pt">
                    <front>
                        <article-meta>
                            <abstract xml:lang="pt">
                                <title>{pt_abstract_title}</title>
                                <sec>
                                    <title>{pt_abstract_sec_title}</title>
                                    <p>{pt_abstract_text}</p>
                                </sec>
                            </abstract>
                        </article-meta>
                    </front>
                    <sub-article xml:lang="en" article-type="translation" id="S01">
                        <front-stub>
                            <abstract xml:lang="en">
                                <title>{en_abstract_title}</title>
                                <sec>
                                    <title>{en_abstract_sec_title}</title>
                                    <p>{en_abstract_text}</p>
                                </sec>
                            </abstract>
                        </front-stub>
                    </sub-article>
                </article>
                """.format(**data)

        fp = io.BytesIO(sample.encode('utf-8'))
        et = etree.parse(fp)
        for lang, html_output in domain.HTMLGenerator(et, valid_only=False):
            abstract = html_output.xpath('//div[@class="abstract"]')
            self.assertEqual(1, len(abstract))
            title = abstract[0].xpath('//h4[@class="abstract-title"]')
            sec_title = abstract[0].xpath('//h5[@class="abstract-sec-title"]')
            text = abstract[0].xpath('//p[@class="abstract-p"]')

            self.assertEqual(1, len(title))
            self.assertEqual(1, len(text))

            self.assertEqual(data['%s_abstract_title' % lang], title[0].text.strip())
            self.assertEqual(data['%s_abstract_sec_title' % lang], sec_title[0].text.strip())
            self.assertEqual(data['%s_abstract_text' % lang], text[0].text.strip())

    """ <TRANS-ABSTRACT> """
    def test_trans_abstract_tag_simple_inside_article_meta_tag(self):
        """
        verifica que os tags <trans-abstract> dentro de <article-meta> seja correto no html.
        Nos artigos publicados na SciELO normalmente apresentam-se em dois formatos:
        - Simples: Quando apresenta de forma sucinta os principais pontos do texto sem a divisão por seções.
        - Estruturado: Quando possui seções. Cada grupo apresentado no resumo será identificado como seção e cada seção terá seu título.
        - - -
        <trans-abstract> aparece em <article-meta>
        """

        data = {
            #  -*- lang: pt -*-
            'pt_abstract_title': 'Resumo',
            'pt_abstract_text': 'Verificar a sensibilidade e especificidade das curvas de fluxo-volume na detecção de obstrução da via aérea central (OVAC)',
            #  -*- lang: en -*-
            'en_abstract_title': 'Summary:',
            'en_abstract_text': 'Check the sensitivity and specificity of the flow-volume curves in the obstruction detection of central air (OVAC)',
        }
        sample = u"""<?xml version="1.0" encoding="UTF-8"?>
                <!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "JATS-journalpublishing1.dtd">
                <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" dtd-version="1.0" article-type="review-article" xml:lang="pt">
                    <front>
                        <article-meta>
                            <abstract xml:lang="pt">
                                <title>{pt_abstract_title}</title>
                                <p>{pt_abstract_text}</p>
                            </abstract>
                            <trans-abstract xml:lang="en">
                                <title>{en_abstract_title}</title>
                                <p>{en_abstract_text}</p>
                            </trans-abstract>
                        </article-meta>
                    </front>
                    <sub-article xml:lang="en" article-type="translation" id="S01">
                    </sub-article>
                </article>
                """.format(**data)

        fp = io.BytesIO(sample.encode('utf-8'))
        et = etree.parse(fp)
        for lang, html_output in domain.HTMLGenerator(et, valid_only=False):
            abstract = html_output.xpath('//div[@class="abstract"]')
            self.assertEqual(1, len(abstract))
            title = abstract[0].xpath('//h4[@class="abstract-title"]')
            text = abstract[0].xpath('//p[@class="abstract-p"]')

            self.assertEqual(1, len(title))
            self.assertEqual(1, len(text))

            self.assertEqual(data['%s_abstract_title' % lang], title[0].text.strip())
            self.assertEqual(data['%s_abstract_text' % lang], text[0].text.strip())

    def test_trans_abstract_tag_strucutured_with_section_inside_article_meta_tag(self):
        """
        verifica que os tags <trans-abstract> dentro de <article-meta> seja correto no html.
        Nos artigos publicados na SciELO normalmente apresentam-se em dois formatos:
        - Simples: Quando apresenta de forma sucinta os principais pontos do texto sem a divisão por seções.
        - Estruturado: Quando possui seções. Cada grupo apresentado no resumo será identificado como seção e cada seção terá seu título.
        - - -
        <trans-abstract> aparece em <article-meta>
        """

        data = {
            #  -*- lang: pt -*-
            'pt_abstract_title': 'Resumo',
            'pt_abstract_sec_title': 'Foo',
            'pt_abstract_text': 'Verificar a sensibilidade e especificidade das curvas de fluxo-volume na detecção de obstrução da via aérea central (OVAC)',
            #  -*- lang: en -*-
            'en_abstract_title': 'Summary:',
            'en_abstract_sec_title': 'Bar',
            'en_abstract_text': 'Check the sensitivity and specificity of the flow-volume curves in the obstruction detection of central air (OVAC)',
        }
        sample = u"""<?xml version="1.0" encoding="UTF-8"?>
                <!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "JATS-journalpublishing1.dtd">
                <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" dtd-version="1.0" article-type="review-article" xml:lang="pt">
                    <front>
                        <article-meta>
                            <abstract xml:lang="pt">
                                <title>{pt_abstract_title}</title>
                                <sec>
                                    <title>{pt_abstract_sec_title}</title>
                                    <p>{pt_abstract_text}</p>
                                </sec>
                            </abstract>
                            <trans-abstract xml:lang="en">
                                <title>{en_abstract_title}</title>
                                <sec>
                                    <title>{en_abstract_sec_title}</title>
                                    <p>{en_abstract_text}</p>
                                </sec>
                            </trans-abstract>
                        </article-meta>
                    </front>
                    <sub-article xml:lang="en" article-type="translation" id="S01">
                    </sub-article>
                </article>
                """.format(**data)

        fp = io.BytesIO(sample.encode('utf-8'))
        et = etree.parse(fp)
        for lang, html_output in domain.HTMLGenerator(et, valid_only=False):
            abstract = html_output.xpath('//div[@class="abstract"]')
            self.assertEqual(1, len(abstract))
            title = abstract[0].xpath('//h4[@class="abstract-title"]')
            sec_title = abstract[0].xpath('//h5[@class="abstract-sec-title"]')
            text = abstract[0].xpath('//p[@class="abstract-p"]')

            self.assertEqual(1, len(title))
            self.assertEqual(1, len(text))

            self.assertEqual(data['%s_abstract_title' % lang], title[0].text.strip())
            self.assertEqual(data['%s_abstract_sec_title' % lang], sec_title[0].text.strip())
            self.assertEqual(data['%s_abstract_text' % lang], text[0].text.strip())

    """ <KWD-GROUP, KWD> """
    def test_kwd_group_tag_inside_article_meta_tag(self):
        """
        verifica que os tags <kwd-group> dentro de <article-meta> seja correto no html.
        - - -
        <kwd-group> aparece em <article-meta>
        <kwd> aparece em <kwd-group>
        """

        data = {
            #  -*- lang: pt -*-
            'pt_kwd_title': 'Palavras-chave',
            'pt_kwd_text_1': 'Broncoscopia',
            'pt_kwd_text_2': 'Curvas de fluxo-volume expiratório máximo',
            'pt_kwd_text_3': 'sensibilidade e especificidade',
            #  -*- lang: en -*-
            'en_kwd_title': 'Keywords',
            'en_kwd_text_1': 'Broncoscopy',
            'en_kwd_text_2': 'Maximal expiratory flow-volume curves',
            'en_kwd_text_3': 'Sensitivity and specificity',
        }
        sample = u"""<?xml version="1.0" encoding="UTF-8"?>
                <!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "JATS-journalpublishing1.dtd">
                <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" dtd-version="1.0" article-type="review-article" xml:lang="pt">
                    <front>
                        <article-meta>
                            <kwd-group xml:lang="pt">
                                <title>{pt_kwd_title}</title>
                                <kwd>{pt_kwd_text_1}</kwd>
                                <kwd>{pt_kwd_text_2}</kwd>
                                <kwd>{pt_kwd_text_3}</kwd>
                            </kwd-group>
                            <kwd-group xml:lang="en">
                                <title>{en_kwd_title}</title>
                                <kwd>{en_kwd_text_1}</kwd>
                                <kwd>{en_kwd_text_2}</kwd>
                                <kwd>{en_kwd_text_3}</kwd>
                            </kwd-group>
                        </article-meta>
                    </front>
                    <sub-article xml:lang="en" article-type="translation" id="S01">
                    </sub-article>
                </article>
                """.format(**data)

        fp = io.BytesIO(sample.encode('utf-8'))
        et = etree.parse(fp)
        for lang, html_output in domain.HTMLGenerator(et, valid_only=False):
            kwd_group = html_output.xpath('//ul[@class="kwd-group list-unstyled"]')
            self.assertEqual(1, len(kwd_group))

            kwd_group_item = kwd_group[0].xpath('li[@class="kwd-group-item"]')
            self.assertEqual(1, len(kwd_group_item))

            kwd_group_title = kwd_group_item[0].xpath('//h4[@class="kwd-group-title"]')
            self.assertEqual(1, len(kwd_group_title))

            kwds = kwd_group_item[0].xpath('ul[@class="kwds list-inline"]/li[@class="kwd"]')
            self.assertEqual(3, len(kwds))

            # kwd-group-title
            self.assertEqual(data['%s_kwd_title' % lang], kwd_group_title[0].text.strip())
            # kwds
            self.assertEqual(data['%s_kwd_text_1' % lang], kwds[0].text.strip())
            self.assertEqual(data['%s_kwd_text_2' % lang], kwds[1].text.strip())
            self.assertEqual(data['%s_kwd_text_3' % lang], kwds[2].text.strip())

    """ <FUNDING-GROUP>, <AWARD-GROUP>, <FUNDING-SOURCE>, <AWARD-ID>, <FUNDING-STATEMENT> """
    def test_funding_source_tag_inside_article_meta_tag(self):
        """
        verifica que os tags <funding-group> dentro de <article-meta> seja correto no html.
        verifica que os tags <award-group> dentro de <funding-group> seja correto no html.
        verifica que os tags <funding-source> dentro de <award-group> seja correto no html.
        verifica que os tags <award-id> dentro de <award-group> seja correto no html.
        verifica que os tags <funding-statement> dentro de <funding-group> seja correto no html.
        - - -
        <funding-group> aparece em <article-meta>
        <award-group> aparece em <funding-group>
        <funding-source> aparece em <award-group>
        <award-id> aparece em <award-group>
        <funding-statement> aparece em <funding-group>
        """

        data = {
            #  -*- lang: pt -*-
            'pt_funding_source': 'Coordenação de Aperfeiçoamento de Pessoal de Nível Superior',
            'pt_award_id': '04/08142-0',
            'pt_funding_statement': 'Este estudo foi apoiado em parte por ...',
            #  -*- lang: en -*-
            'en_funding_source': 'Higher Education Personnel Improvement Coordination',
            'en_award_id': '04/08142-0',
            'en_funding_statement': 'This study was supported in part by ...',
        }
        sample = u"""<?xml version="1.0" encoding="UTF-8"?>
                <!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "JATS-journalpublishing1.dtd">
                <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" dtd-version="1.0" article-type="review-article" xml:lang="pt">
                    <front>
                        <article-meta>
                            <funding-group>
                                <award-group>
                                    <funding-source>{pt_funding_source}</funding-source>
                                    <award-id>{pt_award_id}</award-id>
                                </award-group>
                                <funding-statement>{pt_funding_statement}</funding-statement>
                            </funding-group>
                        </article-meta>
                    </front>
                    <sub-article xml:lang="en" article-type="translation" id="S01">
                        <front-stub>
                            <funding-group>
                                <award-group>
                                    <funding-source>{en_funding_source}</funding-source>
                                    <award-id>{en_award_id}</award-id>
                                </award-group>
                                <funding-statement>{en_funding_statement}</funding-statement>
                            </funding-group>
                        </front-stub>
                    </sub-article>
                </article>
                """.format(**data)

        fp = io.BytesIO(sample.encode('utf-8'))
        et = etree.parse(fp)
        for lang, html_output in domain.HTMLGenerator(et, valid_only=False):
            funding_group = html_output.xpath('//div[@class="funding-group"]')
            self.assertEqual(1, len(funding_group))
            # funding-statement
            funding_statement = funding_group[0].xpath('//li[@class="funding-statement"]')
            self.assertEqual(1, len(funding_statement))
            self.assertEqual(data['%s_funding_statement' % lang], funding_statement[0].text.strip())

    """ <COUNT>, <FIG-COUNT>, <TABLE-COUNT>, <EQUATION-COUNT>, <REF-COUNT>, <PAGE-COUNT> """
    @unittest.skip('tags *count não são exibidas por enquanto')
    def test_count_tags_inside_article_meta_tag(self):
        """
        verifica que os tags <count> dentro de <article-meta> seja correto no html.
        verifica que os tags <fig-count> dentro de <count> seja correto no html.
        verifica que os tags <table-count> dentro de <count> seja correto no html.
        verifica que os tags <equation-count> dentro de <count> seja correto no html.
        verifica que os tags <ref-count> dentro de <count> seja correto no html.
        verifica que os tags <page-count> dentro de <count> seja correto no html.
        - - -
        <count> aparece em <article-meta>
        <fig-count> aparece em <count>
        <table-count> aparece em <count>
        <equation-count> aparece em <count>
        <ref-count> aparece em <count>
        <page-count> aparece em <count>
        """

        data = {
            #  -*- lang: pt -*-
            'pt_fig_count': '1',
            'pt_table_count': '2',
            'pt_equation_count': '3',
            'pt_ref_count': '4',
            'pt_page_count': '5',
            #  -*- lang: en -*-
            'en_fig_count': '1',
            'en_table_count': '2',
            'en_equation_count': '3',
            'en_ref_count': '4',
            'en_page_count': '5',
        }
        sample = u"""<?xml version="1.0" encoding="UTF-8"?>
                <!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "JATS-journalpublishing1.dtd">
                <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" dtd-version="1.0" article-type="review-article" xml:lang="pt">
                    <front>
                        <article-meta>
                            <counts>
                                <fig-count count="{pt_fig_count}"/>
                                <table-count count="{pt_table_count}"/>
                                <equation-count count="{pt_equation_count}"/>
                                <ref-count count="{pt_ref_count}"/>
                                <page-count count="{pt_page_count}"/>
                            </counts>
                        </article-meta>
                    </front>
                    <sub-article xml:lang="en" article-type="translation" id="S01">
                        <front-stub>
                            <counts>
                                <fig-count count="{en_fig_count}"/>
                                <table-count count="{en_table_count}"/>
                                <equation-count count="{en_equation_count}"/>
                                <ref-count count="{en_ref_count}"/>
                                <page-count count="{en_page_count}"/>
                            </counts>
                        </front-stub>
                    </sub-article>
                </article>
                """.format(**data)

        fp = io.BytesIO(sample.encode('utf-8'))
        et = etree.parse(fp)
        for lang, html_output in domain.HTMLGenerator(et, valid_only=False):
            counts = html_output.xpath('//ul[@class="counts"]')
            self.assertEqual(1, len(counts))
            # fig-count
            fig_count = counts[0].xpath('//li/span[@class="fig-count"]')
            self.assertEqual(1, len(fig_count))
            # table-count
            table_count = counts[0].xpath('//li/span[@class="table-count"]')
            self.assertEqual(1, len(table_count))
            # equation-count
            equation_count = counts[0].xpath('//li/span[@class="equation-count"]')
            self.assertEqual(1, len(equation_count))
            # ref-count
            ref_count = counts[0].xpath('//li/span[@class="ref-count"]')
            self.assertEqual(1, len(ref_count))
            # page-count
            page_count = counts[0].xpath('//li/span[@class="page-count"]')
            self.assertEqual(1, len(page_count))
            # # then:
            self.assertEqual(data['%s_fig_count' % lang], fig_count[0].text.strip())
            self.assertEqual(data['%s_table_count' % lang], table_count[0].text.strip())
            self.assertEqual(data['%s_equation_count' % lang], equation_count[0].text.strip())
            self.assertEqual(data['%s_ref_count' % lang], ref_count[0].text.strip())
            self.assertEqual(data['%s_page_count' % lang], page_count[0].text.strip())


class GeneratedBodyTagsTests(unittest.TestCase):

    # *************** #
    # ***** BODY **** #
    # *************** #

    """ <SEC> """
    def test_sec_tag_with_sectype_attrib_simple_inside_body_tag(self):
        """
        verifica que o tag <sec> dentro de <body> seja correto no html.
        - <sec> com atributo @sec-type simples.
        - sem <sec> aninhadas (compostas)
        - - -
        <sec> aparece em <body>
        """
        data = {
            #  -*- lang: pt -*-
            'pt_sec_type': 'intro',
            'pt_title': 'Introdução',
            'pt_text': 'Texto em PT-BR',
            #  -*- lang: en -*-
            'en_sec_type': 'intro',
            'en_title': 'Introduction',
            'en_text': 'Text in EN',
        }
        sample = u"""<?xml version="1.0" encoding="UTF-8"?>
                <!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "JATS-journalpublishing1.dtd">
                <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" dtd-version="1.0" article-type="review-article" xml:lang="pt">
                    <body>
                        <sec sec-type="{pt_sec_type}">
                            <title>{pt_title}</title>
                            <p>{pt_text}</p>
                        </sec>
                    </body>
                    <sub-article xml:lang="en" article-type="translation" id="S01">
                        <body>
                            <sec sec-type="{en_sec_type}">
                                <title>{en_title}</title>
                                <p>{en_text}</p>
                            </sec>
                        </body>
                    </sub-article>
                </article>
                """.format(**data)
        fp = io.BytesIO(sample.encode('utf-8'))
        et = etree.parse(fp)
        for lang, html_output in domain.HTMLGenerator(et, valid_only=False):
            sec_type = data['%s_sec_type' % lang]
            secs = html_output.xpath('//article[@class="body-wrapper"]/section[@class="%s"]' % sec_type)
            self.assertEqual(1, len(secs))
            title = secs[0].xpath('//header/h2')
            self.assertEqual(1, len(title))
            text = secs[0].xpath('//p')
            self.assertEqual(1, len(text))
            self.assertEqual(data['%s_title' % lang], title[0].text.strip())
            self.assertEqual(data['%s_text' % lang], text[0].text.strip())

    def test_sec_tag_without_sectype_attr_inside_body_tag(self):
        """
        verifica que o tag <sec> dentro de <body> seja correto no html.
        o tag <sec> sem atributo @sec-type
        - - -
        <sec> aparece em <body>
        """
        data = {
            #  -*- lang: pt -*-
            'pt_title': 'Introdução',
            'pt_text': 'Texto em PT-BR',
            #  -*- lang: en -*-
            'en_title': 'Introduction',
            'en_text': 'Text in EN',
        }
        sample = u"""<?xml version="1.0" encoding="UTF-8"?>
                <!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "JATS-journalpublishing1.dtd">
                <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" dtd-version="1.0" article-type="review-article" xml:lang="pt">
                    <body>
                        <sec>
                            <title>{pt_title}</title>
                            <p>{pt_text}</p>
                        </sec>
                    </body>
                    <sub-article xml:lang="en" article-type="translation" id="S01">
                        <body>
                            <sec>
                                <title>{en_title}</title>
                                <p>{en_text}</p>
                            </sec>
                        </body>
                    </sub-article>
                </article>
                """.format(**data)
        fp = io.BytesIO(sample.encode('utf-8'))
        et = etree.parse(fp)
        for lang, html_output in domain.HTMLGenerator(et, valid_only=False):
            secs = html_output.xpath('//article[@class="body-wrapper"]/section')
            self.assertEqual(1, len(secs))
            title = secs[0].xpath('//header/h2')
            self.assertEqual(1, len(title))
            text = secs[0].xpath('//p')
            self.assertEqual(1, len(text))
            self.assertEqual(data['%s_title' % lang], title[0].text.strip())
            self.assertEqual(data['%s_text' % lang], text[0].text.strip())

    def test_sec_tag_with_sectype_combined_attr_inside_body_tag(self):
        """
        verifica que o tag <sec> dentro de <body> seja correto no html.
        no <sec> o atributo @sec-type é combinado: "materials|methods"
        - - -
        <sec> aparece em <body>
        """
        data = {
            #  -*- lang: pt -*-
            'pt_sec_type': 'materials|methods',
            'pt_title': 'Introdução',
            'pt_text': 'Texto em PT-BR',
            #  -*- lang: en -*-
            'en_sec_type': 'materials|methods',
            'en_title': 'Introduction',
            'en_text': 'Text in EN',
        }
        sample = u"""<?xml version="1.0" encoding="UTF-8"?>
                <!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "JATS-journalpublishing1.dtd">
                <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" dtd-version="1.0" article-type="review-article" xml:lang="pt">
                    <body>
                        <sec sec-type="{pt_sec_type}">
                            <title>{pt_title}</title>
                            <p>{pt_text}</p>
                        </sec>
                    </body>
                    <sub-article xml:lang="en" article-type="translation" id="S01">
                        <body>
                            <sec sec-type="{en_sec_type}">
                                <title>{en_title}</title>
                                <p>{en_text}</p>
                            </sec>
                        </body>
                    </sub-article>
                </article>
                """.format(**data)
        fp = io.BytesIO(sample.encode('utf-8'))
        et = etree.parse(fp)
        for lang, html_output in domain.HTMLGenerator(et, valid_only=False):
            sec_type = data['%s_sec_type' % lang].replace('|', ' ')
            secs = html_output.xpath('//article[@class="body-wrapper"]/section[@class="%s"]' % sec_type)
            self.assertEqual(1, len(secs))
            title = secs[0].xpath('//header/h2')
            self.assertEqual(1, len(title))
            text = secs[0].xpath('//p')
            self.assertEqual(1, len(text))
            self.assertEqual(data['%s_title' % lang], title[0].text.strip())
            self.assertEqual(data['%s_text' % lang], text[0].text.strip())

    def test_sec_tag_with_subsection_attr_inside_body_tag(self):
        """
        verifica que o tag <sec> dentro de <body> seja correto no html.
        o tag <sec> contem outro tag <sec> aninhadas
        - - -
        <sec> aparece em <body>
        """
        data = {
            #  -*- lang: pt -*-
            'pt_sec_type': 'intro',
            'pt_title': 'Introdução',
            'pt_subsec_type': 'methods',
            'pt_subtitle': 'Metodologia em ciencia',
            'pt_subtext': 'Texto em PT-BR',
            #  -*- lang: en -*-
            'en_sec_type': 'intro',
            'en_title': 'Introduction',
            'en_subsec_type': 'methods',
            'en_subtitle': 'Methodology in Science',
            'en_subtext': 'Text in EN',
        }
        sample = u"""<?xml version="1.0" encoding="UTF-8"?>
                <!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "JATS-journalpublishing1.dtd">
                <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" dtd-version="1.0" article-type="review-article" xml:lang="pt">
                    <body>
                        <sec sec-type="{pt_sec_type}">
                            <title>{pt_title}</title>
                            <sec sec-type="{pt_subsec_type}">
                                <title>{pt_subtitle}</title>
                                <p>{pt_subtext}</p>
                            </sec>
                        </sec>
                    </body>
                    <sub-article xml:lang="en" article-type="translation" id="S01">
                        <body>
                            <sec sec-type="{en_sec_type}">
                                <title>{en_title}</title>
                                <sec sec-type="{en_subsec_type}">
                                    <title>{en_subtitle}</title>
                                    <p>{en_subtext}</p>
                                </sec>
                            </sec>
                        </body>
                    </sub-article>
                </article>
                """.format(**data)
        fp = io.BytesIO(sample.encode('utf-8'))
        et = etree.parse(fp)
        for lang, html_output in domain.HTMLGenerator(et, valid_only=False):
            sec_type = data['%s_sec_type' % lang]
            subsec_type = data['%s_subsec_type' % lang]

            secs = html_output.xpath('//article[@class="body-wrapper"]/section[@class="%s"]' % sec_type)
            self.assertEqual(1, len(secs))

            title = secs[0].xpath('//section[@class="%s"]/header/h2' % sec_type)
            self.assertEqual(1, len(title))

            sub_title = secs[0].xpath('//section[@class="%s"]/section[@class="%s"]/header/h2' % (sec_type, subsec_type))
            self.assertEqual(1, len(sub_title))

            sub_text = secs[0].xpath('//section[@class="%s"]/section[@class="%s"]/p' % (sec_type, subsec_type))
            self.assertEqual(1, len(sub_text))

            self.assertEqual(data['%s_title' % lang], title[0].text.strip())
            self.assertEqual(data['%s_subtitle' % lang], sub_title[0].text.strip())
            self.assertEqual(data['%s_subtext' % lang], sub_text[0].text.strip())

    """ <DISP-FORMULA> with <GRAPHIC> """
    def test_disp_formula_with_graphic_tag_inside_body_tag(self):
        """
        verifica que o tag <disp-formula> (contendo <graphic>), dentro de <body> seja correto no html.
        - - -
        <disp-formula> aparece em <body>, <p>, <th>, <td>, <app>, <supplementary-material>
        """
        data = {
            #  -*- lang: pt -*-
            'pt_disp_id': 'e01',
            'pt_graphic_href': '1234-5678-rctb-45-05-0110-e01.tif',
            #  -*- lang: en -*-
            'en_disp_id': 'e02',
            'en_graphic_href': '1234-5678-rctb-45-05-0110-e02.tif',
        }
        sample = u"""<?xml version="1.0" encoding="UTF-8"?>
                <!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "JATS-journalpublishing1.dtd">
                <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" dtd-version="1.0" article-type="review-article" xml:lang="pt">
                    <body>
                        <disp-formula id="{pt_disp_id}">
                            <graphic xlink:href="{pt_graphic_href}" />
                        </disp-formula>
                    </body>
                    <sub-article xml:lang="en" article-type="translation" id="S01">
                        <body>
                            <disp-formula id="{en_disp_id}">
                                <graphic xlink:href="{en_graphic_href}" />
                            </disp-formula>
                        </body>
                    </sub-article>
                </article>
                """.format(**data)
        fp = io.BytesIO(sample.encode('utf-8'))
        et = etree.parse(fp)
        for lang, html_output in domain.HTMLGenerator(et, valid_only=False):
            formula_id = data['%s_disp_id' % lang]

            formulas = html_output.xpath('//article[@class="body-wrapper"]/div[@class="disp-formula %s"]' % formula_id)
            self.assertEqual(1, len(formulas))

            formula_link = formulas[0].xpath('a')
            self.assertEqual(1, len(formula_link))

            graphic_img = formula_link[0].xpath('img')
            self.assertEqual(1, len(graphic_img))

            self.assertIn(data['%s_graphic_href' % lang], formula_link[0].attrib['href'])
            self.assertIn(data['%s_graphic_href' % lang], graphic_img[0].attrib['src'])

    def test_disp_formula_with_graphic_tag_inside_p_tag(self):
        """
        verifica que o tag <disp-formula> (contendo <graphic>), dentro de <p> seja correto no html.
        - - -
        <disp-formula> aparece em <body>, <p>, <th>, <td>, <app>, <supplementary-material>
        """
        data = {
            #  -*- lang: pt -*-
            'pt_disp_id': 'e01',
            'pt_graphic_href': '1234-5678-rctb-45-05-0110-e01.tif',
            #  -*- lang: en -*-
            'en_disp_id': 'e02',
            'en_graphic_href': '1234-5678-rctb-45-05-0110-e02.tif',
        }
        sample = u"""<?xml version="1.0" encoding="UTF-8"?>
                <!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "JATS-journalpublishing1.dtd">
                <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" dtd-version="1.0" article-type="review-article" xml:lang="pt">
                    <body>
                        <p>
                            <disp-formula id="{pt_disp_id}">
                                <graphic xlink:href="{pt_graphic_href}" />
                            </disp-formula>
                        </p>
                    </body>
                    <sub-article xml:lang="en" article-type="translation" id="S01">
                        <body>
                            <p>
                                <disp-formula id="{en_disp_id}">
                                    <graphic xlink:href="{en_graphic_href}" />
                                </disp-formula>
                            </p>
                        </body>
                    </sub-article>
                </article>
                """.format(**data)
        fp = io.BytesIO(sample.encode('utf-8'))
        et = etree.parse(fp)
        for lang, html_output in domain.HTMLGenerator(et, valid_only=False):
            formula_id = data['%s_disp_id' % lang]

            formulas = html_output.xpath('//article[@class="body-wrapper"]/p/div[@class="disp-formula %s"]' % formula_id)
            self.assertEqual(1, len(formulas))

            formula_link = formulas[0].xpath('a')
            self.assertEqual(1, len(formula_link))

            graphic_img = formula_link[0].xpath('img')
            self.assertEqual(1, len(graphic_img))

            self.assertIn(data['%s_graphic_href' % lang], formula_link[0].attrib['href'])
            self.assertIn(data['%s_graphic_href' % lang], graphic_img[0].attrib['src'])

    def test_disp_formula_with_graphic_tag_inside_th_tag(self):
        """
        verifica que o tag <disp-formula> (contendo <graphic>), dentro de <th> seja correto no html.
        - - -
        <disp-formula> aparece em <body>, <p>, <th>, <td>, <app>, <supplementary-material>
        """
        data = {
            #  -*- lang: pt -*-
            'pt_disp_id': 'e01',
            'pt_graphic_href': '1234-5678-rctb-45-05-0110-e01.tif',
            #  -*- lang: en -*-
            'en_disp_id': 'e02',
            'en_graphic_href': '1234-5678-rctb-45-05-0110-e02.tif',
        }
        sample = u"""<?xml version="1.0" encoding="UTF-8"?>
                <!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "JATS-journalpublishing1.dtd">
                <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" dtd-version="1.0" article-type="review-article" xml:lang="pt">
                    <body>
                        <p>
                            <table-wrap id="t01">
                                <table>
                                    <thead>
                                        <tr>
                                            <th>
                                                <disp-formula id="{pt_disp_id}">
                                                    <graphic xlink:href="{pt_graphic_href}" />
                                                </disp-formula>
                                            </th>
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
                    </body>
                    <sub-article xml:lang="en" article-type="translation" id="S01">
                        <body>
                            <p>
                                <table-wrap id="t01">
                                    <table>
                                        <thead>
                                            <tr>
                                                <th>
                                                    <disp-formula id="{en_disp_id}">
                                                        <graphic xlink:href="{en_graphic_href}" />
                                                    </disp-formula>
                                                </th>
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
                        </body>
                    </sub-article>
                </article>
                """.format(**data)
        fp = io.BytesIO(sample.encode('utf-8'))
        et = etree.parse(fp)
        for lang, html_output in domain.HTMLGenerator(et, valid_only=False):
            formula_id = data['%s_disp_id' % lang]
            formulas = html_output.xpath('//article[@class="body-wrapper"]//table[@class="table"]/thead/tr/th/div[@class="disp-formula %s"]' % formula_id)
            self.assertEqual(1, len(formulas))

            formula_link = formulas[0].xpath('a')
            self.assertEqual(1, len(formula_link))

            graphic_img = formula_link[0].xpath('img')
            self.assertEqual(1, len(graphic_img))

            self.assertIn(data['%s_graphic_href' % lang], formula_link[0].attrib['href'])
            self.assertIn(data['%s_graphic_href' % lang], graphic_img[0].attrib['src'])

    def test_disp_formula_with_graphic_tag_inside_td_tag(self):
        """
        verifica que o tag <disp-formula> (contendo <graphic>), dentro de <td> seja correto no html.
        - - -
        <disp-formula> aparece em <body>, <p>, <th>, <td>, <app>, <supplementary-material>
        """
        data = {
            #  -*- lang: pt -*-
            'pt_disp_id': 'e01',
            'pt_graphic_href': '1234-5678-rctb-45-05-0110-e01.tif',
            #  -*- lang: en -*-
            'en_disp_id': 'e02',
            'en_graphic_href': '1234-5678-rctb-45-05-0110-e02.tif',
        }
        sample = u"""<?xml version="1.0" encoding="UTF-8"?>
                <!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "JATS-journalpublishing1.dtd">
                <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" dtd-version="1.0" article-type="review-article" xml:lang="pt">
                    <body>
                        <p>
                            <table-wrap id="t01">
                                <table>
                                    <thead>
                                        <tr>
                                            <th>FOO</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <tr>
                                            <td>
                                                <disp-formula id="{pt_disp_id}">
                                                    <graphic xlink:href="{pt_graphic_href}" />
                                                </disp-formula>
                                            </td>
                                        </tr>
                                    </tbody>
                                </table>
                            </table-wrap>
                        </p>
                    </body>
                    <sub-article xml:lang="en" article-type="translation" id="S01">
                        <body>
                            <p>
                                <table-wrap id="t01">
                                    <table>
                                        <thead>
                                            <tr>
                                                <th>FOO</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            <tr>
                                                <td>
                                                    <disp-formula id="{en_disp_id}">
                                                        <graphic xlink:href="{en_graphic_href}" />
                                                    </disp-formula>
                                                </td>
                                            </tr>
                                        </tbody>
                                    </table>
                                </table-wrap>
                            </p>
                        </body>
                    </sub-article>
                </article>
                """.format(**data)
        fp = io.BytesIO(sample.encode('utf-8'))
        et = etree.parse(fp)
        for lang, html_output in domain.HTMLGenerator(et, valid_only=False):
            formula_id = data['%s_disp_id' % lang]
            formulas = html_output.xpath('//article[@class="body-wrapper"]//table[@class="table"]/tbody/tr/td/div[@class="disp-formula %s"]' % formula_id)
            self.assertEqual(1, len(formulas))

            formula_link = formulas[0].xpath('a')
            self.assertEqual(1, len(formula_link))

            graphic_img = formula_link[0].xpath('img')
            self.assertEqual(1, len(graphic_img))

            self.assertIn(data['%s_graphic_href' % lang], formula_link[0].attrib['href'])
            self.assertIn(data['%s_graphic_href' % lang], graphic_img[0].attrib['src'])

    @unittest.skip('tag app/app-group não é exibida por enquanto')
    def test_disp_formula_with_graphic_tag_inside_app_tag(self):
        """
        verifica que o tag <disp-formula> (contendo <graphic>), dentro de <app> seja correto no html.
        - - -
        <disp-formula> aparece em <body>, <p>, <th>, <td>, <app>, <supplementary-material>
        """
        data = {
            #  -*- lang: pt -*-
            'pt_disp_id': 'e01',
            'pt_graphic_href': '1234-5678-rctb-45-05-0110-e01.tif',
            #  -*- lang: en -*-
            'en_disp_id': 'e02',
            'en_graphic_href': '1234-5678-rctb-45-05-0110-e02.tif',
        }
        sample = u"""<?xml version="1.0" encoding="UTF-8"?>
                <!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "JATS-journalpublishing1.dtd">
                <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" dtd-version="1.0" article-type="review-article" xml:lang="pt">
                    <back>
                        <app-group>
                            <app id="app01">
                                <disp-formula id="{pt_disp_id}">
                                    <graphic xlink:href="{pt_graphic_href}" />
                                </disp-formula>
                            </app>
                        </app-group>
                    </back>
                    <sub-article xml:lang="en" article-type="translation" id="S01">
                        <back>
                            <app-group>
                                <app id="app01">
                                    <disp-formula id="{en_disp_id}">
                                        <graphic xlink:href="{en_graphic_href}" />
                                    </disp-formula>
                                </app>
                            </app-group>
                        </back>
                    </sub-article>
                </article>
                """.format(**data)
        fp = io.BytesIO(sample.encode('utf-8'))
        et = etree.parse(fp)
        for lang, html_output in domain.HTMLGenerator(et, valid_only=False):
            formula_id = data['%s_disp_id' % lang]
            formulas = html_output.xpath('//div[@class="app-content"]/div[@class="disp-formula %s"]' % formula_id)
            self.assertEqual(1, len(formulas))

            formula_link = formulas[0].xpath('a')
            self.assertEqual(1, len(formula_link))

            graphic_img = formula_link[0].xpath('img')
            self.assertEqual(1, len(graphic_img))

            self.assertIn(data['%s_graphic_href' % lang], formula_link[0].attrib['href'])
            self.assertIn(data['%s_graphic_href' % lang], graphic_img[0].attrib['src'])

    def test_disp_formula_with_graphic_tag_inside_supplementary_material_tag(self):
        """
        verifica que o tag <disp-formula> (contendo <graphic>), dentro de <supplementary-material> seja correto no html.
        - - -
        <disp-formula> aparece em <body>, <p>, <th>, <td>, <app>, <supplementary-material>
        """
        data = {
            #  -*- lang: pt -*-
            'pt_disp_id': 'e01',
            'pt_graphic_href': '1234-5678-rctb-45-05-0110-e01.tif',
            #  -*- lang: en -*-
            'en_disp_id': 'e02',
            'en_graphic_href': '1234-5678-rctb-45-05-0110-e02.tif',
        }
        sample = u"""<?xml version="1.0" encoding="UTF-8"?>
                <!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "JATS-journalpublishing1.dtd">
                <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" dtd-version="1.0" article-type="review-article" xml:lang="pt">
                    <body>
                        <sec sec-type="supplementary-material">
                            <title>Material Supplementario</title>
                            <supplementary-material id="S1">
                                <disp-formula id="{pt_disp_id}">
                                    <graphic xlink:href="{pt_graphic_href}" />
                                </disp-formula>
                            </supplementary-material>
                        </sec>
                    </body>
                    <sub-article xml:lang="en" article-type="translation" id="S01">
                        <body>
                            <sec sec-type="supplementary-material">
                                <title>Material Supplementario</title>
                                <supplementary-material id="S1">
                                    <disp-formula id="{en_disp_id}">
                                        <graphic xlink:href="{en_graphic_href}" />
                                    </disp-formula>
                                </supplementary-material>
                            </sec>
                        </body>
                    </sub-article>
                </article>
                """.format(**data)
        fp = io.BytesIO(sample.encode('utf-8'))
        et = etree.parse(fp)
        for lang, html_output in domain.HTMLGenerator(et, valid_only=False):
            formula_id = data['%s_disp_id' % lang]

            formulas = html_output.xpath('//article[@class="body-wrapper"]/section[@class="supplementary-material"]/div[@class="supplementary-material"]/div[@class="disp-formula %s"]' % formula_id)
            self.assertEqual(1, len(formulas))

            formula_link = formulas[0].xpath('a')
            self.assertEqual(1, len(formula_link))

            graphic_img = formula_link[0].xpath('img')
            self.assertEqual(1, len(graphic_img))

            self.assertIn(data['%s_graphic_href' % lang], formula_link[0].attrib['href'])
            self.assertIn(data['%s_graphic_href' % lang], graphic_img[0].attrib['src'])

    """ <INLINE-GRAPHIC> """
    @unittest.skip('tag product não é exibida por enquanto')
    def test_inline_graphic_tag_inside_product_tag(self):
        """
        verifica que o tag <inline-graphic>, dentro de <product> seja correto no html.
        - - -
        <inline-graphic> aparece em <product>, <body>, <p>, <sec>, th, td
        """
        data = {
            'pt_inline_href': '1234-5678-rctb-45-05-0110-e01.tif',
            'en_inline_href': '1234-5678-rctb-45-05-0110-e02.tif',
        }
        sample = u"""<?xml version="1.0" encoding="UTF-8"?>
                    <!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "JATS-journalpublishing1.dtd">
                    <article xmlns:xlink="http://www.w3.org/1999/xlink" dtd-version="1.0" article-type="review-article" xml:lang="pt">
                        <front>
                            <article-meta>
                                <product product-type="other">
                                    <inline-graphic xlink:href="{pt_inline_href}"/>
                                </product>
                            </article-meta>
                        </front>
                        <sub-article article-type="translation" id="TRen" xml:lang="en">
                            <front-stub>
                                <article-meta>
                                    <product product-type="other">
                                        <inline-graphic xlink:href="{en_inline_href}"/>
                                    </product>
                                </article-meta>
                            </front-stub>
                        </sub-article>
                    </article>
                 """.format(**data)
        fp = io.BytesIO(sample.encode('utf-8'))
        et = etree.parse(fp)
        for lang, html_output in domain.HTMLGenerator(et, valid_only=False):
            products = html_output.xpath('//div[@class="product other"]')
            self.assertEqual(1, len(products))

            graphic = products[0].xpath('//span[@class="inline-graphic"]')
            self.assertEqual(1, len(graphic))

            link = graphic[0].xpath('a')
            self.assertEqual(1, len(link))

            graphic_img = link[0].xpath('img')
            self.assertEqual(1, len(graphic_img))

            self.assertIn(data['%s_inline_href' % lang], link[0].attrib['href'])
            self.assertIn(data['%s_inline_href' % lang], graphic_img[0].attrib['src'])

    def test_inline_graphic_tag_inside_body_tag(self):
        """
        verifica que o tag <inline-graphic>, dentro de <body> seja correto no html.
        - - -
        <inline-graphic> aparece em <product>, <body>, <p>, <sec>, th, td
        """
        data = {
            'pt_inline_href': '1234-5678-rctb-45-05-0110-e01.tif',
            'en_inline_href': '1234-5678-rctb-45-05-0110-e02.tif',
        }
        sample = u"""<?xml version="1.0" encoding="UTF-8"?>
                    <!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "JATS-journalpublishing1.dtd">
                    <article xmlns:xlink="http://www.w3.org/1999/xlink" dtd-version="1.0" article-type="review-article" xml:lang="pt">
                        <body>
                            <inline-graphic xlink:href="{pt_inline_href}"/>
                        </body>
                        <sub-article xml:lang="en" article-type="translation" id="S01">
                            <body>
                                <inline-graphic xlink:href="{en_inline_href}"/>
                            </body>
                        </sub-article>
                    </article>
                 """.format(**data)
        fp = io.BytesIO(sample.encode('utf-8'))
        et = etree.parse(fp)
        for lang, html_output in domain.HTMLGenerator(et, valid_only=False):
            body = html_output.xpath('//article[@class="body-wrapper"]')
            self.assertEqual(1, len(body))

            graphic = body[0].xpath('//span[@class="inline-graphic"]')
            self.assertEqual(1, len(graphic))

            link = graphic[0].xpath('a')
            self.assertEqual(1, len(link))

            graphic_img = link[0].xpath('img')
            self.assertEqual(1, len(graphic_img))

            self.assertIn(data['%s_inline_href' % lang], link[0].attrib['href'])
            self.assertIn(data['%s_inline_href' % lang], graphic_img[0].attrib['src'])

    def test_inline_graphic_tag_inside_p_tag(self):
        """
        verifica que o tag <inline-graphic>, dentro de <p> seja correto no html.
        - - -
        <inline-graphic> aparece em <product>, <body>, <p>, <sec>, th, td
        """
        data = {
            'pt_inline_href': '1234-5678-rctb-45-05-0110-e01.tif',
            'en_inline_href': '1234-5678-rctb-45-05-0110-e02.tif',
        }
        sample = u"""<?xml version="1.0" encoding="UTF-8"?>
                    <!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "JATS-journalpublishing1.dtd">
                    <article xmlns:xlink="http://www.w3.org/1999/xlink" dtd-version="1.0" article-type="review-article" xml:lang="pt">
                        <body>
                            <p>
                                <inline-graphic xlink:href="{pt_inline_href}"/>
                            </p>
                        </body>
                        <sub-article xml:lang="en" article-type="translation" id="S01">
                            <body>
                                <p>
                                    <inline-graphic xlink:href="{en_inline_href}"/>
                                </p>
                            </body>
                        </sub-article>
                    </article>
                 """.format(**data)
        fp = io.BytesIO(sample.encode('utf-8'))
        et = etree.parse(fp)
        for lang, html_output in domain.HTMLGenerator(et, valid_only=False):
            body = html_output.xpath('//article[@class="body-wrapper"]')
            self.assertEqual(1, len(body))

            graphic = body[0].xpath('p/span[@class="inline-graphic"]')
            self.assertEqual(1, len(graphic))

            link = graphic[0].xpath('a')
            self.assertEqual(1, len(link))

            graphic_img = link[0].xpath('img')
            self.assertEqual(1, len(graphic_img))

            self.assertIn(data['%s_inline_href' % lang], link[0].attrib['href'])
            self.assertIn(data['%s_inline_href' % lang], graphic_img[0].attrib['src'])

    def test_inline_graphic_tag_inside_sec_tag(self):
        """
        verifica que o tag <inline-graphic>, dentro de <sec> seja correto no html.
        - - -
        <inline-graphic> aparece em <product>, <body>, <p>, <sec>, th, td
        """
        data = {
            'pt_inline_href': '1234-5678-rctb-45-05-0110-e01.tif',
            'en_inline_href': '1234-5678-rctb-45-05-0110-e02.tif',
        }
        sample = u"""<?xml version="1.0" encoding="UTF-8"?>
                    <!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "JATS-journalpublishing1.dtd">
                    <article xmlns:xlink="http://www.w3.org/1999/xlink" dtd-version="1.0" article-type="review-article" xml:lang="pt">
                        <body>
                            <sec sec-type="intro">
                                <inline-graphic xlink:href="{pt_inline_href}"/>
                            </sec>
                        </body>
                        <sub-article xml:lang="en" article-type="translation" id="S01">
                            <body>
                                <sec sec-type="intro">
                                    <inline-graphic xlink:href="{en_inline_href}"/>
                                </sec>
                            </body>
                        </sub-article>
                    </article>
                 """.format(**data)
        fp = io.BytesIO(sample.encode('utf-8'))
        et = etree.parse(fp)
        for lang, html_output in domain.HTMLGenerator(et, valid_only=False):
            body = html_output.xpath('//article[@class="body-wrapper"]')
            self.assertEqual(1, len(body))

            graphic = body[0].xpath('section[@class="intro"]/span[@class="inline-graphic"]')
            self.assertEqual(1, len(graphic))

            link = graphic[0].xpath('a')
            self.assertEqual(1, len(link))

            graphic_img = link[0].xpath('img')
            self.assertEqual(1, len(graphic_img))

            self.assertIn(data['%s_inline_href' % lang], link[0].attrib['href'])
            self.assertIn(data['%s_inline_href' % lang], graphic_img[0].attrib['src'])

    def test_inline_graphic_tag_inside_th_tag(self):
        """
        verifica que o tag <inline-graphic>, dentro de <th> seja correto no html.
        - - -
        <inline-graphic> aparece em <product>, <body>, <p>, <sec>, th, td
        """
        data = {
            'pt_inline_href': '1234-5678-rctb-45-05-0110-e01.tif',
            'en_inline_href': '1234-5678-rctb-45-05-0110-e02.tif',
        }
        sample = u"""<?xml version="1.0" encoding="UTF-8"?>
                    <!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "JATS-journalpublishing1.dtd">
                    <article xmlns:xlink="http://www.w3.org/1999/xlink" dtd-version="1.0" article-type="review-article" xml:lang="pt">
                        <body>
                            <p>
                                <table-wrap id="t01">
                                    <table>
                                        <thead>
                                            <tr>
                                                <th>
                                                    <inline-graphic xlink:href="{pt_inline_href}"/>
                                                </th>
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
                        </body>
                        <sub-article xml:lang="en" article-type="translation" id="S01">
                            <body>
                                <p>
                                    <table-wrap id="t01">
                                        <table>
                                            <thead>
                                                <tr>
                                                    <th>
                                                        <inline-graphic xlink:href="{en_inline_href}"/>
                                                    </th>
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
                            </body>
                        </sub-article>
                    </article>
                 """.format(**data)
        fp = io.BytesIO(sample.encode('utf-8'))
        et = etree.parse(fp)
        for lang, html_output in domain.HTMLGenerator(et, valid_only=False):
            table = html_output.xpath('//article[@class="body-wrapper"]//table[@class="table"]')
            self.assertEqual(1, len(table))

            graphic = table[0].xpath('thead/tr/th/span[@class="inline-graphic"]')
            self.assertEqual(1, len(graphic))

            link = graphic[0].xpath('a')
            self.assertEqual(1, len(link))

            graphic_img = link[0].xpath('img')
            self.assertEqual(1, len(graphic_img))

            self.assertIn(data['%s_inline_href' % lang], link[0].attrib['href'])
            self.assertIn(data['%s_inline_href' % lang], graphic_img[0].attrib['src'])

    def test_inline_graphic_tag_inside_td_tag(self):
        """
        verifica que o tag <inline-graphic>, dentro de <td> seja correto no html.
        - - -
        <inline-graphic> aparece em <product>, <body>, <p>, <sec>, th, td
        """
        data = {
            'pt_inline_href': '1234-5678-rctb-45-05-0110-e01.tif',
            'en_inline_href': '1234-5678-rctb-45-05-0110-e02.tif',
        }
        sample = u"""<?xml version="1.0" encoding="UTF-8"?>
                    <!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "JATS-journalpublishing1.dtd">
                    <article xmlns:xlink="http://www.w3.org/1999/xlink" dtd-version="1.0" article-type="review-article" xml:lang="pt">
                        <body>
                            <p>
                                <table-wrap id="t01">
                                    <table>
                                        <thead>
                                            <tr>
                                                <th>FOO</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            <tr>
                                                <td>
                                                    <inline-graphic xlink:href="{pt_inline_href}"/>
                                                </td>
                                            </tr>
                                        </tbody>
                                    </table>
                                </table-wrap>
                            </p>
                        </body>
                        <sub-article xml:lang="en" article-type="translation" id="S01">
                            <body>
                                <p>
                                    <table-wrap id="t01">
                                        <table>
                                            <thead>
                                                <tr>
                                                    <th>BAR</th>
                                                </tr>
                                            </thead>
                                            <tbody>
                                                <tr>
                                                    <td>
                                                        <inline-graphic xlink:href="{en_inline_href}"/>
                                                    </td>
                                                </tr>
                                            </tbody>
                                        </table>
                                    </table-wrap>
                                </p>
                            </body>
                        </sub-article>
                    </article>
                 """.format(**data)
        fp = io.BytesIO(sample.encode('utf-8'))
        et = etree.parse(fp)
        for lang, html_output in domain.HTMLGenerator(et, valid_only=False):
            table = html_output.xpath('//article[@class="body-wrapper"]//table[@class="table"]')
            self.assertEqual(1, len(table))

            graphic = table[0].xpath('tbody/tr/td/span[@class="inline-graphic"]')
            self.assertEqual(1, len(graphic))

            link = graphic[0].xpath('a')
            self.assertEqual(1, len(link))

            graphic_img = link[0].xpath('img')
            self.assertEqual(1, len(graphic_img))

            self.assertIn(data['%s_inline_href' % lang], link[0].attrib['href'])
            self.assertIn(data['%s_inline_href' % lang], graphic_img[0].attrib['src'])

    """ <TABLE-WRAP> """
    @unittest.skip('tag app/app-group não é exibida por enquanto')
    def test_table_wrap_tag_inside_app_tag(self):
        """
        verifica que o tag <table-wrap>, dentro de <app> seja correto no html.
        - - -
        <table-wrap> aparece em <app>, <app-group>, <body>, Glossário, <p>, <sec>, <supplementary-material>
        """
        data = {
            #  -*- lang: pt -*-
            'pt_label': 'label PT',
            'pt_caption': 'caption PT',
            'pt_th': 'table header PT',
            'pt_td': 'table data PT',
            'pt_foot': 'table foot PT',
            #  -*- lang: en -*-
            'en_label': 'label EN',
            'en_caption': 'caption EN',
            'en_th': 'table header EN',
            'en_td': 'table data EN',
            'en_foot': 'table foot EN',
        }
        sample = u"""<?xml version="1.0" encoding="UTF-8"?>
                    <!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "JATS-journalpublishing1.dtd">
                    <article xmlns:xlink="http://www.w3.org/1999/xlink" xml:lang="pt">
                        <back>
                            <app-group>
                                <app id="app01">
                                    <table-wrap id="t01">
                                        <label>{pt_label}</label>
                                        <caption>
                                            <title>{pt_caption}</title>
                                        </caption>
                                        <table>
                                            <thead>
                                                <tr><th>{pt_th}</th></tr>
                                            </thead>
                                            <tbody>
                                                <tr><td>{pt_td}</td></tr>
                                            </tbody>
                                        </table>
                                        <table-wrap-foot>
                                            {pt_foot}
                                        </table-wrap-foot>
                                    </table-wrap>
                                </app>
                            </app-group>
                        </back>
                        <sub-article article-type="translation" id="TRen" xml:lang="en">
                            <back>
                                <app-group>
                                    <app id="app01">
                                        <table-wrap id="t01">
                                            <label>{en_label}</label>
                                            <caption>
                                                <title>{en_caption}</title>
                                            </caption>
                                            <table>
                                                <thead>
                                                    <tr><th>{en_th}</th></tr>
                                                </thead>
                                                <tbody>
                                                    <tr><td>{en_td}</td></tr>
                                                </tbody>
                                            </table>
                                            <table-wrap-foot>
                                                {en_foot}
                                            </table-wrap-foot>
                                        </table-wrap>
                                    </app>
                                </app-group>
                            </back>
                        </sub-article>
                    </article>
                """.format(**data)
        fp = io.BytesIO(sample.encode('utf-8'))
        et = etree.parse(fp)
        for lang, html_output in domain.HTMLGenerator(et, valid_only=False):
            app_content = html_output.xpath('//div[@class="app-group"]/div[@class="app"]/div[@class="app-content"]')
            self.assertEqual(1, len(app_content))

            table = app_content[0].xpath('table')
            self.assertEqual(1, len(table))

            caption = app_content[0].xpath('span[@class="label_caption"]/caption')
            self.assertEqual(1, len(caption))

            label = app_content[0].xpath('span[@class="label_caption"]/label[@for="t01"]')
            self.assertEqual(1, len(label))

            table_header = table[0].xpath('thead/tr/th')
            self.assertEqual(1, len(table_header))

            table_cell = table[0].xpath('tbody/tr/td')
            self.assertEqual(1, len(table_cell))

            table_wrap_footer = app_content[0].xpath('div[@class="table-wrap-foot"]')
            self.assertEqual(1, len(table_wrap_footer))

            # then:
            self.assertEqual(data['%s_label' % lang], label[0].text.strip())
            self.assertEqual(data['%s_caption' % lang], caption[0].text.strip())
            self.assertEqual(data['%s_th' % lang], table_header[0].text.strip())
            self.assertEqual(data['%s_td' % lang], table_cell[0].text.strip())
            self.assertEqual(data['%s_foot' % lang], table_wrap_footer[0].text.strip())

    @unittest.skip('tag app/app-group não é exibida por enquanto')
    def test_table_wrap_tag_inside_app_group_tag(self):
        """
        verifica que o tag <table-wrap>, dentro de <app-group> seja correto no html.
        - - -
        <table-wrap> aparece em <app>, <app-group>, <body>, Glossário, <p>, <sec>, <supplementary-material>
        """
        data = {
            #  -*- lang: pt -*-
            'pt_label': 'label PT',
            'pt_caption': 'caption PT',
            'pt_th': 'table header PT',
            'pt_td': 'table data PT',
            'pt_foot': 'table foot PT',
            #  -*- lang: en -*-
            'en_label': 'label EN',
            'en_caption': 'caption EN',
            'en_th': 'table header EN',
            'en_td': 'table data EN',
            'en_foot': 'table foot EN',
        }
        sample = u"""<?xml version="1.0" encoding="UTF-8"?>
                    <!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "JATS-journalpublishing1.dtd">
                    <article xmlns:xlink="http://www.w3.org/1999/xlink" xml:lang="pt">
                        <back>
                            <app-group>
                                <table-wrap id="t01">
                                    <label>{pt_label}</label>
                                    <caption>
                                        <title>{pt_caption}</title>
                                    </caption>
                                    <table>
                                        <thead>
                                            <tr><th>{pt_th}</th></tr>
                                        </thead>
                                        <tbody>
                                            <tr><td>{pt_td}</td></tr>
                                        </tbody>
                                    </table>
                                    <table-wrap-foot>
                                        {pt_foot}
                                    </table-wrap-foot>
                                </table-wrap>
                            </app-group>
                        </back>
                        <sub-article article-type="translation" id="TRen" xml:lang="en">
                            <back>
                                <app-group>
                                    <table-wrap id="t01">
                                        <label>{en_label}</label>
                                        <caption>
                                            <title>{en_caption}</title>
                                        </caption>
                                        <table>
                                            <thead>
                                                <tr><th>{en_th}</th></tr>
                                            </thead>
                                            <tbody>
                                                <tr><td>{en_td}</td></tr>
                                            </tbody>
                                        </table>
                                        <table-wrap-foot>
                                            {en_foot}
                                        </table-wrap-foot>
                                    </table-wrap>
                                </app-group>
                            </back>
                        </sub-article>
                    </article>
                """.format(**data)
        fp = io.BytesIO(sample.encode('utf-8'))
        et = etree.parse(fp)
        for lang, html_output in domain.HTMLGenerator(et, valid_only=False):
            app_content = html_output.xpath('//div[@class="app-group"]')
            self.assertEqual(1, len(app_content))

            table = app_content[0].xpath('table')
            self.assertEqual(1, len(table))

            caption = app_content[0].xpath('span[@class="label_caption"]/caption')
            self.assertEqual(1, len(caption))

            label = app_content[0].xpath('span[@class="label_caption"]/label[@for="t01"]')
            self.assertEqual(1, len(label))

            table_header = table[0].xpath('thead/tr/th')
            self.assertEqual(1, len(table_header))

            table_cell = table[0].xpath('tbody/tr/td')
            self.assertEqual(1, len(table_cell))

            table_wrap_footer = app_content[0].xpath('div[@class="table-wrap-foot"]')
            self.assertEqual(1, len(table_wrap_footer))

            # then:
            self.assertEqual(data['%s_label' % lang], label[0].text.strip())
            self.assertEqual(data['%s_caption' % lang], caption[0].text.strip())
            self.assertEqual(data['%s_th' % lang], table_header[0].text.strip())
            self.assertEqual(data['%s_td' % lang], table_cell[0].text.strip())
            self.assertEqual(data['%s_foot' % lang], table_wrap_footer[0].text.strip())

    def test_table_wrap_tag_inside_body_tag(self):
        """
        verifica que o tag <table-wrap>, dentro de <body> seja correto no html.
        - - -
        <table-wrap> aparece em <app>, <app-group>, <body>, Glossário, <p>, <sec>, <supplementary-material>
        """
        data = {
            #  -*- lang: pt -*-
            'pt_label': 'label PT',
            'pt_caption': 'caption PT',
            'pt_th': 'table header PT',
            'pt_td': 'table data PT',
            'pt_foot': 'table foot PT',
            #  -*- lang: en -*-
            'en_label': 'label EN',
            'en_caption': 'caption EN',
            'en_th': 'table header EN',
            'en_td': 'table data EN',
            'en_foot': 'table foot EN',
        }
        sample = u"""<?xml version="1.0" encoding="UTF-8"?>
                    <!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "JATS-journalpublishing1.dtd">
                    <article xmlns:xlink="http://www.w3.org/1999/xlink" xml:lang="pt">
                        <body>
                            <table-wrap id="t01">
                                <label>{pt_label}</label>
                                <caption>
                                    <title>{pt_caption}</title>
                                </caption>
                                <table>
                                    <thead>
                                        <tr><th>{pt_th}</th></tr>
                                    </thead>
                                    <tbody>
                                        <tr><td>{pt_td}</td></tr>
                                    </tbody>
                                </table>
                                <table-wrap-foot>
                                    {pt_foot}
                                </table-wrap-foot>
                            </table-wrap>
                        </body>
                        <sub-article article-type="translation" id="TRen" xml:lang="en">
                            <body>
                                <table-wrap id="t01">
                                    <label>{en_label}</label>
                                    <caption>
                                        <title>{en_caption}</title>
                                    </caption>
                                    <table>
                                        <thead>
                                            <tr><th>{en_th}</th></tr>
                                        </thead>
                                        <tbody>
                                            <tr><td>{en_td}</td></tr>
                                        </tbody>
                                    </table>
                                    <table-wrap-foot>
                                        {en_foot}
                                    </table-wrap-foot>
                                </table-wrap>
                            </body>
                        </sub-article>
                    </article>
                """.format(**data)
        fp = io.BytesIO(sample.encode('utf-8'))
        et = etree.parse(fp)
        for lang, html_output in domain.HTMLGenerator(et, valid_only=False):
            body = html_output.xpath('//article[@class="body-wrapper"]')
            self.assertEqual(1, len(body))

            table = body[0].xpath('//table')
            self.assertEqual(1, len(table))

            caption = body[0].xpath('//span[@class="label_caption"]/caption')
            self.assertEqual(1, len(caption))

            label = body[0].xpath('//span[@class="label_caption"]/label[@for="t01"]')
            self.assertEqual(1, len(label))

            table_header = table[0].xpath('thead/tr/th')
            self.assertEqual(1, len(table_header))

            table_cell = table[0].xpath('tbody/tr/td')
            self.assertEqual(1, len(table_cell))

            table_wrap_footer = body[0].xpath('//div[@class="table-wrap-foot"]')
            self.assertEqual(1, len(table_wrap_footer))

            # then:
            self.assertEqual(data['%s_label' % lang], label[0].text.strip())
            self.assertEqual(data['%s_caption' % lang], caption[0].text.strip())
            self.assertEqual(data['%s_th' % lang], table_header[0].text.strip())
            self.assertEqual(data['%s_td' % lang], table_cell[0].text.strip())
            self.assertEqual(data['%s_foot' % lang], table_wrap_footer[0].text.strip())

    @unittest.skip('tag glossary não é exibida por enquanto')
    def test_table_wrap_tag_inside_glossary_tag(self):
        """
        verifica que o tag <table-wrap>, dentro de <glossary> seja correto no html.
        - - -
        <table-wrap> aparece em <app>, <app-group>, <body>, Glossário, <p>, <sec>, <supplementary-material>
        """
        data = {
            #  -*- lang: pt -*-
            'pt_label': 'label PT',
            'pt_caption': 'caption PT',
            'pt_th': 'table header PT',
            'pt_td': 'table data PT',
            'pt_foot': 'table foot PT',
            #  -*- lang: en -*-
            'en_label': 'label EN',
            'en_caption': 'caption EN',
            'en_th': 'table header EN',
            'en_td': 'table data EN',
            'en_foot': 'table foot EN',
        }
        sample = u"""<?xml version="1.0" encoding="UTF-8"?>
                    <!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "JATS-journalpublishing1.dtd">
                    <article xmlns:xlink="http://www.w3.org/1999/xlink" xml:lang="pt">
                        <back>
                            <glossary id="gloss01">
                                <table-wrap id="t01">
                                    <label>{pt_label}</label>
                                    <caption>
                                        <title>{pt_caption}</title>
                                    </caption>
                                    <table>
                                        <thead>
                                            <tr><th>{pt_th}</th></tr>
                                        </thead>
                                        <tbody>
                                            <tr><td>{pt_td}</td></tr>
                                        </tbody>
                                    </table>
                                    <table-wrap-foot>
                                        {pt_foot}
                                    </table-wrap-foot>
                                </table-wrap>
                            </glossary>
                        </back>
                        <sub-article article-type="translation" id="TRen" xml:lang="en">
                            <back>
                                <glossary id="gloss01">
                                    <table-wrap id="t01">
                                        <label>{en_label}</label>
                                        <caption>
                                            <title>{en_caption}</title>
                                        </caption>
                                        <table>
                                            <thead>
                                                <tr><th>{en_th}</th></tr>
                                            </thead>
                                            <tbody>
                                                <tr><td>{en_td}</td></tr>
                                            </tbody>
                                        </table>
                                        <table-wrap-foot>
                                            {en_foot}
                                        </table-wrap-foot>
                                    </table-wrap>
                                </glossary>
                            </back>
                        </sub-article>
                    </article>
                """.format(**data)
        fp = io.BytesIO(sample.encode('utf-8'))
        et = etree.parse(fp)
        for lang, html_output in domain.HTMLGenerator(et, valid_only=False):
            glossary = html_output.xpath('//div[@class="glossary"]')
            self.assertEqual(1, len(glossary))

            table = glossary[0].xpath('//table')
            self.assertEqual(1, len(table))

            caption = glossary[0].xpath('//span[@class="label_caption"]/caption')
            self.assertEqual(1, len(caption))

            label = glossary[0].xpath('//span[@class="label_caption"]/label[@for="t01"]')
            self.assertEqual(1, len(label))

            table_header = table[0].xpath('thead/tr/th')
            self.assertEqual(1, len(table_header))

            table_cell = table[0].xpath('tbody/tr/td')
            self.assertEqual(1, len(table_cell))

            table_wrap_footer = glossary[0].xpath('//div[@class="table-wrap-foot"]')
            self.assertEqual(1, len(table_wrap_footer))

            # then:
            self.assertEqual(data['%s_label' % lang], label[0].text.strip())
            self.assertEqual(data['%s_caption' % lang], caption[0].text.strip())
            self.assertEqual(data['%s_th' % lang], table_header[0].text.strip())
            self.assertEqual(data['%s_td' % lang], table_cell[0].text.strip())
            self.assertEqual(data['%s_foot' % lang], table_wrap_footer[0].text.strip())

    def test_table_wrap_tag_inside_p_tag(self):
        """
        verifica que o tag <table-wrap>, dentro de <p> seja correto no html.
        - - -
        <table-wrap> aparece em <app>, <app-group>, <body>, Glossário, <p>, <sec>, <supplementary-material>
        """
        data = {
            #  -*- lang: pt -*-
            'pt_label': 'label PT',
            'pt_caption': 'caption PT',
            'pt_th': 'table header PT',
            'pt_td': 'table data PT',
            'pt_foot': 'table foot PT',
            #  -*- lang: en -*-
            'en_label': 'label EN',
            'en_caption': 'caption EN',
            'en_th': 'table header EN',
            'en_td': 'table data EN',
            'en_foot': 'table foot EN',
        }
        sample = u"""<?xml version="1.0" encoding="UTF-8"?>
                    <!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "JATS-journalpublishing1.dtd">
                    <article xmlns:xlink="http://www.w3.org/1999/xlink" xml:lang="pt">
                        <body>
                            <sec sec-type="intro">
                                <p>
                                    <table-wrap id="t01">
                                        <label>{pt_label}</label>
                                        <caption>
                                            <title>{pt_caption}</title>
                                        </caption>
                                        <table>
                                            <thead>
                                                <tr><th>{pt_th}</th></tr>
                                            </thead>
                                            <tbody>
                                                <tr><td>{pt_td}</td></tr>
                                            </tbody>
                                        </table>
                                        <table-wrap-foot>
                                            {pt_foot}
                                        </table-wrap-foot>
                                    </table-wrap>
                                </p>
                            </sec>
                        </body>
                        <sub-article article-type="translation" id="TRen" xml:lang="en">
                            <body>
                                <sec sec-type="intro">
                                    <p>
                                        <table-wrap id="t01">
                                            <label>{en_label}</label>
                                            <caption>
                                                <title>{en_caption}</title>
                                            </caption>
                                            <table>
                                                <thead>
                                                    <tr><th>{en_th}</th></tr>
                                                </thead>
                                                <tbody>
                                                    <tr><td>{en_td}</td></tr>
                                                </tbody>
                                            </table>
                                            <table-wrap-foot>
                                                {en_foot}
                                            </table-wrap-foot>
                                        </table-wrap>
                                    </p>
                                </sec>
                            </body>
                        </sub-article>
                    </article>
                """.format(**data)
        fp = io.BytesIO(sample.encode('utf-8'))
        et = etree.parse(fp)
        for lang, html_output in domain.HTMLGenerator(et, valid_only=False):
            paragraph = html_output.xpath('//article[@class="body-wrapper"]/section[@class="intro"]/p')
            self.assertEqual(1, len(paragraph))

            table = paragraph[0].xpath('table')
            self.assertEqual(1, len(table))

            caption = paragraph[0].xpath('span[@class="label_caption"]/caption')
            self.assertEqual(1, len(caption))

            label = paragraph[0].xpath('span[@class="label_caption"]/label[@for="t01"]')
            self.assertEqual(1, len(label))

            table_header = table[0].xpath('thead/tr/th')
            self.assertEqual(1, len(table_header))

            table_cell = table[0].xpath('tbody/tr/td')
            self.assertEqual(1, len(table_cell))

            table_wrap_footer = paragraph[0].xpath('div[@class="table-wrap-foot"]')
            self.assertEqual(1, len(table_wrap_footer))

            # then:
            self.assertEqual(data['%s_label' % lang], label[0].text.strip())
            self.assertEqual(data['%s_caption' % lang], caption[0].text.strip())
            self.assertEqual(data['%s_th' % lang], table_header[0].text.strip())
            self.assertEqual(data['%s_td' % lang], table_cell[0].text.strip())
            self.assertEqual(data['%s_foot' % lang], table_wrap_footer[0].text.strip())

    def test_table_wrap_tag_inside_sec_tag(self):
        """
        verifica que o tag <table-wrap>, dentro de <sec> seja correto no html.
        - - -
        <table-wrap> aparece em <app>, <app-group>, <body>, Glossário, <p>, <sec>, <supplementary-material>
        """
        data = {
            #  -*- lang: pt -*-
            'pt_label': 'label PT',
            'pt_caption': 'caption PT',
            'pt_th': 'table header PT',
            'pt_td': 'table data PT',
            'pt_foot': 'table foot PT',
            #  -*- lang: en -*-
            'en_label': 'label EN',
            'en_caption': 'caption EN',
            'en_th': 'table header EN',
            'en_td': 'table data EN',
            'en_foot': 'table foot EN',
        }
        sample = u"""<?xml version="1.0" encoding="UTF-8"?>
                    <!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "JATS-journalpublishing1.dtd">
                    <article xmlns:xlink="http://www.w3.org/1999/xlink" xml:lang="pt">
                        <body>
                            <sec sec-type="intro">
                                <table-wrap id="t01">
                                    <label>{pt_label}</label>
                                    <caption>
                                        <title>{pt_caption}</title>
                                    </caption>
                                    <table>
                                        <thead>
                                            <tr><th>{pt_th}</th></tr>
                                        </thead>
                                        <tbody>
                                            <tr><td>{pt_td}</td></tr>
                                        </tbody>
                                    </table>
                                    <table-wrap-foot>
                                        {pt_foot}
                                    </table-wrap-foot>
                                </table-wrap>
                            </sec>
                        </body>
                        <sub-article article-type="translation" id="TRen" xml:lang="en">
                            <body>
                                <sec sec-type="intro">
                                    <table-wrap id="t01">
                                        <label>{en_label}</label>
                                        <caption>
                                            <title>{en_caption}</title>
                                        </caption>
                                        <table>
                                            <thead>
                                                <tr><th>{en_th}</th></tr>
                                            </thead>
                                            <tbody>
                                                <tr><td>{en_td}</td></tr>
                                            </tbody>
                                        </table>
                                        <table-wrap-foot>
                                            {en_foot}
                                        </table-wrap-foot>
                                    </table-wrap>
                                </sec>
                            </body>
                        </sub-article>
                    </article>
                """.format(**data)
        fp = io.BytesIO(sample.encode('utf-8'))
        et = etree.parse(fp)
        for lang, html_output in domain.HTMLGenerator(et, valid_only=False):
            section = html_output.xpath('//article[@class="body-wrapper"]/section[@class="intro"]')
            self.assertEqual(1, len(section))

            table = section[0].xpath('table')
            self.assertEqual(1, len(table))

            caption = section[0].xpath('span[@class="label_caption"]/caption')
            self.assertEqual(1, len(caption))

            label = section[0].xpath('span[@class="label_caption"]/label[@for="t01"]')
            self.assertEqual(1, len(label))

            table_header = table[0].xpath('thead/tr/th')
            self.assertEqual(1, len(table_header))

            table_cell = table[0].xpath('tbody/tr/td')
            self.assertEqual(1, len(table_cell))

            table_wrap_footer = section[0].xpath('div[@class="table-wrap-foot"]')
            self.assertEqual(1, len(table_wrap_footer))

            # then:
            self.assertEqual(data['%s_label' % lang], label[0].text.strip())
            self.assertEqual(data['%s_caption' % lang], caption[0].text.strip())
            self.assertEqual(data['%s_th' % lang], table_header[0].text.strip())
            self.assertEqual(data['%s_td' % lang], table_cell[0].text.strip())
            self.assertEqual(data['%s_foot' % lang], table_wrap_footer[0].text.strip())

    def test_table_wrap_tag_inside_supplementary_material_tag(self):
        """
        verifica que o tag <table-wrap>, dentro de <supplementary-material> seja correto no html.
        - - -
        <table-wrap> aparece em <app>, <app-group>, <body>, Glossário, <p>, <sec>, <supplementary-material>
        """
        data = {
            #  -*- lang: pt -*-
            'pt_label': 'label PT',
            'pt_caption': 'caption PT',
            'pt_th': 'table header PT',
            'pt_td': 'table data PT',
            'pt_foot': 'table foot PT',
            #  -*- lang: en -*-
            'en_label': 'label EN',
            'en_caption': 'caption EN',
            'en_th': 'table header EN',
            'en_td': 'table data EN',
            'en_foot': 'table foot EN',
        }
        sample = u"""<?xml version="1.0" encoding="UTF-8"?>
                    <!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "JATS-journalpublishing1.dtd">
                    <article xmlns:xlink="http://www.w3.org/1999/xlink" xml:lang="pt">
                        <body>
                            <sec sec-type="supplementary-material">
                                <p>
                                    <supplementary-material id="suppl01">
                                        <table-wrap id="t01">
                                            <label>{pt_label}</label>
                                            <caption>
                                                <title>{pt_caption}</title>
                                            </caption>
                                            <table>
                                                <thead>
                                                    <tr><th>{pt_th}</th></tr>
                                                </thead>
                                                <tbody>
                                                    <tr><td>{pt_td}</td></tr>
                                                </tbody>
                                            </table>
                                            <table-wrap-foot>
                                                {pt_foot}
                                            </table-wrap-foot>
                                        </table-wrap>
                                    </supplementary-material>
                                </p>
                            </sec>
                        </body>
                        <sub-article article-type="translation" id="TRen" xml:lang="en">
                            <body>
                                <sec sec-type="supplementary-material">
                                    <p>
                                        <supplementary-material id="suppl01">
                                            <table-wrap id="t01">
                                                <label>{en_label}</label>
                                                <caption>
                                                    <title>{en_caption}</title>
                                                </caption>
                                                <table>
                                                    <thead>
                                                        <tr><th>{en_th}</th></tr>
                                                    </thead>
                                                    <tbody>
                                                        <tr><td>{en_td}</td></tr>
                                                    </tbody>
                                                </table>
                                                <table-wrap-foot>
                                                    {en_foot}
                                                </table-wrap-foot>
                                            </table-wrap>
                                        </supplementary-material>
                                    </p>
                                </sec>
                            </body>
                        </sub-article>
                    </article>
                """.format(**data)
        fp = io.BytesIO(sample.encode('utf-8'))
        et = etree.parse(fp)
        for lang, html_output in domain.HTMLGenerator(et, valid_only=False):
            supplementary = html_output.xpath('//article[@class="body-wrapper"]/section[@class="supplementary-material"]/div[@class="supplementary-material"]')
            self.assertEqual(1, len(supplementary))

            table = supplementary[0].xpath('table')
            self.assertEqual(1, len(table))

            caption = supplementary[0].xpath('span[@class="label_caption"]/caption')
            self.assertEqual(1, len(caption))

            label = supplementary[0].xpath('span[@class="label_caption"]/label[@for="t01"]')
            self.assertEqual(1, len(label))

            table_header = table[0].xpath('thead/tr/th')
            self.assertEqual(1, len(table_header))

            table_cell = table[0].xpath('tbody/tr/td')
            self.assertEqual(1, len(table_cell))

            table_wrap_footer = supplementary[0].xpath('div[@class="table-wrap-foot"]')
            self.assertEqual(1, len(table_wrap_footer))

            # then:
            self.assertEqual(data['%s_label' % lang], label[0].text.strip())
            self.assertEqual(data['%s_caption' % lang], caption[0].text.strip())
            self.assertEqual(data['%s_th' % lang], table_header[0].text.strip())
            self.assertEqual(data['%s_td' % lang], table_cell[0].text.strip())
            self.assertEqual(data['%s_foot' % lang], table_wrap_footer[0].text.strip())
