"""
``<graphic>`` e ``<inline-graphic>``: imagem, usada sozinha ou dentro de
figura, tabela publicada como imagem, fórmula em imagem e material
suplementar.
"""

import re

from packtools.sps.formats.pdf.extract.inline import plain_text
from packtools.sps.formats.pdf.extract.registry import block_handler, inline_handler
from packtools.sps.formats.pdf.extract.runs import href, tag

# Herdado do old_pdf: content-type "scielo-267x140" marca a miniatura; a versão
# specific-use="scielo-web" é a de maior resolução publicada no site.
_THUMBNAIL = re.compile(r"267x140")
_EXT_RANK = (".png", ".jpg", ".jpeg", ".gif", ".tif", ".tiff")


@inline_handler("graphic", "inline-graphic")
def handle_inline(node, fmt):
    """
    Imagem dentro de texto (título, célula de tabela...).

    Parâmetros
    ----------
    node : lxml.etree._Element
        ``<graphic>`` ou ``<inline-graphic>``.
    fmt : frozenset of str
        Formatos ativos (não usados).

    Retorna
    -------
    list of dict
        Run de imagem, com o texto alternativo (ou o endereço) como reserva.
    """
    return [{"image": href(node), "alt": alt_text(node)}]


@block_handler("graphic")
def handle_block(node, ctx):
    """
    ``<graphic>`` solto (fora de ``<fig>``): figura sem legenda.

    Parâmetros
    ----------
    node : lxml.etree._Element
        ``<graphic>``.
    ctx : dict
        Contexto (não usado).

    Retorna
    -------
    list of dict
        Bloco ``figure``, ou lista vazia se não houver endereço.
    """
    return [figure_block(node, node, [])] if href(node) else []


def alt_text(node):
    """Texto alternativo da imagem: ``<alt-text>``, atributo ``alt`` ou, na falta, o endereço."""
    return plain_text(node.find("alt-text")) or node.get("alt") or href(node)


def best(candidates):
    """
    Escolhe a melhor entre representações alternativas de uma imagem.

    Parâmetros
    ----------
    candidates : iterable of lxml.etree._Element
        Elementos ``<graphic>``; os sem endereço são descartados.

    Retorna
    -------
    lxml.etree._Element or None
        O melhor candidato, ou None se nenhum tiver endereço. Critérios, em
        ordem: não ser miniatura, ser ``scielo-web``, maior área, extensão
        preferida (ver _EXT_RANK).
    """

    def rank(graphic):
        """Chave de ordenação (menor é melhor): (miniatura, não scielo-web, -área, extensão)."""
        ctype = (graphic.get("content-type") or "").lower()
        size = re.search(r"(\d+)x(\d+)", ctype)
        area = int(size.group(1)) * int(size.group(2)) if size else 0
        ext = next(
            (i for i, e in enumerate(_EXT_RANK) if href(graphic).lower().endswith(e)),
            len(_EXT_RANK),
        )
        return (
            bool(_THUMBNAIL.search(ctype)),
            (graphic.get("specific-use") or "").lower() != "scielo-web",
            -area,
            ext,
        )

    candidates = [g for g in candidates if href(g)]
    return min(candidates, key=rank) if candidates else None


def graphics(node):
    """
    Lista as imagens de um elemento (só filhos diretos).

    Parâmetros
    ----------
    node : lxml.etree._Element
        ``<fig>``, ``<table-wrap>``, ``<disp-formula>``...

    Retorna
    -------
    list of lxml.etree._Element
        Cada ``<graphic>`` com endereço e, de cada ``<alternatives>``, a
        melhor imagem (ver `best`).
    """
    found = []
    for item in node:
        if tag(item) == "graphic" and href(item):
            found.append(item)
        elif tag(item) == "alternatives":
            chosen = best(g for g in item if tag(g) == "graphic")
            if chosen is not None:
                found.append(chosen)
    return found


def figure_block(owner, graphic, caption, caption_role="figure_caption", caption_first=False):
    """
    Cria um bloco de figura para uma imagem.

    Parâmetros
    ----------
    owner : lxml.etree._Element
        Elemento dono da figura (fornece o ``id``).
    graphic : lxml.etree._Element
        Imagem (fornece endereço e texto alternativo).
    caption : list of dict
        Runs da legenda.
    caption_role : str, opcional
        Papel (estilo) da legenda.
    caption_first : bool, opcional
        Se True, a legenda vem antes da imagem (tabela publicada como imagem).

    Retorna
    -------
    dict
        Bloco ``figure``.
    """
    return {
        "type": "figure",
        "id": owner.get("id"),
        "href": href(graphic),
        "alt": alt_text(graphic),
        "caption": caption,
        "caption_role": caption_role,
        "caption_first": caption_first,
    }
