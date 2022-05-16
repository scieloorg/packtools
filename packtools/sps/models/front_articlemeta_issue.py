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


class ArticleMetaIssue:

    def __init__(self, xmltree):
        self.xmltree = xmltree

    @property
    def data(self):
        attr_names = (
            "volume", "number", "suppl",
            "elocation", "fpage", "fpage_seq", "lpage",
        )
        _data = {}
        for k in attr_names:
            value = getattr(self, k)
            if value:
                _data[k] = getattr(self, k)
        _data["elocation"] = self.elocation_id
        _data["pub_year"] = self.collection_date["year"]
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
    def number(self):
        # FIXME fazer o parser de issue para extrair number e/ou suppl
        return self.xmltree.findtext(".//front/article-meta/issue")

    @property
    def suppl(self):
        # FIXME verificar a grafia do elemento suppl
        return self.xmltree.findtext(".//front/article-meta/suppl")

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
