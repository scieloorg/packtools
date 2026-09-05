from packtools.sps.models.v2.abstract import Abstract


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
