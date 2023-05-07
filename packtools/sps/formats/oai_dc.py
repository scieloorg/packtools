from lxml import etree as ET
from packtools.sps.models import (
    article_ids,
    journal_meta,
    article_titles,
    article_authors,
    kwd_group,
    article_and_subarticles,
    article_abstract,
    dates,
)

from datetime import datetime, date


def add_identifier(header, xml_tree):
    try:
        identifier = article_ids.ArticleIds(xml_tree).v2
        el = ET.Element('identifier')
        el.text = 'oai:scielo:' + identifier
        header.append(el)
    except TypeError:
        pass


def get_datestamp():
    return date.today().isoformat()


def add_datestamp(header):
    el = ET.Element('datestamp')
    el.text = get_datestamp()
    header.append(el)


def add_set_spec(header, xml_tree):
    issn = get_issn(xml_tree)
    if issn != '':
        el = ET.Element('setSpec')
        el.text = issn
        header.append(el)


def get_issn(xml_tree):
    issns = journal_meta.ISSN(xml_tree)

    return issns.epub or issns.ppub


def add_title(xml_oai_dc, title):
    try:
        el = ET.Element('{http://purl.org/dc/elements/1.1/}title')
        el.text = ET.CDATA(f" {title.article_title.get('text')} ")

        xml_oai_dc.append(el)
    except TypeError:
        pass




def xml_oai_dc_record_pipe():
    record = ET.Element('record')

    return record


def xml_oai_dc_header_pipe(xml_oai_dc, xml_tree):
    """
        <header>
            <identifier>oai:scielo:S0718-71812022000200217</identifier>
            <datestamp>2023-04-04</datestamp>
            <setSpec>0718-7181</setSpec>
        </header>
    """
    header = ET.Element('header')

    get_identifier(header, xml_tree)

    el = ET.Element('datestamp')
    el.text = get_datestamp()
    header.append(el)

    get_set_spec(header, xml_tree)
    xml_oai_dc.append(header)


def xml_oai_dc_metadata(xml_oai_dc):
    """
    <record>
        <metadata>
        </metadata>
    </record>
    """
    metadata = ET.Element('metadata')
    xml_oai_dc.append(metadata)


def setup_oai_dc_header_pipe(xml_oai_dc):
    """
    <oai-dc:dc
    xmlns:oai-dc="http://www.openarchives.org/OAI/2.0/oai_dc/"
    xmlns:dc="http://purl.org/dc/elements/1.1/"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://www.openarchives.org/OAI/2.0/oai_dc/
    http://www.openarchives.org/OAI/2.0/oai_dc.xsd">
    """
    nsmap = {
        'oai-dc': 'http://www.openarchives.org/OAI/2.0/oai_dc/',
        'dc': 'http://purl.org/dc/elements/1.1/',
        'xsi': 'http://www.w3.org/2001/XMLSchema-instance'
    }

    el = ET.Element('{http://www.openarchives.org/OAI/2.0/oai_dc/}dc', nsmap=nsmap)
    el.set('{http://www.w3.org/2001/XMLSchema-instance}schemaLocation',
           'http://www.openarchives.org/OAI/2.0/oai_dc/ http://www.openarchives.org/OAI/2.0/oai_dc.xsd')

    xml_oai_dc.append(el)


def xml_oai_dc_title(xml_oai_dc, xml_tree):
    """
    <dc:title>
        <![CDATA[ La canción reflexiva: en torno al estatuto crítico de la música popular en Brasil ]]>
    </dc:title>
    """
    title = article_titles.ArticleTitles(xml_tree)
    add_title(xml_oai_dc, title)

