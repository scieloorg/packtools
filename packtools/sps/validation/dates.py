from datetime import date
import logging

from packtools.sps.models.dates import ArticleDates
from packtools.sps.validation.values import CHRONOLOGICAL_ORDER_OF_EVENTS


class ArticleDatesValidator:
    def __init__(self, xmltree):
        self.history = ArticleDates(xmltree)
        self.complete = False
        self.ordered = False

