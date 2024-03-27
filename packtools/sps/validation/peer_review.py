from packtools.sps.models.article_and_subarticles import ArticleAndSubArticles
from packtools.sps.models.article_authors import Authors
from packtools.sps.models.dates import ArticleDates
from packtools.sps.models.peer_review import PeerReview
from packtools.sps.models.related_articles import RelatedItems
from packtools.sps.validation.exceptions import ValidationPeerReviewException
from packtools.sps.validation.utils import format_response

from packtools.sps.validation.article_authors import ArticleAuthorsValidation


class PeerReviewValidation:
    def __init__(self, xml_tree, contrib_type_list=None, specific_use_list=None, date_type_list=None,
                 meta_value_list=None, related_article_type_list=None, link_type_list=None):
        self.xml_tree = xml_tree
        self.contrib_type_list = contrib_type_list
        self.specific_use_list = specific_use_list
        self.date_type_list = date_type_list
        self.meta_value_list = meta_value_list
        self.related_article_type_list = related_article_type_list
        self.link_type_list = link_type_list

    title = 'Peer review validation'

    def _get_specific_use(self, contrib):
        return [item.get("specific-use") for item in contrib.get("role")]

    def _get_date_types(self, node):
        return [date_type for date_type in ArticleDates(node).history_dates_dict]

    def _get_articles_by_type(self, node, is_article=False):
        if node.get("article-type") == "reviewer-report":
            return node.xpath(".//article-meta")[0] if is_article else node

    def _get_meta_values(self, node):
        peer_review = PeerReview(node)
        return list(peer_review.meta_values)

    def _get_related_article_attrib(self, node, sub_item):
        related_items = RelatedItems(node)
        return [
            item.get(sub_item) for item in related_items.related_articles
            if item.get(sub_item)
        ]

    def peer_review_validation(self):
        article = [
            self._get_articles_by_type(node, is_article=True)
            for node in self.xml_tree.xpath(".") if node is not None
        ]
        sub_articles = [
            self._get_articles_by_type(node)
            for node in self.xml_tree.xpath(".//sub-article") if node is not None
        ]

        for node in article + sub_articles:
            authors = Authors(node)
            for contrib in authors.contribs:
                yield from self.contrib_type_validation(contrib.get("contrib-type"))
                yield from self.role_specific_use_validation(self._get_specific_use(contrib))
            yield from self.date_type_validation(self._get_date_types(node))
            yield from self.custom_meta_name_validation(node)
            yield from self.custom_meta_value_validation(self._get_meta_values(node))
        for node in article:
            related_article_types = self._get_related_article_attrib(node, "related-article-type")
            related_article_ext_link_type = self._get_related_article_attrib(node, "ext-link-type")
            yield from self.related_article_type_validation(related_article_types)
            yield from self.related_article_xlink_href_validation(node)
            yield from self.related_article_ext_link_type_validation(related_article_ext_link_type)

    def contrib_type_validation(self, contrib_type, contrib_type_list=None):
        # Os pareceres marcados como <article> ou <sub-article> devem obrigatoriamente possuir o elemento
        # @contrib-type com valor "author"
        contrib_type_list = self.contrib_type_list or contrib_type_list
        if not contrib_type_list:
            raise ValidationPeerReviewException("Function requires list of contrib types")
        expected = ' | '.join(contrib_type_list)
        is_valid = contrib_type in contrib_type_list
        yield format_response(
            title=self.title,
            item='./contrib',
            sub_item='@contrib-type',
            is_valid=is_valid,
            validation_type='value in list',
            expected=expected,
            obtained=contrib_type,
            advice=f'provide one item of this list: {expected}'
        )

    def role_specific_use_validation(self, specific_use, specific_use_list=None):
        # Os pareceres marcados como <article> ou <sub-article> devem obrigatoriamente possuir o elemento
        # <role> com @specific-use com valores "reviewer" ou "editor"
        specific_use_list = self.specific_use_list or specific_use_list
        if not specific_use_list:
            raise ValidationPeerReviewException("Function requires list of specific use")
        expected = ' | '.join(specific_use_list)
        obtained = ' | '.join(specific_use)
        is_valid = False
        for item in specific_use:
            if item in specific_use_list:
                is_valid = True
        yield format_response(
            title=self.title,
            item='./role',
            sub_item='@specific-use',
            is_valid=is_valid,
            validation_type='value in list',
            expected=expected,
            obtained=obtained,
            advice=f'provide one item of this list: {expected}'
        )

    def date_type_validation(self, date_types, date_type_list=None):
        # Os pareceres marcados como <article> ou <sub-article> devem obrigatoriamente possuir o elemento
        # @date-type em <history> com valor "reviewer-report-received"
        date_type_list = self.date_type_list or date_type_list
        if not date_type_list:
            raise ValidationPeerReviewException("Function requires list of date type")
        expected = ' | '.join(date_type_list)
        obtained = ' | '.join(date_types)
        is_valid = False
        for date_type in date_types:
            if date_type in date_type_list:
                is_valid = True
        yield format_response(
            title=self.title,
            item='./date',
            sub_item='@date-type',
            is_valid=is_valid,
            validation_type='value in list',
            expected=expected,
            obtained=obtained,
            advice=f'provide one item of this list: {expected}'
        )

    def custom_meta_name_validation(self, node):
        # Os pareceres marcados como <article> ou <sub-article> devem obrigatoriamente possuir os elementos
        # <custom-meta-group> + <custom-meta> + <meta-name> e <meta-value>
        peer_review = PeerReview(node)
        obtained = " | ".join(list(peer_review.meta_names)) or None
        is_valid = obtained is not None
        yield format_response(
            title=self.title,
            item='.//custom-meta-group//custom-meta',
            sub_item='meta-name',
            is_valid=is_valid,
            validation_type='exist',
            expected=obtained if is_valid else 'a value for <custom-meta>',
            obtained=obtained,
            advice='provide a value for <custom-meta>'
        )

    def custom_meta_value_validation(self, meta_values, meta_value_list=None):
        # Os pareceres marcados como <article> ou <sub-article> devem obrigatoriamente possuir os elementos
        # <custom-meta-group> + <custom-meta> + <meta-name> e <meta-value>
        # Os termos possíveis para <meta-value> são:
        # revision, major-revision, minor-revision, reject, reject-with-resubmit, accept, formal-accept,
        # accept-in-principle
        meta_value_list = self.meta_value_list or meta_value_list
        if not meta_value_list:
            raise ValidationPeerReviewException("Function requires list of meta values")
        expected = ' | '.join(meta_value_list)
        obtained = ' | '.join(meta_values)
        is_valid = False
        for meta_value in meta_values:
            if meta_value in meta_value_list:
                is_valid = True
        yield format_response(
            title=self.title,
            item='.//custom-meta-group//custom-meta',
            sub_item='meta-value',
            is_valid=is_valid,
            validation_type='value in list',
            expected=expected,
            obtained=obtained,
            advice=f'provide one item of this list: {expected}'
        )

    def related_article_type_validation(self, related_article_types, related_article_type_list=None):
        # Para parecer como <article> além dos elementos mencionados anteriormente, adiciona-se a tag
        # de <related-article> referenciando o artigo que sofreu o parecer. Neste caso utiliza-se:
        # @related-article-type com valor "peer-reviewed-material";
        related_article_type_list = self.related_article_type_list or related_article_type_list
        if not related_article_type_list:
            raise ValidationPeerReviewException("Function requires list of related articles")
        expected = ' | '.join(related_article_type_list)
        obtained = ' | '.join(related_article_types)
        is_valid = False
        for related_article_type in related_article_types:
            if related_article_type in related_article_type_list:
                is_valid = True
        yield format_response(
            title=self.title,
            item='.//related-article',
            sub_item='@related-article-type',
            is_valid=is_valid,
            validation_type='value in list',
            expected=expected,
            obtained=obtained,
            advice=f'provide one item of this list: {expected}'
        )

    def related_article_xlink_href_validation(self, node):
        # Para parecer como <article> além dos elementos mencionados anteriormente, adiciona-se a tag
        # de <related-article> referenciando o artigo que sofreu o parecer. Neste caso utiliza-se:
        # @xlink:href com número DOI do artigo revisado;
        related_item = RelatedItems(node)
        related_articles = list(item.get("href") for item in related_item.related_articles if item.get("href"))
        if related_articles:
            obtained = " | ".join(related_articles)
        else:
            obtained = None
        is_valid = obtained is not None
        yield format_response(
            title=self.title,
            item='.//related-article',
            sub_item='@xlink:href',
            is_valid=is_valid,
            validation_type='exist',
            expected=obtained if is_valid else 'a value for <related-article @xlink:href>',
            obtained=obtained,
            advice='provide a value for <related-article @xlink:href>'
        )

    def related_article_ext_link_type_validation(self, link_types, link_type_list=None):
        # Para parecer como <article> além dos elementos mencionados anteriormente, adiciona-se a tag
        # de <related-article> referenciando o artigo que sofreu o parecer. Neste caso utiliza-se:
        # @ext-link-type com valor "doi".
        link_type_list = self.link_type_list or link_type_list
        if not link_type_list:
            raise ValidationPeerReviewException("Function requires list of link types")
        expected = ' | '.join(link_type_list)
        obtained = ' | '.join(link_types)
        is_valid = False
        for link_type in link_types:
            if link_type in link_type_list:
                is_valid = True
        yield format_response(
            title=self.title,
            item='.//related-article',
            sub_item='@ext-link-type',
            is_valid=is_valid,
            validation_type='value in list',
            expected=expected,
            obtained=obtained,
            advice=f'provide one item of this list: {expected}'
        )
