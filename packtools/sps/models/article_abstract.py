from packtools.sps.utils import xml_utils

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


def extract_subtag_text(node, subtag):
    function_tag = (
        xml_utils.node_text_without_xref
        if subtag
        else xml_utils.get_node_without_subtag
    )
    return function_tag(node)


class Abstract:
    def __init__(self, xmltree):
        self.xmltree = xmltree

    def get_values_dict_without_title(self, attrib, lang, subtag):
        values = []
        for node in self.xmltree.xpath(f"{attrib}//sec"):
            values.append(extract_subtag_text(node.xpath("./p")[0], subtag=subtag))
        out = {lang: " ".join(values)}
        return out

    def get_values_dict_with_title(self, attrib, subtag):
        out = dict()
        for node in self.xmltree.xpath(f"{attrib}//sec"):
            out[node.xpath("./title")[0].text] = extract_subtag_text(
                node.xpath("p")[0], subtag=subtag
            )

        return out

    def main_abstract_without_title(self, subtag):
        lang = self.xmltree.find(".").get("{http://www.w3.org/XML/1998/namespace}lang")
        return self.get_values_dict_without_title(
            attrib=".//front//article-meta//abstract", lang=lang, subtag=subtag
        )

    def main_abstract_with_title(self, subtag):
        try:
            out = {
                "lang": self.xmltree.find(".").get(
                    "{http://www.w3.org/XML/1998/namespace}lang"
                ),
                "title": self.xmltree.xpath(".//front//article-meta//abstract//title")[0].text,
                "sections": self.get_values_dict_with_title(
                    attrib=".//front//article-meta//abstract", subtag=subtag
                ),
            }
            return out
        except AttributeError:
            pass

    def sub_article_abstract_with_title(self, subtag):
        try:
            out = {
                "lang": self.xmltree.find(".//sub-article").get(
                    "{http://www.w3.org/XML/1998/namespace}lang"
                ),
                "title": self.xmltree.xpath(
                    ".//sub-article//front-stub//abstract//title"
                )[0].text,
                "sections": self.get_values_dict_with_title(
                    attrib=".//sub-article//front-stub//abstract", subtag=subtag
                ),
            }
            return out
        except AttributeError:
            pass

    def sub_article_abstract_without_title(self, subtag):
        lang = self.xmltree.find(".//sub-article").get(
            "{http://www.w3.org/XML/1998/namespace}lang"
        )

        return self.get_values_dict_without_title(
            attrib=".//sub-article//front-stub//abstract", lang=lang, subtag=subtag
        )

    def trans_abstract_with_title(self, subtag):
        try:
            out = {
                "lang": self.xmltree.find(".//trans-abstract").get(
                    "{http://www.w3.org/XML/1998/namespace}lang"
                ),
                "title": self.xmltree.xpath(
                    ".//front//article-meta//trans-abstract//title")[0].text,
                "sections": self.get_values_dict_with_title(
                    attrib=".//front//article-meta//trans-abstract", subtag=subtag
                ),
            }
            return out
        except AttributeError:
            pass

    def trans_abstract_without_title(self, subtag):
        lang = self.xmltree.find(".//trans-abstract").get(
            "{http://www.w3.org/XML/1998/namespace}lang"
        )

        return self.get_values_dict_without_title(
            attrib=".//front//article-meta//trans-abstract", lang=lang, subtag=subtag
        )

    def abstracts_with_title(self, subtag):
        return [
            self.main_abstract_with_title(subtag=subtag),
            self.trans_abstract_with_title(subtag=subtag),
            self.sub_article_abstract_with_title(subtag=subtag),
        ]

    def abstracts_without_title(self, subtag):
        out = self.main_abstract_without_title(subtag=subtag)
        out.update(self.trans_abstract_without_title(subtag=subtag))
        out.update(self.sub_article_abstract_without_title(subtag=subtag))
        return out
