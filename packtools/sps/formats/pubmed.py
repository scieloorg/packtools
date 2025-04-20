# coding: utf-8
from lxml import etree as ET

from packtools.sps.models import (
    aff,
    article_abstract,
    article_and_subarticles,
    article_contribs,
    references,
    article_ids,
    article_titles,
    dates,
    front_articlemeta_issue,
    journal_meta,
    kwd_group,
)


def xml_pubmed_article_pipe():
    return ET.Element("Article")


def xml_pubmed_journal_pipe(xml_pubmed):
    el = ET.Element("Journal")
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
        el = ET.Element("PublisherName")
        el.text = publisher
        xml_pubmed.find("Journal").append(el)


def get_journal_title(xml_tree):
    journal_title = journal_meta.Title(xml_tree)

    return journal_title.abbreviated_journal_title


def xml_pubmed_journal_title_pipe(xml_pubmed, xml_tree):
    """
    <JournalTitle>Arq Bras Cir Dig</JournalTitle>
    """
    journal_title = get_journal_title(xml_tree)
    if journal_title is not None:
        el = ET.Element("JournalTitle")
        el.text = journal_title
        xml_pubmed.find("Journal").append(el)


def get_issn(xml_tree):
    issn = journal_meta.ISSN(xml_tree)

    return issn.epub or issn.ppub


def xml_pubmed_issn_pipe(xml_pubmed, xml_tree):
    """
    <Issn>1678-2674</Issn>
    """
    issn = get_issn(xml_tree)
    if issn != "":
        el = ET.Element("Issn")
        el.text = issn
        xml_pubmed.find("Journal").append(el)


def get_volume(xml_tree):
    issue = front_articlemeta_issue.ArticleMetaIssue(xml_tree)

    return issue.volume


def xml_pubmed_volume_pipe(xml_pubmed, xml_tree):
    """
    <Volume>37</Volume>
    """
    volume = get_volume(xml_tree)
    if volume is not None:
        el = ET.Element("Volume")
        el.text = volume
        xml_pubmed.find("Journal").append(el)


def get_issue(xml_tree):
    issue = front_articlemeta_issue.ArticleMetaIssue(xml_tree)

    return issue.issue


def xml_pubmed_issue_pipe(xml_pubmed, xml_tree):
    """
    <Issue>11</Issue>
    """
    issue = get_issue(xml_tree)
    if issue is not None:
        el = ET.Element("Issue")
        el.text = issue
        xml_pubmed.find("Journal").append(el)


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
        dt = ET.Element("PubDate")
        dt.set("PubStatus", "epublish")
        for element in ["year", "month", "day"]:
            # TODO
            # Season
            # The season of publication. e.g.,Winter, Spring, Summer, Fall. Do not use if a Month is available.
            # There is no example of using this value in the files.

            if date.get(element):
                el = ET.Element(element.capitalize())
                el.text = date.get(element)
                dt.append(el)
        xml_pubmed.find("Journal").append(dt)


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
    titles = get_article_titles(xml_tree)
    title_by_lang = titles.get("en", {}).get("text")
    if title_by_lang is not None:
        el = ET.Element("ArticleTitle")
        el.text = title_by_lang
        xml_pubmed.append(el)


def xml_pubmed_vernacular_title_pipe(xml_pubmed, xml_tree):
    """
    <VernacularTitle>
        Dissecção Espontânea da Artéria Coronária: Existem Diferenças entre Homens e Mulheres?
    </VernacularTitle>
    """
    main_lang = article_and_subarticles.ArticleAndSubArticles(xml_tree).main_lang
    titles = get_article_titles(xml_tree)
    title_by_lang = titles.get(main_lang, {}).get("text")
    if title_by_lang is not None:
        el = ET.Element("VernacularTitle")
        el.text = title_by_lang
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
        el = ET.Element("FirstPage")
        el.set("LZero", "save")
        el.text = first_page
        xml_pubmed.append(el)


def get_elocation(xml_tree):
    ids = article_ids.ArticleIds(xml_tree)

    return ids.data


def add_elocation(xml_pubmed, value, key):
    if value is not None:
        el = ET.Element("ELocationID")
        el.set("EIdType", key)
        el.text = value
        xml_pubmed.append(el)


def xml_pubmed_elocation_pipe(xml_pubmed, xml_tree):
    """
    <ELocationID EIdType="pii">S0001-37652022000501309</ELocationID>
    <ELocationID EIdType="doi">10.1590/0001-3765202220201894</ELocationID>
    """
    ids = get_elocation(xml_tree)
    add_elocation(xml_pubmed, ids.get("v2"), "pii")
    add_elocation(xml_pubmed, ids.get("doi"), "doi")


def get_langs(xml_tree):
    langs = article_and_subarticles.ArticleAndSubArticles(xml_tree)

    return langs.data


def add_langs(xml_pubmed, xml_tree):
    langs = get_langs(xml_tree)
    for lang in langs:
        if lang.get("lang") is not None:
            el = ET.Element("Language")
            el.text = lang.get("lang").upper()
            xml_pubmed.append(el)


def xml_pubmed_language_pipe(xml_pubmed, xml_tree):
    """
    <Language>PT</Language>
    <Language>EN</Language>
    """
    add_langs(xml_pubmed, xml_tree)


def pipeline_pubmed(xml_tree, pretty_print=True):
    xml_pubmed = xml_pubmed_article_pipe()
    xml_pubmed_journal_pipe(xml_pubmed)
    xml_pubmed_publisher_name_pipe(xml_pubmed, xml_tree)
    xml_pubmed_journal_title_pipe(xml_pubmed, xml_tree)
    xml_pubmed_issn_pipe(xml_pubmed, xml_tree)
    xml_pubmed_volume_pipe(xml_pubmed, xml_tree)
    xml_pubmed_issue_pipe(xml_pubmed, xml_tree)
    xml_pubmed_pub_date_pipe(xml_pubmed, xml_tree)
    xml_pubmed_article_title_pipe(xml_pubmed, xml_tree)
    xml_pubmed_first_page_pipe(xml_pubmed, xml_tree)
    xml_pubmed_elocation_pipe(xml_pubmed, xml_tree)
    xml_pubmed_language_pipe(xml_pubmed, xml_tree)
    xml_pubmed_author_list(xml_pubmed, xml_tree)
    xml_pubmed_publication_type(xml_pubmed, xml_tree)
    xml_pubmed_article_id(xml_pubmed, xml_tree)
    xml_pubmed_history(xml_pubmed, xml_tree)
    xml_pubmed_copyright_information(xml_pubmed, xml_tree)
    xml_pubmed_coi_statement(xml_pubmed, xml_tree)
    xml_pubmed_object_list(xml_pubmed, xml_tree)
    xml_pubmed_title_reference_list(xml_pubmed, xml_tree)
    xml_pubmed_citations(xml_pubmed, xml_tree)
    xml_pubmed_abstract(xml_pubmed, xml_tree)
    xml_pubmed_other_abstract(xml_pubmed, xml_tree)

    xml_tree = ET.ElementTree(xml_pubmed)
    return ET.tostring(xml_tree, pretty_print=pretty_print, encoding="utf-8").decode("utf-8")


def get_authors(xml_tree):
    return article_contribs.XMLContribs(xml_tree).contribs


def add_first_name(author_reg, author_tag):
    author_first_name = author_reg.get("contrib_name", {}).get("given-names")
    if author_first_name:
        first = ET.Element("FirstName")
        first.text = author_first_name
        author_tag.append(first)


def add_last_name(author_reg, author_tag):
    author_last_name = author_reg.get("contrib_name", {}).get("surname")
    if author_last_name:
        last = ET.Element("LastName")
        last.text = author_last_name
        author_tag.append(last)


def get_affiliations(author_reg, xml_tree):
    affiliations = aff.AffiliationExtractor(xml_tree).get_affiliation_dict(subtag=False)
    affiliation_list = []
    for item in author_reg.get("affs"):
        affiliation_list.append(
            affiliations.get(item.get("id"), {}).get("institution", {})[0].get("original")
        )
    return affiliation_list


def add_affiliations(affiliations, author_tag):
    for item in affiliations:
        el_aff = ET.Element("Affiliation")
        el_aff.text = item
        if len(affiliations) > 1:
            info = ET.Element("AffiliationInfo")
            info.append(el_aff)
            author_tag.append(info)
        else:
            author_tag.append(el_aff)


def add_orcid(author_reg, author_tag):
    orcid = author_reg.get("contrib_ids", {}).get("orcid")
    if orcid:
        orcid_elem = ET.Element("Identifier")
        orcid_elem.set("Source", "orcid")
        orcid_elem.text = "http://orcid.org/" + orcid
        author_tag.append(orcid_elem)


def xml_pubmed_author_list(xml_pubmed, xml_tree):
    authors = list(get_authors(xml_tree))
    if authors:
        author_list_tag = ET.Element("AuthorList")
        for author_reg in authors:
            author_tag = ET.Element("Author")
            add_first_name(author_reg, author_tag)

            # TODO
            # add_middle_name(author_reg, author_tag)
            # The Author’s full middle name, or initial if the full name is not available.
            # Multiple names are allowed in this tag.
            # There is no example of using this value in the files.

            add_last_name(author_reg, author_tag)

            # TODO
            # add_suffix(author_reg, author_tag)
            # The Author's suffix, if any, e.g. "Jr", "Sr", "II", "IV". Do not include honorific titles,
            # e.g. "M.D.", "Ph.D.".
            # There is no example of using this value in the files

            # TODO
            # add_collective_name(author_reg, author_tag)
            # The name of the authoring committee or organization. The CollectiveName tag should be placed within
            # an Author tag. Omit extraneous text like, “on behalf of.”
            # Please see the following example:
            #   <AuthorList>
            #       <Author>
            #           <CollectiveName>Plastic Surgery Educational Foundation DATA Committee</CollectiveName>
            #       </Author>
            #   </AuthorList>
            # There is no example of using this value in the files

            affiliations = get_affiliations(author_reg, xml_tree)
            add_affiliations(affiliations, author_tag)
            add_orcid(author_reg, author_tag)
            author_list_tag.append(author_tag)

            # TODO
            # add_group_list(author_reg, author_tag)
            # Group information should be enclosed in these tags. If an article has one or more Groups, this tag
            # must be submitted. Groups should be listed in the same order as in the printed article, and Group name
            # format should accurately reflect the article. This tag is Required if the tag Group is present.
            # There is no example of using this value in the files

            # TODO
            # add_group(author_reg, author_tag)
            # Information about a single Group must begin with this tag.
            # There is no example of using this value in the files

            # TODO
            # add_group_name(author_reg, author_tag)
            # The name of the authoring committee or organization. Omit extraneous text like, “on behalf of.”
            # There is no example of using this value in the files

            # TODO
            # add_individual_name(author_reg, author_tag)
            # The name of individual members belonging to the authoring committee or organization.
            # The name should be tagged with the FirstName, MiddleName, LastName, Suffix, and Affiliation tags.
            # There is no example of using this value in the files

        xml_pubmed.append(author_list_tag)


def get_publication_type(xml_tree):
    publication_type = article_and_subarticles.ArticleAndSubArticles(
        xml_tree
    ).main_article_type
    if publication_type is not None:
        return publication_type.replace("-", " ").title()


def xml_pubmed_publication_type(xml_pubmed, xml_tree):
    """
    <PublicationType>Journal Article</PublicationType>
    """
    publication_type = get_publication_type(xml_tree)
    if publication_type is not None:
        el = ET.Element("PublicationType")
        el.text = publication_type
        xml_pubmed.append(el)


def get_article_id_pii(xml_tree):
    return article_ids.ArticleIds(xml_tree).v2


def get_article_id_doi(xml_tree):
    return article_ids.ArticleIds(xml_tree).doi


def xml_pubmed_article_id(xml_pubmed, xml_tree):
    """
    <ArticleIdList>
        <ArticleId IdType="pii">S0102-311X2022001205003</ArticleId>
        <ArticleId IdType="doi">10.1590/0102-311XEN083822</ArticleId>
    </ArticleIdList>
    """
    pii = get_article_id_pii(xml_tree)
    doi = get_article_id_doi(xml_tree)
    if pii is not None or doi is not None:
        article_id_list = ET.Element("ArticleIdList")
        if pii is not None:
            article_id = ET.Element("ArticleId")
            article_id.set("IdType", "pii")
            article_id.text = pii
            article_id_list.append(article_id)
        if doi is not None:
            article_id = ET.Element("ArticleId")
            article_id.set("IdType", "doi")
            article_id.text = doi
            article_id_list.append(article_id)
        xml_pubmed.append(article_id_list)


def get_event_date(xml_tree, event):
    event_date = dates.ArticleDates(xml_tree).history_dates_dict
    return event_date.get(event)


def add_date(date_tag, date_dict):
    for event in ["year", "month", "day"]:
        if date_dict.get(event):
            el = ET.Element(event.capitalize())
            el.text = date_dict.get(event)
            date_tag.append(el)


def xml_pubmed_history(xml_pubmed, xml_tree):
    """
    <History>
        <PubDate PubStatus="received">
            <Year>2021</Year>
            <Month>06</Month>
            <Day>22</Day>
        </PubDate>
        <PubDate PubStatus="accepted">
            <Year>2022</Year>
            <Month>06</Month>
            <Day>15</Day>
        </PubDate>
        <PubDate PubStatus="ecollection">
            <Year>2023</Year>
        </PubDate>
    </History>

    received - date manuscript received for review
    accepted - accepted for publication
    revised - article revised by publisher or author
    aheadofprint - published electronically prior to final publication (without volume and issue)
    epublish – published electronically
    ppublish – published in print
    ecollection – used for electronic-only journals that publish individual articles and later collect them into an “issue” date, typically called an eCollection.
    """
    history_dates = {
        "received": get_event_date(xml_tree, "received"),
        "accepted": get_event_date(xml_tree, "accepted"),
        "ecollection": dates.ArticleDates(xml_tree).collection_date,
    }

    history = ET.Element("History")
    for event, date in history_dates.items():
        if history_dates[event] is not None:
            el = ET.Element("PubDate")
            el.set("PubStatus", event)
            add_date(el, date)
            history.append(el)

    xml_pubmed.append(history)


def xml_pubmed_copyright_information(xml_pubmed, xml_tree):
    ...
    # TODO
    # The Copyright information associated with this article.
    # There is no example of using this value in the files.


def xml_pubmed_coi_statement(xml_pubmed, xml_tree):
    ...
    # TODO
    # The Conflict of Interest statement associated with this article.
    # There is no example of using this value in the files.


def get_keywords(xml_tree):
    return kwd_group.KwdGroup(xml_tree).extract_kwd_data_with_lang_text(subtag=False)


def xml_pubmed_object_list(xml_pubmed, xml_tree):
    """
    <ObjectList>
       <Object Type="keyword">
         <Param Name="value">COPD</Param>
       </Object>
       <Object Type="keyword">
         <Param Name="value">Internet</Param>
       </Object>
       <Object Type="keyword">
         <Param Name="value">coaching</Param>
       </Object>
       <Object Type="keyword">
         <Param Name="value">patient activation</Param>
       </Object>
       <Object Type="grant">
         <Param Name="id">RO1DK561234</Param>
         <Param Name="grantor">National Institutes of Health</Param>
       </Object>
       <Object Type="grant">
         <Param Name="id">2456797AB</Param>
         <Param Name="grantor">The British Granting Agency</Param>
         <Param Name="acronym">BGA</Param>
         <Param Name="country">England</Param>
       </Object>
     </ObjectList>
    """
    kwd_list = get_keywords(xml_tree)
    if not kwd_list:
        return
    obj_list = ET.Element("ObjectList")
    for kwd in kwd_list:
        if kwd.get("lang") == "en":
            obj = ET.Element("Object")
            obj.set("Type", "keyword")
            param = ET.Element("Param")
            param.set("Name", "value")
            param.text = kwd.get("text")
            obj.append(param)
            obj_list.append(obj)
    xml_pubmed.append(obj_list)

    # TODO
    # The Object tag includes the Type attribute, which may include only one of the following values
    # for each identifier.
    # Grant, Comment, Dataset, Erratum, Originalreport, Partialretraction, Patientsummary,
    # Reprint, Republished, Retraction, Update.
    # There is no example of using this value in the files.


def xml_pubmed_title_reference_list(xml_pubmed, xml_tree):
    """
    <ReferenceList>
        <Title>REFERENCES</Title>
    </ReferenceList>
    """
    title = xml_tree.find("./back/ref-list/title")
    if title is not None:
        xml_pubmed.append(ET.Element("ReferenceList"))
        title_el = ET.Element("Title")
        title_el.text = title.text
        xml_pubmed.find("./ReferenceList").append(title_el)


def add_element_citation_id(ids):
    article_id_list = ET.Element("ArticleIdList")
    for key, value in ids.items():
        article_id = ET.Element("ArticleId")
        key = "pubmed" if key == "pmid" else key
        article_id.set("IdType", key)
        article_id.text = value
        article_id_list.append(article_id)
    return article_id_list


def xml_pubmed_citations(xml_pubmed, xml_tree):
    """
    <ReferenceList>
        <Title>REFERENCES</Title>
            <Reference>
                <Citation>British Lung Foundation Chronic obstructive
                pulmonary disease (COPD) statistics. [Accessed January 27,
                2017]. </Citation>
                <ArticleIdList>
                    <ArticleId IdType="pmcid">PMC4153410</ArticleId>
                    <ArticleId IdType="pubmed">24768240</ArticleId>
                </ArticleIdList>
            </Reference>
            <Reference>
                <Citation>Yohannes AM, Baldwin RC, Connolly MJ. Depression and
                anxiety in elderly patients with chronic obstructive pulmonary
                disease. Age Ageing. 2006;35(5):457–459. </Citation>
                <ArticleIdList>
                    <ArticleId IdType="pmcid">PMC3020244</ArticleId>
                    <ArticleId IdType="pubmed">20932581</ArticleId>
                </ArticleIdList>
            </Reference>
     </ReferenceList>
    """
    refs = references.XMLReferences(xml_tree).main_references
    xml = xml_pubmed.find("./ReferenceList")
    for ref in refs:
        ref_el = ET.Element("Reference")
        citation = ET.Element("Citation")
        citation.text = ref.get("mixed_citation")
        ref_el.append(citation)
        ids = ref.get("citation_ids")
        if ids is not None:
            ref_el.append(add_element_citation_id(ids))
        xml.append(ref_el)


def add_abstract_text(label, text):
    abstract_text = ET.Element("AbstractText")
    abstract_text.set("Label", label.upper()[:-1])
    abstract_text.text = text
    return abstract_text


def xml_pubmed_abstract(xml_pubmed, xml_tree):
    """
    <Abstract>
        To assess the effects...
        Patients attending lung...
        Twenty-five patients...
        The findings suggest...
    </Abstract>
    OR
    <Abstract>
        <AbstractText Label="OBJECTIVE">To assess the effects...</AbstractText>
        <AbstractText Label="METHODS">Patients attending lung...</AbstractText>
        <AbstractText Label="RESULTS">Twenty-five patients...</AbstractText>
        <AbstractText Label="CONCLUSIONS">The findings suggest...</AbstractText>
    </Abstract>
    """
    try:
        abstract_el = ET.Element("Abstract")
        abstract = article_abstract.Abstract(xml_tree).get_main_abstract().get('abstract')
        if abstract.get('sections'):
            for item in abstract.get('sections'):
                abstract_el.append(add_abstract_text(item.get('title'), item.get('p')))
        else:
            abstract_el.text = abstract.get('p')
        xml_pubmed.append(abstract_el)
    except AttributeError:
        pass


def xml_pubmed_other_abstract(xml_pubmed, xml_tree):
    """
    <OtherAbstract Language="fr">
      <AbstractText Label="TITRE">Meilleure estimation du fardeau que représentent les facteurs de risque de maladie chronique pour la santé et l’économie au Manitoba.</AbstractText>
      <AbstractText Label="INTRODUCTION">L’estimation du fardeau global que représentent les facteurs de risque multiples au sein d’une population présente certains défis d’ordre analytique. Nous décrivons une méthodologie permettant de tenir compte des facteurs de risque se chevauchant dans certaines sous-populations et entraînant un « double compte » des maladies et du fardeau économique qu’ils engendrent.</AbstractText>
      <AbstractText Label="MÉTHODOLOGIE">Notre démarche permet d’analyser avec précision le fardeau économique global des maladies chroniques dans un cadre multifactoriel tout en tenant compte de l’incidence du poids en tant qu’exposition continue ou polytomique (allant de l’absence d’excédent de poids au surpoids et à l’obésité). Nous appliquons cette méthode au tabagisme, à l’inactivité physique et au surpoids et à l’obésité à la province du Manitoba (Canada).</AbstractText>
      <AbstractText Label="RÉSULTATS">En 2008, le fardeau économique global annuel des facteurs de risque au Manitoba était d’environ 1,6 milliard de dollars (557 millions pour le tabagisme, 299 millions pour l’inactivité physique et 747 millions pour le surpoids et l’obésité). Le fardeau total représente un rajustement à la baisse de 12,6% lorsqu’on tient compte de l’effet des facteurs de risque multiples chez certaines personnes.</AbstractText>
      <AbstractText Label="CONCLUSION">Une meilleure estimation du fardeau économique global des facteurs de risque multiples au sein d’une population peut faciliter l’établissement des priorités et améliorer le soutien aux initiatives de prevention primaire. </AbstractText>
    </OtherAbstract>
    """
    try:
        article_abstracts = article_abstract.Abstract(xml_tree)
        main_lang = article_abstracts.get_main_abstract().get('lang')
        abstracts = article_abstracts.get_abstracts()
        for item in abstracts:
            abstract = item.get('abstract')
            lang = item.get('lang')
            if main_lang != lang:
                abstract_el = ET.Element("OtherAbstract")
                abstract_el.set("Language", lang)
                if abstract.get('sections'):
                    for section in abstract.get('sections'):
                        abstract_el.append(add_abstract_text(section.get('title'), section.get('p')))
                else:
                    abstract_el.text = abstract.get('p')

                xml_pubmed.append(abstract_el)
    except AttributeError:
        pass
     
    