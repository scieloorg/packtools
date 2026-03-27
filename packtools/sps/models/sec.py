from packtools.sps.models.article_and_subarticles import Fulltext


VALID_SEC_TYPES = [
    "cases",
    "conclusions",
    "data-availability",
    "discussion",
    "intro",
    "materials",
    "methods",
    "results",
    "subjects",
    "supplementary-material",
    "transcript",
]

NON_COMBINABLE_SEC_TYPES = [
    "data-availability",
    "supplementary-material",
    "transcript",
]


class Sec:
    """Represents a single <sec> element."""

    def __init__(self, element, parent_attribs=None):
        self.element = element
        self._parent_attribs = parent_attribs or {}

    @property
    def sec_id(self):
        return self.element.get("id")

    @property
    def sec_type(self):
        return self.element.get("sec-type")

    @property
    def specific_use(self):
        return self.element.get("specific-use")

    @property
    def title(self):
        title_elem = self.element.find("title")
        if title_elem is not None:
            return title_elem.text or ""
        return None

    @property
    def paragraphs(self):
        return self.element.findall("p")

    @property
    def is_first_level(self):
        parent = self.element.getparent()
        if parent is not None:
            return parent.tag in ("body", "back", "abstract", "trans-abstract",
                                  "app", "bio", "boxed-text")
        return True

    @property
    def data(self):
        d = {
            "sec_id": self.sec_id,
            "sec_type": self.sec_type,
            "specific_use": self.specific_use,
            "title": self.title,
            "has_title": self.title is not None,
            "paragraph_count": len(self.paragraphs),
            "is_first_level": self.is_first_level,
        }
        d.update(self._parent_attribs)
        return d


class ArticleSecs:
    """Extracts all <sec> elements from an article and sub-articles."""

    def __init__(self, xmltree):
        self.xmltree = xmltree

    @property
    def main_article_type(self):
        return self.xmltree.find(".").get("article-type")

    def _get_secs_from_node(self, node, parent_attribs):
        for sec_elem in node.xpath(".//sec"):
            yield Sec(sec_elem, parent_attribs).data

    @property
    def all_secs(self):
        for node in self.xmltree.xpath(
            ". | ./sub-article[@article-type='translation']"
        ):
            fulltext = Fulltext(node)
            parent_attribs = fulltext.attribs_parent_prefixed
            yield from self._get_secs_from_node(fulltext.node, parent_attribs)

    @property
    def first_level_body_secs(self):
        """Get only first-level <sec> elements inside <body>."""
        for node in self.xmltree.xpath(
            ". | ./sub-article[@article-type='translation']"
        ):
            fulltext = Fulltext(node)
            parent_attribs = fulltext.attribs_parent_prefixed
            body = fulltext.body
            if body is not None:
                for sec_elem in body.findall("sec"):
                    yield Sec(sec_elem, parent_attribs).data

    @property
    def body_sec_types(self):
        """Get all sec-type values from first-level body secs."""
        return [
            sec["sec_type"]
            for sec in self.first_level_body_secs
            if sec.get("sec_type")
        ]
