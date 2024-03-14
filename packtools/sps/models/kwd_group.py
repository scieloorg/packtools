from packtools.sps.utils import xml_utils


class KwdGroup:
    def __init__(self, xmltree):
        self._xmltree = xmltree

    def extract_kwd_data_with_lang_text(self,
                                        subtag,
                                        tags_to_keep=None,
                                        tags_to_keep_with_content=None,
                                        tags_to_remove_with_content=None,
                                        tags_to_convert_to_html=None
                                        ):
        """
        Extract keyword data with language information from XML tree nodes.

        Params
        ------
        subtag (bool): True -> process subtags, False -> plain text
        tags_to_keep (list, optional): Tags to be preserved. Eg.:
            ['bold', 'p']
        tags_to_keep_with_content (list, optional): Tags to be preserved with the respective content. Eg.:
            ['bold', 'p']
        tags_to_remove_with_content (list, optional): Tags to be removed with its content. Eg.:
            ['bold', 'p']
        tags_to_convert_to_html (dict, optional): Tags to be converted into HTML format. Eg.:
            {'bold': 'b'}

        Returns
        -------
        list: A list of dictionaries. Eg.:
            [
                {
                    'lang': 'en',
                    'text': 'Chagas Disease, transmission'
                },...
            ]
        """
        _data = []

        nodes = self._xmltree.xpath('.//article-meta | .//sub-article')

        for node in nodes:
            node_lang = node.get("{http://www.w3.org/XML/1998/namespace}lang")

            for kwd_group in node.xpath('.//kwd-group'):
                kwd_group_lang = kwd_group.get("{http://www.w3.org/XML/1998/namespace}lang", node_lang)

                for kwd in kwd_group.xpath("kwd"):
                    if subtag:
                        keyword_text = xml_utils.process_subtags(kwd, tags_to_keep, tags_to_keep_with_content,
                                                                 tags_to_remove_with_content, tags_to_convert_to_html)
                    else:
                        keyword_text = xml_utils.node_plain_text(kwd)
                    _data.append({"lang": kwd_group_lang, "text": keyword_text})

        return _data

    def extract_kwd_extract_data_by_lang(self,
                                         subtag,
                                         tags_to_keep=None,
                                         tags_to_keep_with_content=None,
                                         tags_to_remove_with_content=None,
                                         tags_to_convert_to_html=None
                                         ):
        """
        Extract keyword data with language information from XML tree nodes.

        Params
        ------
        subtag (bool): True -> process subtags, False -> plain text
        tags_to_keep (list, optional): Tags to be preserved. Eg.:
            ['bold', 'p']
        tags_to_keep_with_content (list, optional): Tags to be preserved with the respective content. Eg.:
            ['bold', 'p']
        tags_to_remove_with_content (list, optional): Tags to be removed with its content. Eg.:
            ['bold', 'p']
        tags_to_convert_to_html (dict, optional): Tags to be converted into HTML format. Eg.:
            {'bold': 'b'}

        Returns
        -------
        dict: A dict. Eg.:
            {
            'en': [
                'Primary health care',
                'Ambulatory care facilities',
                'Chronic pain',
                'Analgesia',
                'Pain management'
            ],
            'pt': [
                'Atenção primária à saúde',
                'Instituições de assistência ambulatorial',
                'Dor crônica',
                'Analgesia',
                'Tratamento da dor'
            ]
        }
        """

        _data_dict = {}
        _data = self.extract_kwd_data_with_lang_text(subtag, tags_to_keep, tags_to_keep_with_content,
                                                     tags_to_remove_with_content, tags_to_convert_to_html)

        for d in _data:
            if d['lang'] not in _data_dict:
                _data_dict[d['lang']] = []
            _data_dict[d['lang']].append(d['text'])
        return _data_dict

    def extract_kwd_data_with_lang_text_by_article_type(self, subtag,
                                                        tags_to_keep=None,
                                                        tags_to_keep_with_content=None,
                                                        tags_to_remove_with_content=None,
                                                        tags_to_convert_to_html=None
                                                        ):
        """
        Extract keyword data with language information by article type from XML tree nodes.

        Params
        ------
        subtag (bool): True -> process subtags, False -> plain text
        tags_to_keep (list, optional): Tags to be preserved. Eg.:
            ['bold', 'p']
        tags_to_keep_with_content (list, optional): Tags to be preserved with the respective content. Eg.:
            ['bold', 'p']
        tags_to_remove_with_content (list, optional): Tags to be removed with its content. Eg.:
            ['bold', 'p']
        tags_to_convert_to_html (dict, optional): Tags to be converted into HTML format. Eg.:
            {'bold': 'b'}

        Returns
        -------
        Iterator[dict]: A generator that yields dictionaries. Eg.:
            {
                'parent_name': 'article',
                'lang': 'pt',
                'text': ['Enfermagem', 'Idoso de 80 Anos ou Mais', 'Relações Familiares']
            },...
        """
        dict_nodes = {
            'article': self._xmltree.xpath('.//article-meta'),
            'sub-article': self._xmltree.xpath('./sub-article')
        }

        for tp, nodes in dict_nodes.items():
            for node in nodes:
                node_lang = node.get("{http://www.w3.org/XML/1998/namespace}lang")
                resp = {}
                if node.get("id") is not None:
                    resp['id'] = node.get("id")

                for kwd_group in node.xpath('.//kwd-group'):
                    kwd_group_lang = kwd_group.get("{http://www.w3.org/XML/1998/namespace}lang", node_lang)

                    keyword_text = []
                    for kwd in kwd_group.xpath("kwd"):
                        if subtag:
                            keywords = xml_utils.process_subtags(kwd, tags_to_keep, tags_to_keep_with_content,
                                                                 tags_to_remove_with_content,
                                                                 tags_to_convert_to_html)
                        else:
                            keywords = xml_utils.node_plain_text(kwd)
                        keyword_text.append(keywords)
                    resp["parent_name"] = tp
                    resp["lang"] = kwd_group_lang
                    resp["text"] = keyword_text

                    yield resp

    def extract_kwd_data_with_lang_html_format(self,
                                               tags_to_keep=None,
                                               tags_to_keep_with_content=None,
                                               tags_to_remove_with_content=None,
                                               tags_to_convert_to_html=None
                                               ):
        """
        Extract keyword data with language information by article type from XML tree nodes.

        Params
        ------
        tags_to_keep (list, optional): Tags to be preserved. Eg.:
            ['bold', 'p']
        tags_to_keep_with_content (list, optional): Tags to be preserved with the respective content. Eg.:
            ['bold', 'p']
        tags_to_remove_with_content (list, optional): Tags to be removed with its content. Eg.:
            ['bold', 'p']
        tags_to_convert_to_html (dict, optional): Tags to be converted into HTML format. Eg.:
            {'bold': 'b'}

        Returns
        -------
        Iterator[dict]: A generator that yields dictionaries. Eg.:
            {
                'parent_name': 'article',
                'lang': 'pt',
                'plain_text': None,
                'html_text': [
                    '<bold>conteúdo de bold</bold> text',
                    'text <bold>conteúdo de bold</bold> text',
                    'text <bold>conteúdo de bold</bold>',
                    'text <bold>conteúdo <i>de</i> bold</bold>'
                ]
            },...
        """
        dict_nodes = {
            'article': self._xmltree.xpath('.//article-meta'),
            'sub-article': self._xmltree.xpath('./sub-article')
        }

        for tp, nodes in dict_nodes.items():
            for node in nodes:
                node_lang = node.get("{http://www.w3.org/XML/1998/namespace}lang")
                resp = {}
                if node.get("id") is not None:
                    resp['id'] = node.get("id")

                for kwd_group in node.xpath('.//kwd-group'):
                    kwd_group_lang = kwd_group.get("{http://www.w3.org/XML/1998/namespace}lang", node_lang)

                    keyword_text = []
                    for kwd in kwd_group.xpath("kwd"):
                        keywords = xml_utils.process_subtags(kwd, tags_to_keep, tags_to_keep_with_content,
                                                             tags_to_remove_with_content, tags_to_convert_to_html)
                        keyword_text.append(keywords)
                    resp["parent_name"] = tp
                    resp["lang"] = kwd_group_lang
                    resp["plain_text"] = None
                    resp["html_text"] = keyword_text

                    yield resp
