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
    related_articles,
    article_uri,
)

from datetime import date


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


def add_creator(xml_oai_dc, author_name):
    el = ET.Element('{http://purl.org/dc/elements/1.1/}creator')
    el.text = ET.CDATA(author_name)

    xml_oai_dc.append(el)


def add_subject(xml_oai_dc, kw, article):
    if kw.get('lang') == article.main_lang:
        el = ET.Element('{http://purl.org/dc/elements/1.1/}subject')
        el.text = ET.CDATA(f" {kw.get('text')} ")

        xml_oai_dc.append(el)


def get_description(abstract):
    try:
        description = [abstract.main_abstract_with_tags['title']]
        for key, value in abstract.main_abstract_with_tags['sections'].items():
            description.append(key)
            description.append(value)

        return " ".join(description)
    except IndexError:
        pass


def add_description(xml_oai_dc, description):
    el = ET.Element('{http://purl.org/dc/elements/1.1/}description')
    el.text = ET.CDATA(f" {description} ")

    xml_oai_dc.append(el)


def add_publisher(xml_oai_dc, publisher):
    try:
        el = ET.Element('{http://purl.org/dc/elements/1.1/}publisher')
        el.text = ET.CDATA(f" {publisher.publishers_names[0]} ")

        xml_oai_dc.append(el)
    except IndexError:
        pass


def add_source(xml_oai_dc, journal):
    el = ET.Element('{http://purl.org/dc/elements/1.1/}source')
    el.text = ET.CDATA(f" {journal.journal_title} ")

    xml_oai_dc.append(el)


def get_date(dt):
    year = dt.pub_dates[0].get('year')
    month = dt.pub_dates[0].get('month')
    day = dt.pub_dates[0].get('day')
    exceptions = [None, '', '0', '00']

    if year is None:
        return
    if month is None and day is None:
        return year
    month = '01' if month in exceptions else month
    day = '01' if day in exceptions else day

    return '-'.join([year, month, day])


def add_date(xml_oai_dc, dt_out):
    el = ET.Element('{http://purl.org/dc/elements/1.1/}date')
    el.text = dt_out
    xml_oai_dc.append(el)


def add_uri_identifier(xml_oai_dc, identifier):
    el = ET.Element('{http://purl.org/dc/elements/1.1/}identifier')
    el.text = identifier.get('sci_arttext')
    xml_oai_dc.append(el)


def add_lang(xml_oai_dc, lang):
    el = ET.Element('{http://purl.org/dc/elements/1.1/}language')
    el.text = lang.main_lang
    xml_oai_dc.append(el)


def xml_oai_dc_record_pipe():

    return ET.Element('record')


def xml_oai_dc_header_pipe(xml_oai_dc, xml_tree):
    """
        <header>
            <identifier>oai:scielo:S0718-71812022000200217</identifier>
            <datestamp>2023-04-04</datestamp>
            <setSpec>0718-7181</setSpec>
        </header>
    """
    header = ET.Element('header')

    add_identifier(header, xml_tree)

    add_datestamp(header)

    add_set_spec(header, xml_tree)
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


def xml_oai_dc_creator(xml_oai_dc, xml_tree):
    """
    <dc:creator>
        <![CDATA[ de-Oliveira-Gerolamo,Ismael ]]>
    </dc:creator>
    """
    author = article_authors.Authors(xml_tree)
    try:
        surname = author.contribs[0].get('surname')
        given_name = author.contribs[0].get('given_names')
        author_name = f' {surname.strip()},{given_name.strip()} '
        add_creator(xml_oai_dc, author_name)
    except IndexError:
        pass


def xml_oai_dc_subject(xml_oai_dc, xml_tree):
    """
    dc:subject>
        <![CDATA[ Canción popular ]]>
    </dc:subject>
    <dc:subject>
        <![CDATA[ música popular brasileña ]]>
    </dc:subject>
    <dc:subject>
        <![CDATA[ canción crítica ]]>
    </dc:subject>
    <dc:subject>
        <![CDATA[ arte político ]]>
    </dc:subject>
    """
    key_words = kwd_group.KwdGroup(xml_tree)
    article = article_and_subarticles.ArticleAndSubArticles(xml_tree)

    for kw in key_words.extract_kwd_data_with_lang_text(subtag=False):
        add_subject(xml_oai_dc, kw, article)


def xml_oai_dc_description(xml_oai_dc, xml_tree):
    """
    <dc:description>
        <![CDATA[ Resumen En el siglo xx, la música popular fue el lenguaje artístico más
        contundente y una de las grandes fuerzas estéticas de Brasil. Desde los años 30, ella
        ocupó una posición importante en debates culturales y proyectos nacionalistas y, a lo
        largo de los años, expandió su alcance con el avance de los medios de comunicación.
        Dicha inversión todavía resultó, más allá de lo esperado, en la producción de una
        modalidad crítica de canción. Así que en los 60, al igual que el arte moderno, la canción
        se tornó reflexiva, operando de manera crítica en relación consigo misma y con el contexto
        cultural y político. El componente reflexivo de la canción parece haber ampliado
        considerablemente su alcance cultural. Tanto es así que no parece irrazonable señalar
        una conexión profunda entre la canción y un cierto horizonte de construcción nacional.
        En este trabajo, intentamos hacer un panorama del desarrollo de la música popular brasileña
        de modo de aclarar ese proceso y, tal vez, posibilitar nuevos planteamientos para pensar
        sus posibilidades críticas desde su dimensión estética. ]]>
    </dc:description>
    """
    abstract = article_abstract.Abstract(xml_tree)

    description = get_description(abstract)

    add_description(xml_oai_dc, description)


def xml_oai_dc_publisher(xml_oai_dc, xml_tree):
    """
    <dc:publisher>
        <![CDATA[ Pontificia Universidad Católica de Chile, Facultad de Filosofía,
        Instituto de Estética ]]>
    </dc:publisher>
    """
    publisher = journal_meta.Publisher(xml_tree)

    add_publisher(xml_oai_dc, publisher)


def xml_oai_dc_source(xml_oai_dc, xml_tree):
    journal = journal_meta.Title(xml_tree)

    add_source(xml_oai_dc, journal)


def xml_oai_dc_date(xml_oai_dc, xml_tree):
    """
    <dc:date>2021-07-01</dc:date>
    """
    dt_out = get_date(dates.ArticleDates(xml_tree))

    add_date(xml_oai_dc, dt_out)


def xml_oai_dc_format(xml_oai_dc):
    el = ET.Element('{http://purl.org/dc/elements/1.1/}format')
    # TODO
    # Não identifiquei a origem de format
    el.text = 'text/html'
    xml_oai_dc.append(el)
