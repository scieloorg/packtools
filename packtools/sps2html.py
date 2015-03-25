#coding: utf-8
from __future__ import print_function
import os
import argparse
import sys
import logging
import pkg_resources
from lxml import etree
from StringIO import StringIO
import packtools

logger = logging.getLogger(__name__)

XML_NAMESPACE = 'http://www.w3.org/XML/1998/namespace'
HERE = os.path.dirname(os.path.abspath(__file__))
XSLT_TEMPLATE_DIR = os.path.abspath(os.path.join(HERE, 'templates_xslt/'))


class SPS2HTML(object):
    """Parses `file` to produce an etree instance.
    The XML can be retrieved given its filesystem path, an URL or a file-object.
    :param file: Path to the XML file, URL or file-object.
    """
    xml = None
    xml_id = None

    def __init__(self, file):
        parser = etree.XMLParser(remove_blank_text=True)
        self.xml = etree.parse(file, parser)
        self.xml_id = self.xml.getroot().base.split('/')[-1]

    @property
    def xml_translations(self):
        try:
            translations = self.xml.xpath('//sub-article[@article-type="translation"]')
            return [val.get('{%s}lang' % XML_NAMESPACE) for val in translations]
        except IndexError:
            return []

    def generate_xhtml(self, xslt_file_path):
        extra_context = {
            'article_lang': etree.XSLT.strparam(self.article_lang),
            'is_translation': etree.XSLT.strparam('False'),
            'bibliographic_legend': etree.XSLT.strparam(self.bibliographic_legend),
            'article_id': etree.XSLT.strparam(self.xml_id),
        }

        xslt = etree.parse(xslt_file_path)
        transform = etree.XSLT(xslt)
        result = transform(self.xml, **extra_context)

        # save result as xhtml file
        output_filename = '%s.html' % self.xml_id
        with open(output_filename, 'w') as fp:
            fp.write(str(result))
        logging.debug('New HTML file: %s for xml: (%s)' % (output_filename, self.xml_id))

        logging.debug('Found this translation: %s for xml:%s' % (self.xml_translations, self.xml_id))
        for translation_lang in self.xml_translations:
            logging.debug('Initializing translation to %s of xml: %s' % (self.xml_id, translation_lang))
            extra_context['article_lang'] = etree.XSLT.strparam(translation_lang)
            extra_context['is_translation'] = etree.XSLT.strparam('True')
            result = transform(self.xml, **extra_context)
            output_filename = '%s_%s.html' % (self.xml_id, translation_lang)
            with open(output_filename, 'w') as fp:
                fp.write(str(result))
            logging.debug('New translation (lang: %s) HTML (%s) file for xml: (%s)' % (translation_lang, output_filename, self.xml_id))

    @property
    def article_title(self):
        return self.xml.xpath('//article-meta/title-group/article-title')[0].text

    @property
    def article_lang(self):
        value = self.xml.xpath('//article')[0]
        return value.get('{%s}lang' % XML_NAMESPACE)

    @property
    def verbose_identification(self):
        volume = self.xml.xpath('//article/front/article-meta/volume')[0].text
        number = self.xml.xpath('//article/front/article-meta/issue')[0].text
        return 'vol.%s n.%s' % (volume, number)

    @property
    def bibliographic_legend(self):
        abrev_title = self.xml.xpath('//article/front/journal-meta/journal-title-group/abbrev-journal-title')[0].text
        issue = self.verbose_identification
        city = '[CITY?]'
        month = self.xml.xpath('//article-meta/pub-date/month')
        if month:
            dates_month = month[0].text
        else:
            dates_month = ''
        dates_year = self.xml.xpath('//article-meta/pub-date/year')[0].text
        if dates_month:
            dates = "%s %s" % (dates_month, dates_year)
        else:
            dates = dates_year
        return '%s %s %s %s'% (abrev_title, issue, city, dates)


def main():
    packtools_version = pkg_resources.get_distribution('packtools').version

    parser = argparse.ArgumentParser(description='sps2html cli utility')
    parser.add_argument('XML', nargs='+', help='filesystem path or URL to the XML')
    parser.add_argument('--version', action='version', version=packtools_version)
    parser.add_argument('--loglevel', default='WARNING')
    parser.add_argument('--xslt', default='default')
    args = parser.parse_args()

    logging.basicConfig(level=getattr(logging, args.loglevel))

    if args.xslt == 'default':
        xslt_file_path = os.path.abspath(os.path.join(XSLT_TEMPLATE_DIR, 'default.xslt'))
    else:
        xslt_file_path = args.xslt

    print('Please wait, this may take a while...', file=sys.stderr)

    for xml in packtools.utils.flatten(args.XML):
        logger.info('starting validation xml: %s' % xml)

        try:
            xml_obj = SPS2HTML(file=xml)
        except IOError as e:
            logger.debug(e)
        except etree.XMLSyntaxError as e:
            logger.debug(e)
        else:
            xml_obj.generate_xhtml(xslt_file_path)

        logger.info('finished validating xml: %s' % (xml,))


if __name__ == '__main__':
    main()
