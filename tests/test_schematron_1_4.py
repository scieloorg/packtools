# coding: utf-8
from __future__ import unicode_literals
import unittest
import io

from lxml import isoschematron, etree

from packtools.catalogs import SCHEMAS


SCH = etree.parse(SCHEMAS['sps-1.4'])


def TestPhase(phase_name, cache):
    """Factory of parsed Schematron phases.

    :param phase_name: the phase name
    :param cache: mapping type
    """
    if phase_name not in cache:
        phase = isoschematron.Schematron(SCH, phase=phase_name)
        cache[phase_name] = phase

    return cache[phase_name]


class PhaseBasedTestCase(unittest.TestCase):
    cache = {}

    def _run_validation(self, sample):
        schematron = TestPhase(self.sch_phase, self.cache)
        return schematron.validate(etree.parse(sample))


class JournalIdTests(PhaseBasedTestCase):
    """Tests for article/front/journal-meta/journal-id elements.

    Ticket #14 makes @journal-id-type="publisher-id" mandatory.
    Ref: https://github.com/scieloorg/scielo_publishing_schema/issues/14
    """
    sch_phase = 'phase.journal-id'

    def test_case1(self):
        """
        presence(@nlm-ta) is True
        presence(@publisher-id) is True
        """
        sample = u"""<article>
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
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))

    def test_case2(self):
        """
        presence(@nlm-ta) is True
        presence(@publisher-id) is False
        """
        sample = u"""<article>
                      <front>
                        <journal-meta>
                          <journal-id journal-id-type="nlm-ta">
                            Rev Saude Publica
                          </journal-id>
                        </journal-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_case3(self):
        """
        presence(@nlm-ta) is False
        presence(@publisher-id) is True
        """
        sample = u"""<article>
                      <front>
                        <journal-meta>
                          <journal-id journal-id-type="publisher-id">
                            RSP
                          </journal-id>
                        </journal-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))

    def test_case4(self):
        """
        presence(@nlm-ta) is False
        presence(@publisher-id) is False
        """
        sample = u"""<article>
                      <front>
                        <journal-meta>
                          <journal-id journal-id-type='doi'>
                            123.plin
                          </journal-id>
                        </journal-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_publisher_id_cannot_be_empty(self):
        sample = u"""<article>
                      <front>
                        <journal-meta>
                          <journal-id journal-id-type="publisher-id"></journal-id>
                        </journal-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))


class JournalTitleGroupTests(PhaseBasedTestCase):
    """Tests for article/front/journal-meta/journal-title-group elements.
    """
    sch_phase = 'phase.journal-title-group'

    def test_journal_title_group_is_absent(self):
        sample = u"""<article>
                      <front>
                        <journal-meta>
                        </journal-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))


    def test_case1(self):
        """
        A: presence(journal-title) is True
        B: presence(abbrev-journal-title[@abbrev-type='publisher']) is True
        A ^ B is True
        """
        sample = u"""<article>
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
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))

    def test_case2(self):
        """
        A: presence(journal-title) is True
        B: presence(abbrev-journal-title[@abbrev-type='publisher']) is False
        A ^ B is False
        """
        sample = u"""<article>
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
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_case3(self):
        """
        A: presence(journal-title) is False
        B: presence(abbrev-journal-title[@abbrev-type='publisher']) is True
        A ^ B is False
        """
        sample = u"""<article>
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
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_case4(self):
        """
        A: presence(journal-title) is False
        B: presence(abbrev-journal-title[@abbrev-type='publisher']) is False
        A ^ B is False
        """
        sample = u"""<article>
                      <front>
                        <journal-meta>
                          <journal-title-group>
                          </journal-title-group>
                        </journal-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_empty_journal_title(self):
        sample = u"""<article>
                      <front>
                        <journal-meta>
                          <journal-title-group>
                            <journal-title></journal-title>
                            <abbrev-journal-title abbrev-type='publisher'>Rev. Saude Publica</abbrev-journal-title>
                          </journal-title-group>
                        </journal-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_empty_abbrev_journal_title(self):
        sample = u"""<article>
                      <front>
                        <journal-meta>
                          <journal-title-group>
                            <journal-title>Revista de Saude Publica</journal-title>
                            <abbrev-journal-title abbrev-type='publisher'></abbrev-journal-title>
                          </journal-title-group>
                        </journal-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))


class PublisherTests(PhaseBasedTestCase):
    """Tests for article/front/journal-meta/publisher elements.
    """
    sch_phase = 'phase.publisher'

    def test_publisher_is_present(self):
        sample = u"""<article>
                      <front>
                        <journal-meta>
                          <publisher>
                            <publisher-name>British Medical Journal</publisher-name>
                          </publisher>
                        </journal-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))

    def test_publisher_is_absent(self):
        sample = u"""<article>
                      <front>
                        <journal-meta>
                        </journal-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_publisher_is_empty(self):
        sample = u"""<article>
                      <front>
                        <journal-meta>
                          <publisher>
                            <publisher-name></publisher-name>
                          </publisher>
                        </journal-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))


class ArticleCategoriesTests(PhaseBasedTestCase):
    """Tests for article/front/article-meta/article-categories elements.
    """
    sch_phase = 'phase.article-categories'

    def test_article_categories_is_present(self):
        sample = u"""<article>
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
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))

    def test_article_categories_is_absent(self):
        sample = u"""<article>
                      <front>
                        <article-meta>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))


class fpage_OR_elocationTests(PhaseBasedTestCase):
    """Tests for article/front/article-meta/fpage or elocation-id elements.
    """
    sch_phase = 'phase.fpage_or_elocation-id'

    def test_case1(self):
        """
        fpage is True
        elocation-id is True
        fpage v elocation-id is True
        """
        sample = u"""<article>
                      <front>
                        <article-meta>
                          <fpage>01</fpage>
                          <elocation-id>E27</elocation-id>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))

    def test_case2(self):
        """
        fpage is True
        elocation-id is False
        fpage v elocation-id is True
        """
        sample = u"""<article>
                      <front>
                        <article-meta>
                          <fpage>01</fpage>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))

    def test_case3(self):
        """
        fpage is False
        elocation-id is True
        fpage v elocation-id is True
        """
        sample = u"""<article>
                      <front>
                        <article-meta>
                          <elocation-id>E27</elocation-id>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))

    def test_case4(self):
        """
        fpage is False
        elocation-id is False
        fpage v elocation-id is False
        """
        sample = u"""<article>
                      <front>
                        <article-meta>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_empty_fpage(self):
        sample = u"""<article>
                      <front>
                        <article-meta>
                          <fpage></fpage>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_empty_elocationid(self):
        sample = u"""<article>
                      <front>
                        <article-meta>
                          <elocation-id></elocation-id>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))


class ISSNTests(PhaseBasedTestCase):
    """Tests for article/front/journal-meta/issn elements.
    """
    sch_phase = 'phase.issn'

    def test_case1(self):
        """
        A: @pub-type='epub' is True
        B: @pub-type='ppub' is True
        A v B is True
        """
        sample = u"""<article>
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
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))

    def test_case2(self):
        """
        A: @pub-type='epub' is True
        B: @pub-type='ppub' is False
        A v B is True
        """
        sample = u"""<article>
                      <front>
                        <journal-meta>
                          <issn pub-type="epub">
                            0959-8138
                          </issn>
                        </journal-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))

    def test_case3(self):
        """
        A: @pub-type='epub' is False
        B: @pub-type='ppub' is True
        A v B is True
        """
        sample = u"""<article>
                      <front>
                        <journal-meta>
                          <issn pub-type="ppub">
                            0959-813X
                          </issn>
                        </journal-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))

    def test_case4(self):
        """
        A: @pub-type='epub' is False
        B: @pub-type='ppub' is False
        A v B is False
        """
        sample = u"""<article>
                      <front>
                        <journal-meta>
                          <issn>
                            0959-813X
                          </issn>
                        </journal-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_empty_issn(self):
        sample = u"""<article>
                      <front>
                        <journal-meta>
                          <issn pub-type="epub"></issn>
                        </journal-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))


class ArticleIdTests(PhaseBasedTestCase):
    """Tests for article/front/article-meta/article-id elements.
    """
    sch_phase = 'phase.article-id'

    def test_article_id_is_absent(self):
        sample = u"""<article>
                      <front>
                        <article-meta>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))


    def test_pub_id_type_doi_is_absent(self):
        sample = u"""<article>
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
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))

    def test_pub_id_type_doi(self):
        sample = u"""<article>
                      <front>
                        <article-meta>
                          <article-id pub-id-type='doi'>
                            10.1590/1414-431X20143434
                          </article-id>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))

    def test_pub_id_type_doi_is_empty(self):
        sample = u"""<article>
                      <front>
                        <article-meta>
                          <article-id pub-id-type='doi'/>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_invalid_pub_id_type(self):
        sample = u"""<article>
                      <front>
                        <article-meta>
                          <article-id pub-id-type='unknown'>
                            10.1590/1414-431X20143434
                          </article-id>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_invalid_pub_id_type_case2(self):
        sample = u"""<article>
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
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_valid_pub_id_type_values(self):
        for typ in ['doi', 'publisher-id', 'other']:
            sample = u"""<article>
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
            sample = io.BytesIO(sample.encode('utf-8'))
            self.assertTrue(self._run_validation(sample))


class SubjGroupTests(PhaseBasedTestCase):
    """Tests for article/front/article-meta/article-categories/subj-group elements.
    """
    sch_phase = 'phase.subj-group'

    def test_subj_group_is_absent(self):
        sample = u"""<article>
                      <front>
                        <article-meta>
                          <article-categories>
                          </article-categories>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_without_heading_type(self):
        sample = u"""<article>
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
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_with_heading_type(self):
        sample = u"""<article>
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
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))

    def test_with_heading_in_subarticle_pt(self):
        sample = u"""<article>
                      <front>
                        <article-meta>
                          <article-categories>
                            <subj-group subj-group-type="heading">
                              <subject>
                                Original Article
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
                      <sub-article xml:lang="pt" article-type="translation" id="S01">
                        <front-stub>
                          <article-categories>
                            <subj-group subj-group-type="heading">
                              <subject>Artigos Originais</subject>
                            </subj-group>
                          </article-categories>
                        </front-stub>
                      </sub-article>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))

    def test_with_many_heading_in_subarticle_pt(self):
        sample = u"""<article>
                      <front>
                        <article-meta>
                          <article-categories>
                            <subj-group subj-group-type="heading">
                              <subject>
                                Original Article
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
                      <sub-article xml:lang="pt" article-type="translation" id="S01">
                        <front-stub>
                          <article-categories>
                            <subj-group subj-group-type="heading">
                              <subject>Artigos Originais</subject>
                            </subj-group>
                            <subj-group subj-group-type="heading">
                              <subject>Artigos Piratas</subject>
                            </subj-group>
                          </article-categories>
                        </front-stub>
                      </sub-article>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_with_heading_type_in_the_deep(self):
        sample = u"""<article>
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
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))

    def test_with_many_heading_type(self):
        sample = u"""<article>
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
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))


class AbstractLangTests(PhaseBasedTestCase):
    """Tests for article/front/article-meta/abstract elements.
    """
    sch_phase = 'phase.abstract_lang'

    def test_is_present(self):
        sample = u"""<article>
                      <front>
                        <article-meta>
                          <abstract>
                            <p>Differing socioeconomic positions in...</p>
                          </abstract>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))

    def test_is_absent(self):
        sample = u"""<article>
                      <front>
                        <article-meta>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))

    def test_is_present_with_lang(self):
        sample = u"""<?xml version="1.0" encoding="UTF-8"?>
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
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_missing_for_research_article(self):
        sample = u"""<?xml version="1.0" encoding="UTF-8"?>
                    <article article-type="research-article">
                      <front>
                        <article-meta>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_research_article(self):
        sample = u"""<?xml version="1.0" encoding="UTF-8"?>
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
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))

    def test_research_article_only_with_transabstract(self):
        sample = u"""<?xml version="1.0" encoding="UTF-8"?>
                    <article article-type="research-article">
                      <front>
                        <article-meta>
                          <trans-abstract xml:lang="en">
                            <p>Differing socioeconomic positions in...</p>
                          </trans-abstract>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))

    def test_missing_for_review_article(self):
        sample = u"""<?xml version="1.0" encoding="UTF-8"?>
                    <article article-type="review-article">
                      <front>
                        <article-meta>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_review_article(self):
        sample = u"""<?xml version="1.0" encoding="UTF-8"?>
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
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))

    def test_review_article_only_with_transabstract(self):
        sample = u"""<?xml version="1.0" encoding="UTF-8"?>
                    <article article-type="review-article">
                      <front>
                        <article-meta>
                          <trans-abstract xml:lang="en">
                            <p>Differing socioeconomic positions in...</p>
                          </trans-abstract>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))


class ArticleTitleLangTests(PhaseBasedTestCase):
    """Tests for article/front/article-meta/title-group/article-title elements.
    """
    sch_phase = 'phase.article-title_lang'

    def test_is_present_in_articlemeta(self):
        sample = u"""<article>
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
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))

    def test_is_present_in_articlemeta_with_lang(self):
        sample = u"""<article>
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
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_is_present_in_elementcitation(self):
        sample = u"""<article>
                      <back>
                        <ref-list>
                          <ref>
                            <mixed-citation>Aires M, Paz AA, Perosa CT. Situação de saúde e grau de dependência de pessoas idosas institucionalizadas. <italic>Rev Gaucha Enferm.</italic> 2009;30(3):192-9.</mixed-citation>
                            <element-citation publication-type="journal">
                              <person-group person-group-type="author">
                                <name>
                                  <surname>Aires</surname>
                                  <given-names>M</given-names>
                                </name>
                                <name>
                                  <surname>Paz</surname>
                                  <given-names>AA</given-names>
                                </name>
                                <name>
                                  <surname>Perosa</surname>
                                  <given-names>CT</given-names>
                                </name>
                              </person-group>
                              <article-title>Situação de saúde e grau de dependência de pessoas idosas institucionalizadas</article-title>
                              <source>Rev Gaucha Enferm</source>
                              <year>2009</year>
                              <volume>30</volume>
                              <issue>3</issue>
                              <fpage>192</fpage>
                              <lpage>199</lpage>
                            </element-citation>
                          </ref>
                        </ref-list>
                      </back>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))

    def test_is_present_in_elementcitation_with_lang(self):
        sample = u"""<article>
                      <back>
                        <ref-list>
                          <ref>
                            <mixed-citation>Aires M, Paz AA, Perosa CT. Situação de saúde e grau de dependência de pessoas idosas institucionalizadas. <italic>Rev Gaucha Enferm.</italic> 2009;30(3):192-9.</mixed-citation>
                            <element-citation publication-type="journal">
                              <person-group person-group-type="author">
                                <name>
                                  <surname>Aires</surname>
                                  <given-names>M</given-names>
                                </name>
                                <name>
                                  <surname>Paz</surname>
                                  <given-names>AA</given-names>
                                </name>
                                <name>
                                  <surname>Perosa</surname>
                                  <given-names>CT</given-names>
                                </name>
                              </person-group>
                              <article-title xml:lang="pt">Situação de saúde e grau de dependência de pessoas idosas institucionalizadas</article-title>
                              <source>Rev Gaucha Enferm</source>
                              <year>2009</year>
                              <volume>30</volume>
                              <issue>3</issue>
                              <fpage>192</fpage>
                              <lpage>199</lpage>
                            </element-citation>
                          </ref>
                        </ref-list>
                      </back>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))


class KwdGroupLangTests(PhaseBasedTestCase):
    """Tests for article/front/article-meta/kwd-group elements.
    """
    sch_phase = 'phase.kwd-group_lang'

    def test_single_occurence(self):
        sample = u"""<article>
                      <front>
                        <article-meta>
                          <kwd-group>
                            <kwd>gene expression</kwd>
                          </kwd-group>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_many_occurencies(self):
        sample = u"""<article>
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
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))

    def test_many_occurencies_without_lang(self):
        sample = u"""<article>
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
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))


class AffContentTypeTests(PhaseBasedTestCase):
    """Tests for:
      - article/front/article-meta/contrib-group
      - article/front/article-meta
    """
    sch_phase = 'phase.aff_contenttypes'

    def test_original_is_present(self):
        sample = u"""<article>
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
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))

    def test_original_is_absent(self):
        sample = u"""<article>
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
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_many_original(self):
        sample = u"""<article>
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
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_original_is_present_and_absent(self):
        sample = u"""<article>
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
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_original_is_present_and_present(self):
        sample = u"""<article>
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
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))

    def test_allowed_orgdiv1(self):
        sample = u"""<article>
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
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))

    def test_allowed_orgdiv2(self):
        sample = u"""<article>
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
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))

    def test_allowed_orgdiv3(self):
        sample = u"""<article>
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
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))

    def test_allowed_normalized(self):
        sample = u"""<article>
                      <front>
                        <article-meta>
                          <aff>
                            <institution content-type="original">
                              Grupo de ...
                            </institution>
                            <institution content-type="normalized">
                              Instituto de Matematica e Estatistica
                            </institution>
                          </aff>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))

    def test_disallowed_orgdiv4(self):
        sample = u"""<article>
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
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_orgname_inside_contrib_group(self):
        sample = u"""<article>
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
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))


class CountsTests(PhaseBasedTestCase):
    """Tests for article/front/article-meta/counts elements.
    """
    sch_phase = 'phase.counts'

    def test_absent(self):
        sample = u"""<article>
                      <front>
                        <article-meta>
                          <fpage>0</fpage>
                          <lpage>0</lpage>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))

    def test_table_is_absent(self):
        sample = u"""<article>
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
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))

    def test_ref_is_absent(self):
        sample = u"""<article>
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
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))

    def test_fig_is_absent(self):
        sample = u"""<article>
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
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))

    def test_equation_is_absent(self):
        sample = u"""<article>
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
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))

    def test_page_is_absent(self):
        sample = u"""<article>
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
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))

    def test_tables(self):
        sample = u"""<article>
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
                            <table-wrap>
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
                            </table-wrap>
                          </p>
                        </sec>
                      </body>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))

    def test_tables_as_graphic(self):
        sample = u"""<article xmlns:xlink="http://www.w3.org/1999/xlink">
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
                            <table-wrap id="t01">
                              <graphic mimetype="image"
                                       xlink:href="1414-431X-bjmbr-1414-431X20142875-gt001">
                              </graphic>
                            </table-wrap>
                          </p>
                        </sec>
                      </body>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))

    def test_ref(self):
        sample = u"""<article>
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
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))

    def test_fig(self):
        sample = u"""<article xmlns:xlink="http://www.w3.org/1999/xlink">
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
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))

    def test_equation(self):
        sample = u"""<article xmlns:xlink="http://www.w3.org/1999/xlink">
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
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))

    def test_page(self):
        sample = u"""<article xmlns:xlink="http://www.w3.org/1999/xlink">
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
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))

    def test_page_wrong_count(self):
        sample = u"""<article xmlns:xlink="http://www.w3.org/1999/xlink">
                      <front>
                        <article-meta>
                          <counts>
                            <table-count count="0"/>
                            <ref-count count="0"/>
                            <fig-count count="0"/>
                            <equation-count count="0"/>
                            <page-count count="50"/>
                          </counts>
                          <fpage>140</fpage>
                          <lpage>150</lpage>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_non_digit_pages(self):
        """Non-digit page interval cannot be checked automatically.
        """
        sample = u"""<article xmlns:xlink="http://www.w3.org/1999/xlink">
                      <front>
                        <article-meta>
                          <counts>
                            <table-count count="0"/>
                            <ref-count count="0"/>
                            <fig-count count="0"/>
                            <equation-count count="0"/>
                            <page-count count="11"/>
                          </counts>
                          <fpage>A140</fpage>
                          <lpage>A150</lpage>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))

    def test_elocationid_pages(self):
        """Electronic pagination cannot be checked automatically.
        """
        sample = u"""<article xmlns:xlink="http://www.w3.org/1999/xlink">
                      <front>
                        <article-meta>
                          <counts>
                            <table-count count="0"/>
                            <ref-count count="0"/>
                            <fig-count count="0"/>
                            <equation-count count="0"/>
                            <page-count count="11"/>
                          </counts>
                          <elocation-id>A140</elocation-id>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))


class AuthorNotesTests(PhaseBasedTestCase):
    """Tests for article/front/article-meta/author-notes elements.
    """
    sch_phase = 'phase.fn-group'

    def test_allowed_fn_types(self):
        for fn_type in ['author', 'con', 'conflict', 'corresp', 'current-aff',
                'deceased', 'edited-by', 'equal', 'on-leave', 'participating-researchers',
                'present-address', 'previously-at', 'study-group-members', 'other']:

            sample = u"""<article>
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
            sample = io.BytesIO(sample.encode('utf-8'))

            self.assertTrue(self._run_validation(sample))

    def test_disallowed_fn_types(self):
        sample = u"""<article>
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
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))


class PubDateTests(PhaseBasedTestCase):
    """Tests for article/front/article-meta/pub-date elements.
    """
    sch_phase = 'phase.pub-date'

    def test_pub_type_absent(self):
        sample = u"""<article>
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
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_pub_type_allowed_values(self):
        for pub_type in ['epub', 'epub-ppub', 'collection']:
            sample = u"""<article>
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
            sample = io.BytesIO(sample.encode('utf-8'))

            self.assertTrue(self._run_validation(sample))

    def test_pub_type_disallowed_value(self):
        sample = u"""<article>
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
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))


class VolumeTests(PhaseBasedTestCase):
    """Tests for:
      - article/front/article-meta/volume
      - article/back/ref-list/ref/element-citation/volume
    """
    sch_phase = 'phase.volume'

    def test_absent_in_front(self):
        sample = u"""<article>
                      <front>
                        <article-meta>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))

    def test_present_but_empty_in_front(self):
        sample = u"""<article>
                      <front>
                        <article-meta>
                          <volume></volume>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_present_in_front(self):
        sample = u"""<article>
                      <front>
                        <article-meta>
                          <volume>10</volume>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))


class IssueTests(PhaseBasedTestCase):
    """Tests for:
      - article/front/article-meta/issue
      - article/back/ref-list/ref/element-citation/issue
    """
    sch_phase = 'phase.issue'

    def test_absent_in_front(self):
        sample = u"""<article>
                      <front>
                        <article-meta>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))

    def test_present_but_empty_in_front(self):
        sample = u"""<article>
                      <front>
                        <article-meta>
                          <issue></issue>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_present_in_front(self):
        sample = u"""<article>
                      <front>
                        <article-meta>
                          <issue>10</issue>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))

    def test_special_number_support(self):
        sample = u"""<article>
                      <front>
                        <article-meta>
                          <issue>spe</issue>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))


class SupplementTests(PhaseBasedTestCase):
    """Tests for:
      - article/front/article-meta/supplement
    """
    sch_phase = 'phase.supplement'

    def test_absent(self):
        sample = u"""<article>
                      <front>
                        <article-meta>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))

    def test_present(self):
        sample = u"""<article>
                      <front>
                        <article-meta>
                          <supplement>Suppl 2</supplement>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))


class ElocationIdTests(PhaseBasedTestCase):
    """Tests for:
      - article/front/article-meta/elocation-id
      - article/back/ref-list/ref/element-citation/elocation-id
    """
    sch_phase = 'phase.elocation-id'

    def test_absent(self):
        sample = u"""<article>
                      <front>
                        <article-meta>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))

    def test_with_fpage(self):
        sample = u"""<article>
                      <front>
                        <article-meta>
                          <elocation-id>E27</elocation-id>
                          <fpage>12</fpage>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_without_fpage(self):
        sample = u"""<article>
                      <front>
                        <article-meta>
                          <elocation-id>E27</elocation-id>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))

    def test_absent_back(self):
        sample = u"""<article>
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
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))

    def test_with_fpage_back(self):
        sample = u"""<article>
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
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_without_fpage_back(self):
        sample = u"""<article>
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
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))

    def test_with_and_without_fpage_back(self):
        sample = u"""<article>
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
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))


class HistoryTests(PhaseBasedTestCase):
    """Tests for:
      - article/front/article-meta/history
    """
    sch_phase = 'phase.history'

    def test_absent(self):
        sample = u"""<article>
                      <front>
                        <article-meta>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))

    def test_(self):
        sample = u"""<article>
                      <front>
                        <article-meta>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))

    def test_date_type_allowed_values(self):
        for pub_type in ['received', 'accepted', 'rev-recd']:
            sample = u"""<article>
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
            sample = io.BytesIO(sample.encode('utf-8'))

            self.assertTrue(self._run_validation(sample))

    def test_date_type_disallowed_values(self):
        sample = u"""<article>
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
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_date_type_allowed_values_multi(self):
        sample = u"""<article>
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
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))


class ProductTests(PhaseBasedTestCase):
    """Tests for:
      - article/front/article-meta/product
    """
    sch_phase = 'phase.product'

    def test_absent(self):
        sample = u"""<article>
                      <front>
                        <article-meta>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))

    def test_absent_allowed_types(self):
        for art_type in ['book-review', 'product-review']:
            sample = u"""<article article-type="%s">
                          <front>
                            <article-meta>
                            </article-meta>
                          </front>
                        </article>
                     """ % art_type
            sample = io.BytesIO(sample.encode('utf-8'))

            self.assertTrue(self._run_validation(sample))

    def test_allowed_types(self):
        for art_type in ['book-review', 'product-review']:
            sample = u"""<article article-type="%s">
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
            sample = io.BytesIO(sample.encode('utf-8'))

            self.assertTrue(self._run_validation(sample))

    def test_disallowed_types(self):
        sample = u"""<article article-type="research-article">
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
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_no_type(self):
        sample = u"""<article>
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
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_product_type(self):
        sample = u"""<article article-type="book-review">
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
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_allowed_product_types(self):
        for prod_type in ['book', 'software', 'article', 'chapter', 'other']:
            sample = u"""<article article-type="book-review">
                          <front>
                            <article-meta>
                              <product product-type="%s">
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
                     """ % prod_type
            sample = io.BytesIO(sample.encode('utf-8'))

            self.assertTrue(self._run_validation(sample))

    def test_disallowed_product_types(self):
        sample = u"""<article article-type="book-review">
                      <front>
                        <article-meta>
                          <product product-type="invalid">
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
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))


class SecTitleTests(PhaseBasedTestCase):
    """Tests for:
      - article/body/sec/title
    """
    sch_phase = 'phase.sectitle'

    def test_absent(self):
        sample = u"""<article>
                      <body>
                        <sec>
                          <p>Foo bar</p>
                        </sec>
                      </body>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_has_title(self):
        sample = u"""<article>
                      <body>
                        <sec>
                          <title>Introduction</title>
                          <p>Foo bar</p>
                        </sec>
                      </body>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))

    def test_has_empty_title(self):
        sample = u"""<article>
                      <body>
                        <sec>
                          <title></title>
                          <p>Foo bar</p>
                        </sec>
                      </body>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))


class ParagraphTests(PhaseBasedTestCase):
    """Tests for //p
    """
    sch_phase = 'phase.paragraph'

    def test_sec_without_id(self):
        sample = u"""<article>
                      <body>
                        <sec>
                          <title>Intro</title>
                          <p>Foo bar</p>
                        </sec>
                      </body>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))

    def test_sec_with_id(self):
        sample = u"""<article>
                      <body>
                        <sec>
                          <title>Intro</title>
                          <p id="p01">Foo bar</p>
                        </sec>
                      </body>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_body_without_id(self):
        sample = u"""<article>
                      <body>
                        <p>Foo bar</p>
                      </body>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))

    def test_body_with_id(self):
        sample = u"""<article>
                      <body>
                        <p id="p01">Foo bar</p>
                      </body>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))


class XrefRidTests(PhaseBasedTestCase):
    """Tests for //xref[@rid]
    """
    sch_phase = 'phase.rid_integrity'

    def test_mismatching_rid(self):
        sample = u"""<article>
                      <front>
                        <article-meta>
                          <contrib-group>
                            <contrib>
                              <xref ref-type="aff" rid="aff1">
                                <sup>I</sup>
                              </xref>
                            </contrib>
                          </contrib-group>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_matching_rid(self):
        sample = u"""<article>
                      <front>
                        <article-meta>
                          <contrib-group>
                            <contrib>
                              <xref ref-type="aff" rid="aff1">
                                <sup>I</sup>
                              </xref>
                            </contrib>
                          </contrib-group>
                          <aff id="aff1">
                            <label>I</label>
                            <institution content-type="orgname">
                              Secretaria Municipal de Saude de Belo Horizonte
                            </institution>
                            <addr-line>
                              <named-content content-type="city">Belo Horizonte</named-content>
                              <named-content content-type="state">MG</named-content>
                            </addr-line>
                            <country>Brasil</country>
                            <institution content-type="original">
                              Secretaria Municipal de Saude de Belo Horizonte. Belo Horizonte, MG, Brasil
                            </institution>
                          </aff>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))

    def test_mismatching_reftype(self):
        sample = u"""<article>
                      <body>
                        <sec>
                          <table-wrap id="t01">
                          </table-wrap>
                        </sec>
                        <sec>
                          <p>
                            <xref ref-type="aff" rid="t01">table 1</xref>
                          </p>
                        </sec>
                      </body>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))


class XrefRefTypeTests(PhaseBasedTestCase):
    """Tests for //xref[@ref-type]
    """
    sch_phase = 'phase.xref_reftype_integrity'

    def test_allowed_ref_types(self):
        for reftype in ['aff', 'app', 'author-notes', 'bibr', 'contrib',
                        'corresp', 'disp-formula', 'fig', 'fn', 'sec',
                        'supplementary-material', 'table', 'table-fn',
                        'boxed-text']:
            sample = u"""<article>
                          <body>
                            <sec>
                              <p>
                                <xref ref-type="%s">foo</xref>
                              </p>
                            </sec>
                          </body>
                        </article>
                     """ % reftype
            sample = io.BytesIO(sample.encode('utf-8'))

            self.assertTrue(self._run_validation(sample))

    def test_disallowed_ref_types(self):
        for reftype in ['chem', 'kwd', 'list', 'other', 'plate'
                        'scheme', 'statement']:
            sample = u"""<article>
                          <body>
                            <sec>
                              <p>
                                <xref ref-type="%s">foo</xref>
                              </p>
                            </sec>
                          </body>
                        </article>
                     """ % reftype
            sample = io.BytesIO(sample.encode('utf-8'))

            self.assertFalse(self._run_validation(sample))


class CaptionTests(PhaseBasedTestCase):
    """Tests for //caption
    """
    sch_phase = 'phase.caption'

    def test_with_title(self):
        sample = u"""<article xmlns:xlink="http://www.w3.org/1999/xlink">
                      <body>
                        <fig id="f03">
                          <label>Figura 3</label>
                          <caption>
                            <title>
                              Percentual de atividade mitocondrial.
                            </title>
                          </caption>
                          <graphic xlink:href="1234-5678-rctb-45-05-0110-gf01.tif"/>
                        </fig>
                      </body>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))

    def test_without_title(self):
        sample = u"""<article xmlns:xlink="http://www.w3.org/1999/xlink">
                      <body>
                        <fig id="f03">
                          <label>Figura 3</label>
                          <caption>
                            <label>
                              Percentual de atividade mitocondrial.
                            </label>
                          </caption>
                          <graphic xlink:href="1234-5678-rctb-45-05-0110-gf01.tif"/>
                        </fig>
                      </body>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_with_title_and_more(self):
        sample = u"""<article xmlns:xlink="http://www.w3.org/1999/xlink">
                      <body>
                        <fig id="f03">
                          <label>Figura 3</label>
                          <caption>
                            <title>
                              Percentual de atividade mitocondrial.
                            </title>
                            <label>
                              Percentual de atividade mitocondrial.
                            </label>
                          </caption>
                          <graphic xlink:href="1234-5678-rctb-45-05-0110-gf01.tif"/>
                        </fig>
                      </body>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))


class LicenseTests(PhaseBasedTestCase):
    """Tests for article/front/article-meta/permissions/license element.
    """
    sch_phase = 'phase.license'

    def test_missing_permissions_elem(self):
        sample = u"""<article xmlns:xlink="http://www.w3.org/1999/xlink">
                      <front>
                        <article-meta>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_missing_license(self):
        sample = u"""<article xmlns:xlink="http://www.w3.org/1999/xlink">
                      <front>
                        <article-meta>
                          <permissions>
                          </permissions>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_allowed_license_type(self):
        sample = u"""<article xmlns:xlink="http://www.w3.org/1999/xlink">
                      <front>
                        <article-meta>
                          <permissions>
                            <license license-type="open-access"
                                     xlink:href="http://creativecommons.org/licenses/by/4.0/"
                                     xml:lang="en">
                              <license-p>
                                This is an open-access article distributed under the terms...
                              </license-p>
                            </license>
                          </permissions>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))

    def test_disallowed_license_type(self):
        sample = u"""<article xmlns:xlink="http://www.w3.org/1999/xlink">
                      <front>
                        <article-meta>
                          <permissions>
                            <license license-type="closed-access"
                                     xlink:href="http://creativecommons.org/licenses/by/4.0/"
                                     xml:lang="en">
                              <license-p>
                                This is an open-access article distributed under the terms...
                              </license-p>
                            </license>
                          </permissions>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_allowed_license_href(self):
        allowed_licenses = [
            'http://creativecommons.org/licenses/by-nc/4.0/',
            'http://creativecommons.org/licenses/by-nc/3.0/',
            'http://creativecommons.org/licenses/by/4.0/',
            'http://creativecommons.org/licenses/by/3.0/',
            'http://creativecommons.org/licenses/by-nc-nd/4.0/',
            'http://creativecommons.org/licenses/by-nc-nd/3.0/',
            'http://creativecommons.org/licenses/by/3.0/igo/',
            'http://creativecommons.org/licenses/by-nc/3.0/igo/',
            'http://creativecommons.org/licenses/by-nc-nd/3.0/igo/',
        ]

        for license in allowed_licenses:
            sample = u"""<article xmlns:xlink="http://www.w3.org/1999/xlink">
                          <front>
                            <article-meta>
                              <permissions>
                                <license license-type="open-access"
                                         xlink:href="%s"
                                         xml:lang="en">
                                  <license-p>
                                    This is an open-access article distributed under the terms...
                                  </license-p>
                                </license>
                              </permissions>
                            </article-meta>
                          </front>
                        </article>
                     """ % license
            sample = io.BytesIO(sample.encode('utf-8'))

            self.assertTrue(self._run_validation(sample))

    def test_allowed_license_href_https_scheme(self):
        allowed_licenses = [
            'https://creativecommons.org/licenses/by-nc/4.0/',
            'https://creativecommons.org/licenses/by-nc/3.0/',
            'https://creativecommons.org/licenses/by/4.0/',
            'https://creativecommons.org/licenses/by/3.0/',
            'https://creativecommons.org/licenses/by-nc-nd/4.0/',
            'https://creativecommons.org/licenses/by-nc-nd/3.0/',
            'https://creativecommons.org/licenses/by/3.0/igo/',
            'https://creativecommons.org/licenses/by-nc/3.0/igo/',
            'https://creativecommons.org/licenses/by-nc-nd/3.0/igo/',
        ]

        for license in allowed_licenses:
            sample = u"""<article xmlns:xlink="http://www.w3.org/1999/xlink">
                          <front>
                            <article-meta>
                              <permissions>
                                <license license-type="open-access"
                                         xlink:href="%s"
                                         xml:lang="en">
                                  <license-p>
                                    This is an open-access article distributed under the terms...
                                  </license-p>
                                </license>
                              </permissions>
                            </article-meta>
                          </front>
                        </article>
                     """ % license
            sample = io.BytesIO(sample.encode('utf-8'))

            self.assertTrue(self._run_validation(sample))

    def test_disallowed_license_href(self):
        sample = u"""<article xmlns:xlink="http://www.w3.org/1999/xlink">
                      <front>
                        <article-meta>
                          <permissions>
                            <license license-type="open-access"
                                     xlink:href="http://opensource.org/licenses/MIT"
                                     xml:lang="en">
                              <license-p>
                                This is an open-access article distributed under the terms...
                              </license-p>
                            </license>
                          </permissions>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_missing_trailing_slash(self):
        allowed_licenses = [
            'https://creativecommons.org/licenses/by-nc/4.0',
        ]

        for license in allowed_licenses:
            sample = u"""<article xmlns:xlink="http://www.w3.org/1999/xlink">
                          <front>
                            <article-meta>
                              <permissions>
                                <license license-type="open-access"
                                         xlink:href="%s"
                                         xml:lang="en">
                                  <license-p>
                                    This is an open-access article distributed under the terms...
                                  </license-p>
                                </license>
                              </permissions>
                            </article-meta>
                          </front>
                        </article>
                     """ % license
            sample = io.BytesIO(sample.encode('utf-8'))

            self.assertTrue(self._run_validation(sample))

    def test_permissions_within_elements_of_the_body(self):
        sample = u"""<article xmlns:xlink="http://www.w3.org/1999/xlink">
                      <front>
                        <article-meta>
                          <permissions>
                            <license license-type="open-access"
                                     xlink:href="http://creativecommons.org/licenses/by/4.0/"
                                     xml:lang="en">
                              <license-p>
                                This is an open-access article distributed under the terms...
                              </license-p>
                            </license>
                          </permissions>
                        </article-meta>
                      </front>
                      <body>
                        <sec>
                          <p>
                            <fig id="f01">
                              <label>Fig. 1</label>
                              <caption>
                                <title>título da imagem</title>
                              </caption>
                              <graphic xlink:href="1234-5678-rctb-45-05-0110-gf01.tif"/>
                              <permissions>
                                <copyright-statement>Copyright © 2014 SciELO</copyright-statement>
                                <copyright-year>2014</copyright-year>
                                <copyright-holder>SciELO</copyright-holder>
                                <license license-type="open-access"
                                         xlink:href="http://creativecommons.org/licenses/by-nc-sa/4.0/"
                                         xml:lang="en">
                                  <license-p>This work is licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.</license-p>
                                </license>
                              </permissions>
                            </fig>
                          </p>
                        </sec>
                      </body>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))

    def test_copyrighted_elements_within_the_body(self):
        sample = u"""<article xmlns:xlink="http://www.w3.org/1999/xlink">
                      <front>
                        <article-meta>
                          <permissions>
                            <license license-type="open-access"
                                     xlink:href="http://creativecommons.org/licenses/by/4.0/"
                                     xml:lang="en">
                              <license-p>
                                This is an open-access article distributed under the terms...
                              </license-p>
                            </license>
                          </permissions>
                        </article-meta>
                      </front>
                      <body>
                        <sec>
                          <p>
                            <fig id="f01">
                              <label>Fig. 1</label>
                              <caption>
                                <title>título da imagem</title>
                              </caption>
                              <graphic xlink:href="1234-5678-rctb-45-05-0110-gf01.tif"/>
                              <permissions>
                                <copyright-statement>Copyright © 2014 SciELO</copyright-statement>
                                <copyright-year>2014</copyright-year>
                                <copyright-holder>SciELO</copyright-holder>
                              </permissions>
                            </fig>
                          </p>
                        </sec>
                      </body>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))

    def test_irrestrict_use_licenses_within_elements_in_the_body(self):
        sample = u"""<article xmlns:xlink="http://www.w3.org/1999/xlink">
                      <front>
                        <article-meta>
                          <permissions>
                            <license license-type="open-access"
                                     xlink:href="http://creativecommons.org/licenses/by/4.0/"
                                     xml:lang="en">
                              <license-p>
                                This is an open-access article distributed under the terms...
                              </license-p>
                            </license>
                          </permissions>
                        </article-meta>
                      </front>
                      <body>
                        <sec>
                          <p>
                            <fig id="f01">
                              <label>Fig. 1</label>
                              <caption>
                                <title>título da imagem</title>
                              </caption>
                              <graphic xlink:href="1234-5678-rctb-45-05-0110-gf01.tif"/>
                              <permissions>
                                <copyright-statement>Copyright © 2014 SciELO</copyright-statement>
                                <copyright-year>2014</copyright-year>
                                <copyright-holder>SciELO</copyright-holder>
                                <license license-type="open-access"
                                         xlink:href="http://creativecommons.org/licenses/by/2.0/"
                                         xml:lang="en">
                                  <license-p>This is an open-access article distributed under the terms of...</license-p>
                                </license>
                              </permissions>
                            </fig>
                          </p>
                        </sec>
                      </body>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))

    def test_main_article_copyright_info(self):
        sample = u"""<article xmlns:xlink="http://www.w3.org/1999/xlink">
                      <front>
                        <article-meta>
                          <permissions>
                            <copyright-statement>Copyright © 2014 SciELO</copyright-statement>
                            <copyright-year>2014</copyright-year>
                            <copyright-holder>SciELO</copyright-holder>
                            <license license-type="open-access"
                                     xlink:href="http://creativecommons.org/licenses/by/4.0/"
                                     xml:lang="en">
                              <license-p>
                                This is an open-access article distributed under the terms...
                              </license-p>
                            </license>
                          </permissions>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))

    def test_lang_mismatch(self):
        sample = u"""<article xmlns:xlink="http://www.w3.org/1999/xlink" xml:lang="en">
                      <front>
                        <article-meta>
                          <permissions>
                            <license license-type="open-access"
                                     xlink:href="http://creativecommons.org/licenses/by/4.0/"
                                     xml:lang="pt">
                              <license-p>
                                Texto em pt-br...
                              </license-p>
                            </license>
                          </permissions>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_lang_mismatch_is_ignored_if_lang_is_en(self):
        sample = u"""<article xmlns:xlink="http://www.w3.org/1999/xlink" xml:lang="pt">
                      <front>
                        <article-meta>
                          <permissions>
                            <license license-type="open-access"
                                     xlink:href="http://creativecommons.org/licenses/by/4.0/"
                                     xml:lang="en">
                              <license-p>
                                This is an open-access article distributed under the terms...
                              </license-p>
                            </license>
                          </permissions>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))

    def test_missing_lang_attribute(self):
        sample = u"""<article xmlns:xlink="http://www.w3.org/1999/xlink" xml:lang="pt">
                      <front>
                        <article-meta>
                          <permissions>
                            <license license-type="open-access"
                                     xlink:href="http://creativecommons.org/licenses/by/4.0/">
                              <license-p>
                                This is an open-access article distributed under the terms...
                              </license-p>
                            </license>
                          </permissions>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))


class AckTests(PhaseBasedTestCase):
    """Tests for article/back/ack element.
    """
    sch_phase = 'phase.ack'

    def test_with_sec(self):
        sample = u"""<article>
                      <back>
                        <ack>
                          <sec>
                            <p>Some</p>
                          </sec>
                        </ack>
                      </back>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_without_sec(self):
        sample = u"""<article>
                      <back>
                        <ack>
                          <title>Acknowledgment</title>
                          <p>Some text</p>
                        </ack>
                      </back>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))


class ElementCitationTests(PhaseBasedTestCase):
    """Tests for article/back/ref-list/ref/element-citation element.
    """
    sch_phase = 'phase.element-citation'

    def test_with_name_outside_persongroup(self):
        sample = u"""<article>
                      <back>
                        <ref-list>
                          <ref>
                            <element-citation publication-type="journal">
                              <name>Foo</name>
                            </element-citation>
                          </ref>
                        </ref-list>
                      </back>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_with_name_inside_persongroup(self):
        sample = u"""<article>
                      <back>
                        <ref-list>
                          <ref>
                            <element-citation publication-type="journal">
                              <person-group>
                                <name>Foo</name>
                              </person-group>
                            </element-citation>
                          </ref>
                        </ref-list>
                      </back>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))

    def test_with_etal_outside_persongroup(self):
        sample = u"""<article>
                      <back>
                        <ref-list>
                          <ref>
                            <element-citation publication-type="journal">
                              <etal>Foo</etal>
                            </element-citation>
                          </ref>
                        </ref-list>
                      </back>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_with_etal_inside_persongroup(self):
        sample = u"""<article>
                      <back>
                        <ref-list>
                          <ref>
                            <element-citation publication-type="journal">
                              <person-group>
                                <etal>Foo</etal>
                              </person-group>
                            </element-citation>
                          </ref>
                        </ref-list>
                      </back>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))

    def test_with_collab_outside_persongroup(self):
        sample = u"""<article>
                      <back>
                        <ref-list>
                          <ref>
                            <element-citation publication-type="journal">
                              <collab>Foo</collab>
                            </element-citation>
                          </ref>
                        </ref-list>
                      </back>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_with_collab_inside_persongroup(self):
        sample = u"""<article>
                      <back>
                        <ref-list>
                          <ref>
                            <element-citation publication-type="journal">
                              <person-group>
                                <collab>Foo</collab>
                              </person-group>
                            </element-citation>
                          </ref>
                        </ref-list>
                      </back>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))

    def test_allowed_publication_types(self):
        for pub_type in ['journal', 'book', 'webpage', 'thesis', 'confproc',
                         'patent', 'software', 'database', 'legal-doc', 'newspaper',
                         'other', 'report']:
            sample = u"""<article>
                          <back>
                            <ref-list>
                              <ref>
                                <element-citation publication-type="%s">
                                </element-citation>
                              </ref>
                            </ref-list>
                          </back>
                        </article>
                     """ % pub_type
            sample = io.BytesIO(sample.encode('utf-8'))

            self.assertTrue(self._run_validation(sample))

    def test_disallowed_publication_types(self):
        sample = u"""<article>
                      <back>
                        <ref-list>
                          <ref>
                            <element-citation publication-type="invalid">
                            </element-citation>
                          </ref>
                        </ref-list>
                      </back>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_outside_ref(self):
        sample = u"""<article>
                      <body>
                        <sec>
                          <p>
                            <element-citation publication-type="journal">
                              <person-group>
                                <collab>Foo</collab>
                              </person-group>
                            </element-citation>
                          </p>
                        </sec>
                      </body>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))


class PersonGroupTests(PhaseBasedTestCase):
    """Tests for
      - article/back/ref-list/ref/element-citation/person-group
      - article/front/article-meta/product/person-group
    """
    sch_phase = 'phase.person-group'

    def test_missing_type(self):
        sample = u"""<article>
                      <back>
                        <ref-list>
                          <ref>
                            <element-citation>
                              <person-group>
                                <name>Foo</name>
                              </person-group>
                            </element-citation>
                          </ref>
                        </ref-list>
                      </back>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_missing_type_at_product(self):
        sample = u"""<article>
                      <front>
                        <article-meta>
                          <product>
                            <person-group>
                              <name>Foo</name>
                            </person-group>
                          </product>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_with_type(self):
        sample = u"""<article>
                      <back>
                        <ref-list>
                          <ref>
                            <element-citation>
                              <person-group person-group-type="author">
                                <name>Foo</name>
                              </person-group>
                            </element-citation>
                          </ref>
                        </ref-list>
                      </back>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))

    def test_allowed_types(self):
        for group_type in ['author', 'compiler', 'editor', 'translator']:
            sample = u"""<article>
                          <back>
                            <ref-list>
                              <ref>
                                <element-citation>
                                  <person-group person-group-type="%s">
                                    <name>Foo</name>
                                  </person-group>
                                </element-citation>
                              </ref>
                            </ref-list>
                          </back>
                        </article>
                     """ % group_type
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))

    def test_disallowed_type(self):
        sample = u"""<article>
                      <back>
                        <ref-list>
                          <ref>
                            <element-citation>
                              <person-group person-group-type="invalid">
                                <name>Foo</name>
                              </person-group>
                            </element-citation>
                          </ref>
                        </ref-list>
                      </back>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_loose_text_below_element_citation_node(self):
        sample = u"""<article>
                      <back>
                        <ref-list>
                          <ref>
                            <element-citation publication-type="journal">
                              <person-group person-group-type="author">HERE
                                <collab>Foo</collab>
                              </person-group>
                            </element-citation>
                          </ref>
                        </ref-list>
                      </back>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_loose_text_below_product_node(self):
        sample = u"""<article>
                      <front>
                        <article-meta>
                          <product>
                            <person-group person-group-type="author">HERE
                              <collab>Foo</collab>
                            </person-group>
                          </product>
                        </article-meta>
                      </front>
                      <back>
                        <ref-list>
                          <ref>
                            <element-citation publication-type="journal">
                              <person-group person-group-type="author">
                                <collab>Foo</collab>
                              </person-group>
                            </element-citation>
                          </ref>
                        </ref-list>
                      </back>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))


class FNGroupTests(PhaseBasedTestCase):
    """Tests for article/back/fn-group/fn element.
    """
    sch_phase = 'phase.fn-group'

    def test_allowed_fn_types(self):
        for fn_type in ['abbr', 'com', 'financial-disclosure', 'supported-by',
                'presented-at', 'supplementary-material', 'other']:

            sample = u"""<article>
                          <back>
                            <fn-group>
                              <fn fn-type="%s">
                                <p>foobar</p>
                              </fn>
                            </fn-group>
                          </back>
                        </article>
                     """ % fn_type
            sample = io.BytesIO(sample.encode('utf-8'))

            self.assertTrue(self._run_validation(sample))

    def test_disallowed_fn_types(self):
        sample = u"""<article>
                      <back>
                        <fn-group>
                          <fn fn-type="invalid">
                            <p>foobar</p>
                          </fn>
                        </fn-group>
                      </back>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_group_title(self):
        sample = u"""<article>
                      <back>
                        <fn-group>
                          <title>Notes</title>
                          <fn fn-type="other">
                            <p>foobar</p>
                          </fn>
                        </fn-group>
                      </back>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))

    def test_many_group_titles_are_not_allowed(self):
        sample = u"""<article>
                      <back>
                        <fn-group>
                          <title>Notes</title>
                          <title>Notes again</title>
                          <fn fn-type="other">
                            <p>foobar</p>
                          </fn>
                        </fn-group>
                      </back>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))


class XHTMLTableTests(PhaseBasedTestCase):
    """Tests for //table elements.
    """
    sch_phase = 'phase.xhtml-table'

    def test_valid_toplevel(self):
        for elem in ['caption', 'summary', 'col', 'colgroup', 'thead', 'tfoot', 'tbody']:

            sample = u"""<article>
                          <body>
                            <sec>
                              <p>
                                <table>
                                  <%s></%s>
                                </table>
                              </p>
                            </sec>
                          </body>
                        </article>
                     """ % (elem, elem)
            sample = io.BytesIO(sample.encode('utf-8'))

            self.assertTrue(self._run_validation(sample))

    def test_invalid_toplevel(self):
        for elem in ['tr']:

            sample = u"""<article>
                          <body>
                            <sec>
                              <p>
                                <table>
                                  <%s></%s>
                                </table>
                              </p>
                            </sec>
                          </body>
                        </article>
                     """ % (elem, elem)
            sample = io.BytesIO(sample.encode('utf-8'))

            self.assertFalse(self._run_validation(sample))

    def test_tbody_upon_th(self):
        sample = u"""<article>
                      <body>
                        <sec>
                          <p>
                            <table>
                              <tbody>
                                <tr>
                                  <th>Foo</th>
                                </tr>
                              </tbody>
                            </table>
                          </p>
                        </sec>
                      </body>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_thead_upon_th(self):
        sample = u"""<article>
                      <body>
                        <sec>
                          <p>
                            <table>
                              <thead>
                                <tr>
                                  <th>Foo</th>
                                </tr>
                              </thead>
                            </table>
                          </p>
                        </sec>
                      </body>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))

    def test_thead_upon_td(self):
        sample = u"""<article>
                      <body>
                        <sec>
                          <p>
                            <table>
                              <thead>
                                <tr>
                                  <td>Foo</td>
                                </tr>
                              </thead>
                            </table>
                          </p>
                        </sec>
                      </body>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))


class SupplementaryMaterialMimetypeTests(PhaseBasedTestCase):
    """Tests for article//supplementary-material elements.
    """
    sch_phase = 'phase.supplementary-material'

    def test_case1(self):
        """mimetype is True
           mime-subtype is True
           mimetype ^ mime-subtype is True
        """
        sample = u"""<article xmlns:xlink="http://www.w3.org/1999/xlink">
                      <body>
                        <supplementary-material id="S1"
                                                xlink:title="local_file"
                                                xlink:href="1471-2105-1-1-s1.pdf"
                                                mimetype="application"
                                                mime-subtype="pdf">
                          <label>Additional material</label>
                          <caption>
                            <p>Supplementary PDF file supplied by authors.</p>
                          </caption>
                        </supplementary-material>
                      </body>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))

    def test_case2(self):
        """mimetype is True
           mime-subtype is False
           mimetype ^ mime-subtype is False
        """
        sample = u"""<article xmlns:xlink="http://www.w3.org/1999/xlink">
                      <body>
                        <supplementary-material id="S1"
                                                xlink:title="local_file"
                                                xlink:href="1471-2105-1-1-s1.pdf"
                                                mimetype="application">
                          <label>Additional material</label>
                          <caption>
                            <p>Supplementary PDF file supplied by authors.</p>
                          </caption>
                        </supplementary-material>
                      </body>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_case3(self):
        """mimetype is False
           mime-subtype is True
           mimetype ^ mime-subtype is False
        """
        sample = u"""<article xmlns:xlink="http://www.w3.org/1999/xlink">
                      <body>
                        <supplementary-material id="S1"
                                                xlink:title="local_file"
                                                xlink:href="1471-2105-1-1-s1.pdf"
                                                mime-subtype="pdf">
                          <label>Additional material</label>
                          <caption>
                            <p>Supplementary PDF file supplied by authors.</p>
                          </caption>
                        </supplementary-material>
                      </body>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_case4(self):
        """mimetype is False
           mime-subtype is False
           mimetype ^ mime-subtype is False
        """
        sample = u"""<article xmlns:xlink="http://www.w3.org/1999/xlink">
                      <body>
                        <supplementary-material id="S1"
                                                xlink:title="local_file"
                                                xlink:href="1471-2105-1-1-s1.pdf">
                          <label>Additional material</label>
                          <caption>
                            <p>Supplementary PDF file supplied by authors.</p>
                          </caption>
                        </supplementary-material>
                      </body>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))


class AuthorNotesFNTests(PhaseBasedTestCase):
    """Tests for article/front/article-meta/author-notes/fn element.
    """
    sch_phase = 'phase.fn-group'

    def test_allowed_fn_types(self):
        for fn_type in ['author', 'con', 'conflict', 'corresp', 'current-aff',
                        'deceased', 'edited-by', 'equal', 'on-leave',
                        'participating-researchers', 'present-address',
                        'previously-at', 'study-group-members', 'other',
                        'presented-at', 'presented-by']:

            sample = u"""<article>
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
            sample = io.BytesIO(sample.encode('utf-8'))

            self.assertTrue(self._run_validation(sample))

    def test_disallowed_fn_types(self):
        sample = u"""<article>
                      <front>
                        <article-meta>
                          <author-notes>
                            <fn fn-type="invalid">
                              <p>foobar</p>
                            </fn>
                          </author-notes>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))


class ArticleAttributesTests(PhaseBasedTestCase):
    """Tests for article element.
    """
    sch_phase = 'phase.article-attrs'

    def test_allowed_article_types(self):
        for art_type in ['other', 'article-commentary', 'case-report',
                'editorial', 'correction', 'letter', 'research-article',
                'in-brief', 'review-article', 'book-review', 'retraction',
                'brief-report', 'rapid-communication', 'reply', 'translation']:

            sample = u"""<article article-type="%s" xml:lang="en" dtd-version="1.0" specific-use="sps-1.4">
                        </article>
                     """ % art_type
            sample = io.BytesIO(sample.encode('utf-8'))

            self.assertTrue(self._run_validation(sample))

    def test_disallowed_article_type(self):
        sample = u"""<article article-type="invalid" dtd-version="1.0" specific-use="sps-1.4">
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_missing_article_type(self):
        sample = u"""<article xml:lang="en" dtd-version="1.0" specific-use="sps-1.4">
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_missing_xmllang(self):
        sample = u"""<article article-type="research-article" dtd-version="1.0" specific-use="sps-1.4">
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_missing_dtdversion(self):
        sample = u"""<article article-type="research-article" xml:lang="en" specific-use="sps-1.4">
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_missing_sps_version(self):
        sample = u"""<article article-type="research-article" dtd-version="1.0" xml:lang="en">
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_invalid_sps_version(self):
        sample = u"""<article article-type="research-article" dtd-version="1.0" xml:lang="en" specific-use="sps-1.0">
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))


class NamedContentTests(PhaseBasedTestCase):
    """Tests for article/front/article-meta/aff/addr-line/named-content elements.
    """
    sch_phase = 'phase.named-content_attrs'

    def test_missing_contenttype(self):
        sample = u"""<article>
                      <front>
                        <article-meta>
                          <aff>
                            <addr-line>
                              <named-content>Foo</named-content>
                            </addr-line>
                          </aff>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_allowed_contenttype(self):
        for ctype in ['city', 'state']:
            sample = u"""<article>
                          <front>
                            <article-meta>
                              <aff>
                                <addr-line>
                                  <named-content content-type="%s">Foo</named-content>
                                </addr-line>
                              </aff>
                            </article-meta>
                          </front>
                        </article>
                     """ % ctype
            sample = io.BytesIO(sample.encode('utf-8'))

            self.assertTrue(self._run_validation(sample))

    def test_disallowed_contenttype(self):
        sample = u"""<article>
                      <front>
                        <article-meta>
                          <aff>
                            <addr-line>
                              <named-content content-type="invalid">Foo</named-content>
                            </addr-line>
                          </aff>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))


class MonthTests(PhaseBasedTestCase):
    """Tests for //month elements.
    """
    sch_phase = 'phase.month'

    def test_range_1_12(self):
        for month in range(1, 13):
            sample = u"""<article>
                          <front>
                            <article-meta>
                              <pub-date>
                                <month>%s</month>
                              </pub-date>
                            </article-meta>
                          </front>
                        </article>
                     """ % month
            sample = io.BytesIO(sample.encode('utf-8'))

            self.assertTrue(self._run_validation(sample))

    def test_range_01_12(self):
        for month in range(1, 13):
            sample = u"""<article>
                          <front>
                            <article-meta>
                              <pub-date>
                                <month>%02d</month>
                              </pub-date>
                            </article-meta>
                          </front>
                        </article>
                     """ % month
            sample = io.BytesIO(sample.encode('utf-8'))

            self.assertTrue(self._run_validation(sample))

    def test_out_of_range(self):
        for month in [0, 13]:
            sample = u"""<article>
                          <front>
                            <article-meta>
                              <pub-date>
                                <month>%s</month>
                              </pub-date>
                            </article-meta>
                          </front>
                        </article>
                     """ % month
            sample = io.BytesIO(sample.encode('utf-8'))

            self.assertFalse(self._run_validation(sample))

    def test_must_be_integer(self):
        sample = u"""<article>
                      <front>
                        <article-meta>
                          <pub-date>
                            <month>January</month>
                          </pub-date>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))


class SizeTests(PhaseBasedTestCase):
    """Tests for:
      - article/front/article-meta/product/size
      - article/back/ref-list/ref/element-citation/size
    """
    sch_phase = 'phase.size'

    def test_in_element_citation(self):
        sample = u"""<article>
                      <back>
                        <ref-list>
                          <ref>
                            <element-citation>
                              <size units="pages">2</size>
                            </element-citation>
                          </ref>
                        </ref-list>
                      </back>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))

    def test_in_product(self):
        sample = u"""<article>
                      <front>
                        <article-meta>
                          <product>
                            <size units="pages">2</size>
                          </product>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))

    def test_missing_units_in_product(self):
        sample = u"""<article>
                      <front>
                        <article-meta>
                          <product>
                            <size>2</size>
                          </product>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_missing_units_in_element_citation(self):
        sample = u"""<article>
                      <back>
                        <ref-list>
                          <ref>
                            <element-citation>
                              <size>2</size>
                            </element-citation>
                          </ref>
                        </ref-list>
                      </back>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_invalid_units_value(self):
        sample = u"""<article>
                      <front>
                        <article-meta>
                          <product>
                            <size units="invalid">2</size>
                          </product>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))


class ListTests(PhaseBasedTestCase):
    """Tests for list elements.
    """
    sch_phase = 'phase.list'

    def test_allowed_list_type(self):
        for list_type in ['order', 'bullet', 'alpha-lower', 'alpha-upper',
                          'roman-lower', 'roman-upper', 'simple']:
            sample = u"""<article>
                          <body>
                            <sec>
                              <p>
                                <list list-type="%s">
                                  <title>Lista Númerica</title>
                                  <list-item>
                                    <p>Nullam gravida tellus eget condimentum egestas.</p>
                                  </list-item>
                                  <list-item>
                                    <list list-type="%s">
                                      <list-item>
                                        <p>Curabitur luctus lorem ac feugiat pretium.</p>
                                      </list-item>
                                    </list>
                                  </list-item>
                                  <list-item>
                                    <p>Donec pulvinar odio ut enim lobortis, eu dignissim elit accumsan.</p>
                                  </list-item>
                                </list>
                              </p>
                            </sec>
                          </body>
                        </article>
                     """ % (list_type, list_type)
            sample = io.BytesIO(sample.encode('utf-8'))

            self.assertTrue(self._run_validation(sample))

    def test_disallowed_list_type(self):
        sample = u"""<article>
                      <body>
                        <sec>
                          <p>
                            <list list-type="invalid">
                              <title>Lista Númerica</title>
                              <list-item>
                                <p>Nullam gravida tellus eget condimentum egestas.</p>
                              </list-item>
                              <list-item>
                                <list list-type="invalid">
                                  <list-item>
                                    <p>Curabitur luctus lorem ac feugiat pretium.</p>
                                  </list-item>
                                </list>
                              </list-item>
                              <list-item>
                                <p>Donec pulvinar odio ut enim lobortis, eu dignissim elit accumsan.</p>
                              </list-item>
                            </list>
                          </p>
                        </sec>
                      </body>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_disallowed_sub_list_type(self):
        sample = u"""<article>
                      <body>
                        <sec>
                          <p>
                            <list list-type="order">
                              <title>Lista Númerica</title>
                              <list-item>
                                <p>Nullam gravida tellus eget condimentum egestas.</p>
                              </list-item>
                              <list-item>
                                <list list-type="invalid">
                                  <list-item>
                                    <p>Curabitur luctus lorem ac feugiat pretium.</p>
                                  </list-item>
                                </list>
                              </list-item>
                              <list-item>
                                <p>Donec pulvinar odio ut enim lobortis, eu dignissim elit accumsan.</p>
                              </list-item>
                            </list>
                          </p>
                        </sec>
                      </body>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_missing_list_type(self):
        sample = u"""<article>
                      <body>
                        <sec>
                          <p>
                            <list>
                              <title>Lista Númerica</title>
                              <list-item>
                                <p>Nullam gravida tellus eget condimentum egestas.</p>
                              </list-item>
                              <list-item>
                                <list>
                                  <list-item>
                                    <p>Curabitur luctus lorem ac feugiat pretium.</p>
                                  </list-item>
                                </list>
                              </list-item>
                              <list-item>
                                <p>Donec pulvinar odio ut enim lobortis, eu dignissim elit accumsan.</p>
                              </list-item>
                            </list>
                          </p>
                        </sec>
                      </body>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_missing_sub_list_type(self):
        sample = u"""<article>
                      <body>
                        <sec>
                          <p>
                            <list list-type="order">
                              <title>Lista Númerica</title>
                              <list-item>
                                <p>Nullam gravida tellus eget condimentum egestas.</p>
                              </list-item>
                              <list-item>
                                <list>
                                  <list-item>
                                    <p>Curabitur luctus lorem ac feugiat pretium.</p>
                                  </list-item>
                                </list>
                              </list-item>
                              <list-item>
                                <p>Donec pulvinar odio ut enim lobortis, eu dignissim elit accumsan.</p>
                              </list-item>
                            </list>
                          </p>
                        </sec>
                      </body>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))


class MediaTests(PhaseBasedTestCase):
    """Tests for article/body//p/media elements.
    """
    sch_phase = 'phase.media_attributes'

    def test_missing_mimetype(self):
        sample = u"""<article xmlns:xlink="http://www.w3.org/1999/xlink">
                      <body>
                        <p><media mime-subtype="mp4" xlink:href="1234-5678-rctb-45-05-0110-m01.mp4"/></p>
                      </body>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_missing_mime_subtype(self):
        sample = u"""<article xmlns:xlink="http://www.w3.org/1999/xlink">
                      <body>
                        <p><media mimetype="video" xlink:href="1234-5678-rctb-45-05-0110-m01.mp4"/></p>
                      </body>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_missing_href(self):
        sample = u"""<article xmlns:xlink="http://www.w3.org/1999/xlink">
                      <body>
                        <p><media mimetype="video" mime-subtype="mp4"/></p>
                      </body>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_all_present(self):
        sample = u"""<article xmlns:xlink="http://www.w3.org/1999/xlink">
                      <body>
                        <p><media mimetype="video" mime-subtype="mp4" xlink:href="1234-5678-rctb-45-05-0110-m01.mp4"/></p>
                      </body>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))


class ExtLinkTests(PhaseBasedTestCase):
    """Tests for ext-link elements.
    """
    sch_phase = 'phase.ext-link'

    def test_complete(self):
        sample = u"""<article xmlns:xlink="http://www.w3.org/1999/xlink">
                      <body>
                        <sec>
                          <p>Neque porro quisquam est <ext-link ext-link-type="uri" xlink:href="http://www.scielo.org">www.scielo.org</ext-link> qui dolorem ipsum quia</p>
                        </sec>
                      </body>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))

    def test_allowed_extlinktype(self):
        for link_type in ['uri', 'clinical-trial' ]:
            sample = u"""<article xmlns:xlink="http://www.w3.org/1999/xlink">
                          <body>
                            <sec>
                              <p>Neque porro quisquam est <ext-link ext-link-type="%s" xlink:href="http://www.scielo.org">www.scielo.org</ext-link> qui dolorem ipsum quia</p>
                            </sec>
                          </body>
                        </article>
                     """ % link_type
            sample = io.BytesIO(sample.encode('utf-8'))

            self.assertTrue(self._run_validation(sample))

    def test_disallowed_extlinktype(self):
        sample = u"""<article xmlns:xlink="http://www.w3.org/1999/xlink">
                      <body>
                        <sec>
                          <p>Neque porro quisquam est <ext-link ext-link-type="invalid" xlink:href="http://www.scielo.org">www.scielo.org</ext-link> qui dolorem ipsum quia</p>
                        </sec>
                      </body>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_missing_extlinktype(self):
        sample = u"""<article xmlns:xlink="http://www.w3.org/1999/xlink">
                      <body>
                        <sec>
                          <p>Neque porro quisquam est <ext-link xlink:href="http://www.scielo.org">www.scielo.org</ext-link> qui dolorem ipsum quia</p>
                        </sec>
                      </body>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_missing_xlinkhref(self):
        sample = u"""<article xmlns:xlink="http://www.w3.org/1999/xlink">
                      <body>
                        <sec>
                          <p>Neque porro quisquam est <ext-link ext-link-type="uri">www.scielo.org</ext-link> qui dolorem ipsum quia</p>
                        </sec>
                      </body>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_uri_without_scheme(self):
        sample = u"""<article xmlns:xlink="http://www.w3.org/1999/xlink">
                      <body>
                        <sec>
                          <p>Neque porro quisquam est <ext-link ext-link-type="uri" xlink:href="www.scielo.org">www.scielo.org</ext-link> qui dolorem ipsum quia</p>
                        </sec>
                      </body>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_file_scheme_is_not_allowed(self):
        sample = u"""<article xmlns:xlink="http://www.w3.org/1999/xlink">
                      <body>
                        <sec>
                          <p>Neque porro quisquam est <ext-link ext-link-type="uri" xlink:href="file:///etc/passwd">www.scielo.org</ext-link> qui dolorem ipsum quia</p>
                        </sec>
                      </body>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_commonly_used_uri_schemes(self):
        for uri in ['ftp://ftp.scielo.org', 'http://www.scielo.org', 'urn:foo:bar']:
            sample = u"""<article xmlns:xlink="http://www.w3.org/1999/xlink">
                          <body>
                            <sec>
                              <p>Neque porro quisquam est <ext-link ext-link-type="uri" xlink:href="{uri}">www.scielo.org</ext-link> qui dolorem ipsum quia</p>
                            </sec>
                          </body>
                        </article>
                     """.format(uri=uri)
            sample = io.BytesIO(sample.encode('utf-8'))

            self.assertTrue(self._run_validation(sample))


class SubArticleAttributesTests(PhaseBasedTestCase):
    """Tests for sub-article element.
    """
    sch_phase = 'phase.sub-article-attrs'

    def test_allowed_article_types(self):
        for art_type in ['abstract', 'letter', 'reply', 'translation']:
            sample = u"""<article article-type="research-article" xml:lang="en" dtd-version="1.0" specific-use="sps-1.4">
                           <sub-article article-type="%s" xml:lang="pt" id="sa1"></sub-article>
                         </article>
                     """ % art_type
            sample = io.BytesIO(sample.encode('utf-8'))

            self.assertTrue(self._run_validation(sample))

    def test_disallowed_article_type(self):
        sample = u"""<article article-type="research-article" dtd-version="1.0" specific-use="sps-1.4">
                       <sub-article article-type="invalid" xml:lang="pt" id="trans_pt"></sub-article>
                     </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_missing_article_type(self):
        sample = u"""<article article-type="research-article" dtd-version="1.0" specific-use="sps-1.4">
                       <sub-article xml:lang="pt" id="trans_pt"></sub-article>
                     </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_missing_xmllang(self):
        sample = u"""<article article-type="research-article" dtd-version="1.0" specific-use="sps-1.4">
                       <sub-article article-type="translation" id="trans_pt"></sub-article>
                     </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_missing_id(self):
        sample = u"""<article article-type="research-article" dtd-version="1.0" specific-use="sps-1.4">
                       <sub-article article-type="translation" xml:lang="pt"></sub-article>
                     </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))


class ResponseAttributesTests(PhaseBasedTestCase):
    """Tests for response element.
    """
    sch_phase = 'phase.response-attrs'

    def test_allowed_response_types(self):
        for type in ['addendum', 'discussion', 'reply']:
            sample = u"""<article>
                           <response response-type="%s" xml:lang="pt" id="r1"></response>
                         </article>
                     """ % type
            sample = io.BytesIO(sample.encode('utf-8'))

            self.assertTrue(self._run_validation(sample))

    def test_disallowed_response_type(self):
        sample = u"""<article>
                       <response response-type="invalid" xml:lang="pt" id="r1"></response>
                     </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_missing_response_type(self):
        sample = u"""<article>
                       <response xml:lang="pt" id="r1"></response>
                     </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_missing_xmllang(self):
        sample = u"""<article>
                       <response response-type="invalid" id="r1"></response>
                     </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_missing_id(self):
        sample = u"""<article>
                       <response response-type="invalid" xml:lang="pt"></response>
                     </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))


class ResponseReplyAttributeTests(PhaseBasedTestCase):
    """Tests for response[@response-type='reply'] elements.
    """
    sch_phase = 'phase.response-reply-type'

    def test_reply_type_demands_an_article_type(self):
        """ the article-type of value `article-commentary` is required
        """
        sample = u"""<article article-type="article-commentary">
                       <response response-type="reply" xml:lang="pt" id="r1">
                         <front-stub>
                           <related-article related-article-type="commentary-article" id="ra1" vol="109" page="87-92"/>
                         </front-stub>
                       </response>
                     </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))

    def test_reply_type_invalid_article_type(self):
        """ anything different of `article-commentary` is invalid
        """
        sample = u"""<article article-type="research-article">
                       <response response-type="reply" xml:lang="pt" id="r1">
                         <front-stub>
                           <related-article related-article-type="commentary-article" id="ra1" vol="109" page="87-92"/>
                         </front-stub>
                       </response>
                     </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_reply_type_missing_related_article(self):
        """ the article-type of value `article-commentary` is required
        """
        sample = u"""<article article-type="article-commentary">
                       <response response-type="reply" xml:lang="pt" id="r1">
                         <front-stub>
                         </front-stub>
                       </response>
                     </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_related_article_missing_vol(self):
        sample = u"""<article article-type="article-commentary">
                       <response response-type="reply" xml:lang="pt" id="r1">
                         <front-stub>
                           <related-article related-article-type="commentary-article" id="ra1" page="87-92"/>
                         </front-stub>
                       </response>
                     </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_related_article_missing_page(self):
        sample = u"""<article article-type="article-commentary">
                       <response response-type="reply" xml:lang="pt" id="r1">
                         <front-stub>
                           <related-article related-article-type="commentary-article" id="ra1" vol="109" elocation-id="1q2w"/>
                         </front-stub>
                       </response>
                     </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))

    def test_related_article_missing_elocationid(self):
        sample = u"""<article article-type="article-commentary">
                       <response response-type="reply" xml:lang="pt" id="r1">
                         <front-stub>
                           <related-article related-article-type="commentary-article" id="ra1" vol="109" page="87-92"/>
                         </front-stub>
                       </response>
                     </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))

    def test_related_article_missing_page_and_elocationid(self):
        sample = u"""<article article-type="article-commentary">
                       <response response-type="reply" xml:lang="pt" id="r1">
                         <front-stub>
                           <related-article related-article-type="commentary-article" id="ra1" vol="109"/>
                         </front-stub>
                       </response>
                     </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))


class RelatedArticleTypesTests(PhaseBasedTestCase):
    """Tests for related-article element.
    """
    sch_phase = 'phase.related-article-attrs'

    def test_allowed_related_article_types(self):
        for type in ['corrected-article', 'press-release', 'commentary-article', 'article-reference']:
            sample = u"""<article>
                           <front>
                             <article-meta>
                               <related-article related-article-type="%s" id="01"/>
                             </article-meta>
                           </front>
                         </article>
                     """ % type
            sample = io.BytesIO(sample.encode('utf-8'))

            self.assertTrue(self._run_validation(sample))

    def test_disallowed_related_article_type(self):
        sample = u"""<article>
                       <front>
                         <article-meta>
                           <related-article related-article-type="invalid" id="01"/>
                         </article-meta>
                       </front>
                     </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_missing_id(self):
        sample = u"""<article>
                       <front>
                         <article-meta>
                           <related-article related-article-type="corrected-article"/>
                         </article-meta>
                       </front>
                     </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_missing_related_article_type(self):
        sample = u"""<article>
                       <front>
                         <article-meta>
                           <related-article id="01"/>
                         </article-meta>
                       </front>
                     </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))


class CorrectionTests(PhaseBasedTestCase):
    """Tests for article[@article-type="correction"] element.
    """
    sch_phase = 'phase.correction'

    def test_expected_elements(self):
        sample = u"""<article article-type="correction">
                       <front>
                         <article-meta>
                           <related-article related-article-type="corrected-article" id="01"/>
                         </article-meta>
                       </front>
                     </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))

    def test_missing_related_article(self):
        """ must have a related-article[@related-article-type='corrected-article']
        element.
        """
        sample = u"""<article article-type="correction">
                       <front>
                         <article-meta>
                         </article-meta>
                       </front>
                     </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_article_type_must_be_correction(self):
        sample = u"""<article article-type="research-article">
                       <front>
                         <article-meta>
                           <related-article related-article-type="corrected-article" id="01"/>
                         </article-meta>
                       </front>
                     </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))


class InBriefTests(PhaseBasedTestCase):
    """Tests for article[@article-type="in-brief"] element.
    """
    sch_phase = 'phase.in-brief'

    def test_expected_elements(self):
        sample = u"""<article article-type="in-brief">
                       <front>
                         <article-meta>
                           <related-article related-article-type="article-reference" id="01"/>
                         </article-meta>
                       </front>
                     </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))

    def test_missing_related_article(self):
        """ must have a related-article[@related-article-type='in-brief']
        element.
        """
        sample = u"""<article article-type="in-brief">
                       <front>
                         <article-meta>
                         </article-meta>
                       </front>
                     </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_article_type_must_be_in_brief(self):
        sample = u"""<article article-type="research-article">
                       <front>
                         <article-meta>
                           <related-article related-article-type="article-reference" id="01"/>
                         </article-meta>
                       </front>
                     </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))


class FundingGroupTests(PhaseBasedTestCase):
    """Tests for article/front/article-meta/funding-group elements.
    """
    sch_phase = 'phase.funding-group'

    def test_funding_statement_when_fn_is_present_missing_award_group(self):
        sample = u"""<article>
                      <front>
                        <article-meta>
                          <funding-group>
                            <funding-statement>This study was supported by FAPEST #12345</funding-statement>
                          </funding-group>
                        </article-meta>
                      </front>
                      <back>
                        <fn-group>
                          <fn id="fn01" fn-type="financial-disclosure">
                            <p>This study was supported by FAPEST #12345</p>
                          </fn>
                        </fn-group>
                      </back>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_funding_statement_when_fn_is_present(self):
        sample = u"""<article>
                      <front>
                        <article-meta>
                          <funding-group>
                            <award-group>
                              <funding-source>FAPEST</funding-source>
                              <award-id>12345</award-id>
                            </award-group>
                            <funding-statement>This study was supported by FAPEST #12345</funding-statement>
                          </funding-group>
                        </article-meta>
                      </front>
                      <back>
                        <fn-group>
                          <fn id="fn01" fn-type="financial-disclosure">
                            <p>This study was supported by FAPEST #12345</p>
                          </fn>
                        </fn-group>
                      </back>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))

    def test_missing_funding_statement_when_fn_is_present(self):
        sample = u"""<article>
                      <front>
                        <article-meta>
                          <funding-group>
                            <award-group>
                              <funding-source>FAPEST</funding-source>
                              <award-id>12345</award-id>
                            </award-group>
                          </funding-group>
                        </article-meta>
                      </front>
                      <back>
                        <fn-group>
                          <fn id="fn01" fn-type="financial-disclosure">
                            <p>This study was supported by FAPEST #12345</p>
                          </fn>
                        </fn-group>
                      </back>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))


class AffCountryTests(PhaseBasedTestCase):
    """ //aff/country/@country is required.

    See: https://github.com/scieloorg/packtools/issues/44
    """
    sch_phase = 'phase.aff_country'

    def test_country_attribute_is_present(self):
        sample = u"""<article>
                      <front>
                        <article-meta>
                          <aff>
                            <institution content-type="original">
                              Grupo de ...
                            </institution>
                            <country country="BR">Brasil</country>
                          </aff>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))

    def test_country_attribute_is_absent(self):
        sample = u"""<article>
                      <front>
                        <article-meta>
                          <aff>
                            <institution content-type="original">
                              Grupo de ...
                            </institution>
                            <country>Brasil</country>
                          </aff>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_country_attribute_value_is_not_validated(self):
        sample = u"""<article>
                      <front>
                        <article-meta>
                          <aff>
                            <institution content-type="original">
                              Grupo de ...
                            </institution>
                            <country country="XZ">Brasil</country>
                          </aff>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))

    def test_country_cannot_be_empty(self):
        sample = u"""<article>
                      <front>
                        <article-meta>
                          <aff>
                            <institution content-type="original">
                              Grupo de ...
                            </institution>
                            <country country="XZ"></country>
                          </aff>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_country_cannot_be_empty_closed_element(self):
        sample = u"""<article>
                      <front>
                        <article-meta>
                          <aff>
                            <institution content-type="original">
                              Grupo de ...
                            </institution>
                            <country country="XZ"/>
                          </aff>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))


class RefTests(PhaseBasedTestCase):
    """Tests for article/back/ref-list/ref element.
    """
    sch_phase = 'phase.ref'

    def test_element_and_mixed_citation_elements(self):
        sample = u"""<article>
                      <back>
                        <ref-list>
                          <ref>
                            <mixed-citation>Aires M, Paz AA, Perosa CT. Situação de saúde e grau de dependência de pessoas idosas institucionalizadas. <italic>Rev Gaucha Enferm.</italic> 2009;30(3):192-9.</mixed-citation>
                            <element-citation publication-type="journal">
                              <person-group person-group-type="author">
                                <name>
                                  <surname>Aires</surname>
                                  <given-names>M</given-names>
                                </name>
                                <name>
                                  <surname>Paz</surname>
                                  <given-names>AA</given-names>
                                </name>
                                <name>
                                  <surname>Perosa</surname>
                                  <given-names>CT</given-names>
                                </name>
                              </person-group>
                              <article-title>Situação de saúde e grau de dependência de pessoas idosas institucionalizadas</article-title>
                              <source>Rev Gaucha Enferm</source>
                              <year>2009</year>
                              <volume>30</volume>
                              <issue>3</issue>
                              <fpage>192</fpage>
                              <lpage>199</lpage>
                            </element-citation>
                          </ref>
                        </ref-list>
                      </back>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))

    def test_missing_element_citation(self):
        sample = u"""<article>
                      <back>
                        <ref-list>
                          <ref>
                            <mixed-citation>Aires M, Paz AA, Perosa CT. Situação de saúde e grau de dependência de pessoas idosas institucionalizadas. <italic>Rev Gaucha Enferm.</italic> 2009;30(3):192-9.</mixed-citation>
                          </ref>
                        </ref-list>
                      </back>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_missing_mixed_citation(self):
        sample = u"""<article>
                      <back>
                        <ref-list>
                          <ref>
                            <element-citation publication-type="journal">
                              <person-group person-group-type="author">
                                <name>
                                  <surname>Aires</surname>
                                  <given-names>M</given-names>
                                </name>
                                <name>
                                  <surname>Paz</surname>
                                  <given-names>AA</given-names>
                                </name>
                                <name>
                                  <surname>Perosa</surname>
                                  <given-names>CT</given-names>
                                </name>
                              </person-group>
                              <article-title>Situação de saúde e grau de dependência de pessoas idosas institucionalizadas</article-title>
                              <source>Rev Gaucha Enferm</source>
                              <year>2009</year>
                              <volume>30</volume>
                              <issue>3</issue>
                              <fpage>192</fpage>
                              <lpage>199</lpage>
                            </element-citation>
                          </ref>
                        </ref-list>
                      </back>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_mixed_citation_cannot_be_empty(self):
        sample = u"""<article>
                      <back>
                        <ref-list>
                          <ref>
                            <mixed-citation></mixed-citation>
                            <element-citation publication-type="journal">
                              <person-group person-group-type="author">
                                <name>
                                  <surname>Aires</surname>
                                  <given-names>M</given-names>
                                </name>
                                <name>
                                  <surname>Paz</surname>
                                  <given-names>AA</given-names>
                                </name>
                                <name>
                                  <surname>Perosa</surname>
                                  <given-names>CT</given-names>
                                </name>
                              </person-group>
                              <article-title>Situação de saúde e grau de dependência de pessoas idosas institucionalizadas</article-title>
                              <source>Rev Gaucha Enferm</source>
                              <year>2009</year>
                              <volume>30</volume>
                              <issue>3</issue>
                              <fpage>192</fpage>
                              <lpage>199</lpage>
                            </element-citation>
                          </ref>
                        </ref-list>
                      </back>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))


class ContribIdTests(PhaseBasedTestCase):
    """Tests for contrib-id element.
    """
    sch_phase = 'phase.contrib-id'

    def test_allowed_contrib_id_type_attrs(self):
        for type in ['lattes', 'orcid', 'researchid', 'scopus']:
            sample = u"""<article>
                           <front>
                             <article-meta>
                               <contrib-group>
                                 <contrib-id contrib-id-type="%s">some id</contrib-id>
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
                     """ % type
            sample = io.BytesIO(sample.encode('utf-8'))

            self.assertTrue(self._run_validation(sample))

    def test_disallowed_related_article_type(self):
        sample = u"""<article>
                       <front>
                         <article-meta>
                           <contrib-group>
                             <contrib-id contrib-id-type="invalid">some id</contrib-id>
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
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_missing_contrib_id_type(self):
        sample = u"""<article>
                       <front>
                         <article-meta>
                           <contrib-group>
                             <contrib-id>some id</contrib-id>
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
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))


class AffTests(PhaseBasedTestCase):
    """ /article//aff is required.
    """
    sch_phase = 'phase.aff'

    def test_country_is_present(self):
        sample = u"""<article>
                      <front>
                        <article-meta>
                          <aff>
                            <institution content-type="original">
                              Grupo de ...
                            </institution>
                            <country country="BR">Brasil</country>
                          </aff>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))

    def test_country_is_absent(self):
        sample = u"""<article>
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
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_country_is_absent_in_subarticle(self):
        for typ in ['abstract', 'letter', 'reply']:
            sample = u"""<article>
                          <front>
                            <article-meta>
                              <aff>
                                <institution content-type="original">
                                  Grupo de ...
                                </institution>
                                <country country="BR">Brasil</country>
                              </aff>
                            </article-meta>
                          </front>
                          <sub-article article-type="{type}"
                                       xml:lang="en"
                                       id="s1">
                            <front-stub>
                              <article-categories>
                                <subj-group subj-group-type="heading">
                                  <subject>Artigos Originais</subject>
                                </subj-group>
                              </article-categories>
                              <aff>
                                <institution content-type="original">
                                  Grupo de ...
                                </institution>
                              </aff>
                            </front-stub>
                          </sub-article>
                        </article>
                     """.format(type=typ)
            sample = io.BytesIO(sample.encode('utf-8'))

            self.assertFalse(self._run_validation(sample))

    def test_country_is_absent_in_subarticle_type_translation(self):
        sample = u"""<article>
                      <front>
                        <article-meta>
                          <aff>
                            <institution content-type="original">
                              Grupo de ...
                            </institution>
                            <country country="BR">Brasil</country>
                          </aff>
                        </article-meta>
                      </front>
                      <sub-article article-type="translation"
                                   xml:lang="en"
                                   id="s1">
                        <front-stub>
                          <article-categories>
                            <subj-group subj-group-type="heading">
                              <subject>Artigos Originais</subject>
                            </subj-group>
                          </article-categories>
                          <aff>
                            <institution content-type="original">
                              Grupo de ...
                            </institution>
                          </aff>
                        </front-stub>
                      </sub-article>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))

