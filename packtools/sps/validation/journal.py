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

