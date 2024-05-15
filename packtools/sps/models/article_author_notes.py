"""
<author-notes>
<corresp>
<label>Correspondência</label>:  Karine de Lima Sírio Boclin  Sousa Lima, 257 apto. 902 Copacabana  22081-010 Rio de Janeiro, RJ, Brasil  E-mail: <email>karine.boclin@gmail.com</email>
</corresp>
<fn fn-type="conflict">
<p>Os autores declaram não haver conflito de interesses.</p>
</fn>
</author-notes>
"""

from packtools.sps.utils.xml_utils import process_subtags


class AuthorNote:
    def __init__(self, node):
        self.node = node

    @property
    def corresp(self):
        for corresp in self.node.xpath('.//corresp'):
            yield process_subtags(corresp)

    @property
    def fn_count(self):
        return len(self.node.xpath('.//fn'))

    @property
    def fn_types(self):
        for fn in self.node.xpath('.//fn'):
            if fn.get('fn-type'):
                yield fn.get('fn-type')


class AuthorNotes:
    def __init__(self, node):
        self.node = node

    @property
    def data(self):
        author_note = AuthorNote(self.node)
        return {
            'corresp': list(author_note.corresp),
            'fn_count': author_note.fn_count,
            'fn_types': list(author_note.fn_types)
        }


class ArticleAuthorNotes:
    def __init__(self, xmltree):
        self.xmltree = xmltree

    @property
    def author_notes(self):
        main = self.xmltree.xpath(".")[0]
        main_lang = main.get("{http://www.w3.org/XML/1998/namespace}lang")
        main_article_type = main.get("article-type")
        for node in self.xmltree.xpath(".//article-meta | .//sub-article"):
            node_lang = node.get("{http://www.w3.org/XML/1998/namespace}lang")
            node_article_type = node.get("article-type")
            author_note = AuthorNotes(node).data
            author_note["parent"] = 'sub-article' if node.tag == 'sub-article' else 'article'
            author_note["parent_id"] = node.get('id')
            author_note["parent_lang"] = node_lang or main_lang
            author_note["parent_article_type"] = node_article_type or main_article_type
            yield author_note
