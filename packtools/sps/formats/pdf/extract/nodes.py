"""
Busca em uma lista de nós como se fossem filhos de um mesmo elemento.

Na tradução, o ``article-meta`` é composto de filhos do artigo e do
``front-stub`` (ver languages.py), sem montar um elemento novo. Estas
funções fazem nessa lista o que ``find``/``iter`` fariam no elemento.
"""

from itertools import chain

from packtools.sps.formats.pdf.extract.runs import tag


def find(nodes, path):
    """
    Primeiro elemento que casa com o caminho.

    Parâmetros
    ----------
    nodes : list of lxml.etree._Element
        Nós tratados como filhos de um mesmo elemento.
    path : str
        Caminho XPath relativo ao elemento pai, como em ``element.find``
        (ex. ``"volume"``, ``'article-id[@pub-id-type="doi"]'``,
        ``"article-categories//subj-group/subject"``).

    Retorna
    -------
    lxml.etree._Element or None
        Primeiro resultado, na ordem dos nós.
    """
    for node in nodes:
        found = node.xpath(f"self::{path}")
        if found:
            return found[0]
    return None


def findall(nodes, name):
    """Os nós da lista com a tag ``name``."""
    return [node for node in nodes if tag(node) == name]


def iter_all(nodes, name):
    """Todos os elementos ``name`` nos nós da lista e nos seus descendentes, na ordem."""
    return chain.from_iterable(node.iter(name) for node in nodes)
