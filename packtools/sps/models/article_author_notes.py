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
    def fn_numbers(self):
        return len(self.node.xpath('.//fn'))

    @property
    def fn_types(self):
        for fn in self.node.xpath('.//fn'):
            if fn.get('fn-type'):
                yield fn.get('fn-type')


class AuthorNotes:
    def __init__(self, xml_tree):
        self.xml_tree = xml_tree

    @property
    def article(self):
        for article in self.xml_tree.xpath('.//article-meta'):
            yield article

    @property
    def sub_articles(self):
        for sub_article in self.xml_tree.xpath('.//sub-article'):
            yield sub_article

    @property
    def article_and_sub_articles(self):
        yield from self.article
        yield from self.sub_articles

    @property
    def data(self):
        for node in self.article_and_sub_articles:
            author_note = AuthorNote(node)
            yield {
                'parent': 'sub-article' if node.get('id') else 'article',
                'parent_id': node.get('id'),
                'corresp': list(author_note.corresp),
                'fn_numbers': author_note.fn_numbers,
                'fn_types': list(author_note.fn_types)
            }

