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


def _citation_code(citation_data, citation_dict):
    # TODO: adicionar a lógica de obtenção do código da citação, eg.: "code": "S1519-6984202400010016500001"
    return citation_dict


def _citation_date(citation_data, citation_dict):
    citation_date = citation_data.get("year") + "0000"
    citation_dict.update({"v865": [{"_": citation_date}]})
    return citation_dict


def _citation_title(citation_data, citation_dict):
    # TODO: adicionar a lógica de obtenção do idioma da citação
    citation_title = citation_data.get("article_title")
    citation_dict.update({"v12": [{"_": citation_title}]})
    return citation_dict


def _citation_volume(citation_data, citation_dict):
    citation_volume = citation_data.get("volume")
    citation_dict.update({"v31": [{"_": citation_volume}]})
    return citation_dict


