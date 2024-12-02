"""
data = {
    "pub": {
        "day": "01",
        "month": "01",
        "year": "2024"
    },
    "collection": {
        "season": "Jan-Fev",
        "year": "2024"
    }
}
"""

from lxml import etree as ET


def build_pub_dates(data):
    for date_type, events_dict in data.items():
        # (((day?, month?) | season)?, year, era?)
        # year is required
        if not events_dict.get("year"):
            raise ValueError("year is required")

        pub_date_elem = ET.Element("pub-date", attrib={"publication-format": "electronic", "date-type": date_type})

        for event in ("day", "month", "season", "year", "era"):
            if (event_text := events_dict.get(event)) is not None:
                event_elem = ET.Element(event)
                event_elem.text = event_text
                pub_date_elem.append(event_elem)
        yield pub_date_elem
