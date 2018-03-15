# coding: utf-8
from __future__ import unicode_literals
import unittest
import io

from lxml import isoschematron, etree

from packtools.catalogs import SCHEMAS


SCH = etree.parse(SCHEMAS['scielo-br'])


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


class ArticleIdTests(PhaseBasedTestCase):
    """Tests for article/front/article-meta/article-id elements.
    """
    sch_phase = 'phase.article-id'

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

        self.assertFalse(self._run_validation(sample))

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


class ArticleTypeValues(PhaseBasedTestCase):
    """Tests for article element.
    """
    sch_phase = 'phase.article-type-values'

    def test_allowed_article_types(self):
        for art_type in ['addendum', 'research-article', 'review-article',
                'letter', 'article-commentary', 'brief-report', 'rapid-communication',
                'oration', 'discussion', 'editorial', 'interview', 'correction',
                'guidelines', 'other', 'obituary', 'case-report', 'book-review',
                'reply', 'retraction', 'partial-retraction', 'clinical-trial']:

            sample = u"""<article article-type="%s" xml:lang="en" dtd-version="1.0" specific-use="sps-1.7">
                        </article>
                     """ % art_type
            sample = io.BytesIO(sample.encode('utf-8'))

            self.assertTrue(self._run_validation(sample))


class HistoryTests(PhaseBasedTestCase):
    """Tests for article/front/article-meta/history/date.
    """
    sch_phase = 'phase.history'

    def test_complete_history(self):
        sample = u"""<article>
                      <front>
                        <article-meta>
                          <history>
                            <date date-type="received">
                              <day>15</day>
                              <month>03</month>
                              <year>2013</year>
                            </date>
                          </history>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))

    def test_day_is_missing(self):
        sample = u"""<article>
                      <front>
                        <article-meta>
                          <history>
                            <date date-type="received">
                              <month>03</month>
                              <year>2013</year>
                            </date>
                          </history>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_month_is_missing(self):
        sample = u"""<article>
                      <front>
                        <article-meta>
                          <history>
                            <date date-type="received">
                              <day>15</day>
                              <year>2013</year>
                            </date>
                          </history>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_year_is_missing(self):
        sample = u"""<article>
                      <front>
                        <article-meta>
                          <history>
                            <date date-type="received">
                              <day>15</day>
                              <month>03</month>
                            </date>
                          </history>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))


class ContribGroupTests(PhaseBasedTestCase):
    sch_phase = 'phase.contrib-group'

    def test_contrib_group_is_present(self):
        sample = u"""<article article-type="research-article">
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

    def test_contrib_group_is_optional_for_corrections(self):
        sample = u"""<article article-type="correction">
                      <front>
                        <article-meta>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))

    def test_contrib_group_is_optional_for_retractions(self):
        sample = u"""<article article-type="retraction">
                      <front>
                        <article-meta>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))

    def test_affs_must_be_referenced_by_contributors(self):
        sample = u"""<article article-type="research-article">
                      <front>
                        <article-meta>
                          <contrib-group>
		            <contrib contrib-type="author">
                              <name>
                                <surname>Brait</surname>
                                <given-names>Beth</given-names>
                              </name>
                              <xref ref-type="aff" rid="aff1"/>
                            </contrib>
                            <aff id="aff1">
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

    def test_must_error_when_affs_unrelated_to_contributors(self):
        sample = u"""<article article-type="research-article">
                      <front>
                        <article-meta>
                          <contrib-group>
		            <contrib contrib-type="author">
                              <name>
                                <surname>Brait</surname>
                                <given-names>Beth</given-names>
                              </name>
                            </contrib>
                            <aff id="aff1">
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


class InstitutionTests(PhaseBasedTestCase):
    sch_phase = 'phase.institution'

    def test_institution_is_present(self):
        sample = u"""<article article-type="research-article">
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

    def test_institution_is_optional_for_corrections(self):
        sample = u"""<article article-type="correction">
                      <front>
                        <article-meta>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))

    def test_institution_is_optional_for_retractions(self):
        sample = u"""<article article-type="retraction">
                      <front>
                        <article-meta>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))


class CountryTests(PhaseBasedTestCase):
    sch_phase = 'phase.country'

    def test_country_in_aff(self):
        sample = u"""<article article-type="research-article">
                      <front>
                        <article-meta>
                          <contrib-group>
                            <aff>
                              <country country="BR">Brasil</country>
                            </aff>
                          </contrib-group>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))

    def test_missing_country_in_aff(self):
        sample = u"""<article article-type="research-article">
                      <front>
                        <article-meta>
                          <contrib-group>
                            <aff>
                            </aff>
                          </contrib-group>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_missing_country_in_aff_of_corrections(self):
        sample = u"""<article article-type="correction">
                      <front>
                        <article-meta>
                          <contrib-group>
                            <aff>
                            </aff>
                          </contrib-group>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))

    def test_missing_country_in_aff_of_retraction(self):
        sample = u"""<article article-type="correction">
                      <front>
                        <article-meta>
                          <contrib-group>
                            <aff>
                            </aff>
                          </contrib-group>
                        </article-meta>
                      </front>
                    </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertTrue(self._run_validation(sample))


class ReferencesTests(PhaseBasedTestCase):
    sch_phase = 'phase.references'

    def test_missing_back_raises_error(self):
        sample = u"""<article article-type="research-article">
                     </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_missing_reflist_raises_error(self):
        sample = u"""<article article-type="research-article">
                       <back>
                       </back>
                     </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

    def test_missing_ref_raises_error(self):
        sample = u"""<article article-type="research-article">
                       <back>
                         <ref-list>
                         </ref-list>
                       </back>
                     </article>
                 """
        sample = io.BytesIO(sample.encode('utf-8'))

        self.assertFalse(self._run_validation(sample))

