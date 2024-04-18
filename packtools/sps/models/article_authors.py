from packtools.sps.models.aff import Affiliation
from packtools.sps.utils.xml_utils import process_subtags


def _get_collab(node):
    try:
        return {"collab": process_subtags(node.xpath(".//collab")[0])}
    except IndexError:
        return {}


class Contrib:
    def __init__(self, xmltree, node):
        self.xmltree = xmltree
        self.node = node

    @property
    def contrib(self):
        _author = _get_collab(self.node)
        for tag in ("surname", "prefix", "suffix"):
            data = self.node.findtext(f".//{tag}")
            if data:
                _author[tag] = data
        if data := self.node.findtext(".//given-names"):
            _author["given_names"] = data

        try:
            _author["orcid"] = self.node.xpath("contrib-id[@contrib-id-type='orcid']")[
                0
            ].text
        except IndexError:
            pass

        _author["role"] = []
        for role in self.node.xpath(".//role"):
            _author["role"].append({
                "text": role.text,
                "content-type": role.get("content-type"),
                "specific-use": role.get("specific-use")
            })
        if not _author["role"]:
            _author.pop("role")

        for xref in self.node.findall('.//xref'):
            rid = xref.get("rid")

            if not rid:
                continue
            _author.setdefault("rid", [])
            _author["rid"].append(rid)

            reftype = xref.get("ref-type")
            if not reftype == "aff":
                continue
            _author.setdefault("rid-aff", [])
            _author["rid-aff"].append(rid)

        _author["aff_rids"] = _author.get("rid-aff")
        _author["contrib-type"] = self.node.attrib.get("contrib-type")
        return _author

    @property
    def contrib_with_aff(self):
        contrib = self.contrib
        affs = Affiliation(self.xmltree)
        affs_by_id = affs.affiliation_by_id
        for rid in contrib.get("aff_rids") or []:
            aff = affs_by_id.get(rid)
            if aff:
                contrib.setdefault("affs", [])
                contrib["affs"].append(aff)
        return contrib


