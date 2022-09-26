from lxml import etree
from packtools.sps.models.article_doi_with_lang import DoiWithLang
from packtools.sps.models.front_journal_meta import ISSN


class InvalidXMLTreeError(Exception):
    ...

