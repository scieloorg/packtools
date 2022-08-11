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
