"""
Contexto do percurso: um dict simples passado a cada handler de bloco.

Chaves:

- ``level``: nível do último título (o corpo começa em 1; ``<sec>`` vira título 2);
- ``role``: papel (estilo) dos parágrafos gerados (``"body"``, ``"abstract"``...);
- ``fmt``: frozenset dos formatos inline herdados de um container (ex. ``<bold>``);
- ``indent``: níveis de recuo (lista aninhada, citação em bloco);
- ``list_depth``: profundidade de listas aninhadas;
- ``inline_titles``: título de seção vira prefixo em negrito (resumo estruturado);
- ``lang``: idioma do documento, para os títulos padrão (config/labels);
- ``exclude``: nós que não entram no fluxo (ex. a nota "como citar", já no rodapé);
- ``ref_title``: título que substitui o da ``<ref-list>`` (tradução, ver languages.py).

O contexto nunca é alterado no lugar: descer um nível cria um novo com
`child`, então nada precisa ser desfeito na volta da recursão.
"""

DEFAULTS = {
    "level": 1,
    "role": "body",
    "fmt": frozenset(),
    "indent": 0,
    "list_depth": 0,
    "inline_titles": False,
    "lang": None,
    "exclude": frozenset(),
    "ref_title": None,
    # lista que recebe os blocos dos anexos (apêndices e material
    # suplementar, ver sec.to_annex); None = extrair no lugar (resumos,
    # sub-articles). É o único valor mutável do contexto: um coletor
    # compartilhado pelo documento, nunca reatribuído.
    "annex": None,
}


def context(**values):
    """
    Cria um contexto.

    Parâmetros
    ----------
    **values
        Chaves que diferem de DEFAULTS.

    Retorna
    -------
    dict
        Contexto completo.
    """
    unknown = set(values) - set(DEFAULTS)
    if unknown:
        raise KeyError(f"chave de contexto desconhecida: {sorted(unknown)}")
    ctx = dict(DEFAULTS, **values)
    ctx["exclude"] = frozenset(ctx["exclude"])
    return ctx


def child(ctx, **changes):
    """
    Cria o contexto de um nível abaixo.

    Parâmetros
    ----------
    ctx : dict
        Contexto atual (não é alterado).
    **changes
        Chaves que mudam (ex. ``level=ctx["level"] + 1``).

    Retorna
    -------
    dict
        Cópia rasa com as mudanças.
    """
    unknown = set(changes) - set(DEFAULTS)
    if unknown:
        raise KeyError(f"chave de contexto desconhecida: {sorted(unknown)}")
    return {**ctx, **changes}
