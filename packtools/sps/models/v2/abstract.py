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


class Abstract:
    def __init__(self, node, lang, tags_to_keep, tags_to_keep_with_content, tags_to_remove_with_content, tags_to_convert_to_html
    ):
        self.node = node
        self.lang = lang or node.get("{http://www.w3.org/XML/1998/namespace}lang")
        self.tags_to_keep = tags_to_keep
        self.tags_to_keep_with_content = tags_to_keep_with_content
        self.tags_to_remove_with_content = tags_to_remove_with_content
        self.tags_to_convert_to_html = tags_to_convert_to_html
        
    @property
    def title(self):
        title = BaseTextNode(
            self.node.find("title"), self.lang,
            tags_to_keep=self.tags_to_keep,
            tags_to_keep_with_content=self.tags_to_keep_with_content,
            tags_to_remove_with_content=self.tags_to_remove_with_content,
            tags_to_convert_to_html=self.tags_to_convert_to_html,
        )
        return {
            "html_text": title.html_text,
            "plain_text": title.plain_text,
        }

    @property
    def p(self):
        for p in self.node.xpath('p'):
            text_node = BaseTextNode(
                p, self.lang,
                tags_to_keep=self.tags_to_keep,
                tags_to_keep_with_content=self.tags_to_keep_with_content,
                tags_to_remove_with_content=self.tags_to_remove_with_content,
                tags_to_convert_to_html=self.tags_to_convert_to_html,
            )
            yield text_node.item

    @property
    def sections(self):
        # <sec>
        #     <title>Objetivo</title>
        #     <p>In rhoncus, felis non tempor mattis, nisl purus commodo turpis, nec volutpat leo tortor ac elit. Vestibulum et nisi elit. Maecenas gravida est ac maximus sodales.</p>
        # </sec>
        for item in self.node.xpath("sec"):
            title = BaseTextNode(
                item.find("title"), self.lang,
                tags_to_keep=self.tags_to_keep,
                tags_to_keep_with_content=self.tags_to_keep_with_content,
                tags_to_remove_with_content=self.tags_to_remove_with_content,
                tags_to_convert_to_html=self.tags_to_convert_to_html,
            )
            p = BaseTextNode(
                item.find("p"), self.lang,
                tags_to_keep=self.tags_to_keep,
                tags_to_keep_with_content=self.tags_to_keep_with_content,
                tags_to_remove_with_content=self.tags_to_remove_with_content,
                tags_to_convert_to_html=self.tags_to_convert_to_html,
            )
            yield {"title": title.item, "p": p.item}

    @property
    def list_items(self):
        for item in self.node.xpath('.//list//item'):
            text_node = BaseTextNode(
                item, self.lang,
                tags_to_keep=self.tags_to_keep,
                tags_to_keep_with_content=self.tags_to_keep_with_content,
                tags_to_remove_with_content=self.tags_to_remove_with_content,
                tags_to_convert_to_html=self.tags_to_convert_to_html,
            )
            yield text_node.item

    @property
    def kwds(self):
        parent = self.node.getparent()
        lang = self.lang
        for kwd_group in parent.xpath(f'kwd-group[@xml:lang="{lang}"]'):
            for kwd in kwd_group.xpath("kwd"):
                text_node = BaseTextNode(
                    kwd, lang,
                    tags_to_keep=self.tags_to_keep,
                    tags_to_keep_with_content=self.tags_to_keep_with_content,
                    tags_to_remove_with_content=self.tags_to_remove_with_content,
                    tags_to_convert_to_html=self.tags_to_convert_to_html,
                )
                yield text_node.item
    @property
    def abstract_type(self):
        return self.node.get("abstract-type")

    @property
    def data(self):
        if self.lang:
            xml = f'<{self.node.tag} xml:lang="{self.lang}">'
        else:
            xml = f'<{self.node.tag}>'
        return {
            "xml": xml,
            "tag": self.node.tag,
            "abstract_type": self.abstract_type,
            "lang": self.lang,
            "title": self.title,
            "p": list(self.p),
            "sections": list(self.sections),
            "list_items": list(self.list_items),
            "kwds": list(self.kwds),
        }


class XMLAbstracts:
    def __init__(self, xmltree):
        self.xmltree = xmltree
        self.lang = xmltree.find(".").get("{http://www.w3.org/XML/1998/namespace}lang")
        self.tags_to_keep = None
        self.tags_to_keep_with_content = None
        self.tags_to_remove_with_content = None
        self.tags_to_convert_to_html = None

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

    def get_abstracts(self, abstract_type=None):
        if abstract_type:
            xpath = f'.//abstract[@abstract-type="{abstract_type}"] | .//trans-abstract[@abstract-type="{abstract_type}"]'
        else:
            xpath = ".//abstract[not(@abstract-type)] | .//trans-abstract[not(@abstract-type)]"

        for node in self.xmltree.xpath(xpath):
            abstract = Abstract(
                node,
                self.lang,
                tags_to_keep=self.tags_to_keep,
                tags_to_keep_with_content=self.tags_to_keep_with_content,
                tags_to_remove_with_content=self.tags_to_remove_with_content,
                tags_to_convert_to_html=self.tags_to_convert_to_html,
            )
            yield abstract.data
            
    @property
    def standard_abstracts(self):
        return self.get_abstracts()

    @property
    def visual_abstracts(self):
        return self.get_abstracts("graphical")

    @property
    def key_points_abstracts(self):
        return self.get_abstracts("key-points")

    @property
    def summary_abstracts(self):
        return self.get_abstracts("summary")

    @property
    def abstracts(self):
        yield from self.standard_abstracts
        yield from self.key_points_abstracts
        yield from self.visual_abstracts
        yield from self.summary_abstracts
        
    def abstracts_by_lang_and_type(self):
        langs = {}
        for item in self.abstracts:
            lang = item["lang"]
            abstract_type = item["abstract_type"]
            langs.setdefault(lang, {})
            langs[lang][abstract_type] = item
        return langs
