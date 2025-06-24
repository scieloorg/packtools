from packtools.sps.models.base_text_node import BaseTextNode

"""
<article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink"
article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
<front>
<article-meta>
<abstract>
<title>Abstract</title>
<sec>
<title>Objective:</title>
<p>objective.</p>
</sec>
<sec>
<title>Method:</title>
<p>method</p>
</sec>
<sec>
<title>Results:</title>
<p>results</p>
</sec>
<sec>
<title>Conclusion:</title>
<p>conclusion</p>
</sec>
</abstract>
<trans-abstract xml:lang="es">
<title>RESUMEN</title>
<sec>
<title>Objetivo:</title>
<p>objetivo</p>
</sec>
<sec>
<title>Método:</title>
<p>metodo</p>
</sec>
<sec>
<title>Resultados:</title>
<p>resultados</p>
</sec>
<sec>
<title>Conclusión:</title>
<p>conclusion</p>
</sec>
</trans-abstract>
</article-meta>
</front>
<sub-article article-type="translation" id="s1" xml:lang="pt">
<front-stub>
<article-id pub-id-type="doi">10.1590/1980-220X-REEUSP-2021-0569pt</article-id>
<abstract>
<title>RESUMO</title>
<sec>
<title>Objetivo:</title>
<p>objetivo</p>
</sec>
<sec>
<title>Método:</title>
<p>metodo</p>
</sec>
<sec>
<title>Resultados:</title>
<p>resultados</p>
</sec>
<sec>
<title>Conclusão:</title>
<p>conclusão</p>
</sec>
</abstract>
</front-stub>
</sub-article>
</article>
"""
from packtools.sps.utils.xml_utils import node_text, get_node_without_subtag, process_subtags


class BaseAbstract:
    def __init__(self, node):
        self.node = node

    @property
    def title(self):
        return self.node.findtext('title')

    @property
    def p(self):
        for highlight in self.node.xpath('p'):
            yield process_subtags(highlight)

    @property
    def kwds(self):
        for kwd in self.node.xpath('.//kwd/text()'):
            yield kwd

    @property
    def abstract_type(self):
        return self.node.get("abstract-type")

    @property
    def data(self):
        return {
            "title": self.title,
            "p": list(self.p),
            "kwds": list(self.kwds),
            "abstract_type": self.abstract_type
        }


class Abstract(BaseAbstract):

    def __init__(self, xmltree):
        self.xmltree = xmltree

    def _get_structured_abstract(self, abstract_node, html=False, tags_to_keep=None, tags_to_remove_with_content=None,
                                 tags_to_convert_to_html=None):
        """
        Retorna o resumo estruturado

        Returns
        -------
        dict : {
            "title": "Abstract",
            "lang": lang,
            "sections": [
                {
                    "title": "",
                    "p": "",
                },
                {
                    "title": "",
                    "p": "",
                },
            ],
            "p": "",
        }
        """
        out = dict()

        node_title = abstract_node.find("title")

        out["title"] = process_subtags(node_title,
                                       tags_to_keep=tags_to_keep,
                                       tags_to_remove_with_content=tags_to_remove_with_content,
                                       tags_to_convert_to_html=tags_to_convert_to_html) \
            if html else get_node_without_subtag(node_title)

        out["lang"] = abstract_node.get("{http://www.w3.org/XML/1998/namespace}lang")

        for node in abstract_node.xpath("sec"):
            # node = abstract/sec
            out.setdefault("sections", [])

            p = title = None
            node_title = node.find("title")
            if node_title is not None:
                title = process_subtags(node_title,
                                        tags_to_keep=tags_to_keep,
                                        tags_to_remove_with_content=tags_to_remove_with_content,
                                        tags_to_convert_to_html=tags_to_convert_to_html) \
                    if html else get_node_without_subtag(node_title)

            node_p = node.find("p")
            if node_p is not None:
                p = process_subtags(node_p,
                                    tags_to_keep=tags_to_keep,
                                    tags_to_remove_with_content=tags_to_remove_with_content,
                                    tags_to_convert_to_html=tags_to_convert_to_html) \
                    if html else get_node_without_subtag(node_p)

            out["sections"].append({"title": title, "p": p})
        else:
            # abstract/p
            node_p = abstract_node.find("p")
            if node_p is not None:
                out["p"] = process_subtags(node_p,
                                           tags_to_keep=tags_to_keep,
                                           tags_to_remove_with_content=tags_to_remove_with_content,
                                           tags_to_convert_to_html=tags_to_convert_to_html) \
                    if html else get_node_without_subtag(node_p).strip()

        return out

    def _format_abstract(self, abstract_node, style=None, html=False, tags_to_keep=None,
                         tags_to_remove_with_content=None, tags_to_convert_to_html=None):
        if style == "xml":
            # formato xml
            return node_text(abstract_node)

        if style == "inline":
            # retorna o conteúdo do nó abstract como str
            if html:
                return process_subtags(abstract_node,
                                       tags_to_keep=tags_to_keep,
                                       tags_to_remove_with_content=tags_to_remove_with_content,
                                       tags_to_convert_to_html=tags_to_convert_to_html)
            return get_node_without_subtag(abstract_node, remove_extra_spaces=True)

        if style == "only_p":
            # retorna somente o conteúdo dos nós abstract//p como str
            texts = []
            for node_p in abstract_node.xpath(".//p"):
                if html:
                    p_text = process_subtags(node_p,
                                             tags_to_keep=tags_to_keep,
                                             tags_to_remove_with_content=tags_to_remove_with_content,
                                             tags_to_convert_to_html=tags_to_convert_to_html)
                else:
                    p_text = get_node_without_subtag(node_p)
                texts.append(p_text.strip())
            return " ".join(texts)

        # retorna abstract em formato de dicionário
        return self._get_structured_abstract(abstract_node,
                                             html,
                                             tags_to_keep=tags_to_keep,
                                             tags_to_remove_with_content=tags_to_remove_with_content,
                                             tags_to_convert_to_html=tags_to_convert_to_html)

    def get_main_abstract(self, style=None, html=False, tags_to_keep=None, tags_to_remove_with_content=None,
                          tags_to_convert_to_html=None):
        """
        Obtem o resumo principal

        Params
        ------
        style : str
            xml -> conteúdo de 'abstract' no formato XML
            inline -> conteúdo de 'abstract' no formato str
            only_p -> conteúdo de 'abstract//p' no formato str
            O formato padrão (style=None) retorna o conteúdo de 'abstract' no formato estruturado (dict):
                {
                    "title": "Abstract",
                    "lang": lang,
                    "sections": [
                        {
                            "title": "",
                            "p": "",
                        },
                        {
                            "title": "",
                            "p": "",
                        },
                    ],
                    "p": "",
                }
        html : bool
            True -> conteúdo de 'abstract' no formato HTML
            False -> conteúdo de 'abstract' no formato indicado por 'style' (padrão)
        tags_to_keep : list
            Lista de 'tags' que serão mantidas no formato HTML, os valores em 'tags_to_keep' serão
            complementados com as seguites 'tags': ['sup', 'sub', 'mml:math', 'math'] (padrão)
        tags_to_remove_with_content : list
            Lista de 'tags' que serão removidas com o respectivo conteúdo no formato HTML,
            os valores em 'tags_to_remove_with_content' serão complementados com as seguites 'tags': ['xref'] (padrão)
        tags_to_convert_to_html : dict
            Dicionário no formato 'tag_xml': 'tag_html' para a conversão de formatos,
            os valores em 'tags_to_convert_to_html' serão complementados com o seguite: {'italic': 'i'} (padrão)

        Returns
        -------
        {
            "parent_name": "article",
            "lang": idioma do 'abstract',
            "abstract": resumo no formato indicado
        }
        """
        try:
            abstract_node = self.xmltree.xpath(".//abstract[not(@abstract-type)]")[0]
        except IndexError:
            abstract_node = None
  
        if abstract_node is not None:
            abstract = self._format_abstract(
                abstract_node=abstract_node,
                style=style,
                html=html,
                tags_to_keep=tags_to_keep,
                tags_to_remove_with_content=tags_to_remove_with_content,
                tags_to_convert_to_html=tags_to_convert_to_html
            )
            article_lang = self.xmltree.find(".").get("{http://www.w3.org/XML/1998/namespace}lang")
            abstract_lang = abstract_node.get("{http://www.w3.org/XML/1998/namespace}lang")
            if not style:
                abstract["lang"] = abstract_lang or article_lang
            return {
                "parent_name": "article",
                "lang": abstract_lang or article_lang,
                "abstract": abstract
            }

    def _get_sub_article_abstracts(self, style=None, html=False, tags_to_keep=None, tags_to_remove_with_content=None,
                                   tags_to_convert_to_html=None):
        """
        Obtem os resumos em 'sub-article'

        Params
        ------
        style : str
            xml -> conteúdo de 'abstract' no formato XML
            inline -> conteúdo de 'abstract' no formato str
            only_p -> conteúdo de 'abstract//p' no formato str
            O formato padrão (style=None) retorna o conteúdo de 'abstract' no formato estruturado (dict):
                {
                    "title": "Abstract",
                    "lang": lang,
                    "sections": [
                        {
                            "title": "",
                            "p": "",
                        },
                        {
                            "title": "",
                            "p": "",
                        },
                    ],
                    "p": "",
                }
        html : bool
            True -> conteúdo de 'abstract' no formato HTML
            False -> conteúdo de 'abstract' no formato indicado por 'style' (padrão)
        tags_to_keep : list
            Lista de 'tags' que serão mantidas no formato HTML, os valores em 'tags_to_keep' serão
            complementados com as seguites 'tags': ['sup', 'sub', 'mml:math', 'math'] (padrão)
        tags_to_remove_with_content : list
            Lista de 'tags' que serão removidas com o respectivo conteúdo no formato HTML,
            os valores em 'tags_to_remove_with_content' serão complementados com as seguites 'tags': ['xref'] (padrão)
        tags_to_convert_to_html : dict
            Dicionário no formato 'tag_xml': 'tag_html' para a conversão de formatos,
            os valores em 'tags_to_convert_to_html' serão complementados com o seguite: {'italic': 'i'} (padrão)

        Returns
        -------
        Gerador de:
            {
                "parent_name": "sub-article",
                "lang": idioma do 'abstract',
                "abstract": resumo no formato indicado,
                "id": identificador do 'sub-article'
            }
        """

        for sub_article in self.xmltree.xpath(".//sub-article"): 
            try:
                abstract_node = sub_article.xpath(".//abstract[not(@abstract-type)]")[0]
            except IndexError:
                abstract_node = None
            if abstract_node is not None:
                sub_article_lang = sub_article.get("{http://www.w3.org/XML/1998/namespace}lang")
                abstract_lang = abstract_node.get("{http://www.w3.org/XML/1998/namespace}lang")
                item = {}
                item["parent_name"] = "sub-article"
                item["lang"] = abstract_lang or sub_article_lang
                item["abstract"] = self._format_abstract(
                    abstract_node=abstract_node,
                    style=style,
                    html=html,
                    tags_to_keep=tags_to_keep,
                    tags_to_remove_with_content=tags_to_remove_with_content,
                    tags_to_convert_to_html=tags_to_convert_to_html
                )
                if not style:
                    item["abstract"]["lang"] = item["lang"]
                item['id'] = sub_article.get("id")
                yield item

    def _get_trans_abstracts(self, style=None, html=False, tags_to_keep=None, tags_to_remove_with_content=None,
                             tags_to_convert_to_html=None):
        """
        Obtem os resumos em 'trans-abstract'

        Params
        ------
        style : str
            xml -> conteúdo de 'trans-abstract' no formato XML
            inline -> conteúdo de 'trans-abstract' no formato str
            only_p -> conteúdo de 'trans-abstract//p' no formato str
            O formato padrão (style=None) retorna o conteúdo de 'abstract' no formato estruturado (dict):
                {
                    "title": "Abstract",
                    "lang": lang,
                    "sections": [
                        {
                            "title": "",
                            "p": "",
                        },
                        {
                            "title": "",
                            "p": "",
                        },
                    ],
                    "p": "",
                }
        html : bool
            True -> conteúdo de 'trans-abstract' no formato HTML
            False -> conteúdo de 'trans-abstract' no formato indicado por 'style' (padrão)
        tags_to_keep : list
            Lista de 'tags' que serão mantidas no formato HTML, os valores em 'tags_to_keep' serão
            complementados com as seguites 'tags': ['sup', 'sub', 'mml:math', 'math'] (padrão)
        tags_to_remove_with_content : list
            Lista de 'tags' que serão removidas com o respectivo conteúdo no formato HTML,
            os valores em 'tags_to_remove_with_content' serão complementados com as seguites 'tags': ['xref'] (padrão)
        tags_to_convert_to_html : dict
            Dicionário no formato 'tag_xml': 'tag_html' para a conversão de formatos,
            os valores em 'tags_to_convert_to_html' serão complementados com o seguite: {'italic': 'i'} (padrão)

        Returns
        -------
        Gerador de:
            {
                "parent_name": "article",
                "lang": idioma do 'trans-abstract',
                "abstract": resumo no formato indicado
            }
        """
        for trans_abstract in self.xmltree.xpath(".//trans-abstract"):
            item = {}
            item["parent_name"] = "article"
            item["lang"] = trans_abstract.get("{http://www.w3.org/XML/1998/namespace}lang")
            item["abstract"] = self._format_abstract(
                abstract_node=trans_abstract,
                style=style,
                html=html,
                tags_to_keep=tags_to_keep,
                tags_to_remove_with_content=tags_to_remove_with_content,
                tags_to_convert_to_html=tags_to_convert_to_html
            )
            yield item

    def get_abstracts(self, style=None):
        """
        Retorna gerador de resumos
        """
        yield self.get_main_abstract(style=style)
        yield from self._get_trans_abstracts(style=style)
        yield from self._get_sub_article_abstracts(style=style)

    def get_abstracts_by_lang(self, style=None):
        """
        Retorna dicionário cuja chave é idioma e valor o resumo no formato dado por style
        """
        d = {}
        abstracts = self.get_abstracts(style=style)
        if not abstracts:
            return d

        for item in abstracts:
            if isinstance(item, dict) and "lang" in item and "abstract" in item:
                d[item["lang"]] = item["abstract"]
        return d


class AbstractTextNode(BaseTextNode):
    pass


class ArticleAbstract:
    def __init__(self, xmltree, selection=None):
        self._xmltree = xmltree
        self.tags_to_keep = None
        self.tags_to_keep_with_content = None
        self.tags_to_remove_with_content = None
        self.tags_to_convert_to_html = None
        # Define os <abstract> considerados:
        # "standard" considera os resumos que possuem tipo específico
        # "all" considera os resumos independentemente do tipo
        self.selection = selection or "standard"

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

    def _get_structured_abstract(self, node, lang):
        """
        Retorna o resumo estruturado

        Returns
        -------
        dict : {
                'lang': 'en',
                'parent_name': 'article',
                'title': {'html_text': 'Abstract', 'lang': 'en', 'plain_text': 'Abstract'},
                'sections': [
                    {
                        'p': {'html_text': '<b>conteúdo de bold</b> text', 'lang': 'en',
                              'plain_text': 'conteúdo de bold text'},
                        'title': {'html_text': 'inicio', 'lang': 'en', 'plain_text': 'inicio'}
                    },
                    {
                        'p': {'html_text': 'text <b>conteúdo de bold</b> text', 'lang': 'en',
                              'plain_text': 'text conteúdo de bold text'},
                        'title': {'html_text': 'meio', 'lang': 'en', 'plain_text': 'meio'}
                    },
                    {
                        'p': {'html_text': 'text <b>conteúdo de bold</b>', 'lang': 'en',
                              'plain_text': 'text conteúdo de bold'},
                        'title': {'html_text': 'fim', 'lang': 'en', 'plain_text': 'fim'}
                    },
                    {
                        'p': {'html_text': 'text <b>conteúdo <i>de</i> bold</b>', 'lang': 'en',
                              'plain_text': 'text conteúdo de bold'},
                        'title': {'html_text': 'aninhado', 'lang': 'en', 'plain_text': 'aninhado'}
                    }
                ]
            }
        """
        out = dict()

        node_title = node.find("title")

        title = AbstractTextNode(
            node=node_title,
            lang=lang
        )
        title.configure(
            tags_to_keep=self.tags_to_keep,
            tags_to_keep_with_content=self.tags_to_keep_with_content,
            tags_to_remove_with_content=self.tags_to_remove_with_content,
            tags_to_convert_to_html=self.tags_to_convert_to_html
        )
        if title:
            out['title'] = title.item

        out["lang"] = lang

        for n in node.xpath("sec"):
            # node = abstract/sec
            out.setdefault("sections", [])

            title = None
            p = None

            node_title = n.find("title")
            if node_title is not None:
                title = AbstractTextNode(
                    node=node_title,
                    lang=lang
                )
                title.configure(
                    tags_to_keep=self.tags_to_keep,
                    tags_to_keep_with_content=self.tags_to_keep_with_content,
                    tags_to_remove_with_content=self.tags_to_remove_with_content,
                    tags_to_convert_to_html=self.tags_to_convert_to_html
                )

            node_p = n.find("p")
            if node_p is not None:
                p = AbstractTextNode(
                    node=node_p,
                    lang=lang
                )
                p.configure(
                    tags_to_keep=self.tags_to_keep,
                    tags_to_keep_with_content=self.tags_to_keep_with_content,
                    tags_to_remove_with_content=self.tags_to_remove_with_content,
                    tags_to_convert_to_html=self.tags_to_convert_to_html
                )
            if title and p:
                out["sections"].append({"title": title.item, "p": p.item})
        else:
            # abstract/p
            node_p = node.find("p")
            if node_p is not None:
                p = AbstractTextNode(
                    node=node_title,
                    lang=lang
                )
                p.configure(
                    tags_to_keep=self.tags_to_keep,
                    tags_to_keep_with_content=self.tags_to_keep_with_content,
                    tags_to_remove_with_content=self.tags_to_remove_with_content,
                    tags_to_convert_to_html=self.tags_to_convert_to_html
                )
                out["p"] = p
        return out

    def get_main_abstract(self, structured=False):
        """
        Obtem o resumo principal

        Params
        ------
        structured : boolean
            True -> conteúdo de 'abstract' no formato de um dicionário
            False -> conteúdo de 'abstract' (padrão)

        Returns
        -------
        [
            {
                'lang': 'en',
                'parent_name': 'article',
                'title': {'html_text': 'Abstract', 'lang': 'en', 'plain_text': 'Abstract'},
                'sections': [
                    {
                        'p': {'html_text': '<b>conteúdo de bold</b> text', 'lang': 'en', 'plain_text': 'conteúdo de bold text'},
                        'title': {'html_text': 'inicio', 'lang': 'en', 'plain_text': 'inicio'}
                    },
                    {
                        'p': {'html_text': 'text <b>conteúdo de bold</b> text', 'lang': 'en', 'plain_text': 'text conteúdo de bold text'},
                        'title': {'html_text': 'meio', 'lang': 'en', 'plain_text': 'meio'}
                    },
                    {
                        'p': {'html_text': 'text <b>conteúdo de bold</b>', 'lang': 'en', 'plain_text': 'text conteúdo de bold'},
                        'title': {'html_text': 'fim', 'lang': 'en', 'plain_text': 'fim'}
                    },
                    {
                        'p': {'html_text': 'text <b>conteúdo <i>de</i> bold</b>', 'lang': 'en', 'plain_text': 'text conteúdo de bold'},
                        'title': {'html_text': 'aninhado', 'lang': 'en', 'plain_text': 'aninhado'}
                    }
                ]
            }
        ]
        ou
        [
            {
                'lang': 'en',
                'parent_name': 'article',
                'html_text': 'Abstract inicio <b>conteúdo de bold</b> text meio text <b>conteúdo de bold</b> text fim text '
                             '<b>conteúdo de bold</b> aninhado text <b>conteúdo <i>de</i> bold</b>',
                'plain_text': 'Abstract inicio conteúdo de bold text meio text conteúdo de bold text fim text conteúdo de '
                              'bold aninhado text conteúdo de bold'
            }
        ]
        """
        if self.selection == "all":
            xpath = ".//article-meta//abstract"
        else:
            xpath = ".//article-meta//abstract[not (@abstract-type)]"
        try:
            abstract_node = self._xmltree.xpath(xpath)[0]
        except IndexError:
            return
        article = self._xmltree.find(".")
        article_lang = article.get("{http://www.w3.org/XML/1998/namespace}lang")
        abstract_lang = abstract_node.get("{http://www.w3.org/XML/1998/namespace}lang")
        if structured:
            resp = self._get_structured_abstract(
                node=abstract_node,
                lang=abstract_lang or article_lang
            )
        else:
            abstract = AbstractTextNode(
                node=abstract_node,
                lang=abstract_lang or article_lang
            )
            abstract.configure(
                tags_to_keep=self.tags_to_keep,
                tags_to_keep_with_content=self.tags_to_keep_with_content,
                tags_to_remove_with_content=self.tags_to_remove_with_content,
                tags_to_convert_to_html=self.tags_to_convert_to_html
            )

            resp = abstract.item

        resp["parent"] = "article"
        resp["parent_id"] = article.get("id")
        resp["parent_lang"] = article_lang
        resp["parent_article_type"] = article.get("article-type")
        resp["abstract_type"] = abstract_node.get("abstract-type")
        yield resp

    def get_sub_article_abstract(self, structured=False):
        """
        Obtem os resumos nos sub-artigos

        Params
        ------
        structured : boolean
            True -> conteúdo de 'abstract' no formato de um dicionário
            False -> conteúdo de 'abstract' (padrão)

        Returns
        -------
        [
            {
                'lang': 'es',
                'parent_name': 'sub-article',
                'title': {'html_text': 'Abstract', 'lang': 'es', 'plain_text': 'Abstract'},
                'sections': [
                    {
                        'p': {'html_text': '<b>conteúdo de bold</b> text', 'lang': 'es', 'plain_text': 'conteúdo de bold text'},
                        'title': {'html_text': 'inicio', 'lang': 'es', 'plain_text': 'inicio'}
                    },
                    {
                        'p': {'html_text': 'text <b>conteúdo de bold</b> text', 'lang': 'es', 'plain_text': 'text conteúdo de bold text'},
                        'title': {'html_text': 'meio', 'lang': 'es', 'plain_text': 'meio'}
                    },
                    {
                        'p': {'html_text': 'text <b>conteúdo de bold</b>', 'lang': 'es', 'plain_text': 'text conteúdo de bold'},
                        'title': {'html_text': 'fim', 'lang': 'es', 'plain_text': 'fim'}
                    },
                    {
                        'p': {'html_text': 'text <b>conteúdo <i>de</i> bold</b>', 'lang': 'es', 'plain_text': 'text conteúdo de bold'},
                        'title': {'html_text': 'aninhado', 'lang': 'es', 'plain_text': 'aninhado'}
                    }
                ]
            }
        ]
        ou
        [
            {
                'lang': 'es',
                'parent_name': 'sub-article',
                'html_text': 'Abstract inicio <b>conteúdo de bold</b> text meio text <b>conteúdo de bold</b> text fim text '
                             '<b>conteúdo de bold</b> aninhado text <b>conteúdo <i>de</i> bold</b>',
                'plain_text': 'Abstract inicio conteúdo de bold text meio text conteúdo de bold text fim text conteúdo de '
                              'bold aninhado text conteúdo de bold'
            }
        ]
        """

        for sub_article in self._xmltree.xpath(".//sub-article"):
            sub_article_id = sub_article.get('id')
            sub_article_lang = sub_article.get("{http://www.w3.org/XML/1998/namespace}lang")

            if self.selection == "all":
                xpath = ".//front-stub//abstract"
            else:
                xpath = ".//front-stub//abstract[not (@abstract-type)]"
            try:
                abstract_node = self._xmltree.xpath(xpath)[0]
            except IndexError:
                return

            abstract_lang = abstract_node.get("{http://www.w3.org/XML/1998/namespace}lang")
            if structured:
                resp = self._get_structured_abstract(
                    node=abstract_node,
                    lang=sub_article_lang or abstract_lang
                )
            else:
                abstract = AbstractTextNode(
                    node=abstract_node,
                    lang=sub_article_lang or abstract_lang
                )
                abstract.configure(
                    tags_to_keep=self.tags_to_keep,
                    tags_to_keep_with_content=self.tags_to_keep_with_content,
                    tags_to_remove_with_content=self.tags_to_remove_with_content,
                    tags_to_convert_to_html=self.tags_to_convert_to_html
                )

                resp = abstract.item

            resp["parent"] = "sub-article"
            resp["parent_id"] = sub_article_id
            resp["parent_lang"] = sub_article_lang
            resp["parent_article_type"] = sub_article.get("article-type")
            resp["id"] = sub_article_id
            resp["abstract_type"] = abstract_node.get("abstract-type")
            yield resp

    def get_trans_abstract(self, structured=False):
        """
        Obtem os resumos traduzidos

        Params
        ------
        structured : boolean
            True -> conteúdo de 'abstract' no formato de um dicionário
            False -> conteúdo de 'abstract' (padrão)

        Returns
        -------
        [
            {
                'lang': 'pt',
                'parent_name': 'article',
                'title': {'html_text': 'Abstract', 'lang': 'pt', 'plain_text': 'Abstract'},
                'sections': [
                        {
                            'p': {'html_text': '<b>conteúdo de bold</b> text', 'lang': 'pt', 'plain_text': 'conteúdo de bold text'},
                            'title': {'html_text': 'inicio', 'lang': 'pt', 'plain_text': 'inicio'}
                        },
                        {
                            'p': {'html_text': 'text <b>conteúdo de bold</b> text', 'lang': 'pt', 'plain_text': 'text conteúdo de bold text'},
                            'title': {'html_text': 'meio', 'lang': 'pt', 'plain_text': 'meio'}
                        },
                        {
                            'p': {'html_text': 'text <b>conteúdo de bold</b>', 'lang': 'pt', 'plain_text': 'text conteúdo de bold'},
                            'title': {'html_text': 'fim', 'lang': 'pt', 'plain_text': 'fim'}
                        },
                        {
                            'p': {'html_text': 'text <b>conteúdo <i>de</i> bold</b>', 'lang': 'pt', 'plain_text': 'text conteúdo de bold'},
                            'title': {'html_text': 'aninhado', 'lang': 'pt', 'plain_text': 'aninhado'}
                        }
                    ]
            }
        ]
        ou
        [
            {
                'lang': 'pt',
                'parent_name': 'article',
                'html_text': 'Abstract inicio <b>conteúdo de bold</b> text meio text <b>conteúdo de bold</b> text fim text '
                             '<b>conteúdo de bold</b> aninhado text <b>conteúdo <i>de</i> bold</b>',
                'plain_text': 'Abstract inicio conteúdo de bold text meio text conteúdo de bold text fim text conteúdo de '
                              'bold aninhado text conteúdo de bold'
            }
        ]
        """

        article = self._xmltree.find(".")
        article_lang = article.get("{http://www.w3.org/XML/1998/namespace}lang")

        if self.selection == "all":
            xpath = ".//article-meta//trans-abstract"
        else:
            xpath = ".//article-meta//trans-abstract[not (@abstract-type)]"

        for abstract_node in self._xmltree.xpath(xpath):
            abstract_lang = abstract_node.get("{http://www.w3.org/XML/1998/namespace}lang")
            if structured:
                resp = self._get_structured_abstract(
                    node=abstract_node,
                    lang=abstract_lang or article_lang
                )
            else:
                abstract = AbstractTextNode(
                    node=abstract_node,
                    lang=abstract_lang or article_lang
                )
                abstract.configure(
                    tags_to_keep=self.tags_to_keep,
                    tags_to_keep_with_content=self.tags_to_keep_with_content,
                    tags_to_remove_with_content=self.tags_to_remove_with_content,
                    tags_to_convert_to_html=self.tags_to_convert_to_html
                )

                resp = abstract.item
            resp["parent"] = "article"
            resp["parent_id"] = article.get("id")
            resp["parent_lang"] = article_lang
            resp["parent_article_type"] = article.get("article-type")
            resp["abstract_type"] = abstract_node.get("abstract-type")
            yield resp

    def get_abstracts(self, structured=False):
        yield from self.get_main_abstract(structured)
        yield from self.get_sub_article_abstract(structured)
        yield from self.get_trans_abstract(structured)

    def get_abstracts_by_lang(self, structured=False):
        """
        Retorna dicionário indexando os resumos pelo idioma

        Returns
        -------
        dict : {
            'en': {
                'lang': 'en',
                'parent_name': 'article',
                'html_text': 'Abstract inicio <b>conteúdo de bold</b> text meio text <b>conteúdo de bold</b> text fim text '
                             '<b>conteúdo de bold</b> aninhado text <b>conteúdo <i>de</i> bold</b>',
                'plain_text': 'Abstract inicio conteúdo de bold text meio text conteúdo de bold text fim text conteúdo de '
                              'bold aninhado text conteúdo de bold'
            },
            'es': {
                'lang': 'es',
                'id': '01',
                'parent_name': 'sub-article',
                'html_text': 'Abstract inicio <b>conteúdo de bold</b> text meio text <b>conteúdo de bold</b> text fim text '
                             '<b>conteúdo de bold</b> aninhado text <b>conteúdo <i>de</i> bold</b>',
                'plain_text': 'Abstract inicio conteúdo de bold text meio text conteúdo de bold text fim text conteúdo de '
                              'bold aninhado text conteúdo de bold'
            },
            'pt': {
                'lang': 'pt',
                'parent_name': 'article',
                'html_text': 'Abstract inicio <b>conteúdo de bold</b> text meio text <b>conteúdo de bold</b> text fim text '
                             '<b>conteúdo de bold</b> aninhado text <b>conteúdo <i>de</i> bold</b>',
                'plain_text': 'Abstract inicio conteúdo de bold text meio text conteúdo de bold text fim text conteúdo de '
                              'bold aninhado text conteúdo de bold'
            }
        """
        d = {}
        for item in self.get_abstracts(structured):
            d[item["lang"]] = item
        return d


class Highlight(BaseAbstract):
    @property
    def tag_list(self):
        for highlight in self.node.xpath('.//list//item'):
            yield process_subtags(highlight)

    @property
    def data(self):
        return {
            "title": self.title,
            "highlights": list(self.p),
            "list": list(self.tag_list),
            "kwds": list(self.kwds),
            "abstract_type": self.abstract_type
        }


class Highlights:
    def __init__(self, node):
        self.node = node

    @property
    def highlights(self):
        for abstract in self.node.xpath(".//abstract[@abstract-type='key-points'] | .//trans-abstract["
                                        "@abstract-type='key-points']"):
            highlight = Highlight(abstract)
            yield highlight.data


class ArticleHighlights:
    def __init__(self, xmltree):
        self.xmltree = xmltree

    def article_abstracts(self):
        main = self.xmltree.xpath(".")[0]
        main_lang = main.get("{http://www.w3.org/XML/1998/namespace}lang")
        main_article_type = main.get("article-type")
        for node in self.xmltree.xpath(".//article-meta | .//sub-article"):
            parent = "sub-article" if node.tag == "sub-article" else "article"
            parent_id = node.get("id")
            lang = node.get("{http://www.w3.org/XML/1998/namespace}lang") or main_lang
            article_type = node.get("article-type") or main_article_type
            for data in Highlights(node).highlights:
                data.update(
                    {
                        "parent": parent,
                        "parent_id": parent_id,
                        "parent_lang": lang,
                        "parent_article_type": article_type,
                    }
                )
                yield data


class VisualAbstract(BaseAbstract):
    @property
    def fig_id(self):
        fig_node = self.node.find(".//fig")
        if fig_node is not None:
            return fig_node.get("id")

    @property
    def caption(self):
        caption_node = self.node.find(".//caption")
        if caption_node is not None:
            return process_subtags(caption_node)

    @property
    def graphic(self):
        graphic_node = self.node.find('.//graphic', namespaces={'xlink': 'http://www.w3.org/1999/xlink'})
        if graphic_node is not None:
            return graphic_node.get('{http://www.w3.org/1999/xlink}href')

    @property
    def data(self):
        return {
            "title": self.title,
            "fig_id": self.fig_id,
            "caption": self.caption,
            "graphic": self.graphic,
            "kwds": list(self.kwds),
            "abstract_type": self.abstract_type
        }


class VisualAbstracts:
    def __init__(self, node):
        self.node = node

    @property
    def visual_abstracts(self):
        for abstract in self.node.xpath(".//abstract[@abstract-type='graphical'] | .//trans-abstract["
                                        "@abstract-type='graphical']"):
            visual_abstract = VisualAbstract(abstract)
            yield visual_abstract.data


class ArticleVisualAbstracts:
    def __init__(self, xmltree):
        self.xmltree = xmltree

    def article_abstracts(self):
        main = self.xmltree.xpath(".")[0]
        main_lang = main.get("{http://www.w3.org/XML/1998/namespace}lang")
        main_article_type = main.get("article-type")
        for node in self.xmltree.xpath(".//article-meta | .//sub-article"):
            parent = "sub-article" if node.tag == "sub-article" else "article"
            parent_id = node.get("id")
            lang = node.get("{http://www.w3.org/XML/1998/namespace}lang") or main_lang
            article_type = node.get("article-type") or main_article_type
            for data in VisualAbstracts(node).visual_abstracts:
                data.update(
                    {
                        "parent": parent,
                        "parent_id": parent_id,
                        "parent_lang": lang,
                        "parent_article_type": article_type,
                    }
                )
                yield data
