from packtools.sps.models.article_authors import Authors
from packtools.sps.models.dates import ArticleDates
from packtools.sps.models.peer_review import PeerReview
from packtools.sps.models.related_articles import RelatedItems
from packtools.sps.validation.exceptions import ValidationPeerReviewException
from packtools.sps.validation.utils import format_response


def get_node_id(node):
    return f" (sub-article: {node.get('id')})" if node.get('id') else " (article: main)"


class RelatedArticleTypePeerValidation:
    def __init__(self, related_article_type, related_article_type_list=None):
        self.related_article_type = related_article_type
        self.related_article_type_list = related_article_type_list

    @property
    def related_article_type_validation(self):
        # Para parecer como <article> além dos elementos mencionados anteriormente, adiciona-se a tag
        # de <related-article> referenciando o artigo que sofreu o parecer. Neste caso utiliza-se:
        # @related-article-type com valor "peer-reviewed-material";
        if not self.related_article_type_list:
            raise ValidationPeerReviewException("Function requires list of related articles")
        expected = ' | '.join(self.related_article_type_list)
        is_valid = self.related_article_type in self.related_article_type_list
        yield format_response(
            title="Peer review validation (article: main)",
            item='related-article',
            sub_item='@related-article-type',
            is_valid=is_valid,
            validation_type='value in list',
            expected=expected,
            obtained=self.related_article_type,
            advice=f'provide one item of this list: {expected}'
        )


class RelatedArticleXlinkPeerValidation:
    def __init__(self, hrefs):
        self.hrefs = hrefs

    @property
    def related_article_xlink_href_validation(self):
        # Para parecer como <article> além dos elementos mencionados anteriormente, adiciona-se a tag
        # de <related-article> referenciando o artigo que sofreu o parecer. Neste caso utiliza-se:
        # @xlink:href com número DOI do artigo revisado;
        if self.hrefs:
            obtained = " | ".join(self.hrefs)
        else:
            obtained = None
        is_valid = obtained is not None
        yield format_response(
            title="Peer review validation (article: main)",
            item='related-article',
            sub_item='@xlink:href',
            is_valid=is_valid,
            validation_type='exist',
            expected=obtained if is_valid else 'a value for <related-article @xlink:href>',
            obtained=obtained,
            advice='provide a value for <related-article @xlink:href>'
        )


class RelatedArticleLinkTypePeerValidation:
    def __init__(self, link_type, link_type_list=None):
        self.link_type = link_type
        self.link_type_list = link_type_list

    @property
    def related_article_ext_link_type_validation(self):
        # Para parecer como <article> além dos elementos mencionados anteriormente, adiciona-se a tag
        # de <related-article> referenciando o artigo que sofreu o parecer. Neste caso utiliza-se:
        # @ext-link-type com valor "doi".
        if not self.link_type_list:
            raise ValidationPeerReviewException("Function requires list of link types")
        expected = ' | '.join(self.link_type_list)
        is_valid = self.link_type in self.link_type_list
        yield format_response(
            title="Peer review validation (article: main)",
            item='related-article',
            sub_item='@ext-link-type',
            is_valid=is_valid,
            validation_type='value in list',
            expected=expected,
            obtained=self.link_type,
            advice=f'provide one item of this list: {expected}'
        )


class CustomMetaPeerReviewValidation:
    def __init__(self, node_id, meta_names, meta_value_list=None):
        self.node_id = node_id
        self.meta_names = meta_names
        self.meta_value_list = meta_value_list

    @property
    def custom_meta_name_validation(self):
        # Os pareceres marcados como <article> ou <sub-article> devem obrigatoriamente possuir os elementos
        # <custom-meta-group> + <custom-meta> + <meta-name> e <meta-value>
        obtained = " | ".join(self.meta_names) if self.meta_names != [] else None
        is_valid = obtained is not None
        yield format_response(
            title='Peer review validation' + self.node_id,
            item='custom-meta',
            sub_item='meta-name',
            is_valid=is_valid,
            validation_type='exist',
            expected=obtained if is_valid else 'a value for <custom-meta>',
            obtained=obtained,
            advice='provide a value for <custom-meta>'
        )

    def custom_meta_value_validation(self, meta_value):
        # Os pareceres marcados como <article> ou <sub-article> devem obrigatoriamente possuir os elementos
        # <custom-meta-group> + <custom-meta> + <meta-name> e <meta-value>
        # Os termos possíveis para <meta-value> são:
        # revision, major-revision, minor-revision, reject, reject-with-resubmit, accept, formal-accept,
        # accept-in-principle
        if not self.meta_value_list:
            raise ValidationPeerReviewException("Function requires list of meta values")
        expected = ' | '.join(self.meta_value_list)
        is_valid = meta_value in self.meta_value_list
        yield format_response(
            title='Peer review validation' + self.node_id,
            item='custom-meta',
            sub_item='meta-value',
            is_valid=is_valid,
            validation_type='value in list',
            expected=expected,
            obtained=meta_value,
            advice=f'provide one item of this list: {expected}'
        )


class AuthorPeerReviewValidation:
    def __init__(self, contrib, node_id, contrib_type_list=None, specific_use_list=None):
        self.contrib = contrib
        self.node_id = node_id
        self.contrib_type_list = contrib_type_list
        self.specific_use_list = specific_use_list

    @property
    def contrib_type(self):
        return self.contrib.get("contrib-type")

    @property
    def specific_use(self):
        return [item.get("specific-use") for item in self.contrib.get("role")]

    @property
    def contrib_type_validation(self):
        # Os pareceres marcados como <article> ou <sub-article> devem obrigatoriamente possuir o elemento
        # @contrib-type com valor "author"
        if not self.contrib_type_list:
            raise ValidationPeerReviewException("Function requires list of contrib types")
        expected = ' | '.join(self.contrib_type_list)
        is_valid = self.contrib_type in self.contrib_type_list
        yield format_response(
            title='Peer review validation' + self.node_id,
            item='contrib',
            sub_item='@contrib-type',
            is_valid=is_valid,
            validation_type='value in list',
            expected=expected,
            obtained=self.contrib_type,
            advice=f'provide one item of this list: {expected}'
        )

    @property
    def role_specific_use_validation(self):
        # Os pareceres marcados como <article> ou <sub-article> devem obrigatoriamente possuir o elemento
        # <role> com @specific-use com valores "reviewer" ou "editor"
        if not self.specific_use_list:
            raise ValidationPeerReviewException("Function requires list of specific use")
        expected = ' | '.join(self.specific_use_list)
        is_valid = False
        obtained = None
        for item in self.specific_use:
            if item in self.specific_use_list:
                is_valid = True
                obtained = item
                break
        yield format_response(
            title='Peer review validation' + self.node_id,
            item='role',
            sub_item='@specific-use',
            is_valid=is_valid,
            validation_type='value in list',
            expected=expected,
            obtained=obtained,
            advice=f'provide one item of this list: {expected}'
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
        related_items = RelatedItems(node)
        yield from self.related_article_type(related_items, "related-article-type")
        yield from self.related_article_href(related_items)
        yield from self.related_article_link_type(related_items, "ext-link-type")

    def author_validation(self, node):
        authors = Authors(node)
        for contrib in authors.contribs:
            validation = AuthorPeerReviewValidation(
                contrib=contrib,
                node_id=get_node_id(node),
                contrib_type_list=self.contrib_type_list,
                specific_use_list=self.specific_use_list
            )
            yield from validation.contrib_type_validation
            yield from validation.role_specific_use_validation

    def date_validation(self, node):
        dates = ArticleDates(node)
        for date_type in dates.history_dates_dict:
            validation = DatePeerReviewValidation(
                date_type=date_type,
                node_id=get_node_id(node),
                date_type_list=self.date_type_list
            )
            yield from validation.date_type_validation

    def custom_meta_validation(self, node):
        peer_review = PeerReview(node)
        meta_names = [item.meta_name for item in peer_review.custom_meta]
        validation = CustomMetaPeerReviewValidation(
            node_id=get_node_id(node),
            meta_names=meta_names,
            meta_value_list=self.meta_value_list
        )
        yield from validation.custom_meta_name_validation
        for meta_value in [item.meta_value for item in peer_review.custom_meta]:
            yield from validation.custom_meta_value_validation(meta_value)

    def related_article_type(self, related_items, sub_item):
        for item in related_items.related_articles:
            validation = RelatedArticleTypePeerValidation(
                related_article_type=item.get(sub_item),
                related_article_type_list=self.related_article_type_list
            )
            yield from validation.related_article_type_validation

    def related_article_href(self, related_items):
        validation = RelatedArticleXlinkPeerValidation(
            hrefs=list(item.get("href") for item in related_items.related_articles if item.get("href"))
        )
        yield from validation.related_article_xlink_href_validation

    def related_article_link_type(self, related_items, sub_item):
        for item in related_items.related_articles:
            validation = RelatedArticleLinkTypePeerValidation(
                link_type=item.get(sub_item),
                link_type_list=self.link_type_list
            )
            yield from validation.related_article_ext_link_type_validation
