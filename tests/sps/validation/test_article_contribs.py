from unittest import TestCase

from lxml import etree

from packtools.sps.models.article_contribs import ArticleContribs
from packtools.sps.validation.article_contribs import ContribValidation, ArticleContribsValidation

credit_taxonomy_terms_and_urls = [
    {
        "term": "Conceptualization",
        "uri": "https://credit.niso.org/contributor-roles/conceptualization/",
    },
    {
        "term": "Data curation",
        "uri": "https://credit.niso.org/contributor-roles/data-curation/",
    },
]


def callable_get_data(orcid):
    tests = {
        "0990-0001-0058-4853": "FRANCISCO VENEGAS MARTÍNEZ",
        "0000-3333-1238-6873": "Vanessa M. Higa",
    }
    return tests.get(orcid)


def callable_get_data_empty(orcid):
    tests = {"0990-0001-0058-4853": None, "0000-3333-1238-6873": None}
    return tests.get(orcid)


class ArticleContribsValidationTest(TestCase):
    def test_without_role(self):
        self.maxDiff = None
        xml = """
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
                            </contrib>
                            <contrib contrib-type="author">
                            <contrib-id contrib-id-type="orcid">0000-0001-5518-4853</contrib-id>
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
        """

        xmltree = etree.fromstring(xml)
        contrib = list(ArticleContribs(xmltree).contribs)[0]
        obtained = list(
            ContribValidation(contrib).validate_contribs_role(
                credit_taxonomy_terms_and_urls=credit_taxonomy_terms_and_urls,
            )
        )

        expected = [
            {
                "title": "CRediT taxonomy for contribs",
                "parent": "article",
                "parent_id": None,
                "item": "role",
                "sub_item": '@content-type="https://credit.niso.org/contributor-roles/*',
                "validation_type": "value in list",
                "response": "ERROR",
                "expected_value": [
                    '<role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>',
                    '<role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>',
                ],
                "got_value": None,
                "message": """Got None, expected ['<role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>', '<role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>']""",
                "advice": """The author FRANCISCO VENEGAS-MARTÍNEZ does not have a valid role. Provide a role from the list: ['<role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>', '<role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>']""",
                "data": {
                    "contrib_name": {
                        "given-names": "FRANCISCO",
                        "prefix": "Prof",
                        "suffix": "Nieto",
                        "surname": "VENEGAS-MARTÍNEZ",
                    },
                    "contrib_type": "author",
                    "contrib_xref": [{"ref_type": "aff", "rid": "aff1", "text": None}],
                    "parent": "article",
                    "parent_article_type": None,
                    "parent_id": None,
                    "parent_lang": None,
                },
            }
        ]

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

    def test_role_and_content_type_empty(self):
        self.maxDiff = None
        xml = """
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
                            <role></role>
                            </contrib>
                            <contrib contrib-type="author">
                            <contrib-id contrib-id-type="orcid">0000-0001-5518-4853</contrib-id>
                            <name>
                                <surname>Higa</surname>
                                <given-names>Vanessa M.</given-names>
                            </name>
                            <xref ref-type="aff" rid="aff1">a</xref>
                            <role></role>
                        </contrib>
                    </contrib-group>
                </article-meta>
            </front>
        </article>
        """

        xmltree = etree.fromstring(xml)
        contrib = list(ArticleContribs(xmltree).contribs)[0]
        obtained = list(
            ContribValidation(contrib).validate_contribs_role(
                credit_taxonomy_terms_and_urls=credit_taxonomy_terms_and_urls,
            )
        )

        expected = [
            {
                "title": "CRediT taxonomy for contribs",
                "parent": "article",
                "parent_id": None,
                "item": "role",
                "sub_item": '@content-type="https://credit.niso.org/contributor-roles/*',
                "validation_type": "value in list",
                "response": "ERROR",
                "expected_value": [
                    "<role "
                    'content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>',
                    "<role "
                    'content-type="https://credit.niso.org/contributor-roles/data-curation/">Data '
                    "curation</role>",
                ],
                "got_value": '<role content-type="None">None</role>',
                "message": """Got <role content-type="None">None</role>, expected ['<role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>', '<role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>']""",
                "advice": """The author FRANCISCO VENEGAS-MARTÍNEZ does not have a valid role. Provide a role from the list: ['<role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>', '<role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>']""",
                "data": {
                    "contrib_name": {
                        "given-names": "FRANCISCO",
                        "prefix": "Prof",
                        "suffix": "Nieto",
                        "surname": "VENEGAS-MARTÍNEZ",
                    },
                    "contrib_role": [
                        {"content-type": None, "specific-use": None, "text": None}
                    ],
                    "contrib_type": "author",
                    "contrib_xref": [{"ref_type": "aff", "rid": "aff1", "text": None}],
                    "parent": "article",
                    "parent_article_type": None,
                    "parent_id": None,
                    "parent_lang": None,
                },
            }
        ]

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

    def test_role_without_content_type(self):
        self.maxDiff = None
        xml = """
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
                                <role>Data curation</role>
                                </contrib>
                                <contrib contrib-type="author">
                                <contrib-id contrib-id-type="orcid">0000-0001-5518-4853</contrib-id>
                                <name>
                                    <surname>Higa</surname>
                                    <given-names>Vanessa M.</given-names>
                                </name>
                                <xref ref-type="aff" rid="aff1">a</xref>
                                <role>Conceptualization</role>
                            </contrib>
                        </contrib-group>
                    </article-meta>
                </front>
            </article>
            """

        expected = [
            {
                "title": "CRediT taxonomy for contribs",
                "parent": "article",
                "parent_id": None,
                "item": "role",
                "sub_item": '@content-type="https://credit.niso.org/contributor-roles/*',
                "validation_type": "value in list",
                "response": "ERROR",
                "got_value": '<role content-type="None">Data curation</role>',
                "expected_value": [
                    "<role "
                    'content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>',
                    "<role "
                    'content-type="https://credit.niso.org/contributor-roles/data-curation/">Data '
                    "curation</role>",
                ],
                "message": """Got <role content-type="None">Data curation</role>, expected ['<role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>', '<role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>']""",
                "advice": """The author FRANCISCO VENEGAS-MARTÍNEZ does not have a valid role. Provide a role from the list: ['<role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>', '<role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>']""",
                "data": {
                    "contrib_name": {
                        "given-names": "FRANCISCO",
                        "prefix": "Prof",
                        "suffix": "Nieto",
                        "surname": "VENEGAS-MARTÍNEZ",
                    },
                    "contrib_role": [
                        {
                            "content-type": None,
                            "specific-use": None,
                            "text": "Data curation",
                        }
                    ],
                    "contrib_type": "author",
                    "contrib_xref": [{"ref_type": "aff", "rid": "aff1", "text": None}],
                    "parent": "article",
                    "parent_article_type": None,
                    "parent_id": None,
                    "parent_lang": None,
                },
            }
        ]

        xmltree = etree.fromstring(xml)
        contrib = list(ArticleContribs(xmltree).contribs)[0]
        obtained = list(
            ContribValidation(contrib).validate_contribs_role(
                credit_taxonomy_terms_and_urls=credit_taxonomy_terms_and_urls,
            )
        )

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

    def test_role_no_text_with_content_type(self):
        self.maxDiff = None
        xml = """
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
                                <role content-type="https://credit.niso.org/contributor-roles/data-curation/"></role>
                                <role content-type="https://credit.niso.org/contributor-roles/conceptualization/"></role>
                                </contrib>
                                <contrib contrib-type="author">
                                <contrib-id contrib-id-type="orcid">0000-0001-5518-4853</contrib-id>
                                <name>
                                    <surname>Higa</surname>
                                    <given-names>Vanessa M.</given-names>
                                </name>
                                <xref ref-type="aff" rid="aff1">a</xref>
                                <role content-type="https://credit.niso.org/contributor-roles/conceptualization/"></role>
                            </contrib>
                        </contrib-group>
                    </article-meta>
                </front>
            </article>
            """

        expected = [
            {
                "title": "CRediT taxonomy for contribs",
                "parent": "article",
                "parent_id": None,
                "item": "role",
                "sub_item": '@content-type="https://credit.niso.org/contributor-roles/*',
                "validation_type": "value in list",
                "response": "ERROR",
                "got_value": '<role content-type="https://credit.niso.org/contributor-roles/data-curation/">None</role>',
                "expected_value": [
                    "<role "
                    'content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>',
                    "<role "
                    'content-type="https://credit.niso.org/contributor-roles/data-curation/">Data '
                    "curation</role>",
                ],
                "message": """Got <role content-type="https://credit.niso.org/contributor-roles/data-curation/">None</role>, expected ['<role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>', '<role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>']""",
                "advice": """The author FRANCISCO VENEGAS-MARTÍNEZ does not have a valid role. Provide a role from the list: ['<role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>', '<role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>']""",
                "data": {
                    "contrib_name": {
                        "given-names": "FRANCISCO",
                        "prefix": "Prof",
                        "suffix": "Nieto",
                        "surname": "VENEGAS-MARTÍNEZ",
                    },
                    "contrib_role": [
                        {
                            "content-type": "https://credit.niso.org/contributor-roles/data-curation/",
                            "specific-use": None,
                            "text": None,
                        },
                        {
                            "content-type": "https://credit.niso.org/contributor-roles/conceptualization/",
                            "specific-use": None,
                            "text": None,
                        },
                    ],
                    "contrib_type": "author",
                    "contrib_xref": [{"ref_type": "aff", "rid": "aff1", "text": None}],
                    "parent": "article",
                    "parent_article_type": None,
                    "parent_id": None,
                    "parent_lang": None,
                },
            }
        ]

        xmltree = etree.fromstring(xml)
        contrib = list(ArticleContribs(xmltree).contribs)[0]
        obtained = list(
            ContribValidation(contrib).validate_contribs_role(
                credit_taxonomy_terms_and_urls=credit_taxonomy_terms_and_urls,
            )
        )

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

    def test_wrong_role_and_content_type(self):
        self.maxDiff = None
        xml = """
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
                            <role content-type="https://credit.niso.org/contributor-roles/data-curan/">Data curation</role>
                            <role content-type="https://credit.niso.org/contributor-roles/conceualizan/">Conceplization</role>
                            </contrib>
                            <contrib contrib-type="author">
                            <contrib-id contrib-id-type="orcid">0000-0001-5518-4853</contrib-id>
                            <name>
                                <surname>Higa</surname>
                                <given-names>Vanessa M.</given-names>
                            </name>
                            <xref ref-type="aff" rid="aff1">a</xref>
                            <role content-type="https://credit.niso.org/contributor-roles/conceualizan/">Conceplization</role>
                        </contrib>
                    </contrib-group>
                </article-meta>
            </front>
        </article>
        """

        expected = [
            {
                "title": "CRediT taxonomy for contribs",
                "parent": "article",
                "parent_id": None,
                "item": "role",
                "sub_item": '@content-type="https://credit.niso.org/contributor-roles/*',
                "validation_type": "value in list",
                "response": "ERROR",
                "got_value": '<role content-type="https://credit.niso.org/contributor-roles/data-curan/">Data curation</role>',
                "expected_value": [
                    "<role "
                    'content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>',
                    "<role "
                    'content-type="https://credit.niso.org/contributor-roles/data-curation/">Data '
                    "curation</role>",
                ],
                "message": """Got <role content-type="https://credit.niso.org/contributor-roles/data-curan/">Data curation</role>, expected ['<role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>', '<role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>']""",
                "advice": """The author FRANCISCO VENEGAS-MARTÍNEZ does not have a valid role. Provide a role from the list: ['<role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>', '<role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>']""",
                "data": {
                    "contrib_name": {
                        "given-names": "FRANCISCO",
                        "prefix": "Prof",
                        "suffix": "Nieto",
                        "surname": "VENEGAS-MARTÍNEZ",
                    },
                    "contrib_role": [
                        {
                            "content-type": "https://credit.niso.org/contributor-roles/data-curan/",
                            "specific-use": None,
                            "text": "Data curation",
                        },
                        {
                            "content-type": "https://credit.niso.org/contributor-roles/conceualizan/",
                            "specific-use": None,
                            "text": "Conceplization",
                        },
                    ],
                    "contrib_type": "author",
                    "contrib_xref": [{"ref_type": "aff", "rid": "aff1", "text": None}],
                    "parent": "article",
                    "parent_article_type": None,
                    "parent_id": None,
                    "parent_lang": None,
                },
            }
        ]

        xmltree = etree.fromstring(xml)
        contrib = list(ArticleContribs(xmltree).contribs)[0]
        obtained = list(
            ContribValidation(contrib).validate_contribs_role(
                credit_taxonomy_terms_and_urls=credit_taxonomy_terms_and_urls,
            )
        )

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

    def test_success_role(self):
        self.maxDiff = None
        xml = """
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
        """

        expected = [
            {
                "title": "CRediT taxonomy for contribs",
                "parent": "article",
                "parent_id": None,
                "item": "role",
                "sub_item": '@content-type="https://credit.niso.org/contributor-roles/*',
                "validation_type": "value in list",
                "response": "OK",
                "expected_value": [
                    '<role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>',
                    '<role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>',
                ],
                "got_value": '<role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>',
                "message": """Got <role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>, expected ['<role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>', '<role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>']""",
                "advice": None,
                "data": {
                    "contrib_name": {
                        "given-names": "FRANCISCO",
                        "prefix": "Prof",
                        "suffix": "Nieto",
                        "surname": "VENEGAS-MARTÍNEZ",
                    },
                    "contrib_role": [
                        {
                            "content-type": "https://credit.niso.org/contributor-roles/data-curation/",
                            "specific-use": None,
                            "text": "Data curation",
                        },
                        {
                            "content-type": "https://credit.niso.org/contributor-roles/conceptualization/",
                            "specific-use": None,
                            "text": "Conceptualization",
                        },
                    ],
                    "contrib_type": "author",
                    "contrib_xref": [{"ref_type": "aff", "rid": "aff1", "text": None}],
                    "parent": "article",
                    "parent_article_type": None,
                    "parent_id": None,
                    "parent_lang": None,
                },
            }
        ]

        xmltree = etree.fromstring(xml)
        contrib = list(ArticleContribs(xmltree).contribs)[0]
        obtained = list(
            ContribValidation(contrib).validate_contribs_role(
                credit_taxonomy_terms_and_urls=credit_taxonomy_terms_and_urls,
            )
        )

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)


class ArticleContribsValidationOrcidTest(TestCase):
    def test_validate_authors_orcid_format_fail(self):
        self.maxDiff = None
        xml = """
        <article>
        <front>
            <article-meta>
              <contrib-group>
                <contrib contrib-type="author">
                    <contrib-id contrib-id-type="orcid">0990-01-58-4853</contrib-id>
                  <name>
                    <surname>VENEGAS-MARTÍNEZ</surname>
                    <given-names>FRANCISCO</given-names>
                    <prefix>Prof</prefix>
                    <suffix>Nieto</suffix>
                  </name>
                  <xref ref-type="aff" rid="aff1"/>
                </contrib>
                <contrib contrib-type="author">
                  <contrib-id contrib-id-type="orcid">00-0001-5518-4853</contrib-id>
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
        """
        xmltree = etree.fromstring(xml)
        contrib = list(ArticleContribs(xmltree).contribs)[0]
        obtained = list(
            ContribValidation(contrib).validate_contribs_orcid_format())

        expected = [
            {
                "title": "Author ORCID",
                "parent": "article",
                "parent_id": None,
                "item": "contrib-id",
                "sub_item": '@contrib-id-type="orcid"',
                "validation_type": "format",
                "response": "ERROR",
                "expected_value": "a Open Researcher and Contributor ID valid",
                "got_value": "0990-01-58-4853",
                "message": "Got 0990-01-58-4853, expected a Open Researcher and Contributor ID valid",
                "advice": "The author FRANCISCO VENEGAS-MARTÍNEZ has 0990-01-58-4853 as ORCID "
                "and its format is not valid. Provide a valid ORCID.",
                "data": {
                    "contrib_ids": {"orcid": "0990-01-58-4853"},
                    "contrib_name": {
                        "given-names": "FRANCISCO",
                        "prefix": "Prof",
                        "suffix": "Nieto",
                        "surname": "VENEGAS-MARTÍNEZ",
                    },
                    "contrib_type": "author",
                    "contrib_xref": [{"ref_type": "aff", "rid": "aff1", "text": None}],
                    "parent": "article",
                    "parent_article_type": None,
                    "parent_id": None,
                    "parent_lang": None,
                },
            }
        ]
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

    def test_validate_authors_orcid_format_without_orcid(self):
        self.maxDiff = None
        xml = """
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
                </contrib>
                <contrib contrib-type="author">
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
        """
        xmltree = etree.fromstring(xml)
        contrib = list(ArticleContribs(xmltree).contribs)[0]
        obtained = list(ContribValidation(contrib).validate_contribs_orcid_format())

        expected = [
            {
                "title": "Author ORCID",
                "parent": "article",
                "parent_id": None,
                "item": "contrib-id",
                "sub_item": '@contrib-id-type="orcid"',
                "validation_type": "format",
                "response": "ERROR",
                "expected_value": "a Open Researcher and Contributor ID valid",
                "got_value": None,
                "message": "Got None, expected a Open Researcher and Contributor ID valid",
                "advice": "The author FRANCISCO VENEGAS-MARTÍNEZ has None as ORCID and its format is not valid. Provide a valid ORCID.",
                "data": {
                    "contrib_name": {
                        "given-names": "FRANCISCO",
                        "prefix": "Prof",
                        "suffix": "Nieto",
                        "surname": "VENEGAS-MARTÍNEZ",
                    },
                    "contrib_type": "author",
                    "contrib_xref": [{"ref_type": "aff", "rid": "aff1", "text": None}],
                    "parent": "article",
                    "parent_article_type": None,
                    "parent_id": None,
                    "parent_lang": None,
                },
            }
        ]

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

    def test_validate_authors_orcid_format_success(self):
        self.maxDiff = None
        xml = """
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
        """

        xmltree = etree.fromstring(xml)
        contrib = list(ArticleContribs(xmltree).contribs)[0]
        obtained = list(
            ContribValidation(contrib).validate_contribs_orcid_format())

        expected = [
            {
                "title": "Author ORCID",
                "parent": "article",
                "parent_id": None,
                "item": "contrib-id",
                "sub_item": '@contrib-id-type="orcid"',
                "validation_type": "format",
                "response": "OK",
                "expected_value": "0990-0001-0058-4853",
                "got_value": "0990-0001-0058-4853",
                "message": "Got 0990-0001-0058-4853, expected 0990-0001-0058-4853",
                "advice": None,
                "data": {
                    "contrib_ids": {"orcid": "0990-0001-0058-4853"},
                    "contrib_name": {
                        "given-names": "FRANCISCO",
                        "prefix": "Prof",
                        "suffix": "Nieto",
                        "surname": "VENEGAS-MARTÍNEZ",
                    },
                    "contrib_type": "author",
                    "contrib_xref": [{"ref_type": "aff", "rid": "aff1", "text": None}],
                    "parent": "article",
                    "parent_article_type": None,
                    "parent_id": None,
                    "parent_lang": None,
                },
            }
        ]

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

    def test_validate_authors_orcid_is_unique_ok(self):
        self.maxDiff = None
        xml = """
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
        """

        xmltree = etree.fromstring(xml)
        orcid_list = list(ArticleContribsValidation(xmltree, data={}).orcid_list)
        contrib = list(ArticleContribs(xmltree).contribs)[0]
        obtained = list(
            ContribValidation(contrib).validate_contribs_orcid_is_unique(orcid_list)
        )

        expected = [
            {
                "title": "Author ORCID element is unique",
                "parent": None,
                "parent_id": None,
                "item": "contrib-id",
                "sub_item": '@contrib-id-type="orcid"',
                "validation_type": "exist/verification",
                "response": "OK",
                "expected_value": "Unique ORCID values",
                "got_value": ["0990-0001-0058-4853", "0000-3333-1238-6873"],
                "message": "Got ['0990-0001-0058-4853', '0000-3333-1238-6873'], expected Unique ORCID values",
                "advice": None,
                "data": None,
            }
        ]

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

    def test_validate_authors_orcid_is_unique_not_ok(self):
        self.maxDiff = None
        xml = """
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
                    <contrib-id contrib-id-type="orcid">0990-0001-0058-4853</contrib-id>
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
        """

        xmltree = etree.fromstring(xml)
        orcid_list = list(ArticleContribsValidation(xmltree, data={}).orcid_list)
        contrib = list(ArticleContribs(xmltree).contribs)[0]
        obtained = list(
            ContribValidation(contrib).validate_contribs_orcid_is_unique(orcid_list)
        )

        expected = [
            {
                "title": "Author ORCID element is unique",
                "parent": None,
                "parent_id": None,
                "item": "contrib-id",
                "sub_item": '@contrib-id-type="orcid"',
                "validation_type": "exist/verification",
                "response": "ERROR",
                "expected_value": "Unique ORCID values",
                "got_value": ["0990-0001-0058-4853", "0990-0001-0058-4853"],
                "message": "Got ['0990-0001-0058-4853', '0990-0001-0058-4853'], expected Unique ORCID values",
                "advice": "Consider replacing the following ORCIDs that are not unique: 0990-0001-0058-4853",
                "data": None,
            }
        ]

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

    def test_validate_authors_orcid_is_registered_sucess(self):
        self.maxDiff = None
        xml = """
                <article>
                <front>
                    <article-meta>
                      <contrib-group>
                        <contrib contrib-type="author">
                            <contrib-id contrib-id-type="orcid">0990-0001-0058-4853</contrib-id>
                          <name>
                            <surname>VENEGAS MARTÍNEZ</surname>
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
                """

        xmltree = etree.fromstring(xml)
        contrib = list(ArticleContribs(xmltree).contribs)[0]
        obtained = list(
            ContribValidation(contrib).validate_contribs_orcid_is_registered(callable_get_data)
        )

        expected = [
            {
                "title": "Author ORCID element is registered",
                "parent": "article",
                "parent_id": None,
                "item": "contrib-id",
                "sub_item": '@contrib-id-type="orcid"',
                "validation_type": "exist",
                "response": "OK",
                "expected_value": ["0990-0001-0058-4853", "FRANCISCO VENEGAS MARTÍNEZ"],
                "got_value": ["0990-0001-0058-4853", "FRANCISCO VENEGAS MARTÍNEZ"],
                "message": "Got ['0990-0001-0058-4853', 'FRANCISCO VENEGAS MARTÍNEZ'], expected "
                "['0990-0001-0058-4853', 'FRANCISCO VENEGAS MARTÍNEZ']",
                "advice": None,
                "data": None,
            }
        ]

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

    def test_validate_authors_orcid_is_registered_fail(self):
        self.maxDiff = None
        xml = """
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
                            <contrib-id contrib-id-type="orcid">0000-3333-1238-6874</contrib-id>
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
                """

        xmltree = etree.fromstring(xml)
        contrib = list(ArticleContribs(xmltree).contribs)[0]
        obtained = list(
            ContribValidation(contrib).validate_contribs_orcid_is_registered(callable_get_data)
        )

        expected = [
            {
                "title": "Author ORCID element is registered",
                "parent": "article",
                "parent_id": None,
                "item": "contrib-id",
                "sub_item": '@contrib-id-type="orcid"',
                "validation_type": "exist",
                "response": "ERROR",
                "expected_value": ["0990-0001-0058-4853", "FRANCISCO VENEGAS MARTÍNEZ"],
                "got_value": ["0990-0001-0058-4853", "FRANCISCO VENEGAS-MARTÍNEZ"],
                "message": "Got ['0990-0001-0058-4853', 'FRANCISCO VENEGAS-MARTÍNEZ'], expected "
                "['0990-0001-0058-4853', 'FRANCISCO VENEGAS MARTÍNEZ']",
                "advice": "ORCID 0990-0001-0058-4853 is not registered to any authors",
                "data": None,
            }
        ]

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

    def test_validate_authors_orcid_is_registered_fail_empty(self):
        self.maxDiff = None
        xml = """
                <article>
                <front>
                    <article-meta>
                      <contrib-group>
                        <contrib contrib-type="author">
                            <contrib-id contrib-id-type="orcid">0990-0001-0058-4853</contrib-id>
                          <name>
                            <surname>VENEGAS MARTÍNEZ</surname>
                            <given-names>FRANCISCO</given-names>
                            <prefix>Prof</prefix>
                            <suffix>Nieto</suffix>
                          </name>
                          <xref ref-type="aff" rid="aff1"/>
                        </contrib>
                        <contrib contrib-type="author">
                            <contrib-id contrib-id-type="orcid">0000-3333-1238-6874</contrib-id>
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
                """

        xmltree = etree.fromstring(xml)
        contrib = list(ArticleContribs(xmltree).contribs)[0]
        obtained = list(
            ContribValidation(contrib).validate_contribs_orcid_is_registered(callable_get_data_empty)
        )

        expected = [
            {
                "title": "Author ORCID element is registered",
                "parent": "article",
                "parent_id": None,
                "item": "contrib-id",
                "sub_item": '@contrib-id-type="orcid"',
                "validation_type": "exist",
                "response": "ERROR",
                "expected_value": ["0990-0001-0058-4853", None],
                "got_value": ["0990-0001-0058-4853", "FRANCISCO VENEGAS MARTÍNEZ"],
                "message": "Got ['0990-0001-0058-4853', 'FRANCISCO VENEGAS MARTÍNEZ'], expected "
                "['0990-0001-0058-4853', None]",
                "advice": "ORCID 0990-0001-0058-4853 is not registered to any authors",
                "data": None,
            }
        ]

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

    def test_validate_authors_with_collab_list(self):
        self.maxDiff = None
        xml_tree = etree.fromstring(
            """
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
            """
        )

        contrib = list(ArticleContribs(xml_tree).contribs)[0]
        content_types = ArticleContribsValidation(xmltree=xml_tree, data={}).content_types
        obtained = list(ContribValidation(contrib).validate_authors_collab_list(content_types))

        self.assertEqual([], obtained)

    def test_validate_authors_without_collab_list(self):
        self.maxDiff = None
        xml_tree = etree.fromstring(
            """
            <article>
                <front>
                    <article-meta>
                        <contrib-group>
                            <contrib contrib-type="author">
                                <collab>The MARS Group</collab>
                            </contrib>
                        </contrib-group>
                    </article-meta>
                </front>
            </article>
            """
        )

        contrib = list(ArticleContribs(xml_tree).contribs)[0]
        content_types = ArticleContribsValidation(xmltree=xml_tree, data={}).content_types
        obtained = list(ContribValidation(contrib).validate_authors_collab_list(content_types))

        expected = [
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
                    'collab': 'The MARS Group',
                    'contrib_type': 'author',
                    'parent': 'article',
                    'parent_article_type': None,
                    'parent_id': None,
                    'parent_lang': None
                }
            }
        ]
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

    def test_validate(self):
        self.maxDiff = None
        xml = """
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
        """

        xmltree = etree.fromstring(xml)
        data = {
                    "credit_taxonomy_terms_and_urls": credit_taxonomy_terms_and_urls,
                    "callable_get_data": callable_get_data,
                }
        obtained = list(ArticleContribsValidation(xmltree=xmltree, data=data).validate())

        expected = [
            {
                "title": "CRediT taxonomy for contribs",
                "parent": "article",
                "parent_id": None,
                "item": "role",
                "sub_item": '@content-type="https://credit.niso.org/contributor-roles/*',
                "validation_type": "value in list",
                "response": "ERROR",
                "expected_value": [
                    '<role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>',
                    '<role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>',
                ],
                "got_value": None,
                "message": """Got None, expected ['<role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>', '<role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>']""",
                "advice": """The author FRANCISCO VENEGAS-MARTÍNEZ does not have a valid role. Provide a role from the list: ['<role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>', '<role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>']""",
                "data": {
                    "contrib_ids": {"orcid": "0990-0001-0058-4853"},
                    "contrib_name": {
                        "given-names": "FRANCISCO",
                        "prefix": "Prof",
                        "suffix": "Nieto",
                        "surname": "VENEGAS-MARTÍNEZ",
                    },
                    "contrib_type": "author",
                    "contrib_xref": [{"ref_type": "aff", "rid": "aff1", "text": None}],
                    "parent": "article",
                    "parent_article_type": None,
                    "parent_id": None,
                    "parent_lang": None,
                },
            },
            {
                "title": "Author ORCID",
                "parent": "article",
                "parent_id": None,
                "item": "contrib-id",
                "sub_item": '@contrib-id-type="orcid"',
                "validation_type": "format",
                "response": "OK",
                "expected_value": "0990-0001-0058-4853",
                "got_value": "0990-0001-0058-4853",
                "message": "Got 0990-0001-0058-4853, expected 0990-0001-0058-4853",
                "advice": None,
                "data": {
                    "contrib_ids": {"orcid": "0990-0001-0058-4853"},
                    "contrib_name": {
                        "given-names": "FRANCISCO",
                        "prefix": "Prof",
                        "suffix": "Nieto",
                        "surname": "VENEGAS-MARTÍNEZ",
                    },
                    "contrib_type": "author",
                    "contrib_xref": [{"ref_type": "aff", "rid": "aff1", "text": None}],
                    "parent": "article",
                    "parent_article_type": None,
                    "parent_id": None,
                    "parent_lang": None,
                },
            },
            {
                "title": "Author ORCID element is registered",
                "parent": "article",
                "parent_id": None,
                "item": "contrib-id",
                "sub_item": '@contrib-id-type="orcid"',
                "validation_type": "exist",
                "response": "ERROR",
                "expected_value": ["0990-0001-0058-4853", "FRANCISCO VENEGAS MARTÍNEZ"],
                "got_value": ["0990-0001-0058-4853", "FRANCISCO VENEGAS-MARTÍNEZ"],
                "message": "Got ['0990-0001-0058-4853', 'FRANCISCO VENEGAS-MARTÍNEZ'], expected "
                           "['0990-0001-0058-4853', 'FRANCISCO VENEGAS MARTÍNEZ']",
                "advice": 'ORCID 0990-0001-0058-4853 is not registered to any authors',
                "data": None,
            },
            {
                "title": "Author ORCID element is unique",
                "parent": None,
                "parent_id": None,
                "item": "contrib-id",
                "sub_item": '@contrib-id-type="orcid"',
                "validation_type": "exist/verification",
                "response": "OK",
                "expected_value": "Unique ORCID values",
                "got_value": ["0990-0001-0058-4853", "0000-3333-1238-6873"],
                "message": "Got ['0990-0001-0058-4853', '0000-3333-1238-6873'], expected Unique ORCID values",
                "advice": None,
                "data": None,
            },
            {
                "title": "CRediT taxonomy for contribs",
                "parent": "article",
                "parent_id": None,
                "item": "role",
                "sub_item": '@content-type="https://credit.niso.org/contributor-roles/*',
                "validation_type": "value in list",
                "response": "ERROR",
                "expected_value": [
                    '<role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>',
                    '<role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>',
                ],
                "got_value": None,
                "message": """Got None, expected ['<role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>', '<role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>']""",
                "advice": """The author Vanessa M. Higa does not have a valid role. Provide a role from the list: ['<role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>', '<role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>']""",
                "data": {
                    "contrib_ids": {"orcid": "0000-3333-1238-6873"},
                    "contrib_name": {"given-names": "Vanessa M.", "surname": "Higa"},
                    "contrib_type": "author",
                    "contrib_xref": [{"ref_type": "aff", "rid": "aff1", "text": "a"}],
                    "parent": "article",
                    "parent_article_type": None,
                    "parent_id": None,
                    "parent_lang": None,
                },
            },
            {
                "title": "Author ORCID",
                "parent": "article",
                "parent_id": None,
                "item": "contrib-id",
                "sub_item": '@contrib-id-type="orcid"',
                "validation_type": "format",
                "response": "OK",
                "expected_value": "0000-3333-1238-6873",
                "got_value": "0000-3333-1238-6873",
                "message": "Got 0000-3333-1238-6873, expected 0000-3333-1238-6873",
                "advice": None,
                "data": {
                    "contrib_ids": {"orcid": "0000-3333-1238-6873"},
                    "contrib_name": {"given-names": "Vanessa M.", "surname": "Higa"},
                    "contrib_type": "author",
                    "contrib_xref": [{"ref_type": "aff", "rid": "aff1", "text": "a"}],
                    "parent": "article",
                    "parent_article_type": None,
                    "parent_id": None,
                    "parent_lang": None,
                },
            },

        ]

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)