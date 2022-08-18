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


class Asset:
    def __init__(self, node, parent_map):
        self.node = node
        self.parent_map = parent_map

    @property
    def name(self):
        return self.node.attrib["{http://www.w3.org/1999/xlink}href"]

    @property
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
