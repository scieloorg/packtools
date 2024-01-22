from packtools.sps.utils import xml_utils


def get_node_without_subtag(node):
    """
        Função que retorna nó sem subtags. 
    """
    return "".join(node.xpath(".//text()"))


class KwdGroup:
    def __init__(self, xmltree):
        self._xmltree = xmltree
    
    def extract_kwd_data_with_lang_text(self, subtag):
        
        _data = []
        kwd_text = xml_utils.node_text_without_xref if subtag else get_node_without_subtag

        for kwd_group in self._xmltree.xpath('.//kwd-group'):
            _lang = kwd_group.get("{http://www.w3.org/XML/1998/namespace}lang")
            for kwd in kwd_group.xpath("kwd"):
                kwd = kwd_text(kwd)
                _data.append({"lang": _lang, "text": kwd})
        return _data

    def extract_kwd_extract_data_by_lang(self, subtag):
        
        _data_dict = {}
        _data = self.extract_kwd_data_with_lang_text(subtag)

        for d in _data:
            if d['lang'] not in _data_dict:
                _data_dict[d['lang']] = []
            _data_dict[d['lang']].append(d['text'])
        return _data_dict

    def extract_kwd_data_with_lang_text_by_article_type(self, subtag):
        kwd_text = xml_utils.node_text_without_xref if subtag else get_node_without_subtag

        dict_nodes = {
            'article': self._xmltree.xpath('.//article-meta'),
            'sub-article': self._xmltree.xpath('.//sub-article')
        }

        for tp, nodes in dict_nodes.items():
            for node in nodes:
                node_lang = node.get("{http://www.w3.org/XML/1998/namespace}lang")

                for kwd_group in node.xpath('.//kwd-group'):
                    kwd_group_lang = kwd_group.get("{http://www.w3.org/XML/1998/namespace}lang", node_lang)

                    keyword_text = []
                    for kwd in kwd_group.xpath("kwd"):
                        keyword_text.append(kwd_text(kwd))
                    yield {"type": tp, "lang": kwd_group_lang, "text": keyword_text}

