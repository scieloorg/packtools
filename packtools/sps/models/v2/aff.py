from packtools.sps.models.article_and_subarticles import Fulltext
from packtools.sps.utils.xml_utils import tostring


class Affiliation:
    def __init__(self, aff_node, parent_data):
        self.aff_node = aff_node
        self.parent_data = parent_data

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
        data = {
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
        data.update(self.parent_data)
        return data

    def _get_institution_info(self, inst_type):
        return self.aff_node.findtext(
            f'institution[@content-type="{inst_type}"]'
        )

    def _get_loc_type_info(self, loc_type):
        location = self.aff_node.findtext(f"addr-line/{loc_type}")
        if not location:
            location = self.aff_node.findtext(
                f'addr-line/named-content[@content-type="{loc_type}"]'
            )
        return location


class FulltextAffiliations(Fulltext):

    def affiliations(self):
        return [item.data for item in self.main_affs]

    @property
    def main_affs(self):
        try:
            for aff_node in self.front.xpath(".//aff"):
                yield Affiliation(aff_node, self.attribs_parent_prefixed)
        except AttributeError:
            pass

    @property
    def translations(self):
        for node in super().translations:
            yield FulltextAffiliations(node)

    @property
    def not_translations(self):
        for node in super().not_translations:
            yield FulltextAffiliations(node)

    @property
    def sub_articles(self):
        for node in super().sub_articles:
            yield FulltextAffiliations(node)

    @property
    def items(self):
        yield from self.affiliations()
        for fulltext in self.sub_articles:
            yield from fulltext.items

    @property
    def data(self):
        data = {}
        data["main"] = self.affiliations()
        if self.translations_data_by_lang:
            data["translations"] = self.translations_data_by_lang
        if self.not_translations_data_by_id:
            data["not_translations"] = self.not_translations_data_by_id
        return data

    @property
    def translations_data_by_lang(self):
        data = {}
        for item in self.translations:
            data[item.lang] = item.affiliations()
        return data

    @property
    def not_translations_data_by_id(self):
        data = {}
        for item in self.not_translations:
            data[item.id] = item.data
        return data


class XMLAffiliations:
    def __init__(self, xml_tree):
        self.xml_tree = xml_tree
        self.fulltext_affs = FulltextAffiliations(self.xml_tree.find("."))

    @property
    def article_affs(self):
        return self.fulltext_affs.affiliations()

    @property
    def data(self):
        return self.fulltext_affs.data

    @property
    def items(self):
        return self.fulltext_affs.items

    @property
    def by_ids(self):
        data = {}
        for item in self.fulltext_affs.items:
            data[item["id"]] = item
        return data
