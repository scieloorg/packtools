from packtools.sps.utils.xml_utils import get_parent_context, put_parent_context, node_text_without_xref


class ArticleTocSections:

    def __init__(self, xmltree):
        self.xmltree = xmltree

    @property
    def sections(self):
        for node, lang, article_type, parent, parent_id in get_parent_context(
                self.xmltree
        ):
            for item in node.xpath(".//subj-group[@subj-group-type='heading']/subject"):
                _section = {
                    "text": node_text_without_xref(item),
                }
                yield put_parent_context(_section, lang, article_type, parent, parent_id)

    @property
    def sections_dict(self):
        return {
            item['parent_lang']: item
            for item in self.sections
        }
