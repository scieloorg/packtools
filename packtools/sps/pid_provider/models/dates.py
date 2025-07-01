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
        self.year = node.findtext("year")
        self.season = node.findtext("season")
        self.month = node.findtext("month")
        self.day = node.findtext("day")

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
        """
        Data completa, com dia, de publicação do artigo no site.
        """
        return self.epub_date

    @property
    def collection_date(self):
        """
        Data de publicação associada ao fascículo (data editorial).
        """
        # TODO criar collection date para ahead of print a partir da data pub
        for _date in self.pub_dates:
            if _date.get("type") == "collection":
                return _date

    @property
    def pub_dates(self):
        """
        Retorna as datas de publicação pub e collection

        Artigos AOP somente tem data pub ou epub
        Antigamente há casos de XML com somente pub ou somente collection.
        Ou melhor:
        - epub (data completa ou incompleta), representando data do artigo (pub) ou do fascículo (collection)
        - epub-ppub (data incompleta), representando a data do fascículo (collection)

        As classes de packtools.sps.models tem como função retornar
        os dados exatamente conforme está no XML para que as validações possam
        ser confiáveis de indicar ausência / presença de falhas.

        No entanto, este método está fazendo um ajuste, uma compatibilização
        das versão anteriores a SPS 1.8.

        """
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

        if len(_dates) == 1 and not _dates[0]["type"]:
            try:
                for key in ("day", "month", "year"):
                    _dates[0][key]
                _dates[0]["type"] = "pub"
            except KeyError:
                _dates[0]["type"] = "collection"

        return _dates

    @property
    def history_dates_list(self):
        _dates = []
        for node in self.xmltree.xpath(".//history//date"):
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

