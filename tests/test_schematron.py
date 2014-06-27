# coding: utf-8
import unittest
from StringIO import StringIO

from lxml import isoschematron, etree

from packtools import stylechecker


SCH = etree.parse(stylechecker.SCHEMAS['sps.sch'])


class JournalIdTests(unittest.TestCase):
    """Tests for article/front/journal-meta/journal-id elements.
    """
    def _run_validation(self, sample):
        schematron = isoschematron.Schematron(SCH, phase='phase.journal-id')
        return schematron.validate(etree.parse(sample))

    def test_case1(self):
        """
        presence(@nlm-ta) is True
        presence(@publisher-id) is True
        presence(@nlm-ta) v presence(@publisher-id) is True
        """
        sample = """<article>
                      <front>
                        <journal-meta>
                          <journal-id journal-id-type="nlm-ta">
                            Rev Saude Publica
                          </journal-id>
                          <journal-id journal-id-type="publisher-id">
                            RSP
                          </journal-id>
                        </journal-meta>
                      </front>
                    </article>
                 """
        sample = StringIO(sample)

        self.assertTrue(self._run_validation(sample))

    def test_case2(self):
        """
        presence(@nlm-ta) is True
        presence(@publisher-id) is False
        presence(@nlm-ta) v presence(@publisher-id) is True
        """
        sample = """<article>
                      <front>
                        <journal-meta>
                          <journal-id journal-id-type="nlm-ta">
                            Rev Saude Publica
                          </journal-id>
                        </journal-meta>
                      </front>
                    </article>
                 """
        sample = StringIO(sample)

        self.assertTrue(self._run_validation(sample))

    def test_case3(self):
        """
        presence(@nlm-ta) is False
        presence(@publisher-id) is True
        presence(@nlm-ta) v presence(@publisher-id) is True
        """
        sample = """<article>
                      <front>
                        <journal-meta>
                          <journal-id journal-id-type="publisher-id">
                            RSP
                          </journal-id>
                        </journal-meta>
                      </front>
                    </article>
                 """
        sample = StringIO(sample)

        self.assertTrue(self._run_validation(sample))

    def test_case4(self):
        """
        presence(@nlm-ta) is False
        presence(@publisher-id) is False
        presence(@nlm-ta) v presence(@publisher-id) is False
        """
        sample = """<article>
                      <front>
                        <journal-meta>
                          <journal-id journal-id-type='doi'>
                            123.plin
                          </journal-id>
                        </journal-meta>
                      </front>
                    </article>
                 """
        sample = StringIO(sample)

        self.assertFalse(self._run_validation(sample))


class JournalTitleGroupTests(unittest.TestCase):
    """Tests for article/front/journal-meta/journal-title-group elements.
    """
    def _run_validation(self, sample):
        schematron = isoschematron.Schematron(SCH, phase='phase.journal-title-group')
        return schematron.validate(etree.parse(sample))

    def test_journal_title_group_is_absent(self):
        sample = """<article>
                      <front>
                        <journal-meta>
                        </journal-meta>
                      </front>
                    </article>
                 """
        sample = StringIO(sample)

        self.assertFalse(self._run_validation(sample))


    def test_case1(self):
        """
        A: presence(journal-title) is True
        B: presence(abbrev-journal-title[@abbrev-type='publisher']) is True
        A ^ B is True
        """
        sample = """<article>
                      <front>
                        <journal-meta>
                          <journal-title-group>
                            <journal-title>
                              Revista de Saude Publica
                            </journal-title>
                            <abbrev-journal-title abbrev-type='publisher'>
                              Rev. Saude Publica
                            </abbrev-journal-title>
                          </journal-title-group>
                        </journal-meta>
                      </front>
                    </article>
                 """
        sample = StringIO(sample)

        self.assertTrue(self._run_validation(sample))

    def test_case2(self):
        """
        A: presence(journal-title) is True
        B: presence(abbrev-journal-title[@abbrev-type='publisher']) is False
        A ^ B is False
        """
        sample = """<article>
                      <front>
                        <journal-meta>
                          <journal-title-group>
                            <journal-title>
                              Revista de Saude Publica
                            </journal-title>
                          </journal-title-group>
                        </journal-meta>
                      </front>
                    </article>
                 """
        sample = StringIO(sample)

        self.assertFalse(self._run_validation(sample))

    def test_case3(self):
        """
        A: presence(journal-title) is False
        B: presence(abbrev-journal-title[@abbrev-type='publisher']) is True
        A ^ B is False
        """
        sample = """<article>
                      <front>
                        <journal-meta>
                          <journal-title-group>
                            <abbrev-journal-title abbrev-type='publisher'>
                              Rev. Saude Publica
                            </abbrev-journal-title>
                          </journal-title-group>
                        </journal-meta>
                      </front>
                    </article>
                 """
        sample = StringIO(sample)

        self.assertFalse(self._run_validation(sample))

    def test_case4(self):
        """
        A: presence(journal-title) is False
        B: presence(abbrev-journal-title[@abbrev-type='publisher']) is False
        A ^ B is False
        """
        sample = """<article>
                      <front>
                        <journal-meta>
                          <journal-title-group>
                          </journal-title-group>
                        </journal-meta>
                      </front>
                    </article>
                 """
        sample = StringIO(sample)

        self.assertFalse(self._run_validation(sample))


class PublisherTests(unittest.TestCase):
    """Tests for article/front/journal-meta/publisher elements.
    """
    def _run_validation(self, sample):
        schematron = isoschematron.Schematron(SCH, phase='phase.publisher')
        return schematron.validate(etree.parse(sample))

    def test_publisher_is_present(self):
        sample = """<article>
                      <front>
                        <journal-meta>
                          <publisher>
                            <publisher-name>British Medical Journal</publisher-name>
                          </publisher>
                        </journal-meta>
                      </front>
                    </article>
                 """
        sample = StringIO(sample)

        self.assertTrue(self._run_validation(sample))

    def test_publisher_is_absent(self):
        sample = """<article>
                      <front>
                        <journal-meta>
                        </journal-meta>
                      </front>
                    </article>
                 """
        sample = StringIO(sample)

        self.assertFalse(self._run_validation(sample))


class ArticleCategoriesTests(unittest.TestCase):
    """Tests for article/front/article-meta/article-categories elements.
    """
    def _run_validation(self, sample):
        schematron = isoschematron.Schematron(SCH, phase='phase.article-categories')
        return schematron.validate(etree.parse(sample))

    def test_article_categories_is_present(self):
        sample = """<article>
                      <front>
                        <article-meta>
                          <article-categories>
                            <subj-group>
                              <subject>ISO/TC 108</subject>
                              <subject>
                                SC 2, Measurement and evaluation of...
                              </subject>
                            </subj-group>
                          </article-categories>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = StringIO(sample)

        self.assertTrue(self._run_validation(sample))

    def test_article_categories_is_absent(self):
        sample = """<article>
                      <front>
                        <article-meta>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = StringIO(sample)

        self.assertFalse(self._run_validation(sample))


class fpage_OR_elocationTests(unittest.TestCase):
    """Tests for article/front/article-meta/fpage or elocation-id elements.
    """
    def _run_validation(self, sample):
        schematron = isoschematron.Schematron(SCH, phase='phase.fpage_or_elocation-id')
        return schematron.validate(etree.parse(sample))

    def test_case1(self):
        """
        fpage is True
        elocation-id is True
        fpage v elocation-id is True
        """
        sample = """<article>
                      <front>
                        <article-meta>
                          <fpage>01</fpage>
                          <elocation-id>E27</elocation-id>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = StringIO(sample)

        self.assertTrue(self._run_validation(sample))

    def test_case2(self):
        """
        fpage is True
        elocation-id is False
        fpage v elocation-id is True
        """
        sample = """<article>
                      <front>
                        <article-meta>
                          <fpage>01</fpage>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = StringIO(sample)

        self.assertTrue(self._run_validation(sample))

    def test_case3(self):
        """
        fpage is False
        elocation-id is True
        fpage v elocation-id is True
        """
        sample = """<article>
                      <front>
                        <article-meta>
                          <elocation-id>E27</elocation-id>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = StringIO(sample)

        self.assertTrue(self._run_validation(sample))

    def test_case4(self):
        """
        fpage is False
        elocation-id is False
        fpage v elocation-id is False
        """
        sample = """<article>
                      <front>
                        <article-meta>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = StringIO(sample)

        self.assertFalse(self._run_validation(sample))

class ISSNTests(unittest.TestCase):
    """Tests for article/front/journal-meta/issn elements.
    """
    def _run_validation(self, sample):
        schematron = isoschematron.Schematron(SCH, phase='phase.issn')
        return schematron.validate(etree.parse(sample))

    def test_case1(self):
        """
        A: @pub-type='epub' is True
        B: @pub-type='ppub' is True
        A v B is True
        """
        sample = """<article>
                      <front>
                        <journal-meta>
                          <issn pub-type="epub">
                            0959-8138
                          </issn>
                          <issn pub-type="ppub">
                            0959-813X
                          </issn>
                        </journal-meta>
                      </front>
                    </article>
                 """
        sample = StringIO(sample)

        self.assertTrue(self._run_validation(sample))

    def test_case2(self):
        """
        A: @pub-type='epub' is True
        B: @pub-type='ppub' is False
        A v B is True
        """
        sample = """<article>
                      <front>
                        <journal-meta>
                          <issn pub-type="epub">
                            0959-8138
                          </issn>
                        </journal-meta>
                      </front>
                    </article>
                 """
        sample = StringIO(sample)

        self.assertTrue(self._run_validation(sample))

    def test_case3(self):
        """
        A: @pub-type='epub' is False
        B: @pub-type='ppub' is True
        A v B is True
        """
        sample = """<article>
                      <front>
                        <journal-meta>
                          <issn pub-type="ppub">
                            0959-813X
                          </issn>
                        </journal-meta>
                      </front>
                    </article>
                 """
        sample = StringIO(sample)

        self.assertTrue(self._run_validation(sample))

    def test_case4(self):
        """
        A: @pub-type='epub' is False
        B: @pub-type='ppub' is False
        A v B is False
        """
        sample = """<article>
                      <front>
                        <journal-meta>
                          <issn>
                            0959-813X
                          </issn>
                        </journal-meta>
                      </front>
                    </article>
                 """
        sample = StringIO(sample)

        self.assertFalse(self._run_validation(sample))


class ArticleIdTests(unittest.TestCase):
    """Tests for article/front/article-meta/article-id elements.
    """
    def _run_validation(self, sample):
        schematron = isoschematron.Schematron(SCH, phase='phase.article-id')
        return schematron.validate(etree.parse(sample))

    def test_article_id_is_absent(self):
        sample = """<article>
                      <front>
                        <article-meta>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = StringIO(sample)

        self.assertFalse(self._run_validation(sample))


    def test_pub_id_type_doi_is_absent(self):
        sample = """<article>
                      <front>
                        <article-meta>
                          <article-id>
                            10.1590/1414-431X20143434
                          </article-id>
                          <article-id pub-id-type='other'>
                            10.1590/1414-431X20143435
                          </article-id>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = StringIO(sample)

        self.assertFalse(self._run_validation(sample))

    def test_pub_id_type_doi(self):
        sample = """<article>
                      <front>
                        <article-meta>
                          <article-id pub-id-type='doi'>
                            10.1590/1414-431X20143434
                          </article-id>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = StringIO(sample)

        self.assertTrue(self._run_validation(sample))

    def test_invalid_pub_id_type(self):
        sample = """<article>
                      <front>
                        <article-meta>
                          <article-id pub-id-type='unknown'>
                            10.1590/1414-431X20143434
                          </article-id>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = StringIO(sample)

        self.assertFalse(self._run_validation(sample))

    def test_invalid_pub_id_type_case2(self):
        sample = """<article>
                      <front>
                        <article-meta>
                          <article-id pub-id-type='unknown'>
                            10.1590/1414-431X20143434
                          </article-id>
                          <article-id pub-id-type='doi'>
                            10.1590/1414-431X20143434
                          </article-id>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = StringIO(sample)

        self.assertFalse(self._run_validation(sample))

    def test_valid_pub_id_type_values(self):
        for typ in ['art-access-id', 'arxiv', 'doaj', 'doi', 'isbn', 'pmcid',
                    'pmid', 'publisher-id', 'publisher-manuscript', 'sici', 'other']:
            sample = """<article>
                          <front>
                            <article-meta>
                              <article-id pub-id-type='%s'>
                                10.1590/1414-431X20143433
                              </article-id>
                              <article-id pub-id-type='doi'>
                                10.1590/1414-431X20143434
                              </article-id>
                            </article-meta>
                          </front>
                        </article>
                     """ % typ
            sample = StringIO(sample)
            self.assertTrue(self._run_validation(sample))


class SubjGroupTests(unittest.TestCase):
    """Tests for article/front/article-meta/article-categories/subj-group elements.
    """
    def _run_validation(self, sample):
        schematron = isoschematron.Schematron(SCH, phase='phase.subj-group')
        return schematron.validate(etree.parse(sample))

    def test_subj_group_is_absent(self):
        sample = """<article>
                      <front>
                        <article-meta>
                          <article-categories>
                          </article-categories>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = StringIO(sample)

        self.assertFalse(self._run_validation(sample))

    def test_without_heading_type(self):
        sample = """<article>
                      <front>
                        <article-meta>
                          <article-categories>
                            <subj-group subj-group-type="kwd">
                              <subject content-type="neurosci">
                                Cellular and Molecular Biology
                              </subject>
                              <subj-group>
                                <subject content-type="neurosci">
                                  Blood and brain barrier
                                </subject>
                              </subj-group>
                            </subj-group>
                          </article-categories>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = StringIO(sample)

        self.assertFalse(self._run_validation(sample))

    def test_with_heading_type(self):
        sample = """<article>
                      <front>
                        <article-meta>
                          <article-categories>
                            <subj-group subj-group-type="heading">
                              <subject>
                                Cellular and Molecular Biology
                              </subject>
                              <subj-group>
                                <subject content-type="neurosci">
                                  Blood and brain barrier
                                </subject>
                              </subj-group>
                            </subj-group>
                          </article-categories>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = StringIO(sample)

        self.assertTrue(self._run_validation(sample))

    def test_with_heading_type_in_the_deep(self):
        sample = """<article>
                      <front>
                        <article-meta>
                          <article-categories>
                            <subj-group>
                              <subject>
                                Cellular and Molecular Biology
                              </subject>
                              <subj-group subj-group-type="heading">
                                <subject>
                                  Blood and brain barrier
                                </subject>
                              </subj-group>
                            </subj-group>
                          </article-categories>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = StringIO(sample)

        self.assertTrue(self._run_validation(sample))

    def test_with_many_heading_type(self):
        sample = """<article>
                      <front>
                        <article-meta>
                          <article-categories>
                            <subj-group subj-group-type="heading">
                              <subject>
                                Cellular and Molecular Biology
                              </subject>
                            </subj-group>
                            <subj-group subj-group-type="heading">
                              <subject>
                                Blood and brain barrier
                              </subject>
                            </subj-group>
                          </article-categories>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = StringIO(sample)

        self.assertFalse(self._run_validation(sample))

