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


class Abstract:

    def __init__(self, xmltree):
        self.xmltree = xmltree

    def get_values_dict_without_tags(self, attrib, lang):
        values = []
        try:
            for node in self.xmltree.xpath(f"{attrib}//sec"):
                values.append(node.xpath("./p")[0].text)
        except IndexError:
            pass
        try:
            for node in self.xmltree.xpath(f"{attrib}"):
                values.append(node.xpath("./p")[0].text)
        except IndexError:
            pass
        out = {lang: " ".join(values)}
        return out

    def get_values_dict_with_tags(self, attrib):
        out = dict()
        for node in self.xmltree.xpath(f"{attrib}//sec"):
            out[node.xpath("./title")[0].text] = node.xpath("./p")[0].text

        return out

    @property
    def main_abstract_without_tags(self):
        lang = self.xmltree.find(".").get("{http://www.w3.org/XML/1998/namespace}lang")

        return self.get_values_dict_without_tags('.//front//article-meta//abstract', lang)

    @property
    def main_abstract_with_tags(self):
        try:
            out = {
                'lang': self.xmltree.find(".").get("{http://www.w3.org/XML/1998/namespace}lang"),
                'title': self.xmltree.xpath(".//front//article-meta//abstract//title")[0].text,
                'sections': self.get_values_dict_with_tags('.//front//article-meta//abstract')
            }
            return out

        except (AttributeError, IndexError):
            pass

    @property
    def sub_article_abstract_with_tags(self):
        try:
            out = {
                'lang': self.xmltree.find(".//sub-article").get("{http://www.w3.org/XML/1998/namespace}lang"),
                'title': self.xmltree.xpath(".//sub-article//front-stub//abstract//title")[0].text,
                'sections': self.get_values_dict_with_tags('.//sub-article//front-stub//abstract')
            }
            return out
        except AttributeError:
            pass

    @property
    def sub_article_abstract_without_tags(self):
        try:
            lang = self.xmltree.find(".//sub-article").get("{http://www.w3.org/XML/1998/namespace}lang")

            return self.get_values_dict_without_tags('.//sub-article//front-stub//abstract', lang)
        except AttributeError:
            pass

    @property
    def trans_abstract_with_tags(self):
        try:
            out = {
                'lang': self.xmltree.find(".//trans-abstract").get("{http://www.w3.org/XML/1998/namespace}lang"),
                'title': self.xmltree.xpath(".//front//article-meta//trans-abstract//title")[0].text,
                'sections': self.get_values_dict_with_tags('.//front//article-meta//trans-abstract')
            }
            return out
        except AttributeError:
            pass

    @property
    def trans_abstract_without_tags(self):
        try:
            lang = self.xmltree.find(".//trans-abstract").get("{http://www.w3.org/XML/1998/namespace}lang")

            return self.get_values_dict_without_tags('.//front//article-meta//trans-abstract', lang)
        except AttributeError:
            pass

    @property
    def abstracts_with_tags(self):
        return [self.main_abstract_with_tags, self.trans_abstract_with_tags, self.sub_article_abstract_with_tags]

    @property
    def abstracts_without_tags(self):
        out = self.main_abstract_without_tags
        try:
            out.update(self.trans_abstract_without_tags)
        except TypeError:
            pass
        try:
            out.update(self.sub_article_abstract_without_tags)
        except TypeError:
            pass
        return out
