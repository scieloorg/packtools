from unittest import TestCase
from lxml import etree
from packtools.sps.utils import xml_utils

from packtools.report import ReportXML


class ReportTest(TestCase):
    def test_report(self):
        xml = ("""
        <article>
            <front>
                <article-meta>
                    <aff id="aff1">
                        <label>I</label>
                        <institution content-type="orgname">Secretaria Municipal de Saúde de Belo Horizonte</institution>
                        <addr-line>
                            <named-content content-type="city">Belo Horizonte</named-content>
                            <named-content content-type="state">MG</named-content>
                        </addr-line>
                        <country>Brasil</country>
                        <institution content-type="original">Secretaria Municipal de Saúde de Belo Horizonte. Belo Horizonte, MG, Brasil</institution>
                    </aff>
                    <aff id="aff2">
                        <label>II</label>
                        <institution content-type="orgdiv1">Faculdade de Medicina</institution>
                        <institution content-type="orgname">Universidade Federal de Minas Gerais</institution>
                        <addr-line>
                            <named-content content-type="city">Belo Horizonte</named-content>
                            <named-content content-type="state">MG</named-content>
                        </addr-line>
                        <country>Brasil</country>
                        <institution content-type="original">Grupo de Pesquisas em Epidemiologia e Avaliação em Saúde. Faculdade de Medicina. Universidade Federal de Minas Gerais. Belo Horizonte, MG, Brasil</institution>
                    </aff>
                </article-meta>
                <front-stub>
                <aff id="aff3">
                    <label>III</label>
                    <institution content-type="orgdiv2">Departamento de Ciências Sociais</institution>
                    <institution content-type="orgdiv1">Escola Nacional de Saúde Pública Sergio Arouca</institution>
                    <institution content-type="orgname">Fundação Oswaldo Cruz</institution>
                    <addr-line>
                        <named-content content-type="city">Rio de Janeiro</named-content>
                        <named-content content-type="state">RJ</named-content>
                    </addr-line>
                    <country>Brasil</country>
                    <institution content-type="original">Departamento de Ciências Sociais. Escola Nacional de Saúde Pública Sergio Arouca. Fundação Oswaldo Cruz. Rio de Janeiro, RJ, Brasil</institution>
                </aff>
            </front-stub>
            <contrib-group>
                <aff id="aff4">
                    <label>IV</label>
                    <institution content-type="orgdiv2">Departamento de Farmácia Social</institution>
                    <institution content-type="orgdiv1">Faculdade de Farmácia</institution>
                    <institution content-type="orgname">Universidade Federal de Minas Gerais</institution>
                    <addr-line>
                        <named-content content-type="city">Belo Horizonte</named-content>
                        <named-content content-type="state">MG</named-content>
                    </addr-line>
                    <country>Brasil</country>
                    <institution content-type="original">Departamento de Farmácia Social. Faculdade de Farmácia. Universidade Federal de Minas Gerais. Belo Horizonte, MG, Brasil</institution>
                </aff>
                <aff id="aff5">
                    <label>V</label>
                    <institution content-type="orgdiv2">Departamento de Saúde Comunitária</institution>
                    <institution content-type="orgdiv1">Faculdade de Medicina</institution>
                    <institution content-type="orgname">Universidade Federal do Ceará</institution>
                    <addr-line>
                        <named-content content-type="city">Fortaleza</named-content>
                        <named-content content-type="state">CE</named-content>
                    </addr-line>
                    <country>Brasil</country>
                    <institution content-type="original">Departamento de Saúde Comunitária. Faculdade de Medicina. Universidade Federal do Ceará. Fortaleza, CE, Brasil</institution>
                </aff>
            </contrib-group>
            </front>
        </article>
        """)

        # xml = etree.fromstring(xml)        
        xml = xml_utils.get_xml_tree('tests/samples/0034-7094-rba-69-03-0227.xml')
        report = ReportXML(xmltree=xml).report()