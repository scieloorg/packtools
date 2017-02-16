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


class LicenseTests(PhaseBasedTestCase):
    """Tests for article/front/article-meta/permissions/license element.
    """
    sch_phase = 'phase.license'

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

