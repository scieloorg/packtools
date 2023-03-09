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
        resp = []
        for license in self.article_license.licenses:
            if f'/{expected_code}/{expected_version}' in license['link']:
                resp.append({
                    "obtained_value": (expected_code, expected_version),
                    "expected_value": (expected_code, expected_version),
                    "result": "ok"
                })
            else:
                resp.append({
                    "obtained_value": (),
                    "expected_value": (expected_code, expected_version),
                    "result": "error",
                    "message": "the license code provided do not match the ones found"
                })
        return resp
