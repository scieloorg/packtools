from unittest import TestCase
from unittest.mock import MagicMock, Mock, patch

from lxml import etree

from packtools.sps.models.article_contribs import XMLContribs
from packtools.sps.validation.article_contribs import (
    CollabListValidation,
    ContribRoleValidation,
    ContribValidation,
    XMLContribsValidation,
)

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
            "status": "not registered",
        },
        "0000-3333-1238-6873": {
            "data": "Vanessa M. Higa",
            "status": "registered",
        },
    }
    return tests.get(orcid)


def callable_get_matched_data(orcid, contrib):
    tests = {
        "0990-0001-0058-4853": {
            "data": "FRANCISCO VENEGAS MARTÍNEZ Nieto",
            "status": "registered",
        },
        "0000-3333-1238-6873": {
            "data": "Vanessa M. Higa",
            "status": "registered",
        },
    }
    return tests.get(orcid)


def callable_get_not_found_data(orcid, contrib):
    return {"data": None, "status": "not registered"}


class TestContribRoleValidation(TestCase):
    def setUp(self):
        self.credit_taxonomy = [
            {
                "term": "Conceptualization",
                "uri": "https://credit.niso.org/contributor-roles/conceptualization/",
            },
            {
                "term": "Data curation",
                "uri": "https://credit.niso.org/contributor-roles/data-curation/",
            },
        ]

        self.params = {
            "credit_taxonomy_terms_and_urls": self.credit_taxonomy,
            "credit_taxonomy_terms_and_urls_error_level": "ERROR",
        }

        # Mock do contrib com nome para mensagens de erro
        self.contrib = {"contrib_full_name": "Albert Einstein"}

    def test_validate_credit_invalid_uri(self):
        """Testa validação com URI inválida"""
        contrib_role = {
            "content-type": "https://invalid-uri/wrong-role/",
            "text": "Wrong Role",
        }

        validator = ContribRoleValidation(
            self.contrib, contrib_role, self.params
        )
        results = list(validator.validate_credit())

        self.assertEqual(len(results), 1)
        result = results[0]

        self.assertEqual(result["title"], "CRediT taxonomy URI")
        self.assertEqual(result["response"], "ERROR")
        self.assertEqual(result["got_value"], "https://invalid-uri/wrong-role/")
        self.assertEqual(
            result["expected_value"],
            {
                "https://credit.niso.org/contributor-roles/conceptualization/",
                "https://credit.niso.org/contributor-roles/data-curation/",
            },
        )
        self.assertIn(
            "Provide the correct role/@content-type", result["advice"]
        )

    def test_validate_credit_valid_uri_wrong_text(self):
        """Testa validação com URI válida mas texto incorreto"""
        contrib_role = {
            "content-type": "https://credit.niso.org/contributor-roles/conceptualization/",
            "text": "Wrong Text",
        }

        validator = ContribRoleValidation(
            self.contrib, contrib_role, self.params
        )
        results = list(validator.validate_credit())

        self.assertEqual(len(results), 1)
        result = results[0]

        self.assertEqual(result["title"], "CRediT taxonomy term")
        self.assertEqual(result["response"], "ERROR")
        self.assertEqual(result["got_value"], "Wrong Text")
        self.assertEqual(result["expected_value"], "Conceptualization")
        self.assertIn("Check the correct role", result["advice"])

    def test_validate_credit_valid_uri_correct_text(self):
        """Testa validação com URI e texto corretos"""
        contrib_role = {
            "content-type": "https://credit.niso.org/contributor-roles/conceptualization/",
            "text": "Conceptualization",
        }

        validator = ContribRoleValidation(
            self.contrib, contrib_role, self.params
        )
        results = list(validator.validate_credit())

        # Não deve gerar nenhum resultado pois está tudo correto
        self.assertEqual(len(list(results)), 0)

    def test_validate_credit_no_content_type(self):
        """Testa validação sem content-type"""
        contrib_role = {"text": "Some Text"}

        validator = ContribRoleValidation(
            self.contrib, contrib_role, self.params
        )
        results = list(validator.validate_credit())

        self.assertEqual(len(results), 1)
        result = results[0]

        self.assertEqual(result["title"], "CRediT taxonomy URI")
        self.assertEqual(result["response"], "ERROR")
        self.assertEqual(result["got_value"], None)
        self.assertEqual(
            result["expected_value"],
            {
                "https://credit.niso.org/contributor-roles/conceptualization/",
                "https://credit.niso.org/contributor-roles/data-curation/",
            },
        )

    def test_validate_credit_no_text(self):
        """Testa validação sem text mas com URI válida"""
        contrib_role = {
            "content-type": "https://credit.niso.org/contributor-roles/conceptualization/"
        }

        validator = ContribRoleValidation(
            self.contrib, contrib_role, self.params
        )
        results = list(validator.validate_credit())

        self.assertEqual(len(results), 1)
        result = results[0]

        self.assertEqual(result["title"], "CRediT taxonomy term")
        self.assertEqual(result["response"], "ERROR")
        self.assertEqual(result["got_value"], None)
        self.assertEqual(result["expected_value"], "Conceptualization")

    def test_validate_credit_empty_role(self):
        """Testa validação com role vazio"""
        contrib_role = {}

        validator = ContribRoleValidation(
            self.contrib, contrib_role, self.params
        )
        results = list(validator.validate_credit())

        self.assertEqual(len(results), 1)
        result = results[0]

        self.assertEqual(result["title"], "CRediT taxonomy URI")
        self.assertEqual(result["response"], "ERROR")
        self.assertEqual(result["got_value"], None)

    def test_validate_credit_case_sensitive(self):
        """Testa validação sensível a maiúsculas/minúsculas"""
        contrib_role = {
            "content-type": "https://credit.niso.org/contributor-roles/conceptualization/",
            "text": "CONCEPTUALIZATION",  # Texto em maiúsculas
        }

        validator = ContribRoleValidation(
            self.contrib, contrib_role, self.params
        )
        results = list(validator.validate_credit())

        self.assertEqual(len(results), 1)
        result = results[0]

        self.assertEqual(result["title"], "CRediT taxonomy term")
        self.assertEqual(result["response"], "ERROR")
        self.assertEqual(result["got_value"], "CONCEPTUALIZATION")
        self.assertEqual(result["expected_value"], "Conceptualization")

    def test_validate_credit_correct_text_and_absent_uri(self):
        """Testa validação sensível a maiúsculas/minúsculas"""
        contrib_role = {
            "content-type": None,
            "text": "Conceptualization",  # Texto em maiúsculas
        }

        validator = ContribRoleValidation(
            self.contrib, contrib_role, self.params
        )
        results = list(validator.validate_credit())

        self.assertEqual(len(results), 1)
        result = results[0]

        self.assertEqual(result["title"], "CRediT taxonomy URI")
        self.assertEqual(result["response"], "ERROR")
        self.assertEqual(result["got_value"], None)
        self.assertEqual(
            result["expected_value"],
            "ttps://credit.niso.org/contributor-roles/conceptualization/",
        )


class ContribsValidationOrcidTest(TestCase):
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
        contrib = list(XMLContribs(xmltree).contribs)[0]
        data = {"orcid_format_error_level": "ERROR"}
        obtained = list(
            ContribValidation(contrib, data).validate_orcid_format()
        )

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
                    "contrib_full_name": "Prof FRANCISCO VENEGAS-MARTÍNEZ Nieto",
                    "contrib_ids": {"orcid": "0990-01-58-4853"},
                    "contrib_name": {
                        "given-names": "FRANCISCO",
                        "prefix": "Prof",
                        "suffix": "Nieto",
                        "surname": "VENEGAS-MARTÍNEZ",
                    },
                    "contrib_type": "author",
                    "contrib_xref": [
                        {"ref_type": "aff", "rid": "aff1", "text": None}
                    ],
                    "parent": "article",
                    "parent_id": None,
                    "parent_article_type": "research-article",
                    "parent_lang": "pt",
                },
            }
        ]
        self.assertEqual(len(obtained), 1)

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
        contrib = list(XMLContribs(xmltree).contribs)[0]
        data = {"orcid_format_error_level": "ERROR"}
        obtained = list(
            ContribValidation(contrib, data).validate_orcid_format()
        )

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
                    "contrib_full_name": "Prof FRANCISCO VENEGAS-MARTÍNEZ Nieto",
                    "contrib_name": {
                        "given-names": "FRANCISCO",
                        "prefix": "Prof",
                        "suffix": "Nieto",
                        "surname": "VENEGAS-MARTÍNEZ",
                    },
                    "contrib_type": "author",
                    "contrib_xref": [
                        {"ref_type": "aff", "rid": "aff1", "text": None}
                    ],
                    "parent": "article",
                    "parent_id": None,
                    "parent_article_type": "research-article",
                    "parent_lang": "pt",
                },
            }
        ]

        self.assertEqual(len(obtained), 1)

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
        contrib = list(XMLContribs(xmltree).contribs)[0]
        data = {"orcid_format_error_level": "ERROR"}
        obtained = list(
            ContribValidation(contrib, data).validate_orcid_format()
        )
        self.assertEqual(len(obtained), 0)

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
            XMLContribsValidation(xmltree, data).validate_orcid_is_unique()
        )
        self.assertEqual([], obtained)

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
            XMLContribsValidation(xmltree, data).validate_orcid_is_unique()
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
                    "0990-0001-0058-4853": [
                        "Prof FRANCISCO VENEGAS-MARTÍNEZ Nieto",
                        "Vanessa M. Higa",
                    ]
                },
                "message": "Got {"
                "'0990-0001-0058-4853': ['Prof FRANCISCO VENEGAS-MARTÍNEZ Nieto', 'Vanessa M. Higa']"
                "}, expected Unique ORCID values",
                "advice": "Consider replacing the following ORCIDs that are not unique: 0990-0001-0058-4853",
                "data": None,
            }
        ]

        self.assertEqual(len(obtained), 1)

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
        contrib = list(XMLContribs(xmltree).contribs)[0]
        data = {
            "orcid_is_registered_error_level": "ERROR",
            "is_orcid_registered": callable_get_matched_data,
        }
        obtained = list(
            ContribValidation(contrib, data).validate_orcid_is_registered()
        )
        self.assertEqual(len(obtained), 0)

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
        contrib = list(XMLContribs(xmltree).contribs)[0]
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
                "expected_value": "registered",
                "got_value": "not registered",
                "message": "Got not registered, expected registered",
                "advice": "Identify the correct ORCID for Prof FRANCISCO VENEGAS-MARTÍNEZ Nieto",
                "data": {"data": None, "status": "not registered"},
            }
        ]

        self.assertEqual(len(obtained), 1)

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
        contrib = list(XMLContribs(xmltree).contribs)[0]
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
                "expected_value": "registered",
                "got_value": "not registered",
                "message": "Got not registered, expected registered",
                "advice": "Identify the correct ORCID for Prof FRANCISCO VENEGAS MARTÍNEZ Nieto",
                "data": {"data": None, "status": "not registered"},
            }
        ]

        self.assertEqual(len(obtained), 1)

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
            "contrib_role_specific_use_list": [],
            "contrib_role_specific_use_error_level": [],
        }
        validator = CollabListValidation(xml_tree.find("."), data)
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
            "contrib_role_specific_use_list": [],
            "contrib_role_specific_use_error_level": [],
        }
        validator = CollabListValidation(xml_tree.find("."), data)
        obtained = list(validator.validate())

        expected = [
            {
                "title": "contrib-group/contrib/name",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "research-article",
                "parent_lang": "pt",
                "item": "contrib-group",
                "sub_item": "collab-list",
                "validation_type": "match",
                "response": "ERROR",
                "expected_value": "contrib-group[@content-type='collab-list']",
                "got_value": None,
                "message": "Got None, expected contrib-group[@content-type='collab-list']",
                "advice": "Add content-type='collab-list' to contrib-group which has contrib/name",
                "data": [
                    {
                        "collab": "The MARS Group",
                        "contrib_type": "author",
                    }
                ],
            }
        ]
        self.assertEqual(len(obtained), 1)
        self.assertEqual(
            "Add content-type='collab-list' to contrib-group which has contrib/name",
            obtained[0]["advice"],
        )

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
            "is_orcid_registered": callable_get_matched_data,
        }
        xmltree = etree.fromstring(xml)
        obtained = list(
            XMLContribsValidation(xmltree, data).validate_orcid_is_unique()
        )
        self.assertEqual(len(obtained), 1)
        self.assertEqual(
            "ORCID must be unique. 0990-0001-0058-4853 is assigned to ['FRANCISCO VENEGAS-MARTÍNEZ', 'Prof FRANCISCO VENEGAS-MARTÍNEZ Nieto']",
            obtained[0]["advice"],
        )


class TestContribRoleValidation(TestCase):
    def setUp(self):
        self.credit_taxonomy = [
            {
                "term": "Conceptualization",
                "uri": "https://credit.niso.org/contributor-roles/conceptualization/",
            },
            {
                "term": "Data curation",
                "uri": "https://credit.niso.org/contributor-roles/data-curation/",
            },
        ]

        self.params = {
            "credit_taxonomy_terms_and_urls": self.credit_taxonomy,
            "credit_taxonomy_terms_and_urls_error_level": "ERROR",
        }

        # Mock do contrib com nome para mensagens de erro
        self.contrib = {"contrib_full_name": "Albert Einstein"}

    def test_validate_credit_invalid_uri(self):
        """Testa validação com URI inválida"""
        contrib_role = {
            "content-type": "https://invalid-uri/wrong-role/",
            "text": "Wrong Role",
        }

        validator = ContribRoleValidation(
            self.contrib, contrib_role, self.params
        )
        results = list(validator.validate_credit())

        self.assertEqual(len(results), 1)
        result = results[0]

        self.assertEqual(result["title"], "CRediT taxonomy URI")
        self.assertEqual(result["response"], "ERROR")
        self.assertEqual(result["got_value"], "https://invalid-uri/wrong-role/")
        self.assertEqual(
            result["expected_value"],
            "one of ['https://credit.niso.org/contributor-roles/conceptualization/', 'https://credit.niso.org/contributor-roles/data-curation/']",
        )
        self.assertEqual(
            """Provide the correct CRediT taxonomy URI (role/@content-type): ['https://credit.niso.org/contributor-roles/conceptualization/', 'https://credit.niso.org/contributor-roles/data-curation/']""",
            result["advice"],
        )

    def test_validate_credit_valid_uri_wrong_text(self):
        """Testa validação com URI válida mas texto incorreto"""
        contrib_role = {
            "content-type": "https://credit.niso.org/contributor-roles/conceptualization/",
            "text": "Wrong Text",
        }

        validator = ContribRoleValidation(
            self.contrib, contrib_role, self.params
        )
        results = list(validator.validate_credit())

        self.assertEqual(len(results), 1)
        result = results[0]

        self.assertEqual(result["title"], "CRediT taxonomy term")
        self.assertEqual(result["response"], "ERROR")
        self.assertEqual(result["got_value"], "Wrong Text")
        self.assertEqual(result["expected_value"], "Conceptualization")
        self.assertIn(
            "Check the CRediT taxonomy term (role) for https://credit.niso.org/contributor-roles/conceptualization/",
            result["advice"],
        )

    def test_validate_credit_valid_uri_correct_text(self):
        """Testa validação com URI e texto corretos"""
        contrib_role = {
            "content-type": "https://credit.niso.org/contributor-roles/conceptualization/",
            "text": "Conceptualization",
        }

        validator = ContribRoleValidation(
            self.contrib, contrib_role, self.params
        )
        results = list(validator.validate_credit())

        # Não deve gerar nenhum resultado pois está tudo correto
        self.assertEqual(len(list(results)), 0)

    def test_validate_credit_no_content_type(self):
        """Testa validação sem content-type"""
        contrib_role = {"text": "Some Text"}

        validator = ContribRoleValidation(
            self.contrib, contrib_role, self.params
        )
        results = list(validator.validate_credit())

        self.assertEqual(len(results), 1)
        result = results[0]

        self.assertEqual(result["title"], "CRediT taxonomy URI")
        self.assertEqual(result["response"], "ERROR")
        self.assertEqual(result["got_value"], None)
        self.assertEqual(
            result["expected_value"],
            "one of ['https://credit.niso.org/contributor-roles/conceptualization/', 'https://credit.niso.org/contributor-roles/data-curation/']",
        )

    def test_validate_credit_no_text(self):
        """Testa validação sem text mas com URI válida"""
        contrib_role = {
            "content-type": "https://credit.niso.org/contributor-roles/conceptualization/"
        }

        validator = ContribRoleValidation(
            self.contrib, contrib_role, self.params
        )
        results = list(validator.validate_credit())

        self.assertEqual(len(results), 1)
        result = results[0]

        self.assertEqual(result["title"], "CRediT taxonomy term")
        self.assertEqual(result["response"], "ERROR")
        self.assertEqual(result["got_value"], None)
        self.assertEqual(result["expected_value"], "Conceptualization")

    def test_validate_credit_empty_role(self):
        """Testa validação com role vazio"""
        contrib_role = {}

        validator = ContribRoleValidation(
            self.contrib, contrib_role, self.params
        )
        results = list(validator.validate_credit())

        self.assertEqual(len(results), 1)
        result = results[0]

        self.assertEqual(result["title"], "CRediT taxonomy URI")
        self.assertEqual(result["response"], "ERROR")
        self.assertEqual(result["got_value"], None)

    def test_validate_credit_case_sensitive(self):
        """Testa validação sensível a maiúsculas/minúsculas"""
        contrib_role = {
            "content-type": "https://credit.niso.org/contributor-roles/conceptualization/",
            "text": "CONCEPTUALIZATION",  # Texto em maiúsculas
        }

        validator = ContribRoleValidation(
            self.contrib, contrib_role, self.params
        )
        results = list(validator.validate_credit())

        self.assertEqual(len(results), 1)
        result = results[0]

        self.assertEqual(result["title"], "CRediT taxonomy term")
        self.assertEqual(result["response"], "ERROR")
        self.assertEqual(result["got_value"], "CONCEPTUALIZATION")
        self.assertEqual(result["expected_value"], "Conceptualization")

    def test_validate_role_specific_use_valid(self):
        """Testa specific-use com valor válido"""
        self.params.update(
            {
                "contrib_role_specific_use_list": ["reviewer", "translator"],
                "contrib_role_specific_use_error_level": "ERROR",
            }
        )

        contrib_role = {"specific-use": "reviewer"}

        validator = ContribRoleValidation(
            self.contrib, contrib_role, self.params
        )
        results = list(validator.validate_role_specific_use())

        # Não deve gerar nenhum resultado pois o valor é válido
        self.assertEqual(len(results), 0)

    def test_validate_role_specific_use_invalid(self):
        """Testa specific-use com valor inválido"""
        self.params.update(
            {
                "contrib_role_specific_use_list": ["reviewer", "translator"],
                "contrib_role_specific_use_error_level": "ERROR",
            }
        )

        contrib_role = {"specific-use": "invalid_role"}

        validator = ContribRoleValidation(
            self.contrib, contrib_role, self.params
        )
        results = list(validator.validate_role_specific_use())

        self.assertEqual(len(results), 1)
        result = results[0]

        self.assertEqual(result["title"], "specific-use")
        self.assertEqual(result["response"], "ERROR")
        self.assertEqual(result["got_value"], "invalid_role")
        self.assertEqual(
            result["expected_value"], "one of ['reviewer', 'translator']"
        )
        self.assertIn(
            "Provide the correct role/@specific-use", result["advice"]
        )

    def test_validate_role_specific_use_empty_list(self):
        """Testa specific-use com lista vazia de valores permitidos"""
        self.params.update(
            {
                "contrib_role_specific_use_list": ["somevalue"],
                "contrib_role_specific_use_error_level": "ERROR",
            }
        )

        contrib_role = {"specific-use": "any_value"}

        validator = ContribRoleValidation(
            self.contrib, contrib_role, self.params
        )
        results = list(validator.validate_role_specific_use())

        self.assertEqual(len(results), 1)
        result = results[0]

        self.assertEqual(result["response"], "ERROR")
        self.assertEqual(result["got_value"], "any_value")
        self.assertEqual(result["expected_value"], "one of ['somevalue']")

    def test_validate_role_specific_use_missing(self):
        """Testa quando specific-use está ausente"""
        self.params.update(
            {
                "contrib_role_specific_use_list": ["reviewer", "translator"],
                "contrib_role_specific_use_error_level": "ERROR",
            }
        )

        contrib_role = {}  # Sem specific-use

        validator = ContribRoleValidation(
            self.contrib, contrib_role, self.params
        )
        results = list(validator.validate_role_specific_use())

        self.assertEqual(len(results), 1)
        result = results[0]

        self.assertEqual(result["response"], "ERROR")
        self.assertEqual(result["got_value"], None)
        self.assertEqual(
            result["expected_value"], "one of ['reviewer', 'translator']"
        )

    def test_validate_role_specific_use_none(self):
        """Testa quando specific-use é None"""
        self.params.update(
            {
                "contrib_role_specific_use_list": ["reviewer", "translator"],
                "contrib_role_specific_use_error_level": "ERROR",
            }
        )

        contrib_role = {"specific-use": None}

        validator = ContribRoleValidation(
            self.contrib, contrib_role, self.params
        )
        results = list(validator.validate_role_specific_use())

        self.assertEqual(len(results), 1)
        result = results[0]

        self.assertEqual(result["response"], "ERROR")
        self.assertEqual(result["got_value"], None)
        self.assertEqual(
            result["expected_value"], "one of ['reviewer', 'translator']"
        )

    def test_validate_role_specific_use_different_error_level(self):
        """Testa specific-use com nível de erro diferente"""
        self.params.update(
            {
                "contrib_role_specific_use_list": ["reviewer", "translator"],
                "contrib_role_specific_use_error_level": "WARNING",  # Diferente erro nível
            }
        )

        contrib_role = {"specific-use": "invalid_role"}

        validator = ContribRoleValidation(
            self.contrib, contrib_role, self.params
        )
        results = list(validator.validate_role_specific_use())

        self.assertEqual(len(results), 1)
        result = results[0]

        self.assertEqual(
            result["response"], "WARNING"
        )  # Deve usar o nível definido
        self.assertEqual(result["got_value"], "invalid_role")
        self.assertEqual(
            result["expected_value"], "one of ['reviewer', 'translator']"
        )

    def test_validate_role_specific_use_case_sensitive(self):
        """Testa sensibilidade a maiúsculas/minúsculas em specific-use"""
        self.params.update(
            {
                "contrib_role_specific_use_list": ["reviewer", "translator"],
                "contrib_role_specific_use_error_level": "ERROR",
            }
        )

        contrib_role = {"specific-use": "REVIEWER"}  # Maiúsculas

        validator = ContribRoleValidation(
            self.contrib, contrib_role, self.params
        )
        results = list(validator.validate_role_specific_use())

        self.assertEqual(len(results), 1)
        result = results[0]

        self.assertEqual(result["response"], "ERROR")
        self.assertEqual(result["got_value"], "REVIEWER")
        self.assertEqual(
            result["expected_value"], "one of ['reviewer', 'translator']"
        )


class TestXMLContribsValidation(TestCase):
    def setUp(self):
        self.credit_taxonomy_terms_and_urls = [
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
                    "status": "not registered",
                },
                "0000-3333-1238-6873": {
                    "data": "Vanessa M. Higa",
                    "status": "registered",
                },
            }
            return tests.get(orcid)

        self.params = {
            "credit_taxonomy_terms_and_urls": self.credit_taxonomy_terms_and_urls,
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
            "contrib_role_specific_use_list": [],
            "contrib_role_specific_use_error_level": [],
            "contrib_role_error_level": "ERROR",
        }

        self.xml = """
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
        self.xmltree = etree.fromstring(self.xml)
        self.validator = XMLContribsValidation(self.xmltree, self.params)

    def test_validate_orcid_format(self):
        """Test ORCID format validation"""
        results = list(self.validator.validate())
        orcid_format_results = [
            r for r in results if r["title"] == "ORCID format"
        ]

        # Deve haver dois resultados de validação de formato de ORCID
        self.assertEqual(len(orcid_format_results), 0)

    def test_validate_orcid_registration(self):
        """Test ORCID registration validation"""
        results = list(self.validator.validate())
        orcid_reg_results = [
            r for r in results if r["title"] == "Registered ORCID"
        ]

        # Deve haver dois resultados de validação de registro de ORCID
        self.assertEqual(len(orcid_reg_results), 1)

        # O primeiro ORCID não está registrado
        first_result = orcid_reg_results[0]
        self.assertEqual(first_result["response"], "ERROR")
        self.assertEqual(first_result["got_value"], "not registered")
        self.assertEqual(first_result["expected_value"], "registered")
        self.assertEqual(
            first_result["advice"],
            "Identify the correct ORCID for Prof FRANCISCO VENEGAS-MARTÍNEZ Nieto",
        )

    def test_validate_affiliations(self):
        """Test affiliation validation"""
        results = list(self.validator.validate())
        aff_results = [
            r for r in results if r["title"] == "Required affiliation"
        ]

        # Deve haver dois resultados de validação de afiliação (um para cada autor)
        self.assertEqual(len(aff_results), 2)

        # Ambos os autores têm xref para afiliação, mas como não há elementos aff,
        # a validação deve falhar com ERROR
        for i, result in enumerate(aff_results):
            author_name = (
                "Prof FRANCISCO VENEGAS-MARTÍNEZ Nieto"
                if i == 0
                else "Vanessa M. Higa"
            )
            self.assertEqual(result["response"], "ERROR")
            self.assertEqual(result["got_value"], None)
            self.assertEqual(result["expected_value"], "affiliation")
            self.assertEqual(
                result["advice"], f"provide affiliation for {author_name}"
            )

    def test_validate_name_or_collab(self):
        """Test name/collab validation"""
        results = list(self.validator.validate())
        name_results = [r for r in results if r["title"] == "name or collab"]

        # Não deve haver erros de name/collab pois ambos os autores têm elemento name
        self.assertEqual(len(name_results), 0)

    def test_validate_role(self):
        """Test role validation"""
        results = list(self.validator.validate())
        role_results = [r for r in results if r["title"] == "role"]

        # Deve haver dois resultados (um para cada autor) indicando ausência de role
        self.assertEqual(len(role_results), 2)

        for result in role_results:
            self.assertEqual(result["response"], "ERROR")
            self.assertEqual(result["got_value"], None)
            self.assertEqual(result["expected_value"], "contrib/role")
            self.assertEqual(result["advice"], "Provide contrib/role")

    def test_validate_orcid_uniqueness(self):
        """Test ORCID uniqueness validation"""
        results = list(self.validator.validate())
        unique_results = [r for r in results if r["title"] == "Unique ORCID"]

        # Não deve haver erro de unicidade pois os ORCIDs são diferentes
        self.assertEqual(len(unique_results), 0)

    @patch("packtools.sps.validation.article_contribs.TextContribsValidation")
    def test_validate_calls_all_methods(self, mock_text_contribs_validation):
        """Test if validate method calls all other validation methods"""

        # Mock para ContribValidation
        mock_contrib_validation = Mock()
        mock_contrib_validation.validate.return_value = []

        # Mock para XMLContribsValidation
        validator = XMLContribsValidation(self.xmltree, self.params)
        validator.validate_orcid_is_unique = Mock(return_value=[])

        # Configure o mock do TextContribsValidation
        mock_instance = mock_text_contribs_validation.return_value
        mock_instance.validate.return_value = []

        # Executa validate
        list(validator.validate())

        # Verifica se validate_orcid_is_unique foi chamado
        validator.validate_orcid_is_unique.assert_called_once()

        # Verifica se TextContribsValidation foi instanciado com os parâmetros corretos
        mock_text_contribs_validation.assert_called_once_with(
            self.xmltree.find("."), self.params
        )

        # Verifica se o método validate do TextContribsValidation foi chamado
        mock_instance.validate.assert_called_once()


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
        contrib = list(XMLContribs(xmltree).contribs)[0]
        data = {"affiliations_error_level": "ERROR"}
        obtained = list(
            ContribValidation(contrib, data).validate_affiliations()
        )
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
        contrib = list(XMLContribs(xmltree).contribs)[0]
        data = {"affiliations_error_level": "ERROR"}
        obtained = list(
            ContribValidation(contrib, data).validate_affiliations()
        )
        expected = [
            {
                "title": "Author without affiliation",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "research-article",
                "parent_lang": "pt",
                "item": "contrib",
                "sub_item": "aff",
                "validation_type": "exist",
                "response": "ERROR",
                "expected_value": "affiliation",
                "got_value": None,
                "message": "Got None, expected affiliation",
                "advice": "provide affiliation for FRANCISCO VENEGAS-MARTÍNEZ",
                "data": {
                    "contrib_full_name": "FRANCISCO VENEGAS-MARTÍNEZ",
                    "contrib_name": {
                        "given-names": "FRANCISCO",
                        "surname": "VENEGAS-MARTÍNEZ",
                    },
                    "contrib_type": "author",
                    "contrib_xref": [
                        {"ref_type": "aff", "rid": "aff1", "text": None}
                    ],
                    "parent": "article",
                    "parent_id": None,
                    "parent_article_type": "research-article",
                    "parent_lang": "pt",
                },
            }
        ]
        self.assertEqual(len(obtained), 1)


class TestContribRoleCreditValidation(TestCase):
    def setUp(self):
        self.credit_taxonomy = [
            {
                "term": "Conceptualization",
                "uri": "https://credit.niso.org/contributor-roles/conceptualization/",
            },
            {
                "term": "Data curation",
                "uri": "https://credit.niso.org/contributor-roles/data-curation/",
            },
        ]

        self.params = {
            "credit_taxonomy_terms_and_urls": self.credit_taxonomy,
            "credit_taxonomy_terms_and_urls_error_level": "ERROR",
            "contrib_role_specific_use_list": [],
            "contrib_role_specific_use_error_level": "ERROR",
        }

        self.contrib = {
            "contrib_name": {"given-names": "John", "surname": "Doe"},
            "contrib_type": "author",
        }

    def test_valid_credit_role(self):
        contrib_role = {
            "content-type": "https://credit.niso.org/contributor-roles/conceptualization/",
            "text": "Conceptualization",
        }

        validator = ContribRoleValidation(
            self.contrib, contrib_role, self.params
        )
        results = list(validator.validate_credit())
        self.assertEqual(len(results), 0)

    def test_invalid_credit_role(self):
        contrib_role = {
            "content-type": "https://credit.niso.org/contributor-roles/invalid-role/",
            "text": "Invalid Role",
        }

        validator = ContribRoleValidation(
            self.contrib, contrib_role, self.params
        )
        results = list(validator.validate_credit())

        self.assertEqual(len(results), 1)
        result = results[0]
        self.assertEqual(result["validation_type"], "value in list")
        self.assertEqual(result["response"], "ERROR")
        self.assertEqual(
            result["got_value"],
            "https://credit.niso.org/contributor-roles/invalid-role/",
        )

    def test_missing_credit_role(self):
        contrib_role = {"content-type": None, "text": "Some Role"}

        validator = ContribRoleValidation(
            self.contrib, contrib_role, self.params
        )
        results = list(validator.validate_credit())

        self.assertEqual(len(results), 1)
        result = results[0]
        self.assertEqual(result["validation_type"], "value in list")
        self.assertEqual(result["response"], "ERROR")
        self.assertEqual(result["got_value"], None)


class TestContribRoleSpecificUseValidation(TestCase):
    def setUp(self):
        self.specific_use_list = ["PHD", "MS", "BS"]
        self.params = {
            "credit_taxonomy_terms_and_urls": [],
            "credit_taxonomy_terms_and_urls_error_level": "ERROR",
            "contrib_role_specific_use_list": self.specific_use_list,
            "contrib_role_specific_use_error_level": "ERROR",
        }

        self.contrib = {
            "contrib_name": {"given-names": "John", "surname": "Doe"},
            "contrib_type": "author",
        }

    def test_valid_specific_use(self):
        contrib_role = {"specific-use": "PHD", "text": "Some Role"}

        validator = ContribRoleValidation(
            self.contrib, contrib_role, self.params
        )
        results = list(validator.validate_role_specific_use())
        self.assertEqual(len(results), 0)

    def test_invalid_specific_use(self):
        contrib_role = {"specific-use": "INVALID", "text": "Some Role"}

        validator = ContribRoleValidation(
            self.contrib, contrib_role, self.params
        )
        results = list(validator.validate_role_specific_use())

        self.assertEqual(len(results), 1)
        result = results[0]
        self.assertEqual(result["validation_type"], "value in list")
        self.assertEqual(result["response"], "ERROR")
        self.assertEqual(result["got_value"], "INVALID")

    def test_missing_specific_use(self):
        contrib_role = {"specific-use": None, "text": "Some Role"}

        validator = ContribRoleValidation(
            self.contrib, contrib_role, self.params
        )
        results = list(validator.validate_role_specific_use())

        self.assertEqual(len(results), 1)
        result = results[0]
        self.assertEqual(result["validation_type"], "value in list")
        self.assertEqual(result["response"], "ERROR")
        self.assertEqual(result["got_value"], None)


class TestContribRoleCompleteValidation(TestCase):
    def setUp(self):
        self.credit_taxonomy = [
            {
                "term": "Conceptualization",
                "uri": "https://credit.niso.org/contributor-roles/conceptualization/",
            }
        ]
        self.specific_use_list = ["PHD"]

        self.params = {
            "credit_taxonomy_terms_and_urls": self.credit_taxonomy,
            "credit_taxonomy_terms_and_urls_error_level": "ERROR",
            "contrib_role_specific_use_list": self.specific_use_list,
            "contrib_role_specific_use_error_level": "ERROR",
        }

        self.contrib = {
            "contrib_name": {"given-names": "John", "surname": "Doe"},
            "contrib_type": "author",
        }

    def test_all_valid(self):
        contrib_role = {
            "content-type": "https://credit.niso.org/contributor-roles/conceptualization/",
            "specific-use": "PHD",
            "text": "Conceptualization",
        }

        validator = ContribRoleValidation(
            self.contrib, contrib_role, self.params
        )
        credit_results = list(validator.validate_credit())
        specific_use_results = list(validator.validate_role_specific_use())

        self.assertEqual(len(credit_results), 0)
        self.assertEqual(len(specific_use_results), 0)

    def test_all_invalid(self):
        contrib_role = {
            "content-type": "invalid",
            "specific-use": "invalid",
            "text": "Invalid Role",
        }

        validator = ContribRoleValidation(
            self.contrib, contrib_role, self.params
        )
        credit_results = list(validator.validate_credit())
        specific_use_results = list(validator.validate_role_specific_use())

        self.assertEqual(len(credit_results), 1)
        self.assertEqual(len(specific_use_results), 1)

        self.assertEqual(credit_results[0]["response"], "ERROR")
        self.assertEqual(specific_use_results[0]["response"], "ERROR")
