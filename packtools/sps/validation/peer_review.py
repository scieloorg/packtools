from packtools.sps.models.article_contribs import ContribGroup
from packtools.sps.models.article_dates import HistoryDates
from packtools.sps.models.peer_review import PeerReview, CustomMeta
from packtools.sps.models.v2.related_articles import RelatedArticles
from packtools.sps.utils.xml_utils import put_parent_context
from packtools.sps.validation.exceptions import ValidationPeerReviewException
from packtools.sps.validation.utils import format_response


class RelatedArticleValidation:
    def __init__(
        self, related_article, related_article_type_list=None, link_type_list=None
    ):
        self.related_article = related_article
        self.related_article_type_list = related_article_type_list
        self.link_type_list = link_type_list

    @property
    def related_article_type_validation(
        self, related_article_type_list=None, error_level="ERROR"
    ):
        # Para parecer como <article> além dos elementos mencionados anteriormente, adiciona-se a tag
        # de <related-article> referenciando o artigo que sofreu o parecer. Neste caso utiliza-se:
        # @related-article-type com valor "peer-reviewed-material";
        related_article_type_list = (
            related_article_type_list or self.related_article_type_list
        )
        if related_article_type_list is None:
            raise ValidationPeerReviewException(
                "Function requires list of related articles"
            )
        related_article_type = self.related_article.get("related-article-type")
        is_valid = related_article_type in self.related_article_type_list
        yield format_response(
            title="Peer review validation",
            parent=self.related_article.get("parent"),
            parent_id=self.related_article.get("parent_id"),
            parent_article_type=self.related_article.get("parent_article_type"),
            parent_lang=self.related_article.get("parent_lang"),
            item="related-article",
            sub_item="@related-article-type",
            validation_type="value in list",
            is_valid=is_valid,
            expected=self.related_article_type_list,
            obtained=related_article_type,
            advice=f"provide one item of this list: {self.related_article_type_list}",
            data=self.related_article,
            error_level=error_level,
        )

    @property
    def related_article_href_validation(self, error_level="ERROR"):
        # Para parecer como <article> além dos elementos mencionados anteriormente, adiciona-se a tag
        # de <related-article> referenciando o artigo que sofreu o parecer. Neste caso utiliza-se:
        # @xlink:href com número DOI do artigo revisado;
        href = self.related_article.get("href")
        is_valid = bool(href)
        yield format_response(
            title="Peer review validation",
            parent=self.related_article.get("parent"),
            parent_id=self.related_article.get("parent_id"),
            parent_article_type=self.related_article.get("parent_article_type"),
            parent_lang=self.related_article.get("parent_lang"),
            item="related-article",
            sub_item="@xlink:href",
            validation_type="exist",
            is_valid=is_valid,
            expected=href if is_valid else "a value for <related-article @xlink:href>",
            obtained=href,
            advice="provide a value for <related-article @xlink:href>",
            data=self.related_article,
            error_level=error_level,
        )

    @property
    def related_article_ext_link_type_validation(
        self, link_type_list=None, error_level="ERROR"
    ):
        # Para parecer como <article> além dos elementos mencionados anteriormente, adiciona-se a tag
        # de <related-article> referenciando o artigo que sofreu o parecer. Neste caso utiliza-se:
        # @ext-link-type com valor "doi".
        link_type_list = link_type_list or self.link_type_list
        if link_type_list is None:
            raise ValidationPeerReviewException("Function requires list of link types")
        link_type = self.related_article.get("ext-link-type")
        is_valid = link_type in self.link_type_list
        yield format_response(
            title="Peer review validation",
            parent=self.related_article.get("parent"),
            parent_id=self.related_article.get("parent_id"),
            parent_article_type=self.related_article.get("parent_article_type"),
            parent_lang=self.related_article.get("parent_lang"),
            item="related-article",
            sub_item="@ext-link-type",
            validation_type="value in list",
            is_valid=is_valid,
            expected=self.link_type_list,
            obtained=link_type,
            advice=f"provide one item of this list: {self.link_type_list}",
            data=self.related_article,
            error_level=error_level,
        )


class CustomMetaPeerReviewValidation:
    def __init__(self, custom_meta, meta_value_list=None):
        self.custom_meta = custom_meta
        self.meta_value_list = meta_value_list

    @property
    def custom_meta_name_validation(self, error_level="ERROR"):
        # Os pareceres marcados como <article> ou <sub-article> devem obrigatoriamente possuir os elementos
        # <custom-meta-group> + <custom-meta> + <meta-name> e <meta-value>
        obtained = self.custom_meta.get("meta_name")
        is_valid = obtained is not None
        yield format_response(
            title="Peer review validation",
            parent=self.custom_meta.get("parent"),
            parent_id=self.custom_meta.get("parent_id"),
            parent_article_type=self.custom_meta.get("parent_article_type"),
            parent_lang=self.custom_meta.get("parent_lang"),
            item="custom-meta",
            sub_item="meta-name",
            validation_type="exist",
            is_valid=is_valid,
            expected=obtained if is_valid else "a value for <custom-meta>",
            obtained=obtained,
            advice="provide a value for <custom-meta>",
            data=self.custom_meta,
            error_level=error_level,
        )

    @property
    def custom_meta_value_validation(self, meta_value_list=None, error_level="ERROR"):
        # Os pareceres marcados como <article> ou <sub-article> devem obrigatoriamente possuir os elementos
        # <custom-meta-group> + <custom-meta> + <meta-name> e <meta-value>
        # Os termos possíveis para <meta-value> são:
        # revision, major-revision, minor-revision, reject, reject-with-resubmit, accept, formal-accept,
        # accept-in-principle
        meta_value_list = meta_value_list or self.meta_value_list
        if not meta_value_list:
            raise ValidationPeerReviewException("Function requires list of meta values")
        obtained = self.custom_meta.get("meta_value")
        is_valid = obtained in self.meta_value_list
        yield format_response(
            title="Peer review validation",
            parent=self.custom_meta.get("parent"),
            parent_id=self.custom_meta.get("parent_id"),
            parent_article_type=self.custom_meta.get("parent_article_type"),
            parent_lang=self.custom_meta.get("parent_lang"),
            item="custom-meta",
            sub_item="meta-value",
            validation_type="value in list",
            is_valid=is_valid,
            expected=self.meta_value_list,
            obtained=obtained,
            advice=f"provide one item of this list: {self.meta_value_list}",
            data=self.custom_meta,
            error_level=error_level,
        )


class AuthorPeerReviewValidation:
    def __init__(self, contrib, contrib_type_list=None, specific_use_list=None):
        self.contrib = contrib
        self.contrib_type_list = contrib_type_list
        self.specific_use_list = specific_use_list

    @property
    def specific_use(self):
        return [item.get("specific-use") for item in self.contrib.get("contrib_role")]

    @property
    def contrib_type_validation(self, contrib_type_list=None, error_level="ERROR"):
        # Os pareceres marcados como <article> ou <sub-article> devem obrigatoriamente possuir o elemento
        # @contrib-type com valor "author"
        contrib_type_list = contrib_type_list or self.contrib_type_list
        if contrib_type_list is None:
            raise ValidationPeerReviewException(
                "Function requires list of contrib types"
            )
        is_valid = self.contrib.get("contrib_type") in self.contrib_type_list
        yield format_response(
            title="Peer review validation",
            parent=self.contrib.get("parent"),
            parent_id=self.contrib.get("parent_id"),
            parent_article_type=self.contrib.get("parent_article_type"),
            parent_lang=self.contrib.get("parent_lang"),
            item="contrib",
            sub_item="@contrib-type",
            validation_type="value in list",
            is_valid=is_valid,
            expected=self.contrib_type_list,
            obtained=self.contrib.get("contrib_type"),
            advice=f"provide one item of this list: {self.contrib_type_list}",
            data=self.contrib,
            error_level=error_level,
        )

    @property
    def role_specific_use_validation(self, specific_use_list=None, error_level="ERROR"):
        # Os pareceres marcados como <article> ou <sub-article> devem obrigatoriamente possuir o elemento
        # <role> com @specific-use com valores "reviewer" ou "editor"
        specific_use_list = specific_use_list or self.specific_use_list
        if specific_use_list is None:
            raise ValidationPeerReviewException(
                "Function requires list of specific uses"
            )
        is_valid = False
        obtained = self.specific_use
        for item in self.specific_use:
            if item in self.specific_use_list:
                is_valid = True
                break
        yield format_response(
            title="Peer review validation",
            parent=self.contrib.get("parent"),
            parent_id=self.contrib.get("parent_id"),
            parent_article_type=self.contrib.get("parent_article_type"),
            parent_lang=self.contrib.get("parent_lang"),
            item="role",
            sub_item="@specific-use",
            validation_type="value in list",
            is_valid=is_valid,
            expected=self.specific_use_list,
            obtained=obtained,
            advice=f"provide one item of this list: {self.specific_use_list}",
            data=self.contrib,
            error_level=error_level,
        )


class DatePeerReviewValidation:
    def __init__(self, date, date_type, date_type_list=None):
        self.date = date
        self.date_type = date_type
        self.date_type_list = date_type_list

    @property
    def date_type_validation(self, date_type_list=None, error_level="ERROR"):
        # Os pareceres marcados como <article> ou <sub-article> devem obrigatoriamente possuir o elemento
        # @date-type em <history> com valor "reviewer-report-received"
        date_type_list = date_type_list or self.date_type_list
        if date_type_list is None:
            raise ValidationPeerReviewException("Function requires list of date types")
        is_valid = self.date_type in self.date_type_list
        yield format_response(
            title="Peer review validation",
            parent=self.date.get("parent"),
            parent_id=self.date.get("parent_id"),
            parent_article_type=self.date.get("parent_article_type"),
            parent_lang=self.date.get("parent_lang"),
            item="date",
            sub_item="@date-type",
            validation_type="value in list",
            is_valid=is_valid,
            expected=self.date_type_list,
            obtained=self.date_type,
            advice=f"provide one item of this list: {self.date_type_list}",
            data=self.date,
            error_level=error_level,
        )


class PeerReviewsValidation:
    def __init__(
        self,
        xml_tree,
        contrib_type_list=None,
        specific_use_list=None,
        date_type_list=None,
        meta_value_list=None,
        related_article_type_list=None,
        link_type_list=None,
    ):
        self.xml_tree = xml_tree
        self.contrib_type_list = contrib_type_list
        self.specific_use_list = specific_use_list
        self.date_type_list = date_type_list
        self.meta_value_list = meta_value_list
        self.related_article_type_list = related_article_type_list
        self.link_type_list = link_type_list

    def article(self):
        if self.xml_tree.attrib.get("article-type") == "reviewer-report":
            node = self.xml_tree.find(".//article-meta")
            node_tag = "article"
            if node is not None:
                node_id = self.xml_tree.attrib.get("id")
                node_lang = self.xml_tree.get(
                    "{http://www.w3.org/XML/1998/namespace}lang"
                )
                yield node, node_tag, node_id, node_lang

    def sub_articles(self):
        nodes = self.xml_tree.xpath(".//sub-article")
        node_tag = "sub-article"
        for node in nodes:
            if node.get("article-type") == "reviewer-report":
                node_id = node.get("id")
                node_lang = node.get("{http://www.w3.org/XML/1998/namespace}lang")
                yield node, node_tag, node_id, node_lang

    def nodes(self):
        yield from self.article()
        yield from self.sub_articles()

    def validate(self):
        article_type = self.xml_tree.get("article-type")
        for node, node_tag, node_id, node_lang in self.nodes():
            for item in self.node_validation(node):
                yield put_parent_context(
                    item, node_lang, article_type, node_tag, node_id
                )
        for node, node_tag, node_id, node_lang in self.article():
            for item in self.specific_validation():
                yield put_parent_context(
                    item, node_lang, article_type, node_tag, node_id
                )

    def node_validation(self, node):
        yield from self.author_validation(node)
        yield from self.date_validation()
        yield from self.custom_meta_validation(node)

    def specific_validation(self):
        yield from self.related_article_validation()

    def author_validation(self, node, contrib_type_list=None, specific_use_list=None):
        contrib_type_list = contrib_type_list or self.contrib_type_list
        specific_use_list = specific_use_list or self.specific_use_list
        if contrib_type_list is None:
            raise ValidationPeerReviewException(
                "Function requires list of contrib type"
            )
        if specific_use_list is None:
            raise ValidationPeerReviewException(
                "Function requires list of specific use"
            )
        authors = ContribGroup(node)
        for contrib in authors.contribs:
            validation = AuthorPeerReviewValidation(
                contrib=contrib,
                contrib_type_list=contrib_type_list,
                specific_use_list=specific_use_list,
            )
            yield from validation.contrib_type_validation
            yield from validation.role_specific_use_validation

    def date_validation(self, date_type_list=None):
        date_type_list = date_type_list or self.date_type_list
        if date_type_list is None:
            raise ValidationPeerReviewException("Function requires list of date types")
        for date in HistoryDates(self.xml_tree).history_dates():
            for date_type in date.get("history"):
                validation = DatePeerReviewValidation(
                    date=date, date_type=date_type, date_type_list=self.date_type_list
                )
                yield from validation.date_type_validation

    def custom_meta_validation(self, node, meta_value_list=None):
        meta_value_list = meta_value_list or self.meta_value_list
        if meta_value_list is None:
            raise ValidationPeerReviewException("Function requires list of meta values")
        peer_review = CustomMeta(node)
        validation = CustomMetaPeerReviewValidation(
            custom_meta=peer_review.data, meta_value_list=self.meta_value_list
        )
        yield from validation.custom_meta_name_validation
        yield from validation.custom_meta_value_validation

    def related_article_validation(
        self, related_article_type_list=None, link_type_list=None
    ):
        related_article_type_list = (
            related_article_type_list or self.related_article_type_list
        )
        link_type_list = link_type_list or self.link_type_list
        if related_article_type_list is None:
            raise ValidationPeerReviewException(
                "Function requires list of related article types"
            )
        if link_type_list is None:
            raise ValidationPeerReviewException("Function requires list of link types")
        related_items = RelatedArticles(self.xml_tree)
        for item in related_items.related_articles():
            validation = RelatedArticleValidation(
                related_article=item,
                related_article_type_list=self.related_article_type_list,
                link_type_list=self.link_type_list,
            )
            yield from validation.related_article_type_validation
            yield from validation.related_article_href_validation
            yield from validation.related_article_ext_link_type_validation
