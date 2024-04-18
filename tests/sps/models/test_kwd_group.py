from unittest import TestCase
from lxml import etree as ET

from packtools.sps.utils import xml_utils

from packtools.sps.models.kwd_group import KwdGroup, KwdGroupTextNode, KwdTextNode, ArticleKeywords


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
        self.maxDiff = None
        xmltree = xml_utils.get_xml_tree('tests/samples/0034-8910-rsp-48-2-0296.xml')
        kwd_extract_kwd_with_lang_subtag = KwdGroup(xmltree).extract_kwd_data_with_lang_text(subtag=True)

        expected_output = [
            {'lang': 'en', 'text': 'Chagas Disease, transmission'},
            {'lang': 'en', 'text': 'Triatominae, <i>Trypanosoma cruzi</i>, isolation'},
            {'lang': 'en', 'text': 'Communicable Diseases, epidemiology'},
            {'lang': 'pt', 'text': 'Doença de Chagas, transmissão'},
            {'lang': 'pt', 'text': 'Triatominae, <i>Trypanosoma cruzi</i>, isolamento'},
            {'lang': 'pt', 'text': 'Doenças Transmissíveis, epidemiologia'}
        ]

        self.assertEqual(kwd_extract_kwd_with_lang_subtag, expected_output)

    def test_extract_kwd_data_without_lang_subtag(self):
        xmltree = xml_utils.get_xml_tree('tests/samples/0034-8910-rsp-48-2-0296.xml')
        kwd_extract_kwd_without_subtag = KwdGroup(xmltree).extract_kwd_data_with_lang_text(subtag=False)

        expected_output = [
            {'lang': 'en', 'text': 'Chagas Disease, transmission'},
            {'lang': 'en', 'text': 'Triatominae, Trypanosoma cruzi , isolation'},
            {'lang': 'en', 'text': 'Communicable Diseases, epidemiology'},
            {'lang': 'pt', 'text': 'Doença de Chagas, transmissão'},
            {'lang': 'pt', 'text': 'Triatominae, Trypanosoma cruzi , isolamento'},
            {'lang': 'pt', 'text': 'Doenças Transmissíveis, epidemiologia'}
        ]

        self.assertEqual(kwd_extract_kwd_without_subtag, expected_output)

    def test_extract_kwd_data_by_lang_with_subtag(self):
        xmltree = xml_utils.get_xml_tree('tests/samples/0034-8910-rsp-48-2-0296.xml')
        kwd_extract_kwd_with_subtag = KwdGroup(xmltree).extract_kwd_extract_data_by_lang(subtag=True)

        expected_output = {
            'en': [
                'Chagas Disease, transmission',
                'Triatominae, <i>Trypanosoma cruzi</i>, isolation',
                'Communicable Diseases, epidemiology'
            ],
            'pt': [
                'Doença de Chagas, transmissão',
                'Triatominae, <i>Trypanosoma cruzi</i>, isolamento',
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
                'Triatominae, Trypanosoma cruzi , isolation',
                'Communicable Diseases, epidemiology'
            ],
            'pt': [
                'Doença de Chagas, transmissão',
                'Triatominae, Trypanosoma cruzi , isolamento',
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
            {'parent_name': 'article', 'lang': 'pt',
             'text': ['Enfermagem', 'Idoso de 80 Anos ou Mais', 'Relações Familiares']},
            {'parent_name': 'article', 'lang': 'es',
             'text': ['Enfermería', 'Anciano de 80 Años o Más', 'Relaciones Familiares']},
            {'parent_name': 'sub-article', 'id': 'SA1', 'lang': 'en',
             'text': ['Nursing', 'Aged, 80 Years or More', 'Family Relationships']}
        ]

        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)


class KwdGroupWithStyleTest(TestCase):
    def setUp(self):
        self.xmltree = ET.fromstring(
            """
            <article 
            article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
            <front>
            <article-meta>
            <kwd-group xml:lang="pt">
                <title>PALAVRAS-CHAVE</title>
                <kwd><bold>conteúdo de bold</bold> text </kwd>
                <kwd>text <bold>conteúdo de bold</bold> text </kwd>
                <kwd>text <bold>conteúdo de bold</bold></kwd>
                <kwd>text <bold>conteúdo <italic>de</italic> bold</bold></kwd>
            </kwd-group>
            </article-meta>
            </front>
            </article>
            """)

    def test_extract_kwd_data_with_lang(self):
        self.maxDiff = None
        kwd_extract_data_with_lang_text = KwdGroup(self.xmltree).extract_kwd_data_with_lang_text(subtag=False)

        expected_output = [
            {'lang': 'pt', 'text': 'conteúdo de bold text'},
            {'lang': 'pt', 'text': 'text conteúdo de bold text'},
            {'lang': 'pt', 'text': 'text conteúdo de bold'},
            {'lang': 'pt', 'text': 'text conteúdo de bold'}
        ]

        self.assertEqual(kwd_extract_data_with_lang_text, expected_output)

    def test_extract_kwd_data_by_lang_without_key_text(self):
        self.maxDiff = None
        kwd_extract_by_lang = KwdGroup(self.xmltree).extract_kwd_extract_data_by_lang(subtag=False)

        expected_output = {
            'pt': [
                'conteúdo de bold text',
                'text conteúdo de bold text',
                'text conteúdo de bold',
                'text conteúdo de bold'
            ]
        }

        self.assertEqual(kwd_extract_by_lang, expected_output)

    def test_extract_kwd_data_with_lang_subtag(self):
        self.maxDiff = None
        kwd_extract_kwd_with_lang_subtag = KwdGroup(self.xmltree).extract_kwd_data_with_lang_text(subtag=True,
                                                                                                  tags_to_keep=['bold'])

        expected_output = [
            {'lang': 'pt', 'text': '<bold>conteúdo de bold</bold> text'},
            {'lang': 'pt', 'text': 'text <bold>conteúdo de bold</bold> text'},
            {'lang': 'pt', 'text': 'text <bold>conteúdo de bold</bold>'},
            {'lang': 'pt', 'text': 'text <bold>conteúdo <i>de</i> bold</bold>'}
        ]

        self.assertEqual(kwd_extract_kwd_with_lang_subtag, expected_output)

    def test_extract_kwd_data_without_lang_subtag(self):
        self.maxDiff = None
        kwd_extract_kwd_without_subtag = KwdGroup(self.xmltree).extract_kwd_data_with_lang_text(subtag=False)

        expected_output = [
            {'lang': 'pt', 'text': 'conteúdo de bold text'},
            {'lang': 'pt', 'text': 'text conteúdo de bold text'},
            {'lang': 'pt', 'text': 'text conteúdo de bold'},
            {'lang': 'pt', 'text': 'text conteúdo de bold'}
        ]

        self.assertEqual(kwd_extract_kwd_without_subtag, expected_output)

    def test_extract_kwd_data_by_lang_with_subtag(self):
        self.maxDiff = None
        kwd_extract_kwd_with_subtag = KwdGroup(self.xmltree).extract_kwd_extract_data_by_lang(subtag=True,
                                                                                              tags_to_keep=['bold'])

        expected_output = {
            'pt': [
                '<bold>conteúdo de bold</bold> text',
                'text <bold>conteúdo de bold</bold> text',
                'text <bold>conteúdo de bold</bold>',
                'text <bold>conteúdo <i>de</i> bold</bold>'
            ],
        }

        self.assertEqual(kwd_extract_kwd_with_subtag, expected_output)

    def test_extract_kwd_data_by_lang_without_subtag(self):
        self.maxDiff = None
        kwd_extract_kwd_with_subtag = KwdGroup(self.xmltree).extract_kwd_extract_data_by_lang(subtag=False)

        expected_output = {
            'pt': [
                'conteúdo de bold text',
                'text conteúdo de bold text',
                'text conteúdo de bold',
                'text conteúdo de bold'
            ],
        }

        self.assertEqual(kwd_extract_kwd_with_subtag, expected_output)

    def test_extract_kwd_data_with_lang_text_kwd_group_without_lang(self):
        self.maxDiff = None
        kwd_extract_data_with_lang_text = KwdGroup(self.xmltree).extract_kwd_data_with_lang_text(subtag=False)

        expected_output = [
            {'lang': 'pt', 'text': 'conteúdo de bold text'},
            {'lang': 'pt', 'text': 'text conteúdo de bold text'},
            {'lang': 'pt', 'text': 'text conteúdo de bold'},
            {'lang': 'pt', 'text': 'text conteúdo de bold'}
        ]

        self.assertEqual(expected_output, kwd_extract_data_with_lang_text)

    def test_extract_kwd_extract_data_by_lang_kwd_group_without_lang(self):
        self.maxDiff = None
        kwd_extract_data_with_lang_text = KwdGroup(self.xmltree).extract_kwd_extract_data_by_lang(subtag=False)

        expected_output = {
            'pt': [
                'conteúdo de bold text',
                'text conteúdo de bold text',
                'text conteúdo de bold',
                'text conteúdo de bold'
            ],
        }

        self.assertEqual(expected_output, kwd_extract_data_with_lang_text)

    def test_extract_kwd_data_with_lang_text_by_article_type(self):
        self.maxDiff = None
        obtained = KwdGroup(self.xmltree).extract_kwd_data_with_lang_text_by_article_type(subtag=False)

        expected = [
            {
                'parent_name': 'article', 'lang': 'pt',
                'text': [
                    'conteúdo de bold text',
                    'text conteúdo de bold text',
                    'text conteúdo de bold',
                    'text conteúdo de bold'
                ]
            },
        ]

        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

    def test_extract_kwd_data_with_lang_html_format(self):
        self.maxDiff = None
        kwd_extract_kwd_with_subtag = list(KwdGroup(self.xmltree).extract_kwd_data_with_lang_html_format(
            tags_to_convert_to_html={'bold': 'b'}
        ))

        expected_output = [
            {
                'parent_name': 'article',
                'lang': 'pt',
                'plain_text': [
                    'conteúdo de bold text',
                    'text conteúdo de bold text',
                    'text conteúdo de bold',
                    'text conteúdo de bold'
                ],
                'html_text': [
                    '<b>conteúdo de bold</b> text',
                    'text <b>conteúdo de bold</b> text',
                    'text <b>conteúdo de bold</b>',
                    'text <b>conteúdo <i>de</i> bold</b>'
                ]
            }
        ]

        self.assertEqual(kwd_extract_kwd_with_subtag, expected_output)


class KwdGroupTextNodeTest(TestCase):

    def test_kwd_plain_text(self):
        self.maxDiff = None
        self.xmltree = ET.fromstring("<kwd><bold>conteúdo de bold</bold> text </kwd>")

        kwd_text_node = KwdTextNode(self.xmltree, 'pt')
        kwd_text_node.configure(tags_to_convert_to_html={'bold': 'b'})
        obtained = kwd_text_node.plain_text
        expected = 'conteúdo de bold text'
        self.assertEqual(obtained, expected)

    def test_kwd_html_text(self):
        self.maxDiff = None
        self.xmltree = ET.fromstring("<kwd><bold>conteúdo de bold</bold> text </kwd>")

        kwd_text_node = KwdTextNode(self.xmltree, 'pt')
        kwd_text_node.configure(tags_to_convert_to_html={'bold': 'b'})
        obtained = kwd_text_node.html_text
        expected = '<b>conteúdo de bold</b> text'
        self.assertEqual(obtained, expected)

    def test_kwd_item(self):
        self.maxDiff = None
        self.xmltree = ET.fromstring("<kwd><bold>conteúdo de bold</bold> text </kwd>")

        kwd_text_node = KwdTextNode(self.xmltree, 'pt')
        kwd_text_node.configure(tags_to_convert_to_html={'bold': 'b'})
        obtained = kwd_text_node.item
        expected = {
            'lang': 'pt',
            'plain_text': 'conteúdo de bold text',
            'html_text': '<b>conteúdo de bold</b> text'
        }
        self.assertEqual(obtained, expected)

    def test_kwd_text_node_items(self):
        self.maxDiff = None
        self.xmltree = ET.fromstring(
                '<kwd-group xml:lang="pt">'
                '<kwd><bold>conteúdo de bold</bold> text </kwd>'
                '<kwd>text <bold>conteúdo de bold</bold> text </kwd>'
                '<kwd>text <bold>conteúdo de bold</bold></kwd>'
                '<kwd>text <bold>conteúdo <italic>de</italic> bold</bold></kwd>'
                '</kwd-group>'
        )

        kwd_group_text_node = KwdGroupTextNode(self.xmltree, 'pt')
        kwd_group_text_node.configure(tags_to_convert_to_html={'bold': 'b'})
        obtained = list(kwd_group_text_node.items)
        expected = [
            {
                'lang': 'pt',
                'plain_text': 'conteúdo de bold text',
                'html_text': '<b>conteúdo de bold</b> text'
            },
            {
                'lang': 'pt',
                'plain_text': 'text conteúdo de bold text',
                'html_text': 'text <b>conteúdo de bold</b> text'
            },
            {
                'lang': 'pt',
                'plain_text': 'text conteúdo de bold',
                'html_text': 'text <b>conteúdo de bold</b>'
            },
            {
                'lang': 'pt',
                'plain_text': 'text conteúdo de bold',
                'html_text': 'text <b>conteúdo <i>de</i> bold</b>'
            }
        ]
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

    def test_kwd_text_node_items_by_lang(self):
        self.maxDiff = None
        self.xmltree = ET.fromstring(
                '<kwd-group xml:lang="pt">'
                '<kwd><bold>conteúdo de bold</bold> text </kwd>'
                '<kwd>text <bold>conteúdo de bold</bold> text </kwd>'
                '</kwd-group>'
        )

        kwd_group_text_node = KwdGroupTextNode(self.xmltree, 'pt')
        kwd_group_text_node.configure(tags_to_convert_to_html={'bold': 'b'})
        obtained = kwd_group_text_node.items_by_lang
        expected = {
            'pt': [
                {
                    'lang': 'pt',
                    'plain_text': 'conteúdo de bold text',
                    'html_text': '<b>conteúdo de bold</b> text'
                },
                {
                    'lang': 'pt',
                    'plain_text': 'text conteúdo de bold text',
                    'html_text': 'text <b>conteúdo de bold</b> text'
                }
            ]
        }
        self.assertDictEqual(expected, obtained)

    def test_article_keywords_items(self):
        self.maxDiff = None
        self.xmltree = ET.fromstring(
            """
            <article 
            article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="pt">
            <front>
            <article-meta>
            <kwd-group xml:lang="pt">
                <kwd><bold>conteúdo de bold</bold> text </kwd>
                <kwd>text <bold>conteúdo de bold</bold> text </kwd>
            </kwd-group>
            </article-meta>
            </front>
            <sub-article article-type="translation" id="TRen" xml:lang="en">
            <front-stub>
            <kwd-group>
                <kwd>text <bold>conteúdo de bold</bold></kwd>
                <kwd>text <bold>conteúdo <italic>de</italic> bold</bold></kwd>
            </kwd-group>
            </front-stub>
            </sub-article>
            </article>
            """
        )

        article_keywords = ArticleKeywords(self.xmltree)
        article_keywords.configure(tags_to_convert_to_html={'bold': 'b'})
        obtained = list(article_keywords.items)
        expected = [
            {
                'id': None,
                'parent_name': 'article',
                'lang': 'pt',
                'plain_text': 'conteúdo de bold text',
                'html_text': '<b>conteúdo de bold</b> text'
            },
            {
                'id': None,
                'parent_name': 'article',
                'lang': 'pt',
                'plain_text': 'text conteúdo de bold text',
                'html_text': 'text <b>conteúdo de bold</b> text'
            },
            {
                'id': 'TRen',
                'parent_name': 'sub-article',
                'lang': 'en',
                'plain_text': 'text conteúdo de bold',
                'html_text': 'text <b>conteúdo de bold</b>'
            },
            {
                'id': 'TRen',
                'parent_name': 'sub-article',
                'lang': 'en',
                'plain_text': 'text conteúdo de bold',
                'html_text': 'text <b>conteúdo <i>de</i> bold</b>'
            }
        ]
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

    def test_article_keywords_items_by_lang(self):
        self.maxDiff = None
        self.xmltree = ET.fromstring(
            """
            <article 
            article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="pt">
            <front>
            <article-meta>
            <kwd-group xml:lang="pt">
                <kwd><bold>conteúdo de bold</bold> text </kwd>
                <kwd>text <bold>conteúdo de bold</bold> text </kwd>
            </kwd-group>
            </article-meta>
            </front>
            <sub-article article-type="translation" id="TRen" xml:lang="en">
            <front-stub>
            <kwd-group>
                <kwd>text <bold>conteúdo de bold</bold></kwd>
                <kwd>text <bold>conteúdo <italic>de</italic> bold</bold></kwd>
            </kwd-group>
            </front-stub>
            </sub-article>
            </article>
            """
        )

        article_keywords = ArticleKeywords(self.xmltree)
        article_keywords.configure(tags_to_convert_to_html={'bold': 'b'})
        obtained = article_keywords.items_by_lang
        expected = {
            'pt': [
                {
                    'id': None,
                    'parent_name': 'article',
                    'lang': 'pt',
                    'plain_text': 'conteúdo de bold text',
                    'html_text': '<b>conteúdo de bold</b> text'
                },
                {
                    'id': None,
                    'parent_name': 'article',
                    'lang': 'pt',
                    'plain_text': 'text conteúdo de bold text',
                    'html_text': 'text <b>conteúdo de bold</b> text'
                }
            ],
            'en': [
                {
                    'id': 'TRen',
                    'parent_name': 'sub-article',
                    'lang': 'en',
                    'plain_text': 'text conteúdo de bold',
                    'html_text': 'text <b>conteúdo de bold</b>'
                },
                {
                    'id': 'TRen',
                    'parent_name': 'sub-article',
                    'lang': 'en',
                    'plain_text': 'text conteúdo de bold',
                    'html_text': 'text <b>conteúdo <i>de</i> bold</b>'
                }
            ]
        }
        self.assertDictEqual(expected, obtained)
