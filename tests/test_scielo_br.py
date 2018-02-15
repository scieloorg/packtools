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

