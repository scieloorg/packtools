from packtools.sps.utils.xml_utils import get_parent_context, put_parent_context, node_text_without_fn_xref


class ArticleTocSections:

    def __init__(self, xmltree):
        self.xmltree = xmltree

    @property
    def sections(self):
        for node, lang, article_type, parent, parent_id in get_parent_context(self.xmltree):
            for item in node.xpath(".//subj-group"):
                subject = node_text_without_fn_xref(item.find("./subject")) or None
                subject_parts = subject.split(':')
                section = subject_parts[0]
                _section = {
                    "subject": subject,
                    "subj_group_type": item.get("subj-group-type"),
                    "section": section
                }
                if len(subject_parts) == 2:
                    _section["subsec"] = subject_parts[-1]

                subsections = []
                for subsection in item.xpath("./subj-group//subject"):
                    subsections.append(node_text_without_fn_xref(subsection) or None)
                _section["subsections"] = subsections
                yield put_parent_context(_section, lang, article_type, parent, parent_id)

    @property
    def sections_dict(self):
        response = {}
        for item in self.sections:
            response.setdefault(item["parent_lang"], [])
            response[item["parent_lang"]].append(item)
        return response
