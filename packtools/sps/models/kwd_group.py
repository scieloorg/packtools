from packtools.sps.utils import xml_utils


def get_node_without_subtag(node):
    """
        Função que retorna nó sem subtags. 
    """
    return "".join(node.xpath(".//text()"))


class KwdGroup:
    def __init__(self, xmltree, subtag=False):
        self._xmltree = xmltree
        self._subtag = subtag

    def illegal_argument_error(self):
        if not isinstance(self._subtag, bool):
            raise TypeError(
                f"Argument subtag must be True or False, not {type(self._subtag)}")

    @property
    def extract_kwd_data_with_lang_text(self):
        
        self.illegal_argument_error()
        
        _data = []
        kwd_text = xml_utils.node_text_without_xref if self._subtag else get_node_without_subtag

        for kwd_group in self._xmltree.xpath('.//kwd-group'):
            _lang = kwd_group.get("{http://www.w3.org/XML/1998/namespace}lang")
            for kwd in kwd_group.xpath("kwd"):
                kwd = kwd_text(kwd)
                _data.append({"lang": _lang, "text": kwd})
        return _data

    @property
    def extract_kwd_extract_data_by_lang(self):
        
        self.illegal_argument_error()
        
        _data_dict = {}
        _data = self.extract_kwd_data_with_lang_text

        for d in _data:
            if d['lang'] not in _data_dict:
                _data_dict[d['lang']] = []
            _data_dict[d['lang']].append(d['text'])
        return _data_dict
 