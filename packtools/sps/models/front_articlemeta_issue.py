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
from packtools.sps.models.dates import ArticleDates
from packtools.sps.models.article_ids import ArticleIds


def extract_number_and_supplement_from_issue_element(issue):
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

    splitted = ["spe"
                if "spe" in s.lower() and s.isalpha() else s
                for s in splitted
                ]
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


class ArticleMetaIssue:

    def __init__(self, xmltree):
        self.xmltree = xmltree

    @property
    def data(self):
        attr_names = (
            "volume", "number", "suppl",
            "fpage", "fpage_seq", "lpage",
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
        return self.xmltree.findtext(".//front/article-meta/volume")

    @property
    def issue(self):
        return self.xmltree.findtext(".//front/article-meta/issue")

    @property
    def parsed_issue(self):
        issue = self.issue
        if not issue:
            return {}
        parts = issue.split()
        if len(parts) == 1:
            return {"number": parts[0]}
        if len(parts) == 3:
            return {"number": parts[0], "type_value": parts[-1], "type": parts[1], "type_valid_format": parts[1] in ("spe", "suppl")}
        if len(parts) == 2:
            if parts[0] in ("spe", "suppl"):
                return {"type_value": parts[-1], "type": parts[0], "type_valid_format": parts[0] in ("spe", "suppl")}
            elif parts[1] in ("spe", "suppl"):
                return {"number": parts[0], "type_value": None, "type": parts[1], "type_valid_format": parts[1] in ("spe", "suppl")}
            else:
                return {"type_value": parts[-1], "type": parts[0], "type_valid_format": parts[0] in ("spe", "suppl")}

    @property
    def number(self):
        _issue = self.issue
        if _issue:
            n, s = extract_number_and_supplement_from_issue_element(_issue)
            return n

    @property
    def suppl(self):
        _suppl = self.xmltree.find(".//front/article-meta/supplement")
        if _suppl is not None:
            # valor de supplement pode ser 0 (ou string vazia?)
            return _suppl.text
        _issue = self.issue
        if _issue:
            n, s = extract_number_and_supplement_from_issue_element(_issue)
            return s

    @property
    def elocation_id(self):
        return self.xmltree.findtext(".//front/article-meta/elocation-id")

    @property
    def fpage(self):
        return self.xmltree.findtext(".//front/article-meta/fpage")

    @property
    def fpage_seq(self):
        try:
            return self.xmltree.xpath(".//front/article-meta/fpage")[0].get("seq")
        except IndexError:
            return None

    @property
    def lpage(self):
        return self.xmltree.findtext(".//front/article-meta/lpage")

    @property
    def order(self):
        _order = self.xmltree.findtext('.//article-id[@pub-id-type="other"]')
        if _order is None:
            _order = ArticleIds(self.xmltree).v2
        return int(_order)

    @property
    def order_string_format(self):
        return self.xmltree.findtext('.//article-id[@pub-id-type="other"]')
