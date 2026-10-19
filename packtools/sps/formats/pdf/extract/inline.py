"""
Percurso inline: conteúdo misto de um elemento -> runs.

Regra que evita perda de dados: todo nó é visitado com seu .text, cada
filho e o .tail de cada filho. Tag sem tratamento próprio (fora de
registry.INLINE) contribui com o texto dela, nunca é descartada;
comentários e instruções de processamento só contribuem com o .tail.
"""

from packtools.sps.formats.pdf.extract import registry
from packtools.sps.formats.pdf.extract.runs import tag, text_runs


def inlines(node, fmt=frozenset(), skip=()):
    """
    Runs do conteúdo de um elemento.

    Parâmetros
    ----------
    node : lxml.etree._Element
        Elemento percorrido.
    fmt : frozenset of str, opcional
        Formatos ativos herdados (ver styles.py).
    skip : sequence of lxml.etree._Element, opcional
        Filhos omitidos (o tail deles fica).

    Retorna
    -------
    list of dict
        Runs de node.text, de cada filho e de cada tail, sem o tail do
        próprio node.
    """
    runs = text_runs(node.text, fmt)
    for item in node:
        if item not in skip:
            runs += inline(item, fmt)
        runs += text_runs(item.tail, fmt)
    return runs


def inline(node, fmt=frozenset()):
    """
    Runs de um elemento (sem o tail), pelo tratamento registrado para a tag.

    Parâmetros
    ----------
    node : lxml.etree._Element
        Elemento.
    fmt : frozenset of str, opcional
        Formatos ativos herdados.

    Retorna
    -------
    list of dict
        Runs do elemento; tag sem tratamento contribui com seu texto.
    """
    name = tag(node)
    if name is None:
        return []
    handler = registry.INLINE.get(name)
    if handler:
        return handler(node, fmt)
    return inlines(node, fmt)


def plain_text(node):
    """
    Texto de um elemento numa linha, com espaços normalizados.

    Parâmetros
    ----------
    node : lxml.etree._Element or None
        Elemento (ou None).

    Retorna
    -------
    str
        Texto do elemento; vazio para None. Usado em metadados de uma linha
        (nome de autor, rótulo, ano...).
    """
    if node is None:
        return ""
    return " ".join("".join(r.get("text", "") for r in inlines(node)).split())
