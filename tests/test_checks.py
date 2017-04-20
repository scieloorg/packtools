# coding: utf-8
from __future__ import unicode_literals
import os
import unittest
import io

from lxml import etree

from packtools import checks


SAMPLES_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    'samples')


class SetupTests(unittest.TestCase):
    def test_message_is_splitted(self):
        fp = etree.parse(io.BytesIO(b'<a><b>bar</b></a>'))
        self.assertEqual(checks.setup(fp), (fp, []))


class TeardownTests(unittest.TestCase):
    def test_returns_errorlist(self):
        fp = etree.parse(io.BytesIO(b'<a><b>bar</b></a>'))
        err_list = ['some error']
        message = (fp, err_list)
        self.assertEqual(checks.teardown(message), err_list)


# ----------------------------------
# Funding Group pipe and utils tests
# ----------------------------------
class FundingGroupPipeTests(unittest.TestCase):
    """See the spec on the pipe's docstring for more info.
    """
    def test_proposition_1_case_1(self):
        """
        HasExplicitContract is True
        HasFundingGroup is True
        (HasExplicitContract <=> HasFundingGroup) is True
        """
        sample = os.path.join(SAMPLES_PATH, '0034-8910-rsp-48-2-0206.xml')

        et = etree.parse(sample)
        _, err_list = checks.funding_group((et, []))

        self.assertEqual(len(err_list), 0)

    def test_proposition_1_case_2(self):
        """
        HasExplicitContract is True
        HasFundingGroup is False
        (HasExplicitContract <=> HasFundingGroup) is False
        """
        sample = io.BytesIO(b"""
        <article>
          <front>
            <article-meta></article-meta>
          </front>
          <back>
            <fn-group>
              <fn id="fn1" fn-type="financial-disclosure">
                <p>This study was supported by the Brazilian Ministry of Health/Secretariat of Health Surveillance/Department of STD, AIDS and Viral Hepatitis, through the Project of International Technical Cooperation AD/BRA/03/H34 between the Brazilian Government and the United Nations Office on Drugs and Crime (Process CSV 234/07).</p>
              </fn>
	    </fn-group>
	  </back>
        </article>
        """)

        et = etree.parse(sample)
        _, err_list = checks.funding_group((et, []))

        self.assertEqual(len(err_list), 1)
        self.assertTrue("'fn-group'" in err_list[0].message)

    def test_proposition_1_case_3(self):
        """
        HasExplicitContract is False
        HasFundingGroup is True
        (HasExplicitContract <=> HasFundingGroup) is False
        """
        sample = io.BytesIO(b"""
        <article>
          <front>
            <article-meta>
	      <funding-group>
	        <award-group>
		  <funding-source>Brazilian Ministry of Health/Secretariat of Health Surveillance/Department of STD, AIDS and Viral Hepatitis</funding-source>
		  <award-id>CSV 234/07</award-id>
		</award-group>
                <funding-statement>This study was supported by the Brazilian Ministry of Health/Secretariat of Health Surveillance/Department of STD, AIDS and Viral Hepatitis, through the Project of International Technical Cooperation AD/BRA/03/H34 between the Brazilian Government and the United Nations Office on Drugs and Crime (Process CSV 234/07).</funding-statement>
	      </funding-group>
            </article-meta>
          </front>
          <back>
            <fn-group>
              <fn id="fn1">
	        <p>This study was supported by the Brazilian Ministry of Health/Secretariat of Health Surveillance/Department of STD, AIDS and Viral Hepatitis, through the Project of International Technical Cooperation AD/BRA/03/H34 between the Brazilian Government and the United Nations Office on Drugs and Crime (Process CSV 234/07).</p>
	      </fn>
            </fn-group>
          </back>
        </article>
        """)

        et = etree.parse(sample)
        _, err_list = checks.funding_group((et, []))

        self.assertEqual(len(err_list), 1)
        self.assertTrue("'funding-group'" in err_list[0].message)

    def test_proposition_1_case_4(self):
        """
        HasExplicitContract is False
        HasFundingGroup is False
        (HasExplicitContract <=> HasFundingGroup) is True
        """
        sample = io.BytesIO(b"""
        <article>
          <front>
            <article-meta></article-meta>
          </front>
          <back>
            <fn-group>
              <fn id="fn1">
                <p>This study was supported by the Brazilian Ministry of Health/Secretariat of Health Surveillance/Department of STD, AIDS and Viral Hepatitis, through the Project of International Technical Cooperation AD/BRA/03/H34 between the Brazilian Government and the United Nations Office on Drugs and Crime (Process CSV 234/07).</p>
              </fn>
            </fn-group>
          </back>
        </article>
        """)

        et = etree.parse(sample)
        _, err_list = checks.funding_group((et, []))

        self.assertEqual(len(err_list), 0)

    def test_proposition_3_case_1(self):
        """
        ∃ContractNo<fn> [ ¬Registered(FundingGroup, ContractNo) ] ^
        ∀ContractNo<ack> [ Registered(FundingGroup, ContractNo) ] ^
        ∀ContractNo<funding-group> [ Registered(Ack, ContractNo) v Registered(Fn, ContractNo) ]
        """
        sample = io.BytesIO(b"""
        <article>
          <front>
            <article-meta>
	      <funding-group>
                <award-group>
                  <funding-source>Brazilian Ministry of Health/Secretariat of Health Surveillance/Department of STD, AIDS and Viral Hepatitis</funding-source>
		  <award-id>234/07</award-id>
                </award-group>
		<funding-statement>This study was supported by the Brazilian Ministry of Health/Secretariat of Health Surveillance/Department of STD, AIDS and Viral Hepatitis, through the Project of International Technical Cooperation AD/BRA/03/H34 between the Brazilian Government and the United Nations Office on Drugs and Crime (Process CSV 234/07).</funding-statement>
                </funding-group>
            </article-meta>
          </front>
          <back>
            <fn-group>
              <fn id="fn1" fn-type="financial-disclosure">
                <p>This study was supported by the Brazilian Ministry of Health/Secretariat of Health Surveillance/Department of STD, AIDS and Viral Hepatitis, through the Project of International Technical Cooperation AD/BRA/03/H34 between the Brazilian Government and the United Nations Office on Drugs and Crime (Process CSV 234/07).</p>
              </fn>
	      <fn id="fn2" fn-type="financial-disclosure">
                <p>Foo Bar Office on Drugs and Crime (Process CSV 235/07).</p>
              </fn>
            </fn-group>
          </back>
        </article>
        """)

        et = etree.parse(sample)
        _, err_list = checks.funding_group((et, []))

        self.assertEqual(len(err_list), 1)
        self.assertTrue("'fn-group'" in err_list[0].message)

    def test_proposition_3_case_2(self):
        """ This cannot be checked by packtools' stylechecker.

        ∀ContractNo<fn> [ Registered(FundingGroup, ContractNo) ] ^
        ∃ContractNo<ack> [ ¬Registered(FundingGroup, ContractNo) ] ^
        ∀ContractNo<funding-group> [ Registered(Ack, ContractNo) v Registered(Fn, ContractNo) ]
        """
        sample = io.BytesIO(b"""
        <article>
          <front>
            <article-meta>
              <funding-group>
                <award-group>
                  <funding-source>Brazilian Ministry of Health/Secretariat of Health Surveillance/Department of STD, AIDS and Viral Hepatitis</funding-source>
                  <award-id>234/07</award-id>
                </award-group>
                <funding-statement>This study was supported by the Brazilian Ministry of Health/Secretariat of Health Surveillance/Department of STD, AIDS and Viral Hepatitis, through the Project of International Technical Cooperation AD/BRA/03/H34 between the Brazilian Government and the United Nations Office on Drugs and Crime (Process CSV 234/07).</funding-statement>
              </funding-group>
            </article-meta>
          </front>
          <back>
            <fn-group>
              <fn id="fn1" fn-type="financial-disclosure">
                <p>This study was supported by the Brazilian Ministry of Health/Secretariat of Health Surveillance/Department of STD, AIDS and Viral Hepatitis, through the Project of International Technical Cooperation AD/BRA/03/H34 between the Brazilian Government and the United Nations Office on Drugs and Crime (Process CSV 234/07).</p>
              </fn>
            </fn-group>
            <ack>
              <p>... this study was supported by FooBar under the process 235/09.</p>
            </ack>
          </back>
        </article>
        """)

        et = etree.parse(sample)
        _, err_list = checks.funding_group((et, []))

        self.assertEqual(len(err_list), 0)  # the error could not be detected

    def test_proposition_3_case_3(self):
        """
        ∀ContractNo<fn> [ Registered(FundingGroup, ContractNo) ] ^
        ∀ContractNo<ack> [ Registered(FundingGroup, ContractNo) ] ^
        ∃ContractNo<funding-group> [ ¬(Registered(Ack, ContractNo)) ^ ¬(Registered(Fn, ContractNo)) ]
        """
        sample = io.BytesIO(b"""
        <article>
          <front>
            <article-meta>
              <funding-group>
                <award-group>
                  <funding-source>Brazilian Ministry of Health/Secretariat of Health Surveillance/Department of STD, AIDS and Viral Hepatitis</funding-source>
                  <award-id>234/07</award-id>
                </award-group>
                <award-group>
                  <funding-source>Brazilian Ministry of Health/Secretariat of Health Surveillance/Department of STD, AIDS and Viral Hepatitis</funding-source>
                  <award-id>236/08</award-id>
                </award-group>
                <funding-statement>This study was supported by the Brazilian Ministry of Health/Secretariat of Health Surveillance/Department of STD, AIDS and Viral Hepatitis, through the Project of International Technical Cooperation AD/BRA/03/H34 between the Brazilian Government and the United Nations Office on Drugs and Crime (Process CSV 234/07).</funding-statement>
              </funding-group>
            </article-meta>
          </front>
          <back>
            <fn-group>
              <fn id="fn1" fn-type="financial-disclosure">
                <p>This study was supported by the Brazilian Ministry of Health/Secretariat of Health Surveillance/Department of STD, AIDS and Viral Hepatitis, through the Project of International Technical Cooperation AD/BRA/03/H34 between the Brazilian Government and the United Nations Office on Drugs and Crime (Process CSV 234/07).</p>
              </fn>
            </fn-group>
          </back>
        </article>
        """)

        et = etree.parse(sample)
        _, err_list = checks.funding_group((et, []))

        self.assertEqual(len(err_list), 1)
        self.assertTrue("'funding-group'" in err_list[0].message)

    def test_fn_p_with_no_content(self):
        sample = io.BytesIO(b"""
        <article>
          <front>
            <article-meta>
            </article-meta>
          </front>
          <back>
            <fn-group>
              <fn id="fn1" fn-type="financial-disclosure">
                <p/>
              </fn>
            </fn-group>
          </back>
        </article>
        """)

        et = etree.parse(sample)
        _, err_list = checks.funding_group((et, []))

        self.assertEqual(len(err_list), 1)
        self.assertTrue("'fn-group'" in err_list[0].message)

    def test_fn_p_with_no_content_with_funding_group(self):
        sample = io.BytesIO(b"""
        <article>
          <front>
            <article-meta>
              <funding-group>
                <award-group>
                  <funding-source>Brazilian Ministry of Health/Secretariat of Health Surveillance/Department of STD, AIDS and Viral Hepatitis</funding-source>
                  <award-id>234/07</award-id>
                </award-group>
              </funding-group>
            </article-meta>
          </front>
          <back>
            <fn-group>
              <fn id="fn1" fn-type="financial-disclosure">
                <p/>
              </fn>
            </fn-group>
          </back>
        </article>
        """)

        et = etree.parse(sample)
        _, err_list = checks.funding_group((et, []))

        self.assertEqual(len(err_list), 1)
        self.assertTrue("'funding-group'" in err_list[0].message)

    def test_fn_p_and_awardid_with_no_content(self):
        sample = io.BytesIO(b"""
        <article>
          <front>
            <article-meta>
              <funding-group>
                <award-group>
                  <funding-source>Brazilian Ministry of Health/Secretariat of Health Surveillance/Department of STD, AIDS and Viral Hepatitis</funding-source>
                  <award-id/>
                </award-group>
              </funding-group>
            </article-meta>
          </front>
          <back>
            <fn-group>
              <fn id="fn1" fn-type="financial-disclosure">
                <p/>
              </fn>
            </fn-group>
          </back>
        </article>
        """)

        et = etree.parse(sample)
        _, err_list = checks.funding_group((et, []))

        self.assertEqual(len(err_list), 1)
        self.assertTrue("'fn-group'" in err_list[0].message)

    def test_valid_with_contractno_after_formatting_markup(self):
        sample = io.BytesIO(b"""
        <article>
          <front>
            <article-meta>
	      <funding-group>
	        <award-group>
		  <funding-source>Brazilian Ministry of Health/Secretariat of Health Surveillance/Department of STD, AIDS and Viral Hepatitis</funding-source>
		  <award-id>CSV 234/07</award-id>
		</award-group>
                <funding-statement>This study was supported by the Brazilian Ministry of Health/Secretariat of Health Surveillance/Department of STD, AIDS and Viral Hepatitis, through the Project of International Technical Cooperation AD/BRA/03/H34 between the Brazilian Government and the United Nations Office on Drugs and Crime (Process CSV 234/07).</funding-statement>
	      </funding-group>
            </article-meta>
          </front>
          <back>
            <ack>
	      <p>This study was supported by the <italic>Brazilian</italic> Ministry of Health/Secretariat of Health Surveillance/Department of STD, AIDS and Viral Hepatitis, through the Project of International Technical Cooperation AD/BRA/03/H34 between the Brazilian Government and the United Nations Office on Drugs and Crime (Process CSV 234/07).</p>
            </ack>
          </back>
        </article>
        """)

        et = etree.parse(sample)
        _, err_list = checks.funding_group((et, []))

        self.assertEqual(len(err_list), 0)

    def test_valid_with_contractno_after_formatting_markup_as_first_element(self):
        sample = io.BytesIO(b"""
        <article>
          <front>
            <article-meta>
	      <funding-group>
	        <award-group>
		  <funding-source>Brazilian Ministry of Health/Secretariat of Health Surveillance/Department of STD, AIDS and Viral Hepatitis</funding-source>
		  <award-id>2010/03107-2</award-id>
		</award-group>
                <funding-statement>Apoio financeiro: Fundacao de Amparo a Pesquisa do Estado de Sao Paulo (FAPESP). Processo 2010/03107-2. Conselho Nacional de Desenvolvimento Cientifico e Tecnologico (CNPq).
                </funding-statement>
              </funding-group>
            </article-meta>
          </front>
          <back>
	    <fn-group>
	      <fn fn-type="financial-disclosure">
	        <p><bold>Apoio financeiro:</bold> Fundacao de Amparo a Pesquisa do Estado de Sao
		   Paulo (FAPESP). Processo 2010/03107-2. Conselho Nacional de
		   Desenvolvimento Cientifico e Tecnologico (CNPq).</p>
	      </fn>
	    </fn-group>
          </back>
        </article>
        """)

        et = etree.parse(sample)
        _, err_list = checks.funding_group((et, []))

        self.assertEqual(len(err_list), 0)


class DoctypePipeTests(unittest.TestCase):

    def test_missing_doctype(self):
        sample = io.BytesIO(b"""
        <article>
          ...
        </article>
        """)

        et = etree.parse(sample)
        _, err_list = checks.doctype((et, []))

        self.assertEqual(len(err_list), 1)
        self.assertTrue("DOCTYPE" in err_list[0].message)

    def test_doctype(self):
        sample = io.BytesIO(b"""
        <!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "JATS-journalpublishing1.dtd">
        <article>
          ...
        </article>
        """)

        et = etree.parse(sample)
        _, err_list = checks.doctype((et, []))

        self.assertEqual(len(err_list), 0)


class CountryCodesTests(unittest.TestCase):

    def test_valid_code(self):
        sample = io.BytesIO(b"""
        <article>
          <front>
            <article-meta>
              <aff id="aff1">
                <label>I</label>
                <institution content-type="orgdiv2">Departamento de Fonoaudiologia</institution>
                <institution content-type="orgdiv1">Faculdade de Medicina</institution>
                <institution content-type="orgname">Universidade Federal do Rio de Janeiro</institution>
                <addr-line>
                  <named-content content-type="city">Rio de Janeiro</named-content>
                  <named-content content-type="state">RJ</named-content>
                </addr-line>
                <country country="BR">Brasil</country>
                <institution content-type="original">Departamento de Fonoaudiologia. Faculdade de Medicina. Universidade Federal do Rio de Janeiro. Rio de Janeiro, RJ, Brasil</institution>
              </aff>
            </article-meta>
          </front>
        </article>
        """)

        et = etree.parse(sample)
        _, err_list = checks.country_code((et, []))

        self.assertEqual(len(err_list), 0)

    def test_valid_code_in_lowercase(self):
        sample = io.BytesIO(b"""
        <article>
          <front>
            <article-meta>
              <aff id="aff1">
                <label>I</label>
                <institution content-type="orgdiv2">Departamento de Fonoaudiologia</institution>
                <institution content-type="orgdiv1">Faculdade de Medicina</institution>
                <institution content-type="orgname">Universidade Federal do Rio de Janeiro</institution>
                <addr-line>
                  <named-content content-type="city">Rio de Janeiro</named-content>
                  <named-content content-type="state">RJ</named-content>
                </addr-line>
                <country country="br">Brasil</country>
                <institution content-type="original">Departamento de Fonoaudiologia. Faculdade de Medicina. Universidade Federal do Rio de Janeiro. Rio de Janeiro, RJ, Brasil</institution>
              </aff>
            </article-meta>
          </front>
        </article>
        """)

        et = etree.parse(sample)
        _, err_list = checks.country_code((et, []))

        self.assertEqual(len(err_list), 1)
        self.assertTrue("country" in err_list[0].message)

    def test_invalid_code(self):
        sample = io.BytesIO(b"""
        <article>
          <front>
            <article-meta>
              <aff id="aff1">
                <label>I</label>
                <institution content-type="orgdiv2">Departamento de Fonoaudiologia</institution>
                <institution content-type="orgdiv1">Faculdade de Medicina</institution>
                <institution content-type="orgname">Universidade Federal do Rio de Janeiro</institution>
                <addr-line>
                  <named-content content-type="city">Rio de Janeiro</named-content>
                  <named-content content-type="state">RJ</named-content>
                </addr-line>
                <country country="INVALID">Brasil</country>
                <institution content-type="original">Departamento de Fonoaudiologia. Faculdade de Medicina. Universidade Federal do Rio de Janeiro. Rio de Janeiro, RJ, Brasil</institution>
              </aff>
            </article-meta>
          </front>
        </article>
        """)

        et = etree.parse(sample)
        _, err_list = checks.country_code((et, []))

        self.assertEqual(len(err_list), 1)
        self.assertTrue("country" in err_list[0].message)

