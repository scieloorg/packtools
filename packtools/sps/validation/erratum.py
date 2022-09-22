from scielo_scholarly_data import standardizer

from packtools.sps.models.article_doi_with_lang import DoiWithLang
from packtools.sps.models.article_errata import ArticleWithErrataNotes
from packtools.sps.models.related_articles import RelatedItems


def has_compatible_errata_and_document(xml_errata, xml_article, articles_types=['corrected-article']):
    if not has_errata_notes(xml_article):
        return False

def has_errata_notes(xml_article):
    errata_notes = ArticleWithErrataNotes(xml_article).footnotes()
    if len(errata_notes) == 0:
        return False

    return True
