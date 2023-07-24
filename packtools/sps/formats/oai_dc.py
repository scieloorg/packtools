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


class AddIdentifierError(Exception):
    ...


def add_identifier(header, xml_tree):
    try:
        identifier = article_ids.ArticleIds(xml_tree).v2
        el = ET.Element('identifier')
        el.text = 'oai:scielo:' + identifier
        header.append(el)
    except Exception as exc:
        raise AddIdentifierError(f"Unable to add identifier {exc}")


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
    el = ET.Element('{http://purl.org/dc/elements/1.1/}title')
    el.text = title.strip()

    xml_oai_dc.append(el)


def add_creator(xml_oai_dc, author_name):
    el = ET.Element('{http://purl.org/dc/elements/1.1/}creator')
    el.text = author_name.strip()

    xml_oai_dc.append(el)


def add_subject(xml_oai_dc, kw, article):
    if kw.get('lang') == article.main_lang:
        el = ET.Element('{http://purl.org/dc/elements/1.1/}subject')
        el.text = kw.get('text').strip()

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


def add_relation(xml_oai_dc, related_article):
    el = ET.Element('{http://purl.org/dc/elements/1.1/}relation')
    for relation in related_article.related_articles:
        if relation:
            el.text = relation.get('href')
            xml_oai_dc.append(el)
            break


def pipeline_xml_oai_dc(xml_tree):
    xml_oai_dc = xml_oai_dc_record_pipe()
    xml_oai_dc_header_pipe(xml_oai_dc, xml_tree)
    xml_oai_dc_metadata(xml_oai_dc)
    setup_oai_dc_header_pipe(xml_oai_dc)
    xml_oai_dc_title(xml_oai_dc, xml_tree)
    xml_oai_dc_creator(xml_oai_dc, xml_tree)
    xml_oai_dc_subject(xml_oai_dc, xml_tree)
    xml_oai_dc_description(xml_oai_dc, xml_tree)
    xml_oai_dc_publisher(xml_oai_dc, xml_tree)
    xml_oai_dc_source(xml_oai_dc, xml_tree)
    xml_oai_dc_date(xml_oai_dc, xml_tree)
    xml_oai_dc_format(xml_oai_dc)
    xml_oai_dc_identifier(xml_oai_dc, xml_tree)
    xml_oai_dc_language(xml_oai_dc, xml_tree)
    xml_oai_dc_relation(xml_oai_dc, xml_tree)

    return xml_oai_dc


def xml_oai_dc_record_pipe():
    """
    Example:
         <record>
        </record>
    """

    return ET.Element('record')


def xml_oai_dc_header_pipe(xml_oai_dc, xml_tree):
    """
    Example:
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
    Example:
        <record>
            <metadata>
            </metadata>
        </record>
    """
    metadata = ET.Element('metadata')
    xml_oai_dc.append(metadata)


def setup_oai_dc_header_pipe(xml_oai_dc):
    """
    Example:
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
    Schema (http://www.openarchives.org/OAI/2.0/openarchivesprotocol.htm#dublincore):
        <complexType name="oai_dcType">
            <choice minOccurs="0" maxOccurs="unbounded">
                <element ref="dc:title"/>
            </choice>
        </complexType>

    Element definition (https://www.dublincore.org/specifications/dublin-core/dces/):
        Term Name:  title
        URI:	    http://purl.org/dc/elements/1.1/title
        Label:	    Title
        Definition:	A name given to the resource.
        Comment:	Typically, a Title will be a name by which the resource is formally known.

    Example:
    <dc:title>
        <![CDATA[ La canción reflexiva: en torno al estatuto crítico de la música popular en Brasil ]]>
    </dc:title>
    """
    title = article_titles.ArticleTitles(xml_tree)
    add_title(xml_oai_dc, title)


def xml_oai_dc_creator(xml_oai_dc, xml_tree):
    """
    Schema (http://www.openarchives.org/OAI/2.0/openarchivesprotocol.htm#dublincore):
        <complexType name="oai_dcType">
            <choice minOccurs="0" maxOccurs="unbounded">
                <element ref="dc:creator"/>
            </choice>
        </complexType>

    Element definition (https://www.dublincore.org/specifications/dublin-core/dces/):
        Term Name:  creator
        URI:	    http://purl.org/dc/elements/1.1/creator
        Label:	    Creator
        Definition:	An entity primarily responsible for making the resource.
        Comment:	Examples of a Creator include a person, an organization, or a service.
                    Typically, the name of a Creator should be used to indicate the entity.

    Example:
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
    Schema (http://www.openarchives.org/OAI/2.0/openarchivesprotocol.htm#dublincore):
        <complexType name="oai_dcType">
            <choice minOccurs="0" maxOccurs="unbounded">
                <element ref="dc:subject"/>
            </choice>
        </complexType>

    Element definition (https://www.dublincore.org/specifications/dublin-core/dces/):
        Term Name:  subject
        URI:	    http://purl.org/dc/elements/1.1/subject
        Label:	    Subject
        Definition:	The topic of the resource.
        Comment:	Typically, the subject will be represented using keywords, key phrases, or classification codes.
                    Recommended best practice is to use a controlled vocabulary.

    Example:
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
    Schema (http://www.openarchives.org/OAI/2.0/openarchivesprotocol.htm#dublincore):
        <complexType name="oai_dcType">
            <choice minOccurs="0" maxOccurs="unbounded">
                <element ref="dc:description"/>
            </choice>
        </complexType>

    Element definition (https://www.dublincore.org/specifications/dublin-core/dces/):
        Term Name:  description
        URI:	    http://purl.org/dc/elements/1.1/description
        Label:	    Description
        Definition:	An account of the resource.
        Comment:	Description may include but is not limited to: an abstract, a table of contents, a graphical
                    representation, or a free-text account of the resource.

    Example:
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
    Schema (http://www.openarchives.org/OAI/2.0/openarchivesprotocol.htm#dublincore):
        <complexType name="oai_dcType">
            <choice minOccurs="0" maxOccurs="unbounded">
                <element ref="dc:publisher"/>
            </choice>
        </complexType>

    Element definition (https://www.dublincore.org/specifications/dublin-core/dces/):
        Term Name:  publisher
        URI:	    http://purl.org/dc/elements/1.1/publisher
        Label:	    Publisher
        Definition:	An entity responsible for making the resource available.
        Comment:	Examples of a Publisher include a person, an organization, or a service. Typically, the name
                    of a Publisher should be used to indicate the entity.

    Example:
        <dc:publisher>
            <![CDATA[ Pontificia Universidad Católica de Chile, Facultad de Filosofía,
            Instituto de Estética ]]>
        </dc:publisher>
    """
    publisher = journal_meta.Publisher(xml_tree)

    add_publisher(xml_oai_dc, publisher)


def xml_oai_dc_source(xml_oai_dc, xml_tree):
    """
    Schema (http://www.openarchives.org/OAI/2.0/openarchivesprotocol.htm#dublincore):
        <complexType name="oai_dcType">
            <choice minOccurs="0" maxOccurs="unbounded">
                <element ref="dc:source"/>
            </choice>
        </complexType>

    Element definition (https://www.dublincore.org/specifications/dublin-core/dces/):
        Term Name:  source
        URI:	    http://purl.org/dc/elements/1.1/source
        Label:	    Source
        Definition:	A related resource from which the described resource is derived.
        Comment:	The described resource may be derived from the related resource in whole or in part.
                    Recommended best practice is to identify the related resource by means of a string
                    conforming to a formal identification system.

    Example:
        '<dc:source xmlns:dc="http://purl.org/dc/elements/1.1/">'
            '<![CDATA[ Acta Paulista de Enfermagem ]]>'
        '</dc:source>'
    """
    journal = journal_meta.Title(xml_tree)

    add_source(xml_oai_dc, journal)


def xml_oai_dc_date(xml_oai_dc, xml_tree):
    """
    Schema (http://www.openarchives.org/OAI/2.0/openarchivesprotocol.htm#dublincore):
        <complexType name="oai_dcType">
            <choice minOccurs="0" maxOccurs="unbounded">
                <element ref="dc:date"/>
            </choice>
        </complexType>

    Element definition (https://www.dublincore.org/specifications/dublin-core/dces/):
        Term Name:  date
        URI:	    http://purl.org/dc/elements/1.1/date
        Label:	    Date
        Definition:	A point or period of time associated with an event in the lifecycle of the resource.
        Comment:	Date may be used to express temporal information at any level of granularity.
                    Recommended best practice is to use an encoding scheme, such as the W3CDTF profile
                    of ISO 8601 [W3CDTF].
        References:	[W3CDTF] http://www.w3.org/TR/NOTE-datetime

    Example:
        <dc:date>2021-07-01</dc:date>
    """
    dt_out = get_date(dates.ArticleDates(xml_tree))

    add_date(xml_oai_dc, dt_out)


def xml_oai_dc_format(xml_oai_dc):
    """
    Schema (http://www.openarchives.org/OAI/2.0/openarchivesprotocol.htm#dublincore):
        <complexType name="oai_dcType">
            <choice minOccurs="0" maxOccurs="unbounded">
                <element ref="dc:format"/>
            </choice>
        </complexType>

    Element definition (https://www.dublincore.org/specifications/dublin-core/dces/):
        Term Name:  format
        URI:	    http://purl.org/dc/elements/1.1/format
        Label:	    Format
        Definition:	The file format, physical medium, or dimensions of the resource.
        Comment:	Examples of dimensions include size and duration. Recommended best practice is to use a controlled
                    vocabulary such as the list of Internet Media Types [MIME].
        References: [MIME] http://www.iana.org/assignments/media-types/

    Examples (https://en.wikipedia.org/wiki/Media_type):
        <dc:format>text/html</dc:format>
        <dc:format>text/plain</dc:format>
        <dc:format>text/css</dc:format>
        <dc:format>text/csv</dc:format>
        <dc:format>text/javascript(.js)</dc:format>
        <dc:format>text/xml</dc:format>
    """
    el = ET.Element('{http://purl.org/dc/elements/1.1/}format')
    el.text = 'text/html'
    xml_oai_dc.append(el)


def xml_oai_dc_identifier(xml_oai_dc, xml_tree):
    """
    Schema (http://www.openarchives.org/OAI/2.0/openarchivesprotocol.htm#dublincore):
        <complexType name="oai_dcType">
            <choice minOccurs="0" maxOccurs="unbounded">
                <element ref="dc:identifier"/>
            </choice>
        </complexType>

    Element definition (https://www.dublincore.org/specifications/dublin-core/dces/):
        Term Name:  identifier
        URI:	    http://purl.org/dc/elements/1.1/identifier
        Label:	    Identifier
        Definition:	An unambiguous reference to the resource within a given context.
        Comment:	Recommended best practice is to identify the resource by means of a string conforming to a formal
                    identification system.

    Example:
        <dc:identifier>http://www.scielo.cl/scielo.php?script=sci_arttext&pid=S0718-71812021000100011</dc:identifier>
    """
    identifier = article_uri.ArticleUri(xml_tree)
    add_uri_identifier(xml_oai_dc, identifier.all_uris)


def xml_oai_dc_language(xml_oai_dc, xml_tree):
    """
    Schema (http://www.openarchives.org/OAI/2.0/openarchivesprotocol.htm#dublincore):
        <complexType name="oai_dcType">
            <choice minOccurs="0" maxOccurs="unbounded">
                <element ref="dc:language"/>
            </choice>
        </complexType>

    Element definition (https://www.dublincore.org/specifications/dublin-core/dces/):
        Term Name:  language
        URI:	    http://purl.org/dc/elements/1.1/language
        Label:	    Language
        Definition:	A language of the resource.
        Comment:	Recommended best practice is to use a controlled vocabulary such as RFC 4646 [RFC4646].
        References:	[RFC4646] http://www.ietf.org/rfc/rfc4646.txt

    Example:
        <dc:language>es</dc:language>
    """
    lang = article_and_subarticles.ArticleAndSubArticles(xml_tree)
    add_lang(xml_oai_dc, lang)


def xml_oai_dc_relation(xml_oai_dc, xml_tree):
    """
    Schema (http://www.openarchives.org/OAI/2.0/openarchivesprotocol.htm#dublincore):
        <complexType name="oai_dcType">
            <choice minOccurs="0" maxOccurs="unbounded">
                <element ref="dc:relation"/>
            </choice>
        </complexType>

    Element definition (https://www.dublincore.org/specifications/dublin-core/dces/):
        Term Name:  relation
        URI:	    http://purl.org/dc/elements/1.1/relation
        Label:	    Relation
        Definition:	A related resource.
        Comment:	Recommended best practice is to identify the related resource by means of a string conforming
                    to a formal identification system.

    Example:
        <dc:relation>10.7764/69.1</dc:relation>
    """
    related_article = related_articles.RelatedItems(xml_tree)
    add_relation(xml_oai_dc, related_article)

