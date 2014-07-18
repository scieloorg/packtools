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


class AbstractLangTests(unittest.TestCase):
    """Tests for article/front/article-meta/abstract elements.
    """
    def _run_validation(self, sample):
        schematron = isoschematron.Schematron(SCH, phase='phase.abstract_lang')
        return schematron.validate(etree.parse(sample))

    def test_is_present(self):
        sample = """<article>
                      <front>
                        <article-meta>
                          <abstract>
                            <p>Differing socioeconomic positions in...</p>
                          </abstract>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = StringIO(sample)

        self.assertTrue(self._run_validation(sample))

    def test_is_absent(self):
        sample = """<article>
                      <front>
                        <article-meta>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = StringIO(sample)

        self.assertTrue(self._run_validation(sample))

    def test_is_present_with_lang(self):
        sample = """<?xml version="1.0" encoding="UTF-8"?>
                    <article>
                      <front>
                        <article-meta>
                          <abstract xml:lang="en">
                            <p>Differing socioeconomic positions in...</p>
                          </abstract>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = StringIO(sample)

        self.assertFalse(self._run_validation(sample))

    def test_missing_for_research_article(self):
        sample = """<?xml version="1.0" encoding="UTF-8"?>
                    <article article-type="research-article">
                      <front>
                        <article-meta>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = StringIO(sample)

        self.assertFalse(self._run_validation(sample))

    def test_research_article(self):
        sample = """<?xml version="1.0" encoding="UTF-8"?>
                    <article article-type="research-article">
                      <front>
                        <article-meta>
                          <abstract>
                            <p>Differing socioeconomic positions in...</p>
                          </abstract>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = StringIO(sample)

        self.assertTrue(self._run_validation(sample))

    def test_missing_for_review_article(self):
        sample = """<?xml version="1.0" encoding="UTF-8"?>
                    <article article-type="review-article">
                      <front>
                        <article-meta>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = StringIO(sample)

        self.assertFalse(self._run_validation(sample))

    def test_review_article(self):
        sample = """<?xml version="1.0" encoding="UTF-8"?>
                    <article article-type="review-article">
                      <front>
                        <article-meta>
                          <abstract>
                            <p>Differing socioeconomic positions in...</p>
                          </abstract>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = StringIO(sample)

        self.assertTrue(self._run_validation(sample))


class ArticleTitleLangTests(unittest.TestCase):
    """Tests for article/front/article-meta/title-group/article-title elements.
    """
    def _run_validation(self, sample):
        schematron = isoschematron.Schematron(SCH, phase='phase.article-title_lang')
        return schematron.validate(etree.parse(sample))

    def test_is_present(self):
        sample = """<article>
                      <front>
                        <article-meta>
                          <title-group>
                            <article-title>
                              Systematic review of day hospital care...
                            </article-title>
                          </title-group>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = StringIO(sample)

        self.assertTrue(self._run_validation(sample))

    def test_is_present_with_lang(self):
        sample = """<article>
                      <front>
                        <article-meta>
                          <title-group>
                            <article-title xml:lang="en">
                              Systematic review of day hospital care...
                            </article-title>
                          </title-group>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = StringIO(sample)

        self.assertFalse(self._run_validation(sample))


class KwdGroupLangTests(unittest.TestCase):
    """Tests for article/front/article-meta/kwd-group elements.
    """
    def _run_validation(self, sample):
        schematron = isoschematron.Schematron(SCH, phase='phase.kwd-group_lang')
        return schematron.validate(etree.parse(sample))

    def test_single_occurence(self):
        sample = """<article>
                      <front>
                        <article-meta>
                          <kwd-group>
                            <kwd>gene expression</kwd>
                          </kwd-group>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = StringIO(sample)

        self.assertFalse(self._run_validation(sample))

    def test_many_occurencies(self):
        sample = """<article>
                      <front>
                        <article-meta>
                          <kwd-group xml:lang="en">
                            <kwd>gene expression</kwd>
                          </kwd-group>
                          <kwd-group xml:lang="pt">
                            <kwd>expressao do gene</kwd>
                          </kwd-group>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = StringIO(sample)

        self.assertTrue(self._run_validation(sample))

    def test_many_occurencies_without_lang(self):
        sample = """<article>
                      <front>
                        <article-meta>
                          <kwd-group>
                            <kwd>gene expression</kwd>
                          </kwd-group>
                          <kwd-group>
                            <kwd>expressao do gene</kwd>
                          </kwd-group>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = StringIO(sample)

        self.assertFalse(self._run_validation(sample))


class AffContentTypeTests(unittest.TestCase):
    """Tests for:
      - article/front/article-meta/contrib-group
      - article/front/article-meta
    """
    def _run_validation(self, sample):
        schematron = isoschematron.Schematron(SCH, phase='phase.aff_contenttypes')
        return schematron.validate(etree.parse(sample))

    def test_original_is_present(self):
        sample = """<article>
                      <front>
                        <article-meta>
                          <aff>
                            <institution content-type="original">
                              Grupo de ...
                            </institution>
                          </aff>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = StringIO(sample)

        self.assertTrue(self._run_validation(sample))

    def test_original_is_absent(self):
        sample = """<article>
                      <front>
                        <article-meta>
                          <aff>
                            <institution>
                              Grupo de ...
                            </institution>
                          </aff>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = StringIO(sample)

        self.assertFalse(self._run_validation(sample))

    def test_many_original(self):
        sample = """<article>
                      <front>
                        <article-meta>
                          <aff>
                            <institution content-type="original">
                              Grupo de ...
                            </institution>
                            <institution content-type="original">
                              Galera de ...
                            </institution>
                          </aff>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = StringIO(sample)

        self.assertFalse(self._run_validation(sample))

    def test_original_is_present_and_absent(self):
        sample = """<article>
                      <front>
                        <article-meta>
                          <aff>
                            <institution content-type="original">
                              Grupo de ...
                            </institution>
                          </aff>
                          <aff>
                            <institution>
                              Grupo de ...
                            </institution>
                          </aff>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = StringIO(sample)

        self.assertFalse(self._run_validation(sample))

    def test_original_is_present_and_present(self):
        sample = """<article>
                      <front>
                        <article-meta>
                          <aff>
                            <institution content-type="original">
                              Grupo de ...
                            </institution>
                          </aff>
                          <aff>
                            <institution content-type="original">
                              Grupo de ...
                            </institution>
                          </aff>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = StringIO(sample)

        self.assertTrue(self._run_validation(sample))

    def test_allowed_orgdiv1(self):
        sample = """<article>
                      <front>
                        <article-meta>
                          <aff>
                            <institution content-type="original">
                              Grupo de ...
                            </institution>
                            <institution content-type="orgdiv1">
                              Instituto de Matematica e Estatistica
                            </institution>
                          </aff>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = StringIO(sample)

        self.assertTrue(self._run_validation(sample))

    def test_allowed_orgdiv2(self):
        sample = """<article>
                      <front>
                        <article-meta>
                          <aff>
                            <institution content-type="original">
                              Grupo de ...
                            </institution>
                            <institution content-type="orgdiv2">
                              Instituto de Matematica e Estatistica
                            </institution>
                          </aff>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = StringIO(sample)

        self.assertTrue(self._run_validation(sample))

    def test_allowed_orgdiv3(self):
        sample = """<article>
                      <front>
                        <article-meta>
                          <aff>
                            <institution content-type="original">
                              Grupo de ...
                            </institution>
                            <institution content-type="orgdiv3">
                              Instituto de Matematica e Estatistica
                            </institution>
                          </aff>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = StringIO(sample)

        self.assertTrue(self._run_validation(sample))

    def test_disallowed_orgdiv4(self):
        sample = """<article>
                      <front>
                        <article-meta>
                          <aff>
                            <institution content-type="original">
                              Grupo de ...
                            </institution>
                            <institution content-type="orgdiv4">
                              Instituto de Matematica e Estatistica
                            </institution>
                          </aff>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = StringIO(sample)

        self.assertFalse(self._run_validation(sample))

    def test_orgname_inside_contrib_group(self):
        sample = """<article>
                      <front>
                        <article-meta>
                          <contrib-group>
                            <aff>
                              <institution content-type="original">
                                Grupo de ...
                              </institution>
                              <institution content-type="orgname">
                                Instituto de Matematica e Estatistica
                              </institution>
                            </aff>
                          </contrib-group>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = StringIO(sample)

        self.assertTrue(self._run_validation(sample))


class CountsTests(unittest.TestCase):
    """Tests for article/front/article-meta/counts elements.
    """
    def _run_validation(self, sample):
        schematron = isoschematron.Schematron(SCH, phase='phase.counts')
        return schematron.validate(etree.parse(sample))

    def test_absent(self):
        sample = """<article>
                      <front>
                        <article-meta>
                          <fpage>0</fpage>
                          <lpage>0</lpage>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = StringIO(sample)

        self.assertFalse(self._run_validation(sample))

    def test_table_is_absent(self):
        sample = """<article>
                      <front>
                        <article-meta>
                          <counts>
                            <ref-count count="0"/>
                            <fig-count count="0"/>
                            <equation-count count="0"/>
                            <page-count count="0"/>
                          </counts>
                          <fpage>0</fpage>
                          <lpage>0</lpage>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = StringIO(sample)

        self.assertFalse(self._run_validation(sample))

    def test_ref_is_absent(self):
        sample = """<article>
                      <front>
                        <article-meta>
                          <counts>
                            <table-count count="0"/>
                            <fig-count count="0"/>
                            <equation-count count="0"/>
                            <page-count count="0"/>
                          </counts>
                          <fpage>0</fpage>
                          <lpage>0</lpage>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = StringIO(sample)

        self.assertFalse(self._run_validation(sample))

    def test_fig_is_absent(self):
        sample = """<article>
                      <front>
                        <article-meta>
                          <counts>
                            <table-count count="0"/>
                            <ref-count count="0"/>
                            <equation-count count="0"/>
                            <page-count count="0"/>
                          </counts>
                          <fpage>0</fpage>
                          <lpage>0</lpage>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = StringIO(sample)

        self.assertFalse(self._run_validation(sample))

    def test_equation_is_absent(self):
        sample = """<article>
                      <front>
                        <article-meta>
                          <counts>
                            <table-count count="0"/>
                            <ref-count count="0"/>
                            <fig-count count="0"/>
                            <page-count count="0"/>
                          </counts>
                          <fpage>0</fpage>
                          <lpage>0</lpage>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = StringIO(sample)

        self.assertFalse(self._run_validation(sample))

    def test_page_is_absent(self):
        sample = """<article>
                      <front>
                        <article-meta>
                          <counts>
                            <table-count count="0"/>
                            <ref-count count="0"/>
                            <fig-count count="0"/>
                            <equation-count count="0"/>
                          </counts>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = StringIO(sample)

        self.assertFalse(self._run_validation(sample))

    def test_zeroes_if_elements_are_missing(self):
        sample = """<article>
                      <front>
                        <article-meta>
                          <counts>
                            <table-count count="0"/>
                            <ref-count count="0"/>
                            <fig-count count="0"/>
                            <equation-count count="0"/>
                            <page-count count="0"/>
                          </counts>
                          <fpage>0</fpage>
                          <lpage>0</lpage>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = StringIO(sample)

        self.assertTrue(self._run_validation(sample))

    def test_tables(self):
        sample = """<article>
                      <front>
                        <article-meta>
                          <counts>
                            <table-count count="1"/>
                            <ref-count count="0"/>
                            <fig-count count="0"/>
                            <equation-count count="0"/>
                            <page-count count="0"/>
                          </counts>
                          <fpage>0</fpage>
                          <lpage>0</lpage>
                        </article-meta>
                      </front>
                      <body>
                        <sec>
                          <p>
                            <table frame="hsides" rules="groups">
                              <colgroup width="25%"><col/><col/><col/><col/></colgroup>
                              <thead>
                                <tr>
                                  <th style="font-weight:normal" align="left">Modelo</th>
                                  <th style="font-weight:normal">Estrutura</th>
                                  <th style="font-weight:normal">Processos</th>
                                  <th style="font-weight:normal">Resultados</th>
                                </tr>
                              </thead>
                              <tbody>
                                <tr>
                                  <td valign="top">SIPA<sup>1,2</sup></td>
                                  <td valign="top">Urgência e hospitalar.</td>
                                  <td valign="top">Realiza triagem para fragilidade.</td>
                                  <td valign="top">Maior gasto comunitário, menor gasto.</td>
                                </tr>
                              </tbody>
                            </table>
                          </p>
                        </sec>
                      </body>
                    </article>
                 """
        sample = StringIO(sample)

        self.assertTrue(self._run_validation(sample))

    def test_ref(self):
        sample = """<article>
                      <front>
                        <article-meta>
                          <counts>
                            <table-count count="0"/>
                            <ref-count count="1"/>
                            <fig-count count="0"/>
                            <equation-count count="0"/>
                            <page-count count="0"/>
                          </counts>
                          <fpage>0</fpage>
                          <lpage>0</lpage>
                        </article-meta>
                      </front>
                      <back>
                        <ref-list>
                          <title>REFERÊNCIAS</title>
	                      <ref id="B1">
                            <label>1</label>
                            <mixed-citation>
                              Béland F, Bergman H, Lebel P, Clarfield AM, Tousignant P, ...
                            </mixed-citation>
                          </ref>
                        </ref-list>
                      </back>
                    </article>
                 """
        sample = StringIO(sample)

        self.assertTrue(self._run_validation(sample))

    def test_fig(self):
        sample = """<article xmlns:xlink="http://www.w3.org/1999/xlink">
                      <front>
                        <article-meta>
                          <counts>
                            <table-count count="0"/>
                            <ref-count count="0"/>
                            <fig-count count="1"/>
                            <equation-count count="0"/>
                            <page-count count="0"/>
                          </counts>
                          <fpage>0</fpage>
                          <lpage>0</lpage>
                        </article-meta>
                      </front>
                      <body>
                        <sec>
                          <p>
                            <fig id="f01">
                              <label>Figura 1</label>
                              <caption>
                                <title>Modelo das cinco etapas da pesquisa translacional.</title>
                              </caption>
                              <graphic xlink:href="0034-8910-rsp-48-2-0347-gf01"/>
                            </fig>
                          </p>
                        </sec>
                      </body>
                    </article>
                 """
        sample = StringIO(sample)

        self.assertTrue(self._run_validation(sample))

    def test_equation(self):
        sample = """<article xmlns:xlink="http://www.w3.org/1999/xlink">
                      <front>
                        <article-meta>
                          <counts>
                            <table-count count="0"/>
                            <ref-count count="0"/>
                            <fig-count count="0"/>
                            <equation-count count="1"/>
                            <page-count count="0"/>
                          </counts>
                          <fpage>0</fpage>
                          <lpage>0</lpage>
                        </article-meta>
                      </front>
                      <body>
                        <sec>
                          <disp-formula>
                            <tex-math id="M1">
                            </tex-math>
                          </disp-formula>
                        </sec>
                      </body>
                    </article>
                 """
        sample = StringIO(sample)

        self.assertTrue(self._run_validation(sample))

    def test_page(self):
        sample = """<article xmlns:xlink="http://www.w3.org/1999/xlink">
                      <front>
                        <article-meta>
                          <counts>
                            <table-count count="0"/>
                            <ref-count count="0"/>
                            <fig-count count="0"/>
                            <equation-count count="0"/>
                            <page-count count="11"/>
                          </counts>
                          <fpage>140</fpage>
                          <lpage>150</lpage>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = StringIO(sample)

        self.assertTrue(self._run_validation(sample))


class AuthorNotesTests(unittest.TestCase):
    """Tests for article/front/article-meta/author-notes elements.
    """
    def _run_validation(self, sample):
        schematron = isoschematron.Schematron(SCH, phase='phase.author-notes')
        return schematron.validate(etree.parse(sample))

    def test_allowed_fn_types(self):
        for fn_type in ['author', 'con', 'conflict', 'corresp', 'current-aff',
                'deceased', 'edited-by', 'equal', 'on-leave', 'participating-researchers',
                'present-address', 'previously-at', 'study-group-members', 'other']:

            sample = """<article>
                          <front>
                            <article-meta>
                              <author-notes>
                                <fn fn-type="%s">
                                  <p>foobar</p>
                                </fn>
                              </author-notes>
                            </article-meta>
                          </front>
                        </article>
                     """ % fn_type
            sample = StringIO(sample)

            self.assertTrue(self._run_validation(sample))

    def test_disallowed_fn_types(self):
        sample = """<article>
                      <front>
                        <article-meta>
                          <author-notes>
                            <fn fn-type="wtf">
                              <p>foobar</p>
                            </fn>
                          </author-notes>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = StringIO(sample)

        self.assertFalse(self._run_validation(sample))


class PubDateTests(unittest.TestCase):
    """Tests for article/front/article-meta/pub-date elements.
    """
    def _run_validation(self, sample):
        schematron = isoschematron.Schematron(SCH, phase='phase.pub-date')
        return schematron.validate(etree.parse(sample))

    def test_pub_type_absent(self):
        sample = """<article>
                      <front>
                        <article-meta>
                          <pub-date>
                            <day>17</day>
                            <month>03</month>
                            <year>2014</year>
                          </pub-date>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = StringIO(sample)

        self.assertFalse(self._run_validation(sample))

    def test_pub_type_allowed_values(self):
        for pub_type in ['epub', 'epub-ppub', 'collection']:
            sample = """<article>
                          <front>
                            <article-meta>
                              <pub-date pub-type="%s">
                                <day>17</day>
                                <month>03</month>
                                <year>2014</year>
                              </pub-date>
                            </article-meta>
                          </front>
                        </article>
                     """ % pub_type
            sample = StringIO(sample)

            self.assertTrue(self._run_validation(sample))

    def test_pub_type_disallowed_value(self):
        sample = """<article>
                      <front>
                        <article-meta>
                          <pub-date pub-type="wtf">
                            <day>17</day>
                            <month>03</month>
                            <year>2014</year>
                          </pub-date>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = StringIO(sample)

        self.assertFalse(self._run_validation(sample))


class VolumeTests(unittest.TestCase):
    """Tests for:
      - article/front/article-meta/volume
      - article/back/ref-list/ref/element-citation/volume
    """
    def _run_validation(self, sample):
        schematron = isoschematron.Schematron(SCH, phase='phase.volume')
        return schematron.validate(etree.parse(sample))

    def test_absent_in_front(self):
        sample = """<article>
                      <front>
                        <article-meta>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = StringIO(sample)

        self.assertFalse(self._run_validation(sample))

    def test_present_but_empty_in_front(self):
        sample = """<article>
                      <front>
                        <article-meta>
                          <volume></volume>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = StringIO(sample)

        self.assertFalse(self._run_validation(sample))

    def test_present_in_front(self):
        sample = """<article>
                      <front>
                        <article-meta>
                          <volume>10</volume>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = StringIO(sample)

        self.assertTrue(self._run_validation(sample))


class IssueTests(unittest.TestCase):
    """Tests for:
      - article/front/article-meta/issue
      - article/back/ref-list/ref/element-citation/issue
    """
    def _run_validation(self, sample):
        schematron = isoschematron.Schematron(SCH, phase='phase.issue')
        return schematron.validate(etree.parse(sample))

    def test_absent_in_front(self):
        sample = """<article>
                      <front>
                        <article-meta>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = StringIO(sample)

        self.assertFalse(self._run_validation(sample))

    def test_present_but_empty_in_front(self):
        sample = """<article>
                      <front>
                        <article-meta>
                          <issue></issue>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = StringIO(sample)

        self.assertFalse(self._run_validation(sample))

    def test_present_in_front(self):
        sample = """<article>
                      <front>
                        <article-meta>
                          <issue>10</issue>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = StringIO(sample)

        self.assertTrue(self._run_validation(sample))


class SupplementTests(unittest.TestCase):
    """Tests for:
      - article/front/article-meta/supplement
    """
    def _run_validation(self, sample):
        schematron = isoschematron.Schematron(SCH, phase='phase.supplement')
        return schematron.validate(etree.parse(sample))

    def test_absent(self):
        sample = """<article>
                      <front>
                        <article-meta>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = StringIO(sample)

        self.assertTrue(self._run_validation(sample))

    def test_present(self):
        sample = """<article>
                      <front>
                        <article-meta>
                          <supplement>Suppl 2</supplement>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = StringIO(sample)

        self.assertFalse(self._run_validation(sample))


class ElocationIdTests(unittest.TestCase):
    """Tests for:
      - article/front/article-meta/elocation-id
      - article/back/ref-list/ref/element-citation/elocation-id
    """
    def _run_validation(self, sample):
        schematron = isoschematron.Schematron(SCH, phase='phase.elocation-id')
        return schematron.validate(etree.parse(sample))

    def test_absent(self):
        sample = """<article>
                      <front>
                        <article-meta>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = StringIO(sample)

        self.assertTrue(self._run_validation(sample))

    def test_with_fpage(self):
        sample = """<article>
                      <front>
                        <article-meta>
                          <elocation-id>E27</elocation-id>
                          <fpage>12</fpage>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = StringIO(sample)

        self.assertFalse(self._run_validation(sample))

    def test_without_fpage(self):
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

    def test_absent_back(self):
        sample = """<article>
                      <back>
                        <ref-list>
                          <ref>
                            <element-citation>
                            </element-citation>
                          </ref>
                        </ref-list>
                      </back>
                    </article>
                 """
        sample = StringIO(sample)

        self.assertTrue(self._run_validation(sample))

    def test_with_fpage_back(self):
        sample = """<article>
                      <back>
                        <ref-list>
                          <ref>
                            <element-citation>
                              <elocation-id>E27</elocation-id>
                              <fpage>12</fpage>
                            </element-citation>
                          </ref>
                        </ref-list>
                      </back>
                    </article>
                 """
        sample = StringIO(sample)

        self.assertFalse(self._run_validation(sample))

    def test_without_fpage_back(self):
        sample = """<article>
                      <back>
                        <ref-list>
                          <ref>
                            <element-citation>
                              <elocation-id>E27</elocation-id>
                            </element-citation>
                          </ref>
                        </ref-list>
                      </back>
                    </article>
                 """
        sample = StringIO(sample)

        self.assertTrue(self._run_validation(sample))

    def test_with_and_without_fpage_back(self):
        sample = """<article>
                      <back>
                        <ref-list>
                          <ref>
                            <element-citation>
                              <elocation-id>E27</elocation-id>
                              <fpage>12</fpage>
                            </element-citation>
                          </ref>
                          <ref>
                            <element-citation>
                              <elocation-id>E27</elocation-id>
                            </element-citation>
                          </ref>
                        </ref-list>
                      </back>
                    </article>
                 """
        sample = StringIO(sample)

        self.assertFalse(self._run_validation(sample))


class HistoryTests(unittest.TestCase):
    """Tests for:
      - article/front/article-meta/history
    """
    def _run_validation(self, sample):
        schematron = isoschematron.Schematron(SCH, phase='phase.history')
        return schematron.validate(etree.parse(sample))

    def test_absent(self):
        sample = """<article>
                      <front>
                        <article-meta>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = StringIO(sample)

        self.assertTrue(self._run_validation(sample))

    def test_(self):
        sample = """<article>
                      <front>
                        <article-meta>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = StringIO(sample)

        self.assertTrue(self._run_validation(sample))

    def test_date_type_allowed_values(self):
        for pub_type in ['received', 'accepted', 'rev-recd']:
            sample = """<article>
                          <front>
                            <article-meta>
                              <history>
                                <date date-type="%s">
                                  <day>17</day>
                                  <month>03</month>
                                  <year>2014</year>
                                </date>
                              </history>
                            </article-meta>
                          </front>
                        </article>
                     """ % pub_type
            sample = StringIO(sample)

            self.assertTrue(self._run_validation(sample))

    def test_date_type_disallowed_values(self):
        sample = """<article>
                      <front>
                        <article-meta>
                          <history>
                            <date date-type="invalid">
                              <day>17</day>
                              <month>03</month>
                              <year>2014</year>
                            </date>
                          </history>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = StringIO(sample)

        self.assertFalse(self._run_validation(sample))

    def test_date_type_allowed_values_multi(self):
        sample = """<article>
                      <front>
                        <article-meta>
                          <history>
                            <date date-type="received">
                              <day>17</day>
                              <month>03</month>
                              <year>2014</year>
                            </date>
                            <date date-type="accepted">
                              <day>17</day>
                              <month>03</month>
                              <year>2014</year>
                            </date>
                          </history>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = StringIO(sample)

        self.assertTrue(self._run_validation(sample))


class ProductTests(unittest.TestCase):
    """Tests for:
      - article/front/article-meta/product
    """
    def _run_validation(self, sample):
        schematron = isoschematron.Schematron(SCH, phase='phase.product')
        return schematron.validate(etree.parse(sample))

    def test_absent(self):
        sample = """<article>
                      <front>
                        <article-meta>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = StringIO(sample)

        self.assertTrue(self._run_validation(sample))

    def test_absent_allowed_types(self):
        for art_type in ['book-review', 'product-review']:
            sample = """<article article-type="%s">
                          <front>
                            <article-meta>
                            </article-meta>
                          </front>
                        </article>
                     """ % art_type
            sample = StringIO(sample)

            self.assertTrue(self._run_validation(sample))

    def test_allowed_types(self):
        for art_type in ['book-review', 'product-review']:
            sample = """<article article-type="%s">
                          <front>
                            <article-meta>
                              <product product-type="book">
                                <person-group person-group-type="author">
                                  <name>
                                    <surname>Sobrenome do autor</surname>
                                    <given-names>Prenomes do autor</given-names>
                                  </name>
                                </person-group>
                                <source>Título do livro</source>
                                <year>Ano de publicação</year>
                                <publisher-name>Nome da casa publicadora/Editora</publisher-name>
                                <publisher-loc>Local de publicação</publisher-loc>
                                <page-count count="total de paginação do livro (opcional)"/>
                                <isbn>ISBN do livro, se houver</isbn>
                                <inline-graphic>1234-5678-rctb-45-05-690-gf01.tif</inline-graphic>
                              </product>
                            </article-meta>
                          </front>
                        </article>
                     """ % art_type
            sample = StringIO(sample)

            self.assertTrue(self._run_validation(sample))

    def test_disallowed_types(self):
        sample = """<article article-type="research-article">
                      <front>
                        <article-meta>
                          <product product-type="book">
                            <person-group person-group-type="author">
                              <name>
                                <surname>Sobrenome do autor</surname>
                                <given-names>Prenomes do autor</given-names>
                              </name>
                            </person-group>
                            <source>Título do livro</source>
                            <year>Ano de publicação</year>
                            <publisher-name>Nome da casa publicadora/Editora</publisher-name>
                            <publisher-loc>Local de publicação</publisher-loc>
                            <page-count count="total de paginação do livro (opcional)"/>
                            <isbn>ISBN do livro, se houver</isbn>
                            <inline-graphic>1234-5678-rctb-45-05-690-gf01.tif</inline-graphic>
                          </product>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = StringIO(sample)

        self.assertFalse(self._run_validation(sample))

    def test_no_type(self):
        sample = """<article>
                      <front>
                        <article-meta>
                          <product product-type="book">
                            <person-group person-group-type="author">
                              <name>
                                <surname>Sobrenome do autor</surname>
                                <given-names>Prenomes do autor</given-names>
                              </name>
                            </person-group>
                            <source>Título do livro</source>
                            <year>Ano de publicação</year>
                            <publisher-name>Nome da casa publicadora/Editora</publisher-name>
                            <publisher-loc>Local de publicação</publisher-loc>
                            <page-count count="total de paginação do livro (opcional)"/>
                            <isbn>ISBN do livro, se houver</isbn>
                            <inline-graphic>1234-5678-rctb-45-05-690-gf01.tif</inline-graphic>
                          </product>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = StringIO(sample)

        self.assertFalse(self._run_validation(sample))

    def test_product_type(self):
        sample = """<article article-type="book-review">
                      <front>
                        <article-meta>
                          <product>
                            <person-group person-group-type="author">
                              <name>
                                <surname>Sobrenome do autor</surname>
                                <given-names>Prenomes do autor</given-names>
                              </name>
                            </person-group>
                            <source>Título do livro</source>
                            <year>Ano de publicação</year>
                            <publisher-name>Nome da casa publicadora/Editora</publisher-name>
                            <publisher-loc>Local de publicação</publisher-loc>
                            <page-count count="total de paginação do livro (opcional)"/>
                            <isbn>ISBN do livro, se houver</isbn>
                            <inline-graphic>1234-5678-rctb-45-05-690-gf01.tif</inline-graphic>
                          </product>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = StringIO(sample)

        self.assertFalse(self._run_validation(sample))


class SecTitleTests(unittest.TestCase):
    """Tests for:
      - article/body/sec/title
    """
    def _run_validation(self, sample):
        schematron = isoschematron.Schematron(SCH, phase='phase.sectitle')
        return schematron.validate(etree.parse(sample))

    def test_absent(self):
        sample = """<article>
                      <body>
                        <sec>
                          <p>Foo bar</p>
                        </sec>
                      </body>
                    </article>
                 """
        sample = StringIO(sample)

        self.assertFalse(self._run_validation(sample))

    def test_has_title(self):
        sample = """<article>
                      <body>
                        <sec>
                          <title>Introduction</title>
                          <p>Foo bar</p>
                        </sec>
                      </body>
                    </article>
                 """
        sample = StringIO(sample)

        self.assertTrue(self._run_validation(sample))

    def test_has_empty_title(self):
        sample = """<article>
                      <body>
                        <sec>
                          <title></title>
                          <p>Foo bar</p>
                        </sec>
                      </body>
                    </article>
                 """
        sample = StringIO(sample)

        self.assertFalse(self._run_validation(sample))


class ParagraphTests(unittest.TestCase):
    """Tests for //p
    """
    def _run_validation(self, sample):
        schematron = isoschematron.Schematron(SCH, phase='phase.paragraph')
        return schematron.validate(etree.parse(sample))

    def test_sec_without_id(self):
        sample = """<article>
                      <body>
                        <sec>
                          <title>Intro</title>
                          <p>Foo bar</p>
                        </sec>
                      </body>
                    </article>
                 """
        sample = StringIO(sample)

        self.assertTrue(self._run_validation(sample))

    def test_sec_with_id(self):
        sample = """<article>
                      <body>
                        <sec>
                          <title>Intro</title>
                          <p id="p01">Foo bar</p>
                        </sec>
                      </body>
                    </article>
                 """
        sample = StringIO(sample)

        self.assertFalse(self._run_validation(sample))

    def test_body_without_id(self):
        sample = """<article>
                      <body>
                        <p>Foo bar</p>
                      </body>
                    </article>
                 """
        sample = StringIO(sample)

        self.assertTrue(self._run_validation(sample))

    def test_body_with_id(self):
        sample = """<article>
                      <body>
                        <p id="p01">Foo bar</p>
                      </body>
                    </article>
                 """
        sample = StringIO(sample)

        self.assertFalse(self._run_validation(sample))


class ParagraphTests(unittest.TestCase):
    """Tests for //disp-formula
    """
    def _run_validation(self, sample):
        schematron = isoschematron.Schematron(SCH, phase='phase.disp-formula')
        return schematron.validate(etree.parse(sample))

    def test_without_id_prefix(self):
        sample = """<article>
                      <body>
                        <sec>
                          <title>Intro</title>
                          <p>
                            Foo bar
                            <disp-formula>
                              <tex-math id="M1">
                              </tex-math>
                            </disp-formula>
                          </p>
                        </sec>
                      </body>
                    </article>
                 """
        sample = StringIO(sample)

        self.assertFalse(self._run_validation(sample))

    def test_wrong_id_prefix(self):
        sample = """<article>
                      <body>
                        <sec>
                          <title>Intro</title>
                          <p>
                            Foo bar
                            <disp-formula id="x01">
                              <tex-math id="M1">
                              </tex-math>
                            </disp-formula>
                          </p>
                        </sec>
                      </body>
                    </article>
                 """
        sample = StringIO(sample)

        self.assertFalse(self._run_validation(sample))

    def test_id_prefix(self):
        sample = """<article>
                      <body>
                        <sec>
                          <title>Intro</title>
                          <p>
                            Foo bar
                            <disp-formula id="e01">
                              <tex-math id="M1">
                              </tex-math>
                            </disp-formula>
                          </p>
                        </sec>
                      </body>
                    </article>
                 """
        sample = StringIO(sample)

        self.assertTrue(self._run_validation(sample))

    def test_repeated_id(self):
        sample = """<article>
                      <body>
                        <sec>
                          <title>Intro</title>
                          <p>
                            Foo bar
                            <disp-formula id="e01">
                              <tex-math id="M1">
                              </tex-math>
                            </disp-formula>
                            <disp-formula id="e01">
                              <tex-math id="M2">
                              </tex-math>
                            </disp-formula>
                          </p>
                        </sec>
                      </body>
                    </article>
                 """
        sample = StringIO(sample)

        self.assertFalse(self._run_validation(sample))

    def test_unique_id(self):
        sample = """<article>
                      <body>
                        <sec>
                          <title>Intro</title>
                          <p>
                            Foo bar
                            <disp-formula id="e01">
                              <tex-math id="M1">
                              </tex-math>
                            </disp-formula>
                            <disp-formula id="e02">
                              <tex-math id="M2">
                              </tex-math>
                            </disp-formula>
                          </p>
                        </sec>
                      </body>
                    </article>
                 """
        sample = StringIO(sample)

        self.assertTrue(self._run_validation(sample))

