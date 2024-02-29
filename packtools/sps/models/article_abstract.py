from packtools.sps.utils import xml_utils
from lxml import etree as ET

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
from packtools.sps.utils.xml_utils import node_text, get_node_without_subtag, convert_xml_to_html


class Abstract:

    def __init__(self, xmltree):
        self.xmltree = xmltree

    def _get_structured_abstract(self, abstract_node, html=False, allowed_tags=None, xml_to_html=None):
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

        out["title"] = abstract_node.findtext("title") if not html else \
            convert_xml_to_html(abstract_node.find("title"), allowed_tags, xml_to_html)
        out["lang"] = abstract_node.get("{http://www.w3.org/XML/1998/namespace}lang")

        for node in abstract_node.xpath("sec"):
            # node = abstract/sec
            out.setdefault("sections", [])

            p = title = None
            node_title = node.find("title")
            if node_title is not None:
                title = get_node_without_subtag(node_title) if not html else \
                    convert_xml_to_html(node_title, allowed_tags, xml_to_html)

            node_p = node.find("p")
            if node_p is not None:
                p = get_node_without_subtag(node_p) if not html else \
                    convert_xml_to_html(node_p, allowed_tags, xml_to_html)

            out["sections"].append({"title": title, "p": p})
        else:
            # abstract/p
            node_p = abstract_node.find("p")
            if node_p is not None:
                out["p"] = get_node_without_subtag(node_p).strip() if not html else \
                    convert_xml_to_html(node_p, allowed_tags, xml_to_html)
        return out

    def _format_abstract(self, abstract_node, style=None, html=False, allowed_tags=None, xml_to_html=None):
        if style == "xml":
            # formato xml
            return node_text(abstract_node)

        if style == "inline":
            # retorna o conteúdo do nó abstract como str
            if html:
                return convert_xml_to_html(abstract_node, allowed_tags, xml_to_html)
            return get_node_without_subtag(abstract_node, remove_extra_spaces=True)

        if style == "only_p":
            # retorna somente o conteúdo dos nós abstract//p como str
            texts = []
            for node_p in abstract_node.xpath(".//p"):
                if html:
                    p_text = convert_xml_to_html(node_p, allowed_tags, xml_to_html)
                else:
                    p_text = get_node_without_subtag(node_p)
                texts.append(p_text.strip())
            return " ".join(texts)

        # retorna abstract em formato de dicionário
        return self._get_structured_abstract(abstract_node, html, allowed_tags, xml_to_html)

    def get_main_abstract(self, style=None, html=False, allowed_tags=None, xml_to_html=None):
        """
        Retorna o resumo principal no formato indicado.
        Formato padrão: inline

        """
        abstract_node = self.xmltree.find(".//article-meta//abstract")
        if abstract_node is not None:
            abstract = self._format_abstract(
                abstract_node=abstract_node,
                style=style,
                html=html,
                allowed_tags=allowed_tags,
                xml_to_html=xml_to_html
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

    def _get_sub_article_abstracts(self, style=None, html=False, allowed_tags=None, xml_to_html=None):
        """
        Retorna gerador de resumos em sub-article
        """
        for sub_article in self.xmltree.xpath(".//sub-article"):
            abstract_node = sub_article.find(".//front-stub//abstract")
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
                    allowed_tags=allowed_tags,
                    xml_to_html=xml_to_html
                )
                if not style:
                    item["abstract"]["lang"] = item["lang"]
                item['id'] = sub_article.get("id")
                yield item

    def _get_trans_abstracts(self, style=None, html=False, allowed_tags=None, xml_to_html=None):
        """
        Retorna gerador de resumos trans-abstract
        """
        for trans_abstract in self.xmltree.xpath(".//trans-abstract"):
            item = {}
            item["parent_name"] = "article"
            item["lang"] = trans_abstract.get("{http://www.w3.org/XML/1998/namespace}lang")
            item["abstract"] = self._format_abstract(
                abstract_node=trans_abstract,
                style=style,
                html=html,
                allowed_tags=allowed_tags,
                xml_to_html=xml_to_html
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
        for item in self.get_abstracts(style=style):
            d[item["lang"]] = item["abstract"]
        return d
