from packtools.sps.models.article_license import ArticleLicense

from packtools.sps.validation.exceptions import (
    ValidationLicenseException,
    ValidationLicenseCodeException
)


class ArticleLicenseValidation:
    def __init__(self,
                 xmltree,
                 tags_to_keep=None,
                 tags_to_keep_with_content=None,
                 tags_to_remove_with_content=None,
                 tags_to_convert_to_html=None
                 ):
        self.article_license = ArticleLicense(
            xmltree,
            tags_to_keep=tags_to_keep,
            tags_to_keep_with_content=tags_to_keep_with_content,
            tags_to_remove_with_content=tags_to_remove_with_content,
            tags_to_convert_to_html=tags_to_convert_to_html
        )

    def validate_license(self, expected_value):
        """
        Checks whether the license data complies with the standard specified by the journal.

        XML input
        ---------
        <article xmlns:xlink="http://www.w3.org/1999/xlink">
            <front>
            <article-meta>
                <permissions>
                    <license license-type="open-access"
                    xlink:href="http://creativecommons.org/licenses/by/4.0/"
                    xml:lang="en">
                        <license-p>This is an article published in open access under a Creative Commons license.</license-p>
                    </license>
                    <license license-type="open-access"
                    xlink:href="http://creativecommons.org/licenses/by/4.0/"
                    xml:lang="pt">
                        <license-p>Este é um artigo publicado em acesso aberto sob uma licença Creative Commons.</license-p>
                    </license>
                    <license license-type="open-access"
                    xlink:href="http://creativecommons.org/licenses/by/4.0/"
                    xml:lang="es">
                        <license-p>Este es un artículo publicado en acceso abierto bajo una licencia Creative Commons.</license-p>
                    </license>
                </permissions>
            </article-meta>
            </front>
        </article>

        Params
        ------
        expected_value : dict, such as:
            {
                'en': {
                    'lang': 'en',
                    'link': 'http://creativecommons.org/licenses/by/4.0/',
                    'license_p': 'This is an article published in open access under a Creative Commons license.'
                },
                'pt': {
                    'lang': 'pt',
                    'link': 'http://creativecommons.org/licenses/by/4.0/',
                    'license_p': 'Este é um artigo publicado em acesso aberto sob uma licença Creative Commons.'
                },
                'es': {
                    'lang': 'es',
                    'link': 'http://creativecommons.org/licenses/by/4.0/',
                    'license_p': 'Este es un artículo publicado en acceso abierto bajo una licencia Creative Commons.'
                }
            }

        Returns
        -------
        list of dict
            A list of dictionaries, such as:
            [
                {
                    'title': 'Article license validation',
                    'xpath': './permissions//license',
                    'validation_type': 'value in list',
                    'response': 'OK',
                    'expected_value': {
                        'lang': 'en',
                        'link': 'http://creativecommons.org/licenses/by/4.0/',
                        'license_p': 'This is an article published in open access under a Creative Commons license.'
                        },
                    'got_value': {
                        'lang': 'en',
                        'link': 'http://creativecommons.org/licenses/by/4.0/',
                        'license_p': 'This is an article published in open access under a Creative Commons license.'
                        },
                    'message': "Got {"
                               "'lang': 'en', "
                               "'link': 'http://creativecommons.org/licenses/by/4.0/', "
                               "'license_p': 'This is an article published in open access under a Creative Commons license.'"
                               "}, expected: {"
                               "'lang': 'en', "
                               "'link': 'http://creativecommons.org/licenses/by/4.0/', "
                               "'license_p': 'This is an article published in open access under a Creative Commons license.'"
                               "}",
                    'advice': None
                },
                ...
            ]
        """
        if not expected_value:
            raise ValidationLicenseException("Provide a dictionary with license data for validation")

        obtained_value = self.article_license.licenses_by_lang

        for lang, data in obtained_value.items():
            obtained_license_p = {
                'lang': data.get('lang'),
                'link': data.get('link'),
                'license_p': data.get('license_p').get('plain_text')
            }
            is_valid = expected_value.get(lang) == obtained_license_p
            expected_value_msg = expected_value.get(
                lang) if is_valid else 'License data that matches the language {}'.format(lang)
            yield {
                'title': 'Article license validation',
                'xpath': './permissions//license',
                'validation_type': 'value',
                'response': 'OK' if is_valid else 'ERROR',
                'expected_value': expected_value_msg,
                'got_value': obtained_license_p,
                'message': f'Got {obtained_license_p}, expected: {expected_value_msg}',
                'advice': None if is_valid else 'Provide license data that is consistent with the language: {} and '
                                                'standard adopted by the journal'.format(lang)
            }

    def validate_license_code(self, expected_code):
        """
        Checks whether the license code complies with the values in code_list.

        XML input
        ---------
        <article xmlns:xlink="http://www.w3.org/1999/xlink">
            <front>
                <article-meta>
                    <permissions>
                        <license license-type="open-access"
                        xlink:href="http://creativecommons.org/licenses/by/4.0/"
                        xml:lang="en">
                            <license-p>This is an article published in open access under a Creative Commons license.</license-p>
                        </license>
                        <license license-type="open-access"
                        xlink:href="http://creativecommons.org/licenses/by/4.0/"
                        xml:lang="pt">
                            <license-p>Este é um artigo publicado em acesso aberto sob uma licença Creative Commons.</license-p>
                        </license>
                        <license license-type="open-access"
                        xlink:href="http://creativecommons.org/licenses/by/4.0/"
                        xml:lang="es">
                            <license-p>Este es un artículo publicado en acceso abierto bajo una licencia Creative Commons.</license-p>
                        </license>
                    </permissions>
                </article-meta>
            </front>
        </article>

        Params
        ------
        expected_code : str

        Returns
        -------
        list of dict
            A list of dictionaries, such as:
            [
                {
                'title': 'Article license code validation',
                'xpath': './permissions//license',
                'validation_type': 'value',
                'response': 'OK',
                'expected_value': 'by',
                'got_value': 'by',
                'message': 'Got: by expected one item of this list: by',
                'advice': None
                },
                ...
            ]
        """
        if not expected_code:
            raise ValidationLicenseCodeException("Provide a code for validation")

        for licenses in self.article_license.licenses:
            obtained_link = licenses.get('link')
            obtained_code = obtained_link.split('/')[4] if obtained_link else None
            is_valid = expected_code == obtained_code
            yield {
                'title': 'Article license code validation',
                'xpath': './permissions//license',
                'validation_type': 'value',
                'response': 'OK' if is_valid else 'ERROR',
                'expected_value': expected_code,
                'got_value': obtained_code,
                'message': f"Got: {obtained_code}, expected: {expected_code}",
                'advice': None if is_valid else f"Provide {expected_code} code license information"
            }
    
    
    def validate(self, data):
        """
        Função que executa as validações da classe ArticleLicenseValidation.

        Returns:
            dict: Um dicionário contendo os resultados das validações realizadas.
        
        """        
        license_results = {'article_license_validation': 
                self.validate_license(data['expected_value_license'])
            }
        code_license_results = {'article_code_license_validation': 
                self.validate_license_code(
                    data['expected_license_code'], 
                    data['expected_license_version']
                )
            }
        license_results.update(code_license_results)
        return license_results      