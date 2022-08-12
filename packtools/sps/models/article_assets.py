class ArticleAssets:
    ASSET_TYPES = (
        'graphic',
        'media',
        'inline-graphic',
        'supplementary-material',
        'inline-supplementary-material',
    )

    XPATH_FOR_IDENTIFYING_ASSETS = '|'.join([
        './/' + at + '[@xlink:href]' for at in ASSET_TYPES
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
            ".//*[@xlink:href]", 
            namespaces={"xlink": "http://www.w3.org/1999/xlink"}
        ):            
            if self._is_asset(node):
                asset = Asset(node, self.parent_map)

                _assets.append(asset)

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
