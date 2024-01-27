from unittest import TestCase

from packtools.sps.utils import xml_utils

from packtools.sps.models.kwd_group import KwdGroup


class KwdGroupTest(TestCase):

    def test_extract_kwd_data_with_lang(self):
        xmltree = xml_utils.get_xml_tree('tests/samples/0034-7094-rba-69-03-0227.xml')
        kwd_extract_data_with_lang_text = KwdGroup(xmltree).extract_kwd_data_with_lang_text(subtag=False)

        expected_output = [
            {'lang': 'en', 'text': 'Primary health care'},
            {'lang': 'en', 'text': 'Ambulatory care facilities'},
            {'lang': 'en', 'text': 'Chronic pain'},
            {'lang': 'en', 'text': 'Analgesia'},
            {'lang': 'en', 'text': 'Pain management'},
            {'lang': 'pt', 'text': 'Atenção primária à saúde'},
            {'lang': 'pt', 'text': 'Instituições de assistência ambulatorial'},
            {'lang': 'pt', 'text': 'Dor crônica'},
            {'lang': 'pt', 'text': 'Analgesia'},
            {'lang': 'pt', 'text': 'Tratamento da dor'}
        ]

        self.assertEqual(kwd_extract_data_with_lang_text, expected_output)

    def test_extract_kwd_data_by_lang_without_key_text(self):
        xmltree = xml_utils.get_xml_tree('tests/samples/0034-7094-rba-69-03-0227.xml')
        kwd_extract_by_lang = KwdGroup(xmltree).extract_kwd_extract_data_by_lang(subtag=False)

        expected_output = {
            'en': [
                'Primary health care',
                'Ambulatory care facilities',
                'Chronic pain',
                'Analgesia',
                'Pain management'
            ],
            'pt': [
                'Atenção primária à saúde',
                'Instituições de assistência ambulatorial',
                'Dor crônica',
                'Analgesia',
                'Tratamento da dor'
            ]
        }

        self.assertEqual(kwd_extract_by_lang, expected_output)

    def test_extract_kwd_data_with_lang_subtag(self):
        xmltree = xml_utils.get_xml_tree('tests/samples/0034-8910-rsp-48-2-0296.xml')
        kwd_extract_kwd_with_lang_subtag = KwdGroup(xmltree).extract_kwd_data_with_lang_text(subtag=True)

        expected_output = [
            {'lang': 'en', 'text': 'Chagas Disease, transmission'},
            {'lang': 'en', 'text': 'Triatominae, <italic>Trypanosoma cruzi</italic>, isolation'},
            {'lang': 'en', 'text': 'Communicable Diseases, epidemiology'},
            {'lang': 'pt', 'text': 'Doença de Chagas, transmissão'},
            {'lang': 'pt', 'text': 'Triatominae, <italic>Trypanosoma cruzi</italic>, isolamento'},
            {'lang': 'pt', 'text': 'Doenças Transmissíveis, epidemiologia'}
        ]

        self.assertEqual(kwd_extract_kwd_with_lang_subtag, expected_output)

    def test_extract_kwd_data_without_lang_subtag(self):
        xmltree = xml_utils.get_xml_tree('tests/samples/0034-8910-rsp-48-2-0296.xml')
        kwd_extract_kwd_without_subtag = KwdGroup(xmltree).extract_kwd_data_with_lang_text(subtag=False)

        expected_output = [
            {'lang': 'en', 'text': 'Chagas Disease, transmission'},
            {'lang': 'en', 'text': 'Triatominae, Trypanosoma cruzi, isolation'},
            {'lang': 'en', 'text': 'Communicable Diseases, epidemiology'},
            {'lang': 'pt', 'text': 'Doença de Chagas, transmissão'},
            {'lang': 'pt', 'text': 'Triatominae, Trypanosoma cruzi, isolamento'},
            {'lang': 'pt', 'text': 'Doenças Transmissíveis, epidemiologia'}
        ]

        self.assertEqual(kwd_extract_kwd_without_subtag, expected_output)

    def test_extract_kwd_data_by_lang_with_subtag(self):
        xmltree = xml_utils.get_xml_tree('tests/samples/0034-8910-rsp-48-2-0296.xml')
        kwd_extract_kwd_with_subtag = KwdGroup(xmltree).extract_kwd_extract_data_by_lang(subtag=True)

        expected_output = {
            'en': [
                'Chagas Disease, transmission',
                'Triatominae, <italic>Trypanosoma cruzi</italic>, isolation',
                'Communicable Diseases, epidemiology'
            ],
            'pt': [
                'Doença de Chagas, transmissão',
                'Triatominae, <italic>Trypanosoma cruzi</italic>, isolamento',
                'Doenças Transmissíveis, epidemiologia'
            ]
        }

        self.assertEqual(kwd_extract_kwd_with_subtag, expected_output)

    def test_extract_kwd_data_by_lang_without_subtag(self):
        xmltree = xml_utils.get_xml_tree('tests/samples/0034-8910-rsp-48-2-0296.xml')
        kwd_extract_kwd_with_subtag = KwdGroup(xmltree).extract_kwd_extract_data_by_lang(subtag=False)

        expected_output = {
            'en': [
                'Chagas Disease, transmission',
                'Triatominae, Trypanosoma cruzi, isolation',
                'Communicable Diseases, epidemiology'
            ],
            'pt': [
                'Doença de Chagas, transmissão',
                'Triatominae, Trypanosoma cruzi, isolamento',
                'Doenças Transmissíveis, epidemiologia'
            ]
        }

        self.assertEqual(kwd_extract_kwd_with_subtag, expected_output)

    def test_extract_kwd_data_with_lang_text_kwd_group_without_lang(self):
        self.maxDiff = None
        xmltree = xml_utils.get_xml_tree('tests/samples/example_xml_keywords_error.xml')
        kwd_extract_data_with_lang_text = KwdGroup(xmltree).extract_kwd_data_with_lang_text(subtag=False)

        expected_output = [
            {'lang': 'pt', 'text': 'Enfermagem'},
            {'lang': 'pt', 'text': 'Idoso de 80 Anos ou Mais'},
            {'lang': 'pt', 'text': 'Relações Familiares'},
            {'lang': 'es', 'text': 'Enfermería'},
            {'lang': 'es', 'text': 'Anciano de 80 Años o Más'},
            {'lang': 'es', 'text': 'Relaciones Familiares'},
            {'lang': 'en', 'text': 'Nursing'},
            {'lang': 'en', 'text': 'Aged, 80 Years or More'},
            {'lang': 'en', 'text': 'Family Relationships'}
        ]

        self.assertEqual(expected_output, kwd_extract_data_with_lang_text)

    def test_extract_kwd_extract_data_by_lang_kwd_group_without_lang(self):
        self.maxDiff = None
        xmltree = xml_utils.get_xml_tree('tests/samples/example_xml_keywords_error.xml')
        kwd_extract_data_with_lang_text = KwdGroup(xmltree).extract_kwd_extract_data_by_lang(subtag=False)

        expected_output = {
            'pt': [
                'Enfermagem',
                'Idoso de 80 Anos ou Mais',
                'Relações Familiares'
            ],
            'es': [
                'Enfermería',
                'Anciano de 80 Años o Más',
                'Relaciones Familiares'
            ],
            'en': [
                'Nursing',
                'Aged, 80 Years or More',
                'Family Relationships'
            ]
        }

        self.assertEqual(expected_output, kwd_extract_data_with_lang_text)

    def test_extract_kwd_data_with_lang_text_by_article_type(self):
        self.maxDiff = None
        xmltree = xml_utils.get_xml_tree('tests/samples/example_xml_keywords_error.xml')
        obtained = KwdGroup(xmltree).extract_kwd_data_with_lang_text_by_article_type(subtag=False)

        expected = [
            {'element_name': 'article', 'id': 'main', 'lang': 'pt',
             'text': ['Enfermagem', 'Idoso de 80 Anos ou Mais', 'Relações Familiares']},
            {'element_name': 'article', 'id': 'main', 'lang': 'es',
             'text': ['Enfermería', 'Anciano de 80 Años o Más', 'Relaciones Familiares']},
            {'element_name': 'sub-article', 'id': 'SA1', 'lang': 'en',
             'text': ['Nursing', 'Aged, 80 Years or More', 'Family Relationships']}
        ]

        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)
