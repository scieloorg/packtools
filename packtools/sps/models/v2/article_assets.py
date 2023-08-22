import os


class AssetReplacementError(Exception):
    ...


ASSET_TAGS = (
    "graphic",
    "media",
    "inline-graphic",
    "supplementary-material",
    "inline-supplementary-material",
)
PARENTE_ASSET_TAGS = (
    "fig",
    "fig-group",
    "table-wrap",
    "supplementary-material",
    "disp-formula",
    "app",
)
PARENTE_ASSET_XPATH = " | ".join(PARENTE_ASSET_TAGS)
ASSET_XPATH = "|".join([".//" + at + "[@xlink:href]" for at in ASSET_TAGS])


class ArticleAssets:
    def __init__(self, xmltree):
        self.xmltree = xmltree

    @property
    def items(self):
        for root in self.xmltree.findall("*"):
            yield from self.get_assets(root)

    @property
    def supplementary_material_items(self):
        for item in self.items:
            if item.is_supplementary_material:
                yield item

    def get_assets(self, root):
        if root is None:
            return

        for asset in asset_parent.xpath(
            ASSET_XPATH, namespaces={"xlink": "http://www.w3.org/1999/xlink"}
        ):
            asset.set("visited", "false")

        for asset_parent in root.xpath(PARENTE_ASSET_XPATH):
            for asset in asset_parent.xpath(
                ASSET_XPATH, namespaces={"xlink": "http://www.w3.org/1999/xlink"}
            ):
                asset.attrib.pop("visited")
                yield Asset(asset, root, parent=asset_parent)

        number = 0
        total = len(root.xpath(".//*[@visited]"))
        zfill = len(str(total))
        for asset in root.xpath(".//*[@visited]"):
            asset.attrib.pop("visited")
            number += 1
            yield Asset(
                asset,
                root,
                number=str(number).zfill(zfill),
            )

    def replace_names(self, from_to):
        """
        Replace names

        Parameters
        ----------
        from_to : dict

        Returns
        -------
        str list : not found names to replace
        """
        not_found = []
        for asset in self.items:
            try:
                asset.xlink_href = from_to[asset.xlink_href]
            except KeyError as e:
                not_found.append(asset.xlink_href)
        return not_found


class Asset:
    def __init__(self, node, root, parent=None, number=None):
        self.node = node
        self._parent = parent
        self._number = number
        self._root = root

    @property
    def id(self):
        return self._parent.get("id")

    @property
    def xlink_href(self):
        return self.node.attrib["{http://www.w3.org/1999/xlink}href"]

    @xlink_href.setter
    def xlink_href(self, value):
        self.node.set("{http://www.w3.org/1999/xlink}href", value)

    @property
    def content_type(self):
        return self.node.get("content-type")

    @property
    def category_prefix(self):
        """
        -g: figure graphic
        -i: inline graphic
        -e: equation
        -s: supplementary data file
        """
        tags = [self.node.tag]
        if self.parent is not None:
            tags.append(self.parent.tag)
        if "disp-formula" in tags:
            return "e"
        if "supplementary" in tags or "app" in tags:
            return "s"
        if "inline" in tags:
            return "i"
        return "g"

    @property
    def suffix(self):
        id_ = self.id or self.number
        content_type = self.content_type or ""
        if content_type:
            content_type = f"-{content_type}"
        lang = self.root.get("{http://www.w3.org/XML/1998/namespace}lang")
        return f"-{self.category_prefix}{id_}{content_type}{lang}"

    @property
    def ext(self):
        _, ext = os.path.splitext(self.xlink_href)
        return ext

    def name_canonical(self, package_name):
        return f"{package_name}{self.suffix}{self.ext}"

    @property
    def type(self):
        """
        <alternatives>
            <graphic xlink:href="original.tif"/>
            <graphic xlink:href="padrao.png" specific-use="scielo-web"/>
            <graphic xlink:href="mini.jpg" specific-use="scielo-web" content-type="scielo-267x140"/>
        </alternatives>

        In the above case, this property returns 'original' for original.tif, 'optimised' for pattern.png and 'thumbnail' for mini.jpg'.
        """
        if "content-type" in self.node.attrib:
            return "thumbnail"
        elif "specific-use" in self.node.attrib:
            return "optimised"
        else:
            return "original"

    @property
    def is_supplementary_material(self):
        if "supplementary" in self.node.tag:
            return True
        if "supplementary" in self.parent.tag:
            return True
        return False
