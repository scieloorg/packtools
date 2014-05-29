import unittest
from StringIO import StringIO

from lxml import etree

from packtools import checks


class SetupTests(unittest.TestCase):
    def test_message_is_splitted(self):
        fp = etree.parse(StringIO(b'<a><b>bar</b></a>'))
        self.assertEqual(checks.setup(fp), (fp, []))


class TeardownTests(unittest.TestCase):
    def test_returns_errorlist(self):
        fp = etree.parse(StringIO(b'<a><b>bar</b></a>'))
        err_list = ['some error']
        message = (fp, err_list)
        self.assertEqual(checks.teardown(message), err_list)


class PipelineTests(unittest.TestCase):
    def test_connected_pipes_no(self):
        ppl = checks.StyleCheckingPipeline()
        self.assertEqual(len(ppl._pipes), 2)

    @unittest.skip('depends on not implemented feature')
    def test_connected_pipes(self):
        """Make sure that all meaningful pipes are part of the pipeline.
        """

class AwardIdMatchingTests(unittest.TestCase):
    """
    For more information about the spec and test-cases, refer to
    :func:`packtools.checks.funding_group`.
    """
    def test_case1(self):
        """Appears in <fn> element.
        """
        text = 'This study was supported by the Conselho Nacional de Desenvolvimento Científico e Tecnológico (CNPq – Process 302.600/2008-6 – Productivity grant).'
        expected = '302.600/2008-6'

    def test_case2(self):
        """Appears in <fn> element.
        """
        text = 'This study was supported by the Brazilian Ministry of Health/Secretariat of Health Surveillance/Department of STD, AIDS and Viral Hepatitis, through the Project of International Technical Cooperation AD/BRA/03/H34 between the Brazilian Government and the United Nations Office on Drugs and Crime (Process CSV 234/07).'
        expected = '234/07'

    def test_case3(self):
        """Appears in <fn> element.
        """
        text = 'This study was supported by the <italic>Fundação para o Desenvolvimento Científico e Tecnológico em Saúde</italic> (FIOTEC – Process ENSP-013-LIV10-2-5-33 –<italic> Programa Inova </italic>ENSP).'
        expected = 'ENSP-013-LIV10-2-5-33'

    def test_case4(self):
        """Appears in <fn> element.
        """
        text = 'Estudo financiado pelo Projeto de Pesquisa Ministério de Ciência e Tecnologia (MCT), Conselho Nacional de Desenvolvimento Científico e Tecnológico (CNPq – Edital MCT-CNPq/CT – Saúde 021/2008 – Processo 402195/2008).'
        expected = '402195/2008'

    def test_case5(self):
        """Appears in <fn> element.
        """
        text = 'The author received a grant from the Coordenação de Aperfeiçoamento de Pessoal de Nível Superior (Capes) during the doctorate and from the Conselho Nacional de Desenvolvimento Científico e Tecnológico (CNPq) during the Sandwich PhD abroad (SWE – Process 200741/2011-0).'
        expected = '200741/2011-0'

    def test_case6(self):
        """Appears in <fn> element.
        """
        text = 'This study was supported by the Fundação de Amparo à Pesquisa do Estado de São Paulo (FAPESP – Process 2009/08844-8).'
        expected = '2009/08844-8'

    def test_case7(self):
        """Appears in <fn> element.
        """
        text = 'This study was partially supported by the <italic>Conselho Nacional de Desenvolvimento Científico e Tecnológico</italic> (CNPq) and by the <italic>Institutos Nacionais de Ciência e Tecnologia</italic> (INCT) <italic>de Hormônios e Saúde da Mulher</italic> (CNPq/INCT 573747/2008-3).'
        expected = '573747/2008-3'

    def test_case8(self):
        """Appears in <fn> element.
        """
        text = 'This study was supported by the <italic>Fundação de Amparo à Pesquisa do Estado do Mato Grosso</italic> (FAPEMAT – Process 446298/2009) and by the <italic>Conselho Nacional de Desenvolvimento Científico e Tecnológico</italic> (CNPq – Process 471063/2009-6).'
        expected = ['446298/2009', '471063/2009-6']

    def test_case9(self):
        """Appears in <fn> element.
        """
        text = 'This study was supported by the <italic>Fundação de Apoio, Pesquisa e Assistência</italic> (FAEPA) of the <italic>Hospital das Clínicas</italic>, Ribeirao Preto Medical School of the <italic>Universidade de São Paulo</italic> (FAEPA/HC-98/2009) and by the <italic>Programa Ensinar com Pesquisa</italic> of the <italic>Universidade de São Paulo</italic> (PROEP/2009) (grants for students in Medicine School).'
        expected = 'FAEPA/HC-98/2009'

    def test_case10(self):
        """Appears in <fn> element.
        """
        text = 'This study was supported by the <italic>Fundação de Amparo à Pesquisa do Estado de Minas Gerais </italic>and the<italic> Universidade Estadual de Montes Claros</italic> (FAPEMIG/UNIMONTES – <italic>Programa de Capacitação de Recursos Humanos</italic> – Process 90508-11 – Doctoral grant to Sibylle Emilie Vogt).'
        expected = '90508-11'

    def test_case11(self):
        """Appears in <fn> element.
        """
        text = 'This study was supported by the Conselho Nacional de Desenvolvimento Científico e Tecnológico (CNPq – Process 124647/2010-3 – scientific initiation grant).'
        expected = '124647/2010-3'

