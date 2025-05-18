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
)


def get_journal(xml_tree, article_data=None):
    article_data = article_data or {}

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

    return {
        **simple_field("v30", title.abbreviated_journal_title),
        **simple_field("v421", journal_id.nlm_ta),
        **simple_field("v62", publisher_name),
        **simple_field("v100", title.journal_title),
        **multiple_complex_field("v435", issn_list),
        **simple_field("v35", article_data.get("v35")),
    }


def get_articlemeta_issue(xml_tree):
    meta = front_articlemeta_issue.ArticleMetaIssue(xml_tree)
    abstracts = article_abstract.Abstract(xml_tree).get_abstracts_by_lang(
        style="inline"
    )

    v882 = {}
    add_item(v882, "v", meta.volume)
    add_item(v882, "n", meta.number)
    add_item(v882, "_", "")

    v14 = {}
    add_item(v14, "e", meta.elocation_id)
    add_item(v14, "f", meta.fpage)
    add_item(v14, "l", meta.lpage)
    add_item(v14, "_", "")

    result = {
        **simple_field("v31", meta.volume),
        **simple_field("v121", meta.order_string_format),
        **complex_field("v882", v882),
        **complex_field("v14", v14),
    }

    if meta.volume:
        result.update(simple_field("v4", f"V{meta.volume}"))

    result.update(simple_field("v709", "article" if abstracts else "text"))
    return result


def get_ids(xml_tree):
    ids = article_ids.ArticleIds(xml_tree)
    return {
        "code": ids.v2,
        **simple_field("v880", ids.v2),
        **simple_field("v237", ids.doi),
    }


def get_contribs(xml_tree):
    contribs = article_contribs.XMLContribs(xml_tree).contribs
    list_contribs = []
    for author in contribs:
        author_type = author.get("contrib_type", "ND")
        if author_type == "author":
            author_type = "ND"

        affs = author.get("affs", [])
        aff_id = affs[0].get("id") if affs else None

        v10 = {}
        add_item(v10, "k", author.get("contrib_ids", {}).get("orcid"))
        add_item(v10, "n", author.get("contrib_name", {}).get("given-names"))
        add_item(v10, "1", aff_id)
        add_item(v10, "s", author.get("contrib_name", {}).get("surname"))
        add_item(v10, "r", author_type)
        add_item(v10, "_", "")
        list_contribs.append(v10)

    return multiple_complex_field("v10", list_contribs)


def get_affs(xml_tree):
    affiliations = aff.Affiliation(xml_tree).affiliation_list
    list_v70 = []
    list_v240 = []

    for item in affiliations:
        if item.get("parent") != "article":
            continue

        v70 = {}
        add_item(v70, "c", item.get("city"))
        add_item(v70, "i", item.get("id"))
        add_item(v70, "l", item.get("label"))
        add_item(v70, "1", item.get("orgdiv1"))
        add_item(v70, "p", item.get("country_name"))
        add_item(v70, "s", item.get("state"))
        add_item(v70, "_", item.get("orgname"))
        list_v70.append(v70)

        v240 = {}
        add_item(v240, "c", item.get("city"))
        add_item(v240, "i", item.get("id"))
        add_item(v240, "p", item.get("country_code"))
        add_item(v240, "s", item.get("state"))
        add_item(v240, "_", item.get("orgname"))
        list_v240.append(v240)

    return {
        **multiple_complex_field("v70", list_v70),
        **multiple_complex_field("v240", list_v240),
    }


def count_references(xml_tree):
    refs = list(references.XMLReferences(xml_tree).items)
    return simple_field("v72", str(len(refs)))


def extract_authors(all_authors):
    v10_list = []
    for author in all_authors or []:
        v10 = {}
        add_item(v10, "n", author.get("given-names"))
        add_item(v10, "s", author.get("surname"))
        add_item(v10, "r", author.get("role", "ND"))
        add_item(v10, "_", "")
        v10_list.append(v10)
    return v10_list


def format_page_range(fpage, lpage):
    if fpage and lpage:
        return f"{fpage}-{lpage}"
    return fpage or lpage or ""


def get_field_v936(article_data=None):
    article_data = article_data or {}

    v936_dict = article_data.get("v936") or {}
    return (
        v936_dict
        if isinstance(v936_dict, dict) and all(k in v936_dict for k in ("i", "y", "o"))
        else None
    )


def get_dates(xml_tree, article_data=None):
    article_data = article_data or {}

    dates = article_dates.ArticleDates(xml_tree)
    v114 = format_date(
        dates.history_dates_dict.get("accepted"), ["year", "month", "day"]
    )
    v112 = format_date(
        dates.history_dates_dict.get("received"), ["year", "month", "day"]
    )
    v65 = (
        format_date(dates.collection_date, ["year"]) + "0000"
        if dates.collection_date
        else None
    )
    v223 = format_date(dates.epub_date, ["year", "month", "day"])

    v265_list = [
        {"k": item["k"], "s": item["s"], "v": item["v"]}
        for item in article_data.get("v265", [])
        if all(k in item for k in ("k", "s", "v"))
    ]

    return {
        **simple_field("v114", v114),
        **simple_field("v112", v112),
        **simple_field("v65", v65),
        **simple_field("v223", v223),
        "processing_date": article_data.get("processing_date"),
        **multiple_complex_field("v265", v265_list),
        **complex_field("v936", get_field_v936(article_data)),
    }


def get_article_and_subarticle(xml_tree):
    articles = article_and_subarticles.ArticleAndSubArticles(xml_tree)
    article_type = articles.main_article_type
    v71_value = ARTICLE_TYPE_MAP.get(article_type)

    result = {
        **simple_field("v40", articles.main_lang),
        **simple_field(
            "v120", f"XML_{articles.dtd_version}" if articles.dtd_version else None
        ),
        **simple_field("v71", v71_value),
    }

    other_langs = [
        {"_": lang}
        for item in articles.data
        if (lang := item.get("lang")) and lang != articles.main_lang
    ]
    if other_langs:
        result.update(multiple_complex_field("v601", other_langs))

    doi_list = [
        {"d": item["doi"], "l": item["lang"], "_": ""}
        for item in articles.data
        if item.get("doi") and item.get("lang")
    ]
    if doi_list:
        result.update(multiple_complex_field("v337", doi_list))

    return result


def get_article_abstract(xml_tree):
    abstracts = article_abstract.Abstract(xml_tree).get_abstracts_by_lang(
        style="inline"
    )
    list_abs = []
    for lang, abstract in abstracts.items():
        v83 = {}
        add_item(v83, "a", abstract)
        add_item(v83, "l", lang)
        add_item(v83, "_", "")
        list_abs.append(v83)
    return multiple_complex_field("v83", list_abs)


def get_keyword(xml_tree):
    keywords = kwd_group.ArticleKeywords(xml_tree)
    keywords.configure()
    list_kw = []
    for kw in keywords.items:
        v85 = {}
        add_item(v85, "k", kw.get("plain_text"))
        add_item(v85, "l", kw.get("lang"))
        add_item(v85, "_", "")
        list_kw.append(v85)
    return multiple_complex_field("v85", list_kw)


def get_title(xml_tree):
    v12_fields = {"l": "lang", "_": "plain_text"}
    v12_list = [
        {k: item.get(v) for k, v in v12_fields.items() if item.get(v)}
        for item in article_titles.ArticleTitles(xml_tree).article_title_list
    ]
    return multiple_complex_field("v12", v12_list)


def get_external_fields(article_data=None):
    article_data = article_data or {}
    return {
        **simple_field("v999", article_data.get("v999")),
        **simple_field("v38", article_data.get("v38")),
        **simple_field("v992", article_data.get("v992")),
        **simple_field("v42", article_data.get("v42")),
        **simple_field("v49", article_data.get("v49")),
        **simple_field("v706", article_data.get("v706")),
        "collection": article_data.get("collection"),
        **simple_field("v2", article_data.get("v2")),
        **simple_field("v91", article_data.get("v91")),
        **simple_field("v701", article_data.get("v701")),
        **simple_field("v700", article_data.get("v700")),
        **simple_field("v702", article_data.get("v702")),
        **simple_field("v705", article_data.get("v705")),
        **simple_field("v708", article_data.get("v708")),
        **simple_field("v3", article_data.get("v3")),
        "applicable": article_data.get("applicable"),
        "created_at": article_data.get("created_at"),
    }


def get_article_metadata(xml_tree, article_data=None):
    article_data = article_data or {}
    return {
        **get_journal(xml_tree, article_data),
        **get_articlemeta_issue(xml_tree),
        **get_ids(xml_tree),
        **get_contribs(xml_tree),
        **get_affs(xml_tree),
        **count_references(xml_tree),
        **get_dates(xml_tree, article_data),
        **get_article_and_subarticle(xml_tree),
        **get_article_abstract(xml_tree),
        **get_keyword(xml_tree),
        **get_title(xml_tree),
        **get_external_fields(article_data),
    }


def get_citations(xml_tree, article_data=None, citation_data=None):
    article_data = article_data or {}
    citation_data = citation_data or {}

    xml_data = {
        **get_ids(xml_tree),
        **get_dates(xml_tree, article_data),
        **get_articlemeta_issue(xml_tree),
        **count_references(xml_tree),
    }

    citation_common = {
        # Identificadores principais
        "code": xml_data.get("code"),
        "v237": xml_data.get("v237"),
        "v4": xml_data.get("v4"),
        "v72": xml_data.get("v72"),
        "v65": xml_data.get("v65"),
        "v708": xml_data.get("v72"),
        # Metadados externos do artigo
        "collection": article_data.get("collection"),
        "v2": article_data.get("v2"),
        "v3": article_data.get("v3"),
        "v999": article_data.get("v999"),
        "v992": article_data.get("v992"),
        "v701": article_data.get("v701"),
        "v702": article_data.get("v702"),
        "v705": article_data.get("v705"),
        "v936": get_field_v936(article_data),
        # Dados específicos de citação
        "v700": citation_data.get("v700", []),
        "processing_date": citation_data.get("processing_date"),
        # Dados de fascículo
        "v882": xml_data.get("v882"),
    }

    refs = []
    v700_refs = citation_common.get("v700")
    for idx, ref in enumerate(references.XMLReferences(xml_tree).items, start=1):
        v64 = format_date(ref, ["year"])
        v65 = v64 + "0000" if v64 else None
        v700 = v700_refs[idx - 1] if v700_refs and idx - 1 < len(v700_refs) else None

        v514 = {}
        add_item(v514, "l", ref.get("lpage"))
        add_item(v514, "f", ref.get("fpage"))
        add_item(v514, "_", "")

        citation = {
            **simple_field("v30", ref.get("source")),
            **simple_field("v31", ref.get("volume")),
            **simple_field("v32", ref.get("issue")),
            "code": (
                f"{citation_common['code']}{idx:05}"
                if citation_common["code"]
                else None
            ),
            **simple_field("v999", citation_common["v999"]),
            **simple_field("v37", ref.get("mixed_citation_xlink")),
            **simple_field("v12", ref.get("article_title")),
            **multiple_complex_field("v10", extract_authors(ref.get("all_authors"))),
            **simple_field("v71", ref.get("publication_type")),
            **simple_field(
                "v14", format_page_range(ref.get("fpage"), ref.get("lpage"))
            ),
            **complex_field("v936", citation_common["v936"]),
            **simple_field("v880", citation_common["code"]),
            "v865": citation_common["v65"],
            **simple_field("v118", ref.get("label")),
            "v237": citation_common["v237"],
            **simple_field("v706", "c"),
            **simple_field("v64", v64),
            **simple_field("v65", v65),
            "collection": citation_common["collection"],
            "v708": citation_common["v708"],
            **simple_field("v2", citation_common["v2"]),
            **simple_field("v3", citation_common["v3"]),
            "v4": citation_common["v4"],
            **simple_field("v992", citation_common["v992"]),
            **simple_field("v701", citation_common["v701"]),
            **simple_field("v700", v700),
            **simple_field("v702", citation_common["v702"]),
            **simple_field("v705", citation_common["v705"]),
            "processing_date": citation_common["processing_date"],
            **complex_field("v514", v514),
            "v882": citation_common["v882"],
        }

        refs.append(citation)

    return refs


def build(xml_tree, article_data=None, citation_data=None):
    code = (get_ids(xml_tree) or {}).get("code")
    journal_data = get_journal(xml_tree, article_data)
    external_fields = get_external_fields(article_data)
    articles = article_and_subarticles.ArticleAndSubArticles(xml_tree)
    article_type = articles.main_article_type
    article_metadata = get_article_metadata(xml_tree, article_data)
    citations = get_citations(xml_tree, article_data, citation_data)
    publication_date = article_metadata.get("v65", [{}])[0].get("_")  # "20250000"
    publication_year = publication_date[:4] if publication_date else None

    issns = [
        item.get("_")
        for field in ("v35", "v435")
        for item in journal_data.get(field, [])
    ]

    return {
        "code": code,
        "collection": external_fields.get("collection"),
        "applicable": external_fields.get("applicable"),
        "article": article_metadata,
        "citations": citations,
        "code_issue": code[1:18] if code and len(code) >= 18 else None,
        "code_title": issns,
        "created_at": external_fields.get("created_at"),
        "document_type": article_type,
        "doi": article_metadata.get("v237", [{}])[0].get("_"),
        "publication_date": publication_date,
        "publication_year": publication_year,
        "sent_wos": article_data.get("sent_wos"),
        "validated_scielo": article_data.get("validated_scielo"),
        "validated_wos": article_data.get("validated_wos"),
        "version": article_data.get("version"),
    }
