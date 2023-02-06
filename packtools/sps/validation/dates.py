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

