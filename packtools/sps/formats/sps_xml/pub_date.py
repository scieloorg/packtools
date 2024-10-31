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
        # (((day?, month?) | season)?, year, era?)
        # year is required
        if not events_dict.get("year"):
            raise ValueError("year is required")
