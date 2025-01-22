from unittest import TestCase

from lxml import etree

from packtools.sps.models.article_contribs import ArticleContribs
from packtools.sps.validation.article_contribs import ContribValidation, ArticleContribsValidation, CollabListValidation

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


def callable_get_unmatched_data(orcid, contrib):
    tests = {
        "0990-0001-0058-4853": {
            "data": "Autor registrado com orcid = 0990-0001-0058-4853",
            "is_valid": False,
        },

        "0000-3333-1238-6873": {
            "data": "Vanessa M. Higa",
            "is_valid": True,
        },
    }
    return tests.get(orcid)


def callable_get_matched_data(orcid, contrib):
    tests = {
        "0990-0001-0058-4853": {
            "data": "FRANCISCO VENEGAS MARTÍNEZ Nieto",
            "is_valid": True,
        },

        "0000-3333-1238-6873": {
            "data": "Vanessa M. Higa",
            "is_valid": True,
        },
    }
    return tests.get(orcid)


def callable_get_not_found_data(orcid, contrib):
    return {"data": None, "is_valid": False}


class ArticleContribsValidationTest(TestCase):
    def test_without_role(self):
        self.maxDiff = None
        xml = """
        <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" 
        dtd-version="1.0" article-type="research-article" xml:lang="pt">
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
        data = {}
        data["credit_taxonomy_terms_and_urls"] = credit_taxonomy_terms_and_urls
        data["credit_taxonomy_terms_and_urls_error_level"] = "ERROR"

        xmltree = etree.fromstring(xml)
        contrib = list(ArticleContribs(xmltree).contribs)[0]
        obtained = list(
            ContribValidation(contrib, data).validate_role()
        )

        expected = [
            {
                "title": "CRediT taxonomy",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "research-article",
                "parent_lang": "pt",
                "item": "role",
                "sub_item": '@content-type="https://credit.niso.org/contributor-roles/*',
                "validation_type": "value in list",
                "response": "ERROR",
                "expected_value": "one of ['<role "
                    'content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>\', '
                    "'<role "
                    'content-type="https://credit.niso.org/contributor-roles/data-curation/">Data '
                    "curation</role>']",
                "got_value": None,
                "message": """Got None, expected one of ['<role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>', '<role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>']""",
                "advice": """Provide the correct CRediT taxonomy: ['<role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>', '<role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>']""",
                "data": {
                    'contrib_full_name': 'Prof FRANCISCO VENEGAS-MARTÍNEZ Nieto',
                    "contrib_name": {
                        "given-names": "FRANCISCO",
                        "prefix": "Prof",
                        "suffix": "Nieto",
                        "surname": "VENEGAS-MARTÍNEZ",
                    },
                    "contrib_type": "author",
                    "contrib_xref": [{"ref_type": "aff", "rid": "aff1", "text": None}],
                    "parent": "article",
                    "parent_id": None,
                    "parent_article_type": "research-article",
                    "parent_lang": "pt",
                },
            }
        ]

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

    def test_role_and_collab_list_empty(self):
        self.maxDiff = None
        xml = """
        <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" 
        dtd-version="1.0" article-type="research-article" xml:lang="pt">
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

        data = {}
        data["credit_taxonomy_terms_and_urls"] = credit_taxonomy_terms_and_urls
        data["credit_taxonomy_terms_and_urls_error_level"] = "ERROR"
        xmltree = etree.fromstring(xml)
        contrib = list(ArticleContribs(xmltree).contribs)[0]
        obtained = list(
            ContribValidation(contrib, data).validate_role()
        )

        expected = [
            {
                "title": "CRediT taxonomy",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "research-article",
                "parent_lang": "pt",
                "item": "role",
                "sub_item": '@content-type="https://credit.niso.org/contributor-roles/*',
                "validation_type": "value in list",
                "response": "ERROR",
                "expected_value": "one of ['<role "
                    'content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>\', '
                    "'<role "
                    'content-type="https://credit.niso.org/contributor-roles/data-curation/">Data '
                    "curation</role>']",
                "got_value": '<role content-type="None">None</role>',
                "message": """Got <role content-type="None">None</role>, expected one of ['<role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>', '<role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>']""",
                "advice": """Provide the correct CRediT taxonomy: ['<role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>', '<role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>']""",
                "data": {
                    'contrib_full_name': 'Prof FRANCISCO VENEGAS-MARTÍNEZ Nieto',
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
                    "parent_id": None,
                    "parent_article_type": "research-article",
                    "parent_lang": "pt",
                },
            }
        ]

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

    def test_role_without_collab_list(self):
        self.maxDiff = None
        xml = """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" 
            dtd-version="1.0" article-type="research-article" xml:lang="pt">
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
                "title": "CRediT taxonomy",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "research-article",
                "parent_lang": "pt",
                "item": "role",
                "sub_item": '@content-type="https://credit.niso.org/contributor-roles/*',
                "validation_type": "value in list",
                "response": "ERROR",
                "got_value": '<role content-type="None">Data curation</role>',
                "expected_value": "one of ['<role "
                                  'content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>\', '
                                  "'<role "
                                  'content-type="https://credit.niso.org/contributor-roles/data-curation/">Data '
                                  "curation</role>']",
                "message": """Got <role content-type="None">Data curation</role>, expected one of ['<role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>', '<role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>']""",
                "advice": """Provide the correct CRediT taxonomy: ['<role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>', '<role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>']""",
                "data": {
                    'contrib_full_name': 'Prof FRANCISCO VENEGAS-MARTÍNEZ Nieto',
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
                    "parent_id": None,
                    "parent_article_type": "research-article",
                    "parent_lang": "pt",
                },
            }
        ]
        data = {}
        data["credit_taxonomy_terms_and_urls"] = credit_taxonomy_terms_and_urls
        data["credit_taxonomy_terms_and_urls_error_level"] = "ERROR"
        xmltree = etree.fromstring(xml)
        contrib = list(ArticleContribs(xmltree).contribs)[0]
        obtained = list(
            ContribValidation(contrib, data).validate_role()
        )

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

    def test_role_no_text_with_collab_list(self):
        self.maxDiff = None
        xml = """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" 
            dtd-version="1.0" article-type="research-article" xml:lang="pt">
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
                "title": "CRediT taxonomy",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "research-article",
                "parent_lang": "pt",
                "item": "role",
                "sub_item": '@content-type="https://credit.niso.org/contributor-roles/*',
                "validation_type": "value in list",
                "response": "ERROR",
                "got_value": '<role content-type="https://credit.niso.org/contributor-roles/data-curation/">None</role>',
                "expected_value": "one of ['<role "
                    'content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>\', '
                    "'<role "
                    'content-type="https://credit.niso.org/contributor-roles/data-curation/">Data '
                    "curation</role>']",
                "message": """Got <role content-type="https://credit.niso.org/contributor-roles/data-curation/">None</role>, expected one of ['<role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>', '<role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>']""",
                "advice": """Provide the correct CRediT taxonomy: ['<role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>', '<role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>']""",
                "data": {
                    'contrib_full_name': 'Prof FRANCISCO VENEGAS-MARTÍNEZ Nieto',
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
                    "parent_id": None,
                    "parent_article_type": "research-article",
                    "parent_lang": "pt",
                },
            }
        ]

        data = {}
        data["credit_taxonomy_terms_and_urls"] = credit_taxonomy_terms_and_urls
        data["credit_taxonomy_terms_and_urls_error_level"] = "ERROR"
        xmltree = etree.fromstring(xml)
        contrib = list(ArticleContribs(xmltree).contribs)[0]
        obtained = list(
            ContribValidation(contrib, data).validate_role()
        )

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

    def test_wrong_role_and_collab_list(self):
        self.maxDiff = None
        xml = """
        <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" 
        dtd-version="1.0" article-type="research-article" xml:lang="pt">
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
                "title": "CRediT taxonomy",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "research-article",
                "parent_lang": "pt",
                "item": "role",
                "sub_item": '@content-type="https://credit.niso.org/contributor-roles/*',
                "validation_type": "value in list",
                "response": "ERROR",
                "got_value": '<role content-type="https://credit.niso.org/contributor-roles/data-curan/">Data curation</role>',
                "expected_value": "one of ['<role "
                    'content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>\', '
                    "'<role "
                    'content-type="https://credit.niso.org/contributor-roles/data-curation/">Data '
                    "curation</role>']",
                "message": """Got <role content-type="https://credit.niso.org/contributor-roles/data-curan/">Data curation</role>, expected one of ['<role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>', '<role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>']""",
                "advice": """Provide the correct CRediT taxonomy: ['<role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>', '<role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>']""",
                "data": {
                    'contrib_full_name': 'Prof FRANCISCO VENEGAS-MARTÍNEZ Nieto',
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
                    "parent_id": None,
                    "parent_article_type": "research-article",
                    "parent_lang": "pt",
                },
            }
        ]

        data = {}
        data["credit_taxonomy_terms_and_urls"] = credit_taxonomy_terms_and_urls
        data["credit_taxonomy_terms_and_urls_error_level"] = "ERROR"
        xmltree = etree.fromstring(xml)
        contrib = list(ArticleContribs(xmltree).contribs)[0]
        obtained = list(
            ContribValidation(contrib, data).validate_role()
        )

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

    def test_success_role(self):
        self.maxDiff = None
        xml = """
        <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" 
        dtd-version="1.0" article-type="research-article" xml:lang="pt">
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
                "title": "CRediT taxonomy",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "research-article",
                "parent_lang": "pt",
                "item": "role",
                "sub_item": '@content-type="https://credit.niso.org/contributor-roles/*',
                "validation_type": "value in list",
                "response": "OK",
                "expected_value": '<role '
                                  'content-type="https://credit.niso.org/contributor-roles/data-curation/">Data '
                                  'curation</role>',
                "got_value": '<role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>',
                "message": """Got <role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>, expected one of ['<role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>', '<role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>']""",
                "advice": None,
                "data": {
                    'contrib_full_name': 'Prof FRANCISCO VENEGAS-MARTÍNEZ Nieto',
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
                    "parent_id": None,
                    "parent_article_type": "research-article",
                    "parent_lang": "pt",
                },
            }
        ]

        data = {}
        data["credit_taxonomy_terms_and_urls"] = credit_taxonomy_terms_and_urls
        data["credit_taxonomy_terms_and_urls_error_level"] = "ERROR"
        xmltree = etree.fromstring(xml)
        contrib = list(ArticleContribs(xmltree).contribs)[0]
        obtained = list(
            ContribValidation(contrib, data).validate_role()
        )

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)


class ArticleContribsValidationOrcidTest(TestCase):
    def test_validate_authors_orcid_format_fail(self):
        self.maxDiff = None
        xml = """
        <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" 
        dtd-version="1.0" article-type="research-article" xml:lang="pt">
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
        data = {
            "orcid_format_error_level": "ERROR"
        }
        obtained = list(
            ContribValidation(contrib, data).validate_orcid_format())

        expected = [
            {
                "title": "ORCID format",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "research-article",
                "parent_lang": "pt",
                "item": "contrib-id",
                "sub_item": '@contrib-id-type="orcid"',
                "validation_type": "format",
                "response": "ERROR",
                "expected_value": "valid ORCID",
                "got_value": "0990-01-58-4853",
                "message": "Got 0990-01-58-4853, expected valid ORCID",
                "advice": "Provide a valid ORCID for Prof FRANCISCO VENEGAS-MARTÍNEZ Nieto",
                "data": {
                    'contrib_full_name': 'Prof FRANCISCO VENEGAS-MARTÍNEZ Nieto',
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
                    "parent_id": None,
                    "parent_article_type": "research-article",
                    "parent_lang": "pt",
                },
            }
        ]
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

    def test_validate_authors_orcid_format_without_orcid(self):
        self.maxDiff = None
        xml = """
        <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" 
        dtd-version="1.0" article-type="research-article" xml:lang="pt">
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
        data = {
            "orcid_format_error_level": "ERROR"
        }
        obtained = list(ContribValidation(contrib, data).validate_orcid_format())

        expected = [
            {
                "title": "ORCID format",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "research-article",
                "parent_lang": "pt",
                "item": "contrib-id",
                "sub_item": '@contrib-id-type="orcid"',
                "validation_type": "format",
                "response": "ERROR",
                "expected_value": "valid ORCID",
                "got_value": None,
                "message": "Got None, expected valid ORCID",
                "advice": "Provide a valid ORCID for Prof FRANCISCO VENEGAS-MARTÍNEZ Nieto",
                "data": {
                    'contrib_full_name': 'Prof FRANCISCO VENEGAS-MARTÍNEZ Nieto',
                    "contrib_name": {
                        "given-names": "FRANCISCO",
                        "prefix": "Prof",
                        "suffix": "Nieto",
                        "surname": "VENEGAS-MARTÍNEZ",
                    },
                    "contrib_type": "author",
                    "contrib_xref": [{"ref_type": "aff", "rid": "aff1", "text": None}],
                    "parent": "article",
                    "parent_id": None,
                    "parent_article_type": "research-article",
                    "parent_lang": "pt",
                },
            }
        ]

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

    def test_validate_authors_orcid_format_success(self):
        self.maxDiff = None
        xml = """
        <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" 
        dtd-version="1.0" article-type="research-article" xml:lang="pt">
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
        data = {
            "orcid_format_error_level": "ERROR"
        }
        obtained = list(
            ContribValidation(contrib, data).validate_orcid_format())

        expected = [
            {
                "title": "ORCID format",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "research-article",
                "parent_lang": "pt",
                "item": "contrib-id",
                "sub_item": '@contrib-id-type="orcid"',
                "validation_type": "format",
                "response": "OK",
                "expected_value": "0990-0001-0058-4853",
                "got_value": "0990-0001-0058-4853",
                "message": "Got 0990-0001-0058-4853, expected 0990-0001-0058-4853",
                "advice": None,
                "data": {
                    'contrib_full_name': 'Prof FRANCISCO VENEGAS-MARTÍNEZ Nieto',
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
                    "parent_id": None,
                    "parent_article_type": "research-article",
                    "parent_lang": "pt",
                },
            }
        ]

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

    def test_validate_authors_orcid_is_unique_ok(self):
        self.maxDiff = None
        xml = """
        <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" 
        dtd-version="1.0" article-type="research-article" xml:lang="pt">
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
        data = {}
        data["orcid_is_unique_error_level"] = "ERROR"
        data["is_orcid_registered"] = callable_get_matched_data
        xmltree = etree.fromstring(xml)
        obtained = list(
            ArticleContribsValidation(xmltree, data).validate_orcid_is_unique()
        )

        expected = [
            {
                "title": "Unique ORCID",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "research-article",
                "parent_lang": "pt",
                "item": "contrib-id",
                "sub_item": '@contrib-id-type="orcid"',
                "validation_type": "uniqueness",
                "response": "OK",
                "expected_value": {'0000-3333-1238-6873': ['Vanessa M. Higa'], '0990-0001-0058-4853': ['Prof FRANCISCO VENEGAS-MARTÍNEZ Nieto']},
                "got_value": {
                    '0000-3333-1238-6873': ['Vanessa M. Higa'],
                    '0990-0001-0058-4853': ['Prof FRANCISCO VENEGAS-MARTÍNEZ Nieto']
                },
                "message": "Got {"
                           "'0990-0001-0058-4853': ['Prof FRANCISCO VENEGAS-MARTÍNEZ Nieto'], "
                           "'0000-3333-1238-6873': ['Vanessa M. Higa']"
                           "}, expected Unique ORCID values",
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
        <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" 
        dtd-version="1.0" article-type="research-article" xml:lang="pt">
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
        data = {}
        data["orcid_is_unique_error_level"] = "ERROR"
        data["is_orcid_registered"] = callable_get_matched_data
        xmltree = etree.fromstring(xml)
        obtained = list(
            ArticleContribsValidation(xmltree, data).validate_orcid_is_unique()
        )

        expected = [
            {
                "title": "Unique ORCID",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "research-article",
                "parent_lang": "pt",
                "item": "contrib-id",
                "sub_item": '@contrib-id-type="orcid"',
                "validation_type": "uniqueness",
                "response": "ERROR",
                "expected_value": "Unique ORCID values",
                "got_value": {
                    '0990-0001-0058-4853': ['Prof FRANCISCO VENEGAS-MARTÍNEZ Nieto', 'Vanessa M. Higa']
                },
                "message": "Got {"
                           "'0990-0001-0058-4853': ['Prof FRANCISCO VENEGAS-MARTÍNEZ Nieto', 'Vanessa M. Higa']"
                           "}, expected Unique ORCID values",
                "advice": "Consider replacing the following ORCIDs that are not unique: 0990-0001-0058-4853",
                "data": None,
            }
        ]

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

    def test_validate_authors_orcid_is_registered_success(self):
        self.maxDiff = None
        xml = """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" 
            dtd-version="1.0" article-type="research-article" xml:lang="pt">
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
        data = {
            "orcid_is_registered_error_level": "ERROR",
            "is_orcid_registered": callable_get_matched_data
        }
        obtained = list(
            ContribValidation(contrib, data).validate_orcid_is_registered()
        )

        expected = [
            {
                "title": "Registered ORCID",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "research-article",
                "parent_lang": "pt",
                "item": "contrib-id",
                "sub_item": '@contrib-id-type="orcid"',
                "validation_type": "registered",
                "response": "OK",
                "expected_value": 'FRANCISCO VENEGAS MARTÍNEZ Nieto',
                "got_value": 'FRANCISCO VENEGAS MARTÍNEZ Nieto',
                "message": "Got FRANCISCO VENEGAS MARTÍNEZ Nieto, expected Prof FRANCISCO VENEGAS MARTÍNEZ Nieto",
                "advice": None,
                "data": {
                    'contrib_full_name': 'Prof FRANCISCO VENEGAS MARTÍNEZ Nieto',
                    "contrib_ids": {"orcid": "0990-0001-0058-4853"},
                    "contrib_name": {
                        "given-names": "FRANCISCO",
                        "prefix": "Prof",
                        "suffix": "Nieto",
                        "surname": "VENEGAS MARTÍNEZ",
                    },
                    "contrib_type": "author",
                    "contrib_xref": [{"ref_type": "aff", "rid": "aff1", "text": None}],
                    "parent": "article",
                    "parent_id": None,
                    "parent_article_type": "research-article",
                    "parent_lang": "pt",
                },
            }
        ]

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

    def test_validate_authors_orcid_is_registered_fail(self):
        self.maxDiff = None
        xml = """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" 
            dtd-version="1.0" article-type="research-article" xml:lang="pt">
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
        data = {
            "orcid_is_registered_error_level": "ERROR",
            "is_orcid_registered": callable_get_not_found_data,
        }
        obtained = list(
            ContribValidation(contrib, data).validate_orcid_is_registered()
        )

        expected = [
            {
                "title": "Registered ORCID",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "research-article",
                "parent_lang": "pt",
                "item": "contrib-id",
                "sub_item": '@contrib-id-type="orcid"',
                "validation_type": "registered",
                "response": "ERROR",
                "expected_value": "Prof FRANCISCO VENEGAS-MARTÍNEZ Nieto",
                "got_value": None,
                "message": "Got None, expected Prof FRANCISCO VENEGAS-MARTÍNEZ Nieto",
                "advice": "Identify the correct ORCID for Prof FRANCISCO VENEGAS-MARTÍNEZ Nieto",
                "data": {
                    'contrib_full_name': 'Prof FRANCISCO VENEGAS-MARTÍNEZ Nieto',
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
                    "parent_id": None,
                    "parent_article_type": "research-article",
                    "parent_lang": "pt",
                },
            }
        ]

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

    def test_validate_authors_orcid_is_registered_fail_empty(self):
        self.maxDiff = None
        xml = """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" 
            dtd-version="1.0" article-type="research-article" xml:lang="pt">
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
        data = {
            "orcid_is_registered_error_level": "ERROR",
            "is_orcid_registered": callable_get_not_found_data
        }
        obtained = list(
            ContribValidation(contrib, data).validate_orcid_is_registered()
        )

        expected = [
            {
                "title": "Registered ORCID",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "research-article",
                "parent_lang": "pt",
                "item": "contrib-id",
                "sub_item": '@contrib-id-type="orcid"',
                "validation_type": "registered",
                "response": "ERROR",
                "expected_value": "Prof FRANCISCO VENEGAS MARTÍNEZ Nieto",
                "got_value": None,
                "message": "Got None, expected Prof FRANCISCO VENEGAS MARTÍNEZ Nieto",
                "advice": "Identify the correct ORCID for Prof FRANCISCO VENEGAS MARTÍNEZ Nieto",
                "data": {
                    'contrib_full_name': 'Prof FRANCISCO VENEGAS MARTÍNEZ Nieto',
                    "contrib_ids": {"orcid": "0990-0001-0058-4853"},
                    "contrib_name": {
                        "given-names": "FRANCISCO",
                        "prefix": "Prof",
                        "suffix": "Nieto",
                        "surname": "VENEGAS MARTÍNEZ",
                    },
                    "contrib_type": "author",
                    "contrib_xref": [{"ref_type": "aff", "rid": "aff1", "text": None}],
                    "parent": "article",
                    "parent_id": None,
                    "parent_article_type": "research-article",
                    "parent_lang": "pt",
                },
            }
        ]

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

    def test_validate_authors_with_collab_list(self):
        self.maxDiff = None
        xml_tree = etree.fromstring(
            """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" 
            dtd-version="1.0" article-type="research-article" xml:lang="pt">
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

        data = {
            "name_error_level": "ERROR",
            "collab_error_level": "ERROR",
            "collab_list_error_level": "ERROR",
        }
        validator = CollabListValidation(parent_node=xml_tree.find("."), args=data)
        obtained = list(validator.validate())
        self.assertEqual([], obtained)

    def test_validate_authors_without_collab_list(self):
        self.maxDiff = None
        xml_tree = etree.fromstring(
            """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" 
            dtd-version="1.0" article-type="research-article" xml:lang="pt">
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
        data = {
            "name_error_level": "ERROR",
            "collab_error_level": "ERROR",
            "collab_list_error_level": "ERROR",
        }
        validator = CollabListValidation(parent_node=xml_tree.find("."), args=data)
        obtained = list(validator.validate())

        expected = [
            {
                'title': 'contrib-group/contrib/name',
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "research-article",
                "parent_lang": "pt",
                'item': 'contrib-group',
                'sub_item': 'collab-list',
                'validation_type': 'match',
                'response': 'ERROR',
                'expected_value': "contrib-group[@content-type='collab-list']",
                'got_value': None,
                'message': "Got None, expected contrib-group[@content-type='collab-list']",
                'advice': "Add content-type='collab-list' to contrib-group must have contrib/name",
                'data': [{
                    'collab': 'The MARS Group',
                    'contrib_type': 'author',
                }]
            }
        ]
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

    def test_validate(self):
        self.maxDiff = None
        xml = """
        <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" 
        dtd-version="1.0" article-type="research-article" xml:lang="pt">
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
            "credit_taxonomy_terms_and_urls_error_level": "ERROR",
            "orcid_format_error_level": "ERROR",
            "orcid_is_registered_error_level": "ERROR",
            "affiliations_error_level": "ERROR",
            "name_error_level": "ERROR",
            "collab_error_level": "ERROR",
            "name_or_collab_error_level": "ERROR",
            "orcid_is_unique_error_level": "ERROR",
            "collab_list_error_level": "ERROR",
            "is_orcid_registered": callable_get_unmatched_data,
        }
        obtained = list(ArticleContribsValidation(xmltree=xmltree, data=data).validate())

        expected = [
            {
                "title": "Unique ORCID",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "research-article",
                "parent_lang": "pt",
                "item": "contrib-id",
                "sub_item": '@contrib-id-type="orcid"',
                "validation_type": "uniqueness",
                "response": "OK",
                "expected_value": {
                    '0000-3333-1238-6873': ['Vanessa M. Higa'],
                    '0990-0001-0058-4853': ['Prof FRANCISCO VENEGAS-MARTÍNEZ Nieto']},
                "got_value": {
                    '0000-3333-1238-6873': ['Vanessa M. Higa'],
                    '0990-0001-0058-4853': ['Prof FRANCISCO VENEGAS-MARTÍNEZ Nieto']
                },
                "message": "Got {"
                           "'0990-0001-0058-4853': ['Prof FRANCISCO VENEGAS-MARTÍNEZ Nieto'], "
                           "'0000-3333-1238-6873': ['Vanessa M. Higa']"
                           "}, expected Unique ORCID values",
                "advice": None,
                "data": None,
            },
            {
                "title": "CRediT taxonomy",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "research-article",
                "parent_lang": "pt",
                "item": "role",
                "sub_item": '@content-type="https://credit.niso.org/contributor-roles/*',
                "validation_type": "value in list",
                "response": "ERROR",
                "expected_value": "one of ['<role "
                    'content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>\', '
                    "'<role "
                    'content-type="https://credit.niso.org/contributor-roles/data-curation/">Data '
                    "curation</role>']",
                "got_value": None,
                "message": """Got None, expected one of ['<role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>', '<role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>']""",
                "advice": """Provide the correct CRediT taxonomy: ['<role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>', '<role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>']""",
                "data": {
                    'contrib_full_name': 'Prof FRANCISCO VENEGAS-MARTÍNEZ Nieto',
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
                    "parent_id": None,
                    "parent_article_type": "research-article",
                    "parent_lang": "pt",
                },
            },
            {
                "title": "ORCID format",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "research-article",
                "parent_lang": "pt",
                "item": "contrib-id",
                "sub_item": '@contrib-id-type="orcid"',
                "validation_type": "format",
                "response": "OK",
                "expected_value": "0990-0001-0058-4853",
                "got_value": "0990-0001-0058-4853",
                "message": "Got 0990-0001-0058-4853, expected 0990-0001-0058-4853",
                "advice": None,
                "data": {
                    'contrib_full_name': 'Prof FRANCISCO VENEGAS-MARTÍNEZ Nieto',
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
                    "parent_id": None,
                    "parent_article_type": "research-article",
                    "parent_lang": "pt",
                },
            },
            {
                "title": "Registered ORCID",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "research-article",
                "parent_lang": "pt",
                "item": "contrib-id",
                "sub_item": '@contrib-id-type="orcid"',
                "validation_type": "registered",
                "response": "ERROR",
                "expected_value": "Prof FRANCISCO VENEGAS-MARTÍNEZ Nieto",
                "got_value": "Autor registrado com orcid = 0990-0001-0058-4853",
                "message": "Got Autor registrado com orcid = 0990-0001-0058-4853, expected Prof FRANCISCO VENEGAS-MARTÍNEZ Nieto",
                "advice": "Identify the correct ORCID for Prof FRANCISCO VENEGAS-MARTÍNEZ Nieto",
                "data": {
                    'contrib_full_name': 'Prof FRANCISCO VENEGAS-MARTÍNEZ Nieto',
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
                    "parent_id": None,
                    "parent_article_type": "research-article",
                    "parent_lang": "pt",
                },
            },
            {
                'title': 'Author without affiliation',
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "research-article",
                "parent_lang": "pt",
                'item': 'contrib',
                'sub_item': 'aff',
                'validation_type': 'exist',
                'response': 'ERROR',
                'expected_value': 'affiliation',
                'got_value': None,
                'message': 'Got None, expected affiliation',
                'advice': 'provide affiliation for Prof FRANCISCO VENEGAS-MARTÍNEZ Nieto',
                'data': {
                    'contrib_name': {
                        'given-names': 'FRANCISCO',
                        'surname': 'VENEGAS-MARTÍNEZ',
                        'prefix': 'Prof',
                        'suffix': 'Nieto',
                    },
                    'contrib_full_name': 'Prof FRANCISCO VENEGAS-MARTÍNEZ Nieto',
                    'contrib_ids': {'orcid': '0990-0001-0058-4853'},
                    'contrib_type': 'author',
                    'contrib_xref': [{'ref_type': 'aff', 'rid': 'aff1', 'text': None}],
                    "parent": "article",
                    "parent_id": None,
                    "parent_article_type": "research-article",
                    "parent_lang": "pt",
                }
            },
            {
                "title": "CRediT taxonomy",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "research-article",
                "parent_lang": "pt",
                "item": "role",
                "sub_item": '@content-type="https://credit.niso.org/contributor-roles/*',
                "validation_type": "value in list",
                "response": "ERROR",
                "expected_value": "one of ['<role "
                    'content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>\', '
                    "'<role "
                    'content-type="https://credit.niso.org/contributor-roles/data-curation/">Data '
                    "curation</role>']",
                "got_value": None,
                "message": """Got None, expected one of ['<role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>', '<role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>']""",
                "advice": """Provide the correct CRediT taxonomy: ['<role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>', '<role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>']""",
                "data": {
                    'contrib_full_name': 'Vanessa M. Higa',
                    "contrib_ids": {"orcid": "0000-3333-1238-6873"},
                    "contrib_name": {"given-names": "Vanessa M.", "surname": "Higa"},
                    "contrib_type": "author",
                    "contrib_xref": [{"ref_type": "aff", "rid": "aff1", "text": "a"}],
                    "parent": "article",
                    "parent_id": None,
                    "parent_article_type": "research-article",
                    "parent_lang": "pt",
                },
            },
            {
                "title": "ORCID format",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "research-article",
                "parent_lang": "pt",
                "item": "contrib-id",
                "sub_item": '@contrib-id-type="orcid"',
                "validation_type": "format",
                "response": "OK",
                "expected_value": "0000-3333-1238-6873",
                "got_value": "0000-3333-1238-6873",
                "message": "Got 0000-3333-1238-6873, expected 0000-3333-1238-6873",
                "advice": None,
                "data": {
                    'contrib_full_name': 'Vanessa M. Higa',
                    "contrib_ids": {"orcid": "0000-3333-1238-6873"},
                    "contrib_name": {"given-names": "Vanessa M.", "surname": "Higa"},
                    "contrib_type": "author",
                    "contrib_xref": [{"ref_type": "aff", "rid": "aff1", "text": "a"}],
                    "parent": "article",
                    "parent_id": None,
                    "parent_article_type": "research-article",
                    "parent_lang": "pt",
                },
            },
        ]

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

    def test_validate_unique_orcid_for_authors_with_same_name(self):
        self.maxDiff = None
        xml = """
        <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" 
        dtd-version="1.0" article-type="research-article" xml:lang="pt">
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
                    </contrib-group>
                </article-meta>
            </front>
            <sub-article article-type="translation" id="01" xml:lang="en">
                <front-stub>
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
                    </contrib-group>
                </front-stub>
            </sub-article>
        </article>
        """
        data = {
            "orcid_is_unique_error_level": "ERROR",
            "is_orcid_registered": callable_get_matched_data
        }
        xmltree = etree.fromstring(xml)
        obtained = list(
            ArticleContribsValidation(xmltree, data).validate_orcid_is_unique()
        )

        expected = [
            {
                "title": "Unique ORCID",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "research-article",
                "parent_lang": "pt",
                "item": "contrib-id",
                "sub_item": '@contrib-id-type="orcid"',
                "validation_type": "uniqueness",
                "response": "OK",
                "expected_value": {'0990-0001-0058-4853': ['Prof FRANCISCO VENEGAS-MARTÍNEZ Nieto']},
                "got_value": {
                    '0990-0001-0058-4853': [
                        'Prof FRANCISCO VENEGAS-MARTÍNEZ Nieto'
                    ]
                },
                "message": "Got {"
                           "'0990-0001-0058-4853': ["
                           "'Prof FRANCISCO VENEGAS-MARTÍNEZ Nieto'"
                           "]}, expected Unique ORCID values",
                "advice": None,
                "data": None,
            }
        ]

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

    def test_validate_unique_orcid_for_authors_with_different_names(self):
        self.maxDiff = None
        xml = """
        <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" 
        dtd-version="1.0" article-type="research-article" xml:lang="pt">
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
                    </contrib-group>
                </article-meta>
            </front>
            <sub-article article-type="translation" id="01" xml:lang="en">
                <front-stub>
                    <contrib-group>
                        <contrib contrib-type="author">
                            <contrib-id contrib-id-type="orcid">0990-0001-0058-4853</contrib-id>
                            <name>
                                <surname>VENEGAS-MARTÍNEZ</surname>
                                <given-names>FRANCISCO</given-names>
                            </name>
                            <xref ref-type="aff" rid="aff1"/>
                        </contrib>
                    </contrib-group>
                </front-stub>
            </sub-article>
        </article>
        """
        data = {
            "orcid_is_unique_error_level": "ERROR",
            "is_orcid_registered": callable_get_matched_data
        }
        xmltree = etree.fromstring(xml)
        obtained = list(
            ArticleContribsValidation(xmltree, data).validate_orcid_is_unique()
        )

        expected = [
            {
                "title": "Unique ORCID",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "research-article",
                "parent_lang": "pt",
                "item": "contrib-id",
                "sub_item": '@contrib-id-type="orcid"',
                "validation_type": "uniqueness",
                "response": "ERROR",
                "expected_value": "Unique ORCID values",
                "got_value": {
                    '0990-0001-0058-4853': [
                        'FRANCISCO VENEGAS-MARTÍNEZ',
                        'Prof FRANCISCO VENEGAS-MARTÍNEZ Nieto'
                    ]
                },
                "message": "Got {'0990-0001-0058-4853': ['FRANCISCO VENEGAS-MARTÍNEZ', 'Prof "
                           "FRANCISCO VENEGAS-MARTÍNEZ Nieto']}, expected Unique ORCID values",
                "advice": 'Consider replacing the following ORCIDs that are not unique: 0990-0001-0058-4853',
                "data": None,
            }
        ]

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)


class ArticleAuthorsValidationAff(TestCase):
    def test_validate_authors_affiliations_success(self):
        self.maxDiff = None
        xml = """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" 
            dtd-version="1.0" article-type="research-article" xml:lang="pt">
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
                        <aff id="aff1">
                            <label>I</label>
                            <institution content-type="orgname">Secretaria Municipal de Saúde de Belo Horizonte</institution>
                            <addr-line>
                                <named-content content-type="city">Belo Horizonte</named-content>
                                <named-content content-type="state">MG</named-content>
                            </addr-line>
                            <country>Brasil</country>
                            <institution content-type="original">Secretaria Municipal de Saúde de Belo Horizonte. Belo Horizonte, MG, Brasil</institution>
                        </aff>
                        <aff id="aff2">
                            <label>II</label>
                            <institution content-type="orgdiv1">Faculdade de Medicina</institution>
                            <institution content-type="orgname">Universidade Federal de Minas Gerais</institution>
                            <addr-line>
                                <named-content content-type="city">Belo Horizonte</named-content>
                                <named-content content-type="state">MG</named-content>
                            </addr-line>
                            <country>Brasil</country>
                            <institution content-type="original">Grupo de Pesquisas em Epidemiologia e Avaliação em Saúde. Faculdade de Medicina. Universidade Federal de Minas Gerais. Belo Horizonte, MG, Brasil</institution>
                        </aff>
                    </article-meta>
                </front>
            </article>
            """

        xmltree = etree.fromstring(xml)
        contrib = list(ArticleContribs(xmltree).contribs)[0]
        data = {
            "affiliations_error_level": "ERROR"
        }
        obtained = list(ContribValidation(contrib, data).validate_affiliations())
        self.assertListEqual(obtained, [])

    def test_validate_authors_affiliations_fail(self):
        self.maxDiff = None
        xml = """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" 
            dtd-version="1.0" article-type="research-article" xml:lang="pt">
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
            """

        xmltree = etree.fromstring(xml)
        contrib = list(ArticleContribs(xmltree).contribs)[0]
        data = {
            "affiliations_error_level": "ERROR"
        }
        obtained = list(ContribValidation(contrib, data).validate_affiliations())
        expected = [
            {
                'title': 'Author without affiliation',
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "research-article",
                "parent_lang": "pt",
                'item': 'contrib',
                'sub_item': 'aff',
                'validation_type': 'exist',
                'response': 'ERROR',
                'expected_value': 'affiliation',
                'got_value': None,
                'message': 'Got None, expected affiliation',
                'advice': 'provide affiliation for FRANCISCO VENEGAS-MARTÍNEZ',
                'data': {
                    'contrib_full_name': 'FRANCISCO VENEGAS-MARTÍNEZ',
                    'contrib_name': {
                        'given-names': 'FRANCISCO',
                        'surname': 'VENEGAS-MARTÍNEZ'
                    },
                    'contrib_type': 'author',
                    'contrib_xref': [{'ref_type': 'aff', 'rid': 'aff1', 'text': None}],
                    "parent": "article",
                    "parent_id": None,
                    "parent_article_type": "research-article",
                    "parent_lang": "pt",
                }
            }
        ]
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)
