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
CHILD_ASSET_TAGS = (
    "graphic",
    "media",
    "supplementary-material",
    "inline-supplementary-material",
)
PARENT_ASSET_TAGS = (
    "fig-group",
    "fig",
    "table-wrap",
    "supplementary-material",
    "disp-formula",
    "app",
)
PARENT_ASSET_XPATH = " | ".join([f".//{at}[@id]" for at in PARENT_ASSET_TAGS])
CHILD_ASSET_XPATH = (
    "|".join([f".//{at}[@xlink:href]" for at in CHILD_ASSET_TAGS])
    + "|"
    + "|".join([f".//alternatives//{at}[@xlink:href]" for at in CHILD_ASSET_TAGS])
)

ASSET_XPATH = (
    "|".join([f".//{at}[@xlink:href]" for at in ASSET_TAGS])
    + "|"
    + "|".join([f".//alternatives//{at}[@xlink:href]" for at in CHILD_ASSET_TAGS])
)


class ArticleAssets:
    def __init__(self, xmltree):
        self.xmltree = xmltree

    @property
    def items(self):
        for root in self.xmltree.findall("*"):
            # front, body, back, sub-article
            yield from self.get_assets(root)

    @property
    def supplementary_material_items(self):
        for item in self.items:
            if item.is_supplementary_material:
                yield item

    def get_assets(self, root):
        if root is None:
            return

        for asset in root.xpath(
            ASSET_XPATH, namespaces={"xlink": "http://www.w3.org/1999/xlink"}
        ):
            asset.set("visited", "false")

        total = len(root.xpath(".//*[@visited]"))

        for asset_parent in root.xpath(PARENT_ASSET_XPATH):
            for asset in asset_parent.xpath(
                CHILD_ASSET_XPATH,
                namespaces={"xlink": "http://www.w3.org/1999/xlink"}
            ):

                if not asset.get("visited"):
                    continue
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

    @property
    def grouped_by_id(self):
        group = {}
        for item in self.items:
            ids = [
                item.root.get("id"),
                item.id or item.number,
            ]
            id_ = "".join([v for v in ids if v])
            group.setdefault(id_, [])
            group[id_].append(item.data)
        return group

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
        self.parent = parent
        self.number = number
        self.root = root

    @property
    def data(self):
        try:
            tag = self.parent.tag
        except AttributeError:
            tag = self.node.tag
        return {
            "tag": tag,
            "id": self.id,
            "number": self.number,
            "xlink_href": self.xlink_href,
            "type": self.type,
            "is_supplementary_material": self.is_supplementary_material,
        }

    @property
    def id(self):
        id_ = self.node.get("id")
        if not id_:
            try:
                id_ = self.parent.get("id")
            except AttributeError:
                pass
        return id_

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
        lang = self.root.get("{http://www.w3.org/XML/1998/namespace}lang") or ""
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
        tags = [self.node.tag]
        if self.parent is not None:
            tags.append(self.parent.tag)
        for tag in tags:
            if tag and "supplementary" in tag:
                return True
        return False
