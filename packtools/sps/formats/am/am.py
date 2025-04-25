from packtools.sps.models import (
journal_meta,
front_articlemeta_issue,
article_ids,
article_contribs,
aff,
references,
)

from packtools.sps.formats.am import record


def get_journal(xml_tree):
    journal = journal_meta.Title(xml_tree)
    return record.simple_field("v30", journal.abbreviated_journal_title)

def get_articlemeta_issue(xml_tree):
    article_meta = front_articlemeta_issue.ArticleMetaIssue(xml_tree)
    d = {}
    d.update(record.simple_field("v31", article_meta.volume))
    d.update(record.simple_field("v121", article_meta.order_string_format))
    d.update(
        {
            "v882": [
                record.multiple_fields(
                    keys=("v", "n", "_"),
                    values=[
                        article_meta.volume,
                        article_meta.number,
                        ""
                    ]
                )
            ]
        }
    )
    return d

def get_ids(xml_tree):
    ids = article_ids.ArticleIds(xml_tree)
    return {"code": ids.v2}

def get_contrib_data(author):
    author_type = author.get("contrib_type")
    if author_type == "author":
        author_type = "ND"

    return [
        author.get("contrib_ids", {}).get("orcid"),
        author.get("contrib_name", {}).get("given-names"),
        author.get("affs", [{}])[0].get("id"),
        author.get("contrib_name", {}).get("surname"),
        author_type,
        ""
    ]

def get_contribs(xml_tree):
    return record.multiple_fields_list(
        key="v10",
        nested_keys=("k", "n", "1", "s", "r", "_"),
        iterator=article_contribs.XMLContribs(xml_tree).contribs,
        extractor=get_contrib_data
    )



def build(xml_tree):
    resp = {}
    resp.update(get_journal(xml_tree))
    resp.update(get_articlemeta_issue(xml_tree))
    resp.update(get_ids(xml_tree))
    resp.update(get_contribs(xml_tree))
    return resp
