from packtools.sps.utils.xml_utils import get_parent_context, put_parent_context, node_plain_text, process_subtags


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
                text_between = comment.text
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


class FullTextReferences:

    def __init__(self, fulltext_node):
        """
        fulltext_node : article or sub-article node
        """
        self.fulltext_node = fulltext_node

    @property
    def items(self):
        for node, lang, article_type, parent, parent_id in get_parent_context(
                self.fulltext_node
        ):
            for item in node.xpath("ref-list/ref"):
                ref = Reference(item)
                data = ref.data()
                yield put_parent_context(data, lang, article_type, parent, parent_id)


class ArticleReferences:

    def __init__(self, xmltree):
        self.xmltree = xmltree

    @property
    def article_references(self):
        yield from FullTextReferences(self.xmltree.find(".")).items

    @property
    def sub_article_references(self):
        for node in self.xmltree.xpath(".//sub-article"):
            yield from FullTextReferences(node).items