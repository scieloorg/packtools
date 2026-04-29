from packtools.sps.models.fig import Figs


class ArticleFigs:
    def __init__(self, xml_tree):
        self.xml_tree = xml_tree

    @property
    def get_all_figs(self):
        yield from self.get_article_figs
        yield from self.get_sub_article_translation_figs
        yield from self.get_sub_article_non_translation_figs

    @property
    def get_article_figs(self):
        yield from Figs(self.xml_tree.find(".")).figs()

    @property
    def get_sub_article_translation_figs(self):
        for node in self.xml_tree.xpath(".//sub-article[@article-type='translation']"):
            yield from Figs(node).figs()

    @property
    def get_sub_article_non_translation_figs(self):
        for node in self.xml_tree.xpath(".//sub-article[@article-type!='translation']"):
            yield from Figs(node).figs()
