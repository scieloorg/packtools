class DoiWithLang:
    """
    Torna acessível os dados representados pelos elementos `article-id`
    Permite a atualização ou criação apenas dos `previous-pid` e `scielo-v3`

    <article-id specific-use="scielo-v3" pub-id-type="publisher-id">P3swRmPHQfy37r9xRbLCw8G</article-id>
    <article-id specific-use="scielo-v2" pub-id-type="publisher-id">S1678-69712003000100108</article-id>
    <article-id specific-use="previous-pid" pub-id-type="publisher-id">S1678-69712002005000108</article-id>
    <article-id pub-id-type="doi">10.1590/1678-69712003/administracao.v4n1p108-123</article-id>
    <article-id pub-id-type="other">123</article-id>
    """

    def __init__(self, xmltree):
        self._xmltree = xmltree

    def _get_node(self, xpath, node=None):
        if node is None:
            node = self._xmltree
        try:
            return node.xpath(xpath)[0]
        except IndexError:
            return None

    def _get_node_text(self, xpath, node=None):
        if node is None:
            node = self._xmltree
        try:
            return self._get_node(xpath, node).text
        except AttributeError:
            return None

    @property
    def main_doi(self):
        return self._get_node_text('.//front//article-id[@pub-id-type="doi"]')

    @property
    def main_lang(self):
        return self._xmltree.find(".").get("{http://www.w3.org/XML/1998/namespace}lang")

    @property
    def data(self):
        _data = [
            {
                "lang": self.main_lang,
                "value": self.main_doi,
                "parent": "article",
                "parent_article_type": self._xmltree.get("article-type"),
            }
        ]

        for sub_article in self._xmltree.xpath(
            ".//sub-article[@article-type='translation']"
        ):
            lang = sub_article.get("{http://www.w3.org/XML/1998/namespace}lang")
            value = self._get_node_text(
                './/article-id[@pub-id-type="doi"]', sub_article
            )
            # Obs.: este módulo foi mantido por não haver modificação na resposta
            # houve apenas adição de valores no dicionário que não compromete outras utilizações
            _data.append(
                {
                    "lang": lang,
                    "value": value,
                    "parent": "sub-article",
                    "parent_article_type": "translation",
                    "parent_id": sub_article.get("id"),
                }
            )
        return _data
