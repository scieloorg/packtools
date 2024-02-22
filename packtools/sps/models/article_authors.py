from packtools.sps.models.aff import Affiliation
from packtools.sps.utils.xml_utils import node_plain_text


def _get_collab(node):
    try:
        return {"collab": node_plain_text(node.xpath(".//collab")[0])}
    except IndexError:
        return {}


class Authors:
    def __init__(self, xmltree):
        self.xmltree = xmltree

    @property
    def collab(self):
        try:
            return self.xmltree.xpath(".//front//collab")[0].text
        except IndexError:
            return None

    @property
    def contribs(self):
        _data = []
        for node in self.xmltree.xpath(".//front//contrib"):
            _author = _get_collab(node)
            for tag in ("surname", "prefix", "suffix"):
                data = node.findtext(f".//{tag}")
                if data:
                    _author[tag] = data
            if data := node.findtext(".//given-names"):
                _author["given_names"] = data

            try:
                _author["orcid"] = node.xpath("contrib-id[@contrib-id-type='orcid']")[
                    0
                ].text
            except IndexError:
                pass

            _author["role"] = []
            for role in node.xpath(".//role"):
                _author["role"].append({
                    "text": role.text,
                    "content-type": role.get("content-type")})
            if not _author["role"]:
                _author.pop("role")

            for xref in node.findall('.//xref'):
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
            _author["contrib-type"] = node.attrib.get("contrib-type")
            _data.append(_author)
        return _data

    @property
    def contribs_with_affs(self):
        affs = Affiliation(self.xmltree)
        affs_by_id = affs.affiliation_by_id

        for item in self.contribs:
            for rid in item.get("aff_rids") or []:
                item.setdefault("affs", [])
                item["affs"].append(affs_by_id.get(rid))
            yield item
