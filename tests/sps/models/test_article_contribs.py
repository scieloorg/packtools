from unittest import TestCase

from lxml import etree

from packtools.sps.models.article_contribs import Contrib


class ContribTest(TestCase):
    def setUp(self):
        xml = """
            <article>
                <front>
                    <article-meta>
                        <contrib-group>
                            <contrib contrib-type="author">
                                <contrib-id contrib-id-type="orcid">0000-0001-8528-2091</contrib-id>
                                <contrib-id contrib-id-type="scopus">24771926600</contrib-id>
                                <collab>The MARS Group</collab>
                                <name>
                                    <surname>Einstein</surname>
                                    <given-names>Albert</given-names>
                                    <prefix>Prof</prefix>
                                    <suffix>Nieto</suffix>
                                </name>
                                <xref ref-type="aff" rid="aff1">1</xref>
                                <role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>
                                <role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>
                                <role specific-use="reviewer">Reviewer</role>
                            </contrib>
                        </contrib-group>
                    </article-meta>
                </front>
            </article>
            """
        self.xmltree = etree.fromstring(xml)

    def test_contrib_type(self):
        contrib = self.xmltree.xpath(".//contrib")[0]
        obtained = Contrib(contrib).contrib_type

        self.assertEqual(obtained, "author")

    def test_contrib_ids(self):
        contrib = self.xmltree.xpath(".//contrib")[0]
        obtained = Contrib(contrib).contrib_ids
        expected = {
            'orcid': '0000-0001-8528-2091',
            'scopus': '24771926600'
        }

        self.assertDictEqual(obtained, expected)

    def test_contrib_name(self):
        contrib = self.xmltree.xpath(".//contrib")[0]
        obtained = Contrib(contrib).contrib_name
        expected = {
            'given-names': 'Albert',
            'surname': 'Einstein',
            'prefix': 'Prof',
            'suffix': 'Nieto',
        }

        self.assertDictEqual(obtained, expected)

    def test_collab(self):
        contrib = self.xmltree.xpath(".//contrib")[0]
        obtained = Contrib(contrib).collab

        self.assertEqual(obtained, "The MARS Group")

    def test_contrib_xref(self):
        contrib = self.xmltree.xpath(".//contrib")[0]
        obtained = list(Contrib(contrib).contrib_xref)
        expected = [
            {
                'rid': 'aff1',
                'ref_type': 'aff',
                'text': '1'
            }
        ]

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(item, obtained[i])

    def test_contrib_role(self):
        contrib = self.xmltree.xpath(".//contrib")[0]
        obtained = list(Contrib(contrib).contrib_role)
        expected = [
            {
                "text": 'Data curation',
                "content-type": "https://credit.niso.org/contributor-roles/data-curation/",
                "specific-use": None,
            },
            {
                "text": 'Conceptualization',
                "content-type": "https://credit.niso.org/contributor-roles/conceptualization/",
                "specific-use": None,
            },
            {
                "text": "Reviewer",
                "content-type": None,
                "specific-use": "reviewer",
            },
        ]

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(item, obtained[i])

    def test_data(self):
        self.maxDiff = None
        contrib = self.xmltree.xpath(".//contrib")[0]
        obtained = Contrib(contrib).data
        expected = {
            'contrib_type': 'author',
            'contrib_ids': {
                'orcid': '0000-0001-8528-2091',
                'scopus': '24771926600'
            },
            'collab': 'The MARS Group',
            'contrib_name': {
                'given-names': 'Albert',
                'surname': 'Einstein',
                'prefix': 'Prof',
                'suffix': 'Nieto'
            },
            'contrib_xref': [
                {
                    'ref_type': 'aff',
                    'rid': 'aff1',
                    'text': '1'
                }
            ],
            'contrib_role': [
                {
                    'content-type': 'https://credit.niso.org/contributor-roles/data-curation/',
                    'specific-use': None,
                    'text': 'Data curation'
                },
                {
                    'content-type': 'https://credit.niso.org/contributor-roles/conceptualization/',
                    'specific-use': None,
                    'text': 'Conceptualization'
                },
                {
                    'content-type': None,
                    'specific-use': 'reviewer',
                    'text': 'Reviewer'
                }
            ],
        }

        self.assertDictEqual(obtained, expected)


class ContribWithoutContribTypeTest(TestCase):
    def setUp(self):
        xml = """
            <article>
                <front>
                    <article-meta>
                        <contrib-group>
                            <contrib>
                                <contrib-id contrib-id-type="orcid">0000-0001-8528-2091</contrib-id>
                                <contrib-id contrib-id-type="scopus">24771926600</contrib-id>
                                <collab>The MARS Group</collab>
                                <name>
                                    <surname>Einstein</surname>
                                    <given-names>Albert</given-names>
                                    <prefix>Prof</prefix>
                                    <suffix>Nieto</suffix>
                                </name>
                                <xref ref-type="aff" rid="aff1">1</xref>
                                <role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>
                                <role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>
                                <role specific-use="reviewer">Reviewer</role>
                            </contrib>
                        </contrib-group>
                    </article-meta>
                </front>
            </article>
            """
        self.xmltree = etree.fromstring(xml)

    def test_data(self):
        self.maxDiff = None
        contrib = self.xmltree.xpath(".//contrib")[0]
        obtained = Contrib(contrib).data
        expected = {
            'contrib_ids': {
                'orcid': '0000-0001-8528-2091',
                'scopus': '24771926600'
            },
            'collab': 'The MARS Group',
            'contrib_name': {
                'given-names': 'Albert',
                'surname': 'Einstein',
                'prefix': 'Prof',
                'suffix': 'Nieto'
            },
            'contrib_xref': [
                {
                    'ref_type': 'aff',
                    'rid': 'aff1',
                    'text': '1'
                }
            ],
            'contrib_role': [
                {
                    'content-type': 'https://credit.niso.org/contributor-roles/data-curation/',
                    'specific-use': None,
                    'text': 'Data curation'
                },
                {
                    'content-type': 'https://credit.niso.org/contributor-roles/conceptualization/',
                    'specific-use': None,
                    'text': 'Conceptualization'
                },
                {
                    'content-type': None,
                    'specific-use': 'reviewer',
                    'text': 'Reviewer'
                }
            ],
        }

        self.assertDictEqual(obtained, expected)


class ContribWithoutContribIdTest(TestCase):
    def setUp(self):
        xml = """
            <article>
                <front>
                    <article-meta>
                        <contrib-group>
                            <contrib contrib-type="author">
                                <collab>The MARS Group</collab>
                                <name>
                                    <surname>Einstein</surname>
                                    <given-names>Albert</given-names>
                                    <prefix>Prof</prefix>
                                    <suffix>Nieto</suffix>
                                </name>
                                <xref ref-type="aff" rid="aff1">1</xref>
                                <role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>
                                <role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>
                                <role specific-use="reviewer">Reviewer</role>
                            </contrib>
                        </contrib-group>
                    </article-meta>
                </front>
            </article>
            """
        self.xmltree = etree.fromstring(xml)

    def test_data(self):
        self.maxDiff = None
        contrib = self.xmltree.xpath(".//contrib")[0]
        obtained = Contrib(contrib).data
        expected = {
            'contrib_type': 'author',
            'collab': 'The MARS Group',
            'contrib_name': {
                'given-names': 'Albert',
                'surname': 'Einstein',
                'prefix': 'Prof',
                'suffix': 'Nieto'
            },
            'contrib_xref': [
                {
                    'ref_type': 'aff',
                    'rid': 'aff1',
                    'text': '1'
                }
            ],
            'contrib_role': [
                {
                    'content-type': 'https://credit.niso.org/contributor-roles/data-curation/',
                    'specific-use': None,
                    'text': 'Data curation'
                },
                {
                    'content-type': 'https://credit.niso.org/contributor-roles/conceptualization/',
                    'specific-use': None,
                    'text': 'Conceptualization'
                },
                {
                    'content-type': None,
                    'specific-use': 'reviewer',
                    'text': 'Reviewer'
                }
            ],
        }

        self.assertDictEqual(obtained, expected)


class ContribWithoutCollabTest(TestCase):
    def setUp(self):
        xml = """
            <article>
                <front>
                    <article-meta>
                        <contrib-group>
                            <contrib contrib-type="author">
                                <contrib-id contrib-id-type="orcid">0000-0001-8528-2091</contrib-id>
                                <contrib-id contrib-id-type="scopus">24771926600</contrib-id>
                                <name>
                                    <surname>Einstein</surname>
                                    <given-names>Albert</given-names>
                                    <prefix>Prof</prefix>
                                    <suffix>Nieto</suffix>
                                </name>
                                <xref ref-type="aff" rid="aff1">1</xref>
                                <role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>
                                <role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>
                                <role specific-use="reviewer">Reviewer</role>
                            </contrib>
                        </contrib-group>
                    </article-meta>
                </front>
            </article>
            """
        self.xmltree = etree.fromstring(xml)

    def test_data(self):
        self.maxDiff = None
        contrib = self.xmltree.xpath(".//contrib")[0]
        obtained = Contrib(contrib).data
        expected = {
            'contrib_type': 'author',
            'contrib_ids': {
                'orcid': '0000-0001-8528-2091',
                'scopus': '24771926600'
            },
            'contrib_name': {
                'given-names': 'Albert',
                'surname': 'Einstein',
                'prefix': 'Prof',
                'suffix': 'Nieto'
            },
            'contrib_xref': [
                {
                    'ref_type': 'aff',
                    'rid': 'aff1',
                    'text': '1'
                }
            ],
            'contrib_role': [
                {
                    'content-type': 'https://credit.niso.org/contributor-roles/data-curation/',
                    'specific-use': None,
                    'text': 'Data curation'
                },
                {
                    'content-type': 'https://credit.niso.org/contributor-roles/conceptualization/',
                    'specific-use': None,
                    'text': 'Conceptualization'
                },
                {
                    'content-type': None,
                    'specific-use': 'reviewer',
                    'text': 'Reviewer'
                }
            ],
        }

        self.assertDictEqual(obtained, expected)


class ContribWithoutNameTest(TestCase):
    def setUp(self):
        xml = """
            <article>
                <front>
                    <article-meta>
                        <contrib-group>
                            <contrib contrib-type="author">
                                <contrib-id contrib-id-type="orcid">0000-0001-8528-2091</contrib-id>
                                <contrib-id contrib-id-type="scopus">24771926600</contrib-id>
                                <collab>The MARS Group</collab>
                                <xref ref-type="aff" rid="aff1">1</xref>
                                <role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>
                                <role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>
                                <role specific-use="reviewer">Reviewer</role>
                            </contrib>
                        </contrib-group>
                    </article-meta>
                </front>
            </article>
            """
        self.xmltree = etree.fromstring(xml)

    def test_data(self):
        self.maxDiff = None
        contrib = self.xmltree.xpath(".//contrib")[0]
        obtained = Contrib(contrib).data
        expected = {
            'contrib_type': 'author',
            'contrib_ids': {
                'orcid': '0000-0001-8528-2091',
                'scopus': '24771926600'
            },
            'collab': 'The MARS Group',
            'contrib_xref': [
                {
                    'ref_type': 'aff',
                    'rid': 'aff1',
                    'text': '1'
                }
            ],
            'contrib_role': [
                {
                    'content-type': 'https://credit.niso.org/contributor-roles/data-curation/',
                    'specific-use': None,
                    'text': 'Data curation'
                },
                {
                    'content-type': 'https://credit.niso.org/contributor-roles/conceptualization/',
                    'specific-use': None,
                    'text': 'Conceptualization'
                },
                {
                    'content-type': None,
                    'specific-use': 'reviewer',
                    'text': 'Reviewer'
                }
            ],
        }

        self.assertDictEqual(obtained, expected)


class ContribWithoutXrefTest(TestCase):
    def setUp(self):
        xml = """
            <article>
                <front>
                    <article-meta>
                        <contrib-group>
                            <contrib contrib-type="author">
                                <contrib-id contrib-id-type="orcid">0000-0001-8528-2091</contrib-id>
                                <contrib-id contrib-id-type="scopus">24771926600</contrib-id>
                                <collab>The MARS Group</collab>
                                <name>
                                    <surname>Einstein</surname>
                                    <given-names>Albert</given-names>
                                    <prefix>Prof</prefix>
                                    <suffix>Nieto</suffix>
                                </name>
                                <role content-type="https://credit.niso.org/contributor-roles/data-curation/">Data curation</role>
                                <role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>
                                <role specific-use="reviewer">Reviewer</role>
                            </contrib>
                        </contrib-group>
                    </article-meta>
                </front>
            </article>
            """
        self.xmltree = etree.fromstring(xml)

    def test_data(self):
        self.maxDiff = None
        contrib = self.xmltree.xpath(".//contrib")[0]
        obtained = Contrib(contrib).data
        expected = {
            'contrib_type': 'author',
            'contrib_ids': {
                'orcid': '0000-0001-8528-2091',
                'scopus': '24771926600'
            },
            'collab': 'The MARS Group',
            'contrib_name': {
                'given-names': 'Albert',
                'surname': 'Einstein',
                'prefix': 'Prof',
                'suffix': 'Nieto'
            },
            'contrib_role': [
                {
                    'content-type': 'https://credit.niso.org/contributor-roles/data-curation/',
                    'specific-use': None,
                    'text': 'Data curation'
                },
                {
                    'content-type': 'https://credit.niso.org/contributor-roles/conceptualization/',
                    'specific-use': None,
                    'text': 'Conceptualization'
                },
                {
                    'content-type': None,
                    'specific-use': 'reviewer',
                    'text': 'Reviewer'
                }
            ],
        }

        self.assertDictEqual(obtained, expected)


class ContribWithoutRoleTest(TestCase):
    def setUp(self):
        xml = """
            <article>
                <front>
                    <article-meta>
                        <contrib-group>
                            <contrib contrib-type="author">
                                <contrib-id contrib-id-type="orcid">0000-0001-8528-2091</contrib-id>
                                <contrib-id contrib-id-type="scopus">24771926600</contrib-id>
                                <collab>The MARS Group</collab>
                                <name>
                                    <surname>Einstein</surname>
                                    <given-names>Albert</given-names>
                                    <prefix>Prof</prefix>
                                    <suffix>Nieto</suffix>
                                </name>
                                <xref ref-type="aff" rid="aff1">1</xref>
                            </contrib>
                        </contrib-group>
                    </article-meta>
                </front>
            </article>
            """
        self.xmltree = etree.fromstring(xml)

    def test_data(self):
        self.maxDiff = None
        contrib = self.xmltree.xpath(".//contrib")[0]
        obtained = Contrib(contrib).data
        expected = {
            'contrib_type': 'author',
            'contrib_ids': {
                'orcid': '0000-0001-8528-2091',
                'scopus': '24771926600'
            },
            'collab': 'The MARS Group',
            'contrib_name': {
                'given-names': 'Albert',
                'surname': 'Einstein',
                'prefix': 'Prof',
                'suffix': 'Nieto'
            },
            'contrib_xref': [
                {
                    'ref_type': 'aff',
                    'rid': 'aff1',
                    'text': '1'
                }
            ]
        }

        self.assertDictEqual(obtained, expected)
