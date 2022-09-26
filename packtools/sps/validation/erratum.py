from scielo_scholarly_data import standardizer

from packtools.sps.models.article_doi_with_lang import DoiWithLang
from packtools.sps.models.article_errata import ArticleWithErrataNotes
from packtools.sps.models.related_articles import RelatedItems


def has_compatible_errata_and_document(xml_errata, xml_article, articles_types=['corrected-article']):
    if not has_errata_notes(xml_article):
        return False

    article_doi_list = set()
    for lang_doi in DoiWithLang(xml_article).data:
        doi = lang_doi['value']
        doi_std = standardizer.document_doi(doi)
        if doi_std:
            article_doi_list.add(doi_std)    

    for doi_and_type in RelatedItems(xml_errata).related_articles:
        ra_doi = standardizer.document_doi(doi_and_type['href'])
        ra_type = doi_and_type['related-article-type']

        if ra_doi in article_doi_list and ra_type in articles_types:
            return True

    return False


def has_errata_notes(xml_article):
    errata_notes = ArticleWithErrataNotes(xml_article).footnotes()
    if len(errata_notes) == 0:
        return False

    return True
