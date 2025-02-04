import datetime
import re

from packtools.sps.models.article_ids import ArticleIds
from packtools.sps.models.journal_meta import ISSN
from packtools.sps.models.article_doi_with_lang import DoiWithLang
from packtools.sps.models.article_dates import ArticleDates


def code(xml_tree, h_record_dict):
    article_id_v2 = ArticleIds(xml_tree).v2
    if article_id_v2:
        h_record_dict.update({"code": article_id_v2})
    return h_record_dict

def collection(xml_tree, h_record_dict):
    # TODO: adicionar a lógica de obtenção do código da coleção
    return h_record_dict

def processing_dates(h_record_dict):
    date = (
        datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[
            :-3
        ]
        + "Z"
    )
    h_record_dict.update({
        "processing_date": date,
        "created_at": {"$date": date},
    })
    return h_record_dict

def wos_status(xml_tree, h_record_dict, sent_wos=False, validated_wos=False):
    # TODO: adicionar a lógica de obtenção do status referente a WOS
    h_record_dict.update({"sent_wos": sent_wos, "validated_wos": validated_wos})
    return h_record_dict

def code_issue(xml_tree, h_record_dict):
    # TODO: validar se o valor para cod_issue é uma sub-cadeia de article-id (v2)
    # article-id = S1414-98932020000100118  cod_issue = 1414-989320200001
    article_id_v2 = ArticleIds(xml_tree).v2
    match = None
    if article_id_v2:
        match = re.match(r"S(\d{4}-\d{4}\d{8})\d{5}$", article_id_v2)
    if match:
        h_record_dict.update({"code_issue": match.group(1)})
    return h_record_dict

def code_title(xml_tree, h_record_dict):
    issns = ISSN(xml_tree).data
    resp = []
    for issn in issns:
        resp.append(issn.get("value"))
    if resp:
        h_record_dict.update({"code_title": resp})
    return h_record_dict

def doi(xml_tree, h_record_dict):
    doi_value = DoiWithLang(xml_tree).main_doi
    if doi_value:
        h_record_dict.update({"doi": doi_value})
    return h_record_dict

def applicable(xml_tree, h_record_dict, value=False):
    h_record_dict.update({"applicable": value})
    return h_record_dict

