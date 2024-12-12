import datetime

from packtools.sps.models.article_ids import ArticleIds


def code(xml_tree, am_dict):
    article_id_v2 = ArticleIds(xml_tree).v2
    am_dict.update({"code": article_id_v2})
    return am_dict


def collection(xml_tree, am_dict):
    # TODO: adicionar a lógica de obtenção do código da coleção
    return am_dict


