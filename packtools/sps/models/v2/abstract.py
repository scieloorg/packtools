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
        if parent is None:
            return
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
    def fig_id(self):
        """
        Extracts figure ID from visual abstract.
        Used for graphical abstracts with <fig> element.
        """
        fig_node = self.node.find(".//fig")
        if fig_node is not None:
            return fig_node.get("id")
        return None

    @property
    def caption(self):
        """
        Extracts caption from visual abstract.
        Returns the text content of <caption> element.
        """
        caption_node = self.node.find(".//caption")
        if caption_node is not None:
            caption_text = BaseTextNode(
                caption_node, self.lang,
                tags_to_keep=self.tags_to_keep,
                tags_to_keep_with_content=self.tags_to_keep_with_content,
                tags_to_remove_with_content=self.tags_to_remove_with_content,
                tags_to_convert_to_html=self.tags_to_convert_to_html,
            )
            return caption_text.item
        return None

    @property
    def graphic_href(self):
        """
        Extracts graphic element from visual abstract.
        Returns the xlink:href attribute value of <graphic> element.

        In JATS/SPS XML, <graphic> is a JATS element without namespace,
        but the href attribute uses the xlink namespace.

        Example XML:
            <abstract abstract-type="graphical">
                <p>
                    <fig id="vs1">
                        <graphic xlink:href="1234-5678-va-01.jpg"/>
                    </fig>
                </p>
            </abstract>

        Returns:
            str: The xlink:href attribute value (e.g., "1234-5678-va-01.jpg")
            None: If no <graphic> element is found

        Note:
            This implementation is consistent with JATS/SPS schema where:
            - <graphic> element has no namespace (it's a JATS element)
            - xlink:href attribute DOES have the xlink namespace

            DO NOT use find() with namespaces parameter as it's not officially
            supported by lxml and will be ignored silently.
        """
        # Find <graphic> element (no namespace needed for JATS elements)
        graphic_node = self.node.find('.//graphic')

        if graphic_node is not None:
            # Extract xlink:href attribute (namespace IS needed for xlink attributes)
            return graphic_node.get('{http://www.w3.org/1999/xlink}href')

        return None

    @property
    def abstract_type(self):
        return self.node.get("abstract-type")

    @property
    def text(self):
        """
        Returns the concatenated text content of the abstract.
        - With sections: concatenates title and p from each section
        - Without sections but with p: concatenates p elements
        - Without sections or p (non-SPS-compliant legacy XML, e.g. some
          migrated articles): falls back to the node's raw text, excluding
          the title
        """
        text_parts = []

        # Check if abstract has sections by querying the node directly
        if self.node.xpath("sec"):
            # With sections: include title and p from each section
            for section in self.sections:
                if section.get("title") and section["title"].get("plain_text"):
                    text_parts.append(section["title"]["plain_text"])
                if section.get("p") and section["p"].get("plain_text"):
                    text_parts.append(section["p"]["plain_text"])
        else:
            p_items = list(self.p)
            if p_items:
                # Without sections: include only p elements
                for p_item in p_items:
                    if p_item.get("plain_text"):
                        text_parts.append(p_item["plain_text"])
            else:
                # Legacy/non-SPS-compliant abstracts: text sits directly
                # under <abstract>/<trans-abstract>, not wrapped in <p>/<sec>
                raw_text = self._raw_text_excluding_title
                if raw_text:
                    text_parts.append(raw_text)

        return " ".join(text_parts)

    @property
    def _raw_text_excluding_title(self):
        full_text = " ".join(t.strip() for t in self.node.itertext() if t.strip())
        title_node = self.node.find("title")
        if title_node is not None:
            title_text = " ".join(
                t.strip() for t in title_node.itertext() if t.strip()
            )
            if title_text and full_text.startswith(title_text):
                full_text = full_text[len(title_text):].strip()
        return full_text

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
            "text": self.text,
            "graphic_href": self.graphic_href,  # For visual abstracts
            "fig_id": self.fig_id,    # For visual abstracts
            "caption": self.caption,  # For visual abstracts
        }


class XMLAbstracts:
    """
    Collects the <abstract>/<trans-abstract> elements of an article, in the
    main article and in every <sub-article>, as plain data (no validation
    rule or expected-value logic lives here).

    PR #1180 (2026-05) had moved this class into
    packtools.sps.validation.models.abstract on the premise that it was
    used only by validation code; that premise was wrong (scms-upload's
    TOC builder consumes it directly for presentation data, not
    validation), so it moved back here. See issues #1153/#1181.
    """

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

    def _build_abstract(self, node, lang):
        abstract = Abstract(
            node,
            lang,
            tags_to_keep=self.tags_to_keep,
            tags_to_keep_with_content=self.tags_to_keep_with_content,
            tags_to_remove_with_content=self.tags_to_remove_with_content,
            tags_to_convert_to_html=self.tags_to_convert_to_html,
        )
        return abstract.data

    def get_abstracts(self, abstract_type=None):
        type_filter = f'[@abstract-type="{abstract_type}"]' if abstract_type else "[not(@abstract-type)]"

        # Abstracts do artigo principal: exclui qualquer coisa dentro de
        # sub-article (traduções), para nunca misturar os dois casos.
        main_xpath = (
            f".//abstract{type_filter}[not(ancestor::sub-article)] | "
            f".//trans-abstract{type_filter}[not(ancestor::sub-article)]"
        )
        for node in self.xmltree.xpath(main_xpath):
            lang = node.get("{http://www.w3.org/XML/1998/namespace}lang") or self.lang
            yield self._build_abstract(node, lang)

        # Abstracts de sub-article: o lang vem do próprio nó, com fallback
        # para o xml:lang do sub-article que o contém. Nunca cai para o
        # lang do artigo principal, já que um sub-article representa outro
        # idioma.
        sub_xpath = (
            f".//sub-article//abstract{type_filter} | "
            f".//sub-article//trans-abstract{type_filter}"
        )
        for node in self.xmltree.xpath(sub_xpath):
            sub_article = node.xpath("ancestor::sub-article[1]")
            sub_lang = (
                sub_article[0].get("{http://www.w3.org/XML/1998/namespace}lang")
                if sub_article else None
            )
            lang = node.get("{http://www.w3.org/XML/1998/namespace}lang") or sub_lang
            yield self._build_abstract(node, lang)

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
