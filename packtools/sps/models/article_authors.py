from packtools.sps.models.aff import Affiliation


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
            _author = {}
            for tag in ("surname", "prefix", "suffix"):
                xpath = f".//{tag}"
                try:
                    _author[tag] = node.xpath(xpath)[0].text
                except IndexError:
                    pass
            try:
                _author["given_names"] = node.xpath(".//given-names")[0].text
            except IndexError:
                pass
            try:
                _author["orcid"] = node.xpath("contrib-id[@contrib-id-type='orcid']")[
                    0
                ].text
            except IndexError:
                pass

            if node.xpath(".//role"):
                _author["role"] = []

            for role in node.xpath(".//role"):
                _role = role.text
                _content_type = role.get("content-type")
                _author["role"].append({"text": _role, "content-type": _content_type})

            _author['rid'] = [xref.get('rid') for xref in node.findall('.//xref')]
            _author['rid-aff'] = [xref.get('rid') for xref in node.findall('.//xref[@ref-type="aff"]')]
            _author['aff_rids'] = _author['rid-aff']
            _author['contrib-type'] = node.attrib['contrib-type']
            _data.append(_author)
        return _data

    @property
    def contribs_with_affs(self):
        affs = Affiliation(self.xmltree)
        affs_by_id = affs.affiliation_by_id

        for item in self.contribs:
            for rid in item["aff_rids"]:
                item.setdefault("affs", [])
                item["affs"].append(affs_by_id.get(rid))
            yield item
