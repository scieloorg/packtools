from packtools.sps.utils import xml_utils


class ArticleTitles:

    def __init__(
        self,
        xmltree,
        tags_to_keep=None,
        tags_to_keep_with_content=None,
        tags_to_remove_with_content=None,
        tags_to_convert_to_html=None,
    ):
        self.xmltree = xmltree
        self.tags_to_keep = tags_to_keep
        self.tags_to_keep_with_content = tags_to_keep_with_content
        self.tags_to_remove_with_content = tags_to_remove_with_content
        self.tags_to_convert_to_html = tags_to_convert_to_html

    @property
    def data(self):
        return [self.article_title] + self.trans_titles + self.sub_article_titles

    @property
    def article_title_list(self):
        return self.data

    @property
    def article_title_dict(self):
        return {item["lang"]: item["text"] for item in self.article_title_list}

    @property
    def article_title(self):
        for node_with_lang in xml_utils.get_nodes_with_lang(
            self.xmltree, ".", ".//article-meta//article-title"
        ):
            return {
                "parent_name": "article",
                "lang": node_with_lang["lang"],
                "text": xml_utils.node_text_without_xref(node_with_lang["node"]),
                "plain_text": xml_utils.node_plain_text(node_with_lang["node"]),
                "html_text": xml_utils.process_subtags(
                    node_with_lang["node"],
                    tags_to_keep=self.tags_to_keep,
                    tags_to_keep_with_content=self.tags_to_keep_with_content,
                    tags_to_remove_with_content=self.tags_to_remove_with_content,
                    tags_to_convert_to_html=self.tags_to_convert_to_html,
                ),
            }

    @property
    def trans_titles(self):
        _titles = []
        for node_with_lang in xml_utils.get_nodes_with_lang(
            self.xmltree, ".//article-meta//trans-title-group", "trans-title"
        ):
            _title = {
                "parent_name": "article",
                "lang": node_with_lang["lang"],
                "text": xml_utils.node_text_without_xref(node_with_lang["node"]),
                "plain_text": xml_utils.node_plain_text(node_with_lang["node"]),
                "html_text": xml_utils.process_subtags(
                    node_with_lang["node"],
                    tags_to_keep=self.tags_to_keep,
                    tags_to_keep_with_content=self.tags_to_keep_with_content,
                    tags_to_remove_with_content=self.tags_to_remove_with_content,
                    tags_to_convert_to_html=self.tags_to_convert_to_html,
                ),
            }
            _titles.append(_title)
        return _titles

    @property
    def sub_article_titles(self):
        _titles = []
        for node_with_lang in xml_utils.get_nodes_with_lang(
            self.xmltree,
            ".//sub-article[@article-type='translation']",
            ".//front-stub//article-title",
        ):
            _title = {
                "parent_name": "sub-article",
                "lang": node_with_lang["lang"],
                "text": xml_utils.node_text_without_xref(node_with_lang["node"]),
                "plain_text": xml_utils.node_plain_text(node_with_lang["node"]),
                "html_text": xml_utils.process_subtags(
                    node_with_lang["node"],
                    tags_to_keep=self.tags_to_keep,
                    tags_to_keep_with_content=self.tags_to_keep_with_content,
                    tags_to_remove_with_content=self.tags_to_remove_with_content,
                    tags_to_convert_to_html=self.tags_to_convert_to_html,
                ),
                "id": node_with_lang["id"],
            }
            _titles.append(_title)
        return _titles
