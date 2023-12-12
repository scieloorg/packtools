import re

from packtools.sps.models.article_authors import Authors


class ArticleAuthorsValidation:
    def __init__(self, xmltree):
        self._xmltree = xmltree
        self.article_authors = Authors(self._xmltree)

    def validate_authors_role(self, credit_taxonomy_terms_and_urls):
        """
        Checks contributor roles according to CRediT taxonomy.

        XML input
        ---------
        <article>
            <front>
                <article-meta>
                    <contrib-group>
                        <contrib contrib-type="author">
                            <name>
                                <surname>VENEGAS-MARTÍNEZ</surname>
                                <given-names>FRANCISCO</given-names>
                                <prefix>Prof</prefix>
                                <suffix>Nieto</suffix>
                            </name>
                            <xref ref-type="aff" rid="aff1"/>
                            <role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>
                            <role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>
                            </contrib>
                            <contrib contrib-type="author">
                            <contrib-id contrib-id-type="orcid">0000-0001-5518-4853</contrib-id>
                            <name>
                                <surname>Higa</surname>
                                <given-names>Vanessa M.</given-names>
                            </name>
                            <xref ref-type="aff" rid="aff1">a</xref>
                            <role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>
                        </contrib>
                    </contrib-group>
                </article-meta>
            </front>
        </article>

        Returns
        -------
        list of dict
            A list of dictionaries, such as:
            [
                {
                    'title': 'CRediT taxonomy for contribs',
                    'xpath': './contrib-group//contrib//role[@content-type="https://credit.niso.org/contributor-roles/*"]',
                    'validation_type': 'value in list',
                    'response': 'OK',
                    'expected_value': [
                        '<role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>',
                        '<role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>'
                    ],
                    'got_value': '<role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>',
                    'message': '''Got <role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role> expected ['<role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>', '<role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>']''',
                    'advice': None
                },...
            ]
        """
        expected_value = ['<role content-type="{}">{}</role>'.format(role['uri'], role['term']) for role in credit_taxonomy_terms_and_urls]
        for author in self.article_authors.contribs:
            _author_name = f"{author['given_names']} {author['surname']}"
            obtained_value = ['<role content-type="{}">{}</role>'.format(role.get('content-type'), role.get('text')) for role in author.get('role') or []]
            if obtained_value:
                for role in obtained_value:
                    is_valid = role in expected_value
                    yield {
                        'title': 'CRediT taxonomy for contribs',
                        'xpath': './contrib-group//contrib//role[@content-type="https://credit.niso.org/contributor-roles/*"]',
                        'validation_type': 'value in list',
                        'response': 'OK' if is_valid else 'ERROR',
                        'expected_value': expected_value,
                        'got_value': role,
                        'message': f'Got {role} expected {expected_value}',
                        'advice': None if is_valid else f"The author {_author_name} does not have a valid role. Provide a role from the list: {expected_value}"
                    }
            else:
                yield {
                    'title': 'CRediT taxonomy for contribs',
                    'xpath': './contrib-group//contrib//role[@content-type="https://credit.niso.org/contributor-roles/*"]',
                    'validation_type': 'value in list',
                    'response': 'ERROR',
                    'expected_value': expected_value,
                    'got_value': None,
                    'message': f'Got None expected {expected_value}',
                    'advice': f"The author {_author_name} does not have a valid role. Provide a role from the list: {expected_value}"
                }

    def validate_authors_orcid(self):
        _result_dict = []
        _default_orcid = r'^[0-9a-zA-Z]{4}-[0-9a-zA-Z]{4}-[0-9a-zA-Z]{4}-[0-9a-zA-Z]{4}$'

        for author in self.article_authors.contribs:
            _author_name = f"{author['given_names']} {author['surname']}"

            if 'orcid' not in author:                 
                _result_dict.append({
                    'result': "error",
                    'error_type': "Orcid not found",
                    'message': f"The author {_author_name} does not have an orcid. Please add a valid orcid.",
                    'author': author, 
                })
            else:
                if re.match(_default_orcid, author['orcid']):
                    _result_dict.append({
                        'result': 'success',
                        'message': f"The author {_author_name} has a valid orcid.",
                        'author': author,
                    })
                else:
                    _result_dict.append({
                        'result': 'error',
                        'error_type': "Format invalid",
                        'message': f"The author {_author_name} has an orcid in an invalid format. Please ensure that the ORCID is entered correctly, including the proper format (e.g., 0000-0002-1825-0097).",
                        'author': author,
                    })
        return _result_dict
    

    def validate(self, data):
        """
        Função que executa as validações da classe ArticleAuthorsValidation.

        Returns:
            dict: Um dicionário contendo os resultados das validações realizadas.
        
        """
        credit_terms_and_urls_results = {
            'authors_credit_terms_and_urls_validation': self.validate_authors_role(data['credit_taxonomy_terms_and_urls'])
            }
        orcid_results = {
            'authors_orcid_validation': self.validate_authors_orcid()
            }
        credit_terms_and_urls_results.update(orcid_results)
        return credit_terms_and_urls_results