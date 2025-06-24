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


def get_journal(xml_tree):
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
    result = {}

    if ids.v2:
        result["code"] = ids.v2
        result.update(simple_field("v880", ids.v2))

    if ids.doi:
        result.update(simple_field("v237", ids.doi))

    return result


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


def get_dates(xml_tree):
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

    return {
        **simple_field("v114", v114),
        **simple_field("v112", v112),
        **simple_field("v65", v65),
        **simple_field("v223", v223),
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


def get_external_fields(external_article_data=None):
    external_article_data = external_article_data or {}

    v265_list = [
        {"k": item["k"], "s": item["s"], "v": item["v"]}
        for item in external_article_data.get("v265", [])
        if all(k in item for k in ("k", "s", "v"))
    ]

    v936_dict = external_article_data.get("v936") or {}
    v936 = (
        v936_dict
        if isinstance(v936_dict, dict) and all(k in v936_dict for k in ("i", "y", "o"))
        else None
    )

    result = {
        "applicable": external_article_data.get("applicable"),
        "collection": external_article_data.get("collection"),
        "created_at": external_article_data.get("created_at"),
        "processing_date": external_article_data.get("processing_date"),
        "v35": external_article_data.get("v35"),
        "v42": external_article_data.get("v42"),
        "v701": external_article_data.get("v701"),
        "v992": external_article_data.get("v992"),
        "v999": external_article_data.get("v999"),
        **simple_field("v2", external_article_data.get("v2")),
        **simple_field("v3", external_article_data.get("v3")),
        **simple_field("v38", external_article_data.get("v38")),
        **simple_field("v49", external_article_data.get("v49")),
        **simple_field("v700", external_article_data.get("v700")),
        **simple_field("v702", external_article_data.get("v702")),
        **simple_field("v705", external_article_data.get("v705")),
        **simple_field("v706", external_article_data.get("v706")),
        **simple_field("v708", external_article_data.get("v708")),
        **simple_field("v91", external_article_data.get("v91")),
        **complex_field("v936", v936),
        **multiple_complex_field("v265", v265_list),
    }

    return {k: v for k, v in result.items() if v is not None}


def get_article_metadata(xml_tree, external_article_data=None):
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
        **count_references(xml_tree),
    }

    citation_common = get_citation_common(
        xml_data, external_article_data, external_citation_data
    )
    v700_refs = citation_common.get("v700", [])

    refs = []
    for idx, ref in enumerate(references.XMLReferences(xml_tree).items, start=1):
        refs.append(build_citation(ref, citation_common, idx, v700_refs))

    return refs


def get_citation_common(xml_data, external_article_data, external_citation_data):
    return {
        "code": xml_data.get("code"),
        "collection": external_article_data.get("collection"),
        "processing_date": external_citation_data.get("processing_date"),
        "v237": xml_data.get("v237"),
        "v2": external_article_data.get("v2"),
        "v3": external_article_data.get("v3"),
        "v4": xml_data.get("v4"),
        "v65": xml_data.get("v65"),
        "v700": external_citation_data.get("v700", []),
        "v701": external_article_data.get("v701"),
        "v702": external_article_data.get("v702"),
        "v705": external_article_data.get("v705"),
        "v708": xml_data.get("v72"),
        "v882": xml_data.get("v882"),
        "v936": external_article_data.get("v936"),
        "v992": external_article_data.get("v992"),
        "v999": external_article_data.get("v999"),
    }


def build_citation(ref, common, idx, v700_refs):
    v64 = format_date(ref, ["year"])
    v65 = f"{v64}0000" if v64 else None
    v700 = v700_refs[idx - 1] if idx - 1 < len(v700_refs) else None

    v514 = {
        "l": ref.get("lpage"),
        "f": ref.get("fpage"),
        "_": "",
    }

    result = {
        "code": f"{common['code']}{idx:05}" if common["code"] else None,
        "collection": common["collection"],
        "processing_date": common["processing_date"],
        "v237": common["v237"],
        "v4": common["v4"],
        "v865": common["v65"],
        "v882": common["v882"],
        "v999": common["v999"],
        "v701": common["v701"],
        "v708": common["v708"],
        "v992": common["v992"],
        **simple_field("v118", ref.get("label")),
        **simple_field("v12", ref.get("article_title")),
        **simple_field("v14", format_page_range(ref.get("fpage"), ref.get("lpage"))),
        **simple_field("v2", common["v2"]),
        **simple_field("v3", common["v3"]),
        **simple_field("v30", ref.get("source")),
        **simple_field("v31", ref.get("volume")),
        **simple_field("v32", ref.get("issue")),
        **simple_field("v37", ref.get("mixed_citation_xlink")),
        **simple_field("v64", v64),
        **simple_field("v65", v65),
        **simple_field("v700", v700),
        **simple_field("v702", common["v702"]),
        **simple_field("v705", common["v705"]),
        **simple_field("v706", "c"),
        **simple_field("v71", ref.get("publication_type")),
        **simple_field("v880", common["code"]),
        **complex_field("v514", v514),
        **complex_field("v936", common["v936"]),
        **multiple_complex_field("v10", extract_authors(ref.get("all_authors"))),
    }

    return {k: v for k, v in result.items() if v is not None}


def build(xml_tree, external_article_data=None, external_citation_data=None):
    external_article_data = external_article_data or {}
    external_citation_data = external_citation_data or {}

    article_metadata = get_article_metadata(xml_tree, external_article_data)
    citations = get_citations(xml_tree, external_article_data, external_citation_data)
    journal_data = get_journal(xml_tree)
    external_fields = get_external_fields(external_article_data)
    article_type = article_and_subarticles.ArticleAndSubArticles(xml_tree).main_article_type

    def extract_first_text(lst):
        return lst[0].get("_") if isinstance(lst, list) and lst and isinstance(lst[0], dict) else None

    publication_date = extract_first_text(article_metadata.get("v65"))
    publication_year = publication_date[:4] if publication_date else None
    doi = extract_first_text(article_metadata.get("v237"))
    code = article_metadata.get("code")
    code_issue = code[1:18] if code and len(code) >= 18 else None

    issns = [
        item.get("_") for item in external_article_data.get("v35", []) + journal_data.get("v435", [])
        if isinstance(item, dict) and item.get("_")
    ]

    result = {
        "collection": external_fields.get("collection"),
        "applicable": external_fields.get("applicable"),
        "article": article_metadata,
        "citations": citations,
        "code_title": issns,
        "created_at": external_fields.get("created_at"),
        "document_type": article_type,
        "doi": doi,
        "publication_date": publication_date,
        "publication_year": publication_year,
        "sent_wos": external_article_data.get("sent_wos"),
        "validated_scielo": external_article_data.get("validated_scielo"),
        "validated_wos": external_article_data.get("validated_wos"),
        "version": external_article_data.get("version"),
        "code": code,
        "code_issue": code_issue,
    }

    return {k: v for k, v in result.items() if v is not None}



