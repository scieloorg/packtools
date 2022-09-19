class ArticleAndSubArticles:
    def __init__(self, xmltree):
        self.xmltree = xmltree

    @property
    def main_article_type(self):
        return self.xmltree.find(".").get("article-type")
