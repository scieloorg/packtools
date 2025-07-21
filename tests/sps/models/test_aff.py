from unittest import TestCase

from packtools.sps.models.aff import AffiliationExtractor
from packtools.sps.models.aff import Affiliation

from lxml import etree


class AffTest(TestCase):
    def test_extract_affliation_article_meta_front_stub_contrib_group(self):
        xml = """
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
        """

        xml = etree.fromstring(xml)
        data = AffiliationExtractor(xml).get_affiliation_data_from_multiple_tags(
            subtag=False
        )

        expected_output = [
            {
                "id": "aff1",
                "label": "I",
                "institution": [
                    {
                        "orgname": "Secretaria Municipal de Saúde de Belo Horizonte",
                        "orgdiv1": "",
                        "orgdiv2": "",
                        "original": "Secretaria Municipal de Saúde de Belo Horizonte. Belo Horizonte, MG, Brasil",
                    }
                ],
                "city": "Belo Horizonte",
                "state": "MG",
                "country": [{"code": "", "name": "Brasil"}],
                "email": "",
            },
            {
                "id": "aff2",
                "label": "II",
                "city": "Belo Horizonte",
                "state": "MG",
                "country": [{"code": "", "name": "Brasil"}],
                "institution": [
                    {
                        "orgname": "Universidade Federal de Minas Gerais",
                        "orgdiv1": "Faculdade de Medicina",
                        "orgdiv2": "",
                        "original": "Grupo de Pesquisas em Epidemiologia e Avaliação em Saúde. Faculdade de Medicina. Universidade Federal de Minas Gerais. Belo Horizonte, MG, Brasil",
                    }
                ],
                "email": "",
            },
            {
                "id": "aff3",
                "label": "III",
                "institution": [
                    {
                        "orgname": "Fundação Oswaldo Cruz",
                        "orgdiv1": "Escola Nacional de Saúde Pública Sergio Arouca",
                        "orgdiv2": "Departamento de Ciências Sociais",
                        "original": "Departamento de Ciências Sociais. Escola Nacional de Saúde Pública Sergio Arouca. Fundação Oswaldo Cruz. Rio de Janeiro, RJ, Brasil",
                    }
                ],
                "city": "Rio de Janeiro",
                "state": "RJ",
                "country": [{"code": "", "name": "Brasil"}],
                "email": "",
            },
            {
                "id": "aff4",
                "label": "IV",
                "institution": [
                    {
                        "orgname": "Universidade Federal de Minas Gerais",
                        "orgdiv1": "Faculdade de Farmácia",
                        "orgdiv2": "Departamento de Farmácia Social",
                        "original": "Departamento de Farmácia Social. Faculdade de Farmácia. Universidade Federal de Minas Gerais. Belo Horizonte, MG, Brasil",
                    }
                ],
                "city": "Belo Horizonte",
                "state": "MG",
                "country": [{"code": "", "name": "Brasil"}],
                "email": "",
            },
            {
                "id": "aff5",
                "label": "V",
                "institution": [
                    {
                        "orgname": "Universidade Federal do Ceará",
                        "orgdiv1": "Faculdade de Medicina",
                        "orgdiv2": "Departamento de Saúde Comunitária",
                        "original": "Departamento de Saúde Comunitária. Faculdade de Medicina. Universidade Federal do Ceará. Fortaleza, CE, Brasil",
                    }
                ],
                "city": "Fortaleza",
                "state": "CE",
                "country": [{"code": "", "name": "Brasil"}],
                "email": "",
            },
        ]

        self.assertEqual(data, expected_output)

    def test_extract_affiliation_with_subtag(self):
        xml = """
        <article>
            <front>
                <article-meta>
                    <aff id="aff1">
                        <label>I</label>
                        <institution content-type="orgname">Secretaria <italic>Municipal</italic> de Saúde de Belo Horizonte</institution>
                        <addr-line>
                            <named-content content-type="city"><bold>Belo Horizonte</bold></named-content>
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
                            <named-content content-type="city"><italic>Belo Horizonte</italic></named-content>
                            <named-content content-type="state">MG</named-content>
                        </addr-line>
                        <country>Brasil</country>
                        <institution content-type="original">Grupo de Pesquisas em Epidemiologia e Avaliação em Saúde. Faculdade de Medicina. Universidade Federal de Minas Gerais. Belo Horizonte, MG, Brasil</institution>
                    </aff>
                </article-meta>
                <front-stub>
                <aff id="aff3">
                    <label>III</label>
                    <institution content-type="orgdiv2"><italic>Departamento de Ciências Sociais</italic></institution>
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
                    <institution content-type="orgname"><bold>Universidade Federal de Minas Gerais</bold></institution>
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
                        <named-content content-type="city"><italic>Fortaleza</italic></named-content>
                        <named-content content-type="state">CE</named-content>
                    </addr-line>
                    <country>Brasil</country>
                    <institution content-type="original">Departamento de Saúde Comunitária. Faculdade de Medicina. Universidade Federal do Ceará. Fortaleza, CE, Brasil</institution>
                </aff>
            </contrib-group>
            </front>
        </article>
        """

        xml = etree.fromstring(xml)
        data = AffiliationExtractor(xml).get_affiliation_data_from_multiple_tags(
            subtag=True
        )

        expected_output = [
            {
                "id": "aff1",
                "label": "I",
                "institution": [
                    {
                        "orgname": "Secretaria <italic>Municipal</italic> de Saúde de Belo Horizonte",
                        "orgdiv1": "",
                        "orgdiv2": "",
                        "original": "Secretaria Municipal de Saúde de Belo Horizonte. Belo Horizonte, MG, Brasil",
                    }
                ],
                "city": "<bold>Belo Horizonte</bold>",
                "state": "MG",
                "country": [{"code": "", "name": "Brasil"}],
                "email": "",
            },
            {
                "id": "aff2",
                "label": "II",
                "institution": [
                    {
                        "orgname": "Universidade Federal de Minas Gerais",
                        "orgdiv1": "Faculdade de Medicina",
                        "orgdiv2": "",
                        "original": "Grupo de Pesquisas em Epidemiologia e Avaliação em Saúde. Faculdade de Medicina. Universidade Federal de Minas Gerais. Belo Horizonte, MG, Brasil",
                    }
                ],
                "city": "<italic>Belo Horizonte</italic>",
                "state": "MG",
                "country": [{"code": "", "name": "Brasil"}],
                "email": "",
            },
            {
                "id": "aff3",
                "label": "III",
                "institution": [
                    {
                        "orgname": "Fundação Oswaldo Cruz",
                        "orgdiv1": "Escola Nacional de Saúde Pública Sergio Arouca",
                        "orgdiv2": "<italic>Departamento de Ciências Sociais</italic>",
                        "original": "Departamento de Ciências Sociais. Escola Nacional de Saúde Pública Sergio Arouca. Fundação Oswaldo Cruz. Rio de Janeiro, RJ, Brasil",
                    }
                ],
                "city": "Rio de Janeiro",
                "state": "RJ",
                "country": [{"code": "", "name": "Brasil"}],
                "email": "",
            },
            {
                "id": "aff4",
                "label": "IV",
                "institution": [
                    {
                        "orgname": "<bold>Universidade Federal de Minas Gerais</bold>",
                        "orgdiv1": "Faculdade de Farmácia",
                        "orgdiv2": "Departamento de Farmácia Social",
                        "original": "Departamento de Farmácia Social. Faculdade de Farmácia. Universidade Federal de Minas Gerais. Belo Horizonte, MG, Brasil",
                    }
                ],
                "city": "Belo Horizonte",
                "state": "MG",
                "country": [{"code": "", "name": "Brasil"}],
                "email": "",
            },
            {
                "id": "aff5",
                "label": "V",
                "institution": [
                    {
                        "orgname": "Universidade Federal do Ceará",
                        "orgdiv1": "Faculdade de Medicina",
                        "orgdiv2": "Departamento de Saúde Comunitária",
                        "original": "Departamento de Saúde Comunitária. Faculdade de Medicina. Universidade Federal do Ceará. Fortaleza, CE, Brasil",
                    }
                ],
                "city": "<italic>Fortaleza</italic>",
                "state": "CE",
                "country": [{"code": "", "name": "Brasil"}],
                "email": "",
            },
        ]

        self.assertEqual(data, expected_output)

    def test_extract_affiliation_without_subtag(self):
        xml = """
        <article>
            <front>
                <article-meta>
                    <aff id="aff1">
                        <label>I</label>
                        <institution content-type="orgname">Secretaria <italic>Municipal</italic> de Saúde de Belo Horizonte</institution>
                        <addr-line>
                            <named-content content-type="city"><bold>Belo Horizonte</bold></named-content>
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
                            <named-content content-type="city"><italic>Belo Horizonte</italic></named-content>
                            <named-content content-type="state">MG</named-content>
                        </addr-line>
                        <country>Brasil</country>
                        <institution content-type="original">Grupo de Pesquisas em Epidemiologia e Avaliação em Saúde. Faculdade de Medicina. Universidade Federal de Minas Gerais. Belo Horizonte, MG, Brasil</institution>
                    </aff>
                </article-meta>
                <front-stub>
                <aff id="aff3">
                    <label>III</label>
                    <institution content-type="orgdiv2"><italic>Departamento de Ciências Sociais</italic></institution>
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
                    <institution content-type="orgname"><bold>Universidade Federal de Minas Gerais</bold></institution>
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
                        <named-content content-type="city"><italic>Fortaleza</italic></named-content>
                        <named-content content-type="state">CE</named-content>
                    </addr-line>
                    <country>Brasil</country>
                    <institution content-type="original">Departamento de Saúde Comunitária. Faculdade de Medicina. Universidade Federal do Ceará. Fortaleza, CE, Brasil</institution>
                </aff>
            </contrib-group>
            </front>
        </article>
        """

        xml = etree.fromstring(xml)
        data = AffiliationExtractor(xml).get_affiliation_data_from_multiple_tags(
            subtag=False
        )

        expected_output = [
            {
                "id": "aff1",
                "label": "I",
                "institution": [
                    {
                        "orgname": "Secretaria Municipal de Saúde de Belo Horizonte",
                        "orgdiv1": "",
                        "orgdiv2": "",
                        "original": "Secretaria Municipal de Saúde de Belo Horizonte. Belo Horizonte, MG, Brasil",
                    }
                ],
                "city": "Belo Horizonte",
                "state": "MG",
                "country": [{"code": "", "name": "Brasil"}],
                "email": "",
            },
            {
                "id": "aff2",
                "label": "II",
                "institution": [
                    {
                        "orgname": "Universidade Federal de Minas Gerais",
                        "orgdiv1": "Faculdade de Medicina",
                        "orgdiv2": "",
                        "original": "Grupo de Pesquisas em Epidemiologia e Avaliação em Saúde. Faculdade de Medicina. Universidade Federal de Minas Gerais. Belo Horizonte, MG, Brasil",
                    }
                ],
                "city": "Belo Horizonte",
                "state": "MG",
                "country": [{"code": "", "name": "Brasil"}],
                "email": "",
            },
            {
                "id": "aff3",
                "label": "III",
                "institution": [
                    {
                        "orgname": "Fundação Oswaldo Cruz",
                        "orgdiv1": "Escola Nacional de Saúde Pública Sergio Arouca",
                        "orgdiv2": "Departamento de Ciências Sociais",
                        "original": "Departamento de Ciências Sociais. Escola Nacional de Saúde Pública Sergio Arouca. Fundação Oswaldo Cruz. Rio de Janeiro, RJ, Brasil",
                    }
                ],
                "city": "Rio de Janeiro",
                "state": "RJ",
                "country": [{"code": "", "name": "Brasil"}],
                "email": "",
            },
            {
                "id": "aff4",
                "label": "IV",
                "institution": [
                    {
                        "orgname": "Universidade Federal de Minas Gerais",
                        "orgdiv1": "Faculdade de Farmácia",
                        "orgdiv2": "Departamento de Farmácia Social",
                        "original": "Departamento de Farmácia Social. Faculdade de Farmácia. Universidade Federal de Minas Gerais. Belo Horizonte, MG, Brasil",
                    }
                ],
                "city": "Belo Horizonte",
                "state": "MG",
                "country": [{"code": "", "name": "Brasil"}],
                "email": "",
            },
            {
                "id": "aff5",
                "label": "V",
                "institution": [
                    {
                        "orgname": "Universidade Federal do Ceará",
                        "orgdiv1": "Faculdade de Medicina",
                        "orgdiv2": "Departamento de Saúde Comunitária",
                        "original": "Departamento de Saúde Comunitária. Faculdade de Medicina. Universidade Federal do Ceará. Fortaleza, CE, Brasil",
                    }
                ],
                "city": "Fortaleza",
                "state": "CE",
                "country": [{"code": "", "name": "Brasil"}],
                "email": "",
            },
        ]
        self.assertEqual(data, expected_output)

    def test_get_affiliation_dict(self):
        xml = """
        <article>
            <front>
                <article-meta>
                    <aff id="aff1">
                        <label>I</label>
                        <institution content-type="orgname">Secretaria <italic>Municipal</italic> de Saúde de Belo Horizonte</institution>
                        <addr-line>
                            <named-content content-type="city"><bold>Belo Horizonte</bold></named-content>
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
                            <named-content content-type="city"><italic>Belo Horizonte</italic></named-content>
                            <named-content content-type="state">MG</named-content>
                        </addr-line>
                        <country>Brasil</country>
                        <institution content-type="original">Grupo de Pesquisas em Epidemiologia e Avaliação em Saúde. Faculdade de Medicina. Universidade Federal de Minas Gerais. Belo Horizonte, MG, Brasil</institution>
                    </aff>
                </article-meta>
                <front-stub>
                <aff id="aff3">
                    <label>III</label>
                    <institution content-type="orgdiv2"><italic>Departamento de Ciências Sociais</italic></institution>
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
                    <institution content-type="orgname"><bold>Universidade Federal de Minas Gerais</bold></institution>
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
                        <named-content content-type="city"><italic>Fortaleza</italic></named-content>
                        <named-content content-type="state">CE</named-content>
                    </addr-line>
                    <country>Brasil</country>
                    <institution content-type="original">Departamento de Saúde Comunitária. Faculdade de Medicina. Universidade Federal do Ceará. Fortaleza, CE, Brasil</institution>
                </aff>
            </contrib-group>
            </front>
        </article>
        """

        xml = etree.fromstring(xml)
        data = AffiliationExtractor(xml).get_affiliation_dict(subtag=True)

        expected_output = {
            "aff1": {
                "id": "aff1",
                "label": "I",
                "institution": [
                    {
                        "orgname": "Secretaria <italic>Municipal</italic> de Saúde de Belo Horizonte",
                        "orgdiv1": "",
                        "orgdiv2": "",
                        "original": "Secretaria Municipal de Saúde de Belo Horizonte. Belo Horizonte, MG, Brasil",
                    }
                ],
                "city": "<bold>Belo Horizonte</bold>",
                "state": "MG",
                "country": [{"code": "", "name": "Brasil"}],
                "email": "",
            },
            "aff2": {
                "id": "aff2",
                "label": "II",
                "institution": [
                    {
                        "orgname": "Universidade Federal de Minas Gerais",
                        "orgdiv1": "Faculdade de Medicina",
                        "orgdiv2": "",
                        "original": "Grupo de Pesquisas em Epidemiologia e Avaliação em Saúde. Faculdade de Medicina. Universidade Federal de Minas Gerais. Belo Horizonte, MG, Brasil",
                    }
                ],
                "city": "<italic>Belo Horizonte</italic>",
                "state": "MG",
                "country": [{"code": "", "name": "Brasil"}],
                "email": "",
            },
            "aff3": {
                "id": "aff3",
                "label": "III",
                "institution": [
                    {
                        "orgname": "Fundação Oswaldo Cruz",
                        "orgdiv1": "Escola Nacional de Saúde Pública Sergio Arouca",
                        "orgdiv2": "<italic>Departamento de Ciências Sociais</italic>",
                        "original": "Departamento de Ciências Sociais. Escola Nacional de Saúde Pública Sergio Arouca. Fundação Oswaldo Cruz. Rio de Janeiro, RJ, Brasil",
                    }
                ],
                "city": "Rio de Janeiro",
                "state": "RJ",
                "country": [{"code": "", "name": "Brasil"}],
                "email": "",
            },
            "aff4": {
                "id": "aff4",
                "label": "IV",
                "institution": [
                    {
                        "orgname": "<bold>Universidade Federal de Minas Gerais</bold>",
                        "orgdiv1": "Faculdade de Farmácia",
                        "orgdiv2": "Departamento de Farmácia Social",
                        "original": "Departamento de Farmácia Social. Faculdade de Farmácia. Universidade Federal de Minas Gerais. Belo Horizonte, MG, Brasil",
                    }
                ],
                "city": "Belo Horizonte",
                "state": "MG",
                "country": [{"code": "", "name": "Brasil"}],
                "email": "",
            },
            "aff5": {
                "id": "aff5",
                "label": "V",
                "institution": [
                    {
                        "orgname": "Universidade Federal do Ceará",
                        "orgdiv1": "Faculdade de Medicina",
                        "orgdiv2": "Departamento de Saúde Comunitária",
                        "original": "Departamento de Saúde Comunitária. Faculdade de Medicina. Universidade Federal do Ceará. Fortaleza, CE, Brasil",
                    }
                ],
                "city": "<italic>Fortaleza</italic>",
                "state": "CE",
                "country": [{"code": "", "name": "Brasil"}],
                "email": "",
            },
        }
        self.assertEqual(data, expected_output)


class AffiliationTest(TestCase):
    def test_extract_affiliation_list_only_from_article_meta(self):
        xml = """
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
        """

        xml = etree.fromstring(xml)
        data = list(Affiliation(xml).affiliation_list)

        expected_output = [
            {
                "id": "aff1",
                "label": "I",
                "normalized": None,
                "orgname": "Secretaria Municipal de Saúde de Belo Horizonte",
                "orgdiv1": None,
                "orgdiv2": None,
                "original": "Secretaria Municipal de Saúde de Belo Horizonte. Belo Horizonte, MG, Brasil",
                "city": "Belo Horizonte",
                "state": "MG",
                "country_code": None,
                "country_name": "Brasil",
                "email": None,
                "parent": "article",
                "parent_article_type": None,
                "parent_id": None,
                "parent_lang": None,
            },
            {
                "id": "aff2",
                "label": "II",
                "city": "Belo Horizonte",
                "state": "MG",
                "country_code": None,
                "country_name": "Brasil",
                "normalized": None,
                "orgname": "Universidade Federal de Minas Gerais",
                "orgdiv1": "Faculdade de Medicina",
                "orgdiv2": None,
                "original": "Grupo de Pesquisas em Epidemiologia e Avaliação em Saúde. Faculdade de Medicina. Universidade Federal de Minas Gerais. Belo Horizonte, MG, Brasil",
                "email": None,
                "parent": "article",
                "parent_article_type": None,
                "parent_id": None,
                "parent_lang": None,
            },
            {
                "id": "aff3",
                "label": "III",
                "normalized": None,
                "orgname": "Fundação Oswaldo Cruz",
                "orgdiv1": "Escola Nacional de Saúde Pública Sergio Arouca",
                "orgdiv2": "Departamento de Ciências Sociais",
                "original": "Departamento de Ciências Sociais. Escola Nacional de Saúde Pública Sergio Arouca. Fundação Oswaldo Cruz. Rio de Janeiro, RJ, Brasil",
                "city": "Rio de Janeiro",
                "state": "RJ",
                "country_code": None,
                "country_name": "Brasil",
                "email": None,
                "parent": "article",
                "parent_article_type": None,
                "parent_id": None,
                "parent_lang": None,
            },
            {
                "id": "aff4",
                "label": "IV",
                "normalized": None,
                "orgname": "Universidade Federal de Minas Gerais",
                "orgdiv1": "Faculdade de Farmácia",
                "orgdiv2": "Departamento de Farmácia Social",
                "original": "Departamento de Farmácia Social. Faculdade de Farmácia. Universidade Federal de Minas Gerais. Belo Horizonte, MG, Brasil",
                "city": "Belo Horizonte",
                "state": "MG",
                "country_code": None,
                "country_name": "Brasil",
                "email": None,
                "parent": "article",
                "parent_article_type": None,
                "parent_id": None,
                "parent_lang": None,
            },
            {
                "id": "aff5",
                "label": "V",
                "normalized": None,
                "orgname": "Universidade Federal do Ceará",
                "orgdiv1": "Faculdade de Medicina",
                "orgdiv2": "Departamento de Saúde Comunitária",
                "original": "Departamento de Saúde Comunitária. Faculdade de Medicina. Universidade Federal do Ceará. Fortaleza, CE, Brasil",
                "city": "Fortaleza",
                "state": "CE",
                "country_code": None,
                "country_name": "Brasil",
                "email": None,
                "parent": "article",
                "parent_article_type": None,
                "parent_id": None,
                "parent_lang": None,
            },
        ]

        self.assertEqual(5, len(data))
        for i, item in enumerate(data):
            with self.subTest(i):
                self.assertDictEqual(item, expected_output[i])

    def test_extract_affiliation_by_id_only_from_article_meta(self):
        xml = """
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
                        <institution content-type="normalized">Universidade Estadual do Oeste do Paraná</institution>
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
        """

        xml = etree.fromstring(xml)
        data = Affiliation(xml).affiliation_by_id

        expected_output = {
            "aff1": {
                "id": "aff1",
                "label": "I",
                "normalized": None,
                "orgname": "Secretaria Municipal de Saúde de Belo Horizonte",
                "orgdiv1": None,
                "orgdiv2": None,
                "original": "Secretaria Municipal de Saúde de Belo Horizonte. Belo Horizonte, MG, Brasil",
                "city": "Belo Horizonte",
                "state": "MG",
                "country_code": None,
                "country_name": "Brasil",
                "email": None,
                "parent": "article",
                "parent_article_type": None,
                "parent_id": None,
                "parent_lang": None,
            },
            "aff2": {
                "id": "aff2",
                "label": "II",
                "city": "Belo Horizonte",
                "state": "MG",
                "country_code": None,
                "country_name": "Brasil",
                "normalized": "Universidade Estadual do Oeste do Paraná",
                "orgname": "Universidade Federal de Minas Gerais",
                "orgdiv1": "Faculdade de Medicina",
                "orgdiv2": None,
                "original": "Grupo de Pesquisas em Epidemiologia e Avaliação em Saúde. Faculdade de Medicina. Universidade Federal de Minas Gerais. Belo Horizonte, MG, Brasil",
                "email": None,
                "parent": "article",
                "parent_article_type": None,
                "parent_id": None,
                "parent_lang": None,
            },
            "aff3": {
                "id": "aff3",
                "label": "III",
                "normalized": None,
                "orgname": "Fundação Oswaldo Cruz",
                "orgdiv1": "Escola Nacional de Saúde Pública Sergio Arouca",
                "orgdiv2": "Departamento de Ciências Sociais",
                "original": "Departamento de Ciências Sociais. Escola Nacional de Saúde Pública Sergio Arouca. Fundação Oswaldo Cruz. Rio de Janeiro, RJ, Brasil",
                "city": "Rio de Janeiro",
                "state": "RJ",
                "country_code": None,
                "country_name": "Brasil",
                "email": None,
                "parent": "article",
                "parent_article_type": None,
                "parent_id": None,
                "parent_lang": None,
            },
            "aff4": {
                "id": "aff4",
                "label": "IV",
                "normalized": None,
                "orgname": "Universidade Federal de Minas Gerais",
                "orgdiv1": "Faculdade de Farmácia",
                "orgdiv2": "Departamento de Farmácia Social",
                "original": "Departamento de Farmácia Social. Faculdade de Farmácia. Universidade Federal de Minas Gerais. Belo Horizonte, MG, Brasil",
                "city": "Belo Horizonte",
                "state": "MG",
                "country_code": None,
                "country_name": "Brasil",
                "email": None,
                "parent": "article",
                "parent_article_type": None,
                "parent_id": None,
                "parent_lang": None,
            },
            "aff5": {
                "id": "aff5",
                "label": "V",
                "normalized": None,
                "orgname": "Universidade Federal do Ceará",
                "orgdiv1": "Faculdade de Medicina",
                "orgdiv2": "Departamento de Saúde Comunitária",
                "original": "Departamento de Saúde Comunitária. Faculdade de Medicina. Universidade Federal do Ceará. Fortaleza, CE, Brasil",
                "city": "Fortaleza",
                "state": "CE",
                "country_code": None,
                "country_name": "Brasil",
                "email": None,
                "parent": "article",
                "parent_article_type": None,
                "parent_id": None,
                "parent_lang": None,
            },
        }

        self.assertEqual(5, len(data))
        for k, item in data.items():
            with self.subTest(k):
                self.assertDictEqual(expected_output[k], item)
