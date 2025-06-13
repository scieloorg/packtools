from lxml import etree


class ArticleIds:

    """
    Torna acessível os dados representados pelos elementos `article-id`
    Permite a atualização ou criação apenas dos `previous-pid` e `scielo-v3`

    <article-id>S1678-69712003000100108</article-id>
    <article-id specific-use="scielo-v3" pub-id-type="publisher-id">P3swRmPHQfy37r9xRbLCw8G</article-id>
    <article-id specific-use="scielo-v2" pub-id-type="publisher-id">S1678-69712003000100108</article-id>
    <article-id specific-use="previous-pid" pub-id-type="publisher-id">S1678-69712002005000108</article-id>
    <article-id pub-id-type="doi">10.1590/1678-69712003/administracao.v4n1p108-123</article-id>
    <article-id pub-id-type="other">123</article-id>
    """

    def __init__(self, xmltree):
        self._xmltree = xmltree

    @property
    def am(self):
        return self._xmltree.xpath(".//front/article-meta")[0]

    @property
    def v3(self):
        return self._get_node_text(".//article-id[@specific-use='scielo-v3']")

    @property
    def v2(self):
        return self._get_node_text(".//article-id[@specific-use='scielo-v2']")

    @property
    def aop_pid(self):
        return self._get_node_text(
            './/article-id[@specific-use="previous-pid" and '
            '@pub-id-type="publisher-id"]'
        )

    @property
    def other(self):
        return self._get_node_text('.//article-id[@pub-id-type="other"]')

    @property
    def doi(self):
        return self._get_node_text('.//article-id[@pub-id-type="doi"]')

    @property
    def data(self):
        _data = {}
        if self.v3:
            _data["v3"] = self.v3
        if self.v2:
            _data["v2"] = self.v2
        if self.aop_pid:
            _data["aop_pid"] = self.aop_pid
        if self.other:
            _data["other"] = self.other
        if self.doi:
            _data["doi"] = self.doi
        return _data

    @v2.setter
    def v2(self, value):
        value = value and value.strip()
        if not value or len(value) != 23:
            raise ValueError(
                "can't set attribute ArticleIds.v2. "
                "Expected value must have 23 characters. Got: %s" % value
            )
        try:
            node = self.am.xpath('.//article-id[@specific-use="scielo-v2"]')[0]
        except IndexError:
            node = None
        if node is None:
            node = etree.Element("article-id")
            node.set("pub-id-type", "publisher-id")
            node.set("specific-use", "scielo-v2")
            self.am.insert(1, node)
        node.text = value

    @v3.setter
    def v3(self, value):
        value = value and value.strip()
        if not value or len(value) != 23:
            raise ValueError(
                "can't set attribute ArticleIds.v3. "
                "Expected value must have 23 characters. Got: %s" % value
            )
        try:
            node = self.am.xpath('.//article-id[@specific-use="scielo-v3"]')[0]
        except IndexError:
            node = None

        if node is None:
            node = etree.Element("article-id")
            node.set("pub-id-type", "publisher-id")
            node.set("specific-use", "scielo-v3")
            self.am.insert(1, node)
        if node is not None:
            node.text = value

    @aop_pid.setter
    def aop_pid(self, value):
        value = value and value.strip()
        if not value or len(value) != 23:
            raise ValueError(
                "can't set attribute ArticleIds.aop_pid. "
                "Expected value must have 23 characters. Got: %s" % value
            )
        try:
            node = self.am.xpath(
                './/article-id[@specific-use="previous-pid" and '
                '@pub-id-type="publisher-id"]'
            )[0]
        except IndexError:
            node = None

        if node is None:
            node = etree.Element("article-id")
            node.set("pub-id-type", "publisher-id")
            node.set("specific-use", "previous-pid")
            self.am.insert(1, node)
        if node is not None:
            node.text = value

    def _get_node(self, xpath):
        try:
            return self.am.xpath(xpath)[0]
        except IndexError:
            return None

    def _get_node_text(self, xpath):
        try:
            return self._get_node(xpath).text
        except AttributeError:
            return None
