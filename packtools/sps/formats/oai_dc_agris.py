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


