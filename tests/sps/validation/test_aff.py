from unittest import TestCase

from lxml import etree

from packtools.sps.validation.aff import AffiliationValidation


class ArticleAuthorsValidationTest(TestCase):
    def test_affliation_without_original(self):
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
                </aff>
            </front-stub>
            </front>
        </article>
        """)

        data = etree.fromstring(xml)
        message = AffiliationValidation(data).validate_affiliation

        expected_output = [
            {
                'result': 'success', 
                'message': 'The affiliation of id: aff1 is ok!'
            },
            {
                'result': 'error', 
                'error_type': 'No original found', 
                'message': 'The affiliation of id: aff2 does not have an original. Please add one.'
            },
            {
                'result': 'error', 
                'error_type': 'No original found', 
                'message': 'The affiliation of id: aff3 does not have an original. Please add one.'
            },            
        ]

        self.assertEqual(message, expected_output)


    def test_affiliations_without_country(self):
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
            </front>
        </article>
        """)

        data = etree.fromstring(xml)
        message = AffiliationValidation(data).validate_affiliation        

        expected_output = [
            {
                'result': 'error',
                'error_type': 'No country found',
                'message': 'The affiliation of id: aff1 does not have a country. Please add one.'
            },
            {
                'result': 'error',
                'error_type': 'No country found',
                'message': 'The affiliation of id: aff2 does not have a country. Please add one.'
            },
            {
                'result': 'success', 
                'message': 'The affiliation of id: aff3 is ok!'
            }            
        ]

        self.assertEqual(message, expected_output)


    def test_affiliations(self):
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
            </front>
        </article>
        """)
        data = etree.fromstring(xml)
        message = AffiliationValidation(data).validate_affiliation

        expected_output = [
            {
                'result': 'success',
                'message': 'The affiliation of id: aff1 is ok!'
            },
            {
                'result': 'success',
                'message': 'The affiliation of id: aff2 is ok!'
            },
            {
                'result': 'success', 
                'message': 'The affiliation of id: aff3 is ok!'
            }
        ]

        self.assertEqual(message, expected_output)    