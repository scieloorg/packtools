from packtools.sps.utils import xml_utils
from packtools.sps.models.base_text_node import BaseTextNode


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
                        keyword_text = keyword_text.replace(" ,", ",")
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

                    keyword_plain_text = []
                    keyword_html_text = []
                    for kwd in kwd_group.xpath("kwd"):
                        keyword_html_text.append(xml_utils.process_subtags(kwd,
                                                                           tags_to_keep,
                                                                           tags_to_keep_with_content,
                                                                           tags_to_remove_with_content,
                                                                           tags_to_convert_to_html))
                        keyword_plain_text.append(xml_utils.node_plain_text(kwd))
                    resp["parent_name"] = tp
                    resp["lang"] = kwd_group_lang
                    resp["plain_text"] = keyword_plain_text
                    resp["html_text"] = keyword_html_text

                    yield resp


class KwdTextNode(BaseTextNode):
    pass


class KwdGroupTextNode(BaseTextNode):

    @property
    def language(self):
        return (
            self._node.get("{http://www.w3.org/XML/1998/namespace}lang") or
            self._lang
        )

    @property
    def items(self):
        for node_kwd in self._node.xpath("kwd"):
            kn = KwdTextNode(
                node_kwd,
                self.language,
                self.tags_to_keep,
                self.tags_to_keep_with_content,
                self.tags_to_remove_with_content,
                self.tags_to_convert_to_html,
            )
            yield kn.item

    @property
    def items_by_lang(self):
        return {
            self.language: list(self.items)
        }


class ArticleKeywords:

    def __init__(self, xmltree):
        self._xmltree = xmltree

    def configure(
        self,
        tags_to_keep=None,
        tags_to_keep_with_content=None,
        tags_to_remove_with_content=None,
        tags_to_convert_to_html=None,
    ):
        self.tags_to_keep = tags_to_keep
        self.tags_to_keep_with_content = tags_to_keep_with_content
        self.tags_to_remove_with_content = tags_to_remove_with_content
        self.tags_to_convert_to_html = tags_to_convert_to_html

    @property
    def items(self):
        """
        Extract keyword data with language information from XML tree nodes.

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
        list: A list of dictionaries. Eg.:
            [
                {
                    'id': 'TRen',
                    'parent_name': 'sub-article',
                    'lang': 'en',
                    'plain_text': 'text conteúdo de bold',
                    'html_text': 'text <b>conteúdo de bold</b>'
                },...
            ]
        """
        article_lang = self._xmltree.find(".").get("{http://www.w3.org/XML/1998/namespace}lang")
        nodes = self._xmltree.xpath('.//article-meta | .//sub-article')

        for node in nodes:
            sub_article_lang = node.get("{http://www.w3.org/XML/1998/namespace}lang")

            for kwd_group in node.xpath('.//kwd-group'):
                kwd_group_text_node = KwdGroupTextNode(
                    node=kwd_group,
                    lang=sub_article_lang or article_lang,
                )
                kwd_group_text_node.configure(
                    tags_to_keep=self.tags_to_keep,
                    tags_to_keep_with_content=self.tags_to_keep_with_content,
                    tags_to_remove_with_content=self.tags_to_remove_with_content,
                    tags_to_convert_to_html=self.tags_to_convert_to_html,
                )
                for item in kwd_group_text_node.items:
                    item["parent_name"] = node.tag if node.tag == "sub-article" else 'article'
                    item["id"] = node.get("id")
                    yield item

    @property
    def items_by_lang(self):
        """
        Extract keyword data with language information from XML tree nodes.

        Returns
        -------
        dict: A dict. Eg.:
            'en': [
                    {
                        'id': 'TRen',
                        'parent_name': 'sub-article',
                        'lang': 'en',
                        'plain_text': 'text conteúdo de bold',
                        'html_text': 'text <b>conteúdo de bold</b>'
                    },...
                ]
        """
        d = {}
        for item in self.items:
            d.setdefault(item['lang'], [])
            d[item['lang']].append(item)
        return d
