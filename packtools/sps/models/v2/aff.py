import re

from lxml import etree


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
        return self._clean_string(
           self.aff_node.findtext(f'institution[@content-type="{inst_type}"]')
        )

    def _get_loc_type_info(self, loc_type):
        location = self.aff_node.findtext(f"addr-line/{loc_type}")
        if not location:
            location = self.aff_node.findtext(f'addr-line/named-content[@content-type="{loc_type}"]')
        return location

    def _clean_string(self, text):
        if text:
            text_without_whitespace = re.sub(r'[\n\t\r]+', ' ', text)
            final_text = re.sub(r'\s+', ' ', text_without_whitespace).strip()
            return final_text


class Affiliations:
    def __init__(self, node):
        self.node = node

    def affiliations(self):
        for aff_node in self.node.xpath("./article-meta/aff | ./contrib-group/aff | ./front-stub/aff"):
            yield Affiliation(aff_node)


class ArticleAffiliations:
    def __init__(self, xml_tree):
        self.xml_tree = xml_tree

    def _get_affiliation_data(self, node, article_type, lang, parent="article", parent_id=None):
        for aff in Affiliations(node).affiliations():
            data = aff.data
            data["parent"] = parent
            data["parent_id"] = parent_id
            data["parent_article_type"] = article_type
            data["parent_lang"] = lang
            yield data

    def article_affs(self):
        main = self.xml_tree.xpath(".")[0]
        lang = main.get("{http://www.w3.org/XML/1998/namespace}lang")
        article_type = main.get("article-type")
        for node in self.xml_tree.xpath("./front | ./body | ./back"):
            yield from self._get_affiliation_data(node, article_type, lang)

    def sub_article_translation_affs(self):
        for node in self.xml_tree.xpath("./sub-article[@article-type='translation']"):
            lang = node.get("{http://www.w3.org/XML/1998/namespace}lang")
            yield from self._get_affiliation_data(node, "translation", lang, parent="sub-article", parent_id=node.get("id"))

    def sub_article_non_translation_affs(self):
        for node in self.xml_tree.xpath("./sub-article[@article-type!='translation']"):
            article_type = node.get("article-type")
            lang = node.get("{http://www.w3.org/XML/1998/namespace}lang")
            yield from self._get_affiliation_data(node, article_type, lang, parent="sub-article", parent_id=node.get("id"))

    def all_affs(self):
        yield from self.article_affs()
        yield from self.sub_article_translation_affs()
        yield from self.sub_article_non_translation_affs()
