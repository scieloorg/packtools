import datetime
import re

from packtools.sps.models.article_ids import ArticleIds


def code(xml_tree, h_record_dict):
    article_id_v2 = ArticleIds(xml_tree).v2
    if article_id_v2:
        h_record_dict.update({"code": article_id_v2})
    return h_record_dict

def collection(xml_tree, h_record_dict):
    # TODO: adicionar a lógica de obtenção do código da coleção
    return h_record_dict


def processing_date(h_record_dict):
    date = (
        datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[
            :-3
        ]
        + "Z"
    )
    h_record_dict.update({"processing_date": date})
    return h_record_dict

