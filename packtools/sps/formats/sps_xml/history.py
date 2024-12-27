"""
data = [
    {
        "date_type": "received",
        "day": "15",
        "month": "03",
        "year": "2013"
    },
    {
        "date_type": "rev-recd",
        "day": "06",
        "month": "11",
        "year": "2013"
    },
    {
        "date_type": "accepted",
        "day": "12",
        "month": "05",
        "year": "2013"
    },
    {
        "date_type": "preprint",
        "day": "21",
        "month": "09",
        "year": "2012"
    },
]
"""

from lxml import etree as ET


def build_history(data):
    history_elem = ET.Element("history")

    for item in data:
        if not item.get("year"):
            raise ValueError("year is required")

        date_type = item.get("date_type")
        if not date_type:
            raise ValueError("date_type is required")

        date_elem = ET.Element("date", attrib={"date-type": date_type})

        for event in ("day", "month", "season", "year", "era"):
            if (event_text := item.get(event)) is not None:
                date_part_elem = ET.Element(event)
                date_part_elem.text = event_text
                date_elem.append(date_part_elem)
        history_elem.append(date_elem)
    return history_elem
