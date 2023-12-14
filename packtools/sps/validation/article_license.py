from packtools.sps.models.article_license import ArticleLicense

from packtools.sps.validation.exceptions import (
    ValidationLicenseException,
    ValidationLicenseCodeException
)


class ArticleLicenseValidation:
    def __init__(self, xmltree):
        self.article_license = ArticleLicense(xmltree)

    def validate_license(self, expected_value=None):
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
                    'licence_p': 'This is an article published in open access under a Creative Commons license.'
                },
                'pt': {
                    'lang': 'pt',
                    'link': 'http://creativecommons.org/licenses/by/4.0/',
                    'licence_p': 'Este é um artigo publicado em acesso aberto sob uma licença Creative Commons.'
                },
                'es': {
                    'lang': 'es',
                    'link': 'http://creativecommons.org/licenses/by/4.0/',
                    'licence_p': 'Este es un artículo publicado en acceso abierto bajo una licencia Creative Commons.'
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
                        'licence_p': 'This is an article published in open access under a Creative Commons license.'
                        },
                    'got_value': {
                        'lang': 'en',
                        'link': 'http://creativecommons.org/licenses/by/4.0/',
                        'licence_p': 'This is an article published in open access under a Creative Commons license.'
                        },
                    'message': "Got {"
                               "'lang': 'en', "
                               "'link': 'http://creativecommons.org/licenses/by/4.0/', "
                               "'licence_p': 'This is an article published in open access under a Creative Commons license.'"
                               "} expected {"
                               "'lang': 'en', "
                               "'link': 'http://creativecommons.org/licenses/by/4.0/', "
                               "'licence_p': 'This is an article published in open access under a Creative Commons license.'"
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
            is_valid = expected_value.get(lang) == data
            expected_value_msg = expected_value.get(
                lang) if is_valid else 'License data that matches the language {}'.format(lang)
            yield {
                'title': 'Article license validation',
                'xpath': './permissions//license',
                'validation_type': 'value in list',
                'response': 'OK' if is_valid else 'ERROR',
                'expected_value': expected_value_msg,
                'got_value': data,
                'message': f'Got {data} expected {expected_value_msg}',
                'advice': None if is_valid else 'Provide license data that is consistent with the language: {} and '
                                                'standard adopted by the journal'.format(lang)
            }

    def validate_license_code(self, code_list=None):
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
        code_list : list, such as:
            ['by', '4.0']

        Returns
        -------
        list of dict
            A list of dictionaries, such as:
            [
                {
                'title': 'Article license code validation',
                'xpath': './permissions//license',
                'validation_type': 'value in list',
                'response': 'OK',
                'expected_value': 'http://creativecommons.org/licenses/by/4.0/',
                'got_value': 'http://creativecommons.org/licenses/by/4.0/',
                'message': 'Got: http://creativecommons.org/licenses/by/4.0/ expected: http://creativecommons.org/licenses/by/4.0/',
                'advice': None
                },
                ...
            ]
        """
        if not code_list:
            raise ValidationLicenseCodeException("Provide a list of codes for validation")

        for licenses in self.article_license.licenses:
            is_valid = f"http://creativecommons.org/licenses/{code_list[0]}/{code_list[1]}/" == licenses.get('link')
            yield {
                'title': 'Article license code validation',
                'xpath': './permissions//license',
                'validation_type': 'value in list',
                'response': 'OK' if is_valid else 'ERROR',
                'expected_value': f"http://creativecommons.org/licenses/{code_list[0]}/{code_list[1]}/",
                'got_value': licenses.get('link'),
                'message': f"Got: {licenses.get('link')} expected: http://creativecommons.org/licenses/{code_list[0]}/{code_list[1]}/",
                'advice': None if is_valid else f"Provide license code that is consistent with http://creativecommons.org/licenses/{code_list[0]}/{code_list[1]}/"
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