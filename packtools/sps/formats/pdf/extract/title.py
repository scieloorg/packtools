"""
Rótulos, títulos e legendas: ``<label>``, ``<title>`` e ``<caption>``.

Folhas reaproveitadas por seções, figuras, tabelas, fórmulas, listas e notas.
"""

import re

from packtools.sps.formats.pdf.extract.inline import inline, inlines, plain_text
from packtools.sps.formats.pdf.extract.runs import has_content, normalize, runs_text, tag, text_run


# -----------------
# ``<label>``: rótulo usado por vários elementos pais.
# -----------------
# O mesmo ``<label>`` tem apresentações diferentes conforme o pai:
#
# - nota (``<fn>``, ``<corresp>``): marca sobrescrita ou palavra em negrito,
#   no início do texto (`note_label_runs`);
# - fórmula: entre parênteses depois dela (`after_runs`);
# - seção, figura, tabela, item de lista: tratado por `title_runs`,
#   `caption_runs` (abaixo) e list_.py, que reaproveitam `label_of`.


# marca curta de nota: símbolos (*, †), número ou uma letra minúscula
_NOTE_MARK = re.compile(r"[^\w\s]{1,4}|\d{1,3}|[a-z]")


def label_of(node):
    """O ``<label>`` filho direto do elemento, ou None."""
    return node.find("label")


def note_label_runs(label):
    """
    Rótulo de nota, para o início do texto da nota.

    Parâmetros
    ----------
    label : lxml.etree._Element
        ``<label>`` de ``<fn>`` ou ``<corresp>``.

    Retorna
    -------
    list of dict
        Marca curta ("1", "*", "a") sobrescrita; palavra ("Editor") em
        negrito. Inclui o espaço final; vazio se o rótulo não tem texto.
    """
    text = plain_text(label)
    if not text:
        return []
    fmt = "superscript" if _NOTE_MARK.fullmatch(text) else "bold"
    return inlines(label, frozenset({fmt})) + [text_run(" ")]


def after_runs(node):
    """
    Rótulo para pôr depois do conteúdo (fórmula numerada).

    Parâmetros
    ----------
    node : lxml.etree._Element
        Elemento com ``<label>`` opcional.

    Retorna
    -------
    list of dict
        Run com o rótulo precedido de espaço (ex. " (1)"), ou lista vazia.
    """
    text = plain_text(label_of(node))
    return [text_run(f" {text}")] if text else []


# -----------------
# ``<title>``: título de seção, apêndice, lista, nota, resumo...
# -----------------
# Reaproveitado por todo elemento com título próprio (sec.py e quem o usa).


def title_runs(node, replacement=None):
    """
    Monta o título de um elemento a partir de ``<label>`` e ``<title>``.

    Parâmetros
    ----------
    node : lxml.etree._Element
        Elemento que pode ter ``<label>`` e ``<title>`` (só filhos diretos).
    replacement : str, opcional
        Texto que substitui o do ``<title>`` (ex. título das referências na
        tradução, ver languages.py); o ``<label>`` é mantido.

    Retorna
    -------
    runs : list of dict
        Runs normalizados de "rótulo título".
    consumed : list of lxml.etree._Element
        Elementos usados, para o chamador pular no fluxo.
    """
    label, title = label_of(node), node.find("title")
    runs = inlines(label) if label is not None else []
    if title is not None or replacement:
        if runs:
            runs.append(text_run(" "))
        runs += [text_run(replacement)] if replacement else inlines(title)
    return normalize(runs), [e for e in (label, title) if e is not None]


# -----------------
# ``<caption>``: legenda de figura, tabela, fórmula e grupo de figuras/tabelas.
# -----------------


# filhos do elemento que não entram na legenda: metadados da imagem e o
# próprio conteúdo (imagem, tabela, membros de grupo, notas da tabela)
METADATA = {"label", "caption", "graphic", "alternatives", "object-id", "alt-text", "long-desc"}
GROUP_MEMBERS = {"fig", "table-wrap", "fig-group", "table-wrap-group"}
NOT_CAPTION = METADATA | GROUP_MEMBERS | {"table", "table-wrap-foot"}


def caption_runs(node):
    """
    Monta a legenda de uma figura, tabela, fórmula ou grupo.

    Parâmetros
    ----------
    node : lxml.etree._Element
        Elemento com ``<label>`` e ``<caption>`` opcionais.

    Retorna
    -------
    list of dict
        Runs normalizados de "Rótulo. Título Parágrafos...", com o rótulo
        em negrito, seguidos de ``<attrib>``, ``<permissions>`` e qualquer
        outro filho que não seja metadado nem conteúdo (ver NOT_CAPTION).
    """
    label = label_of(node)
    runs = inlines(label, frozenset({"bold"})) if label is not None else []
    caption = node.find("caption")
    if caption is not None:
        body = []
        for item in caption:
            if tag(item):
                body += ([text_run(" ")] if body else []) + inline(item)
        if has_content(body) and runs:
            runs.append(text_run(" " if runs_text(runs).rstrip()[-1:] in ".:" else ". "))
        runs += body
    for item in node:
        if tag(item) and tag(item) not in NOT_CAPTION:
            runs += [text_run(" ")] + inline(item)
    return normalize(runs)
