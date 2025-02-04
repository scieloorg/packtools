from packtools.sps.models.article_contribs import ContribGroup
from packtools.sps.models.article_dates import HistoryDates
from packtools.sps.models.peer_review import CustomMeta, PeerReview
from packtools.sps.models.v2.related_articles import RelatedArticles
from packtools.sps.utils.xml_utils import put_parent_context
from packtools.sps.validation.article_contribs import ContribValidation
from packtools.sps.validation.exceptions import ValidationPeerReviewException

# from packtools.sps.validation.dates import FulltextDatesValidation
from packtools.sps.validation.related_articles import (
    FulltextRelatedArticlesValidation,
)
from packtools.sps.validation.utils import build_response, format_response


class CustomMetaPeerReviewValidation:
    def __init__(self, custom_meta, params):
        self.custom_meta = custom_meta
        self.params = params

    def validate(self):
        yield from self.validate_custom_meta_name()
        yield from self.validate_custom_meta_value()

    def validate_custom_meta_name(self):
        """Validate custom metadata for peer review recommendations"""
        if not self.custom_meta["meta_name"]:
            yield build_response(
                title="Review recommendation name",
                parent=self.custom_meta,
                item="custom-meta",
                sub_item="meta-name",
                validation_type="exist",
                is_valid=False,
                expected="meta-name",
                obtained=None,
                advice=f"Peer review must include a recommendation (custom-meta/meta-name).",
                data=self.custom_meta,
                error_level=self.params.get("meta_name_error_level"),
            )

    def validate_custom_meta_value(self):
        """Validate custom metadata for peer review recommendations"""
        # Não validar os termos possíveis em <meta-value> podem haver termos diferentes então são termos opcionais
        if not self.custom_meta["meta_value"]:
            yield build_response(
                title="Review recommendation value",
                parent=self.custom_meta,
                item="custom-meta",
                sub_item="meta-value",
                validation_type="exist",
                is_valid=False,
                expected="meta-value",
                obtained=None,
                advice=f"Peer review must include a recommendation (custom-meta/meta-value).",
                data=self.custom_meta,
                error_level=self.params.get("meta_value_error_level"),
            )


class XMLPeerReviewValidation:
    """
    Validates a peer review document according to SciELO and JATS rules.

    This class orchestrates the validation of all aspects of a peer review,
    including contributors, dates, related articles, and specific peer review rules.
    """

    def __init__(self, xml_tree, params):
        """
        Initialize peer review validation.

        Parameters
        ----------
        peer_review : PeerReview
            Instance of PeerReview containing the document to validate
        params : dict, optional
            Configuration parameters for validation rules
        """
        self.xml_tree = xml_tree
        self.params = params or {}
        self._set_default_params()

    def _set_default_params(self):
        """Set default validation parameters"""
        self.params.setdefault("article_type_error_level", "CRITICAL")
        self.params.setdefault(
            "credit_taxonomy_terms_and_urls_error_level", "CRITICAL"
        )
        self.params.setdefault("orcid_format_error_level", "CRITICAL")
        self.params.setdefault("orcid_is_registered_error_level", "CRITICAL")
        self.params.setdefault("affiliations_error_level", "CRITICAL")
        self.params.setdefault("name_error_level", "CRITICAL")
        self.params.setdefault("collab_error_level", "CRITICAL")
        self.params.setdefault("name_or_collab_error_level", "CRITICAL")
        self.params.setdefault("missing_events_error_level", "CRITICAL")
        self.params.setdefault("meta_error_level", "CRITICAL")

        self.params.setdefault("required_events", ["reviewer-report-received"])
        self.params.setdefault("history_order_error_level", "CRITICAL")
        self.params.setdefault("ext_link_types", ["doi", "uri"])

        # Specific peer review parameters
        self.params.setdefault("article_type_list", ["reviewer-report"])
        self.params.setdefault("acceptable_article_types", ["reviewer-report"])
        self.params.setdefault("contrib_type_list", ["author"])
        self.params.setdefault("contrib_role_type_list", ["reviewer", "editor"])
        self.params["credit_taxonomy_terms_and_urls"] = []

    def validate(self):
        article = self.xml_tree.find(".")

        if article.get("article-type") == "reviewer-report":
            validator = PeerReviewValidation(article, self.params)
            yield from validator.validate()
        else:
            for node in article.xpath(
                "sub-article[@article-type='reviewer-report']"
            ):
                validator = PeerReviewValidation(node, self.params)
                yield from validator.validate()



class PeerReviewValidation:
    """
    Validates a peer review document according to SciELO and JATS rules.

    This class orchestrates the validation of all aspects of a peer review,
    including contributors, dates, related articles, and specific peer review rules.
    """

    def __init__(self, node, params):
        """
        Initialize peer review validation.

        Parameters
        ----------
        peer_review : PeerReview
            Instance of PeerReview containing the document to validate
        params : dict, optional
            Configuration parameters for validation rules
        """
        self.node = node
        self.peer_review = PeerReview(node)
        self.params = params or {}

    def validate_article_type(self):
        """Validate if the article type is correct for peer review"""
        # esta validação está propositalmente redundante
        # isso terá sido validado ao validar article_type genericamente
        article_type = self.peer_review.article_type
        is_valid = article_type in self.params["article_type_list"]

        if not is_valid:
            yield build_response(
                title="Article Type",
                parent=self.peer_review.attribs_parent_prefixed,
                item="article",
                sub_item="article-type",
                validation_type="value in list",
                is_valid=False,
                expected=self.params["article_type_list"],
                obtained=article_type,
                advice=f"Article type must be one of {self.params['article_type_list']}",
                data=self.peer_review.attribs,
                error_level=self.params["article_type_error_level"],
            )

    def validate_contribs(self):
        """Validate all contributors in the peer review"""
        # esta validação está propositalmente redundante
        # isso terá sido validado ao validar contrib genericamente
        for contrib in self.peer_review.contribs:
            validator = ContribValidation(contrib.data, self.params)
            yield from validator.validate()

    def validate_history_dates(self):
        """Validate dates in the peer review"""
        # esta validação está propositalmente redundante
        # isso terá sido validado ao validar contrib genericamente
        for item in self.params["required_events"]:
            if not self.peer_review.history_dates.get(item):
                yield build_response(
                    title="Required history date",
                    parent=self.peer_review.attribs_parent_prefixed,
                    item="history",
                    sub_item="date",
                    validation_type="exist",
                    is_valid=False,
                    expected=item,
                    obtained=list(self.peer_review.history_dates.keys()),
                    advice=f"history must have date which date-type is: {item}",
                    data=self.peer_review.history_dates,
                    error_level=self.params["missing_events_error_level"],
                )

    def validate_related_articles(self):
        """Validate related articles"""
        validator = FulltextRelatedArticlesValidation(
            self.node, params=self.params
        )
        yield from validator.validate()

    def validate_custom_meta(self):
        """Validate custom metadata for peer review recommendations"""
        for meta in self.peer_review.custom_meta_items:

            item = {}
            item.update(meta.data)
            item.update(self.peer_review.attribs_parent_prefixed)
            validator = CustomMetaPeerReviewValidation(item, self.params)
            yield from validator.validate()

    def validate(self):
        """
        Run all validations for the peer review.

        Returns
        -------
        list
            List of validation results
        """
        if self.node.get("article-type") == "reviewer-report":
            yield from self.validate_article_type()
            yield from self.validate_contribs()
            yield from self.validate_history_dates()
            yield from self.validate_related_articles()
            yield from self.validate_custom_meta()

            for node in self.peer_review.translations:
                validator = PeerReviewValidation(node)
                yield from validator.validate()
