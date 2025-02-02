from packtools.sps.utils.xml_utils import put_parent_context, tostring


class Affiliation:
    def __init__(self, aff_node):
        self.aff_node = aff_node

    @property
    def str_main_tag(self):
        return f'<aff id="{self.aff_id}">'

    def __str__(self):
        return tostring(self.aff_node, xml_declaration=False)

    def xml(self, pretty_print=True):
        return tostring(
            node=self.aff_node,
            doctype=None,
            pretty_print=pretty_print,
            xml_declaration=False,
        )

    @property
    def aff_id(self):
        return self.aff_node.get("id")

    @property
    def label(self):
        return self.aff_node.findtext("label")

    @property
    def orgname(self):
        return self._get_institution_info("orgname")

    @property
    def orgdiv1(self):
        return self._get_institution_info("orgdiv1")

    @property
    def orgdiv2(self):
        return self._get_institution_info("orgdiv2")

    @property
    def original(self):
        return self._get_institution_info("original")

    @property
    def country(self):
        return self.aff_node.findtext("country")

    @property
    def country_code(self):
        try:
            return self.aff_node.find("country").get("country")
        except AttributeError:
            return None

    @property
    def state(self):
        return self._get_loc_type_info("state")

    @property
    def city(self):
        return self._get_loc_type_info("city")

    @property
    def email(self):
        return self.aff_node.findtext("email")

    @property
    def data(self):
        return {
            "id": self.aff_id,
            "label": self.label,
            "original": self.original,
            "orgname": self.orgname,
            "orgdiv1": self.orgdiv1,
            "orgdiv2": self.orgdiv2,
            "country_name": self.country,
            "country_code": self.country_code,
            "state": self.state,
            "city": self.city,
            "email": self.email,
        }

    def _get_institution_info(self, inst_type):
        return self.aff_node.findtext(f'institution[@content-type="{inst_type}"]')

    def _get_loc_type_info(self, loc_type):
        location = self.aff_node.findtext(f"addr-line/{loc_type}")
        if not location:
            location = self.aff_node.findtext(
                f'addr-line/named-content[@content-type="{loc_type}"]'
            )
        return location


class Affiliations:
    def __init__(self, node):
        """
        Initializes the Affiliations class with an XML node.

        Parameters:
        node : lxml.etree._Element
            The XML node (element) that contains one or more <aff> elements.
            This can be the root of an `xml_tree` or a node representing a `sub-article`.
        """
        self.node = node
        self.parent = self.node.tag
        self.parent_id = self.node.get("id")
        self.lang = self.node.get("{http://www.w3.org/XML/1998/namespace}lang")
        self.article_type = self.node.get("article-type")

    def affiliations(self):
        if self.parent == "article":
            path = "./front/article-meta//aff"
        else:
            path = "./contrib-group//aff | ./front-stub//aff"

        for aff_node in self.node.xpath(path):
            data = Affiliation(aff_node).data

            yield put_parent_context(
                data, self.lang, self.article_type, self.parent, self.parent_id
            )


class ArticleAffiliations:
    def __init__(self, xml_tree):
        self.xml_tree = xml_tree

    def article_affs(self):
        yield from Affiliations(self.xml_tree.find(".")).affiliations()

    def sub_article_translation_affs(self):
        for node in self.xml_tree.xpath(".//sub-article[@article-type='translation']"):
            yield from Affiliations(node).affiliations()

    def sub_article_translation_affs_by_lang(self):
        langs = {}
        for node in self.xml_tree.xpath(".//sub-article[@article-type='translation']"):
            langs[node.get("{http://www.w3.org/XML/1998/namespace}lang")] = list(
                Affiliations(node).affiliations()
            )
        return langs

    def sub_article_non_translation_affs(self):
        for node in self.xml_tree.xpath(".//sub-article[@article-type!='translation']"):
            yield from Affiliations(node).affiliations()

    def all_affs(self):
        yield from self.article_affs()
        yield from self.sub_article_translation_affs()
        yield from self.sub_article_non_translation_affs()
