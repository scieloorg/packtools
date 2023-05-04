from lxml import etree as ET
from packtools.sps.models import article_ids, journal_meta

from datetime import datetime, date


def get_identifier(header, xml_tree):
    identifier = article_ids.ArticleIds(xml_tree).v2
    if identifier is None:
        identifier = article_ids.ArticleIds(xml_tree).without_specific_use
    if identifier is not None:
        el = ET.Element('identifier')
        el.text = 'oai:scielo:' + identifier
        header.append(el)


def get_datestamp():
    return date.today().isoformat()


def get_set_spec(header, xml_tree):
    el = ET.Element('setSpec')
    el.text = get_issn(xml_tree)
    header.append(el)


def get_issn(xml_tree):
    issn = journal_meta.ISSN(xml_tree).epub
    if issn == '':
        issn = journal_meta.ISSN(xml_tree).without_pub_type

    return issn


def xml_oai_dc_record_pipe():
    record = ET.Element('record')

    return record


