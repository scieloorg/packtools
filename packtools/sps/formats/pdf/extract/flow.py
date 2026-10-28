"""
Percurso de blocos: conteúdo misto de um elemento -> lista plana de blocos.

Formas de bloco::

    {"type": "heading", "level": int, "runs": [...]}
    {"type": "paragraph", "role": str, "runs": [...], "indent": int, "preserve": bool,
     "char_role": str (opcional, estilo de caractere dos runs)}
    {"type": "formula", "runs": [{"omml": ...}, ...]}
    {"type": "figure", "id", "href", "alt", "caption": [...], "caption_role", "caption_first"}
    {"type": "table", "id", "panel", "caption": [...], "nrows", "ncols",
     "cells": [{"row", "col", "rowspan", "colspan", "header", "runs"}], "foot": [[...]]}

O único aninhamento é o necessário: o bloco contém seus runs (e a tabela,
suas células e notas). Bloco que é alvo de ``<xref>`` ganha um run
``{"bookmark": id}`` no início ou a chave ``anchor`` (figura, tabela).

`flow` acumula o texto, os inlines e os tails num parágrafo e o fecha
sempre que encontra um filho de bloco, que vai para o handler registrado
em registry.BLOCK. Elemento sem handler vira inline; se tiver algum bloco
dentro, é percorrido como container. Assim todo texto do XML chega à saída.
"""

from packtools.sps.formats.pdf.extract import inline, registry, styles
from packtools.sps.formats.pdf.extract.context import child as child_context
from packtools.sps.formats.pdf.extract.runs import (
    bookmark_runs,
    has_content,
    normalize,
    tag,
    text_run,
    text_runs,
)


def flow(node, ctx, prefix=None, skip=(), handlers=None):
    """
    Converte o conteúdo misto de um elemento em blocos.

    Parâmetros
    ----------
    node : lxml.etree._Element
        Elemento cujo conteúdo será percorrido.
    ctx : dict
        Contexto (ver context.py).
    prefix : list of dict, opcional
        Runs prepostos ao primeiro parágrafo (marcador de lista, rótulo de
        nota). Se o primeiro filho for um ``<p>`` sem texto antes dele, o
        prefixo entra no início desse ``<p>``.
    skip : sequence of lxml.etree._Element, opcional
        Filhos já consumidos pelo chamador (título, rótulo).
    handlers : dict, opcional
        Handlers locais (tag -> ``função(node, ctx)``), com precedência
        sobre registry.BLOCK só neste nível (ex. ``<list-item>`` de uma lista).

    Retorna
    -------
    list of dict
        Blocos na ordem do documento.
    """
    return flow_nodes(node.text, list(node), ctx, prefix, skip, handlers)


def flow_nodes(text, children, ctx, prefix=None, skip=(), handlers=None):
    """
    Converte em blocos uma sequência de nós que não precisam ter o mesmo pai.

    Parâmetros
    ----------
    text : str or None
        Texto antes do primeiro nó.
    children : list of lxml.etree._Element
        Nós na ordem desejada (ex. o ``<back>`` de uma tradução, montado com
        filhos do artigo e da tradução, sem copiar nada).
    ctx, prefix, skip, handlers
        Como em `flow`.

    Retorna
    -------
    list of dict
        Blocos na ordem dos nós.
    """
    blocks, buffer = [], list(prefix or [])
    pending = len(buffer)  # prefixo ainda sem texto próprio: vai para o primeiro <p>
    buffer += text_runs(text, ctx["fmt"])
    for node in children:
        process_child(node, ctx, buffer, pending, blocks, skip, handlers)
        buffer += text_runs(node.tail, ctx["fmt"])
        if has_content(buffer[pending:]) or not buffer:
            pending = 0
    flush(buffer, blocks, ctx)
    return blocks


def flush(buffer, blocks, ctx):
    """Fecha o parágrafo acumulado em ``buffer`` (se tiver conteúdo) e o acrescenta a ``blocks``."""
    if has_content(buffer):
        blocks.extend(paragraph(buffer, ctx))
    buffer.clear()


def handler(node, handlers=None):
    """
    Escolhe quem trata o nó como bloco.

    Parâmetros
    ----------
    node : lxml.etree._Element
        Filho do elemento percorrido.
    handlers : dict, opcional
        Handlers locais deste nível; valor None manda a tag para o texto.

    Retorna
    -------
    callable or None
        ``função(node, ctx) -> blocos``, ou None quando o nó não é bloco e
        deve virar texto do parágrafo em aberto.
    """
    name = tag(node)
    # 1. handler local deste nível (ex. "list-item" dentro de uma lista);
    #    None faz a tag virar texto do parágrafo (material suplementar no <p>)
    if handlers and name in handlers:
        return handlers[name]
    # 2. handler registrado pelo módulo do elemento
    if name in registry.BLOCK:
        return registry.BLOCK[name]
    # 3. tag desconhecida com blocos dentro: percorre como container
    if contains_block(node, handlers):
        return handle_container
    return None


def process_child(node, ctx, buffer, pending, blocks, skip, handlers):
    """
    Trata um filho do elemento percorrido por `flow_nodes`.

    Parâmetros
    ----------
    node : lxml.etree._Element
        O filho (comentário/instrução também chegam aqui e são ignorados).
    ctx : dict
        Contexto.
    buffer : list of dict
        Runs do parágrafo em aberto; alterado no lugar.
    pending : int
        Quantos runs do início de ``buffer`` são o prefixo ainda sem texto próprio.
    blocks : list of dict
        Blocos já produzidos; alterado no lugar.
    skip : sequence of lxml.etree._Element
        Filhos já consumidos pelo chamador.
    handlers : dict or None
        Handlers locais deste nível.

    Notas
    -----
    ``buffer`` e ``blocks`` são alterados no lugar: precisam continuar sendo
    os mesmos objetos de `flow_nodes`. ``handlers`` chega por parâmetro (e
    não por variável global) porque vale só para os filhos deste nó: o
    ``{"list-item": ...}`` de uma lista não pode valer para uma lista
    aninhada, nem a rota dos anexos (article.py) para uma ``<sec>`` interna.
    """
    if tag(node) is None or node in skip or node in ctx["exclude"]:
        return
    block = handler(node, handlers)
    # sem handler: o nó é texto do parágrafo em aberto
    if block is None:
        buffer += inline.inline(node, ctx["fmt"])
        return
    if pending and tag(node) == "p" and not has_content(buffer[pending:]):
        # o handler do <p> (sec.handle_p), não flow direto: ele decide se o material suplementar fica no texto
        produced = block(node, ctx, prefix=buffer[:pending])
        buffer.clear()
    else:
        flush(buffer, blocks, ctx)
        produced = block(node, ctx)
    blocks += mark_target(node, produced)


def contains_block(node, handlers=None):
    """
    True se algum descendente é elemento de bloco (decide se uma tag desconhecida é container).

    Tag que ``handlers`` manda para o texto (valor None) não conta, nem o que
    está dentro dela: ``<italic>`` em volta de material suplementar no ``<p>``
    continua inline, mesmo com ``<p>`` na legenda do item.
    """
    inline_here = {name for name, value in (handlers or {}).items() if value is None}
    for e in node.iterchildren():
        if tag(e) in inline_here:
            continue
        if tag(e) in registry.BLOCK or contains_block(e, handlers):
            return True
    return False


def handle_container(node, ctx):
    """
    Trata elemento sem handler que contém blocos.

    Parâmetros
    ----------
    node : lxml.etree._Element
        Elemento container (tag desconhecida ou de estilo, como ``<bold>``).
    ctx : dict
        Contexto.

    Retorna
    -------
    list of dict
        Blocos do conteúdo; o formato do próprio elemento (ex. ``<bold>``)
        vale para todo o conteúdo.
    """
    name = tag(node)
    fmt = ctx["fmt"] | ({styles.FORMATS[name]} if name in styles.FORMATS else frozenset())
    return flow(node, child_context(ctx, fmt=fmt))


def paragraph(runs, ctx, role=None, preserve=False):
    """
    Cria um bloco de parágrafo com os runs normalizados.

    Parâmetros
    ----------
    runs : list of dict
        Runs do parágrafo.
    ctx : dict
        Contexto (papel e recuo).
    role : str, opcional
        Papel do parágrafo; se omitido, ``ctx["role"]``.
    preserve : bool, opcional
        Se True, preserva espaços e quebras de linha.

    Retorna
    -------
    list of dict
        Lista com um bloco ``paragraph``, ou vazia se não sobrar conteúdo.
    """
    runs = normalize(runs, preserve_space=preserve)
    if not has_content(runs):
        return []
    return [
        {
            "type": "paragraph",
            "role": role or ctx["role"],
            "runs": runs,
            "indent": ctx["indent"],
            "preserve": preserve,
        }
    ]


def styled_paragraph(runs, role, char_role=None):
    """
    Cria um parágrafo da capa com runs já prontos.

    Parâmetros
    ----------
    runs : list of dict
        Runs montados pelo chamador (autores, afiliação, palavras-chave...);
        não são normalizados de novo.
    role : str
        Papel (estilo) do parágrafo.
    char_role : str, opcional
        Estilo de caractere de todos os runs (um run pode ter o seu próprio
        em ``run["char_role"]``).

    Retorna
    -------
    list of dict
        Lista com um bloco ``paragraph``, ou vazia sem conteúdo.
    """
    if not has_content(runs):
        return []
    block = {"type": "paragraph", "role": role, "runs": runs, "indent": 0, "preserve": False}
    if char_role:
        block["char_role"] = char_role
    return [block]


def mark_target(node, blocks):
    """
    Torna o primeiro bloco do elemento alvo possível de um ``<xref>``.

    Parâmetros
    ----------
    node : lxml.etree._Element
        Elemento de bloco que gerou os blocos (aff, ref, fig, table-wrap, fn, sec...).
    blocks : list of dict
        Blocos gerados; o primeiro é alterado no lugar.

    Retorna
    -------
    list of dict
        Os mesmos blocos. Com ``@id``, o primeiro recebe um run
        ``{"bookmark": id}`` no início (parágrafo, título, fórmula) ou a
        chave ``anchor`` (figura, tabela). Feito aqui, no despacho, vale
        para qualquer elemento com ``@id``.
    """
    marks = bookmark_runs(node)
    if marks and blocks:
        first = blocks[0]
        if "runs" in first:
            first["runs"] = marks + first["runs"]
        else:
            first.setdefault("anchor", marks[0]["bookmark"])
    return blocks


def block_runs(blocks):
    """
    Achata blocos em runs, para lugares onde só cabem runs (célula de tabela).

    Parâmetros
    ----------
    blocks : list of dict
        Blocos.

    Retorna
    -------
    list of dict
        Runs dos blocos separados por quebra de linha. Figura vira run de
        imagem seguido da legenda; tabela, o texto das células.
    """
    runs = []
    for block in blocks:
        if runs:
            runs.append({"break": True})
        if block.get("anchor"):
            runs.append({"bookmark": block["anchor"]})
        if block["type"] == "figure":
            runs.append({"image": block["href"], "alt": block["alt"]})
            runs += block["caption"]
        elif block["type"] == "table":
            for cell in block["cells"]:
                runs += cell["runs"] + [text_run(" ")]
        else:
            runs += block["runs"]
    return runs
