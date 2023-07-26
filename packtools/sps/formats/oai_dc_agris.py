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


class GetDateError(Exception):
    ...


class AddLanguageError(Exception):
    ...


class AddTitleError(Exception):
    ...


class GetDescriptionError(Exception):
    ...


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
    if issn:
        el = ET.Element('setSpec')
        el.text = issn
        header.append(el)


def get_issn(xml_tree):
    issns = journal_meta.ISSN(xml_tree)

    return issns.epub or issns.ppub


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
    title = article_titles.ArticleTitles(xml_tree)
    lang = article_and_subarticles.ArticleAndSubArticles(xml_tree)

    el = ET.Element('{http://purl.org/dc/elements/1.1/}title')

    try:
        el.set('{http://www.w3.org/XML/1998/namespace}lang', lang.main_lang)
    except Exception as exc:
        raise AddLanguageError(f"Unable to add language {exc}")

    try:
        el.text = title.article_title['text'].strip()
    except Exception as exc:
        raise AddTitleError(f"Unable to add title {exc}")

    xml_oai_dc_agris.find(".//ags:resource", {"ags": "http://purl.org/agmes/1.1/"}).append(el)


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
    publishers = journal_meta.Publisher(xml_tree).publishers_names

    if publishers:
        dc = ET.Element('{http://purl.org/dc/elements/1.1/}publisher')

        for publisher in publishers:
            ags = ET.Element('{http://purl.org/agmes/1.1/}publisherName')
            ags.text = publisher.strip()
            dc.append(ags)

        xml_oai_dc_agris.find(".//ags:resource", {"ags": "http://purl.org/agmes/1.1/"}).append(dc)


def get_date(dt, m=False, d=False):
    try:
        year = dt.get('year')
        if year is None:
            return

        month = dt.get('month')
        day = dt.get('day')
        exceptions = [None, '', '0', '00']
        if month is None and day is None:
            return year

        month = '01' if month in exceptions else month
        day = '01' if day in exceptions else day

        if d:
            return '-'.join([year, month, day])
        elif m:
            return '-'.join([year, month])
        else:
            return year
    except Exception as exc:
        raise GetDateError(f"Unable to get date {exc}")


def xml_oai_dc_agris_date_pipe(xml_oai_dc_agris, xml_tree):
    """
    Schema (https://agris.fao.org/agris_ods/dlio.dtd.txt):
        <!-- ELEMENT date -->
        <!ELEMENT dc:date (dcterms:dateIssued | dcterms:modified)*>
        <!ELEMENT dcterms:dateIssued (#PCDATA)>
        <!ATTLIST dcterms:dateIssued
            scheme (dcterms:W3CDTF) #IMPLIED
        >
        <!ELEMENT dcterms:modified (#PCDATA)>
        <!ATTLIST dcterms:modified
            scheme (dcterms:W3CDTF) #IMPLIED
        >

    Example:
        <dc:date>
            <dcterms:dateIssued>2021</dcterms:dateIssued>
        </dc:date>
    """
    dt_out = get_date(dates.ArticleDates(xml_tree).article_date)

    if dt_out is not None:
        term = ET.Element('{http://purl.org/dc/terms/}dateIssued')
        term.text = dt_out

        dc = ET.Element('{http://purl.org/dc/elements/1.1/}date')
        dc.append(term)

        xml_oai_dc_agris.find(".//ags:resource", {"ags": "http://purl.org/agmes/1.1/"}).append(dc)


def add_subject(xml_oai_dc_agris, kw):
    el = ET.Element('{http://purl.org/dc/elements/1.1/}subject')
    el.set('{http://www.w3.org/XML/1998/namespace}lang', kw.get('lang'))
    el.text = kw.get('text')

    xml_oai_dc_agris.find(".//ags:resource", {"ags": "http://purl.org/agmes/1.1/"}).append(el)


def xml_oai_dc_agris_subject_pipe(xml_oai_dc_agris, xml_tree):
    """
    Schema (https://agris.fao.org/agris_ods/dlio.dtd.txt):
        <!-- ELEMENT subject -->
        <!ELEMENT dc:subject (#PCDATA | ags:subjectClassification | ags:subjectThesaurus)*>
        <!ATTLIST dc:subject
            xml:lang CDATA #IMPLIED
        >
        <!ELEMENT ags:subjectClassification (#PCDATA)>
        <!ATTLIST ags:subjectClassification
            xml:lang CDATA #IMPLIED
            scheme (ags:ASC | ags:CABC | dcterms:DDC | dcterms:LCC | dcterms:UDC | ags:ASFAC | ags:GFISC | ags:IWMIC | ags:JEL | ags:ECASC) #REQUIRED
        >
        <!ELEMENT ags:subjectThesaurus (#PCDATA)>
        <!ATTLIST ags:subjectThesaurus
            xml:lang CDATA #IMPLIED
            scheme (ags:CABT | ags:AGROVOC | ags:NALT | ags:ASFAT | dcterms:LCSH | dcterms:MeSH | ags:GFIST | ags:MEDITAGRI | ags:LEMB | ags:INRA | ags:UNBIST) #REQUIRED
        >

    Example:
        <dc:subject xml:lang="es">Canción popular</dc:subject>
        <dc:subject xml:lang="es">música popular brasileña</dc:subject>
        <dc:subject xml:lang="es">canción crítica</dc:subject>
        <dc:subject xml:lang="es">arte político</dc:subject>
        <dc:subject xml:lang="en">Popular song</dc:subject>
        <dc:subject xml:lang="en">critical song</dc:subject>
        <dc:subject xml:lang="en">Brazilian popular music</dc:subject>
        <dc:subject xml:lang="en">art and politics</dc:subject>
    """
    key_words = kwd_group.KwdGroup(xml_tree)

    for kw in key_words.extract_kwd_data_with_lang_text(subtag=False):
        add_subject(xml_oai_dc_agris, kw)


def xml_oai_dc_agris_description_pipe(xml_oai_dc_agris, xml_tree):
    """
    Schema (https://agris.fao.org/agris_ods/dlio.dtd.txt):
        <!-- ELEMENT description -->
        <!ELEMENT dc:description (ags:descriptionNotes | ags:descriptionEdition | dcterms:abstract)*>
        <!ELEMENT ags:descriptionNotes (#PCDATA)>
        <!ELEMENT ags:descriptionEdition (#PCDATA)>
        <!ELEMENT dcterms:abstract (#PCDATA)>
        <!ATTLIST dcterms:abstract
            xml:lang CDATA #IMPLIED
        >

    Example:
        <dc:description>
        <dcterms:abstract xml:lang="es">
        <![CDATA[ Resumen En el siglo xx, la música popular fue el lenguaje artístico más contundente y una de las grandes fuerzas estéticas de Brasil. Desde los años 30, ella ocupó una posición importante en debates culturales y proyectos nacionalistas y, a lo largo de los años, expandió su alcance con el avance de los medios de comunicación. Dicha inversión todavía resultó, más allá de lo esperado, en la producción de una modalidad crítica de canción. Así que en los 60, al igual que el arte moderno, la canción se tornó reflexiva, operando de manera crítica en relación consigo misma y con el contexto cultural y político. El componente reflexivo de la canción parece haber ampliado considerablemente su alcance cultural. Tanto es así que no parece irrazonable señalar una conexión profunda entre la canción y un cierto horizonte de construcción nacional. En este trabajo, intentamos hacer un panorama del desarrollo de la música popular brasileña de modo de aclarar ese proceso y, tal vez, posibilitar nuevos planteamientos para pensar sus posibilidades críticas desde su dimensión estética. ]]>
        </dcterms:abstract>
        </dc:description>
        <dc:description>
        <dcterms:abstract xml:lang="en">
        <![CDATA[ Abstract In the twentieth century, popular music was the most relevant artistic language and one great aesthetic forces of Brazil. Since the 30's this musical production occupied an important position in cultural nationalist ideologies and, over the years, expanded its reach with the advancement of the media. This investment has paid off beyond expectations and results in the production of a critical type of song. So, in the 60's this popular music becomes reflexive, operating critically in relation to itself and to the cultural and political context. In this paper, we try to make an overview of the development of Brazilian popular music so as to clarify this process and perhaps make possible new approaches to think its possibilities of criticism from its aesthetic dimension. ]]>
        </dcterms:abstract>
        </dc:description>
    """
    try:
        abstracts = article_abstract.Abstract(xml_tree).get_abstracts(style="inline")

        for abstract in abstracts:
            term = ET.Element('{http://purl.org/dc/terms/}abstract')
            term.set('{http://www.w3.org/XML/1998/namespace}lang', abstract.get("lang"))
            term.text = abstract.get("abstract")

            dc = ET.Element('{http://purl.org/dc/elements/1.1/}description')
            dc.append(term)

            xml_oai_dc_agris.find(".//ags:resource", {"ags": "http://purl.org/agmes/1.1/"}).append(dc)
    except Exception as exc:
        raise GetDescriptionError(f"Unable to get description {exc}")


def add_uri_identifier(xml_oai_dc_agris, identifier):
    dc = ET.Element('{http://purl.org/dc/elements/1.1/}identifier')
    dc.set('scheme', 'dcterms:URI')
    dc.text = identifier
    # dc.text = identifier.get('sci_arttext')

    xml_oai_dc_agris.find(".//ags:resource", {"ags": "http://purl.org/agmes/1.1/"}).append(dc)


def add_uri_doi(xml_oai_dc_agris, doi):
    dc = ET.Element('{http://purl.org/dc/elements/1.1/}identifier')
    dc.set('scheme', 'ags:DOI')
    dc.text = doi

    xml_oai_dc_agris.find(".//ags:resource", {"ags": "http://purl.org/agmes/1.1/"}).append(dc)


def xml_oai_dc_agris_identifier_pipe(xml_oai_dc_agris, xml_tree, data):
    """
    Schema (https://agris.fao.org/agris_ods/dlio.dtd.txt):
        <!-- ELEMENT identifier -->
        <!ELEMENT dc:identifier (#PCDATA)>
        <!ATTLIST dc:identifier
            xml:lang CDATA #IMPLIED
            scheme (ags:IPC | ags:RN | ags:PN | ags:ISBN | ags:JN | dcterms:URI | ags:DOI | ags:PC) #IMPLIED
        >

    Example:
        <dc:identifier scheme="dcterms:URI">
            http://www.scielo.cl/scielo.php?script=sci_arttext&pid=S0718-71812021000100011&lng=en&nrm=iso
        </dc:identifier>
        <dc:identifier scheme="ags:DOI">10.7764/69.1</dc:identifier>
    """
    # TODO
    # O modelo que provê a informação é disponível em outro PR
    # Quando o PR for incorporado a funcionalidade será implementada
    # identifier = article_uri.ArticleUri(xml_tree)
    # add_uri_identifier(xml_oai_dc_agris, identifier.all_uris)

    doi = article_ids.ArticleIds(xml_tree).doi
    add_uri_identifier(xml_oai_dc_agris, data.get('identifier'))
    add_uri_doi(xml_oai_dc_agris, doi)


def xml_oai_dc_agris_type_pipe(xml_oai_dc_agris, data=None):
    """
    Schema (https://agris.fao.org/agris_ods/dlio.dtd.txt):
        <!-- ELEMENT type -->
        <!ELEMENT dc:type (#PCDATA)>
        <!ATTLIST dc:type
            scheme (dcterms:DCMIType | isis) #IMPLIED
        >

    Example:
        <dc:type>journal article</dc:type>
    """
    tp = data and data.get('type') or 'journal article'
    if tp is not None:
        dc = ET.Element('{http://purl.org/dc/elements/1.1/}type')
        dc.text = tp

        xml_oai_dc_agris.find(".//ags:resource", {"ags": "http://purl.org/agmes/1.1/"}).append(dc)


def xml_oai_dc_agris_format_pipe(xml_oai_dc_agris, data):
    """
    Schema (https://agris.fao.org/agris_ods/dlio.dtd.txt):
        <!-- ELEMENT format -->
        <!ELEMENT dc:format (dcterms:extent | dcterms:medium)*>
        <!ELEMENT dcterms:extent (#PCDATA)>
        <!ELEMENT dcterms:medium (#PCDATA)>
        <!ATTLIST dcterms:medium
            scheme (dcterms:IMT) #IMPLIED
        >

    Example:
        <dc:format>
            <dcterms:medium>text/xml</dcterms:medium>
        </dc:format>
    """
    ft = data.get('format')
    if ft is not None:
        term = ET.Element('{http://purl.org/dc/terms/}medium')
        term.text = ft

        dc = ET.Element('{http://purl.org/dc/elements/1.1/}format')
        dc.append(term)

        xml_oai_dc_agris.find(".//ags:resource", {"ags": "http://purl.org/agmes/1.1/"}).append(dc)


def xml_oai_dc_agris_language_pipe(xml_oai_dc_agris, xml_tree):
    """
    Schema (https://agris.fao.org/agris_ods/dlio.dtd.txt):
        <!-- ELEMENT language -->
        <!ELEMENT dc:language (#PCDATA)>
        <!ATTLIST dc:language
            scheme (ags:ISO639-1 | dcterms:ISO639-2) #IMPLIED
        >

    Example:
        <dc:language scheme="ags:ISO639-1">es</dc:language>
    """
    lang = article_and_subarticles.ArticleAndSubArticles(xml_tree)

    el = ET.Element('{http://purl.org/dc/elements/1.1/}language')
    el.set('scheme', 'ags:ISO639-1')
    el.text = lang.main_lang

def get_location(data):
    try:
        return data.get('location')
    except AttributeError:
        pass


def add_location(location):
    loc = ET.Element('{http://purl.org/agmes/1.1/}availabilityLocation')
    loc.text = location
    return loc


def get_doi(xml_tree):
    return article_ids.ArticleIds(xml_tree).doi


def add_doi(doi):
    number = ET.Element('{http://purl.org/agmes/1.1/}availabilityNumber')
    number.text = doi

    return number


def xml_oai_dc_agris_availability_pipe(xml_oai_dc_agris, xml_tree, data=None):
    """
    Schema (https://agris.fao.org/agris_ods/dlio.dtd.txt):
        <!-- ELEMENT availability -->
        <!ELEMENT agls:availability (ags:availabilityLocation | ags:availabilityNumber)*>
        <!ELEMENT ags:availabilityLocation (#PCDATA)>
        <!ELEMENT ags:availabilityNumber (#PCDATA)>

    Example:
        <agls:availability>
            <ags:availabilityLocation>SCIELO</ags:availabilityLocation>
            <ags:availabilityNumber>10.7764/69.1</ags:availabilityNumber>
        </agls:availability>
    """
    agls = ET.Element('{http://www.naa.gov.au/recordkeeping/gov_online/agls/1.2}availability')

    location = get_location(data)
    if location is not None:
        agls.append(add_location(location))

    doi = get_doi(xml_tree)
    if doi is not None:
        agls.append(add_doi(doi))

    if location is not None or doi is not None:
        xml_oai_dc_agris.find(".//ags:resource", {"ags": "http://purl.org/agmes/1.1/"}).append(agls)


def get_citation_title(xml_tree):
    title = journal_meta.Title(xml_tree).journal_title
    if title is not None:
        return title, 'citationTitle'


def get_citation_identifier(xml_tree):
    issn = journal_meta.ISSN(xml_tree).epub
    if issn != '':
        return issn, 'citationIdentifier'


def get_citation_number(xml_tree):
    volume = front_articlemeta_issue.ArticleMetaIssue(xml_tree).volume
    if volume is not None:
        return volume, 'citationNumber'


def get_citation_chronology(xml_tree):
    date = get_date(dates.ArticleDates(xml_tree), d=True)
    if date is not None:
        return date, 'citationChronology'


def add_citation_elements(citation, elements):
    for element in elements:
        try:
            el = ET.Element('{http://purl.org/agmes/1.1/}' + element[1])
            if element[1] == 'citationIdentifier':
                el.set('scheme', 'ags:ISSN')
            el.text = element[0]
            citation.append(el)
        except TypeError:
            pass


def xml_oai_dc_agris_citation_pipe(xml_oai_dc_agris, xml_tree):
    """
    Schema (https://agris.fao.org/agris_ods/dlio.dtd.txt):
        <!-- ELEMENT citation -->
        <!ELEMENT ags:citation (ags:citationTitle | ags:citationIdentifier | ags:citationNumber | ags:citationChronology)*>
        <!ELEMENT ags:citationTitle (#PCDATA)>
        <!ATTLIST ags:citationTitle
            xml:lang CDATA #IMPLIED
        >
        <!ELEMENT ags:citationIdentifier (#PCDATA)>
        <!ATTLIST ags:citationIdentifier
            scheme (ags:ISSN | ags:CODEN | bibo:eissn) #REQUIRED
        >
        <!ELEMENT ags:citationNumber (#PCDATA)>
        <!ELEMENT ags:citationChronology (#PCDATA)>

    Example:
        <ags:citation>
            <ags:citationTitle>Aisthesis</ags:citationTitle>
            <ags:citationIdentifier scheme="ags:ISSN">0718-7181</ags:citationIdentifier>
            <ags:citationNumber> num.69</ags:citationNumber>
            <ags:citationChronology>2021/07</ags:citationChronology>
        </ags:citation>
    """
    citation = ET.Element('{http://purl.org/agmes/1.1/}citation')

    elements = [
        get_citation_title(xml_tree),
        get_citation_identifier(xml_tree),
        get_citation_number(xml_tree),
        get_citation_chronology(xml_tree),
    ]

    if elements:
        add_citation_elements(citation, elements)
        xml_oai_dc_agris.find(".//ags:resource", {"ags": "http://purl.org/agmes/1.1/"}).append(citation)


def pipeline_oai_dc_agris(xml_tree, data):
    xml_oai_dc_agris = xml_oai_dc_agris_record_pipe()
    xml_oai_dc_agris_header_pipe(xml_oai_dc_agris, xml_tree)
    xml_oai_dc_agris_metadata_pipe(xml_oai_dc_agris)
    xml_oai_dc_agris_resouce_pipe(xml_oai_dc_agris, xml_tree)
    xml_oai_dc_agris_title_pipe(xml_oai_dc_agris, xml_tree)
    xml_oai_dc_agris_creator_pipe(xml_oai_dc_agris, xml_tree)
    xml_oai_dc_agris_publisher_pipe(xml_oai_dc_agris, xml_tree)
    xml_oai_dc_agris_date_pipe(xml_oai_dc_agris, xml_tree)
    xml_oai_dc_agris_subject_pipe(xml_oai_dc_agris, xml_tree)
    xml_oai_dc_agris_description_pipe(xml_oai_dc_agris, xml_tree)
    xml_oai_dc_agris_identifier_pipe(xml_oai_dc_agris, xml_tree, data)
    xml_oai_dc_agris_type_pipe(xml_oai_dc_agris, data)
    xml_oai_dc_agris_format_pipe(xml_oai_dc_agris, data)
    xml_oai_dc_agris_language_pipe(xml_oai_dc_agris, xml_tree)
    xml_oai_dc_agris_availability_pipe(xml_oai_dc_agris, xml_tree, data)
    xml_oai_dc_agris_citation_pipe(xml_oai_dc_agris, xml_tree)

    return xml_oai_dc_agris
