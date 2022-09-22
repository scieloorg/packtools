from scielo_scholarly_data import standardizer

from packtools.sps.models.article_doi_with_lang import DoiWithLang
from packtools.sps.models.article_errata import ArticleWithErrataNotes
from packtools.sps.models.related_articles import RelatedItems


def has_compatible_errata_and_document(xml_errata, xml_article, articles_types=['corrected-article']):
