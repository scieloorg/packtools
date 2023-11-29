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

    def validate_article_date(self):
        """
        Check whether the article language matches the options provided in a standard list.

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
                        <year>2020</year>
                    </pub-date>
                </article-meta>
            </front>
        </article>

        Params
        ------
        language_codes_list : list

        Returns
        -------
        dict such as:
            {
                'title': 'Article element lang attribute validation',
                'xpath': './article/@xml:lang',
                'validation_type': 'value in list',
                'response': 'OK',
                'expected_value': ['pt', 'en', 'es'],
                'got_value': 'en',
                'message': 'Got en, to research-article whose id is main, expected one item of this list: pt | en | es',
                'advice': 'XML research-article has en as language, to research-article whose id is main, expected one item
                of this list: pt | en | es'
            }
        """
        result = []
        for elem in ['day', 'month', 'year']:
            value = self.article_date[elem]
            expected_number_of_digits = 2 if elem != 'year' else 4
            obtained_number_of_digits = len(value)
            validated_digits = obtained_number_of_digits == expected_number_of_digits
            result.append(
                {
                    'title': 'Article pub-date validation',
                    'xpath': './/front//pub-date/@date-type:pub',
                    'validation_type': 'format (number of digits)',
                    'response': 'OK' if validated_digits else 'ERROR',
                    'expected_value': '{} represented with {} digits'.format(elem, expected_number_of_digits),
                    'got_value': value,
                    'message': 'Got {} expected {} numeric digits'.format(obtained_number_of_digits, expected_number_of_digits),
                    'advice': None if validated_digits else 'Provide a {}-digit numeric value for {}'.format(expected_number_of_digits, elem)
                }
            )

        day, month, year = [self.article_date[elem] for elem in ['day', 'month', 'year']]
        try:
            pub_date = datetime(int(year), int(month), int(day))
            current_date = datetime.now()
            future_date = pub_date.year - current_date.year > 0
            msg = None
            validated = True
        except ValueError as e:
            future_date = False
            msg = str(e)
            validated = False
        if validated:
            advise = None if not future_date else 'The publication date is in the future, consider replacing it with a date in the past'
        else:
            advise = 'Fix the following issue on the given date: {}'.format(msg)

        result.append(
            {
                'title': 'Article pub-date validation',
                'xpath': './/front//pub-date/@date-type:pub',
                'validation_type': 'format (valid date)',
                'response': 'OK' if validated else 'ERROR',
                'expected_value': 'A date in the format: YYYY-MM-DD',
                'got_value': '{}-{}-{}'.format(year, month, day),
                'message': '{}-{}-{} is an {}'.format(year, month, day, 'valid date' if validated else 'invalid date'),
                'advice': advise
            }
        )

        return result


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
