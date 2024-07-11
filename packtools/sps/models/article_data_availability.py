"""
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

from packtools.sps.utils.xml_utils import get_parent_context, put_parent_context


class DataAvailability:
    def __init__(self, xmltree):
        self.xmltree = xmltree

    @property
    def specific_use(self):
        for node, lang, article_type, parent, parent_id in get_parent_context(self.xmltree):
            xpath_query = './/*[self::sec[@sec-type="data-availability"] | self::fn[@fn-type="data-availability"]]'
            for item in self.xmltree.xpath(xpath_query):
                response = {
                    'tag': item.tag,
                    'specific_use': item.get('specific-use')
                }
                yield put_parent_context(response, lang, article_type, parent, parent_id)
