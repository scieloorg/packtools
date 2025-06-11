class Fulltext:

    def __init__(self, node, original_article_type=None):
        """
        node : article or sub-article
        """
        self._original_article_type = original_article_type
        self.node = node
        self.tag = node.tag
        self.lang = node.get("{http://www.w3.org/XML/1998/namespace}lang")
        self.article_type = node.get("article-type")
        self.id = node.get("id")

    @property
    def original_article_type(self):
        if not self._original_article_type:
            if self.article_type == "translation":
                self._original_article_type = self.node.getparent().get("article-type")
            else:
                self._original_article_type = self.node.get("article-type")
        return self._original_article_type

    @property
    def front(self):
        if not hasattr(self, "_front"):
            if self.tag == "article":
                self._front = self.node.find("front")
            else:
                self._front = self.node.find("front-stub")
        return self._front

    @property
    def body(self):
        if not hasattr(self, "_body"):
            self._body = self.node.find("body")
        return self._body

    @property
    def back(self):
        if not hasattr(self, "_back"):
            self._back = self.node.find("back")
        return self._back

    @property
    def sub_articles(self):
        if not hasattr(self, "_sub_articles"):
            self._sub_articles = self.node.xpath("sub-article")
        return self._sub_articles

    @property
    def translations(self):
        if not hasattr(self, "_translations"):
            self._translations = self.node.xpath(
                "sub-article[@article-type='translation']"
            )
        return self._translations

    @property
    def not_translations(self):
        if not hasattr(self, "_not_translations"):
            self._not_translations = self.node.xpath(
                "sub-article[@article-type!='translation']"
            )
        return self._not_translations

    @property
    def attribs(self):
        return {
            "tag": self.tag,
            "id": self.id,
            "lang": self.lang,
            "article_type": self.article_type,
        }

    @property
    def attribs_parent_prefixed(self):
        return {
            "parent": self.tag,
            "parent_id": self.id,
            "parent_lang": self.lang,
            "parent_article_type": self.article_type,
            "original_article_type": self.original_article_type,
        }

    @property
    def fulltexts(self):
        data = {}
        data["attribs"] = self.attribs
        data["attribs_parent_prefixed"] = self.attribs_parent_prefixed
        data["translations"] = [Fulltext(node) for node in self.translations]
        data["not_translations"] = [Fulltext(node) for node in self.not_translations]
        data["sub_articles"] = [Fulltext(node) for node in self.sub_articles]
        return data


class ArticleAndSubArticles:
    def __init__(self, xmltree):
        self.xmltree = xmltree

    @property
    def main_article_type(self):
        return self.xmltree.find(".").get("article-type")

    @property
    def main_lang(self):
        return self.xmltree.find(".").get("{http://www.w3.org/XML/1998/namespace}lang")

    @property
    def main_line_number(self):
        return self.xmltree.find(".").sourceline

    @property
    def specific_use(self):
        return self.xmltree.find(".").get("specific-use")

    @property
    def dtd_version(self):
        return self.xmltree.find(".").get("dtd-version")

    @property
    def doi(self):
        elem = self.xmltree.find('.//article-meta/article-id[@pub-id-type="doi"]')
        return elem.text if elem is not None else None

    @property
    def main_subject(self):
        return self.xmltree.findtext(".//subject")

    @property
    def article(self):
        node = self.xmltree.find(".//article-meta")
        if node is not None:
            yield node

    @property
    def sub_articles(self):
        nodes = self.xmltree.xpath(".//sub-article")
        for node in nodes:
            yield node

    @property
    def article_and_sub_articles(self):
        yield from self.article
        yield from self.sub_articles

    @property
    def data(self):
        _data = []
        if self.main_article_type:
            _data.append(
                {
                    "lang": self.main_lang,
                    "article_type": self.main_article_type,
                    "article_id": None,
                    "line_number": self.main_line_number,
                    "subject": self.main_subject,
                    "parent_name": "article",
                    "doi": self.doi
                }
            )

        for sub_article in self.xmltree.xpath(".//sub-article"):
            lang = sub_article.get("{http://www.w3.org/XML/1998/namespace}lang")

            subject = sub_article.find(".//subject")
            doi = sub_article.find('.//article-id[@pub-id-type="doi"]')

            _data.append(
                {
                    "lang": lang,
                    "article_type": sub_article.get("article-type"),
                    "article_id": sub_article.get("id"),
                    "line_number": sub_article.sourceline,
                    "subject": subject.text if subject is not None else None,
                    "parent_name": "sub-article",
                    "doi": doi.text if doi is not None else None
                }
            )
        return _data
