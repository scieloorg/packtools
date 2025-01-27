from packtools.sps.models.aff import Affiliation
from packtools.sps.utils.xml_utils import (
    node_plain_text,
    get_parent_context,
    put_parent_context,
)

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
    def contrib_anonymous(self):
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
                "contrib_anonymous",
                "contrib_name",
                "contrib_full_name",
                "collab",
                "contrib_xref",
                "contrib_role",
            ),
            (
                self.contrib_type,
                self.contrib_ids,
                self.contrib_anonymous,
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

    def _extract_contrib_group(self, xpath_contrib):
        for node, lang, article_type, parent, parent_id in get_parent_context(
            self.xmltree
        ):
            for contrib_group in node.xpath(xpath_contrib):
                for contrib in ContribGroup(contrib_group).contribs:
                    affs = list(_get_affs(self.aff, contrib))
                    if affs:
                        contrib["affs"] = affs
                    yield put_parent_context(
                        contrib, lang, article_type, parent, parent_id
                    )

    @property
    def contribs_in_sub_article(self):
        # FIXME: Em sub-article, podem existir contribs duplicados.
        # Para evitar duplicidade, é necessário verificar se o contrib já foi adicionado ao conjunto de dados.
        # Solução sugerida: Utilize uma estrutura como um conjunto (set) ou uma lógica de verificação
        # para garantir que cada contrib seja adicionado apenas uma vez ao data.
        return self._extract_contrib_group(
            xpath_contrib=".//sub-article//contrib-group"
        )

    @property
    def contribs_in_article_meta(self):
        return self._extract_contrib_group(
            xpath_contrib=".//article-meta//contrib-group"
        )

    @property
    def contribs(self):
        return self._extract_contrib_group(xpath_contrib=".//contrib-group")


def _get_affs(affs, contrib):
    if affs and contrib:
        for xref in contrib.get("contrib_xref") or []:
            aff = affs.get(xref.get("rid"))
            if aff:
                yield aff
