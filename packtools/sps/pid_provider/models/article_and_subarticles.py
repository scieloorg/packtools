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
    def main_specific_use(self):
        return self.xmltree.find(".").get("specific-use")

    @property
    def main_dtd_version(self):
        return self.xmltree.find(".").get("dtd-version")

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
                }
            )

        for sub_article in self.xmltree.xpath(".//sub-article"):
            lang = sub_article.get("{http://www.w3.org/XML/1998/namespace}lang")

            subject = sub_article.find(".//subject")

            _data.append(
                {
                    "lang": lang,
                    "article_type": sub_article.get("article-type"),
                    "article_id": sub_article.get("id"),
                    "line_number": sub_article.sourceline,
                    "subject": subject.text if subject is not None else None,
                }
            )
        return _data
