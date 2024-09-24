from packtools.sps.validation.utils import format_response
from packtools.sps.models.v2.related_articles import RelatedArticles
from packtools.sps.models.article_dates import ArticleDates


class RelatedArticlesValidation:
    def __init__(self, xml_tree, correspondence_list):
        self.xml_tree = xml_tree
        self.correspondence_list = correspondence_list
        self.article_type = xml_tree.find(".").get("article-type")
        self.related_articles = list(RelatedArticles(xml_tree).related_articles())
        self.history_dates = ArticleDates(xml_tree).history_dates_dict

    def get_related_article_types_by_article_type(self, obtained_article_type):
        return {item['related-article-type'] for item in self.correspondence_list
                if item['article-type'] == obtained_article_type}

    def get_related_article_types(self):
        return {item['related-article-type'] for item in self.related_articles}

    def get_history_events_by_related_article_type(self):
        obtained_related_article_types = self.get_related_article_types()
        return {item['date-type'] for item in self.correspondence_list
                if item['related-article-type'] in obtained_related_article_types and item['date-type']}

    def get_history_events(self):
        return set(self.history_dates.keys())

    def validate_related_articles(self, error_level="ERROR"):
        expected_related_article_types = self.get_related_article_types_by_article_type(self.article_type)
        obtained_related_article_types = self.get_related_article_types()

        missing_types = expected_related_article_types - obtained_related_article_types
        if missing_types:
            related_article_type = next(iter(missing_types))
            yield format_response(
                title=f"matching '{self.article_type}' and '{related_article_type}'",
                parent="article",
                parent_id=None,
                parent_article_type=self.article_type,
                parent_lang=self.xml_tree.find(".").get("{http://www.w3.org/XML/1998/namespace}lang"),
                item="related-article",
                sub_item="@related-article-type",
                validation_type="match",
                is_valid=False,
                expected=f'at least one <related-article related-article-type="{related_article_type}">',
                obtained=None,
                advice=f'provide <related-article related-article-type="{related_article_type}">',
                data=self.related_articles,
                error_level=error_level
            )

    def validate_history_events(self, error_level="ERROR"):
        expected_history_events = self.get_history_events_by_related_article_type()
        obtained_history_events = self.get_history_events()

        missing_events = expected_history_events - obtained_history_events
        if missing_events:
            yield format_response(
                title="exist historical date event for the related-article",
                parent="article",
                parent_id=None,
                parent_article_type=self.article_type,
                parent_lang=self.xml_tree.find(".").get("{http://www.w3.org/XML/1998/namespace}lang"),
                item="related-article",
                sub_item="@related-article-type",
                validation_type="exist",
                is_valid=False,
                expected=' '.join([f'<date date-type="{event}">' for event in missing_events]),
                obtained=None,
                advice='provide ' + ' '.join([f'<date date-type="{event}">' for event in missing_events]),
                data=self.history_dates,
                error_level=error_level,
            )
