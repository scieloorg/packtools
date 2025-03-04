from packtools.sps.models.article_and_subarticles import Fulltext
from packtools.sps.models.article_data_availability import DataAvailability
from packtools.sps.validation.exceptions import ValidationDataAvailabilityException
from packtools.sps.validation.utils import format_response, build_response


class DataAvailabilityValidation:
    def __init__(self, xmltree, params=None):
        self.xmltree = xmltree
        self.data_availability = DataAvailability(self.xmltree)
        self.params = self.get_default_params()
        self.params.update(params or {})
        self.specific_use_list = self.params.get("specific_use_list")

    def get_default_params(self):
        return {
            "specific_use_list": [
                "data-available",
                "data-available-upon-request"
            ],
            "error_level": "ERROR"
        }
    def validate_data_availability(self):
        yield from self.validate_data_availability_exist()
        yield from self.validate_data_availability_mode()

    def validate_data_availability_mode(self):
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
        error_level = self.params.get("error_level", "ERROR")
        specific_use_list = self.specific_use_list

        if not specific_use_list:
            raise ValidationDataAvailabilityException(
                "Function requires a list of specific use."
            )

        items = list(self.data_availability.items)
        valid_values = str(specific_use_list)
        for item in items:
            tag = item.get("tag")
            if tag:
                got_value = item.get("specific_use")
                is_valid = got_value in specific_use_list
                xml = f'<{tag} {tag}-type="data-availability" specific-use="">'
                yield build_response(
                    title="data availability mode",
                    parent=item,
                    item="fn | sec",
                    sub_item="@specific-use",
                    validation_type="value in list",
                    is_valid=is_valid,
                    expected=specific_use_list,
                    obtained=got_value,
                    advice=f'''Complete  specific-use="" in {xml} with valid value: {valid_values}''',
                    data=item,
                    error_level=error_level,
                )

    def validate_data_availability_exist(self):
        error_level = self.params.get("error_level", "ERROR")
        valid_values = str(self.specific_use_list)
        data_availability_demand = self.params.get("article-types")

        for lang, found in self.data_availability.items_by_lang.items():

            if found["parent_id"]:
                xml = f'''<{found["parent"]} id="{found['parent_id']}">'''
            else:
                xml = f'''<{found["parent"]}>'''

            article_type = found["original_article_type"]
            demand = data_availability_demand.get(article_type)
            if demand in ("required", None):
                valid = bool(found.get("tag"))
                expected = found
                advice = (
                    f'''Mark in {xml} the data availability statement in footnote with <fn fn-type="data-availability" specific-use=""> or in text with <sec sec-type="data_availability" specific-use="">. And complete specific-use="" with valid value: {valid_values}'''
                )
            elif demand == "optional":
                valid = True
                expected = found
                advice = None
            elif demand == "unexpected":
                valid = not bool(found.get("tag"))
                expected = None
                tag = found.get("tag")
                advice = (
                    f'''Remove from {xml} the data availability statement (<{tag} {tag}-type="data-availability">) because it is unexpected for {article_type}'''
                )

            yield build_response(
                title="data availability statement",
                parent=found,
                item="fn | sec",
                sub_item="@specific-use",
                validation_type="exist",
                is_valid=valid,
                expected=expected,
                obtained=found,
                advice=advice,
                data=found,
                error_level=error_level,
            )
