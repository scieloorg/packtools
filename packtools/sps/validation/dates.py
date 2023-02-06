from datetime import date
import logging

from packtools.sps.models.dates import ArticleDates
from packtools.sps.validation.values import CHRONOLOGICAL_ORDER_OF_EVENTS


class ArticleDatesValidator:
    def __init__(self, xmltree):
        self.history = ArticleDates(xmltree)
        self.complete = False
        self.ordered = False

    def dates_are_complete(self):
        for history_date in self.history.history_dates:
            response = is_complete(history_date, history_date['type'])
            if response['result'] == 'error':
                return self.complete
        self.complete = True

        return self.complete

    def dates_are_sorted(self, order=CHRONOLOGICAL_ORDER_OF_EVENTS):
        expected = []
        for event_type in order:
            for history_date in self.history.history_dates:
                if history_date['type'] == event_type:
                    expected.append(date(int(history_date['year']), int(history_date['month']), int(history_date['day'])))
        if expected == sorted(expected):
            self.ordered = True

        return self.ordered


