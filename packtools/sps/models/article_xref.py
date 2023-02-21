
class ArticleXref:
    def __init__(self, xmltree):
        self._xmltree = xmltree

    @property
    def all_ids(self):
        ids = set()
        for node in self._xmltree.xpath('.//*[@id]'):
            ids.add(node.get('id'))
        return ids

    @property
    def all_xref_rids(self):
        rids = set()
        for node in self._xmltree.xpath('.//xref[@rid]'):
            rids.add(node.get('rid'))
        return rids
