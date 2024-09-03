from packtools.sps.validation.utils import format_response
from packtools.sps.models.related_articles import RelatedItems
from packtools.sps.models.article_dates import HistoryDates


class ValidationBase:
    def __init__(self, xml_tree, expected_article_type, expected_related_article_type):
        self.xml_tree = xml_tree
        self.article_lang = xml_tree.get("{http://www.w3.org/XML/1998/namespace}lang")
        self.article_type = xml_tree.find(".").get("article-type")
        self.expected_article_type = expected_article_type
        self.expected_related_article_type = expected_related_article_type
        self.related_articles = self._get_related_articles()

    def validate_related_article(self, title, error_level="ERROR"):
        """
        Validates the related articles against the expected type and other criteria.

        Args:
            error_level (str, optional): The error level for the validation response. Defaults to "ERROR".

        Yields:
            dict: A formatted response indicating whether the validation passed or failed.
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
                    obtained=self._format_obtained(related_article),
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

    def _get_related_articles(self,):
        return [
            article for article in RelatedItems(self.xml_tree).related_articles
            if article.get("related-article-type") == self.expected_related_article_type
        ]

    def _format_obtained(self, related_article):
        return (
            f'<related-article ext-link-type="{related_article.get("ext-link-type")}" '
            f'id="{related_article.get("id")}" related-article-type="{related_article.get("related-article-type")}" '
            f'xlink:href="{related_article.get("href")}"/>'
        )


class ErrataValidation(ValidationBase):
    def __init__(self, xml_tree, expected_article_type, expected_related_article_type):
        super().__init__(xml_tree, expected_article_type, expected_related_article_type)

    def validate_related_article(self, error_level="ERROR", title="validation matching 'correction' and 'corrected-article'"):
        """
        Validates related articles specifically for corrected articles.

        Args:
            error_level (str, optional): The error level for the validation response. Defaults to "ERROR".

        Yields:
            dict: A formatted response indicating whether the validation passed or failed.
        """
        yield from super().validate_related_article(error_level=error_level, title=title)


class CorrectedArticleValidation(ValidationBase):
    def __init__(self, xml_tree, expected_article_type, expected_related_article_type):
        super().__init__(xml_tree, expected_article_type, expected_related_article_type)
        self.history_dates = self._get_history_dates()

    def validate_related_article(self, error_level="ERROR", title="validation matching 'correction' and 'correction-forward'"):
        """
        Validates related articles specifically for corrected articles.

        Args:
            error_level (str, optional): The error level for the validation response. Defaults to "ERROR".

        Yields:
            dict: A formatted response indicating whether the validation passed or failed.
        """
        yield from super().validate_related_article(error_level=error_level, title=title)

    def validate_history_dates(self, error_level="ERROR"):
        """
        Validates that the number of related articles matches the number of corresponding corrected dates.

        Args:
            error_level (str, optional): The error level for the validation response. Defaults to "ERROR".

        Yields:
            dict: A formatted response indicating whether the validation passed or failed.
        """
        history_date_count = len(self.history_dates)
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
                expected='equal numbers of <related-article type="correction-forward"> and <date type="corrected">',
                obtained=f'{related_article_count} <related-article type="correction-forward"> and {history_date_count} <date type="corrected">',
                advice='for each <related-article type="correction-forward">, there must be a corresponding <date type="corrected"> in <history>',
                data=self.history_dates,
                error_level=error_level,
            )

    def _get_history_dates(self):
        return [
            date for date in HistoryDates(self.xml_tree).history_dates()
            if "corrected" in date.get("history")
        ]
