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
)

from packtools.sps.formats.am import record


def get_journal(xml_tree):
    journal_title = journal_meta.Title(xml_tree)
    journal_id = journal_meta.JournalID(xml_tree)
    publisher_name = journal_meta.Publisher(xml_tree)
    issns = journal_meta.ISSN(xml_tree)

    dict_journal_meta = {}

    dict_journal_meta.update(record.simple_field("v30", journal_title.abbreviated_journal_title))
    dict_journal_meta.update(record.simple_field("v421", journal_id.nlm_ta))
    dict_journal_meta.update(record.simple_field("v62", publisher_name.publishers_names[0]))
    dict_journal_meta.update(record.simple_field("v100", journal_title.journal_title))

    issn_map = {"epub": issns.epub, "ppub": issns.ppub}
    issn_list = [{"t": t, "_": val} for t, val in issn_map.items() if val]
    dict_journal_meta.update(record.multiple_complex_field("v435", issn_list))

    return dict_journal_meta

def get_articlemeta_issue(xml_tree):
    article_meta = front_articlemeta_issue.ArticleMetaIssue(xml_tree)
    dict_issue = {}
    dict_issue.update(record.simple_field("v31", article_meta.volume))
    dict_issue.update(record.simple_field("v121", article_meta.order_string_format))

    v882 = {}
    record.add_item(v882, "v", article_meta.volume)
    record.add_item(v882, "n", article_meta.number)
    # TODO fixme
    record.add_item(v882, "_", "")
    dict_issue.update(record.complex_field("v882", v882))

    v14 = {}
    record.add_item(v14, "e", article_meta.elocation_id)
    record.add_item(v14, "f", article_meta.fpage)
    record.add_item(v14, "l", article_meta.lpage)
    # TODO fixme
    record.add_item(v14, "_", "")
    dict_issue.update(record.complex_field("v14", v14))

    return dict_issue

def get_ids(xml_tree):
    ids = article_ids.ArticleIds(xml_tree)
    dict_id = {"code": ids.v2}
    dict_id.update(record.simple_field("v880", ids.v2))
    dict_id.update(record.simple_field("v237", ids.doi))
    return dict_id

def get_contribs(xml_tree):
    dict_contrib = {}
    list_contribs = []
    for author in article_contribs.XMLContribs(xml_tree).contribs:

        author_type = author.get("contrib_type")
        if author_type == "author":
            author_type = "ND"

        v10 = {}
        record.add_item(v10, "k", author.get("contrib_ids", {}).get("orcid"))
        record.add_item(v10, "n", author.get("contrib_name", {}).get("given-names"))
        record.add_item(v10, "1", author.get("affs", [{}])[0].get("id"))
        record.add_item(v10, "s", author.get("contrib_name", {}).get("surname"))
        record.add_item(v10, "r", author_type)
        # TODO fixme
        record.add_item(v10, "_", "")

        list_contribs.append(v10)

    dict_contrib.update(record.multiple_complex_field("v10", list_contribs))

    return dict_contrib

def get_affs(xml_tree):
    dict_aff = {}
    list_affs = []

    for item in aff.Affiliation(xml_tree).affiliation_list:
        v70 = {}
        record.add_item(v70, "c", item.get("city"))
        record.add_item(v70, "i", item.get("id"))
        record.add_item(v70, "l", item.get("label"))
        record.add_item(v70, "1", item.get("orgdiv1"))
        record.add_item(v70, "p", item.get("country_name"))
        record.add_item(v70, "s", item.get("state"))
        record.add_item(v70, "_", item.get("orgname"))
        list_affs.append(v70)

    dict_aff.update(record.multiple_complex_field("v70", list_affs))

    return dict_aff

def get_references(xml_tree):
    refs = list(references.XMLReferences(xml_tree).items)
    dict_ref = {}
    dict_ref.update(record.simple_field("v72", len(refs)))
    return dict_ref

def get_dates(xml_tree):
    dates = article_dates.ArticleDates(xml_tree)
    history_dates = dates.history_dates_dict
    collection_date = dates.collection_date
    dict_dates = {}
    try:
        v114 = "".join([history_dates["accepted"]["year"], history_dates["accepted"]["month"], history_dates["accepted"]["day"]])
    except KeyError:
        v114 = None

    try:
        v112 = "".join([history_dates["received"]["year"], history_dates["received"]["month"], history_dates["received"]["day"]])
    except KeyError:
        v112 = None

    try:
        v65 = "".join([collection_date["year"], "0000"])
    except KeyError:
        v65 = None

    dict_dates.update(record.simple_field("v114", v114))
    dict_dates.update(record.simple_field("v112", v112))
    dict_dates.update(record.simple_field("v65", v65))
    return dict_dates

def get_article_and_subarticle(xml_tree):
    articles = article_and_subarticles.ArticleAndSubArticles(xml_tree)
    dict_articles = {}
    v40 = articles.main_lang
    dict_articles.update(record.simple_field("v40", v40))
    return dict_articles

def get_article_abstract(xml_tree):
    abstracts = article_abstract.Abstract(xml_tree).get_abstracts_by_lang(style="inline")

    dict_abs = {}
    list_abs = []

    for lang, abstract in abstracts.items():
        v83 = {}
        record.add_item(v83, "a", abstract)
        record.add_item(v83, "l", lang)
        record.add_item(v83, "_", "")
        list_abs.append(v83)

    dict_abs.update(record.multiple_complex_field("v83", list_abs))

    return dict_abs



def build(xml_tree):
    resp = {}
    resp.update(get_journal(xml_tree))
    resp.update(get_articlemeta_issue(xml_tree))
    resp.update(get_ids(xml_tree))
    resp.update(get_contribs(xml_tree))
    resp.update(get_affs(xml_tree))
    return resp
