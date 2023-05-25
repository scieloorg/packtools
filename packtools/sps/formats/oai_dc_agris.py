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
    front_articlemeta_issue,
)


def get_identifier(xml_tree):
    """
    Schema (https://agris.fao.org/agris_ods/dlio.dtd.txt):
        <!-- ELEMENT identifier -->
        <!ELEMENT dc:identifier (#PCDATA)>
        <!ATTLIST dc:identifier
            xml:lang CDATA #IMPLIED
            scheme (ags:IPC | ags:RN | ags:PN | ags:ISBN | ags:JN | dcterms:URI | ags:DOI | ags:PC) #IMPLIED
        >

    Example:
        <identifier>oai:agris.scielo:XS2021000111</identifier>
    """
    try:
        identifier = article_ids.ArticleIds(xml_tree).v2
        if len(identifier) == 23:
            return ''.join([identifier[10:18], identifier[21:]])
    except TypeError:
        pass


def add_identifier(header, xml_tree):
    """
        Schema (https://agris.fao.org/agris_ods/dlio.dtd.txt):
            <!-- ELEMENT identifier -->
            <!ELEMENT dc:identifier (#PCDATA)>
            <!ATTLIST dc:identifier
                xml:lang CDATA #IMPLIED
                scheme (ags:IPC | ags:RN | ags:PN | ags:ISBN | ags:JN | dcterms:URI | ags:DOI | ags:PC) #IMPLIED
            >

        Example:
            <identifier>oai:agris.scielo:XS2021000111</identifier>
        """
    identifier = get_identifier(xml_tree)
    if identifier is not None:
        value = f'oai:agris.scielo:XS{identifier}'
        el = ET.Element('identifier')
        el.text = value
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


def add_title(xml_oai_dc_agris, xml_tree):
    try:
        title = article_titles.ArticleTitles(xml_tree)
        lang = article_and_subarticles.ArticleAndSubArticles(xml_tree)

        el = ET.Element('{http://purl.org/dc/elements/1.1/}title')
        el.set('{http://www.w3.org/XML/1998/namespace}lang', lang.main_lang)
        el.text = title.article_title['text'].strip()

        xml_oai_dc_agris.find(".//ags:resource", {"ags": "http://purl.org/agmes/1.1/"}).append(el)
    except (AttributeError, TypeError):
        pass


def add_creator(xml_oai_dc_agris, author_name):
    ags = ET.Element('{http://purl.org/agmes/1.1/}creatorPersonal')
    ags.text = author_name

    dc = ET.Element('{http://purl.org/dc/elements/1.1/}creator')
    dc.append(ags)

    xml_oai_dc_agris.find(".//ags:resource", {"ags": "http://purl.org/agmes/1.1/"}).append(dc)


def xml_oai_dc_agris_record_pipe():
    """
    Example:
        <record>
        </record>
    """

    return ET.Element('record')


def xml_oai_dc_agris_header_pipe(xml_oai_dc_agris, xml_tree):
    """
    Schema (https://agris.fao.org/agris_ods/dlio.dtd.txt):
            <!-- ELEMENT identifier -->
            <!ELEMENT dc:identifier (#PCDATA)>
            <!ATTLIST dc:identifier
                xml:lang CDATA #IMPLIED
                scheme (ags:IPC | ags:RN | ags:PN | ags:ISBN | ags:JN | dcterms:URI | ags:DOI | ags:PC) #IMPLIED
            >

    Example:
        <header>
            <identifier>oai:agris.scielo:XS2021000111</identifier>
            <setSpec>0718-7181</setSpec>
        </header>
    """
    header = ET.Element('header')

    add_identifier(header, xml_tree)

    add_set_spec(header, xml_tree)
    xml_oai_dc_agris.append(header)


def xml_oai_dc_agris_metadata_pipe(xml_oai_dc_agris):
    """
    Example:
        <record>
            <metadata>
                <ags:resources
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:ags="http://purl.org/agmes/1.1/"
                xmlns:dc="http://purl.org/dc/elements/1.1/"
                xmlns:agls="http://www.naa.gov.au/recordkeeping/gov_online/agls/1.2"
                xmlns:dcterms="http://purl.org/dc/terms/">
            </metadata>
        </record>
    """

    nsmap = {
        'xsl': 'http://www.w3.org/1999/XSL/Transform',
        'ags': 'http://purl.org/agmes/1.1/',
        'dc': 'http://purl.org/dc/elements/1.1/',
        'agls': 'http://www.naa.gov.au/recordkeeping/gov_online/agls/1.2',
        'dcterms': 'http://purl.org/dc/terms/'
    }

    el = ET.Element('{http://purl.org/agmes/1.1/}resources', nsmap=nsmap)

    metadata = ET.Element('metadata')
    metadata.append(el)
    xml_oai_dc_agris.append(metadata)


def xml_oai_dc_agris_resouce_pipe(xml_oai_dc_agris, xml_tree):
    """
     Schema (https://agris.fao.org/agris_ods/dlio.dtd.txt):
        <!ELEMENT ags:resource (
        dc:title+,
        dc:creator*,
        dc:publisher*,
        dc:date*,
        dc:subject*,
        dc:description*,
        dc:identifier*,
        dc:type*,
        dc:format*,
        dc:language*,
        dc:relation*,
        agls:availability*,
        dc:source*,
        dc:coverage*,
        dc:rights*,
        ags:citation*
        )>
        <!ATTLIST ags:resource
            ags:ARN ID #REQUIRED
            ags:type (Record | Dataset)  #IMPLIED
        >
    Example:
        <record>
            <metadata>
                <ags:resources
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:ags="http://purl.org/agmes/1.1/"
                xmlns:dc="http://purl.org/dc/elements/1.1/"
                xmlns:agls="http://www.naa.gov.au/recordkeeping/gov_online/agls/1.2"
                xmlns:dcterms="http://purl.org/dc/terms/">
                    <ags:resource ags:ARN="XS2021000111">
            </metadata>
        </record>
    """
    el = ET.Element('{http://purl.org/agmes/1.1/}resource')
    el.set('{http://purl.org/agmes/1.1/}ARN', 'XS' + get_identifier(xml_tree))

    xml_oai_dc_agris.find('./metadata/{http://purl.org/agmes/1.1/}resources').append(el)


def xml_oai_dc_agris_title_pipe(xml_oai_dc_agris, xml_tree):
    """
    Schema (https://agris.fao.org/agris_ods/dlio.dtd.txt):
        <!-- ELEMENT title -->
        <!ELEMENT dc:title (#PCDATA | dcterms:alternative | ags:titleSupplement)*>
        <!ATTLIST dc:title
            xml:lang CDATA #IMPLIED
        >

    Example:
        <record>
            <metadata>
                <ags:resources>
                    <ags:resource ags:ARN="XS2021000111">
                        <dc:title xml:lang="es">
                            <![CDATA[ La canción reflexiva: en torno al estatuto crítico de la música popular en Brasil ]]>
                        </dc:title>
                    </ags:resource>
                </ags:resources>
            </metadata>
        </record>
    """
    add_title(xml_oai_dc_agris, xml_tree)


def xml_oai_dc_agris_creator_pipe(xml_oai_dc_agris, xml_tree):
    """
    Schema (https://agris.fao.org/agris_ods/dlio.dtd.txt):
        <!-- ELEMENT creator -->
        <!ELEMENT dc:creator (#PCDATA | ags:creatorPersonal | ags:creatorCorporate | ags:creatorConference)*>
        <!ELEMENT ags:creatorPersonal (#PCDATA)>
        <!ELEMENT ags:creatorCorporate (#PCDATA)>
        <!ELEMENT ags:creatorConference (#PCDATA)>

    Example:
        <record>
            <metadata>
                <ags:resources>
                    <ags:resource ags:ARN="XS2021000111">
                        <dc:creator>
                            <ags:creatorPersonal>de-Oliveira-Gerolamo, Ismael</ags:creatorPersonal>
                        </dc:creator>
                    </ags:resource>
                </ags:resources>
            </metadata>
        </record>
    """
    author = article_authors.Authors(xml_tree)
    try:
        surname = author.contribs[0].get('surname')
        given_name = author.contribs[0].get('given_names')
        author_name = f' {surname.strip()}, {given_name.strip()} '
        add_creator(xml_oai_dc_agris, author_name.strip())
    except IndexError:
        pass


def add_publisher(xml_oai_dc_agris, publisher):
    try:
        ags = ET.Element('{http://purl.org/agmes/1.1/}publisherName')
        ags.text = publisher.publishers_names[0].strip()

        dc = ET.Element('{http://purl.org/dc/elements/1.1/}publisher')
        dc.append(ags)

        xml_oai_dc_agris.find(".//ags:resource", {"ags": "http://purl.org/agmes/1.1/"}).append(dc)
    except IndexError:
        pass


def xml_oai_dc_agris_publisher_pipe(xml_oai_dc_agris, xml_tree):
    """
    Schema (https://agris.fao.org/agris_ods/dlio.dtd.txt):
        <!-- ELEMENT publisher -->
        <!ELEMENT dc:publisher (ags:publisherName | ags:publisherPlace)*>
        <!ELEMENT ags:publisherName (#PCDATA)>
        <!ELEMENT ags:publisherPlace (#PCDATA)>

    Example:
        <dc:publisher>
            <ags:publisherName>Pontificia Universidad Católica de Chile, Facultad de Filosofía, Instituto de Estética</ags:publisherName>
        </dc:publisher>
    """
    publisher = journal_meta.Publisher(xml_tree)

    add_publisher(xml_oai_dc_agris, publisher)


