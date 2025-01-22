from packtools.sps.models.article_and_subarticles import Fulltext
from packtools.sps.models.related_articles import Fulltext as FulltextRelatedArticles
from packtools.sps.models.dates import FulltextDates
from packtools.sps.models.article_contribs import Contrib
from packtools.sps.models.article_license import License


class CustomMeta:
    def __init__(self, custom_meta_node):
        self.custom_meta_node = custom_meta_node

    @property
    def meta_name(self):
        return self.custom_meta_node.findtext('.//meta-name')

    @property
    def meta_value(self):
        # 'revision', 'major-revision', 'minor-revision', 'reject',
        # 'reject-with-resubmit', 'accept', 'formal-accept', 'accept-in-principle'
        return self.custom_meta_node.findtext('.//meta-value')

    @property
    def data(self):
        return {
            "meta_name": self.meta_name,
            "meta_value": self.meta_value
        }


class PeerReview(Fulltext):
    """
    instanciado com node de article ou sub-article
    """

    @property
    def related_articles(self):
        if not hasattr(self, '_related_articles'):
            fulltext_dates = FulltextRelatedArticles(self.node)
            self._related_articles = fulltext_dates.related_articles
        return self._related_articles

    @property
    def contribs(self):
        if not hasattr(self, '_contribs'):
            self._contribs = []
            for contrib in self.front.xpath('.//contrib'):
                self._contribs.append(contrib)
        return self._contribs

    @property
    def history(self):
        if not hasattr(self, '_history'):
            fulltext_dates = FulltextDates(self.node)
            self._history = fulltext_dates.history_dates_dict
        return self._history

    @property
    def license_code(self):
        if not hasattr(self, '_license_code'):
            self._license_code = None
            node = self.node.find(".//permission//license")
            if node is not None:
                fulltext_dates = License(self.node)
                self._license_code = License(self.node).code
        return self._license_code

    @property
    def custom_meta_items(self):
        if not hasattr(self, '_custom_meta_items'):
            self._custom_meta_items = []
            for item in self.front.xpath('.//custom-meta'):
                self._custom_meta_items.append(CustomMeta(item))
        return self._custom_meta_items
