from packtools.sps.utils.xml_utils import get_parent_context, put_parent_context, node_plain_text, process_subtags


class ArticleReference:
    def __init__(self, ref):
        self.ref = ref

    def get_label(self):
        text = node_plain_text(self.ref.find("./label"))
        if text is not None and text.endswith("."):
            text = text[:-1]
        return text

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
        collabs = self.ref.xpath("./element-citation/person-group//collab")
        return [node_plain_text(collab) for collab in collabs]

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

    def get_citation_ids(self):
        ids = {}
        for pub_id in self.ref.xpath(".//pub-id"):
            ids[pub_id.attrib["pub-id-type"]] = node_plain_text(pub_id)
        return ids

    def get_elocation_id(self):
        return node_plain_text(self.ref.find("./element-citation/elocation-id"))

    def get_ref_id(self):
        return self.ref.get("id")



class ArticleCitations:

    def __init__(self, xmltree):
        self.xmltree = xmltree

    @property
    def article_citations(self):
        for node, lang, article_type, parent, parent_id in get_parent_context(
            self.xmltree
        ):
            for item in node.xpath(".//ref-list/ref"):
                ref = ArticleReference(item)
                tags = [
                    ("ref_id", ref.get_ref_id()),
                    ("label", ref.get_label()),
                    ("publication_type", ref.get_publication_type()),
                    ("source", ref.get_source()),
                    ("main_author", ref.get_main_author()),
                    ("all_authors", ref.get_all_authors()),
                    ("volume", ref.get_volume()),
                    ("issue", ref.get_issue()),
                    ("fpage", ref.get_fpage()),
                    ("lpage", ref.get_lpage()),
                    ("elocation_id", ref.get_elocation_id()),
                    ("year", ref.get_year()),
                    ("article_title", ref.get_article_title()),
                    ("citation_ids", ref.get_citation_ids()),
                    ("mixed_citation", ref.get_mixed_citation()),
                    ("comment_text", ref.get_extlink_and_comment_content()),
                    ("text_before_extlink", ref.get_text_before_extlink())
                ]
                d = dict()
                for name, value in tags:
                    if value is not None and len(value) > 0:
                        try:
                            d[name] = value.text
                        except AttributeError:
                            d[name] = value
                d["author_type"] = "institutional" if ref.get_collab() else "person"
                yield put_parent_context(d, lang, article_type, parent, parent_id)
