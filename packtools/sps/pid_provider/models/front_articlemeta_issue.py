"""<article>
<front>
    <article-meta>
      <pub-date publication-format="electronic" date-type="collection">
        <year>2003</year>
      </pub-date>
      <volume>4</volume>
      <issue>1</issue>
      <fpage>108</fpage>
      <lpage>123</lpage>
    </article-meta>
  </front>
</article>
"""

"""<article>
<front>
    <article-meta>
      <pub-date publication-format="electronic" date-type="collection">
        <year>2003</year>
      </pub-date>
      <volume>4</volume>
      <issue>1</issue>
      <fpage>108</fpage>
      <lpage>123</lpage>
    </article-meta>
  </front>
</article>
"""
from packtools.sps.pid_provider.models.dates import ArticleDates
from packtools.sps.pid_provider.models.article_ids import ArticleIds


def _extract_number_and_supplment_from_issue_element(issue):
    """
    Extrai do conteúdo de <issue>xxxx</issue>, os valores number e suppl.
    Valores possíveis
    5 (suppl), 5 Suppl, 5 Suppl 1, 5 spe, 5 suppl, 5 suppl 1, 5 suppl. 1,
    25 Suppl 1, 2-5 suppl 1, 2spe, Spe, Supl. 1, Suppl, Suppl 12,
    s2, spe, spe 1, spe pr, spe2, spe.2, spepr, supp 1, supp5 1, suppl,
    suppl 1, suppl 5 pr, suppl 12, suppl 1-2, suppl. 1
    """
    if not issue:
        return None, None
    issue = issue.strip().replace(".", "")
    splitted = [s for s in issue.split() if s]

    splitted = ["spe" if "spe" in s.lower() and s.isalpha() else s for s in splitted]
    if len(splitted) == 1:
        issue = splitted[0]
        if issue.isdigit():
            return issue, None
        if "sup" in issue.lower():
            # match como sup*
            return None, "0"
        if issue.startswith("s"):
            if issue[1:].isdigit():
                return None, issue[1:]
        # match com spe, 2-5, 3B
        return issue, None

    if len(splitted) == 2:
        if "sup" in splitted[0].lower():
            return None, splitted[1]
        if "sup" in splitted[1].lower():
            return splitted[0], "0"
        # match spe 4 -> spe4
        return "".join(splitted), None

    if len(splitted) == 3:
        if "sup" in splitted[1].lower():
            return splitted[0], splitted[2]
    # match ????
    return "".join(splitted), None


def zero_to_none(value):
    """
    Normaliza valores de campos numéricos de paginação e volume/número,
    removendo zeros não significativos.

    Usado para: volume, number, fpage, lpage

    Args:
        value: Valor a ser normalizado (string ou None)

    Returns:
        String normalizada ou None se o valor for vazio ou zero
    """
    if not value:
        return None

    try:
        if int(value) == 0:
            return None
        return value
    except (TypeError, ValueError):
        # Valor não é numérico, retorna como está
        return value


class ArticleMetaIssue:

    def __init__(self, xmltree):
        self.xmltree = xmltree

    @property
    def data(self):
        attr_names = (
            "volume",
            "number",
            "suppl",
            "fpage",
            "fpage_seq",
            "lpage",
            "elocation_id",
        )
        _data = {}
        for k in attr_names:
            try:
                value = getattr(self, k)
            except AttributeError:
                continue
            else:
                if value:
                    _data[k] = value
        try:
            _data["pub_year"] = self.collection_date["year"]
        except (KeyError, TypeError):
            pass
        return _data

    @property
    def collection_date(self):
        _date = ArticleDates(self.xmltree)
        return _date.collection_date

    @property
    def volume(self):
        volume = self.xmltree.findtext(".//front/article-meta/volume")
        return zero_to_none(volume)

    @property
    def issue(self):
        return self.xmltree.findtext(".//front/article-meta/issue")

    @property
    def number(self):
        _issue = self.issue
        if _issue:
            n, s = _extract_number_and_supplment_from_issue_element(_issue)
            return zero_to_none(n)

    @property
    def suppl(self):
        _suppl = self.xmltree.find(".//front/article-meta/supplement")
        if _suppl is not None:
            # valor de supplement pode ser 0 (ou string vazia?)
            return _suppl.text
        _issue = self.issue
        if _issue:
            n, s = _extract_number_and_supplment_from_issue_element(_issue)
            return s

    @property
    def elocation_id(self):
        return self.xmltree.findtext(".//front/article-meta/elocation-id")

    @property
    def fpage(self):
        fpage = self.xmltree.findtext(".//front/article-meta/fpage")
        return zero_to_none(fpage)

    @property
    def fpage_seq(self):
        try:
            return self.xmltree.xpath(".//front/article-meta/fpage")[0].get("seq")
        except IndexError:
            return None

    @property
    def lpage(self):
        lpage = self.xmltree.findtext(".//front/article-meta/lpage")
        return zero_to_none(lpage)

    @property
    def order(self):
        """
        Obtém o order do artigo, primeiro tentando article-id[@pub-id-type="other"],
        depois usando os últimos 5 dígitos do pid v2 como fallback.

        Returns:
            int: Order do artigo ou 0 se não for possível obter um valor válido
        """
        _order = self.xmltree.findtext('.//article-id[@pub-id-type="other"]')

        if not _order:
            # Fallback: usa os últimos 5 dígitos do pid v2
            _order = ArticleIds(self.xmltree).v2
            if _order:
                _order = _order[-5:]

        return int(_order or 0)
