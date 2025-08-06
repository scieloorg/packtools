from functools import lru_cache

"""<article>
<front>
    <article-meta>
      <pub-date publication-format="electronic" date-type="pub">
        <day>20</day>
        <month>04</month>
        <year>2022</year>
      </pub-date>
      <pub-date publication-format="electronic" date-type="collection">
        <year>2003</year>
      </pub-date>
      <history>
        <date date-type="received">
          <day>18</day>
          <month>10</month>
          <year>2002</year>
        </date>
        <date date-type="accepted">
          <day>20</day>
          <month>12</month>
          <year>2002</year>
        </date>
      </history>
    </article-meta>
  </front>
</article>
"""


class Date:
    def __init__(self, node):
        self.node = node

    @property
    @lru_cache(maxsize=1)
    def date_type(self):
        # Normaliza tipos legados
        date_type = self.node.get("date-type")
        if date_type:
            return date_type

        if self.node.tag == "pub-date":
            if self.node.findtext("day"):
                return "pub"
            return "collection"

    @property
    @lru_cache(maxsize=1)
    def data(self):
        _d = {
            name: value
            for name in ("year", "month", "season", "day")
            if (value := self.node.findtext(name))
        }
        _d["type"] = self.date_type
        return _d


class ArticleDates:

    def __init__(self, xmltree):
        self.xmltree = xmltree

    @property
    def epub_date(self):
        # não pode ter cache
        return self.article_date

    @property
    def article_date(self):
        # não pode ter cache
        try:
            # XPath direto para pub-date com date-type="pub" ou pub-type="epub"
            nodes = self.xmltree.xpath(
                './/front//pub-date[@date-type="pub" or @pub-type="epub"]'
            )
            return Date(nodes[0]).data
        except IndexError:
            return None
        except Exception:
            return None

    @property
    @lru_cache(maxsize=1)
    def collection_date(self):
        try:
            # XPath direto para pub-date com date-type="collection" ou pub-type="epub-ppub"
            nodes = self.xmltree.xpath(
                './/front//pub-date[@date-type="collection" or @pub-type="epub-ppub"]'
            )
            return Date(nodes[0]).data
        except IndexError:
            return None
        except Exception:
            return None

    @property
    def pub_dates(self):
        dates = []
        if self.article_date:
            dates.append(self.article_date)
        if self.collection_date:
            dates.append(self.collection_date)
        return dates
