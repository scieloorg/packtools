import re

from packtools.sps.models.article_authors import Authors
from packtools.sps.validation.utils import format_response


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
        for author in self.article_authors.all_contribs:
            _author_name = f"{author.contrib_with_aff['given_names']} {author.contrib_with_aff['surname']}"
            obtained_value = ['<role content-type="{}">{}</role>'.format(role.get('content-type'), role.get('text')) for role in author.contrib_with_aff.get('role') or []]
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

    def validate_authors_orcid_format(self):
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

        for author in self.article_authors.all_contribs:
            _author_name = f"{author.contrib_with_aff.get('given_names')} {author.contrib_with_aff.get('surname')}"
            _orcid = author.contrib_with_aff.get('orcid')
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

    def validate_authors_orcid_is_unique(self):
        """
        Checks whether a contributor's ORCID is unique.

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
                    'title': 'Author ORCID element is unique',
                    'xpath': './/contrib-id[@contrib-id-type="orcid"]',
                    'validation_type': 'exist/verification',
                    'response': 'OK',
                    'expected_value': 'Unique ORCID values',
                    'got_value': ['0990-0001-0058-4853', '0000-3333-1238-6873'],
                    'message': 'Got ORCIDs and frequencies (\'0990-0001-0058-4853\', 1) | (\'0000-3333-1238-6873\', 1)',
                    'advice': None
                }
            ]
        """
        is_valid = True
        orcid_list = [contrib.contrib_with_aff.get('orcid') for contrib in self.article_authors.all_contribs]
        orcid_freq = {}
        for orcid in orcid_list:
            if orcid in orcid_freq:
                is_valid = False
                orcid_freq[orcid] += 1
            else:
                orcid_freq[orcid] = 1

        if not is_valid:
            diff = [item for item, freq in orcid_freq.items() if freq > 1]

        yield {
                'title': 'Author ORCID element is unique',
                'xpath': './/contrib-id[@contrib-id-type="orcid"]',
                'validation_type': 'exist/verification',
                'response': 'OK' if is_valid else 'ERROR',
                'expected_value': 'Unique ORCID values',
                'got_value': orcid_list,
                'message': 'Got ORCIDs and frequencies {}'.format(
                    " | ".join([str((item, freq)) for item, freq in orcid_freq.items()])),
                'advice': None if is_valid else 'Consider replacing the following ORCIDs that are not unique: {}'.format(
                    " | ".join(diff))
            }

    def validate_authors_orcid_is_registered(self, callable_get_validate=None):
        """
        Checks whether a contributor's ORCID is registered.

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

        Params
        ------
        callable_get_validation : function
            A function that will be passed as an argument.
            This function must have the signature 'def callable_get_validate(orcid):' and
            returns the name of the author associated with ORCID

        Returns
        -------
        list of dict
            A list of dictionaries, such as:
            [
                {
                'title': 'Author ORCID element is registered',
                'xpath': './/contrib-id[@contrib-id-type="orcid"]',
                'validation_type': 'exist',
                'response': 'OK',
                'expected_value': ['0990-0001-0058-4853', 'FRANCISCO VENEGAS-MARTÍNEZ'],
                'got_value': ['0990-0001-0058-4853', 'FRANCISCO VENEGAS-MARTÍNEZ'],
                'message': 'Got ['0990-0001-0058-4853', 'FRANCISCO VENEGAS-MARTÍNEZ'] expected '
                           '['0990-0001-0058-4853', 'FRANCISCO VENEGAS-MARTÍNEZ']',
                'advice': None
                },
                ...
            ]
        """
        callable_get_validate = callable_get_validate or _callable_extern_validate_default
        for author in self.article_authors.all_contribs:
            obtained_author_name = f"{author.contrib_with_aff.get('given_names')} {author.contrib_with_aff.get('surname')}"
            orcid = author.contrib_with_aff.get('orcid')
            expected_author_name = callable_get_validate(orcid)
            is_valid = obtained_author_name == expected_author_name

            yield {
                'title': 'Author ORCID element is registered',
                'xpath': './/contrib-id[@contrib-id-type="orcid"]',
                'validation_type': 'exist',
                'response': 'OK' if is_valid else 'ERROR',
                'expected_value': [orcid, expected_author_name],
                'got_value': [orcid, obtained_author_name],
                'message': 'Got {} expected {}'.format([orcid, obtained_author_name], [orcid, expected_author_name]),
                'advice': None if is_valid else "ORCID {} is not registered to any authors".format(orcid)
            }

    def validate_authors_affiliations(self):
        """
        Checks if an author has the corresponding affiliation data.

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
                          </name>
                          <xref ref-type="aff" rid="aff1"/>
                        </contrib>
                        <contrib contrib-type="author">
                          <name>
                            <surname>SILVA</surname>
                            <given-names>JOSÉ</given-names>
                          </name>
                          <xref ref-type="aff" rid="aff2"/>
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
                    'title': 'Author without affiliation',
                    'item': 'contrib',
                    'sub_item': 'aff',
                    'parent': 'article',
                    'parent_id': None,
                    'validation_type': 'exist',
                    'response': 'ERROR',
                    'expected_value': 'author affiliation data',
                    'got_value': None,
                    'message': 'Got None, expected author affiliation data',
                    'advice': 'provide author affiliation data for FRANCISCO VENEGAS-MARTÍNEZ',
                    'data': {
                        'aff_rids': ['aff1'],
                        'contrib-type': 'author',
                        'given_names': 'FRANCISCO',
                        'parent': 'article',
                        'parent_id': None,
                        'rid': ['aff1'],
                        'rid-aff': ['aff1'],
                        'surname': 'VENEGAS-MARTÍNEZ'
                    }
                },...
            ]
        """
        for author in self.article_authors.article_contribs:
            author_data = author.contrib_with_aff
            author_affs = author_data.get("affs")
            if not author_affs:
                yield format_response(
                    title='Author without affiliation',
                    parent=author_data.get("parent"),
                    parent_id=author_data.get("parent_id"),
                    item='contrib',
                    sub_item='aff',
                    validation_type='exist',
                    is_valid=False,
                    expected='author affiliation data',
                    obtained=None,
                    advice=f'provide author affiliation data for {author_data.get("given_names")} {author_data.get("surname")}',
                    data=author_data
                )

    def validate(self, data):
        """
        Função que executa as validações da classe ArticleAuthorsValidation.

        """
        yield from self.validate_authors_role(data['credit_taxonomy_terms_and_urls'])
        yield from self.validate_authors_orcid_format()
        yield from self.validate_authors_orcid_is_unique()
        yield from self.validate_authors_orcid_is_registered(callable_get_validate=data['callable_get_data'])
        yield from self.validate_authors_affiliations()
