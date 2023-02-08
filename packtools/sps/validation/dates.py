from datetime import date
import logging

from packtools.sps.models.dates import ArticleDates


def date_dict_to_date(date_dict):
    return date(int(date_dict['year']), int(date_dict['month']), int(date_dict['day']))


class ArticleDatesValidator:
    def __init__(self, xmltree):
        self.history = ArticleDates(xmltree)

    def history_dates_are_complete(self):
        response = []
        for history_date in self.history.history_dates_list:
            date_validated = is_complete(history_date, history_date['type'])
            response.append(date_validated)

        return response

    def dates_are_sorted(self, order, required_events):
        """
        Checks the chronological order of occurrence dates of document publishing events.

        Parameters
        ----------
        order : list
            A list with the order in which events occur.
        required_events : list
            A list with required events.

        Returns
        -------
        dict
            A dictionary that registers the input data, eventual messages, the result and the expected and found orders.

        Examples
        --------
        >>> dates_are_sorted(["received", "rev-request", "rev-recd", "accepted", "approved",],
        ["received", "approved"])

        {
            'input': {
                'order_of_events': ["received", "rev-request", "rev-recd", "accepted", "approved"],
                'required_events': ["received", "approved"]
            },
            'message': ['the event received is required'],
            'result': 'error',
            'expected_order': [date(1998, 3, 14), date(1998, 5, 24), date(1998, 6, 6), date(2012, 6, 1)],
            'found_order': [date(1998, 3, 14), date(1998, 5, 24), date(1998, 6, 6), date(2012, 6, 1)]
        }
        """
        seq = []
        history_dates = self.history.history_dates_dict
        result = {
            'input': {'order_of_events': order, 'required_events': required_events},
            'message': [],
        }
        for event_type in order:
            try:
                seq.append(date_dict_to_date(history_dates[event_type]))
            except KeyError:
                if event_type in required_events:
                    result['message'].append(f'the event {event_type} is required')
                else:
                    pass
        if seq == sorted(seq) and len(seq) == len(order):
            result['result'] = 'ok'
            self.ordered = True
        else:
            result['result'] = 'error'
            self.ordered = False
        result['expected_order'] = sorted(seq)
        result['found_order'] = seq

        return result




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
