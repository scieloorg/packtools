from packtools.sps.utils.xml_utils import get_parent_context, put_parent_context


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

    def data(self):
        for node, lang, article_type, parent, parent_id in get_parent_context(self._xmltree):
            ids = set()
            for item in node.xpath('.//*[@id]'):
                ids.add((item.tag, item.get('id')))
            sorted_ids = sorted(ids)
            response = {"ids": sorted_ids}
            rids = set()
            for item in node.xpath('.//xref[@rid]'):
                rids.add(item.get('rid'))
            sorted_rids = sorted(rids)
            response.update({"rids": sorted_rids})
            yield put_parent_context(response, lang, article_type, parent, parent_id)
