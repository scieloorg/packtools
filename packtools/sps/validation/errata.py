from packtools.sps.validation.utils import format_response
from packtools.sps.models.related_articles import RelatedItems
from packtools.sps.models.article_dates import HistoryDates


def _get_related_articles(xml_tree, expected_related_article_type):
    return [
        article for article in RelatedItems(xml_tree).related_articles
        if article.get("related-article-type") == expected_related_article_type
    ]


def _format_obtained(related_article):
    return (
        f'<related-article ext-link-type="{related_article.get("ext-link-type")}" '
        f'id="{related_article.get("id")}" related-article-type="{related_article.get("related-article-type")}" '
        f'xlink:href="{related_article.get("href")}"/>'
    )


class ValidationBase:
    def __init__(self, xml_tree, expected_article_type, expected_related_article_type):
        self.xml_tree = xml_tree
        self.article_lang = xml_tree.get("{http://www.w3.org/XML/1998/namespace}lang")
        self.article_type = xml_tree.find(".").get("article-type")
        self.expected_article_type = expected_article_type
        self.expected_related_article_type = expected_related_article_type
        self.related_articles = _get_related_articles(xml_tree, expected_related_article_type)

    def validate_related_article(self, title, error_level="ERROR"):
        """
        Validates the related articles against the expected type and other criteria.
        """
        if self.article_type != self.expected_article_type:
            return

        expected_response = f'at least one <related-article related-article-type="{self.expected_related_article_type}">'

        if self.related_articles:
            yield from (
                format_response(
                    title=title,
                    parent=related_article.get("parent"),
                    parent_id=related_article.get("parent_id"),
                    parent_article_type=related_article.get("parent_article_type"),
                    parent_lang=related_article.get("parent_lang"),
                    item="related-article",
                    sub_item="@related-article-type",
                    validation_type="match",
                    is_valid=True,
                    expected=expected_response,
                    obtained=_format_obtained(related_article),
                    advice=None,
                    data=related_article,
                    error_level=error_level
                )
                for related_article in self.related_articles
            )
        else:
            yield format_response(
                title=title,
                parent="article",
                parent_id=None,
                parent_article_type=self.article_type,
                parent_lang=self.article_lang,
                item="related-article",
                sub_item="@related-article-type",
                validation_type="exist",
                is_valid=False,
                expected=expected_response,
                obtained=None,
                advice=f'provide <related-article related-article-type="{self.expected_related_article_type}">',
                data=None,
                error_level=error_level
            )

    def validate_history_dates(self, expected_history_event, error_level="ERROR"):
        """
        Validates that the number of related articles matches the number of corresponding corrected dates.
        """
        history_data = list(HistoryDates(self.xml_tree).history_dates())
        history_dates = [date for date in history_data if expected_history_event in date.get("history")]
        history_date_count = len(history_dates)
        related_article_count = len(self.related_articles)

        if history_date_count < related_article_count:
            yield format_response(
                title="validation related and corrected dates count",
                parent="article",
                parent_id=None,
                parent_article_type=self.article_type,
                parent_lang=self.article_lang,
                item="related-article",
                sub_item="@related-article-type",
                validation_type="exist",
                is_valid=False,
                expected=f'equal numbers of <related-article type="{self.expected_related_article_type}"> and <date type="{expected_history_event}">',
                obtained=f'{related_article_count} <related-article type="{self.expected_related_article_type}"> and {history_date_count} <date type="{expected_history_event}">',
                advice=f'for each <related-article type="{self.expected_related_article_type}">, there must be a corresponding <date type="{expected_history_event}"> in <history>',
                data=history_data,
                error_level=error_level,
            )


class SpecificValidation(ValidationBase):
    """
    Base class for specific validations to handle common functionality for Errata, ArticleCorrected,
    ArticleRetracted, and ArticlePartiallyRetracted validations.
    """

    def __init__(self, xml_tree, expected_article_type, expected_related_article_type):
        super().__init__(xml_tree, expected_article_type, expected_related_article_type)

    def validate_related_article(self, error_level="ERROR", title=None):
        """
        Common logic for validating related articles, where `title` must be provided by subclasses.
        """
        if title is None:
            raise ValueError("Title must be provided for the validation.")
        yield from super().validate_related_article(title=title, error_level=error_level)

    def validate_history_dates(self, error_level="ERROR", expected_history_event=None):
        """
        Common logic for validating history dates, where `expected_history_event` must be provided by subclasses.
        """
        if expected_history_event is None:
            raise ValueError("Expected history event must be provided.")
        yield from super().validate_history_dates(expected_history_event=expected_history_event, error_level=error_level)


class ErrataValidation(SpecificValidation):
    def validate_related_article(self, error_level="ERROR", title="validation matching 'correction' and 'corrected-article'"):
        yield from super().validate_related_article(error_level=error_level, title=title)


class ArticleCorrectedValidation(SpecificValidation):
    def validate_related_article(self, error_level="ERROR", title="validation matching 'correction' and 'correction-forward'"):
        yield from super().validate_related_article(error_level=error_level, title=title)

    def validate_history_dates(self, error_level="ERROR", expected_history_event="corrected"):
        yield from super().validate_history_dates(error_level=error_level, expected_history_event=expected_history_event)


class ArticleRetractedInFullValidation(SpecificValidation):
    def validate_related_article(self, error_level="ERROR", title="validation matching 'retraction' and 'retracted-article'"):
        yield from super().validate_related_article(error_level=error_level, title=title)

    def validate_history_dates(self, error_level="ERROR", expected_history_event="retracted"):
        yield from super().validate_history_dates(error_level=error_level, expected_history_event=expected_history_event)


class ArticlePartiallyRetractedValidation(SpecificValidation):
    def validate_related_article(self, error_level="ERROR", title="validation matching 'retraction' and 'partial-retraction'"):
        yield from super().validate_related_article(error_level=error_level, title=title)

    def validate_history_dates(self, error_level="ERROR", expected_history_event="retracted"):
        yield from super().validate_history_dates(error_level=error_level, expected_history_event=expected_history_event)
