import re

from packtools.sps.models.article_authors import Authors


def _callable_extern_validate_default(orcid):
    raise NotImplementedError


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
        """
        Checks whether a contributor's ORCID is valid.

        XML input
        ---------
        <article>
            <front>
                <article-meta>
                    <contrib-group>
                        <contrib contrib-type="author">
                            <contrib-id contrib-id-type="orcid">0990-0001-0058-4853</contrib-id>
                            <name>
                                <surname>VENEGAS-MARTÍNEZ</surname>
                                <given-names>FRANCISCO</given-names>
                                <prefix>Prof</prefix>
                                <suffix>Nieto</suffix>
                            </name>
                            <xref ref-type="aff" rid="aff1"/>
                        </contrib>
                        <contrib contrib-type="author">
                            <contrib-id contrib-id-type="orcid">0000-3333-1238-6873</contrib-id>
                            <name>
                                <surname>Higa</surname>
                                <given-names>Vanessa M.</given-names>
                            </name>
                            <xref ref-type="aff" rid="aff1">a</xref>
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
                    'title': 'Author ORCID',
                    'xpath': './/contrib-id[@contrib-id-type="orcid"]',
                    'validation_type': 'format',
                    'response': 'OK',
                    'expected_value': '0990-0001-0058-4853',
                    'got_value': '0990-0001-0058-4853',
                    'message': f'Got 0990-0001-0058-4853 expected 0990-0001-0058-4853',
                    'advice': None
                },...
            ]
        """
        _default_orcid = r'^[0-9a-zA-Z]{4}-[0-9a-zA-Z]{4}-[0-9a-zA-Z]{4}-[0-9a-zA-Z]{4}$'

        for author in self.article_authors.contribs:
            _author_name = f"{author.get('given_names')} {author.get('surname')}"
            _orcid = author.get('orcid')
            is_valid = re.match(_default_orcid, _orcid) if _orcid else False
            expected_value = _orcid if is_valid else 'A Open Researcher and Contributor ID valid'

            yield {
                'title': 'Author ORCID',
                'xpath': './/contrib-id[@contrib-id-type="orcid"]',
                'validation_type': 'format',
                'response': 'OK' if is_valid else 'ERROR',
                'expected_value': expected_value,
                'got_value': _orcid,
                'message': f'Got {_orcid} expected {expected_value[:1].lower() + expected_value[1:]}',
                'advice': None if is_valid else f"The author {_author_name} has {_orcid} as ORCID and its format is not valid. Provide a valid ORCID."
            }

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