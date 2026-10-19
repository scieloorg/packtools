"""
Runs: os pedaços de texto (com formato) que formam um parágrafo.

Formas de run::

    {"text": str, <formato>: True, "href": url, "anchor": id, "char_role": papel}
    {"omml": <m:oMath>}                 fórmula
    {"image": href, "alt": str}         imagem inline
    {"break": True}                     quebra de linha
    {"bookmark": id}                    marca (alvo de um <xref>)

Este módulo só cria, junta e mede runs; não conhece elementos XML.
"""

import re

from lxml import etree

XLINK_HREF = "{http://www.w3.org/1999/xlink}href"
MATHML = "{http://www.w3.org/1998/Math/MathML}"

# formatos que um run de texto pode ter (ver styles.py, que os aplica)
FLAGS = (
    "italic",
    "bold",
    "superscript",
    "subscript",
    "small_caps",
    "underline",
    "strike",
    "monospace",
)


def tag(node):
    """
    Nome local da tag.

    Parâmetros
    ----------
    node : lxml.etree._Element
        Elemento, comentário ou instrução de processamento.

    Retorna
    -------
    str or None
        Nome sem namespace; None para comentário/instrução.
    """
    return etree.QName(node).localname if isinstance(node.tag, str) else None


def href(node):
    """Endereço do elemento (xlink:href ou href); vazio se não houver."""
    return node.get(XLINK_HREF) or node.get("href") or ""


def text_run(text, fmt=frozenset(), **extra):
    """
    Cria um run de texto.

    Parâmetros
    ----------
    text : str
        Texto.
    fmt : iterable of str, opcional
        Formatos ativos (ver FLAGS), marcados como True.
    **extra
        Outras chaves do run (``href``, ``anchor``, ``char_role``...).

    Retorna
    -------
    dict
        Run de texto.
    """
    run = {"text": text}
    run.update(dict.fromkeys(fmt, True))
    run.update(extra)
    return run


def text_runs(text, fmt=frozenset()):
    """Lista com um run de texto, ou vazia se não houver texto (para .text/.tail ausentes)."""
    return [text_run(text, fmt)] if text else []


def bookmark_runs(node):
    """
    Marca (alvo de ``<xref>``) para o ``@id`` do elemento.

    Parâmetros
    ----------
    node : lxml.etree._Element or None
        Elemento que pode ter ``@id``.

    Retorna
    -------
    list of dict
        ``[{"bookmark": id}]``, ou lista vazia sem ``@id``. O render converte
        em ``<w:bookmarkStart/End>``, para onde aponta o link do ``<xref>``.
    """
    anchor = node.get("id") if node is not None else None
    return [{"bookmark": anchor}] if anchor else []


def has_content(runs):
    """True se há texto não vazio, fórmula ou imagem (quebra de linha ou marca sozinha não conta)."""
    return any(
        ("text" not in r and not r.get("break") and "bookmark" not in r)
        or r.get("text", "").strip()
        for r in runs
    )


def runs_text(runs):
    """Texto concatenado dos runs (fórmulas, imagens e marcas não contribuem)."""
    return "".join(r.get("text", "") for r in runs)


# -----------------
# Normalização de espaços
# -----------------


def _same_format(a, b):
    """True se os dois runs têm os mesmos formatos, link e estilo (podem ser unidos)."""
    return all(a.get(k) == b.get(k) for k in FLAGS + ("href", "anchor", "char_role"))


def _merge(runs):
    """Une runs de texto vizinhos com o mesmo formato; os demais são copiados."""
    merged = []
    for run in runs:
        if (
            "text" in run
            and merged
            and "text" in merged[-1]
            and _same_format(merged[-1], run)
        ):
            merged[-1] = {**merged[-1], "text": merged[-1]["text"] + run["text"]}
        else:
            merged.append(dict(run))
    return merged


def _fix_punctuation(text):
    """Remove espaço depois de "(" e "[" e antes de ")", "]", "," e ";"."""
    text = re.sub(r"([(\[])\s+", r"\1", text)
    return re.sub(r"\s+([)\],;])", r"\1", text)


def normalize(runs, preserve_space=False):
    """
    Limpa os espaços de uma sequência de runs.

    Parâmetros
    ----------
    runs : list of dict
        Runs na ordem do documento.
    preserve_space : bool, opcional
        Se True (texto pré-formatado), só junta runs vizinhos.

    Retorna
    -------
    list of dict
        Runs vizinhos de mesmo formato unidos, espaços colapsados (inclusive
        na fronteira entre runs), espaço junto a parênteses/vírgula
        corrigido e pontas de cada linha aparadas. Runs de texto vazios
        saem; fórmula, imagem, quebra e marca ficam.
    """
    runs = _merge(runs)
    if preserve_space:
        return [r for r in runs if r.get("text") != ""]
    last, last_run = "", None  # last == "": início de linha
    for run in runs:
        if run.get("break"):
            if last_run:
                last_run["text"] = last_run["text"].rstrip()
            last, last_run = "", None
            continue
        if "bookmark" in run:
            continue  # marca não ocupa espaço nem separa palavras
        if "text" not in run:
            last, last_run = "x", None
            continue
        text = _fix_punctuation(re.sub(r"\s+", " ", run["text"]))
        if last in ("", " ", "(", "["):
            text = text.lstrip()
        if text[:1] in ")],;" and last_run and last_run["text"].endswith(" "):
            last_run["text"] = last_run["text"].rstrip()
        run["text"] = text
        if text:
            last, last_run = text[-1], run
    if last_run:
        last_run["text"] = last_run["text"].rstrip()
    return [r for r in runs if r.get("text") != ""]
