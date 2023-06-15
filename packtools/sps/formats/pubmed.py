# coding: utf-8
from lxml import etree as ET

from packtools.sps.models import (
    journal_meta,
    front_articlemeta_issue,
    dates,
    article_titles,
    article_ids,
    article_and_subarticles,
    article_authors,
    aff,
    kwd_group,
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
            # TODO
            # Season
            # The season of publication. e.g.,Winter, Spring, Summer, Fall. Do not use if a Month is available.
            # There is no example of using this value in the files.

            if date.get(element):
                el = ET.Element(element.capitalize())
                el.text = date.get(element)
                dt.append(el)
        xml_pubmed.find('Journal').append(dt)


def xml_pubmed_replaces_pipe(xml_pubmed, xml_tree):
    ...
    # TODO
    # Replaces
    # The identifier of the article to be replaced. Do not use this tag for new articles.
    # The <Replaces> tag can be used to update an Ahead of Print citation, or to correct an error.
    # The Replaces tag includes the IdType attribute, which may contain only one of the following values:
    #       pubmed - PubMed Unique Identifier (PMID) (default value)
    #       pii - publisher identifier
    #       doi - Digital Object Identifier
    # There is no example of using this value in the files.


def get_article_titles(xml_tree):
    title = article_titles.ArticleTitles(xml_tree)

    return title.article_title_dict


def xml_pubmed_article_title_pipe(xml_pubmed, xml_tree):
    """
    <ArticleTitle>
        Spontaneous Coronary Artery Dissection: Are There Differences between Men and Women?
    </ArticleTitle>
    """
    title = get_article_titles(xml_tree)
    if title.get('en') is not None:
        el = ET.Element('ArticleTitle')
        el.text = title.get('en')
        xml_pubmed.append(el)


def xml_pubmed_vernacular_title_pipe(xml_pubmed, xml_tree):
    """
    <VernacularTitle>
        Dissecção Espontânea da Artéria Coronária: Existem Diferenças entre Homens e Mulheres?
    </VernacularTitle>
    """
    main_lang = article_and_subarticles.ArticleAndSubArticles(xml_tree).main_lang
    title = get_article_titles(xml_tree)
    if title.get(main_lang) is not None:
        el = ET.Element('VernacularTitle')
        el.text = title.get(main_lang)
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


def add_elocation(xml_pubmed, value, key):
    if value is not None:
        el = ET.Element('ELocationID')
        el.set('EIdType', key)
        el.text = value
        xml_pubmed.append(el)


def xml_pubmed_elocation_pipe(xml_pubmed, xml_tree):
    """
    <ELocationID EIdType="pii">S0001-37652022000501309</ELocationID>
    <ELocationID EIdType="doi">10.1590/0001-3765202220201894</ELocationID>
    """
    ids = get_elocation(xml_tree)
    add_elocation(xml_pubmed, ids.get('v2'), 'pii')
    add_elocation(xml_pubmed, ids.get('doi'), 'doi')


def get_langs(xml_tree):
    langs = article_and_subarticles.ArticleAndSubArticles(xml_tree)

    return langs.data


def add_langs(xml_pubmed, xml_tree):
    langs = get_langs(xml_tree)
    for lang in langs:
        if lang.get('lang') is not None:
            el = ET.Element('Language')
            el.text = lang.get('lang').upper()
            xml_pubmed.append(el)


def xml_pubmed_language_pipe(xml_pubmed, xml_tree):
    """
    <Language>PT</Language>
    <Language>EN</Language>
    """
    add_langs(xml_pubmed, xml_tree)


def get_authors(xml_tree):
    return article_authors.Authors(xml_tree).contribs


def add_first_name(author_reg, author_tag):
    if author_reg.get('given_names'):
        first = ET.Element('FirstName')
        first.text = author_reg.get('given_names')
        author_tag.append(first)


def add_last_name(author_reg, author_tag):
    if author_reg.get('surname'):
        last = ET.Element('LastName')
        last.text = author_reg.get('surname')
        author_tag.append(last)


def get_affiliations(author_reg, xml_tree):
    affiliations = aff.AffiliationExtractor(xml_tree).get_affiliation_dict(subtag=False)
    affiliation_list = []
    for rid in author_reg.get('rid-aff'):
        affiliation_list.append(affiliations.get(rid).get('institution')[0].get('original'))
    return affiliation_list


def add_affiliations(affiliations, author_tag):
    for item in affiliations:
        el_aff = ET.Element('Affiliation')
        el_aff.text = item
        if len(affiliations) > 1:
            info = ET.Element('AffiliationInfo')
            info.append(el_aff)
            author_tag.append(info)
        else:
            author_tag.append(el_aff)


