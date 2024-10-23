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

import xml.etree.ElementTree as ET


def build_pub_dates(data):
    for date_type, events_dict in data.items():
        if isinstance(events_dict, dict) and any(events_dict.get(key) for key in ("day", "month", "year", "season")):
            pub_date_elem = ET.Element("pub-date", attrib={"publication-format": "electronic", "date-type": date_type})
            for event, event_text in events_dict.items():
                if event_text:
                    event_elem = ET.Element(event)
                    event_elem.text = event_text
                    pub_date_elem.append(event_elem)
            yield pub_date_elem
