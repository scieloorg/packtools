import requests
from langdetect import detect

from packtools.sps.libs.requester import fetch_data


def format_response(
    title,
    parent,
    parent_id,
    parent_article_type,
    parent_lang,
    item,
    sub_item,
    validation_type,
    is_valid,
    expected,
    obtained,
    advice,
    data,
    error_level,
):
    return {
        "title": title,
        "parent": parent,
        "parent_id": parent_id,
        "parent_article_type": parent_article_type,
        "parent_lang": parent_lang,
        "item": item,
        "sub_item": sub_item,
        "validation_type": validation_type,
        "response": "OK" if is_valid else error_level,
        "expected_value": expected,
        "got_value": obtained,
        "message": f"Got {obtained}, expected {expected}",
        "advice": None if is_valid else advice,
        "data": data,
    }


def get_doi_information(doi):
    url = f"https://api.crossref.org/works/{doi}"
    response = fetch_data(url=url, json=True)
    item = response['message']

    result = {}

    # Extrair títulos e detectar idioma
    titles = item.get('title', [])
    original_titles = item.get('original-title', [])
    all_titles = titles + original_titles

    for title in all_titles:
        try:
            lang = detect(title)  # Detecta o idioma do título
        except:
            lang = 'unknown'
        result[lang] = {
            'title': title,
            'doi': doi
        }

    # Adicionar autores ao resultado
    result['authors'] = [
        f"{author['family']}, {author['given']}"
        for author in item.get('author', [])
    ]

    return result
