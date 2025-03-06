# coding: utf-8
import re
import uuid
from copy import deepcopy
from datetime import datetime

from lxml import etree as ET

from packtools.sps.models import (
    aff,
    article_abstract,
    article_and_subarticles,
    article_authors,
    references,
    article_doi_with_lang,
    article_ids,
    article_license,
    article_titles,
    dates,
    front_articlemeta_issue,
    journal_meta,
)

SUPPLBEG_REGEX = re.compile(r"^0 ")
SUPPLEND_REGEX = re.compile(r" 0$")


def get_timestamp():
    return datetime.now().strftime("%Y%m%d%H%M%S")


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
    if item.get("source") is not None:
        el = ET.Element("journal_title")
        el.text = item.get("source")
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
        main_author = item.get("main_author")
        el = ET.Element("author")
        el.text = " ".join([main_author.get("surname"), main_author.get("given-names")])
        citation.append(el)
    except (TypeError, AttributeError):
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
    if item.get("volume") is not None:
        el = ET.Element("volume")
        el.text = item.get("volume")
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
    if item.get("issue") is not None:
        el = ET.Element("issue")
        el.text = item.get("issue")
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
    if item.get("fpage") is not None:
        el = ET.Element("first_page")
        el.text = item.get("fpage")
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
    if item.get("year") is not None:
        el = ET.Element("cYear")
        el.text = item.get("year")
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
    if item.get("article_title") is not None:
        el = ET.Element("article_title")
        el.text = item.get("article_title")
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
    citation = ET.Element("citation")
    if item.get("label"):
        citation.set("key", "ref" + item.get("label"))

    create_journal_title(item, citation)
    create_author(item, citation)
    create_volume(item, citation)
    create_issue(item, citation)
    create_first_page(item, citation)
    create_year(item, citation)
    create_article_title(item, citation)

    return citation


def get_one_contributor(seq, author):
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
    person_name = ET.Element("person_name")
    person_name.set("contributor_role", author.get("contrib-type"))
    if seq == 0:
        person_name.set("sequence", "first")
    else:
        person_name.set("sequence", "additional")

    _given_name = author.get("given_names")
    if _given_name:
        given_name = ET.Element("given_name")
        given_name.text = _given_name
        person_name.append(given_name)

    _surname = author.get("surname")
    if _surname:
        surname = ET.Element("surname")
        surname.text = _surname
        person_name.append(surname)

    try:
        _author_aff = author.get("affs")[0]
        if _author_aff:
            affiliation = ET.Element("affiliation")
            affiliation.text = ", ".join(
                [_author_aff.get("orgname"), _author_aff.get("country_name")]
            )
            person_name.append(affiliation)
    except TypeError:
        pass

    _orcid = author.get("orcid")
    if _orcid:
        orcid = ET.Element("ORCID")
        orcid.text = "http://orcid.org/" + _orcid
        person_name.append(orcid)

    return person_name


def pipeline_crossref(xml_tree, data, pretty_print=True):
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

    xml_tree = ET.ElementTree(xml_crossref)
    return ET.tostring(xml_tree, pretty_print=pretty_print, encoding="utf-8").decode(
        "utf-8"
    )


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
        "ai": "http://www.crossref.org/AccessIndicators.xsd",
        "jats": "http://www.ncbi.nlm.nih.gov/JATS1",
        "xsi": "http://www.w3.org/2001/XMLSchema-instance",
        "xml": "http://www.w3.org/XML/1998/namespace",
    }

    el = ET.Element("doi_batch", nsmap=nsmap)
    el.set("version", "4.4.0")
    el.set("xmlns", "http://www.crossref.org/schema/4.4.0")
    el.set(
        "{http://www.w3.org/2001/XMLSchema-instance}schemaLocation",
        "http://www.crossref.org/schema/4.4.0 http://www.crossref.org/schemas/crossref4.4.0.xsd",
    )

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
    head = ET.Element("head")

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
    doi_batch_id = ET.Element("doi_batch_id")
    doi_batch_id.text = get_doi_batch_id()

    xml_crossref.find("./head").append(doi_batch_id)


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
    timestamp = ET.Element("timestamp")
    timestamp.text = get_timestamp()

    xml_crossref.find("./head").append(timestamp)


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
    depositor = ET.Element("depositor")
    depositor_name = ET.Element("depositor_name")
    email_address = ET.Element("email_address")

    depositor_name.text = data.get("depositor_name")
    email_address.text = data.get("depositor_email_address")

    depositor.append(depositor_name)
    depositor.append(email_address)

    xml_crossref.find("./head").append(depositor)


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
    registrant = ET.Element("registrant")
    registrant.text = data.get("registrant")

    xml_crossref.find("./head").append(registrant)


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
    body = ET.Element("body")

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
    journal = ET.Element("journal")

    xml_crossref.find("./body").append(journal)


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
    journal_metadata = ET.Element("journal_metadata")

    xml_crossref.find("./body/journal").append(journal_metadata)


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
    full_title = ET.Element("full_title")
    full_title.text = titles.journal_title

    xml_crossref.find("./body/journal/journal_metadata").append(full_title)


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
    abbrev_title = ET.Element("abbrev_title")
    abbrev_title.text = titles.abbreviated_journal_title

    xml_crossref.find("./body/journal/journal_metadata").append(abbrev_title)


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

    issn = ET.Element("issn")
    issn.text = issns.epub
    issn.set("media_type", "electronic")
    xml_crossref.find("./body/journal/journal_metadata").append(issn)

    issn = ET.Element("issn")
    issn.text = issns.ppub
    issn.set("media_type", "print")
    xml_crossref.find("./body/journal/journal_metadata").append(issn)


def xml_crossref_journalissue_pipe(xml_crossref):
    """
    Adiciona o elemento 'journal_issue' ao xml_crossref.

    Parameters
    ----------
    xml_crossref : lxml.etree._Element
        Elemento XML no padrão CrossRef em construção

    Returns
    -------
    <?xml version="1.0" encoding="UTF-8"?>
    <doi_batch ...>
       <body>
          <journal>
             <journal_issue />
          </journal>
       </body>
    </doi_batch>
    """
    journal_issue = ET.Element("journal_issue")

    xml_crossref.find("./body/journal").append(journal_issue)


def xml_crossref_pubdate_pipe(xml_crossref, xml_tree):
    """
    Adiciona o elemento 'publication_date' ao xml_crossref.

    Parameters
    ----------
    xml_crossref : lxml.etree._Element
        Elemento XML no padrão CrossRef em construção

    xml_tree : lxml.etree._Element
        Elemento XML no padrão SciELO com os dados de origem

    Returns
    -------
    <?xml version="1.0" encoding="UTF-8"?>
    <doi_batch>
       <body>
          <journal>
             <journal_issue>
                <publication_date media_type="online">
                   <year>2022</year>
                </publication_date>
             </journal_issue>
          </journal>
       </body>
    </doi_batch>
    """
    try:
        year = ET.Element("year")
        year.text = dates.ArticleDates(xml_tree).article_date.get("year")

        publication_date = ET.Element("publication_date")
        publication_date.set("media_type", "online")
        publication_date.append(year)

        xml_crossref.find("./body/journal/journal_issue").append(publication_date)

    except AttributeError:
        pass


def xml_crossref_journalvolume_pipe(xml_crossref):
    """
    Adiciona o elemento 'journal_volume' ao xml_crossref.

    Parameters
    ----------
    xml_crossref : lxml.etree._Element
        Elemento XML no padrão CrossRef em construção

    Returns
    -------
    <?xml version="1.0" encoding="UTF-8"?>
    <doi_batch ...>
       <body>
          <journal>
             <journal_issue>
                <journal_volume />
             </journal_issue>
          </journal>
       </body>
    </doi_batch>
    """
    journal_volume = ET.Element("journal_volume")

    xml_crossref.find("./body/journal/journal_issue").append(journal_volume)


def xml_crossref_volume_pipe(xml_crossref, xml_tree):
    """
    Adiciona o elemento 'volume' ao xml_crossref.

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
             <journal_issue>
                <journal_volume>
                   <volume>30</volume>
                </journal_volume>
             </journal_issue>
          </journal>
       </body>
    </doi_batch>
    """
    volume = ET.Element("volume")
    volume.text = front_articlemeta_issue.ArticleMetaIssue(xml_tree).volume

    xml_crossref.find("./body/journal/journal_issue/journal_volume").append(volume)


def xml_crossref_issue_pipe(xml_crossref, xml_tree):
    """
    Adiciona o elemento 'issue' ao xml_crossref.

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
             <journal_issue>
                <journal_volume>
                   <issue>4</issue>
                </journal_volume>
             </journal_issue>
          </journal>
       </body>
    </doi_batch>
    """
    issue = ET.Element("issue")
    issue.text = front_articlemeta_issue.ArticleMetaIssue(xml_tree).issue

    xml_crossref.find("./body/journal/journal_issue/journal_volume").append(issue)


def xml_crossref_journalarticle_pipe(xml_crossref, xml_tree):
    """
    Adiciona o elemento 'journal_article' ao xml_crossref.

    Parameters
    ----------
    xml_crossref : lxml.etree._Element
        Elemento XML no padrão CrossRef em construção

    xml_tree : lxml.etree._Element
        Elemento XML no padrão SciELO com os dados de origem

    Returns
    -------
    <?xml version="1.0" encoding="UTF-8"?>
    <doi_batch>
       <body>
          <journal>
             <journal_article language="en" publication_type="research-article" reference_distribution_opts="any" />
             <journal_article language="pt" publication_type="translation" reference_distribution_opts="any" />
          </journal>
       </body>
    </doi_batch>
    """
    articles = article_and_subarticles.ArticleAndSubArticles(xml_tree).data
    for article in articles:
        journal_article = ET.Element("journal_article")
        journal_article.set("language", article["lang"])
        journal_article.set("publication_type", article["article_type"])
        journal_article.set("reference_distribution_opts", "any")
        xml_crossref.find("./body/journal").append(journal_article)


def xml_crossref_articletitles_pipe(xml_crossref, xml_tree):
    """
    Adiciona o elemento 'titles' ao xml_crossref.

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
             <journal_article language="pt" publication_type="research-article" reference_distribution_opts="any">
                <titles>
                   <title>Impacto do monitoramento telefônico em pacientes com insuficiência cardíaca: ensaio clínico randomizado</title>
                   <original_language_title language="en">Impact of telephone monitoring on patients with heart failure: a randomized clinical trial</original_language_title>
                </titles>
             </journal_article>
             <journal_article language="en" publication_type="translation" reference_distribution_opts="any">
                <titles>
                   <title>Impact of telephone monitoring on patients with heart failure: a randomized clinical trial</title>
                   <original_language_title language="pt">Impacto do monitoramento telefônico em pacientes com insuficiência cardíaca: ensaio clínico randomizado</original_language_title>
                </titles>
             </journal_article>
          </journal>
       </body>
    </doi_batch>
    """
    art_titles = article_titles.ArticleTitles(xml_tree).article_title_dict
    art_lang = [
        lang.get("lang")
        for lang in article_and_subarticles.ArticleAndSubArticles(xml_tree).data
    ]

    for lang in art_lang:
        titles = ET.Element("titles")
        title = ET.Element("title")
        title.text = art_titles.get(lang)
        titles.append(title)
        original_language_title = ET.Element("original_language_title")
        orig_lang = "pt" if lang == "en" else "en"
        original_language_title.set("language", orig_lang)
        original_language_title.text = art_titles.get(orig_lang)
        titles.append(original_language_title)
        xml_crossref.find(f"./body/journal/journal_article[@language='{lang}']").append(
            titles
        )


def xml_crossref_articlecontributors_pipe(xml_crossref, xml_tree):
    """
    Adiciona o elemento 'contributors' ao xml_crossref.

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
             <journal_article language="pt" publication_type="research-article" reference_distribution_opts="any">
                <contributors>
                   <person_name contributor_role="author" sequence="first">
                      <given_name>Josiana Araujo de</given_name>
                      <surname>Oliveira</surname>
                      <affiliation>Universidade do Estado do Rio de Janeiro, Brasil</affiliation>
                   </person_name>
                   <person_name contributor_role="author" sequence="additional">
                      <given_name>Ricardo Gonçalves</given_name>
                      <surname>Cordeiro</surname>
                      <affiliation>Universidade do Estado do Rio de Janeiro, Brasil</affiliation>
                   </person_name>
                   <person_name contributor_role="author" sequence="additional">
                      <given_name>Ronilson Gonçalves</given_name>
                      <surname>Rocha</surname>
                      <affiliation>Universidade do Estado do Rio de Janeiro, Brasil</affiliation>
                   </person_name>
                   <person_name contributor_role="author" sequence="additional">
                      <given_name>Tereza Cristina Felippe</given_name>
                      <surname>Guimarães</surname>
                      <affiliation>Instituto Nacional de Cardiologia, Brasil</affiliation>
                   </person_name>
                   <person_name contributor_role="author" sequence="additional">
                      <given_name>Denilson Campos de</given_name>
                      <surname>Albuquerque</surname>
                      <affiliation>Universidade do Estado do Rio de Janeiro, Brasil</affiliation>
                   </person_name>
                </contributors>
             </journal_article>
             <journal_article language="en" publication_type="translation" reference_distribution_opts="any">
                <contributors>
                   <person_name contributor_role="author" sequence="first">
                      <given_name>Josiana Araujo de</given_name>
                      <surname>Oliveira</surname>
                      <affiliation>Universidade do Estado do Rio de Janeiro, Brasil</affiliation>
                   </person_name>
                   <person_name contributor_role="author" sequence="additional">
                      <given_name>Ricardo Gonçalves</given_name>
                      <surname>Cordeiro</surname>
                      <affiliation>Universidade do Estado do Rio de Janeiro, Brasil</affiliation>
                   </person_name>
                   <person_name contributor_role="author" sequence="additional">
                      <given_name>Ronilson Gonçalves</given_name>
                      <surname>Rocha</surname>
                      <affiliation>Universidade do Estado do Rio de Janeiro, Brasil</affiliation>
                   </person_name>
                   <person_name contributor_role="author" sequence="additional">
                      <given_name>Tereza Cristina Felippe</given_name>
                      <surname>Guimarães</surname>
                      <affiliation>Instituto Nacional de Cardiologia, Brasil</affiliation>
                   </person_name>
                   <person_name contributor_role="author" sequence="additional">
                      <given_name>Denilson Campos de</given_name>
                      <surname>Albuquerque</surname>
                      <affiliation>Universidade do Estado do Rio de Janeiro, Brasil</affiliation>
                   </person_name>
                </contributors>
             </journal_article>
          </journal>
       </body>
    </doi_batch>
    """
    articles = article_and_subarticles.ArticleAndSubArticles(xml_tree)
    article_data = articles.data
    article_nodes = articles.article
    for article_node in article_nodes:
        authors = list(article_authors.Authors(article_node).contribs_with_affs)
    contributors = ET.Element("contributors")
    for seq, author in enumerate(authors):
        person_name = get_one_contributor(seq, author)
        contributors.append(person_name)

    for article in article_data:
        if article.get("article_type") != "reviewer-report":
            xml_crossref.find(
                f"./body/journal/journal_article[@language='{article['lang']}']"
            ).append(deepcopy(contributors))


def xml_crossref_articleabstract_pipe(xml_crossref, xml_tree):
    """
    Adiciona o elemento 'abstract' ao xml_crossref.

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
             <journal_article language="pt" publication_type="research-article" reference_distribution_opts="any">
                <jats:abstract xml:lang="pt">
                   <jats:p>Resumo Objetivo Analisar o autocuidado e o conhecimento em pacientes com insuficiência cardíaca monitorados por contato telefônico e analisar a correlação do conhecimento com o autocuidado. Métodos Ensaio clínico randomizado, realizado em uma clínica especializada, no período de abril de 2015 a dezembro de 2015. Foram monitorados e randomizados 36 pacientes no Grupo Controle (17) ou no Grupo Intervenção (19). Ambos os grupos participaram do monitoramento convencional, compreendendo três atendimentos (Basal; 2° mês; 4° mês); no Grupo Intervenção houve associação do monitoramento telefônico por meio de um guia padronizado. Foram utilizados os Questionários de Conhecimento e de Autocuidado para avaliação dos desfechos primários e secundários. Resultados Houve diferença no conhecimento (12,7±1,7 vs. 10,8±2,2; p=0,009) e autocuidado (25,4±6,6 vs. 29,5±4,8; p=0,04) no 4° mês; correlação negativa entre os escores do conhecimento e autocuidado no 2° mês (r=-0,48; p=0,03). Conclusão O monitoramento convencional combinado ao monitoramento telefônico mostra-se eficaz no 4° mês com a melhoria do conhecimento e autocuidado de pacientes com insuficiência cardíaca e correlação significativa desses desfechos no 2° mês.</jats:p>
                </jats:abstract>
                <jats:abstract xml:lang="en">
                   <jats:p>Abstract Objective To analyze self-care and knowledge in patients with heart failure who were monitored telephonically, and to analyze the correlation of knowledge with self-care. Methods It was a randomized clinical trial, performed in a specialized clinic from April of 2015 to December of 2015. Thirty-six patients were monitored and randomized, with 17 in the control group and 19 in the intervention group. Both groups participated in the conventional monitoring, which included three visits (initial, second and fourth month); the intervention group was associated with telephone support by means of a standardized guide. The Knowledge and Self-Care Questionnaires were used to evaluate the primary and secondary outcomes. Results Difference in knowledge (12.7±1.7 vs. 10.8±2.2, p=0.009) and self-care (25.4±6.6 vs. 29.5±4.8, p=0. 04) were identified in the fourth month; and there was a negative correlation between knowledge and self-care scores in the second month (r =-0.48; p=0.03). Conclusion The conventional management combined with telephone monitoring was effective in the 4&lt;sup xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink"&gt;th&lt;/sup&gt; month with improved knowledge and self-care of patients with heart failure and a significant correlation of these outcomes in the second month.</jats:p>
                </jats:abstract>
             </journal_article>
             <journal_article language="en" publication_type="translation" reference_distribution_opts="any">
                <jats:abstract xml:lang="pt">
                   <jats:p>Resumo Objetivo Analisar o autocuidado e o conhecimento em pacientes com insuficiência cardíaca monitorados por contato telefônico e analisar a correlação do conhecimento com o autocuidado. Métodos Ensaio clínico randomizado, realizado em uma clínica especializada, no período de abril de 2015 a dezembro de 2015. Foram monitorados e randomizados 36 pacientes no Grupo Controle (17) ou no Grupo Intervenção (19). Ambos os grupos participaram do monitoramento convencional, compreendendo três atendimentos (Basal; 2° mês; 4° mês); no Grupo Intervenção houve associação do monitoramento telefônico por meio de um guia padronizado. Foram utilizados os Questionários de Conhecimento e de Autocuidado para avaliação dos desfechos primários e secundários. Resultados Houve diferença no conhecimento (12,7±1,7 vs. 10,8±2,2; p=0,009) e autocuidado (25,4±6,6 vs. 29,5±4,8; p=0,04) no 4° mês; correlação negativa entre os escores do conhecimento e autocuidado no 2° mês (r=-0,48; p=0,03). Conclusão O monitoramento convencional combinado ao monitoramento telefônico mostra-se eficaz no 4° mês com a melhoria do conhecimento e autocuidado de pacientes com insuficiência cardíaca e correlação significativa desses desfechos no 2° mês.</jats:p>
                </jats:abstract>
                <jats:abstract xml:lang="en">
                   <jats:p>Abstract Objective To analyze self-care and knowledge in patients with heart failure who were monitored telephonically, and to analyze the correlation of knowledge with self-care. Methods It was a randomized clinical trial, performed in a specialized clinic from April of 2015 to December of 2015. Thirty-six patients were monitored and randomized, with 17 in the control group and 19 in the intervention group. Both groups participated in the conventional monitoring, which included three visits (initial, second and fourth month); the intervention group was associated with telephone support by means of a standardized guide. The Knowledge and Self-Care Questionnaires were used to evaluate the primary and secondary outcomes. Results Difference in knowledge (12.7±1.7 vs. 10.8±2.2, p=0.009) and self-care (25.4±6.6 vs. 29.5±4.8, p=0. 04) were identified in the fourth month; and there was a negative correlation between knowledge and self-care scores in the second month (r =-0.48; p=0.03). Conclusion The conventional management combined with telephone monitoring was effective in the 4&lt;sup xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink"&gt;th&lt;/sup&gt; month with improved knowledge and self-care of patients with heart failure and a significant correlation of these outcomes in the second month.</jats:p>
                </jats:abstract>
             </journal_article>
          </journal>
       </body>
    </doi_batch>
    """
    abstracts = article_abstract.Abstract(xml_tree).get_abstracts(None)
    articles = article_and_subarticles.ArticleAndSubArticles(xml_tree).data

    for article in articles:
        for abstract, lang in [(item.get("abstract"), item.get("lang")) for item in abstracts]:
            if abstract:
                jats = ET.Element("{http://www.ncbi.nlm.nih.gov/JATS1}abstract")
                jats.set("{http://www.w3.org/XML/1998/namespace}lang", lang)
                jats_p = ET.Element("{http://www.ncbi.nlm.nih.gov/JATS1}p")
                text = [abstract.get("title")] if abstract.get("title") else []
                try:
                    for item in abstract.get("sections"):
                        text.append(item.get("title"))
                        text.append(item.get("p"))
                except TypeError:
                    text.append(abstract.get("title"))
                    text.append(abstract.get("p"))
                jats_p.text = " ".join([item for item in text if item])
                jats.append(jats_p)
                xml_crossref.find(
                    f"./body/journal/journal_article[@language='{article['lang']}']"
                ).append(deepcopy(jats))


def xml_crossref_articlepubdate_pipe(xml_crossref, xml_tree):
    """
    Adiciona o elemento 'publication_date' ao xml_crossref.

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
             <journal_article language="pt" publication_type="research-article" reference_distribution_opts="any">
                <publication_date media_type="online">
                   <year>2017</year>
                </publication_date>
             </journal_article>
             <journal_article language="en" publication_type="translation" reference_distribution_opts="any">
                <publication_date media_type="online">
                   <year>2017</year>
                </publication_date>
             </journal_article>
          </journal>
       </body>
    </doi_batch>
    """
    articles = article_and_subarticles.ArticleAndSubArticles(xml_tree).data
    pub_date = dates.ArticleDates(xml_tree).collection_date

    for article in articles:
        publication_date = ET.Element("publication_date")
        publication_date.set("media_type", "online")

        year = ET.Element("year")
        year.text = pub_date.get("year")

        publication_date.append(year)

        xml_crossref.find(
            f"./body/journal/journal_article[@language='{article['lang']}']"
        ).append(publication_date)


def xml_crossref_pages_pipe(xml_crossref, xml_tree):
    """
    Adiciona o elemento 'pages' ao xml_crossref.

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
             <journal_article language="pt" publication_type="research-article" reference_distribution_opts="any">
                <pages>
                   <first_page>333</first_page>
                   <last_page>342</last_page>
                </pages>
             </journal_article>
          </journal>
       </body>
    </doi_batch>
    """
    _data = front_articlemeta_issue.ArticleMetaIssue(xml_tree).data

    page = ET.Element("pages")
    fpage = ET.Element("first_page")
    lpage = ET.Element("last_page")
    fpage.text = _data.get("fpage")
    lpage.text = _data.get("lpage")
    page.append(fpage)
    page.append(lpage)
    xml_crossref.find("./body/journal/journal_article").append(page)


def xml_crossref_pid_pipe(xml_crossref, xml_tree):
    """
    Adiciona o elemento 'publisher_item' ao xml_crossref.

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
             <journal_article language="pt" publication_type="research-article" reference_distribution_opts="any">
                <publisher_item>
                   <identifier id_type="pii">S0103-21002017000400333</identifier>
                </publisher_item>
             </journal_article>
          </journal>
       </body>
    </doi_batch>
    """
    pid_v2 = article_ids.ArticleIds(xml_tree).v2

    identifier = ET.Element("identifier")
    identifier.set("id_type", "pii")
    identifier.text = pid_v2

    publisher_item = ET.Element("publisher_item")
    publisher_item.append(identifier)

    xml_crossref.find("./body/journal/journal_article").append(publisher_item)


def xml_crossref_elocation_pipe(xml_crossref, xml_tree):
    """
    Adiciona o elemento 'item_number' ao xml_crossref.

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
             <journal_article language="pt" publication_type="research-article" reference_distribution_opts="any">
                <publisher_item>
                   <item_number item_number_type="article_number" />
                </publisher_item>
             </journal_article>
          </journal>
       </body>
    </doi_batch>
    """
    _data = front_articlemeta_issue.ArticleMetaIssue(xml_tree).data

    item_number = ET.Element("item_number")
    item_number.set("item_number_type", "article_number")
    item_number.text = _data.get("elocation_id")
    xml_crossref.find("./body/journal/journal_article/publisher_item").append(
        item_number
    )


def xml_crossref_permissions_pipe(xml_crossref, xml_tree):
    """
    Adiciona o elemento 'program' ao xml_crossref.

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
             <journal_article language="pt" publication_type="research-article" reference_distribution_opts="any">
                <ai:program name="AccessIndicators">
                   <ai:free_to_read />
                   <ai:license_ref applies_to="vor">https://creativecommons.org/licenses/by/4.0/</ai:license_ref>
                   <ai:license_ref applies_to="am">https://creativecommons.org/licenses/by/4.0/</ai:license_ref>
                   <ai:license_ref applies_to="tdm">https://creativecommons.org/licenses/by/4.0/</ai:license_ref>
                </ai:program>
             </journal_article>
             <journal_article language="en" publication_type="translation" reference_distribution_opts="any">
                <ai:program name="AccessIndicators">
                   <ai:free_to_read />
                   <ai:license_ref applies_to="vor">https://creativecommons.org/licenses/by/4.0/</ai:license_ref>
                   <ai:license_ref applies_to="am">https://creativecommons.org/licenses/by/4.0/</ai:license_ref>
                   <ai:license_ref applies_to="tdm">https://creativecommons.org/licenses/by/4.0/</ai:license_ref>
                </ai:program>
             </journal_article>
          </journal>
       </body>
    </doi_batch>
    """
    art_license = article_license.ArticleLicense(xml_tree).licenses
    articles = article_and_subarticles.ArticleAndSubArticles(xml_tree).data

    for article in articles:
        free_to_read = ET.Element(
            "{http://www.crossref.org/AccessIndicators.xsd}free_to_read"
        )

        program = ET.Element("{http://www.crossref.org/AccessIndicators.xsd}program")
        program.set("name", "AccessIndicators")
        program.append(free_to_read)

        for context in ["vor", "am", "tdm"]:
            license_ref = ET.Element(
                "{http://www.crossref.org/AccessIndicators.xsd}license_ref"
            )
            license_ref.set("applies_to", context)
            license_ref.text = art_license[0].get("link")
            program.append(license_ref)

        xml_crossref.find(
            f"./body/journal/journal_article[@language='{article['lang']}']"
        ).append(program)


def xml_crossref_programrelateditem_pipe(xml_crossref, xml_tree):
    """
    Adiciona o elemento 'program' ao xml_crossref.

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
             <journal_article language="pt" publication_type="research-article" reference_distribution_opts="any">
                <program xmlns="http://www.crossref.org/relations.xsd">
                   <related_item>
                      <description>Impact of telephone monitoring on patients with heart failure: a randomized clinical trial</description>
                      <intra_work_relation relationship-type="hasTranslation" identifier-type="doi" />
                   </related_item>
                </program>
             </journal_article>
             <journal_article language="en" publication_type="translation" reference_distribution_opts="any">
                <program xmlns="http://www.crossref.org/relations.xsd">
                   <related_item>
                      <description>Impacto do monitoramento telefônico em pacientes com insuficiência cardíaca: ensaio clínico randomizado</description>
                      <intra_work_relation relationship-type="isTranslationOf" identifier-type="doi">10.1590/1982-0194201700050</intra_work_relation>
                   </related_item>
                </program>
             </journal_article>
          </journal>
       </body>
    </doi_batch>
    """
    art_titles = article_titles.ArticleTitles(xml_tree).article_title_dict
    art_lang = [
        lang.get("lang")
        for lang in article_and_subarticles.ArticleAndSubArticles(xml_tree).data
    ]
    doi = {}
    for d in article_doi_with_lang.DoiWithLang(xml_tree).data:
        doi[d.get("lang")] = d.get("value")
    for lang in art_lang:
        related_item = ET.Element("related_item")

        orig_lang = "pt" if lang == "en" else "en"
        description = ET.Element("description")
        description.text = art_titles.get(orig_lang)

        intra_work_relation = ET.Element("intra_work_relation")
        intra_work_relation_type = (
            "isTranslationOf" if lang == "en" else "hasTranslation"
        )
        intra_work_relation.set("relationship-type", intra_work_relation_type)
        intra_work_relation.set("identifier-type", "doi")
        intra_work_relation.text = doi.get(orig_lang)

        related_item.append(description)
        related_item.append(intra_work_relation)

        program = ET.Element("program")
        program.set("xmlns", "http://www.crossref.org/relations.xsd")
        program.append(related_item)

        xml_crossref.find(f"./body/journal/journal_article[@language='{lang}']").append(
            program
        )


def xml_crossref_doidata_pipe(xml_crossref):
    """
    Adiciona o elemento 'doi_data' ao xml_crossref.

    Parameters
    ----------
    xml_crossref : lxml.etree._Element
        Elemento XML no padrão CrossRef em construção

    Returns
    -------
    <?xml version="1.0" encoding="UTF-8"?>
    <doi_batch ...>
       <body>
          <journal>
             <journal_article language="pt" publication_type="research-article" reference_distribution_opts="any">
                <doi_data />
             </journal_article>
             <journal_article language="en" publication_type="translation" reference_distribution_opts="any">
                <doi_data />
             </journal_article>
          </journal>
       </body>
    </doi_batch>
    """
    for journal_article in xml_crossref.findall("./body/journal//journal_article"):
        doi_data = ET.Element("doi_data")
        journal_article.append(doi_data)


def xml_crossref_doi_pipe(xml_crossref, xml_tree):
    """
    Adiciona o elemento 'doi' ao xml_crossref.

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
             <journal_article language="pt" publication_type="research-article" reference_distribution_opts="any">
                <doi_data>
                   <doi>10.1590/1982-0194201700050</doi>
                </doi_data>
             </journal_article>
             <journal_article language="en" publication_type="translation" reference_distribution_opts="any">
                <doi_data>
                   <doi />
                </doi_data>
             </journal_article>
          </journal>
       </body>
    </doi_batch>
    """
    art_lang = [
        lang.get("lang")
        for lang in article_and_subarticles.ArticleAndSubArticles(xml_tree).data
    ]
    dict_doi = {}
    for d in article_doi_with_lang.DoiWithLang(xml_tree).data:
        dict_doi[d.get("lang")] = d.get("value")
    for lang in art_lang:
        doi = ET.Element("doi")
        doi.text = dict_doi.get(lang)

        xml_crossref.find(
            f"./body/journal/journal_article[@language='{lang}']/doi_data"
        ).append(doi)


def xml_crossref_resource_pipe(xml_crossref, xml_tree):
    """
    Adiciona o elemento 'doi' ao xml_crossref.

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
             <journal_article language="pt" publication_type="research-article" reference_distribution_opts="any">
                <doi_data>
                   <resource>http://www.scielo.br/scielo.php?script=sci_arttext&amp;pid=S0103-21002017000400333&amp;tlng=pt</resource>
                </doi_data>
             </journal_article>
             <journal_article language="en" publication_type="translation" reference_distribution_opts="any">
                <doi_data>
                   <resource>http://www.scielo.br/scielo.php?script=sci_arttext&amp;pid=S0103-21002017000400333&amp;tlng=en</resource>
                </doi_data>
             </journal_article>
          </journal>
       </body>
    </doi_batch>
    """
    url = "http://www.scielo.br/scielo.php?script=sci_arttext&pid={}&tlng={}"

    art_lang = [
        lang.get("lang")
        for lang in article_and_subarticles.ArticleAndSubArticles(xml_tree).data
    ]
    pid_v2 = article_ids.ArticleIds(xml_tree).v2

    for lang in art_lang:
        resource = ET.Element("resource")
        resource.text = url.format(pid_v2, lang)
        xml_crossref.find(
            f"./body/journal/journal_article[@language='{lang}']/doi_data"
        ).append(resource)


def xml_crossref_collection_pipe(xml_crossref, xml_tree):
    """
    Adiciona o elemento 'collection' ao xml_crossref.

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
             <journal_article language="pt" publication_type="research-article" reference_distribution_opts="any">
                <doi_data>
                   <collection property="crawler-based">
                      <item crawler="iParadigms">
                         <resource>http://www.scielo.br/scielo.php?script=sci_pdf&amp;pid=S0103-21002017000400333&amp;tlng=pt</resource>
                      </item>
                   </collection>
                </doi_data>
             </journal_article>
             <journal_article language="en" publication_type="translation" reference_distribution_opts="any">
                <doi_data>
                   <collection property="crawler-based">
                      <item crawler="iParadigms">
                         <resource>http://www.scielo.br/scielo.php?script=sci_pdf&amp;pid=S0103-21002017000400333&amp;tlng=en</resource>
                      </item>
                   </collection>
                </doi_data>
             </journal_article>
          </journal>
       </body>
    </doi_batch>
    """
    url = "http://www.scielo.br/scielo.php?script=sci_pdf&pid={}&tlng={}"

    art_lang = [
        lang.get("lang")
        for lang in article_and_subarticles.ArticleAndSubArticles(xml_tree).data
    ]
    pid_v2 = article_ids.ArticleIds(xml_tree).v2

    for lang in art_lang:
        collection = ET.Element("collection")
        collection.set("property", "crawler-based")

        item = ET.Element("item")
        item.set("crawler", "iParadigms")

        resource = ET.Element("resource")
        resource.text = url.format(pid_v2, lang)

        item.append(resource)
        collection.append(item)
        xml_crossref.find(
            f"./body/journal/journal_article[@language='{lang}']/doi_data"
        ).append(collection)


def xml_crossref_close_pipe(xml_crossref):
    return '<?xml version="1.0" encoding="utf-8"?>' + ET.tostring(
        xml_crossref, encoding="utf-8", pretty_print=True
    ).decode("utf-8")


def xml_crossref_articlecitations_pipe(xml_crossref, xml_tree):
    """
    Adiciona o elemento 'citation_list' ao xml_crossref.

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
             <journal_article language="pt" publication_type="research-article" reference_distribution_opts="any">
                <citation_list>
                   <citation key="ref">
                      <journal_title>Circulation</journal_title>
                      <author>Go AS</author>
                      <volume>129</volume>
                      <issue>3</issue>
                      <first_page>e28</first_page>
                      <cYear>2014</cYear>
                      <article_title>Heart disease and stroke statistics-2014 update: a report from the American Heart Association</article_title>
                   </citation>
                   <citation key="ref">
                      <journal_title>Arq Bras Cardiol</journal_title>
                      <author>Albuquerque DC</author>
                      <volume>104</volume>
                      <issue>6</issue>
                      <first_page>433</first_page>
                      <cYear>2015</cYear>
                      <article_title>I Brazilian Registry of Heart Failure - clinical aspects, care quality and hospitalization outcomes</article_title>
                   </citation>
                </citation_list>
             </journal_article>
             <journal_article language="en" publication_type="translation" reference_distribution_opts="any">
                <citation_list>
                   <citation key="ref">
                      <journal_title>Circulation</journal_title>
                      <author>Go AS</author>
                      <volume>129</volume>
                      <issue>3</issue>
                      <first_page>e28</first_page>
                      <cYear>2014</cYear>
                      <article_title>Heart disease and stroke statistics-2014 update: a report from the American Heart Association</article_title>
                   </citation>
                   <citation key="ref">
                      <journal_title>Arq Bras Cardiol</journal_title>
                      <author>Albuquerque DC</author>
                      <volume>104</volume>
                      <issue>6</issue>
                      <first_page>433</first_page>
                      <cYear>2015</cYear>
                      <article_title>I Brazilian Registry of Heart Failure - clinical aspects, care quality and hospitalization outcomes</article_title>
                   </citation>
                </citation_list>
             </journal_article>
          </journal>
       </body>
    </doi_batch>
    """
    citations = references.XMLREferences(xml_tree).main_references
    citation_list = ET.Element("citation_list")
    for item in citations:
        citation = get_citation(item)
        citation_list.append(citation)

    for journal_article in xml_crossref.findall("./body/journal//journal_article"):
        journal_article.append(deepcopy(citation_list))
