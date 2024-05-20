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
        return {
            item.get("contrib-id-type"): item.text for item in self.node.xpath(".//contrib-id")
        }

    @property
    def contrib_name(self):
        name = self.node.find("name")
        if name is not None:
            return {
                item.tag: item.text for item in name
            }

    @property
    def collab(self):
        return self.node.findtext("collab")

    @property
    def contrib_xref(self):
        for item in self.node.xpath(".//xref"):
            yield {
                "rid": item.get("rid"),
                "ref_type": item.get("ref-type"),
                "text": item.text
            }

    @property
    def contrib_role(self):
        for item in self.node.xpath(".//role"):
            yield {
                "text": item.text,
                "content-type": item.get("content-type"),
                "specific-use": item.get("specific-use")
            }

    @property
    def data(self):
        data = {}
        for key, value in zip(
            (
                "contrib_type",
                "contrib_ids",
                "contrib_name",
                "collab",
                "contrib_xref",
                "contrib_role"
            ),
            (
                self.contrib_type,
                self.contrib_ids,
                self.contrib_name,
                self.collab,
                list(self.contrib_xref),
                list(self.contrib_role)
            )
        ):
            if value:
                data[key] = value
        return data
