from packtools.sps.models.article_authors import Authors
from packtools.sps.models.dates import ArticleDates
from packtools.sps.models.peer_review import PeerReview
from packtools.sps.models.related_articles import RelatedItems
from packtools.sps.validation.exceptions import ValidationPeerReviewException
from packtools.sps.validation.utils import format_response


def _get_parent(node):
    return node.tag if node.tag == 'sub-article' else 'article'


def _get_parent_id(node):
    return node.get('id')


class RelatedArticleValidation:
    def __init__(self, related_article_type, href, link_type, related_article_type_list=None, link_type_list=None):
        self.related_article_type = related_article_type
        self.related_article_type_list = related_article_type_list
        self.href = href
        self.link_type = link_type
        self.link_type_list = link_type_list

    @property
    def related_article_type_validation(self, related_article_type_list=None):
        # Para parecer como <article> além dos elementos mencionados anteriormente, adiciona-se a tag
        # de <related-article> referenciando o artigo que sofreu o parecer. Neste caso utiliza-se:
        # @related-article-type com valor "peer-reviewed-material";
        related_article_type_list = related_article_type_list or self.related_article_type_list
        if related_article_type_list is None:
            raise ValidationPeerReviewException("Function requires list of related articles")
        is_valid = self.related_article_type in self.related_article_type_list
        yield format_response(
            item='related-article',
            sub_item='@related-article-type',
            is_valid=is_valid,
            validation_type='value in list',
            expected=self.related_article_type_list,
            obtained=self.related_article_type,
            advice=f'provide one item of this list: {self.related_article_type_list}'
        )

    @property
    def related_article_href_validation(self):
        # Para parecer como <article> além dos elementos mencionados anteriormente, adiciona-se a tag
        # de <related-article> referenciando o artigo que sofreu o parecer. Neste caso utiliza-se:
        # @xlink:href com número DOI do artigo revisado;
        is_valid = self.href is not None
        yield format_response(
            item='related-article',
            sub_item='@xlink:href',
            is_valid=is_valid,
            validation_type='exist',
            expected=self.href if is_valid else 'a value for <related-article @xlink:href>',
            obtained=self.href,
            advice='provide a value for <related-article @xlink:href>'
        )

    @property
    def related_article_ext_link_type_validation(self, link_type_list=None):
        # Para parecer como <article> além dos elementos mencionados anteriormente, adiciona-se a tag
        # de <related-article> referenciando o artigo que sofreu o parecer. Neste caso utiliza-se:
        # @ext-link-type com valor "doi".
        link_type_list = link_type_list or self.link_type_list
        if link_type_list is None:
            raise ValidationPeerReviewException("Function requires list of link types")
        is_valid = self.link_type in self.link_type_list
        yield format_response(
            item='related-article',
            sub_item='@ext-link-type',
            is_valid=is_valid,
            validation_type='value in list',
            expected=self.link_type_list,
            obtained=self.link_type,
            advice=f'provide one item of this list: {self.link_type_list}'
        )


class CustomMetaPeerReviewValidation:
    def __init__(self, meta_name, meta_value, meta_value_list=None):
        self.meta_name = meta_name
        self.meta_value = meta_value
        self.meta_value_list = meta_value_list

    @property
    def custom_meta_name_validation(self):
        # Os pareceres marcados como <article> ou <sub-article> devem obrigatoriamente possuir os elementos
        # <custom-meta-group> + <custom-meta> + <meta-name> e <meta-value>
        obtained = self.meta_name
        is_valid = obtained is not None
        yield format_response(
            item='custom-meta',
            sub_item='meta-name',
            is_valid=is_valid,
            validation_type='exist',
            expected=obtained if is_valid else 'a value for <custom-meta>',
            obtained=obtained,
            advice='provide a value for <custom-meta>'
        )

    @property
    def custom_meta_value_validation(self, meta_value_list=None):
        # Os pareceres marcados como <article> ou <sub-article> devem obrigatoriamente possuir os elementos
        # <custom-meta-group> + <custom-meta> + <meta-name> e <meta-value>
        # Os termos possíveis para <meta-value> são:
        # revision, major-revision, minor-revision, reject, reject-with-resubmit, accept, formal-accept,
        # accept-in-principle
        meta_value_list = meta_value_list or self.meta_value_list
        if not meta_value_list:
            raise ValidationPeerReviewException("Function requires list of meta values")
        is_valid = self.meta_value in self.meta_value_list
        yield format_response(
            item='custom-meta',
            sub_item='meta-value',
            is_valid=is_valid,
            validation_type='value in list',
            expected=self.meta_value_list,
            obtained=self.meta_value,
            advice=f'provide one item of this list: {self.meta_value_list}'
        )


class AuthorPeerReviewValidation:
    def __init__(self, contrib, contrib_type_list=None, specific_use_list=None):
        self.contrib = contrib
        self.contrib_type_list = contrib_type_list
        self.specific_use_list = specific_use_list

    @property
    def contrib_type(self):
        return self.contrib.get("contrib-type")

    @property
    def specific_use(self):
        return [item.get("specific-use") for item in self.contrib.get("role")]

    @property
    def contrib_type_validation(self, contrib_type_list=None):
        # Os pareceres marcados como <article> ou <sub-article> devem obrigatoriamente possuir o elemento
        # @contrib-type com valor "author"
        contrib_type_list = contrib_type_list or self.contrib_type_list
        if contrib_type_list is None:
            raise ValidationPeerReviewException("Function requires list of contrib types")
        is_valid = self.contrib_type in self.contrib_type_list
        yield format_response(
            item='contrib',
            sub_item='@contrib-type',
            is_valid=is_valid,
            validation_type='value in list',
            expected=self.contrib_type_list,
            obtained=self.contrib_type,
            advice=f'provide one item of this list: {self.contrib_type_list}'
        )

    @property
    def role_specific_use_validation(self, specific_use_list=None):
        # Os pareceres marcados como <article> ou <sub-article> devem obrigatoriamente possuir o elemento
        # <role> com @specific-use com valores "reviewer" ou "editor"
        specific_use_list = specific_use_list or self.specific_use_list
        if specific_use_list is None:
            raise ValidationPeerReviewException("Function requires list of specific uses")
        is_valid = False
        obtained = None
        for item in self.specific_use:
            if item in self.specific_use_list:
                is_valid = True
                obtained = item
                break
        yield format_response(
            item='role',
            sub_item='@specific-use',
            is_valid=is_valid,
            validation_type='value in list',
            expected=self.specific_use_list,
            obtained=obtained,
            advice=f'provide one item of this list: {self.specific_use_list}'
        )


class DatePeerReviewValidation:
    def __init__(self, date_type, date_type_list=None):
        self.date_type = date_type
        self.date_type_list = date_type_list

    @property
    def date_type_validation(self, date_type_list=None):
        # Os pareceres marcados como <article> ou <sub-article> devem obrigatoriamente possuir o elemento
        # @date-type em <history> com valor "reviewer-report-received"
        date_type_list = date_type_list or self.date_type_list
        if date_type_list is None:
            raise ValidationPeerReviewException("Function requires list of date types")
        is_valid = self.date_type in self.date_type_list
        yield format_response(
            item='date',
            sub_item='@date-type',
            is_valid=is_valid,
            validation_type='value in list',
            expected=self.date_type_list,
            obtained=self.date_type,
            advice=f'provide one item of this list: {self.date_type_list}'
        )


class PeerReviewsValidation:
    def __init__(self, xml_tree, contrib_type_list=None, specific_use_list=None, date_type_list=None,
                 meta_value_list=None, related_article_type_list=None, link_type_list=None):
        self.xml_tree = xml_tree
        self.contrib_type_list = contrib_type_list
        self.specific_use_list = specific_use_list
        self.date_type_list = date_type_list
        self.meta_value_list = meta_value_list
        self.related_article_type_list = related_article_type_list
        self.link_type_list = link_type_list

    @property
    def article(self):
        if self.xml_tree.attrib.get("article-type") == "reviewer-report":
            node = self.xml_tree.find(".//article-meta")
            if node is not None:
                yield node

    @property
    def sub_articles(self):
        nodes = self.xml_tree.xpath(".//sub-article")
        for node in nodes:
            if node.get("article-type") == "reviewer-report":
                yield node

    @property
    def nodes(self):
        yield from self.article
        yield from self.sub_articles

    @property
    def nodes_validation(self):
        for node in self.nodes:
            yield from self.node_validation(node)
        for node in self.article:
            yield from self.specific_validation(node)

    def node_validation(self, node):
        yield from self.author_validation(node)
        yield from self.date_validation(node)
        yield from self.custom_meta_validation(node)

    def specific_validation(self, node):
        yield from self.related_article_validation(node)

    def author_validation(self, node, contrib_type_list=None, specific_use_list=None):
        contrib_type_list = contrib_type_list or self.contrib_type_list
        specific_use_list = specific_use_list or self.specific_use_list
        if contrib_type_list is None:
            raise ValidationPeerReviewException("Function requires list of contrib type")
        if specific_use_list is None:
            raise ValidationPeerReviewException("Function requires list of specific use")
        authors = Authors(node)
        for contrib in authors.contribs:
            validation = AuthorPeerReviewValidation(
                contrib=contrib,
                contrib_type_list=contrib_type_list,
                specific_use_list=specific_use_list
            )
            resps = list(validation.contrib_type_validation) + list(validation.role_specific_use_validation)
            for resp in resps:
                resp['title'] = 'Peer review validation'
                resp['parent'] = _get_parent(node)
                resp['parent_id'] = _get_parent_id(node)
                yield resp

    def date_validation(self, node, date_type_list=None):
        date_type_list = date_type_list or self.date_type_list
        if date_type_list is None:
            raise ValidationPeerReviewException("Function requires list of date types")
        dates = ArticleDates(node)
        for date_type in dates.history_dates_dict:
            validation = DatePeerReviewValidation(
                date_type=date_type,
                date_type_list=self.date_type_list
            )
            for resp in validation.date_type_validation:
                resp['title'] = 'Peer review validation'
                resp['parent'] = _get_parent(node)
                resp['parent_id'] = _get_parent_id(node)
                yield resp

    def custom_meta_validation(self, node, meta_value_list=None):
        meta_value_list = meta_value_list or self.meta_value_list
        if meta_value_list is None:
            raise ValidationPeerReviewException("Function requires list of meta values")
        peer_review = PeerReview(node)
        for item in peer_review.custom_meta:
            validation = CustomMetaPeerReviewValidation(
                meta_name=item.meta_name,
                meta_value=item.meta_value,
                meta_value_list=self.meta_value_list
            )
            resps = list(validation.custom_meta_name_validation) + list(validation.custom_meta_value_validation)
            for resp in resps:
                resp['title'] = 'Peer review validation'
                resp['parent'] = _get_parent(node)
                resp['parent_id'] = _get_parent_id(node)
                yield resp

    def related_article_validation(self, node, related_article_type_list=None, link_type_list=None):
        related_article_type_list = related_article_type_list or self.related_article_type_list
        link_type_list = link_type_list or self.link_type_list
        if related_article_type_list is None:
            raise ValidationPeerReviewException("Function requires list of related article types")
        if link_type_list is None:
            raise ValidationPeerReviewException("Function requires list of link types")
        related_items = RelatedItems(node)
        for item in related_items.related_articles:
            validation = RelatedArticleValidation(
                related_article_type=item.get("related-article-type"),
                related_article_type_list=self.related_article_type_list,
                href=item.get("href"),
                link_type=item.get("ext-link-type"),
                link_type_list=self.link_type_list
            )
            resps = list(validation.related_article_type_validation) + \
                    list(validation.related_article_href_validation) + \
                    list(validation.related_article_ext_link_type_validation)

            for resp in resps:
                resp['title'] = 'Peer review validation'
                resp['parent'] = _get_parent(node)
                resp['parent_id'] = _get_parent_id(node)
                yield resp
