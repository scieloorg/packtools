import urllib.parse
import re

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
    if validation_type == "value in list" and "one of " not in expected:
        expected = f"one of {expected}"
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
        "expected_value": obtained if is_valid else expected,
        "got_value": obtained,
        "message": f"Got {obtained}, expected {expected}",
        "advice": None if is_valid else advice,
        "data": data,
    }


def build_response(
    title,
    parent,
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
    if validation_type == "value in list" and "one of " not in expected:
        expected = f"one of {expected}"
    return {
        "title": title,
        "parent": parent.get("parent"),
        "parent_id": parent.get("parent_id"),
        "parent_article_type": parent.get("parent_article_type"),
        "parent_lang": parent.get("parent_lang"),
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
    try:
        response = fetch_data(url=url, json=True)
    except Exception as e:
        return {"doi": doi, "exception_msg": str(e), "exception_type": str(type(e))}

    item = response["message"]

    result = {}

    # Extrair títulos e detectar idioma
    titles = item.get("title") or []
    original_titles = item.get("original-title") or []
    all_titles = titles + original_titles

    for title in all_titles:
        try:
            lang = detect(title)  # Detecta o idioma do título
        except:
            lang = "unknown"
        result[lang] = {"title": title, "doi": doi}

    # Adicionar autores ao resultado
    result["authors"] = []
    for item in item.get("author") or []:
        try:
            result["authors"].append(
                f"{item['family']}, {item['given']}"
            )
        except KeyError:
            pass
    
    return result


def is_valid_url_format(text):
    """Checks if a given text string resembles a URL pattern using urllib.parse."""
    try:
        parsed_url = urllib.parse.urlparse(text)
        return bool(parsed_url.scheme) and bool(parsed_url.netloc)
    except ValueError:
        return False


def validate_doi_format(doi):
    """
    Valida o formato de um DOI (Digital Object Identifier)

    Regras de validação:
    1. Deve começar com "10."
    2. Após o "10.", deve ter 4 ou 5 dígitos
    3. Deve ter uma barra (/) após os dígitos
    4. Deve ter caracteres alfanuméricos após a barra
    5. Pode conter hífens e pontos após a barra
    6. Não deve conter espaços

    Args:
        doi (str): O DOI a ser validado

    Returns:
        Dict[str, Union[bool, str]]: Dicionário contendo status de validação e mensagem
    """
    # Verifica se o input é uma string e não está vazio
    if not isinstance(doi, str) or not doi:
        return {"valido": False, "mensagem": "DOI deve ser uma string não vazia"}

    # Remove possíveis espaços em branco
    doi = doi.strip()

    # Regex para validar o formato do DOI
    doi_regex = r"^10\.\d{4,5}\/[a-zA-Z0-9./-]+$"

    # Testa o formato básico
    if not re.match(doi_regex, doi):
        return {
            "valido": False,
            "mensagem": "Formato de DOI inválido. Deve seguir o padrão: 10.XXXX/string-alfanumérica",
        }

    # Verifica se não há caracteres especiais inválidos após a barra
    sufixo = doi.split("/")[1]
    if not re.match(r"^[a-zA-Z0-9./-]+$", sufixo):
        return {
            "valido": False,
            "mensagem": "O sufixo do DOI contém caracteres inválidos",
        }

    return {"valido": True, "mensagem": "DOI válido"}
