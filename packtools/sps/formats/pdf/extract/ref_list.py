"""
Referências bibliográficas: ``<ref-list>`` e ``<ref>``.
"""

from packtools.sps.formats.pdf.extract.flow import paragraph
from packtools.sps.formats.pdf.extract.inline import inlines, plain_text
from packtools.sps.formats.pdf.extract.registry import block_handler
from packtools.sps.formats.pdf.extract.runs import normalize, runs_text, text_run
from packtools.sps.formats.pdf.extract.sec import handle_section
from packtools.sps.formats.pdf.extract.title import label_of
from packtools.sps.formats.pdf.config.labels import label


# -----------------
# ``<ref-list>``: lista de referências bibliográficas (cada ``<ref>`` abaixo).
# -----------------


@block_handler("ref-list")
def handle_ref_list(node, ctx):
    """
    Converte a lista de referências.

    Parâmetros
    ----------
    node : lxml.etree._Element
        ``<ref-list>``.
    ctx : dict
        Contexto; ``ctx["ref_title"]`` substitui o título do XML (tradução
        com referências herdadas do artigo, ver languages.py).

    Retorna
    -------
    list of dict
        Título e uma referência por parágrafo. Sem ``<title>``, o título
        padrão é "References" no idioma do documento.
    """
    return handle_section(
        node, ctx, default_title=label("references", ctx["lang"]), title=ctx["ref_title"]
    )


# -----------------
# ``<ref>``: uma referência bibliográfica.
# -----------------


@block_handler("ref")
def handle_ref(node, ctx):
    """
    Converte uma referência em parágrafo.

    Parâmetros
    ----------
    node : lxml.etree._Element
        ``<ref>``.
    ctx : dict
        Contexto.

    Retorna
    -------
    list of dict
        Parágrafo com ``role="reference"``, ou lista vazia sem conteúdo.

    Notas
    -----
    O texto vem do ``<mixed-citation>``, que traz a referência já formatada
    pelo editor; ``<element-citation>`` (os mesmos dados, estruturados) é
    ignorado. Uma ``<ref>`` sem ``<mixed-citation>`` cai no texto dos demais
    filhos, sem formatação, para não perder a referência. O ``<label>`` só é
    preposto quando a citação ainda não começa por ele.
    """
    citations = node.findall("mixed-citation")
    label = label_of(node)
    runs = []
    for citation in citations or [node]:
        if runs:
            runs.append(text_run(" "))
        runs += inlines(citation) if citations else inlines(citation, skip=[label])
    label_text = plain_text(label)
    if label_text and not runs_text(normalize(runs)).lstrip().startswith(label_text):
        separator = ". " if label_text[-1:].isalnum() else " "
        runs = [text_run(f"{label_text}{separator}")] + runs
    runs = drop_unmatched_open_parentheses(normalize(runs))
    # Herdado do old_pdf: toda referência termina com ponto final.
    if runs and runs[-1].get("text") and not runs[-1]["text"].endswith("."):
        runs[-1]["text"] += "."
    return paragraph(runs, ctx, role="reference")


def drop_unmatched_open_parentheses(runs):
    """
    Tira o "(" repetido de "((" quando a referência tem "(" sem par.

    Parâmetros
    ----------
    runs : list of dict
        Runs normalizados da referência.

    Retorna
    -------
    list of dict
        Os mesmos runs (alterados no lugar), com até N "(" removidos, N =
        quantidade de "(" sem ")" correspondente; só o primeiro de cada "(("
        sai, o que vale também entre runs ("(" no fim de um run, "(" no
        início do seguinte).

    Notas
    -----
    Herdado do old_pdf (_remove_unmatched_open_parentheses): o editor às
    vezes envolve com parênteses um ``<comment>`` que já começa por "(",
    e a referência saía "versão 1.2. ((URL)".
    """
    text_runs = [r for r in runs if "text" in r]
    joined = "".join(r["text"] for r in text_runs)
    extra = joined.count("(") - joined.count(")")
    for i, run in enumerate(text_runs):
        if extra <= 0:
            break
        following = "".join(r["text"] for r in text_runs[i + 1:])
        chars = list(run["text"])
        for j in range(len(chars)):
            after = "".join(chars[j + 1:]) + following
            if extra > 0 and chars[j] == "(" and after.startswith("("):
                chars[j] = ""
                extra -= 1
        run["text"] = "".join(chars)
    return [r for r in runs if "text" not in r or r["text"]]
