from packtools.sps.models.aff import Affiliation
from packtools.sps.utils.xml_utils import node_plain_text

"""
<contrib contrib-type="author">
    <contrib-id contrib-id-type="orcid">0000-0001-8528-2091</contrib-id>
    <contrib-id contrib-id-type="scopus">24771926600</contrib-id>
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
    def __init__(self, node):
        self.node = node

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
    def contrib_name(self):
        name = self.node.find("name")
        if name is not None:
            return {item.tag: item.text for item in name}

    @property
    def contrib_full_name(self):
        name_parts = ['prefix', 'given-names', 'surname', 'suffix']
        name = self.contrib_name
        if name is not None:
            return ' '.join(name.get(part, '') for part in name_parts).strip()

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
                "contrib_name",
                "contrib_full_name",
                "collab",
                "contrib_xref",
                "contrib_role",
            ),
            (
                self.contrib_type,
                self.contrib_ids,
                self.contrib_name,
                self.contrib_full_name,
                self.collab,
                list(self.contrib_xref),
                list(self.contrib_role),
            ),
        ):
            if value:
                data[key] = value
        return data


class ContribGroup:
    def __init__(self, node):
        self.node = node

    @property
    def contribs(self):
        for contribs in self.node.xpath(".//contrib"):
            contrib = Contrib(contribs)
            yield contrib.data


class ArticleContribs:
    def __init__(self, xmltree):
        self.xmltree = xmltree
        self.aff = Affiliation(xmltree).affiliation_by_id

    @property
    def contribs(self):
        for node, lang, article_type, parent, parent_id in _get_parent_context(
            self.xmltree
        ):
            for contrib_group in node.xpath(".//contrib-group"):
                for contrib in ContribGroup(contrib_group).contribs:
                    affs = list(_get_affs(self.aff, contrib))
                    if affs:
                        contrib["affs"] = affs
                    yield _put_parent_context(
                        contrib, lang, article_type, parent, parent_id
                    )


def _get_parent_context(xmltree):
    main = xmltree.xpath(".")[0]
    main_lang = main.get("{http://www.w3.org/XML/1998/namespace}lang")
    main_article_type = main.get("article-type")
    for node in xmltree.xpath(".//article-meta | .//sub-article"):
        parent = "sub-article" if node.tag == "sub-article" else "article"
        parent_id = node.get("id")
        lang = node.get("{http://www.w3.org/XML/1998/namespace}lang") or main_lang
        article_type = node.get("article-type") or main_article_type
        yield node, lang, article_type, parent, parent_id


def _put_parent_context(data, lang, article_type, parent, parent_id):
    data.update(
        {
            "parent": parent,
            "parent_id": parent_id,
            "parent_lang": lang,
            "parent_article_type": article_type,
        }
    )
    return data


def _get_affs(affs, contrib):
    if affs and contrib:
        for xref in contrib.get("contrib_xref"):
            aff = affs.get(xref.get("rid"))
            if aff:
                yield aff
