from packtools.sps.models.article_and_subarticles import Fulltext
from packtools.sps.models.dates import FulltextDates
from packtools.sps.utils.xml_utils import node_plain_text


class Reference:
    def __init__(self, ref):
        self.ref = ref
        self.check_marks()

    def check_marks(self):
        self.marked = []
        self.unmatched = []
        mixed_citation = (self.get_mixed_citation() or '').strip()
        label = self.get_label()
        if label and mixed_citation.startswith(label):
            mixed_citation = mixed_citation[len(label):].strip()

        marked = []
        for node in self.ref.xpath('.//element-citation//*'):
            for text in (node.text, node.tail):
                text = (text or '').strip()
                if text:
                    marked.append({"tag": node.tag, "text": text})

        for item in sorted(marked, key=lambda x: len(x["text"]), reverse=True):
            text = item["text"]
            if text in mixed_citation:
                mixed_citation = mixed_citation.replace(text, "<tag/>", 1)
                self.marked.append(item)
            else:
                self.unmatched.append(item)

        self.not_marked = mixed_citation.split("<tag/>")
        self.filtered_not_marked = list(self.exclude_separators(self.not_marked))

    def exclude_separators(self, not_marked):
        for item in not_marked:
            item = item.strip()
            for c in ",.;":
                if not item:
                    break
                if item[-1] == c:
                    item = item[:-1].strip()
                if item and item[0] == c:
                    item = item[1:].strip()
            if item:
                if item.isdigit():
                    yield item
                elif len(item) > 20:
                    yield item

    def get_label(self):
        return node_plain_text(self.ref.find("./label"))

    def get_publication_type(self):
        return self.ref.find("./element-citation").get("publication-type")

    def get_publisher_name(self):
        return node_plain_text(self.ref.find("./element-citation/publisher-name"))

    def get_publisher_loc(self):
        return node_plain_text(self.ref.find("./element-citation/publisher-loc"))

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
        for person_group in self.ref.xpath("./element-citation//person-group"):
            for author in person_group.xpath(".//name"):
                d = {"person_group_type": person_group.get("person-group-type")}
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

    def get_date_in_citation(self):
        return node_plain_text(self.ref.find("./element-citation/date-in-citation"))

    def get_article_title(self):
        return node_plain_text(self.ref.find("./element-citation/article-title"))

    def get_mixed_citation(self):
        return node_plain_text(self.ref.find("./mixed-citation"))

    def get_xlink(self):
        ext_link = self.ref.find(".//ext-link[@ext-link-type='uri']")
        if ext_link is not None:
            return ext_link.get("{http://www.w3.org/1999/xlink}href")
        return None

    def get_mixed_citation_sub_tags(self):
        element = self.ref.find("./mixed-citation")
        if element is not None:
            return [child.tag for child in element]

    def get_citation_ids(self):
        ids = {}
        try:
            for pub_id in self.ref.xpath(".//pub-id"):
                try:
                    pub_id_type = pub_id.attrib.get("pub-id-type")
                    if pub_id_type:
                        text_value = node_plain_text(pub_id)
                        if text_value and text_value.strip():
                            ids[pub_id_type] = text_value.strip()
                except Exception:
                    continue
        except Exception:
            pass
        return ids

    def get_elocation_id(self):
        return node_plain_text(self.ref.find("./element-citation/elocation-id"))

    def get_ref_id(self):
        return self.ref.get("id")

    def get_extlink_and_comment_content(self):
        has_comment = False
        full_comment = None
        text_between = None
        text_before = None

        comment = self.ref.find("./element-citation//comment")
        if comment is not None:
            has_comment = True
            text_between = comment.text
            full_comment = "".join(comment.xpath(".//text()")) or None

        ext_link = self.ref.find("./element-citation//ext-link")
        try:
            href = ext_link.get("{http://www.w3.org/1999/xlink}href")
            ext_link_text = " ".join(ext_link.xpath(".//text()")) or None

            try:
                text_before = ext_link.getprevious().tail
            except AttributeError:
                if not has_comment:
                    text_before = ext_link.getparent().text

        except AttributeError:
            href = None
            ext_link_text = None

        if text_before and not text_before.strip():
            text_before = None
        if text_between and not text_between.strip():
            text_between = None

        return {
            'ext_link_uri': href,
            'full_comment': full_comment,
            'has_comment': has_comment,
            'text_between': text_between,
            'ext_link_text': ext_link_text,
            'text_before_extlink': text_before
        }

    def get_chapter_title(self):
        return node_plain_text(self.ref.find("./element-citation/chapter-title"))

    def get_part_title(self):
        return node_plain_text(self.ref.find("./element-citation/part-title"))

    def get_comment(self):
        el = self.ref.find("./element-citation/comment")
        if el is None:
            return None
        return "".join(el.itertext()).strip()

    def get_degree(self):
        el = self.ref.xpath('./element-citation/comment[@content-type="degree"]')
        if len(el) == 0:
            return None
        return "".join(el[0].itertext()).strip()

    def get_edition(self):
        return node_plain_text(self.ref.find("./element-citation/edition"))

    def get_citation_lang(self):
        citation = self.ref.find("./element-citation")
        if citation is not None:
            return citation.get("{http://www.w3.org/XML/1998/namespace}lang")
        return None

    def get_size_info(self):
        size_el = self.ref.find(".//size")
        if size_el is not None and size_el.text:
            units = size_el.get("units")
            text = size_el.text.strip()
            return {"units": units, "text": text}
        return None

    def get_conf_name(self):
        return node_plain_text(self.ref.find("./element-citation/conf-name"))

    def get_conf_loc(self):
        return node_plain_text(self.ref.find("./element-citation/conf-loc"))

    @property
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
            ("chapter_title", self.get_chapter_title()),
            ("part_title", self.get_part_title()),
            ("xlink", self.get_xlink()),
            ("collab", self.get_collab()),
            ("publisher_name", self.get_publisher_name()),
            ("publisher_loc", self.get_publisher_loc()),
            ("date_in_citation", self.get_date_in_citation()),
            ("comment", self.get_comment()),
            ("edition", self.get_edition()),
            ("lang", self.get_citation_lang()),
            ("size_info", self.get_size_info()),
            ("conf_name", self.get_conf_name()),
            ("conf_loc", self.get_conf_loc()),
            ("degree", self.get_degree()),
        ]
        d = dict()
        for name, value in tags:
            if value is not None:
                if isinstance(value, str):
                    if value.strip():
                        d[name] = value
                else:
                    try:
                        d[name] = value.text
                    except AttributeError:
                        d[name] = value

        d["author_type"] = "institutional" if self.get_collab() else "person"
        d["count_persons"] = len(self.ref.findall(".//person-group"))
        d["has_etal"] = self.ref.find(".//person-group/etal") is not None

        d.update({
            "filtered_not_marked": self.filtered_not_marked,
            "not_marked": self.not_marked,
            "marked": self.marked,
            "unmatched": self.unmatched,
        })
        d.update(self.get_extlink_and_comment_content())
        return d


def get_ext_link(node):
    return [node_plain_text(item) for item in node.xpath(".//element-citation//ext-link")]


class FullTextReferences(Fulltext):

    def __init__(self, node, citing_pub_year=None):
        super().__init__(node)
        self._citing_pub_year = citing_pub_year
        self.fulltext = Fulltext(node)

    @property
    def citing_pub_year(self):
        if not self._citing_pub_year:
            fulltext = FulltextDates(self.node)
            self._citing_pub_year = (
                fulltext.collection_date or fulltext.article_date or {}
            ).get("year")
        return self._citing_pub_year

    @property
    def common_data(self):
        common = {}
        common.update(self.attribs_parent_prefixed)
        common["citing_pub_year"] = self.citing_pub_year
        return common

    def get_references(self, node):
        reflists = node.xpath("./back/ref-list") or []
        for index, reflist in enumerate(reflists):
            for node_ref in reflist.xpath("ref"):
                ref = Reference(node_ref)
                data = {}
                data["ref-list-index"] = index
                data.update(ref.data)
                data.update(self.common_data)
                yield data

    @property
    def main_references(self):
        return self.get_references(self.node.find("."))


class XMLReferences:

    def __init__(self, xmltree):
        self.xmltree = xmltree
        self.fulltext = FullTextReferences(xmltree.find("."))

    @property
    def main_references(self):
        yield from self.fulltext.main_references

    @property
    def subarticle_references(self):
        items = {}
        for node in self.xmltree.xpath(".//sub-article[@article-type!='translation'] | .//response"):
            if node.get("id"):
                k = f'{node.tag} {node.get("id")}'
            else:
                k = f'{node.tag}'
            fulltext = FullTextReferences(node)
            items[k] = fulltext.main_references
        return items

    @property
    def items(self):
        yield from self.main_references
        for refs in self.subarticle_references.values():
            yield from refs
