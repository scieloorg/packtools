import datetime

from packtools.sps.models.article_ids import ArticleIds


def code(xml_tree, am_dict):
    article_id_v2 = ArticleIds(xml_tree).v2
    am_dict.update({"code": article_id_v2})
    return am_dict


def collection(xml_tree, am_dict):
    # TODO: adicionar a lógica de obtenção do código da coleção
    return am_dict


def processing_date(xml_tree, am_dict):
    date = (
        datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[
            :-3
        ]
        + "Z"
    )
    am_dict.update({"processing_date": date})
    return am_dict


def _citation_id(citation_data, citation_dict):
    citation_id = citation_data.get("ref_id")
    citation_dict.update({"v700": [{"_": citation_id}]})
    return citation_dict


