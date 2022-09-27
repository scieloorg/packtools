from lxml import etree
from packtools.sps import exceptions
from packtools.sps.models.front_journal_meta import Acronym, ISSN, Title


def are_journal_issns_compatible(xml_article, issns):
    """
    Params
    ------
    xml_article: ElementTree
    issns: list
    """
    obj_journal_issn = ISSN(xml_article)
    for i in [j for j in [obj_journal_issn.epub, obj_journal_issn.ppub] if j != '']:
        if i not in issns:
            raise exceptions.ArticleHasIncompatibleJournalISSNError(data={'xml': i, 'issns': issns})
    return True


def are_journal_titles_compatible(xml_article, titles):
    """
    Params
    ------
    xml_article: ElementTree
    titles: list
    """
    obj_journal_title_values = [d['value'] for d in Title(xml_article).data]
    for t in obj_journal_title_values:
        if t in titles:
            return True
    raise exceptions.ArticleHasIncompatibleJournalTitleError(data={'xml': obj_journal_title_values, 'titles': titles})


def are_journal_acronyms_compatible(xml_article, acronym):
    """
    Params
    ------
    xml_article: ElementTree
    acronym: str
    """
    xml_acronym = Acronym(xml_article).text
    if xml_acronym != acronym:
        raise exceptions.ArticleHasIncompatibleJournalAcronymError(data={'xml': xml_acronym, 'acronym': acronym})
    return True
