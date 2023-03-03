"""
    <kwd-group xml:lang="en">
        <title>KEYWORDS</title>
        <kwd>Primary health care</kwd>
        <kwd>Ambulatory care facilities</kwd>
        <kwd>Chronic pain</kwd>
        <kwd>Analgesia</kwd>
        <kwd>Pain management</kwd>
    </kwd-group>

    <kwd-group xml:lang="pt">
        <title>PALAVRAS-CHAVE</title>
        <kwd>Atenção primária à saúde</kwd>
        <kwd>Instituições de assistência ambulatorial</kwd>
        <kwd>Dor crônica</kwd>
        <kwd>Analgesia</kwd>
        <kwd>Tratamento da dor</kwd>
    </kwd-group>
"""

from unittest import TestCase

from packtools.sps.utils import xml_utils

from packtools.sps.models.kwd_group import KwdGroup 


class KwdGroupTest(TestCase):

    def test_extract_kwd_data_with_lang(self):
        
        with open('tests/samples/0034-7094-rba-69-03-0227.xml', 'r', encoding='utf-8') as f:
            data = f.read()

        xmltree = xml_utils.get_xml_tree(data)
        kwd_extract_data_with_lang_text = KwdGroup(xmltree).extract_kwd_data_with_lang_text

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
            {'lang': 'pt', 'text': 'Tratamento da dor'}]
        
        self.assertEqual(kwd_extract_data_with_lang_text, expected_output)


    def test_data_without_key(self):

        with open('tests/samples/0034-7094-rba-69-03-0227.xml', 'r', encoding='utf-8') as f:
            data = f.read()
       
        xmltree = xml_utils.get_xml_tree(data)
        kwd_extract_by_lang = KwdGroup(xmltree).extract_kwd_extract_data_by_lang
        
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