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

from packtools.sps.utils.xml_utils import node_text, node_text_without_tags


class Abstract:
    def __init__(self, xmltree):
        self.xmltree = xmltree

    def _get_inline_abstract_with_lang(self, abstract_xpath, lang):
        """
        Retorna o resumo associado com idioma no formato "linear":
        ```
            {"en": "textos contidos nos elementos sec/p concatenados com um espaço"}
        ```
        O título do resumo, e os títulos das seções são ignorados.
        """
        values = []
        for node in self.xmltree.xpath(f"{abstract_xpath}//sec"):
            values.append(node_text_without_tags(node.find("p")))
        else:
            # não existe abstract/sec, mas existe abstract/p
            node_p = self.xmltree.find(f"{abstract_xpath}/p")
            if node_p is not None:
                values.append(node_text_without_tags(node_p))
        out = {lang: " ".join(values)}
        return out

    def _get_structured_abstract(self, abstract_xpath):
        """
        Retorna um resumo no formato estruturado, cada seção associada com seu título

        ```
        {
            "Título da seção 1": "texto da seção 1, com preservação de elementos de XML",
            "Título da seção 2": "texto da seção 2, com preservação de elementos de XML",
            "Título da seção 3": "texto da seção 3, com preservação de elementos de XML",
        }
        ```

        """
        out = dict()
        for node in self.xmltree.xpath(f"{abstract_xpath}//sec"):
            out[node.xpath("./title")[0].text] = node_text(node.find("p"))
        return out

    def _get_abstract_by_lang(self, abstract_xpath, lang, return_title=True, return_sec_title=True, return_tags=True):
        """
        Retorna resumo selectionado por `abstract_xpath`,
        associado com a chave `lang`,
        incluindo `title`, incluindo `sec_title`, mantendo `tags`, se True.
        """
        abstract = {}

        get_text = node_text if return_tags else node_text_without_tags

        if return_title:
            node_title = self.xmltree.find(f"{abstract_xpath}/title")
            if node_title is not None:
                abstract["title"] = get_text(node_title)

        for node_sec in self.xmltree.xpath(f"{abstract_xpath}/sec"):
            abstract.setdefault("sections", [])
            sec = {}
            # sec/title
            if return_sec_title:
                node_sec_title = node_sec.find("title")
                if node_sec_title is not None:
                    sec["title"] = get_text(node_sec_title)

            # sec/p
            node_sec_p = node_sec.find("p")
            if node_sec_p is not None:
                sec["p"] = get_text(node_sec_p)

            abstract["sections"].append(sec)
        else:
            # no abstract/sec, but abstract/p
            node_p = self.xmltree.find(f"{abstract_xpath}/p")
            if node_p is not None:
                abstract["p"] = get_text(node_p)
        return {lang: abstract}

    def get_main_abstract(self, return_title=True, return_sec_title=True, return_tags=True):
        """
        Retorna resumo principal,
        incluindo `title`, incluindo `sec_title`, mantendo `tags`, se True.

        Returns
        -------
        dict
            {
                "lang": lang,
                "abstract": {
                    "title": "",
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
            }

        """
        lang = self.xmltree.find(".").get("{http://www.w3.org/XML/1998/namespace}lang")
        abstract = self._get_abstract_by_lang(
            abstract_xpath=".//article-meta/abstract",
            lang=lang,
            return_title=return_title,
            return_sec_title=return_sec_title,
            return_tags=return_tags,
        )
        return {
            "lang": self.xmltree.find(".").get("{http://www.w3.org/XML/1998/namespace}lang"),
            "abstract": abstract[lang]
        }

    @property
    def main_abstract_without_tags(self):
        lang = self.xmltree.find(".").get("{http://www.w3.org/XML/1998/namespace}lang")

        return self._get_inline_abstract_with_lang(
            ".//front//article-meta//abstract", lang
        )

    @property
    def main_abstract_with_tags(self):
        try:
            out = {
                "lang": self.xmltree.find(".").get(
                    "{http://www.w3.org/XML/1998/namespace}lang"
                ),
                "title": self.xmltree.xpath(".//front//article-meta//abstract//title")[
                    0
                ].text,
                "sections": self._get_structured_abstract(
                    ".//front//article-meta//abstract"
                ),
            }
            if not out["sections"]:
                # remove sections
                out.pop("sections")
                node_p = self.xmltree.find(".//front//article-meta//abstract/p")
                if node_p is not None:
                    out["p"] = node_text(node_p)

            return out
        except AttributeError:
            pass

    @property
    def sub_article_abstract_with_tags(self):
        try:
            out = {
                "lang": self.xmltree.find(".//sub-article").get(
                    "{http://www.w3.org/XML/1998/namespace}lang"
                ),
                "title": self.xmltree.xpath(
                    ".//sub-article//front-stub//abstract//title"
                )[0].text,
                "sections": self._get_structured_abstract(
                    ".//sub-article//front-stub//abstract"
                ),
            }
            return out
        except AttributeError:
            pass

    @property
    def sub_article_abstract_without_tags(self):
        lang = self.xmltree.find(".//sub-article").get(
            "{http://www.w3.org/XML/1998/namespace}lang"
        )

        return self._get_inline_abstract_with_lang(
            ".//sub-article//front-stub//abstract", lang
        )

    @property
    def trans_abstract_with_tags(self):
        try:
            out = {
                "lang": self.xmltree.find(".//trans-abstract").get(
                    "{http://www.w3.org/XML/1998/namespace}lang"
                ),
                "title": self.xmltree.xpath(
                    ".//front//article-meta//trans-abstract//title"
                )[0].text,
                "sections": self._get_structured_abstract(
                    ".//front//article-meta//trans-abstract"
                ),
            }
            return out
        except AttributeError:
            pass

    @property
    def trans_abstract_without_tags(self):
        lang = self.xmltree.find(".//trans-abstract").get(
            "{http://www.w3.org/XML/1998/namespace}lang"
        )

        return self._get_inline_abstract_with_lang(
            ".//front//article-meta//trans-abstract", lang
        )

    @property
    def abstracts_with_tags(self):
        return [
            self.main_abstract_with_tags,
            self.trans_abstract_with_tags,
            self.sub_article_abstract_with_tags,
        ]

    @property
    def abstracts_without_tags(self):
        out = self.main_abstract_without_tags
        out.update(self.trans_abstract_without_tags)
        out.update(self.sub_article_abstract_without_tags)
        return out
