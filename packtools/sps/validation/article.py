from lxml import etree
from packtools.sps import exceptions
from packtools.sps.models.article_doi_with_lang import DoiWithLang
from packtools.sps.models.journal_meta import ISSN


def are_similar_articles(xml1, xml2):
    """
    Params
    ------
    xml1: ElementTree
    xml2: ElementTree
    """
    if not isinstance(xml1, etree._Element) or not isinstance(xml2, etree._Element):
        raise exceptions.ArticleHasInvalidInstanceError()

    if not have_similar_issn_codes(xml1, xml2):
        return False
    
    if not have_similar_doi_codes(xml1, xml2):
        return False

    return True


def have_similar_doi_codes(xml1, xml2):
    """
    Params
    ------
    xml1: ElementTree
    xml2: ElementTree
    """
    a1_doi_list = [d['value'] for d in DoiWithLang(xml1).data]
    a2_doi_list = [d['value'] for d in DoiWithLang(xml2).data]

    if set(a1_doi_list) ^ set(a2_doi_list):
        return False

    return True


def have_similar_issn_codes(xml1, xml2):
    """
    Params
    ------
    xml1: ElementTree
    xml2: ElementTree
    """
    a1_issn = ISSN(xml1)
    a2_issn = ISSN(xml2)
    
    if a1_issn.epub != a2_issn.epub:
        return False

    if a1_issn.ppub != a2_issn.ppub:
        return False

    return True
