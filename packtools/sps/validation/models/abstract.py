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

    def get_abstracts(self, abstract_type=None):
        if abstract_type:
            xpath = f'.//abstract[@abstract-type="{abstract_type}"] | .//trans-abstract[@abstract-type="{abstract_type}"]'
        else:
            xpath = ".//abstract[not(@abstract-type)] | .//trans-abstract[not(@abstract-type)]"

        for node in self.xmltree.xpath(xpath):
            abstract = Abstract(
                node,
                node.get("{http://www.w3.org/XML/1998/namespace}lang") or self.lang,
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
