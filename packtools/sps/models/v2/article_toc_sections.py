from packtools.sps.models.article_and_subarticles import Fulltext
from packtools.sps.utils.xml_utils import node_text_without_fn_xref


class ArticleTocSections:

    def __init__(self, xmltree):
        self.xmltree = xmltree

    @property
    def sections(self):
        for node in self.xmltree.xpath(
            ". | ./sub-article[@article-type='translation']"
        ):
            fulltext = Fulltext(node)
            parent_data = fulltext.attribs_parent_prefixed
            journal = None
            try:
                subj_groups = fulltext.front.xpath(".//subj-group")
                journal = fulltext.front.findtext(".//journal-title")
            except AttributeError:
                yield parent_data
            else:
                common_data = {}
                common_data.update(parent_data)
                common_data["journal"] = journal
                common_data["article_title"] = node_text_without_fn_xref(fulltext.front.find(".//article-title"))
                for subj_group in subj_groups:
                    _section = {}
                    _section.update(common_data)
                    _section.update(
                        self.get_data(
                            subj_group.find("./subject"), subj_group.get("subj-group-type")
                        )
                    )
                    subsections = []
                    for subsection in subj_group.xpath("./subj-group//subject"):
                        subsections.append(node_text_without_fn_xref(subsection) or None)
                    _section["subsections"] = subsections                
                    yield _section
                if not subj_groups:
                    common_data["section"] = None
                    common_data["subject"] = None
                    common_data["subj_group_type"] = None
                    common_data["subsec"] = None
                    common_data["subsections"] = None
                    yield common_data

    @property
    def sections_dict(self):
        return self.sections_by_lang

    @property
    def sections_by_lang(self):
        response = {}
        for item in self.sections:
            response.setdefault(item["parent_lang"], [])
            response[item["parent_lang"]].append(item)
        return response

    def get_data(self, subject_node, subject_group_type):
        subject = node_text_without_fn_xref(subject_node) or ""
        subject_parts = subject.split(":")
        section = subject_parts[0]
        data = {
            "subject": subject,
            "subj_group_type": subject_group_type,
            "section": section,
        }
        if len(subject_parts) == 2:
            data["subsec"] = subject_parts[-1]
        return data
