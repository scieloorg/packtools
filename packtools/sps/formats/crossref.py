# coding: utf-8
import re
import uuid
from copy import deepcopy
from datetime import datetime

from lxml import etree as ET

from packtools.sps.models import (
    journal_meta,
    dates,
    front_articlemeta_issue,
    article_and_subarticles,
    article_authors,
    aff,
    article_abstract,
    article_ids,
    article_license,
    article_titles,
    article_doi_with_lang,
    article_citations,
)

SUPPLBEG_REGEX = re.compile(r'^0 ')
SUPPLEND_REGEX = re.compile(r' 0$')


def get_timestamp():
    return datetime.now().strftime('%Y%m%d%H%M%S')


def get_doi_batch_id():
    return uuid.uuid4().hex


def create_journal_title(item, citation):
    """
        Adiciona o título do periódico ao elemento 'citation'

        Parameters
        ----------
        item : dict
            Dicionário com dados de citação, como por exemplo:
            {
                "label": "1",
                "source": "Drug Alcohol Depend.",
                "main_author": {"surname": "Tran", "given_name": "B"},
                "all_authors": [
                    {"surname": "Tran", "given_name": "B"},
                    {"surname": "Falster", "given_name": "MO"},
                    {"surname": "Douglas", "given_name": "K"},
                    {"surname": "Blyth", "given_name": "F"},
                    {"surname": "Jorm", "given_name": "LR"},
                ],
                "volume": "150",
                "fpage": "85",
                "lpage": "91",
                "year": "2015",
                "article_title": "Smoking and potentially preventable hospitalisation: the benefit of smoking cessation in
                                  older ages",
                "mixed_citation": "1. Tran B, Falster MO, Douglas K, Blyth F, Jorm LR. Smoking and potentially preventable
                                   hospitalisation: the benefit of smoking cessation in older ages. Drug Alcohol Depend.
                                   2015;150:85-91. DOI:\n            https://doi.org/10.1016/j.drugalcdep.2015.02.028",
            }

        citation : lxml.etree._Element
            Elemento xml, como por exemplo:
            <citation key="ref1" />

        Returns
        -------
        lxml.etree._Element
            <citation key="ref1">
                <source>Drug Alcohol Depend.</source>
            </citation>
        """
    if item.get('source') is not None:
        el = ET.Element('journal_title')
        el.text = item.get('source')
        citation.append(el)


def create_author(item, citation):
    """
    Adiciona nome de autor ao elemento 'citation'

    Parameters
    ----------
    item : dict
        Dicionário com dados de citação, como por exemplo:
        {
            "label": "1",
            "source": "Drug Alcohol Depend.",
            "main_author": {"surname": "Tran", "given_name": "B"},
            "all_authors": [
                {"surname": "Tran", "given_name": "B"},
                {"surname": "Falster", "given_name": "MO"},
                {"surname": "Douglas", "given_name": "K"},
                {"surname": "Blyth", "given_name": "F"},
                {"surname": "Jorm", "given_name": "LR"},
            ],
            "volume": "150",
            "fpage": "85",
            "lpage": "91",
            "year": "2015",
            "article_title": "Smoking and potentially preventable hospitalisation: the benefit of smoking cessation in
                              older ages",
            "mixed_citation": "1. Tran B, Falster MO, Douglas K, Blyth F, Jorm LR. Smoking and potentially preventable
                               hospitalisation: the benefit of smoking cessation in older ages. Drug Alcohol Depend.
                               2015;150:85-91. DOI:\n            https://doi.org/10.1016/j.drugalcdep.2015.02.028",
        }

    citation : lxml.etree._Element
        Elemento xml, como por exemplo:
        <citation key="ref1" />

    Returns
    -------
    lxml.etree._Element
        <citation key="ref1">
            <author>Tran B</author>
        </citation>
    """
    try:
        main_author = item.get('main_author')
        el = ET.Element('author')
        el.text = ' '.join([main_author.get('surname'), main_author.get('given_name')])
        citation.append(el)
    except TypeError:
        pass


def create_volume(item, citation):
    """
    Adiciona identificação do volume ao elemento 'citation'

    Parameters
    ----------
    item : dict
        Dicionário com dados de citação, como por exemplo:
        {
            "label": "1",
            "source": "Drug Alcohol Depend.",
            "main_author": {"surname": "Tran", "given_name": "B"},
            "all_authors": [
                {"surname": "Tran", "given_name": "B"},
                {"surname": "Falster", "given_name": "MO"},
                {"surname": "Douglas", "given_name": "K"},
                {"surname": "Blyth", "given_name": "F"},
                {"surname": "Jorm", "given_name": "LR"},
            ],
            "volume": "150",
            "fpage": "85",
            "lpage": "91",
            "year": "2015",
            "article_title": "Smoking and potentially preventable hospitalisation: the benefit of smoking cessation in
                              older ages",
            "mixed_citation": "1. Tran B, Falster MO, Douglas K, Blyth F, Jorm LR. Smoking and potentially preventable
                               hospitalisation: the benefit of smoking cessation in older ages. Drug Alcohol Depend.
                               2015;150:85-91. DOI:\n            https://doi.org/10.1016/j.drugalcdep.2015.02.028",
        }

    citation : lxml.etree._Element
        Elemento xml, como por exemplo:
        <citation key="ref1" />

    Returns
    -------
    lxml.etree._Element
        <citation key="ref1">
            <volume>150</volume>
        </citation>
    """
    if item.get('volume') is not None:
        el = ET.Element('volume')
        el.text = item.get('volume')
        citation.append(el)


def create_issue(item, citation):
    """
    Adiciona identificação do fascículo ao elemento 'citation'

    Parameters
    ----------
    item : dict
        Dicionário com dados de citação, como por exemplo:
        {
            "label": "1",
            "source": "Drug Alcohol Depend.",
            "main_author": {"surname": "Tran", "given_name": "B"},
            "all_authors": [
                {"surname": "Tran", "given_name": "B"},
                {"surname": "Falster", "given_name": "MO"},
                {"surname": "Douglas", "given_name": "K"},
                {"surname": "Blyth", "given_name": "F"},
                {"surname": "Jorm", "given_name": "LR"},
            ],
            "volume": "150",
            "fpage": "85",
            "lpage": "91",
            "year": "2015",
            "issue": "4",
            "article_title": "Smoking and potentially preventable hospitalisation: the benefit of smoking cessation in
                              older ages",
            "mixed_citation": "1. Tran B, Falster MO, Douglas K, Blyth F, Jorm LR. Smoking and potentially preventable
                               hospitalisation: the benefit of smoking cessation in older ages. Drug Alcohol Depend.
                               2015;150:85-91. DOI:\n            https://doi.org/10.1016/j.drugalcdep.2015.02.028",
        }

    citation : lxml.etree._Element
        Elemento xml, como por exemplo:
        <citation key="ref1" />

    Returns
    -------
    lxml.etree._Element
        <citation key="ref1">
            <issue>4</issue>
        </citation>
    """
    if item.get('issue') is not None:
        el = ET.Element('issue')
        el.text = item.get('issue')
        citation.append(el)


def create_first_page(item, citation):
    """
    Adiciona número da primeira página do artigo ao elemento 'citation'

    Parameters
    ----------
    item : dict
        Dicionário com dados de citação, como por exemplo:
        {
            "label": "1",
            "source": "Drug Alcohol Depend.",
            "main_author": {"surname": "Tran", "given_name": "B"},
            "all_authors": [
                {"surname": "Tran", "given_name": "B"},
                {"surname": "Falster", "given_name": "MO"},
                {"surname": "Douglas", "given_name": "K"},
                {"surname": "Blyth", "given_name": "F"},
                {"surname": "Jorm", "given_name": "LR"},
            ],
            "volume": "150",
            "fpage": "85",
            "lpage": "91",
            "year": "2015",
            "issue": "4",
            "article_title": "Smoking and potentially preventable hospitalisation: the benefit of smoking cessation in
                              older ages",
            "mixed_citation": "1. Tran B, Falster MO, Douglas K, Blyth F, Jorm LR. Smoking and potentially preventable
                               hospitalisation: the benefit of smoking cessation in older ages. Drug Alcohol Depend.
                               2015;150:85-91. DOI:\n            https://doi.org/10.1016/j.drugalcdep.2015.02.028",
        }

    citation : lxml.etree._Element
        Elemento xml, como por exemplo:
        <citation key="ref1" />

    Returns
    -------
    lxml.etree._Element
        <citation key="ref1">
            <first_page>85</first_page>
        </citation>
    """
    if item.get('fpage') is not None:
        el = ET.Element('first_page')
        el.text = item.get('fpage')
        citation.append(el)


def create_year(item, citation):
    """
    Adiciona o ano de publicação do artigo ao elemento 'citation'

    Parameters
    ----------
    item : dict
        Dicionário com dados de citação, como por exemplo:
        {
            "label": "1",
            "source": "Drug Alcohol Depend.",
            "main_author": {"surname": "Tran", "given_name": "B"},
            "all_authors": [
                {"surname": "Tran", "given_name": "B"},
                {"surname": "Falster", "given_name": "MO"},
                {"surname": "Douglas", "given_name": "K"},
                {"surname": "Blyth", "given_name": "F"},
                {"surname": "Jorm", "given_name": "LR"},
            ],
            "volume": "150",
            "fpage": "85",
            "lpage": "91",
            "year": "2015",
            "issue": "4",
            "article_title": "Smoking and potentially preventable hospitalisation: the benefit of smoking cessation in
                              older ages",
            "mixed_citation": "1. Tran B, Falster MO, Douglas K, Blyth F, Jorm LR. Smoking and potentially preventable
                               hospitalisation: the benefit of smoking cessation in older ages. Drug Alcohol Depend.
                               2015;150:85-91. DOI:\n            https://doi.org/10.1016/j.drugalcdep.2015.02.028",
        }

    citation : lxml.etree._Element
        Elemento xml, como por exemplo:
        <citation key="ref1" />

    Returns
    -------
    lxml.etree._Element
        <citation key="ref1">
            <year>2015</year>
        </citation>
    """
    if item.get('year') is not None:
        el = ET.Element('cYear')
        el.text = item.get('year')
        citation.append(el)


def create_article_title(item, citation):
    """
    Adiciona o título do artigo ao elemento 'citation'

    Parameters
    ----------
    item : dict
        Dicionário com dados de citação, como por exemplo:
        {
            "label": "1",
            "source": "Drug Alcohol Depend.",
            "main_author": {"surname": "Tran", "given_name": "B"},
            "all_authors": [
                {"surname": "Tran", "given_name": "B"},
                {"surname": "Falster", "given_name": "MO"},
                {"surname": "Douglas", "given_name": "K"},
                {"surname": "Blyth", "given_name": "F"},
                {"surname": "Jorm", "given_name": "LR"},
            ],
            "volume": "150",
            "fpage": "85",
            "lpage": "91",
            "year": "2015",
            "issue": "4",
            "article_title": "Smoking and potentially preventable hospitalisation: the benefit of smoking cessation in
                              older ages",
            "mixed_citation": "1. Tran B, Falster MO, Douglas K, Blyth F, Jorm LR. Smoking and potentially preventable
                               hospitalisation: the benefit of smoking cessation in older ages. Drug Alcohol Depend.
                               2015;150:85-91. DOI:\n            https://doi.org/10.1016/j.drugalcdep.2015.02.028",
        }

    citation : lxml.etree._Element
        Elemento xml, como por exemplo:
        <citation key="ref1" />

    Returns
    -------
    lxml.etree._Element
        <citation key="ref1">
            <article_title>Smoking and potentially preventable hospitalisation: the benefit of smoking cessation in
                              older ages</article_title>
        </citation>
    """
    if item.get('article_title') is not None:
        el = ET.Element('article_title')
        el.text = item.get('article_title')
        citation.append(el)


def get_citation(item):
    """
        Cria o elemento 'citation'.

        Parameters
        ----------
        item : dict
            Dicionário com dados de citação, como por exemplo:
            {
                "label": "1",
                "source": "Drug Alcohol Depend.",
                "main_author": {"surname": "Tran", "given_name": "B"},
                "all_authors": [
                    {"surname": "Tran", "given_name": "B"},
                    {"surname": "Falster", "given_name": "MO"},
                    {"surname": "Douglas", "given_name": "K"},
                    {"surname": "Blyth", "given_name": "F"},
                    {"surname": "Jorm", "given_name": "LR"},
                ],
                "volume": "150",
                "fpage": "85",
                "lpage": "91",
                "year": "2015",
                "issue": "4",
                "article_title": "Smoking and potentially preventable hospitalisation: the benefit of smoking cessation in
                                  older ages",
                "mixed_citation": "1. Tran B, Falster MO, Douglas K, Blyth F, Jorm LR. Smoking and potentially preventable
                                   hospitalisation: the benefit of smoking cessation in older ages. Drug Alcohol Depend.
                                   2015;150:85-91. DOI:\n            https://doi.org/10.1016/j.drugalcdep.2015.02.028",
            }

        Returns
        -------
        lxml.etree._Element
            <citation key="ref1">
                <journal_title>Drug Alcohol Depend.</journal_title>
                <author>Tran B</author>
                <volume>150</volume>
                <first_page>85</first_page>
                <cYear>2015</cYear>
                <article_title>Smoking and potentially preventable hospitalisation: the benefit of smoking cessation in older ages</article_title>
            </citation>
        """
    citation = ET.Element('citation')
    citation.set('key', 'ref' + item.get('label'))

    create_journal_title(item, citation)
    create_author(item, citation)
    create_volume(item, citation)
    create_issue(item, citation)
    create_first_page(item, citation)
    create_year(item, citation)
    create_article_title(item, citation)

    return citation


def get_affiliation(xml_tree, author):
    """
        Adiciona o ano de publicação do artigo ao elemento 'citation'

        Parameters
        ----------
        xml_tree : lxml.etree._Element
            Elemento XML no padrão SciELO que será convertido para o padrão CrossRef

        author: dict
            Dicionário com os dados dos autores da publicação, por exemplo:
            {
                "surname": "Oliveira",
                "given_names": "Josiana Araujo de",
                "rid": "aff1",
                "contrib-type": "author",
            }

        Returns
        -------
        lxml.etree._Element
            <affiliation>
                Universidade Federal do Rio Grande do Sul, Brazil
            </affiliation>
        """
    affiliation = ET.Element('affiliation')
    affs = aff.AffiliationExtractor(xml_tree).get_affiliation_data_from_multiple_tags(subtag=False)
    for a in affs:
        if a.get('id') == author.get('rid') and a.get('id') is not None:
            orgname = a.get('institution')[0].get('orgname')
            name = a.get('country')[0].get('name')
            if orgname is not None and name is not None:
                affiliation.text = orgname + ', ' + name
    if affiliation.text != '':
        return affiliation
    else:
        return


def get_one_contributor(xml_tree, seq, author):
    """
    Obtem os dados referentes a um autor de uma publicação.

    Parameters
    ----------
    xml_tree : lxml.etree._Element
        Elemento XML no padrão SciELO que será convertido para o padrão CrossRef

    seq : int
        Número que indica a ordem dos autores na publicação

    author: dict
        Dicionário com os dados dos autores da publicação, por exemplo:
        {
            "surname": "Oliveira",
            "given_names": "Josiana Araujo de",
            "rid": "aff1",
            "contrib-type": "author",
        }

    Returns
    -------
    lxml.etree._Element
        <person_name contributor_role="author" sequence="first">
            <given_name>Josiana Araujo de</given_name>
            <surname>Oliveira</surname>
            <affiliation>Universidade do Estado do Rio de Janeiro, Brasil</affiliation>
        </person_name>
    """
    person_name = ET.Element('person_name')
    person_name.set('contributor_role', author.get('contrib-type'))
    if seq == 0:
        person_name.set('sequence', 'first')
    else:
        person_name.set('sequence', 'additional')
    if author.get('given_names') is not None:
        given_name = ET.Element('given_name')
        given_name.text = author.get('given_names')
        person_name.append(given_name)
    if author.get('surname') is not None:
        surname = ET.Element('surname')
        surname.text = author.get('surname')
        person_name.append(surname)
    if get_affiliation(xml_tree, author) is not None:
        affiliation = get_affiliation(xml_tree, author)
        person_name.append(affiliation)
    if author.get('orcid') is not None:
        orcid = ET.Element('ORCID')
        orcid.text = 'http://orcid.org/' + author.get('orcid')
        person_name.append(orcid)

    return person_name


def pipeline_crossref(xml_tree, data):
    xml_crossref = setupdoibatch_pipe()
    xml_crossref_head_pipe(xml_crossref)
    xml_crossref_doibatchid_pipe(xml_crossref)
    xml_crossref_timestamp_pipe(xml_crossref)
    xml_crossref_depositor_pipe(xml_crossref, data)
    xml_crossref_registrant_pipe(xml_crossref, data)
    xml_crossref_body_pipe(xml_crossref)
    xml_crossref_journal_pipe(xml_crossref)
    xml_crossref_journalmetadata_pipe(xml_crossref)
    xml_crossref_journaltitle_pipe(xml_crossref, xml_tree)
    xml_crossref_abbreviatedjournaltitle_pipe(xml_crossref, xml_tree)
    xml_crossref_issn_pipe(xml_crossref, xml_tree)
    xml_crossref_journalissue_pipe(xml_crossref)
    xml_crossref_pubdate_pipe(xml_crossref, xml_tree)
    xml_crossref_journalvolume_pipe(xml_crossref)
    xml_crossref_volume_pipe(xml_crossref, xml_tree)
    xml_crossref_issue_pipe(xml_crossref, xml_tree)
    xml_crossref_journalarticle_pipe(xml_crossref, xml_tree)
    xml_crossref_articletitles_pipe(xml_crossref, xml_tree)
    # xml_crossref_articletitle_pipe(xml_crossref, xml_tree)
    xml_crossref_articlecontributors_pipe(xml_crossref, xml_tree)
    xml_crossref_articleabstract_pipe(xml_crossref, xml_tree)
    xml_crossref_articlepubdate_pipe(xml_crossref, xml_tree)
    xml_crossref_pages_pipe(xml_crossref, xml_tree)
    xml_crossref_pid_pipe(xml_crossref, xml_tree)
    xml_crossref_elocation_pipe(xml_crossref, xml_tree)
    xml_crossref_permissions_pipe(xml_crossref, xml_tree)
    xml_crossref_programrelateditem_pipe(xml_crossref, xml_tree)
    xml_crossref_doidata_pipe(xml_crossref)
    xml_crossref_doi_pipe(xml_crossref, xml_tree)
    xml_crossref_resource_pipe(xml_crossref, xml_tree)
    xml_crossref_collection_pipe(xml_crossref, xml_tree)
    xml_crossref_articlecitations_pipe(xml_crossref, xml_tree)
    xml_crossref_close_pipe(xml_crossref)

    return xml_crossref


def setupdoibatch_pipe():
    """
    Cria o elemento XML inicial padronizado.

    Returns
    -------
    lxml.etree._Element
        <doi_batch xmlns:ai="http://www.crossref.org/AccessIndicators.xsd"
        xmlns:jats="http://www.ncbi.nlm.nih.gov/JATS1"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xmlns="http://www.crossref.org/schema/4.4.0"
        xsi:schemaLocation="http://www.crossref.org/schema/4.4.0
        http://www.crossref.org/schemas/crossref4.4.0.xsd"/>
    """

    nsmap = {
        'ai': 'http://www.crossref.org/AccessIndicators.xsd',
        'jats': 'http://www.ncbi.nlm.nih.gov/JATS1',
        'xsi': 'http://www.w3.org/2001/XMLSchema-instance',
        'xml': 'http://www.w3.org/XML/1998/namespace'

    }

    el = ET.Element('doi_batch', nsmap=nsmap)
    el.set('version', '4.4.0')
    el.set('xmlns', 'http://www.crossref.org/schema/4.4.0')
    el.set('{http://www.w3.org/2001/XMLSchema-instance}schemaLocation',
           'http://www.crossref.org/schema/4.4.0 http://www.crossref.org/schemas/crossref4.4.0.xsd')

    return el


def xml_crossref_head_pipe(xml_crossref):
    """
        Adiciona o elemento 'head' ao xml_crossref.

        Parameters
        ----------
        xml_crossref : lxml.etree._Element
            Elemento XML no padrão CrossRef em construção

        Returns
        -------
        lxml.etree._Element
            <?xml version="1.0" encoding="UTF-8"?>
            <doi_batch ...>
                <head />
            </doi_batch>
        """
    head = ET.Element('head')

    xml_crossref.append(head)


def xml_crossref_doibatchid_pipe(xml_crossref):
    """
    Adiciona o elemento 'doi_batch_id' ao xml_crossref.

    Parameters
    ----------
    xml_crossref : lxml.etree._Element
        Elemento XML no padrão CrossRef em construção

    Returns
    -------
    lxml.etree._Element
        <?xml version="1.0" encoding="UTF-8"?>
        <doi_batch ...>
            <head>
                <doi_batch_id>49d374553c5d48c0bdd54d25080e0045</doi_batch_id>
            </head>
        </doi_batch>
    """
    doi_batch_id = ET.Element('doi_batch_id')
    doi_batch_id.text = get_doi_batch_id()

    xml_crossref.find('./head').append(doi_batch_id)


def xml_crossref_timestamp_pipe(xml_crossref):
    """
    Adiciona o elemento 'timestamp' ao xml_crossref.

    Parameters
    ----------
    xml_crossref : lxml.etree._Element
        Elemento XML no padrão CrossRef em construção

    Returns
    -------
    lxml.etree._Element
        <?xml version="1.0" encoding="UTF-8"?>
        <doi_batch ...>
            <head>
                <timestamp>20230405112328</timestamp>
            </head>
        </doi_batch>
    """
    timestamp = ET.Element('timestamp')
    timestamp.text = get_timestamp()

    xml_crossref.find('./head').append(timestamp)


def xml_crossref_depositor_pipe(xml_crossref, data):
    """
    Adiciona o elemento 'depositor' ao xml_crossref.

    Parameters
    ----------
    xml_crossref : lxml.etree._Element
        Elemento XML no padrão CrossRef em construção

    data : dict
        Dicionário com dados suplementares para a criação do xml_crossref como, por exemplo:
        data = {
                    "depositor_name": depositor,
                    "depositor_email_address": name@domain.com
                }

    Returns
    -------
    lxml.etree._Element
        <?xml version="1.0" encoding="UTF-8"?>
        <doi_batch ...>
            <head>
                <depositor>
                    <depositor_name>depositor</depositor_name>
                    <email_address>name@domain.com</email_address>
                </depositor>
            </head>
        </doi_batch>
        """
    depositor = ET.Element('depositor')
    depositor_name = ET.Element('depositor_name')
    email_address = ET.Element('email_address')

    depositor_name.text = data.get('depositor_name')
    email_address.text = data.get('depositor_email_address')

    depositor.append(depositor_name)
    depositor.append(email_address)

    xml_crossref.find('./head').append(depositor)


def xml_crossref_registrant_pipe(xml_crossref, data):
    """
    Adiciona o elemento 'registrant' ao xml_crossref.

    Parameters
    ----------
    xml_crossref : lxml.etree._Element
        Elemento XML no padrão CrossRef em construção

    data : dict
        Dicionário com dados suplementares para a criação do xml_crossref como, por exemplo:
        data = {
                    "registrant": registrant
                }

    Returns
    -------
    lxml.etree._Element
        <?xml version="1.0" encoding="UTF-8"?>
        <doi_batch ...>
            <head>
                <registrant>registrant</registrant>
            </head>
        </doi_batch>
    """
    registrant = ET.Element('registrant')
    registrant.text = data.get('registrant')

    xml_crossref.find('./head').append(registrant)


def xml_crossref_body_pipe(xml_crossref):
    """
    Adiciona o elemento 'body' ao xml_crossref.

    Parameters
    ----------
    xml_crossref : lxml.etree._Element
        Elemento XML no padrão CrossRef em construção

    Returns
    -------
    lxml.etree._Element
        <?xml version="1.0" encoding="UTF-8"?>
        <doi_batch ...>
            </head>
            <body/>
        </doi_batch>
    """
    body = ET.Element('body')

    xml_crossref.append(body)


def xml_crossref_journal_pipe(xml_crossref):
    """
    Adiciona o elemento 'journal' ao xml_crossref.

    Parameters
    ----------
    xml_crossref : lxml.etree._Element
        Elemento XML no padrão CrossRef em construção

    Returns
    -------
    lxml.etree._Element
        <?xml version="1.0" encoding="UTF-8"?>
        <doi_batch ...>
            </head>
            <body>
                <journal/>
            </body>
        </doi_batch>
    """
    journal = ET.Element('journal')

    xml_crossref.find('./body').append(journal)


def xml_crossref_journalmetadata_pipe(xml_crossref):
    """
    Adiciona o elemento 'journal_metadata' ao xml_crossref.

    Parameters
    ----------
    xml_crossref : lxml.etree._Element
        Elemento XML no padrão CrossRef em construção

    Returns
    -------
    lxml.etree._Element
        <?xml version="1.0" encoding="UTF-8"?>
        <doi_batch ...>
            </head>
            <body>
                <journal>
                    <journal_metadata/>
                </journal>
            </body>
        </doi_batch>
    """
    journal_metadata = ET.Element('journal_metadata')

    xml_crossref.find('./body/journal').append(journal_metadata)


def xml_crossref_journaltitle_pipe(xml_crossref, xml_tree):
    """
    Adiciona o elemento 'full_title' ao xml_crossref.

    Parameters
    ----------
    xml_crossref : lxml.etree._Element
        Elemento XML no padrão CrossRef em construção

    xml_tree : lxml.etree._Element
        Elemento XML no padrão SciELO com os dados de origem

    Returns
    -------
    lxml.etree._Element
        <?xml version="1.0" encoding="UTF-8"?>
        <doi_batch ...>
            </head>
            <body>
                <journal>
                    <journal_metadata/>
                </journal>
            </body>
        </doi_batch>
    """
    titles = journal_meta.Title(xml_tree)
    full_title = ET.Element('full_title')
    full_title.text = titles.journal_title

    xml_crossref.find('./body/journal/journal_metadata').append(full_title)


def xml_crossref_abbreviatedjournaltitle_pipe(xml_crossref, xml_tree):
    """
    Adiciona o elemento 'abbrev_title' ao xml_crossref.

    Parameters
    ----------
    xml_crossref : lxml.etree._Element
        Elemento XML no padrão CrossRef em construção

    xml_tree : lxml.etree._Element
        Elemento XML no padrão SciELO com os dados de origem

    Returns
    -------
    <?xml version="1.0" encoding="UTF-8"?>
    <doi_batch ...>
       <body>
          <journal>
             <journal_metadata>
                <abbrev_title>Acta Paul Enferm</abbrev_title>
             </journal_metadata>
          </journal>
       </body>
    </doi_batch>
    """
    titles = journal_meta.Title(xml_tree)
    abbrev_title = ET.Element('abbrev_title')
    abbrev_title.text = titles.abbreviated_journal_title

    xml_crossref.find('./body/journal/journal_metadata').append(abbrev_title)


def xml_crossref_issn_pipe(xml_crossref, xml_tree):
    """
    Adiciona o elemento 'issn' ao xml_crossref.

    Parameters
    ----------
    xml_crossref : lxml.etree._Element
        Elemento XML no padrão CrossRef em construção

    xml_tree : lxml.etree._Element
        Elemento XML no padrão SciELO com os dados de origem

    Returns
    -------
    <?xml version="1.0" encoding="UTF-8"?>
    <doi_batch ...>
       <body>
          <journal>
             <journal_metadata>
                <issn media_type="electronic">1982-0194</issn>
                <issn media_type="print">0103-2100</issn>
             </journal_metadata>
          </journal>
       </body>
    </doi_batch>
    """
    issns = journal_meta.ISSN(xml_tree)

    issn = ET.Element('issn')
    issn.text = issns.epub
    issn.set('media_type', 'electronic')
    xml_crossref.find('./body/journal/journal_metadata').append(issn)

    issn = ET.Element('issn')
    issn.text = issns.ppub
    issn.set('media_type', 'print')
    xml_crossref.find('./body/journal/journal_metadata').append(issn)


def xml_crossref_journalissue_pipe(xml_crossref):
    """
    <journal_issue>
        <publication_date media_type="online">
            <year>2022</year>
        </publication_date>
        <journal_volume>
            <volume>56</volume>
        </journal_volume>
    </journal_issue>
    """
    journal_issue = ET.Element('journal_issue')

    xml_crossref.find('./body/journal').append(journal_issue)


def xml_crossref_pubdate_pipe(xml_crossref, xml_tree):
    """
    <journal_issue>
        <publication_date media_type="online">
            <year>2022</year>
        </publication_date>
    </journal_issue>
    """
    try:
        year = ET.Element('year')
        year.text = dates.ArticleDates(xml_tree).article_date.get('year')

        publication_date = ET.Element('publication_date')
        publication_date.set('media_type', 'online')
        publication_date.append(year)

        xml_crossref.find('./body/journal/journal_issue').append(publication_date)
    except AttributeError:
        pass


def xml_crossref_journalvolume_pipe(xml_crossref):
    journal_volume = ET.Element('journal_volume')

    xml_crossref.find('./body/journal/journal_issue').append(journal_volume)


def xml_crossref_volume_pipe(xml_crossref, xml_tree):
    """
    <journal_issue>
        <journal_volume>
            <volume>56</volume>
        </journal_volume>
    </journal_issue>
    """
    volume = ET.Element('volume')
    volume.text = front_articlemeta_issue.ArticleMetaIssue(xml_tree).volume

    xml_crossref.find('./body/journal/journal_issue/journal_volume').append(volume)


def xml_crossref_issue_pipe(xml_crossref, xml_tree):
    """
    <journal_issue>
        <journal_volume>
            <issue>4</issue>
        </journal_volume>
    </journal_issue>
    """
    issue = ET.Element('issue')
    issue.text = front_articlemeta_issue.ArticleMetaIssue(xml_tree).issue

    xml_crossref.find('./body/journal/journal_issue/journal_volume').append(issue)


def xml_crossref_journalarticle_pipe(xml_crossref, xml_tree):
    """
    <body>
        <journal>
            <journal_article language="en" publication_type="research-article" reference_distribution_opts="any"/>
            <journal_article language="pt" publication_type="translation" reference_distribution_opts="any"/>
        </journal>
    </body>
    """
    articles = article_and_subarticles.ArticleAndSubArticles(xml_tree).data
    for article in articles:
        journal_article = ET.Element('journal_article')
        journal_article.set('language', article['lang'])
        journal_article.set('publication_type', article['article_type'])
        journal_article.set('reference_distribution_opts', 'any')
        xml_crossref.find('./body/journal').append(journal_article)


def xml_crossref_articletitles_pipe(xml_crossref, xml_tree):
    """
    IN (SciELO format) ->
    <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
    <front>
    <article-meta>
    <article-id specific-use="scielo-v3" pub-id-type="publisher-id">ZwzqmpTpbhTmtwR9GfDzP7c</article-id>
    <article-id specific-use="scielo-v2" pub-id-type="publisher-id">S0080-62342022000100445</article-id>
    <article-id pub-id-type="doi">10.1590/1980-220X-REEUSP-2021-0569en</article-id>
    <article-id pub-id-type="other">00445</article-id>
    <title-group>
    <article-title>
    Effects of an educational intervention with nursing professionals on approaches to hospitalized smokers: a quasi-experimental study
    <xref ref-type="fn" rid="FN1">*</xref>
    </article-title>
    <trans-title-group xml:lang="es">
    <trans-title>Efectos de una intervención educativa con profesionales de enfermería en el abordaje de pacientes fumadores: un estudio cuasi-experimental</trans-title>
    </trans-title-group>
    </title-group>
    </article-meta>
    </front>
    <sub-article article-type="translation" id="s1" xml:lang="pt">
    <front-stub>
    <title-group>
    <article-title>
    Efeitos de uma intervenção educativa com profissionais de enfermagem sobre abordagens ao paciente tabagista: estudo quase-experimental
    <xref ref-type="fn" rid="FN2">*</xref>
    </article-title>
    </title-group>
    </front-stub>
    </sub-article>
    </article>

    OUT (CrossRef format) ->
    <doi_batch
    xmlns:ai="http://www.crossref.org/AccessIndicators.xsd"
    xmlns:jats="http://www.ncbi.nlm.nih.gov/JATS1"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xmlns="http://www.crossref.org/schema/4.4.0" version="4.4.0"
    xsi:schemaLocation="http://www.crossref.org/schema/4.4.0
    http://www.crossref.org/schemas/crossref4.4.0.xsd">
    <body>
    <journal>
    <journal_article language="en" publication_type="research-article" reference_distribution_opts="any">
    <titles>
    <title>Effects of an educational intervention with nursing professionals on approaches to hospitalized smokers: a quasi-experimental study</title>
    <original_language_title language="pt">Efeitos de uma intervenção educativa com profissionais de enfermagem sobre abordagens ao paciente tabagista: estudo quase-experimental</original_language_title>
    </titles>
    </journal_article>
    <journal_article language="pt" publication_type="translation" reference_distribution_opts="any">
    <titles>
    <title>Efeitos de uma intervenção educativa com profissionais de enfermagem sobre abordagens ao paciente tabagista: estudo quase-experimental</title>
    <original_language_title language="en">Effects of an educational intervention with nursing professionals on approaches to hospitalized smokers: a quasi-experimental study</original_language_title>
    </titles>
    </journal_article>
    </journal>
    </body>
    </doi_batch>
    """
    art_titles = article_titles.ArticleTitles(xml_tree).article_title_dict
    art_lang = [lang.get('lang') for lang in article_and_subarticles.ArticleAndSubArticles(xml_tree).data]

    for lang in art_lang:
        titles = ET.Element('titles')
        title = ET.Element('title')
        title.text = art_titles.get(lang)
        titles.append(title)
        original_language_title = ET.Element('original_language_title')
        orig_lang = 'pt' if lang == 'en' else 'en'
        original_language_title.set('language', orig_lang)
        original_language_title.text = art_titles.get(orig_lang)
        titles.append(original_language_title)
        xml_crossref.find(f"./body/journal/journal_article[@language='{lang}']").append(titles)


def xml_crossref_articlecontributors_pipe(xml_crossref, xml_tree):
    """
    <journal_article language="en" publication_type="research-article" reference_distribution_opts="any">
        <contributors>
            <person_name contributor_role="author" sequence="first">
                <given_name>Fernanda Guarilha</given_name>
                <surname>Boni</surname>
                <affiliation>Universidade Federal do Rio Grande do Sul, Brazil</affiliation>
                <ORCID>http://orcid.org/0000-0003-0843-6485</ORCID>
            </person_name>
            <person_name contributor_role="author" sequence="additional">
                <given_name>Yasmin Lorenz</given_name>
                <surname>da Rosa</surname>
                <affiliation>Universidade Federal do Rio Grande do Sul, Brazil</affiliation>
                <ORCID>http://orcid.org/0000-0001-7364-4753</ORCID>
            </person_name>
        </contributors>
    </journal_article>
    <journal_article language="pt" publication_type="translation" reference_distribution_opts="any">
        <contributors>
            <person_name contributor_role="author" sequence="first">
                <given_name>Fernanda Guarilha</given_name>
                <surname>Boni</surname>
                <affiliation>Universidade Federal do Rio Grande do Sul, Brazil</affiliation>
                <ORCID>http://orcid.org/0000-0003-0843-6485</ORCID>
            </person_name>
            <person_name contributor_role="author" sequence="additional">
                <given_name>Yasmin Lorenz</given_name>
                <surname>da Rosa</surname>
                <affiliation>Universidade Federal do Rio Grande do Sul, Brazil</affiliation>
                <ORCID>http://orcid.org/0000-0001-7364-4753</ORCID>
            </person_name>
        </contributors>
    </journal_article>
    """
    articles = article_and_subarticles.ArticleAndSubArticles(xml_tree).data
    authors = article_authors.Authors(xml_tree).contribs
    for article in articles:
        contributors = ET.Element('contributors')
        for seq, author in enumerate(authors):
            person_name = get_one_contributor(xml_tree, seq, author)
            contributors.append(person_name)
        xml_crossref.find(f"./body/journal/journal_article[@language='{article['lang']}']").append(contributors)


def xml_crossref_articleabstract_pipe(xml_crossref, xml_tree):
    """
    <jats:abstract xml:lang="en">
        <jats:p>Abstract Objective: to assess the effects of an educational intervention on smoking cessation aimed at the nursing team. Method: this is a quasi-experimental study with 37 nursing professionals from a Brazilian hospital from May/2019 to December/2020. The intervention consisted of training nursing professionals on approaches to hospitalized smokers divided into two steps, the first, online, a prerequisite for the face-to-face/videoconference. The effect of the intervention was assessed through pre- and post-tests completed by participants. Smokers’ medical records were also analyzed. For analysis, McNemar’s chi-square test was used. Results: there was an increase in the frequency of actions aimed at smoking cessation after the intervention. Significant differences were found in guidelines related to disclosure to family members of their decision to quit smoking and the need for support, encouragement of abstinence after hospital discharge, and information on tobacco cessation and relapse strategies. Conclusion: the educational intervention proved to be innovative and with a great capacity for disseminating knowledge. The post-test showed a positive effect on the frequency of actions aimed at smoking cessation implemented by the nursing team.</jats:p>
    </jats:abstract>
    <jats:abstract xml:lang="es">
        <jats:p>RESUMEN Objetivo: evaluar los efectos de una intervención educativa para dejar de fumar dirigida al equipo de enfermería. Método: estudio cuasi-experimental con 37 profesionales de enfermería de un hospital brasileño de mayo/2019 a diciembre/2020. La intervención consistió en capacitar a los profesionales de enfermería en el abordaje del paciente fumador, dividida en dos etapas, la primera, en línea, requisito previo para la presencial/videoconferencia. El efecto de la intervención se evaluó a través del pre y post test realizado por los participantes. También se analizaron los registros en las historias clínicas de los fumadores. Para el análisis se utilizó la prueba Chi-Square de McNemar. Resultados: hubo un aumento en la frecuencia de acciones dirigidas a dejar de fumar después de la intervención. Se encontraron diferencias significativas en las guías relacionadas con la divulgación a los familiares de la decisión de dejar de fumar y la necesidad de apoyo, el estímulo de la abstinencia después del alta hospitalaria y la información sobre estrategias para dejar de fumar y recaer. Conclusión: la intervención educativa demostró ser innovadora y con gran capacidad de diseminación del conocimiento. El post-test mostró un efecto positivo en la frecuencia de las acciones dirigidas a la deshabituación tabáquica implementadas por el equipo de enfermería.</jats:p>
    </jats:abstract>
    <jats:abstract xml:lang="pt">
        <jats:p>RESUMO Objetivo: avaliar os efeitos de uma intervenção educativa sobre cessação do tabagismo direcionada à equipe de enfermagem. Método: estudo quase-experimental com 37 profissionais de enfermagem de um hospital brasileiro de maio/2019 a dezembro/2020. A intervenção consistiu em capacitar profissionais de enfermagem sobre abordagens aos pacientes tabagistas, dividida em duas etapas, a primeira, online, pré-requisito para a presencial/videoconferência. O efeito da intervenção foi avaliado por meio do pré- e pós-teste preenchido pelos participantes. Também foram analisados registros em prontuários de pacientes fumantes. Para análise, utilizou-se o Teste do Qui-Quadrado de McNemar. Resultados: houve aumento da frequência das ações visando à cessação tabágica após a intervenção. Diferenças significativas foram encontradas em orientações relacionadas à divulgação aos familiares da decisão de parar de fumar e necessidade de apoio, incentivo à abstinência após alta hospitalar e informações sobre estratégias para cessação do tabaco e recaídas. Conclusão: a intervenção educativa se mostrou inovadora e com grande capacidade de difusão do conhecimento. O pós-teste evidenciou efeito positivo na frequência das ações visando à cessação tabágica implementadas pela equipe de enfermagem.</jats:p>
    </jats:abstract>
    """
    abstracts = article_abstract.Abstract(xml_tree).abstracts_with_tags
    articles = article_and_subarticles.ArticleAndSubArticles(xml_tree).data

    for article in articles:
        for abstract in abstracts:
            if abstract:
                jats = ET.Element('{http://www.ncbi.nlm.nih.gov/JATS1}abstract')
                jats.set('{http://www.w3.org/XML/1998/namespace}lang', abstract.get('lang'))
                jats_p = ET.Element('{http://www.ncbi.nlm.nih.gov/JATS1}p')
                text = [abstract.get('title')]
                for key, value in abstract.get('sections').items():
                    text.append(key)
                    text.append(value)
                jats_p.text = ' '.join(text)
                jats.append(jats_p)
                xml_crossref.find(f"./body/journal/journal_article[@language='{article['lang']}']").append(deepcopy(jats))


def xml_crossref_articlepubdate_pipe(xml_crossref, xml_tree):
    """
    <journal_article language="en" publication_type="full_text" reference_distribution_opts="any">
        <publication_date media_type="online">
            <year>2022</year>
        </publication_date>
    </journal_article>
    <journal_article language="pt" publication_type="full_text" reference_distribution_opts="any">
        <publication_date media_type="online">
            <year>2022</year>
        </publication_date>
    </journal_article>

    todo
    publication_type in SciELO format: research-article and translation
    publication_type in CrossRef format: full_text
    """
    articles = article_and_subarticles.ArticleAndSubArticles(xml_tree).data
    pub_date = dates.ArticleDates(xml_tree).collection_date

    for article in articles:
        publication_date = ET.Element('publication_date')
        publication_date.set('media_type', 'online')

        year = ET.Element('year')
        year.text = pub_date.get('year')

        publication_date.append(year)

        xml_crossref.find(f"./body/journal/journal_article[@language='{article['lang']}']").append(publication_date)


def xml_crossref_pages_pipe(xml_crossref, xml_tree):
    """
    IN (SciELO format) ->
    <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink"
    article-type="research-article" dtd-version="1.0" specific-use="sps-1.6" xml:lang="pt">
        <front>
            <article-meta>
                <article-id pub-id-type="publisher-id" specific-use="scielo-v3">XZrRmc87LzCkDtLdcXwgztp</article-id>
                <article-id pub-id-type="publisher-id" specific-use="scielo-v2">S0103-21002017000400333</article-id>
                <article-id pub-id-type="publisher-id">1982-0194201700050</article-id>
                <article-id pub-id-type="doi">10.1590/1982-0194201700050</article-id>
                <fpage>333</fpage>
                <lpage>342</lpage>
            </article-meta>
        </front>
    </article>

    OUT (CrossRef format) ->
    <pages>
        <first_page>333</first_page>
        <last_page>342</last_page>
    </pages>
    """
    _data = front_articlemeta_issue.ArticleMetaIssue(xml_tree).data

    page = ET.Element('pages')
    fpage = ET.Element('first_page')
    lpage = ET.Element('last_page')
    fpage.text = _data.get('fpage')
    lpage.text = _data.get('lpage')
    page.append(fpage)
    page.append(lpage)
    xml_crossref.find('./body/journal/journal_article').append(page)


def xml_crossref_pid_pipe(xml_crossref, xml_tree):
    """
    IN (SciELO format) ->
    <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink"
    article-type="research-article" dtd-version="1.0" specific-use="sps-1.6" xml:lang="pt">
        <front>
            <article-meta>
                <article-id pub-id-type="publisher-id" specific-use="scielo-v3">XZrRmc87LzCkDtLdcXwgztp</article-id>
                <article-id pub-id-type="publisher-id" specific-use="scielo-v2">S0103-21002017000400333</article-id>
                <article-id pub-id-type="publisher-id">1982-0194201700050</article-id>
                <article-id pub-id-type="doi">10.1590/1982-0194201700050</article-id>
            </article-meta>
        </front>
    </article>

    OUT (CrossRef format) ->
    <publisher_item>
        <identifier id_type="pii">S0103-21002017000400333</identifier>
    </publisher_item>
    """
    pid_v2 = article_ids.ArticleIds(xml_tree).v2

    identifier = ET.Element('identifier')
    identifier.set('id_type', 'pii')
    identifier.text = pid_v2

    publisher_item = ET.Element('publisher_item')
    publisher_item.append(identifier)

    xml_crossref.find('./body/journal/journal_article').append(publisher_item)


def xml_crossref_elocation_pipe(xml_crossref, xml_tree):
    """
    IN (SciELO format) ->
    <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink"
    article-type="research-article" dtd-version="1.0" specific-use="sps-1.6" xml:lang="pt">
        <front>
            <article-meta>
                <article-id pub-id-type="publisher-id" specific-use="scielo-v3">XZrRmc87LzCkDtLdcXwgztp</article-id>
                <article-id pub-id-type="publisher-id" specific-use="scielo-v2">S0103-21002017000400333</article-id>
                <article-id pub-id-type="publisher-id">1982-0194201700050</article-id>
                <article-id pub-id-type="doi">10.1590/1982-0194201700050</article-id>
                <elocation-id>e20210569</elocation-id>
            </article-meta>
        </front>
    </article>

    OUT (CrossRef format) ->
    <publisher_item>
        <item_number item_number_type="article_number">e20210569</item_number>
    </publisher_item>
    """
    _data = front_articlemeta_issue.ArticleMetaIssue(xml_tree).data

    publisher_item = ET.Element('publisher_item')
    item_number = ET.Element('item_number')
    item_number.set('item_number_type', 'article_number')
    item_number.text = _data.get('elocation_id')
    publisher_item.append(item_number)
    xml_crossref.find('./body/journal/journal_article').append(publisher_item)


def xml_crossref_permissions_pipe(xml_crossref, xml_tree):
    """
    IN (SciELO format) ->
    <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink"
    article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
    <front>
    <article-meta>
    <article-id specific-use="scielo-v3" pub-id-type="publisher-id">ZwzqmpTpbhTmtwR9GfDzP7c</article-id>
    <article-id specific-use="scielo-v2" pub-id-type="publisher-id">S0080-62342022000100445</article-id>
    <article-id pub-id-type="doi">10.1590/1980-220X-REEUSP-2021-0569en</article-id>
    <article-id pub-id-type="other">00445</article-id>
    <permissions>
    <license license-type="open-access" xlink:href="https://creativecommons.org/licenses/by/4.0/" xml:lang="en">
    <license-p>This is an Open Access article distributed under the terms of the Creative Commons Attribution License, which permits unrestricted use, distribution, and reproduction in any medium, provided the original work is properly cited.</license-p>
    </license>
    </permissions>
    </article-meta>
    </front>
    </article>

    OUT (CrossRef format) ->
    <doi_batch xmlns:ai="http://www.crossref.org/AccessIndicators.xsd" xmlns:jats="http://www.ncbi.nlm.nih.gov/JATS1"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://www.crossref.org/schema/4.4.0" version="4.4.0"
    xsi:schemaLocation="http://www.crossref.org/schema/4.4.0 http://www.crossref.org/schemas/crossref4.4.0.xsd">
    <body>
    <journal>
    <journal_article language="en" publication_type="full_text" reference_distribution_opts="any">
    <ai:program name="AccessIndicators">
    <ai:free_to_read/>
    <ai:license_ref applies_to="vor">http://creativecommons.org/licenses/by/4.0/</ai:license_ref>
    <ai:license_ref applies_to="am">http://creativecommons.org/licenses/by/4.0/</ai:license_ref>
    <ai:license_ref applies_to="tdm">http://creativecommons.org/licenses/by/4.0/</ai:license_ref>
    </ai:program>
    </journal_article>
    <journal_article language="pt" publication_type="full_text" reference_distribution_opts="any">
    <ai:program name="AccessIndicators">
    <ai:free_to_read/>
    <ai:license_ref applies_to="vor">http://creativecommons.org/licenses/by/4.0/</ai:license_ref>
    <ai:license_ref applies_to="am">http://creativecommons.org/licenses/by/4.0/</ai:license_ref>
    <ai:license_ref applies_to="tdm">http://creativecommons.org/licenses/by/4.0/</ai:license_ref>
    </ai:program>
    </journal_article>
    </journal>
    </body>
    </doi_batch>
    """
    art_license = article_license.ArticleLicense(xml_tree).licenses
    articles = article_and_subarticles.ArticleAndSubArticles(xml_tree).data

    for article in articles:
        free_to_read = ET.Element("{http://www.crossref.org/AccessIndicators.xsd}free_to_read")

        program = ET.Element("{http://www.crossref.org/AccessIndicators.xsd}program")
        program.set("name", "AccessIndicators")
        program.append(free_to_read)

        for context in ["vor", "am", "tdm"]:
            license_ref = ET.Element("{http://www.crossref.org/AccessIndicators.xsd}license_ref")
            license_ref.set("applies_to", context)
            license_ref.text = art_license[0].get('link')
            program.append(license_ref)

        xml_crossref.find(f"./body/journal/journal_article[@language='{article['lang']}']").append(program)


def xml_crossref_programrelateditem_pipe(xml_crossref, xml_tree):
    """
    IN (SciELO format) ->
    <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
    <front>
    <article-meta>
    <article-id specific-use="scielo-v3" pub-id-type="publisher-id">ZwzqmpTpbhTmtwR9GfDzP7c</article-id>
    <article-id specific-use="scielo-v2" pub-id-type="publisher-id">S0080-62342022000100445</article-id>
    <article-id pub-id-type="doi">10.1590/1980-220X-REEUSP-2021-0569en</article-id>
    <article-id pub-id-type="other">00445</article-id>
    <title-group>
    <article-title>
    Effects of an educational intervention with nursing professionals on approaches to hospitalized smokers: a quasi-experimental study
    <xref ref-type="fn" rid="FN1">*</xref>
    </article-title>
    <trans-title-group xml:lang="es">
    <trans-title>Efectos de una intervención educativa con profesionales de enfermería en el abordaje de pacientes fumadores: un estudio cuasi-experimental</trans-title>
    </trans-title-group>
    </title-group>
    </article-meta>
    </front>
    <sub-article article-type="translation" id="s1" xml:lang="pt">
    <front-stub>
    <article-id pub-id-type="doi">10.1590/1980-220X-REEUSP-2021-0569pt</article-id>
    <title-group>
    <article-title>
    Efeitos de uma intervenção educativa com profissionais de enfermagem sobre abordagens ao paciente tabagista: estudo quase-experimental
    <xref ref-type="fn" rid="FN2">*</xref>
    </article-title>
    </title-group>
    </front-stub>
    </sub-article>
    </article>

    OUT (CrossRef format) ->
    <doi_batch xmlns:ai="http://www.crossref.org/AccessIndicators.xsd" xmlns:jats="http://www.ncbi.nlm.nih.gov/JATS1" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://www.crossref.org/schema/4.4.0" version="4.4.0" xsi:schemaLocation="http://www.crossref.org/schema/4.4.0 http://www.crossref.org/schemas/crossref4.4.0.xsd">
    <body>
    <journal>
    <journal_article language="en" publication_type="full_text" reference_distribution_opts="any">
    <program xmlns="http://www.crossref.org/relations.xsd">
    <related_item>
    <description>Efeitos de uma intervenção educativa com profissionais de enfermagem sobre abordagens ao paciente tabagista: estudo quase-experimental</description>
    <intra_work_relation relationship-type="isTranslationOf" identifier-type="doi">10.1590/1980-220x-reeusp-2021-0569pt</intra_work_relation>
    </related_item>
    </program>
    </journal_article>
    <journal_article language="pt" publication_type="full_text" reference_distribution_opts="any">
    <program xmlns="http://www.crossref.org/relations.xsd">
    <related_item>
    <description>Effects of an educational intervention with nursing professionals on approaches to hospitalized smokers: a quasi-experimental study</description>
    <intra_work_relation relationship-type="hasTranslation" identifier-type="doi">10.1590/1980-220x-reeusp-2021-0569en</intra_work_relation>
    </related_item>
    </program>
    </journal_article>
    </journal>
    </body>
    </doi_batch>
    """
    art_titles = article_titles.ArticleTitles(xml_tree).article_title_dict
    art_lang = [lang.get('lang') for lang in article_and_subarticles.ArticleAndSubArticles(xml_tree).data]
    doi = {}
    for d in article_doi_with_lang.DoiWithLang(xml_tree).data:
        doi[d.get('lang')] = d.get('value')
    for lang in art_lang:
        related_item = ET.Element('related_item')

        orig_lang = 'pt' if lang == 'en' else 'en'
        description = ET.Element('description')
        description.text = art_titles.get(orig_lang)

        intra_work_relation = ET.Element('intra_work_relation')
        intra_work_relation_type = 'isTranslationOf' if lang == 'en' else 'hasTranslation'
        intra_work_relation.set('relationship-type', intra_work_relation_type)
        intra_work_relation.set('identifier-type', 'doi')
        intra_work_relation.text = doi.get(orig_lang)

        related_item.append(description)
        related_item.append(intra_work_relation)

        program = ET.Element('program')
        program.set('xmlns', 'http://www.crossref.org/relations.xsd')
        program.append(related_item)

        xml_crossref.find(f"./body/journal/journal_article[@language='{lang}']").append(program)


def xml_crossref_doidata_pipe(xml_crossref):
    for journal_article in xml_crossref.findall('./body/journal//journal_article'):
        doi_data = ET.Element('doi_data')
        journal_article.append(doi_data)


def xml_crossref_doi_pipe(xml_crossref, xml_tree):
    """
    OUT (CrossRef format) ->
    <doi_batch xmlns:ai="http://www.crossref.org/AccessIndicators.xsd" xmlns:jats="http://www.ncbi.nlm.nih.gov/JATS1" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://www.crossref.org/schema/4.4.0" version="4.4.0" xsi:schemaLocation="http://www.crossref.org/schema/4.4.0 http://www.crossref.org/schemas/crossref4.4.0.xsd">
    <body>
    <journal>
    <journal_article language="en" publication_type="full_text" reference_distribution_opts="any">
    <doi_data>
    <doi>10.1590/1980-220x-reeusp-2021-0569en</doi>
    <resource>http://www.scielo.br/scielo.php?script=sci_arttext&pid=S0080-62342022000100445&tlng=en</resource>
    <collection property="crawler-based">
    <item crawler="iParadigms">
    <resource>http://www.scielo.br/scielo.php?script=sci_pdf&pid=S0080-62342022000100445&tlng=en</resource>
    </item>
    </collection>
    </doi_data>
    </journal_article>
    <journal_article language="pt" publication_type="full_text" reference_distribution_opts="any">
    <doi_data>
    <doi>10.1590/1980-220x-reeusp-2021-0569pt</doi>
    <resource>http://www.scielo.br/scielo.php?script=sci_arttext&pid=S0080-62342022000100445&tlng=pt</resource>
    <collection property="crawler-based">
    <item crawler="iParadigms">
    <resource>http://www.scielo.br/scielo.php?script=sci_pdf&pid=S0080-62342022000100445&tlng=pt</resource>
    </item>
    </collection>
    </doi_data>
    </journal_article>
    </journal>
    </body>
    </doi_batch>
    """
    art_lang = [lang.get('lang') for lang in article_and_subarticles.ArticleAndSubArticles(xml_tree).data]
    dict_doi = {}
    for d in article_doi_with_lang.DoiWithLang(xml_tree).data:
        dict_doi[d.get('lang')] = d.get('value')
    for lang in art_lang:
        doi = ET.Element('doi')
        doi.text = dict_doi.get(lang)

        xml_crossref.find(f"./body/journal/journal_article[@language='{lang}']/doi_data").append(doi)


def xml_crossref_resource_pipe(xml_crossref, xml_tree):
    """
    IN (SciELO format) ->
    <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
    <front>
    <article-meta>
    <article-id specific-use="scielo-v3" pub-id-type="publisher-id">ZwzqmpTpbhTmtwR9GfDzP7c</article-id>
    <article-id specific-use="scielo-v2" pub-id-type="publisher-id">S0080-62342022000100445</article-id>
    <article-id pub-id-type="doi">10.1590/1980-220X-REEUSP-2021-0569en</article-id>
    <article-id pub-id-type="other">00445</article-id>
    </article-meta>
    </front>
    <sub-article article-type="translation" id="s1" xml:lang="pt">
    <front-stub>
    <article-id pub-id-type="doi">10.1590/1980-220X-REEUSP-2021-0569pt</article-id>
    </front-stub>
    </sub-article>
    </article>

    OUT (CrossRef format) ->
    <doi_batch xmlns:ai="http://www.crossref.org/AccessIndicators.xsd" xmlns:jats="http://www.ncbi.nlm.nih.gov/JATS1" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://www.crossref.org/schema/4.4.0" version="4.4.0" xsi:schemaLocation="http://www.crossref.org/schema/4.4.0 http://www.crossref.org/schemas/crossref4.4.0.xsd">
    <body>
    <journal>
    <journal_article language="en" publication_type="full_text" reference_distribution_opts="any">
    <doi_data>
    <doi>10.1590/1980-220x-reeusp-2021-0569en</doi>
    <resource>http://www.scielo.br/scielo.php?script=sci_arttext&pid=S0080-62342022000100445&tlng=en</resource>
    <collection property="crawler-based">
    <item crawler="iParadigms">
    <resource>http://www.scielo.br/scielo.php?script=sci_pdf&pid=S0080-62342022000100445&tlng=en</resource>
    </item>
    </collection>
    </doi_data>
    </journal_article>
    <journal_article language="pt" publication_type="full_text" reference_distribution_opts="any">
    <doi_data>
    <doi>10.1590/1980-220x-reeusp-2021-0569pt</doi>
    <resource>http://www.scielo.br/scielo.php?script=sci_arttext&pid=S0080-62342022000100445&tlng=pt</resource>
    <collection property="crawler-based">
    <item crawler="iParadigms">
    <resource>http://www.scielo.br/scielo.php?script=sci_pdf&pid=S0080-62342022000100445&tlng=pt</resource>
    </item>
    </collection>
    </doi_data>
    </journal_article>
    </journal>
    </body>
    </doi_batch>
    """
    url = 'http://www.scielo.br/scielo.php?script=sci_arttext&pid={}&tlng={}'

    art_lang = [lang.get('lang') for lang in article_and_subarticles.ArticleAndSubArticles(xml_tree).data]
    pid_v2 = article_ids.ArticleIds(xml_tree).v2

    for lang in art_lang:
        resource = ET.Element('resource')
        resource.text = url.format(pid_v2, lang)
        xml_crossref.find(f"./body/journal/journal_article[@language='{lang}']/doi_data").append(resource)


def xml_crossref_collection_pipe(xml_crossref, xml_tree):
    """
    IN (SciELO format) ->
    <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
    <front>
    <article-meta>
    <article-id specific-use="scielo-v3" pub-id-type="publisher-id">ZwzqmpTpbhTmtwR9GfDzP7c</article-id>
    <article-id specific-use="scielo-v2" pub-id-type="publisher-id">S0080-62342022000100445</article-id>
    <article-id pub-id-type="doi">10.1590/1980-220X-REEUSP-2021-0569en</article-id>
    <article-id pub-id-type="other">00445</article-id>
    </article-meta>
    </front>
    <sub-article article-type="translation" id="s1" xml:lang="pt">
    <front-stub>
    <article-id pub-id-type="doi">10.1590/1980-220X-REEUSP-2021-0569pt</article-id>
    </front-stub>
    </sub-article>
    </article>

    OUT (CrossRef format) ->
    <doi_batch xmlns:ai="http://www.crossref.org/AccessIndicators.xsd" xmlns:jats="http://www.ncbi.nlm.nih.gov/JATS1" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://www.crossref.org/schema/4.4.0" version="4.4.0" xsi:schemaLocation="http://www.crossref.org/schema/4.4.0 http://www.crossref.org/schemas/crossref4.4.0.xsd">
    <body>
    <journal>
    <journal_article language="en" publication_type="full_text" reference_distribution_opts="any">
    <doi_data>
    <doi>10.1590/1980-220x-reeusp-2021-0569en</doi>
    <resource>http://www.scielo.br/scielo.php?script=sci_arttext&pid=S0080-62342022000100445&tlng=en</resource>
    <collection property="crawler-based">
    <item crawler="iParadigms">
    <resource>http://www.scielo.br/scielo.php?script=sci_pdf&pid=S0080-62342022000100445&tlng=en</resource>
    </item>
    </collection>
    </doi_data>
    </journal_article>
    <journal_article language="pt" publication_type="full_text" reference_distribution_opts="any">
    <doi_data>
    <doi>10.1590/1980-220x-reeusp-2021-0569pt</doi>
    <resource>http://www.scielo.br/scielo.php?script=sci_arttext&pid=S0080-62342022000100445&tlng=pt</resource>
    <collection property="crawler-based">
    <item crawler="iParadigms">
    <resource>http://www.scielo.br/scielo.php?script=sci_pdf&pid=S0080-62342022000100445&tlng=pt</resource>
    </item>
    </collection>
    </doi_data>
    </journal_article>
    </journal>
    </body>
    </doi_batch>
    """
    url = 'http://www.scielo.br/scielo.php?script=sci_pdf&pid={}&tlng={}'

    art_lang = [lang.get('lang') for lang in article_and_subarticles.ArticleAndSubArticles(xml_tree).data]
    pid_v2 = article_ids.ArticleIds(xml_tree).v2

    for lang in art_lang:
        collection = ET.Element('collection')
        collection.set('property', 'crawler-based')

        item = ET.Element('item')
        item.set('crawler', 'iParadigms')

        resource = ET.Element('resource')
        resource.text = url.format(pid_v2, lang)

        item.append(resource)
        collection.append(item)
        xml_crossref.find(f"./body/journal/journal_article[@language='{lang}']/doi_data").append(collection)


def xml_crossref_close_pipe(xml_crossref):
    return '<?xml version="1.0" encoding="utf-8"?>' + ET.tostring(xml_crossref, encoding="utf-8", pretty_print=True).decode("utf-8")


def xml_crossref_articlecitations_pipe(xml_crossref, xml_tree):
    """
    IN (SciELO format) ->
    <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
    <back>
    <ref-list>
    <title>REFERENCES</title>
    <ref id="B1">
    <label>1.</label>
    <mixed-citation>
    1. Tran B, Falster MO, Douglas K, Blyth F, Jorm LR. Smoking and potentially preventable hospitalisation: the benefit of smoking cessation in older ages. Drug Alcohol Depend. 2015;150:85-91. DOI:
    <ext-link ext-link-type="uri" xlink:href="https://doi.org/10.1016/j.drugalcdep.2015.02.028">https://doi.org/10.1016/j.drugalcdep.2015.02.028</ext-link>
    </mixed-citation>
    <element-citation publication-type="journal">
    <person-group person-group-type="author">
    <name>
    <surname>Tran</surname>
    <given-names>B</given-names>
    </name>
    <name>
    <surname>Falster</surname>
    <given-names>MO</given-names>
    </name>
    <name>
    <surname>Douglas</surname>
    <given-names>K</given-names>
    </name>
    <name>
    <surname>Blyth</surname>
    <given-names>F</given-names>
    </name>
    <name>
    <surname>Jorm</surname>
    <given-names>LR</given-names>
    </name>
    </person-group>
    <article-title>Smoking and potentially preventable hospitalisation: the benefit of smoking cessation in older ages</article-title>
    <source>Drug Alcohol Depend.</source>
    <year>2015</year>
    <volume>150</volume>
    <fpage>85</fpage>
    <lpage>91</lpage>
    <comment>
    DOI:
    <ext-link ext-link-type="uri" xlink:href="https://doi.org/10.1016/j.drugalcdep.2015.02.028">https://doi.org/10.1016/j.drugalcdep.2015.02.028</ext-link>
    </comment>
    </element-citation>
    </ref>
    <ref id="B2">
    <label>2.</label>
    <mixed-citation>
    2. Kwon JA, Jeon W, Park EC, Kim JH, Kim SJ, Yoo KB, et al. Effects of disease detection on changes in smoking behavior. Yonsei Med J. 2015;56(4): 1143-9. DOI:
    <ext-link ext-link-type="uri" xlink:href="https://doi.org/10.3349/ymj.2015.56.4.1143">https://doi.org/10.3349/ymj.2015.56.4.1143</ext-link>
    </mixed-citation>
    <element-citation publication-type="journal">
    <person-group person-group-type="author">
    <name>
    <surname>Kwon</surname>
    <given-names>JA</given-names>
    </name>
    <name>
    <surname>Jeon</surname>
    <given-names>W</given-names>
    </name>
    <name>
    <surname>Park</surname>
    <given-names>EC</given-names>
    </name>
    <name>
    <surname>Kim</surname>
    <given-names>JH</given-names>
    </name>
    <name>
    <surname>Kim</surname>
    <given-names>SJ</given-names>
    </name>
    <name>
    <surname>Yoo</surname>
    <given-names>KB</given-names>
    </name>
    <etal/>
    </person-group>
    <article-title>Effects of disease detection on changes in smoking behavior</article-title>
    <source>Yonsei Med J.</source>
    <year>2015</year>
    <volume>56</volume>
    <issue>4</issue>
    <fpage>1143</fpage>
    <lpage>9</lpage>
    <comment>
    DOI:
    <ext-link ext-link-type="uri" xlink:href="https://doi.org/10.3349/ymj.2015.56.4.1143">https://doi.org/10.3349/ymj.2015.56.4.1143</ext-link>
    </comment>
    </element-citation>
    </ref>
    </ref-list>
    </back>
    </article>
    """

    """
    OUT (CrossRef format) ->
    <doi_batch xmlns:ai="http://www.crossref.org/AccessIndicators.xsd" xmlns:jats="http://www.ncbi.nlm.nih.gov/JATS1" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://www.crossref.org/schema/4.4.0" version="4.4.0" xsi:schemaLocation="http://www.crossref.org/schema/4.4.0 http://www.crossref.org/schemas/crossref4.4.0.xsd">
    <body>
    <journal>
    <journal_article language="en" publication_type="full_text" reference_distribution_opts="any">
    <citation_list>
    <citation key="ref1">
    <journal_title>Drug Alcohol Depend.</journal_title>
    <author>Tran B</author>
    <volume>150</volume>
    <first_page>85</first_page>
    <cYear>2015</cYear>
    <article_title>Smoking and potentially preventable hospitalisation: the benefit of smoking cessation in older ages</article_title>
    </citation>
    </citation_list>
    </journal_article>
    
    <journal_article language="pt" publication_type="full_text" reference_distribution_opts="any">
    <citation_list>
    <citation key="ref1">
    <journal_title>Drug Alcohol Depend.</journal_title>
    <author>Tran B</author>
    <volume>150</volume>
    <first_page>85</first_page>
    <cYear>2015</cYear>
    <article_title>Smoking and potentially preventable hospitalisation: the benefit of smoking cessation in older ages</article_title>
    </citation>
    </citation_list>
    </journal_article>
    </journal>
    </body>
    </doi_batch>
    """
    citations = article_citations.ArticleCitations(xml_tree).article_citations
    citation_list = ET.Element('citation_list')
    for item in citations:
        citation = get_citation(item)
        citation_list.append(citation)

    for journal_article in xml_crossref.findall('./body/journal//journal_article'):
        journal_article.append(deepcopy(citation_list))
