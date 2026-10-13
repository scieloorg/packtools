"""
Tabelas tag -> função, preenchidas pelos módulos de cada elemento.

Cada módulo de elemento registra as tags que trata com os decoradores
abaixo; ``extract/__init__.py`` importa todos os módulos, então as tabelas
estão completas assim que o pacote é carregado. O percurso (inline.py e
flow.py) só consulta as tabelas e não importa os módulos de elemento, o
que evita import circular.

- INLINE: ``função(node, fmt) -> runs``, para o que fica dentro de um
  parágrafo (itálico, link, fórmula inline...).
- BLOCK: ``função(node, ctx) -> blocos``, para o que abre um bloco próprio
  (seção, parágrafo, lista, figura, tabela...).
"""

INLINE = {}
BLOCK = {}


def inline_handler(*tags):
    """
    Registra a função decorada como tratamento inline das tags.

    Parâmetros
    ----------
    *tags : str
        Nomes locais das tags.

    Retorna
    -------
    callable
        Decorador que devolve a própria função.
    """

    def register(function):
        """Associa a função às tags em INLINE."""
        for name in tags:
            INLINE[name] = function
        return function

    return register


def block_handler(*tags):
    """
    Registra a função decorada como tratamento de bloco das tags.

    Parâmetros
    ----------
    *tags : str
        Nomes locais das tags.

    Retorna
    -------
    callable
        Decorador que devolve a própria função.
    """

    def register(function):
        """Associa a função às tags em BLOCK."""
        for name in tags:
            BLOCK[name] = function
        return function

    return register
