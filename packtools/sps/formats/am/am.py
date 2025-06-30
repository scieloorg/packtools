from packtools.sps.models import (
    journal_meta,
    front_articlemeta_issue,
    article_ids,
    article_contribs,
    aff,
    references,
    article_dates,
    article_and_subarticles,
    article_abstract,
    kwd_group,
    article_titles,
)

from packtools.sps.formats.am.am_utils import (
    simple_field,
    complex_field,
    multiple_complex_field,
    add_item,
    format_date,
    ARTICLE_TYPE_MAP,
    extract_first_text,
)


def get_journal(xml_tree):
    """
    Dados do periódico.
    """
    title = journal_meta.Title(xml_tree)
    journal_id = journal_meta.JournalID(xml_tree)
    publisher = journal_meta.Publisher(xml_tree)
    issns = journal_meta.ISSN(xml_tree)

    issn_list = [
        {"t": t, "_": val}
        for t, val in {"epub": issns.epub, "ppub": issns.ppub}.items()
        if val
    ]

    publisher_name = (
        publisher.publishers_names[0] if publisher.publishers_names else None
    )

    response = {}
    if title.abbreviated_journal_title:
        response.update(
            simple_field("v30", title.abbreviated_journal_title)
        )  # título abreviado

    if journal_id.nlm_ta:
        response.update(simple_field("v421", journal_id.nlm_ta))  # título Medline

    if publisher_name:
        response.update(simple_field("v62", publisher_name))  # nome do editor

    if title.journal_title:
        response.update(
            simple_field("v100", title.journal_title)
        )  # título da publicação

    if issn_list:
        response.update(multiple_complex_field("v435", issn_list))  # ISSNs

    return response


def get_articlemeta_issue(xml_tree):
    """
    Dados do fascículo.
    """
    meta = front_articlemeta_issue.ArticleMetaIssue(xml_tree)
    abstracts = article_abstract.Abstract(xml_tree).get_abstracts_by_lang(
        style="inline"
    )
    has_abstracts = bool(abstracts)

    v882 = {}
    if meta.volume:
        add_item(v882, "v", meta.volume)  # volume
    if meta.number:
        add_item(v882, "n", meta.number)  # número
    if v882:
        add_item(v882, "_", "")

    v14 = {}
    if meta.elocation_id:
        add_item(v14, "e", meta.elocation_id)  # elocation-id
    if meta.fpage:
        add_item(v14, "f", meta.fpage)  # página inicial
    if meta.lpage:
        add_item(v14, "l", meta.lpage)  # página final
    if v14:
        add_item(v14, "_", "")

    result = {}

    if meta.order_string_format:
        result.update(simple_field("v121", meta.order_string_format))  # ordem

    if v882:
        result.update(complex_field("v882", v882))  # volume e número

    if v14:
        result.update(complex_field("v14", v14))  # localização (elocation/page)

    if meta.volume:
        result.update(simple_field("v31", meta.volume))  # volume
        result.update(simple_field("v4", f"V{meta.volume}"))  # volume formatado

    result.update(
        simple_field("v709", "article" if has_abstracts else "text")
    )  # tipo de conteúdo
    return result


def get_ids(xml_tree):
    """
    Identificadores do artigo.
    """
    ids = article_ids.ArticleIds(xml_tree)
    result = {}

    if ids.v2:
        result["code"] = ids.v2
        result.update(simple_field("v880", ids.v2))  # código SciELO

    if ids.doi:
        result.update(simple_field("v237", ids.doi))  # DOI

    return result


def get_contribs(xml_tree):
    """
    Dados dos autores.
    """
    contribs = article_contribs.XMLContribs(xml_tree).contribs
    list_contribs = [
        build_v10_contrib(author) for author in contribs if build_v10_contrib(author)
    ]
    return multiple_complex_field("v10", list_contribs)


def build_v10_contrib(author):
    """
    Constrói o dicionário v10 para um autor.
    """
    author_type = author.get("contrib_type", "ND")
    if author_type == "author":
        author_type = "ND"

    affs = author.get("affs", [])
    aff_id = affs[0].get("id") if affs else None

    v10 = {}

    orcid = author.get("contrib_ids", {}).get("orcid")
    if orcid:
        add_item(v10, "k", orcid)  # ORCID

    given_names = author.get("contrib_name", {}).get("given-names")
    if given_names:
        add_item(v10, "n", given_names)  # prenome

    if aff_id:
        add_item(v10, "1", aff_id)  # afiliação (id)

    surname = author.get("contrib_name", {}).get("surname")
    if surname:
        add_item(v10, "s", surname)  # sobrenome

    if author_type:
        add_item(v10, "r", author_type)  # tipo de contribuição

    if v10:
        add_item(v10, "_", "")
        return v10

    return None


def get_affs(xml_tree):
    """
    Dados das afiliações.
    """
    affiliations = aff.Affiliation(xml_tree).affiliation_list
    list_v70 = []
    list_v240 = []

    for item in affiliations:
        if item.get("parent") != "article":
            continue

        v70 = {}
        city = item.get("city")
        if city:
            add_item(v70, "c", city)  # cidade

        aff_id = item.get("id")
        if aff_id:
            add_item(v70, "i", aff_id)  # id afiliação

        label = item.get("label")
        if label:
            add_item(v70, "l", label)  # label

        orgdiv1 = item.get("orgdiv1")
        if orgdiv1:
            add_item(v70, "1", orgdiv1)  # divisão

        country_name = item.get("country_name")
        if country_name:
            add_item(v70, "p", country_name)  # país (nome)

        state = item.get("state")
        if state:
            add_item(v70, "s", state)  # estado

        orgname = item.get("orgname")
        if orgname:
            add_item(v70, "_", orgname)  # nome da organização

        if v70:
            list_v70.append(v70)

        v240 = {}
        if city:
            add_item(v240, "c", city)  # cidade

        if aff_id:
            add_item(v240, "i", aff_id)  # id afiliação

        country_code = item.get("country_code")
        if country_code:
            add_item(v240, "p", country_code)  # país (código)

        if state:
            add_item(v240, "s", state)  # estado

        if orgname:
            add_item(v240, "_", orgname)  # nome da organização

        if v240:
            list_v240.append(v240)

    return {
        **multiple_complex_field("v70", list_v70),
        **multiple_complex_field("v240", list_v240),
    }


def count_references(xml_tree):
    refs = list(references.XMLReferences(xml_tree).items)
    return simple_field("v72", str(len(refs)))


def extract_authors(all_authors):
    """
    Dados simplificados dos autores.
    """
    v10_list = []

    for author in all_authors or []:
        v10 = {}

        given_names = author.get("given-names")
        if given_names:
            add_item(v10, "n", given_names)  # prenome

        surname = author.get("surname")
        if surname:
            add_item(v10, "s", surname)  # sobrenome

        role = author.get("role", "ND")
        if role:
            add_item(v10, "r", role)  # tipo de contribuição

        if v10:
            add_item(v10, "_", "")
            v10_list.append(v10)

    return v10_list


def format_page_range(fpage, lpage):
    if fpage and lpage:
        return f"{fpage}-{lpage}"
    return fpage or lpage or ""


def get_dates(xml_tree):
    """
    Datas do artigo.
    """
    dates = article_dates.ArticleDates(xml_tree)

    v114 = format_date(
        dates.history_dates_dict.get("accepted"), ["year", "month", "day"]
    )  # v114 = data de aceite
    v112 = format_date(
        dates.history_dates_dict.get("received"), ["year", "month", "day"]
    )  # v112 = data de recebimento
    v65 = (
        format_date(dates.collection_date, ["year"]) + "0000"
        if dates.collection_date
        else None
    )  # v65 = ano de coleção (complementado com zeros)
    v223 = format_date(
        dates.epub_date, ["year", "month", "day"]
    )  # v223 = data de publicação eletrônica

    result = {}

    if v114:
        result.update(simple_field("v114", v114))  # data de aceite
    if v112:
        result.update(simple_field("v112", v112))  # data de recebimento
    if v65:
        result.update(simple_field("v65", v65))  # ano de coleção
    if v223:
        result.update(simple_field("v223", v223))  # data de publicação eletrônica

    return result


def get_article_and_subarticle(xml_tree):
    """
    Dados do artigo e subartigos.
    """
    articles = article_and_subarticles.ArticleAndSubArticles(xml_tree)
    article_type = articles.main_article_type
    v71_value = ARTICLE_TYPE_MAP.get(article_type)  # tipo do artigo (mapeado)

    result = {}

    if articles.main_lang:
        result.update(simple_field("v40", articles.main_lang))  # idioma principal

    if articles.dtd_version:
        result.update(simple_field("v120", f"XML_{articles.dtd_version}"))  # versão DTD

    if v71_value:
        result.update(simple_field("v71", v71_value))  # tipo do artigo

    # v601 = idiomas secundários
    other_langs = [
        {"_": lang}
        for item in articles.data
        if (lang := item.get("lang")) and lang != articles.main_lang
    ]
    if other_langs:
        result.update(multiple_complex_field("v601", other_langs))

    # v337 = DOI + idioma
    doi_list = [
        {"d": item["doi"], "l": item["lang"], "_": ""}
        for item in articles.data
        if item.get("doi") and item.get("lang")
    ]
    if doi_list:
        result.update(multiple_complex_field("v337", doi_list))

    return result


def get_article_abstract(xml_tree):
    """
    Geração dos resumos (abstracts) do artigo, agrupados por idioma.
    """
    abstracts = article_abstract.Abstract(xml_tree).get_abstracts_by_lang(
        style="inline"
    )
    result = {}

    list_abs = []
    for lang, abstract in abstracts.items():
        if abstract:
            item = {"a": abstract, "l": lang, "_": ""}
            list_abs.append(item)

    if list_abs:
        result.update(multiple_complex_field("v83", list_abs))

    return result


def get_keyword(xml_tree):
    """
    Geração das palavras-chave (keywords) do artigo, agrupadas por idioma.
    """
    keywords = kwd_group.ArticleKeywords(xml_tree)
    keywords.configure()

    result = {}
    list_kw = []

    for kw in keywords.items:
        plain_text = kw.get("plain_text")
        lang = kw.get("lang")

        if plain_text:
            item = {"k": plain_text, "l": lang, "_": ""}
            list_kw.append(item)

    if list_kw:
        result.update(multiple_complex_field("v85", list_kw))

    return result


def get_title(xml_tree):
    """
    Geração dos títulos do artigo, agrupados por idioma.
    """
    titles = article_titles.ArticleTitles(xml_tree).article_title_list
    result = {}
    v12_list = []

    for item in titles:
        plain_text = item.get("plain_text")
        lang = item.get("lang")

        if plain_text:
            v12_item = {"l": lang, "_": plain_text}
            v12_list.append(v12_item)

    if v12_list:
        result.update(multiple_complex_field("v12", v12_list))

    return result


def get_external_fields(external_article_data=None):
    """
    Geração dos campos externos do ArticleMeta a partir dos dados fornecidos.

    Parameters
    ----------
    external_article_data : dict, optional
        Dicionário contendo dados externos do artigo no formato ArticleMeta.

    Returns
    -------
    dict
        Campos formatados prontos para inclusão no ArticleMeta.

    Example
    -------
    external_article_data = {
        "v2": "S0034-8910(25)05900000202",       # identificador de controle do artigo
        "v3": "1518-8787-rsp-59-e2.xml",         # caminho relativo do XML
        "v38": "TAB",                            # tipo de elemento presente (ex.: tabela)
        "v49": "RSP940",                         # código interno de status/processamento
        "v700": "2",                             # ordem do registro no processamento
        "v702": "rsp/v59/1518-8787-rsp-59-e2.xml", # caminho completo do XML
        "v705": "S",                             # tipo de registro (S = artigo)
        "v706": "h",                             # subtipo do registro (h = artigo)
        "v708": "1",                             # contador de referências
        "v91": "20250328",                       # data de processamento no sistema
        "collection": "scl",                     # coleção
        "applicable": "True",                    # flag indicando se o registro é aplicável
        "processing_date": "2025-03-28",         # data de processamento
        "v35": [{"_": "0034-8910"}],             # ISSN impresso
        "v42": [{"_": "1"}],                     # status do fascículo
        "v701": [{"_": "1"}],                    # sequência de publicação
        "v992": [{"_": "scl"}],                  # coleção
        "v999": [{"_": "../bases-work/rsp/rsp"}],# dados internos do sistema
        "v265": [                                # dados complementares de processamento
            {"k": "real", "s": "xml", "v": "20250331"},     # data real de processamento do XML
            {"k": "expected", "s": "xml", "v": "202500"}    # data esperada de processamento
        ],
        "v936": {                                # identificador composto do fascículo
            "i": "0034-8910",                    # ISSN
            "y": "2025",                         # ano
            "o": "1"                             # ordem do fascículo no ano
        }
    }
    """
    external_article_data = external_article_data or {}
    result = {}

    # v265: dados complementares de processamento (ex.: data real e esperada do XML)
    v265_list = []
    for item in external_article_data.get("v265", []):
        if all(k in item for k in ("k", "s", "v")):
            v265_list.append(
                {
                    "k": item["k"],  # chave (ex.: real, expected)
                    "s": item["s"],  # subtipo/contexto (ex.: xml)
                    "v": item["v"],  # valor (ex.: data)
                }
            )
    if v265_list:
        result.update(multiple_complex_field("v265", v265_list))

    # v936: identificador composto (ISSN, ano, ordem do fascículo)
    v936 = external_article_data.get("v936")
    if isinstance(v936, dict) and all(k in v936 for k in ("i", "y", "o")):
        result.update(complex_field("v936", v936))

    # Campos simples de controle e identificadores
    simple_keys = [
        "v2",  # identificador de controle do artigo (ex.: S0034-8910(25)...)
        "v3",  # caminho relativo do XML
        "v38",  # tipos de elemento presentes (ex.: TAB, GRA)
        "v49",  # código interno de status/processamento
        "v700",  # ordem do registro no processamento
        "v702",  # caminho completo do XML
        "v705",  # tipo de registro (S = artigo, c = citação)
        "v706",  # subtipo do registro (ex.: h = artigo, c = citação)
        "v708",  # contador de referências
        "v91",  # data de processamento no sistema
    ]
    for key in simple_keys:
        value = external_article_data.get(key)
        if value is not None:
            result.update(simple_field(key, value))

    # Campos diretos: metadados gerais
    direct_keys = [
        "applicable",  # flag indicando se o registro é aplicável
        "collection",  # coleção
        "created_at",  # data de criação do registro
        "processing_date",  # data de processamento
        "v35",  # ISSN impresso
        "v42",  # status do fascículo
        "v701",  # sequência de publicação
        "v992",  # coleção
        "v999",  # dados internos do sistema
    ]
    for key in direct_keys:
        value = external_article_data.get(key)
        if value is not None:
            result[key] = value

    return result


def get_article_metadata(xml_tree, external_article_data=None):
    """
    Gera os metadados do artigo no formato ArticleMeta.
    """
    external_article_data = external_article_data or {}
    return {
        **get_journal(xml_tree),
        **get_articlemeta_issue(xml_tree),
        **get_ids(xml_tree),
        **get_contribs(xml_tree),
        **get_affs(xml_tree),
        **count_references(xml_tree),
        **get_dates(xml_tree),
        **get_article_and_subarticle(xml_tree),
        **get_article_abstract(xml_tree),
        **get_keyword(xml_tree),
        **get_title(xml_tree),
        **get_external_fields(external_article_data),
    }


def get_citations(xml_tree, external_article_data=None, external_citation_data=None):
    external_article_data = external_article_data or {}
    external_citation_data = external_citation_data or {}

    xml_data = {
        **get_ids(xml_tree),
        **get_dates(xml_tree),
        **get_articlemeta_issue(xml_tree),
        "v708": count_references(xml_tree).get(
            "v72"
        ),  # v708: número total de referências
    }

    v700_refs = external_citation_data.get(
        "v700", []
    )  # v700: ordem das referências

    xml_common = get_xml_data_common(xml_data)
    ext_article_common = get_external_article_data_common(external_article_data)

    # Dados fixos das citações
    base_citation_common = {}
    if processing_date := external_citation_data.get("processing_date"):
        base_citation_common["processing_date"] = (
            processing_date  # Data de processamento
        )

    refs = []
    for idx, ref in enumerate(references.XMLReferences(xml_tree).items, start=1):
        citation_common = base_citation_common.copy()
        v700 = v700_refs[idx - 1] if 0 <= idx - 1 < len(v700_refs) else None
        if v700:
            citation_common.update(
                simple_field("v700", v700)
            )  # v700: ordem das referências

        refs.append(
            build_citation(ref, xml_common, ext_article_common, citation_common, idx)
        )

    return refs


def get_xml_data_common(xml_data):
    result = {}
    if code := xml_data.get("code"):
        result["code"] = code  # Código do artigo (código único SciELO)
        result.update(simple_field("v880", code))  # v880: código base do artigo
    if v237 := xml_data.get("v237"):
        result["v237"] = v237  # v237: DOI do artigo
    if v4 := xml_data.get("v4"):
        result["v4"] = v4  # v4: volume do artigo
    if v65 := xml_data.get("v65"):
        result["v865"] = v65  # v865: data de publicação normalizada
    if v708 := xml_data.get("v708"):
        result["v708"] = v708  # v708: número total de referências
    if v882 := xml_data.get("v882"):
        result["v882"] = v882  # v882: reforço do volume
    result.update(simple_field("v706", "c"))  # v706: tipo de registro (citação)
    return result


def get_external_article_data_common(external_article_data):
    result = {}
    if collection := external_article_data.get("collection"):
        result["collection"] = collection  # Nome da coleção
    if v2 := external_article_data.get("v2"):
        result.update(simple_field("v2", v2))  # v2: identificador de controle
    if v3 := external_article_data.get("v3"):
        result.update(simple_field("v3", v3))  # v3: caminho relativo do XML
    if v701 := external_article_data.get("v701"):
        result["v701"] = v701  # v701: sequência de publicação
    if v705 := external_article_data.get("v705"):
        result.update(simple_field("v705", v705))  # v705: tipo do registro (S = artigo)
    if v936 := external_article_data.get("v936"):
        result.update(
            complex_field("v936", v936)
        )  # v936: identificador composto (ISSN, ano, ordem)
    if v992 := external_article_data.get("v992"):
        result["v992"] = v992  # v992: coleção
    if v999 := external_article_data.get("v999"):
        result["v999"] = v999  # v999: dados internos
    if v702 := external_article_data.get("v702"):
        result.update(simple_field("v702", v702))  # v702: caminho completo do XML
    return result


def get_external_citation_data_common(external_citation_data, idx, v700_refs):
    result = {}
    if processing_date := external_citation_data.get("processing_date"):
        result["processing_date"] = processing_date  # Data de processamento
    v700 = v700_refs[idx - 1] if 0 <= idx - 1 < len(v700_refs) else None
    if v700:
        result.update(simple_field("v700", v700))  # v700: ordem no arquivo externo
    return result


def build_citation(ref, xml_common, ext_article_common, ext_citation_common, idx):
    v64 = format_date(ref, ["year"])  # v64: ano da publicação da referência
    v65 = f"{v64}0000" if v64 else None  # v65: ano + '0000'
    v514 = {"l": ref.get("lpage"), "f": ref.get("fpage"), "_": ""}  # v514: paginação

    result = {}
    result.update(xml_common)
    result.update(ext_article_common)
    result.update(ext_citation_common)
    if code := xml_common.get("code"):
        result["code"] = f"{code}{idx:05d}"  # Código único da citação

    # Dados da citação (referência)
    ref_fields = [
        ("v118", "label"),  # v118: rótulo da citação
        ("v12", "article_title"),  # v12: título do artigo citado
        ("v30", "source"),  # v30: fonte (nome do periódico)
        ("v31", "volume"),  # v31: volume citado
        ("v32", "issue"),  # v32: número citado
        ("v37", "mixed_citation_xlink"),  # v37: DOI da citação
        ("v71", "publication_type"),  # v71: tipo de publicação
    ]
    for out_field, in_field in ref_fields:
        if value := ref.get(in_field):
            result.update(simple_field(out_field, value))

    if page_range := format_page_range(ref.get("fpage"), ref.get("lpage")):
        result.update(simple_field("v14", page_range))  # v14: intervalo de páginas
    if v64:
        result.update(simple_field("v64", v64))  # v64: ano citado
    if v65:
        result.update(simple_field("v65", v65))  # v65: ano citado + '0000'

    if authors := extract_authors(ref.get("all_authors")):
        result.update(multiple_complex_field("v10", authors))  # v10: autores da citação

    if v514["l"] or v514["f"]:
        result.update(complex_field("v514", v514))  # v514: paginação complexa

    return result


def build(xml_tree, external_article_data=None, external_citation_data=None):
    """
    Gera o dicionário completo do ArticleMeta no formato final.
    """
    external_article_data = external_article_data or {}
    external_citation_data = external_citation_data or {}

    # Extrai dados estruturais do artigo e citações
    article_metadata = get_article_metadata(xml_tree, external_article_data)
    citations = get_citations(xml_tree, external_article_data, external_citation_data)
    journal_data = get_journal(xml_tree)
    external_fields = get_external_fields(external_article_data)
    article_type = article_and_subarticles.ArticleAndSubArticles(
        xml_tree
    ).main_article_type

    # Extração de dados calculados
    publication_date = extract_first_text(
        article_metadata.get("v65")
    )  # data principal de publicação
    publication_year = publication_date[:4] if publication_date else None
    doi = extract_first_text(article_metadata.get("v237"))  # DOI principal
    code = article_metadata.get("code")  # código de controle do artigo
    code_issue = code[1:18] if code and len(code) >= 18 else None  # código do fascículo

    # Lista de ISSNs coletados
    issns = [
        item.get("_")
        for item in external_article_data.get("v35", []) + journal_data.get("v435", [])
        if isinstance(item, dict) and item.get("_")
    ]

    result = {}

    # Dados gerais do documento
    if external_fields.get("collection"):
        result["collection"] = external_fields.get("collection")
    if external_fields.get("applicable"):
        result["applicable"] = external_fields.get("applicable")

    # Dados principais
    result["article"] = article_metadata
    result["citations"] = citations

    # Dados complementares
    if issns:
        result["code_title"] = issns
    if external_fields.get("created_at"):
        result["created_at"] = external_fields.get("created_at")
    if article_type:
        result["document_type"] = article_type
    if doi:
        result["doi"] = doi
    if publication_date:
        result["publication_date"] = publication_date
    if publication_year:
        result["publication_year"] = publication_year
    if external_article_data.get("sent_wos"):
        result["sent_wos"] = external_article_data.get("sent_wos")
    if external_article_data.get("validated_scielo"):
        result["validated_scielo"] = external_article_data.get("validated_scielo")
    if external_article_data.get("validated_wos"):
        result["validated_wos"] = external_article_data.get("validated_wos")
    if external_article_data.get("version"):
        result["version"] = external_article_data.get("version")
    if code:
        result["code"] = code
    if code_issue:
        result["code_issue"] = code_issue

    return result
