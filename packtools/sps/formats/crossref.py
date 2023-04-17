# coding: utf-8
from lxml import etree as ET
import re
import os
import uuid
from copy import deepcopy
from datetime import datetime

from packtools.sps.models import (
    journal_meta,
    dates,
    front_articlemeta_issue,
    article_and_subarticles,
    article_authors,
    aff,
)

SUPPLBEG_REGEX = re.compile(r'^0 ')
SUPPLEND_REGEX = re.compile(r' 0$')


def get_timestamp():
    return datetime.now().strftime('%Y%m%d%H%M%S')


def get_doi_batch_id():
    return uuid.uuid4().hex


def pipeline_crossref(xml_tree, data):
    xml_crossref = setupdoibatch_pipe()
    xml_head_pipe(xml_crossref)
    xml_doibatchid_pipe(xml_crossref, data)
    xml_timestamp_pipe(xml_crossref, data)
    xml_depositor_pipe(xml_crossref, data)
    xml_registrant_pipe(xml_crossref, data)
    xml_body_pipe(xml_crossref)
    xml_journal_pipe(xml_crossref)
    xml_journalmetadata_pipe(xml_crossref)
    xml_journaltitle_pipe(xml_tree, xml_crossref)
    xml_abbreviatedjournaltitle_pipe(xml_tree, xml_crossref)
    xml_issn_pipe(xml_tree, xml_crossref)
    xml_journalissue_pipe(xml_crossref)
    xml_pubdate_pipe(xml_tree, xml_crossref)
    xml_journalvolume_pipe(xml_crossref)
    xml_volume_pipe(xml_tree, xml_crossref)
    xml_issue_pipe(xml_tree, xml_crossref)
    xml_journalarticle_pipe(xml_tree, xml_crossref)
    # xml_articletitles_pipe(xml_tree, xml_crossref)
    # xml_articletitle_pipe(xml_tree, xml_crossref)
    xml_articlecontributors_pipe(xml_tree, xml_crossref)
    # xml_articleabstract_pipe(xml_tree, xml_crossref)
    # xml_articlepubdate_pipe(xml_tree, xml_crossref)
    # xml_pages_pipe(xml_tree, xml_crossref)
    # xml_pid_pipe(xml_tree, xml_crossref)
    # xml_elocation_pipe(xml_tree, xml_crossref)
    # xml_permissions_pipe(xml_tree, xml_crossref)
    # xml_programrelateditem_pipe(xml_tree, xml_crossref)
    # xml_doidata_pipe(xml_tree, xml_crossref)
    # xml_doi_pipe(xml_tree, xml_crossref)
    # xml_resource_pipe(xml_tree, xml_crossref)
    # xml_collection_pipe(xml_tree, xml_crossref)
    # xml_articlecitations_pipe(xml_tree, xml_crossref)
    # xml_close_pipe(xml_tree, xml_crossref)

    return xml_crossref


def setupdoibatch_pipe():
    """
    <doi_batch xmlns:ai="http://www.crossref.org/AccessIndicators.xsd"
    xmlns:jats="http://www.ncbi.nlm.nih.gov/JATS1"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xmlns="http://www.crossref.org/schema/4.4.0"
    xsi:schemaLocation="http://www.crossref.org/schema/4.4.0 http://www.crossref.org/schemas/crossref4.4.0.xsd"/>
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


def xml_head_pipe(xml_crossref):
    head = ET.Element('head')

    xml_crossref.append(head)


def xml_doibatchid_pipe(xml_crossref):
    """
    <head>
        <doi_batch_id>49d374553c5d48c0bdd54d25080e0045</doi_batch_id>
    </head>
    """

    doi_batch_id = ET.Element('doi_batch_id')
    doi_batch_id.text = get_doi_batch_id()

    xml_crossref.find('./head').append(doi_batch_id)


def xml_timestamp_pipe(xml_crossref, data):
    """
            data = {
                        "timestamp": 20230405112328
                    }

            <head>
                <timestamp>20230405112328</timestamp>
            </head>
            """

    timestamp = ET.Element('timestamp')
    timestamp.text = data.get('timestamp')
    # todo
    # timestamp.text = datetime.now().strftime('%Y%m%d%H%M%S')

    xml_crossref.find('./head').append(timestamp)


def xml_depositor_pipe(xml_crossref, data):
    """
            data = {
                        "depositor_name": depositor,
                        "depositor_email_address": name@domain.com
                    }

            <head>
                <depositor>
                    <depositor_name>depositor</depositor_name>
                    <email_address>name@domain.com</email_address>
                </depositor>
            </head>
            """

    depositor = ET.Element('depositor')
    depositor_name = ET.Element('depositor_name')
    email_address = ET.Element('email_address')

    depositor_name.text = data.get('depositor_name')
    email_address.text = data.get('depositor_email_address')

    depositor.append(depositor_name)
    depositor.append(email_address)

    xml_crossref.find('./head').append(depositor)


def xml_registrant_pipe(xml_crossref, data):
    """
        data = {
                    "registrant": registrant
                }

        <head>
            <registrant>registrant</registrant>
        </head>
    """

    registrant = ET.Element('registrant')
    registrant.text = data.get('registrant')

    xml_crossref.find('./head').append(registrant)


def xml_body_pipe(xml_crossref):
    body = ET.Element('body')

    xml_crossref.append(body)


def xml_journal_pipe(xml_crossref):
    journal = ET.Element('journal')

    xml_crossref.find('./body').append(journal)


def xml_journalmetadata_pipe(xml_crossref):
    journal_metadata = ET.Element('journal_metadata')

    xml_crossref.find('./body/journal').append(journal_metadata)


def xml_journaltitle_pipe(xml_tree, xml_crossref):
    """
        <journal>
            <journal_metadata>
                <full_title>Revista da Escola de Enfermagem da USP</full_title>
            </journal_metadata>
        </journal>
    """
    titles = journal_meta.Title(xml_tree)
    full_title = ET.Element('full_title')
    full_title.text = titles.journal_title

    xml_crossref.find('./body/journal/journal_metadata').append(full_title)


def xml_abbreviatedjournaltitle_pipe(xml_tree, xml_crossref):
    """
        <journal>
            <journal_metadata>
                <abbrev_title>Rev. esc. enferm. USP</abbrev_title>
            </journal_metadata>
        </journal>
    """
    titles = journal_meta.Title(xml_tree)
    abbrev_title = ET.Element('abbrev_title')
    abbrev_title.text = titles.abbreviated_journal_title

    xml_crossref.find('./body/journal/journal_metadata').append(abbrev_title)


def xml_issn_pipe(xml_tree, xml_crossref):
    """
        <journal>
            <journal_metadata>
                <issn media_type="electronic">1980-220X</issn>
                <issn media_type="print">0080-6234</issn>
            </journal_metadata>
        </journal>
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


def xml_journalissue_pipe(xml_crossref):
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


def xml_pubdate_pipe(xml_tree, xml_crossref):
    """
    <journal_issue>
        <publication_date media_type="online">
            <year>2022</year>
        </publication_date>
    </journal_issue>
    """
    year = ET.Element('year')
    year.text = dates.ArticleDates(xml_tree).article_date.get('year')

    publication_date = ET.Element('publication_date')
    publication_date.set('media_type', 'online')
    publication_date.append(year)

    xml_crossref.find('./body/journal/journal_issue').append(publication_date)


def xml_journalvolume_pipe(xml_crossref):
    journal_volume = ET.Element('journal_volume')

    xml_crossref.find('./body/journal/journal_issue').append(journal_volume)


def xml_volume_pipe(xml_tree, xml_crossref):
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


def xml_issue_pipe(xml_tree, xml_crossref):
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


def xml_journalarticle_pipe(xml_tree, xml_crossref):
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
        # todo
        # reference_distribution_opts=?
        journal_article.set('reference_distribution_opts', 'any')
        xml_crossref.find('./body/journal').append(journal_article)


def xml_articlecontributors_pipe(xml_tree, xml_crossref):
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
        seq = 0
        for author in authors:
            person_name = ET.Element('person_name')
            person_name.set('contributor_role', author.get('contrib-type'))
            if seq == 0:
                person_name.set('sequence', 'first')
            else:
                person_name.set('sequence', 'additional')
            seq = 1
            given_name = ET.Element('given_name')
            given_name.text = author.get('given_names')
            person_name.append(given_name)
            surname = ET.Element('surname')
            surname.text = author.get('surname')
            person_name.append(surname)
            affiliation = ET.Element('affiliation')
            affs = aff.AffiliationExtractor(xml_tree).get_affiliation_data_from_multiple_tags(subtag=False)
            for a in affs:
                if a['id'] == author['rid']:
                    affiliation.text = a.get('institution')[0].get('orgname') + ', ' + a.get('country')[0].get('name')
            person_name.append(affiliation)
            ORCID = ET.Element('ORCID')
            ORCID.text = 'http://orcid.org/' + author.get('orcid')
            person_name.append(ORCID)
            contributors.append(person_name)
        xml_crossref.find(f"./body/journal/journal_article[@language='{article['lang']}']").append(contributors)


