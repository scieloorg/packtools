from lxml import etree
from packtools.sps import exceptions
from packtools.sps.models.front_journal_meta import Acronym, ISSN, Title


def are_article_and_journal_data_compatible(xml_article, journal_print_issn, journal_electronic_issn, journal_titles):
    """
    Params
    ------
    xml_article: ElementTree
    journal_print_issn: str
    journal_electronic_issn: str
    journal_titles: list
    """
    if not isinstance(xml_article, etree._Element):
        raise exceptions.ArticleHasInvalidInstanceError()

    try:
        are_journal_issns_compatible(xml_article, journal_print_issn, journal_electronic_issn)
    except exceptions.ArticleHasIncompatibleJournalISSNError:
        raise
    
    try:
        are_journal_titles_compatible(xml_article, journal_titles)
    except exceptions.ArticleHasIncompatibleJournalTitleError:
        raise

    return True
    

def are_journal_issns_compatible(xml_article, print_issn, electronic_issn):
    """
    Params
    ------
    xml_article: ElementTree
    issns: list
    """
    obj_journal_issn = ISSN(xml_article)
    incompatible_pairs = []

    if obj_journal_issn.ppub != print_issn:
        incompatible_pairs.append({'xml': obj_journal_issn.ppub, 'print_issn': print_issn})

    if obj_journal_issn.epub != electronic_issn:
        incompatible_pairs.append({'xml': obj_journal_issn.epub, 'electronic_issn': electronic_issn})
    
    if len(incompatible_pairs) > 0:
        raise exceptions.ArticleHasIncompatibleJournalISSNError(data=incompatible_pairs)

    return True


def are_journal_titles_compatible(xml_article, titles):
    """
    Params
    ------
    xml_article: ElementTree
    titles: list
    """
    for d in Title(xml_article).data:
        if d['value'] not in titles:
            raise exceptions.ArticleHasIncompatibleJournalTitleError(data={'xml': d['value'], 'titles': titles})

    return True


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
