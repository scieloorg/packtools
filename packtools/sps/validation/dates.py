from datetime import date
import logging

from packtools.sps.models.dates import ArticleDates


def date_dict_to_date(date_dict):
    return date(int(date_dict['year']), int(date_dict['month']), int(date_dict['day']))


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


def is_complete(dict_date, date_element):
    result = dict(
        input=dict_date,
        result='ok',
        element=date_element
    )
    try:
        object_date = date(int(dict_date['year']), int(dict_date['month']), int(dict_date['day']))
    except KeyError as e:
        result.update(
            result='error',
            message=f'{date_element} must be complete. Provide {e} of the date.',
            element=str(e).replace("'", "")
        )
        return result

    except ValueError as e:
        if 'invalid literal' in str(e):
            result.update(
                result='error',
                message=f'{date_element} must contain valid values, enter valid values for day, month and year',
            )
        else:
            result.update(
                result='error',
                message=f'{date_element} must contain valid values, {e}, enter valid values for day, month and year',
            )
        return result
    else:
        result['object_date'] = object_date
        return result
