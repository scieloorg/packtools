from packtools.sps.models.article_license import ArticleLicense


class ArticleLicenseValidation:
    def __init__(self, xmltree):
        self.article_license = ArticleLicense(xmltree)

    def validate_license(self, expected_value):
        obtained_value = self.article_license.license_p
        resp = {
            "obtained_value": obtained_value,
            "expected_value": expected_value
        }
        if obtained_value == expected_value:
            resp.update({
                "result": "ok"
            })
        else:
            resp.update({
                "result": "error",
                "message": "the license text does not match the license text adopted by the journal"
            })
        return resp

    def validate_license_code(self, expected_value):
        links = self.article_license.link
        codes = []
        for code in links:
            start_code = code['text'].find('/by/') + 4
            end_code = start_code + 3
            codes.append((code['text'][start_code:end_code]))
        resp = {
                    "obtained_value": codes,
                    "expected_value": expected_value
        }
        if codes == expected_value:
            resp.update({
                "result": "ok"
            })
        else:
            resp.update({
                "result": "error",
                "message": "the license codes provided do not match the ones found"
            })
        return resp
