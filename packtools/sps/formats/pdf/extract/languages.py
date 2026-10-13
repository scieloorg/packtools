"""
Um documento por idioma do texto, como o htmlgenerator (domain.HTMLGenerator):
o idioma principal (``article/@xml:lang``) e o de cada ``<sub-article
article-type="translation">``.

`document_for` devolve uma *visão* do documento: um dict com referências
aos nós originais que o compõem, sem copiar nem alterar o XML::

    {
        "root": <article>,
        "lang": "en",
        "meta": [filhos de article-meta, já com os do front-stub no lugar],
        "abstracts": [(<abstract>, "en"), (<abstract>, "pt"), ...],
        "kwd_groups": [(<kwd-group>, "en"), ...],
        "body": <body> ou None,
        "back_text": texto antes do primeiro filho do back,
        "back": [filhos de back, já com os da tradução no lugar],
        "sub_articles": [pareceres, respostas...],
        "ref_title": título das referências no idioma da tradução ou None,
    }

Para uma tradução:

- front: ``article/front``, valendo os elementos do ``front-stub`` onde
  existirem (título, autores, resumo, palavras-chave...);
- body: ``sub-article/body``;
- back: ``article/back`` (referências, apêndices...), valendo os elementos
  do ``sub-article/back`` onde existirem (agradecimentos e notas
  traduzidos); o título das referências herdadas vai para o idioma da
  tradução (``ref_title``);
- sub-articles (pareceres, respostas...): os da tradução, se ela tiver;
  senão, os do artigo.
"""

from itertools import chain

from packtools.sps.formats.pdf.extract.runs import tag
from packtools.sps.formats.pdf.config.labels import has_language, label

XML_LANG = "{http://www.w3.org/XML/1998/namespace}lang"
TRANSLATION = "translation"

# no front-stub, resumos e palavras-chave valem por idioma (e não por tag)
_BY_LANGUAGE = {"abstract", "trans-abstract", "kwd-group"}


def root_of(xml_tree):
    """O elemento ``<article>`` de uma árvore ou do próprio elemento."""
    return xml_tree.getroot() if hasattr(xml_tree, "getroot") else xml_tree


def _is_translation(node):
    """True para ``<sub-article article-type="translation">``."""
    return tag(node) == "sub-article" and node.get("article-type") == TRANSLATION


def translations(xml_tree):
    """Os ``<sub-article>`` de tradução, em qualquer nível, na ordem do documento."""
    return [s for s in root_of(xml_tree).iter("sub-article") if _is_translation(s)]


def languages(xml_tree):
    """
    Lista os idiomas do texto: o principal e o de cada tradução.

    Parâmetros
    ----------
    xml_tree : lxml.etree._ElementTree or lxml.etree._Element
        Artigo SPS.

    Retorna
    -------
    list of str
        Códigos de idioma sem repetição, o principal primeiro (mesma regra
        de ``HTMLGenerator.languages``).
    """
    root = root_of(xml_tree)
    found = [root.get(XML_LANG)] + [s.get(XML_LANG) for s in translations(root)]
    return list(dict.fromkeys(lang for lang in found if lang))


def document_for(xml_tree, lang=None):
    """
    Monta a visão do documento no idioma pedido.

    Parâmetros
    ----------
    xml_tree : lxml.etree._ElementTree or lxml.etree._Element
        Artigo SPS original (não é copiado nem alterado).
    lang : str, opcional
        Idioma desejado; None ou o idioma principal dá o artigo original.

    Retorna
    -------
    dict
        Visão do documento (ver o docstring do módulo). Os
        ``<sub-article>`` de tradução nunca entram: cada um é o próprio
        documento.

    Levanta
    -------
    ValueError
        Se ``lang`` não é o idioma principal nem o de uma tradução.
    """
    root = root_of(xml_tree)
    view = _main_view(root)
    if lang is None or lang == view["lang"]:
        return view
    sub_article = next((s for s in translations(root) if s.get(XML_LANG) == lang), None)
    if sub_article is None:
        raise ValueError(f"idioma não encontrado no XML: {lang!r} (disponíveis: {languages(root)})")
    return _translation_view(view, sub_article, lang)


def iter_tag(view, name):
    """
    Percorre todos os elementos ``name`` da visão, na ordem do documento.

    Parâmetros
    ----------
    view : dict
        Visão do documento.
    name : str
        Tag procurada.

    Retorna
    -------
    iterator of lxml.etree._Element
        Elementos encontrados no front, body, back e sub-articles da visão.
    """
    parts = view["meta"] + [view["body"]] + view["back"] + view["sub_articles"]
    return chain.from_iterable(part.iter(name) for part in parts if part is not None)


def _main_view(root):
    """Visão do artigo no idioma principal: os nós como estão no XML."""
    main_lang = root.get(XML_LANG)
    meta = root.find("front/article-meta")
    if meta is None:
        meta = root.find(".//article-meta")
    children = [c for c in meta if tag(c)] if meta is not None else []
    back = root.find("back")
    return {
        "root": root,
        "lang": main_lang,
        "meta": [c for c in children if tag(c) not in _BY_LANGUAGE],
        "abstracts": [(n, _abstract_lang(n, main_lang)) for n in _abstract_nodes(children)],
        "kwd_groups": [
            (n, n.get(XML_LANG) or main_lang) for n in children if tag(n) == "kwd-group"
        ],
        "body": root.find("body"),
        "back_text": back.text if back is not None else None,
        "back": [c for c in back if tag(c)] if back is not None else [],
        "sub_articles": [
            s for s in root.iter("sub-article")
            if not _is_translation(s) and not any(_is_translation(a) for a in s.iterancestors())
        ],
        "ref_title": None,
    }


def _translation_view(main, sub_article, lang):
    """
    Visão de uma tradução, composta da visão principal e do sub-article.

    Notas
    -----
    Resumos e palavras-chave valem por idioma: os do ``front-stub`` vêm
    primeiro (o resumo da tradução vira o principal) e os do artigo ficam,
    exceto os do mesmo tipo e idioma de um que a tradução traz. Os demais
    elementos valem por tag: os do ``front-stub`` (e do ``back`` da
    tradução) substituem todos os de mesma tag, na posição deles.
    """
    stub = sub_article.find("front-stub")
    if stub is None:
        stub = sub_article.find("front/article-meta")
    stub_children = [c for c in stub if tag(c)] if stub is not None else []
    stub_abstracts = [(n, _abstract_lang(n, lang)) for n in _abstract_nodes(stub_children)]
    stub_kwd_groups = [(n, n.get(XML_LANG) or lang) for n in stub_children if tag(n) == "kwd-group"]
    taken = {("abstract", l) for _, l in stub_abstracts} | {("kwd-group", l) for _, l in stub_kwd_groups}

    sub_back = sub_article.find("back")
    nested = [s for s in sub_article.findall("sub-article") if not _is_translation(s)]
    has_own_references = sub_back is not None and sub_back.find("ref-list") is not None
    return {
        **main,
        "lang": lang,
        "meta": _override(
            main["meta"], [c for c in stub_children if tag(c) not in _BY_LANGUAGE]
        ),
        "abstracts": stub_abstracts
        + [(n, l) for n, l in main["abstracts"] if ("abstract", l) not in taken],
        "kwd_groups": stub_kwd_groups
        + [(n, l) for n, l in main["kwd_groups"] if ("kwd-group", l) not in taken],
        "body": sub_article.find("body"),
        "back": _override(main["back"], [c for c in sub_back if tag(c)] if sub_back is not None else []),
        "sub_articles": nested or main["sub_articles"],
        # As referências não se traduzem e vêm do article/back, mas o título
        # delas ("REFERÊNCIAS") viria no idioma original. Só é trocado quando
        # há texto para o idioma em config/labels; senão, fica o do XML.
        "ref_title": label("references", lang)
        if not has_own_references and has_language(lang)
        else None,
    }


def _abstract_nodes(children):
    """``<abstract>`` seguidos de ``<trans-abstract>``, cada grupo na ordem do documento."""
    return [n for n in children if tag(n) == "abstract"] + [
        n for n in children if tag(n) == "trans-abstract"
    ]


def _abstract_lang(node, default):
    """Idioma do resumo: ``@xml:lang``; sem ele, ``default`` para ``<abstract>`` e vazio para ``<trans-abstract>``."""
    return node.get(XML_LANG) or (default if tag(node) == "abstract" else "")


def _override(original, replacements):
    """
    Lista de nós em que os de ``replacements`` substituem os de mesma tag.

    Parâmetros
    ----------
    original : list of lxml.etree._Element
        Nós do artigo.
    replacements : list of lxml.etree._Element
        Nós da tradução.

    Retorna
    -------
    list of lxml.etree._Element
        Os nós da tradução entram na posição do primeiro nó do artigo com a
        mesma tag (ou no fim, se o artigo não tinha aquela tag); os demais
        nós do artigo ficam. Nenhum nó é copiado nem movido.
    """
    by_tag = {}
    for node in replacements:
        by_tag.setdefault(tag(node), []).append(node)
    result, placed = [], set()
    for node in original:
        name = tag(node)
        if name not in by_tag:
            result.append(node)
        elif name not in placed:
            result += by_tag[name]
            placed.add(name)
    for name, nodes in by_tag.items():
        if name not in placed:
            result += nodes
    return result
