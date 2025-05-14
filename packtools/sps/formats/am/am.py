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


def get_journal(xml_tree, data=None):
    title = journal_meta.Title(xml_tree)
    journal_id = journal_meta.JournalID(xml_tree)
    publisher = journal_meta.Publisher(xml_tree)
    issns = journal_meta.ISSN(xml_tree)

    issn_list = [
        {"t": t, "_": val}
        for t, val in {"epub": issns.epub, "ppub": issns.ppub}.items()
        if val
    ]

    data = data or {}

    publisher_name = (
        publisher.publishers_names[0] if publisher.publishers_names else None
    )

    return {
        **simple_field("v30", title.abbreviated_journal_title),
        **simple_field("v421", journal_id.nlm_ta),
        **simple_field("v62", publisher_name),
        **simple_field("v100", title.journal_title),
        **multiple_complex_field("v435", issn_list),
        **simple_field("v35", data.get("v35")),
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

    if abstracts:
        result.update(simple_field("v709", "article"))
    else:
        result.update(simple_field("v709", "text"))

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

        v10 = {}
        add_item(v10, "k", author.get("contrib_ids", {}).get("orcid"))
        add_item(v10, "n", author.get("contrib_name", {}).get("given-names"))
        add_item(v10, "1", author.get("affs", [{}])[0].get("id"))
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
    return simple_field("v72", len(refs))


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


def get_citation(xml_tree, article_data=None):
    article_data = article_data or {}

    article_code = (get_ids(xml_tree) or {}).get("code")

    for idx, ref in enumerate(references.XMLReferences(xml_tree).items, start=1):
        v64 = format_date(ref, ["year"])
        v65 = v64 + "0000" if v64 else None
        yield {
            **simple_field("v30", ref.get("source")),
            **simple_field("v31", ref.get("volume")),
            **simple_field("v32", ref.get("issue")),
            # considerando que o valor de "code" para referências seja o identificador do artigo (v2)
            # concatenado com um inteiro sequencial de cinco caracteres, eg.: S0104-1169202500010030000001
            **{"code": f"{article_code}{idx:05}"},
            **simple_field("v999", article_data.get("v999")),
            **simple_field("v37", ref.get("mixed_citation_xlink")),
            **simple_field("v12", ref.get("article_title")),
            **multiple_complex_field("v10", extract_authors(ref.get("all_authors"))),
            **simple_field("v71", ref.get("publication_type")),
            **simple_field("v14", format_page_range(ref.get("fpage"), ref.get("lpage"))),
            **complex_field("v936", get_field_v936(article_data)),
            **simple_field("v880", article_code),
            **{"v865": (get_dates(xml_tree) or {}).get("v65")},
            **simple_field("v118", ref.get("label")),
            **{"v237": (get_ids(xml_tree) or {}).get("v237")},
            **simple_field("v706", "c"),
            **simple_field("v64", v64),
            **simple_field("v65", v65),
        }



def get_citations(xml_tree, article_data=None):
    return [ref for ref in get_citation(xml_tree, article_data)]


def get_field_v936(data):
    v936_dict = data.get("v936") or {}
    return (
        v936_dict
        if isinstance(v936_dict, dict) and all(k in v936_dict for k in ("i", "y", "o"))
        else None
    )


def get_dates(xml_tree, data=None):
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

    data = data or {}

    v265_list = []
    for item in data.get("v265", []):
        if all(k in item for k in ("k", "s", "v")):
            v265_list.append({"k": item["k"], "s": item["s"], "v": item["v"]})

    return {
        **simple_field("v114", v114),
        **simple_field("v112", v112),
        **simple_field("v65", v65),
        **simple_field("v223", v223),
        **{"processing_date": data.get("processing_date")},
        **multiple_complex_field("v265", v265_list),
        **complex_field("v936", get_field_v936(data)),
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


def get_external_fields(data):
    if not data:
        return

    return {
        **simple_field("v999", data.get("v999")),
        **simple_field("v38", data.get("v38")),
        **simple_field("v992", data.get("v992")),
        **simple_field("v42", data.get("v42")),
        **simple_field("v49", data.get("v49")),
        **simple_field("v706", data.get("v706")),
        **{"collection": data.get("collection")},
        **simple_field("v2", data.get("v2")),
        **simple_field("v91", data.get("v91")),
        **simple_field("v701", data.get("v701")),
        **simple_field("v700", data.get("v700")),
        **simple_field("v702", data.get("v702")),
        **simple_field("v705", data.get("v705")),
        **simple_field("v708", data.get("v708")),
        **simple_field("v3", data.get("v3")),
    }


def get_article_metadata(xml_tree, data):
    return {
        **get_journal(xml_tree, data),
        **get_articlemeta_issue(xml_tree),
        **get_ids(xml_tree),
        **get_contribs(xml_tree),
        **get_affs(xml_tree),
        **count_references(xml_tree),
        **get_dates(xml_tree, data),
        **get_article_and_subarticle(xml_tree),
        **get_article_abstract(xml_tree),
        **get_keyword(xml_tree),
        **get_title(xml_tree),
        **get_external_fields(data),
    }


def build(xml_tree, data=None):
    data = data or {}
    return {
        "article": get_article_metadata(xml_tree, data),
        "citations": get_citations(xml_tree, article_data=data),
    }
