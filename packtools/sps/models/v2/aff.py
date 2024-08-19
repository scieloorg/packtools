import re

from lxml import etree

from packtools.sps.utils.xml_utils import get_parent_context, put_parent_context

class Affiliation:
    def __init__(self, aff_node):
        self.aff_node = aff_node

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
            "city": self.city,
            "country_code": self.country_code,
            "country_name": self.country,
            "email": self.email,
            "id": self.aff_id,
            "label": self.label,
            "orgdiv1": self.orgdiv1,
            "orgdiv2": self.orgdiv2,
            "orgname": self.orgname,
            "original": self.original,
            "state": self.state
        }

    def _get_institution_info(self, inst_type):
        return self.aff_node.findtext(f'institution[@content-type="{inst_type}"]')

    def _get_loc_type_info(self, loc_type):
        location = self.aff_node.findtext(f"addr-line/{loc_type}")
        if not location:
            location = self.aff_node.findtext(f'addr-line/named-content[@content-type="{loc_type}"]')
        return location


class Affiliations:
    def __init__(self, node, lang, article_type, parent, parent_id):
        self.node = node
        self.lang = lang
        self.article_type = article_type
        self.parent = parent
        self.parent_id = parent_id

    def affiliations(self):
        for aff_node in self.node.xpath("./article-meta//aff | ./contrib-group//aff | ./front-stub//aff"):
            data = Affiliation(aff_node).data
            data["node"] = aff_node
            yield put_parent_context(data, self.lang, self.article_type, self.parent, self.parent_id)


class ArticleAffiliations:
    def __init__(self, xml_tree):
        self.xml_tree = xml_tree

    def article_affs(self):
        for aff in self.all_affs():
            if aff.get("parent") == "article":
                yield aff

    def sub_article_translation_affs(self):
        for aff in self.all_affs():
            if aff.get("parent") == "sub-article" and aff.get("parent_article_type") == "translation":
                yield aff

    def sub_article_non_translation_affs(self):
        for aff in self.all_affs():
            if aff.get("parent") == "sub-article" and aff.get("parent_article_type") != "translation":
                yield aff

    def all_affs(self):
        for node, lang, article_type, parent, parent_id in get_parent_context(self.xml_tree):
            for aff in Affiliations(node, lang, article_type, parent, parent_id).affiliations():
                yield aff
