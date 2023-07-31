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
from packtools.sps.utils.xml_utils import node_text, get_node_without_subtag


class Abstract:

    def __init__(self, xmltree):
        self.xmltree = xmltree

    def _get_section_titles_and_paragraphs(self, attrib):
        # TODO identificar quem usa este método e eliminar o uso e o método
        # pois não parecer fazer sentido ter como chaves de dicionário o título de seção do resumo 
        # além disso, dict não tem como característica
        # manter os itens ordenados, sendo assim o mais adequado é usar list
        """
        Retorna os títulos pareados com os textos das seções do resumo

        Returns
        -------
        dict : {
            "Título da seção 1": "Parágrafo associado com a seção 1",
            "Título da seção 2": "Parágrafo associado com a seção 2",
            "Título da seção 3": "Parágrafo associado com a seção 3",
        }
        """
        out = dict()
        for node in self.xmltree.xpath(f"{attrib}//sec"):

            node_title = node.find("title")
            if node_title is None:
                continue

            node_p = node.find("p")
            if node_p is None:
                continue

            title = node_text(node_title)
            out[title] = node_text(node_p)

        return out

    def _get_structured_abstract(self, abstract_node):
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

        out["title"] = abstract_node.findtext("title")
        out["lang"] = abstract_node.get("{http://www.w3.org/XML/1998/namespace}lang")

        for node in abstract_node.xpath("sec"):
            # node = abstract/sec
            out.setdefault("sections", [])

            p = title = None
            node_title = node.find("title")
            if node_title is not None:
                title = node_text(node_title)

            node_p = node.find("p")
            if node_p is not None:
                p = node_text(node_p)

            out["sections"].append({"title": title, "p": p})
        else:
            # abstract/p
            node_p = abstract_node.find("p")
            if node_p is not None:
                out["p"] = node_text(node_p).strip()
        return out

    def _format_abstract(self, abstract_node, style=None):
        if style == "xml":
            # formato xml
            return node_text(abstract_node)

        if style == "inline":
            # retorna o conteúdo do nó abstract como str
            return get_node_without_subtag(abstract_node, remove_extra_spaces=True)

        if style == "only_p":
            # retorna somente o conteúdo dos nós abstract//p como str
            texts = []
            for node_p in abstract_node.xpath(".//p"):
                p_text = get_node_without_subtag(node_p)
                texts.append(p_text.strip())
            return " ".join(texts)

        # retorna abstract em formato de dicionário
        return self._get_structured_abstract(abstract_node)

    def get_main_abstract(self, style=None):
        """
        Retorna o resumo principal no formato indicado.
        Formato padrão: inline

        """
        lang = self.xmltree.find(".").get("{http://www.w3.org/XML/1998/namespace}lang")
        abstract = self._format_abstract(
            abstract_node=self.xmltree.find(".//abstract"),
            style=style,
        )
        if not style:
            abstract["lang"] = lang
        return {
            "lang": lang,
            "abstract": abstract,
        }

    @property
    def main_abstract_without_tags(self):
        # TODO adaptar o código usuário deste método para no lugar deste
        # usar get_main_abstract(style="only_p")
        # pois com este nome parece que retorna o resumo principal
        # sem "tags", ou seja, todos os textos conteúdo de todos os elementos (title, p, sec, etc),
        # mas o que faz é retornar um dicionário cuja chave é o idioma
        # do resumo principal e o valor é o conteúdo concatenados somente dos elementos p
        lang = self.xmltree.find(".").get("{http://www.w3.org/XML/1998/namespace}lang")

        p_text = self._format_abstract(
            abstract_node=self.xmltree.find(".//abstract"),
            style="only_p"
        )
        return {lang: p_text}

    @property
    def main_abstract_with_tags(self):
        # TODO adaptar o código usuário deste método para no lugar deste
        # usar get_main_abstract(style=None)
        # pois com este nome parece que retorna o resumo principal com "tags",
        # ou seja, parece que retorna o próprio xml do abstract,
        # mas o que faz é retornar um dicionário cuja chave é o idioma
        # do resumo principal e o valor é o resumo estruturado em dicionário
        try:
            out = {
                'lang': self.xmltree.find(".").get("{http://www.w3.org/XML/1998/namespace}lang"),
                'title': self.xmltree.xpath(".//front//article-meta//abstract//title")[0].text,
                'sections': self._get_section_titles_and_paragraphs('.//front//article-meta//abstract')
            }
            return out

        except (AttributeError, IndexError):
            pass

    def _get_sub_article_abstracts(self, style=None):
        """
        Retorna gerador de resumos em sub-article
        """
        for sub_article in self.xmltree.xpath(".//sub-article"):
            item = {}
            item["lang"] = sub_article.get("{http://www.w3.org/XML/1998/namespace}lang")
            item["abstract"] = self._format_abstract(
                abstract_node=sub_article.find(".//front-stub//abstract"),
                style=style
            )
            if not style:
                item["abstract"]["lang"] = item["lang"]
            yield item

    @property
    def _sub_article_abstract_with_tags(self):
        # TODO adaptar o código usuário deste método para no lugar deste
        # usar _get_sub_article_abstracts(style=None)
        # pois com este nome parece que retorna os resumos com "tags",
        # ou seja, parece que retorna o próprio xml do abstract,
        # mas o que faz é retornar um dicionário representando o resumo em
        # formato estruturado
        # além disso, este código não considera que sub-article ocorra mais de 1 vez
        try:
            out = {
                'lang': self.xmltree.find(".//sub-article").get("{http://www.w3.org/XML/1998/namespace}lang"),
                'title': self.xmltree.xpath(".//sub-article//front-stub//abstract//title")[0].text,
                'sections': self._get_section_titles_and_paragraphs('.//sub-article//front-stub//abstract')
            }
            return out
        except AttributeError:
            pass

    def _get_trans_abstracts(self, style=None):
        """
        Retorna gerador de resumos trans-abstract
        """
        for trans_abstract in self.xmltree.xpath(".//trans-abstract"):
            item = {}
            item["lang"] = trans_abstract.get("{http://www.w3.org/XML/1998/namespace}lang")
            item["abstract"] = self._format_abstract(
                abstract_node=trans_abstract,
                style=style
            )
            yield item

    @property
    def _trans_abstract_with_tags(self):
        # TODO adaptar o código usuário deste método para no lugar deste
        # usar _get_trans_abstracts(style=None)
        # pois com este nome parece que retorna os resumos com "tags",
        # ou seja, parece que retorna o próprio xml do abstract,
        # mas o que faz é retornar um dicionário representando o resumo em
        # formato estruturado
        # além disso, este código não considera que trans-abstract ocorra mais de 1 vez
        try:
            out = {
                'lang': self.xmltree.find(".//trans-abstract").get("{http://www.w3.org/XML/1998/namespace}lang"),
                'title': self.xmltree.xpath(".//front//article-meta//trans-abstract//title")[0].text,
                'sections': self._get_section_titles_and_paragraphs('.//front//article-meta//trans-abstract')
            }
            return out
        except AttributeError:
            pass

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
        for item in self.get_abstracts(style=style):
            d[item["lang"]] = item["abstract"]
        return d

    @property
    def abstracts_with_tags(self):
        # TODO adaptar o código usuário deste método para no lugar deste
        # usar get_abstracts(style=None)
        # pois com este nome parece que retorna os resumos com "tags",
        # ou seja, parece que retorna o próprio xml do abstract,
        # mas o que faz é retornar um dicionário representando o resumo em
        # formato estruturado
        return [self.main_abstract_with_tags, self._trans_abstract_with_tags, self._sub_article_abstract_with_tags]

    @property
    def abstracts_without_tags(self):
        return self.get_abstracts_by_lang(style="only_p")
