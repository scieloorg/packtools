"""
Capa e metadados do gerador de PDF (formats/pdf).

Migra de tests/sps/formats/old_pdf/pipeline/test_xml.py as classes de capa e
metadados: TestExtractAbstractData, TestExtractTransAbstractData,
TestExtractArticleMainLanguage, TestExtractArticleTitle, TestExtractArticleType,
TestExtractCiteAsPartOne, TestBuildFullCitation, TestBuildCslReferenceType,
TestExtractContribData, TestExtractDOI, TestExtractFooterData,
TestExtractJournalTitle e TestExtractKeywordsData.

O old_pdf tinha uma função por campo (extract_abstract_data, extract_doi...)
que devolvia texto achatado; aqui o mesmo comportamento é verificado em
``meta`` e nos blocos de ``front`` de extract_article (e, quando o teste antigo
pedia o nó, no DOCX gerado ou na própria nota).

Diferenças intencionais gerais em relação ao old_pdf:
- campos ausentes viram texto vazio em ``meta`` em vez de None ou
  AttributeError;
- cada ``<p>`` do resumo é um parágrafo próprio (o old_pdf juntava tudo
  numa string separada por espaço);
- o idioma é sempre ``xml:lang`` (não há parâmetro de namespaces).
"""

import unittest
from unittest import mock

from packtools.sps.formats.pdf.extract import citation
from packtools.sps.formats.pdf.extract.languages import document_for
from packtools.sps.formats.pdf.render.front import journal_title_two_lines, vol_issue_year

from .helpers import NS, article, article_xml, docx, summary, xml


def front(meta_xml, **kwargs):
    """Blocos da capa sem o parágrafo de categoria (sempre presente por causa do article-type)."""
    return [b for b in article(article_xml(front=meta_xml, **kwargs))['front']
            if b.get('role') != 'article_category']


def meta(meta_xml='', **kwargs):
    """``meta`` do artigo mínimo com ``meta_xml`` no article-meta."""
    return article(article_xml(front=meta_xml, **kwargs))['meta']


def all_text(container):
    """Texto dos parágrafos de um cabeçalho/rodapé, inclusive dentro de tabelas."""
    out = [p.text for p in container.paragraphs]
    for table in container.tables:
        for row in table.rows:
            for cell in row.cells:
                out += [p.text for p in cell.paragraphs]
    return out


def with_journal(journal_meta, article_meta='', lang='en', article_type=None, back=''):
    """Artigo com ``<journal-meta>`` próprio (helpers.article_xml fixa o título "Revista")."""
    type_attr = f' article-type="{article_type}"' if article_type is not None else ''
    return xml(
        f'<article {NS} xml:lang="{lang}"{type_attr}><front><journal-meta>{journal_meta}</journal-meta>'
        f'<article-meta>{article_meta}</article-meta></front>'
        + (f'<body><p>x</p></body><back>{back}</back>' if back else '')
        + '</article>'
    )


# -----------------
# <abstract> e <trans-abstract>
# -----------------


class AbstractTest(unittest.TestCase):
    def test_abstract_title_and_one_paragraph_per_p(self):
        """
        old: TestExtractAbstractData.test_extract_abstract_data_with_title_and_content

        Diferença intencional: cada <p> é um parágrafo (o old_pdf juntava em
        'First paragraph. Second paragraph.').
        """
        blocks = front('<abstract><title>Abstract Title</title>'
                       '<p>First paragraph.</p><p>Second paragraph.</p></abstract>')
        self.assertEqual(summary(blocks), [
            ('abstract_title', 'Abstract Title'),
            ('abstract', 'First paragraph.'),
            ('abstract', 'Second paragraph.'),
        ])

    def test_abstract_partial_or_missing(self):
        """
        old: TestExtractAbstractData.test_extract_abstract_data_with_title_only
        old: TestExtractAbstractData.test_extract_abstract_data_with_content_only
        old: TestExtractAbstractData.test_extract_abstract_data_empty_abstract
        old: TestExtractAbstractData.test_extract_abstract_data_no_abstract

        Sem título não há parágrafo de título; resumo vazio ou ausente não
        gera bloco (o old_pdf devolvia título/conteúdo vazios).
        """
        cases = [
            ('<abstract><title>Abstract Title</title></abstract>',
             [('abstract_title', 'Abstract Title')]),
            ('<abstract><p>First paragraph.</p><p>Second paragraph.</p></abstract>',
             [('abstract', 'First paragraph.'), ('abstract', 'Second paragraph.')]),
            ('<abstract></abstract>', []),
            ('', []),
        ]
        for meta_xml, expected in cases:
            with self.subTest(meta_xml=meta_xml):
                self.assertEqual(summary(front(meta_xml)), expected)

    def test_abstract_inline_markup_is_kept(self):
        """
        old: TestExtractAbstractData.test_extract_abstract_data_with_nested_elements

        Todo o texto sai; no conteúdo, a formatação também (o título do
        resumo é texto simples, como no old_pdf).
        """
        blocks = front('<abstract><title>Abstract <italic>Title</italic></title>'
                       '<p>First <bold>paragraph</bold>.</p>'
                       '<p>Second <italic>paragraph</italic>.</p></abstract>')
        self.assertEqual(summary(blocks), [
            ('abstract_title', 'Abstract Title'),
            ('abstract', 'First paragraph.'),
            ('abstract', 'Second paragraph.'),
        ])
        self.assertIn({'text': 'paragraph', 'bold': True}, blocks[1]['runs'])
        self.assertIn({'text': 'paragraph', 'italic': True}, blocks[2]['runs'])

    def test_structured_abstract_subsections_become_title_colon_text(self):
        """
        old: TestExtractAbstractData.test_extract_abstract_data_structured_with_sections
        old: TestExtractAbstractData.test_extract_abstract_data_structured_section_title_without_punctuation
        old: TestExtractAbstractData.test_extract_abstract_data_structured_section_without_title
        old: TestExtractAbstractData.test_extract_abstract_data_mixed_direct_and_sectioned_paragraphs
        old: TestExtractTransAbstractData.test_extract_trans_abstract_data_structured_with_sections

        Regressão #1332: o <p> dentro de <sec> não pode sumir. Diferença
        intencional: cada subseção é um parágrafo "Título: texto" (título em
        negrito), em vez de uma string única.
        """
        cases = [
            ('<abstract><title>Abstract</title>'
             '<sec><title>Introduction:</title><p>Some introduction text.</p></sec>'
             '<sec><title>Methods:</title><p>Some methods text.</p></sec></abstract>',
             [('abstract_title', 'Abstract'),
              ('abstract', 'Introduction: Some introduction text.'),
              ('abstract', 'Methods: Some methods text.')]),
            # sem ':' no título, ele é acrescentado
            ('<abstract><sec><title>Objetivo</title><p>Descrever o metodo.</p></sec></abstract>',
             [('abstract', 'Objetivo: Descrever o metodo.')]),
            ('<abstract><sec><p>Untitled section text.</p></sec></abstract>',
             [('abstract', 'Untitled section text.')]),
            ('<abstract><p>Lead paragraph.</p>'
             '<sec><title>Conclusion:</title><p>Final remarks.</p></sec></abstract>',
             [('abstract', 'Lead paragraph.'), ('abstract', 'Conclusion: Final remarks.')]),
            ('<trans-abstract xml:lang="pt"><title>Resumo</title>'
             '<sec><title>Contexto:</title><p>Texto de contexto.</p></sec>'
             '<sec><title>Métodos:</title><p>Texto de métodos.</p></sec></trans-abstract>',
             [('abstract_title', 'Resumo'),
              ('abstract', 'Contexto: Texto de contexto.'),
              ('abstract', 'Métodos: Texto de métodos.')]),
        ]
        for meta_xml, expected in cases:
            with self.subTest(meta_xml=meta_xml):
                self.assertEqual(summary(front(meta_xml)), expected)
        title_run = front(cases[1][0])[0]['runs'][0]
        self.assertEqual(title_run, {'text': 'Objetivo', 'bold': True})

    def test_trans_abstracts_follow_main_abstract_in_document_order(self):
        """
        old: TestExtractTransAbstractData.test_extract_trans_abstract_data_basic
        old: TestExtractTransAbstractData.test_extract_trans_abstract_data_multiple_abstracts
        """
        blocks = front(
            '<trans-abstract xml:lang="en"><title>English Abstract</title>'
            '<p>First paragraph.</p><p>Second paragraph.</p></trans-abstract>'
            '<trans-abstract xml:lang="es"><title>Resumen en Español</title>'
            '<p>Primer párrafo.</p></trans-abstract>'
            '<abstract><title>Resumo</title><p>Texto.</p></abstract>'
        )
        self.assertEqual(summary(blocks), [
            ('abstract_title', 'Resumo'), ('abstract', 'Texto.'),
            ('abstract_title', 'English Abstract'),
            ('abstract', 'First paragraph.'), ('abstract', 'Second paragraph.'),
            ('abstract_title', 'Resumen en Español'), ('abstract', 'Primer párrafo.'),
        ])

    def test_trans_abstract_missing_empty_or_without_xml_lang(self):
        """
        old: TestExtractTransAbstractData.test_extract_trans_abstract_data_no_abstracts
        old: TestExtractTransAbstractData.test_extract_trans_abstract_data_empty_abstract
        old: TestExtractTransAbstractData.test_extract_trans_abstract_data_custom_namespace

        Diferença intencional: resumo vazio não gera parágrafos vazios; e não
        há parâmetro de namespaces: um ``custom:lang`` não é idioma, mas o
        resumo não se perde (sai sem idioma, sem palavras-chave pareadas).
        """
        cases = [
            ('', []),
            ('<trans-abstract xml:lang="en"><title></title><p></p></trans-abstract>', []),
            ('<trans-abstract xmlns:custom="http://custom.namespace" custom:lang="fr">'
             '<title>Résumé en Français</title><p>Premier paragraphe.</p></trans-abstract>',
             [('abstract_title', 'Résumé en Français'), ('abstract', 'Premier paragraphe.')]),
        ]
        for meta_xml, expected in cases:
            with self.subTest(meta_xml=meta_xml):
                self.assertEqual(summary(front(meta_xml)), expected)

    def test_trans_abstract_inline_markup_is_kept(self):
        """
        old: TestExtractTransAbstractData.test_extract_trans_abstract_data_paragraph_with_inline_markup
        old: TestExtractTransAbstractData.test_extract_trans_abstract_data_title_with_inline_markup

        Regressão #1321: o texto depois do <italic> não pode sumir.
        """
        blocks = front('<trans-abstract xml:lang="pt"><title>Resumo<italic>*</italic></title>'
                       '<p>Efeito do milho (<italic>Zea mays</italic> L.) na produtividade.</p>'
                       '</trans-abstract>')
        self.assertEqual(summary(blocks), [
            ('abstract_title', 'Resumo*'),
            ('abstract', 'Efeito do milho (Zea mays L.) na produtividade.'),
        ])
        self.assertIn({'text': 'Zea mays', 'italic': True}, blocks[1]['runs'])


# -----------------
# <kwd-group>
# -----------------


class KeywordsTest(unittest.TestCase):
    def test_keywords_paragraph_title_then_words(self):
        """
        old: TestExtractKeywordsData.test_extract_keywords_data_basic
        old: TestExtractKeywordsData.test_extract_keywords_data_no_title

        "Título palavra, palavra" (título em keywords_title_char, como o
        "{title} " do old_pdf).
        """
        cases = [
            ('<title>Keywords</title><kwd>Keyword1</kwd><kwd>Keyword2</kwd>',
             'Keywords Keyword1, Keyword2'),
            ('<kwd>Keyword1</kwd><kwd>Keyword2</kwd>', 'Keyword1, Keyword2'),
        ]
        for group, expected in cases:
            with self.subTest(group=group):
                blocks = front(f'<kwd-group xml:lang="en">{group}</kwd-group>')
                self.assertEqual(summary(blocks), [('keywords', expected)])
        blocks = front(f'<kwd-group xml:lang="en">{cases[0][0]}</kwd-group>')
        self.assertEqual(blocks[0]['runs'][0], {'text': 'Keywords ', 'char_role': 'keywords_title_char'})
        self.assertEqual(blocks[0]['char_role'], 'keywords_char')

    def test_keywords_without_kwd_or_group_give_no_paragraph(self):
        """
        old: TestExtractKeywordsData.test_extract_keywords_data_no_keywords
        old: TestExtractKeywordsData.test_extract_keywords_data_no_kwd_group

        Diferença intencional: grupo sem <kwd> não gera parágrafo com o
        título solto (o old_pdf devolvia o título com palavras vazias).
        """
        for meta_xml in ('<kwd-group xml:lang="en"><title>Keywords</title></kwd-group>', ''):
            with self.subTest(meta_xml=meta_xml):
                self.assertEqual(front(meta_xml), [])

    def test_keywords_follow_the_abstract_of_their_language(self):
        """
        old: TestExtractKeywordsData.test_extract_keywords_data_different_language

        O old_pdf escolhia o grupo pelo parâmetro lang; aqui cada grupo vai
        logo depois do resumo do mesmo idioma (e um grupo sem resumo do seu
        idioma sai sozinho no fim, para não se perder).
        """
        blocks = front(
            '<abstract><title>Resumo</title><p>pt</p></abstract>'
            '<trans-abstract xml:lang="es"><title>Resumen</title><p>es</p></trans-abstract>'
            '<kwd-group xml:lang="es"><title>Palabras clave</title><kwd>Palabra1</kwd><kwd>Palabra2</kwd></kwd-group>'
            '<kwd-group xml:lang="pt"><title>Palavras-chave</title><kwd>p1</kwd></kwd-group>'
            '<kwd-group xml:lang="fr"><kwd>mot</kwd></kwd-group>'
        )
        self.assertEqual(summary(blocks), [
            ('abstract_title', 'Resumo'), ('abstract', 'pt'), ('keywords', 'Palavras-chave p1'),
            ('abstract_title', 'Resumen'), ('abstract', 'es'),
            ('keywords', 'Palabras clave Palabra1, Palabra2'),
            ('keywords', 'mot'),
        ])

    def test_keywords_inline_markup_is_kept(self):
        """
        old: TestExtractKeywordsData.test_extract_keywords_data_keyword_with_inline_markup
        old: TestExtractKeywordsData.test_extract_keywords_data_title_with_inline_markup

        Regressão #1321: <kwd> com <italic> não pode ser truncado.
        """
        blocks = front('<kwd-group xml:lang="en"><title>Keywords<italic>*</italic></title>'
                       '<kwd>maize (<italic>Zea mays</italic> L.)</kwd>'
                       '<kwd>growth stimulation</kwd></kwd-group>')
        self.assertEqual(summary(blocks),
                         [('keywords', 'Keywords* maize (Zea mays L.), growth stimulation')])
        self.assertIn({'text': 'Zea mays', 'italic': True}, blocks[0]['runs'])


# -----------------
# idioma, título, tipo, DOI, periódico, rodapé
# -----------------


class MetaTest(unittest.TestCase):
    def test_main_language_is_article_xml_lang(self):
        """
        old: TestExtractArticleMainLanguage.test_extract_article_main_language_with_valid_lang
        old: TestExtractArticleMainLanguage.test_extract_article_main_language_without_lang
        old: TestExtractArticleMainLanguage.test_extract_article_main_language_with_custom_namespace
        old: TestExtractArticleMainLanguage.test_extract_article_main_language_with_multiple_langs

        Diferença intencional: sem idioma, '' (e não None); não há parâmetro
        de namespaces, então ``custom:lang`` não é idioma.
        """
        cases = [
            ('<article xml:lang="en"><front><article-meta/></front></article>', 'en'),
            ('<article><front><article-meta/></front></article>', ''),
            ('<article xmlns:custom="http://custom.namespace" custom:lang="pt">'
             '<front><article-meta/></front></article>', ''),
            # só o do <article> vale, não o de um descendente
            ('<article xml:lang="es"><front xml:lang="en"><article-meta/></front></article>', 'es'),
        ]
        for source, expected in cases:
            with self.subTest(source=source):
                self.assertEqual(article(xml(source))['meta']['lang'], expected)

    def test_article_title_text(self):
        """
        old: TestExtractArticleTitle.test_extract_article_title_basic
        old: TestExtractArticleTitle.test_extract_article_title_empty
        old: TestExtractArticleTitle.test_extract_article_title_with_formatting
        old: TestExtractArticleTitle.test_extract_article_title_missing

        Diferença intencional: sem <article-title>, '' e nenhum parágrafo de
        título (o old_pdf levantava AttributeError).
        """
        cases = [
            ('<title-group><article-title>Sample Title</article-title></title-group>', 'Sample Title'),
            ('<title-group><article-title></article-title></title-group>', ''),
            ('<title-group><article-title>Title with <italic>formatting</italic></article-title></title-group>',
             'Title with formatting'),
            ('', ''),
        ]
        for meta_xml, expected in cases:
            with self.subTest(meta_xml=meta_xml):
                self.assertEqual(meta(meta_xml)['title_text'], expected)
                titles = [b for b in front(meta_xml) if b['role'] == 'article_title']
                self.assertEqual(summary(titles), [('article_title', expected)] if expected else [])

    def test_article_title_block_keeps_formatting(self):
        """
        old: TestExtractArticleTitle.test_extract_article_title_return_element

        O old_pdf devolvia o elemento para o render preservar a formatação;
        aqui os runs do título a carregam.
        """
        blocks = front('<title-group><article-title>Sample <italic>Title</italic></article-title></title-group>')
        self.assertEqual(blocks[0]['runs'], [{'text': 'Sample '}, {'text': 'Title', 'italic': True}])

    def test_article_type(self):
        """
        old: TestExtractArticleType.test_extract_article_type_valid
        old: TestExtractArticleType.test_extract_article_type_missing
        old: TestExtractArticleType.test_extract_article_type_empty

        Diferença intencional: ausente vira '' (e não None).
        """
        for article_type, expected in (('research-article', 'research-article'), (None, ''), ('', '')):
            with self.subTest(article_type=article_type):
                root = with_journal('', article_type=article_type)
                self.assertEqual(article(root)['meta']['article_type'], expected)

    def test_doi(self):
        """
        old: TestExtractDOI.test_extract_doi_text
        old: TestExtractDOI.test_extract_doi_missing_doi
        old: TestExtractDOI.test_extract_doi_empty_doi
        old: TestExtractDOI.test_extract_doi_malformed_xml

        Diferença intencional: sem DOI (ausente, vazio ou sem
        pub-id-type="doi"), '' em vez de AttributeError/None.
        """
        cases = [
            ('<article-id pub-id-type="doi">10.1234/example.doi.2023</article-id>', '10.1234/example.doi.2023'),
            ('<article-id pub-id-type="other">12345</article-id>', ''),
            ('<article-id pub-id-type="doi"></article-id>', ''),
            ('<article-id>10.1234/malformed</article-id>', ''),
        ]
        for meta_xml, expected in cases:
            with self.subTest(meta_xml=meta_xml):
                self.assertEqual(meta(meta_xml)['doi'], expected)

    def test_journal_title(self):
        """
        old: TestExtractJournalTitle.test_extract_journal_title_basic
        old: TestExtractJournalTitle.test_extract_journal_title_empty
        old: TestExtractJournalTitle.test_extract_journal_title_missing
        old: TestExtractJournalTitle.test_extract_journal_title_with_nested_elements

        Diferença intencional: ausente vira '' (o old_pdf levantava AttributeError).
        """
        cases = [
            ('<journal-title-group><journal-title>Science Journal</journal-title></journal-title-group>',
             'Science Journal'),
            ('<journal-title-group><journal-title></journal-title></journal-title-group>', ''),
            ('', ''),
            ('<journal-title-group><journal-title>Science <italic>Journal</italic></journal-title>'
             '</journal-title-group>', 'Science Journal'),
        ]
        for journal_meta, expected in cases:
            with self.subTest(journal_meta=journal_meta):
                self.assertEqual(article(with_journal(journal_meta))['meta']['journal_title'], expected)

    def test_journal_title_doi_and_article_title_reach_the_docx_headers(self):
        """
        old: TestExtractJournalTitle.test_extract_journal_title_return_node
        old: TestExtractDOI.test_extract_doi_element

        O old_pdf devolvia os nós para o render; aqui verifica-se o DOCX:
        periódico em 2 linhas e link do DOI no cabeçalho da 1ª página;
        periódico | título no cabeçalho das demais.
        """
        root = with_journal(
            '<journal-title-group><journal-title>Science Journal</journal-title></journal-title-group>',
            '<article-id pub-id-type="doi">10.1234/example.doi.2023</article-id>'
            '<title-group><article-title>Sample Title</article-title></title-group>',
            back='<ack><p>ok</p></ack>',
        )
        section = docx(root).sections[0]
        self.assertEqual(all_text(section.first_page_header),
                         ['Science\nJournal', 'http://dx.doi.org/10.1234/example.doi.2023'])
        self.assertEqual(all_text(section.header), ['Science Journal', 'Sample Title'])
        self.assertEqual(journal_title_two_lines('Science Journal of X'), 'Science\nJournal of X')
        self.assertEqual(journal_title_two_lines('Science'), 'Science')

    def test_footer_data(self):
        """
        old: TestExtractFooterData.test_extract_footer_data_complete
        old: TestExtractFooterData.test_extract_footer_data_missing_elements
        old: TestExtractFooterData.test_extract_footer_data_no_pub_date
        old: TestExtractFooterData.test_extract_footer_data_uses_elocation_id_when_fpage_is_absent

        Diferença intencional: fpage/lpage são texto ('123'), não int.
        """
        keys = ('year', 'volume', 'issue', 'fpage', 'lpage', 'elocation_id', 'location_label')
        date = ('<pub-date date-type="collection" publication-format="electronic">'
                '<year>{}</year></pub-date>')
        cases = [
            (date.format(2023) + '<volume>10</volume><issue>2</issue><fpage>123</fpage><lpage>130</lpage>',
             ('2023', '10', '2', '123', '130', '', '123-130'), 'VOL. 10 (2) 2023: 123-130'),
            (date.format(2023), ('2023', '', '', '', '', '', ''), '2023'),
            ('', ('', '', '', '', '', '', ''), ''),
            (date.format(2024) + '<volume>33</volume><issue>3</issue><elocation-id>e282794</elocation-id>',
             ('2024', '33', '3', '', '', 'e282794', 'e282794'), 'VOL. 33 (3) 2024: e282794'),
        ]
        for meta_xml, expected, footer in cases:
            with self.subTest(meta_xml=meta_xml):
                data = meta(meta_xml)
                self.assertEqual(tuple(data[k] for k in keys), expected)
                self.assertEqual(vol_issue_year(data), footer)

    def test_footer_year_prefers_electronic_collection_date(self):
        """old: TestExtractFooterData.test_extract_footer_data_complete (data de coleção eletrônica)"""
        data = meta('<pub-date date-type="pub"><year>2022</year></pub-date>'
                    '<pub-date date-type="collection" publication-format="electronic"><year>2023</year></pub-date>')
        self.assertEqual(data['year'], '2023')


# -----------------
# <contrib-group>, <aff>, <author-notes>
# -----------------


AUTHOR = ('<contrib><name><surname>{surname}</surname><given-names>{given}</given-names></name>'
          '{xrefs}</contrib>')


def author(surname, given, *rids):
    return AUTHOR.format(surname=surname, given=given,
                         xrefs=''.join(f'<xref ref-type="aff" rid="{r}"/>' for r in rids))


def aff(aff_id, institution, label=None):
    label_xml = f'<label>{label}</label>' if label is not None else ''
    inst = f'<institution content-type="original">{institution}</institution>' if institution else ''
    return f'<aff id="{aff_id}">{label_xml}{inst}</aff>'


class ContribTest(unittest.TestCase):
    def test_author_affiliation_and_corresponding_note(self):
        """
        old: TestExtractContribData.test_extract_contrib_data_complete

        'John Smith[^]1*' -> marcas sobrescritas (e links para afiliação e
        nota); '*[^] Corresponding author: e-mail; ORCID' -> nota de autor.
        """
        blocks = front(
            '<contrib-group><contrib><name><surname>Smith</surname><given-names>John</given-names></name>'
            '<xref ref-type="aff" rid="aff1"/><xref ref-type="corresp" rid="c1"/>'
            '<contrib-id contrib-id-type="orcid">0000-0002-1234-5678</contrib-id></contrib></contrib-group>'
            + aff('aff1', 'University of Testing', '1')
            + '<author-notes><corresp id="c1"><email>john.smith@test.edu</email></corresp></author-notes>'
        )
        self.assertEqual(summary(blocks), [
            ('author', 'John Smith1*'),
            ('affiliation', '1 University of Testing'),
            ('affiliation', '* Corresponding author: john.smith@test.edu; https://orcid.org/0000-0002-1234-5678'),
        ])
        authors, affiliation, corresp = blocks
        self.assertEqual([(r['text'], r.get('anchor')) for r in authors['runs'] if r.get('superscript')],
                         [('1', 'aff1'), ('*', 'c1')])
        self.assertEqual(affiliation['runs'][:2], [{'bookmark': 'aff1'}, {'text': '1', 'superscript': True}])
        self.assertEqual(corresp['runs'][:2], [{'bookmark': 'c1'}, {'text': '* ', 'superscript': True}])

    def test_multiple_authors_without_corresponding_note(self):
        """old: TestExtractContribData.test_extract_contrib_data_multiple_authors"""
        blocks = front(
            f'<contrib-group>{author("Smith", "John", "aff1")}{author("Doe", "Jane", "aff2")}</contrib-group>'
            + aff('aff1', 'University A', '1') + aff('aff2', 'University B', '2')
        )
        self.assertEqual(summary(blocks), [
            ('author', 'John Smith1 and Jane Doe2'),
            ('affiliation', '1 University A'),
            ('affiliation', '2 University B'),
        ])

    def test_no_contrib_gives_no_author_blocks(self):
        """old: TestExtractContribData.test_extract_contrib_data_empty_tree"""
        self.assertEqual(front(''), [])

    def test_affiliation_without_text_or_label(self):
        """
        old: TestExtractContribData.test_extract_contrib_data_missing_institution
        old: TestExtractContribData.test_extract_contrib_data_missing_label

        Afiliação sem texto não sai; sem rótulo, sai sem marca (o old_pdf
        deixava uma marca sobrescrita vazia '[^]').
        """
        blocks = front(f'<contrib-group>{author("Smith", "John", "aff1")}</contrib-group>'
                       + aff('aff1', '', '1'))
        self.assertEqual(summary(blocks), [('author', 'John Smith1')])

        blocks = front(f'<contrib-group>{author("Smith", "John", "aff1")}</contrib-group>'
                       + aff('aff1', 'University X'))
        # sem rótulo, sem o espaço que o separaria do texto (o old_pdf deixava ' University X')
        self.assertEqual(summary(blocks), [('author', 'John Smith'), ('affiliation', 'University X')])
        self.assertFalse(any(r.get('superscript') for b in blocks for r in b['runs']))

    def test_translation_affiliations_stay_in_the_translation_document(self):
        """
        old: TestExtractContribData.test_subarticle_affiliation_is_not_printed
        old: TestExtractContribData.test_main_article_affiliation_without_xref_is_printed

        Diferença intencional: a tradução é outro documento, com as
        afiliações do seu front-stub.
        """
        sub_article = (
            '<sub-article article-type="translation" xml:lang="pt"><front-stub>'
            '<contrib-group>{contrib}</contrib-group>'
            '<aff id="aff1e"><label>I</label><institution content-type="original">Universidade A</institution></aff>'
            '</front-stub></sub-article>'
        )
        cases = [
            (author('Smith', 'John', 'aff1'), author('Smith', 'John', 'aff1e'), 'I'),
            # autor sem <xref>: a afiliação sai mesmo assim
            (author('Smith', 'John'), '', None),
        ]
        for contrib, sub_contrib, label in cases:
            with self.subTest(contrib=contrib):
                root = article_xml(
                    front=f'<contrib-group>{contrib}</contrib-group>' + aff('aff1', 'University A', label or '1'),
                    lang='en', extra=sub_article.format(contrib=sub_contrib),
                )
                main = [b for b in article(root)['front'] if b.get('role') == 'affiliation']
                self.assertEqual(summary(main), [('affiliation', f'{label or "1"} University A')])
                translated = [b for b in article(root, 'pt')['front'] if b.get('role') == 'affiliation']
                self.assertEqual(summary(translated), [('affiliation', 'I Universidade A')])

    def test_affiliations_kept_regardless_of_id_pattern(self):
        """old: TestExtractContribData.test_main_article_affiliations_are_kept_regardless_of_id_pattern"""
        blocks = front(
            f'<contrib-group>{author("Smith", "John", "aff01")}{author("Doe", "Jane", "aff0100")}</contrib-group>'
            + aff('aff01', 'University A', '1') + aff('aff0100', 'University B', '2')
        )
        self.assertEqual(summary([b for b in blocks if b['role'] == 'affiliation']),
                         [('affiliation', '1 University A'), ('affiliation', '2 University B')])


# -----------------
# "CITE AS": nota "como citar" e citação montada
# -----------------


class CiteAsNoteTest(unittest.TestCase):
    def test_cite_as_note_text(self):
        """
        old: TestExtractCiteAsPartOne.test_extract_cite_as_part_one_text
        old: TestExtractCiteAsPartOne.test_extract_cite_as_part_one_strips_inline_phrase_only_without_label
        old: TestExtractCiteAsPartOne.test_extract_cite_as_part_one_skips_unrelated_fn_type_other
        old: TestExtractCiteAsPartOne.test_extract_cite_as_part_one_full_text_with_nested_markup

        #1349: sem <label>, a frase "Cite as:"/"Como citar:" sai do <p>; só a
        nota identificada como "como citar" vale (não a primeira
        fn-type="other"); o texto inteiro, inclusive depois de <ext-link>.
        A nota não se repete no corpo.
        """
        cases = [
            ('<fn fn-type="other"><p>Cite as: Example Citation</p></fn>', 'Example Citation', []),
            ('<fn fn-type="other"><p>Como citar: Souza CM, Iser BM, Malta DC. Example title. '
             'Journal 31(3):e31030043.</p></fn>',
             'Souza CM, Iser BM, Malta DC. Example title. Journal 31(3):e31030043.', []),
            ('<fn fn-type="other"><label>ZooBank register</label><p>https://zoobank.org/some-id</p></fn>'
             '<fn fn-type="other"><label>How to cite this article</label>'
             '<p>Author AB (2024) Example citation.</p></fn>',
             'Author AB (2024) Example citation.', ['ZooBank register https://zoobank.org/some-id']),
            ('<fn fn-type="other"><label>CITE AS:</label><p>Author AB. Example title. Journal 1: 2. '
             '<ext-link>https://doi.org/10.1590/example</ext-link></p></fn>',
             'Author AB. Example title. Journal 1: 2. https://doi.org/10.1590/example', []),
        ]
        for notes, expected, other_notes in cases:
            with self.subTest(notes=notes):
                result = article(article_xml(body='<p>x</p>', back=f'<fn-group>{notes}</fn-group>'))
                self.assertEqual(result['meta']['cite_as'], expected)
                self.assertEqual([t for _, t in summary(result['main'])], ['x'] + other_notes)

    def test_no_cite_as_note(self):
        """
        old: TestExtractCiteAsPartOne.test_extract_cite_as_part_one_no_fn_group
        old: TestExtractCiteAsPartOne.test_extract_cite_as_part_one_no_fn_type_other
        old: TestExtractCiteAsPartOne.test_extract_cite_as_part_one_none_when_no_note_is_a_citation

        Sem nota "como citar" (e sem autores para montar a citação),
        cite_as é ''; as outras notas continuam no corpo.
        """
        cases = [
            ('', []),
            ('<fn-group><fn fn-type="conflict"><p>Not a citation</p></fn></fn-group>', ['Not a citation']),
            ('<fn-group><fn fn-type="other"><p>Study carried out at University X.</p></fn></fn-group>',
             ['Study carried out at University X.']),
        ]
        for back, notes in cases:
            with self.subTest(back=back):
                root = article_xml(body='<p>x</p>', back=back)
                self.assertIsNone(citation.cite_as_note(document_for(root)))
                result = article(root)
                self.assertEqual(result['meta']['cite_as'], '')
                self.assertEqual([t for _, t in summary(result['main'])], ['x'] + notes)

    def test_cite_as_note_node_and_footer(self):
        """
        old: TestExtractCiteAsPartOne.test_extract_cite_as_part_one_node

        cite_as_note devolve a <fn> (cujo <p> tem o texto original); no DOCX,
        o rodapé da 1ª página mostra "CITE AS: " + a nota, com ponto final.
        """
        root = article_xml(
            front='<pub-date><year>2023</year></pub-date><volume>10</volume><fpage>1</fpage><lpage>3</lpage>',
            body='<p>x</p>', back='<fn-group><fn fn-type="other"><p>Cite as: Example Citation</p></fn></fn-group>',
        )
        note = citation.cite_as_note(document_for(root))
        self.assertEqual((note.tag, note.get('fn-type')), ('fn', 'other'))
        self.assertEqual(note.find('p').text, 'Cite as: Example Citation')
        footer = all_text(docx(root).sections[0].first_page_footer)
        self.assertEqual(footer, ['CITE AS: Example Citation.', ' | VOL. 10 2023: 1-3'])


def cited_article(given_names=('Bárbara Passos da Silva', 'Kelly Regina Batista'), article_meta='',
                  journal='<abbrev-journal-title>Ex. J.</abbrev-journal-title>', contribs=None):
    """Artigo sem nota "como citar": a citação do rodapé é montada pelos metadados."""
    if contribs is None:
        contribs = ''.join(
            f'<contrib contrib-type="author"><name><surname>Surname{i}</surname>'
            f'<given-names>{given}</given-names></name></contrib>'
            for i, given in enumerate(given_names)
        )
    return with_journal(
        f'<journal-title-group><journal-title>Full Journal Name</journal-title>{journal}</journal-title-group>',
        f'<article-id pub-id-type="doi">10.1590/example</article-id>'
        f'<title-group><article-title>Example Article Title</article-title></title-group>'
        f'<contrib-group>{contribs}</contrib-group>{article_meta}',
    )


class BuiltCitationTest(unittest.TestCase):
    def test_complete_citation_with_volume_issue_and_doi(self):
        """old: TestBuildFullCitation.test_builds_complete_citation_with_volume_issue_and_doi"""
        root = cited_article(article_meta='<pub-date><year>2024</year></pub-date><volume>10</volume>'
                                          '<issue>2</issue><elocation-id>e12345</elocation-id>')
        self.assertEqual(
            article(root)['meta']['cite_as'],
            'Surname0 BPS, Surname1 KRB. Example Article Title. Ex. J. '
            '2024;10(2):e12345. https://doi.org/10.1590/example',
        )

    def test_missing_issue_or_volume(self):
        """
        old: TestBuildFullCitation.test_omits_issue_parens_when_issue_is_absent
        old: TestBuildFullCitation.test_omits_volume_when_absent
        """
        cases = [
            ('<pub-date><year>2024</year></pub-date><volume>10</volume><elocation-id>e12345</elocation-id>',
             '2024;10:e12345.'),
            ('<pub-date><year>2023</year></pub-date><elocation-id>e236720</elocation-id>', '2023;e236720.'),
        ]
        for article_meta, fragment in cases:
            with self.subTest(article_meta=article_meta):
                result = article(cited_article(('Bárbara Passos da Silva',), article_meta))['meta']['cite_as']
                self.assertIn(fragment, result)
                self.assertNotIn('()', result)

    def test_author_list_initials_and_et_al(self):
        """
        old: TestBuildFullCitation.test_initials_exclude_lowercase_particles
        old: TestBuildFullCitation.test_truncates_to_et_al_beyond_six_authors
        """
        cases = [
            (('Bárbara Passos da Silva',), 'Surname0 BPS.'),
            ([f'Author{i}' for i in range(8)],
             'Surname0 A, Surname1 A, Surname2 A, Surname3 A, Surname4 A, Surname5 A, et al.'),
        ]
        for names, start in cases:
            with self.subTest(names=names):
                result = article(cited_article(names, '<pub-date><year>2024</year></pub-date>'))['meta']['cite_as']
                self.assertTrue(result.startswith(start), result)

    def test_no_authors_gives_no_built_citation_and_footer_falls_back(self):
        """
        old: TestBuildFullCitation.test_returns_empty_string_when_there_are_no_authors

        Sem autores não se monta citação; o rodapé usa "periódico volume: local".
        """
        root = cited_article((), '<pub-date><year>2024</year></pub-date><volume>5</volume><fpage>7</fpage>')
        self.assertEqual(article(root)['meta']['cite_as'], '')
        footer = all_text(docx(root).sections[0].first_page_footer)
        self.assertEqual(footer[0], 'CITE AS: Full Journal Name 5: 7.')

    def test_full_journal_title_when_no_abbrev(self):
        """old: TestBuildFullCitation.test_falls_back_to_full_journal_title_when_no_abbrev"""
        root = cited_article(('Ana Maria',), '<pub-date><year>2024</year></pub-date>', journal='')
        self.assertIn('Full Journal Name.', article(root)['meta']['cite_as'])

    def test_unknown_style_gives_empty_citation(self):
        """old: TestBuildFullCitation.test_unknown_style_returns_empty_string"""
        from packtools.sps.formats.pdf.extract.article import extract_article
        root = cited_article(('Bárbara Passos da Silva',), '<pub-date><year>2024</year></pub-date>')
        self.assertEqual(extract_article(root, citation_style='abnt')['meta']['cite_as'], '')
        self.assertNotEqual(extract_article(root)['meta']['cite_as'], '')

    def test_only_authors_enter_the_citation(self):
        """
        old: TestBuildFullCitation.test_excludes_non_author_contrib_from_citation
        old: TestBuildFullCitation.test_includes_contrib_with_no_contrib_type_attribute

        #1350: tradutor não é autor; <contrib> sem contrib-type é autor.
        """
        cases = [
            ('<contrib contrib-type="author"><name><surname>Cholodenko</surname><given-names>Alan</given-names>'
             '</name></contrib><contrib contrib-type="translator"><name><surname>Sousa</surname>'
             '<given-names>Adriano</given-names></name></contrib>', 'Cholodenko A.'),
            ('<contrib><name><surname>Surname</surname><given-names>Ana</given-names></name></contrib>',
             'Surname A.'),
        ]
        for contribs, start in cases:
            with self.subTest(contribs=contribs):
                result = article(cited_article(contribs=contribs))['meta']['cite_as']
                self.assertTrue(result.startswith(start), result)
                self.assertNotIn('Sousa', result)

    def test_csl_item_type(self):
        """
        old: TestBuildCslReferenceType.test_defaults_to_article_journal
        old: TestBuildCslReferenceType.test_accepts_custom_csl_type

        O tipo do item CSL é 'article-journal' por padrão e pode ser trocado
        (verificado no item entregue ao citeproc).
        """
        root = cited_article(contribs='<contrib contrib-type="author"><name><surname>Surname</surname>'
                                      '<given-names>Ana</given-names></name></contrib>')
        view = document_for(root)
        meta_data = article(root)['meta']
        for kwargs, expected in (({}, 'article-journal'), ({'csl_type': 'editorial'}, 'editorial')):
            with self.subTest(kwargs=kwargs):
                with mock.patch.object(citation, 'CiteProcJSON', wraps=citation.CiteProcJSON) as source:
                    result = citation.build_citation(meta_data, view['meta'], **kwargs)
                (references,), _ = source.call_args
                self.assertEqual(references[0]['type'], expected)
                self.assertTrue(result.startswith('Surname A.'), result)


if __name__ == '__main__':
    unittest.main()
