"""
<related-article ext-link-type="doi" id="A01" related-article-type="commentary-article" xlink:href="10.1590/0101-3173.2022.v45n1.p139">
Referência do artigo comentado: FREITAS, J. H. de. Cinismo e indiferenciación: la huella de Glucksmann en
<italic>El coraje de la verdad</italic>
de Foucault.
<bold>Trans/form/ação</bold>
: revista de Filosofia da Unesp, v. 45, n. 1, p. 139-158, 2022.
</related-article>
"""

from packtools.sps.utils.xml_utils import put_parent_context, process_subtags


class RelatedArticle:
    def __init__(self, related_article_node):
        self.related_article_node = related_article_node
        self.ext_link_type = self.related_article_node.get("ext-link-type")
        self.related_article_type = self.related_article_node.get("related-article-type")
        self.id = self.related_article_node.get("id")
        self.href = self.related_article_node.get("{http://www.w3.org/1999/xlink}href")
        self.text = process_subtags(self.related_article_node)

    def data(self):
        return {
            "ext-link-type": self.ext_link_type,
            "id": self.id,
            "related-article-type": self.related_article_type,
            "href": self.href,
            "text": self.text
        }


class RelatedArticlesByNode:
    def __init__(self, node):
        self.node = node
        self.node = node
        self.parent = self.node.tag
        self.parent_id = self.node.get("id")
        self.article_type = node.get("article-type")
        self.lang = self.node.get("{http://www.w3.org/XML/1998/namespace}lang")

    def related_articles(self):
        if self.parent == "article":
            path = ".//article-meta//related-article"
        else:
            path = ".//front-stub//related-article"
        for related_article in self.node.xpath(path):
            data = RelatedArticle(related_article).data()
            yield put_parent_context(
                data, self.lang, self.article_type, self.parent, self.parent_id
            )


class RelatedArticles:
    def __init__(self, xml_tree):
        self.xml_tree = xml_tree

    def article(self):
        yield from RelatedArticlesByNode(self.xml_tree.find(".")).related_articles()

    def sub_articles(self):
        for sub_article in self.xml_tree.xpath(".//sub-article"):
            yield from RelatedArticlesByNode(sub_article).related_articles()

    def related_articles(self):
        yield from self.article()
        yield from self.sub_articles()
