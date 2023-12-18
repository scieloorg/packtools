import unittest
from lxml import etree

from packtools.sps.validation.article_data_availability import DataAvailabilityValidation


class DataAvailabilityTest(unittest.TestCase):

    def test_validate_data_availability_with_sec_with_fn_ok(self):
        self.maxDiff = None
        xml = """
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
            """
        xmltree = etree.fromstring(xml)
        expected = [
            {
                'title': 'Data availability validation',
                'xpath': './back//fn[@fn-type="data-availability"]/@specific-use ./back//sec[@sec-type="data-availability"]/@specific-use',
                'validation_type': 'exist, value in list',
                'response': 'OK',
                'expected_value': ["data-available", "data-available-upon-request"],
                'got_value': 'data-available-upon-request',
                'message': 'Got data-available-upon-request expected one item of this list: data-available | data-available-upon-request',
                'advice': None
            },
            {
                'title': 'Data availability validation',
                'xpath': './back//fn[@fn-type="data-availability"]/@specific-use ./back//sec[@sec-type="data-availability"]/@specific-use',
                'validation_type': 'exist, value in list',
                'response': 'OK',
                'expected_value': ["data-available", "data-available-upon-request"],
                'got_value': 'data-available',
                'message': 'Got data-available expected one item of this list: data-available | data-available-upon-request',
                'advice': None
            }
        ]
        obtained = DataAvailabilityValidation(xmltree).validate_data_availability(
            ["data-available", "data-available-upon-request"]
        )
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

    def test_validate_data_availability_with_sec_with_fn_not_ok(self):
        self.maxDiff = None
        xml = """
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
            """
        xmltree = etree.fromstring(xml)
        expected = [
            {
                'title': 'Data availability validation',
                'xpath': './back//fn[@fn-type="data-availability"]/@specific-use ./back//sec[@sec-type="data-availability"]/@specific-use',
                'validation_type': 'exist, value in list',
                'response': 'ERROR',
                'expected_value': ["data-not-available", "uninformed"],
                'got_value': 'data-available-upon-request',
                'message': 'Got data-available-upon-request expected one item of this list: data-not-available | uninformed',
                'advice': 'Provide a data availability statement from the following list: data-not-available | uninformed'
            },
            {
                'title': 'Data availability validation',
                'xpath': './back//fn[@fn-type="data-availability"]/@specific-use ./back//sec[@sec-type="data-availability"]/@specific-use',
                'validation_type': 'exist, value in list',
                'response': 'ERROR',
                'expected_value': ["data-not-available", "uninformed"],
                'got_value': 'data-available',
                'message': 'Got data-available expected one item of this list: data-not-available | uninformed',
                'advice': 'Provide a data availability statement from the following list: data-not-available | uninformed'
            }
        ]
        obtained = DataAvailabilityValidation(xmltree).validate_data_availability(
            ["data-not-available", "uninformed"]
        )
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

    def test_validate_data_availability_with_sec_without_fn_ok(self):
        self.maxDiff = None
        xml = """
                <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article">
                    <back>
                        <sec sec-type="data-availability" specific-use="data-available-upon-request">
                            <label>Data availability statement</label>
                            <p>Data will be available upon request.</p>
                        </sec>
                    </back>
                </article>
            """
        xmltree = etree.fromstring(xml)
        expected = [
            {
                'title': 'Data availability validation',
                'xpath': './back//fn[@fn-type="data-availability"]/@specific-use ./back//sec[@sec-type="data-availability"]/@specific-use',
                'validation_type': 'exist, value in list',
                'response': 'OK',
                'expected_value': ["data-available", "data-available-upon-request"],
                'got_value': 'data-available-upon-request',
                'message': 'Got data-available-upon-request expected one item of this list: data-available | data-available-upon-request',
                'advice': None
            }
        ]
        obtained = DataAvailabilityValidation(xmltree).validate_data_availability(
            ["data-available", "data-available-upon-request"]
        )
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

    def test_validate_data_availability_without_sec_with_fn_ok(self):
        self.maxDiff = None
        xml = """
                <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article">
                    <back>
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
            """
        xmltree = etree.fromstring(xml)
        expected = [
            {
                'title': 'Data availability validation',
                'xpath': './back//fn[@fn-type="data-availability"]/@specific-use ./back//sec[@sec-type="data-availability"]/@specific-use',
                'validation_type': 'exist, value in list',
                'response': 'OK',
                'expected_value': ["data-available", "data-available-upon-request"],
                'got_value': 'data-available',
                'message': 'Got data-available expected one item of this list: data-available | data-available-upon-request',
                'advice': None
            }
        ]
        obtained = DataAvailabilityValidation(xmltree).validate_data_availability(
            ["data-available", "data-available-upon-request"]
        )
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

    def test_validate_data_availability_without_sec_without_fn_ok(self):
        self.maxDiff = None
        xml = """
                <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article">
                    <back>
                    </back>
                </article>
            """
        xmltree = etree.fromstring(xml)
        expected = []
        obtained = DataAvailabilityValidation(xmltree).validate_data_availability(
            ["data-available", "data-available-upon-request"]
        )
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)


if __name__ == '__main__':
    unittest.main()
