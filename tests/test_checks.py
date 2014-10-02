# coding: utf-8
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


class PipelineTests(unittest.TestCase):
    def test_connected_pipes_no(self):
        ppl = checks.StyleCheckingPipeline()
        self.assertEqual(len(ppl._pipes), 4)

    @unittest.skip('depends on not implemented feature')
    def test_connected_pipes(self):
        """Make sure that all meaningful pipes are part of the pipeline.
        """


# ----------------------------------
# Funding Group pipe and utils tests
# ----------------------------------
class AwardIdMatchingTests(unittest.TestCase):
    """
    For more information about the spec and test-cases, refer to
    :func:`packtools.checks.funding_group`.
    """
    pattern = checks.AWARDID_PATTERN

    def test_case1(self):
        """Appears in <fn> element.
        """
        text = u'This study was supported by the Conselho Nacional de Desenvolvimento Científico e Tecnológico (CNPq – Process 302.600/2008-6 – Productivity grant).'
        expected = '302.600/2008-6'

        matches = self.pattern.findall(text)
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0], expected)

        # Trying to eliminate false positives.
        self.assertEqual(checks._find_contract_numbers(text), [expected])

    def test_case2(self):
        """Appears in <fn> element.
        """
        text = u'This study was supported by the Brazilian Ministry of Health/Secretariat of Health Surveillance/Department of STD, AIDS and Viral Hepatitis, through the Project of International Technical Cooperation AD/BRA/03/H34 between the Brazilian Government and the United Nations Office on Drugs and Crime (Process CSV 234/07).'
        expected = '234/07'

        matches = self.pattern.findall(text)
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0], expected)

        # Trying to eliminate false positives.
        self.assertEqual(checks._find_contract_numbers(text), [expected])

    def test_case3(self):
        """Appears in <fn> element.
        """
        text = u'This study was supported by the <italic>Fundação para o Desenvolvimento Científico e Tecnológico em Saúde</italic> (FIOTEC – Process ENSP-013-LIV10-2-5-33 –<italic> Programa Inova </italic>ENSP).'
        expected = 'ENSP-013-LIV10-2-5-33'

        matches = self.pattern.findall(text)
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0], expected)

        # Trying to eliminate false positives.
        self.assertEqual(checks._find_contract_numbers(text), [expected])

    def test_case4(self):
        """Appears in <fn> element.
        """
        text = u'Estudo financiado pelo Projeto de Pesquisa Ministério de Ciência e Tecnologia (MCT), Conselho Nacional de Desenvolvimento Científico e Tecnológico (CNPq – Edital MCT-CNPq/CT – Saúde 021/2008 – Processo 402195/2008).'
        expected = '402195/2008'

        matches = self.pattern.findall(text)
        # Impossible to disambiguate the edital number and the process number.
        # In that cases, the reviewer must be warned and perform a manual
        # validation.
        self.assertEqual(len(matches), 2)
        self.assertIn(expected, matches)
        self.assertIn('021/2008', matches)  # edital number

        # Trying to eliminate false positives.
        self.assertEqual(sorted(checks._find_contract_numbers(text)),
                         sorted([expected, '021/2008']))

    def test_case5(self):
        """Appears in <fn> element.
        """
        text = u'The author received a grant from the Coordenação de Aperfeiçoamento de Pessoal de Nível Superior (Capes) during the doctorate and from the Conselho Nacional de Desenvolvimento Científico e Tecnológico (CNPq) during the Sandwich PhD abroad (SWE – Process 200741/2011-0).'
        expected = '200741/2011-0'

        matches = self.pattern.findall(text)
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0], expected)

        # Trying to eliminate false positives.
        self.assertEqual(checks._find_contract_numbers(text), [expected])

    def test_case6(self):
        """Appears in <fn> element.
        """
        text = u'This study was supported by the Fundação de Amparo à Pesquisa do Estado de São Paulo (FAPESP – Process 2009/08844-8).'
        expected = '2009/08844-8'

        matches = self.pattern.findall(text)
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0], expected)

        # Trying to eliminate false positives.
        self.assertEqual(checks._find_contract_numbers(text), [expected])

    def test_case7(self):
        """Appears in <fn> element.
        """
        text = u'This study was partially supported by the <italic>Conselho Nacional de Desenvolvimento Científico e Tecnológico</italic> (CNPq) and by the <italic>Institutos Nacionais de Ciência e Tecnologia</italic> (INCT) <italic>de Hormônios e Saúde da Mulher</italic> (CNPq/INCT 573747/2008-3).'
        expected = '573747/2008-3'

        matches = self.pattern.findall(text)
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0], expected)

        # Trying to eliminate false positives.
        self.assertEqual(checks._find_contract_numbers(text), [expected])

    def test_case8(self):
        """Appears in <fn> element.
        """
        text = u'This study was supported by the <italic>Fundação de Amparo à Pesquisa do Estado do Mato Grosso</italic> (FAPEMAT – Process 446298/2009) and by the <italic>Conselho Nacional de Desenvolvimento Científico e Tecnológico</italic> (CNPq – Process 471063/2009-6).'
        expected = ['446298/2009', '471063/2009-6']

        matches = self.pattern.findall(text)
        self.assertEqual(len(matches), 2)
        self.assertEqual(sorted(matches), sorted(expected))

        # Trying to eliminate false positives.
        self.assertEqual(checks._find_contract_numbers(text), expected)

    @unittest.expectedFailure
    def test_case9(self):
        """Appears in <fn> element.

        The OR does not prevent the last regex from being processed,
        so `2009` from `PROEP/2009` is also matched. By now years are
        handled as false positives at :func:`checks._find_contract_numbers`.
        """
        text = u'This study was supported by the <italic>Fundação de Apoio, Pesquisa e Assistência</italic> (FAEPA) of the <italic>Hospital das Clínicas</italic>, Ribeirao Preto Medical School of the <italic>Universidade de São Paulo</italic> (FAEPA/HC-98/2009) and by the <italic>Programa Ensinar com Pesquisa</italic> of the <italic>Universidade de São Paulo</italic> (PROEP/2009) (grants for students in Medicine School).'
        expected = 'FAEPA/HC-98/2009'

        matches = self.pattern.findall(text)
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0], expected)

    def test_case9_false_positive_handling(self):
        """Appears in <fn> element.
        """
        text = u'This study was supported by the <italic>Fundação de Apoio, Pesquisa e Assistência</italic> (FAEPA) of the <italic>Hospital das Clínicas</italic>, Ribeirao Preto Medical School of the <italic>Universidade de São Paulo</italic> (FAEPA/HC-98/2009) and by the <italic>Programa Ensinar com Pesquisa</italic> of the <italic>Universidade de São Paulo</italic> (PROEP/2009) (grants for students in Medicine School).'
        expected = 'FAEPA/HC-98/2009'

        # Trying to eliminate false positives.
        self.assertEqual(checks._find_contract_numbers(text), [expected])

    def test_case10(self):
        """Appears in <fn> element.
        """
        text = u'This study was supported by the <italic>Fundação de Amparo à Pesquisa do Estado de Minas Gerais </italic>and the<italic> Universidade Estadual de Montes Claros</italic> (FAPEMIG/UNIMONTES – <italic>Programa de Capacitação de Recursos Humanos</italic> – Process 90508-11 – Doctoral grant to Sibylle Emilie Vogt).'
        expected = '90508-11'

        matches = self.pattern.findall(text)
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0], expected)

        # Trying to eliminate false positives.
        self.assertEqual(checks._find_contract_numbers(text), [expected])

    def test_case11(self):
        """Appears in <fn> element.
        """
        text = u'This study was supported by the Conselho Nacional de Desenvolvimento Científico e Tecnológico (CNPq – Process 124647/2010-3 – scientific initiation grant).'
        expected = '124647/2010-3'

        matches = self.pattern.findall(text)
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0], expected)

        # Trying to eliminate false positives.
        self.assertEqual(checks._find_contract_numbers(text), [expected])

    @unittest.skip('# should not be part of the contract number. waiting for confirmation.')
    def test_case12(self):
        """Appears in <ack> element.
        """
        text = u'Research supported by FAPESP (#2000/08755-0), CNPq (#301483/2006-0) and FUNDECT (#0248/12).'
        expected = ['#2000/08755-0', '#301483/2006-0', '#0248/12']

        matches = self.pattern.findall(text)
        self.assertEqual(len(matches), 3)
        self.assertEqual(sorted(matches), sorted(expected))

        # Trying to eliminate false positives.
        self.assertEqual(checks._find_contract_numbers(text), expected)


class FindContractNumbersTests(unittest.TestCase):
    def test_contract_numbers_in_fn_element(self):
        sample = os.path.join(SAMPLES_PATH, '0034-8910-rsp-48-2-0206.xml')

        et = etree.parse(sample)
        found_numbers = checks.find_contract_numbers(et)
        self.assertEqual(found_numbers, {'fn': ['234/07']})


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
        self.assertTrue("'funding-group'" in err_list[0].message)

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
        """
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

        self.assertEqual(len(err_list), 1)
        self.assertTrue("'ack'" in err_list[0].message)

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

