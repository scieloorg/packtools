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
    def _is_asset(self, node):
        if node.tag in (
            'graphic',
            'media',
            'inline-graphic',
            'supplementary-material',
            'inline-supplementary-material',
        ):
            return True
