from packtools.sps.models.article_data_availability import DataAvailability
from packtools.sps.validation.exceptions import ValidationDataAvailabilityException


class DataAvailabilityValidation:
    def __init__(self, xmltree, specific_use_list=None):
        self.xmltree = xmltree
        self.data_availability = DataAvailability(self.xmltree)
        self.specific_use_list = specific_use_list

    def validate_data_availability(self, specific_use_list=None):
        """
        Check whether the data availability statement matches the options provided in a standard list.

        XML input
        ---------
        <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article">
            <back>
                <sec sec-type="data-availability" specific-use="data-available-upon-request">
                    <label>Data availability statement</label>
                    <p>Data will be available upon request.</p>
                </sec>
                <fn-group>
                    <fn fn-type="data-availability" specific-use="data-available" id="fn1">
                        <label>Data Availability Statement</label>
                        <p>The data and code used to generate plots and perform statistical analyses have been
                        uploaded to the Open Science Framework archive: <ext-link ext-link-type="uri"
                        xlink:href="https://osf.io/jw6vg/?view_only=0335a15b6db3477f93d0ae636cdf3b4e">https://osf.io/j
                        w6vg/?view_only=0335a15b6db3477f93d0ae636cdf3b4e</ext-link>.</p>
                    </fn>
                </fn-group>
            </back>
        </article>

        Params
        ------
        specific_use_list : list, such as:
            ["data-available", "data-available-upon-request"]

        Returns
        -------
        list of dict
            A list of dictionaries, such as:
            [
                {
                    'title': 'Data availability validation',
                    'xpath': './/back//fn[@fn-type="data-availability"]/@specific-use .//back//sec[@sec-type="data-availability"]/@specific-use',
                    'validation_type': 'value in list',
                    'response': 'OK',
                    'expected_value': ["data-available", "data-available-upon-request"],
                    'got_value': 'data-available-upon-request',
                    'message': 'Got data-available-upon-request expected one item of this list: data-available | data-available-upon-request',
                    'advice': None
                }, ...
            ]
        """
        specific_use_list = specific_use_list or self.specific_use_list
        if not specific_use_list:
            raise ValidationDataAvailabilityException("Function requires a list of specific use.")

        if not self.data_availability.specific_use:
            yield self._create_response(None, specific_use_list)
        else:
            for specific_use in self.data_availability.specific_use:
                yield self._create_response(specific_use, specific_use_list)

    def _create_response(self, specific_use, specific_use_list):
        got_value = specific_use['specific_use'] if specific_use else None
        is_valid = got_value in specific_use_list
        response_status = 'OK' if is_valid else 'ERROR'
        message = f"Got {got_value} expected one item of this list: {' | '.join(specific_use_list)}"
        advice = None if is_valid else f"Provide a data availability statement from the following list: {' | '.join(specific_use_list)}"

        return {
            'title': 'Data availability validation',
            'xpath': './/back//fn[@fn-type="data-availability"]/@specific-use .//back//sec[@sec-type="data-availability"]/@specific-use',
            'validation_type': 'value in list',
            'response': response_status,
            'expected_value': specific_use_list,
            'got_value': got_value,
            'message': message,
            'advice': advice
        }
