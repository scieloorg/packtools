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
