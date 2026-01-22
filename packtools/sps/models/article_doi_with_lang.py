from packtools.sps.models.article_titles import ArticleTitles
from packtools.sps.models.article_contribs import XMLContribs


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
        self.titles = ArticleTitles(xmltree).article_title_dict
        self.authors = XMLContribs(xmltree).contribs

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
        xml_authors = []
        for author in self.authors:
            try:
                contrib_name = author["contrib_name"]
                fullname = f'{contrib_name["surname"]}, {contrib_name["given-names"]}'
                xml_authors.append(fullname)
            except KeyError:
                pass

        try:
            article_titles = self.titles.get(self.main_lang).get("plain_text")
        except AttributeError:
            article_titles = None

        _data = [
            {
                "lang": self.main_lang,
                "value": self.main_doi,
                "parent": "article",
                "parent_article_type": self._xmltree.get("article-type"),
                "article_title": article_titles,
                "authors": xml_authors,
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

            try:
                article_titles = self.titles.get(lang).get("plain_text")
            except AttributeError:
                article_titles = None

            _data.append(
                {
                    "lang": lang,
                    "value": value,
                    "parent": "sub-article",
                    "parent_article_type": "translation",
                    "parent_id": sub_article.get("id"),
                    "article_title": article_titles,
                    "authors": xml_authors,
                }
            )
        return _data

    @property
    def all_data(self):
        """
        Similar a data(), mas captura TODOS os sub-articles,
        não apenas translations.

        Usado para validações que precisam verificar todos os tipos
        de sub-article (reviewer-report, correction, addendum, etc.)

        Returns:
            list of dict: Lista de dicionários contendo:
                - lang: idioma do artigo/sub-article
                - value: valor do DOI
                - parent: 'article' ou 'sub-article'
                - parent_article_type: tipo do artigo
                - parent_id: id do sub-article (se aplicável)
                - article_title: título do artigo
                - authors: lista de autores
        """
        xml_authors = []
        for author in self.authors:
            try:
                contrib_name = author["contrib_name"]
                fullname = f'{contrib_name["surname"]}, {contrib_name["given-names"]}'
                xml_authors.append(fullname)
            except KeyError:
                pass

        try:
            article_titles = self.titles.get(self.main_lang).get("plain_text")
        except AttributeError:
            article_titles = None

        _data = [
            {
                "lang": self.main_lang,
                "value": self.main_doi,
                "parent": "article",
                "parent_article_type": self._xmltree.get("article-type"),
                "article_title": article_titles,
                "authors": xml_authors,
            }
        ]

        # Captura TODOS os sub-articles, não apenas translations
        for sub_article in self._xmltree.xpath(".//sub-article"):
            lang = sub_article.get("{http://www.w3.org/XML/1998/namespace}lang")
            value = self._get_node_text(
                './/article-id[@pub-id-type="doi"]', sub_article
            )
            article_type = sub_article.get("article-type")

            try:
                article_titles = self.titles.get(lang).get("plain_text")
            except AttributeError:
                article_titles = None

            _data.append(
                {
                    "lang": lang,
                    "value": value,
                    "parent": "sub-article",
                    "parent_article_type": article_type,
                    "parent_id": sub_article.get("id"),
                    "article_title": article_titles,
                    "authors": xml_authors,
                }
            )
        return _data
