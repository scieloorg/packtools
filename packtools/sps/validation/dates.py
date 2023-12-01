from datetime import datetime, date
import logging

from packtools.sps.models.dates import ArticleDates


def date_dict_to_date(date_dict):
    return date(int(date_dict['year']), int(date_dict['month']), int(date_dict['day']))


class ArticleDatesValidation:
    def __init__(self, xmltree):
        self.history = ArticleDates(xmltree)
        self.article_date = ArticleDates(xmltree).article_date

    def history_dates_are_complete(self):
        response = []
        for history_date in self.history.history_dates_list:
            date_validated = is_complete(history_date, history_date['type'])
            response.append(date_validated)

        return response

    def history_dates_are_sorted(self, order, required_events):
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
                'required_events': ["received", "approved"],
                'events_date': [
                {'rev-request': date(1998, 3, 14)},
                {'rev-recd': date(1998, 5, 24)},
                {'accepted': date(1998, 6, 6)},
                {'approved': date(2012, 6, 1)}
                ]
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
            'input': {
                'order_of_events': order,
                'required_events': required_events,
                'events_date': history_dates
            },
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
        else:
            result['result'] = 'error'
        result['expected_order'] = sorted(seq)
        result['found_order'] = seq

        return result

    def validate_number_of_digits_in_article_date(self):
        """
        Checks whether date components have the correct number of digits.

        XML input
        ---------
        <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink"
        article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
            <front>
                <article-meta>
                    <article-id pub-id-type="publisher-id" specific-use="scielo-v3">TPg77CCrGj4wcbLCh9vG8bS</article-id>
                    <article-id pub-id-type="publisher-id" specific-use="scielo-v2">S0104-11692020000100303</article-id>
                    <article-id pub-id-type="doi">10.1590/1518-8345.2927.3231</article-id>
                    <article-id pub-id-type="other">00303</article-id>
                    <pub-date date-type="pub" publication-format="electronic">
                        <day>03</day>
                        <month>02</month>
                        <year>2024</year>
                    </pub-date>
                </article-meta>
            </front>
        </article>

        Returns
        -------
        list of dict such as:
            [
                {
                    'title': 'Article pub-date day validation',
                    'xpath': './/front//pub-date[@date-type="pub"]/day',
                    'validation_type': 'format',
                    'response': 'OK',
                    'expected_value': '03',
                    'got_value': '03',
                    'message': 'Got 2 expected 2 numeric digits',
                    'advice': None
                },...
            ]
        """
        result = []
        for elem, expected in zip(('day', 'month', 'year'), (2, 2, 4)):
            value = self.article_date[elem]
            obtained = len(value)
            validated = obtained == expected
            if value.isdigit():
                expected_value = value.zfill(expected)
                message = 'Got {} expected {} numeric digits'.format(obtained, expected)
            else:
                expected_value = 'A numeric digit for {} represented with {} digits'.format(elem, expected)
                message = 'Got a non-numeric value for {}'.format(elem)
                validated = False
            result.append(
                {
                    'title': 'Article pub-date {} validation'.format(elem),
                    'xpath': './/front//pub-date[@date-type="pub"]/{}'.format(elem),
                    'validation_type': 'format',
                    'response': 'OK' if validated else 'ERROR',
                    'expected_value': expected_value,
                    'got_value': value,
                    'message': message,
                    'advice': None if validated else 'Provide a {}-digit numeric value for {}'.format(expected, elem)
                }
            )
        return result

    def validate_article_date(self, future_date):
        """
        Checks if the publication date is valid and before a deadline.

        XML input
        ---------
        <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink"
        article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
            <front>
                <article-meta>
                    <article-id pub-id-type="publisher-id" specific-use="scielo-v3">TPg77CCrGj4wcbLCh9vG8bS</article-id>
                    <article-id pub-id-type="publisher-id" specific-use="scielo-v2">S0104-11692020000100303</article-id>
                    <article-id pub-id-type="doi">10.1590/1518-8345.2927.3231</article-id>
                    <article-id pub-id-type="other">00303</article-id>
                    <pub-date date-type="pub" publication-format="electronic">
                        <day>01</day>
                        <month>01</month>
                        <year>2023</year>
                    </pub-date>
                </article-meta>
            </front>
        </article>

        Params
        ------
        future_date : str

        Returns
        -------
        dict such as:
            {
                'title': 'Article pub-date validation',
                'xpath': './/front//pub-date[@date-type="pub"]',
                'validation_type': 'value',
                'response': 'OK',
                'expected_value': 'A date in the format: YYYY-MM-DD less than 2023-12-12',
                'got_value': '2023-01-01',
                'message': '2023-01-01 is an valid date',
                'advice': None
            }
        """

        got_value = '-'.join([self.article_date[elem] for elem in ['year', 'month', 'day']])
        try:
            pub_date = date_dict_to_date(self.article_date)
            validated = got_value <= future_date
            advice = None if validated else 'The publication date must be a date before or equal to {}'.format(future_date)
        except ValueError as e:
            validated = False
            advice = f'Fix the following issue on the given date: {e}'

        return {
            'title': 'Article pub-date validation',
            'xpath': './/front//pub-date[@date-type="pub"]',
            'validation_type': 'value',
            'response': 'OK' if validated else 'ERROR',
            'expected_value': 'A date in the format: YYYY-MM-DD before or equal to {}'.format(future_date),
            'got_value': got_value,
            'message': '{} is an {}'.format(got_value, 'valid date' if validated else 'invalid date'),
            'advice': advice
        }

    def validate(self, data):
        """
        Função que executa as validações da classe ArticleDatesValidation.

        Returns:
            dict: Um dicionário contendo os resultados das validações realizadas.
        
        """              
        dates_req_order_events_results = {
                'article_dates_required_order_events_validation': self.history_dates_are_sorted(
                data['history_dates_required_order'], 
                data['required_events'])
            }
        dates_are_complete_results = { 
            'article_dates_are_complete_validation': self.history_dates_are_complete()
            }
        dates_req_order_events_results.update(dates_are_complete_results)
        return dates_req_order_events_results


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
