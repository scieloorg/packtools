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
    def data(self):
        _date = {}
        for name in ("year", "month", "season", "day"):
            value = self.node.findtext(name)
            if value:
                _date[name] = value
        return _date


class ArticleDates:

    def __init__(self, xmltree):
        self.xmltree = xmltree

    @property
    def epub_date(self):
        for _date in self.pub_dates:
            if _date.get("type") == "pub":
                return _date

    @property
    def article_date(self):
        return self.epub_date

    @property
    def collection_date(self):
        for _date in self.pub_dates:
            if _date.get("type") == "collection":
                return _date

    @property
    def pub_dates(self):
        _dates = []
        for node in self.xmltree.xpath(".//front//pub-date"):
            type = node.get("date-type")
            if not type:
                # handle legacy attribute
                type = node.get("pub-type")
                if type == "epub":
                    type = "pub"
                elif type == "epub-ppub":
                    type = "collection"
            _date = Date(node)
            data = _date.data
            data["type"] = type
            _dates.append(data)
        return _dates

    @property
    def history_dates_list(self):
        _dates = []
        for node in self.xmltree.xpath(".//front//history//date"):
            type = node.get("date-type")
            _date = Date(node)
            data = _date.data
            data["type"] = type
            _dates.append(data)
        return _dates

    @property
    def history_dates_dict(self):
        _dates = {}
        for event_date in self.history_dates_list:
            _dates[event_date['type']] = event_date
        return _dates

