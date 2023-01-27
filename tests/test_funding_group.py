# coding: utf-8
from __future__ import unicode_literals
import unittest
try:
    from unittest import mock
except:
    import mock

from lxml import etree
from packtools.sps.models.funding_group import FundingGroup


class FundingGroupOneFundingSourceNAwardIdTests(unittest.TestCase):
    def setUp(self):
        xml = (
            """
            <article> 
                <funding-group>
                      <award-group>
                          <funding-source>CNPQ</funding-source>
                          <award-id>12345</award-id>
                          <award-id>67890</award-id>
                      </award-group>
                      <award-group>
                          <funding-source>FAPESP</funding-source>
                          <award-id>23456</award-id>
                          <award-id>56789</award-id>
                      </award-group>
                </funding-group>
            </article>
            """
        )
        self.funding_group = FundingGroup(etree.fromstring(xml))

    def test_funding_sources(self):
        expected = ['CNPQ', 'FAPESP']
        result = self.funding_group.funding_sources
        self.assertEqual(expected, result)

    def test_award_groups(self):
        expected = [
            {'funding-source': ['CNPQ'], 'award-id': ['12345', '67890']},
            {'funding-source': ['FAPESP'], 'award-id': ['23456', '56789']},
        ]
        result = self.funding_group.award_groups
        self.assertEqual(expected, result)


class FundingGroupOneFundingSourceOneAwardIdTests(unittest.TestCase):
    def setUp(self):
        xml = (
            """
            <article> 
                <funding-group>
                     <award-group>
                         <funding-source>CNPq</funding-source>
                         <award-id>1685X6-7</award-id>
                     </award-group>
                </funding-group>
            </article>
            """
        )
        self.funding_group = FundingGroup(etree.fromstring(xml))

    def test_funding_sources(self):
        expected = ['CNPq']
        result = self.funding_group.funding_sources
        self.assertEqual(expected, result)

    def test_award_groups(self):
        expected = [
            {'funding-source': ['CNPq'], 'award-id': ['1685X6-7']}
        ]
        result = self.funding_group.award_groups
        self.assertEqual(expected, result)


class FundingGroupNFundingSourceOneAwardIdTests(unittest.TestCase):
    def setUp(self):
        xml = (
            """
            <article> 
                <funding-group>
                    <award-group>
                        <funding-source>CNPq</funding-source>
                        <funding-source>FAPESP</funding-source>
                        <award-id>#09/06953-4</award-id>
                    </award-group>
                </funding-group>
            </article>
            """
        )
        self.funding_group = FundingGroup(etree.fromstring(xml))

    def test_funding_sources(self):
        expected = ['CNPq', 'FAPESP']
        result = self.funding_group.funding_sources
        self.assertEqual(expected, result)

    def test_award_groups(self):
        expected = [
            {'funding-source': ['CNPq', 'FAPESP'], 'award-id': ['#09/06953-4']}
        ]
        result = self.funding_group.award_groups
        self.assertEqual(expected, result)


class FundingGroupNFundingSourceOneAwardIdWithFundingStatementTests(unittest.TestCase):
    def setUp(self):
        xml = (
            """
            <article> 
                <funding-group>
                    <award-group>
                        <funding-source>Coordenação de Aperfeiçoamento de Pessoal de Nível Superior</funding-source>
                        <funding-source> Fundação de Amparo à Pesquisa do Estado de São Paulo</funding-source>
                        <award-id>04/08142-0</award-id>
                    </award-group>
                    <funding-statement>This study was supported in part by Coordenação
                    de Aperfeiçoamento de Pessoal de Nível Superior (Capes — Brasília,
                    Brazil), Fundação de Amparo à Pesquisa do Estado de São Paulo (FAPESP —
                    Grant no. 04/08142-0; São Paulo, Brazil)</funding-statement>
                </funding-group>
            </article>
            """
        )
        self.funding_group = FundingGroup(etree.fromstring(xml))

    def test_funding_sources(self):
        expected = ['Coordenação de Aperfeiçoamento de Pessoal de Nível Superior',
                    ' Fundação de Amparo à Pesquisa do Estado de São Paulo']
        result = self.funding_group.funding_sources
        self.assertEqual(expected, result)

    def test_award_groups(self):
        expected = [
            {'funding-source': ['Coordenação de Aperfeiçoamento de Pessoal de Nível Superior',
                                ' Fundação de Amparo à Pesquisa do Estado de São Paulo'], 'award-id': ['04/08142-0']}
        ]
        result = self.funding_group.award_groups
        self.assertEqual(expected, result)
