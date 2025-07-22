import re

ARTICLE_TYPE_MAP = {
    "research-article": "oa",
    "editorial": "ed",
    "abstract": "ab",
    "announcement": "an",
    "article-commentary": "co",
    "case-report": "cr",
    "letter": "le",
    "review-article": "ra",
    "rapid-communication": "sc",
    "addendum": "addendum",
    "book-review": "rc",
    "books-received": "books-received",
    "brief-report": "rn",
    "calendar": "calendar",
    "clinical-trial": "oa",
    "collection": "zz",
    "correction": "er",
    "discussion": "discussion",
    "dissertation": "dissertation",
    "editorial-material": "ed",
    "in-brief": "pr",
    "introduction": "ed",
    "meeting-report": "meeting-report",
    "news": "news",
    "obituary": "obituary",
    "oration": "oration",
    "partial-retraction": "partial-retraction",
    "product-review": "product-review",
    "reply": "reply",
    "reprint": "reprint",
    "retraction": "re",
    "translation": "translation",
    "technical-report": "oa",
    "other": "zz",
    "guideline": "guideline",
    "interview": "in",
    "data-article": "data-article",
}


def simple_field(key, value):
    if value:
        return {key: [{"_": value}]}
    return {}


def complex_field(key, value):
    if value:
        return {key: [value]}
    return {}


def multiple_complex_field(key, value_list):
    if value_list:
        return {key: value_list}
    return {}


def format_date(date_dict, fields, sep=""):
    """
    Concatena campos de uma data (como 'year', 'month', 'day') em uma string compacta.
    Retorna None se o dicionário for None ou se todos os campos estiverem ausentes.
    """
    if not date_dict:
        return None
    parts = [date_dict.get(field, "") for field in fields]
    return sep.join(parts) if any(parts) else None


def generate_am_dict(fields):
    response = {}
    for tag, value, formatter in fields:
        if value is not None:
            response.update(formatter(tag, value))
    return response

def simple_kv(tag, value):
    return {tag: value}

def format_page_range(fpage, lpage):
    if fpage and not lpage:
        return fpage
    if lpage and not fpage:
        return lpage
    if fpage == lpage:
        return fpage
    return f"{fpage}-{lpage}"


def abbreviate_page_range(first, last):
    """
    Abrevia a última página removendo o primeiro dígito comum com a primeira página,
    apenas se ambos tiverem o mesmo número de dígitos.
    """
    if not first or not last:
        return first, last

    if not first.isdigit() or not last.isdigit():
        return first, last

    if first == last:
        return first, last

    if len(first) != len(last):
        return first, last

    for i in range(len(first)):
        if first[i] != last[i]:
            return first, last[i:]

    return first, last
