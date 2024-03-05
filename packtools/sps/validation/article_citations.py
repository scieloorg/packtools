from packtools.sps.models.article_citations import ArticleCitations
from packtools.sps.validation.exceptions import ValidationArticleCitationsException


class ArticleCitationsValidation:
    def __init__(self, xmltree, publication_type_list=None):
        self._xmltree = xmltree
        self.article_citations = list(ArticleCitations(self._xmltree).article_citations)
        self.publication_type_list = publication_type_list

