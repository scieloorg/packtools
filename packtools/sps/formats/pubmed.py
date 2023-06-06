# coding: utf-8
from lxml import etree as ET

from packtools.sps.models import (
    journal_meta,
    front_articlemeta_issue,
    dates,
    article_titles,
    article_ids,
    article_and_subarticles,
)


def xml_pubmed_article_pipe():
    root = ET.Element("Article")
    tree = ET.ElementTree(root)

    return tree


def xml_pubmed_journal_pipe(xml_pubmed):
    el = ET.Element('Journal')
    xml_pubmed.append(el)


def get_publisher(xml_tree):
    publisher = journal_meta.Publisher(xml_tree)
    try:
        return publisher.publishers_names[0]
    except IndexError:
        pass


def xml_pubmed_publisher_name_pipe(xml_pubmed, xml_tree):
    """
    <PublisherName>Colégio Brasileiro de Cirurgia Digestiva</PublisherName>
    """
    publisher = get_publisher(xml_tree)
    if publisher is not None:
        el = ET.Element('PublisherName')
        el.text = publisher
        xml_pubmed.find('Journal').append(el)


def get_journal_title(xml_tree):
    journal_title = journal_meta.Title(xml_tree)

    return journal_title.abbreviated_journal_title


def xml_pubmed_journal_title_pipe(xml_pubmed, xml_tree):
    """
    <JournalTitle>Arq Bras Cir Dig</JournalTitle>
    """
    journal_title = get_journal_title(xml_tree)
    if journal_title is not None:
        el = ET.Element('JournalTitle')
        el.text = journal_title
        xml_pubmed.find('Journal').append(el)


def get_issn(xml_tree):
    issn = journal_meta.ISSN(xml_tree)

    return issn.epub or issn.ppub


def xml_pubmed_issn_pipe(xml_pubmed, xml_tree):
    """
    <Issn>1678-2674</Issn>
    """
    issn = get_issn(xml_tree)
    if issn != '':
        el = ET.Element('Issn')
        el.text = issn
        xml_pubmed.find('Journal').append(el)


def get_volume(xml_tree):
    issue = front_articlemeta_issue.ArticleMetaIssue(xml_tree)

    return issue.volume


def xml_pubmed_volume_pipe(xml_pubmed, xml_tree):
    """
    <Volume>37</Volume>
    """
    volume = get_volume(xml_tree)
    if volume is not None:
        el = ET.Element('Volume')
        el.text = volume
        xml_pubmed.find('Journal').append(el)


def get_issue(xml_tree):
    issue = front_articlemeta_issue.ArticleMetaIssue(xml_tree)

    return issue.issue


def xml_pubmed_issue_pipe(xml_pubmed, xml_tree):
    """
    <Issue>11</Issue>
    """
    issue = get_issue(xml_tree)
    if issue is not None:
        el = ET.Element('Issue')
        el.text = issue
        xml_pubmed.find('Journal').append(el)


def get_date(xml_tree):
    date = dates.ArticleDates(xml_tree)

    return date.article_date


def xml_pubmed_pub_date_pipe(xml_pubmed, xml_tree):
    """
    <PubDate PubStatus="epublish">
        <Year>2023</Year>
        <Month>01</Month>
        <Day>06</Day>
    </PubDate>
    """
    date = get_date(xml_tree)
    if date is not None:
        dt = ET.Element('PubDate')
        dt.set('PubStatus', 'epublish')
        for element in ['year', 'month', 'day']:
            if date.get(element):
                el = ET.Element(element.capitalize())
                el.text = date.get(element)
                dt.append(el)
        xml_pubmed.find('Journal').append(dt)


def get_article_title(xml_tree):
    title = article_titles.ArticleTitles(xml_tree)

    return title.article_title.get('text')


def xml_pubmed_article_title_pipe(xml_pubmed, xml_tree):
    """
    <ArticleTitle>
        The mechanism study of inhibition effect of prepared Radix Rehmanniainon combined with Radix Astragali
        osteoporosis through PI3K-AKT signaling pathway
    </ArticleTitle>
    """
    title = get_article_title(xml_tree)
    if title is not None:
        el = ET.Element('ArticleTitle')
        el.text = title
        xml_pubmed.append(el)


def get_first_page(xml_tree):
    issue = front_articlemeta_issue.ArticleMetaIssue(xml_tree)

    return issue.elocation_id


def xml_pubmed_first_page_pipe(xml_pubmed, xml_tree):
    """
    <FirstPage LZero="save">e20220291</FirstPage>
    """
    first_page = get_first_page(xml_tree)
    if first_page is not None:
        el = ET.Element('FirstPage')
        el.set('LZero', 'save')
        el.text = first_page
        xml_pubmed.append(el)


def get_elocation(xml_tree):
    ids = article_ids.ArticleIds(xml_tree)

    return ids.data


