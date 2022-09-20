class AssetReplacementError(Exception):
    ...


class ArticleAssets:
    ASSET_TAGS = (
        'graphic',
        'media',
        'inline-graphic',
        'supplementary-material',
        'inline-supplementary-material',
    )

    XPATH_FOR_IDENTIFYING_ASSETS = '|'.join([
        './/' + at + '[@xlink:href]' for at in ASSET_TAGS
    ])

    def __init__(self, xmltree):
        self.xmltree = xmltree
        self.create_parent_map()

    def create_parent_map(self):
        self.parent_map = dict(
            (c, p) for p in self.xmltree.iter() for c in p
        )

    @property
    def article_assets(self):
        _assets = []

        for node in self.xmltree.xpath(
            ArticleAssets.XPATH_FOR_IDENTIFYING_ASSETS,
            namespaces={"xlink": "http://www.w3.org/1999/xlink"}
        ):
            _assets.append(Asset(node, self.parent_map))

        return _assets

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
        for asset in self.article_assets:
            try:
                asset.name = from_to[asset.name]
            except KeyError as e:
                not_found.append(asset.name)
        return not_found


class Asset:
    def __init__(self, node, parent_map):
        self.node = node
        self.parent_map = parent_map

    @property
    def name(self):
        return self.node.attrib["{http://www.w3.org/1999/xlink}href"]

    @name.setter
    def name(self, value):
        self.node.set("{http://www.w3.org/1999/xlink}href", value)

    @property
    def _content_type(self):
        ct = self.node.get('content-type')
        if ct:
            return f'-{ct}'
        return ''

    @property
    def _category_name_code(self):
        """
        -g: figure graphic
        -i: inline graphic
        -e: equation
        -s: supplementary data file
        """
        if "display-formula" in self.node.tag:
            return "e"
        if "supplementary" in self.node.tag:
            return "s"
        if "inline" in self.node.tag:
            return "i"
        return "g"

    @property
    def _suffix(self):
        id_number = ''.join([i for i in self.id if i.isdigit()]).zfill(2)
        return f"-{self._category_name_code}{id_number}{self._content_type or ''}"

    def id(self):
        current_node = self.node

        while current_node is not None and hasattr(current_node, 'attrib') and 'id' not in current_node.attrib:
            current_node = self.parent_map.get(current_node)

        if current_node is None or not hasattr(current_node, 'attrib'):
            return

        current_node_attrib = getattr(current_node, 'attrib')
        if current_node_attrib:
            return current_node_attrib.get('id')

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
        if 'content-type' in self.node.attrib:
            return 'thumbnail'
        elif 'specific-use' in self.node.attrib:
            return 'optimised'
        else:
            return 'original'


class SupplementaryMaterials:

    def __init__(self, xmltree):
        self.xmltree = xmltree
        self._assets = ArticleAssets(xmltree)

    @property
    def items(self):
        return [item
                for item in self._assets.article_assets
                if item.node.tag in ('supplementary-material',
                                     'inline-supplementary-material')
                ]

    @property
    def data(self):
        return [{"id": item.id, "name": item.name, }
                for item in self.items
                ]
