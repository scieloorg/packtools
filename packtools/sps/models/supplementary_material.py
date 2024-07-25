from packtools.sps.utils.xml_utils import get_parent_context, put_parent_context


class SupplementaryMaterial:
    def __init__(self, node):
        self.node = node

    @property
    def supplementary_material_id(self):
        return self.node.get("id")

    @property
    def supplementary_material_label(self):
        return self.node.findtext("label")

    @property
    def mimetype(self):
        return self.node.get("mimetype")

    @property
    def mime_subtype(self):
        return self.node.get("mime-subtype")

    @property
    def xlink_href(self):
        return self.node.get("{http://www.w3.org/1999/xlink}href")

    @property
    def data(self):
        return {
            "supplementary_material_id": self.supplementary_material_id,
            "supplementary_material_label": self.supplementary_material_label,
            "mimetype": self.mimetype,
            "mime_subtype": self.mime_subtype,
            "xlink_href": self.xlink_href,
        }


class ArticleSupplementaryMaterials:
    def __init__(self, xml_tree):
        self.xml_tree = xml_tree

    def data(self):
        for node, lang, article_type, parent, parent_id in get_parent_context(
            self.xml_tree
        ):
            for supp_node in node.xpath(
                ".//supplementary-material | .//inline-supplementary-material"
            ):
                supp_data = SupplementaryMaterial(supp_node).data
                yield put_parent_context(
                    supp_data, lang, article_type, parent, parent_id
                )
