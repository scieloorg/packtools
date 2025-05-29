class ArticleRenditions:
    def __init__(self, xmltree):
        self.xmltree = xmltree

    @property
    def article_renditions(self):
        _renditions = []

        main_rendition = Rendition(
            self.xmltree.find("."),
            True,
        )
        _renditions.append(main_rendition)

        for sub_article in self.xmltree.xpath(
            ".//sub-article[@article-type='translation']"
        ):
            _renditions.append(Rendition(sub_article))

        return _renditions


class Rendition:
    def __init__(self, node, is_main_language=False):
        self.node = node
        self.is_main_language = is_main_language

    @property
    def language(self):
        return self.node.get("{http://www.w3.org/XML/1998/namespace}lang")
