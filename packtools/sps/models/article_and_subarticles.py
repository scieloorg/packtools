class ArticleAndSubArticles:
    def __init__(self, xmltree):
        self.xmltree = xmltree

    @property
    def main_article_type(self):
        return self.xmltree.find(".").get("article-type")

    @property
    def main_lang(self):
        return self.xmltree.find(".").get("{http://www.w3.org/XML/1998/namespace}lang")

