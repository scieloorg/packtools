from packtools.sps.models.article_and_subarticles import Fulltext
from packtools.sps.models.dates import FulltextDates
from packtools.sps.utils.xml_utils import tostring, get_parent_context, put_parent_context, node_plain_text, process_subtags


class Reference:
    def __init__(self, ref):
        self.ref = ref

    def get_label(self):
        return node_plain_text(self.ref.find("./label"))

    def get_publication_type(self):
        return self.ref.find("./element-citation").get("publication-type")

    def get_source(self):
        return node_plain_text(self.ref.find("./element-citation/source"))

    def get_main_author(self):
        try:
            return self.get_all_authors()[0]
        except IndexError:
            return

    def get_all_authors(self):
        tags = ["surname", "given-names", "prefix", "suffix"]
        result = []
        authors = self.ref.xpath("./element-citation/person-group//name")
        for author in authors:
            d = {}
            for tag in tags:
                if text := node_plain_text(author.find(tag)):
                    d[tag] = text
            result.append(d)
        if collab := self.get_collab():
            result.append({"collab": collab})

        return result

    def get_collab(self):
        return [node_plain_text(collab) for collab in self.ref.xpath("./element-citation/person-group//collab")]

    def get_volume(self):
        return node_plain_text(self.ref.find("./element-citation/volume"))

    def get_issue(self):
        return node_plain_text(self.ref.find("./element-citation/issue"))

    def get_fpage(self):
        return node_plain_text(self.ref.find("./element-citation/fpage"))

    def get_lpage(self):
        return node_plain_text(self.ref.find("./element-citation/lpage"))

    def get_year(self):
        return node_plain_text(self.ref.find("./element-citation/year"))

    def get_article_title(self):
        return node_plain_text(self.ref.find("./element-citation/article-title"))

    def get_mixed_citation(self):
        return node_plain_text(self.ref.find("./mixed-citation"))

    def get_mixed_citation_sub_tags(self):
        element = self.ref.find("./mixed-citation")
        if element is not None:
            return [child.tag for child in element]

    def get_citation_ids(self):
        ids = {}
        for pub_id in self.ref.xpath(".//pub-id"):
            ids[pub_id.attrib["pub-id-type"]] = node_plain_text(pub_id)
        return ids

    def get_elocation_id(self):
        return node_plain_text(self.ref.find("./element-citation/elocation-id"))

    def get_ref_id(self):
        return self.ref.get("id")

    def get_extlink_and_comment_content(self):
        ext_link = self.ref.find("./element-citation//ext-link")
        if ext_link is not None:
            comment = self.ref.find("./element-citation/comment")
            full_comment = None
            text_between = None
            if comment is not None:
                text_between = (comment.text or "").strip()
                full_comment = process_subtags(comment) or None
            return {
                'full_comment': full_comment,
                'has_comment': comment is not None,
                'text_between': text_between,
                'ext_link_text': process_subtags(ext_link),
                'text_before': self.get_text_before_extlink()
            }

    def get_text_before_extlink(self):
        extlink_node = self.ref.find("./element-citation/ext-link")
        if extlink_node is not None:
            previous = extlink_node.getprevious()
            if previous is not None:
                return previous.tail

    def get_chapter_title(self):
        return node_plain_text(self.ref.find("./element-citation/chapter-title"))

    def get_part_title(self):
        return node_plain_text(self.ref.find("./element-citation/part-title"))

    def data(self):
        tags = [
            ("ref_id", self.get_ref_id()),
            ("label", self.get_label()),
            ("publication_type", self.get_publication_type()),
            ("source", self.get_source()),
            ("main_author", self.get_main_author()),
            ("all_authors", self.get_all_authors()),
            ("volume", self.get_volume()),
            ("issue", self.get_issue()),
            ("fpage", self.get_fpage()),
            ("lpage", self.get_lpage()),
            ("elocation_id", self.get_elocation_id()),
            ("year", self.get_year()),
            ("article_title", self.get_article_title()),
            ("citation_ids", self.get_citation_ids()),
            ("mixed_citation", self.get_mixed_citation()),
            ("mixed_citation_sub_tags", self.get_mixed_citation_sub_tags()),
            ("comment_text", self.get_extlink_and_comment_content()),
            ("text_before_extlink", self.get_text_before_extlink()),
            ("chapter_title", self.get_chapter_title()),
            ("part_title", self.get_part_title())
        ]
        d = dict()
        for name, value in tags:
            if value is not None and len(value) > 0:
                try:
                    d[name] = value.text
                except AttributeError:
                    d[name] = value
        d["author_type"] = "institutional" if self.get_collab() else "person"

        return d


def get_ext_link(node):
    return [node_plain_text(item) for item in node.xpath(".//element-citation//ext-link")]


class FullTextReferences(Fulltext):

    def __init__(self, node, citing_pub_year=None):
        super().__init__(node)
        self._citing_pub_year = citing_pub_year

    @property
    def citing_pub_year(self):
        if not self._citing_pub_year:
            fulltext = FulltextDates(self.node)
            self._citing_pub_year = (
                fulltext.collection_date or fulltext.article_date
            ).get("year")
        return self._citing_pub_year

    @property
    def common_data(self):
        common = {}
        common.update(self.attribs_parent_prefixed)
        common["citing_pub_year"] = self.citing_pub_year
        return common

    @property
    def main_references(self):
        try:
            refs = self.back.xpath("ref-list/ref")
        except AttributeError:
            return

        if not refs:
            return

        for item in refs:
            ref = Reference(item)
            data = ref.data()
            data.update(self.common_data)
            yield data

    @property
    def subarticle_references(self):
        d = {}
        for node in self.node.xpath("sub-article[@article-type!='translation']"):
            if node.find("back/ref-list") is not None:
                fulltext = FullTextReferences(node, self.citing_pub_year)
                d[fulltext.id] = fulltext.data
        return d

    @property
    def data(self):
        d = {}
        if refs := list(self.main_references):
            d["main_references"] = refs
            d.update(self.subarticle_references)
        return d

    @property
    def items(self):
        yield from self.main_references
        for id_, refs in self.subarticle_references.items():
            yield from refs


class XMLReferences:

    def __init__(self, xmltree):
        self.xmltree = xmltree
        self.fulltext = FullTextReferences(self.xmltree.find("."))

    @property
    def main_references(self):
        yield from self.fulltext.main_references

    @property
    def subarticle_references(self):
        return self.fulltext.subarticle_references

    @property
    def items(self):
        yield from self.main_references
        for refs in self.subarticle_references.values():
            yield from refs
