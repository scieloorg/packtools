from unittest import TestCase

from packtools.sps.utils import xml_utils

from packtools.sps.models.kwd_group import KwdGroup 


def get_kwd_data_with_lang(data, subtag=False):
    xmltree = xml_utils.get_xml_tree(data)
    return KwdGroup(xmltree, subtag=subtag).extract_kwd_data_with_lang_text

def get_kwd_data_without_key_text(data, subtag=False):
    xmltree = xml_utils.get_xml_tree(data)
    return KwdGroup(xmltree, subtag=subtag).extract_kwd_extract_data_by_lang


class KwdGroupTest(TestCase):

    def test_extract_kwd_data_with_lang(self):

        # xml sem subtags em kwd
        with open('tests/samples/0034-7094-rba-69-03-0227.xml', 'r', encoding='utf-8') as f:
            data = f.read()
        
        kwd_extract_data_with_lang_text = get_kwd_data_with_lang(data)

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

    def test_extract_kwd_data_without_key_text(self):

        # xml sem subtags em kwd
        with open('tests/samples/0034-7094-rba-69-03-0227.xml', 'r', encoding='utf-8') as f:
            data = f.read()

        kwd_extract_by_lang = get_kwd_data_without_key_text(data)
        
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
       
        # xml com subtags em kwd
        with open('tests/samples/0034-8910-rsp-48-2-0296.xml', 'r', encoding='utf-8') as f:
            data = f.read()

        kwd_extract_kwd_with_lang_subtag = get_kwd_data_with_lang(data, subtag=True)

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
        
        # xml com subtags em kwd
        with open('tests/samples/0034-8910-rsp-48-2-0296.xml', 'r', encoding='utf-8') as f:
            data = f.read()

        kwd_extract_kwd_without_subtag = get_kwd_data_with_lang(data, subtag=False)

        expected_output = [
            {'lang': 'en', 'text': 'Chagas Disease, transmission'}, 
            {'lang': 'en', 'text': 'Triatominae, Trypanosoma cruzi, isolation'}, 
            {'lang': 'en', 'text': 'Communicable Diseases, epidemiology'}, 
            {'lang': 'pt', 'text': 'Doença de Chagas, transmissão'}, 
            {'lang': 'pt', 'text': 'Triatominae, Trypanosoma cruzi, isolamento'}, 
            {'lang': 'pt', 'text': 'Doenças Transmissíveis, epidemiologia'}
        ]

        self.assertEqual(kwd_extract_kwd_without_subtag, expected_output)

    def test_extract_kwd_data_with_subtag(self):
                
        # xml com subtags em kwd
        with open('tests/samples/0034-8910-rsp-48-2-0296.xml', 'r', encoding='utf-8') as f:
            data = f.read()

        kwd_extract_kwd_with_subtag = get_kwd_data_without_key_text(data, subtag=True)
        
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
    
    def test_extract_kwd_data_without_subtag(self):
                
        # xml com subtags em kwd
        with open('tests/samples/0034-8910-rsp-48-2-0296.xml', 'r', encoding='utf-8') as f:
            data = f.read()

        kwd_extract_kwd_with_subtag = get_kwd_data_without_key_text(data, subtag=False)

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