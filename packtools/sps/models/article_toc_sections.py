from packtools.sps.utils import xml_utils


class ArticleTocSections:

    def __init__(self, xmltree):
        self.xmltree = xmltree

    @property
    def article_section(self):
        _sections = []
        for node_with_lang in xml_utils.get_nodes_with_lang(
                self.xmltree,
                ".",
                ".//article-meta//subj-group[@subj-group-type='heading']/subject"
        ):
            _section = {
                "lang": node_with_lang["lang"],
                "text": xml_utils.node_text_without_fn_xref(node_with_lang["node"]),
            }
            _sections.append(_section)
        return _sections

    @property
    def article_section_dict(self):
        return {
            item['lang']: item['text']
            for item in self.article_section
        }

    @property
    def sub_article_section(self):
        _sections = []
        for node_with_lang in xml_utils.get_nodes_with_lang(
                self.xmltree,
                ".//sub-article[@article-type='translation']",
                ".//front-stub//subj-group[@subj-group-type='heading']/subject"
        ):

            _section = {
                "id": node_with_lang["id"],
                "lang": node_with_lang["lang"],
                "text": xml_utils.node_text_without_fn_xref(node_with_lang["node"]),
            }
            _sections.append(_section)
        return _sections

    @property
    def sub_article_section_dict(self):
        return {
            item['lang']: item['text']
            for item in self.sub_article_section
        }

    @property
    def all_section_dict(self):
        d = self.article_section_dict
        d.update(self.sub_article_section_dict)
        return d

    @property
    def sub_section(self):
        _sub_sections = []
        for node_with_lang in xml_utils.get_nodes_with_lang(
                self.xmltree,
                ".", ".//article-meta//subj-group[@subj-group-type='heading']/subj-group/subject"):
            _sub_section = {
                "lang": node_with_lang["lang"],
                "text": xml_utils.node_text_without_fn_xref(node_with_lang["node"]),
            }
            _sub_sections.append(_sub_section)
        return _sub_sections

    @property
    def sub_section_dict(self):
        return {
            item['lang']: item['text']
            for item in self.sub_section
        }
