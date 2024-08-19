import urllib.parse
from langdetect import detect
import xml.etree.ElementTree as ET

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


def is_valid_url_format(text):
    """Checks if a given text string resembles a URL pattern using urllib.parse."""
    try:
        parsed_url = urllib.parse.urlparse(text)
        return bool(parsed_url.scheme) and bool(parsed_url.netloc)
    except ValueError:
        return False


def extract_urls_from_node(xml_node):
    """
    Extracts all URLs from the given XML node and its descendants.

    This function searches for any attributes with the `xlink:href` namespace
    in the provided XML node and its children. It returns a dictionary where
    the keys are the tag names and the values are lists of URLs associated
    with each tag.

    Parameters:
    -----------
    xml_node : xml.etree.ElementTree.Element
        The XML node from which URLs are to be extracted.

    Returns:
    --------
    dict
        A dictionary where each key is the name of a tag containing a URL,
        and each value is a list of URLs found within that tag.
        Example:
        {
            'ext-link': ['https://example.com', 'https://another-example.com'],
            'graphic': ['https://images.example.com/image1.jpg']
        }

    Example:
    --------
    xml_data = '''
    <article xmlns:xlink="http://www.w3.org/1999/xlink">
        <ext-link xlink:href="https://example.com"/>
        <sec>
            <ext-link xlink:href="https://another-example.com"/>
            <graphic xlink:href="https://images.example.com/image1.jpg"/>
        </sec>
    </article>
    '''

    xml_tree = etree.fromstring(xml_data)
    links_dict = extract_urls_from_node(xml_tree)
    print(links_dict)
    # Output:
    # {
    #     'ext-link': ['https://example.com', 'https://another-example.com'],
    #     'graphic': ['https://images.example.com/image1.jpg']
    # }
    """
    links_dict = {}

    # Verifica se o nó atual tem o atributo xlink:href considerando o namespace
    xlink_href = xml_node.get('{http://www.w3.org/1999/xlink}href')
    if xlink_href:
        tag = xml_node.tag
        links_dict.setdefault(tag, [])
        links_dict[tag].append(xlink_href)

    # Recursivamente aplica o mesmo processo aos filhos do nó atual
    for child in xml_node:
        child_links = extract_urls_from_node(child)
        for tag, urls in child_links.items():
            links_dict.setdefault(tag, [])
            links_dict[tag].extend(urls)

    return links_dict


