import re

from packtools.sps.models.article_contribs import ArticleContribs
from packtools.sps.validation.utils import format_response


def _callable_extern_validate_default(orcid):
    raise NotImplementedError


def _response(contrib, is_valid, expected, obtained, author, error_level="ERROR"):
    return format_response(
        title="CRediT taxonomy for contribs",
        parent=contrib.get("parent"),
        parent_id=contrib.get("parent_id"),
        parent_article_type=contrib.get("parent_article_type"),
        parent_lang=contrib.get("parent_lang"),
        item="role",
        sub_item='@content-type="https://credit.niso.org/contributor-roles/*',
        validation_type="value in list",
        is_valid=is_valid,
        expected=expected,
        obtained=obtained,
        advice=f"The author {author} does not have a valid role. Provide a role from the list: {expected}",
        data=contrib,
        error_level=error_level
    )


class ContribValidation:
    def __init__(self, contrib):
        self.contrib = contrib

    def validate_contribs_role(self, credit_taxonomy_terms_and_urls):
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

        _contrib_name = self.contrib.get("contrib_full_name")

        obtained_value = [
            f'<role content-type="{role.get("content-type")}">{role.get("text")}</role>'
            for role in (self.contrib.get("contrib_role") or [])
        ]

        if obtained_value:
            for role in obtained_value:
                is_valid = role in expected_value
                yield _response(
                    contrib=self.contrib,
                    is_valid=is_valid,
                    expected=expected_value,
                    obtained=role,
                    author=_contrib_name,
                )
        else:
            yield _response(
                contrib=self.contrib,
                is_valid=False,
                expected=expected_value,
                obtained=None,
                author=_contrib_name,
            )

    def validate_contribs_orcid_format(self, error_level="ERROR"):
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

        _contrib_name = self.contrib.get("contrib_full_name")
        _orcid = self.contrib.get("contrib_ids", {}).get("orcid")
        is_valid = bool(_orcid and re.match(_default_orcid, _orcid))
        expected_value = (
            _orcid if is_valid else "a Open Researcher and Contributor ID valid"
        )

        yield format_response(
            title="Author ORCID",
            parent=self.contrib.get("parent"),
            parent_id=self.contrib.get("parent_id"),
            parent_article_type=self.contrib.get("parent_article_type"),
            parent_lang=self.contrib.get("parent_lang"),
            item="contrib-id",
            sub_item='@contrib-id-type="orcid"',
            validation_type="format",
            is_valid=is_valid,
            expected=expected_value,
            obtained=_orcid,
            advice=f"The author {_contrib_name} has {_orcid} as ORCID and its format is not valid. Provide a valid ORCID.",
            data=self.contrib,
            error_level=error_level
        )

    def validate_contribs_orcid_is_registered(self, callable_get_validate=None, error_level="ERROR"):
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
        obtained_contrib_name = self.contrib.get("contrib_full_name")
        orcid = self.contrib.get("contrib_ids", {}).get("orcid")
        expected_contrib_name = callable_get_validate(orcid)
        is_valid = obtained_contrib_name == expected_contrib_name

        yield format_response(
            title="Author ORCID element is registered",
            parent=self.contrib.get("parent"),
            parent_id=self.contrib.get("parent_id"),
            parent_article_type=self.contrib.get("parent_article_type"),
            parent_lang=self.contrib.get("parent_lang"),
            item="contrib-id",
            sub_item='@contrib-id-type="orcid"',
            validation_type="exist",
            is_valid=is_valid,
            expected=[orcid, expected_contrib_name],
            obtained=[orcid, obtained_contrib_name],
            advice="ORCID {} is not registered to any authors".format(orcid),
            data=self.contrib,
            error_level=error_level
        )

    def validate_contribs_collab_list(self, content_types, error_level="ERROR"):
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
        collab = self.contrib.get('collab')
        if collab and 'collab-list' not in content_types:
            yield format_response(
                title='Collab list authors identification',
                parent=self.contrib.get("parent"),
                parent_id=self.contrib.get("parent_id"),
                parent_article_type=self.contrib.get("parent_article_type"),
                parent_lang=self.contrib.get("parent_lang"),
                item='contrib-group',
                sub_item='@content-type',
                validation_type='exist',
                is_valid=False,
                expected=f'contrib group with identification of members of {collab}',
                obtained=None,
                advice=f'provide the identification of members of {collab}',
                data=self.contrib,
                error_level=error_level
            )

    def validate_contribs_affiliations(self, error_level="ERROR"):
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
        affs = self.contrib.get("affs")
        if not affs:
            _contrib_name = self.contrib.get("contrib_full_name")
            yield format_response(
                title='Author without affiliation',
                parent=self.contrib.get("parent"),
                parent_id=self.contrib.get("parent_id"),
                parent_article_type=self.contrib.get("parent_article_type"),
                parent_lang=self.contrib.get("parent_lang"),
                item='contrib',
                sub_item='aff',
                validation_type='exist',
                is_valid=False,
                expected='author affiliation data',
                obtained=None,
                advice=f'provide author affiliation data for {_contrib_name}',
                data=self.contrib,
                error_level=error_level
            )


class ContribsValidation:
    def __init__(self, contrib, data, content_types):
        self.contrib = contrib
        self.data = data
        self.content_types = content_types

    def validate(self):
        contrib = ContribValidation(self.contrib)

        yield from contrib.validate_contribs_role(self.data["credit_taxonomy_terms_and_urls"])
        yield from contrib.validate_contribs_orcid_format()
        yield from contrib.validate_contribs_orcid_is_registered(self.data["callable_get_data"])
        yield from contrib.validate_contribs_collab_list(self.content_types)
        yield from contrib.validate_contribs_affiliations()


class ArticleContribsValidation:
    def __init__(self, xmltree, data):
        self.xmltree = xmltree
        self.data = data
        self.contribs = ArticleContribs(self.xmltree)

    @property
    def content_types(self):
        return [
            contrib_group.get('content-type')
            for contrib_group in self.xmltree.xpath('.//contrib-group')
        ]

    def validate_contribs_orcid_is_unique(self, error_level="ERROR"):
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
                    'validation_type': 'uniqueness',
                    'response': 'OK',
                    'expected_value': 'Unique ORCID values',
                    'got_value': ['0990-0001-0058-4853', '0000-3333-1238-6873'],
                    'message': 'Got ORCIDs and frequencies (\'0990-0001-0058-4853\', 1) | (\'0000-3333-1238-6873\', 1)',
                    'advice': None
                }
            ]
        """
        orcid_dict = {}
        for contrib in self.contribs.contribs:
            orcid = contrib.get("contrib_ids", {}).get("orcid")
            if orcid:
                orcid_dict.setdefault(orcid, [])
                orcid_dict[orcid].append(contrib.get("contrib_full_name"))

        diff = []
        if not is_valid:
            diff = [item for item, freq in orcid_freq.items() if freq > 1]

        yield format_response(
            title="Author ORCID element is unique",
            parent="article",
            parent_id=None,
            parent_article_type=self.xmltree.get("article-type"),
            parent_lang=self.xmltree.get("{http://www.w3.org/XML/1998/namespace}lang"),
            item="contrib-id",
            sub_item='@contrib-id-type="orcid"',
            validation_type="uniqueness",
            is_valid=is_valid,
            expected="Unique ORCID values",
            obtained=self.orcid_list,
            advice="Consider replacing the following ORCIDs that are not unique: {}".format(
                " | ".join(diff)
            ),
            data=None,
            error_level=error_level
        )

    def validate(self):
        # A validação da unicidade do ORCID é feita uma única vez por artigo
        yield from self.validate_contribs_orcid_is_unique()
        for contrib in self.contribs.contribs:
            yield from ContribsValidation(contrib, self.data, self.content_types).validate()



