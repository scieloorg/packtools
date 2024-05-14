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
            'parent': 'sub-article' if self.node.get('id') else 'article',
            'parent_id': self.node.get('id'),
            'corresp': list(author_note.corresp),
            'fn_count': author_note.fn_count,
            'fn_types': list(author_note.fn_types)
        }


class ArticleAuthorNotes:
    def __init__(self, xmltree):
        self.xmltree = xmltree

    @property
    def author_notes(self):
        for node in self.xmltree.xpath(".//article-meta | .//sub-article"):
            author_note = AuthorNotes(node)
            yield author_note.data
