from packtools.sps.models.article_license import ArticleLicense


class ArticleLicenseValidation:
    def __init__(self, xmltree):
        self.article_license = ArticleLicense(xmltree)

    def validate_license(self, expected_value):
        obtained_value = self.article_license.licenses_by_lang
        resp = {
            "obtained_value": obtained_value,
            "expected_value": expected_value
        }
        msg = []
        result = 'ok'
        for language, dictonary in obtained_value.items():
            try:
                if expected_value[language] == dictonary:
                    msg.append(f'ok, the license text for {language} does match the license text adopted by the journal')
                else:
                    result = 'error'
                    msg.append(f'error, the license text for {language} does not match the license text adopted by the journal')
            except KeyError:
                    result = 'error'
                    msg.append(f'error, the language {language} is not foreseen by the journal')

        resp.update({
            "result": result,
            "message": msg
        })
        return resp

    def validate_license_code(self, expected_code, expected_version):
        links = self.article_license.licenses
        codes = []
        for code in links:
            finding = code['link'].find(f'/{expected_code}/{expected_version}')
            if finding != -1:
                codes.append((expected_code, expected_version))
        resp = {
                    "obtained_value": codes,
                    "expected_value": (expected_code, expected_version)
        }
        if (expected_code, expected_version) in codes:
            resp.update({
                "result": "ok"
            })
        else:
            resp.update({
                "result": "error",
                "message": "the license code provided do not match the ones found"
            })
        return resp
