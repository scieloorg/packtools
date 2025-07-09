from packtools.sps.models import (
    journal_meta,
    front_articlemeta_issue,
    article_ids,
    article_contribs,
    aff,
    references,
    dates,
    article_and_subarticles,
    article_abstract,
    kwd_group,
    article_titles,
    funding_group,
)

from packtools.sps.formats.am.am_utils import (
    simple_field,
    complex_field,
    multiple_complex_field,
    format_date,
    ARTICLE_TYPE_MAP,
    generate_am_dict,
    simple_kv,
)


def get_journal(xml_tree):
    """
    Extrai e estrutura os dados do periódico no formato ArticleMeta.
    """

    # Obtenção dos valores do XML
    title = journal_meta.Title(xml_tree)
    journal_id = journal_meta.JournalID(xml_tree)
    try:
        publisher = journal_meta.Publisher(xml_tree).publishers_names[0]
    except IndexError:
        publisher = None
    issns = journal_meta.ISSN(xml_tree)

    # Lista de ISSNs (e-ISSN e p-ISSN)
    issn_types = [("epub", issns.epub), ("ppub", issns.ppub)]
    issn_list = [{"t": t, "_": val} for t, val in issn_types if val]

    # (campo ArticleMeta, valor, função geradora)
    fields = [
        ("v30", title.abbreviated_journal_title, simple_field),     # Título abreviado do periódico
        ("v421", journal_id.nlm_ta, simple_field),                  # Título Medline do periódico
        ("v62", publisher, simple_field),                           # Nome do editor
        ("v100", title.journal_title, simple_field),                # Título completo do periódico
        ("v435", issn_list, multiple_complex_field),                # Lista de ISSNs do periódico
    ]

    return generate_am_dict(fields)


def get_articlemeta_issue(xml_tree):
    """
    Extrai e estrutura os dados do fascículo no formato ArticleMeta.
    """

    # Obtenção dos valores do XML
    meta = front_articlemeta_issue.ArticleMetaIssue(xml_tree)
    abstracts = article_abstract.Abstract(xml_tree).get_abstracts_by_lang(style="inline")
    has_abstracts = bool(abstracts)

    fields = [
        ("e", meta.elocation_id, simple_kv),
        ("f", meta.fpage, simple_kv),
        ("l", meta.lpage, simple_kv),
        ("_", "", simple_kv),
    ]
    paginations_or_elocation = generate_am_dict(fields)

    # v42: total de páginas do artigo ou "1" caso elocation
    if meta.fpage and meta.lpage:
        try:
            pages = str(int(meta.lpage) - int(meta.fpage) + 1)
        except ValueError:
            pages = "1"
    else:
        pages = "1"

    # (campo ArticleMeta, valor, função geradora)
    fields = [
        ("v121", meta.order_string_format, simple_field), # ordem do artigo no fascículo
        ("v31", meta.volume, simple_field), # volume
        ("v14", paginations_or_elocation if paginations_or_elocation else None, complex_field), # elocation-id ou paginação
        ("v709", "article" if has_abstracts else "text", simple_field), # tipo de conteúdo
        ("v42", pages, simple_field),  # tipo de conteúdo
        ("v701", "1", simple_field),  # Número sequencial por tipo de registro
        # fixme: definir a obtenção do valor de v701

    ]

    return generate_am_dict(fields)


def get_ids(xml_tree):
    """
    Extrai e estrutura os identificadores do artigo no formato ArticleMeta.
    """
    ids = article_ids.ArticleIds(xml_tree)

    # (campo ArticleMeta, valor, função geradora)
    fields = [
        ("v237", ids.doi, simple_field), # DOI
    ]

    return generate_am_dict(fields)


def get_contribs(xml_tree):
    """
    Extrai e estrutura os dados dos autores no formato ArticleMeta.
    """
    contribs = article_contribs.XMLContribs(xml_tree).contribs
    contribs_list = [build_contrib(author) for author in contribs if build_contrib(author)]
    return multiple_complex_field("v10", contribs_list)


def build_contrib(author):
    """
    Constrói o dicionário v10 para um autor no formato ArticleMeta.
    """
    author_type = author.get("contrib_type", "ND")
    if author_type == "author":
        author_type = "ND"

    affs = author.get("affs", [])
    aff_id = affs[0].get("id") if affs else None

    # (campo ArticleMeta, valor, função geradora)
    fields = [
        ("k", author.get("contrib_ids", {}).get("orcid"), simple_kv),  # ORCID
        ("n", author.get("contrib_name", {}).get("given-names"), simple_kv),  # prenome
        ("1", aff_id, simple_kv),  # id da afiliação
        ("s", author.get("contrib_name", {}).get("surname"), simple_kv),  # sobrenome
        ("r", author_type, simple_kv),  # tipo de contribuição
        ("_", "", simple_kv)
    ]

    return generate_am_dict(fields)


def get_affs(xml_tree):
    """
    Extrai e estrutura os dados das afiliações no formato ArticleMeta.
    """
    affiliations = aff.Affiliation(xml_tree).affiliation_list

    list_full_affs = []
    list_short_affs = []

    for item in affiliations:
        if item.get("parent") != "article":
            continue

        # v70: afiliação detalhada
        fields_full_affs = [
            ("c", item.get("city"), simple_kv),                # cidade
            ("i", item.get("id"), simple_kv),                  # id afiliação
            ("l", item.get("label"), simple_kv),               # label
            ("d", item.get("orgdiv"), simple_kv),              # orgdiv(v. 2.x/3.0)
            ("1", item.get("orgdiv1"), simple_kv),             # orgdiv1
            ("2", item.get("orgdiv2"), simple_kv),             # orgdiv2
            ("3", item.get("orgdiv3"), simple_kv),             # orgdiv3
            ("p", item.get("country_name"), simple_kv),        # país (nome)
            ("s", item.get("state"), simple_kv),               # estado
            ("e", item.get("email"), simple_kv),               # e-mail
            ("_", item.get("orgname"), simple_kv),             # nome da organização
        ]
        full_affs = generate_am_dict(fields_full_affs)
        if full_affs:
            list_full_affs.append(full_affs)

        # v240: afiliação reduzida (com código do país)
        fields_short_affs = [
            ("c", item.get("city"), simple_kv),                # cidade
            ("i", item.get("id"), simple_kv),                  # id afiliação
            ("p", item.get("country_code"), simple_kv),        # país (código)
            ("s", item.get("state"), simple_kv),               # estado
            ("_", item.get("orgname"), simple_kv),             # nome da organização
        ]
        short_affs = generate_am_dict(fields_short_affs)
        if short_affs:
            list_short_affs.append(short_affs)

    return {
        **multiple_complex_field("v70", list_full_affs),
        **multiple_complex_field("v240", list_short_affs),
    }


def count_references(xml_tree):
    refs = list(references.XMLReferences(xml_tree).items)
    return str(len(refs))


def extract_authors(all_authors):
    """
    Extrai e estrutura os dados simplificados dos autores no formato ArticleMeta (v10).
    """
    authors_list = []

    for author in all_authors or []:
        name = author.get("given-names") or None
        surname = author.get("surname") or None
        fields = [
            ("n", name, simple_kv),     # prenome
            ("s", surname, simple_kv),         # sobrenome
            ("r", author.get("role", "ND"), simple_kv),      # tipo de contribuição
            ("_", "", simple_kv),                            # campo vazio obrigatório
        ]

        authors = generate_am_dict(fields)
        if name or surname:
            authors_list.append(authors)

    return authors_list


def format_page_range(fpage, lpage):
    if fpage and lpage:
        return f"{fpage}-{lpage}"
    return fpage or lpage or ""


def get_dates(xml_tree):
    """
    Extrai e estrutura as datas do artigo no formato ArticleMeta.
    """
    dt = dates.ArticleDates(xml_tree)

    accepted_date = format_date(dt.history_dates_dict.get("accepted"), ["year", "month", "day"])
    received_date = format_date(dt.history_dates_dict.get("received"), ["year", "month", "day"])
    collection_year = f"{format_date(dt.collection_date, ['year'])}0000" if dt.collection_date else None
    epub_date = format_date(dt.epub_date, ["year", "month", "day"])

    fields = [
        ("v114", accepted_date, simple_field),
        ("v112", received_date, simple_field),
        ("v65", collection_year, simple_field),
        ("v223", epub_date, simple_field),
    ]

    return generate_am_dict(fields)


def get_article_and_subarticle(xml_tree):
    """
    Extrai e estrutura os dados do artigo e subartigos no formato ArticleMeta.
    """
    articles = article_and_subarticles.ArticleAndSubArticles(xml_tree)
    article_type = articles.main_article_type
    mapped_article_type = ARTICLE_TYPE_MAP.get(article_type)  # tipo do artigo (mapeado)

    # Idiomas secundários (v601)
    other_langs = [
        {"_": lang}
        for item in articles.data
        if (lang := item.get("lang")) and lang != articles.main_lang
    ]

    # DOIs por idioma (v337)
    doi_list = [
        {"d": item["doi"], "l": item["lang"], "_": ""}
        for item in articles.data
        if item.get("doi") and item.get("lang")
    ]

    fields = [
        ("v40", articles.main_lang, simple_field),
        ("v120", f"XML_{articles.dtd_version}" if articles.dtd_version else None, simple_field),
        ("v71", mapped_article_type, simple_field),
        ("v601", other_langs if other_langs else None, multiple_complex_field),
        ("v337", doi_list if doi_list else None, multiple_complex_field),
    ]

    return generate_am_dict(fields)


def get_article_abstract(xml_tree):
    """
    Extrai e estrutura os resumos do artigo no formato ArticleMeta.
    """
    abstracts = article_abstract.Abstract(xml_tree).get_abstracts_by_lang(style="inline")

    abstract_list = [
        {"a": abstract, "l": lang, "_": ""}
        for lang, abstract in abstracts.items()
        if abstract
    ]

    if abstract_list:
        return multiple_complex_field("v83", abstract_list)
    return {}


def get_keyword(xml_tree):
    """
    Extrai e estrutura as palavras-chave do artigo no formato ArticleMeta.
    """
    keywords = kwd_group.ArticleKeywords(xml_tree)
    keywords.configure()

    kw_list = [
        {"k": kw.get("plain_text"), "l": kw.get("lang"), "_": ""}
        for kw in keywords.items
        if kw.get("plain_text")
    ]

    if kw_list:
        return multiple_complex_field("v85", kw_list)
    return {}


def get_title(xml_tree):
    """
    Extrai e estrutura os títulos do artigo no formato ArticleMeta.
    """
    titles = article_titles.ArticleTitles(xml_tree).article_title_list

    title_list = [
        {"l": item.get("lang"), "_": item.get("plain_text")}
        for item in titles
        if item.get("plain_text")
    ]

    if title_list:
        return multiple_complex_field("v12", title_list)
    return {}


def get_funding(xml_tree):
    """
    Extrai e estrutura os dados de financiamento do artigo no formato ArticleMeta.
    """
    funding = funding_group.FundingGroup(xml_tree)

    statement = funding.funding_statement

    # v58: órgãos financiadores do artigo.
    sponsors = [{"_": sponsor} for sponsor in funding.funding_sources]

    fields = [
        ("v102", statement, simple_field),
        ("v58", sponsors, simple_kv)
    ]

    return generate_am_dict(fields)


def get_external_article_data(external_article_data=None):
    """
    Geração dos campos externos do ArticleMeta a partir dos dados fornecidos.
    """
    external_article_data = external_article_data or {}

    # v265: Dados complementares de processamento do XML: real (data real), expected (data esperada).
    processing_dates_list = [
        {"k": item["k"], "s": item["s"], "v": item["v"], "_": ""}
        for item in external_article_data.get("v265", [])
        if all(k in item for k in ("k", "s", "v"))
    ]

    # v936: Identificador composto do fascículo: inclui ISSN (i), ano (y), ordem no ano (o).
    composite_issue_id = external_article_data.get("v936")
    composite_issue_id_valid = (
        composite_issue_id
        if isinstance(composite_issue_id, dict) and all(k in composite_issue_id for k in ("i", "y", "o"))
        else None
    )

    # v38: tipo de ilustrações ou recursos visuais existentes no artigo.
    elements_type = [{"_": item} for item in external_article_data.get("v38") or []]

    fields = [
        ("v38", elements_type, simple_kv),  # Tipo de elemento presente no artigo
        ("v49", external_article_data.get("v49"), simple_field),  # Código interno de status
        ("v700", external_article_data.get("v700"), simple_field),  # Ordem no processamento
        ("v91", external_article_data.get("v91"), simple_field),  # Data de processamento (AAAAMMDD)
        ("v265", processing_dates_list if processing_dates_list else None, multiple_complex_field),  # Datas de processamento
        ("applicable", external_article_data.get("applicable"), simple_kv),  # Flag se o registro é aplicável
        ("created_at", external_article_data.get("created_at"), simple_kv),  # Data de criação
        ("processing_date", external_article_data.get("processing_date"), simple_kv),  # Data de processamento
        ("v35", external_article_data.get("v35"), simple_field),  # ISSN impresso
        ("v42", external_article_data.get("v42"), simple_field),  # Status do fascículo
    ]

    return generate_am_dict(fields)


def get_external_common_data(external_article_data=None):
    """
    Gera os campos externos comuns usados nas referências de artigo no ArticleMeta.
    """
    external_article_data = external_article_data or {}

    fields = [
        ("collection", external_article_data.get("collection"), simple_kv),  # Nome da coleção
        ("v2", external_article_data.get("v2"), simple_field),               # Identificador de controle
        ("v3", external_article_data.get("v3"), simple_field),               # Caminho relativo do XML
        ("v705", external_article_data.get("v705"), simple_field),           # Tipo do registro (S = artigo)
        ("v936", external_article_data.get("v936"), complex_field),          # Identificador composto (ISSN, ano, ordem)
        ("v992", external_article_data.get("v992"), simple_field),              # Código da coleção
        ("v999", external_article_data.get("v999"), simple_field),              # Dados internos
        ("v702", external_article_data.get("v702"), simple_field),           # Caminho completo do XML
    ]

    return generate_am_dict(fields)


def get_external_citation_data(external_citation_data):
    """
    Gera os campos externos comuns usados nas citações no ArticleMeta.
    """

    fields = [
        ("processing_date", external_citation_data.get("processing_date"), simple_kv),  # Data de processamento das citações
        ("v700", external_citation_data.get("v700"), simple_field)
    ]

    return generate_am_dict(fields)


def get_xml_common_data(xml_tree):
    # Obtenção dos valores do XML
    ids = article_ids.ArticleIds(xml_tree)
    meta = front_articlemeta_issue.ArticleMetaIssue(xml_tree)

    fields = [
        ("v", meta.volume, simple_kv),
        ("n", meta.number, simple_kv),
        ("_", "", simple_kv)
    ]
    volume_and_number = generate_am_dict(fields)

    # (campo comum, valor, função geradora)
    fields = [
        ("code", ids.v2, simple_kv),  # código SciELO no dicionário direto
        ("v882", volume_and_number if volume_and_number else None, complex_field),  # volume e número do fascículo
        ("v880", ids.v2, simple_field),  # código SciELO no campo v880
        ("v4", f"V{meta.volume}" if meta.volume else None, simple_field),  # volume formatado
    ]

    return generate_am_dict(fields)


def get_xml_article_metadata(xml_tree):
    """
    Gera os metadados do artigo no formato ArticleMeta.
    """

    return {
        **get_journal(xml_tree),
        **get_contribs(xml_tree),
        **get_affs(xml_tree),
        **simple_field("v72", count_references(xml_tree)),
        **get_article_and_subarticle(xml_tree),
        **get_article_abstract(xml_tree),
        **get_keyword(xml_tree),
        **get_title(xml_tree),
        **get_ids(xml_tree),
        **get_dates(xml_tree),
        **get_articlemeta_issue(xml_tree),
        **get_funding(xml_tree),
        **simple_field("v708", "1"), # Qtd de registros do tipo atual
        **simple_field("v706", "h"),  # Tipo de registro
    }


def get_xml_citation_data(ref):
    citation_title = ref.get("article_title") or ref.get("chapter_title") or ref.get("part_title")
    fields = [
        ("v118", ref.get("label"), simple_field),  # rótulo da citação
        ("v12", citation_title, simple_field),  # título do artigo citado
        ("v31", ref.get("volume"), simple_field),  # volume citado
        ("v32", ref.get("issue"), simple_field),  # número citado
        ("v37", ref.get("mixed_citation_xlink"), simple_field),  # link do DOI da citação
        ("v71", ref.get("publication_type"), simple_field),  # tipo de publicação
        ("v14", format_page_range(ref.get("fpage"), ref.get("lpage")), simple_field), # intervalo de páginas
        ("v64", format_date(ref, ["year"]), simple_field),  # ano da publicação da referência
        ("v65", f"{format_date(ref, ["year"])}0000", simple_field),  # ano + '0000'
        ("v10", extract_authors(ref.get("all_authors")), multiple_complex_field), # autores da citação
        ("v514", {"l": ref.get("lpage"), "f": ref.get("fpage"), "_": ""}, complex_field), # paginação
        ("v237", ref.get("citation_ids", {}).get("doi"), simple_field),  # DOI
        ("v17", ref.get("collab")[0] if ref.get("collab") else None, simple_field), # Autor institucional (corporativo)
        ("v62", ref.get("publisher_name"), simple_field),  # Nome do editor
        ("v66", ref.get("publisher_loc"), simple_field),  # Localização do editor
    ]

    if ref.get("publication_type") == "journal":
        fields.append(("v30", ref.get("source"), simple_field)) # Título de obra seriada
    else:
        fields.append(("v18", ref.get("source"), simple_field)) # Título de obra não seriada

    return generate_am_dict(fields)


def build(xml_tree, external_data=None):
    """
    Gera o dicionário completo do ArticleMeta no formato final.
    """
    external_data = external_data or {}

    # Extrai e formata dados externos do artigo
    external_article_data = get_external_article_data(external_data)

    # Extrai e formata dados externos comuns ao artigo e às citações
    external_common_data = get_external_common_data(external_data)

    # Extrai e formata dados do XML comuns ao artigo e às citações
    xml_common_data = get_xml_common_data(xml_tree)

    # Extrai metadados do artigo no formato AM
    article_metadata = get_xml_article_metadata(xml_tree)
    article_metadata.update(xml_common_data)
    article_metadata.update(external_article_data)
    article_metadata.update(external_common_data)

    # Extrai metadados das citações no formato AM
    citations_number = count_references(xml_tree)

    # Extrai dados externos das citações
    external_citations_data_list = external_data.get("external_citation_data") or []

    citations_data = []
    for idx, ref in enumerate(references.XMLReferences(xml_tree).items, start=1):
        # Formata dados externos das citações
        try:
            external_citation_data = get_external_citation_data(external_citations_data_list[idx - 1])
        except IndexError:
            external_citation_data = {}

        citation_data = get_xml_citation_data(ref)
        citation_data.update(external_citation_data)
        citation_data.update(external_common_data)
        citation_data.update(xml_common_data)

        # Formata code e v880 específicos para as citações
        base_v880 = citation_data.get("v880")[0]["_"] if citation_data.get("v880") else None
        if base_v880:
            citation_v880 = f"{base_v880}{idx:05d}"
            citation_data["v880"] = [{"_": citation_v880}]
            citation_data["code"] = citation_v880

        citation_data["v865"] = article_metadata.get("v65") # Data do artigo
        citation_data.update(simple_field("v701", str(idx))) # Número sequencial por tipo de registro
        citation_data.update(simple_field("v708", citations_number)) # Número de citações do artigo
        citation_data.update(simple_field("v706", "c"))  # Tipo de registro

        citations_data.append(citation_data)

    fields = [
        ("article", article_metadata, simple_kv),
        ("citations", citations_data, simple_kv),
    ]

    return generate_am_dict(fields)
