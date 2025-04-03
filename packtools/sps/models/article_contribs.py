from packtools.sps.models.article_and_subarticles import Fulltext
from packtools.sps.models.v2.aff import XMLAffiliations
from packtools.sps.utils.xml_utils import node_plain_text

"""
<contrib contrib-type="author">
    <contrib-id contrib-id-type="orcid">0000-0001-8528-2091</contrib-id>
    <contrib-id contrib-id-type="scopus">24771926600</contrib-id>
    <anonymous/>
    <collab>The MARS Group</collab>
    <name>
        <surname>Einstein</surname>
        <given-names>Albert</given-names>
        <prefix>Prof</prefix>
        <suffix>Nieto</suffix>
    </name>
    <xref ref-type="aff" rid="aff1">1</xref>
    <role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>
    <role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>
    <role specific-use="reviewer">Reviewer</role>
</contrib>
"""


class Contrib:
    def __init__(self, node, parent_data=None):
        self.node = node
        self.parent_data = parent_data

    @property
    def contrib_type(self):
        return self.node.get("contrib-type")

    @property
    def contrib_ids(self):
        # os valores de @contrib-id-type podem ser: lattes, orcid, researchid e scopus
        return {
            item.get("contrib-id-type"): item.text
            for item in self.node.xpath(".//contrib-id")
        }

    @property
    def anonymous(self):
        anonymous = self.node.find("anonymous")
        if anonymous is not None:
            return "anonymous"

    @property
    def contrib_name(self):
        name = self.node.find("name")
        if name is not None:
            return {item.tag: item.text for item in name if item.text}

    @property
    def contrib_full_name(self):
        name_parts = ["prefix", "given-names", "surname", "suffix"]
        name = self.contrib_name
        if name is not None:
            return " ".join(
                name.get(part, "") for part in name_parts if name.get(part)
            ).strip()

    @property
    def collab(self):
        return node_plain_text(self.node.find("collab"))

    @property
    def contrib_xref(self):
        for item in self.node.xpath(".//xref"):
            yield {
                "rid": item.get("rid"),
                "ref_type": item.get("ref-type"),
                "text": item.text,
            }

    @property
    def contrib_role(self):
        for item in self.node.xpath(".//role"):
            yield {
                "text": item.text,
                "content-type": item.get("content-type"),
                "specific-use": item.get("specific-use"),
            }

    @property
    def data(self):
        data = {}
        for key, value in zip(
            (
                "contrib_type",
                "contrib_ids",
                "anonymous",
                "contrib_name",
                "contrib_full_name",
                "collab",
                "contrib_xref",
                "contrib_role",
            ),
            (
                self.contrib_type,
                self.contrib_ids,
                self.anonymous,
                self.contrib_name,
                self.contrib_full_name,
                self.collab,
                list(self.contrib_xref),
                list(self.contrib_role),
            ),
        ):
            if value:
                data[key] = value
        if self.parent_data:
            data.update(self.parent_data)
        return data


class ContribGroup:
    def __init__(self, node):
        self.node = node

    @property
    def type(self):
        return self.node.get("content-type")

    @property
    def contribs(self):
        for contribs in self.node.xpath(".//contrib"):
            yield Contrib(contribs)

    @property
    def data(self):
        return {
            "type": self.type,
            "contribs": list([item.data for item in self.contribs]),
            "has_collab": self.node.find(".//collab") is not None,
            "has_name": self.node.find(".//name") is not None
        }


class XMLContribs:
    def __init__(self, xmltree):
        self.xmltree = xmltree
        self.aff = XMLAffiliations(xmltree).by_ids
        self.text_contribs = TextContribs(self.xmltree.find("."))

    @property
    def contribs(self):
        # main contribs
        if self.aff:
            for item in self.text_contribs.main_contribs:
                yield self._add_affs(item)
        else:
            yield from self.text_contribs.main_contribs

    @property
    def all_contribs(self):
        if self.aff:
            for item in self.text_contribs.items:
                yield self._add_affs(item)
        else:
            yield from self.text_contribs.items

    @property
    def translations_contrib(self):
        for contrib in self.all_contribs:
            if contrib.get("contrib_type") == "translator":
                yield contrib

    def _add_affs(self, contrib):
        if self.aff and contrib and (xrefs := contrib.get("contrib_xref")):
            affs = []
            for xref in xrefs:
                if aff := self.aff.get(xref.get("rid")):
                    affs.append(aff)
            if affs:
                contrib["affs"] = affs
        return contrib

    @property
    def contrib_full_name_by_orcid(self):
        orcid_dict = {}
        for contrib in self.all_contribs:
            if orcid := contrib.get("contrib_ids", {}).get("orcid"):
                orcid_dict.setdefault(orcid, set())
                orcid_dict[orcid].add(contrib.get("contrib_full_name"))
        return orcid_dict


class TextContribs(Fulltext):

    @property
    def collab(self):
        return self.front.findtext(".//contrib-group//collab")

    @property
    def contrib_groups(self):
        for contrib_group in self.front.xpath(".//contrib-group"):
            yield ContribGroup(contrib_group)

    @property
    def data(self):
        data = {"parent": self.attribs_parent_prefixed}
        data["contrib-groups"] = []
        for group in self.contrib_groups:
            data["contrib-groups"].append(group.data)
        return data

    @property
    def main_contribs(self):
        for group in self.contrib_groups:
            for item in group.contribs:
                data = {}
                data["contrib-group-type"] = group.type
                data.update(self.attribs_parent_prefixed)
                data.update(item.data)
                yield data

    @property
    def items(self):
        yield from self.main_contribs
        for node in self.sub_articles:
            fulltext = TextContribs(node)
            yield from fulltext.items


class ArticleContribs(XMLContribs):
    ...
