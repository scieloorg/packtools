import re

from packtools.sps.models.article_contribs import ArticleContribs
from packtools.sps.validation.utils import format_response


def _callable_extern_validate_default(orcid):
    raise NotImplementedError


def _response(contrib, is_valid, expected, obtained, author):
    return format_response(
        title="CRediT taxonomy for contribs",
        parent=contrib.get("parent"),
        parent_id=contrib.get("parent_id"),
        item="role",
        sub_item='@content-type="https://credit.niso.org/contributor-roles/*',
        validation_type="value in list",
        is_valid=is_valid,
        expected=expected,
        obtained=obtained,
        advice=f"The author {author} does not have a valid role. Provide a role from the list: {expected}",
        data=contrib,
    )


class ArticleContribsValidation:
    def __init__(self, xmltree):
        self._xmltree = xmltree
        self.article_contribs = ArticleContribs(self._xmltree)

    @property
    def content_types(self):
        return (
            contrib_group.get('content-type')
            for contrib_group in self._xmltree.xpath('.//contrib-group')
        )

    def validate_contribs_role(self, contrib, credit_taxonomy_terms_and_urls):
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
        expected_value = [
            f'<role content-type="{role["uri"]}">{role["term"]}</role>'
            for role in credit_taxonomy_terms_and_urls
        ]

        names = contrib.get("contrib_name", {})
        _author_name = f"{names.get('given-names', '')} {names.get('surname', '')}"

        obtained_value = [
            f'<role content-type="{role.get("content-type")}">{role.get("text")}</role>'
            for role in (contrib.get("contrib_role") or [])
        ]

        if obtained_value:
            for role in obtained_value:
                is_valid = role in expected_value
                yield _response(
                    contrib=contrib,
                    is_valid=is_valid,
                    expected=expected_value,
                    obtained=role,
                    author=_author_name,
                )
        else:
            yield _response(
                contrib=contrib,
                is_valid=False,
                expected=expected_value,
                obtained=None,
                author=_author_name,
            )

    def validate_contribs_orcid_format(self, contrib):
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
        _default_orcid = (
            r"^[0-9a-zA-Z]{4}-[0-9a-zA-Z]{4}-[0-9a-zA-Z]{4}-[0-9a-zA-Z]{4}$"
        )

        names = contrib.get("contrib_name", {})
        _author_name = f"{names.get('given-names', '')} {names.get('surname', '')}"
        _orcid = contrib.get("contrib_ids", {}).get("orcid")
        is_valid = bool(_orcid and re.match(_default_orcid, _orcid))
        expected_value = (
            _orcid if is_valid else "A Open Researcher and Contributor ID valid"
        )

        yield format_response(
            title="Author ORCID",
            parent=contrib.get("parent"),
            parent_id=contrib.get("parent_id"),
            item="contrib-id",
            sub_item='@contrib-id-type="orcid"',
            validation_type="format",
            is_valid=is_valid,
            expected=expected_value[:1].lower() + expected_value[1:],
            obtained=_orcid,
            advice=f"The author {_author_name} has {_orcid} as ORCID and its format is not valid. Provide a valid ORCID.",
            data=contrib,
        )

    def validate_contribs_orcid_is_unique(self):
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
        orcid_list = [
            contrib.get("contrib_ids", {}).get("orcid")
            for contrib in self.article_contribs.contribs
        ]
        orcid_freq = {}
        for orcid in filter(None, orcid_list):
            if orcid in orcid_freq:
                is_valid = False
                orcid_freq[orcid] += 1
            else:
                orcid_freq[orcid] = 1

        diff = []
        if not is_valid:
            diff = [item for item, freq in orcid_freq.items() if freq > 1]

        yield format_response(
            title="Author ORCID element is unique",
            parent=None,
            parent_id=None,
            item="contrib-id",
            sub_item='@contrib-id-type="orcid"',
            validation_type="exist/verification",
            is_valid=is_valid,
            expected="Unique ORCID values",
            obtained=orcid_list,
            advice="Consider replacing the following ORCIDs that are not unique: {}".format(
                " | ".join(diff)
            ),
            data=None,
        )

    def validate_contribs_orcid_is_registered(
        self, contrib, callable_get_validate=None
    ):
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
        callable_get_validate = (
            callable_get_validate or _callable_extern_validate_default
        )
        names = contrib.get("contrib_name", {})
        obtained_author_name = (
            f"{names.get('given-names', '')} {names.get('surname', '')}"
        )
        orcid = contrib.get("contrib_ids", {}).get("orcid")
        expected_author_name = callable_get_validate(orcid)
        is_valid = obtained_author_name == expected_author_name

        yield format_response(
            title="Author ORCID element is registered",
            parent=contrib.get("parent"),
            parent_id=contrib.get("parent_id"),
            item="contrib-id",
            sub_item='@contrib-id-type="orcid"',
            validation_type="exist",
            is_valid=is_valid,
            expected=[orcid, expected_author_name],
            obtained=[orcid, obtained_author_name],
            advice="ORCID {} is not registered to any authors".format(orcid),
        )

    def validate_authors_collab_list(self, contrib):
        """
        Checks if there is identification of authors for a group of collaborators.

        XML input
        ---------
        <article>
            <front>
                <article-meta>
                    <contrib-group>
                        <contrib contrib-type="author">
                            <collab>The MARS Group</collab>
                        </contrib>
                    </contrib-group>
                    <contrib-group content-type="collab-list">
                        <contrib contrib-type="author" rid="collab">
                        <contrib-id contrib-id-type="orcid">0000-0001-0002-0003</contrib-id>
                        <name>
                        <surname>Wright</surname>
                        <given-names>Rick W.</given-names>
                        </name>
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
                    'title': 'Collab list authors identification',
                    'parent': None,
                    'parent_id': None,
                    'item': 'contrib-group',
                    'sub_item': '@content-type',
                    'validation_type': 'exist',
                    'response': 'ERROR',
                    'expected_value': 'contrib group with identification of members of The MARS Group',
                    'got_value': None,
                    'message': 'Got None, expected contrib group with identification of members of The MARS Group',
                    'advice': 'provide the identification of members of The MARS Group',
                    'data': {
                        'aff_rids': None,
                        'collab': 'The MARS Group',
                        'contrib-type': 'author'
                    }
                }...
            ]
        """
        collab = contrib.get('collab')
        if collab and 'collab-list' not in self.content_types:
            yield format_response(
                title='Collab list authors identification',
                parent=None,
                parent_id=None,
                item='contrib-group',
                sub_item='@content-type',
                validation_type='exist',
                is_valid=False,
                expected=f'contrib group with identification of members of {collab}',
                obtained=None,
                advice=f'provide the identification of members of {collab}',
                data=contrib
            )

    def validate(self, data):
        """
        Função que executa as validações da classe ArticleAuthorsValidation.

        """
        for contrib in self.article_contribs.contribs:
            yield from self.validate_contribs_role(
                contrib, data["credit_taxonomy_terms_and_urls"]
            )
            yield from self.validate_contribs_orcid_format(contrib)
            yield from self.validate_contribs_orcid_is_registered(
                contrib, callable_get_validate=data["callable_get_data"]
            )
            yield from self.validate_authors_collab_list(contrib)
        yield from self.validate_contribs_orcid_is_unique()
class ArticleContribsValidation:
    def __init__(self, xmltree, data):
        self.xmltree = xmltree
        self.data = data
        self.contribs = ArticleContribs(self.xmltree)

    @property
    def content_types(self):
        return (
            contrib_group.get('content-type')
            for contrib_group in self.xmltree.xpath('.//contrib-group')
        )

    @property
    def orcid_list(self):
        return [
            contrib.get("contrib_ids", {}).get("orcid")
            for contrib in self.contribs.contribs
        ]

    def validate(self):
        for contrib in self.contribs.contribs:
            yield from ContribsValidation(contrib, self.data, self.content_types, self.orcid_list).validate()



