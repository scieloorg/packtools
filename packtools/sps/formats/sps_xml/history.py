"""
data = {
    "received": {
        "day": "15",
        "month": "03",
        "year": "2013"
    },
    "rev-recd": {
        "day": "06",
        "month": "11",
        "year": "2013"
    },
    "accepted": {
        "day": "12",
        "month": "05",
        "year": "2013"
    },
    "preprint": {
        "day": "21",
        "month": "09",
        "year": "2012"
    },
}
"""

import xml.etree.ElementTree as ET


def build_history(data):
    history_elem = ET.Element("history")

    for event, date in data.items():
        if isinstance(date, dict) and any(date.get(key) for key in ("day", "month", "year")):
            date_elem = ET.Element("date", attrib={"date-type": event})
            for date_part, value in date.items():
                if value:
                    date_part_elem = ET.Element(date_part)
                    date_part_elem.text = value
                    date_elem.append(date_part_elem)
            history_elem.append(date_elem)
    return history_elem
