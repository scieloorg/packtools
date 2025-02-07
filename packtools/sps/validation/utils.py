import urllib.parse
import re

import requests
from langdetect import detect
from packtools.sps.libs.requester import fetch_data
from packtools.sps.validation.similarity_utils import most_similar, similarity, how_similar


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
    element_name=None,
    sub_element_name=None,
    attribute_name=None,
    xml=None,
):
    if validation_type == "value in list" and "one of " not in expected:
        expected = f"one of {expected}"
    
    advice = format_advice(
        title,
        validation_type,
        is_valid,
        expected,
        obtained,
        advice,
        data,
        element_name,
        sub_element_name,
        attribute_name,
        xml,
        item,
        sub_item,
    )
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
    element_name=None,
    sub_element_name=None,
    attribute_name=None,
    xml=None,
):
    if validation_type == "value in list" and "one of " not in expected:
        expected = f"one of {expected}"

    if not attribute_name:
        if sub_item and '@' == sub_item[0]:
            attribute_name = sub_item[1:]
    if not element_name:
        element_name = item

    advice = format_advice(
        title,
        validation_type,
        is_valid,
        expected,
        obtained,
        advice,
        data,
        element_name,
        sub_element_name,
        attribute_name,
        xml,
        item,
        sub_item
    )
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
        return fetch_data(url=url, json=True)
    except Exception as e:
        return {"exception_msg": str(e), "exception_type": str(type(e))}


def handle_doi_response(item):
    result = {}

    # Extrair títulos e detectar idioma
    result["titles"] = item.get("title") or []
    result["original_titles"] = item.get("original-title") or []
    result["all_titles"] = result["titles"] + result["original_titles"]

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


def check_doi_is_registered(article_data):
    doi = article_data["value"]
    response = get_doi_information(doi)
    try:
        message = response["message"]
    except KeyError:
        response["doi"] = doi
        return response
    else:
        registered = handle_doi_response(message)
        title_similarity, most_similar_titles = most_similar(
            similarity(registered["all_titles"], article_data["article_title"])
        )
        authors_similarity = how_similar(str(registered["authors"]), str(article_data["authors"]))
        return {
            "doi": doi,
            "valid": ((title_similarity + authors_similarity) / 2) > 0.9
            "registered": registered,
        }


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


def format_advice(
    title,
    validation_type,
    is_valid,
    expected,
    obtained,
    advice,
    data,
    element_name,
    sub_element_name,
    attribute_name,
    xml,
    item,
    sub_item,
):
    if is_valid:
        return ''

    # if not attribute_name:
    #     if sub_item:
    #         if '@' == sub_item[0]:
    #             attribute_name = sub_item[1:]
    #         else:
    #             sub_element_name = sub_item
    # if not element_name:
    #     element_name = item

    if element_name or sub_element_name or attribute_name or xml:
        if validation_type == "value in list" and "one of " not in expected:
            expected = f"one of {expected}"

        if validation_type == "exist":
            marked = ""
            verb = "Mark"
            if attribute_name:
                verb = "Add "
                marked = f' {attribute_name}="VALUE"'
            if sub_element_name:
                marked = f"<{sub_element_name}{marked}>"
            if element_name:
                marked = f"<{element_name}{marked}>"
            advice = f"{verb} {title} with {marked}"

        elif validation_type == "value in list":

            if obtained:
                incorrect = ""
                if attribute_name:
                    incorrect = f' {attribute_name}="{obtained}"'
                if sub_element_name:
                    incorrect = f"<{sub_element_name}{incorrect}>"
                if element_name:
                    incorrect = f"<{element_name}{incorrect}>"
                advice = f"Replace {obtained} in {incorrect} with {expected}"
            else:
                incomplete = ""
                if attribute_name:
                    attribute = f' {attribute_name}="VALUE"'
                if sub_element_name:
                    incomplete = f"<{sub_element_name}{incomplete}>"
                if element_name:
                    incomplete = f"<{element_name}{incomplete}>"
                advice = f"Add {attribute} in {incomplete} and replace VALUE with {expected}"

    return advice
    