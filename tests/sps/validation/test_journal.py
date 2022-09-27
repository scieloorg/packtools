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
