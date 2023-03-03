from packtools.sps.utils import xml_utils

from lxml import etree


class ArticleTitles:

    def __init__(self, xmltree):
        self.xmltree = xmltree

    @property
    def data(self):
        return (
            [self.article_title] +
            self.trans_titles +
            self.sub_article_titles
        )

    @property
    def article_title_list(self):
        return (
                [self.article_title] +
                self.trans_titles +
                self.sub_article_titles
        )

    @property
    def article_title_dict(self):
        return {
            item['lang']: item['text']
            for item in self.article_title_list
        }

    @property
    def article_title(self):
        for node_with_lang in xml_utils.get_nodes_with_lang(
                self.xmltree,
                ".", ".//article-meta//article-title"):
            return {
                "lang": node_with_lang["lang"],
                "text": xml_utils.node_text_without_xref(node_with_lang["node"]),
            }

    @property
    def trans_titles(self):
        _titles = []
        nodes = xml_utils.get_nodes_with_lang(
                self.xmltree,
                ".//article-meta//trans-title-group", "trans-title")
        for node_with_lang in xml_utils.get_nodes_with_lang(
                self.xmltree,
                ".//article-meta//trans-title-group", "trans-title"):
            _title = {
                "lang": node_with_lang["lang"],
                "text": xml_utils.node_text_without_xref(node_with_lang["node"]),
            }
            _titles.append(_title)
        return _titles

    @property
    def sub_article_titles(self):
        _titles = []
        for node_with_lang in xml_utils.get_nodes_with_lang(
                self.xmltree,
                ".//sub-article[@article-type='translation']",
                ".//front-stub//article-title"):
            _title = {
                "lang": node_with_lang["lang"],
                "text": xml_utils.node_text_without_xref(node_with_lang["node"]),
            }
            _titles.append(_title)
        return _titles
