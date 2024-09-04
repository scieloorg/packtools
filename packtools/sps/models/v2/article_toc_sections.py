from packtools.sps.utils.xml_utils import get_parent_context, put_parent_context, node_text_without_xref


class ArticleTocSections:

    def __init__(self, xmltree):
        self.xmltree = xmltree

    @property
    def sections(self):
        for node, lang, article_type, parent, parent_id in get_parent_context(self.xmltree):
            for item in node.xpath(".//subj-group"):
                _section = {
                    "subj_group_type": item.get("subj-group-type"),
                    "section": node_text_without_xref(section := item.find("./subject"))
                }
                subsections = []
                for subsection in item.xpath(".//subject"):
                    if subsection is not None and subsection != section:
                        subsections.append(node_text_without_xref(subsection))
                _section["subsections"] = subsections
                yield put_parent_context(_section, lang, article_type, parent, parent_id)

    @property
    def sections_dict(self):
        response = {}
        for item in self.sections:
            response.setdefault(item["parent_lang"], [])
            response[item["parent_lang"]].append(item)
        return response
