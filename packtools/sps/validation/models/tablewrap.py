from packtools.sps.models.tablewrap import TableWrappers


class ArticleTableWrappers:
    def __init__(self, xml_tree):
        self.xml_tree = xml_tree

    @property
    def get_all_table_wrappers(self):
        yield from self.get_article_table_wrappers
        yield from self.get_sub_article_translation_table_wrappers
        yield from self.get_sub_article_non_translation_table_wrappers

    @property
    def get_article_table_wrappers(self):
        yield from TableWrappers(self.xml_tree.find(".")).table_wrappers()

    @property
    def get_sub_article_translation_table_wrappers(self):
        for node in self.xml_tree.xpath(".//sub-article[@article-type='translation']"):
            yield from TableWrappers(node).table_wrappers()

    @property
    def get_sub_article_non_translation_table_wrappers(self):
        for node in self.xml_tree.xpath(".//sub-article[@article-type!='translation']"):
            yield from TableWrappers(node).table_wrappers()
