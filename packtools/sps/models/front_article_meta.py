
class ArticleId:

    """
    <article-id specific-use="scielo-v3" pub-id-type="publisher-id">P3swRmPHQfy37r9xRbLCw8G</article-id>
    <article-id specific-use="scielo-v2" pub-id-type="publisher-id">S1678-69712003000100108</article-id>
    <article-id specific-use="previous-pid" pub-id-type="publisher-id">S1678-69712002005000108</article-id>
    <article-id pub-id-type="doi">10.1590/1678-69712003/administracao.v4n1p108-123</article-id>
    <article-id pub-id-type="other">123</article-id>
    """

    def __init__(self, xmltree):
        self.xmltree = xmltree
        self.am = self.xmltree.xpath(".//front/article-meta")[0]

    @property
    def v3(self):
        try:
            return self.am.xpath(".//article-id[@specific-use='scielo-v3']")[0].text
        except IndexError:
            return None

    @property
    def v2(self):
        try:
            return self.am.xpath(".//article-id[@specific-use='scielo-v2']")[0].text
        except IndexError:
            return None

    @property
    def aop_pid(self):
        try:
            return self.am.xpath(
                './/article-id[@specific-use="previous-pid" and '
                '@pub-id-type="publisher-id"]')[0].text
        except IndexError:
            return None

    @property
    def other(self):
        try:
            return self.am.xpath('.//article-id[@pub-id-type="other"]')[0].text
        except IndexError:
            return None

    @property
    def doi(self):
        try:
            return self.am.xpath('.//article-id[@pub-id-type="doi"]')[0].text
        except IndexError:
            return None

    @property
    def data(self):
        _data = {}
        if self.v3:
            _data["v3"] = self.v3
        if self.v2:
            _data["v2"] = self.v2
        if self.other:
            _data["other"] = self.other
        if self.doi:
            _data["doi"] = self.doi
        return _data
