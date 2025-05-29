from datetime import date

from packtools.sps.models.article_and_subarticles import Fulltext


class Date:
    """Represents and processes a single date from an XML node.

    This class handles the extraction and structuring of date information from XML nodes,
    supporting year, month, day and season data.

    Attributes:
        node: XML node containing date information
        year: Year value extracted from node
        season: Season value extracted from node
        month: Month value extracted from node
        day: Day value extracted from node

    Example:
        date_node = article.find('.//pub-date')
        date = Date(date_node)
        date_dict = date.data
    """

    def __init__(self, node):
        """Initialize a Date instance with an XML node.

        Args:
            node: XML node containing date elements (year, month, day, season)
        """
        self.node = node
        self.year = node.findtext("year")
        self.season = node.findtext("season")
        self.month = node.findtext("month")
        self.day = node.findtext("day")
        self.type = node.get("date-type")
        if not self.type:
            if node.get("pub-type") == "epub":
                self.type = "pub"
            else:
                self.type = "collection"

    @property
    def data(self):
        """Get date information as a dictionary.

        Returns a dictionary containing available date components (year, month, season, day).
        Only components that exist in the source XML are included.

        Returns:
            dict: Date information with available components

        Example:
            {'year': '2024', 'month': '01', 'day': '15'}
        """
        _date = {}
        for name in ("year", "month", "season", "day"):
            value = self.node.findtext(name)
            if value:
                _date[name] = value
        _date["type"] = self.type
        _date["display"] = self.display
        _date["is_complete"] = bool(self.date)
        _date["parts"] = self.parts
        return _date

    def __str__(self):
        return self.display or str(
            {"year": self.year, "month": self.month, "day": self.day}
        )

    @property
    def parts(self):
        return {
            "year": self.year,
            "season": self.season,
            "month": self.month,
            "day": self.day,
        }

    @property
    def display(self):
        if self.season:
            return "/".join([item for item in (self.season, self.year) if item])

        try:
            date(int(self.year), int(self.month or 1), int(self.day or 1))
        except (ValueError, TypeError):
            return None

        parts = []
        if self.year and len(self.year) == 4:
            parts.append(self.year)
            if self.month:
                parts.append(self.month.zfill(2))
                if self.day:
                    parts.append(self.day.zfill(2))
        return "-".join(parts)

    @property
    def date(self):
        try:
            return date(int(self.year), int(self.month), int(self.day))
        except (ValueError, TypeError):
            return None


class XMLDates:
    """High-level interface to access article dates.

    Provides a convenient interface to access all date information from an article
    through delegation to FulltextDates.

    Attributes:
        xmltree: XML tree containing the article
        main_dates: FulltextDates instance for the main article
    """

    def __init__(self, xmltree):
        """Initialize an ArticleDates instance.

        Args:
            xmltree: XML tree containing the article to process
        """
        self.xmltree = xmltree
        self.main_dates = FulltextDates(xmltree.find("."))

    def __getattr__(self, name):
        """Delegate attribute access to main_dates.

        Provides access to FulltextDates attributes through ArticleDates.
        Raises AttributeError if the attribute doesn't exist.

        Args:
            name: Name of the attribute to access

        Returns:
            The requested attribute from main_dates

        Raises:
            AttributeError: If the attribute doesn't exist in ArticleDates or FulltextDates
        """
        if hasattr(self.main_dates, name):
            return getattr(self.main_dates, name)
        raise AttributeError(
            f"ArticleDates.{name} or FulltextDates.{name} does not exist"
        )

    @property
    def fulltext_dates(self):
        yield self.main_dates
        for sub_article_node in self.xmltree.xpath(".//sub-article"):
            yield FulltextDates(sub_article_node)


class ArticleDates(XMLDates): ...


class FulltextDates(Fulltext):
    """Processes and provides access to all date-related data from articles and sub-articles.

    This class handles extraction and organization of dates from SPS XML documents,
    maintaining hierarchy and relationships between different date types.

    Attributes:
        fulltext_node: Root XML node for date extraction
    """

    @property
    def main_data(self):
        data = {}
        data["parent"] = self.attribs_parent_prefixed
        data["pub"] = self.epub_date
        data["article_date"] = self.article_date
        data["collection_date"] = self.collection_date
        data["history_dates"] = self.history_dates_list
        data["events_ordered_by_date"] = self.ordered_events
        data["history_dates_by_event"] = self.history_dates_dict
        data.update(self.history_dates_dict)
        return data

    @property
    def related_articles(self):
        """
        <related-article
            ext-link-type="doi"
            id="A01"
            related-article-type="commentary-article"
            xlink:href="10.1590/0101-3173.2022.v45n1.p139"
        >Referência do artigo comentado: FREITAS, J. H. de. Cinismo e indiferenciación: la huella de Glucksmann en <italic>El coraje de la verdad</italic> de Foucault. <bold>Trans/form/ação</bold>: revista de Filosofia da Unesp, v. 45, n. 1, p. 139-158, 2022.</related-article>
        """
        for node in self.node.xpath(
            "front//related-article | front-stub//related-article | body//related-article | back//related-article"
        ):
            yield {
                "related-article-type": node.get("related-article-type"),
                "xlink_href": node.get("{http://www.w3.org/1999/xlink}href"),
                "ext-link-type": node.get("ext-link-type"),
            }

    @property
    def data(self):
        data = {}
        data.update(self.main_data)
        data["translations"] = {}
        for item in self.translations:
            data["translations"][item.lang] = item.data
        data["not_translations"] = {}
        for item in self.not_translations:
            data["not_translations"][item.id] = item.data
        return data

    @property
    def translations(self):
        for node in super().translations:
            yield FulltextDates(node)

    @property
    def not_translations(self):
        for node in super().not_translations:
            yield FulltextDates(node)

    @property
    def items(self):
        """Get date information in a flattened structure.

        Yields date information for the main document and all related documents
        (translations and not_translations) in a flat structure, simplifying data processing.

        Yields:
            dict: Flattened date information for each document part

        Example:
            for item in dates.items:
                print(f"Document ID: {item['parent']['parent_id']}")
                print(f"Pub date: {item['pub']}")
        """
        yield self.main_data

        for item in self.translations:
            yield from item.items

        for item in self.not_translations:
            yield from item.items

    @property
    def epub_date_model(self):
        if not hasattr(self, "_epub_date_model"):
            try:
                node = self.front.xpath(
                    ".//pub-date[@date-type='pub'] | .//pub-date[@pub-type='epub']"
                )[0]
            except (IndexError, AttributeError):
                self._epub_date_model = None
            else:
                self._epub_date_model = Date(node)
        return self._epub_date_model

    @property
    def epub_date(self):
        try:
            return self.epub_date_model.data
        except AttributeError:
            return None

    @property
    def article_date(self):
        return self.epub_date

    @property
    def collection_date_model(self):
        if not hasattr(self, "_collection_model"):
            try:
                node = self.front.xpath(
                    ".//pub-date[@date-type='collection'] | .//pub-date[@pub-type='epub-ppub']"
                )[0]
            except (IndexError, AttributeError):
                self._collection_model = None
            else:
                self._collection_model = Date(node)
        return self._collection_model

    @property
    def collection_date(self):
        try:
            return self.collection_date_model.data
        except AttributeError:
            return None

    @property
    def pub_dates(self):
        _dates = []
        if self.collection_date:
            _dates.append(self.collection_date)
        if self.epub_date:
            _dates.append(self.epub_date)
        return _dates

    @property
    def history_dates(self):
        try:
            for node in self.front.xpath(".//history//date"):
                yield Date(node).data
        except AttributeError:
            return

    @property
    def history_dates_list(self):
        """Get article history dates as a list.

        Extracts all history dates (received, accepted, etc.) from the document,
        adding type and parent information to each date.

        Returns:
            list: List of history dates with type and parent information

        Example:
            [
                {'year': '2023', 'month': '12', 'type': 'received', 'parent': {...}},
                {'year': '2024', 'month': '01', 'type': 'accepted', 'parent': {...}}
            ]
        """
        return [item for item in self.history_dates]

    @property
    def history_dates_dict(self):
        """Get article history dates as a dictionary.

        Converts the history dates list into a dictionary keyed by date type,
        providing easier access to specific history dates.

        Returns:
            dict: History dates indexed by date type

        Example:
            {
                'received': {'year': '2023', 'month': '12', ...},
                'accepted': {'year': '2024', 'month': '01', ...}
            }
        """
        _dates = {}
        for event_date in self.history_dates_list:
            _dates[event_date["type"]] = event_date
        return _dates

    @property
    def ordered_events(self):
        obtained_events = [
            (k, item["display"]) for k, item in self.history_dates_dict.items()
        ]
        # ordena a lista de eventos de forma cronológica
        return [tp for tp in sorted(obtained_events, key=lambda x: x[1])]

    @property
    def date_types_ordered_by_date(self):
        # obtem uma lista com os nomes dos eventos ordenados
        return [event[0] for event in self.ordered_events]
