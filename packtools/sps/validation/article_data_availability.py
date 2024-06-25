from packtools.sps.models.article_data_availability import DataAvailability
from packtools.sps.validation.exceptions import ValidationDataAvailabilityException
from packtools.sps.validation.utils import format_response


class DataAvailabilityValidation:
    def __init__(self, xmltree, specific_use_list=None):
        self.xmltree = xmltree
        self.data_availability = DataAvailability(self.xmltree)
        self.specific_use_list = specific_use_list

    def validate_data_availability(self, specific_use_list=None, error_level="ERROR"):
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

        specific_uses = list(self.data_availability.specific_use)

        if not specific_uses:
            yield format_response(
                title="Data availability validation",
                parent=None,
                parent_id=None,
                parent_article_type=None,
                parent_lang=None,
                item="fn | sec",
                sub_item="@specific-use",
                validation_type="value in list",
                is_valid=False,
                expected=specific_use_list,
                obtained=None,
                advice=f"Provide a data availability statement from the following list: {' | '.join(specific_use_list)}",
                data=None,
                error_level=error_level,
            )
        else:
            for specific_use in specific_uses:
                got_value = specific_use['specific_use']
                is_valid = got_value in specific_use_list
                yield format_response(
                    title="Data availability validation",
                    parent=specific_use.get("parent"),
                    parent_id=specific_use.get("parent_id"),
                    parent_article_type=specific_use.get("parent_article_type"),
                    parent_lang=specific_use.get("parent_lang"),
                    item="fn | sec",
                    sub_item="@specific-use",
                    validation_type="value in list",
                    is_valid=is_valid,
                    expected=specific_use_list,
                    obtained=got_value,
                    advice=f"Provide a data availability statement from the following list: {' | '.join(specific_use_list)}",
                    data=specific_use,
                    error_level=error_level,
                )
