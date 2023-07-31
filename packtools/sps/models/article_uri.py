class ArticleUri:
    def __init__(self, xmltree):
        self._xmltree = xmltree

    @property
    def all_uris(self):
        keys = ['sci_arttext', 'sci_abstract', 'sci_pdf']
        xlink_href = {}
        self_uri = self._xmltree.findall('.//self-uri')
        for uri in self_uri:
            value = uri.attrib['{http://www.w3.org/1999/xlink}href']
            for key in keys:
                if key in value:
                    xlink_href[key] = value

        return xlink_href
