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


def _translate_publication_type_to_literature_type(publication_type):
    """
    Translates a publication type from the SciELO XML standard to the v705 classification.

    Args:
        publication_type (str): The 'publication-type' value from SciELO XML.

    Returns:
        str: The corresponding v705 classification. Defaults to 'D' (Document of work) if the type is not recognized.
    """
    publication_type_to_v705 = {
        "journal": "S",  # Serial (journals, periodicals)
        "book": "M",  # Monograph (books)
        "chapter": "C",  # Component (book chapters)
        "conference": "A",  # Analytical (conference proceedings)
        "thesis": "M",  # Monograph (theses and dissertations)
        "report": "M",  # Monograph (technical reports)
        "web": "G",  # Collection (digital material)
        "other": "D",  # Document of work (undefined or others)
    }
    return publication_type_to_v705.get(publication_type, "D")


def _literature_type(citation_data, citation_dict):
    citation_type = citation_data.get("publication_type")
    literature_type = _translate_publication_type_to_literature_type(citation_type)
    citation_dict.update({"v705": [{"_": literature_type}]})
    return citation_dict
