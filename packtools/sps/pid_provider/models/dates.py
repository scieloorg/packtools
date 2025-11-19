from datetime import date
from functools import lru_cache, cached_property

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
class XMLWithPreArticlePublicationDateError(Exception):
    ...


@lru_cache(maxsize=200)
def format_date(year=None, month=None, day=None, **kwargs) -> str:
    """
    Formata uma data de artigo para o formato YYYY-MM-DD.
    
    Args:
        year: Ano como string ou int
        month: Mês como string ou int
        day: Dia como string ou int
        
    Returns:
        String formatada no padrão YYYY-MM-DD
        
    Raises:
        XMLWithPreArticlePublicationDateError: Se a data for inválida
    """
    try:
        # Valida a data criando um objeto date
        d = date(int(year), int(month), int(day))
        
        # Retorna a string formatada
        return f"{year}-{str(month).zfill(2)}-{str(day).zfill(2)}"
        
    except (ValueError, TypeError) as e:
        raise XMLWithPreArticlePublicationDateError(
            f"Unable to format_date "
            f"year={year}, month={month}, day={day}: {type(e).__name__}: {e}"
        )


class Date:
    def __init__(self, node):
        self.node = node

    @cached_property
    def date_type(self):
        # Normaliza tipos legados
        date_type = self.node.get("date-type")
        if date_type:
            return date_type

        if self.node.tag == "pub-date":
            if self.node.findtext("day"):
                return "pub"
            return "collection"

    @cached_property
    def data(self):
        _d = {
            name: value
            for name in ("year", "month", "season", "day")
            if (value := self.node.findtext(name))
        }
        _d["type"] = self.date_type
        return _d

    @cached_property
    def isoformat(self):
        return format_date(**self.data)


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
                './/front//pub-date[@date-type="pub" or @pub-type="epub" or @pub-type="epub-ppub"]'
            )
            return Date(nodes[0]).data
        except IndexError:
            return None
        except Exception:
            return None

    @property
    def article_date_isoformat(self):
        return format_date(**self.article_date)

    @property
    def article_year(self):
        try:
            return self.article_date["year"]
        except (TypeError, KeyError):
            return None

    @cached_property
    def collection_year(self):
        try:
            return self.collection_date["year"]
        except (TypeError, KeyError):
            return None

    @cached_property
    def collection_date(self):
        try:
            # XPath direto para pub-date com date-type="collection" ou pub-type="epub-ppub"
            nodes = self.xmltree.xpath(
                ".//front//pub-date[@date-type='collection' or @pub-type='epub-ppub' or @pub-type='collection']"
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
