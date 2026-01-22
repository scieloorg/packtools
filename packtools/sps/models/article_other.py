class OtherWithLang:
    """
    Extrai dados de <article-id pub-id-type="other">
    
    Similar a DoiWithLang, mas para o elemento 'other'.
    Usado para validações de publicação contínua (PC) e ordenação.
    
    Example:
        <article-id pub-id-type="other">00123</article-id>
    
    O elemento 'other' é obrigatório para:
    - Periódicos em modalidade de Publicação Contínua (PC)
    - Periódicos em modalidade regular com paginação irregular
    
    O formato deve ser exatamente 5 dígitos numéricos (00001-99999)
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
    def main_other(self):
        """
        Retorna o valor de other do artigo principal.
        
        Returns:
            str or None: Valor do other (ex: "00123") ou None se não existir
        """
        return self._get_node_text('.//front//article-id[@pub-id-type="other"]')
    
    @property
    def main_lang(self):
        """
        Retorna o idioma do artigo principal.
        
        Returns:
            str: Código do idioma (ex: "en", "pt", "es")
        """
        return self._xmltree.find(".").get("{http://www.w3.org/XML/1998/namespace}lang")
    
    @property
    def data(self):
        """
        Retorna lista de dicionários com informações sobre other
        em article e todos os sub-articles.
        
        Returns:
            list of dict: Lista de dicionários contendo:
                - lang: idioma do artigo/sub-article
                - value: valor do other (ex: "00123")
                - parent: 'article' ou 'sub-article'
                - parent_article_type: tipo do artigo
                - parent_id: id do sub-article (se aplicável)
        
        Example:
            [
                {
                    'lang': 'en',
                    'value': '00123',
                    'parent': 'article',
                    'parent_article_type': 'research-article'
                },
                {
                    'lang': 'pt',
                    'value': '00124',
                    'parent': 'sub-article',
                    'parent_article_type': 'translation',
                    'parent_id': 's1'
                }
            ]
        """
        _data = [
            {
                "lang": self.main_lang,
                "value": self.main_other,
                "parent": "article",
                "parent_article_type": self._xmltree.get("article-type"),
            }
        ]
        
        # Captura todos os sub-articles
        for sub_article in self._xmltree.xpath(".//sub-article"):
            lang = sub_article.get("{http://www.w3.org/XML/1998/namespace}lang")
            value = self._get_node_text(
                './/article-id[@pub-id-type="other"]', sub_article
            )
            
            _data.append({
                "lang": lang,
                "value": value,
                "parent": "sub-article",
                "parent_article_type": sub_article.get("article-type"),
                "parent_id": sub_article.get("id"),
            })
        return _data
