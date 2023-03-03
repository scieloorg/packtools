"""
    <kwd-group xml:lang="en">
        <kwd>Triatoma sordida</kwd>
        <kwd>Triatoma guasayana</kwd>
        <kwd>Trypanosoma cruzi</kwd>
        <kwd>dispersive flight</kwd>
        <kwd>Argentina</kwd>
    </kwd-group>
"""

class KwdGroup:
    def __init__(self, xmltree):
        self._xmltree = xmltree

    @property
    def extract_kwd_data_with_lang_text(self):
        _data = []
        for kwd_group in self._xmltree.xpath('.//kwd-group'):
            _lang = kwd_group.get("{http://www.w3.org/XML/1998/namespace}lang")
            for kwd in kwd_group.xpath("kwd"):
                _data.append({"lang": _lang, "text": kwd.text})
        
        return _data

    @property
    def extract_kwd_extract_data_by_lang(self):
        _data_dict = {}
        _data = self.extract_kwd_data_with_lang_text
        
        for d in _data:
            if d['lang'] not in _data_dict:
                _data_dict[d['lang']] = []    
            _data_dict[d['lang']].append(d['text'])
        return _data_dict
       


