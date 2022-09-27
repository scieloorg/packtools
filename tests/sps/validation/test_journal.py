from unittest import TestCase

from packtools.sps.utils.xml_utils import get_xml_tree
from packtools.sps.validation import journal
from packtools.sps import exceptions


class JournalTest(TestCase):
    def test_are_journal_issns_compatible_true_identical_issns(self):
        xml_article_str = """
        <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="en">
            <front>
                <journal-meta>
                    <issn pub-type="ppub">0103-5053</issn>
                    <issn pub-type="epub">1678-4790</issn>
                </journal-meta>
            </front>
        </article>
        """
        xml_article = get_xml_tree(xml_article_str)
        issns = ['0103-5053', '1678-4790']
        self.assertTrue(journal.are_journal_issns_compatible(xml_article, issns))
    
    def test_are_journal_issns_compatible_missing_issn_raises_exception(self):
        # Um dos códigos ISSN do XML não está na lista padrão
        xml_article_str = """
        <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="en">
            <front>
                <journal-meta>
                    <issn pub-type="epub">1678-4790</issn>
                </journal-meta>
            </front>
        </article>
        """
        xml_article = get_xml_tree(xml_article_str)
        issns = ['0103-5053', '1678-4790']
        with self.assertRaises(exceptions.ArticleHasIncompatibleJournalISSNError):
            journal.are_journal_issns_compatible(xml_article, issns)

    def test_are_journal_issns_compatible_one_different_issn_raises_exception(self):
        # Um dos códigos ISSN da lista padrão é diferente do que está no XML
        xml_article_str = """
        <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="en">
            <front>
                <journal-meta>
                    <issn pub-type="ppub">0103-5053</issn>
                    <issn pub-type="epub">1678-4790</issn>
                </journal-meta>
            </front>
        </article>
        """
        xml_article = get_xml_tree(xml_article_str)
        issns = ['0103-5053', '2222-2222']
        with self.assertRaises(exceptions.ArticleHasIncompatibleJournalISSNError):
            journal.are_journal_issns_compatible(xml_article, issns)

    def test_are_journal_issns_compatible_false_two_different_issn_raises_exception(self):
        # Nenhum código ISSN coincide
        xml_article_str = """
        <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="en">
            <front>
                <journal-meta>
                    <issn pub-type="ppub">0103-5053</issn>
                    <issn pub-type="epub">1678-4790</issn>
                </journal-meta>
            </front>
        </article>
        """
        xml_article = get_xml_tree(xml_article_str)
        issns = ['0103-0000', '0000-4790']
        with self.assertRaises(exceptions.ArticleHasIncompatibleJournalISSNError):
            journal.are_journal_issns_compatible(xml_article, issns)

    def test_are_journal_issns_compatible_false_empty_issn_list_raises_exception(self):
        xml_article_str = """
        <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="en">
            <front>
                <journal-meta>
                    <issn pub-type="ppub">0103-5053</issn>
                    <issn pub-type="epub">1678-4790</issn>
                </journal-meta>
            </front>
        </article>
        """
        xml_article = get_xml_tree(xml_article_str)
        with self.assertRaises(exceptions.ArticleHasIncompatibleJournalISSNError):
            journal.are_journal_issns_compatible(xml_article, [])

    def test_are_journal_titles_compatible_true(self):
        xml_article_str = """
        <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="en">
            <front>
                <journal-meta>
                    <journal-id journal-id-type="publisher-id">jbchs</journal-id>
                    <journal-title-group>
                        <journal-title>Journal of the Brazilian Chemical Society</journal-title>
                        <abbrev-journal-title abbrev-type="publisher">J. Braz. Chem. Soc.</abbrev-journal-title>
                    </journal-title-group>
                </journal-meta>
            </front>
        </article>
        """
        xml_article = get_xml_tree(xml_article_str)
        titles = ['Journal of the Brazilian Chemical Society', 'J. Braz. Chem. Soc.']
        self.assertTrue(journal.are_journal_titles_compatible(xml_article, titles))        
        self.assertTrue(journal.are_journal_titles_compatible(xml_article, ['J. Braz. Chem. Soc.']))
        self.assertTrue(journal.are_journal_titles_compatible(xml_article, ['Journal of the Brazilian Chemical Society']))


    def test_are_journal_titles_compatible_title_different_raises_exception(self):
        xml_article_str = """
        <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="en">
            <front>
                <journal-meta>
                    <journal-title-group>
                        <journal-title>Journal of the German Chemical Society</journal-title>
                        <abbrev-journal-title abbrev-type="publisher">J. Ger. Chem. Soc.</abbrev-journal-title>
                    </journal-title-group>
                </journal-meta>
            </front>
        </article>
        """
        xml_article = get_xml_tree(xml_article_str)
        titles = ['Journal of the Brazilian Chemical Society', 'J. Braz. Chem. Soc.']
        with self.assertRaises(exceptions.ArticleHasIncompatibleJournalTitleError):
            journal.are_journal_titles_compatible(xml_article, titles)

    def test_are_journal_acronyms_compatible_true(self):
        xml_article_str = """
        <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="en">
            <front>
                <journal-meta>
                    <journal-id journal-id-type="publisher-id">jbchs</journal-id>
                </journal-meta>
            </front>
        </article>
        """
        xml_article = get_xml_tree(xml_article_str)
        self.assertTrue(journal.are_journal_acronyms_compatible(xml_article, 'jbchs'))

    def test_are_journal_acronyms_compatible_acronym_different_raises_error(self):
        xml_article_str = """
        <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="en">
            <front>
                <journal-meta>
                    <journal-id journal-id-type="publisher-id">jbchs</journal-id>
                </journal-meta>
            </front>
        </article>
        """
        xml_article = get_xml_tree(xml_article_str)
        with self.assertRaises(exceptions.ArticleHasIncompatibleJournalAcronymError):
            journal.are_journal_acronyms_compatible(xml_article, 'jbch')

