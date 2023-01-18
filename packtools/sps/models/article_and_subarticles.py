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
    def data(self):
        _data = []
        if self.main_article_type:
            _data.append({"lang": self.main_lang, "article_type": self.main_article_type, "line_number": self.main_line_number})

        for sub_article in self.xmltree.xpath(".//sub-article"):
            lang = sub_article.get("{http://www.w3.org/XML/1998/namespace}lang")
            article_type = sub_article.get('article-type')
            _data.append({"lang": lang, "article_type": article_type, "line_number": sub_article.sourceline})
        return _data
