from unittest import TestCase

from lxml import etree

from packtools.sps.models.v2.notes import Fn, FnGroup, FnGroups, AuthorNote, AuthorNotes, ArticleNotes


class FnTest(TestCase):
    def setUp(self):
        xml = (
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'dtd-version="1.0" article-type="research-article" xml:lang="pt">'
            '<front>'
            '<article-meta>'
            '<author-notes>'
            '<corresp>'
            '<label>Correspondência</label>:  Roseana Mara Aredes Priuli  Av. Juscelino Kubistcheck de Oliveira, 1220, '
            'Jardim Panorama, Condomínio Recanto Real Rua 4, 440  15021-450 São José do Rio Preto, SP, Brasil  E-mail: '
            '<email>roseanap@gmail.com</email>'
            '</corresp>'
            '<fn id="fn_01" fn-type="conflict">'
            '<bold>*</bold>'
            '<label>1</label>'
            '<p>Os autores declaram não haver conflito de interesses.</p>'
            '</fn>'
            '</author-notes>'
            '</article-meta>'
            '</front>'
            '</article>'
        )
        xmltree = etree.fromstring(xml)
        self.fn = Fn(xmltree.xpath(".//fn")[0])

    def test_id(self):
        self.assertEqual(self.fn.id, "fn_01")

    def test_type(self):
        self.assertEqual(self.fn.type, "conflict")

    def test_label(self):
        self.assertEqual(self.fn.label, "1")

    def test_text(self):
        self.assertEqual(self.fn.text, "*1Os autores declaram não haver conflito de interesses.")

    def test_has_bold(self):
        self.assertTrue(self.fn.has_bold)

    def test_fn_data(self):
        self.assertDictEqual(
            self.fn.data,
            {
                "fn_id": "fn_01",
                "fn_type": "conflict",
                "fn_label": "1",
                "fn_text": "*1Os autores declaram não haver conflito de interesses.",
                "fn_has_bold": True
            }
        )


class FnGroupTest(TestCase):
    def setUp(self):
        xml = (
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'dtd-version="1.0" article-type="research-article" xml:lang="pt">'
            '<back>'
            '<fn-group>'
            '<title>Highlights: </title>'
            '<fn fn-type="other" id="fn2">'
            '<p>Study presents design and production of an LED lamp for photovoltaic light traps.</p>'
            '</fn>'
            '<fn fn-type="other" id="fn3">'
            '<p>The LED lamp switches on and off automatically, controls the battery charge and indicates the operating status of the system.</p>'
            '</fn>'
            '<fn fn-type="other" id="fn4">'
            '<p>The LED lamp is a superior substitute for the standard fluorescent lamps used in conventional light traps.</p>'
            '</fn>'
            '</fn-group>'
            '</back>'
            '</article>'
        )
        self.xml_tree = etree.fromstring(xml)

    def test_fn_group(self):
        obtained = list(FnGroup(self.xml_tree.xpath(".//fn-group")[0]).fns)
        expected = [
            {
                'fn_id': 'fn2',
                'fn_text': 'Study presents design and production of an LED lamp for photovoltaic light traps.',
                'fn_label': None,
                'fn_type': 'other',
                'fn_parent': 'fn-group',
                'fn_has_bold': False
            },
            {
                'fn_id': 'fn3',
                'fn_text': 'The LED lamp switches on and off automatically, controls the battery charge and indicates '
                           'the operating status of the system.',
                'fn_label': None,
                'fn_type': 'other',
                'fn_parent': 'fn-group',
                'fn_has_bold': False
            },
            {
                'fn_id': 'fn4',
                'fn_text': 'The LED lamp is a superior substitute for the standard fluorescent lamps used in '
                           'conventional light traps.',
                'fn_label': None,
                'fn_type': 'other',
                'fn_parent': 'fn-group',
                'fn_has_bold': False
            }
        ]
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(item, expected[i])


class FnGroupsTest(TestCase):
    def setUp(self):
        xml = (
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'dtd-version="1.0" article-type="research-article" xml:lang="pt">'
            '<back>'
            '<fn-group>'
            '<title>Highlights: </title>'
            '<fn fn-type="other" id="fn2">'
            '<p>Study presents design and production of an LED lamp for photovoltaic light traps.</p>'
            '</fn>'
            '<fn fn-type="other" id="fn3">'
            '<p>The LED lamp switches on and off automatically, controls the battery charge and indicates the operating status of the system.</p>'
            '</fn>'
            '<fn fn-type="other" id="fn4">'
            '<p>The LED lamp is a superior substitute for the standard fluorescent lamps used in conventional light traps.</p>'
            '</fn>'
            '</fn-group>'
            '</back>'
            '</article>'
        )
        self.xml_tree = etree.fromstring(xml)

    def test_fn_groups(self):
        self.maxDiff = None
        obtained = list(FnGroups(self.xml_tree.find(".")).items)
        expected = [
            {
                'parent': 'article',
                'parent_article_type': 'research-article',
                'parent_id': None,
                'parent_lang': 'pt',
                'label': None,
                'title': 'Highlights: ',
                'fns': [
                    {
                        'fn_id': 'fn2',
                        'fn_text': 'Study presents design and production of an LED lamp for photovoltaic light traps.',
                        'fn_label': None,
                        'fn_type': 'other',
                        'fn_parent': 'fn-group',
                        'fn_has_bold': False
                    },
                    {
                        'fn_id': 'fn3',
                        'fn_text': 'The LED lamp switches on and off automatically, controls the battery charge and indicates '
                                   'the operating status of the system.',
                        'fn_label': None,
                        'fn_type': 'other',
                        'fn_parent': 'fn-group',
                        'fn_has_bold': False
                    },
                    {
                        'fn_id': 'fn4',
                        'fn_text': 'The LED lamp is a superior substitute for the standard fluorescent lamps used in '
                                   'conventional light traps.',
                        'fn_label': None,
                        'fn_type': 'other',
                        'fn_parent': 'fn-group',
                        'fn_has_bold': False
                    }
                ]
            }
        ]
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(item, expected[i])


class AuthorNoteTest(TestCase):
    def setUp(self):
        xml = (
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'dtd-version="1.0" article-type="research-article" xml:lang="pt">'
            '<front>'
            '<article-meta>'
            '<author-notes>'
            '<corresp>'
            '<label>Correspondência</label>:  Roseana Mara Aredes Priuli  Av. Juscelino Kubistcheck de Oliveira, 1220, '
            'Jardim Panorama, Condomínio Recanto Real Rua 4, 440  15021-450 São José do Rio Preto, SP, Brasil  E-mail: '
            '<email>roseanap@gmail.com</email>'
            '</corresp>'
            '<fn id="fn_01" fn-type="conflict">'
            '<label>1</label>'
            '<p>Os autores declaram não haver conflito de interesses.</p>'
            '</fn>'
            '</author-notes>'
            '</article-meta>'
            '</front>'
            '</article>'
        )
        self.xml_tree = etree.fromstring(xml)

    def test_author_note(self):
        obtained = list(AuthorNote(self.xml_tree.xpath(".//author-notes")[0]).fns)
        expected = [
            {
                'fn_id': 'fn_01',
                'fn_label': '1',
                'fn_parent': 'author-notes',
                'fn_text': '1Os autores declaram não haver conflito de interesses.',
                'fn_type': 'conflict',
                'fn_has_bold': False
            }
        ]
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(item, expected[i])


class AuthorNotesTest(TestCase):
    def setUp(self):
        xml = (
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'dtd-version="1.0" article-type="research-article" xml:lang="pt">'
            '<front>'
            '<article-meta>'
            '<author-notes>'
            '<corresp>'
            '<label>Correspondência</label>:  Roseana Mara Aredes Priuli  Av. Juscelino Kubistcheck de Oliveira, 1220, '
            'Jardim Panorama, Condomínio Recanto Real Rua 4, 440  15021-450 São José do Rio Preto, SP, Brasil  E-mail: '
            '<email>roseanap@gmail.com</email>'
            '</corresp>'
            '<fn id="fn_01" fn-type="conflict">'
            '<label>1</label>'
            '<p>Os autores declaram não haver conflito de interesses.</p>'
            '</fn>'
            '</author-notes>'
            '<author-notes>'
            '<corresp id="c01">'
            '<label>*</label>'
            '<bold>Correspondence</bold>: Dr. Edmundo Figueira Departamento de Fisioterapia,'
            'Universidade FISP - Hogwarts,'
            '</corresp>'
            'Brasil. E-mail: <email>contato@foo.com</email><fn fn-type="coi-statement">'
            '<p>Não há conflito de interesse entre os autores do artigo.</p>'
            '</fn>'
            '<fn fn-type="equal">'
            '<p>Todos os autores tiveram contribuição igualitária na criação do artigo.</p>'
            '</fn>'
            '</author-notes>'
            '</article-meta>'
            '</front>'
            '</article>'
        )
        self.xml_tree = etree.fromstring(xml)

    def test_author_notes(self):
        self.maxDiff = None
        obtained = list(AuthorNotes(self.xml_tree.find(".")).items)
        expected = [
            {
                'parent': 'article',
                'parent_article_type': 'research-article',
                'parent_id': None,
                'parent_lang': 'pt',
                'corresp': 'Correspondência: Roseana Mara Aredes Priuli Av. Juscelino '
                           'Kubistcheck de Oliveira, 1220, Jardim Panorama, Condomínio '
                           'Recanto Real Rua 4, 440 15021-450 São José do Rio Preto, SP, '
                           'Brasil E-mail: roseanap@gmail.com',
                'corresp_label': 'Correspondência',
                'fns': [
                    {
                        'fn_id': 'fn_01',
                        'fn_label': '1',
                        'fn_parent': 'author-notes',
                        'fn_text': '1Os autores declaram não haver conflito de interesses.',
                        'fn_type': 'conflict',
                        'fn_has_bold': False
                    },
                ]
            },
            {
                'parent': 'article',
                'parent_article_type': 'research-article',
                'parent_id': None,
                'parent_lang': 'pt',
                'corresp': '*Correspondence: Dr. Edmundo Figueira Departamento de '
                           'Fisioterapia,Universidade FISP - Hogwarts,',
                'corresp_label': '*',
                'fns': [
                    {
                        'fn_id': None,
                        'fn_label': None,
                        'fn_parent': 'author-notes',
                        'fn_text': 'Não há conflito de interesse entre os autores do artigo.',
                        'fn_type': 'coi-statement',
                        'fn_has_bold': False
                    },
                    {
                        'fn_id': None,
                        'fn_label': None,
                        'fn_parent': 'author-notes',
                        'fn_text': 'Todos os autores tiveram contribuição igualitária na criação do artigo.',
                        'fn_type': 'equal',
                        'fn_has_bold': False
                    }
                ]
            }
        ]
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(item, expected[i])


class ArticleNotesTest(TestCase):
    def setUp(self):
        xml = (
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'dtd-version="1.0" article-type="research-article" xml:lang="pt">'
            '<front>'
            '<article-meta>'
            '<author-notes>'
            '<corresp>'
            '<label>Correspondência</label>:  Roseana Mara Aredes Priuli  Av. Juscelino Kubistcheck de Oliveira, 1220, '
            'Jardim Panorama, Condomínio Recanto Real Rua 4, 440  15021-450 São José do Rio Preto, SP, Brasil  E-mail: '
            '<email>roseanap@gmail.com</email>'
            '</corresp>'
            '<fn id="fn_01" fn-type="conflict">'
            '<label>1</label>'
            '<p>Os autores declaram não haver conflito de interesses.</p>'
            '</fn>'
            '</author-notes>'
            '<author-notes>'
            '<corresp id="c01">'
            '<label>*</label>'
            '<bold>Correspondence</bold>: Dr. Edmundo Figueira Departamento de Fisioterapia,'
            'Universidade FISP - Hogwarts,'
            '</corresp>'
            'Brasil. E-mail: <email>contato@foo.com</email><fn fn-type="coi-statement">'
            '<p>Não há conflito de interesse entre os autores do artigo.</p>'
            '</fn>'
            '<fn fn-type="equal">'
            '<p>Todos os autores tiveram contribuição igualitária na criação do artigo.</p>'
            '</fn>'
            '</author-notes>'
            '</article-meta>'
            '</front>'
            '<back>'
            '<fn-group>'
            '<title>Highlights: </title>'
            '<fn fn-type="other" id="fn2">'
            '<bold>A)</bold>'
            '<p>Study presents design and production of an LED lamp for photovoltaic light traps.</p>'
            '</fn>'
            '<fn fn-type="other" id="fn3">'
            '<p>The LED lamp switches on and off automatically, controls the battery charge and indicates the operating status of the system.</p>'
            '</fn>'
            '<fn fn-type="other" id="fn4">'
            '<p>The LED lamp is a superior substitute for the standard fluorescent lamps used in conventional light traps.</p>'
            '</fn>'
            '</fn-group>'
            '</back>'
            '</article>'
        )
        self.xml_tree = etree.fromstring(xml)

    def test_all_notes(self):
        self.maxDiff = None
        obtained = list(ArticleNotes(self.xml_tree).all_notes())
        expected = [
            {
                'parent': 'article',
                'parent_article_type': 'research-article',
                'parent_id': None,
                'parent_lang': 'pt',
                'label': None,
                'title': 'Highlights: ',
                'fns': [
                    {
                        'fn_id': 'fn2',
                        'fn_text': 'A)Study presents design and production of an LED lamp for photovoltaic light traps.',
                        'fn_label': None,
                        'fn_type': 'other',
                        'fn_parent': 'fn-group',
                        'fn_has_bold': True
                    },
                    {
                        'fn_id': 'fn3',
                        'fn_text': 'The LED lamp switches on and off automatically, controls the battery charge and indicates '
                                   'the operating status of the system.',
                        'fn_label': None,
                        'fn_type': 'other',
                        'fn_parent': 'fn-group',
                        'fn_has_bold': False
                    },
                    {
                        'fn_id': 'fn4',
                        'fn_text': 'The LED lamp is a superior substitute for the standard fluorescent lamps used in '
                                   'conventional light traps.',
                        'fn_label': None,
                        'fn_type': 'other',
                        'fn_parent': 'fn-group',
                        'fn_has_bold': False
                    }
                ]
            },
            {
                'parent': 'article',
                'parent_article_type': 'research-article',
                'parent_id': None,
                'parent_lang': 'pt',
                'corresp': 'Correspondência: Roseana Mara Aredes Priuli Av. Juscelino '
                           'Kubistcheck de Oliveira, 1220, Jardim Panorama, Condomínio '
                           'Recanto Real Rua 4, 440 15021-450 São José do Rio Preto, SP, '
                           'Brasil E-mail: roseanap@gmail.com',
                'corresp_label': 'Correspondência',
                'fns': [
                    {
                        'fn_id': 'fn_01',
                        'fn_label': '1',
                        'fn_parent': 'author-notes',
                        'fn_text': '1Os autores declaram não haver conflito de interesses.',
                        'fn_type': 'conflict',
                        'fn_has_bold': False
                    },
                ]
            },
            {
                'parent': 'article',
                'parent_article_type': 'research-article',
                'parent_id': None,
                'parent_lang': 'pt',
                'corresp': '*Correspondence: Dr. Edmundo Figueira Departamento de '
                           'Fisioterapia,Universidade FISP - Hogwarts,',
                'corresp_label': '*',
                'fns': [
                    {
                        'fn_id': None,
                        'fn_label': None,
                        'fn_parent': 'author-notes',
                        'fn_text': 'Não há conflito de interesse entre os autores do artigo.',
                        'fn_type': 'coi-statement',
                        'fn_has_bold': False
                    },
                    {
                        'fn_id': None,
                        'fn_label': None,
                        'fn_parent': 'author-notes',
                        'fn_text': 'Todos os autores tiveram contribuição igualitária na criação do artigo.',
                        'fn_type': 'equal',
                        'fn_has_bold': False
                    }
                ]
            }
        ]
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(item, expected[i])
