class ArticleAssets:
    """
    './/graphic[@xlink:href]',
    './/media[@xlink:href]',
    './/inline-graphic[@xlink:href]',
    './/supplementary-material[@xlink:href]',
    './/inline-supplementary-material[@xlink:href]',
    """

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

    def _is_asset(self, node):
        if node.tag in (
            'graphic',
            'media',
            'inline-graphic',
            'supplementary-material',
            'inline-supplementary-material',
        ):
            return True


class Asset:
    def __init__(self, node, parent_map):
        self.node = node
        self.parent_map = parent_map

    @property
    def name(self):
        return self.node.attrib["{http://www.w3.org/1999/xlink}href"]

